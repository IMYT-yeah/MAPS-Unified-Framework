# -*- coding: utf-8 -*-
"""第 94 轮 补丁：候选池 void-CPT-κ 结项 —— C-51 / C-52 / C-53 ＋ N-39

改动面：论文 ZH/EN（摘要、§8.4、§9 表、第 90/91 轮台账 各 4-5 处）、工程期望清单、环境交接说明。
所有锚点预检单命中（29/29）。
"""
import io

ZH = "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
LIST = "工程期望清单.md"
HH = "../环境交接说明.md"

FAIL = 0


def sub_once(path, old, new, tag):
    global FAIL
    t = io.open(path, encoding="utf-8").read()
    if t.count(old) != 1:
        print("  [FAIL] {}  命中 {} 次".format(tag, t.count(old)))
        FAIL += 1
        return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    print("  [PASS] {}  已替换".format(tag))


def ins_after_line(path, sub, block, tag):
    global FAIL
    lines = io.open(path, encoding="utf-8").read().split("\n")
    idx = [i for i, s in enumerate(lines) if sub in s]
    if len(idx) != 1:
        print("  [FAIL] {}  锚命中 {} 次".format(tag, len(idx)))
        FAIL += 1
        return
    lines[idx[0] + 1:idx[0] + 1] = block.split("\n")
    io.open(path, "w", encoding="utf-8").write("\n".join(lines))
    print("  [PASS] {}  已插入（锚行 {}）".format(tag, idx[0] + 1))


def ins_before_line(path, sub, block, tag):
    global FAIL
    lines = io.open(path, encoding="utf-8").read().split("\n")
    idx = [i for i, s in enumerate(lines) if sub in s]
    if len(idx) != 1:
        print("  [FAIL] {}  锚命中 {} 次".format(tag, len(idx)))
        FAIL += 1
        return
    lines[idx[0]:idx[0]] = block.split("\n")
    io.open(path, "w", encoding="utf-8").write("\n".join(lines))
    print("  [PASS] {}  已插入（锚行 {}）".format(tag, idx[0] + 1))


# ---------------------------------------------------------------- 1. 论文 ZH（10 处）
print("=== 1. 论文 ZH：摘要 C-52 ＋ §8.4 条件性 ＋ §9 表 ＋ 两台账（含汇总/派生句）===")
sub_once(ZH,
    "暗物质 = 本支普朗克涨落残余 + 镜像支引力投影的叠加模型；**初始微扰（ε₀=7.7×10⁻²⁰）与重子不对称/暗能量三源同根**（§4.9 P4）。",
    "暗物质 = 本支普朗克涨落残余 + 镜像支引力投影的叠加模型；**初始微扰（ε₀=7.7×10⁻²⁰）与重子不对称/暗能量三源同根**（§4.9 P4）。"
    "〔⚠️ **第 94 轮注（C-52）**：暗物质的定量解释目前为**空白** —— §8.2 自标「ε_B 机制差 ~70 倍 ⟹ 仍是空白」，"
    "§8.3 的**镜像支分量已被否证**【v2.9 修正】；本点「ε_B 给出暗物质密度」「叠加模型」为**旧表述**，**以 §8.2／§8.3 为准**。〕",
    "ZH-1 摘要 C-52")

sub_once(ZH,
    "- 可检验预言：**void-CPT-κ 异常**（空洞区弱透镜偏强 + 质量-光脱耦，10–30 Mpc/h 尺度最显；候选对象 CDG-2、J0613+52）。",
    "- 可检验预言（⚠️ **条件性 —— 第 94 轮注（C-51）**：**仅当上句机制被重建后才成立**；引用不得省略本条件）："
    "**void-CPT-κ 异常**（空洞区弱透镜偏强 + 质量-光脱耦，10–30 Mpc/h 尺度最显；候选对象 CDG-2、J0613+52）。",
    "ZH-2 §8.4 条件性")

sub_once(ZH, "可检验（分析方案已给出） |",
    "可检验（分析方案已给出）⚠️ **机制已撤（§8.3 否证）：仅重建后成立（第 94 轮）** |",
    "ZH-3 §9 表第 2 行")

sub_once(ZH,
    "> | 2 | void-CPT-κ 异常 | **真预言** | 分析方案已给出、结果未出 |",
    "> | 2 | void-CPT-κ 异常 | ~~**真预言**~~ **悬空（机制未重建）** | 分析方案已给出、结果未出；"
    "⚠️ **第 94 轮 C-51**：机制（镜像支投影）已硬否证（5.31×/3.82×） |",
    "ZH-4 90 台账行")

sub_once(ZH, "**真预言 11** ｜ **推导 / 数值 3**",
    "~~**真预言 11**~~ **真预言 10 ＋ 悬空（机制未重建）1** ｜ **推导 / 数值 3**",
    "ZH-5 90 汇总")

sub_once(ZH, "**关键读法（此前没有一处写出来）**：11 条「真预言」里",
    "**关键读法（此前没有一处写出来）**：~~11~~ **10** 条「真预言」里",
    "ZH-6 90 派生句")

sub_once(ZH, "**报「出口」前先数「独立关系」而不是「行数」**。",
    "**报「出口」前先数「独立关系」而不是「行数」**。\n"
    "> ⚠️ **【第 94 轮更正（C-51）】** 本表第 2 行「真预言」**降级为「悬空（机制未重建）」**：该行「依据」列**未引任何已登记轮次**"
    "（违反本块自己的规范），而其机制侧早已登记【已否证】—— §8.3【v2.9 修正】（读法 A 低 5.31 倍／读法 B 高 3.82 倍）、"
    "清单 **S-8**、第 84 轮审计。⟹ 汇总按 **10 ＋ 悬空 1** 读；「独立出口」结论（EMRI 系）不变。",
    "ZH-7 90 块尾注")

sub_once(ZH,
    "> | §8.4 | void-CPT-κ 可检验预言 | **真预言** | 未观测（DES/Y3） |",
    "> | §8.4 | void-CPT-κ 可检验预言 | ~~**真预言**~~ **悬空（机制未重建）** | 未观测（DES/Y3）；"
    "⚠️ **第 94 轮 C-51**：机制已被否证（§8.3） |",
    "ZH-8 91 台账行")

sub_once(ZH, "**真预言 2 ｜ postdiction 3",
    "~~**真预言 2**~~ **真预言 1 ＋ 悬空 1** ｜ postdiction 3",
    "ZH-9 91 汇总")

sub_once(ZH, "（本条与第 88 轮 C-43 同族）。",
    "（本条与第 88 轮 C-43 同族）。\n"
    "> ⚠️ **【第 94 轮更正（C-51，同第 90 轮块）】** 本表 §8.4 行「真预言」**降级为「悬空（机制未重建）」**（机制已否证，§8.3）；"
    "汇总按 **1 ＋ 悬空 1** 读。",
    "ZH-10 91 块尾注")

# ---------------------------------------------------------------- 2. 论文 EN（10 处）
print("=== 2. 论文 EN：同步 10 处 ===")
sub_once(EN,
    "**the initial perturbation (ε₀=7.7×10⁻²⁰) shares one root with baryon asymmetry and dark energy — three sources, one origin** (§4.9 P4).",
    "**the initial perturbation (ε₀=7.7×10⁻²⁰) shares one root with baryon asymmetry and dark energy — three sources, one origin** (§4.9 P4)."
    " 〔⚠️ **Round-94 note (C-52)**: the quantitative account of dark matter is currently **blank** — §8.2 self-marks "
    "\"the ε_B mechanism is off by ~70× ⟹ still blank\", and the **mirror-branch component was falsified** (§8.3, v2.9 correction). "
    "The phrases \"yields the dark-matter density\" / \"superposition model\" above are **legacy wording**; §8.2/§8.3 govern.〕",
    "EN-1 abstract C-52")

sub_once(EN,
    "- Testable prediction: **void-CPT-κ anomaly** (void regions with stronger weak lensing + mass–light decoupling, most prominent at 10–30 Mpc/h scales; candidate objects CDG-2, J0613+52).",
    "- Testable prediction (⚠️ **conditional — round-94 note (C-51)**: **holds only if the mechanism above is rebuilt**; this condition must not be omitted): "
    "**void-CPT-κ anomaly** (void regions with stronger weak lensing + mass–light decoupling, most prominent at 10–30 Mpc/h scales; candidate objects CDG-2, J0613+52).",
    "EN-2 §8.4 conditional")

sub_once(EN, "testable (analysis scheme given) |",
    "testable (analysis scheme given) ⚠️ **mechanism withdrawn (§8.3 falsification): holds only if rebuilt (round 94)** |",
    "EN-3 §9 table row 2")

sub_once(EN,
    "> | 2 | void-CPT-κ anomaly | **true prediction** | analysis plan given, no result yet |",
    "> | 2 | void-CPT-κ anomaly | ~~**true prediction**~~ **dangling (mechanism not rebuilt)** | analysis plan given, no result yet; "
    "⚠️ **round-94 C-51**: mechanism (mirror-branch projection) hard-falsified (5.31×/3.82×) |",
    "EN-4 90 ledger row")

sub_once(EN, "**Tally (23 rows)**: **true prediction 11** | derivation/numerics 3",
    "**Tally (23 rows)**: ~~**true prediction 11**~~ **true prediction 10 + dangling (mechanism not rebuilt) 1** | derivation/numerics 3",
    "EN-5 90 tally")

sub_once(EN, "among the 11 \"true predictions\"",
    "among the ~~11~~ **10** \"true predictions\"",
    "EN-6 90 derivative")

sub_once(EN, "before quoting an \"exit\" count**.",
    "before quoting an \"exit\" count**.\n"
    "> ⚠️ **【Round-94 correction (C-51)】** Row 2's \"true prediction\" is **downgraded to \"dangling (mechanism not rebuilt)\"**: "
    "its rationale column cites **no registered round** (against this block's own norm), while its mechanism side was long registered as falsified — "
    "§8.3 【v2.9 correction】 (reading A 5.31× low / reading B 3.82× high), checklist **S-8**, round-84 audit. "
    "⟹ read the tally as **10 + dangling 1**; the \"independent exits\" conclusion (EMRI set) is unchanged.",
    "EN-7 90 block-end note")

sub_once(EN,
    "> | §8.4 | void-CPT-κ testable prediction | **true prediction** | unobserved (DES/Y3) |",
    "> | §8.4 | void-CPT-κ testable prediction | ~~**true prediction**~~ **dangling (mechanism not rebuilt)** | unobserved (DES/Y3); "
    "⚠️ **round-94 C-51**: mechanism falsified (§8.3) |",
    "EN-8 91 ledger row")

sub_once(EN, "true prediction 2 | postdiction 3",
    "~~true prediction 2~~ **true prediction 1 + dangling 1** | postdiction 3",
    "EN-9 91 tally")

sub_once(EN, "(same family as round 88's C-43).",
    "(same family as round 88's C-43).\n"
    "> ⚠️ **【Round-94 correction (C-51), same as the round-90 block】** The §8.4 row is downgraded to **\"dangling (mechanism not rebuilt)\"** "
    "(mechanism falsified, §8.3); read the tally as **1 + dangling 1**.",
    "EN-10 91 block-end note")

# ---------------------------------------------------------------- 3. 清单
print("=== 3. 清单：池条目结项 ＋ 对账注 ＋ 三行更新 ＋ 台账行 ＋ 计数 ＋ 四条新行 ===")
lines = io.open(LIST, encoding="utf-8").read().split("\n")
idx = [i for i, s in enumerate(lines) if s.startswith("8. **void-CPT-κ 异常**")]
if len(idx) != 1:
    print("  [FAIL] LIST-0  池条目锚命中 {} 次".format(len(idx)))
    FAIL += 1
else:
    orig = lines[idx[0]]
    new_block = [
        "8. ✅ **已结项（第 94 轮）** —— **判定降级**：~~真预言~~ ⟹ **悬空（机制未重建）**（**C-51**）。"
        "机制侧：镜像支投影**已硬否证**（读法 A 低 5.31 倍／读法 B 高 3.82 倍；§8.3【v2.9 修正】）；"
        "四处下游（§9 表／§8.4／第 90＋91 轮台账）已同步降级；登记 **N-39**。",
        "   ❌ ~~原条目~~：" + (orig[3:] if orig.startswith("8. ") else orig),
        "> ⚠️ **编号对账（第 94 轮 C-53）**：本表与 §1.x「剩余待办」行的 **#7/#8 互换**（本表 #7=EMRI、#8=void-CPT-κ；"
        "剩余行 #7=void-CPT-κ、#8=EMRI）；本表 #6=规范群结构，而第 74 轮回溯「组 III」C6=宇宙学动力学（已于第 75 轮结项）。"
        "⟹ **引用候选池条目一律用名字，#号不作引用键**。（另：第 93 轮漏改的 #5 与台账 C6 过期，本轮已补 —— 见 C-53 行。）",
    ]
    lines[idx[0]:idx[0] + 1] = new_block
    io.open(LIST, "w", encoding="utf-8").write("\n".join(lines))
    print("  [PASS] LIST-0  池条目 8 已结项 ＋ 对账注（行 {}）".format(idx[0] + 1))

sub_once(LIST, "／#7 void-CPT-κ／#8 EMRI",
         "／~~#7 void-CPT-κ~~（✅ 第 94 轮结项）／#8 EMRI", "LIST-1 剩余待办①（L192）")
sub_once(LIST, "候选池 **#1/#2/#4/#5/#7/#8**（#4 η/s = H2 的一部分，已判不独有）",
         "候选池 **#1/#2/#4/#7/#8（#5 ✅ 93 轮；void-CPT-κ ✅ 94 轮）**（#4 η/s = H2 的一部分，已判不独有）",
         "LIST-2 剩余待办②（L212）")
sub_once(LIST, "#5（PPN 优越系）/#7（void-CPT-κ）/#8（EMRI）",
         "~~#5（PPN 优越系）~~（✅ 93 轮）／~~#7（void-CPT-κ）~~（✅ 94 轮）/#8（EMRI）",
         "LIST-3 剩余待办③（L226，含第 93 轮漏改补正）")
sub_once(LIST, "**C6 宇宙学动力学（加速度＋连续性方程，§8.6.3 自认仍缺）**／C7 void-CPT-κ／C8 EMRI。",
         "**C6 ✅ 宇宙学动力学（第 75 轮结项 ⟹ I-20；「自认仍缺」已裁决为「不该有」）**／**C7 ~~void-CPT-κ~~（✅ 第 94 轮结项：悬空）**／C8 EMRI。",
         "LIST-4 台账行 C6/C7")

sub_once(LIST, "| **负面判定** | **38 条**（**N-38",
         "| **负面判定** | **39 条**（**N-39 把（机制已撤的）void-CPT-κ 当作可维持的可检验预言**"
         "（第 94 轮：唯一机制已硬否证 5.31×/3.82×；仅重建后成立 ⟹ **不得计入预言 / 出口**）｜**N-38",
         "LIST-5 负面 38 → 39")

sub_once(LIST, "| **撤回 / 更正** | **49 条**（**C-48 / C-49 / C-50 ⭐（第 93 轮，候选池 #5 结项）**：",
         "| **撤回 / 更正** | **52 条**（**C-51 / C-52 / C-53 ⭐（第 94 轮，候选池 void-CPT-κ 结项）**："
         "**C-51** void-CPT-κ 判定降级 ⟹ **悬空（机制未重建）**（四处下游同步：§9 表／§8.4／第 90＋91 轮台账）｜"
         "**C-52** 摘要第 5 条暗物质旧表述加限定（以 §8.2「空白」/§8.3「已否证」为准）｜"
         "**C-53** 候选池引用对账（#7/#8 两套互换、#6 异义、#5 漏改、台账 C6 过期）｜**C-48 / C-49 / C-50 ⭐（第 93 轮，候选池 #5 结项）**：",
         "LIST-6 更正 49 → 52")

ROWS = """| **C-51** | **void-CPT-κ 的「真预言」判定降级 ⟹ 悬空（四处下游同步）（第 94 轮）** | **更正 / 判定** | 机制侧早已登记【已否证】（§8.3【v2.9 修正】：读法 A 低 5.31 倍／读法 B 高 3.82 倍；§8.3 自写「仅在该机制被重建后才成立」），而四处下游未同步：**§9 表第 2 行**（加机制警告）、**§8.4 列表**（加条件性）、**第 90 轮台账**（~~真预言~~ ⟹ **悬空**；汇总 11 → 10＋悬空 1；派生句「11 条」→「10 条」）、**第 91 轮台账**（同；汇总 2 → 1＋悬空 1）。⚠️ 第 90 轮该行「依据」列**未引任何已登记轮次**（违反本块自己的规范）。 | 第 94 轮（`_voidcpt_94.py` VC-1…VC-10） | —— |
| **C-52** | **摘要第 5 条的暗物质表述与 §8.2／§8.3 不相容（第 94 轮）** | **更正 / 口径** | 「ε_B **给出**暗物质密度」「暗物质 = … + **镜像支引力投影**的叠加模型」——而 §8.2 自标「ε_B 机制差 ~70 倍 ⟹ **仍是空白**」、§8.3 的镜像支分量**已被否证**。⟹ **不删原句**，加第 94 轮限定注（以 §8.2／§8.3 为准；中英同步）。 | 第 94 轮 | —— |
| **C-53** | **候选池引用对账（第 94 轮）** | **更正 / 编号** | ① 池表 **#7=EMRI、#8=void-CPT-κ** vs 「剩余待办」行 **#7=void-CPT-κ、#8=EMRI**（**两套互换**）；② 池表 #6=规范群结构 vs 第 74 轮回溯「组 III」C6=宇宙学动力学（**异义**）；③ 第 93 轮漏改一处 **`#5（PPN 优越系）`**（括号写法不在锚点内）——本轮补划线；④ 台账行 **C6 状态过期**（第 75 轮已结项未标；**C-19 族第 12 条**）——已就地补标。⟹ 池表加对账注：**引用一律用名字**。 | 第 94 轮 | —— |
| **N-39** | **把（机制已撤的）void-CPT-κ 当作可维持的可检验预言（乃至「框架最强预言」）** | **负面** | **判否**：唯一机制（镜像支引力投影）已**硬否证**（5.31×/3.82×），§8.3 自写「**仅在该机制被重建后才成立**」；**不得计入可检验预言或出口计数**。⚠️ 历史出处（前否证时代表述，未回溯标注）：M5 报告「已有数据 0–3 年」四项之一、P2 报告「最强可检验预言」。 | 第 94 轮（`_voidcpt_94.py`） | 同 C-51 备忘录 |"""
ins_after_line(LIST, "| **I-22** | **tick 片层的 1PN 消隐", ROWS, "LIST-7 四条新行（C-51/52/53/N-39）")

# ---------------------------------------------------------------- 4. 交接说明
print("=== 4. 交接说明：§七 新建议 ＋ 第 94 轮新增块 ===")
sub_once(HH, "0. 🎯 **当前建议（第 93 轮后）**：",
         "0. 🎯 **（历史，第 93 轮后，已被上式取代）**：", "HH-1 降级旧建议")

HH_ITEM = """0. 🎯 **当前建议（第 94 轮后）**：**候选池「void-CPT-κ」已结项** —— 判定降级为「**悬空（机制未重建）**」
   （镜像支投影早于 2026-09-16/17 硬否证：5.31×/3.82×；§8.3 自写「仅重建后成立」），四处下游（§9 表／§8.4／第 90＋91 轮台账）已同步降级。
   ⭐ **净增量**：**C-51 / C-52 / C-53** ＋ **N-39** ＋ 摘要限定（**中英同步**）。
   📌 **剩余待办**：候选池 **#1 η 能标／#2 暗能量能标／#4 η/s**；**EMRI**（等 LISA）；**A1（Lean 资产恢复）**。⚠️ **#1/#2 是「配出来的数」（低优先）**。
"""
ins_before_line(HH, "0. 🎯 **（历史，第 93 轮后，已被上式取代）**", HH_ITEM, "HH-2 新建议")

HH_BLOCK94 = """**第 94 轮新增（候选池 void-CPT-κ 结项：机制已否证而判定未降级）**：脚本 `_voidcpt_94.py`（**VC-1…VC-10，22 项 0 失败**）。
① ✅ **判定降级（C-51）**：第 90/91 轮台账把 void-CPT-κ 标为「**真预言**」——而机制侧早已登记【已否证】（§8.3；5.31×/3.82×）⟹ 四处下游同步为「**悬空（机制未重建）**」；§9 表「真预言 11 → 10＋悬空 1」、正文级台账「2 → 1＋悬空 1」。
② ⚠️ **C-52**：摘要第 5 条（「ε_B 给出暗物质密度／叠加模型」）与 §8.2「空白」/§8.3「已否证」不相容 —— 加限定注。
③ ⚠️ **C-53**：候选池引用对账（#7/#8 两套互换；#6 异义；第 93 轮漏改一处 #5；台账 C6 过期 = C-19 族第 12 条）。
④ ⚠️ **N-39**：不得把（机制已撤的）void-CPT-κ 计为可维持的可检验预言。
⑤ ⭐ **方法论（技能陷阱 89）**：判定「真预言」需要**两根轴** —— **机制轴**（依据现役？）× **观测轴**（未观测？）；第 90/91 轮只看观测轴 ⟹ 把「已否证×未观测」错判为真预言（正确档 = **悬空**）。
⑥ 📌 **规范（第 94 轮起）**：**凡列「真预言」，机制轴与观测轴都必须过**；**引用候选池条目一律用名字**。
"""
ins_before_line(HH, "0. 🎯 **（历史，第 86 轮，已被上式取代）**：**审计轮三连", HH_BLOCK94, "HH-3 第 94 轮新增块")

print()
print("=" * 60)
print("PATCH 94 DONE  FAIL = {}".format(FAIL))
print("=" * 60)
