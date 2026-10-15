# -*- coding: utf-8 -*-
"""tick 群的生成元（**第 48 轮更正后的正确版本**，后续所有轨道/H/N 计算都用它）。

一次 tick = 选一个轴 a + 该轴每条线**独立**选相位（0 或 1），沿该轴做完美匹配。
化简（第 41 轮证明，第 48 轮更正写法）：

    M_a·T(p) = ∏_{j: p_j = 1} σ_j        ⟹  T(p) = M_a · ∏ σ_j
    ⟹  G = ⟨ M_x, M_y, M_z ；所有 σ_j ⟩

其中
    M_a = 该轴「全 0 相位」匹配；
    σ_j = 该线（相位 1 匹配）∘（相位 0 匹配）  ⟹ **偶位 +2、奇位 −2**。

⚠️ 陷阱（第 48 轮查出）：σ_j **不是**「全体 +2 的纯平移」。
    两者在 L ≤ 4 时逐元素相同，L ≥ 6 时群不同（纯平移不在 tick 群里）。
    这里的 `sigma_on_line` 直接用两个匹配的复合计算，不手写公式 ⟹ 不会再踩。
"""

# ------------------------------------------------------------------ 基本工具
def other_axes(axis):
    return [c for c in range(3) if c != axis]


def idx_of(dims):
    Lx, Ly = dims[0], dims[1]
    return lambda c: c[0] + c[1] * Lx + c[2] * Lx * Ly


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
        used.add(u)
        used.add(v)
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


def compose(a, b):
    """先 b 后 a：c[i] = a[b[i]]。"""
    return [a[b[i]] for i in range(len(a))]


def sigma_on_line(dims, axis, a, b, N):
    """σ_j =（相位 1 匹配）∘（相位 0 匹配）—— 偶位 +2、奇位 −2。"""
    m0 = list(match_on_line(dims, axis, a, b, 0, N))
    m1 = list(match_on_line(dims, axis, a, b, 1, N))
    return tuple(compose(m0, m1))


def gens_correct(dims):
    """正确化简生成元：M_a + 每线 σ_j。"""
    N = dims[0] * dims[1] * dims[2]
    gens = []
    for axis in range(3):
        L = dims[axis]
        if L < 2:
            continue
        gens.append(M_of_axis(dims, axis, N))
        if L < 4:
            continue                      # L = 2 ⟹ 两相位相同 ⟹ σ_j = 恒等
        ls, _ = lines_of(dims, axis)
        for (a, b) in ls:
            gens.append(sigma_on_line(dims, axis, a, b, N))
    return gens


def gens_buggy(dims):
    """第 41–47 轮实际用的（纯平移 +2）—— **仅供对照，勿用于新计算**。"""
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


# ------------------------------------------------------------------ 随机构型
def random_cfgs(N, k, S, seed):
    import random
    rng = random.Random(seed)
    out = []
    for _ in range(S):
        m = 0
        for i in rng.sample(range(N), k):
            m |= 1 << i
        out.append(m)
    return out


if __name__ == "__main__":
    for dims in [(2, 2, 4), (2, 2, 6), (2, 4, 4), (4, 4, 4)]:
        g = gens_correct(dims)
        b = gens_buggy(dims)
        print("{} 正确 {} 个 / 旧 {} 个 ⟹ {}".format(
            dims, len(g), len(b), "逐元素相同" if g == b else "**有差异**"))
