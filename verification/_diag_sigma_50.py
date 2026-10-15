# -*- coding: utf-8 -*-
"""第 50 轮诊断：H/N(2,2,6, k=12) = 0.4510（第 48 轮）vs 0.4334（本轮）—— 差异出自哪里？

背景：两轮的化简生成元**看起来**用同一种复合（m0∘m1），却给出不同的 H/N。
本脚本把**所有候选生成集**放在一起，对 (2,2,6) 做三件事：
  ① 枚举元素集（|G| = 648，小群可精确枚举）比较是否同一群；
  ② 用每个群精确算 k=12 层的 H/N（遍历 C(24,12) = 2,704,156 个构型）；
  ③ 判定哪个等于**真 tick 集**（全部「轴 × 每线相位」组合）。
另外单独检查长度 6 的环上 σ = m0∘m1 与 m1∘m0 是否互为逆。
"""

import io
import itertools
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


# ------------------------------------------------------------ 三种生成集
def gen_sigma_forward(dims):
    """A：σ_j = m0 ∘ m1（`_tickgroup.sigma_on_line` 与本轮所用）。"""
    return tg.gens_correct(dims)


def gen_sigma_backward(dims):
    """B：σ_j = m1 ∘ m0（反序复合 = 上式的逆）。"""
    N = dims[0] * dims[1] * dims[2]
    gens = []
    for axis in range(3):
        L = dims[axis]
        if L < 2:
            continue
        gens.append(tg.M_of_axis(dims, axis, N))
        if L < 4:
            continue
        ls, _ = tg.lines_of(dims, axis)
        for (a, b) in ls:
            m0 = list(tg.match_on_line(dims, axis, a, b, 0, N))
            m1 = list(tg.match_on_line(dims, axis, a, b, 1, N))
            gens.append(tuple(tg.compose(m1, m0)))      # 反序
    return gens


def gen_pure_shift(dims):
    """C：第 41–47 轮实际用的「全体 +2 纯平移」。"""
    return tg.gens_buggy(dims)


def gen_full_tick(dims):
    """D：**真 tick 集** —— 每个轴 × 每条线独立取 0/1 相位的全部组合。

    这是定义的直接实现，不含任何化简，是判定的**基准**。
    """
    N = dims[0] * dims[1] * dims[2]
    gens = []
    for axis in range(3):
        L = dims[axis]
        if L < 2:
            continue
        ls, _ = tg.lines_of(dims, axis)
        nph = 2 if L >= 4 else 1
        for bits in range(nph ** len(ls)):
            p = list(range(N))
            for li, (a, b) in enumerate(ls):
                offs = (bits // (nph ** li)) % nph
                q = tg.match_on_line(dims, axis, a, b, offs, N)
                for i in range(N):
                    if q[i] != i:
                        p[i] = q[i]
            gens.append(tuple(p))
    return gens


# ------------------------------------------------------------ 工具
def enum_group(gens, N, cap=200000):
    e = tuple(range(N))
    seen = {e}
    fr = [e]
    G = [list(g) for g in gens]
    while fr:
        x = fr.pop()
        for g in G:
            y = tuple(g[i] for i in x)
            if y not in seen:
                seen.add(y)
                fr.append(y)
                if len(seen) > cap:
                    return None
    return seen


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


def hn_layer(dims, k, gens):
    """精确算 k 层的 H/N（遍历该层全部构型，轨道等权）。"""
    N = dims[0] * dims[1] * dims[2]
    apply = make_apply(N, gens)
    ng = len(gens)
    seen = set()
    sumln = 0.0
    cnt = 0
    t0 = time.time()
    for m in range(1 << N):
        if m.bit_count() != k:
            continue
        if m in seen:
            continue
        stack = [m]
        seen.add(m)
        size = 0
        while stack:
            x = stack.pop()
            size += 1
            for gi in range(ng):
                y = apply(x, gi)
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        sumln += math.log(size) * size
        cnt += size
    return LN2 - (sumln / cnt) / N, time.time() - t0


# ================================================================== 1  单线
hdr("D1  单条长度 6 的环：σ = m0∘m1 与 m1∘m0 是不是互为逆？")
dims = (1, 1, 6)
N = 6
m0 = list(tg.match_on_line(dims, 2, 0, 0, 0, N))
m1 = list(tg.match_on_line(dims, 2, 0, 0, 1, N))
fwd = tg.compose(m0, m1)
bwd = tg.compose(m1, m0)
print("  m0 = {}".format(m0))
print("  m1 = {}".format(m1))
print("  σ_fwd = m0∘m1 = {}".format(list(fwd)))
print("  σ_bwd = m1∘m0 = {}".format(list(bwd)))
ident = tuple(range(N))
prod1 = tuple(fwd[bwd[i]] for i in range(N))
prod2 = tuple(bwd[fwd[i]] for i in range(N))
print("  σ_fwd∘σ_bwd = {}   σ_bwd∘σ_fwd = {}".format(list(prod1), list(prod2)))
print("  ⟹ 二者{}（{}）".format("互为逆" if prod1 == ident == prod2 else "**不是**互为逆",
                                "σ_fwd = σ_bwd⁻¹"))
# 循环分解
def cycles(p):
    seen = set()
    out = []
    for i in range(len(p)):
        if i in seen:
            continue
        c = []
        j = i
        while j not in seen:
            seen.add(j)
            c.append(j)
            j = p[j]
        if len(c) > 1:
            out.append(tuple(c))
    return out


print("  循环分解：σ_fwd = {}   σ_bwd = {}".format(cycles(fwd), cycles(bwd)))
print("  与技能第 27 条的对照：技能写「积 = (0 2 4)(1 5 3)」，实算 σ_fwd = {}（**逆**）".format(cycles(fwd)))

# ================================================================== 2  群等同
hdr("D2  (2,2,6) / (2,2,8)：四套生成集给出的是不是同一个群？")
for dims2 in [(2, 2, 6), (2, 2, 8), (2, 2, 10)]:
    N2 = dims2[0] * dims2[1] * dims2[2]
    sets = {
        "A σ=m0∘m1": gen_sigma_forward(dims2),
        "B σ=m1∘m0": gen_sigma_backward(dims2),
        "C 纯平移": gen_pure_shift(dims2),
    }
    gf = gen_full_tick(dims2)
    Sfull = enum_group(gf, N2)
    print("  格点 {:<10} |真 tick 集生成群| = {}".format(str(dims2), len(Sfull)))
    for name, g in sets.items():
        S = enum_group(g, N2)
        eq = (S == Sfull)
        sub = (S is not None and Sfull is not None and S <= Sfull)
        print("     {:<12} |G| = {:<8} 与真 tick 群 {}   ⊆真群 = {}  生成元数 {}".format(
            name, len(S), "**相等**" if eq else "不等", sub, len(g)))

# ================================================================== 3  H/N
hdr("D3  (2,2,6)、k=12：各生成集给出的 H/N（精确，遍历 C(24,12) = 2,704,156 构型）")
res = {}
for name, g in (("A σ=m0∘m1", gen_sigma_forward((2, 2, 6))),
                ("B σ=m1∘m0", gen_sigma_backward((2, 2, 6))),
                ("C 纯平移", gen_pure_shift((2, 2, 6)))):
    h, dt = hn_layer((2, 2, 6), 12, g)
    res[name] = h
    print("  {:<12} H/N = {:.4f}   （{:.0f} s）".format(name, h, dt))
print()
for name, h in res.items():
    print("  {:<12} {:.4f}   {}".format(name, h, "≈ 0.4510（第 48 轮）" if abs(h - 0.4510) < 0.003
                                       else ("≈ 0.4334（本轮）" if abs(h - 0.4334) < 0.003 else "两者都不符")))

print()
print("=" * 78)
print("结论见备忘录。")
print("=" * 78)
