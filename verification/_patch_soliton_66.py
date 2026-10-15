# -*- coding: utf-8 -*-
"""第 66 轮 · 论文补丁（中英同步）：§8.2 H1–H4 之后插入【第 66 轮】块。"""
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


ZH_BLOCK = r'''> **【v2.9 补充（第 66 轮：孤子的诞生 —— 随机湮灭中的拓扑残余）】** 触发问题：「**在随机湮灭中出现了无法湮灭的稳定点**，也就是正物质的诞生」。框架侧的对应物**全部是已有内容**：§2.3 的层级链写着「**孤子化 ⟹ 粒子（稳定局域结构）**」；§5.3「**三代费米子 = 涡的卷绕模**」；本节 **H1** 给出拓扑强制。本轮把它做成可判定问题（脚本 `_soliton_66.py`，SO-1…SO-9，**9 项 0 失败**）。
>
> **① 数值证实 H1**（icosphere 细分 3 次 = 642 顶点；用 **Morse 谱**计数）：**30 个独立随机平滑场给出 Σ = #max − #saddle + #min ≡ 2**（30 次全部相同），而 `#max`（均值 2.10）、`#min`（2.07）、`#saddle`（2.17）**每次都不同**。三档解析标定（f = p_x / p_y / p_z，真临界点各 2 个）**全部给 +2** ✓ ⟹ **H1 的「至少 2 个涡心」得到数值支撑**。
>
> **② 湮灭实验**：按「指数 +1 与 −1 相遇 ⟹ 双双消失」随机配对，**40 次独立试验的终点分布只有一种：2 个 +1 / 0 个 −1**。⟹ **随机湮灭抹掉大部分涡心（视构型 50–98%），但净荷 χ 是几何恒等式，一个也去不掉。**
>
> **③ 反面对照（毛球定理的直接陈述）**：
>
> | 曲面 | χ | 最少涡心数 | 存在处处非零场？ |
> |---|---|---|---|
> | **S²**（方向空间） | **2** | **≥ 2** | 否（毛球定理） |
> | **T²**（环面） | 0 | **0** | **是**（v = ∂/∂u，模恒为 1.000000） |
> | **S³** | 0 | 0 | **是**（可平行化） |
>
> ⟹ 「能否全部湮灭」由 **χ** 决定、**与随机性无关** —— 与本节第 1083 行的 S³ 澄清是同一个判据。
>
> **④ H2 可重写**：`ε_topo(R) = (l_P/R)²/(2π) = χ/(4π)·(l_P/R)²`（因 χ/(4π) = 1/(2π)）⟺ 「单元立体角 ΔΩ = (l_P/R)²，涡心占 **χ = 2** 个」。代入 R = l_P：`ε_topo(l_P) = 1/(2π) = 0.1591549` —— **与 H3 的「普朗克尺度拓扑主导（0.159）」精确一致** ✓ ⚠️ 这是**算术恒等**（把 1/(2π) 认出来是 χ/(4π)），**不是新推导**。
>
> **⑤ 与 §5.7 弦网是同一句话**：`Σ 指数 = χ = 2`（方向场）与 `Π_v A_v = Π_p B_p = 1`（弦网）是**同一个拓扑守恒**的两种实现 ⟹ 登记为**一致性**，不是两条独立成果。
>
> ⚠️ **两个方法学教训**（供后续复用）：① **经纬网格的极点会让 1-ring 退化** —— 顶点 (1, j) 的三个「上一行」邻居全映射到同一个北极点 ⟹ 绕数全错（实测 Σ = −8 而非 2）；换 **icosphere** 后正常。② **「单位化 ∇f 的绕数」≠「临界点指数」** —— 单位化会把 `|∇f|` 小的**非零点**放大成伪涡心（`f = p_x` 报 6 个 +1，伪影落在 `|∇f| ≈ 0.156` 处，而它并不是零点）⟹ **拓扑计数必须用 Morse 谱**。附带：判据**只在平滑层上成立** —— 逐点独立的随机场给 Σ = +9 ≠ 2（「处处都是极值」），这正是 §2.3「**孤子化**」那一步的内容。
>
> ⚠️ **诚实边界三条**：① 本轮算的是**静态几何**，「湮灭」在数值上是**抽象配对**，不是从时空动力学推出的；② **未验证 ε 泄漏**（P1 是【本框架设定】）⟹ **拓扑荷 ≠ 物质–反物质不对称**，两者在框架里是**两条独立命题**；③ 只验证了**拓扑不可抹去**，**未验证动力学稳定性**（那是「孤子成为粒子」的必要不充分条件）。
> ⚠️ **措辞更正**：不是「随机波动中**出现**了稳定点」，而是「**被拓扑强制**」——判据 = Σ 是否为随机变量（**不是**：30 次全为 2）。

'''

EN_BLOCK = r'''> **【v2.9 supplement (round 66: the birth of a soliton — topological residue under random annihilation)】** Triggering question: "**in random annihilation, stable points that cannot be annihilated appear** — that is the birth of matter". The framework-side counterparts are **all pre-existing content**: §2.3's hierarchy chain states "**solitonization ⟹ particles (stable localized structures)**"; §5.3 states "**three fermion generations = the winding modes of vortices**"; and **H1** of this subsection supplies the topological forcing. This round turns it into a decidable problem (script `_soliton_66.py`, SO-1…SO-9, **9 pass / 0 fail**).
>
> **① Numerical confirmation of H1** (icosphere subdiv 3 = 642 vertices; counted via the **Morse spectrum**): **30 independent random smooth fields all give Σ = #max − #saddle + #min ≡ 2** (identical in all 30 runs), while `#max` (mean 2.10), `#min` (2.07) and `#saddle` (2.17) **differ every time**. Three analytic calibrations (f = p_x / p_y / p_z, each with exactly 2 true critical points) **all give +2** ✓ ⟹ **the "at least 2 vortex cores" of H1 now has numerical support**.
>
> **② Annihilation experiment**: pairing randomly under "index +1 meeting −1 ⟹ both vanish", **the endpoint distribution over 40 independent trials has a single outcome: 2 of +1 / 0 of −1**. ⟹ **random annihilation wipes out most vortex cores (50–98% depending on the configuration), but the net charge χ is a geometric identity — not one of them can be removed.**
>
> **③ Counter-check (the hairy-ball theorem stated directly)**:
>
> | Surface | χ | Minimum number of vortex cores | Admit a nowhere-zero field? |
> |---|---|---|---|
> | **S²** (direction space) | **2** | **≥ 2** | No (hairy-ball theorem) |
> | **T²** (torus) | 0 | **0** | **Yes** (v = ∂/∂u, modulus exactly 1.000000) |
> | **S³** | 0 | 0 | **Yes** (parallelizable) |
>
> ⟹ "whether everything can be annihilated" is decided by **χ**, **independently of randomness** — the same criterion as the S³ clarification on line 1083 of this subsection.
>
> **④ H2 can be rewritten**: `ε_topo(R) = (l_P/R)²/(2π) = χ/(4π)·(l_P/R)²` (since χ/(4π) = 1/(2π)) ⟺ "unit solid angle ΔΩ = (l_P/R)², with **χ = 2** cores among the units". Substituting R = l_P: `ε_topo(l_P) = 1/(2π) = 0.1591549` — **exactly consistent with the H3 statement "Planck-scale topological dominance (0.159)"** ✓ ⚠️ This is an **arithmetic identity** (recognizing 1/(2π) as χ/(4π)), **not a new derivation**.
>
> **⑤ The same sentence as the §5.7 string net**: `Σ index = χ = 2` (direction field) and `Π_v A_v = Π_p B_p = 1` (string net) are **two realizations of the same topological conservation law** ⟹ registered as **consistency**, not as two independent results.
>
> ⚠️ **Two methodological lessons** (for later reuse): ① **poles of a latitude–longitude grid degenerate the 1-ring** — for vertex (1, j) the three "previous-row" neighbours all map to the same north pole ⟹ the winding numbers are all wrong (measured Σ = −8 instead of 2); switching to an **icosphere** fixes it. ② **"the winding number of the normalized ∇f" ≠ "the index of a critical point"** — normalization magnifies **non-zero points** with small `|∇f|` into spurious vortex cores (`f = p_x` reports 6 of +1, with artefacts sitting at `|∇f| ≈ 0.156`, which are not zeros at all) ⟹ **topological counting must use the Morse spectrum**. Relatedly, the criterion **holds only on a smooth layer** — a pointwise-independent random field gives Σ = +9 ≠ 2 ("everywhere is an extremum"), which is precisely the content of the "**solitonization**" step in §2.3.
>
> ⚠️ **Three honest boundaries**: ① this round computes **static geometry**; "annihilation" is an **abstract pairing** in the numerics, not derived from spacetime dynamics; ② **ε leakage is not verified** (P1 is a【framework assumption】) ⟹ **topological charge ≠ matter–antimatter asymmetry**; the two are **independent propositions** within the framework; ③ only **topological irremovability** was verified, **not dynamical stability** (which is a necessary but not sufficient condition for "a soliton becoming a particle").
> ⚠️ **Wording correction**: it is not that "stable points **appear** in random fluctuations", but that they are **topologically forced** — the criterion being whether Σ is a random variable (**it is not**: 2 in all 30 runs).

'''

sub_once(ZH, "\n\n### 8.3 暗物质叠加模型",
         "\n\n" + ZH_BLOCK + "### 8.3 暗物质叠加模型",
         "ZH §8.2 插入第 66 轮块")

sub_once(EN, "\n\n### 8.3 Dark-matter superposition model",
         "\n\n" + EN_BLOCK + "### 8.3 Dark-matter superposition model",
         "EN §8.2 插入第 66 轮块")

print()
print("通过 {} 项，失败 {} 项".format(OK, BAD))
