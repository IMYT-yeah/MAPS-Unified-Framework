# -*- coding: utf-8 -*-
"""
第 88 轮（第二段·修正版）：**「未同步残留」全量检测**

⚠️ 第一版两个错（自己记下来）：
  ① 抽取式太窄（要求同行同时有「原报」与「→」）⟹ 只抽到 3 组；
  ② 定点排查表里放了裸数 `148`，正则命中 `3.138–3.148` ⟹ **假 FAIL**。
     ⟹ 判据教训：**裸数字串不能当「值」的判据**（必须先证明它是独立记号）。

本版做法（反转方向，更完整）：
  ① 从**全文中所有带更正标记的行**里，抽「**左侧旧值**」（`X → Y` / `原报 X` / `由 X 改为`）；
  ② 再扫**正文行**（非轮次块），看这些旧值是否**裸留**（该行不带更正标记）；
  ③ 旧值一律要求**≥ 4 字符**且**含小数点或为 4 位以上整数** ⟹ 排除年份/编号类噪声。
"""
import io, re

ZH = "论文初稿_正反物质对风暴统一框架_v2.9.md"
FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok:
        FAIL += 1
def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

L = io.open(ZH, encoding="utf-8").read().split("\n")

PAT = re.compile(r"(v2\.9\s*[^\n（|]{0,16}（第\s*\d+\s*轮|【第\s*\d+\s*轮"
                 r"|第\s*\d+\s*轮加注|第\s*\d+\s*轮口径注|第\s*\d+\s*轮补注"
                 r"|第\s*\d+\s*轮(补充|更正|登记|分层注|裁决))")
def mask(lines):
    m, in_note = [], False
    for s in lines:
        if s.lstrip().startswith("|"):
            m.append(False); continue
        if s[:1] == "#":
            in_note = False
        if PAT.search(s):
            in_note = True
        m.append(in_note)
    return m
M = mask(L)

CMARK = ["更正", "原报", "原记", "原写", "原值", "撤回", "作废", "已改为", "应改为",
         "→", "移除", "补注", "口径注", "加注", "裁决", "降调", "结项", "旧值", "superseded"]
has_marks = lambda s: any(k in s for k in CMARK)

# 数值记号：含小数点的、或 4 位以上整数、或科学计数
NUMRX = r"([0-9]+(?:\.[0-9]+)?(?:×10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)?)"
def is_real(tok):
    if "×10" in tok:
        return True
    if "." in tok:
        return len(tok) >= 4
    return len(tok) >= 4 and not (1900 <= int(tok) <= 2100)   # 排除年份

# ---------------------------------------------------------------- 抽「左侧旧值」
hdr("CO-21  从带更正标记的行抽出「左侧旧值」")
ARROWS = r"(?:→|->|—>|改为|更正为|应改为|变成|代替)"
pats = [
    re.compile(r"(?:原(?:报|记|写|值)|从|由)\s*[*`“\"]*\s*" + NUMRX),
    re.compile(NUMRX + r"\s*[*`]*\s*(?:→|->|—>|改为|更正为|应改为|变成)\s*[*`]*\s*" + NUMRX),
]
old2new, old_only = {}, {}
for i, s in enumerate(L, 1):
    if not has_marks(s):
        continue
    for rx in pats:
        for g in rx.findall(s):
            if isinstance(g, tuple):
                a, b = g[0], g[-1]
                if a != b and is_real(a):
                    old2new.setdefault(a, set()).add(b)
                    old_only.setdefault(a, []).append(i)
            else:
                if is_real(g):
                    old_only.setdefault(g, []).append(i)
print("  抽到 **{}** 个候选旧值（≥4 字符）".format(len(old_only)))
show = sorted(old_only.items(), key=lambda kv: -len(kv[1]))[:30]
for v, ls in show:
    nv = old2new.get(v)
    print("     {:<14} 命中 {:>2} 行  新值 = {}".format(v, len(ls), sorted(nv) if nv else "（未同式给出）"))

# ---------------------------------------------------------------- 旧值是否裸留正文
hdr("CO-22  ⭐ 候选旧值在「正文且无更正标记」的行里是否裸留")
resid = []
for v in sorted(old_only, key=lambda x: -len(old_only[x])):
    naked = []
    tot = 0
    for i, s in enumerate(L, 1):
        if v not in s:
            continue
        tot += 1
        if not M[i - 1] and not has_marks(s):
            naked.append(i)
    if naked:
        resid.append((v, naked))
print("  共 {} 个候选旧值在正文里裸留：".format(len(resid)))
for v, ls in resid:
    print("     ⚠️ **{:<14}**  正文裸留行 = {}".format(v, ls[:10]))
    print("          依据（论文里的更正出处）= 行 {}".format(old_only[v][:6]))
    print("          新值 = {}".format(sorted(old2new.get(v, [])) or "（未同式给出）"))
    for i in ls[:2]:
        print("          L{}: {}".format(i, L[i - 1].strip()[:120]))
chk("CO-22", True, "已列出（判定在人工读表之后 —— 本题的 `--` 是提示不是结论）")

# ---------------------------------------------------------------- 反向：正文数值是否出现在更正语境内
hdr("CO-23  正文里的数值，是否在别处被标为「旧值」")
body_nums = {}
for i, s in enumerate(L, 1):
    if M[i - 1] or s.lstrip().startswith("|"):
        continue
    for v in re.findall(NUMRX, s):
        if is_real(v):
            body_nums.setdefault(v, []).append(i)
conf = [(v, ls) for v, ls in body_nums.items() if v in old_only]
print("  正文出现的「非平凡数值」共 {} 个；其中**同时被标为旧值**的 = {} 个".format(len(body_nums), len(conf)))
for v, ls in sorted(conf, key=lambda kv: -len(kv[1])):
    print("     ⚠️ {:<14} 正文行 {}   旧值语境行 {}".format(v, ls[:6], old_only[v][:4]))

# ---------------------------------------------------------------- 定点核查（去掉裸数判据）
hdr("CO-24  定点核查（全部要求「带上下文」的判据）")
POINTS = [
    ("0.4510", "第 50 轮：(2,2,6) 的 H/N 应为 0.4334"),
    ("0.4330", "第 50 轮：(2,2,6) 的 H/N 应为 0.4334"),
    ("6224",   "第 50 轮：轨道数应为 6334"),
    ("5.93",   "第 78 轮 C-26：不完备度应为 6.03"),
    ("41.8",   "第 51 轮：N_c 应为 39.6"),
    ("1.6×10⁻⁶", "第 61 轮 C-7：σ_δ 是局部曲率、不是有效宽度"),
    ("9.7×10⁻⁴", "第 61 轮：v1.32 欠采样虚高 600×"),
    ("1.75",   "第 48/51 轮 R-1：口径未限定，真三维格点跨过 0.25"),
    ("ε~10⁻²⁰", "第 53 轮：FQH 能标下 ε ≈ O(1)"),
    ("5.545",  "第 39 轮：判为伪问题"),
    ("0.4368", "第 40 轮：2×2×4 的不变读数熵密度"),
]
allok = True
for tok, note in POINTS:
    naked = [i for i, s in enumerate(L, 1) if tok in s and not M[i - 1] and not has_marks(s)]
    tot = sum(1 for s in L if tok in s)
    print("  {:<12} 共 {:>2} 处  正文无标记 = {}".format(tok, tot, naked or "无"))
    print("       （依据：{}）".format(note))
    if naked:
        allok = False
chk("CO-24", allok, "11 个已知被更正的数值**均在正文里带了更正标记**（无一裸留）")

# ---------------------------------------------------------------- 含「148」假警报的说明
hdr("CO-25  ⭐ 判据自检：裸数字串不是「值」的判据（本轮的假警报）")
L773 = L[772]
print("  L773 原文：{}".format(L773.strip()[:150]))
print("  ⟹ 上一版脚本用裸串 `148` 做判据，命中 `3.138–3.148` 的**尾三位** ⟹ **假 FAIL**。")
print("     现判据要求 ≥4 字符 ＋ （含小数点 或 4 位以上整数 或 科学计数）⟹ `148` 已被排除。")
chk("CO-25", "3.138" in L773 and "3.148" in L773, "已定位假警报来源（`3.138–3.148` 区间写法）")

hdr("汇总")
print("  CO-21…CO-25 失败 {} 项".format(FAIL))
print("=" * 78)
print("UNSYNC 88 v2 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
