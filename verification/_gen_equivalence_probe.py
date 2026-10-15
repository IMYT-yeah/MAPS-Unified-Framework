# -*- coding: utf-8 -*-
"""生成元集等价性探针 v2（修正版）。

三套生成元：
- **A**（第 47 轮 `_orbit_3d32.py` 用的）：M_a（全匹配，相位 0）+ L≥4 时**每线 shift-by-2**
- **C**（真 tick 群的定义）：M_a + **每线、每个相位的完整匹配**（相位 0 与相位 1 各一个）
  ⟹ 这是"一次 tick"能产生的全部置换所生成的群（同一条线两个相位 = 两个完美匹配）
- **D**（第 41 轮证明的化简）：M_a + 每线**相位 0 匹配**（单个 s_j）

关系预期：C = D（因为相位 1 匹配 = σ_line · 相位 0 匹配，而 σ ∈ ⟨M_a, s_j⟩），
           A ⊆ C（σ_line 是 A 的生成元，而 σ_line = 相位1·相位0）。
关键问题：**A = C 吗？** 若不是，第 46/47 轮用的群**小于**真 tick 群。
"""

import sys

from sympy.combinatorics import Permutation, PermutationGroup

sys.setrecursionlimit(100000)


def idx_of(dims):
    Lx, Ly, Lz = dims
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
    """该线上相位 offs 的完美匹配（其余格点固定）。"""
    co = line_coords(dims, axis, a, b)
    L = dims[axis]
    p = list(range(N))
    # 环面配对：起点 offs（0/1），绕回；配成 (i, i+1) 型对
    seen = set()
    for t in range(L):
        u = (offs + t) % L
        if u in seen:
            continue
        v = (u + 1) % L
        if v in seen or v == u:
            continue
        seen.add(u); seen.add(v)
        p[co[u]], p[co[v]] = p[co[v]], p[co[u]]
    return tuple(p)


def shift_on_line(dims, axis, a, b, step, N):
    co = line_coords(dims, axis, a, b)
    L = dims[axis]
    p = list(range(N))
    for i in range(L):
        p[co[i]] = co[(i + step) % L]
    return tuple(p)


def all_matchings(dims, N):
    """M_a：每个轴上所有线都取相位 0 的匹配。"""
    out = []
    for axis in range(3):
        if dims[axis] < 2:
            continue
        ls, _ = lines_of(dims, axis)
        p = list(range(N))
        for (a, b) in ls:
            co = line_coords(dims, axis, a, b)
            L = dims[axis]
            for i in range(0, L - 1, 2):
                u, v = co[i], co[i + 1]
                p[u], p[v] = p[v], p[u]
        out.append(tuple(p))
    return out


def genA(dims):
    N = dims[0] * dims[1] * dims[2]
    gens = list(all_matchings(dims, N))
    for axis in range(3):
        L = dims[axis]
        if L < 4:
            continue
        ls, _ = lines_of(dims, axis)
        for (a, b) in ls:
            gens.append(shift_on_line(dims, axis, a, b, 2, N))
    return gens


def genC(dims):
    """真 tick 群：M_a + 每线**两个相位**的完整匹配。"""
    N = dims[0] * dims[1] * dims[2]
    gens = list(all_matchings(dims, N))
    for axis in range(3):
        L = dims[axis]
        if L < 2:
            continue
        ls, _ = lines_of(dims, axis)
        for (a, b) in ls:
            for offs in (0, 1):
                gens.append(match_on_line(dims, axis, a, b, offs, N))
    return gens


def genD(dims):
    """第 41 轮化简：M_a + 每线**相位 0**匹配。"""
    N = dims[0] * dims[1] * dims[2]
    gens = list(all_matchings(dims, N))
    for axis in range(3):
        if dims[axis] < 2:
            continue
        ls, _ = lines_of(dims, axis)
        for (a, b) in ls:
            gens.append(match_on_line(dims, axis, a, b, 0, N))
    return gens


def PG(gens):
    return PermutationGroup([Permutation(list(g)) for g in gens])


print("{:<11} {:>4}  {:>5} {:>5} {:>5}  {:<24} {:<24}".format(
    "格点", "N", "|A|", "|C|", "|D|", "ordA", "ordC = ordD"))
print("-" * 96)
rows = []
for dims in [(2, 2, 2), (2, 2, 4), (2, 2, 6), (2, 4, 4), (4, 4, 4)]:
    N = dims[0] * dims[1] * dims[2]
    A, C, D = genA(dims), genC(dims), genD(dims)
    GA, GC, GD = PG(A), PG(C), PG(D)
    oA, oC, oD = GA.order(), GC.order(), GD.order()
    same_CD = (oC == oD)
    A_sub_C = GA.is_subgroup(GC)
    C_sub_A = GC.is_subgroup(GA)
    rows.append((dims, N, oA, oC, oD, A_sub_C, C_sub_A, same_CD))
    print("{:<11} {:>4}  {:>5} {:>5} {:>5}  {:<24} {:<24}".format(
        str(dims), N, len(A), len(C), len(D), oA, "{} ({})".format(oC, "=D✓" if same_CD else "≠D!")))
    del GA, GC, GD

print()
print("包含关系（A = 第 47 轮用的群；C = 真 tick 群）：")
for dims, N, oA, oC, oD, A_sub_C, C_sub_A, same_CD in rows:
    ratio = oC / oA if oA else 0
    print("  {:<11} A⊆C={:<5} C⊆A={:<5} |C|/|A| = {:<8.4g} {}".format(
        str(dims), str(A_sub_C), str(C_sub_A), ratio,
        "✓ 同一群" if (A_sub_C and C_sub_A) else "❌ **A 是真子群**"))
