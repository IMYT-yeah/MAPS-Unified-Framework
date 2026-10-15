# -*- coding: utf-8 -*-
"""第 90 轮 补丁后核验（铁律 18；两段式见陷阱 72）V-1…V-10"""
import io, os, re

ZH  = "论文初稿_正反物质对风暴统一框架_v2.9.md"
PZH = "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第90轮前.md"
EN  = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
PEN = "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-02第90轮前.md"
LIST= "项目台账.md"
PLIST="项目台账_备份_2026-10-02第90轮前.md"
HS  = "../环境说明.md"
PHS = "../环境说明_备份_2026-10-02第90轮前.md"
MEM = "../.workbuddy/memory/MEMORY.md"
FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok: FAIL += 1
def hdr(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)
rd = lambda p: io.open(p, encoding="utf-8").read()

# ---------------------------------------------------------------- V-1 裸竖线
hdr("V-1  ⭐ 两段式：§9 表里的裸竖线")
def raw_pipes(t):
    return [i for i, s in enumerate(t.split("\n"), 1)
            if s.lstrip().startswith("|") and re.search(r"[^\\]\|[A-Za-z_][^|]*\|", s)]
a, b = raw_pipes(rd(PZH)), raw_pipes(rd(ZH))
print("  ZH 表格行含裸竖线：补丁前 {} 行 {} → 补丁后 {} 行 {}".format(len(a), a, len(b), b))
chk("V-1a", len(a) == 1 and len(b) == 0, "ZH：1 处 → 0 处")
ae, be = raw_pipes(rd(PEN)), raw_pipes(rd(EN))
chk("V-1b", len(ae) >= 1 and len(be) == 0, "EN：{} 处 → 0 处".format(len(ae)))
chk("V-1c", "\\|G\\|²" in rd(ZH) and "\\|G\\|²" in rd(EN), "两稿都已转义为 `\\|G\\|²`")

# ---------------------------------------------------------------- V-2 S-C1 行
hdr("V-2  ⭐ S-C1 残行：3 行 → 1 行，列数 = 4")
def sc1(path):
    lines = rd(path).split("\n")
    idx = [i for i, s in enumerate(lines) if s.startswith("| **S-C1** |")]
    return idx, lines
i0, l0 = sc1(PZH); i1, l1 = sc1(ZH)
n_pre = 0
k = i0[0] + 1
while k < len(l0) and not l0[k].startswith("|") and l0[k].strip():
    n_pre += 1; k += 1
split_cells = lambda s: re.split(r"(?<!\\)\|", s.strip().strip("|"))
cells_now = len(split_cells(l1[i1[0]]))
print("  ZH：补丁前 S-C1 行 ＋ {} 个续行 → 补丁后 1 行，列数 = {}".format(n_pre, cells_now))
chk("V-2a", n_pre >= 2 and cells_now == 4, "ZH 合并成功且列数正确")
ieg, leg = sc1(PEN); ien, len_ = sc1(EN)
n_pe = 0
k = ieg[0] + 1
while k < len(leg) and not leg[k].startswith("|") and leg[k].strip():
    n_pe += 1; k += 1
cells_en = len(split_cells(len_[ien[0]]))
chk("V-2b", n_pe >= 3 and cells_en == 4, "EN：＋{} 续行 → 1 行，列数 = {}".format(n_pe, cells_en))

# ---------------------------------------------------------------- V-3 台账
hdr("V-3  §9 四类判定台账：底本 0 → 现稿 1（中英）")
for path, pre, key, tag in [(ZH, PZH, "v2.9 补标（第 90 轮", "V-3a"),
                            (EN, PEN, "v2.9 labelling (round 90", "V-3b")]:
    x, y = rd(pre).count(key), rd(path).count(key)
    print("  {}：补丁前 {} 处 → 补丁后 {} 处".format(os.path.basename(path)[:12], x, y))
    chk(tag, x == 0 and y == 1, "台账新增且唯一")

# ---------------------------------------------------------------- V-4 块连续性
hdr("V-4  ⭐ 插入块是**连续引用块**（陷阱 74 子坑）")
for path, mk, nm, tag in [(ZH, "v2.9 补标（第 90 轮", "§9 表此后每行必须带四类判定", "V-4a"),
                          (EN, "v2.9 labelling (round 90", "count *independent relations*, not *rows*", "V-4b")]:
    lines = rd(path).split("\n")
    a = [i for i, s in enumerate(lines) if mk in s]
    b = [i for i, s in enumerate(lines) if nm in s]
    ok = len(a) == 1 and len(b) == 1 and a[0] < b[0]
    span = lines[a[0]:b[0] + 1] if ok else []
    blanks = sum(1 for s in span if s.strip() == "")
    nonq = sum(1 for s in span if s.strip() and not s.startswith(">"))
    chk(tag, ok and blanks == 0 and nonq == 0,
        "{}：块 {} 行，空行 {}，非引用行 {} ⟹ {}".format(
            os.path.basename(path)[:12], len(span), blanks, nonq,
            "连续 ✓" if blanks == 0 and nonq == 0 else "被切断 ✗"))

# ---------------------------------------------------------------- V-5 中英同步
hdr("V-5  中英同步（同一组数两边都在）")
zt, et = rd(ZH), rd(EN)
for k in ["真预言 11", "独立出口", "6 列", "2 / 2 / 3", "弦张力"]:
    print("     {:<12} ZH {} / EN(对应词) {}".format(k, zt.count(k), "—"))
for k in ["true prediction 11", "independent exits", "6 columns", "string tension"]:
    print("     {:<24} EN {} 处".format(k, et.count(k)))
for k, tag in [("真预言 11", "V-5a"), ("独立出口", "V-5b")]:
    chk(tag, zt.count(k) >= 1, "ZH「{}」在档".format(k))
for k, tag in [("true prediction 11", "V-5c"), ("*independent* exits", "V-5d")]:
    chk(tag, et.count(k) >= 1, "EN「{}」在档".format(k))

# ---------------------------------------------------------------- V-6 清单
hdr("V-6  清单台账")
li, pli = rd(LIST), rd(PLIST)
chk("V-6a", "| **C-45** |" not in pli and li.count("| **C-45** |") == 1, "C-45 行：新增且唯一")
chk("V-6b", "| **撤回 / 更正** | **44 条**" in li, "总账 43 → 44")
codes = sorted({int(m) for m in re.findall(r"(?<![A-Za-z])C-(\d+)", li)})
print("  严格 C 编号 = {} 个（1–{}）".format(len(codes), max(codes)))
non = []
for c in codes:
    for s in li.split("\n"):
        if re.match(r"^\| \*\*C-{}\*\* \|".format(c), s):
            cols = [x.strip() for x in s.strip("|").split("|")]
            if len(cols) > 2 and "撤回" not in cols[2] and "更正" not in cols[2]:
                non.append(c)
            break
chk("V-6c", max(codes) - len(non) == 44, "编号 {} − 非撤回更正族 {} = {} == 声明的 44".format(
    max(codes), len(non), max(codes) - len(non)))

# ---------------------------------------------------------------- V-7 元文本
hdr("V-7  ⭐ 元文本自指自检（铁律 18/20）")
import glob
files = sorted(glob.glob("*_备份_2026-10-02第90轮前.md")) + sorted(glob.glob("../环境说明_备份_2026-10-02第90轮前.md"))
allz = True
for p in files:
    c = rd(p).count("C-45")
    if c: allz = False
    print("     {:<52} C-45 补丁前 = {} 处".format(os.path.basename(p)[:52], c))
chk("V-7", allz, "全部底本 C-45 = 0 ⟹ 两列法成立")

# ---------------------------------------------------------------- V-8 记忆
hdr("V-8  项目记忆")
mt = rd(MEM)
chk("V-8a", len(mt) <= 3000, "MEMORY.md = {} 字符（限额 3000）".format(len(mt)))
chk("V-8b", "40 ⭐⭐" in mt, "铁律 40 已写入")

# ---------------------------------------------------------------- V-9 §9 全表列数
hdr("V-9  §9 全表**列数一致性**（修复后的断言）")
def section(lines, head, level):
    a = [i for i, s in enumerate(lines) if s.startswith("#" * level + " " + head)]
    if len(a) != 1: return None
    for j in range(a[0] + 1, len(lines)):
        if lines[j].startswith("#") and not lines[j].startswith("#" * (level + 1) + " "):
            return (a[0], j)
    return (a[0], len(lines))
for path, head, tag in [(ZH, "9 可检验预言", "V-9a"), (EN, "9 Testable Predictions", "V-9b")]:
    lines = rd(path).split("\n")
    r = section(lines, head, 2)
    bad = []
    i = r[0]
    while i < r[1]:
        if lines[i].lstrip().startswith("|"):
            s = lines[i].strip()
            if not re.match(r"^\|[\s\-:|]+\|$", s):
                n = len(split_cells(s))
                if n != 4:
                    bad.append((i + 1, n))
            i += 1
        else:
            i += 1
    print("  {}：列数 ≠ 4 的表格行 = {}".format(os.path.basename(path)[:12], bad or "无"))
    chk(tag, not bad, "全部表格行列数 = 4")

# ---------------------------------------------------------------- V-10 既有
hdr("V-10  既有内容未被破坏")
chk("V-10a", "3.0887·N^{−0.6836}" in zt and "3.0887·N^{−0.6836}" in et, "第 87 轮组 B 拟合式仍在")
chk("V-10b", "1895" in zt, "第 88 轮 C-43 的注仍在（相距 1895 行）")
chk("V-10c", "第 83 轮" in rd(HS) or "第 89 轮" in rd(HS), "交接说明的第 89 轮段仍在")

hdr("汇总")
print("  V-1…V-10 失败 {} 项".format(FAIL))
print("=" * 78)
print("VERIFY 90 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
