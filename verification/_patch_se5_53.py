# -*- coding: utf-8 -*-
r"""第 53 轮论文补丁：S-E5 的 ε 能标更正 + E_c 恒等式更正 + S-6 降调（中英同步）。"""
import io, os, shutil, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")

OK, XX = [], []


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<34} 命中 {} 次 —— 拒绝".format(tag, n))
        XX.append(tag)
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<34} 已改".format(tag))
    OK.append(tag)


# ---------------------------------------------------------------- 备份
os.makedirs(HIST, exist_ok=True)
stamp = datetime.date.today().isoformat()
for src, tag in ((ZH, "zh"), (EN, "en")):
    stem = os.path.splitext(os.path.basename(src))[0]
    dst = os.path.join(HIST, "{}_备份_{}第53轮前.md".format(stem, stamp))
    shutil.copy2(src, dst)
    print("  备份 -> {}".format(os.path.basename(dst)))

print()
print("=== A. §8.1 的 ε₀ 口径统一 ===")
sub_once(ZH,
         "- β = log(6×10⁻¹⁰)/log(10⁻¹⁵) ≈ **0.615**，ε₀ ≈ 7.6×10⁻²⁰。",
         "- β = log(6×10⁻¹⁰)/log(10⁻¹⁵) ≈ **0.615**，ε₀ = **7.731×10⁻²⁰**。\n"
         "  （**【第 53 轮口径统一】**本节原写 7.6×10⁻²⁰、§1 摘要与 §6 写 7.7×10⁻²⁰、§8.2 H3 写 7.67×10⁻²⁰，\n"
         "  四值跨度 2% ⟹ 现统一为**由定义式 ε₀ = ε(1TeV)/(M_Pl/1TeV)^β 算得的值**。E_c 对 ε₀ 敏感，故此项须唯一。）",
         "ZH-A1 ε₀ 统一")

sub_once(EN,
         "- β = log(6×10⁻¹⁰)/log(10⁻¹⁵) ≈ **0.615**, ε₀ ≈ 7.6×10⁻²⁰.",
         "- β = log(6×10⁻¹⁰)/log(10⁻¹⁵) ≈ **0.615**, ε₀ = **7.731×10⁻²⁰**.\n"
         "  (**【round-53 caliber unification】** this section wrote 7.6×10⁻²⁰, the abstract and §6 wrote 7.7×10⁻²⁰,\n"
         "  and §8.2 H3 wrote 7.67×10⁻²⁰ — a 2% spread; now unified to the value **computed from the defining relation**\n"
         "  ε₀ = ε(1TeV)/(M_Pl/1TeV)^β. E_c is sensitive to ε₀, so this constant must be unique.)",
         "EN-A1 ε₀ unify")

print()
print("=== B. §8.1 的「截断能标【推导】」更正 ===")
sub_once(ZH,
         "**截断能标**【推导】：概率归一化 ε_A(E_c) = 1 ⟹ E_c = M_Pl·ε₀^{1/β} = **1.0181 meV**——与暗能量特征能标 2.3 meV 同量级（(E_c)⁴ 差 27 倍，O(1) 系数待定）。",
         "**截断能标**【推导】：概率归一化 ε_A(E_c) = 1 ⟹ E_c = M_Pl·ε₀^{1/β} = **1.0181 meV**——与暗能量特征能标 2.3 meV 同量级（(E_c)⁴ 差 27 倍，O(1) 系数待定）。\n"
         "\n"
         "> **【第 53 轮更正：E_c 是恒等式，不是【推导】】**把 ε₀ 的定义代入即可：\n"
         "> `E_c = M_Pl·[ε(1TeV)/(M_Pl/1TeV)^β]^{1/β} = 1TeV·ε(1TeV)^{1/β}` —— **M_Pl 完全消掉**，\n"
         "> 数值 = **1.000000 meV 精确**（原记 1.0181 meV 系 ε₀ / M_Pl 取值的**数值残差 −1.78%**）。\n"
         "> ⟹ 因 β ≡ ln(η)/ln(1meV/1TeV) 本就是这个等式解出来的，「E_c 与暗能量能标同量级」是**锚点 2 的重述**；\n"
         "> 用它去验证锚点 2（ρ_Λ ~ (meV)⁴）是**循环**。四类判定 = **半拟合**（两个锚点定 β 与 ε₀，第三个量无独立内容）。\n"
         "> **仍成立**：**meV 量级**这个量级结论（与 β 的敏感度无关）。详见第 53 轮块（本节末）。",
         "ZH-B1 E_c 恒等式")

sub_once(EN,
         "**Cutoff scale**【Derivation】: probability normalization ε_A(E_c) = 1 ⟹ E_c = M_Pl·ε₀^{1/β} = **1.0181 meV** — of the same order as the dark-energy characteristic scale 2.3 meV ((E_c)⁴ differs by a factor 27; O(1) coefficient undetermined).",
         "**Cutoff scale**【Derivation】: probability normalization ε_A(E_c) = 1 ⟹ E_c = M_Pl·ε₀^{1/β} = **1.0181 meV** — of the same order as the dark-energy characteristic scale 2.3 meV ((E_c)⁴ differs by a factor 27; O(1) coefficient undetermined).\n"
         "\n"
         "> **【round-53 correction: E_c is an identity, not a【Derivation】】** substituting the definition of ε₀ gives\n"
         "> `E_c = M_Pl·[ε(1TeV)/(M_Pl/1TeV)^β]^{1/β} = 1TeV·ε(1TeV)^{1/β}` — **M_Pl cancels completely**,\n"
         "> value = **1.000000 meV exactly** (the recorded 1.0181 meV is a **numerical residual of −1.78%** from the ε₀ / M_Pl values used).\n"
         "> ⟹ since β ≡ ln(η)/ln(1meV/1TeV) *was solved from this very equation*, \"E_c is of the same order as the dark-energy scale\"\n"
         "> is a **restatement of anchor 2**; using it to verify anchor 2 (ρ_Λ ~ (meV)⁴) is **circular**. Four-way verdict = **semi-fitted**.\n"
         "> **Still valid**: the **meV order of magnitude** (independent of β sensitivity). See the round-53 block at the end of this section.",
         "EN-B1 E_c identity")

print()
print("=== C. §8.1 末尾插入【第 53 轮】块 ===")
BLOCK_ZH = r"""
> **【v2.9 补充（第 53 轮：S-E5 的 ε 是能标错置，且 E_c 是恒等式）】** 审查对象 = 清单里唯一的 ★★★ 项 **S-6（FQH 引力子模）**。本轮不跑数值，全部是**算术 + 引文核对**（脚本 `_se5_eps_53.py`，SE-1…SE-8，**7 项 0 失败**）。
>
> · **① 能标错置（判为失败）**：§5.8 与 §9 的 S-E5 写 `ε ~ 10⁻²⁰`，而那是**本节的 ε₀ = ε(M_Pl)**。按本节自己的公式 `ε(E) = ε₀(M_Pl/E)^β`，FQH 能标（GaAs 2DEG：ℏω_c = 86–259 meV、E_C = 9.7–16.9 meV、Δ_GMP ≈ 0.6E_C、k_BT@mK = 0.9–4.3 μeV）下 **ε ∈ [0.042, 77]** ⟹ 与 10⁻²⁰ 差 **18–21 个数量级**。本节第 892 行本来就写着 **ε(1 meV) ~ 1** ⟹ **§8.1 与 S-E5 直接冲突**（同一个符号，两个能标）。
> · **② E_c 是恒等式（半拟合），不是【推导】**：见上方更正框 —— `E_c = 1TeV·ε(1TeV)^{1/β} = 1.000000 meV`，M_Pl 消掉，「与暗能量能标同量级」是锚点 2 的重述 ⟹ **循环**。
> · **③ Γ_flux 无定义（不可识别）**：`Γ_flux` 在全文只出现 **2 次**、都在同一预言句，**没有任何表达式**。而观测量是**一个实数**（线宽 Γ）⟹ 未知量 ≥ 一个自由函数 ⟹ 与第 45 轮（公设上移）、第 52 轮（不可识别拆分）**同源，这是第四次出现**。判据：**未知量个数 > 方程个数 ⟹ 不可识别**。
> · **④ 两难**：标准侧已有引力子模**内在衰减率**的机制与定量提取（GMP 1970s → Haldane 2016 几何理论 → Liang et al., Nature 628, 78 (2024) 实验 → Balram–Sreejith–Jain, PRL 133, 246605 (2024) 分裂 → Du, arXiv:2509.04408 (2025) 有效场论 → IOP Rep. Prog. Phys. (2025) 提取 decay rate，机制 = 衰变进**双磁旋子连续谱**）。若 ε = O(1)，则 Γ_flux 与 Γ_Coulomb **同量级** ⟹ **「框架独有、标准无此项」与「与实验一致」只能取一**。
> · **⑤ 附带**：ε₀ 原有**四个写法**（7.6 / 7.7 / 7.67 / 7.751 ×10⁻²⁰，跨度 2%），本条已统一为 7.731×10⁻²⁰。
> · **判决**：S-E5 的 `ε ~ 10⁻²⁰` = **失败**；`E_c` 的【推导】标注 = **半拟合**；整体可检验性 = **不可识别**；「框架独有」 = **未成立**。⟹ **S-6 的 ★★★ 评级与「框架独有」定位均需降调**，清单里「唯一 ★★★ 且独有」的说法不成立。修复路径：①（必做）把 S-E5 的 ε 改为 `ε(FQH 能标) ≈ O(1)`、把「线宽余项」改为「与 Γ_Coulomb 同量级的附加项」；②（唯一能复活的路）**给出 Γ_flux 的表达式**，并证其相对标准 Γ 是**独立贡献**；③ 若 1/2 不做，则降为「方向性主张、无定量」。
"""

BLOCK_EN = r"""
> **【v2.9 supplement (round 53: S-E5's ε is a scale misplacement, and E_c is an identity)】** Audited object = **S-6 (the FQH graviton mode)**, the only ★★★ item on the list. No numerics were run: this round is **arithmetic + citation checking** (script `_se5_eps_53.py`, SE-1…SE-8, **7 pass / 0 fail**).
>
> · **① Scale misplacement (verdict: failure)**: §5.8 and §9 state `ε ~ 10⁻²⁰` for S-E5, but that is **this section's ε₀ = ε(M_Pl)**. Using this section's own law `ε(E) = ε₀(M_Pl/E)^β`, at FQH scales (GaAs 2DEG: ℏω_c = 86–259 meV, E_C = 9.7–16.9 meV, Δ_GMP ≈ 0.6E_C, k_BT@mK = 0.9–4.3 μeV) one gets **ε ∈ [0.042, 77]** ⟹ **18–21 orders of magnitude** away from 10⁻²⁰. Line 892 of this section already states **ε(1 meV) ~ 1** ⟹ **§8.1 and S-E5 directly conflict** (same symbol, two scales).
> · **② E_c is an identity (semi-fitted), not a【Derivation】**: see the correction box above — `E_c = 1TeV·ε(1TeV)^{1/β} = 1.000000 meV`, M_Pl cancels, and "same order as the dark-energy scale" restates anchor 2 ⟹ **circular**.
> · **③ Γ_flux is undefined (not identifiable)**: the string `Γ_flux` occurs **twice** in the whole paper, both inside the same prediction sentence, with **no expression**. The observable is **one real number** (the linewidth Γ) ⟹ unknowns ≥ one free function ⟹ same disease as round 45 (axiom promotion) and round 52 (non-identifiable split) — **the fourth occurrence**. Criterion: **unknowns > equations ⟹ not identifiable**.
> · **④ Dilemma**: the standard side already has a mechanism for the graviton mode's **intrinsic decay rate** and has extracted it (GMP 1970s → Haldane 2016 geometric theory → Liang et al., Nature 628, 78 (2024) experiment → Balram–Sreejith–Jain, PRL 133, 246605 (2024) splitting → Du, arXiv:2509.04408 (2025) effective theory → IOP Rep. Prog. Phys. (2025) decay-rate extraction; mechanism = decay into the **two-magnetoroton continuum**). If ε = O(1), then Γ_flux is **of the same order** as Γ_Coulomb ⟹ **"framework-unique, absent in standard condensed matter" and "consistent with experiment" cannot both hold**.
> · **⑤ Side finding**: ε₀ had **four variants** (7.6 / 7.7 / 7.67 / 7.751 ×10⁻²⁰, a 2% spread); now unified to 7.731×10⁻²⁰.
> · **Verdict**: S-E5's `ε ~ 10⁻²⁰` = **failure**; the【Derivation】label on `E_c` = **semi-fitted**; testability = **not identifiable**; "framework-unique" = **not established**. ⟹ **both the ★★★ rating of S-6 and its "framework-unique" positioning must be downgraded**; the list's claim of "the only ★★★ and unique item" does not hold. Repair paths: ① (mandatory) change S-E5's ε to `ε(FQH scale) ≈ O(1)` and "linewidth excess" to "an additional term of the same order as Γ_Coulomb"; ② (the only route to revival) **supply an expression for Γ_flux** and show it is an **independent** contribution relative to the standard Γ; ③ if neither, downgrade to "directional claim, no quantitative content".
"""

sub_once(ZH, "\n### 8.2 统计衰减因子（ε_B）与暗物质",
         BLOCK_ZH + "\n### 8.2 统计衰减因子（ε_B）与暗物质", "ZH-C1 插入第53轮块")
sub_once(EN, "\n### 8.2 Statistical decay factor (ε_B) and dark matter",
         BLOCK_EN + "\n### 8.2 Statistical decay factor (ε_B) and dark matter", "EN-C1 round-53 block")

print()
print("=== D. §5.8 的 S-E5 预言句更正 ===")
sub_once(ZH,
         "（ε~10⁻²⁰ 泄漏项，线宽余项）——极低温强磁场平台可测，标准凝聚态无此项（§9 S-E5）。",
         "（**原写 ε~10⁻²⁰ —— 第 53 轮更正：那是 ε(M_Pl)，FQH 能标下按 ε(E) = ε₀(M_Pl/E)^β 应为 ε ≈ O(1)**；\n"
         "    故「线宽余项」应读作「与 Γ_Coulomb 同量级的附加项」；且 **Γ_flux 至今无表达式** ⟹ 目前**不可识别**；\n"
         "    「标准凝聚态无此项」亦未成立（标准侧已有内在衰减率机制，见 §8.1 第 53 轮块））——极低温强磁场平台可测（§9 S-E5）。",
         "ZH-D1 S-E5 预言句")

sub_once(EN,
         "(ε~10⁻²⁰ leakage term, linewidth excess) — measurable on extremely-low-temperature high-magnetic-field platforms; standard condensed matter has no such term (§9 S-E5).",
         "(**originally written ε~10⁻²⁰ — round-53 correction: that is ε(M_Pl); at FQH scales ε(E) = ε₀(M_Pl/E)^β gives ε ≈ O(1)**; hence \"linewidth excess\"\n"
         "    should read \"an additional term of the same order as Γ_Coulomb\"; and **Γ_flux still has no expression** ⟹ currently **not identifiable**;\n"
         "    \"standard condensed matter has no such term\" is also not established — the standard side already has an intrinsic decay-rate mechanism, see the round-53 block in §8.1) — measurable on extremely-low-temperature high-magnetic-field platforms (§9 S-E5).",
         "EN-D1 S-E5 sentence")

print()
print("=== E. §9 的 S-E5 表行更正 ===")
sub_once(ZH,
         "| **S-E5** | **FQH 引力子模衰减率含 ε 项**（Γ=Γ_Coulomb+ε·Γ_flux，ε~10⁻²⁰ 泄漏；本框架预言，v1.29） | 极低温强磁场 FQH 平台（线宽余项） | 可检验（框架独有） |",
         "| **S-E5** | **FQH 引力子模衰减率含 ε 项**（Γ=Γ_Coulomb+ε·Γ_flux；v1.29 原写 `ε~10⁻²⁰` —— **第 53 轮更正为 FQH 能标下 ε ≈ O(1)**，差 18–21 个数量级；且 **Γ_flux 无表达式** ⟹ 未定义） | 极低温强磁场 FQH 平台 | ⚠️ **降为「方向性主张、无定量」**（第 53 轮：能标错置 + 不可识别 + 「独有」未成立） |",
         "ZH-E1 S-E5 表行")

sub_once(EN,
         "| **S-E5** | **FQH graviton-mode decay rate contains ε term** (Γ=Γ_Coulomb+ε·Γ_flux, ε~10⁻²⁰ leakage; framework prediction, v1.29) | extremely-low-temperature high-field FQH platforms (linewidth excess) | testable (framework-unique) |",
         "| **S-E5** | **FQH graviton-mode decay rate contains ε term** (Γ=Γ_Coulomb+ε·Γ_flux; v1.29 wrote `ε~10⁻²⁰` — **round 53 corrects this to ε ≈ O(1) at FQH scales**, a gap of 18–21 orders of magnitude; and **Γ_flux has no expression** ⟹ undefined) | extremely-low-temperature high-field FQH platforms | ⚠️ **downgraded to \"directional claim, no quantitative content\"** (round 53: scale misplacement + not identifiable + \"unique\" not established) |",
         "EN-E1 S-E5 row")

print()
print("=== F. 摘要/预言清单里的 S-E5 降调 ===")
sub_once(ZH,
         "**FQH 引力子模 ε 项**（S-E5，本框架预言）",
         "**FQH 引力子模 ε 项**（S-E5；**第 53 轮降调**：ε 曾被错标为 10⁻²⁰，FQH 能标下实为 O(1)，且 Γ_flux 至今无定义 ⟹ **方向性主张、无定量**）",
         "ZH-F1 摘要降调")

sub_once(EN,
         "**FQH graviton-mode ε term** (S-E5, framework prediction)",
         "**FQH graviton-mode ε term** (S-E5; **downgraded in round 53**: ε was mislabelled 10⁻²⁰, actually O(1) at FQH scales, and Γ_flux is still undefined ⟹ **directional claim, no quantitative content**)",
         "EN-F1 abstract downgrade")

print()
print("=" * 92)
print("  汇总：通过 {} 项，失败 {} 项".format(len(OK), len(XX)))
if XX:
    print("  失败：{}".format(", ".join(XX)))
print("=" * 92)
