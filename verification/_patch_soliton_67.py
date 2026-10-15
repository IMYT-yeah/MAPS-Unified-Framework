# -*- coding: utf-8 -*-
"""第 67 轮 · 论文补丁（中英同步）：§8.2 H1–H4 之后插入【第 67 轮】块。"""
import io, os
BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
OK = BAD = 0
def sub_once(path, old, new, tag):
    global OK, BAD
    t = io.open(path, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        print("  [XX] {:<26} 命中 {} 次 —— 拒绝".format(tag, n)); BAD += 1; return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    OK += 1
    print("  [OK] {:<26} 已改".format(tag))

ZH_BLOCK = '''> **【v2.9 补充（第 67 轮：孤子的动力学 —— 涡心的运动、湮灭与拓扑修正）】** 第 66 轮留下「湮灭是抽象配对、未做动力学」。本轮补上，并**先声明性质**：引文取证显示，**「图热流 / Dirichlet 能量 / 调和映照 / Laplace–Beltrami / 平行移动 / 联络 / 时间演化 / 演化方程 / 梯度流」在本论文中各 0 处** ⟹ **本轮的动力学是新增假设，不是框架原有的**（框架自己规定的时间演化只有 §8.6.7 的 tick 置换；四个哈密顿量都是静态的）。可声称的只有一处相容性：**tick 是置换 ⟹ 保拓扑荷**，而本轮的演化也**严格保拓扑荷**。脚本 `_vortex_67.py`（VX-1…VX-9，**9 项 0 失败**）、`_vortex_point_67.py`（VP-1…VP-7，**7 项 0 失败**）。
>
> **① ⭐ 裸绕数和不是 χ，而是 3χ**（对本节 H1 的数值精确化）：icosphere(3) + 测地平行移动下，**裸 Σ w_i 恒为 +6 = 3χ**（12 个随机轴 × subdiv 2/3/4，极差 1.8×10⁻¹⁵）；**扣掉曲率后 `Σ(w_i − 2K_i/2π) = χ = 2`**（精确到 1e-15）。多出的 2χ 恰是离散曲率：Gauss–Bonnet 给 `ΣK_i = 2πχ`（面板实测 `ΣK_i = 4π`）⟹ `裸 Σ = χ + 2χ = 3χ`。
> ⚠️ **适用范围**：修正式**只对「平滑、且零点不落在格点上」的场成立** —— 反例：`∇p_z` 的零点恰在南北极顶点上时修正给 **−2**、`x̂×p` 给 **0**。判据必须连条件一起写，否则是选择性标定。
> ⚠️ 与第 66 轮同族：**「离散绕数」这个量本身不等于任何拓扑不变量，除非做修正。**
>
> **② 为什么第 66 轮用绕数错、本轮对**（必须显式论证，否则会被本节第 1105 行反过来打）：第 66 轮的伪影来自 **∇f 的模长在非零点可以任意小**（它不是归一化的场），单位化把「模长小」放大成「方向疯狂转弯」，其尺度与 1-ring 可比 ⟹ 离散绕数失效。本轮的 `v` **本身就是单位切向量场**（模恒为 1），**不存在这个放大机制** ✓（前提仍是 1-ring 尺度上的平滑 —— 即「孤子化」）。
>
> **③ 动力学确实让涡心自己湮灭**（演化 = 切丛内图热流 `v ← (1−α)v + α·⟨v'⟩`，α = 0.3，**不是抽样配对**）：
>
> | 初态 | 涡心数（t = 0 / 20 / 50 / 100 / 200） |
> |---|---|
> | 噪声层 | **299 → 72 → 40 → 22 → 6**（−98%） |
> | 平滑层 | 18 → 18 → … → 6（t ≈ 1000） |
> | **T²（χ = 0）** | 130 → 12 → **0**（Σ 的最大绝对值 = **1.3×10⁻¹⁵**，严格零） |
>
> ⭐ **5 个种子 × 两种初态 × 2000 步，全部收敛到同样的 6 个（+1）涡心** —— 与初值、种子、时程都无关。
> 点粒子层（过阻尼涡旋 `dr_i/dt = q_i Σ_j q_j (r_i−r_j)/|r_i−r_j|²`）给**解析标度**：一对 (+1,−1) 的相遇时间 **t* = r₀²/4**（五档全中，相对差 < 0.03%），**d(r²)/dt 异号 −4、同号 +4（完全对称）**；噪声持续产生下**净荷恒为 Δ**。
> ⚠️ 与 §4.2 的 `R_mix = l_P√(t/t_P)` 取**同一标度**（`R² ∝ t`）但**来源不同**（扩散方程 vs 过阻尼涡旋运动）⟹ **不声称深层统一**。
>
> **④ 两轮独立得到同一结论：拓扑荷只在平滑层上定义**：第 66 轮（逐点独立随机场给 Σ = +9 ≠ 2）；第 67 轮（**噪声层裸 Σ ∈ [−5, +4]**，40 次扫描均值 +0.35／std 2.40 —— **根本没有拓扑荷**；平滑层才有）。⟹ **§2.3「孤子化」是必需的**；⚠️ 但其**机制本轮仍未从第一性推出**（只验证了必要性）。
>
> **⑤ 不构成第三条成果**：本节第 1103 行已把「方向场的 Σ 指数 = χ」与「弦网的 `Π_v A_v = 1`」登记为**同一个拓扑守恒的两种实现**，明写「不是两条独立成果」⟹ 本轮**只是给同一守恒补上动力学**，不新增计数。
>
> ⚠️ **六条诚实边界**：① 动力学是**新增假设**（0 处检索）；② 裸绕数 = 3χ，修正式**有适用范围**；③ **守恒是「拓扑量子级的近似」** —— Σw 是精确整数（40/40），但**逐步严格相同 0/40**、极差 ≤ 2 者 39/40、众数 = 终值者 39/40（涡心跳跃落在棱上时读单步 ±1 抖动，下一步复原，**不是漂移**）；且「严格逐步相同」与「涡心数下降」**互斥**（同时成立 0/40）；④ 种子无关性是**演化的产物**（t = 0 时有 2/5 种子读 5）；⑤ 噪声层无拓扑荷；⑥ **稳定 ≠ 动力学稳定** —— 证的是「拓扑上抹不掉」（必要），不是「抗任意微扰」（充分）。

'''

EN_BLOCK = '''> **【v2.9 supplement (round 67: soliton dynamics — vortex motion, annihilation, and a topological correction)】** Round 66 left open "annihilation is an abstract pairing; no dynamics was done". This round supplies it, and **states its nature first**: a citation sweep shows that "**graph heat flow / Dirichlet energy / harmonic map / Laplace-Beltrami / parallel transport / connection / time evolution / evolution equation / gradient flow**" occur **0 times each** in this paper ⟹ **the dynamics used here is a NEW assumption, not something the framework already had** (the framework's own time evolution is only the §8.6.7 tick permutation; all four Hamiltonians are static). The only claim of compatibility: **the tick is a permutation ⟹ it preserves topological charge**, and the evolution used here **also strictly preserves it**. Scripts `_vortex_67.py` (VX-1…VX-9, **9 pass / 0 fail**), `_vortex_point_67.py` (VP-1…VP-7, **7 pass / 0 fail**).
>
> **① ⭐ The bare winding-number sum is not χ but 3χ** (a numerical sharpening of H1 in this subsection): on icosphere(3) with geodesic parallel transport, **the bare Σ w_i is identically +6 = 3χ** (12 random axes × subdiv 2/3/4, spread 1.8×10⁻¹⁵); **after subtracting curvature, `Σ(w_i − 2K_i/2π) = χ = 2`** (to 1e-15). The extra 2χ is exactly the discrete curvature: Gauss–Bonnet gives `ΣK_i = 2πχ` (the panel measures `ΣK_i = 4π`) ⟹ `bare Σ = χ + 2χ = 3χ`.
> ⚠️ **Scope**: the corrected formula **holds only for fields that are smooth AND whose zeros do not fall on lattice vertices** — counterexamples: for `∇p_z` with its zero exactly at a pole the correction gives **−2**, and `x̂×p` gives **0**. The criterion must state its conditions, or it becomes selective calibration.
> ⚠️ Same family as round 66: **"discrete winding number" is by itself not a topological invariant unless corrected.**
>
> **② Why the winding number was wrong in round 66 but right here** (this must be argued explicitly, or line 1105 of this subsection can be quoted back against it): round 66's artefacts came from **the modulus of ∇f being arbitrarily small away from zeros** (it is not a normalized field); normalizing magnifies "small modulus" into "wildly turning direction", at a scale comparable to the 1-ring ⟹ the discrete winding number fails. Here `v` **is itself a unit tangent vector field** (modulus identically 1), so **that magnification mechanism does not exist** ✓ (the precondition is still smoothness at the 1-ring scale — i.e. "solitonization").
>
> **③ The dynamics really does make vortices annihilate by themselves** (evolution = the graph heat flow inside the tangent bundle, `v ← (1−α)v + α·⟨v'⟩`, α = 0.3, **not a sampled pairing**):
>
> | Initial state | Vortex count (t = 0 / 20 / 50 / 100 / 200) |
> |---|---|
> | noisy layer | **299 → 72 → 40 → 22 → 6** (−98%) |
> | smooth layer | 18 → 18 → … → 6 (t ≈ 1000) |
> | **T² (χ = 0)** | 130 → 12 → **0** (maximum absolute value of Σ = **1.3×10⁻¹⁵**, strictly zero) |
>
> ⭐ **5 seeds × 2 initial layers × 2000 steps all converge to the same 6 (+1) vortices** — independent of initial state, seed and duration.
> The point-particle layer (overdamped vortices, `dr_i/dt = q_i Σ_j q_j (r_i−r_j)/|r_i−r_j|²`) gives an **analytic scaling**: the meeting time of a (+1,−1) pair is **t* = r₀²/4** (five cases, relative error < 0.03%), with **d(r²)/dt = −4 for opposite and +4 for like signs (fully symmetric)**; under continuous noise generation the **net charge stays exactly Δ**.
> ⚠️ This takes the **same scaling** as §4.2's `R_mix = l_P√(t/t_P)` (`R² ∝ t`) but from a **different source** (diffusion equation vs overdamped vortex motion) ⟹ **no claim of deep unification**.
>
> **④ Two rounds independently reach the same conclusion: topological charge is defined only on the smooth layer**: round 66 (a pointwise-independent random field gives Σ = +9 ≠ 2); round 67 (the **noisy layer's bare Σ ∈ [−5, +4]**, over 40 scans mean +0.35 / std 2.40 — **no topological charge at all**; the smooth layer has it). ⟹ **the "solitonization" step of §2.3 is necessary**; ⚠️ but its **mechanism is still not derived from first principles this round** (only its necessity was verified).
>
> **⑤ This does not constitute a third result**: line 1103 of this subsection already registers "the direction field's Σ index = χ" and "the string net's `Π_v A_v = 1`" as **two realizations of the same topological conservation law**, explicitly stating they are "not two independent results" ⟹ this round **merely adds dynamics to that same conservation law** and adds nothing to the count.
>
> ⚠️ **Six honest boundaries**: ① the dynamics is a **new assumption** (0 hits in the sweep); ② the bare winding number is 3χ and the correction **has a scope**; ③ **conservation is "topological-quantum-level approximate"** — Σw is an exact integer (40/40) but is **strictly constant step-by-step in 0/40**, has spread ≤ 2 in 39/40 and mode = final value in 39/40 (when a vortex hops across an edge the discrete winding number reads ±1, occasionally ±2, and recovers on the next step — **not a drift**); moreover "strictly constant step-by-step" and "vortex count decreasing" are **mutually exclusive** (both hold in 0/40); ④ seed-independence is a **product of the evolution** (at t = 0, 2 of 5 seeds read 5); ⑤ the noisy layer has no topological charge; ⑥ **stable ≠ dynamically stable** — what is proved is "topologically irremovable" (necessary), not "robust against arbitrary perturbations" (sufficient).

'''

sub_once(ZH, "\n\n### 8.3 暗物质叠加模型", "\n\n" + ZH_BLOCK + "### 8.3 暗物质叠加模型", "ZH §8.2 插入第 67 轮块")
sub_once(EN, "\n\n### 8.3 Dark-matter superposition model", "\n\n" + EN_BLOCK + "### 8.3 Dark-matter superposition model", "EN §8.2 插入第 67 轮块")
print()
print("通过 {} 项，失败 {} 项".format(OK, BAD))
