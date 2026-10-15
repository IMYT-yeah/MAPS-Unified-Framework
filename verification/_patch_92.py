# -*- coding: utf-8 -*-
"""第 92 轮 补丁：C-47（第 55 轮块主题错位 ⟹ 核心判否无归属）"""
import io
ZH, EN = "论文初稿_正反物质对风暴统一框架_v2.9.md", "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
LIST = "工程期望清单.md"
FAIL = 0
def ins_after_line(path, head_sub, block, tag):
    global FAIL
    lines = io.open(path, encoding="utf-8").read().split("\n")
    idx = [i for i, s in enumerate(lines) if head_sub in s]
    if len(idx) != 1:
        print("  [FAIL] {}  锚命中 {} 次".format(tag, len(idx))); FAIL += 1; return
    lines[idx[0] + 1:idx[0] + 1] = block.split("\n")
    io.open(path, "w", encoding="utf-8").write("\n".join(lines))
    print("  [PASS] {}  已插入（锚行 {}）".format(tag, idx[0] + 1))
def sub_once(path, old, new, tag):
    global FAIL
    t = io.open(path, encoding="utf-8").read()
    if t.count(old) != 1:
        print("  [FAIL] {}  命中 {} 次".format(tag, t.count(old))); FAIL += 1; return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    print("  [PASS] {}  已替换".format(tag))

# ---------------------------------------------------------------- 1. 第 55 轮块归属注
print("=== 1. 第 55 轮块：加归属注（ZH / EN）===")
ZH_NOTE = """> ⚠️ **【第 92 轮归属注（C-47）】** 本轮有**两个**产物，本块只承载了第一个：
> · ① **（本节正文）** 跨支通道的用途限于「**信息**」，不含「**能量**」；
> · ② ⭐ **（本轮的主产物；此前在论文里没有归属）** **战略审查：框架对化学储能零内容 —— 三条路径全部判否**
>   （直接路径「化学储能」/ 跨支能量通道 / 电化学转换），锚定量 `f ≡ Q/c²` 与化学储能的 `f ~ 10⁻¹⁰` 相差约 10 个数量级。
> ⚠️ **量化缺口的证据**：本块内「**储能**」「**电池**」「**化学**」「**判否**」「**不覆盖**」「**零内容**」**各 0 处**；
>   ②只在**下一轮块的首句**被顺带提到（见下方第 56 轮块：「第 55 轮把战略目标「电池能量密度」审为**框架不覆盖**」）。
> ⟹ ⚠️ **引用第 55 轮时必须同时引第 56 轮块首句与清单 `S-13`**；否则读者只读本块会以为该轮只做了一条边界。
> 📌 **规范**：**每轮块的主题必须等于该轮备忘录的主题**；若一轮产出多条，**主题应取自其中的主产物**。"""

ins_after_line(ZH, "【v2.9 补充（第 55 轮：跨支通道的用途限于", ZH_NOTE, "ZH-1 第 55 轮归属注")

EN_NOTE = """> ⚠️ **【Round-92 attribution note (C-47)】** This round produced **two** items; this block carries only the first:
> · ① **(the body text below)** the cross-branch channel carries **information**, not **energy**;
> · ② ⭐ **(the round's main product; previously it had no home in the paper)** **strategic review: the framework has zero content for chemical energy storage — all three routes ruled out** (the direct route "chemical storage" / the cross-branch energy channel / electrochemical conversion), with the anchor `f ≡ Q/c²` about 10 orders of magnitude away from chemical storage's `f ~ 10⁻¹⁰`.
> ⚠️ **Quantified evidence of the gap**: inside this block the words "**storage**", "**battery**", "**chemical**", "**ruled out**", "**not covered**" and "**zero content**" each occur **0 times**; item ② appears only as a passing remark in the **first sentence of the next round's block** ("round 55 reviewed the strategic goal 'battery energy density' as **not covered by the framework**").
> ⟹ ⚠️ **Any citation of round 55 must also cite the first sentence of the round-56 block and item `S-13` of the checklist**; otherwise a reader of this block alone would think the round only added one boundary.
> 📌 **Norm**: **a round block's topic must equal that round's memo topic**; when a round yields several items, **the topic should be taken from the main product**. """
ins_after_line(EN, "round 55: the cross-branch channel carries", EN_NOTE, "EN-1 round-55 attribution note")

# ---------------------------------------------------------------- 2. 清单
print("=== 2. 清单 ===")
C47 = ("| **C-47** | **第 55 轮块主题错位 ⟹ 该轮核心判否在论文里没有归属（第 92 轮）** | **更正 / 溯源** | "
       "第 55 轮块的**标题**是「跨支通道的用途限于「信息」，不含「能量」」，而该轮**备忘录的主题**是"
       "「战略审查：电池能量密度能否由框架支撑」⟹ 块的**主题取错了**（取成了三条分支里的一条）。"
       "⚠️ **量化**：该块内「储能」「电池」「化学」「判否」「不覆盖」「零内容」**各 0 处**；核心判否"
       "（**框架对化学储能零内容、三条路径全部判否**）只作为**下一轮块的首句背景**出现。"
       "⚠️ **中英对称**（EN 块内 `storage`/`battery`/`chemical`/`not covered` 亦各 0 处）。"
       "⟹ 已在块首加**归属注**（写明两个产物 ＋ 缺口的量化证据 ＋ 必须同时引第 56 轮块与 S-13）。"
       "⭐ 同轮**方法论产出**：**两个失败过的检测器**（① 数值近邻「同前缀异尾数」29 对全部假警报 —— "
       "`0.4330/0.4334/0.4335` 是 N=8/16/24 三个不同格点；② 标题字面重合度把第 88 轮判成 0%）"
       "⟹ ✅ **正解是内容判据**：看该轮核心判否词在块里出现几次；**换措辞认不出的都不算冲突**。"
       " | 第 92 轮（`_memoalign_92.py` MA-1…MA-7） | 技能陷阱 86 |")
lines = io.open(LIST, encoding="utf-8").read().split("\n")
idx = [i for i, s in enumerate(lines) if s.startswith("| **C-46** |")]
if len(idx) != 1:
    print("  [FAIL] LIST-1  C-46 锚行命中 {} 次".format(len(idx))); FAIL += 1
else:
    lines[idx[0] + 1:idx[0] + 1] = [C47.replace("'", '"')]
    io.open(LIST, "w", encoding="utf-8").write("\n".join(lines))
    print("  [PASS] LIST-1  C-47 行已插入（行 {}）".format(idx[0] + 2))
sub_once(LIST, "| **撤回 / 更正** | **45 条**（**C-46 ⭐",
         "| **撤回 / 更正** | **46 条**（**C-47 ⭐ 轮次块主题错位 ⟹ 核心判否无归属**"
         "（第 92 轮：第 55 轮块标题 = 跨支通道、备忘录主题 = 电池能量密度；块内「储能/电池/化学/判否/不覆盖/零内容」**各 0 处**，"
         "核心判否只在下一轮块首句出现；**中英对称** ⟹ 已在块首加归属注；⭐ 同轮方法论：**数值近邻与标题重合度两个检测器都失败**，"
         "正解 = **内容判据**）｜**C-46 ⭐", "LIST-2 总账 45 → 46")

print()
print("=" * 60)
print("PATCH 92 DONE  FAIL = {}".format(FAIL))
print("=" * 60)
