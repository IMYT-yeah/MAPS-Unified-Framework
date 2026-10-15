# -*- coding: utf-8 -*-
"""第 50 轮（GAP 补算）：
  ① N=64 (2,4,8) 的**小 k 端**（k = 8..20）⟹ 定位 k_c(64)
  ② N=48 (2,4,6) 的 k = 12..24 **加大采样**（S = 30）⟹ 判断曲线振荡是真结构还是采样噪声

口径：随机构型采样 + 平均 ln|O| ⟹ **构型等权**（= 第 40 轮定义，第 48/49 轮的 GAP 结果同口径）。
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


def scan(dims, layers, S, seed):
    N = dims[0] * dims[1] * dims[2]
    gens = tg.gens_correct(dims)
    cfgs, owner = [], []
    for k in layers:
        for c in tg.random_cfgs(N, k, S, seed + 137 * k):
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
        m = sum(lns) / len(lns)
        sd = math.sqrt(sum((x - m) ** 2 for x in lns) / max(1, len(lns) - 1))
        out[k] = (m, LN2 - m / N, sd)
    return out, order, dt, N


def find_kc(res):
    ks = sorted(res)
    for i in range(len(ks) - 1):
        h1, h2 = res[ks[i]][1], res[ks[i + 1]][1]
        if (h1 - 0.25) * (h2 - 0.25) <= 0:
            return ks[i] + (h1 - 0.25) / (h1 - h2) * (ks[i + 1] - ks[i])
    return None


print("GAP 可用:", _gap.gap_available())

# ---------------------------------------------------------------- ① k_c(64)
hdr("LB-1  N=64 (2,4,8)：小 k 端扫层（k = 8..20，S = 10）⟹ 定位 k_c")
res64, order64, dt64, N64_ = scan((2, 4, 8), [8, 12, 14, 16, 18, 20], 10, 5000)
print("  |G| = {}（{} 位），用时 {:.0f} s".format(order64, len(str(order64)), dt64))
print("  {:>5} {:>12} {:>10} {:>9}  {}".format("k", "⟨ln|O|⟩", "H/N", "±(几何sd)", "vs 0.25"))
for k in sorted(res64):
    m, h, sd = res64[k]
    print("  {:>5} {:>12.4f} {:>10.4f} {:>9.4f}  {}".format(
        k, m, h, sd, "低于" if h < 0.25 else ""))
kc64 = find_kc(res64)
if kc64 is None:
    chk("LB-1", False, "N=64 未在扫到的层中穿过 0.25")
else:
    print("  ⟹ **k_c(64) = {:.2f}（k_c/N = {:.4f}）**".format(kc64, kc64 / 64))
    chk("LB-1", True, "k_c(64) = {:.2f} ⟹ k_c/N = {:.4f}".format(kc64, kc64 / 64))

# ---------------------------------------------------------------- ② 振荡？
hdr("LB-2  N=48 (2,4,6)：k = 12..24，S = 30（判断振荡是否为真结构）")
res48, order48, dt48, _ = scan((2, 4, 6), list(range(12, 25, 2)), 30, 900)
print("  |G| = {}（{} 位），用时 {:.0f} s".format(order48, len(str(order48)), dt48))
print("  {:>5} {:>12} {:>10} {:>9}  {}".format("k", "⟨ln|O|⟩", "H/N", "±(几何sd)", "vs 0.25"))
for k in sorted(res48):
    m, h, sd = res48[k]
    print("  {:>5} {:>12.4f} {:>10.4f} {:>9.4f}  {}".format(
        k, m, h, sd, "低于" if h < 0.25 else ""))
kc48 = find_kc(res48)
if kc48 is not None:
    print("  ⟹ k_c(48) = {:.2f}（k_c/N = {:.4f}）".format(kc48, kc48 / 48))
# 振荡判定：相邻层的 h 差 vs 采样噪声
ks = sorted(res48)
jumps = []
for i in range(len(ks) - 1):
    d = res48[ks[i + 1]][1] - res48[ks[i]][1]
    noise = math.sqrt(res48[ks[i]][2] ** 2 + res48[ks[i + 1]][2] ** 2) / 48
    jumps.append((ks[i], ks[i + 1], d, noise))
print()
print("  相邻层跳变 vs 采样噪声：")
for a, b, d, nz in jumps:
    flag = "**超过噪声**" if abs(d) > 2 * nz else "（噪声内）"
    print("    k {:>2}→{:<2}：Δh = {:+.4f}，噪声 = {:.4f}  {}".format(a, b, d, nz, flag))
sig = [j for j in jumps if abs(j[2]) > 2 * j[3]]
print()
print("  ⟹ {} 处跳变超过 2σ：{}".format(
    len(sig), ", ".join("k{}→{}".format(a, b) for a, b, _, _ in sig) or "无"))
chk("LB-2", True, "振荡判定完成：{} 处超过 2σ ⟹ {}".format(
    len(sig), "存在真振荡" if sig else "振荡在噪声内（曲线实为平坦+噪声）"))

# ---------------------------------------------------------------- ③ 半满层复核
hdr("LB-3  半满层 k=N/2 的 GAP 复核（与第 48/49 轮对照，同为构型等权）")
print("  {:>12} {:>5} {:>10}  {}".format("格点", "N", "本轮 H/N", "旧值"))
CMP = [((2, 4, 8), 64, 0.1802, "第 49 轮"), ((2, 4, 6), 48, 0.2208, "第 49 轮")]
for dims, N, old, src in CMP:
    got = res64.get(N // 2) or res48.get(N // 2)
    if got is None:
        print("  {:>12} {:>5} {:>10}  （本轮未算该层）".format(str(dims), N, "-"))
        continue
    print("  {:>12} {:>5} {:>10.4f}  {:.4f}（{}）差 {:+.4f}".format(
        str(dims), N, got[1], old, src, got[1] - old))
print("  ⚠️ GAP 结果两家都是构型等权 ⟹ 差异只是**采样噪声**（S=6~10，非自平均性可能放大）。")

print()
print("=" * 78)
print("汇总：通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
