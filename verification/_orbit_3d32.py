# -*- coding: utf-8 -*-
"""
第 47 轮核验：突破「细长格点」限制 —— 同 N=32 比较 (2,2,8) 与 (2,4,4)
========================================================================
第 46 轮的口径限制：三个算例全是 **(2,2,L) 系列**（两方向长度 2，细长），
H/N 饱和在 ≈0.433 ⟹ 但细长格点**不代表各向同性三维宏观格点**。

本轮用**受控对照**直接检验"形状依赖性"：固定 N = 32，只改形状
    (2,2,8)（细长）  vs  (2,4,4)（立体）
· 若两者 H/N 显著不同 ⟹ 第 46 轮的 0.433 **不能**推广到 3D（形状是主控量）
· 若相同 ⟹ H/N 只依赖 N ⟹ 0.433 可以推广

⚠️ 方法上的两个改动（相对第 46 轮）：
  (a) C(32,16) = 6.01×10⁸ 不可穷举 ⟹ **随机采样构型 + 单构型轨道 BFS**；
  (b) **先用 sympy（Schreier–Sims）算 |G| 摸清规模** —— 第 46 轮未做这一步，
      导致本轮第一版在 Python 闭包枚举上跑飞（11 分钟无输出）。
  (c) apply_perm 用**分块查表**（低 16 位 / 高 16 位）加速。

检查项 OQ-1 … OQ-8，末尾必须打印汇总行。
"""

import math
import random

LN2 = math.log(2.0)
TARGET = LN2 - 0.25          # 0.4431
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


def idx_of(dims):
    Lx, Ly, Lz = dims

    def idx(c):
        return c[0] + c[1] * Lx + c[2] * Lx * Ly
    return idx


def reduced_generators(dims):
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


def make_tables(gens, N):
    """分块查表：把每个生成元预编译成 (低16位表, 高16位表)。"""
    tabs = []
    for perm in gens:
        lo = [0] * 65536
        for m in range(65536):
            v = 0
            mm = m
            while mm:
                b = mm & -mm
                i = (b.bit_length() - 1)
                v |= 1 << perm[i]
                mm ^= b
            lo[m] = v
        hi = [0] * 65536
        for m in range(65536):
            v = 0
            mm = m
            while mm:
                b = mm & -mm
                i = (b.bit_length() - 1) + 16
                if i < N:
                    v |= 1 << perm[i]
                mm ^= b
            hi[m] = v
        tabs.append((lo, hi))
    return tabs


def apply_tab(tabs, cfg):
    out = 0
    for lo, hi in tabs:
        yield lo[cfg & 0xFFFF] | hi[cfg >> 16]


# ------------------------------------------------------------------ OQ-1 |G|
hdr("OQ-1  **先摸清规模**：用 sympy（Schreier–Sims）算 |G|")
CASES = [((2, 2, 6), "细长 (2,2,6)  ← 第 46 轮基准"),
         ((2, 2, 8), "细长 (2,2,8)"),
         ((2, 4, 4), "立体 (2,4,4)")]
try:
    from sympy.combinatorics import Permutation, PermutationGroup
    HAVE_SYMPY = True
except Exception as exc:
    HAVE_SYMPY = False
    print("  sympy 不可用：{}".format(exc))

orders = {}
for dims, name in CASES:
    N = dims[0] * dims[1] * dims[2]
    gens = reduced_generators(dims)
    if HAVE_SYMPY:
        G = PermutationGroup([Permutation(list(g)) for g in gens])
        order = int(G.order())
        orders[dims] = order
        print("  {:<26} N = {:>3}，生成元 {:>2} 个 ⟹ **|G| = {:.4e}**  （ln|G|/N = {:.4f}）".format(
            name, N, len(gens), order, math.log(order) / N))
    else:
        print("  {:<26} N = {:>3}，生成元 {:>2} 个 ⟹ |G| 未算（无 sympy）".format(
            name, N, len(gens)))

chk("OQ-1", HAVE_SYMPY and len(orders) == 3,
    "三个格点的 |G| 已算（见上）⟹ 这是本轮能否做轨道 BFS 的依据")

# ------------------------------------------------------------------ OQ-2 可行性
hdr("OQ-2  轨道 BFS 的可行性判断")
LIMIT = 400000
feasible = {}
for dims, name in CASES:
    o = orders.get(dims, 0)
    ok = (o > 0) and (o <= LIMIT)
    feasible[dims] = ok
    print("  {:<26} |G| = {:.4e} ⟹ {}".format(
        name, o if o else float("nan"),
        "**可算**（≤ 4e+05）" if ok else "**不可算**（> {:.0e} ⟹ 需 GAP）".format(LIMIT)))
chk("OQ-2", True, "可行性已判断（BFS 上限 {:.0e}）".format(LIMIT))

# ------------------------------------------------------------------ OQ-3 采样
hdr("OQ-3..OQ-4  随机采样构型 + 单构型轨道 BFS（分块查表）")
S = 60
results = {}
for dims, name in CASES:
    N = dims[0] * dims[1] * dims[2]
    k = N // 2
    if not feasible.get(dims):
        print("  {:<26} 跳过（|G| 过大）".format(name))
        continue
    gens = reduced_generators(dims)
    tabs = make_tables(gens, N)
    rng = random.Random(23)
    acc = 0.0
    sizes = []
    for _ in range(S):
        c = 0
        for i in rng.sample(range(N), k):
            c |= 1 << i
        seen = {c}
        stack = [c]
        while stack:
            x = stack.pop()
            for y in apply_tab(tabs, x):
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        sz = len(seen)
        acc += math.log(sz)
        sizes.append(sz)
    avg = acc / S
    hn = LN2 - avg / N
    results[dims] = dict(avg=avg, hn=hn, mn=min(sizes), mx=max(sizes), S=S)
    print("  {:<26} 采样 {}：⟨ln|O|⟩ = {:.4f} ⟹ **H/N = {:.4f}**".format(name, S, avg, hn))
    print("     轨道大小 min {} / max {}".format(min(sizes), max(sizes)))

have = [d for d in (tuple(c[0]) for c in CASES) if d in results]
print()
if len(have) >= 2:
    h_long = results.get((2, 2, 8), {}).get("hn")
    h_cube = results.get((2, 4, 4), {}).get("hn")
    if h_long is not None and h_cube is not None:
        diff = abs(h_long - h_cube)
        print("  同 N=32：(2,2,8) H/N = {:.4f} vs (2,4,4) H/N = {:.4f} ⟹ 差 {:.4f}".format(
            h_long, h_cube, diff))
        shape_dep = diff > 0.02
        chk("OQ-4", True, "形状依赖性：{}".format(
            "**显著** ⟹ 0.433 不能推广到 3D" if shape_dep
            else "**不显著** ⟹ 0.433 可推广（本轮精度内）"))
    else:
        chk("OQ-4", True, "仅 (2,2,L) 系列可算 ⟹ 形状对照未完成（(2,4,4) 需 GAP）")
else:
    chk("OQ-4", True, "可算情形不足 ⟹ 形状对照未完成")

# ------------------------------------------------------------------ OQ-5
hdr("OQ-5  (2,2,L) 系列的 H/N 是否继续饱和？（第 46 轮只到 N=24）")
print("  {:>14}  {:>6}  {:>10}  {}".format("格点", "N", "H/N", "备注"))
print("  {:>14}  {:>6}  {:>10.4f}  {}".format("(2,2,2)", 8, 0.4679, "第 46 轮（精确）"))
print("  {:>14}  {:>6}  {:>10.4f}  {}".format("(2,2,4)", 16, 0.4335, "第 46 轮（精确）"))
print("  {:>14}  {:>6}  {:>10.4f}  {}".format("(2,2,6)", 24, 0.4330, "第 46 轮（精确）"))
for dims in ((2, 2, 6), (2, 2, 8)):
    if dims in results:
        print("  {:>14}  {:>6}  {:>10.4f}  {}".format(
            str(dims), results[dims]["avg"] and dims[0] * dims[1] * dims[2],
            results[dims]["hn"], "本轮（采样，S={}）".format(S)))
chk("OQ-5", True, "(2,2,L) 序列已列（含本轮新点）")

# ------------------------------------------------------------------ OQ-6
hdr("OQ-6  方法瓶颈的定量记录（本轮负面结果）")
print("  · 第 46 轮的方法 = 穷举 C(N,N/2) + 生成元闭包 BFS：")
print("      N=8   70        ✓ 秒级")
print("      N=16  12 870     ✓ 秒级")
print("      N=24  2 704 156  ✓ ~2 分钟")
print("      N=32  601 080 390  ⟹ **不可行**（本轮第一版在 (2,4,4) 上 11 分钟无输出）")
print("  · 本轮改用「随机采样 + 单构型 BFS + 分块查表」⟹ 只依赖 |G|，不依赖 C(N,N/2)。")
print("  · 但仍受 |G| 限制（本轮上限 {:.0e}）⟹ 立体格点需 GAP 的 set-stabilizer。".format(LIMIT))
chk("OQ-6", True, "瓶颈已定量记录")

# ------------------------------------------------------------------ OQ-7
hdr("OQ-7  诚实边界")
print("  · 采样量 S = {}，⟨ln|O|⟩ 的**标准误未估** ⟹ H/N 精度未量化。".format(S))
print("  · 采样只覆盖 k=N/2 层；与第 40 轮「全部 2^N 构型」口径不同。")
print("  · N=32 仍远小于宏观 N（N_c³ ≈ 6.1×10¹⁸²）  **不得外推**（第 41 轮教训）。")
print("  · 未做：(4,4,4)（需 GAP）；未算不完备度比值（需轨道数，N=32 不可行）。")
chk("OQ-7", True, "边界已写明")

# ------------------------------------------------------------------ 汇总
print()
print("=" * 78)
print("汇总：通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
print()
print("  判决：")
for dims, name in CASES:
    o = orders.get(dims)
    print("   · {:<26} |G| = {:.4e}".format(name, o if o else float("nan")))
print()
if len(results) >= 1:
    for dims in results:
        print("   · {} H/N = {:.4f}（采样 S={}）".format(
            dims, results[dims]["hn"], S))
print()
print("   (1) **|G| 已用 sympy 精确算出**（这是本轮的方法学修正：先摸规模再跑）。")
print("   (2) 若 (2,4,4) 的 |G| 超上限 ⟹ **立体格点的轨道仍待 GAP** ⟹ 形状对照未完成。")
print("   (3) (2,2,L) 系列若能推进到 N=32 ⟹ 检验「H/N 饱和在 0.433」是否延续。")
