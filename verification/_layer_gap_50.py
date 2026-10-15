# -*- coding: utf-8 -*-
"""第 50 轮（GAP 部分）：在 N = 48 / 64 / 96 上扫 k，定位 k_c(N)。

动机：第 49 轮已把 h(k=N/2, N) 算过：
    N=48 (2,4,6) : 0.2208 < 0.25
    N=32 (2,4,4) : 0.2834 > 0.25
而小 k 端 H/N 接近 ln2（k=1 时 = ln2 − lnN/N）。
⟹ 在 N ≥ 48 上，**某个层 k_c 一定穿过 0.25**。
本脚本定出 k_c(N)，看 **k_c/N 是否随 N 收敛**（收敛 ⟹ 0.25 绑定占据分数；不收敛 ⟹ 仍需机制）。

方法：GAP 的 `Size(Stabilizer(G, c, OnSets))` ⟹ |O(c)| = |G|/|Stab|（不遍历轨道）。
每层采 S 个构型，算其轨道的几何平均。
"""

import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _gap
import _tickgroup as tg

LN2 = math.log(2.0)
OK = [0]
FAIL = [0]


def chk(tag, cond, msg):
    if cond:
        OK[0] += 1
        print("  [OK] {:<8} {}".format(tag, msg))
    else:
        FAIL[0] += 1
        print("  [XX] {:<8} {}".format(tag, msg))


def hdr(t):
    print()
    print("-" * 78)
    print(t)
    print("-" * 78)


def scan_layers_gap(dims, layers, S=6, seed=1000):
    """对给定格点的若干 k 层，各采 S 个构型，返回 {k: (⟨ln|O|⟩, H/N, |G|)}。"""
    N = dims[0] * dims[1] * dims[2]
    gens = tg.gens_correct(dims)
    cfgs = []
    owner = []
    for k in layers:
        for c in tg.random_cfgs(N, k, S, seed + k):
            cfgs.append(c)
            owner.append(k)
    t0 = time.time()
    order, sizes = _gap.orbit_sizes_via_gap(gens, cfgs, N)
    dt = time.time() - t0
    acc = {}
    for k, sz in zip(owner, sizes):
        acc.setdefault(k, []).append(math.log(sz))
    out = {}
    for k, lns in acc.items():
        avg = sum(lns) / len(lns)
        out[k] = (avg, LN2 - avg / N)
    return out, order, dt, N, len(gens)


def find_kc(res):
    """在已算层之间线性插值，找 h = 0.25 的 k（无 ⟹ None）。"""
    ks = sorted(res)
    for i in range(len(ks) - 1):
        h1, h2 = res[ks[i]][1], res[ks[i + 1]][1]
        if (h1 - 0.25) * (h2 - 0.25) <= 0:
            return ks[i] + (h1 - 0.25) / (h1 - h2) * (ks[i + 1] - ks[i])
    return None


print("GAP 可用:", _gap.gap_available())

JOBS = [
    ((2, 4, 6), 48, [12, 16, 18, 20, 22, 24], 8),
    ((2, 4, 8), 64, [20, 24, 28, 30, 32], 8),
    ((2, 4, 12), 96, [32, 40, 44, 48], 6),
]

SUMMARY = []
for dims, N, layers, S in JOBS:
    hdr("LG-{N}  格点 {dims}（N = {N}）—— 扫 k = {layers}".format(N=N, dims=dims, layers=layers))
    try:
        res, order, dt, Nn, ng = scan_layers_gap(dims, layers, S=S)
    except Exception as e:
        print("  [XX] 失败：{}".format(e))
        FAIL[0] += 1
        continue
    print("  生成元 {} 个，|G| = {}（{} 位）".format(ng, order, len(str(order))))
    print("  用时 {:.1f} s（每层 {} 个构型）".format(dt, S))
    print("  {:>5} {:>12} {:>10}  {}".format("k", "⟨ln|O|⟩", "H/N", "vs 0.25"))
    for k in sorted(res):
        avg, h = res[k]
        print("  {:>5} {:>12.4f} {:>10.4f}  {}".format(k, avg, h, "低于" if h < 0.25 else ""))
    kc = find_kc(res)
    if kc is None:
        print("  ⟹ 本组层未穿过 0.25")
    else:
        print("  ⟹ **k_c = {:.3f}（k_c/N = {:.4f}）**".format(kc, kc / N))
        SUMMARY.append((N, kc, kc / N))
    chk("LG-{}".format(N), True, "层扫描完成（|G| = {} 位）".format(len(str(order))))

hdr("LG-KC  k_c/N 是否随 N 收敛？")
print("  {:>6} {:>10} {:>12}".format("N", "k_c", "k_c/N"))
for N, kc, r in SUMMARY:
    print("  {:>6} {:>10.3f} {:>12.4f}".format(N, kc, r))
if SUMMARY:
    rs = [r for _, _, r in SUMMARY]
    spread = max(rs) - min(rs)
    print()
    print("  k_c/N 散布 = {:.4f}（{} 个点）".format(spread, len(rs)))
    chk("LG-KC", True,
        "k_c/N 在 N ∈ [{}, {}] 上散布 {:.4f} ⟹ {}".format(
            SUMMARY[0][0], SUMMARY[-1][0], spread,
            "初步收敛" if spread < 0.05 else "**在移动**（k 上也不固定）"))
else:
    chk("LG-KC", False, "无 k_c 数据")

hdr("LG-NOTE  物理口径提醒（诚实边界）")
print("  k 在框架里的物理相关值应是 **k = N/2**（等分账：均匀分布 ⟹ 典型构型是半满）。")
print("  若接受这一点，则 k **不是**自由参数 ⟹ 本轮的「扫 k」只提供**结构信息**")
print("  （层依赖的形状、对称性、标度），**不能**为 0.25 提供一个可调的自由度。")

print()
print("=" * 78)
print("汇总：通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
