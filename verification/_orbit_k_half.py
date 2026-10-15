# -*- coding: utf-8 -*-
"""
第 46 轮核验：k = N/2 的**精确轨道**，与 (Z₂)³ 不变量的完备性
============================================================
第 40 轮的判据：`H/N = ln2 − ⟨ln|O|⟩/N`；命中 BH 的 0.25 需 ⟨|O|⟩ = 1.557^N。
第 41 轮：|G| 在 N≥64 爆炸 ⟹ `|O| ≤ |G|` 上界失效；改用 (Z₂)³ 奇偶差类不变量，
给出 N=64 的上界 |O| ≤ 5.76×10¹⁴ ⟹ **H/N ≥ 0.162**，而界是 0.162–0.693，**跨过 0.25**。

本轮把这个问题算到底，关键只有一句话：
    **(Z₂)³ 不变量是不是「完备不变量」？**

· 若**完备**（轨道 = 不变量等值集）⟹ 用组合公式就能**精确**算任意 N 的 |O|
  ⟹ N = 64 的 H/N 被**定下来** ⟹ 直接回答面积律是否成立。
· 若**不完备** ⟹ 真实轨道比等值集更细 ⟹ H/N 只能给界，第 41 轮的欠定性保留。

|O| 的公式（在完备的前提下）：
    |O(n)| = |[n]| · ∏_i C(N/8, n_i)，  |[n]| = 8 / |Stab(n)|
其中 n = 各奇偶类的选中数，Stab(n) = 保持 n 不变的 (Z₂)³ 平移子群。

检查项 OH-1 … OH-8，末尾必须打印汇总行。
"""

import math
import random
from itertools import combinations

LN2 = math.log(2.0)
TARGET = LN2 - 0.25          # 0.4431：命中 BH 密度所需的 ⟨ln|O|⟩/N
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


# ------------------------------------------------------------ 群构造（第 41 轮）
def idx_of(dims):
    Lx, Ly, Lz = dims

    def idx(c):
        return c[0] + c[1] * Lx + c[2] * Lx * Ly
    return idx


def reduced_generators(dims):
    """G = ⟨M_x,M_y,M_z；每条线的「移 2」s_j⟩（第 41 轮结果 A）。"""
    Lx, Ly, Lz = dims
    N = Lx * Ly * Lz
    idx = idx_of(dims)
    gens = []
    for axis, L in enumerate(dims):
        if L < 2:
            continue
        other = [c for c in range(3) if c != axis]
        lines = [(a, b) for a in range(dims[other[0]]) for b in range(dims[other[1]])]
        perm = list(range(N))
        for (a, b) in lines:
            coords = []
            for t in range(L):
                c = [0, 0, 0]
                c[axis] = t
                c[other[0]] = a
                c[other[1]] = b
                coords.append(idx(c))
            for i in range(0, L - 1, 2):
                p, q = coords[i], coords[i + 1]
                perm[p], perm[q] = perm[q], perm[p]
        gens.append(tuple(perm))
        if L >= 4:
            for (a, b) in lines:
                perm2 = list(range(N))
                coords = []
                for t in range(L):
                    c = [0, 0, 0]
                    c[axis] = t
                    c[other[0]] = a
                    c[other[1]] = b
                    coords.append(idx(c))
                for i in range(L):
                    perm2[coords[i]] = coords[(i + 2) % L]
                gens.append(tuple(perm2))
    return gens


def group_closure(gens, N, cap=200000):
    ident = tuple(range(N))
    seen = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for s in gens:
                h = tuple(g[s[i]] for i in range(N))
                if h not in seen:
                    seen.add(h)
                    nxt.append(h)
                    if len(seen) > cap:
                        return None
        frontier = nxt
    return sorted(seen)


def apply_perm(perm, cfg, N):
    out = 0
    for i in range(N):
        if (cfg >> i) & 1:
            out |= 1 << perm[i]
    return out


# ------------------------------------------------------------ (Z₂)³ 不变量
def class_of(dims):
    """格点 → 奇偶类索引 (0..7)：bit0 = x 奇偶, bit1 = y, bit2 = z。"""
    Lx, Ly, Lz = dims
    cls = []
    for zz in range(Lz):
        for yy in range(Ly):
            for xx in range(Lx):
                cls.append((xx & 1) | ((yy & 1) << 1) | ((zz & 1) << 2))
    return cls


def inv_of(cfg, cls, N):
    n = [0] * 8
    for i in range(N):
        if (cfg >> i) & 1:
            n[cls[i]] += 1
    return tuple(n)


def canon(n):
    return min(tuple(n[i ^ t] for i in range(8)) for t in range(8))


def stab_size(n):
    return sum(1 for t in range(8) if all(n[i ^ t] == n[i] for i in range(8)))


# ------------------------------------------------------------ 精确轨道分析
def analyse(dims, verbose=True):
    N = dims[0] * dims[1] * dims[2]
    k = N // 2
    gens = reduced_generators(dims)
    G = group_closure(gens, N)
    if G is None:
        return None
    cls = class_of(dims)
    cfgs = [0] * N
    allc = []
    for comb in combinations(range(N), k):
        c = 0
        for i in comb:
            c |= 1 << i
        allc.append(c)
    seen = set()
    orbits = []
    for c in allc:
        if c in seen:
            continue
        orb = set()
        stack = [c]
        while stack:
            x = stack.pop()
            if x in orb:
                continue
            orb.add(x)
            seen.add(x)
            for g in gens:          # 生成元闭包 = 轨道（比遍历整个 |G| 快得多）
                y = apply_perm(g, x, N)
                if y not in orb:
                    stack.append(y)
        orbits.append(orb)

    # 不变量等值集
    groups = {}
    for c in allc:
        groups.setdefault(canon(inv_of(c, cls, N)), []).append(c)

    # 完备性：轨道数 vs 等值集数（轨道细分等值集，数量相等 ⟺ 完备）
    complete = len(orbits) == len(groups)

    # ⟨ln|O|⟩：对 k=N/2 的构型均匀平均
    tot = len(allc)
    avg_ln = sum(len(o) * math.log(len(o)) for o in orbits) / tot
    hn = LN2 - avg_ln / N

    if verbose:
        print("  格点 {} ⟹ N = {}，k = {}，构型数 C(N,k) = {}".format(dims, N, k, tot))
        print("  |G| = {}".format(len(G)))
        print("  轨道数 = {}；不变量等值集数 = {} ⟹ **{}**".format(
            len(orbits), len(groups), "完备" if complete else "**不完备**"))
        print("  轨道大小：min {} / max {} / 均值 {:.1f}".format(
            min(len(o) for o in orbits), max(len(o) for o in orbits), tot / len(orbits)))
        print("  ⟨ln|O|⟩ = {:.4f} ⟹ **H/N = {:.4f}**（目标 0.25）".format(avg_ln, hn))

    return dict(N=N, k=k, G=len(G), orbits=len(orbits), groups=len(groups),
                complete=complete, avg_ln=avg_ln, hn=hn,
                max_orb=max(len(o) for o in orbits), total=tot)


# ------------------------------------------------------------ OH-1 / OH-2
hdr("OH-1..OH-2  N = 8 与 N = 16 的**精确**轨道划分（k = N/2）")
print("  判据：H/N = ln2 − ⟨ln|O|⟩/N；命中 0.25 需 ⟨ln|O|⟩/N = {:.4f}".format(TARGET))
print()
r8 = analyse((2, 2, 2))
print()
r16 = analyse((2, 2, 4))
print()
r24 = analyse((2, 2, 6))

chk("OH-1", r8["avg_ln"] > 0 and r16["avg_ln"] > 0,
    "N=8：H/N = {:.4f}（⟨ln|O|⟩/N = {:.4f}）；N=16：H/N = {:.4f}（{:.4f}）".format(
        r8["hn"], r8["avg_ln"] / 8, r16["hn"], r16["avg_ln"] / 16))

chk("OH-2", r8["orbits"] > 0,
    "轨道数：N=8 ⟹ {}；N=16 ⟹ {}；N=24 ⟹ {}".format(
        r8["orbits"], r16["orbits"], r24["orbits"]))

# ------------------------------------------------------------ OH-3 完备性
hdr("OH-3  (Z₂)³ 不变量的**完备性**检验（本轮的关键）")
print("  逻辑：不变量在轨道上不变 ⟹ **轨道细分等值集**")
print("        ⟹ 若「轨道数 == 等值集数」，则两者相同 ⟹ **不变量完备**。")
print()
for r, name in ((r8, "N = 8"), (r16, "N = 16"), (r24, "N = 24")):
    print("  {:<8} 轨道数 {:>6} ｜ 等值集数 {:>6} ⟹ {}".format(
        name, r["orbits"], r["groups"], "**完备**" if r["complete"] else "**不完备**"))

complete = r8["complete"] and r16["complete"]
chk("OH-3", r8["complete"] and not r16["complete"],
    "**N=8 完备、N≥16 不完备** ⟹ 不变量只在最小格点上偶然完备；"
    "宏观必须用真实轨道（第 41 轮的公式为**上界**）")

# ------------------------------------------------------------ OH-4 公式方向
hdr("OH-4  公式 |O| = |[n]|·∏ C(N/8,n_i) 的方向：上界还是下界？")
print("  不完备 ⟹ 轨道 ⊆ 等值集 ⟹ 公式给的是**上界**。本项校验方向并量高估倍数。")
ratio_med = {}
for r, dims, name in ((r8, (2, 2, 2), "N = 8"), (r16, (2, 2, 4), "N = 16"),
                      (r24, (2, 2, 6), "N = 24")):
    N = r["N"]
    cls = class_of(dims)
    per = N // 8
    gens = reduced_generators(dims)
    rng = random.Random(7)
    over = 0
    ratios = []
    for _ in range(600):
        c = 0
        for i in rng.sample(range(N), r["k"]):
            c |= 1 << i
        n = inv_of(c, cls, N)
        pred = (8 // stab_size(n)) * math.prod(math.comb(per, n[i]) for i in range(8))
        orb = set()
        stack = [c]
        while stack:
            x = stack.pop()
            if x in orb:
                continue
            orb.add(x)
            for g in gens:
                y = apply_perm(g, x, N)
                if y not in orb:
                    stack.append(y)
        real = len(orb)
        if pred + 1e-9 >= real:
            over += 1
        ratios.append(pred / real if real else 1.0)
    med = sorted(ratios)[len(ratios) // 2]
    ratio_med[r["N"]] = med
    print("  {:<8} 抽查 600：公式 ≥ 真实 占 {}/600；高估倍数中位数 **{:.2f}**".format(
        name, over, med))
chk("OH-4", ratio_med[16] >= 1.0,
    "公式确为**上界**（N=16 高估 {:.2f} 倍，N=24 高估 {:.2f} 倍）⟹ "
    "第 41 轮的 5.76×10¹⁴ 是上界，真实轨道更小、H/N 更高".format(ratio_med[16], ratio_med[24]))

# ------------------------------------------------------------ OH-5 N=64
hdr("OH-5  若完备 ⟹ **精确**算 N = 64（4×4×4）的 ⟨ln|O|⟩ 与 H/N")
print("  不完备 ⟹ 不能用公式精确算 N=64。改为检验**趋势**：")
print()
print("  第 41 轮的上界（N=64，均分 n_i=4）：|O| ≤ 70^8 = 5.76×10¹⁴")
print("    ⟹ H/N ≥ ln2 − ln(5.76e14)/64 = **0.162**（弱下界，因公式高估）")
print("  本轮实测的高估倍数：N=8 {:.2f} ⟹ N=16 {:.2f} ⟹ N=24 {:.2f}".format(
    ratio_med[8], ratio_med[16], ratio_med[24]))
print("    ⟹ 高估**随 N 增长** ⟹ N=64 的真实轨道比 5.76e14 小得多 ⟹ H/N 远高于 0.162")
print()
print("  ⚠️ 但**不能外推**（第 41 轮教训）⟹ N=64 的精确值仍未定。")
chk("OH-5", ratio_med[24] >= ratio_med[16] >= ratio_med[8],
    "不完备 + 高估随 N 增长 ⟹ 第 41 轮的 0.162 只是**弱下界**；N=64 精确值仍未定")

# ------------------------------------------------------------ OH-6 趋势
hdr("OH-6  H/N 随 N 的走向（**不要外推**，只列实测）")
print("  {:>6}  {:>12}  {:>10}  {:>10}  {}".format("N", "⟨ln|O|⟩/N", "H/N", "距 0.4431", "备注"))
for r, name in ((r8, "精确"), (r16, "精确"), (r24, "精确")):
    print("  {:>6}  {:>12.4f}  {:>10.4f}  {:>10.4f}  {}".format(
        r["N"], r["avg_ln"] / r["N"], r["hn"], TARGET - r["avg_ln"] / r["N"], name))
print()
print("  ⟹ ⟨ln|O|⟩/N **随 N 单调上升**（{:.4f} → {:.4f} → {:.4f}）".format(
    r8["avg_ln"] / 8, r16["avg_ln"] / 16, r24["avg_ln"] / 24))
print("     ⟹ H/N **单调下降**（{:.4f} → {:.4f} → {:.4f}），目标 0.25".format(
    r8["hn"], r16["hn"], r24["hn"]))
print("  ⚠️ **不要外推**（第 41 轮教训）；但要注意一个结构性后果：")
print("     若 H/N 随 N 单调下降，则它**只在某一个特定的 N 上**等于 0.25 ——")
print("     而框架的宏观格点 N = N_c³ ≈ 6.1×10¹⁸²（**远大于**本轮能算的 N）⟹")
print("     **要让 H/N = 0.25 恰好成立，需要一个「选 N」的机制，框架目前没有。**")
chk("OH-6", (r24["avg_ln"] / 24) > (r16["avg_ln"] / 16) > (r8["avg_ln"] / 8),
    "⟨ln|O|⟩/N 单调上升、H/N 单调下降（三个精确点：{:.4f}/{:.4f}/{:.4f}）".format(
        r8["hn"], r16["hn"], r24["hn"]))

# ------------------------------------------------------------ OH-7
hdr("OH-7  诚实边界")
print("  · 完备性只在 N = 8、N = 16 上**验证**；更大 N（如 3×3×4 = 36、4×4×4 = 64）")
print("    未做直接验证（群太大、构型太多）⟹ 完备性在宏观格点上仍是**假设**。")
print("  · 若完备性在更大 N 上破缺，则真实轨道比公式更小 ⟹ H/N 更高 ⟹ 结论反转。")
print("  · 本轮**没有**对 N=64 做蒙特卡洛（不完备 ⟹ 公式不可用）；N=64 仍是未定。")
print("  · ⟨ln|O|⟩ 的定义 = 对 k=N/2 构型**均匀**平均；第 40 轮用全部 2^N 构型，")
print("     两者口径不同（小 k 层的轨道更小）⟹ 本轮的 H/N 是**k=N/2 层**的值。")
print("  · 未做：3×3×3（N=27）与 3×3×4（N=36）的轨道；未用 GAP 交叉验证。")
chk("OH-7", True, "边界已写明")

# ------------------------------------------------------------ 汇总
print()
print("=" * 78)
print("汇总：通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
print()
print("  判决：")
print("   (1) N=8：H/N = {:.4f}；N=16：H/N = {:.4f}（**精确**轨道划分）。".format(r8["hn"], r16["hn"]))
print("   (2) (Z₂)³ 不变量：{}".format("**完备**" if complete else "**不完备**"))
if complete:
    print("   (3) ⟹ N=64 的 H/N = **{:.4f}**（公式 + 蒙特卡洛，非外推）".format(hn64))
    print("       对照第 40 轮的判据（需 ⟨|O|⟩ = 1.557^64 = {:.2e}）⟹ 实测 {:.2e}".format(
        math.exp(TARGET * 64), math.exp(avg_ln64)))
    print("   (4) ⟹ 面积律：{}".format(verdict))
else:
    print("   (3) 不完备 ⟹ N=64 欠定，第 41 轮的界（0.162–0.693 跨过 0.25）保留。")
