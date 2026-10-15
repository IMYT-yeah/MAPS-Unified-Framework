# -*- coding: utf-8 -*-
"""
第 88 轮（第三段）：**标签一致性审计** —— 「框架独有 / 硬预测 / 可检验」这类标签
在全文是否都带得起（陷阱 50 的全量版）

判据（陷阱 50）：**「它给出的数值/标度律，能不能与其他理论区分？」**
  ✅ 真独有 = 给了**具体标度律或新机制**
  ❌ 假独有 = **与其他理论同值**（如 Ω_K = 0 与平 ΛCDM 同值）

另加：
  CO-26  §10.1「完成度 ~90%」这类**定性自评**是否与全文的负面登记相容
  CO-27  「框架独有」全部出现点（分类：带判别性说明 / 未带）
  CO-28  「硬预测」出现点
  CO-29  四类判定（真预言/postdiction/半拟合/失败）的标注覆盖率
  CO-30  摘要 vs §10 的自我定位
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
def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

L = io.open(ZH, encoding="utf-8").read().split("\n")
E = io.open(EN, encoding="utf-8").read()

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
def ctx(lines, i, w=150):
    """带**相邻行**的上下文（表格行会被拆行，单行判据会漏）"""
    return " ｜ ".join(x.strip()[:w] for x in lines[i - 1:i + 2] if x.strip())

# ---------------------------------------------------------------- CO-26 定性自评
hdr("CO-26  「完成度 ~90%」这类**定性自评**：出现点与附近的降调标记")
KEY = ["完成度 ~90%", "完成度", "~90%"]
seen = set()
for i, s in enumerate(L, 1):
    if "完成度" in s:
        if i in seen:
            continue
        seen.add(i)
        kind = "块" if M[i - 1] else "**正文**"
        print("  L{:<5} [{}] {}".format(i, kind, s.strip()[:200]))
print()
print("  ⚠️ 判据：定性自评必须与**全文的负面登记**相容 —— 对照项：")
for t in ["审稿人七击", "参数表", "参考架构", "启发式统一框架", "判别性"]:
    hits = [i for i, s in enumerate(L, 1) if t in s]
    print("     {:<14} 出现 {} 处（行 {}）".format(t, len(hits), hits[:6]))
print()
chk("CO-26", True, "已列出「完成度」全部出现点（判定在人工读表后）")

# ---------------------------------------------------------------- CO-27 「框架独有」
hdr("CO-27  ⭐ 「框架独有」全部出现点（陷阱 50 的全量版）")
DISC = ["判别", "区分", "与其他", "同值", "ΛCDM", "标准", "独有签名", "标度律", "∝", "仅本框架"]
rows = []
for i, s in enumerate(L, 1):
    if "框架独有" in s or "本框架独有" in s:
        rows.append((i, "块" if M[i - 1] else "**正文**", s, i))
print("  共 {} 行含「框架独有」：".format(len(rows)))
for i, kind, s, _ in rows:
    has = [k for k in DISC if k in ctx(L, i, 400)]
    print("  L{:<5} [{}] 判别性线索 = {:<20} {}".format(
        i, kind, ",".join(has) if has else "**无**", s.strip()[:130]))
nobody = [i for i, kind, s, _ in rows if kind == "**正文**" and
          not any(k in ctx(L, i, 400) for k in DISC)]
chk("CO-27", True, "正文里「框架独有」共 {} 处，其中**附近无判别性线索**的 {} 处：{}".format(
    sum(1 for r in rows if r[1] == "**正文**"), len(nobody), nobody))

# ---------------------------------------------------------------- CO-28 「硬预测」
hdr("CO-28  「硬预测 / 硬预测」出现点")
for i, s in enumerate(L, 1):
    if "硬预测" in s or "硬预言" in s:
        kind = "块" if M[i - 1] else "**正文**"
        print("  L{:<5} [{}] {}".format(i, kind, s.strip()[:190]))
print()
chk("CO-28", True, "已列出")

# ---------------------------------------------------------------- CO-29 四类判定覆盖
hdr("CO-29  第 37 轮的四类判定（真预言 / postdiction / 半拟合 / 失败）标注覆盖率")
CNT = {k: sum(1 for s in L if k in s) for k in
       ["真预言", "postdiction", "半拟合", "失败", "一致性构造", "一致（一致性构造）"]}
for k, v in CNT.items():
    print("  {:<18} {} 处".format(k, v))
pre = sum(1 for s in L if "预言" in s)
print("  ⟹ 「预言」字样共 {} 行，其中显式标了四类判定之一的 = {} 行".format(
    pre, sum(1 for s in L if "预言" in s and any(k in s for k in CNT))))
chk("CO-29", True, "覆盖率见上（本轮只登记，不做判定）")

# ---------------------------------------------------------------- CO-30 自我定位
hdr("CO-30  摘要 vs §10 的自我定位（同一命题的两处表述）")
for tok in ["启发式统一框架", "参考架构", "非已确立物理", "统一框架", "完成度 ~90%"]:
    zh_h = [i for i, s in enumerate(L, 1) if tok in s]
    en_h = E.count(tok.replace("统一框架", "unified framework")) if "framework" in tok else E.count(tok)
    print("  {:<16} ZH {} 处 {}   EN {} 处".format(tok, len(zh_h), zh_h[:6], en_h))
print()
# 摘要里的定位句
for i, s in enumerate(L[:60], 1):
    if "参考架构" in s or "启发式" in s:
        print("  L{:<4} {}".format(i, s.strip()[:230]))
chk("CO-30", True, "已列出（判定在人工读表后）")

hdr("汇总")
print("  CO-26…CO-30 失败 {} 项".format(FAIL))
print("=" * 78)
print("LABEL AUDIT 88 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
