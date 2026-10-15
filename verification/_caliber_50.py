# -*- coding: utf-8 -*-
"""第 50 轮：口径审查 —— 「构型等权」vs「轨道等权」两种 H/N 的差。

## 背景

第 40 轮的权威定义（`_observer_resolution.py::part_entropy`）：

    H = ln M − Σ_o (|O_o|/M)·ln|O_o|        （M = 该层构型数）

即**对构型等权**（等分账下均匀分布在所有构型上，所以典型构型的权重是 |O|/M）。
写成 H/N 形式：H/N ≈ ln2 − ⟨ln|O|⟩_cfg/N。

而第 46 / 48 轮的 Python 全层脚本用的是：

    avg = Σ_o ln|O_o| / (#轨道)             ⟹ ⟨ln|O|⟩_orb

即**对轨道等权** —— **偏离第 40 轮的定义**。

本脚本对三层格点**同时**算两种口径，量化差：
- 若差 ≈ 0 ⟹ 旧值不受影响；
- 若差不可忽略 ⟹ 受影响的旧值必须更正。

⚠️ 注意：第 48/49 轮的 **GAP 结果不受影响** —— 它们是「随机抽构型 → 算各自 |O| → 平均 ln|O|」，
   这**正是构型等权**。第 46 轮若也是按构型采样，则同样不受影响。
"""

import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tickgroup as tg

LN2 = math.log(2.0)
CH = 8


def hdr(t):
    print()
    print("-" * 78)
    print(t)
    print("-" * 78)


def make_apply(N, gens):
    nch = (N + CH - 1) // CH
    tables = []
    for g in gens:
        tb = []
        for c in range(nch):
            shift = c * CH
            t = [0] * (1 << CH)
            for v in range(1 << CH):
                acc = 0
                for b in range(CH):
                    if (v >> b) & 1:
                        i = shift + b
                        if i < N:
                            acc |= 1 << g[i]
                t[v] = acc
            tb.append(t)
        tables.append(tb)
    masks = [(1 << CH) - 1] * nch

    def apply(cfg, gi):
        tb = tables[gi]
        acc = 0
        x = cfg
        for c in range(nch):
            acc |= tb[c][x & masks[c]]
            x >>= CH
        return acc
    return apply


def scan_both(dims):
    """全层划分，同时统计两种口径。

    返回 {k: dict(orb=, cfg=, n_orb=, n_cfg=, h_cfg=, h_orb=) }
    """
    N = dims[0] * dims[1] * dims[2]
    gens = tg.gens_correct(dims)
    apply = make_apply(N, gens)
    ng = len(gens)
    visited = bytearray(1 << N)
    s_cfg = [0.0] * (N + 1)      # Σ |O|·ln|O|
    s_orb = [0.0] * (N + 1)      # Σ ln|O|
    cnt = [0] * (N + 1)
    norb = [0] * (N + 1)
    t0 = time.time()
    for start in range(1 << N):
        if visited[start]:
            continue
        k = start.bit_count()
        stack = [start]
        visited[start] = 1
        size = 0
        while stack:
            x = stack.pop()
            size += 1
            for gi in range(ng):
                y = apply(x, gi)
                if not visited[y]:
                    visited[y] = 1
                    stack.append(y)
        ln = math.log(size)
        s_cfg[k] += ln * size
        s_orb[k] += ln
        cnt[k] += size
        norb[k] += 1
    out = {}
    for k in range(N + 1):
        if cnt[k] == 0:
            continue
        avg_cfg = s_cfg[k] / cnt[k]
        avg_orb = s_orb[k] / norb[k]
        out[k] = dict(n_orb=norb[k], n_cfg=cnt[k],
                      h_cfg=LN2 - avg_cfg / N,
                      h_orb=LN2 - avg_orb / N,
                      d=(LN2 - avg_cfg / N) - (LN2 - avg_orb / N))
    return out, time.time() - t0, N


print("口径：第 40 轮定义 H = ln M − Σ(|O|/M)ln|O| ⟹ **构型等权**（本脚本 h_cfg 列）")

SUMMARY = []
for dims in [(2, 2, 2), (2, 2, 4), (2, 2, 6)]:
    hdr("CAL-{}  格点 {} —— 两种口径逐层对照".format(dims[-1], dims))
    res, dt, N = scan_both(dims)
    print("  用时 {:.1f} s".format(dt))
    print("  {:>4} {:>9} {:>9} {:>10} {:>10} {:>11}  {}".format(
        "k", "轨道数", "构型数", "h_cfg", "h_orb", "h_cfg−h_orb", "口径差%"))
    for k in sorted(res):
        r = res[k]
        rel = 100.0 * r["d"] / r["h_cfg"] if r["h_cfg"] else 0.0
        print("  {:>4} {:>9} {:>9} {:>10.4f} {:>10.4f} {:>11.4f}  {:>6.2f}".format(
            k, r["n_orb"], r["n_cfg"], r["h_cfg"], r["h_orb"], r["d"], rel))
    kk = N // 2
    print()
    print("  k = N/2 = {}：h_cfg = {:.4f}   h_orb = {:.4f}   差 = {:+.4f}".format(
        kk, res[kk]["h_cfg"], res[kk]["h_orb"], res[kk]["d"]))
    SUMMARY.append((dims, N, res[kk]["h_cfg"], res[kk]["h_orb"], res[kk]["d"]))

hdr("CAL-SUMMARY  k = N/2 处的口径差")
print("  {:>12} {:>5} {:>10} {:>10} {:>10}".format("格点", "N", "h_cfg（正确）", "h_orb", "差"))
for dims, N, hc, ho, d in SUMMARY:
    print("  {:>12} {:>5} {:>10.4f} {:>10.4f} {:>10.4f}".format(str(dims), N, hc, ho, d))
print()
mx = max(abs(d) for _, _, _, _, d in SUMMARY)
print("  最大口径差 = {:.4f}（{:.1f}% 相对）".format(mx, 100.0 * mx / min(hc for _, _, hc, _, _ in SUMMARY)))
print()
print("  已知旧值对照（k = N/2）：")
OLD = [((2, 2, 2), 8, 0.4679, "第 46/48 轮"),
       ((2, 2, 4), 16, 0.4335, "第 46/48 轮"),
       ((2, 2, 6), 24, 0.4510, "第 48 轮 FR-1（轨道等权）"),
       ((2, 2, 6), 24, 0.4330, "第 46 轮（错误群）")]
for dims, N, v, src in OLD:
    cur = [r for r in SUMMARY if r[1] == N][0]
    tag = "与本轮 h_cfg 差 {:+.4f}".format(v - cur[2])
    print("  {:>12} N={:<4} 旧值 {:.4f}（{}）⟹ {}".format(str(dims), N, v, src, tag))

print()
print("  ⚠️ 未受影响：第 48/49 轮的 **GAP 结果**（随机构型采样 → 平均 ln|O| = 构型等权）。")
print("=" * 78)
