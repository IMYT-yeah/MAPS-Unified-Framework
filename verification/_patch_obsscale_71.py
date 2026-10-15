# -*- coding: utf-8 -*-
"""第 71 轮 · 论文补丁（中英同步）：
① §8.2 块链末（§8.3 之前）插入【第 71 轮】块；
② §4.10 第 531 行（Nyquist 论证）后加一句指向该块的口径注（C-14）。"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

OK = BAD = 0


def sub_once(path, old, new, tag):
    global OK, BAD
    t = io.open(path, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        print("  [XX] {:<30} 命中 {} 次 —— 拒绝".format(tag, n))
        BAD += 1
        return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    OK += 1
    print("  [OK] {:<30} 已改".format(tag))


ZH_BLOCK = '''> **【v2.9 补充（第 71 轮：观测者的粗粒化尺度 —— 框架写过这条链，但少写了一个口径）】** 第 70 轮说「平滑 = 在大于 l_P 的尺度上读数」，**未给那个尺度**。本轮去找它，结论是：**框架已经写过这条推导链**（§4.10 的定理包），**能连成**，但推出的是**不等式**。脚本 `_observer_scale_71.py`（**OS-1…OS-9，9 项 0 失败**）。
>
> **① 链条逐环**（每环标性质）：① 普朗克尺度事件流（**公理 1**）→ ② 方向管最细尺度 = l_P（**本框架设定**，§4.10）→ ③ **方向簇 k ≥ 4**（**定理 1：Lusternik–Schnirelmann / Borsuk**，数学）→ ④ 每面元 4 个方向模式（③ + Tammes，数学）→ ⑤ 4 模式需 ≥ 4 采样点（**Nyquist 采样定理**，信息论）→ ⑥ **相干块 ≥ N_模式 l_P²**（**不等式** ✓）→ ⑦ 块内 4 自由度最大压缩 ⟹ 1 纳特/块（**额外假设**）→ ⑧ `S = A/(4l_P²)`（等号；第 52 轮已裁为半拟合 / 一致性）。⟹ **只有 ① 是公理；③④⑤ 全是数学与信息论** —— 这是框架里少见的「硬」链。
>
> ⭐ **② 本轮查出的口径缺口（C-14）**：第 ⑤ 环写「**4 模式需 ≥ 4 采样点**」（附「数值秩验证」），但**正四面体的 4 个方向在 3D 里线性相关**（`Σ n_a = 0`，数值 `[0,0,0]` 精确）。独立复算 `k×4` 采样矩阵的秩：
>
> | 模式基底 | k = 2 / 3 / 4 / 5 / 8 时的秩 |
> |---|---|
> | **正四面体 · 线性**（`n_a·p`） | 2 / 3 / **3** / **3** / **3** |
> | **随机 4 泛函**（与框架无关） | 2 / 3 / **3** / **3** / **3** |
> | 正四面体 · 绝对值 / 高斯 | 2 / 3 / 4 / 4 / 4 |
>
> ⟹ **「需 ≥ 4 采样点」依赖「模式如何定义」，而原文未写明**。若模式是**线性**泛函，独立维度只有 **3** ⟹ 下界应为 **3 个采样点**。⚠️ 这**不等于**该处有错：框架的「4 个方向模式」更可能指「4 个方向上的**连接状态**」（非线性 / 离散量）⟹ 那样确实可以 4 维。**缺的是口径，不是结论。**
>
> ⭐ **③ 口径分歧直接改变下界**：线性模式 ⟹ 相干块 ≥ 3l_P² ⟹ 尺度 ≥ **√3 l_P = 1.7321 l_P**；非线性模式 ⟹ ≥ 4l_P² ⟹ 尺度 ≥ **2.0000 l_P**。⟹ **保守可声称的是区间 `1.73 – 2.00 l_P`**（**不等式**；取等号还需第 ⑦ 环的「最大压缩」假设）。
>
> ⭐ **④ 尺度换算**：按「面元 = l_P²」的口径（表面 N = A/l_P² 个面元），icosphere(3)（642 顶点 / 1280 面 / 1920 边）给 **R = 10.0925 l_P**、**1-ring 平均边长 = 1.5227 l_P** ⟹ 第 66/67 轮在 1-ring 上数 Morse 谱 / 绕数**恰好在这个尺度附近**（略欠粗粒化，不改变结论）。第 66/67 轮的平滑核 σ = 0.55 rad ⟹ **5.55 l_P**（**更粗、保守安全**）；而 σ = 0.15 rad ⟹ 1.51 l_P，按框架口径**欠粗粒化**，那一档的数字不该用。
>
> ⭐ **⑤ 与第 70 轮的对接**：第 70 轮的「平滑 = 在大于 l_P 的尺度上读数」**精确化为「≥ 1.73 – 2.00 l_P」**。在**格距 = l_P** 的衬底上（§8.6.8 的设定），2 l_P 对应 **2×2 = 4 个面元** ⟹ 正好是「每 4 面元 1 个相干单元」（§4.8）。⟹ **两轮互补**：第 70 轮证「**平滑不是衬底产生的**」（负面），本轮证「**粗粒化尺度有下界且可算**」（正面）⟹ 合起来「**平滑来自观测者，而观测者的尺度下界是可算的**」。
>
> ⚠️ **⑥ 与已判死方向区分**（本轮的自我审查）：第 40 / 51 / 52 轮判死的是「**用衬底推观测者读数分辨率**」—— 那条路问的是**熵密度**（H/N，纳特/格点）、**要算衬底量**；本轮问的是**长度**（粗粒化尺度，l_P）、**只用数学（LST）+ 信息论（Nyquist）** ⟹ **不撞那条死**。⚠️ 但第 ⑦ 环（取等号）**正是第 52 轮裁决过的那一步** ⟹ 本轮**止步于不等式**，不重开。
>
> ⚠️ **五条诚实边界**：① 第 ② 环是**设定**（「方向管最细尺度 = l_P」标【本框架设定】）—— 整条链的第一环是公理、第二环是设定；② 第 ⑦ 环是**额外假设**，`S = A/(4l_P²)` 的**等号不因此成立**；③ 第 ⑤ 环的**口径未写明**（C-14）⟹ 下界是**区间**而非单值；④ `R = 10.09 l_P` 依赖「面元 = l_P²」这个口径，把它用在**弯曲球面**上是**类比**，不是严格推导；⑤ **本轮不给「观测者的读数算子」** —— 第 40 轮的三难仍然成立。

'''

EN_BLOCK = '''> **【v2.9 supplement (round 71: the observer's coarse-graining scale — the framework wrote this chain but left one caliber unstated)】** Round 70 said "smooth = read on a scale larger than l_P" without giving that scale. This round goes to find it; the conclusion is that **the framework has already written this derivation chain** (the theorem package of §4.10), that it **does close**, but that what it yields is an **inequality**. Script `_observer_scale_71.py` (**OS-1…OS-9, 9 pass / 0 fail**).
>
> **① Ring by ring** (each labelled by its nature): ① Planck-scale event stream (**axiom 1**) → ② the finest scale of a direction tube = l_P (**a setting of this framework**, §4.10) → ③ **direction cluster k ≥ 4** (**Theorem 1: Lusternik–Schnirelmann / Borsuk**, mathematics) → ④ four direction modes per surface element (③ + Tammes, mathematics) → ⑤ four modes need ≥ 4 sampling points (**Nyquist sampling theorem**, information theory) → ⑥ **coherence block ≥ N_mode l_P²** (**an inequality** ✓) → ⑦ maximal compression of the block's 4 degrees of freedom ⟹ 1 nat/block (**an extra assumption**) → ⑧ `S = A/(4l_P²)` (equality; already adjudicated in round 52 as half-fitting / consistency). ⟹ **Only ① is an axiom; ③④⑤ are pure mathematics and information theory** — this is a rare "hard" chain inside the framework.
>
> ⭐ **② A caliber gap found this round (C-14)**: ring ⑤ says "**four modes need ≥ 4 sampling points**" (with a "numerical rank check" attached), but **the tetrahedron's four directions are linearly dependent in 3D** (`Σ n_a = 0`, numerically `[0,0,0]`, exactly). Independently recomputing the rank of the `k×4` sampling matrix:
>
> | mode basis | rank at k = 2 / 3 / 4 / 5 / 8 |
> |---|---|
> | **tetrahedron · linear** (`n_a·p`) | 2 / 3 / **3** / **3** / **3** |
> | **random 4 functionals** (unrelated to the framework) | 2 / 3 / **3** / **3** / **3** |
> | tetrahedron · absolute value / Gaussian | 2 / 3 / 4 / 4 / 4 |
>
> ⟹ **"needs ≥ 4 sampling points" depends on how the modes are defined, and the original text does not say**. If the modes are **linear** functionals, the independent dimension is only **3** ⟹ the bound should be **3 sampling points**. ⚠️ This **does not** mean that passage is wrong: the framework's "four direction modes" more plausibly means "the **connection states** in four directions" (non-linear / discrete), for which four dimensions is indeed attainable. **What is missing is a caliber, not a conclusion.**
>
> ⭐ **③ The caliber split directly changes the bound**: linear modes ⟹ block ≥ 3l_P² ⟹ scale ≥ **√3 l_P = 1.7321 l_P**; non-linear modes ⟹ ≥ 4l_P² ⟹ scale ≥ **2.0000 l_P**. ⟹ **What can conservatively be claimed is the interval `1.73 – 2.00 l_P`** (**an inequality**; the equality additionally needs ring ⑦'s "maximal compression" assumption).
>
> ⭐ **④ Scale conversion**: under the caliber "surface element = l_P²" (surface has N = A/l_P² elements), icosphere(3) (642 vertices / 1280 faces / 1920 edges) gives **R = 10.0925 l_P** and a **mean 1-ring edge length of 1.5227 l_P** ⟹ the 1-ring Morse-spectrum / winding-number counting of rounds 66/67 sits **right around this scale** (slightly under-coarse-grained, which does not change the conclusion). Round 66/67's smoothing kernel σ = 0.55 rad ⟹ **5.55 l_P** (**coarser, conservatively safe**); whereas σ = 0.15 rad ⟹ 1.51 l_P is **under-coarse-grained** by the framework's own caliber, so numbers from that tier should not be used.
>
> ⭐ **⑤ Interface with round 70**: round 70's "smooth = read on a scale larger than l_P" is **sharpened to "≥ 1.73 – 2.00 l_P"**. On a substrate with **lattice spacing = l_P** (§8.6.8's setting), 2 l_P corresponds to **2×2 = 4 surface elements** ⟹ exactly "one coherence unit per 4 surface elements" (§4.8). ⟹ **The two rounds are complementary**: round 70 proved "**smoothness is not produced by the substrate**" (negative), this round proves "**the coarse-graining scale has a computable lower bound**" (positive) ⟹ together, "**smoothness comes from the observer, and the observer's scale has a computable lower bound**".
>
> ⚠️ **⑥ Distinction from the dead ends** (this round's self-audit): rounds 40 / 51 / 52 killed the route "**infer the observer's readout resolution from the substrate**" — that route asks about an **entropy density** (H/N, nats per site) and **requires computing substrate quantities**; this round asks about a **length** (the coarse-graining scale, in l_P) and uses **only mathematics (LST) + information theory (Nyquist)** ⟹ **it does not hit that dead end**. ⚠️ But ring ⑦ (taking the equality) **is exactly the step adjudicated in round 52** ⟹ this round **stops at the inequality** and does not reopen it.
>
> ⚠️ **Five honest boundaries**: ① ring ② is a **setting** ("the finest scale of a direction tube = l_P", labelled 【a setting of this framework】) — the chain's first ring is an axiom and its second is a setting; ② ring ⑦ is an **extra assumption**, so the **equality** of `S = A/(4l_P²)` **does not follow**; ③ ring ⑤'s **caliber is unstated** (C-14) ⟹ the bound is an **interval** rather than a single value; ④ `R = 10.09 l_P` relies on the caliber "surface element = l_P²", and applying it to a **curved sphere** is an **analogy**, not a rigorous derivation; ⑤ **this round does not supply the "observer's readout operator"** — round 40's trilemma still stands.

'''

sub_once(ZH, "### 8.3 暗物质叠加模型", ZH_BLOCK + "### 8.3 暗物质叠加模型", "ZH §8.2 末插入第 71 轮块")
sub_once(EN, "### 8.3 Dark-matter superposition model",
         EN_BLOCK + "### 8.3 Dark-matter superposition model", "EN §8.2 末插入第 71 轮块")

# ── ② 在 §4.10 的 Nyquist 行加口径注（指回第 71 轮块）
ZH_NYQ = "Nyquist 采样定理：4 模式需 ≥4 采样点（数值秩验证：4 模式×2/3 点秩 2/3 欠采样、×4 点秩 4 满秩）"
EN_NYQ = ("Nyquist sampling theorem: 4 modes require ≥4 sampling points "
          "(numerical rank check: 4 modes × 2/3 points give rank 2/3, under-sampled; ×4 points give rank 4, full rank)")
if ZH.count(ZH_NYQ) == 1:
    sub_once(ZH, ZH_NYQ,
             ZH_NYQ + "。⚠️**【第 71 轮口径注（C-14）】**「4 模式」的**定义未写明**：正四面体 4 方向"
             "**线性相关**（`Σ n_a = 0`）⟹ 若模式为**线性**泛函则独立维度只 **3**，下界应为 **3 个采样点**；"
             "要得 4，模式须为**非线性**（如「4 个方向上的连接状态」）。⟹ 相干块下界是"
             "**区间 3 – 4 l_P²**（尺度 **√3 – 2 l_P**），详见 §8.2 第 71 轮块",
             "ZH §4.10 加口径注")
else:
    print("  [--] ZH §4.10 Nyquist 行命中 {} 次，跳过".format(ZH.count(ZH_NYQ)))
if EN.count(EN_NYQ) == 1:
    sub_once(EN, EN_NYQ,
             EN_NYQ + ". ⚠️ **[Round-71 caliber note (C-14)]** The **definition of \\\"4 modes\\\" is not stated**: the tetrahedron's "
             "four directions are **linearly dependent** (`Σ n_a = 0`) ⟹ if the modes are **linear** functionals the independent "
             "dimension is only **3** and the bound should be **3 sampling points**; obtaining 4 requires **non-linear** modes "
             "(e.g. \\\"the connection states in four directions\\\"). ⟹ the coherence-block bound is the **interval 3 – 4 l_P²** "
             "(scale **√3 – 2 l_P**); see the round-71 block in §8.2",
             "EN §4.10 caliber note")
else:
    print("  [--] EN §4.10 Nyquist 行命中 {} 次，跳过".format(EN.count(EN_NYQ)))

print()
print("通过 {} 项，失败 {} 项".format(OK, BAD))
