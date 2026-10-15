# -*- coding: utf-8 -*-
"""第 61 轮论文补丁（中英同步）：
   ① §9 S-E1 加 σ_δ 口径限定；② §9 S-C1 加「非判别性」限定；③ 插入【第 61 轮】块。"""
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
    print("  [OK] {:<30} 已改".format(tag))
    OK += 1


# ── ① S-E1 的 σ_δ 口径限定 ─────────────────────────────────────────────
ZH_E1_OLD = "（σ_δ=1.6×10⁻⁶，v1.32 的 9.7×10⁻⁴ 欠采样虚高 600×）"
ZH_E1_NEW = ("（v1.32 的 9.7×10⁻⁴ 欠采样虚高 600×） ⚠️ **第 61 轮加注**：σ_δ=1.6×10⁻⁶ 是"
             "**局部曲率**、**不是有效宽度**（主简并 δ-φ0，ρ≈−0.85，似然非高斯）；"
             "由 ΔlnL 反推的**有效**宽度 **σ_δ,eff = δ/√(2ΔlnL) = 7.5×10⁻⁴**"
             "（与 v1.27 的 8.3×10⁻⁴ 同量级）⟹ **两数不可并存引用，以 ΔlnL 判据（27σ）为准**")
sub_once(ZH, ZH_E1_OLD, ZH_E1_NEW, "ZH §9 S-E1 口径加注")

EN_E1_OLD = ("(σ_δ=1.6×10⁻⁶; v1.32's 9.7×10⁻⁴ was undersampling-inflated by 600×) — "
             "single-source verdict**")
EN_E1_NEW = ("(v1.32's 9.7×10⁻⁴ was undersampling-inflated by 600×) — single-source verdict** "
             "⚠️ **Added in round 61**: σ_δ=1.6×10⁻⁶ is a **local curvature, not an effective width** "
             "(the main degeneracy δ-φ0, ρ≈−0.85, makes the likelihood non-Gaussian); the **effective** "
             "width back-inferred from ΔlnL is **σ_δ,eff = δ/√(2ΔlnL) = 7.5×10⁻⁴** (same order as v1.27's "
             "8.3×10⁻⁴) ⟹ **the two numbers must not be cited together; use the ΔlnL criterion (27σ)**")
sub_once(EN, EN_E1_OLD, EN_E1_NEW, "EN §9 S-E1 caliber note")

# ── ② S-C1 的「非判别性」限定 ──────────────────────────────────────────
sub_once(ZH, "**框架硬预测，可与 wa 检验并行**",
         "**框架硬预测，可与 wa 检验并行** ⚠️ **第 61 轮加注**：这里的「硬」指**从公理解出而非假设**"
         "（= **解释力**）；但**标准平 ΛCDM 给出的 Ω_K 也是 0** ⟹ **观测上不可区分** ⟹ "
         "本条**不是判别性预言**，应读作**解释性成果**（判据：全文「Ω_K」与「ΛCDM」同行共现 **0 次**，"
         "区分性**没有论证**）",
         "ZH §9 S-C1 非判别性加注")

sub_once(EN, "**hard framework prediction; runs in parallel with the wa test**",
         "**hard framework prediction; runs in parallel with the wa test** ⚠️ **Added in round 61**: "
         "\"hard\" here means **derived from the axioms rather than assumed** (= **explanatory power**); "
         "but **standard flat ΛCDM also gives Ω_K = 0** ⟹ **observationally indistinguishable** ⟹ this item "
         "is **not a discriminating prediction** and should be read as an **explanatory result** "
         "(criterion: \"Ω_K\" and \"ΛCDM\" co-occur on the same line **0 times** — the distinction is "
         "**never argued**)",
         "EN §9 S-C1 non-discriminating note")

# ── ③ 插入【第 61 轮】块（§4.8 的 v2.9 补充链末）───────────────────────
ZH_BLOCK = "\n".join([
    "",
    "> **【v2.9 补充（第 61 轮：工程可达性重估 —— 工程出口为零，★★★ 判别性归零）】** 工作流第 1 批 1.2（候选池 37）。逐条审完 **13 条工程项 + 14 组 §9 预言**（脚本 `_feasibility_61.py`，EX-1…EX-9，**9 项 0 失败**）。",
    ">",
    "> · **工程出口 = 0**。原问题「★★ 条目里有没有框架独有且可测的项」的答案是 **0 条**（S-1 是负面、S-5 与 Landauer 同向、S-7/S-12 是解释、S-11 已降调）。全部与材料 / 化学 / 器件相关的工程项（**S-3 超导**第 44 轮 → **S-6 FQH** 第 53–54 轮 → **S-13 电池**第 55–56 轮）先后判否，**理由是同一个**（第 60 轮给出）：**框架缺「势阱型的构型差」**。",
    ">",
    "> · **观测出口 = 1 条**：**EMRI（S-E1–S-E4，δ = 0.30·x_p）** —— 框架独有（标度律 δ∝x_p）＋ 可测（LISA）。⚠️ 但三个前提**全在框架之外**：LISA 发射（~10–15 年）、EMRI 事件率、波形模型（论文自标 quadrupole / 圆轨道 / 非 Teukolsky）。",
    ">",
    "> · ⭐ **★★★ 的判别性 = 0（顺带发现）**：唯一的 ★★★（**S-C1 / S-12 平坦性 Ω_K = 0**）与**标准平 ΛCDM 观测同值**。判据：全文「Ω_K」与「ΛCDM」**在同一行共现 0 次** ⟹ 区分性**没有论证**（不是「论证不足」）。原表述「硬预测」的「硬」指**从公理解出而非假设**（= **解释力**）⟹ 该条应读作**解释性成果，而非判别性预言**。**★★★ 清零。**",
    ">",
    "> · ⚠️ **EMRI 的数字口径须统一（顺带发现）**：若似然近似高斯，`ΔlnL = (δ/σ_δ)²/2` 必须自洽。实测 **v1.27 自洽（Δ = 0.8%）**，而 **v1.35 不自洽** —— 由 σ_δ = 1.63×10⁻⁶ 推 ΔlnL = 7.53×10⁷，报的是 357（**σ 口径差 459 倍**）。由 ΔlnL = 357 反推的有效宽度 **σ_δ,eff = δ/√(2ΔlnL) = 7.49×10⁻⁴**，与 v1.27 的 8.3×10⁻⁴ 同量级 ⟹ 1.63×10⁻⁶ 是**局部曲率**、不是有效宽度（根源：主简并 **δ-φ0**（ρ≈−0.85）使似然**非高斯**）。§9 同节另有「7108σ」（= δ/σ_tot），与 27σ **σ 口径差 267 倍** ⟹ **应统一到 ΔlnL 判据（27σ）**。",
    ">",
    "> · **第 60 轮的后续**：存活出口全在**引力 + 宇宙学**侧（框架唯一有势的地方 = 引力 `Φ(r) = −GM/r`）。⚠️ 与第 60 轮**不矛盾** —— 第 60 轮说的是「无**两体**势、无**几何构型**自由度」，而引力侧只需**外源场中的测地线**（**单粒子问题**）⟹ **精确化：框架能做「测试粒子在外源场中」的物理，不能做「两个可比质量物体的排布」的物理。**",
    ">",
    "> · **诚实标注**：「框架独有」的判据（能否给出与**其他理论**可区分的具体数值 / 标度律）与「工程出口」的定义（能指导造物）都是本轮的**口径**；EMRI 的波形 / Fisher 实现本身**未核验**（只查数字间一致性）；**未**给出「把观测出口变成工程出口」的路径 —— 按第 60 轮结论，**目前不存在**。",
    "",
])
sub_once(ZH, "\n---\n\n## 5 规范群结构", ZH_BLOCK + "\n---\n\n## 5 规范群结构", "ZH 插入第 61 轮块")

EN_BLOCK = "\n".join([
    "",
    "> **【v2.9 supplement (round 61: engineering-reachability re-assessment — zero engineering exits, and the ★★★ loses all discriminating power)】** Workflow batch 1, item 1.2 (candidate pool 37). All **13 engineering items + 14 groups of §9 predictions** were audited one by one (script `_feasibility_61.py`, EX-1…EX-9, **9 pass / 0 fail**).",
    ">",
    "> · **Engineering exits = 0.** The original question — \"among the ★★ items, is there one that is both framework-unique and measurable?\" — has the answer **0** (S-1 is a negative verdict, S-5 runs with Landauer, S-7/S-12 are explanations, S-11 was already downgraded). Every engineering item tied to materials / chemistry / devices (**S-3 superconductivity** round 44 → **S-6 FQH** rounds 53–54 → **S-13 batteries** rounds 55–56) was rejected in turn, and **the reason is the same** (given by round 60): **the framework lacks a \"well-type configurational difference\".**",
    ">",
    "> · **Observational exits = 1**: **EMRI (S-E1–S-E4, δ = 0.30·x_p)** — framework-unique (the scaling law δ∝x_p) and measurable (LISA). ⚠️ But its three preconditions **all lie outside the framework**: LISA launch (~10–15 years), the EMRI event rate, and the waveform model (self-labelled quadrupole / circular orbit / non-Teukolsky).",
    ">",
    "> · ⭐ **The ★★★ has zero discriminating power (found in passing)**: the only ★★★ (**S-C1 / S-12 flatness, Ω_K = 0**) has **the same value as standard flat ΛCDM**. Criterion: \"Ω_K\" and \"ΛCDM\" **co-occur on the same line 0 times** ⟹ the distinction is **never argued** (not merely \"under-argued\"). In the original wording \"hard prediction\", \"hard\" means **derived from the axioms rather than assumed** (= **explanatory power**) ⟹ the item should be read as an **explanatory result, not a discriminating prediction**. **The ★★★ tier is now empty.**",
    ">",
    "> · ⚠️ **The EMRI numbers need a single caliber (found in passing)**: if the likelihood is approximately Gaussian, `ΔlnL = (δ/σ_δ)²/2` must be self-consistent. Measured: **v1.27 is self-consistent (Δ = 0.8%)**, while **v1.35 is not** — from σ_δ = 1.63×10⁻⁶ one gets ΔlnL = 7.53×10⁷ versus the reported 357 (**a factor 459 apart in σ**). Back-inferring from ΔlnL = 357 gives an effective width **σ_δ,eff = δ/√(2ΔlnL) = 7.49×10⁻⁴**, the same order as v1.27's 8.3×10⁻⁴ ⟹ 1.63×10⁻⁶ is a **local curvature, not an effective width** (root cause: the main degeneracy **δ-φ0** (ρ≈−0.85) makes the likelihood **non-Gaussian**). The same §9 section also carries \"7108σ\" (= δ/σ_tot), which is **267× apart from 27σ in σ**) ⟹ **everything should be unified onto the ΔlnL criterion (27σ)**.",
    ">",
    "> · **Follow-up to round 60**: the surviving exits all lie on the **gravity + cosmology** side (the only place the framework has a potential = gravity, `Φ(r) = −GM/r`). ⚠️ This does **not** contradict round 60 — round 60 said \"no **two-body** potential, no **geometric-configuration** degrees of freedom\", whereas the gravity side needs only **geodesics in an external field** (a **single-particle problem**) ⟹ **sharpened: the framework can do \"a test particle in an external field\", but not \"the arrangement of two comparable-mass bodies\".**",
    ">",
    "> · **Honest notes**: both the criterion for \"framework-unique\" (whether it gives a specific number / scaling law distinguishable from **other theories**) and the definition of \"engineering exit\" (can it guide the making of something) are **calibers of this round**; the EMRI waveform / Fisher implementation itself was **not re-verified** (only the consistency among its numbers); and **no** path is offered for turning an observational exit into an engineering exit — per round 60, **none currently exists**.",
    "",
])
sub_once(EN, "\n---\n## 5 Gauge-Group Structure", EN_BLOCK + "\n---\n## 5 Gauge-Group Structure", "EN insert round-61 block")

print()
print("通过 {} 项，失败 {} 项".format(OK, BAD))
