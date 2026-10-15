# -*- coding: utf-8 -*-
"""
相位模式的维度诊断（第 43 轮附）
================================
目的：解释主脚本里「完整格点 global 给 61.3%，而第 26 轮声称 29.7%」的差异。
做法：在 1D / 2D / 3D 上分别测四种相位模式的 ⟨r²⟩/n，并扫 L 与种子。

模型：d 维简单立方（周期边界），每 tick 在 d 个轴中随机选一个，
所有线共用相位（global）或每线独立（indep）；配对 (φ,φ+1),(φ+2,φ+3)…
"""

import math
import random

N_TICKS = 2000


def final_lattice(mode, dim, lx, n=N_TICKS, seed=0, p=1.0):
    """返回 ⟨r²⟩（所有诸元最终位移平方的平均，真实位移）。"""
    if dim == 1:
        N = lx
    elif dim == 2:
        N = lx * lx
    else:
        N = lx ** 3

    def idx(c):
        i = 0
        for k in range(dim):
            i = i * lx + c[k]
        return i

    grid = list(range(N))
    c0 = [[(i // (lx ** k)) % lx for k in range(dim)] for i in range(N)]
    coords = [c[:] for c in c0]
    rng = random.Random(seed)
    fixed = {}

    def lines():
        """枚举 (其它坐标, 沿线坐标) 组合的迭代器：产出 (axis, other_coords list)"""
        for axis in range(dim):
            others = [range(lx) for k in range(dim) if k != axis]
            stack = [[]]
            for r in others:
                stack = [s + [v] for s in stack for v in r]
            for combo in stack:
                yield axis, combo

    all_lines = list(lines())

    for _ in range(n):
        axis = rng.randrange(dim)
        gphi = rng.randint(0, 1) if mode == "global" else None
        for ax, combo in all_lines:
            if ax != axis:
                continue
            if mode == "indep":
                phi = rng.randint(0, 1)
            elif mode == "global":
                phi = gphi
            elif mode == "fixed_line":
                key = (ax,) + tuple(combo)
                if key not in fixed:
                    fixed[key] = rng.randint(0, 1)
                phi = fixed[key]
            elif mode == "fixed_global":
                phi = 0
            else:
                raise ValueError(mode)

            if rng.random() >= p:
                continue

            for t in range(lx):
                if (t - phi) % 2 != 0:
                    continue
                t2 = (t + 1) % lx
                cA = [0] * dim
                cB = [0] * dim
                ci = 0
                for k in range(dim):
                    if k == ax:
                        cA[k], cB[k] = t, t2
                    else:
                        cA[k] = cB[k] = combo[ci]
                        ci += 1
                i, j = idx(cA), idx(cB)
                gi, gj = grid[i], grid[j]
                grid[i], grid[j] = gj, gi
                coords[gi][ax] += 1
                coords[gj][ax] -= 1

    tot = 0.0
    for lab in range(N):
        tot += sum((coords[lab][k] - c0[lab][k]) ** 2 for k in range(dim))
    return tot / N


print("=" * 78)
print("相位模式的维度诊断：⟨r²⟩/n")
print("=" * 78)

print()
print("  ① 维度扫描（L = 10，n = 2000，单种子 7）")
print("  {:>12}  {:>12}  {:>12}  {:>12}".format("dim", "indep", "global", "fixed_line"))
for dim in (1, 2, 3):
    vals = []
    for mode in ("indep", "global", "fixed_line"):
        v = final_lattice(mode, dim, 10, seed=7)
        vals.append(v / N_TICKS)
    print("  {:>12}  {:>12.4f}  {:>12.4f}  {:>12.4f}".format(dim, vals[0], vals[1], vals[2]))

print()
print("  ② L 与种子的稳健性（3D，global 模式）")
print("  {:>6}  {}".format("L", "   ".join("seed{}".format(s) for s in (1, 2, 3, 4, 5))))
for lx in (6, 8, 10, 12):
    row = []
    for s in (1, 2, 3, 4, 5):
        n = N_TICKS
        v = final_lattice("global", 3, lx, n=n, seed=s)
        row.append(v / n)
    print("  {:>6}  {}".format(lx, "   ".join("{:.4f}".format(x) for x in row)))

print()
print("  ③ 同口径下 indep 的对照（3D）")
for lx in (8, 10, 12):
    row = []
    for s in (1, 2, 3):
        v = final_lattice("indep", 3, lx, n=N_TICKS, seed=s)
        row.append(v / N_TICKS)
    print("  {:>6}  {}".format(lx, "   ".join("{:.4f}".format(x) for x in row)))

print()
print("  ④ 统计分布（3D，L = 10，n = 2000，20 个种子）—— 检验是否自平均")
print("  第 26 轮原文只用了**两个种子**（29.7% / 42.5%），本节检验这两个数是不是噪声。")
for mode in ("indep", "global"):
    vals = [final_lattice(mode, 3, 10, seed=s) / N_TICKS for s in range(20)]
    m = sum(vals) / len(vals)
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))
    print("  {:<8}  均值 {:.3f}   标准差 {:.3f}   范围 [{:.3f}, {:.3f}]   相对散布 {:.0%}".format(
        mode, m, sd, min(vals), max(vals), sd / m))

print()
print("=" * 78)
print("  读法：indep 的相对散布应很小（自平均）；global 若散布很大 ⟹ **非自平均**，")
print("        那么第 26 轮的「29.7% / 42.5%（两个种子）」只是噪声，不是「塌缩值」。")
print("        结论（每线独立是必需条件）仍成立，但**数值表述必须改**。")
print("=" * 78)
