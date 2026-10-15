# -*- coding: utf-8 -*-
"""第 95 轮补丁：候选池清尾（四条结项）＋ #2 判决补录进论文。
ZH 4 处 ＋ EN 4 处 ＋ 清单 9 处 ＋ 交接说明 2 处。
锚点一律取整行、sub_once 显式报未命中（陷阱 73/74）。插入块内无空行（陷阱 74 子坑）。"""
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
LI = os.path.join(BASE, "工程期望清单.md")
HH = os.path.join(BASE, "..", "环境交接说明.md")

OK = 0; BAD = 0
def sub_once(path, old, new, tag):
    global OK, BAD
    t = io.open(path, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        BAD += 1; print("  [XX] {:<40} 命中 {} 次 —— 拒绝".format(tag, n)); return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    OK += 1; print("  [OK] {:<40} 已改".format(tag))

# ================================================================ ZH-1: §8.1 N-40 注
Z1_ANCHOR = "  四值跨度 2% ⟹ 现统一为**由定义式 ε₀ = ε(1TeV)/(M_Pl/1TeV)^β 算得的值**。E_c 对 ε₀ 敏感，故此项须唯一。）"
Z1_NOTE = (
    "> ⚠️ **第 95 轮注（N-40：能标是输入、且不可独立解释）**：上面**两个能标（1 TeV / 1 meV）都是锚点（输入）**，不是导出值 ——\n"
    "> 对**任意** `E*` 都存在 `(ε₀*, β*)` 使两锚点**同时精确成立**（一维简并族：`β*(E*) = ln(1/η)/ln(E*/1meV)`；\n"
    "> 实测 `E*` = 0.246 / 0.969 / 5 / 100 TeV 均给 `ε(E*) = η` 至 1e-15）⟹ **`ε(1 TeV) ≈ η` 的匹配不携带能标信息**。\n"
    "> 因此「框架独立解释为何重子能标 ~1 TeV」= **判否**（「电弱」全文 2 处、均与重子能标无关；**无任何重子能标机制** —— CM-2：「框架没给出它」）。\n"
    "> ⟹ **引用 `ε(1 TeV) = 6×10⁻¹⁰ ≈ η` 时必须写明 1 TeV 是输入**（候选池 #1 由此结项）。"
)
sub_once(ZH, Z1_ANCHOR, Z1_ANCHOR + "\n" + Z1_NOTE, "ZH-1 §8.1 N-40 注")

# ================================================================ ZH-2: §8.1 第 53 轮框尾 C-54 短注
Z2_ANCHOR = "> **仍成立**：**meV 量级**这个量级结论（与 β 的敏感度无关）。详见第 53 轮块（本节末）。"
Z2_NOTE = (
    "> ⚠️ **第 95 轮补（C-54）**：上文的「（(E_c)⁴ 差 27 倍，O(1) 系数待定）」里**「O(1) 系数」的期待已判否** ——\n"
    "> 定量识别 `ρ_Λ = E_c⁴/(ℏc)³` 比观测**小 23.76 倍**，且无机制的天然因子救不回来（`4! = 24`、`e^π`、`8π` 均不够）；\n"
    "> **判决 = 放弃该识别（保住 meV 量级）**，详见 §8.4 第 95 轮块。"
)
sub_once(ZH, Z2_ANCHOR, Z2_ANCHOR + "\n" + Z2_NOTE, "ZH-2 §8.1 C-54 短注")

# ================================================================ ZH-3: §8.4 主判决块
Z3_ANCHOR = "【推导】暗能量 = ε_A 饱和区贡献 ρ_Λ ~ (E_c)⁴；饱和能标随宇宙膨胀缓慢漂移 E_c(z) = E_c,0(1+z)^ε ⟹"
Z3_BLOCK = (
    "> **【v2.9 判决注（第 95 轮 C-54）：`ρ_Λ = E_c⁴` 的定量识别已放弃】** 上句的【推导】应降调为**量级陈述**：**量级（meV 尺度）成立、定量识别不成立**。判决（2026-09-17，`ΩΛ缺口判决_二选一与放弃.md`，OM-1…OM-6；第 95 轮补录进论文）：\n"
    "> ① **数值**：`Ω_Λ(框架) = 0.0290` vs 观测 `0.6889 ± 0.0056`，差 **23.76 倍**（复算两路互验：`ρ_Λ = E_c⁴/(ℏc)³` 与闭式 `8π/3·(R_H/l_P)²·ε₀^{4/β}`）；\n"
    "> ② **二选一**：配住 Ω_Λ 的联立解要 `ε₀` 砍 39%、`β` 加 2.26% ⟹ `E_c` 变成 2.25 meV（2.2×）—— **框架无法同时给出正确的暗能量能标与正确的暗能量密度**；\n"
    "> ③ **敏感度病态**：`dlnΩ_Λ/dβ = 465`（要让 Ω_Λ 精度在 10% 内，β 须精确到 0.021%）；\n"
    "> ④ **拒绝数值占卜**：最接近的天然因子（`4! = 24`、`e^π = 23.14`、`π⁴/4 = 24.35`、`8π = 25.13`）与 23.76 的偏差均 ≥1% —— 凑得上的不少、**有机制的没有**；\n"
    "> ⑤ 另一条构造 `ρ_P/N` 与观测差 12.2 倍（两条路相差 289 倍）⟹ **都还差一个 O(10) 因子**。\n"
    "> ⛔ **不得**再以「框架给出暗能量密度 / 组分比例」引用本节；引用「meV 量级」时须同时写本判决。"
)
sub_once(ZH, Z3_ANCHOR, Z3_ANCHOR + "\n\n" + Z3_BLOCK, "ZH-3 §8.4 主判决块")

# ================================================================ ZH-4: P4 尾注
Z4_TARGET = "观测者模型与宇宙学侧（§8）正式同源。"
Z4_NOTE = "〔⚠️ **第 95 轮注（N-40）**：「重子不对称（6×10⁻¹⁰ @1TeV）」的**能标是输入**（一维简并族，见 §8.1 第 95 轮注）⟹「三源同根」成立于**同一 ε 函数**的意义上，**不含对能标的预言**。〕"
sub_once(ZH, Z4_TARGET, Z4_TARGET + Z4_NOTE, "ZH-4 P4 尾注")

# ================================================================ EN-1: §8.1 N-40
E1_ANCHOR = "  ε₀ = ε(1TeV)/(M_Pl/1TeV)^β. E_c is sensitive to ε₀, so this constant must be unique.)"
E1_NOTE = (
    "> ⚠️ **Round-95 note (N-40: the scales are inputs and cannot be independently explained)**: both energy scales above (**1 TeV / 1 meV**) are **anchors (inputs)**, not derived values — for **any** `E*` there exists `(ε₀*, β*)` making both anchors hold **exactly** (a one-parameter degenerate family: `β*(E*) = ln(1/η)/ln(E*/1meV)`; tested `E*` = 0.246 / 0.969 / 5 / 100 TeV, all give `ε(E*) = η` to 1e-15) ⟹ **the match `ε(1 TeV) ≈ η` carries no information about the scale**. Hence \"the framework independently explains why the baryon scale is ~1 TeV\" = **ruled out** (\"electroweak\" appears only twice in the text, both unrelated to the baryon scale; **there is no baryon-scale mechanism** — CM-2: \"the framework does not provide it\"). ⟹ **citing `ε(1 TeV) = 6×10⁻¹⁰ ≈ η` must state that 1 TeV is an input** (candidate-pool #1 thereby closed)."
)
sub_once(EN, E1_ANCHOR, E1_ANCHOR + "\n" + E1_NOTE, "EN-1 §8.1 N-40 注")

# ================================================================ EN-2: §8.1 框尾 C-54
E2_ANCHOR = "> **Still valid**: the **meV order of magnitude** (independent of β sensitivity). See the round-53 block at the end of this section."
E2_NOTE = (
    "> ⚠️ **Round-95 addendum (C-54)**: in the text above, the expectation attached to \"(E_c)⁴ differs by a factor 27; O(1) coefficient undetermined\" is **ruled out** — the quantitative identification `ρ_Λ = E_c⁴/(ℏc)³` is **23.76× smaller** than observation, and no mechanism-bearing natural factor rescues it (`4! = 24`, `e^π`, `8π` all fail); **verdict = abandon the identification (keep the meV order of magnitude)** — see the round-95 block in §8.4."
)
sub_once(EN, E2_ANCHOR, E2_ANCHOR + "\n" + E2_NOTE, "EN-2 §8.1 C-54 短注")

# ================================================================ EN-3: §8.4 主判决块
E3_ANCHOR = "【Derivation】 Dark energy = contribution of the ε_A saturation region ρ_Λ ~ (E_c)⁴; the saturation scale drifts slowly with cosmic expansion E_c(z) = E_c,0(1+z)^ε ⟹"
E3_BLOCK = (
    "> **【v2.9 verdict note (round 95, C-54): the quantitative identification `ρ_Λ = E_c⁴` is abandoned】** The【Derivation】tag above must be demoted to a **statement of order of magnitude**: **the meV scale holds; the quantitative identification does not**. Verdict (2026-09-17, `ΩΛ缺口判决_二选一与放弃.md`, OM-1…OM-6; entered into the paper in round 95): ① **numbers**: `Ω_Λ(framework) = 0.0290` vs observed `0.6889 ± 0.0056`, a **23.76× gap** (two cross-checked routes: `ρ_Λ = E_c⁴/(ℏc)³` and the closed form `8π/3·(R_H/l_P)²·ε₀^{4/β}`); ② **a clean dichotomy**: the joint solution matching Ω_Λ requires `ε₀` cut by 39% and `β` raised by 2.26% ⟹ `E_c` becomes 2.25 meV (2.2×) — **the framework cannot simultaneously give the correct dark-energy scale and the correct dark-energy density**; ③ **pathological sensitivity**: `dlnΩ_Λ/dβ = 465` (β must be accurate to 0.021% for Ω_Λ within 10%); ④ **numeric divination refused**: the closest natural factors (`4! = 24`, `e^π = 23.14`, `π⁴/4 = 24.35`, `8π = 25.13`) all deviate ≥1% from 23.76 — many near-misses, none with a mechanism; ⑤ the alternative construction `ρ_P/N` is 12.2× off (the two routes differ by 289×) ⟹ **both are still one O(10) factor short**. ⛔ Do **not** cite this section as \"the framework gives the dark-energy density / composition\"; citing the \"meV order of magnitude\" must include this verdict."
)
sub_once(EN, E3_ANCHOR, E3_ANCHOR + "\n\n" + E3_BLOCK, "EN-3 §8.4 主判决块")

# ================================================================ EN-4: P4 尾注
E4_TARGET = "the observer model and cosmology side (§8) formally share one origin."
E4_NOTE = " (⚠️ **Round-95 note (N-40)**: the **scale** of \"baryon asymmetry (6×10⁻¹⁰ @1TeV)\" is an **input** (one-parameter degenerate family; see the round-95 note in §8.1) ⟹ \"one origin\" holds in the sense of **a single ε function**, and **carries no prediction of the scale**.)"
sub_once(EN, E4_TARGET, E4_TARGET + E4_NOTE, "EN-4 P4 尾注")

# ================================================================ LI-1..4: 池条目
LI1_OLD = "1. **重子不对称 η** — `ε(0.969 TeV) = 6.14×10⁻¹⁰`；⚠️ 能标是**配出来的**，不是预言（需独立解释为何 ~1 TeV）"
LI1_NEW = ("1. ✅ **已结项（第 95 轮）** —— 判定：**半拟合**（**一维简并族**：对任意 `E*` 都存在 (ε₀*, β*) 使两锚点同时精确成立 ⟹ **能标不被约束**）；"
           "「需独立解释为何 ~1 TeV」= **判否**（**N-40**：「框架没给出它」；无任何重子能标机制）。\n"
           "   ❌ ~~原条目~~：**重子不对称 η** — `ε(0.969 TeV) = 6.14×10⁻¹⁰`；⚠️ 能标是**配出来的**，不是预言（需独立解释为何 ~1 TeV）")
sub_once(LI, LI1_OLD, LI1_NEW, "LI-1 池条目 #1 结项")

LI2_OLD = "2. **暗能量能标** — A2 两参数锁定 `E_c = 1.0181 meV`；⚠️ 但 `dlnΩ_Λ/dβ = 465`，β +1% ⟹ E_c ×2.0"
LI2_NEW = ("2. ✅ **已结项（第 95 轮）** —— 判决（2026-09-17，OM-1…OM-6；**第 95 轮补录进论文 = C-54**）：**保住** meV 量级／**放弃** `ρ_Λ = E_c⁴/(ℏc)³` 的定量识别"
           "（差 **23.76 倍**；二选一：配住 Ω_Λ 则 `E_c → 2.25 meV`；β 敏感度 465；拒绝数值占卜）。\n"
           "   ❌ ~~原条目~~：**暗能量能标** — A2 两参数锁定 `E_c = 1.0181 meV`；⚠️ 但 `dlnΩ_Λ/dβ = 465`，β +1% ⟹ E_c ×2.0")
sub_once(LI, LI2_OLD, LI2_NEW, "LI-2 池条目 #2 结项")

LI3_OLD = "4. **湍流 / 输运** — `η/s → 1/4π`（KSS 界）"
LI3_NEW = ("4. ✅ **已结项（第 95 轮）** —— 判定：**postdiction / 一致性**（`η/s → 1/4π` = **KSS 界，2001**，非框架独有）；与 **H2 行**（S-3 收口）同源，双轨登记已合并（**C-55**）。\n"
           "   ❌ ~~原条目~~：**湍流 / 输运** — `η/s → 1/4π`（KSS 界）")
sub_once(LI, LI3_OLD, LI3_NEW, "LI-3 池条目 #4 结项")

LI4_OLD = "6. **规范群结构（§5）** — SU(3)×SU(2)×U(1) ↔ 配对阶数 n = 3,2,1"
LI4_NEW = ("6. ✅ **已结项（第 95 轮）** —— 两级判定：**结构对应 = 解释性（判别力 0）**；**数值映射 = 判否**（**N-34**：差 5.03 倍 ≈ 100σ、4 个换算因子全缺）。\n"
           "   ❌ ~~原条目~~：**规范群结构（§5）** — SU(3)×SU(2)×U(1) ↔ 配对阶数 n = 3,2,1")
sub_once(LI, LI4_OLD, LI4_NEW, "LI-4 池条目 #6 结项")

# ================================================================ LI-5..7: 剩余待办三行
LI5_OLD = "**剩余待办（全部）**：候选池 **#1 η 能标／#2 暗能量能标／#4 η/s（已判不独有）／~~#5 PPN 优越系~~（✅ 第 93 轮结项）／~~#7 void-CPT-κ~~（✅ 第 94 轮结项）／#8 EMRI**；**A1 Lean 资产恢复**。⚠️ **有明确可判定入口的只有 A1**。"
LI5_NEW = "**剩余待办（全部）**：候选池 **~~#1 η 能标~~／~~#2 暗能量能标~~／~~#4 η/s~~／~~#5 PPN 优越系~~／~~#6 规范群结构~~／~~#7 void-CPT-κ~~（以上 ✅ 第 93–95 轮结项）／#8 EMRI（等 LISA）**；**A1 Lean 资产恢复**。⚠️ **有明确可判定入口的只有 A1**。"
sub_once(LI, LI5_OLD, LI5_NEW, "LI-5 剩余待办行①")

LI6_OLD = "**剩余待办**：候选池 **#1/#2/#4/#7/#8（#5 ✅ 93 轮；void-CPT-κ ✅ 94 轮）**（#4 η/s = H2 的一部分，已判不独有）；**A1（Lean 资产恢复）**。"
LI6_NEW = "**剩余待办**：候选池 **~~#1/#2/#4/#6~~（✅ 第 95 轮清尾）／~~#5~~（✅ 93 轮）／~~void-CPT-κ~~（✅ 94 轮）／#8 EMRI（等 LISA）**；**A1（Lean 资产恢复）**。"
sub_once(LI, LI6_OLD, LI6_NEW, "LI-6 剩余待办行②")

LI7_OLD = "**剩余待办**（组 III–VI）：候选池 **#1（η 能标）/#2（暗能量能标）/#4（η/s）/~~#5（PPN 优越系）~~（✅ 93 轮）／~~#7（void-CPT-κ）~~（✅ 94 轮）/#8（EMRI）**；"
LI7_NEW = "**剩余待办**（组 III–VI）：候选池 **~~#1（η 能标）~~／~~#2（暗能量能标）~~／~~#4（η/s）~~／~~#6（规范群结构）~~（以上 ✅ 第 95 轮清尾）／~~#5（PPN 优越系）~~（✅ 93 轮）／~~#7（void-CPT-κ）~~（✅ 94 轮）／#8（EMRI，等 LISA）**；"
sub_once(LI, LI7_OLD, LI7_NEW, "LI-7 剩余待办行③")

# ================================================================ LI-8: 台账三行
LI8_ANCHOR = "| **N-39** | **把（机制已撤的）void-CPT-κ 当作可维持的可检验预言（乃至「框架最强预言」）** | **负面** | **判否**：唯一机制（镜像支引力投影）已**硬否证**（5.31×/3.82×），§8.3 自写「**仅在该机制被重建后才成立**」；**不得计入可检验预言或出口计数**。⚠️ 历史出处（前否证时代表述，未回溯标注）：M5 报告「已有数据 0–3 年」四项之一、P2 报告「最强可检验预言」。 | 第 94 轮（`_voidcpt_94.py`） | 同 C-51 备忘录 |"
LI8_NEW = (
    LI8_ANCHOR + "\n"
    "| **N-40** | **把「η 能标 ~1 TeV」当作框架能导出的量（第 95 轮）** | **负面** | **判否**：**一维简并族** —— 对任意 `E*` 都存在 (ε₀*, β*) 使两锚点同时精确成立（实测 E* = 0.246/0.969/5/100 TeV 均给 ε(E*) = η 至 1e-15）⟹ **能标不被约束**；「电弱」全文 2 处、均与重子能标无关，**无任何重子能标机制**（CM-2：「框架没给出它」）。⛔ 引用「ε(1 TeV) = 6×10⁻¹⁰ ≈ η」时必须写明 **1 TeV 是输入**。 | 第 95 轮（`_candpool_95.py`） | 候选池 #1 结项 |\n"
    "| **C-54** | **#2 暗能量能标的判决（2026-09-17）从未进入论文（第 95 轮）** | **更正 / 同步** | 判决核心（「23.76 倍」「二选一」）在论文里 **0 处**；§8.4 至今把 `ρ_Λ ~ (E_c)⁴` 标【推导】、§8.1「O(1) 系数待定」未收回 ⟹ 本轮补录判决注（§8.1 两处 ＋ §8.4 一处，**中英同步**）。**判决做出 25 天（跨 90+ 轮）未被论文收到** —— 「判决做了、论文没收到」的首次完整登记。 | 第 95 轮（`_candpool_95.py`） | 同 `ΩΛ缺口判决…md` |\n"
    "| **C-55** | **候选池双轨对账（第二轮）：#4/#6 池条目过期 ＋ 回顾漏项（第 95 轮）** | **更正 / 编号** | ① **#4 η/s**：H2 行已 ✅ 收口、池条目仍挂起；② **#6 规范群结构**：判定两级完成（**N-34**）而池条目未结项；③ ⚠️ **第 93/94 轮回顾只说「#1/#2/#4」——漏了 #6**（C-18 族）。⟹ 四条一并结项；**清尾后剩 EMRI ＋ A1**。📌 规范：池表清点**脚本化**，不靠回忆。 | 第 95 轮（`_candpool_95.py`） | 同 C-53 族 |"
)
sub_once(LI, LI8_ANCHOR, LI8_NEW, "LI-8 台账 N-40/C-54/C-55")

# ================================================================ LI-9: 总账计数
LI9A_OLD = "| **负面判定** | **39 条**（**N-39 把（机制已撤的）void-CPT-κ 当作可维持的可检验预言**"
LI9A_NEW = "| **负面判定** | **40 条**（**N-40 把「η 能标 ~1 TeV」当作框架能导出的量**（第 95 轮：一维简并族 ⟹ 能标不被约束；「框架没给出它」）｜**N-39 把（机制已撤的）void-CPT-κ 当作可维持的可检验预言**"
sub_once(LI, LI9A_OLD, LI9A_NEW, "LI-9a 负面 39→40")

LI9B_OLD = "| **撤回 / 更正** | **52 条**（**C-51 / C-52 / C-53 ⭐（第 94 轮，候选池 void-CPT-κ 结项）**："
LI9B_NEW = "| **撤回 / 更正** | **54 条**（**C-54 / C-55 ⭐（第 95 轮，候选池清尾）**：**C-54** #2 暗能量能标判决从未入论文 ⟹ 补录（§8.1 两处 ＋ §8.4，中英同步）｜**C-55** 池表双轨对账（#4/#6 过期 ＋ 回顾漏项）｜**C-51 / C-52 / C-53 ⭐（第 94 轮，候选池 void-CPT-κ 结项）**："
sub_once(LI, LI9B_OLD, LI9B_NEW, "LI-9b 更正 52→54")

# ================================================================ HH-1: 交接 §三
HH1_ANCHOR = "**第 94 轮新增（候选池 void-CPT-κ 结项：机制已否证而判定未降级）**：脚本 `_voidcpt_94.py`（**VC-1…VC-10，22 项 0 失败**）。"
HH1_NEW = (
    "**第 95 轮新增（候选池清尾：四条形式结项 ＋ 一条 25 天未进论文的判决）**：脚本 `_candpool_95.py`（**CP-1…CP-10，34 项 0 失败**）。\n"
    "① ✅ **#2 判决补录（C-54）**：OM 判决（2026-09-17）「保住 meV 量级／放弃 `ρ_Λ = E_c⁴` 定量识别」在论文里 **0 处**（「23.76」「二选一」）⟹ 补录进 §8.1（两处）＋ §8.4（一处），**中英同步**。\n"
    "② ⚠️ **#1 判否（N-40）**：**一维简并族** —— 任意 `E*` 都能配住两锚点 ⟹ 能标不被约束；「独立解释为何 ~1 TeV」判否。\n"
    "③ ⚠️ **#4 / #6 结项（C-55）**：#4 η/s = postdiction（KSS 2001）；#6 规范群结构 = 结构解释性 ＋ 数值判否（N-34）；⚠️ **第 93/94 轮回顾漏了 #6**（C-18 族）。\n"
    "④ ⭐ **方法论**：**「判决做了、论文没收到」首次完整登记**（判决静默过期 25 天）；**池表清点脚本化**。\n"
    "⑤ 📌 **候选池已清尾**：剩余 = **EMRI**（等 LISA）＋ **A1**（换机资产）。\n"
    "\n"
    + HH1_ANCHOR
)
sub_once(HH, HH1_ANCHOR, HH1_NEW, "HH-1 交接 §三")

# ================================================================ HH-2: 交接 §七
HH2_ANCHOR = "0. 🎯 **当前建议（第 94 轮后）**：**候选池「void-CPT-κ」已结项** —— 判定降级为「**悬空（机制未重建）**」"
HH2_NEW = (
    "0. 🎯 **当前建议（第 95 轮后）**：**候选池清尾完成** —— 四条（#1 η 能标／#2 暗能量能标／#4 η/s／#6 规范群结构）全部形式结项；\n"
    "   清尾后剩余 = **EMRI**（等 LISA，三前提框架外）＋ **A1**（Lean 资产恢复，唯一有明确可判定入口）。\n"
    "   ⭐ **净增量**：**C-54 / C-55** ＋ **N-40** ＋ **§8.4 判决补录（中英同步）**。\n"
    "   📌 **下一步三选项**：① **A1**（资产恢复）；② **EMRI 材料包**（给 LISA 组的 S-E1–E4 打包）；③ **私审准备包**（§4.5b／§9／§8.1 ＋ 审计结论 —— C-54 刚为它添了一页）。\n"
    "\n"
    "0. 🎯 **（历史，第 94 轮后，已被上式取代）**：**候选池「void-CPT-κ」已结项** —— 判定降级为「**悬空（机制未重建）**」"
)
sub_once(HH, HH2_ANCHOR, HH2_NEW, "HH-2 交接 §七")

print()
print("=" * 100)
print("补丁：成功 {} 处，失败 {} 处".format(OK, BAD))
