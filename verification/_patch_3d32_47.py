# -*- coding: utf-8 -*-
"""
第 47 轮论文补丁（中英同步，6 项）。

A 段（2 项）：**修正第 46 轮块**的措辞 —— 第 47 轮实测 (2,2,8) 给 H/N = 0.4614
    （高于 N=24 的 0.4330）⟹ 「H/N 饱和在 ≈0.433」不成立，改为「落在 0.43–0.47，非单调」。
B 段（2 项）：在第 46 轮块之后插入【第 47 轮】块（|G| 的形状敏感性、H/N 非单调、
    立体格点轨道不可算 ⟹ 需 GAP）。
C 段（2 项）：同 A 段，但针对判决 3 的正文。

锚点必须恰好命中一次。
"""

import io
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
STAMP = "2026-09-22第47轮前"

N_OK = [0]
N_FAIL = [0]


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<30} 命中 {} 次 —— 拒绝".format(tag, n))
        N_FAIL[0] += 1
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<30} 已改".format(tag))
    N_OK[0] += 1


os.makedirs(HIST, exist_ok=True)
for src, stem in ((ZH, "论文初稿_v2.9"), (EN, "Paper_v2.9_EN")):
    dst = os.path.join(HIST, "{}_备份_{}.md".format(stem, STAMP))
    shutil.copy2(src, dst)
    print("  备份 ->", os.path.basename(dst))
print()

# ---------------------------------------------------------------- A 段：标题修正
sub_once(ZH,
         "> **【v2.9 补充（第 46 轮：k = N/2 的精确轨道 —— 不变量不完备，H/N 饱和在 ≈ 0.433）】**",
         "> **【v2.9 补充（第 46 轮：k = N/2 的精确轨道 —— 不变量不完备，H/N 落在 0.43–0.47）】**"
         " ⚠️ **第 47 轮修正**：原文的「H/N 饱和在 ≈0.433」**不成立** —— "
         "把 (2,2,L) 系列推进到 N=32 得 H/N = **0.4614**（高于 N=24 的 0.4330）⟹ **非单调**。",
         "ZH 46 标题修正")
sub_once(EN,
         "> **【v2.9 supplement (round 46: the exact orbit at k = N/2 — the invariant is incomplete, "
         "and H/N saturates at ≈ 0.433)**】**",
         "> **【v2.9 supplement (round 46: the exact orbit at k = N/2 — the invariant is incomplete, "
         "and H/N lies in 0.43–0.47)**】** ⚠️ **Corrected in round 47**: the original claim that "
         "\"H/N saturates at ≈0.433\" **fails** — extending the (2,2,L) family to N=32 gives "
         "H/N = **0.4614** (above the N=24 value 0.4330) ⟹ **non-monotonic**.",
         "EN 46 title fix")

# ---------------------------------------------------------------- B 段：插入 47 块
A_ZH = "> · **副产品**：不完备度（轨道数/等值集数）= 1.00 ⟶ 1.63 ⟶ **5.93**，随 N 增长 ⟹ 该比值本身可能是有结构的量，已列入候选池。"
A_EN = ("> · **By-product**: the incompleteness ratio (#orbits / #level sets) = 1.00 ⟶ 1.63 ⟶ "
        "**5.93** grows with N ⟹ this ratio may itself be a structured quantity; it has been "
        "added to the candidate pool.")

BLOCK_ZH = """
> **【v2.9 补充（第 47 轮：同 N=32 的形状对照 —— |G| 对形状极敏感，且 H/N 非单调）】** 上一条只能算 (2,2,L) 细长系列。本轮做**受控对照**：固定 N=32，只改形状。

> · **方法修正（本轮踩坑）**：上一条未先用 Schreier–Sims 摸清 |G| 就跑 Python 闭包枚举 ⟹ 在 (2,4,4) 上**11 分钟无输出**被迫中止。本轮改为：先算 |G|（sympy）⟶ 再判可行性 ⟶ 采样构型 + 单构型轨道 BFS（分块查表加速）。

| 格点 | N | 生成元 | **\|G\|** | ln\|G\|/N | **H/N** |
|---|---|---|---|---|---|
| (2,2,6) | 24 | 7 | 6.48×10² | 0.2697 | 0.4330（精）/ 0.4343（采） |
| (2,2,8) | 32 | 7 | **2.048×10³** | 0.2383 | **0.4614**（采） |
| (2,4,4) | 32 | 19 | **2.2015×10¹¹** | 0.8162 | **未算**（超上限） |

> · **判决 1（新发现）**：**同 N=32，只改形状，|G| 差 8 个数量级**（2.05×10³ vs 2.20×10¹¹）⟹ 群规模本身就是**形状的函数** ⟹ 上一条"细长格点不能代表 3D"的担心是**实质性的**。
> · **判决 2（修正上一条）**：**H/N 非单调** —— (2,2,L) 系列给 0.4679（N=8）⟶ 0.4335（N=16）⟶ 0.4330（N=24）⟶ **0.4614（N=32）**。机制：H/N 由 `ln|G|/N` 主导，而 ln|G|/N 从 0.2697（L=6）**降**到 0.2383（L=8）⟹ 轨道相对受限 ⟹ H/N 回升。⟹ 上一条的「饱和」改为「**落在 0.43–0.47 区间**」。
> · **判决 3（方法瓶颈）**：立体格点 (2,4,4) 的 |G| = 2.20×10¹¹ 超出本轮上限 ⟹ **形状对照未完成**。⚠️ 且 **不能从 |G| 推断 H/N**：(2,4,4) 的 ln|G|/N = 0.8162 > ln2，若轨道接近 |G| 则 H/N < 0（不可能）⟹ 其轨道**远小于** |G|（存在巨大稳定子）⟹ **必须算真实轨道，需要 GAP 的 set-stabilizer**。
> · **方法自校验**：(2,2,6) 采样给 0.4343，上一条精确值 0.4330 ⟹ 差 **0.0013** ⟹ 采样法可信。
> ⚠️ 采样量 S=60，标准误未估；N=32 仍远小于宏观 N ⟹ **不得外推**（第 41 轮教训）。

"""

BLOCK_EN = """
> **【v2.9 supplement (round 47: a shape control at fixed N=32 — |G| is extremely shape-sensitive, and H/N is non-monotonic)**】** The previous block could only handle the elongated (2,2,L) family. This round performs a **controlled comparison**: fix N=32 and change only the shape.

> · **Methodological correction (a pitfall of this round)**: the previous block ran a Python closure enumeration without first establishing |G| via Schreier–Sims ⟹ on (2,4,4) it produced **no output for 11 minutes** and had to be killed. This round instead: compute |G| (sympy) ⟶ judge feasibility ⟶ sample configurations + single-configuration orbit BFS (with block lookup tables).

| lattice | N | gens | **\|G\|** | ln\|G\|/N | **H/N** |
|---|---|---|---|---|---|
| (2,2,6) | 24 | 7 | 6.48×10² | 0.2697 | 0.4330 (exact) / 0.4343 (sampled) |
| (2,2,8) | 32 | 7 | **2.048×10³** | 0.2383 | **0.4614** (sampled) |
| (2,4,4) | 32 | 19 | **2.2015×10¹¹** | 0.8162 | **not computed** (over the cap) |

> · **Verdict 1 (new finding)**: at fixed N=32, changing only the shape changes |G| by **eight orders of magnitude** (2.05×10³ vs 2.20×10¹¹) ⟹ the group order is itself **a function of shape** ⟹ the previous block's worry that "elongated lattices do not represent 3D" is **substantive**.
> · **Verdict 2 (corrects the previous block)**: **H/N is non-monotonic** — the (2,2,L) family gives 0.4679 (N=8) ⟶ 0.4335 (N=16) ⟶ 0.4330 (N=24) ⟶ **0.4614 (N=32)**. Mechanism: H/N is governed by `ln|G|/N`, which **drops** from 0.2697 (L=6) to 0.2383 (L=8) ⟹ orbits are relatively more constrained ⟹ H/N rises again. ⟹ the previous "saturation" becomes "**lies in the 0.43–0.47 band**".
> · **Verdict 3 (methodological bottleneck)**: for the cubic-ish (2,4,4), |G| = 2.20×10¹¹ exceeds this round's cap ⟹ **the shape comparison is unfinished**. ⚠️ Moreover **H/N cannot be inferred from |G|**: ln|G|/N = 0.8162 > ln2, so an orbit close to |G| would give H/N < 0 (impossible) ⟹ its orbits are **far smaller** than |G| (a huge stabiliser) ⟹ **the true orbit must be computed, requiring GAP's set-stabilizer**.
> · **Self-check of the method**: (2,2,6) sampled gives 0.4343 against the previous exact 0.4330 ⟹ a difference of **0.0013** ⟹ the sampling method is trustworthy.
> ⚠️ Sample size S=60, standard error not estimated; N=32 is still far below the macroscopic N ⟹ **do not extrapolate** (lesson of round 41).

"""

sub_once(ZH, A_ZH, A_ZH + BLOCK_ZH, "ZH 插入第 47 轮块")
sub_once(EN, A_EN, A_EN + BLOCK_EN, "EN 插入第 47 轮块")

# ---------------------------------------------------------------- C 段：判决 3 正文修正
sub_once(ZH,
         "> · **判决 3（正面，本轮最有用）**：**H/N 饱和在 ≈ 0.433**",
         "> · **判决 3（正面，本轮最有用；⚠️ 第 47 轮修正为「非单调」）**：**H/N 落在 0.43–0.47**（原写「饱和在 ≈0.433」，第 47 轮把系列推到 N=32 得 0.4614 ⟹ 非单调）",
         "ZH 46 判决3修正")
sub_once(EN,
         "> · **Verdict 3 (positive, the most useful result here)**: **H/N saturates at ≈ 0.433**",
         "> · **Verdict 3 (positive; ⚠️ corrected in round 47 to \"non-monotonic\")**: **H/N lies in 0.43–0.47** (originally \"saturates at ≈0.433\"; round 47 extended the family to N=32 and obtained 0.4614 ⟹ non-monotonic)",
         "EN 46 verdict3 fix")

print()
print("=" * 70)
print("补丁汇总：成功 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
print("=" * 70)
