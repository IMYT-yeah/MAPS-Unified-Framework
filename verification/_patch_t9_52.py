# -*- coding: utf-8 -*-
"""第 52 轮论文补丁（中英同步）：插入【第 52 轮】块 —— 裁决张力 T-9。"""

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
        print("  [XX] {:<28} 命中 {} 次 —— 拒绝".format(tag, n))
        return False
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    OK[0] += 1
    print("  [OK] {:<28} 已改".format(tag))
    return True


os.makedirs(HIST, exist_ok=True)
for src, dst in ((ZH, "论文初稿_正反物质对风暴统一框架_v2.9.md_备份_2026-09-23第52轮前.md"),
                 (EN, "Paper_MatterAntimatterPairStorm_v2.9_EN.md_备份_2026-09-23第52轮前.md")):
    shutil.copy2(src, os.path.join(HIST, dst))
    print("  备份 → {}".format(dst))

ZH_A = "③ 便宜项：不完备度比值（1.00→1.63→5.93）用更正后的群重算。"
ZH_BLOCK = """> **【v2.9 补充（第 52 轮：裁决张力 T-9 —— B5 的 0.25 =「观测钉住的组合 + 无机制的拆分」）】** 上一条把 T-9 的裁决列为首要项并给了两个选项（① 接受「0.25 是纯公设」；② 给出观测者读数与不变读数的具体关系）。本轮**两个都不采纳**，给出第三个选项。
>
> · ⭐ **「每 4l_P² = 1 纳特」不是设定，而是被 Hawking 温度钉住的**（第 25 轮判别式的复算）：太阳质量黑洞取 1 纳特给 **6.16865×10⁻⁸ K**、取 1 比特给 **8.89948×10⁻⁸ K**（论文记值 6.16868 / 8.8995，相对差 < 0.1%）；比值 `1/ln2 = 1.442695` ⟹ 偏差 **+44.27%** 逐位一致 ⟹ **判别式复现 ✓** ⟹ 该**组合**有观测支撑。
> · ⚠️ **但观测钉住的是「乘积」，拆不开**：观测量只有一个数 `σ = S/A = 0.25 纳特/l_P²`。写成 `σ = (1 单元 / a 面元) × (b 纳特 / 单元) = b/a` ⟹ 观测只约束 **b/a = 0.25**；(a, b) = (4, 1)、(2, 0.5)、(8, 2)、(1, 0.25)、(16, 4) 给出**完全相同的观测量** ⟹ **没有任何实验能定 a 或 b 单独的值** ⟹ 框架的 a = 4、b = 1 是一次**纯因式分解**。
> · **「4」的定性**：§4.9 引理 1；第 29 轮已把其标注由「本框架推论」**更正为【本框架设定】** ⟹ **无机制**（本轮沿用，未新证）。
> · ⟹ **裁决**：B5 的 0.25 = ① 一个被 Hawking 温度**钉住的乘积** ＋ ② 一个**不可观测的因式分解** ＋ ③ 一个**设定**（格距 = l_P）。按第 37 轮四类判定 ⟹ **半拟合 / 一致性** —— **不是**真预言，也**不是**纯公设。
> · ⚠️ **那条不等式 `H/N ≤ 0.25` 实际上不可证伪**：形式上 N ≤ 41 会违反（N_c = 41.8，如 (2,4,4) 的 0.2834），但那些是**普朗克尺度**格点（R ≈ 1.8 l_P）；一切真实黑洞（N ≥ 10⁷⁷）都满足，余量 ≈ 10⁵⁰ ⟹ **该不等式不构成对衬底的有效约束**。⟹ **T-9 的实质：B5 的 0.25 与衬底在这条链上只是松耦合。**
> · 📌 **本轮没有做的事**：`a = 4` 的机制；能**单独**定 a 或 b 的可观测量（**仍然没有**）⟹ T-9 的第 ② 选项**仍然关闭**。
> 🔧 **下一步（收口）**：这条（B5 ↔ 衬底）链路**到此收口**。⚠️ 值得先想清楚一件事 —— 第 46–52 轮共**七轮**都在「格点离散结构 ↔ 面积律」这条链上，结论一路走向**负面**（无等式、无机制、只余一条松不等式）⟹ 是否该**正式把这条链登记为「框架不覆盖」**，把资源换到别的方向（如 **S-6 FQH 的 ε 项** —— 清单里唯一 ★★★ 且是框架**独有**的可测项）？"""

sub_once(ZH, ZH_A, ZH_A + "\n" + ZH_BLOCK, "ZH 插入第52轮块")

EN_A = " cheap item: recompute the incompleteness ratio (1.00→1.63→5.93) with the corrected group."
EN_BLOCK = """> **【v2.9 supplement (round 52: adjudicating tension T-9 — B5's 0.25 is "an observation-pinned product plus a mechanism-free factorisation")】** The previous block made adjudicating T-9 the top priority and offered two options (① accept "0.25 is a pure postulate"; ② give the concrete relation between the observer readout and the invariant readout). This round **adopts neither** and supplies a third.
>
> · ⭐ **"1 nat per 4 l_P²" is not an assumption; it is pinned by the Hawking temperature** (recomputation of the round-25 discriminant): a solar-mass black hole gives **6.16865×10⁻⁸ K** for 1 nat and **8.89948×10⁻⁸ K** for 1 bit (recorded values 6.16868 / 8.8995; relative discrepancy < 0.1%); the ratio `1/ln2 = 1.442695` ⟹ a deviation of **+44.27%**, agreeing digit for digit ⟹ **the discriminant is reproduced ✓** ⟹ this **product** has observational support.
> · ⚠️ **But what observation pins is the product, and it cannot be factored apart**: the observable is the single number `σ = S/A = 0.25 nat per l_P²`. Writing `σ = (1 unit / a plaquettes) × (b nat / unit) = b/a`, observation constrains only **b/a = 0.25**; (a, b) = (4, 1), (2, 0.5), (8, 2), (1, 0.25), (16, 4) all give **exactly the same observable** ⟹ **no experiment can fix a or b separately** ⟹ the framework's a = 4, b = 1 is a **pure factorisation**.
> · **Status of the "4"**: §4.9 Lemma 1; round 29 already **corrected** its label from "a derivation of this framework" to **【an assumption of this framework】** ⟹ **no mechanism** (retained here, not newly established).
> · ⟹ **Verdict**: B5's 0.25 = ① a product **pinned by the Hawking temperature** + ② a **non-observable factorisation** + ③ an **assumption** (lattice spacing = l_P). Under the fourfold classification of round 37 ⟹ **semi-fitted / consistency** — **not** a genuine prediction, and **not** a pure postulate either.
> · ⚠️ **The inequality `H/N ≤ 0.25` is not falsifiable in practice**: formally N ≤ 41 violates it (N_c = 41.8, e.g. 0.2834 at (2,4,4)), but those are **Planck-scale** lattices (R ≈ 1.8 l_P); every real black hole (N ≥ 10⁷⁷) satisfies it with a margin of ≈ 10⁵⁰ ⟹ **the inequality imposes no effective constraint on the substrate**. ⟹ **The substance of T-9: B5's 0.25 and the substrate are only loosely coupled on this chain.**
> · 📌 **Not done here**: a mechanism for `a = 4`; an observable that fixes **a or b separately** (**still none**) ⟹ option ② of T-9 **remains closed**.
> 🔧 **Next (closure)**: the (B5 ↔ substrate) chain **closes here**. ⚠️ One thing worth settling first — rounds 46–52, **seven rounds in all**, have sat on the chain "lattice discreteness ↔ area law", and the verdicts have been **negative** throughout (no equality, no mechanism, only a loose inequality) ⟹ should this chain be **formally registered as "not covered by the framework"**, with resources moved elsewhere (e.g. the **ε term of S-6 FQH** — the only ★★★ item in the list and the framework's only **exclusive** testable prediction)?"""

sub_once(EN, EN_A, EN_A + "\n" + EN_BLOCK, "EN insert round-52 block")

print()
print("=" * 78)
print("补丁汇总：成功 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
