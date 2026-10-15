# -*- coding: utf-8 -*-
"""
第 89 轮（第二段·加强版）：**与轮次号无关**的「备忘录 → 论文」收录检测

RC-1 只用「轮次号」做判据 ⟹ 漏得掉「有发现、但论文里没提轮次号」的情形。
本版换更强的判据：**逐备忘录抽「标题数字 / 判决数字」，查论文是否收录**。

⚠️ 第一版的第八类判据陷阱（本版已修）：
  **行号 / 条目号不是「值」** —— `L1918`、`_refs_67.md` 的 `1278 / 1280 / 1300` 都被当成「值」了。
  ✅ 修法：**A 档 = 含小数点或科学计数法**（一定是物理量）；**B 档 = 4 位以上整数**，
     且**不得**紧跟在 `L` / `行` / `第` 之后，**也不得**出现在 `/` 分隔的裸整数串里（那是编号列表）。
"""
import io, os, re, glob, collections

MEMOS = sorted(p for p in glob.glob("*.md")
               if "_备份_" not in p
               and not p.startswith("论文初稿") and not p.startswith("Paper_")
               and p != "项目台账.md"
               and "本轮推演总结" not in p and "交接说明" not in p
               and "未完成研究工作流" not in p and not p.startswith("_"))

ZH = "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
ZH_T = io.open(ZH, encoding="utf-8").read()
EN_T = io.open(EN, encoding="utf-8").read()

FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok:
        FAIL += 1
def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

# ---------------------------------------------------------------- 判据（第八类陷阱已修）
A = re.compile(r"([0-9]+\.[0-9]{2,}(?:×10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)?)")
B = re.compile(r"(?<![L行第0-9.])([0-9]{4,})(?![0-9])")
BARE_LIST = re.compile(r"[0-9]{3,}(\s*/\s*[0-9]{3,}){2,}")   # 「a / b / c / …」编号串
def values(text):
    """返回该文本里的「物理值」集合（去噪：行号 / 条目号 / 编号串）。"""
    out = set()
    for m in A.finditer(text):
        out.add(m.group(1))
    for m in B.finditer(text):
        v = m.group(1)
        if 1900 <= int(v) <= 2100:
            continue                       # 年份
        ctx = text[max(0, m.start() - 24):m.end() + 24]
        if BARE_LIST.search(context_full(text, m)):
            continue
        if "L" + v in text or "行 " + v in text or "行" + v in text:
            continue                       # 行号引用
        out.add(v)
    return out

def context_full(text, m):
    """取该数字所处的「行」。"""
    a = text.rfind("\n", 0, m.start()) + 1
    b = text.find("\n", m.end())
    return text[a:b if b > 0 else len(text)]

def headline(text):
    """抽「标题 / 一句话结论 / 判决」区的文本。"""
    lines = text.split("\n")
    picked = []
    grab = False
    for i, s in enumerate(lines):
        if i < 14:
            picked.append(s)                       # 头部信息区
        if re.match(r"^#{1,4} ", s) and any(k in s for k in
                ["一句话结论", "判决", "结论", "净增量", "产出", "核心结果", "⭐"]):
            grab = True
            continue
        if grab:
            if re.match(r"^#{1,4} ", s):
                grab = False
            else:
                picked.append(s)
    return "\n".join(picked)

# ---------------------------------------------------------------- RC-5
hdr("RC-5  ⭐ 逐备忘录：「标题/判决」区的数字，论文收录了几个？")
rows = []
for p in MEMOS:
    t = io.open(p, encoding="utf-8", errors="replace").read()
    vs = values(headline(t))
    if not vs:
        continue
    hit = [v for v in vs if v in ZH_T]
    rows.append((p, len(vs), len(hit), sorted(set(vs) - set(hit))))
rows.sort(key=lambda r: (r[2] / r[1]))
print("  共 {} 份备忘录抽到标题数字（其余 {} 份标题区无数字）".format(len(rows), len(MEMOS) - len(rows)))
print("\n  | 备忘录 | 标题数字 | 论文已收 | 收录率 | 未收录示例（前 4） |")
print("  |---|---|---|---|---|")
for p, n, h, miss in rows[:35]:
    print("  | {} | {} | {} | {:.0%} | {} |".format(
        p[:34], n, h, h / n, ", ".join(miss[:4]) if miss else "—"))
print("  …（共 {} 行）".format(len(rows)))
zeroed = [(p, n, h, miss) for p, n, h, miss in rows if h == 0]
print()
print("  ⭐ **收录率 = 0 的备忘录**（标题数字一个都没进论文）= {} 份：".format(len(zeroed)))
for p, n, h, miss in zeroed:
    print("     ⚠️ {:<50} 标题数字 {} 个：{}".format(p[:50], n, ", ".join(miss[:6])))
chk("RC-5", True, "已列出（判定在人工读表后）")

# ---------------------------------------------------------------- RC-6 修正 RC-3
hdr("RC-6  ⭐ 清单 C-编号全集 vs 声明总数（修正第 88 轮 RC-3 的判据）")
LI_T = io.open("项目台账.md", encoding="utf-8").read()
codes = sorted({int(m) for m in re.findall(r"C-(\d+)", LI_T)})
declared = re.search(r"\*\*撤回 / 更正\*\* \| \*\*(\d+) 条\*\*", LI_T)
print("  清单里出现的 C-编号：{} 个（最小 {}，最大 {}）".format(len(codes), min(codes), max(codes)))
print("  声明的总账条数 = {}".format(declared.group(1) if declared else "未找到"))
# C-1/C-2 等早期条目可能不在本文件里；用「最大编号 − 缺口」核对
gaps = [i for i in range(min(codes), max(codes) + 1) if i not in codes]
print("  编号区间 {}–{} 内的缺口 = {}".format(min(codes), max(codes), gaps or "无"))
exp = max(codes) - len(gaps)
print("  ⟹ 实际连续编号数 = {} − {} = {}".format(max(codes), len(gaps), exp))
chk("RC-6", declared is not None and exp == int(declared.group(1)),
    "声明的 {} 条 == 实际连续编号 {} 条".format(declared.group(1) if declared else "?", exp))
print("  ⚠️ 上一版（RC-3）用 `^\\| \\*\\*C-\\d+\\*\\* \\|` 数**行数**得 36，而 C 条目是**合并行**")
print("     （C-3…C-41 被写在同一行的长串里）⟹ 判据错，不是台账错。")

# ---------------------------------------------------------------- RC-7 修正 RC-4
hdr("RC-7  ⭐ 最近 10 轮的备忘录定位（修正：**glob 而不是硬编码文件名**）")
RECENT_ROUNDS = list(range(79, 89))
found = {}
for n in RECENT_ROUNDS:
    hits = []
    for p in MEMOS:
        t = io.open(p, encoding="utf-8", errors="replace").read()[:600]
        if re.search(r"第\s*{} \s*轮".format(n), t):
            hits.append(p)
    found[n] = hits
for n in RECENT_ROUNDS:
    z = len(re.findall(r"第\s*{} \s*轮".format(n), ZH_T))
    print("  第 {} 轮  备忘录 {}  论文 ZH {} 处".format(n, found[n] or "⚠️未定位", z))
chk("RC-7", all(found[n] for n in RECENT_ROUNDS),
    "10 轮全部定位到备忘录（上一版我**硬编码文件名**，第 83 轮记错了 ⟹ 假『缺文件』）")

# ---------------------------------------------------------------- RC-8 第八类陷阱
hdr("RC-8  ⭐ 第八类判据陷阱：**行号 / 条目号不是「值」**")
print("  第一版把下面这些都当成了「物理值」并去论文里找：")
for s in ["L1918", "`_refs_67.md` L192 的 `1278 / 1280 / 1300 / 1303 / 1344`"]:
    print("     ⚠️ {}".format(s))
print("  ⟹ 它们分别是**论文行号引用**与**参考文献条目号**，论文里当然查不到 —— 纯假警报。")
chk("RC-8", "1278" not in ZH_T and "L1918" not in ZH_T,
    "已复现（`1278` / `L1918` 在论文里确实 0 处，但它们本就不该在）")

hdr("汇总")
print("  RC-5…RC-8 失败 {} 项".format(FAIL))
print("=" * 78)
print("REVERSE CHECK 89 v2 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
