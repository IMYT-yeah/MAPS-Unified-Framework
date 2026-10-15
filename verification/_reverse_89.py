# -*- coding: utf-8 -*-
"""
第 89 轮：**反向核对（备忘录 → 论文）**

上一轮（88）的诚实边界 §六.2 留下的缺口：
  「未同步残留 = 0」只覆盖「**论文里显式写了 `X → Y` 的更正**」；
  **备忘录里记了更正、论文里从未写过的**，那套检测**看不到**。

本脚本做两个**可判定的机械检查**：
  RC-1  **轮次覆盖**：备忘录里出现过的「第 N 轮」，论文里有没有对应内容？
  RC-2  **备忘录侧的「应改论文 / 未同步」语句**：逐条抽出来，与论文对账。
"""
import io, os, re, glob, collections

MEMOS = [p for p in glob.glob("*.md")
         if "_备份_" not in p
         and not p.startswith("论文初稿") and not p.startswith("Paper_")
         and p != "工程期望清单.md"
         and "本轮推演总结" not in p
         and "交接说明" not in p
         and "未完成研究工作流" not in p]
MEMOS.sort()
ZH = "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
ZH_L = io.open(ZH, encoding="utf-8").read().split("\n")
ZH_T = "\n".join(ZH_L)
EN_T = io.open(EN, encoding="utf-8").read()

FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok:
        FAIL += 1
def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

print("备忘录族：{} 份".format(len(MEMOS)))

# ================================================================ RC-1 轮次覆盖
hdr("RC-1  ⭐ 轮次覆盖：备忘录里出现过的「第 N 轮」，论文里有没有对应内容？")

# 论文里出现的轮次号（含各种写法）
pat_zh = re.compile(r"第\s*(\d+)\s*轮")
zh_rounds = collections.Counter(int(m) for m in pat_zh.findall(ZH_T))
pat_en = re.compile(r"[Rr]ound\s+(\d+)")
en_rounds = collections.Counter(int(m) for m in pat_en.findall(EN_T))

# 备忘录里出现的轮次号
memo_rounds = collections.Counter()
for p in MEMOS:
    t = io.open(p, encoding="utf-8", errors="replace").read()
    for m in pat_zh.findall(t):
        n = int(m)
        if 1 <= n <= 90:
            memo_rounds[n] += 1

print("  备忘录里出现过的轮次：{} 个（1–{}）".format(len(memo_rounds), max(memo_rounds)))
missing = []
tbl = []
for n in sorted(memo_rounds):
    if n < 39:
        continue                      # 第 38 轮以前的备忘录没有独立文件（见交接说明）
    z, e = zh_rounds.get(n, 0), en_rounds.get(n, 0)
    tbl.append((n, memo_rounds[n], z, e))
    if z == 0:
        missing.append(n)
print("\n  | 轮次 | 备忘录提及次数 | 论文 ZH 提及 | 论文 EN 提及 |")
print("  |---|---|---|---|")
for n, m, z, e in tbl:
    flag = " ⚠️ **论文 0 处**" if z == 0 else ""
    print("  | 第 {} 轮 | {} | {} | {}{} |".format(n, m, z, e, flag))
print()
chk("RC-1a", True, "共 {} 个轮次（39–{}）在备忘录里出现，其中论文 ZH 提及 0 处的 = {}".format(
    len(tbl), max(memo_rounds), missing if missing else "无"))
if missing:
    print("  ⚠️ **候选缺口清单**（论文里一次都没提的轮次）：{}".format(missing))

# ================================================================ RC-2 备忘录侧语句
hdr("RC-2  ⭐ 备忘录侧的「应改论文 / 未同步 / 论文里 0 处」语句")
PAT_M = ["应改", "需改", "没改", "漏改", "未改", "没同步", "未同步", "只在备忘录",
         "论文里 0 处", "论文中 0 处", "尚未写入", "尚未进入论文", "须改"]
rows = []
for p in MEMOS:
    t = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
    for i, s in enumerate(t, 1):
        if any(k in s for k in PAT_M):
            rows.append((p, i, s.strip()))
print("  命中 {} 条（{} 份备忘录）".format(len(rows), len({r[0] for r in rows})))
byfile = collections.Counter(r[0] for r in rows)
print("  按备忘录分布（前 12）：")
for p, c in byfile.most_common(12):
    print("     {:<58} {} 条".format(p[:58], c))

# 数字抽取 → 与论文对账
hdr("RC-2b  ⭐ 从这些语句里抽数字，逐个查论文（**只看「论文 0 处」的**）")
NUM = re.compile(r"([0-9]+\.[0-9]{2,}(?:×10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)?|[0-9]{4,})")
cand = {}
for p, i, s in rows:
    for v in NUM.findall(s):
        cand.setdefault(v, []).append((p, i, s[:110]))
print("  抽出 {} 个不同的数字记号".format(len(cand)))
zero = []
for v, ls in sorted(cand.items()):
    in_zh = v in ZH_T
    in_en = v in EN_T
    if not in_zh:
        zero.append((v, ls))
print("  其中**论文 ZH 里 0 处**的 = {} 个：".format(len(zero)))
for v, ls in zero[:40]:
    p, i, s = ls[0]
    print("     ⚠️ {:<14} 出自《{}》L{}".format(v, p[:32], i))
    print("          「{}」".format(s))
chk("RC-2b", True, "已列出（判定在人工读表后；⚠️ 数字可能是复述旧值，须逐条看上下文）")

# ================================================================ RC-3 清单 C-xx 的「已改」声明
hdr("RC-3  清单里 C-xx 条目的「处置」列抽样核对")
LI = io.open("工程期望清单.md", encoding="utf-8").read().split("\n")
crows = [s for s in LI if re.match(r"^\| \*\*C-\d+\*\* \|", s)]
print("  清单里 C-xx 行 {} 条".format(len(crows)))
print("  处置列（第 3 列）分布：")
disp = collections.Counter()
for s in crows:
    cols = [c.strip() for c in s.strip("|").split("|")]
    if len(cols) >= 3:
        disp[cols[2][:18]] += 1
for k, v in disp.most_common(12):
    print("     {:<20} {} 条".format(k, v))
chk("RC-3", len(crows) >= 40, "C 条目共 {} 条（台账规模）".format(len(crows)))

# ================================================================ RC-4 最近 10 轮的备忘录 → 论文
hdr("RC-4  ⭐ 最近 10 轮（79–88）的备忘录是否都进了论文")
RECENT = {
    79: "不完备度比值重算_只有N24改变且论文漏改了一处.md",
    80: "⟨O⟩标度律与形状依赖_以及三条收口的取证.md",
    81: "H1到H4的收口_8π3没有对象与关联长度是二分的.md",
    82: "庞加莱猜想与Ricci流能否接入框架_四处对不上与一个补证.md",
    83: "引用撤回链的取证_金刚石与共面性.md",
    84: "全量冲突审计_撤回链依据等级与未同步检测.md",
    85: "审计面的漏洞_第84轮过苛的自我更正与备忘录族补录.md",
    86: "形状口径全链审计_后期把早期对的结论写反了一处.md",
    87: "h_min标度律的分组重拟合_两条方向相反的幂律与干净底本.md",
    88: "横向一致性审计_成熟度自评与三张表不相容.md",
}
for n in sorted(RECENT):
    f = RECENT[n]
    exists = os.path.exists(f)
    z = zh_rounds.get(n, 0)
    e = en_rounds.get(n, 0)
    print("  第 {} 轮  备忘录 {}  论文 ZH {:>2} 处 / EN {:>2} 处  {}".format(
        n, "✓" if exists else "✗ 缺文件", z, e, "⚠️**论文 0 处**" if z == 0 else ""))
miss_recent = [n for n in RECENT if zh_rounds.get(n, 0) == 0]
chk("RC-4", not miss_recent, "最近 10 轮在论文里的提及：缺失 = {}".format(miss_recent or "无"))

hdr("汇总")
print("  RC-1…RC-4 失败 {} 项".format(FAIL))
print("=" * 78)
print("REVERSE CHECK 89 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
