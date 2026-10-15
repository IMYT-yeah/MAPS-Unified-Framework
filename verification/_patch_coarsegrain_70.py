# -*- coding: utf-8 -*-
"""第 70 轮 · 论文补丁（中英同步）：§8.2 末尾（§8.3 之前）插入【第 70 轮】块。"""
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
        print("  [XX] {:<28} 命中 {} 次 —— 拒绝".format(tag, n))
        BAD += 1
        return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    OK += 1
    print("  [OK] {:<28} 已改".format(tag))


ZH_BLOCK = '''> **【v2.9 补充（第 70 轮：粗粒化截断与 Φ 的质量 —— 两个开口为何不能共用一个尺度）】** 本轮是 **I-18（第 67 轮）＋ I-17（第 62 轮）的合并轮**。合并理由：§4.5b 明写 Φ 的数学身份是**谱作用** `S = Tr f(D²/Λ²)`（**自带截断 Λ**），而第 423 行给出「粗粒化」的**群论定义** ⟹ 若两者共用同一个截断，就是一条机制 —— 这是**可判定**的。脚本 `_coarsegrain_70.py`（**CG-1…CG-10，11 项 0 失败**）。
>
> **① 框架里「粗粒化 / 截断」共 10 个实现，口径逐一表列**：① 群论粗粒化（第 423 行「G 的轨道划分就是最大的 tick 不变粗粒化」，**无尺度**）｜② 宏观不可逆的来源（第 1317 行「底层无熵产生，宏观不可逆只能来自粗粒化」）｜③ **普朗克截断**（第 322 行「截断 = 普朗克（公理 1 自然给出）」，尺度 l_P）｜④ **谱作用截断 Λ**（第 791 行，**Λ 未给值**）｜⑤ F2 降标机制（第 311 行 `δ = √(R·l_P)`）｜⑥ `Q_res`（第 674 行，第 56 轮命名「粗粒化截断能标」）｜⑦ 概率归一化能标 `E_c`（第 1090 行，**恒等式**，C-4）｜⑧ **Φ⁴ 势的 μ**（第 984 行，**μ 是输入**）｜⑨ 强度截断 `r_c = GM/c²`（第 1585 行）｜⑩ 玻尔兹曼弱场截断（第 187/261 行）。⟹ **10 个里只有 ④ 与 ⑧ 是纯输入 —— 而恰恰这两个决定 Φ 的质量。**
>
> **② 判据：两者结构上不同** —— 群论粗粒化**只用置换群、算法里不含任何量纲量**（`_tickgroup.gens_correct` 里浮点字面常数 = **0 个**），而截断类**每一个都必须带一个尺度**（R、1 meV、GM/c²、l_P）⟹ **一个组合、一个度量，不可能是同一个东西**。
>
> **③ I-18 的答案：平滑层不是衬底产生的** —— 从**极端平滑**初态（`z ∈ {0,1,2}` 全满）出发跑 tick（(2,2,6)，z 线长 6）：块密度方差 **B 在 2 步内从 0.250000 衰减到 0.006944**（随机基线 0.020833）；同一 tick 轨道内 B 极差 **0.250000**、相邻对同值比例 S 极差 **0.590909**、`|d₀ − d₁|` 从 **1.0000 降到 0.0000** ⟹ **tick 演化摧毁平滑，不产生平滑**。⟹ **平滑 = 「在大于 l_P 的尺度上读数」**（本轮的解释，非框架原文）—— 与本节第 322 行的「截断 = 普朗克」及 B5 的观测者分辨率**相容**；而第 66/67 轮用的高斯核 σ = 0.55 弧度是**玩具模型的外部选择**。
>
> **④ I-17 的加固 ＋ 一个新的可判别结构**：Φ 的质量挂在 ④ 与 ⑧ 两个**纯输入**上 ⟹ **公设上移未解决**。⭐ 但反解 F2 降标机制（`E(R) = √(ℏc·E_P/R)`，全 eV 制、ℏc = 1.97327×10⁻⁷ eV·m）给出**质量档位与力程的对应**：
>
> | `m_Φ` 取 | 力程 λ = ℏc/m | 在第五力搜索窗口（10⁻⁶ → 3.1×10²⁰ m）内？ |
> |---|---|---|
> | 弦网标量扇区 `Δ_标量 = 0.41 J` | **0.813 l_P** | ❌ 差 **28.9** 个数量级 |
> | 粗粒化截断 @ `E_c`（1.0181 meV） | **0.1938 mm** | ✅ |
> | 粗粒化截断 @ `E(R_H)`（4.1894 meV） | **0.0471 mm** | ✅ |
> | 普朗克（公理 1） | 1.000 l_P | ❌ 差 **28.8** 个数量级 |
>
> ⟹ **(a) 与 (b) 的力程比 = 1.475×10³¹，即差 31.2 个数量级** —— 「第五力能不能被看到」取决于 Φ 的质量取哪一档。⚠️ **但力程在窗口内只是必要条件**（0.05–0.2 mm 的**与引力同强度**的标量力早已被 Eöt-Wash 类实验排除；未被排除的只剩**极弱耦合**窄带），而**耦合强度正是 I-17 未给的另一半** ⟹ **(b)/(c) 仍不是可检验预言**。
>
> **⑤ 副产品（反解）**：`E(R) = 1 meV` ⟹ **R = 16.93 R_H**（交叉验证：`(4.19/1.0181)² = 16.93` ✓）。⚠️ 但 1 meV 是**恒等式**（C-4）、4.19 meV 与标准暗能量能标 `√(M_Pl H₀)` **是同一个组合**（C-6）⟹ **这两个 meV 都不是新成果**。
>
> ⚠️ **七条诚实边界**：① **「m_Φ = Λ」是假设**（四类判定 = 半拟合），框架**从未**把 Φ 的质量与具体能标连起来；② 「平滑 = 在大于 l_P 的尺度上读数」是本轮的**解释**，**不是**框架原文；③ **(2,2,6) 仍是小格点**，未做 L ≥ 8 外推；④ **本轮未新增演化方程**（用的是框架原有的 tick —— 与第 67 轮不同）；⑤ 力程在窗口内 ≠ 可观测；⑥ 本轮的「31.2 个数量级」是**两个候选之比**，与第 62 轮的「28.9–55.4」是**候选与窗口的距离** —— **口径不同，不要混引**；⑦ **实现层发现（须记）**：**(2,2,4) 的 z 线长 = 4 让「块方差」退化成 tick 不变量**（相位 1 匹配 `(1 2)(3 0)` 恰好把「被 z 配对切开的两块」整体互换 ⟹ `(d₀ − 0.5)²` 不变，实测极差 = 0）⟹ 以后凡用「块方差」做判据，**必须避开 z 线长 = 4**。

'''

EN_BLOCK = '''> **【v2.9 supplement (round 70: the coarse-graining cutoff and the mass of Φ — why the two gaps cannot share one scale)】** This round **merges I-18 (round 67) with I-17 (round 62)**. Reason for merging: §4.5b states that Φ's mathematical identity is the **spectral action** `S = Tr f(D²/Λ²)` (**which carries a cutoff Λ**), while line 423 gives a **group-theoretic definition** of "coarse-graining" ⟹ if the two shared one and the same cutoff, they would be one mechanism — and that is **decidable**. Script `_coarsegrain_70.py` (**CG-1…CG-10, 11 pass / 0 fail**).
>
> **① Ten implementations of "coarse-graining / cutoff" in the framework** (with their calibers): ① group-theoretic coarse-graining (line 423, "the orbit partition of G is the maximal tick-invariant coarse-graining", **no scale**) | ② the source of macroscopic irreversibility (line 1317, "the bottom layer produces no entropy, so macroscopic irreversibility can only come from coarse-graining") | ③ **Planck cutoff** (line 322, "cutoff = Planck (given naturally by axiom 1)", scale l_P) | ④ **spectral-action cutoff Λ** (line 791, **Λ is not given**) | ⑤ F2 down-scaling (line 311, `δ = √(R·l_P)`) | ⑥ `Q_res` (line 674, named "coarse-graining cutoff scale" in round 56) | ⑦ probability-normalization scale `E_c` (line 1090, an **identity**, C-4) | ⑧ **the μ of the Φ⁴ potential** (line 984, **μ is an input**) | ⑨ rigidity cutoff `r_c = GM/c²` (line 1585) | ⑩ Boltzmann weak-field cutoff (lines 187/261). ⟹ **Only ④ and ⑧ are pure inputs — and precisely these two fix the mass of Φ.**
>
> **② The criterion: the two are structurally different** — group-theoretic coarse-graining **uses only a permutation group and contains no dimensional quantity whatsoever** (the implementation `_tickgroup.gens_correct` contains **0** floating-point literals), whereas **every** cutoff must carry a scale (R, 1 meV, GM/c², l_P) ⟹ **one is combinatorial, the other metric; they cannot be the same thing**.
>
> **③ The answer to I-18: the smooth layer is not produced by the substrate** — starting from a **maximally smooth** initial state (`z ∈ {0,1,2}` fully occupied) and running ticks ((2,2,6), z-line length 6): the block-density variance **B decays from 0.250000 to 0.006944 within 2 steps** (random baseline 0.020833); within a single tick orbit the spread of B is **0.250000**, that of the nearest-neighbour equal-value fraction S is **0.590909**, and `|d₀ − d₁|` falls from **1.0000 to 0.0000** ⟹ **tick evolution destroys smoothness; it does not create it**. ⟹ **"Smooth" = "read on a scale larger than l_P"** (an interpretation of this round, **not** the framework's own wording) — **compatible** with line 322 ("cutoff = Planck") and with B5's observer resolution; the Gaussian kernel σ = 0.55 rad used in rounds 66/67 is an **external choice of the toy model**.
>
> **④ I-17 reinforced, plus a new discriminable structure**: the mass of Φ hangs on the two **pure inputs** ④ and ⑧ ⟹ **the postulate shift is not resolved**. ⭐ But inverting the F2 down-scaling law (`E(R) = √(ℏc·E_P/R)`, all in eV with ℏc = 1.97327×10⁻⁷ eV·m) gives a **correspondence between mass tier and force range**:
>
> | `m_Φ` taken as | force range λ = ℏc/m | inside the fifth-force search window (10⁻⁶ → 3.1×10²⁰ m)? |
> |---|---|---|
> | string-net scalar sector `Δ_scalar = 0.41 J` | **0.813 l_P** | ❌ off by **28.9** orders of magnitude |
> | coarse-graining cutoff @ `E_c` (1.0181 meV) | **0.1938 mm** | ✅ |
> | coarse-graining cutoff @ `E(R_H)` (4.1894 meV) | **0.0471 mm** | ✅ |
> | Planck (axiom 1) | 1.000 l_P | ❌ off by **28.8** orders of magnitude |
>
> ⟹ **The range ratio between (a) and (b) is 1.475×10³¹, i.e. 31.2 orders of magnitude** — whether a fifth force can be seen depends on which tier Φ's mass takes. ⚠️ **But being inside the window is only a necessary condition** (a scalar force of gravitational strength at 0.05–0.2 mm has long been excluded by Eöt-Wash-type experiments; only a **very weakly coupled** narrow band survives), and **the coupling strength is precisely the other half that I-17 does not give** ⟹ **(b)/(c) are still not testable predictions**.
>
> **⑤ A by-product (inversion)**: `E(R) = 1 meV` ⟹ **R = 16.93 R_H** (cross-check: `(4.19/1.0181)² = 16.93` ✓). ⚠️ But 1 meV is an **identity** (C-4), and 4.19 meV is **the same combination** as the standard dark-energy scale estimate `√(M_Pl H₀)` (C-6) ⟹ **neither meV is a new result**.
>
> ⚠️ **Seven honest boundaries**: ① **"m_Φ = Λ" is an assumption** (four-way verdict = half-fitting); the framework has **never** tied Φ's mass to any concrete scale; ② "smooth = read on a scale larger than l_P" is this round's **interpretation**, **not** the framework's own statement; ③ **(2,2,6) is still a small lattice**, with no L ≥ 8 extrapolation; ④ **this round introduces no new evolution equation** (it uses the framework's own tick — unlike round 67); ⑤ being inside the range window ≠ being observable; ⑥ this round's "31.2 orders of magnitude" is the ratio **between two candidates**, whereas round 62's "28.9–55.4" is the distance **from a candidate to the window** — **different calibers, do not mix**; ⑦ **implementation-level finding (must be recorded)**: **at (2,2,4) the z-line length 4 makes "block variance" degenerate into a tick invariant** (the phase-1 matching `(1 2)(3 0)` happens to swap the two blocks carved out by the z-pairing as a whole ⟹ `(d₀ − 0.5)²` is invariant, measured spread = 0) ⟹ any future criterion using "block variance" **must avoid z-line length 4**.

'''

sub_once(ZH, "### 8.3 暗物质叠加模型", ZH_BLOCK + "### 8.3 暗物质叠加模型", "ZH §8.2 末插入第 70 轮块")
sub_once(EN, "### 8.3 Dark-matter superposition model",
         EN_BLOCK + "### 8.3 Dark-matter superposition model", "EN §8.2 末插入第 70 轮块")

print()
print("通过 {} 项，失败 {} 项".format(OK, BAD))
