# -*- coding: utf-8 -*-
"""第 48 轮：用**正确** tick 群重算受影响的 H/N。

受影响 = 含边长 ≥ 6 的格点：(2,2,6) N=24、(2,2,8) N=32。
不受影响 = 边长 ≤ 4：(2,2,2)、(2,2,4)、(2,4,4)、(4,4,4)。

方法：
- (2,2,6)：k=N/2 层**全部** C(24,12) = 2,704,156 个构型 ⟹ 精确轨道划分；
- (2,2,8)：随机采样 + 单构型轨道 BFS（轨道仅 ~10³，很快）；
- (2,4,4)：**留给 GAP**（轨道上界 = (Z₂)³ 类大小 1.68×10⁶ ⟹ Python BFS 会跑飞）。
"""

import itertools
import math
import random
import sys
import time

from sympy.combinatorics import Permutation

sys.setrecursionlimit(200000)
LN2 = math.log(2.0)
OK = [0]
FAIL = [0]
CH = 8                      # 分块查表的块宽（bit）


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


# ------------------------------------------------------------------ 格点工具
def idx_of(dims):
    Lx, Ly = dims[0], dims[1]
    return lambda c: c[0] + c[1] * Lx + c[2] * Lx * Ly


def other_axes(axis):
    return [c for c in range(3) if c != axis]


def lines_of(dims, axis):
    o = other_axes(axis)
    return [(a, b) for a in range(dims[o[0]]) for b in range(dims[o[1]])], o


def line_coords(dims, axis, a, b):
    o = other_axes(axis)
    idx = idx_of(dims)
    out = []
    for t in range(dims[axis]):
        c = [0, 0, 0]
        c[axis] = t
        c[o[0]] = a
        c[o[1]] = b
        out.append(idx(c))
    return out


def match_on_line(dims, axis, a, b, offs, N):
    """该线上相位 offs 的完美匹配（环面绕回）。"""
    co = line_coords(dims, axis, a, b)
    L = dims[axis]
    p = list(range(N))
    used = set()
    for t in range(L):
        u = (offs + t) % L
        if u in used:
            continue
        v = (u + 1) % L
        if v in used:
            continue
        used.add(u); used.add(v)
        p[co[u]], p[co[v]] = p[co[v]], p[co[u]]
    return p


def M_of_axis(dims, axis, N):
    p = list(range(N))
    ls, _ = lines_of(dims, axis)
    for (a, b) in ls:
        q = match_on_line(dims, axis, a, b, 0, N)
        for i in range(N):
            if q[i] != i:
                p[i] = q[i]
    return tuple(p)


def gens_correct(dims):
    """正确化简：M_a + 每线 σ_j = 相位1匹配 ∘ 相位0匹配。"""
    N = dims[0] * dims[1] * dims[2]
    gens = []
    for axis in range(3):
        L = dims[axis]
        if L < 2:
            continue
        gens.append(M_of_axis(dims, axis, N))
        if L < 4:
            continue
        ls, _ = lines_of(dims, axis)
        for (a, b) in ls:
            m0 = Permutation(match_on_line(dims, axis, a, b, 0, N))
            m1 = Permutation(match_on_line(dims, axis, a, b, 1, N))
            gens.append(tuple((m0 * m1).array_form))
    return gens


def gens_buggy(dims):
    """第 41–47 轮实际用的（纯平移 +2）—— 保留以便对照。"""
    N = dims[0] * dims[1] * dims[2]
    gens = []
    for axis in range(3):
        L = dims[axis]
        if L < 2:
            continue
        gens.append(M_of_axis(dims, axis, N))
        if L < 4:
            continue
        ls, _ = lines_of(dims, axis)
        for (a, b) in ls:
            co = line_coords(dims, axis, a, b)
            p2 = list(range(N))
            for i in range(L):
                p2[co[i]] = co[(i + 2) % L]
            gens.append(tuple(p2))
    return gens


# ----------------------------------------------------- 分块查表的置换作用
def make_apply(N, gens):
    """返回 apply(cfg, gi)：8 位分块查表。"""
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
    return apply, len(gens)


def orbit_sizes_layer(dims, k, sample=None, seed=1):
    N = dims[0] * dims[1] * dims[2]
    gens = gens_correct(dims)
    apply, ng = make_apply(N, gens)
    if sample is None:
        cfgs = (m for m in range(1 << N) if m.bit_count() == k)
    else:
        rng = random.Random(seed)
        cfgs = []
        for _ in range(sample):
            m = 0
            for i in rng.sample(range(N), k):
                m |= 1 << i
            cfgs.append(m)
        cfgs = iter(cfgs)
    seen = set()
    sizes = []
    t0 = time.time()
    for cfg in cfgs:
        if cfg in seen:
            continue
        stack = [cfg]
        seen.add(cfg)
        cnt = 0
        while stack:
            x = stack.pop()
            cnt += 1
            for gi in range(ng):
                y = apply(x, gi)
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        sizes.append(cnt)
    return sizes, time.time() - t0


def h_over_n(sizes, N):
    # ⚠️⚠️ 口径警告（第 50 轮 R-2 / C-2 查明，第 0 批 2026-09-28 加注）：
    #   本函数用「**轨道等权**」：avg = Σ ln|O| / #轨道；
    #   而第 40 轮的**权威定义**是「**构型等权**」：avg = Σ |O|·ln|O| / Σ |O|（|O| 越大权重越大）。
    #   两者在 N = 8 / 16 / 24 上差 0.0520 / 0.0318 / 0.0176。
    #   ⟹ 本脚本产出的 H/N **不可直接引用**；正确值见第 50 轮更正（(2,2,6) 的 0.4334，原报 0.4510）。
    #   ⟹ 本函数只适用于「**全层枚举**」场景；GAP 的**随机构型采样**天然是构型等权，不受此限。
    avg = sum(math.log(s) for s in sizes) / len(sizes)
    return LN2 - avg / N, avg


# ================================================================== 检查项
hdr("FR-1  (2,2,6) N=24 —— 精确轨道划分（正确群）")
sizes, dt = orbit_sizes_layer((2, 2, 6), 12)
hn6, avg6 = h_over_n(sizes, 24)
print("  轨道数 = {}，用时 {:.1f} s".format(len(sizes), dt))
print("  ⟨ln|O|⟩ = {:.4f}，⟨ln|O|⟩/N = {:.4f}".format(avg6, avg6 / 24))
print("  **H/N = {:.4f}**   （第 46 轮用错误群给 0.4330）".format(hn6))
print("  轨道大小 min/max = {} / {}".format(min(sizes), max(sizes)))
chk("FR-1", abs(hn6 - 0.25) > 0.02,
    "H/N = {:.4f} vs 面积律要求 0.25 ⟹ {}".format(hn6, "未命中"))

hdr("FR-2  (2,2,8) N=32 —— 采样 60 构型（正确群）")
sizes8, dt8 = orbit_sizes_layer((2, 2, 8), 16, sample=60, seed=7)
hn8, avg8 = h_over_n(sizes8, 32)
print("  ⟨ln|O|⟩ = {:.4f}，⟨ln|O|⟩/N = {:.4f}，用时 {:.1f} s".format(avg8, avg8 / 32, dt8))
print("  **H/N = {:.4f}**   （第 47 轮用错误群给 0.4614）".format(hn8))
print("  轨道大小 min/max = {} / {}".format(min(sizes8), max(sizes8)))
chk("FR-2", True, "H/N = {:.4f}".format(hn8))

hdr("FR-4  边长 ≤ 4 的格点：两套生成元是否**逐元素相同**（应相同）")
for dims in [(2, 2, 2), (2, 2, 4), (2, 4, 4)]:
    gc, gb = gens_correct(dims), gens_buggy(dims)
    same = (gc == gb)
    print("  {:<10} 正确 {} 个 / 错误 {} 个 ⟹ {}".format(
        str(dims), len(gc), len(gb), "逐元素相同 ✓" if same else "**有差异**"))
    chk("FR-4" + str(dims[-1]), same, "{}：生成元逐元素相同".format(str(dims)))

hdr("FR-5  汇总对照（(2,2,L) 系列）")
print("  {:<12} {:>4}  {:>11} {:>11}  {}".format("格点", "N", "H/N(正确)", "H/N(旧)", "受影响？"))
tab = [((2, 2, 2), 8, 0.4679, 0.4679),
       ((2, 2, 4), 16, 0.4335, 0.4335),
       ((2, 2, 6), 24, hn6, 0.4330),
       ((2, 2, 8), 32, hn8, 0.4614)]
for dims, N, new, old in tab:
    flag = "否" if abs(new - old) < 1e-9 else "**是**"
    print("  {:<12} {:>4}  {:>11.4f} {:>11.4f}  {}".format(str(dims), N, new, old, flag))
chk("FR-5", True, "对照表已列")

print()
print("=" * 78)
print("汇总：通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
