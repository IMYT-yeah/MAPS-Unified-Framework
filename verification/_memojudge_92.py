# -*- coding: utf-8 -*-
"""
第 92 轮：**「备忘录 vs 论文块」的判决方向一致性**
（第 89 轮查「有没有遗漏」；本轮查「同一命题两处表述是否冲突」）

⚠️ **数值层的路走不通（本轮实测，第 15 类判据陷阱）**：
   用「近似不相等」（同前缀异尾数）找冲突，**29 对候选全部是假警报** ——
   `0.4330 / 0.4334 / 0.4335` 是 (2,2,L) 族里 **N=8/16/24 三个不同格点**的合法值；
   加「标签共现」过滤后仍有 56 对（表格行同时含 (2,2,2)/(2,2,4)/(2,2,6)）。
   ⟹ **数值本身不携带身份**。改判**判决方向**（定性），这是更硬也更贴项目价值的判据。

MC-7  ⭐ 判决方向一致性：备忘录结论区有**否定判决**词，而论文块里**一个都没有**
MC-8  反向：论文块有否定判决，备忘录没有
MC-9  逐轮列出「备忘录否定词 / 论文块否定词」对照表
"""
import io, re, glob, collections

PZH = "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第92轮前.md"
L = io.open(PZH, encoding="utf-8").read().split("\n")
FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok: FAIL += 1
def hdr(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

# ---------------------------------------------------------------- 配对
MK = re.compile(r"【v2\.9\s*(?:补充|口径注|补标|审查|修正)?\s*[（(]\s*第\s*(\d+)\s*轮")
marks = [(i, int(m.group(1))) for i, s in enumerate(L, 1)
         if (m := MK.search(s))]
blocks = {}
for k, (ln, n) in enumerate(marks):
    end = marks[k + 1][0] - 1 if k + 1 < len(marks) else len(L)
    for j in range(ln, end):
        if L[j].startswith("#"): end = j; break
    blocks.setdefault(n, []).append((ln, end))
def block_text(n):
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
print("配对：论文块 {} 轮 × 备忘录 {} 轮 ⟹ **两边都有 = {}**".format(len(blocks), len(OWN), len(both)))

# ---------------------------------------------------------------- 判决词表
NEG = ["判否", "不成立", "不可判定", "无路径", "已被排除", "被排除", "零预言力", "零内容",
       "结项", "撤回", "作废", "降调", "不覆盖", "不可识别", "没有对象", "无机制", "失败"]
POS = ["成立", "通过", "已推进", "已解决", "可检验", "独有", "已兼容", "一致"]
KEY = ["一句话结论", "判决", "结论", "校准", "核心", "净增量", "产出", "收口"]
def memo_concl(p):
    lines = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
    keep, grab = [], False
    for i, s in enumerate(lines):
        if i < 40: keep.append(s)
        if re.match(r"^#{1,4} ", s) and any(k in s for k in KEY):
            grab = True; continue
        if grab:
            if re.match(r"^#{1,4} ", s): grab = False
            else: keep.append(s)
    return "\n".join(keep)
def toks(text, table):
    return sorted({k for k in table if k in text})

hdr("MC-7  ⭐ 判决方向一致性")
print("  判据：**备忘录结论区出现了否定判决词，而论文对应块里**一个否定词都没有** ⟹ 候选「判决未进论文」")
missing, tbl = [], []
for n in both:
    mt = "\n".join(memo_concl(p) for p in OWN[n])
    pt = block_text(n)
    mn, pn = toks(mt, NEG), toks(pt, NEG)
    mp, pp = toks(mt, POS), toks(pt, POS)
    tbl.append((n, mn, pn, mp, pp))
    if mn and not pn:
        missing.append((n, mn, OWN[n]))
print("  轮次数 = {}；其中**备忘录有否定词、论文块没有** = {} 轮：{}".format(
    len(tbl), len(missing), [m[0] for m in missing]))
print()
for n, mn, ps in missing:
    print("     第 {} 轮  《{}》".format(n, ps[0][:48]))
    print("          备忘录否定词 = {}".format(mn))
    print("          论文块前 160 字 = {}".format(block_text(n).strip()[:160].replace("\n", " ")))
chk("MC-7", True, "候选 {} 轮（人工判定）".format(len(missing)))

hdr("MC-8  反向：论文块有否定词、备忘录结论区没有")
rev = [n for n, mn, pn, mp, pp in tbl if pn and not mn]
print("  轮次 = {} 个：{}".format(len(rev), rev))
chk("MC-8", True, "已列出")

hdr("MC-9  逐轮对照表（仅列有否定词的轮次）")
print("  | 轮次 | 备忘录否定词 | 论文块否定词 | 状态 |")
print("  |---|---|---|---|")
for n, mn, pn, mp, pp in sorted(tbl):
    if not (mn or pn):
        continue
    st = "✅ 两边都有" if (mn and pn) else ("⚠️ **只在备忘录**" if mn else "（只在论文块）")
    print("  | {} | {} | {} | {} |".format(n, "／".join(mn[:5]) or "—", "／".join(pn[:5]) or "—", st))

hdr("汇总")
print("  MC-7…MC-9 失败 {} 项".format(FAIL))
print("=" * 78)
print("MEMO-JUDGMENT 92 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
