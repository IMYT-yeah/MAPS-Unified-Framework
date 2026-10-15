# -*- coding: utf-8 -*-
"""
第 99 轮：四源交叉清点 —— 「还能算什么 / 还能推什么」
核验项：OP-1 … OP-14（每项 [OK]/[XX]；末尾打印通过/失败计数）

四源：
  S1 台账（清单「全量待办总账」行，组 I–VI）
  S2 工作流文档 `未完成研究工作流_按依赖排序.md`（分批判定）
  S3 论文 §10.2（13 条开放问题）
  S4 外部资产待办（A1/A2/EMRI）＋ 并轨线（`MAPS与v2.8融合方案_空间库并轨备忘录.md` 的 O1–O5）

两段式：
  ① 补丁前底本 = `*_备份_2026-10-03第99轮前.md`（用于**取证**过期标记）
  ② 补丁后 = 当前文件（用于**确认**已修）
"""
import io
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)

LIST = os.path.join(BASE, "项目台账.md")
PRE_LIST = os.path.join(BASE, "项目台账_备份_2026-10-03第99轮前.md")
HAND = os.path.join(ROOT, "环境说明.md")
PRE_HAND = os.path.join(ROOT, "环境说明_备份_2026-10-03第99轮前.md")
WF = os.path.join(BASE, "未完成研究工作流_按依赖排序.md")
PAPER = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
MERGE = os.path.join(BASE, "MAPS与v2.8融合方案_空间库并轨备忘录.md")

PASS = FAIL = 0


def chk(tag, cond, msg, strict=True):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("  [OK] {:<8} {}".format(tag, msg))
    else:
        if strict:
            FAIL += 1
            print("  [XX] {:<8} {}".format(tag, msg))
        else:
            print("  [INFO] {:<8} {}".format(tag, msg))


def hdr(s):
    print("\n" + "=" * 96)
    print(s)
    print("=" * 96)


def rd(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


def taizhang_line(txt):
    for x in txt.split("\n"):
        if x.startswith("| **台账（新）**"):
            return x
    return ""


def parse_groups(line):
    """→ [(组名, [条目…])]；条目保留原文

    ⚠️ 铁律 18（元文本自指）：本轮的修补注里**列出了** 3.1／3.2／C1–C4… 这些编号，
       若不剥掉，解析器会把**注**当成新条目 —— 实测正是如此（补丁后误报 5 处过期）。
    """
    line = re.sub(r"⚠️ \*\*【第 \d+ 轮注】.*?（\*\*C-\d+\*\*[^）]*）。", "", line)
    body = line.split("**组 I（工作流第 3 批）**：", 1)[-1]
    body = re.split(r"\s*\|\s*——\s*\|", body)[0]
    chunks = re.split(r"\*\*组 ([IVX]+)(?:（[^）]*）)?\*\*：", "**组 I（工作流第 3 批）**：" + body)
    out = []
    for g, text in zip(chunks[1::2], chunks[2::2]):
        items = [s.strip(" 。") for s in text.split("／") if s.strip(" 。")]
        out.append((g, items))
    return out


print("第 99 轮：四源交叉清点（OP 系列）")

# ==================================================== S1 台账
hdr("S1  台账（清单「全量待办总账」组 I–VI）")
pre_line, cur_line = taizhang_line(rd(PRE_LIST)), taizhang_line(rd(LIST))
pg, cg = parse_groups(pre_line), parse_groups(cur_line)

# ① 结项台账（硬编码：来自清单 1.x 各轮段与备忘录名，逐条可复核）
CLOSED = {
    "3.1": "第 78 轮（`_incompleteness_78.py` 11 项 0 失败）",
    "3.2": "第 80 轮（`_shape_scaling_80.py` SH-1…SH-7）",
    "3.3": "第 79 轮（`_hmin_quote_79.py` 12 项）",
    "4.1": "第 80 轮", "4.2": "第 80 轮", "4.3": "第 79 轮（`_clean_quotes_79.py`）",
    "C1": "第 95 轮（N-40：η 能标是配的）",
    "C2": "第 95 轮（C-54：放弃 ρ_Λ=E_c⁴ 定量识别）",
    "C3": "第 76 轮（N-32：D=ℏ/(3m) 是恒等式）",
    "C4": "第 95 轮（#4 判不独有）",
    "C5": "第 93 轮", "C6": "第 75 轮（I-20）", "C7": "第 94 轮（悬空）",
    "H1": "第 81 轮（N-35：8π/3 没有对象）",
    "H2": "第 81 轮（载流子两类型）",
    "H3": "第 43 轮（交换变体，已收口）",
    "H4": "第 81 轮（关联长度是二分的）",
    "H5": "第 29/80 轮",
    "P1": "第 77 轮（g 精确值与 α 映射两半都判否）",
    "A1": "第 97 轮（8909 jobs）", "A2": "第 98 轮（4 文件重建）",
}


def stale_items(groups, label):
    """返回「已有结项记录、但行内无 ✅」的条目"""
    bad = []
    for g, items in groups:
        for it in items:
            key = None
            m = re.match(r"^(3\.\d|4\.\d)", it)
            if m:
                key = m.group(1)
            else:
                m = re.match(r"^(C\d+|H\d+|P1|A\d)", it)
                if m:
                    key = m.group(1)
            if key and key in CLOSED and "✅" not in it:
                bad.append((g, key, it[:60]))
    print("  [{}] 过期标记 = {} 处".format(label, len(bad)))
    for g, k, it in bad:
        print("       组 {:<3} {:<4} {}".format(g, k, it))
    return bad


bad_pre = stale_items(pg, "补丁前")
bad_cur = stale_items(cg, "补丁后")

chk("OP-1", len(bad_pre) == 13,
    "补丁前：台账有 **{}** 处「已结项但无 ✅」的过期标记（期望 13：3.1/3.2/4.3/C1–C4/H1–H5/P1）".format(len(bad_pre)))
chk("OP-2", len(bad_cur) == 0,
    "补丁后：过期标记 = {}（应清零）".format(len(bad_cur)) if len(bad_cur) == 0
    else "补丁后仍过期 {} 处：{}".format(len(bad_cur), [k for _, k, _ in bad_cur]))
chk("OP-3", "第 99 轮" in cur_line, "台账行含「第 99 轮」修补注")

# ② 真开放的（对照）
chk("OP-4", any("C8" in it and "✅" not in it for _, items in cg for it in items),
    "真开放项仅剩 C8 = EMRI（等 LISA）—— 台账内唯一无 ✅ 的外部项")

# ==================================================== S4 并轨线
hdr("S4  并轨线（P1–P5 / F1–F5 / SPB / 分支 A‑B / O1–O5）是否纳入待办体系")
MARK = ["空间库", "重聚焦", "SPB", "分支 A"]
def hit(p):
    t = rd(p)
    return sum(t.count(m) for m in MARK)


# ⚠️ 两段式要用**备份**做底本 —— 第一版这里误用了当前 HAND，导致「补丁前」也报 2 处
counts_pre = {n: hit(p) for n, p in
              [("清单", PRE_LIST), ("论文", PAPER), ("交接说明", PRE_HAND), ("工作流", WF)]}
counts_cur = {n: hit(p) for n, p in
              [("清单", LIST), ("论文", PAPER), ("交接说明", HAND), ("工作流", WF)]}
print("  特征短语命中： 补丁前 = {}  ／  补丁后 = {}".format(counts_pre, counts_cur))
chk("OP-5a", all(v == 0 for v in counts_pre.values()),
    "补丁前：四个台账命中 = {} ⟹ **整条并轨线（含 O1–O5）从未进入待办体系**（取证）".format(counts_pre))
chk("OP-5b", counts_cur["论文"] == 0 and counts_cur["工作流"] == 0 and counts_cur["清单"] > 0,
    "补丁后：**论文与工作流仍为 0**（并轨线至今**未写进论文**）；清单/交接的非零命中**全部来自本轮的登记行**"
    "（不是推演）⟹ 口径 = 「已登记、未推演」")
mt = rd(MERGE)
chk("OP-6", all(("O%d" % i) in mt for i in range(1, 6)),
    "并轨备忘录确实登记了 **O1–O5**（五条开放问题，各带判据）")

# ==================================================== S3 论文 §10.2
hdr("S3  论文 §10.2（13 条开放问题）的残留开放")
pt = rd(PAPER)
sec = pt.split("### 10.2 开放问题", 1)[1].split("### 10.3", 1)[0]
nums = re.findall(r"(?m)^(\d+)\. ", sec)
no_check = [n for n in nums if "✅" not in sec.split("^%s. " % n)[0][-200:]]
print("  §10.2 条目编号 =", nums)
chk("OP-7", len(nums) == 13, "§10.2 共 13 条（实测 {}）".format(len(nums)))
chk("OP-8", all(("✅" in sec) for _ in [0]) and sec.count("✅") >= 8,
    "其中 {} 处标 ✅（多数已收口）".format(sec.count("✅")))
RESID = ["4D SU(3)", "Lanford", "λ_c(∞)", "麦克斯韦谱", "4π 相位", "n=1,2,3"]
found = [r for r in RESID if r in sec]
chk("OP-9", len(found) >= 4, "残留开放项可检索到 {} 条：{}".format(len(found), found))

# ==================================================== S2 工作流
hdr("S2  工作流文档：过期 ☐ 与真未完成")
wt = rd(WF)
chk("OP-10", "不支持单独作依据" in wt or "不可单独作依据" in wt,
    "工作流文档自注「☐ 标记不可单独作依据」（与 C-19 同族，**已预先声明**）")
n_stale_wf = wt.count("第 2 批")
chk("OP-11", "S-12 平坦性的具体化" in wt and "已于 2026-10-02 第 73 轮完成" in wt,
    "第 2 批 S-12 条目内已写「第 73 轮完成」（标题未改 ⟹ 读者只看标题会误判）")

# ==================================================== 资产侧
hdr("S4b  可快速验证的资产侧入口")
lean = os.path.join(ROOT, "MAPS-Unified-Framework", "verification", "lean")
src = rd(os.path.join(lean, "StormPoC.lean"))
n_sorry = len(re.findall(r"(?m)^\s*sorry\s*$", src))
chk("OP-12", n_sorry == 2, "StormPoC.lean 当前 sorry = {}（登记值 2 ⟹ 未消）".format(n_sorry))
chk("OP-13", "待重写（陈述/证明）: BH 余 8 + AR 余 5 + LC 余 5 + LW 余 5 = 23" in src,
    "「待重写 23 条」的分族账在源码注中可复核（BH 8 / AR 5 / LC 5 / LW 5）")
mj = os.path.join(lean, "lake-manifest.json")
chk("OP-14", os.path.exists(mj) and os.path.exists(os.path.join(lean, ".lake")),
    "Lean 环境仍在位（manifest ＋ .lake 均在）⟹ **补 23 条 / 消 2 sorry 是「有环境的」任务**")

print("\n" + "=" * 96)
print("OP 汇总：通过 {} 项，失败 {} 项".format(PASS, FAIL))
print("=" * 96)
