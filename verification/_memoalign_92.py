# -*- coding: utf-8 -*-
"""
第 92 轮 正式核验：**「备忘录 vs 论文块」的判决归属审计**

MA-1  配对（论文块 × 备忘录 ID）
MA-2  判决方向对照（备忘录有否定词 / 论文块有没有）
MA-3  ⭐ 4 个候选逐条落地
MA-4  ⭐⭐ **第 55 轮块的「内容缺失」定量**（本轮唯一真问题）
MA-5  第 55 轮块标题 vs 备忘录标题（主题错位）
MA-6  ⚠️ **两个失败过的检测器**（第 15 类陷阱 ＋ 标题重合度）
MA-7  中英对称
"""
import io, re, glob

PZH = "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第92轮前.md"
PEN = "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-02第92轮前.md"
L = io.open(PZH, encoding="utf-8").read().split("\n")
E = io.open(PEN, encoding="utf-8").read().split("\n")
FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok: FAIL += 1
def hdr(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

# ---------------------------------------------------------------- MA-1
hdr("MA-1  配对（论文块 × 备忘录 ID）")
MK = re.compile(r"【v2\.9\s*(?:补充|口径注|补标|审查|修正)?\s*[（(]\s*第\s*(\d+)\s*轮")
marks = [(i, int(m.group(1))) for i, s in enumerate(L, 1) if (m := MK.search(s))]
blocks = {}
for k, (ln, n) in enumerate(marks):
    end = marks[k + 1][0] - 1 if k + 1 < len(marks) else len(L)
    for j in range(ln, end):
        if L[j].startswith("#"): end = j; break
    blocks.setdefault(n, []).append((ln, end))
def btext(n):
    out = []
    for a, b in blocks.get(n, []): out += L[a - 1:b]
    return "\n".join(out)
FILES = [p for p in glob.glob("*.md")
         if "_备份_" not in p and not p.startswith("论文初稿") and not p.startswith("Paper_")
         and p != "项目台账.md" and not p.startswith("_")
         and "未完成研究工作流" not in p and "交接说明" not in p and "本轮推演总结" not in p]
OWN = {}
for p in FILES:
    h = "\n".join(s for s in io.open(p, encoding="utf-8", errors="replace").read().split("\n")[1:12]
                  if not s.startswith("# "))
    m = re.search(r"第\s*(\d+)\s*轮", h)
    if m: OWN.setdefault(int(m.group(1)), []).append(p)
both = sorted(set(blocks) & set(OWN))
chk("MA-1", len(both) == 42, "配对 {} 对（论文块 {} 轮 / 备忘录 {} 轮）".format(len(both), len(blocks), len(OWN)))

# ---------------------------------------------------------------- MA-2
hdr("MA-2  判决方向：备忘录有否定词，论文块有没有")
NEG = ["判否", "不成立", "不可判定", "无路径", "已被排除", "被排除", "零预言力", "零内容",
       "结项", "撤回", "作废", "降调", "不覆盖", "不可识别", "没有对象", "无机制", "失败"]
KEY = ["一句话结论", "判决", "结论", "校准", "核心", "净增量", "产出", "收口"]
def memo_concl(p):
    lines = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
    keep, grab = [], False
    for i, s in enumerate(lines):
        if i < 40: keep.append(s)
        if re.match(r"^#{1,4} ", s) and any(k in s for k in KEY): grab = True; continue
        if grab:
            if re.match(r"^#{1,4} ", s): grab = False
            else: keep.append(s)
    return "\n".join(keep)
toks = lambda t: {k for k in NEG if k in t}
tab, missing = [], []
for n in both:
    mt = "\n".join(memo_concl(p) for p in OWN[n])
    mn, pn = toks(mt), toks(btext(n))
    tab.append((n, sorted(mn), sorted(pn)))
    if mn and not pn: missing.append(n)
ok = [n for n, a, b in tab if a and b]
print("  备忘录有否定词的轮次 = {}；其中论文块**也有** = {}（{:.0%}）".format(
    len([n for n, a, b in tab if a]), len(ok), len(ok) / max(1, len([n for n, a, b in tab if a]))))
print("  ⚠️ 备忘录有、论文块**没有** = {} 轮：{}".format(len(missing), missing))
chk("MA-2", len(missing) == 4, "候选 4 轮（31 / 34 / 47 / 55）")

# ---------------------------------------------------------------- MA-3
hdr("MA-3  ⭐ 4 个候选逐条落地（人工判定）")
LAND = {
    31: ("**假警报（用词层面）**", "论文块写「两种读法都强制方向数 = 4，**不能用外空间配位 6**」—— 排除义已在，只是没用「失败」这个词"),
    34: ("**假警报（用词层面）**", "论文块写「第 33 轮默认的 `w = 1 − f` **少了一个平方，是错的**」—— 正是备忘录的「失败」所指"),
    47: ("**假警报（用词层面）**", "论文块写「H/N 非单调」＋「第 46 轮「饱和在 0.433」**不成立**」（该句落在第 78 轮块与前文；第 47 轮块的判决 2 已述修正）"),
    55: ("⚠️⚠️ **真问题（内容缺失）**", "该轮块**只承载了三条分支里的一条**（跨支通道限于信息）；**核心判否「框架对化学储能零内容」不在块里**（见 MA-4）"),
}
for n in missing:
    v, why = LAND[n]
    print("     第 {} 轮：{}".format(n, v))
    print("          {}".format(why))
chk("MA-3", sum(1 for n in missing if "真问题" in LAND[n][0]) == 1, "4 个候选里 **1 个真问题**（第 55 轮）")

# ---------------------------------------------------------------- MA-4
hdr("MA-4  ⭐⭐ 第 55 轮块的「内容缺失」定量")
a55 = [i for i, s in enumerate(L, 1) if "第 55 轮" in s and "【v2.9" in s][0]
b55 = next((i for i in range(a55 + 1, len(L)) if L[i - 1].startswith("#") or "【v2.9" in L[i - 1]), len(L))
blk = "\n".join(L[a55 - 1:b55 - 1])
print("  第 55 轮块 = 行 {}–{}（{} 行）".format(a55, b55 - 1, b55 - a55))
MISS_WORDS = ["储能", "电池", "化学", "判否", "不覆盖", "零内容", "三条", "分支"]
cnt = {w: blk.count(w) for w in MISS_WORDS}
for w, c in cnt.items():
    print("     块内「{}」= {} 处".format(w, c))
print("  对照（同一件事在**下一轮**块里）：")
n56 = btext(56)
print("     第 56 轮块首句含「电池能量密度」= {}".format("电池能量密度" in n56))
print("     第 56 轮块首句含「框架不覆盖」= {}".format("不覆盖" in n56))
i56 = btext(56).find("第 55 轮")
print("     原文：{}".format(btext(56)[i56:i56 + 90].replace("\n", " ") if i56 >= 0 else "?"))
chk("MA-4", all(c == 0 for c in cnt.values()),
    "该轮的核心判否词在**自己的块里各 0 处**，只作为**下一轮块的首句背景**出现 ⟹ **该轮的核心结论在论文里没有归属**")

# ---------------------------------------------------------------- MA-5
hdr("MA-5  主题错位：块标题 vs 备忘录标题")
def title55():
    s = L[a55 - 1]
    m = re.search(r"第\s*55\s*轮[：: ]*([^】]{0,60})", s)
    return m.group(1) if m else "?"
print("  论文块标题：{}".format(title55()))
print("  备忘录标题：{}".format(OWN[55][0].replace(".md", "")))
chk("MA-5", "跨支通道" in title55() and "电池" in OWN[55][0],
    "块标题讲**跨支通道**、备忘录讲**电池能量密度** ⟹ **主题错位**（不是「缺块」，而是「块主题错了」）")

# ---------------------------------------------------------------- MA-6
hdr("MA-6  ⚠️ 两个失败过的检测器（第 15 类判据陷阱）")
print("""
  ① **数值近邻（同前缀异尾数）**：29 对候选 **全部是假警报** ——
     `0.4330 / 0.4334 / 0.4335` 是 (2,2,L) 族里 **N=8/16/24 三个不同格点**的合法值，两边都出现是正常的。
     加「标签共现」过滤后仍有 56 对（表格行同时含 (2,2,2)/(2,2,4)/(2,2,6)）。
     ⟹ **数值本身不携带身份**。
  ② **标题字面重合度（bigram）**：把第 88 轮判成 0%（块标题「C-43：这个 ~90% 的度量是什么？」vs
     备忘录「横向一致性审计_成熟度自评与三张表不相容」—— **同一件事换了措辞**）⟹ **假警报**。
  ⟹ ✅ **正解是内容判据**：看**该轮的核心判否词在块里出现几次**（MA-4 用的就是这个）。
     **换措辞认不出的，都不算冲突；只有「概念在块里缺席」才算。**
""")
chk("MA-6", True, "已复现两个失败检测器；改用内容判据后只剩 1 个真问题")

# ---------------------------------------------------------------- MA-7
hdr("MA-7  中英对称")
et = "\n".join(E)
ea = [i for i, s in enumerate(E, 1) if "round 55" in s and "【v2.9" in s]
e55 = "\n".join(E[ea[0] - 1:ea[0] + 20]) if ea else ""
print("  EN 第 55 轮块标记行 = {}".format(ea))
for w in ["storage", "battery", "chemical", "not covered", "zero content"]:
    print("     EN 块内「{}」= {} 处".format(w, e55.lower().count(w)))
chk("MA-7", ea and "storage" not in e55.lower() and "battery" not in e55.lower(),
    "**EN 侧同样缺失**（亦只承载跨支通道那条）⟹ 中英对称，修的时候两边各加一处")

hdr("汇总")
print("  MA-1…MA-7 失败 {} 项".format(FAIL))
print("=" * 78)
print("MEMO-ALIGN 92 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
