# -*- coding: utf-8 -*-
"""生成元集错误的定位与修正（第 48 轮核心发现）。

背景（第 41/46/47 轮共用的代码）：
    perm2[coords[i]] = coords[(i + 2) % L]      # ← 全体 +2 的「纯平移」
被当成每线的 σ_j。但正确的 σ_j（= 相位 1 匹配 ∘ 相位 0 匹配）是
**偶位 +2、奇位 −2**（即 M_{j,0}·M_{j,1}），纯平移**不在** tick 群里。

判据：把 full（真全 tick 集）/ 正确化简 / 第41–47 轮化简 三者的群阶一起算。
只有在**线长 ≥ 6** 时才会暴露（L = 2/4 时两者恰好相同）。
"""

import itertools
import sys

from sympy.combinatorics import Permutation, PermutationGroup

sys.setrecursionlimit(200000)


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
    """该线上相位 offs 的完美匹配（环面绕回），其余格点固定。"""
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
    """M_a：该轴所有线取相位 0 的匹配。"""
    p = list(range(N))
    ls, _ = lines_of(dims, axis)
    for (a, b) in ls:
        q = match_on_line(dims, axis, a, b, 0, N)
        for i in range(N):
            if q[i] != i:
                p[i] = q[i]
    return tuple(p)


def full_generators(dims):
    """真全 tick 集（第 41 轮 `full_generators` 的正确写法）。"""
    N = dims[0] * dims[1] * dims[2]
    gens = []
    for axis in range(3):
        L = dims[axis]
        if L < 2:
            continue
        ls, _ = lines_of(dims, axis)
        nph = 2 if L >= 4 else 1
        for phbits in range(nph ** len(ls)):
            p = list(range(N))
            for li, (a, b) in enumerate(ls):
                off = (phbits // (nph ** li)) % nph
                q = match_on_line(dims, axis, a, b, off, N)
                for i in range(N):
                    if q[i] != i:
                        p[i] = q[i]
            gens.append(tuple(p))
    return gens


def reduced_correct(dims):
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


def reduced_buggy(dims):
    """第 41/46/47 轮实际用的（纯平移 +2）—— 有意保留以便对照。"""
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


def PG(gens):
    return PermutationGroup([Permutation(list(g)) for g in gens])


print("=" * 100)
print("三套生成集的群阶对照")
print("=" * 100)
print("{:<11} {:>4}  {:>5} {:>5} {:>5}  {:<22} {:<22} {:<22}".format(
    "格点", "N", "|full|", "|正|", "|错|", "|full|", "|正确化简|", "|第41–47 轮|"))
print("-" * 100)
rows = []
CASES = [(2, 2, 2), (2, 2, 4), (2, 2, 6), (2, 2, 8), (2, 4, 4), (2, 2, 10), (4, 4, 4)]
for dims in CASES:
    N = dims[0] * dims[1] * dims[2]
    F, C, B = full_generators(dims), reduced_correct(dims), reduced_buggy(dims)
    if len(F) > 400:      # 4×4×4 的全集太大，跳过
        oF = None
    else:
        oF = PG(F).order()
    oC = PG(C).order()
    oB = PG(B).order()
    rows.append((dims, N, len(F), len(C), len(B), oF, oC, oB))
    print("{:<11} {:>4}  {:>5} {:>5} {:>5}  {:<22} {:<22} {:<22}".format(
        str(dims), N, len(F), len(C), len(B),
        "-" if oF is None else str(oF), str(oC), str(oB)))

print()
print("=" * 100)
print("判决")
print("=" * 100)
for dims, N, nF, nC, nB, oF, oC, oB in rows:
    same = (oB == oC)
    full_ok_c = (oF is None) or (oF == oC)
    print("  {:<11} 正确化简 vs 第41–47轮：{:<10} ｜ 全集 vs 正确化简：{}".format(
        str(dims),
        "相同 ✓" if same else "**不同 ✗（|错|/|正| = {:.4g}）**".format(oB / oC),
        "未算" if oF is None else ("相同 ✓" if full_ok_c else "**不同 ✗**")))
