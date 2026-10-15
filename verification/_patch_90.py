# -*- coding: utf-8 -*-
"""第 90 轮 补丁：C-45（§9 表四类判定补标 ＋ 两处结构破损修复）"""
import io

ZH = "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
LIST = "工程期望清单.md"
FAIL = 0

def sub_once(path, old, new, tag):
    global FAIL
    t = io.open(path, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        print("  [FAIL] {}  命中 {} 次（应为 1）".format(tag, n)); FAIL += 1; return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    print("  [PASS] {}  已替换".format(tag))

def merge_row(path, head, tail_prefix, joiner, tag):
    """把从 head 开头的行、到以 tail_prefix 开头的那一行（含）合并为一行。"""
    global FAIL
    lines = io.open(path, encoding="utf-8").read().split("\n")
    a = [i for i, s in enumerate(lines) if s.startswith(head)]
    b = [i for i, s in enumerate(lines) if s.startswith(tail_prefix)]
    if len(a) != 1 or len(b) != 1 or b[0] <= a[0]:
        print("  [FAIL] {}  锚定位失败（head {} / tail {}）".format(tag, len(a), len(b))); FAIL += 1; return
    i, j = a[0], b[0]
    parts = [lines[i].rstrip()] + [lines[k].strip() for k in range(i + 1, j + 1)]
    merged = parts[0] + joiner.join(parts[1:])
    ncell = len([c for c in merged.strip().strip("|").split("|")])
    lines[i:j + 1] = [merged]
    io.open(path, "w", encoding="utf-8").write("\n".join(lines))
    print("  [PASS] {}  已并为一行（原 {} 行），列数 = {}".format(tag, j - i + 1, ncell))

# ==================================================================== 1. 裸竖线
print("=== 1. 修复裸竖线 |G|² → \\|G\\|² ===")
sub_once(ZH, "环面基态简并 |G|²、任意子分数统计", "环面基态简并 \\|G\\|²、任意子分数统计", "ZH-1a 裸竖线（ZH）")
sub_once(EN, "torus ground-state degeneracy |G|², anyonic", "torus ground-state degeneracy \\|G\\|², anyonic", "ZH-1b 裸竖线（EN）")

# ==================================================================== 2. 合并 S-C1 残行
print("=== 2. 合并 S-C1 残行 ===")
merge_row(ZH, "| **S-C1** |", "DESI DR2 / Euclid 2026-10", " ", "ZH-2a S-C1 合并（ZH）")
merge_row(EN, "| **S-C1** |", "**hard framework prediction; runs in parallel", " ", "ZH-2b S-C1 合并（EN）")

# ==================================================================== 3. 追加四类判定台账
print("=== 3. 追加 §9 四类判定台账 ===")
ZH_BLOCK = """> **【v2.9 补标（第 90 轮：§9 表的**四类判定** —— 第 37 轮定的判决口径，此前在全文覆盖率仅 13%）】** 脚本 `_fourclass_90.py`（**FC-1…FC-5，0 失败**）。逐行定案，**依据一律引已登记的轮次**：
> | 行 | 命题（简） | **四类判定** | 依据 |
> |---|---|---|---|
> | 1 | B1–B5 黑洞强场预言包 | **真预言** | 框架先给、EHT/LIGO/LISA 未做 |
> | 2 | void-CPT-κ 异常 | **真预言** | 分析方案已给出、结果未出 |
> | 3 | `w = −1+4ε/3`（`wa = 0`） | **半拟合** | `ε` 是能标参数；**第 73 轮**：`wa = 0` **不是框架独有**（ΛCDM 同值）⟹ 判别力 = 0 |
> | 4 | SU(3) β 阶梯跳跃 | **未定量** | 「数值待推导」—— 没有可算的数 |
> | 5 | 第四代费米子 | **失败** | 「与 LHC 未发现存在张力」 |
> | 6 | 霍金辐射非热修正 ~`1/S` | **真预言** | 有数、未观测（接近窗口边缘） |
> | 6′ | 火墙厚度 ~`√(l_P/R)` | **真预言** | 有标度律、未观测 |
> | 7 | PeV 中微子味比率异常 | **未定量** | 只写「定性预言」 |
> | 8 | 纠缠熵面积律系数 | **真预言** | 系数含 `ln2`、可算、未观测 |
> | 9 | 拓扑序激发（量子双 / 弦网） | **推导 / 数值** | 2+1D 格点模型的**严格结果**，不是对自然的预言 |
> | 10 | 禁闭弦张力 ＋ 相变点定位 | **推导 / 数值** | 同上（⚠️ 关键词「张力」有两个义项，见下） |
> | **S1** | `α = 1.00±0.06` | **postdiction** | EHT 阴影**已观测**（框架调 `α` 以兼容 ⟹ 附带**半拟合**） |
> | **S2** | QNM `f = f_GR/α` | **真预言** | ET/CE 未建 |
> | **S3** | 火墙弥散 `δ/R ~ 10⁻⁹` | **真预言** | 原初黑洞未观测 |
> | **S4** | 过载区无奇点 ＋ 声速消失 | **推导 / 数值** | 自标「✅ 流体模型 ＋ 微观推导」 |
> | **S5** | 阴影边缘普朗克弥散 | **真预言（不可测）** | ~10⁻¹⁹–10⁻²⁴ ⟹ **可检验性 = 0** |
> | **S-E1…S-E4** | EMRI 四项 | **真预言** | LISA 未发射（⚠️ **第 61 轮 C-7**：`σ` 口径须统一） |
> | **S-E5** | FQH 引力子模 | **失败** | ❌ **结项（第 54 轮）**：T-11 裁决 |
> | **S-E6** | 胶球 = 非阿贝尔通量自束缚态 | **postdiction** | BESIII X(2370) **已确认**，框架做「翻译」 |
> | **S-C1** | `wa = 0` ∧ `Ω_K = 0` | **解释性（判别力 0）** | **第 61 轮 N-22**：与平 ΛCDM **同值** ⟹ 观测不可区分 |
> · ⭐ **汇总（23 行）**：**真预言 11** ｜ **推导 / 数值 3** ｜ 未定量 2 ｜ 失败 2 ｜ postdiction 2 ｜ 半拟合 1 ｜ 真预言（不可测）1 ｜ **解释性（判别力 0）1**。
> · ⭐⭐ **关键读法（此前没有一处写出来）**：11 条「真预言」里 **EMRI 系（S-E1–S-E4）四项同源** —— 都来自 `δ = 0.30·x_p` **一个关系** ⟹ **按「独立出口」计 = 1 条**（与**第 61 轮**「观测出口 = 1 条」一致）。⟹ **表中 4 行 ≠ 出口 4 条。**
> · ⚠️ **两处结构破损（本轮修）**：① 第 9 行的 `|G|²` 是全文表格里**唯一的裸竖线** ⟹ 被拆成 **6 列**，已转义为 `\\|G\\|²`；② **S-C1 行跨三行**（2 / 2 / 3 列）⟹ 已并为**一行**。
> · ⚠️ **补标时踩到的假命中**：规则表把第 10 行的「**弦张力**」（string tension，一个物理量）当成「与观测**存在张力**」⟹ 误判为「失败」。**同形词不同义** —— 与第 88 轮「`0.04` ⊂ `0.0493`」同族，但机制不同（不是子串，是同词两义）。
> · 📌 **规范（第 90 轮）**：**§9 表此后每行必须带四类判定**；**报「出口」前先数「独立关系」而不是「行数」**。"""

EN_BLOCK = """> **【v2.9 labelling (round 90: the **four-way verdict** for the §9 table — the round-37 rule, whose coverage in the paper was only 13%)】** Script `_fourclass_90.py` (**FC-1 … FC-5, 0 failures**). Row-by-row verdicts; **every rationale cites an already-registered round**:
> | Row | Proposition (abridged) | **Four-way verdict** | Rationale |
> |---|---|---|---|
> | 1 | B1–B5 black-hole strong-field package | **true prediction** | framework first, EHT/LIGO/LISA not done |
> | 2 | void-CPT-κ anomaly | **true prediction** | analysis plan given, no result yet |
> | 3 | `w = −1+4ε/3` (`wa = 0`) | **half-fit** | `ε` is a scale parameter; **round 73**: `wa = 0` is **not framework-unique** (ΛCDM gives it too) ⟹ discriminating power = 0 |
> | 4 | SU(3) β-function step | **not quantified** | "value still to be derived" — no number |
> | 5 | fourth-generation fermions | **failed** | "in tension with the LHC null result" |
> | 6 | Hawking non-thermal correction ~`1/S` | **true prediction** | has a number, unobserved (near the window edge) |
> | 6′ | firewall thickness ~`√(l_P/R)` | **true prediction** | has a scaling law, unobserved |
> | 7 | PeV neutrino flavour ratio | **not quantified** | only "qualitative prediction" |
> | 8 | entanglement-entropy coefficient | **true prediction** | contains `ln2`, computable, unobserved |
> | 9 | topological-order excitations | **derivation / numerics** | a **rigorous 2+1D lattice result**, not a prediction about nature |
> | 10 | confined string tension + transition point | **derivation / numerics** | same (⚠️ "tension" has two senses here — see below) |
> | **S1** | `α = 1.00±0.06` | **postdiction** | the EHT shadow is **already observed** (α tuned to match ⟹ also **half-fit**) |
> | **S2** | QNM `f = f_GR/α` | **true prediction** | ET/CE not built |
> | **S3** | firewall spread `δ/R ~ 10⁻⁹` | **true prediction** | primordial black holes unobserved |
> | **S4** | no singularity + sound-speed vanishing | **derivation / numerics** | self-labelled "✅ fluid model + micro-derivation" |
> | **S5** | shadow-edge Planck spread | **true prediction (unmeasurable)** | ~10⁻¹⁹–10⁻²⁴ ⟹ **testability = 0** |
> | **S-E1…S-E4** | the four EMRI items | **true prediction** | LISA not launched (⚠️ **round 61, C-7**: the `σ` caliber must be unified) |
> | **S-E5** | FQH graviton mode | **failed** | ❌ **closed out (round 54)**: the T-11 ruling |
> | **S-E6** | glueball = non-Abelian flux bound state | **postdiction** | BESIII X(2370) **already confirmed**; the framework "translates" it |
> | **S-C1** | `wa = 0` ∧ `Ω_K = 0` | **interpretive (zero discriminating power)** | **round 61, N-22**: **same value** as flat ΛCDM ⟹ observationally indistinguishable |
> · ⭐ **Tally (23 rows)**: **true prediction 11** | derivation/numerics 3 | not quantified 2 | failed 2 | postdiction 2 | half-fit 1 | true prediction (unmeasurable) 1 | **interpretive (zero discriminating power) 1**.
> · ⭐⭐ **The key reading (never written down anywhere before)**: among the 11 "true predictions", the **four EMRI items (S-E1–S-E4) share one and the same relation** — all come from `δ = 0.30·x_p` ⟹ **counted as *independent* exits, that is 1** (consistent with **round 61**'s "observation exits = 1"). ⟹ **4 rows in the table ≠ 4 exits.**
> · ⚠️ **Two structural defects (fixed this round)**: ① the `|G|²` in row 9 is the **only unescaped pipe** in any table in the paper ⟹ it was split into **6 columns**; escaped to `\\|G\\|²`. ② the **S-C1 row spanned three lines** (2 / 2 / 3 cells) ⟹ merged into **one row**.
> · ⚠️ **A false positive hit while labelling**: the rule table read row 10's "**string tension**" (a physical quantity) as "tension **with observation**" ⟹ mislabelled it "failed". **Same word, two senses** — the same family as round 88's "`0.04` ⊂ `0.0493`", but a different mechanism (not a substring, a homonym).
> · 📌 **Norm (round 90)**: **every §9 row must now carry its four-way verdict**; **count *independent relations*, not *rows*, before quoting an "exit" count**. """

def append_before(path, anchor, block, tag):
    global FAIL
    t = io.open(path, encoding="utf-8").read()
    n = t.count(anchor)
    if n != 1:
        print("  [FAIL] {}  锚命中 {} 次".format(tag, n)); FAIL += 1; return
    io.open(path, "w", encoding="utf-8").write(t.replace(anchor, block + "\n\n" + anchor, 1))
    print("  [PASS] {}  已插入".format(tag))

append_before(ZH, "## 10 结论与开放问题", ZH_BLOCK, "ZH-3 四类判定台账（ZH）")
append_before(EN, "## 10 Conclusions and Open Problems", EN_BLOCK, "ZH-3 四类判定台账（EN）")

# ==================================================================== 4. 清单
print("=== 4. 清单 ===")
C45 = ("| **C-45** | **§9「可检验预言」表从未带四类判定；且有两处结构破损（第 90 轮）** | **更正 / 补标** | "
       "① ⚠️ **第 37 轮定的判决口径（真预言 / postdiction / 半拟合 / 失败）在论文里覆盖率仅 13%**"
       "（含「预言」的 60 行里只 8 行标了）⟹ 本轮对 **§9 全表 23 行逐行补标**（依据一律引已登记轮次）："
       "**真预言 11**｜推导/数值 3｜未定量 2｜失败 2｜postdiction 2｜半拟合 1｜真预言（不可测）1｜"
       "**解释性（判别力 0）1**。② ⭐⭐ **关键读法（此前没有一处写出来）**：11 条「真预言」里 "
       "**EMRI 系（S-E1–S-E4）四项同源**（都来自 `δ = 0.30·x_p` 一个关系）⟹ **独立出口 = 1 条**"
       "（与第 61 轮一致）——**表中 4 行 ≠ 出口 4 条**。③ 🐞 **两处结构破损**：第 9 行的 `\\|G\\|²` 是全文表格里"
       "**唯一的裸竖线**（被拆成 6 列）；**S-C1 行跨三行**（2/2/3 列）——均已修。④ ⚠️ 补标时踩到"
       "**同形词假命中**：「弦张力」被规则表当成「与观测存在张力」⟹ 误判为「失败」。"
       " | 第 90 轮（`_fourclass_90.py` FC-1…FC-5） | 技能陷阱 84 |")
lines = io.open(LIST, encoding="utf-8").read().split("\n")
idx = [i for i, s in enumerate(lines) if s.startswith("| **C-44** |")]
if len(idx) != 1:
    print("  [FAIL] LIST-1  C-44 锚行命中 {} 次".format(len(idx))); FAIL += 1
else:
    lines[idx[0] + 1:idx[0] + 1] = [C45]
    io.open(LIST, "w", encoding="utf-8").write("\n".join(lines))
    print("  [PASS] LIST-1  C-45 行已插入（行 {}）".format(idx[0] + 2))

sub_once(LIST, "| **撤回 / 更正** | **43 条**（**C-44 ⭐",
         "| **撤回 / 更正** | **44 条**（**C-45 ⭐ §9 表从未带四类判定 ＋ 两处结构破损**"
         "（第 90 轮：口径覆盖率仅 **13%**；补标 23 行 ⟹ **真预言 11 但独立出口 = 1**（EMRI 四项同源）；"
         "修 `\\|G\\|²` 裸竖线与 S-C1 残行）｜**C-44 ⭐", "LIST-2 总账 43 → 44")

print()
print("=" * 60)
print("PATCH 90 DONE  FAIL = {}".format(FAIL))
print("=" * 60)
