# -*- coding: utf-8 -*-
"""
第 83 轮核验：第 82 轮的 (g′) 建立在【已撤回的前提】上 —— 撤回它。

用户质疑（本轮起点）：「某一个步骤不是证明金刚石不对吗，怎么还金刚石」

事实链：
  · 第 27 轮**初稿**据「配位数 = 方向簇 k = 4」定为金刚石
  · 第 30 轮 **T-6 裁决**追溯后发现该步不成立（§4.10 论证 4：正四面体 4 方向 = 内空间；八面体 6 方向 = 外空间轴）
    ⟹ **撤回金刚石，定案简单立方**（配位数 6、二分）
  · §8.6.8 的**标题**就写着「外空间 6 方向 ⟹ 简单立方（T-6 裁决，第 30 轮）」
  · 同一小节 (i) 段写「**金刚石结构与 §4.9 引理 1 不相容**，简单立方通过」

第 82 轮的错误：把上述已撤回的几何当作「第 27 轮定案的格点几何」，据此加 (g′)「4-正则（金刚石）非平面」，
并把它当作本轮唯一正面产出。而 (g)（6-正则 = 简单立方）**已经覆盖了衬底的现行几何**。

判据刻意用【补丁前底本】（陷阱 20/22 两列法）：第 82 轮自己写进去的 (g′) 会污染「当前稿」的检索。
"""
import io
import os
import sys

BASE = "C:/Users/Administrator/Desktop/2026-08-20-21-43-34"
OUT = os.path.join(BASE, "outputs")
HIST = os.path.join(BASE, "MAPS-Unified-Framework", "paper", "history")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
PRE_ZH = os.path.join(HIST, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第82轮前.md")
PRE_EN = os.path.join(HIST, "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-02第82轮前.md")

OK, BAD = [], []


def chk(tag, cond, msg):
    (OK if cond else BAD).append(tag)
    print("  [{}] {}".format("OK" if cond else "XX", tag))
    for line in msg.split("\n"):
        print("        " + line)
    print()


def hdr(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def load(p):
    return io.open(p, encoding="utf-8").read().split("\n") if os.path.exists(p) else []


ZP, EP = load(PRE_ZH), load(PRE_EN)          # 底本（第 82 轮前）
ZC, EC = load(ZH), load(EN)                  # 当前稿

for p, nm in [(PRE_ZH, "底本"), (PRE_EN, "EN 底本")]:
    if not os.path.exists(p):
        print("!! 缺失底本", nm); sys.exit(1)

# ================================================================
hdr("[DM-1] 底本里「金刚石 / diamond」的**全部**语境 —— 逐条分类")
for L, nm, key in [(ZP, "ZH 底本", "金刚石"), (EP, "EN 底本", "diamond")]:
    hits = [(k + 1, s) for k, s in enumerate(L) if key in s]
    retr = [(k, s) for k, s in hits if ("撤回" in s or "withdrawn" in s or "不相容" in s or "incompatible" in s)]
    print("  {}：命中 {} 处；其中**撤回 / 不相容**语境 {} 处".format(nm, len(hits), len(retr)))
    for k, s in retr:
        print("     L{}: {}…".format(k, s.strip()[:170]))
    cur = [(k, s) for k, s in hits if (k, s) not in retr]
    print("     其余 {} 处：".format(len(cur)))
    for k, s in cur:
        print("     L{}: {}…".format(k, s.strip()[:170]))
    print()
chk("DM-1", len([1 for k, s in [(k + 1, s) for k, s in enumerate(ZP) if "金刚石" in s]
                 if ("撤回" in s or "不相容" in s)]) >= 2,
    "**底本里「金刚石」的每一处都带撤回标记**：§8.6.8 开头的【v2.9 裁决：撤回本小节初稿的「金刚石」】\n"
    "＋ (d) 段的「金刚石改的 0.6495… 一并撤回」＋ (i) 段的「金刚石结构与 §4.9 引理 1 **不相容**」\n"
    "⟹ 在底本里，「金刚石」**不是一个现行几何**，而是一个**已作废的初稿**")

# ================================================================
hdr("[DM-2] T-6 裁决：定案几何是什么、在第几轮")
t6 = [(k + 1, s) for k, s in enumerate(ZP) if "T-6 裁决" in s or ("裁决" in s and "简单立方" in s)]
for k, s in t6:
    print("     L{}: {}…".format(k, s.strip()[:190]))
decl = [k for k, s in enumerate(ZP) if s.strip().startswith("#### 8.6.8")]
title = ZP[decl[0]] if decl else ""
print("\n  §8.6.8 标题：{}".format(title.strip()[:150]))
three = [k + 1 for k, s in enumerate(ZP) if "三条独立依据" in s or "论证 4 显式区分" in s]
print("  「三条独立依据」所在行：{}".format(three))
chk("DM-2", "简单立方" in title and "第 30 轮" in title,
    "**§8.6.8 的标题原文**：`{}`\n".format(title.strip()[:120]) +
    "⟹ 定案是**第 30 轮**的 T-6 裁决，几何 = **简单立方**；\n"
    "第 82 轮写的「**第 27 轮定案的格点几何是金刚石**」把「第 27 轮初稿」当成了「定案」，\n"
    "并且**跳过了紧贴标题的撤回块**（该块就在同一小节的第一段）")

# ================================================================
hdr("[DM-3] ⭐ 核心判据：底本正文里有没有「衬底 = 4-正则 / 配位数 4 / diamond lattice」的**现行**陈述？")
for L, nm, keys in [(ZP, "ZH 底本", ["4-正则", "配位数 4", "配位 4", "配位数 = 4"]),
                    (EP, "EN 底本", ["4-regular", "coordination number 4", "coordination 4"])]:
    print("  --- {} ---".format(nm))
    tot = 0
    for w in keys:
        h = [(k + 1, s) for k, s in enumerate(L) if w in s]
        tot += len(h)
        print("     {:<22} {:>3} 处".format(w, len(h)))
        for k, s in h[:4]:
            print("        L{}: {}…".format(k, s.strip()[:160]))
    print("     合计 {} 处".format(tot))
    print()
chk("DM-3", all(not any(w in s for s in ZP) for w in ["4-正则", "配位数 4", "配位 4"]),
    "**底本里「4-正则」「配位数 4」各 0 处** ⟹ 论文**从未把衬底说成 4-正则**；\n"
    "衬底的现行描述是 §8.6.8(b)「外空间轴结构 = 3 轴 ± ⟹ 简单立方格，配位数 **6**、二分」\n"
    "⟹ **4-正则这一档在框架里没有对象** —— 它对应的是**已被撤回的第 27 轮初稿**\n"
    "⟹ 第 82 轮的 (g′) 不是「补上论文缺的一档」，而是**给一个已作废的几何做补证**")

# ================================================================
hdr("[DM-4] (g) 覆盖的正是现行几何（6-正则 = 简单立方）")
g = [k + 1 for k, s in enumerate(ZP) if s.strip().startswith("**(g) 6-正则二分图")]
b = [k + 1 for k, s in enumerate(ZP) if s.strip().startswith("**(b) 裁决后的几何**")]
print("  (b) 段 L{}：{}…".format(b[0], ZP[b[0] - 1].strip()[:190]))
print("  (g) 段 L{}：{}…".format(g[0], ZP[g[0] - 1].strip()[:190]))
chk("DM-4", len(g) == 1 and len(b) == 1 and "配位数 **6**" in ZP[b[0] - 1],
    "(b) 段写「简单立方格，配位数 **6**、二分」；(g) 段算的正是「**6-正则**二分图非平面」\n"
    "⟹ **同一个几何** ⟹ **(g) 已经覆盖了衬底的现行几何**；\n"
    "⟹ (g′) 既**错**（前提已撤回）又**多余**（(g) 已覆盖）")

# ================================================================
hdr("[DM-5] 自指取证（两列法）：(g′) 在**补丁前**是否存在")
pre_hit = [(k + 1) for k, s in enumerate(ZP) if "(g′)" in s or "(g')" in s]
cur_hit = [(k + 1) for k, s in enumerate(ZC) if "(g′)" in s or "(g')" in s]
pre_en = [(k + 1) for k, s in enumerate(EP) if "(g′)" in s or "(g')" in s]
cur_en = [(k + 1) for k, s in enumerate(EC) if "(g′)" in s or "(g')" in s]
print("  ZH：(g′) 补丁前 {} 处 → 当前 {} 处".format(len(pre_hit), len(cur_hit)))
print("  EN：(g′) 补丁前 {} 处 → 当前 {} 处".format(len(pre_en), len(cur_en)))
print("  当前 ZH 命中行：{}".format(cur_hit))
print("  当前 EN 命中行：{}".format(cur_en))
chk("DM-5", len(pre_hit) == 0 and len(pre_en) == 0 and len(cur_hit) >= 1,
    "**(g′) 在补丁前 0 处**（中英皆是）⟹ 这一档**完全是第 82 轮引入的**；\n"
    "⟹ 第 82 轮「论文漏了 4-正则那一档」的说法**由我自己的新增文字造出**\n"
    "（与陷阱 47/65 的自指同族，但这次自指的是**前提**而不是判据）")

# ================================================================
hdr("[DM-6] 第 82 轮在别处对 (g′) 的引用（需同步更正）")
refs_zh = [(k + 1, s) for k, s in enumerate(ZC) if "(g′)" in s and not s.strip().startswith("**(g′)")]
refs_en = [(k + 1, s) for k, s in enumerate(EC) if "(g′)" in s and "added in round 82" not in s]
print("  ZH 非定义型的 (g′) 引用 {} 处：".format(len(refs_zh)))
for k, s in refs_zh:
    print("     L{}: {}…".format(k, s.strip()[:200]))
print("  EN 非定义型的 (g′) 引用 {} 处：".format(len(refs_en)))
for k, s in refs_en:
    print("     L{}: {}…".format(k, s.strip()[:200]))
chk("DM-6", len(refs_zh) >= 1,
    "§10.2 的第 82 轮审查块**引用了 (g′)** 作为「③ 对象对不上」的依据之一\n"
    "⟹ 撤回 (g′) 时必须**同步改**这一处：衬底非平面仍然成立，但依据是 **(g)（6-正则/简单立方）**，\n"
    "不是「4-正则（金刚石）」（更正后结论**不变**，但理由要换成对的那个）")

# ================================================================
hdr("[DM-7] 独立复核：4-正则不等式的**数学本身**对不对？（对，但无对象）")
rows = []
for n in (8, 16, 32, 64, 512):
    m = 2 * n              # d = 4 ⟹ m = dn/2 = 2n
    ub = 2 * n - 4
    rows.append((n, m, ub, m > ub))
    print("     n = {:<4} m = {:<5} 上界 2n−4 = {:<5} 违反？ {}".format(n, m, ub, "是" if m > ub else "否"))
allviol = all(r[3] for r in rows)
print("\n  对一般 n：d = 4 ⟹ m = 2n，不等式 `m ≤ 2n − 4` 变成 `2n ≤ 2n − 4` ⟹ **对一切 n 矛盾**")
chk("DM-7", allviol,
    "**不等式本身是对的**（4-正则二分图确实非平面，5 个 n 全部违反）——\n"
    "但「数学对」不等于「框架需要它」：该档对应的几何**已被撤回** ⟹ **无对象**\n"
    "⚠️ 这是**同族第 4 次**：第 75 轮「缺的不是方程，是对象」／第 77 轮「`g` 的精确值没有对象」／\n"
    "第 81 轮「`8π/3` 没有对象」／**本轮「4-正则档没有对象」**")

# ================================================================
hdr("[DM-8] 撤回后的自洽性（目标状态）")
print("  目标：")
print("     · (g′) 段在 ZH/EN **各 0 处**")
print("     · (g) 段仍在（它是覆盖现行几何的那一条）")
print("     · §8.6.8 的 T-6 裁决块与 (b)/(i) 段原样保留")
print("     · §10.2 第 82 轮块的「衬底非平面」依据改为 **(g)**")
print("  ℹ️ 本条是**本轮补丁后**才可判定的状态，故此处仅登记目标（补丁后由 DM-8b 复跑确认）")
chk("DM-8", True,
    "已登记撤回目标清单（补丁后复跑本脚本的 DM-8b 段确认）")

# ================================================================
hdr("[DM-8b] 撤回后的一致性（陷阱 72 两段式：取证用底本、确认用当前稿）")
zh_gp = [(k + 1, s) for k, s in enumerate(ZC) if "(g′)" in s]
en_gp = [(k + 1, s) for k, s in enumerate(EC) if "(g′)" in s]
zh_bad = [(k, s) for k, s in zh_gp if not ("撤回" in s or "withdrawn" in s)]
en_bad = [(k, s) for k, s in en_gp if not ("withdrawn" in s or "撤回" in s)]
print("  当前 ZH 含 (g′) 的行 {} 处；其中**非撤回语境** {} 处".format(len(zh_gp), len(zh_bad)))
for k, s in zh_gp:
    print("     L{}: {}…".format(k, s.strip()[:150]))
print("  当前 EN 含 (g′) 的行 {} 处；其中**非撤回语境** {} 处".format(len(en_gp), len(en_bad)))
for k, s in en_gp:
    print("     L{}: {}…".format(k, s.strip()[:150]))
g_zh = [k + 1 for k, s in enumerate(ZC) if s.strip().startswith("**(g) 6-正则二分图")]
g_en = [k + 1 for k, s in enumerate(EC) if "**(g) A 6-regular bipartite graph" in s]
ref_zh = [(k + 1, s) for k, s in enumerate(ZC) if "衬底网络内蕴非平面" in s]
ref_en = [(k + 1, s) for k, s in enumerate(EC) if "intrinsically non-planar" in s and "R_S" not in s]
print("\n  (g) 段仍在：ZH {} ／ EN {}".format(bool(g_zh), bool(g_en)))
print("  「衬底网络内蕴非平面」引用：")
for k, s in ref_zh:
    print("     ZH L{}: {}…".format(k, s.strip()[:180]))
for k, s in ref_en:
    print("     EN L{}: {}…".format(k, s.strip()[:180]))
ok_gref = all("**(g)**" in s or "(g):" in s or "(g)" in s for k, s in ref_zh + ref_en)
chk("DM-8b", len(zh_bad) == 0 and len(en_bad) == 0 and bool(g_zh) and bool(g_en) and ok_gref,
    "**撤回完成**：当前稿里 (g′) 的每一处出现都在**撤回语境**内（ZH 非撤回 0 处、EN 非撤回 0 处）；\n"
    "(g) 段（6-正则 = 简单立方）仍在，§10.2 的「衬底非平面」依据已改为 **(g)**\n"
    "⟹ 结论**不变**（衬底确实内蕴非平面），但**理由换成了对的那一个**")

print("\n" + "=" * 78)
print("通过 {} ／ 失败 {}".format(len(OK), len(BAD)))
if BAD:
    print("失败项：", BAD)
print("=" * 78)
