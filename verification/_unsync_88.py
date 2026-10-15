# -*- coding: utf-8 -*-
"""
第 88 轮（第二段）：**「未同步残留」机械化检测**

思路（比逐条列点更硬）：
  ① 从全文抽出所有「**旧值 → 新值**」型更正（模式词：原报 / 原记 / 原写 / 更正为 / 应为 / 改为 / → / 撤回）；
  ② 对每个**旧值**，列出它在全文的出现点；
  ③ 若某个旧值出现在**正文行**（非轮次块）且该行**不带任何更正标记** ⟹ **未同步残留**（C-35 族）。
  ④ 另附：**同一命题在正文两处数值不同**（带同一标签的行，值集合 > 1）。
"""
import io, re

ZH = "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok:
        FAIL += 1
def info(tag, msg):
    print("  [INFO] {}  {}".format(tag, msg))
def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

zh_lines = io.open(ZH, encoding="utf-8").read().split("\n")
en_text = io.open(EN, encoding="utf-8").read()

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
M = mask(zh_lines)

# 更正标记（出现这些词的行 = 已挂留痕）
CMARK = ["更正", "原报", "原记", "原写", "原值", "撤回", "作废", "已改为", "应改为", "改为",
         "→", "移除", "补注", "口径注", "加注", "裁决", "降调", "结项", "误", "残留", "旧值"]
def has_marks(s):
    return any(k in s for k in CMARK)

# ---------------------------------------------------------------- 抽「旧值 → 新值」
hdr("CO-16  从全文抽出「旧值 → 新值」型更正")
CORR = re.compile(r"(?:原(?:报|记|写|值)|从|由)\s*[*`]*([0-9]+(?:\.[0-9]+)?(?:×10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)?)"
                  r"[*`]*\s*(?:→|—>|改为|更正为|应改为|变成)\s*[*`]*([0-9]+(?:\.[0-9]+)?(?:×10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)?)")
pairs = {}
for i, s in enumerate(zh_lines, 1):
    for old, new in CORR.findall(s):
        if old != new:
            pairs.setdefault((old, new), []).append(i)
print("  抽出 {} 组 (旧值, 新值)：".format(len(pairs)))
for (o, n), ls in sorted(pairs.items(), key=lambda kv: kv[1][0]):
    print("     {:<12} → {:<12} 命中行 {}".format(o, n, ls[:6]))

# ---------------------------------------------------------------- 旧值是否还裸留在正文
hdr("CO-17  ⭐ 旧值在「正文且无更正标记」的行里是否残留")
OLD = sorted({o for (o, _) in pairs}, key=lambda x: x)
bad = []
for o in OLD:
    hits = []
    for i, s in enumerate(zh_lines, 1):
        if o not in s:
            continue
        hits.append((i, "块" if M[i - 1] else "正文", has_marks(s)))
    naked = [(i, k) for i, k, mk in hits if k == "正文" and not mk]
    print("  旧值 {:<12} 出现 {:>2} 处；其中**正文无标记** = {}".format(
        o, len(hits), naked if naked else "无"))
    if naked:
        bad.append((o, naked))
        for i, _ in naked[:3]:
            print("        L{}: {}".format(i, zh_lines[i - 1].strip()[:110]))
chk("CO-17", not bad, "无「正文裸留旧值」{}".format("" if not bad else "—— **发现残留** " + str([b[0] for b in bad])))

# ---------------------------------------------------------------- 定点排查几个已知旧值
hdr("CO-18  定点排查：几个已知被更正的数值")
POINTS = {
    "0.4510": "第 50 轮：(2,2,6) 的 H/N 应为 0.4334",
    "0.4330": "第 50 轮：(2,2,6) 的 H/N 应为 0.4334",
    "6224":   "第 50 轮：轨道数应为 6334",
    "5.93":   "第 78 轮 C-26：不完备度应为 6.03",
    "41.8":   "第 51 轮：N_c 应为 39.6",
    "1.6×10⁻⁶": "第 61 轮 C-7：σ_δ 是局部曲率、不是有效宽度",
    "9.7×10⁻⁴": "第 61 轮：v1.32 欠采样虚高 600×",
    "Δ = 1":  "第 69 轮 C-11：能隙应为 Δ = 4J",
    "1.75":   "第 48/51 轮 R-1：口径未限定，真三维格点跨过 0.25",
    "ε~10⁻²⁰": "第 53 轮：FQH 能标下 ε ≈ O(1)",
    "0.4368": "第 40 轮：2×2×4 的不变读数熵密度",
    "5.545":  "第 39 轮：判为伪问题",
}
for tok, note in POINTS.items():
    body_naked = []
    tot = 0
    for i, s in enumerate(zh_lines, 1):
        if tok in s:
            tot += 1
            if not M[i - 1] and not has_marks(s):
                body_naked.append(i)
    flag = "⚠️ 正文无标记" if body_naked else "✓"
    print("  {:<12} 共 {:>2} 处  {}  {}".format(tok, tot, flag, ("L" + str(body_naked) if body_naked else "")))
    print("       （依据：{}）".format(note))

# ---------------------------------------------------------------- 正文内同类标签多值
hdr("CO-19  正文内「同一标签多个值」检测")
LABELS = {
    "(4,4,4)":      re.compile(r"0\.1[0-9]{3}"),
    "(6,6,6)":      re.compile(r"0\.0[0-9]{3}"),
    "(2,2,6)":      re.compile(r"0\.4[0-9]{3}"),
    "N_c":          re.compile(r"\b4[0-9]\.\d\b|\b3[0-9]\.\d\b"),
    "太阳质量黑洞":  re.compile(r"[0-9]\.\d+×10⁷⁷"),
}
for lab, rx in LABELS.items():
    vals, where = {}, {}
    for i, s in enumerate(zh_lines, 1):
        if lab in s and not M[i - 1]:
            for v in rx.findall(s):
                vals.setdefault(v, []).append(i)
    print("  {:<14} 正文中出现的值 = {}".format(lab, sorted(vals.keys())))
    for v, ls in sorted(vals.items()):
        print("        {:<12} 行 {}".format(v, ls[:8]))

# ---------------------------------------------------------------- 中英同构检查
hdr("CO-20  中英「更正标记」数对照（英文稿不能落后）")
zmark = sum(1 for s in zh_lines if has_marks(s))
emark = sum(1 for s in en_text.split("\n")
            if any(k in s for k in ["correct", "correction", "superseded", "withdrawn",
                                    "formerly", "previously", "revised", "→"]))
print("  ZH 带更正标记行 = {}；EN 带更正标记行 = {}".format(zmark, emark))
chk("CO-20", emark >= zmark * 0.7,
    "EN 标记密度不低于 ZH 的 70%（{:.0%}）".format(emark / max(zmark, 1)))

hdr("汇总")
print("  CO-16…CO-20 失败 {} 项".format(FAIL))
print("=" * 78)
print("UNSYNC 88 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
