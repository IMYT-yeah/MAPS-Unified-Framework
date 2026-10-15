# -*- coding: utf-8 -*-
"""决定性检验：正确化简群 vs 第 41–47 轮（纯平移）群 —— 是否**同一群**。

阶相同不代表群相同（单线 L=6 的例子：两个 6 阶子群只共有 {e, M0}）。
所以这里做两件事：
  (a) 小群（|G| ≤ 10⁵）直接**枚举元素集**比较；
  (b) 大群用 sympy 的**双向包含**检查（is_subgroup 两个方向）。
"""

import sys

from sympy.combinatorics import Permutation, PermutationGroup

sys.setrecursionlimit(200000)

exec(open("_gen_fix_48_defs.py", encoding="utf-8").read()) if False else None


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


def reduced_correct(dims):
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


def enumerate_group(gens, N, cap=400000):
    """生成元闭包，返回元素集合（超上限返回 None）。"""
    e = tuple(range(N))
    seen = {e}
    frontier = [e]
    G = [Permutation(list(g)) for g in gens]
    while frontier:
        x = frontier.pop()
        px = Permutation(list(x))
        for g in G:
            y = tuple((px * g).array_form)
            if y not in seen:
                seen.add(y)
                frontier.append(y)
                if len(seen) > cap:
                    return None
    return seen


def PG(gens):
    return PermutationGroup([Permutation(list(g)) for g in gens])


print("=" * 96)
print("决定性检验：正确化简 vs 第 41–47 轮（纯平移）")
print("=" * 96)
for dims in [(2, 2, 6), (2, 2, 8), (2, 2, 10), (2, 2, 4), (2, 2, 2)]:
    N = dims[0] * dims[1] * dims[2]
    Cb, Bb = reduced_correct(dims), reduced_buggy(dims)
    GC, GB = PG(Cb), PG(Bb)
    oC, oB = GC.order(), GB.order()
    # (a) 生成元是否互相在对方群里（最强判据，且便宜）
    C_in_B = all(GB.contains(Permutation(list(g))) for g in Cb)
    B_in_C = all(GC.contains(Permutation(list(g))) for g in Bb)
    # (b) 高精度穷举验证
    sc = enumerate_group(Cb, N, cap=6000)
    sb = enumerate_group(Bb, N, cap=6000)
    enum_eq = (sc is not None and sb is not None and sc == sb)
    print("  格点 {:<10} N={:<3} |正|={:<8} |错|={:<8} 正生成元⊆错群={:<5} 错生成元⊆正群={:<5} 穷举相等={}".format(
        str(dims), N, oC, oB, str(C_in_B), str(B_in_C),
        str(enum_eq) if (sc is not None and sb is not None) else "超上限"))
    del GC, GB

print()
print("单个线的对照（只看一条长度 6 的线，无其他轴）：")
for dims in [(1, 1, 4), (1, 1, 6), (1, 1, 8)]:
    N = dims[0] * dims[1] * dims[2]
    Cb, Bb = reduced_correct(dims), reduced_buggy(dims)
    sc = enumerate_group(Cb, N)
    sb = enumerate_group(Bb, N)
    print("  线长 {:<3} |正|={:<5} |错|={:<5} 穷举相等={:<6} 共有元素={}".format(
        dims[2], len(sc), len(sb), str(sc == sb),
        "{} / {}".format(len(sc & sb), len(sc | sb))))
