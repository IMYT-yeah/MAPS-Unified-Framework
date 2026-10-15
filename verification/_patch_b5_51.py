# -*- coding: utf-8 -*-
"""第 51 轮论文补丁（中英同步）。

- A. 更正第 46–50 轮的**等式口径**为不等式（中英各 3 处）；
- B. 插入【第 51 轮】块（中英各 1 处）。
"""

import io
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")

OK = [0]
FAIL = [0]


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        FAIL[0] += 1
        print("  [XX] {:<30} 命中 {} 次 —— 拒绝".format(tag, n))
        return False
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    OK[0] += 1
    print("  [OK] {:<30} 已改".format(tag))
    return True


os.makedirs(HIST, exist_ok=True)
for src, dst in ((ZH, "论文初稿_正反物质对风暴统一框架_v2.9.md_备份_2026-09-23第51轮前.md"),
                 (EN, "Paper_MatterAntimatterPairStorm_v2.9_EN.md_备份_2026-09-23第51轮前.md")):
    shutil.copy2(src, os.path.join(HIST, dst))
    print("  备份 → {}".format(dst))

print()
print("=== A. 中文：等式 → 不等式 ===")
sub_once(ZH,
         "⟹ **0.25 被跨过**；**不得**再把「偏大 1.75 倍」当作宏观结论。",
         "⟹ **0.25 被跨过**；**不得**再把「偏大 1.75 倍」当作宏观结论。"
         "⚠️ **第 51 轮口径更正**：两者关系是**不等式** `H/N ≤ 0.25`（不变读数 ≤ 观测者读数），"
         "「0.25 被跨过」应读作「0.2834 **违反**自洽性、0.1839 **满足**自洽性」，见【第 51 轮】块。",
         "ZH-A1 第48轮判决3")
sub_once(ZH,
         "本轮用 GAP 沿 (2,4,L) 扫描并补算，结果是**把上一条的判据细化**。",
         "本轮用 GAP 沿 (2,4,L) 扫描并补算，结果是**把上一条的判据细化**。"
         "⚠️ **第 51 轮口径更正**：本块的「跨点」一词应读作「**自洽性下界**」（不等式 `H/N ≤ 0.25`），"
         "数值不变而语义变了，见【第 51 轮】块。",
         "ZH-A2 第49轮标题")
sub_once(ZH,
         "若无，则 0.25 与本框架的衬底之间**根本不存在定量联系**（这是一个可以写清的负面结论）。",
         "若无，则 0.25 与本框架的衬底之间**根本不存在定量联系**（这是一个可以写清的负面结论）。"
         "⟹ **【第 51 轮已回答】**：B5 **不含** N、k、形状 ⟹ **都没有**；且两者关系应为**不等式**"
         "（观测者的 0.25 纳特与衬底的 H/N 相差 ~50 个数量级）⟹ 见【第 51 轮】块。",
         "ZH-A3 第50轮下一步")

print()
print("=== A'. 英文：等式 → 不等式 ===")
sub_once(EN,
         '⟹ **0.25 is straddled**; "too large by 1.75×" must **not** be quoted as a macroscopic conclusion.',
         '⟹ **0.25 is straddled**; "too large by 1.75×" must **not** be quoted as a macroscopic conclusion. '
         '⚠️ **Caliber corrected in round 51**: the relation is an **inequality** `H/N ≤ 0.25` '
         '(invariant readout ≤ observer readout); "straddled" should read as "0.2834 **violates** '
         'self-consistency, 0.1839 **satisfies** it" — see the round-51 block.',
         "EN-A1 round-48 verdict 3")
sub_once(EN,
         "This round scans along (2,4,L) with GAP and **refines** that block's criterion.",
         "This round scans along (2,4,L) with GAP and **refines** that block's criterion. "
         "⚠️ **Caliber corrected in round 51**: the word \"crossing point\" below should read "
         "**\"lower bound of self-consistency\"** (an inequality `H/N ≤ 0.25`); the numbers are unchanged, "
         "the meaning is not — see the round-51 block.",
         "EN-A2 round-49 heading")
sub_once(EN,
         "if it does not, then **no quantitative link exists between 0.25 and this framework's substrate** "
         "— a negative conclusion that can be stated cleanly.",
         "if it does not, then **no quantitative link exists between 0.25 and this framework's substrate** "
         "— a negative conclusion that can be stated cleanly. "
         "⟹ **【Answered in round 51】**: B5 contains **neither** N, nor k, nor the shape ⟹ **none of them**; "
         "and the relation is an **inequality** (the observer's 0.25 nat and the substrate's H/N differ by "
         "~50 orders of magnitude) — see the round-51 block.",
         "EN-A3 round-50 next")

print()
print("=== B. 插入第 51 轮块 ===")

ZH_ANCHOR = ("⟹ **【第 51 轮已回答】**：B5 **不含** N、k、形状 ⟹ **都没有**；且两者关系应为**不等式**"
             "（观测者的 0.25 纳特与衬底的 H/N 相差 ~50 个数量级）⟹ 见【第 51 轮】块。")
ZH_BLOCK = """> **【v2.9 补充（第 51 轮：B5 与衬底的定量联系 —— 是**不等式**，不是等式）】** 上一条把 🎯 定为「机制一侧」，问 B5 的「每 4l_P² 取 1 纳特」是否隐含一个特定的 N 或 k。本轮用**引文核对 + 纯算术 + 方向判据**回答，并顺带更正上五轮的**判据方向**。
>
> · **🎯 的直接答案：都没有。** B5 的 `S = A/(4l_P²)` 里**只出现面积 A 与 l_P**；**格点总数 N、占据数 k、格点形状三个都不出现** ⟹ B5 给的是一条**「面积 → 熵」的换算率**，对格点层面的离散结构**零约束**。
> · **B5 真正隐含的量：每格点（每面元）0.25 纳特。** 算术：§8.6.8 的**格距 = l_P**（⟹ 每面元面积 = l_P²；⚠️ 定性是**设定** —— 「本框架设定的自然选择、非强制推导」）＋ §4.8 的**表面 N = A/l_P² 个面元、每 4 面元 1 个相干单元、每单元 1 纳特** ⟹ 单元数 = A/(4l_P²) ⟹ S = A/(4l_P²) 纳特 ⟹ **每面元 1/4 = 0.25 纳特**（= 0.3607 比特）。⟹ **0.25 不是待命中的目标，而是两个设定算出来的输入。**
> · ⚠️ **判据方向更正（本轮最重要）**：第 40 轮已证明「观测者的读数**不能**是 tick 不变量」⟹ 观测者用的是**瞬时**读数，而 tick 不变读数是它的一个函数 ⟹ `H/N`（不变读数的熵密度）**≤** `0.25`（观测者的读数分辨率）⟹ **这是不等式，不是等式**。⟹ 第 46–50 轮找「H/N = 0.25 的跨点」时，隐含假设「观测者读数 = tick 不变读数」**已被第 40 轮否证** ⟹ 那条路线的**目标错了**，不是没找到（记为 **N-13**）。
> · ⟹ **正确的读法**：(2,4,4) 的 0.2834 是**违反**自洽性；(4,4,4) 的 0.1839 是**满足**。不是「0.25 被跨过」。
> · ✅ **宏观自洽性轻松满足**：用第 50 轮的**拟合**标度律 `h_min = 3.01·N^{−2/3}`（⚠️ 仅作量级）—— 太阳质量黑洞 N = A/l_P² ≈ **4.20×10⁷⁷** ⟹ H/N ≈ **5.4×10⁻⁵²** 纳特/格点 ⟹ **余量 ≈ 4.7×10⁵⁰ 倍**；10⁶ M☉ 余量 ≈ 4.7×10⁵⁸ 倍。
> · ✅ **自洽性下界**：解 `3.01·N^{−2/3} = 0.25` ⟹ **N_c = 41.8**（对应视界半径 R = 1.82 l_P，**普朗克尺度**）⟹ **凡 N ≥ 42 的视界都自洽**。⟹ 与第 49 轮的区间 (32, 48) **数值交叉验证一致**，但**语义不同**：那是「跨点」，这里是「下界」。
> · 🆕 **张力 T-9（登记，未裁决）**：B5 的「每格点 0.25 纳特」与衬底的「H/N → 0（大 N）」相差 **~50 个数量级**。这**不是矛盾**（不等式允许），但说明**观测者的 0.25 纳特几乎全部来自 tick 可变的自由度**，衬底的不可分辨性只贡献 ~10⁻⁵² 纳特/格点 ⟹ **观测者的分辨率几乎不受衬底约束**。⟹ 这解释了第 40 轮「三难」与第 45 轮「τ 判否」的**机制层理由**：两者之间本来**只有一条很松的不等式，没有等式可追**。
> ⚠️ **诚实边界**：每格点 0.25 纳特的算术**严格**，但依赖两个**设定**（其一明确标为「非强制推导」）；`H/N ≤ 0.25` 由信息处理不等式 + 第 40 轮结论 ⟹ 严格；但 **N_c = 41.8 与宏观余量 10⁵⁰ 依赖第 50 轮的拟合标度律**（残差 2.6%，且**未在 N → 10⁷⁷ 上验证**，外推跨 77 个数量级）⟹ **只作量级，不得作定量结论**；「每 4 面元 1 单元」里的 **4 仍是设定**（§4.9 引理 1，原标「推论」已更正）⟹ **0.25 里的「4」没有机制**。
> 🔧 **下一步**：① 不再追 `H/N = 0.25`（N-13）；② **裁决 T-9 的第一问** —— 接受「B5 的 0.25 是纯公设、与衬底只有一条松不等式」并写进 §4.8（与第 39 轮「一致性构造」的口径一致）；③ 便宜项：不完备度比值（1.00→1.63→5.93）用更正后的群重算。"""

sub_once(ZH, ZH_ANCHOR, ZH_ANCHOR + "\n" + ZH_BLOCK, "ZH-B 插入第51轮块")

EN_ANCHOR = ("⟹ **【Answered in round 51】**: B5 contains **neither** N, nor k, nor the shape ⟹ **none of them**; "
             "and the relation is an **inequality** (the observer's 0.25 nat and the substrate's H/N differ by "
             "~50 orders of magnitude) — see the round-51 block.")
EN_BLOCK = """> **【v2.9 supplement (round 51: the quantitative link between B5 and the substrate — an **inequality**, not an equality)】** The previous block moved the priority to the "mechanism side", asking whether B5's "1 nat per 4 l_P²" implies a particular N or k. This round answers by **citation checking, pure arithmetic and a direction-of-criterion argument**, and in passing corrects the **direction** of the last five rounds.
>
> · **The direct answer to the priority question: none of them.** In B5's `S = A/(4 l_P²)` only **the area A and l_P occur**; **the site count N, the occupation number k and the lattice shape all fail to appear** ⟹ B5 supplies an **"area → entropy" conversion rate** with **zero constraint** on the discrete structure at the lattice level.
> · **What B5 does imply: 0.25 nat per site (per plaquette).** Arithmetic: the **lattice spacing = l_P** of §8.6.8 (⟹ each plaquette has area l_P²; ⚠️ its status is an **assumption** — "the natural choice of this framework, not a forced derivation") plus §4.8's **surface N = A/l_P² plaquettes, 1 coherent unit per 4 plaquettes, 1 nat per unit** ⟹ #units = A/(4 l_P²) ⟹ S = A/(4 l_P²) nat ⟹ **1/4 = 0.25 nat per plaquette** (= 0.3607 bit). ⟹ **0.25 is not a target to be hit; it is an input computed from two assumptions.**
> · ⚠️ **Correction of the direction (the most important item here)**: round 40 established that "the observer's readout **cannot** be a tick invariant" ⟹ the observer uses an **instantaneous** readout, of which the tick-invariant readout is a function ⟹ `H/N` (entropy density of the invariant readout) **≤** `0.25` (the observer's readout resolution) ⟹ **this is an inequality, not an equality**. ⟹ rounds 46–50 were looking for "the crossing point of H/N = 0.25" under the tacit assumption "observer readout = tick-invariant readout", an assumption **already refuted in round 40** ⟹ that route **aimed at the wrong target**; it did not merely fail to find it (recorded as **N-13**).
> · ⟹ **The correct reading**: 0.2834 at (2,4,4) **violates** self-consistency; 0.1839 at (4,4,4) **satisfies** it. Not "0.25 is straddled".
> · ✅ **Macroscopic self-consistency holds with room to spare**: using round 50's **fitted** scaling law `h_min = 3.01·N^{-2/3}` (⚠️ order of magnitude only) — a solar-mass black hole has N = A/l_P² ≈ **4.20×10⁷⁷** ⟹ H/N ≈ **5.4×10⁻⁵²** nat/site ⟹ a **margin of ≈ 4.7×10⁵⁰**; for 10⁶ M☉ the margin is ≈ 4.7×10⁵⁸.
> · ✅ **Lower bound of self-consistency**: solving `3.01·N^{-2/3} = 0.25` gives **N_c = 41.8** (horizon radius R = 1.82 l_P, i.e. **Planck scale**) ⟹ **every horizon with N ≥ 42 is self-consistent**. ⟹ **Cross-checked numerically** against round 49's bracket (32, 48), but with a **different meaning**: that was a "crossing point", this is a "lower bound".
> · 🆕 **Tension T-9 (registered, not adjudicated)**: B5's "0.25 nat per site" and the substrate's "H/N → 0 (large N)" differ by **~50 orders of magnitude**. This is **not a contradiction** (the inequality permits it), but it shows that **almost all of the observer's 0.25 nat comes from tick-varying degrees of freedom**, while the substrate's indistinguishability contributes only ~10⁻⁵² nat/site ⟹ **the observer's resolution is barely constrained by the substrate at all**. ⟹ This gives the **mechanism-level reason** for round 40's "trilemma" and round 45's "τ refuted": between the two there is **only a very loose inequality; there is no equality to chase**.
> ⚠️ **Honest limits**: the arithmetic giving 0.25 nat per site is **exact**, but rests on two **assumptions** (one explicitly marked "not a forced derivation"); `H/N ≤ 0.25` follows from the data-processing inequality plus round 40 ⟹ exact; but **N_c = 41.8 and the 10⁵⁰ margin depend on round 50's fitted scaling law** (residual 2.6%, and **unverified at N → 10⁷⁷**, i.e. extrapolated over 77 orders of magnitude) ⟹ **orders of magnitude only, not quantitative conclusions**; the **4** in "1 unit per 4 plaquettes" is still an **assumption** (§4.9 Lemma 1, whose label "derivation" was corrected to "assumption") ⟹ **there is no mechanism for the "4" inside 0.25**.
> 🔧 **Next**: ① stop chasing `H/N = 0.25` (N-13); ② **adjudicate the first half of T-9** — accept "B5's 0.25 is a pure postulate, connected to the substrate only by a loose inequality" and write it into §4.8 (consistent with round 39's "consistency construction" wording); ③ cheap item: recompute the incompleteness ratio (1.00→1.63→5.93) with the corrected group."""

sub_once(EN, EN_ANCHOR, EN_ANCHOR + "\n" + EN_BLOCK, "EN-B insert round-51 block")

print()
print("=" * 78)
print("补丁汇总：成功 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
