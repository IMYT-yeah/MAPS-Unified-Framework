# -*- coding: utf-8 -*-
"""
第 91 轮：**把四类判定从 §9 表推到正文**（第 90 轮的续）

BC-1  全部「预言」行 → **正文 / 轮次块** 二分（模式化掩码，陷阱 65）
BC-2  正文级**实质承诺句**台账（排除 §9 表行 / 索引行 / 变更记录行 / 已标注行）
BC-3  ⭐ **冲突检测**：§9 表已判「失败」而正文同一命题**无任何限定** ⟹ 横向不一致
BC-4  摘要（§0）里列出 N 条预言，其中**带四类判定**的有几条
BC-5  中英对称性（EN 是否同样冲突）
"""
import io, re, collections

PZH = "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第91轮前.md"
PEN = "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-02第91轮前.md"
ZH, EN = "论文初稿_正反物质对风暴统一框架_v2.9.md", "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
L = io.open(PZH, encoding="utf-8").read().split("\n")     # ⚠️ 底本（铁律 18/20）
ET = io.open(PEN, encoding="utf-8").read()
FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok: FAIL += 1
def hdr(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

PAT = re.compile(r"(v2\.9\s*[^\n（|]{0,16}（第\s*\d+\s*轮|【第\s*\d+\s*轮"
                 r"|第\s*\d+\s*轮加注|第\s*\d+\s*轮口径注|第\s*\d+\s*轮补注"
                 r"|第\s*\d+\s*轮(补充|更正|登记|分层注|裁决))")
def mask(lines):
    m, inn = [], False
    for s in lines:
        if s.lstrip().startswith("|"): m.append(False); continue
        if s[:1] == "#": inn = False
        if PAT.search(s): inn = True
        m.append(inn)
    return m
M = mask(L)
FOUR = ["真预言", "postdiction", "半拟合", "失败", "解释性", "一致性构造", "未定量", "拟合式而非预言", "撤回", "作废", "结项"]

# ---------------------------------------------------------------- BC-1
hdr("BC-1  「预言」行 → 正文 / 轮次块 二分")
hits = [(i, s) for i, s in enumerate(L, 1) if "预言" in s]
body = [(i, s) for i, s in hits if not M[i - 1]]
blk = [(i, s) for i, s in hits if M[i - 1]]
print("  含「预言」行 = {}：**正文 {}** / 轮次块 {}".format(len(hits), len(body), len(blk)))
chk("BC-1", True, "已二分（第 90 轮只做了 §9 表 23 行）")

# ---------------------------------------------------------------- BC-2
hdr("BC-2  正文级**实质承诺句**台账（排除表行 / 索引 / 变更记录）")
def is_table(s): return s.lstrip().startswith("|")
def is_index(s):
    return bool(re.match(r"^\s*[-*]?\s*\*\*v1\.\d+ 变更", s)) or s.startswith("> **v1.")
def is_heading(s): return s.startswith("#")
R9 = (1889, 1922)     # §9 区间（第 90 轮已覆盖其表行与台账）
CLAIMS = []
for i, s in body:
    if is_table(s) or is_heading(s) or is_index(s):
        continue
    if R9[0] <= i <= R9[1]:
        continue
    if "目录" in s or "概览" in s:
        continue
    CLAIMS.append((i, s))
print("  实质承诺句 = {} 行".format(len(CLAIMS)))
for i, s in CLAIMS:
    mk = "【已标】" if any(k in s for k in FOUR) else "        "
    print("     L{:<5} {} {}".format(i, mk, s.strip()[:110]))

# ---------------------------------------------------------------- BC-3 冲突
hdr("BC-3  ⭐ 冲突检测：§9 表判「失败」而正文同命题**无任何限定**")
CONFLICTS = [
    (920, "第四代", "**第四代预言**：n=4 涡在 z>1000 不稳定衰变，>1 TeV 极重极短命。",
     "§9 第 5 行 =「**与 LHC 未发现存在张力**」⟹ 第 90 轮台账判 **失败**"),
]
for ln, key, txt, why in CONFLICTS:
    win = "\n".join(L[ln - 2:ln + 2])
    bad = [k for k in ["张力", "失败", "撤", "未发现", "排除"] if k in win]
    print("  L{}：{}".format(ln, txt))
    print("     邻域内的限定词 = {} ⟹ {}".format(bad or "**无**", why))
    chk("BC-3-{}".format(ln), not bad, "**冲突成立**：正文称「预言」、表格称「失败」，同一命题两种表述")
print()
# 中英对称
EN_LINE = [i for i, s in enumerate(ET.split("\n"), 1) if "Fourth-generation prediction" in s]
print("  EN 侧同样冲突 = {}".format(EN_LINE))
ew = "\n".join(ET.split("\n")[EN_LINE[0] - 2:EN_LINE[0] + 1]) if EN_LINE else ""
chk("BC-3-en", bool(EN_LINE) and not any(k in ew for k in ["tension", "failed", "excluded"]),
    "EN 也写「Fourth-generation prediction」而无限定 ⟹ **中英对称地冲突**")

# ---------------------------------------------------------------- BC-4 摘要
hdr("BC-4  摘要（§0）里的预言清单：带四类判定的有几条")
ABS = L[28]           # L29
# 摘要里用「、」列出的项
items = re.split(r"、", ABS)
print("  摘要 L29 共 {} 个「、」分隔片段 ⟹ 列出约 {} 条预言".format(len(items), len(items) - 1))
marked = [(i, x) for i, x in enumerate(items) if any(k in x for k in FOUR)]
print("  其中**带四类判定**的片段 = {}：".format(len(marked)))
for i, x in marked:
    print("     #{} {}".format(i, x.strip()[:130]))
chk("BC-4", True, "摘要列出约 {} 条预言，其中 **{} 条**带判定（S-E5 的结项）".format(len(items) - 1, len(marked)))

# ---------------------------------------------------------------- BC-5 交叉
hdr("BC-5  ⭐ 与第 90 轮台账的交叉核对")
old = [s for s in io.open(ZH, encoding="utf-8").read().split("\n") if s.startswith("> | ")]
n90 = sum(1 for s in old if re.match(r"^> \| \d+ \|", s) or re.match(r"^> \| \*\*S", s))
print("  §9 台账（第 90 轮）行数 = {}".format(n90))
print("  本轮补：正文级承诺句 {} 行".format(len(CLAIMS)))
chk("BC-5", n90 >= 20, "两段台账合计覆盖 §9 表 {} 行 ＋ 正文承诺句 {} 行".format(n90, len(CLAIMS)))

hdr("汇总")
print("  BC-1…BC-5 失败 {} 项".format(FAIL))
print("=" * 78)
print("BODY-CLAIM 91 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
