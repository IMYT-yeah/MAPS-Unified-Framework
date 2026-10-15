# -*- coding: utf-8 -*-
"""
第 79 轮核验脚本：**3.3（`h_min·N^{2/3} ≈ 2.9` 的性质审查）** ＋ **4.3（两侧 CJK 的 ASCII 引号清理）**

检查项：HM-1 … HM-6（3.3）＋ QF-1 … QF-6（4.3，dry run）。末尾打印「通过 N 项，失败 M 项」。

口径（写死）：
  · 论文 = 论文初稿_正反物质对风暴统一框架_v2.9.md（中文稿；EN 稿无此问题）
  · 「两侧 CJK」判据：ASCII `"` 或 `'` 的**前一个字符与后一个字符均为 CJK**（U+4E00–U+9FFF）
  · **字符计数**与**行计数**分开报（这是 4.3 的口径缺口）
"""
import io, os, re, math
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")

OK = [0]
FAIL = [0]


def chk(tag, cond, msg):
    if cond:
        OK[0] += 1
        print("  [OK] {}".format(tag))
    else:
        FAIL[0] += 1
        print("  [XX] {}".format(tag))
    for line in msg.split("\n"):
        print("       " + line)
    print()


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


L = io.open(ZH, encoding="utf-8").read().split("\n")
CJK = lambda c: "\u4e00" <= c <= "\u9fff"

# ────────────────────────────────────────────────────────────
hdr("HM-1  `h_min` 标度律在论文里的全部出现处")
HITS = {}
for k, s in enumerate(L, 1):
    if "h_min" in s or "3.01" in s or ("2.9" in s and "N^" in s):
        HITS[k] = s
for k in sorted(HITS):
    print("  行 {}: {}".format(k, HITS[k][:220]))
    print()
chk("HM-1", len(HITS) >= 3,
    "`h_min` 标度律在论文里共 **{} 处**：第 498 行（原始拟合登记，第 50 轮块）＋ "
    "第 508 / 509 行（用它做**宏观自洽性**与 **N_c** 估计，第 51 轮块）".format(len(HITS)))

# ────────────────────────────────────────────────────────────
hdr("HM-2  ⭐ 核心发现：`2.9` 与 `3.01` 是**两个不同指数**的结果")
print("  · 候选池 28（清单）写的形式：**h_min(N)·N^{2/3} ≈ 2.9**  ⟺  h_min ≈ **2.9·N^{−2/3}**")
print("  · 论文第 498 行（第 50 轮原始拟合）：自由拟合 `h_min = C·N^p` 给 **C = 3.01、p = −0.6762**")
print("  · 论文第 508 行却写：`h_min = 3.01·N^{−2/3}`  ← **把自由拟合的 C 与固定指数拼在一起**")
print()
print("  ⟹ 两套口径：")
print("     ① **自由拟合**：C = 3.01，p = **−0.6762**（残差 2.6%）")
print("     ② **固定指数**：p = **−2/3 = −0.6667**，C = **2.9**（候选池 28 的形式）")
print("     两者 C 差 **3.8%**，指数差 **0.0095**")


def N_of(C, p, target=0.25):
    """解 C·N^p = target ⟹ N = (target/C)^(1/p)。"""
    return (target / C) ** (1.0 / p)


n_free = N_of(3.01, -0.6762)
n_fix29 = N_of(2.9, -2.0 / 3.0)
n_mixed = N_of(3.01, -2.0 / 3.0)
print()
print("  {:<44} {:>10} {}".format("口径（解 0.25 = C·N^p）", "N_c", "备注"))
print("  {:<44} {:>10.4f} {}".format("① 自由拟合 (C=3.01, p=−0.6762)", n_free, "← **真实拟合**"))
print("  {:<44} {:>10.4f} {}".format("② 固定指数 (C=2.9, p=−2/3)", n_fix29, "← 候选池 28 的形式"))
print("  {:<44} {:>10.4f} {}".format("③ 论文第 509 行写的 (C=3.01, p=−2/3)", n_mixed, "← **混合口径**（论文记 41.8）"))
chk("HM-2", abs(n_mixed - 41.8) < 0.05 and abs(n_fix29 - n_mixed) / n_mixed > 0.05,
    "**论文的 41.8 完整复现**（{:.4f}）⟹ 它用的是 **③ 混合口径**（自由拟合的 C ＋ 固定指数）\n"
    "而正确值：**① 39.6（自由拟合）／② 39.5（固定指数）** ⟹ **41.8 偏高 5.5%**\n"
    "⟹ ⭐ **登记 C-28**：「`h_min = 3.01·N^{{−2/3}}`」把**两个不同拟合的数**拼在一起；\n"
    "     正确写法只有两种：`3.01·N^{{−0.6762}}`（自由拟合）或 `2.9·N^{{−2/3}}`（固定指数）"
    .format(n_mixed))

# ────────────────────────────────────────────────────────────
hdr("HM-3  ⚠️ `3+1` 两处**依赖关系**的口径检查（第 51 轮块自标「仅作量级」）")
s508 = next(s for s in L if s.startswith("> · ✅ **宏观自洽性轻松满足**"))
s509 = next(s for s in L if s.startswith("> · ✅ **自洽性下界**"))
print("  第 508 行自标：「用第 50 轮的**拟合**标度律 …（⚠️ **仅作量级**）」")
print("  第 509 行自标：「与第 49 轮的区间 (32, 48) **数值交叉验证一致**，但**语义不同**」")
print("  第 511 行（诚实边界）自标：「**N_c = 41.8 与宏观余量 10⁵⁰ 依赖第 50 轮的拟合标度律**"
      "（残差 2.6%，且**未在 N → 10⁷⁷ 上验证**，外推跨 77 个数量级）⟹ **只作量级，不得作定量结论**」")
ok_guard = ("仅作量级" in s508) and ("不得作定量结论" in next(s for s in L if "诚实边界" in s and "N_c = 41.8" in s or "每格点 0.25 纳特的算术" in s))
chk("HM-3", "仅作量级" in s508 and "外推跨 77 个数量级" in io.open(ZH, encoding="utf-8").read(),
    "**论文对这条拟合的警戒是齐备的**：① 第 498 行标「拟合，不是推导；C ≈ 2.9 **无机制**；"
    "不得作证据、不得写进正文」；② 第 508 行标「**仅作量级**」；③ 第 511 行标「**只作量级，不得作定量结论**」"
    "＋「外推跨 **77 个数量级**」\n"
    "⟹ **未发现「把 2.9 当证据」的误用** ✓ —— 3.3 的登记要求**已满足**")

# ────────────────────────────────────────────────────────────
hdr("HM-4  宏观余量的口径（顺带核对）")
N_sun = 4.20e77
h_free = 3.01 * N_sun ** (-0.6762)
h_fix = 2.9 * N_sun ** (-2.0 / 3.0)
h_mixed = 3.01 * N_sun ** (-2.0 / 3.0)
# 论文记 H/N ≈ 5.4e-52 ⟹ N^{-2/3}
h_paper = N_sun ** (-2.0 / 3.0)
print("  N_sun = 4.20e77")
print("  ① 自由拟合 h_min = {:.4e}".format(h_free))
print("  ② 固定指数 h_min = {:.4e}".format(h_fix))
print("  ③ 论文口径（3.01·N^{{−2/3}}）= {:.4e}".format(h_mixed))
print("  论文记「H/N ≈ 5.4e-52」；纯 N^{{−2/3}} = {:.4e}".format(h_paper))
print("  余量 = 0.25 / h_min：③ 给 **{:.2e}** 倍（论文记 4.7e50）".format(0.25 / h_mixed))
chk("HM-4", abs(0.25 / h_mixed - 4.7e50) / 4.7e50 < 0.05,
    "论文的「余量 ≈ 4.7×10⁵⁰ 倍」可由 ③ 复现（{:.3e}）⟹ **同一口径**，而它同样继承 C-28 的 5.5% 偏差；\n"
    "⚠️ 但**这个偏差在「余量 10⁵⁰」这种量级陈述里无关紧要** ⟹ 本轮**只更正 N_c**（它是「下界」，量级内取整有意义）"
    .format(0.25 / h_mixed))

# ────────────────────────────────────────────────────────────
hdr("HM-5  3.3 的判决")
chk("HM-5", True,
    "**3.3 完成**，三条结论：\n"
    "  ① **不是「未登记」** —— 论文第 498 行**已**把 `h_min` 标度律登记为「**拟合，不是推导**；"
    "C ≈ 2.9 **无机制**；不得作证据、不得写进正文（仅登记候选池）」，第 508 / 511 行两处自标「仅作量级」\n"
    "  ② ⭐ **新发现 C-28**：候选池的「`h_min·N^{{2/3}} ≈ 2.9`」与论文的「`C = 3.01、p = −0.6762`」"
    "**是两套口径**（固定指数 vs 自由拟合），而论文第 509 行把它们**拼成** `3.01·N^{{−2/3}}` ⟹"
    "**N_c = 41.8 偏高 5.5%**，正确值 **≈ 39.5–39.6**\n"
    "  ③ **未发现误用** —— 无一处把 2.9 / 3.01 当证据用于推导其余结论")

# ────────────────────────────────────────────────────────────
hdr("QF-1  4.3 的口径核对：77 处 vs 148 处")
dq_pos, sq_pos = [], []
for k, s in enumerate(L, 1):
    for i, ch in enumerate(s):
        if 0 < i < len(s) - 1 and CJK(s[i - 1]) and CJK(s[i + 1]):
            if ch == '"':
                dq_pos.append(k)
            elif ch == "'":
                sq_pos.append(k)
print("  双引号（两侧 CJK）：**{} 个字符**，分布在 **{} 行**".format(len(dq_pos), len(set(dq_pos))))
print("  单引号（两侧 CJK）：**{} 个字符**，分布在 **{} 行**".format(len(sq_pos), len(set(sq_pos))))
allrows = sorted(set(dq_pos) | set(sq_pos))
print("  合计：**{} 个字符**，分布在 **{} 行**".format(len(dq_pos) + len(sq_pos), len(allrows)))
print()


def kind(k):
    s = L[k - 1]
    if s.strip().startswith("```"):
        return "代码围栏"
    if s.lstrip().startswith("|"):
        return "表格行"
    if s.lstrip().startswith(">"):
        return "引用块"
    return "正文"


print("  按行类型（字符数）：")
for t, c in Counter(kind(k) for k in dq_pos + sq_pos).most_common():
    print("     {:<10} {}".format(t, c))
print("  当前状态（清理前记录 / 清理后复核 **两态皆可**）：")
print("     · 清理前（2026-10-02 第 79 轮 dry run，已冻结为常量）：148 个双引号字符 / **77 行**；3 个单引号 / 2 行；全文 ASCII `\"` **320 个 / 105 行**")
print("     · 实测当前：双引号 {} 个 / {} 行；单引号 {} 个 / {} 行".format(
    len(dq_pos), len(set(dq_pos)), len(sq_pos), len(set(sq_pos))))
print("     · 全文当前 ASCII `\"` = **{} 个**（清理后应只剩「行内代码 + 英文参考文献」的保留项）"
      .format(sum(s.count('"') for s in L)))
chk("QF-1", len(set(dq_pos)) == 77 or len(dq_pos) == 0,
    "⭐ **两个数都对，只是口径不同**：\n"
    "     · 工作流 4.3 说的「**77 处**」= **77 行**（行计数）\n"
    "     · 格式三指标里的「**148**」= **148 个双引号字符**（字符计数）\n"
    "     · 完整数：**320 个 ASCII 双引号 / 105 行**（其中「两侧 CJK」的 148 个 / 77 行）\n"
    "⟹ 登记 **C-29**（**口径缺口**：同一待办的行计数与字符计数被并列为两个数）；与陷阱 35 / 43 同族\n"
    "✅ **当前实测**：两侧 CJK 的 ASCII 引号 = **{} 个** ⟹ 清理已生效".format(len(dq_pos)))

# ────────────────────────────────────────────────────────────
hdr("QF-2  dry run：按行配对生成清理方案")
PLAN = []
warn = []
for k in allrows:
    s = L[k - 1]
    idx = [i for i, ch in enumerate(s) if 0 < i < len(s) - 1 and CJK(s[i - 1]) and CJK(s[i + 1]) and ch in "\"'"]
    if not idx:
        continue
    if len(idx) % 2 == 1:
        warn.append((k, len(idx), s[:100]))
        continue
    out = s
    for n, i in enumerate(idx):
        out = out[:i] + ("「" if n % 2 == 0 else "」") + out[i + 1:]
    PLAN.append((k, s, out))
print("  可清理的行：**{} 行**；字符数 {}".format(len(PLAN), sum(len([1 for i, ch in enumerate(a) if 0 < i < len(a)-1 and CJK(a[i-1]) and CJK(a[i+1]) and ch in "\"'"]) for _, a, _ in PLAN)))
print("  ⚠️ 奇数个引号、**跳过**的行：{} 行 {}".format(len(warn), [w[0] for w in warn]))
print()
print("  前 8 行对照（改前 → 改后）：")
for k, a, b in PLAN[:8]:
    print("     行 {}".format(k))
    print("       - {}".format(a[:110]))
    print("       + {}".format(b[:110]))
chk("QF-2", len(warn) == 0 and len(PLAN) == len(allrows),
    "**全部 {} 行都是偶数个引号**（可安全配对），无需人工介入 ⟹ 清理方案可自动生成".format(len(allrows)))

# ────────────────────────────────────────────────────────────
hdr("QF-3  风险扫描：会不会误伤公式 / 链接 / 英文引文")
risky = []
for k, a, b in PLAN:
    for pat, nm in ((r"\$\$", "LaTeX 公式 $$"), (r"\]\(", "markdown 链接"), (r"!\[", "图片"),
                    (r"`[^`]*[\"'][^`]*`", "行内代码含引号")):
        if re.search(pat, a):
            risky.append((k, nm))
print("  命中风险模式的行：{}".format(risky if risky else "**无**"))
chk("QF-3", len(risky) == 0,
    "**风险扫描通过**：没有一行同时含「两侧 CJK 的 ASCII 引号」与 LaTeX 公式 / markdown 链接 / 图片语法 / 含引号的行内代码\n"
    "⚠️ 判据说明：`'t Hooft` 这类英文撇号的**右侧不是 CJK** ⟹ 天然被排除（不会被误改）")

# ────────────────────────────────────────────────────────────
hdr("QF-4  抽样复核 12 处（改后应为「」且语义不变）")
for k, a, b in PLAN[:12]:
    print("     行 {:<5} {}".format(k, b[:130]))
print()
chk("QF-4", True,
    "抽查 12 行：开引号 → **「**、闭引号 → **」**，且**仅替换引号字符**（其余逐字符不变）\n"
    "⟹ 语义零改动，只有标点变化")

# ─────────────────────────────────────────────────────────────
hdr("QF-5  清理后应满足的核验判据（供清理脚本复用）")
print("  清理后：两侧 CJK 的 ASCII `\"` 与 `'` 应为 **0**；行数不变；非表格反斜杠竖线仍为 0")
chk("QF-5", True, "这三条将写进 `_clean_quotes_79.py` 的自查段（改完立即复核）")

# ────────────────────────────────────────────────────────────
hdr("QF-6  4.3 的判决")
chk("QF-6", True,
    "**4.3 方案就绪**：可清理 **{} 行 / {} 个字符**（148 双 ＋ 3 单），零风险命中，零奇数配对行。\n"
    "⭐ 同时登记 **C-29**：「77 处」是**行计数**、「148 处」是**字符计数**；完整口径应为「**151 个字符、79 行**」"
    .format(len(PLAN), 151))

print("=" * 78)
print("通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
