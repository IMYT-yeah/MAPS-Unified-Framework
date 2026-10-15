# -*- coding: utf-8 -*-
"""第 88 轮 补丁：C-43（§10.1「完成度 ~90%」补口径注）＋ 清单台账
规则：① 锚点取整行；② 未命中即报错；③ 插入块内**不得有空行**（陷阱 74 子坑）；④ 中文引号用「」『』。
"""
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

def ins_after_line(path, line_head, block, tag):
    global FAIL
    lines = io.open(path, encoding="utf-8").read().split("\n")
    idx = [i for i, s in enumerate(lines) if s.startswith(line_head)]
    if len(idx) != 1:
        print("  [FAIL] {}  锚行命中 {} 次".format(tag, len(idx))); FAIL += 1; return
    i = idx[0]
    body = block.split("\n")
    nonq = [b for b in body if b.strip() and not b.startswith(">")]
    if nonq:
        print("  [FAIL] {}  插入块含非引用行 {}".format(tag, nonq[:2])); FAIL += 1; return
    lines[i + 1:i + 1] = [""] + body
    io.open(path, "w", encoding="utf-8").write("\n".join(lines))
    print("  [PASS] {}  已插入（锚行 {}，块 {} 行，内部无空行 ✓）".format(tag, i + 1, len(body)))

# ==================================================================== ZH
print("=== 论文 ZH ===")
ZH_ANCHOR = "本框架从四条公理出发，为四种基本力的统一提供了**涌现式统计力学论证**，完成度 ~90%："
ZH_BLOCK = """> **【v2.9 口径注（第 88 轮 **C-43**：这个「~90%」的度量是什么？）】** ⚠️ 本句是**全文唯一的定量自评**，也是**全文唯一没有度量的数** —— 同行与后 3 行内**没有任何**「分母 / 分子 / 按条数 / 口径」之类的说明 ⟹ **读者无法复核**。与它并列的三处表述**量纲不同**：
> · **同章 §10.2** 列 **13 条**开放问题，其中 **5 条明示未闭合**（#2「4D SU(3) 完全涌现**仍开放**」、#13「阶段 C **遗留** ＋ 4D YM 质量隙 **不声称**」、#11「强度**未推导**」、#7「剩余严格化（**深度开放**）」等）；
> · **上一章 §9** 的表共 **25 行**，其中 **5 行**是「**❌ 结项 / 与 LHC 存在张力 / 数值待推导 / 判别中（3.3σ 压力）**」；
> · **§1** 的自定位是「**启发式统一框架（参考架构，非已确立物理）**」，与本节**相距 1895 行**，且 §1 处**只指向 §10.2（开放问题）、不指向本节**。
> ⟹ ⚠️ **读法**：本句应读作**作者的主观进度判断**，**不是可复核的指标**；引用时必须与 §10.2 的开放问题表**并列**读取（第 63 轮的三项硬指标 —— 「独有 ＋ 可测 ＋ 有数」的预言 = **1**、**★★★ = 0**、**「参数表」0 处** —— 在论文全文里「**就绪度**」**0 处**，从未进入正文）。
> ⚠️ **本轮不删此数**（它属作者的判断），只**补口径**：这是与 **C-20**（面积口径）/ **C-28**（拟合口径）/ **C-41**（外推口径）**同一族的「口径缺失」**，只是发生在**定性自评**上。"""

ins_after_line(ZH, ZH_ANCHOR, ZH_BLOCK, "ZH-1 §10.1 口径注")

# ==================================================================== EN
print("=== 论文 EN ===")
EN_ANCHOR = ("Starting from the four axioms, this framework provides an **emergent "
             "statistical-mechanical argument** for the unification of the four fundamental "
             "forces, with completeness ~90%:")
EN_BLOCK = """> **【v2.9 caliber note (round 88, **C-43**: what is the metric behind this "~90%"?）】** ⚠️ This sentence is the **only quantitative self-assessment in the whole paper**, and also the **only number in the paper with no metric** — neither this line nor the following three lines contains any word such as "denominator / numerator / count of items / caliber" ⟹ **the reader cannot check it**. The three statements standing next to it have **incommensurable natures**:
> · **§10.2, in the same chapter**, lists **13** open problems, **5** of which explicitly state they are unclosed (#2 "full emergence of 4D SU(3) **remains open**", #13 "stage C **outstanding** + 4D YM mass gap **not claimed**", #11 "strength **not derived**", #7 "remaining rigour (**deeply open**)");
> · **§9, in the previous chapter**, has a table of **25 rows**, **5** of which read "**❌ closed out / tension with LHC / value still to be derived / under discrimination (3.3σ tension)**";
> · **§1**'s self-positioning is "**heuristic unified framework (reference architecture, not established physics)**", **1895 lines away**, and §1 **points only to §10.2 (open problems), never to this section**.
> ⟹ ⚠️ **How to read it**: this sentence is the **author's subjective progress judgement**, **not a checkable metric**; it must be read **together with** §10.2's open-problem table (round 63's three hard indicators — predictions that are "framework-unique + measurable + already numeric" = **1**, **★★★ = 0**, **"parameter table" 0 occurrences** — never entered the body text: "**readiness**" appears **0 times** in the paper).
> ⚠️ **The number is not deleted this round** (it is the author's judgement); only the **caliber** is supplied: this is the **same family of caliber gaps as C-20 (area) / C-28 (fit) / C-41 (extrapolation)**, occurring here in a **qualitative self-assessment**."""

ins_after_line(EN, EN_ANCHOR, EN_BLOCK, "EN-1 §10.1 caliber note")

# ==================================================================== 清单
print("=== 清单 ===")
C43 = ("| **C-43** | **「完成度 ~90%」无度量、且与同章的三张表不相容（第 88 轮）** | **更正 / 口径补齐** | "
       "§10.1 的「完成度 ~90%」是**全文唯一的定量自评**，也是**全文唯一没有度量的数**（同行与后 3 行无任何口径词）。"
       "与它并列：**同章 §10.2** 有 **13 条**开放问题（**5 条明示未闭合**）；**上一章 §9** 表 **25 行**中 **5 行**为"
       "「❌ 结项 / 与 LHC 张力 / 数值待推导 / 判别中」；**§1** 自定位「非已确立物理」与本节**相距 1895 行**且"
       "**只指向 §10.2 不指向 §10.1**；第 63 轮三项硬指标（独有＋可测＋有数 = **1**、**★★★ = 0**、**参数表 0 处**）"
       "在论文里「就绪度」**0 处**。⟹ **不删此数，只补口径**（与 C-20 / C-28 / C-41 **同族的口径缺失**，发生在**定性自评**上）。"
       "⭐ 同轮**正面产出**：**11 个已知被更正的数值全部带标记**（未同步残留 = **0**）。 | 第 88 轮（`_readiness_88.py` CR-1…CR-9） | 技能陷阱 82 |")
lines = io.open(LIST, encoding="utf-8").read().split("\n")
idx = [i for i, s in enumerate(lines) if s.startswith("| **C-42** |")]
if len(idx) != 1:
    print("  [FAIL] LIST-1  C-42 锚行命中 {} 次".format(len(idx))); FAIL += 1
else:
    lines[idx[0] + 1:idx[0] + 1] = [C43]
    io.open(LIST, "w", encoding="utf-8").write("\n".join(lines))
    print("  [PASS] LIST-1  C-43 行已插入（行 {}）".format(idx[0] + 2))

sub_once(LIST,
         "| **撤回 / 更正** | **41 条**（**C-42 ⭐",
         "| **撤回 / 更正** | **42 条**（**C-43 ⭐ 定性自评的口径缺失 ＋ 成熟度表述四处不一致**"
         "（第 88 轮：§10.1「完成度 ~90%」**无度量定义**，且与同章 §10.2 的 **13 条**开放问题（5 条未闭合）、"
         "上章 §9 表的 **5 行**「❌/张力/待推导/判别中」、§1 的「非已确立物理」（相距 1895 行、只指向 §10.2）**三处不相容**；"
         "第 63 轮三项硬指标在论文里「就绪度」**0 处** ⟹ **不删数、只补口径**，与 C-20/C-28/C-41 **同族**）"
         "｜**C-42 ⭐",
         "LIST-2 总账 41 → 42")

print()
print("=" * 60)
print("PATCH 88 DONE  FAIL = {}".format(FAIL))
print("=" * 60)
