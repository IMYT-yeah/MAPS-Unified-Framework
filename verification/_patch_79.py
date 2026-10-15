# -*- coding: utf-8 -*-
"""第 79 轮论文补丁（中英同步）：C-28 口径更正（N_c 41.8 → 39.6）＋【第 79 轮】块"""
import io, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(ROOT, "MAPS-Unified-Framework", "paper", "history")
TAG = "2026-10-02第79轮前"

for p in (ZH, EN):
    b = os.path.join(HIST, os.path.basename(p).replace(".md", "_备份_{}.md".format(TAG)))
    shutil.copy2(p, b)
    print("  [BK] {}".format(os.path.basename(b)))


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<34} 命中 {} 次 —— 拒绝".format(tag, n))
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<34} 已改".format(tag))


# ── ZH 1：第 508 行公式 ──────────────────────────────────
sub_once(ZH,
         "用第 50 轮的**拟合**标度律 `h_min = 3.01·N^{−2/3}`（⚠️ 仅作量级）",
         "用第 50 轮的**拟合**标度律 `h_min = 3.01·N^{−0.6762}`（⚠️ 仅作量级；**第 79 轮 C-28**：原写 `N^{−2/3}` "
         "把**自由拟合的 C** 与**固定指数**拼在一起 —— 见本节末【第 79 轮】块）",
         "ZH 508 公式")

# ── ZH 2：第 509 行 N_c ─────────────────────────────────
sub_once(ZH,
         "解 `3.01·N^{−2/3} = 0.25` ⟹ **N_c = 41.8**（对应视界半径 R = 1.82 l_P，**普朗克尺度**）⟹ **凡 N ≥ 42 的视界都自洽**",
         "解 `3.01·N^{−0.6762} = 0.25` ⟹ **N_c = 39.6**（对应视界半径 R = 1.78 l_P，**普朗克尺度**；"
         "⚠️ **第 79 轮更正 C-28**：原记 41.8 系混用口径所致，偏高 5.5%；若改取固定指数 `2.9·N^{−2/3}` 则为 39.5）"
         "⟹ **凡 N ≥ 40 的视界都自洽**",
         "ZH 509 N_c")

# ── ZH 3：第 511 行诚实边界 ─────────────────────────────
sub_once(ZH,
         "但 **N_c = 41.8 与宏观余量 10⁵⁰ 依赖第 50 轮的拟合标度律**",
         "但 **N_c = 39.6（第 79 轮更正；原记 41.8）与宏观余量 10⁵⁰ 依赖第 50 轮的拟合标度律**",
         "ZH 511 边界")

# ── ZH 4 / 5：第 519 行两处 ─────────────────────────────
sub_once(ZH,
         "形式上 N ≤ 41 会违反（N_c = 41.8，如 (2,4,4) 的 0.2834）",
         "形式上 N ≤ 39 会违反（N_c = 39.6，如 (2,4,4) 的 0.2834）",
         "ZH 519 N_c")

# ── ZH 6：插【第 79 轮】块（在第 78 轮块之后） ──────────
ZH_ANCHOR = "> **【v2.9 补充（第 78 轮：工作流 3.1 —— 不完备度比值用更正后的群重算）】**"
BLOCK = """---

> **【v2.9 补充（第 79 轮：工作流 3.3 ＋ 4.3 —— `h_min` 拟合的口径更正（C-28）＋ 中文引号清理（C-29））】** 本轮是**审查 ＋ 数值复算 ＋ 排版清理**（脚本 `_hmin_quote_79.py` / `_clean_quotes_79.py`，**HM-1 … HM-6 ＋ QF-1 … QF-6，12 项 0 失败**）。
>
> · **3.3（`h_min·N^{2/3} ≈ 2.9` 的性质审查）**：① **登记要求已满足** —— 第 498 行**已**写「这是**拟合，不是推导**；C ≈ 2.9 **无机制**；按本项目铁律**不得作证据、不得写进正文**（仅登记候选池）」，第 508 / 511 行两处自标「仅作量级」；② **未发现误用** —— 全文**无一处**把 2.9 / 3.01 当证据用于推导其余结论。
>
> · ⭐ **C-28（本轮新查出的口径混用）**：候选池 28 的「`h_min·N^{2/3} ≈ 2.9`」与第 50 轮的自由拟合「`C = 3.01、p = −0.6762`」**是两套口径**（**固定指数** vs **自由拟合**），而本节上文把它们**拼成** `3.01·N^{−2/3}` ⟹ 由它算的 `N_c` **偏高 5.5%**：
>
> | 口径 | 含义 | 解 `0.25 = C·N^p` 给 N_c |
> |---|---|---|
> | ① **自由拟合**（C = 3.01, p = −0.6762） | 忠实于 9 个数据点的拟合 | **39.6** ← 本轮采用 |
> | ② **固定指数**（C = 2.9, p = −2/3） | 指数取整（候选池 28 的形式） | **39.5** |
> | ③ **混用**（C = 3.01, p = −2/3） | 原写法 | ~~41.8~~ |
>
> ⟹ 本轮**改用 ①**（`3.01·N^{−0.6762}`，`N_c = 39.6`，`N ≥ 40` 起自洽），后文引用的 41.8 一并更正。⚠️ 该更正只改变「**普朗克尺度下的自洽性下界**」这一档的数值，**判据语义不变**；「余量 ≈ 10⁵⁰ 倍」同样继承 5.5% 偏差，但在量级陈述里无关紧要，本轮**不逐个更正**（仅此说明）。
>
> · ⭐ **4.3（中文引号清理）**：把**中文行里的 ASCII 双引号**统一为「」—— 共 **316 个引号 / 103 行**；保留 **4 个**（行 486 的行内代码 ＋ 行 1820 的英文参考文献）。清理后「**两侧 CJK 的 ASCII 引号**」由 **148 → 0**，且**行数 / 表格 / 残片**三项自查全过。
>   ⚠️ **C-29（口径缺口）**：工作流 4.3 记的「**77 处**」是**行计数**、而格式三指标里的「**148**」是**两侧 CJK 的字符计数**，全文 ASCII 双引号实为 **320 个（105 行）** ⟹ **一个待办被记成了两个互不相容的数**。完整口径应为「**中文行里的全部 ASCII 引号：103 行 / 316 个**」。
>   ⚠️ **实现坑**：旧判据「引号**两侧均为 CJK**」太窄 —— `"配对阶数" n=3` 的**闭引号右侧是空格**，不计入 ⟹ 该行只剩 1 个候选 ⟹ **配对错位**（首次 dry run 只改了开引号）。正解 = **按行处理**：若该行是中文行（CJK ≥ 10）且引号数为**偶数**，则把该行**全部** `"` 按出现顺序配对。实测 105 个含引号的行**引号数全为偶数**（零奇数行）。
>
> ⚠️ **四条诚实边界**：① **3.3 的结论是「已登记且无误用」**，本轮**新增的是 C-28**（口径混用），**不是**发现新机制；② C-28 只改变 `N_c`（语义为**下界**）这一个数，**不影响**任何已登记的判定；③ 引号清理是**纯排版**（逐字符替换，语义零改动）；**中英在此处不同步是有意的** —— 英文正文用 ASCII 引号是正确写法；④ 本轮未改动 (2,2,L) 系列的结论，也未触碰第 78 轮刚更正的 6.03。

"""
sub_once(ZH, ZH_ANCHOR, BLOCK + ZH_ANCHOR, "ZH §4.8 插【第 79 轮】块")

# ── EN 对应 ─────────────────────────────────────────────
sub_once(EN,
         "using round 50's **fitted** scaling law `h_min = 3.01·N^{-2/3}` (⚠️ order of magnitude only)",
         "using round 50's **fitted** scaling law `h_min = 3.01·N^{-0.6762}` (⚠️ order of magnitude only; "
         "**round-79 C-28**: the original `N^{-2/3}` glued the **free-fit C** to a **fixed exponent** — see the round-79 block below)",
         "EN 531 公式")
sub_once(EN,
         "solving `3.01·N^{-2/3} = 0.25` gives **N_c = 41.8** (horizon radius R = 1.82 l_P, i.e. **Planck scale**) ⟹ **every horizon with N ≥ 42 is self-consistent**",
         "solving `3.01·N^{-0.6762} = 0.25` gives **N_c = 39.6** (horizon radius R = 1.78 l_P, i.e. **Planck scale**; "
         "⚠️ **round-79 correction C-28**: the former 41.8 came from a mixed caliber and was 5.5% high; with the fixed exponent `2.9·N^{-2/3}` it is 39.5) "
         "⟹ **every horizon with N ≥ 40 is self-consistent**",
         "EN 532 N_c")
sub_once(EN,
         "but **N_c = 41.8 and the 10⁵⁰ margin depend on round 50's",
         "but **N_c = 39.6 (corrected in round 79; formerly 41.8) and the 10⁵⁰ margin depend on round 50's",
         "EN 534 边界")
sub_once(EN,
         "formally N ≤ 41 violates it (N_c = 41.8, e.g. 0.2834 at (2,4,4))",
         "formally N ≤ 39 violates it (N_c = 39.6, e.g. 0.2834 at (2,4,4))",
         "EN 542 N_c")
EN_ANCHOR = "> **【v2.9 supplement (round 78: workflow item 3.1"
EN_BLOCK = """---

> **【v2.9 supplement (round 79: workflow items 3.3 + 4.3 — a caliber correction for the `h_min` fit (C-28), and Chinese quotation-mark cleanup (C-29))】** This round is **review + numerical recomputation + typesetting cleanup** (scripts `_hmin_quote_79.py` / `_clean_quotes_79.py`, **HM-1 … HM-6 + QF-1 … QF-6, 12 items, 0 failures**).
>
> · **3.3 (nature review of `h_min·N^{2/3} ≈ 2.9`)**: ① **the registration requirement is already met** — line 498 **already** states "this is a **fit, not a derivation**; C ≈ 2.9 has **no mechanism**; under this project's iron rules it **must not be used as evidence nor written into the main text** (candidate pool only)", and lines 508 / 511 both self-flag "order of magnitude only"; ② **no misuse found** — nowhere in the paper are 2.9 / 3.01 used as evidence to derive other conclusions.
>
> · ⭐ **C-28 (a caliber mix-up newly found this round)**: the candidate pool's "`h_min·N^{2/3} ≈ 2.9`" and round 50's free fit "`C = 3.01, p = −0.6762`" are **two different calibers** (**fixed exponent** vs **free fit**), yet the text above **glued them into** `3.01·N^{−2/3}` ⟹ the resulting `N_c` is **5.5% high**:
>
> | Caliber | Meaning | N_c from `0.25 = C·N^p` |
> |---|---|---|
> | ① **Free fit** (C = 3.01, p = −0.6762) | fit faithful to the 9 data points | **39.6** ← adopted |
> | ② **Fixed exponent** (C = 2.9, p = −2/3) | exponent rounded (candidate-pool form) | **39.5** |
> | ③ **Mixed** (C = 3.01, p = −2/3) | the original wording | ~~41.8~~ |
>
> ⟹ This round switches to ① (`3.01·N^{−0.6762}`, `N_c = 39.6`, self-consistent from `N ≥ 40`) and corrects the downstream 41.8. ⚠️ The correction changes only this one number (a **lower bound at Planck scale**); **the criterion's meaning is unchanged**. The "margin ≈ 10⁵⁰" inherits the same 5.5% bias but is immaterial at that order, so it is **not** corrected item by item (noted here only).
>
> · ⭐ **4.3 (Chinese quotation-mark cleanup)**: ASCII double quotes in Chinese lines are unified to 「」 — **316 quotes over 103 lines**; **4 are kept** (line 486 inline code + line 1820 English references). After cleanup, "ASCII quotes with CJK on both sides" goes from **148 → 0**, and the line-count / table / fragment self-checks all pass.
>   ⚠️ **C-29 (caliber gap)**: the "**77 places**" recorded for item 4.3 is a **line count**, while the "**148**" in the formatting metrics is a **character count of quotes with CJK on both sides**; the paper actually has **320 ASCII double quotes (105 lines)** ⟹ **one to-do got recorded as two mutually inconsistent numbers**. The complete caliber is "**all ASCII quotes in Chinese lines: 103 lines / 316 quotes**".
>   ⚠️ **Implementation trap**: the old criterion "CJK on **both** sides" is too narrow — in `"配对阶数" n=3` the **closing** quote is followed by a space, so it is not counted ⟹ only one candidate remains in that line ⟹ **mis-pairing** (the first dry run changed only the opening quote). The fix: **process line by line** — if the line is Chinese (CJK ≥ 10) and has an **even** number of quotes, pair **all** of its `"` in order. Measured: all 105 lines containing quotes have an **even** count.
>
> ⚠️ **Four honesty boundaries**: ① 3.3's conclusion is "**already registered and not misused**"; what is new here is **C-28** (a caliber mix-up), **not** a new mechanism; ② C-28 changes only `N_c` (a **lower bound**) and **does not affect** any registered verdict; ③ the quote cleanup is **pure typesetting** (character-by-character, zero semantic change); **the ZH/EN asynchrony here is intentional** — ASCII quotes are correct in English text; ④ this round does not touch the (2,2,L) conclusions nor the 6.03 corrected in round 78.

"""
sub_once(EN, EN_ANCHOR, EN_BLOCK + EN_ANCHOR, "EN §4.8 round-79 block")

print()
for p, nm in ((ZH, "ZH"), (EN, "EN")):
    L = io.open(p, encoding="utf-8").read().split("\n")
    bad_pipe = sum(1 for s in L if "\\|" in s and not s.lstrip().startswith("|"))
    ASCII_Q = sum(s.count('"') for s in L)
    frag = [i + 1 for i, s in enumerate(L) if s.strip().startswith(("，", ","))]
    print("  {} 行数 {}；ASCII 引号 {}；非表格反斜杠竖线 {}；残片 {}".format(nm, len(L), ASCII_Q, bad_pipe, frag))
print("  ZH「第 79 轮」=", io.open(ZH, encoding="utf-8").read().count("第 79 轮"))
print("  EN「round 79」=", io.open(EN, encoding="utf-8").read().count("round 79"))
print("  ZH 39.6 =", io.open(ZH, encoding="utf-8").read().count("39.6"))
print("  EN 39.6 =", io.open(EN, encoding="utf-8").read().count("39.6"))
