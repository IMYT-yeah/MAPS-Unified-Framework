# -*- coding: utf-8 -*-
"""
第 83 轮补丁：撤回第 82 轮的 (g′)，并把 §10.2 里的依据改为 (g)。

规范遵循：
  · 陷阱 73 —— 一律 sub_once 式显式检查（不用 `if old in t:`；未命中必须报）
  · 陷阱 74 —— 锚点**逐字取整行**
  · 陷阱 20/22 —— 保留删除线留痕 + 两列法
  · 中英同步
"""
import io
import os
import shutil
import sys

BASE = "C:/Users/Administrator/Desktop/2026-08-20-21-43-34"
OUT = os.path.join(BASE, "outputs")
HIST = os.path.join(BASE, "MAPS-Unified-Framework", "paper", "history")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

BAD = []


def sub_once(path, old, new, tag, count_expected=1):
    t = io.open(path, encoding="utf-8").read()
    n = t.count(old)
    if n != count_expected:
        print("  [XX] {:<34} 命中 {} 次（期望 {}）".format(tag, n, count_expected))
        BAD.append(tag)
        return False
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, count_expected))
    print("  [OK] {:<34} 已改（{} 处）".format(tag, count_expected))
    return True


def find_whole_line(path, prefix):
    """陷阱 74：锚点逐字取整行"""
    L = io.open(path, encoding="utf-8").read().split("\n")
    cand = [x for x in L if x.startswith(prefix)]
    assert len(cand) == 1, "前缀 {!r} 命中 {} 行".format(prefix, len(cand))
    return cand[0]


# 备份
for p in (ZH, EN):
    shutil.copy2(p, os.path.join(HIST, os.path.basename(p).replace(".md", "_备份_2026-10-02第83轮前.md")))
print("[备份] 已存第 83 轮前备份\n")

# ================================================================
print("[ZH-1] §8.6.8：撤回 (g′)，替换为【第 83 轮撤回】留痕块")
pref = "**(g′) ⭐ 4-正则二分图"
L = io.open(ZH, encoding="utf-8").read().split("\n")
i = next(k for k, s in enumerate(L) if s.startswith(pref))
j = next(k for k in range(i, len(L)) if L[k].startswith("（脚本 `_ricci_82.py`"))
old_block = "\n".join(L[i:j + 1])
print("      块范围 L{}–L{}（{} 行）".format(i + 1, j + 1, j - i + 1))

NEW_ZH = """**(g′) 【第 83 轮撤回】** ⚠️ 第 82 轮曾在此加一段「**4-正则**二分图（**金刚石**）非平面」，
**前提有误，予以撤回**：本小节 (b) 段已定「简单立方格，配位数 **6**」——
**6-正则 = 简单立方 = 衬底的现行几何** ⟹ **(g) 已经覆盖它**；
而「4-正则（配位数 4）」对应的是**第 27 轮初稿的「金刚石」**，
**第 30 轮 T-6 裁决已撤回**（见本小节开头的裁决块，以及 (i) 段「**金刚石结构与 §4.9 引理 1 不相容**」）。
⟹ **框架里并不存在一个 4-正则的衬底几何**，该档**没有对象** —— 不是「论文漏算」，是「**不该算**」。
不等式本身无误（4-正则二分图确实非平面：`m = 2n` vs 上界 `2n−4`，对一切 n 矛盾），但**框架用不上**。
⭐ 教训：**检索到一个词 ≠ 那个词是现行的**（本处「金刚石」在底本 5 处里 4 处带撤回标记）。**登记 C-33。**"""

sub_once(ZH, old_block, NEW_ZH, "ZH 撤回 (g′)")

print("\n[EN-1] §8.6.8: withdraw (g′)")
pref_en = "**(g′) ⭐ A 4-regular bipartite graph"
L = io.open(EN, encoding="utf-8").read().split("\n")
i = next(k for k, s in enumerate(L) if s.startswith(pref_en))
j = next(k for k in range(i, len(L)) if L[k].startswith("⟹ **The diamond substrate network is intrinsically non-planar**")
         or L[k].startswith("(script `_ricci_82.py`, RC-5)"))
old_block_en = "\n".join(L[i:j + 1])
print("      块范围 L{}–L{}（{} 行）".format(i + 1, j + 1, j - i + 1))

NEW_EN = """**(g′) 【withdrawn in round 83】** ⚠️ In round 82 a paragraph was added here claiming that a **4-regular** bipartite graph (the **diamond** lattice) is non-planar. **Its premise was wrong and it is withdrawn**: item (b) of this subsection already fixes the **simple-cubic lattice with coordination number 6**, and **6-regular = simple cubic = the substrate's current geometry** ⟹ **(g) already covers it**. The "4-regular (coordination 4)" case belongs to the **round-27 earlier draft's "diamond"**, which the **round-30 T-6 verdict has already withdrawn** (see the verdict block at the head of this subsection, and item (i): "**the diamond structure is incompatible with §4.9 Lemma 1**"). ⟹ **No 4-regular substrate geometry exists in the framework**; that case **has no object** — it is not "a missing computation" but "a computation that should not be made". The inequality itself is correct (a 4-regular bipartite graph is indeed non-planar: `m = 2n` versus the bound `2n−4`, a contradiction for every n), but **the framework cannot use it**. ⭐ Lesson: **retrieving a word ≠ that word being current** (here 4 of the 5 occurrences of "diamond" in the base document carry withdrawal markers). **Registered as C-33.**"""

sub_once(EN, old_block_en, NEW_EN, "EN withdraw (g′)")

# ================================================================
print("\n[ZH-2] §10.2：把「衬底非平面」的依据由 (g′) 改为 (g)")
ZH_REF_OLD = "且**衬底网络内蕴非平面**（见 §8.6.8 (g′)，4-正则二分图必非平面）"
ZH_REF_NEW = "且**衬底网络内蕴非平面**（见 §8.6.8 **(g)**：**6-正则 = 简单立方**二分图必非平面 —— ⚠️ 第 82 轮曾引 (g′)「4-正则/金刚石」，**已由第 83 轮撤回**，理由见 §8.6.8 (g′) 条）"
sub_once(ZH, ZH_REF_OLD, ZH_REF_NEW, "ZH §10.2 依据改 (g)")

print("\n[EN-2] §10.2 EN: change the ground from (g′) to (g)")
L = io.open(EN, encoding="utf-8").read().split("\n")
k1864 = next(k for k in range(len(L)) if "substrate network is intrinsically non-planar" in L[k])
print("      EN L{}: {}".format(k1864 + 1, L[k1864].strip()[:230]))
EN_REF_OLD = "the **substrate network is intrinsically non-planar** (see §8.6.8 (g′), a 4-regular bipartite graph is necessarily non-planar)"
EN_REF_NEW = "the **substrate network is intrinsically non-planar** (see §8.6.8 **(g)**: a **6-regular = simple-cubic** bipartite graph is necessarily non-planar — ⚠️ round 82 cited (g′) \"4-regular/diamond\", **withdrawn in round 83**, see the (g′) item of §8.6.8)"
sub_once(EN, EN_REF_OLD, EN_REF_NEW, "EN §10.2 依据改 (g)", count_expected=1)

print("\n" + "=" * 70)
print("补丁完成。失败项：{}".format(BAD if BAD else "无 ✓"))
print("=" * 70)
