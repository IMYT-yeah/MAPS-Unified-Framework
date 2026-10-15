# -*- coding: utf-8 -*-
"""
第 88 轮 正式核验：**C-43 —— §10.1 的「完成度 ~90%」与 §9 / §10.2 / §1 不相容**

发现路径（三段审计）：
  ① _consistency_88.py ：14 条命题的出现点台账（正文 vs 轮次块）
  ② _unsync_88b.py     ：未同步残留全量检测（旧值是否裸留正文）
  ③ _label_audit_88.py ：「框架独有 / 硬预测 / 完成度」标签一致性
  ⟹ ①② 全部**通过**（无残留）；③ 在「**定性自评**」这一格上翻出真问题。

C-43 的判据：**「完成度 ~90%」是全文唯一的定量自评，却是全文唯一没有度量的数**；
  它与 ①同章 §10.2 的开放问题表、②§9 表的状态列、③§1 的自定位声明**三处不相容**。
"""
import io, re

ZH = "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
PRE = "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第88轮前.md"
LIST = "工程期望清单.md"

FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok:
        FAIL += 1
def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

L = io.open(ZH, encoding="utf-8").read().split("\n")
E = io.open(EN, encoding="utf-8").read().split("\n")
P = io.open(PRE, encoding="utf-8").read().split("\n")

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
M = mask(P)      # ⚠️ 底本用**补丁前的备份**（陷阱 20/47）：本轮的补丁会给它加注

# ---------------------------------------------------------------- CR-1
hdr("CR-1  「完成度 ~90%」是全文唯一的定量自评，且**没有度量**")
hits = [i for i, s in enumerate(P, 1) if "完成度" in s]
print("  「完成度」出现行 = {}".format(hits))
for i in hits:
    print("     L{}: {}".format(i, P[i - 1].strip()[:170]))
CTX = " ｜ ".join(P[i - 1] for i in range(hits[0], min(hits[0] + 4, len(P))))
METRIC = ["度量", "分母", "分子", "按条数", "按条目", "定义", "口径", "如何计", "标准是", "以…计"]
has_metric = [k for k in METRIC if k in CTX]
chk("CR-1a", len(hits) == 1, "「完成度」全文只出现 1 处（行 {}）—— 与 §9 表里 14+ 行状态并存".format(hits))
chk("CR-1b", not has_metric,
    "同行与后 3 行内**没有任何度量定义**（命中词 = {}）⟹ 90% 的来源不可复核".format(has_metric or "无"))

# ---------------------------------------------------------------- CR-2
hdr("CR-2  §9 表（可检验预言）里「未完成 / 有张力」状态行数")
STAT = ["❌", "待推导", "张力", "判别中", "定性预言", "理论可检验", "未发现", "接近窗口边缘"]
sec9 = [(i, P[i - 1]) for i in range(1890, 1921) if P[i - 1].lstrip().startswith("|")]
cnt = {}
for i, s in sec9:
    for k in STAT:
        if k in s:
            cnt.setdefault(k, []).append(i)
print("  §9（行 1890–1920）表格行 {} 行；状态词计数：".format(len(sec9)))
for k, v in sorted(cnt.items(), key=lambda kv: -len(kv[1])):
    print("     {:<12} {} 行 {}".format(k, len(v), v))
neg = len([1 for i, s in sec9 if ("❌" in s or "张力" in s or "待推导" in s or "判别中" in s)])
chk("CR-2", neg >= 3,
    "§9 表里「❌ / 张力 / 待推导 / 判别中」共 {} 行 ⟹ 9 成完成度与这张表并列时读者会困惑".format(neg))

# ---------------------------------------------------------------- CR-3
hdr("CR-3  §10.2 开放问题表：仍开放 / 不声称 的条数")
sec102 = [(i, P[i - 1]) for i in range(1945, 1960) if re.match(r"^\d+\. ", P[i - 1])]
OPEN = ["仍开放", "不声称", "遗留", "待做", "未推导", "深度开放", "仍待"]
op = [(i, s) for i, s in sec102 if any(k in s for k in OPEN)]
print("  §10.2 编号条目 {} 条；其中显式含「仍开放 / 不声称 / 遗留」的 {} 条：".format(len(sec102), len(op)))
for i, s in op:
    print("     L{}: {}".format(i, s.strip()[:150]))
chk("CR-3", len(op) >= 3, "§10.2 有 {} 条明示仍未闭合（同章与「完成度 ~90%」并列）".format(len(op)))

# ---------------------------------------------------------------- CR-4
hdr("CR-4  §1 自定位 vs §10.1：不同章、相距 > 1000 行、**只指向 §10.2 不指向 §10.1**")
pos = [i for i, s in enumerate(P, 1) if ("参考架构" in s or "非已确立物理" in s)]
print("  §1 自定位行 = {}".format(pos))
for i in pos:
    print("     L{}: {}".format(i, P[i - 1].strip()[:160]))
d = hits[0] - max(pos)
# ⚠️ 第一版判据写错：我用 `"§10" in s` ⟹ §1 的 L31 里含 **§10.2** ⟹ 假 FAIL。
#    正确的判据要**精确到小节号**：§1 指明了 §10.2（开放问题），却**没有**指明 §10.1（完成度）。
cross101 = [i for i in pos if "§10.1" in P[i - 1]]
cross102 = [i for i in pos if "§10.2" in P[i - 1] or "§10.3" in P[i - 1]]
print("  §1 处指向 **§10.1** 的交叉引用 = {}".format(cross101 or "无"))
print("  §1 处指向 **§10.2 / §10.3** 的交叉引用 = {}".format(cross102 or "无"))
print("  ⚠️ 第一版判据用 `\"§10\" in s`，被 §1 里的 **§10.2** 命中 ⟹ 假 FAIL（判据太粗）")
chk("CR-4", d > 1000 and not cross101,
    "相距 {} 行；§1 只指向 §10.2（开放问题）、**不指向 §10.1（完成度）** ⟹ "
    "「非已确立物理」的声明与「~90%」的声明**从未在同一处被并列**".format(d))

# ---------------------------------------------------------------- CR-5
hdr("CR-5  第 63 轮的「公开就绪度」评估是否进入论文")
for tok in ["就绪度", "公开发表", "投稿", "审稿人", "参数表", "★★★"]:
    n = sum(1 for s in P if tok in s)
    print("  {:<10} 论文里 {} 处".format(tok, n))
chk("CR-5", sum(1 for s in P if "就绪度" in s) == 0,
    "「就绪度」0 处 ⟹ 第 63 轮的三项硬指标（独有+可测+有数=1 / ★★★=0 / 参数表 0 处）**从未进入论文**")

# ---------------------------------------------------------------- CR-6
hdr("CR-6  中英同步：这一处**不是**同步问题（排除一个方向）")
zh_n = sum(1 for s in P if "完成度" in s)
en_n = sum(1 for s in E if "completeness" in s or "90%" in s)
print("  ZH「完成度」{} 处；EN「completeness / 90%」{} 处".format(zh_n, en_n))
chk("CR-6", zh_n >= 1 and en_n >= 1, "两稿都有 ⟹ C-43 是**内容**问题，不是中英不同步")

# ---------------------------------------------------------------- CR-7 正面确认
hdr("CR-7  ⭐ 正面确认：11 个已知被更正的数值**全部带更正标记**（未同步残留 = 0）")
CMARK = ["更正", "原报", "原记", "原写", "原值", "撤回", "作废", "已改为", "应改为", "→",
         "移除", "补注", "口径注", "加注", "裁决", "降调", "结项", "旧值"]
has = lambda s: any(k in s for k in CMARK)
POINTS = ["0.4510", "0.4330", "6224", "5.93", "41.8", "1.6×10⁻⁶", "9.7×10⁻⁴",
          "1.75", "ε~10⁻²⁰", "5.545", "0.4368"]
allok = True
for t in POINTS:
    naked = [i for i, s in enumerate(P, 1) if t in s and not M[i - 1] and not has(s)]
    if naked:
        allok = False
    print("  {:<12} 正文无标记行 = {}".format(t, naked or "无"))
chk("CR-7", allok, "11/11 全部带标记 ⟹ **无「正文裸留旧值」**（这是本轮最重要的**正面**产出）")

# ---------------------------------------------------------------- CR-8 判据陷阱
hdr("CR-8  ⭐ 本轮踩到的四类「判据陷阱」（全部为假警报，逐条复现）")
print("  ① **裸数字串不是「值」的判据**：`148`")
L773 = P[772]
print("     L773 含 `3.138–3.148`（区间写法）⟹ 裸串命中尾三位 ⟹ 假 FAIL")
chk("CR-8a", "3.138" in L773 and "3.148" in L773, "已复现（`3.138–3.148`）")
print("  ② **数字子串判据会误命中**：`0.04` ⊂ `0.0493`（L1435）、`1.00` ⊂ `α=1`（L278/280）")
chk("CR-8b", any("0.0493" in s for s in P) and any("α=1 " in s or "α=1为" in s or "α = 1" in s for s in P),
    "已复现（`0.0493` / `α=1`）")
print("  ③ **`X → Y` 不一定是更正，也可能是「序列/递进」**：")
L465, L589 = P[464], P[588]
print("     L465：{}".format(L465.strip()[:170]))
print("     L589：{}".format(L589.strip()[:170]))
chk("CR-8c", "0.4679" in L465 and "0.4335" in L465 and "0.4334" in L465,
    "L465 的 `0.4679 → 0.4335 → 0.4334 → 0.4617` 是**跨 N 曲线**（N=8→16→24→32），不是更正对")
chk("CR-8d", "0.4335" in L589 and "0.4334" in L589,
    "L589 的 `0.4335 → 0.4334` 是 **N=16 vs N=24**（原文写「N=16 → 24 几乎饱和」）")
print("  ④ **表格行会被拆成多行**：§9 的 S-C1 / S-E1 行，加注写在**续行**上")
# ⚠️ 第一版判据写错：`[i for i,s in ...if "S-C1" in s][0]` 取到的是**第 61 轮块里的 S-C1**（L853），
#    不是 §9 表格行（L1918）⟹ 又踩「同名条目定位错位」（技能陷阱 73）。
#    正确判据：**锚定表格行**（以 `| **S-C1** |` 开头）。
s_c1_rows = [i for i, s in enumerate(P, 1) if s.startswith("| **S-C1** |")]
s_e1_rows = [i for i, s in enumerate(P, 1) if s.startswith("| **S-E1** |")]
print("  §9 表格行定位：S-C1 = {}，S-E1 = {}（⚠️ 全文另有 {} 处「S-C1」出现在轮次块里）".format(
    s_c1_rows, s_e1_rows, sum(1 for s in P if "S-C1" in s) - len(s_c1_rows)))
r = s_c1_rows[0]
cont = " ｜ ".join(P[r - 1:r + 2])
print("  S-C1 行 + 续行 = {}".format(cont[:260]))
chk("CR-8e", "第 61 轮加注" in cont,
    "S-C1（表行 L{}）的加注在**续行 L{}** ⟹ 单行判据会漏（本条我第一遍就漏了）".format(r, r + 2))
e = s_e1_rows[0]
chk("CR-8f", "第 61 轮加注" in " ｜ ".join(P[e - 1:e + 2]),
    "S-E1（表行 L{}）同样：加注在续行 L{}".format(e, e + 2))

# ---------------------------------------------------------------- CR-9
hdr("CR-9  C-43 的「三处不相容」定量化")
print("  (a) §10.1「完成度 ~90%」：1 处，**无度量定义**")
print("  (b) §10.2 同章开放问题：{} 条编号条目，其中 {} 条明示未闭合".format(len(sec102), len(op)))
print("  (c) §9 可检验预言表：{} 行，其中「❌/张力/待推导/判别中」{} 行".format(len(sec9), neg))
print("  (d) §1 自定位「参考架构，非已确立物理」：{} 处，与 §10.1 相距 {} 行".format(len(pos), d))
print("  (e) 全文「就绪度」0 处（第 63 轮评估未入论文）")
chk("CR-9", len(sec102) >= 10 and neg >= 3 and len(pos) >= 2 and d > 1000,
    "「完成度 ~90%」与 (b)(c)(d) 并列时**无任何限定语** ⟹ 判据：**同一命题（成熟度）四处表述不一致**")

hdr("汇总")
print("  CR-1…CR-9 失败 {} 项".format(FAIL))
print("=" * 78)
print("READINESS 88 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
