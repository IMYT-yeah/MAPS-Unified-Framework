# -*- coding: utf-8 -*-
"""第 65 轮 · 论文补丁（中英同步）：§8.6.7 块链末尾插入【第 65 轮】块。"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

OK = 0
BAD = 0


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


# ══════════════════════════ 中文块 ══════════════════════════
ZH_BLOCK = r'''> **【v2.9 补充（第 65 轮：tick 的「像」与真随机白噪声 —— 九条判据的分界）】** 动机：模拟器（`宇宙模拟器.html`）的界面「看起来与电视雪花屏一模一样」。本轮把这个观察做成**可判定**的问题：**空格点的 tick 演化构型，与 i.i.d. 白噪声在哪些统计量上分得开？**（脚本 `_snow_65.py`，SN-1…SN-9，**11 项 0 失败**）
>
> **九条判据**（格点 12³ = 1728 个位点、密度 1/2；tick 构型为**真跑 tick 演化 30 步**后的末态）：
>
> | 档 | 判据 | tick | 白噪声 | 判定 |
> |---|---|---|---|---|
> | **单帧 / 局部** | 单点密度 | 0.500 | 0.499 | ❌ 相同 |
> | | 最近邻两点关联 C(1) | +1.0×10⁻⁴ | +5.1×10⁻⁴ | ❌ **信号 < 噪声基线 6.2×10⁻⁴** |
> | | 块密度方差（粗粒化） | 3.642×10⁻³ | 3.990×10⁻³ | ❌ 差 **8.7%** |
> | | **帧间逐位变化量 Δ** | 0.503 | 0.500 | ❌ **相同**（见下） |
> | **时间 / 守恒量** | **轴对齐的线级重排** | **1.0000** | **0.1802** | ✅ **结构性恒等 vs 概率巧合** |
> | | **k（亮点数）** | 极差 **0** | 极差 **104** | ✅ 守恒 vs 不守恒 |
> | | 可逆性 | 双射 + 对合 | 不可逆 | ✅ 可分 |
> | | **有序初态的混合时间** | **62 步** | **1 步** | ✅ 差 **62 倍** |
> | | **混合时间的尺寸标度** | **τ ∝ L²** | τ = 1 | ✅ 可分 |
>
> **分界干净**：前 4 条**全在「单帧 / 局部」、全部不可分**；后 5 条**全在「时间 / 守恒量」、全部分得开**。
> ⟹ **通则**：判别「确定 vs 随机」**不要比空间快照，要比时间序列与守恒量** —— 快照只是系综的一个样本，而**系综分布在两种情形下可以完全相同**，能被分开的东西必然住在**路径**里。
> ⚠️ 其中「轴对齐的线级重排」是最硬的一条：它对 tick 是**结构性恒等**（沿交换轴的**每条线**上亮点数必不变，因为交换只在一条线内部发生），对白噪声只是**概率巧合**（≈ `C(24,12)/2²⁴` = 0.1612）。
>
> **τ ∝ L² 的数据点**（有序初态 ⟹ |左半密度 − 0.5| 首次跌破 2× 超几何基线）：L = 6 / 8 / 10 给 τ = 15 / 23 / 46，**τ/L² = 0.42 / 0.36 / 0.46 ⟹ 比值稳定**（L = 4 太小，未计入）。
> **机理解释**：tick 交换的是**相邻配对** ⟹ 它是**局域扩散**步骤，不是全局重抽（若是后者，τ 应与 L 无关）。
> ⚠️ 这与 §4.2 的 `R_mix = l_P√(t/t_P)` 是**同一个标度**（`R² ∝ t` ⟺ `t ∝ L²`），但**来源不同**（这里是置换链的弛豫，那里是扩散方程）⟹ **不声称深层统一**（与第 59 轮的同名保留一致）。
>
> ⚠️ **本轮的一个负面发现（自己的预测被推翻）**：原推理为「tick 只动一个轴 ⟹ 1/3 的机会；且沿该轴配对交换，一半的配对『换了等于没换』⟹ `Δ_tick = 1/4`，比白噪声的一半还小」。**实测 0.503 ≈ 0.500，相同。**
> 错因：tick 的**每一个位置都必然被改写为「它的伙伴的旧值」**（相位只决定**伙伴是谁**，而**伙伴永远 ≠ 自己**）⟹ `P(值改变) = P(伙伴值不同) = 1/2`。
> ⟹ **「逐位变化率」不是判据**（登记 **N-24**）。
>
> ⚠️ **诚实边界三条**：① 浏览器与脚本里的「真随机」只能是**伪随机**（第 44 轮的硬限制）⟹ 严格说，本轮比较的是「高质量的确定性**置换**」vs「低质量的确定性**重抽**」，**不是**「确定性 vs 真随机」；这不影响时间侧五条判据（它们都是**结构性**的）。② 「人眼不可分」只用**块密度方差**做了操作化（差 8.7%），**未**建立视觉系统的信息论模型（真实的视觉系统含稀疏采样、对比度响应、运动检测，比「块平均」复杂）。③ 本轮**不**裁断「tick 是不是更本质的选择」—— 那是 §8.6.7 的公设，不是本轮的结论。
> ⟹ **与第 43 轮的口径一致**：「**无信息丢失**说的是**状态**，『**熵增**』说的是**我们对状态的无知**」—— 本轮的九条判据正是这句话的**可视图象**：状态侧（k、可逆性、线级重排）**严格守恒**，而系综侧（粗粒化读数）用 **62 步**才均匀。
> ⟹ 附：模拟器新增第 ④ 面板「雪花屏对照 ★」（左 tick / 右白噪声，密度相同，含「有序初态」按钮）；面板级测试 `_sim_snow_test.js`（**6 项 0 失败**）。

'''

sub_once(ZH, "\n\n**【诚实边界（8.6.7）】**",
         "\n\n" + ZH_BLOCK + "**【诚实边界（8.6.7）】**",
         "ZH §8.6.7 插入第 65 轮块")

# ══════════════════════════ 英文块 ══════════════════════════
EN_BLOCK = r'''> **【v2.9 supplement (round 65: the tick's "image" versus true white noise — the nine-criterion divide)】** Motivation: the simulator's canvas "looks exactly like TV snow". This round turns that observation into a **decidable** question: **on which statistics do tick-evolved substrate configurations and i.i.d. white noise separate?** (script `_snow_65.py`, SN-1…SN-9, **11 pass / 0 fail**)
>
> **The nine criteria** (lattice 12³ = 1728 sites, density 1/2; the tick configurations are the **actual end states after 30 ticks**, not random draws):
>
> | Tier | Criterion | tick | white noise | Verdict |
> |---|---|---|---|---|
> | **single frame / local** | single-site density | 0.500 | 0.499 | ❌ identical |
> | | nearest-neighbour two-point correlation C(1) | +1.0×10⁻⁴ | +5.1×10⁻⁴ | ❌ signal < noise floor 6.2×10⁻⁴ |
> | | block-density variance (coarse-graining) | 3.642×10⁻³ | 3.990×10⁻³ | ❌ 8.7% apart |
> | | **frame-to-frame bit-flip fraction Δ** | 0.503 | 0.500 | ❌ **identical** (see below) |
> | **time / conserved quantities** | **axis-aligned line-level rearrangement** | **1.0000** | **0.1802** | ✅ structural identity vs coincidence |
> | | **k (number of lit sites)** | range **0** | range **104** | ✅ conserved vs not |
> | | reversibility | bijective + involutive | irreversible | ✅ separable |
> | | **mixing time from an ordered initial state** | **62 steps** | **1 step** | ✅ 62× apart |
> | | **size scaling of the mixing time** | **τ ∝ L²** | τ = 1 | ✅ separable |
>
> **The divide is clean**: the first four live **entirely in "single frame / local" and are all inseparable**; the last five live **entirely in "time / conserved quantities" and are all separable**.
> ⟹ **Rule of thumb**: to discriminate "deterministic vs random", **do not compare spatial snapshots — compare time series and conserved quantities**: a snapshot is a single sample from the ensemble, and **ensemble distributions can be identical in both cases**; whatever separates them must live in the **path**.
> ⚠️ The hardest of the nine is "axis-aligned line-level rearrangement": for tick it is a **structural identity** (the number of lit sites on **every line** along the swapped axis must be preserved, because the swap happens strictly inside one line), whereas for white noise it is only a **probabilistic coincidence** (≈ `C(24,12)/2²⁴` = 0.1612).
>
> **The τ ∝ L² data points** (ordered initial state ⟹ |left-half density − 0.5| first drops below 2× the hypergeometric floor): L = 6 / 8 / 10 give τ = 15 / 23 / 46, so **τ/L² = 0.42 / 0.36 / 0.46 ⟹ stable** (L = 4 is too small and was excluded).
> **Mechanism**: tick swaps **adjacent pairs** ⟹ it is a **local diffusive** step, not a global redraw (a global redraw would give a τ independent of L).
> ⚠️ This is the **same scaling** as §4.2's `R_mix = l_P√(t/t_P)` (`R² ∝ t` ⟺ `t ∝ L²`), but from a **different source** (relaxation of a permutation chain versus a diffusion equation) ⟹ **no claim of deep unification** (same reservation as round 59).
>
> ⚠️ **A negative finding of this round (my own prediction refuted)**: the reasoning was "tick moves only one axis ⟹ 1/3 chance; and since the swap is done in pairs, half the pairs 'swap to no effect' ⟹ Δ_tick = 1/4, half as large as white noise". **Measured 0.503 ≈ 0.500 — identical.**
> Why: **every site is necessarily rewritten** as "its partner's old value" (the phase only decides **who the partner is**, and **the partner is never the site itself**) ⟹ `P(value changes) = P(partner differs) = 1/2`.
> ⟹ **the bit-flip fraction is not a criterion** (registered as **N-24**).
>
> ⚠️ **Three honest boundaries**: ① "true randomness" in a browser or a script can only be **pseudo-random** (the hard limit of round 44) ⟹ strictly, this round compares a "high-quality deterministic **permutation**" against a "low-quality deterministic **redraw**", **not** "deterministic vs truly random"; this does not affect the five time-side criteria (all of them are **structural**). ② "The eye cannot tell" was operationalized only through **block-density variance** (8.7% apart); **no** information-theoretic model of the visual system was built (the real system involves sparse sampling, contrast response and motion detection, which are richer than a block average). ③ This round **does not** adjudicate "whether tick is the more fundamental choice" — that is the postulate of §8.6.7, not a result here.
> ⟹ **Consistent with round 43**: "**no information loss**" refers to the **state**, while "'**entropy growth**' refers to **our ignorance of the state**" — the nine criteria are the **visual image** of that sentence: the state side (k, reversibility, line-level rearrangement) is **strictly conserved**, whereas the ensemble side (coarse-grained readout) takes **62 steps** to homogenize.
> ⟹ Addendum: the simulator has a new panel ④ "snow-screen comparison ★" (tick left / white noise right, identical density, with an "ordered initial state" button); the panel-level test `_sim_snow_test.js` gives **6 pass / 0 fail**.

'''

sub_once(EN, "\n\n**【Honest boundary (8.6.7)】**",
         "\n\n" + EN_BLOCK + "**【Honest boundary (8.6.7)】**",
         "EN §8.6.7 插入第 65 轮块")

print()
print("通过 {} 项，失败 {} 项".format(OK, BAD))
