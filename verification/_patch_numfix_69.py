# -*- coding: utf-8 -*-
"""第 69 轮 · 论文补丁（中英同步）
A（C-11）：能隙 Δ=1 → Δ=4J，并加口径注（开 vs 周期 + L=2 退化）
B（C-12）：ε~10⁻⁵⁰ 解除待核实 → 改为「叙事性输入」，并加「两个 ε」区分注
"""
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
        print("  [XX] {:<32} 命中 {} 次 —— 拒绝".format(tag, n))
        BAD += 1
        return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    OK += 1
    print("  [OK] {:<32} 已改".format(tag))


ZH_A = "\n".join([
    "",
    "> **【第 69 轮更正 C-11：2+1D 能隙的口径】** 本节原记「能隙 **Δ=1**」，**未写明归一化**，"
    "且与本节自己的 `J` 定义不符。本轮精确对角化（256 态）与解析（`E(a,b) = 2(a+b) − (N_v+N_p)`）**双确认**："
    "`E0 = −8.0000`（**与本节一致**）、`E1 = −4.0000`、**`Δ = E1 − E0 = 4J`**，"
    "且 **Δ = 4J 对 L = 2…50 全部成立**（非有限尺寸效应）。",
    "> 机理：翻转一条边 `X_e` ⟹ 两个端点 `A_v` 各变号 ⟹ `ΣA_v` 减 4；且 **`Π_v A_v = 1` 是算符恒等式 "
    "⟹ 缺陷必成对** ⟹ 最小激发 = **4J**（不是 2J）。",
    "> ⭐ **口径差异的真正来源是「开 vs 周期」，不是维度**：**周期** ⟹ 有 `Π A = 1` ⟹ 成对 ⟹ **4J**；"
    "**开** ⟹ 无该恒等式 ⟹ 单个 `A_c` 可独立翻转 ⟹ **2J**（§5.8 的单 / 双立方体是**开**边界，"
    "数值 `E0 = −1`、`Δ = 2.0000` ✓）。",
    "> ⚠️ **为什么「1」无法被还原**：在 L = 2 上，三个不同归一化（`Δ/(2L)`、`Δ/4`、`|E0|/(N_v+N_p)`）"
    "**恰好都给 1.000000**（因 `2L = 4 = N_v + N_p`）—— **数值退化，无法区分**；"
    "只有 L ≥ 3 才能分开（`Δ/(2L)` 给 0.667）。",
    "> ⟹ **教训**：报能隙必须**同时写 J 的归一化与边界条件**。脚本 `_numfix_69.py`"
    "（**NC-1…NC-8，8 项 0 失败**）。",
    "",
])

EN_A = "\n".join([
    "",
    "> **【Round-69 correction C-11: the caliber of the 2+1D gap】** This subsection originally wrote"
    " \"gap **Δ=1**\" **without stating its normalization**, and inconsistently with its own definition of `J`."
    " Exact diagonalization (256 states) and the analytic form (`E(a,b) = 2(a+b) − (N_v+N_p)`) **agree**:"
    " `E0 = −8.0000` (**matching this subsection**), `E1 = −4.0000`, **`Δ = E1 − E0 = 4J`**; and"
    " **Δ = 4J holds for L = 2…50** (not a finite-size effect).",
    "> Mechanism: flipping one edge `X_e` changes the sign of `A_v` at both endpoints ⟹ `ΣA_v` drops by 4;"
    " and **`Π_v A_v = 1` is an operator identity ⟹ defects must come in pairs** ⟹ the minimal excitation is"
    " **4J** (not 2J).",
    "> ⭐ **The real source of the discrepancy is \"open vs periodic\", not the dimension**: **periodic** ⟹"
    " `Π A = 1` exists ⟹ pairs ⟹ **4J**; **open** ⟹ no such identity ⟹ a single `A_c` can be flipped"
    " independently ⟹ **2J** (§5.8's single/double cube is **open**-boundary: `E0 = −1`, `Δ = 2.0000` ✓).",
    "> ⚠️ **Why the \"1\" cannot be reconstructed**: at L = 2 three different normalizations"
    " (`Δ/(2L)`, `Δ/4`, `|E0|/(N_v+N_p)`) **all give exactly 1.000000** (because `2L = 4 = N_v + N_p`) —"
    " **a numerical degeneracy that cannot be resolved**; only L ≥ 3 separates them (`Δ/(2L)` gives 0.667).",
    "> ⟹ **Lesson**: a gap must always be reported **together with the normalization of J and the boundary"
    " condition**. Script `_numfix_69.py` (**NC-1…NC-8, 8 pass / 0 fail**).",
    "",
])

ZH_B = "\n".join([
    "",
    "> **【第 69 轮更正 C-12：两个 ε 不能混用（解除第 0 批的「待核实」）】** 本处原写「泄漏 ε~10⁻⁵⁰」，"
    "并在第 0 批加过 ⚠️ 待核实。**该项待核实现已解除**，理由三条：",
    "> ① **出处**：「10⁻⁵⁰」来自 **A2 报告**（第 21 / 146 行：「σ_ann ≠ σ_regen 的失配参数 **δ ~ ε ~ 10⁻⁵⁰**」），"
    "且它在 A2 的「框架表述（公理 1）→ 本报告数学对象」**对应表**里 ⟹ **是输入，不是推导**"
    "（A2 全文「10⁻⁵⁰」共 2 处，无一处给出定义式）。",
    "> ② **它 §8.1 的 `ε_A(E)` 不是同一个量**。判据（可反推）：把 ε = 10⁻⁵⁰ 代进 §8.1 的 "
    "`ε(E) = ε₀(M_Pl/E)^β`，反推能标给 **`E = 2.05×10⁶⁹ GeV`** —— **超出普朗克能标约 49 个数量级** "
    "⟹ 该公式在此**不适用**。",
    "> ③ 因此第 0 批记的「差 40 个数量级」是**把两个量当成同一个 ε** 造成的**假警报**"
    "（与「符号撞车」同族，但这次是**跨章节的同一符号两个身份**：§8.1 的 `ε_A` 是**能标依赖的泄漏概率**，"
    "A2 的 `δ` 是**湮灭-再生的截面失配参数**）。",
    "> ⟹ **本处改写为**：「泄漏参数 ε 极小（**叙事性量级输入，无独立推导**）不产生 LHC 信号」；",
    "> ⟹ 并注意：**「LHC 无新物理」的论证不依赖它**（前面的「差 15 量级」已充分给出）。",
    "> ⚠️ **保留的诚实标注**：10⁻⁵⁰ **没有机制**（不得作证据）；两个 ε 若将来要统一，必须先给出"
    "把「失配参数」与「能标依赖泄漏」联系起来的**独立方程**，否则就是**公设上移**。",
    "",
])

EN_B = "\n".join([
    "",
    "> **【Round-69 correction C-12: the two ε's must not be conflated (the batch-0 \"to be verified\" flag is"
    " now cleared)】** This passage originally read \"leakage ε~10⁻⁵⁰\" and carried a ⚠️ to-be-verified flag"
    " from batch 0. **That flag is now cleared**, for three reasons:",
    "> ① **Provenance**: \"10⁻⁵⁰\" comes from the **A2 report** (lines 21 / 146: \"the mismatch parameter of"
    " σ_ann ≠ σ_regen, **δ ~ ε ~ 10⁻⁵⁰**\"), where it sits in A2's **correspondence table** from"
    " \"framework statement (Axiom 1) → mathematical object in this report\" ⟹ **it is an input, not a"
    " derivation** (A2 contains \"10⁻⁵⁰\" exactly twice, neither with a defining expression).",
    "> ② **It is not the same quantity as §8.1's `ε_A(E)`**. Decidable test (invert it): substituting"
    " ε = 10⁻⁵⁰ into §8.1's `ε(E) = ε₀(M_Pl/E)^β` and solving for the scale gives"
    " **`E = 2.05×10⁶⁹ GeV`** — **about 49 orders of magnitude above the Planck scale** ⟹ that formula"
    " **does not apply** there.",
    "> ③ Hence batch 0's \"40 orders of magnitude\" was a **false alarm caused by treating two different"
    " quantities as one ε** (same family as the \"symbol collision\" trap, but here it is **one symbol with"
    " two identities across sections**: §8.1's `ε_A` is a **scale-dependent leakage probability**, while"
    " A2's `δ` is the **annihilation–regeneration cross-section mismatch parameter**).",
    "> ⟹ **This passage is rewritten as**: \"the leakage parameter ε is extremely small (**a narrative"
    " order-of-magnitude input, with no independent derivation**) and produces no LHC signal\";",
    "> ⟹ and note: **the claim \"no new physics at LHC\" does not depend on it** (the preceding \"15 orders of"
    " magnitude\" already suffices).",
    "> ⚠️ **Honest caveat retained**: 10⁻⁵⁰ **has no mechanism** (it may not be used as evidence); if the two"
    " ε's are ever to be unified, an **independent equation** linking the \"mismatch parameter\" to the"
    " \"scale-dependent leakage\" must first be supplied — otherwise it is a **postulate shift**.",
    "",
])

print("=== A（C-11）：能隙 Δ = 1 → 4J ===")
sub_once(ZH, "- **B3 能隙 Δ=1>0**：2+1D 有正能隙规范理论的严格例证",
         "- **B3 能隙 Δ=4J>0**（⚠️ 第 69 轮更正 C-11，原记 1）：2+1D 有正能隙规范理论的严格例证",
         "ZH 848 B3 能隙")
sub_once(EN, "- **B3 energy gap Δ=1>0**: rigorous example of a gapped gauge theory",
         "- **B3 energy gap Δ=4J>0** (⚠️ round-69 correction C-11; originally 1): rigorous example of a gapped gauge theory",
         "EN 871 B3 能隙")
sub_once(ZH, "环面简并 tr=4.000=|G|² ✓；能隙 Δ=1 ✓。",
         "环面简并 tr=4.000=|G|² ✓；**能隙 Δ=4J ✓**（更正见下）。" + ZH_A,
         "ZH 852 数值验证 + 口径注")
sub_once(EN, "torus degeneracy tr=4.000=|G|² ✓; gap Δ=1 ✓.",
         "torus degeneracy tr=4.000=|G|² ✓; **gap Δ=4J ✓** (correction below)." + EN_A,
         "EN 875 + 口径注")
sub_once(ZH, "弦端点激发能隙 Δ~1（§5.6–5.8）",
         "弦端点激发能隙 Δ~**1–4J（依边界条件：开 2J / 周期 4J，见 §5.7 第 69 轮更正 C-11）**（§5.6–5.8）",
         "ZH 1524 表格行")
sub_once(EN, "string-endpoint excitation gap Δ~1 (§5.6–5.8)",
         "string-endpoint excitation gap Δ~**1–4J (boundary-dependent: 2J open / 4J periodic; see §5.7,"
         " round-69 correction C-11)** (§5.6–5.8)",
         "EN 1562 表格行")

print()
print("=== B（C-12）：ε~10⁻⁵⁰ 解除待核实 ===")
OLD_ZH = ("泄漏 ε~10⁻⁵⁰（⚠️ **待核实**〔第 0 批，2026-09-28〕：按 §8.1 的 `ε(E) = ε₀(M_Pl/E)^β`，"
          "LHC 能标（10⁴ GeV）下应为 **1.47×10⁻¹⁰**，与本处 **差 40 个数量级**；10⁻⁵⁰ 的来源尚未查明，"
          "**暂不改数值**）不产生 LHC 信号；")
sub_once(ZH, OLD_ZH,
         "泄漏参数 ε 极小（**叙事性量级输入，无独立推导**；⚠️ 与 §8.1 的 `ε_A` **不是同一个量**，"
         "见下注 C-12）不产生 LHC 信号；" + ZH_B,
         "ZH 201 ε 改注")
OLD_EN = ("leakage ε~10⁻⁵⁰ (⚠️ **to be verified** [batch 0, 2026-09-28]: per §8.1's "
          "`ε(E) = ε₀(M_Pl/E)^β`, at the LHC scale (10⁴ GeV) it should be **1.47×10⁻¹⁰** — a "
          "**40 order-of-magnitude** discrepancy; the origin of 10⁻⁵⁰ is not yet identified, and the value "
          "is **not changed for now**) produces no LHC signal;")
sub_once(EN, OLD_EN,
         "the leakage parameter ε is extremely small (**a narrative order-of-magnitude input, with no "
         "independent derivation**; ⚠️ it is **not the same quantity** as §8.1's `ε_A` — see note C-12 "
         "below) and produces no LHC signal;" + EN_B,
         "EN 196 ε 改注")

print()
print("通过 {} 项，失败 {} 项".format(OK, BAD))
