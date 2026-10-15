# -*- coding: utf-8 -*-
r"""第 49 轮论文补丁（中英同步）：插入【第 49 轮】块。

锚点 = 第 48 轮块的最后一行（🔧 下一步），在其后插入。
"""

import io
import os
import shutil
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
STAMP = "2026-09-22第49轮前"
N_OK = [0]
N_FAIL = [0]


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<34} 命中 {} 次".format(tag, n))
        N_FAIL[0] += 1
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<34}".format(tag))
    N_OK[0] += 1


os.makedirs(HIST, exist_ok=True)
for src, stem in ((ZH, "论文初稿_v2.9"), (EN, "Paper_v2.9_EN")):
    dst = os.path.join(HIST, "{}_备份_{}.md".format(stem, STAMP))
    shutil.copy2(src, dst)
    print("  备份 ->", os.path.basename(dst))
print()

ZH_A = "> 🔧 **下一步（两条都可证伪）**：① 在 N=32/64/128 上补形状，定位 **0.25 的跨点**"
EN_A = "> 🔧 **Next (both falsifiable)**: ① add shapes at N=32/64/128 to locate **the crossing point of 0.25**"

ZH_BLOCK = """
> **【v2.9 补充（第 49 轮：定位 0.25 的跨点 —— H/N 随 N 的**两条反向曲线**）】** 上一条留下两条可证伪的预判。本轮用 GAP 沿 (2,4,L) 扫描并补算，结果是**把上一条的判据细化**。
>
> · **跨点已夹住**：沿 (2,4,L)（1 个 L=2 方向）扫 —— **(2,4,4) N=32：0.2834**（[0.272,0.295]，偏大）⟶ **(2,4,6) N=48：0.2208**（[0.211,0.231]，偏小）⟶ (2,4,8) N=64：0.1802 ⟶ **(2,4,10) N=80：0.1571** ⟶ **(2,4,12) N=96：0.1338**。⟹ **0.25 的跨点落在 N ∈ (32, 48)**，且组内 H/N **单调下降**。⚠️ 本轮**没有格点"命中" 0.25**（所有 95% 区间都不含 0.25）⟹ 跨点只能给**区间**。
> · **本轮的结构性发现：两组随 N 走向相反**。**≥2 个 L=2 方向**随 N **上升**：0.4335（N=16）⟶ 0.4510（24）⟶ **0.4802**（40）⟶ **0.5041**（48）⟶ **0.5170**（56）⟶ 0.5307（64）；**≤1 个 L=2 方向**随 N **下降**：0.2834（32）⟶ 0.2208（48）⟶ 0.1802 / 0.1839（64）⟶ **0.1652**（72，(2,6,6)）⟶ 0.1571（80）⟶ 0.1338 / 0.1484（96）。⟹ **上一条的判据要细化：「L = 2 方向的个数」决定的是分组，而组内 H/N 主要由 N 决定。**
> · **预判 PA 成立 ✓**：(2,6,6)（1 个 L=2 方向）⟹ **H/N = 0.1652 ± 0.0042**（|G| = 9.396×10⁴⁵，轨道 1.5×10¹⁴ – 3.4×10¹⁷）⟹ 确属「≤1 个退化方向」组。
> · **预判 PB 的设定被本轮否定（不是 GAP 失败）**：PB 要求 (6,6,6) ≈ (4,4,4) 的 0.1839，但既然 **H/N 随 N 强烈下降**，(6,6,6) 的 N=216 远大于 (4,4,4) 的 64 ⟹ 「同类 ⟹ 同值」的前提不成立。此外 **degree ≈ 216 已接近 GAP 的实用上限**（单次构型约 200 s）。
> · **形状仍有小的独立作用**（不完全由 N 决定）：固定 N=96 —— (2,4,12)（1 个退化方向）= 0.1338 vs **(4,4,6)（0 个）= 0.1484 ± 0.0053**，|Δ| = 0.0146 大于两者标准误合成的 95% 容差 0.0123 ⟹ **不相容**。
> · **⚠️ 一个工具缺陷（已修；旧值全部有效）**：(6,6,6) 一度报 `list index out of range`，真因是 **GAP 对超长整数折行**（|G| 有 223 位）⟹ 「ORDER」行没有第二个 token。已加 `SetPrintFormattingStatus("*stdout*", false)` 并把解析器改为「拼接标记之间的数字片段」。⚠️ 只有 |G| 超过约 78 位才会触发 ⟹ **第 48 轮与本轮的所有数值都不受影响**（最长的是 (2,6,6) 的 46 位）。
> · **判决**：0.25 **不是"渐近逼近"，而是被穿过一次** ⟹ 若框架要复现面积律，需要一个**钉住 N（或形状）的机制，目前没有**。这把该问题从「判死项」变成「**有解但无机制**」。
> ⚠️ **诚实边界**：全部 N ≤ 216，与宏观 N_c³ ≈ 6.1×10¹⁸² 差 ~180 个数量级 ⟹ **不得外推**；各处采样量不同（S = 40/30/24/20/12），标准误已随值给出；k 固定为 N/2；只扫了 (2,2,L)、(2,4,L) 两个系列加 5 个散点 ⟹ 「两条反向曲线」是**趋势**不是拟合出的律（**本轮刻意不做 N 的幂律拟合**）。
> 🔧 **下一步**：① 在 N = 32–48 之间加密（(4,6,4) / (6,6,4) 等），把跨点区间收窄；② 在 N = 96 上补第三个形状，量化「形状修正」的量级；③ (6,6,6) 单次 200 s ⟹ 性价比低，暂缓。
"""

EN_BLOCK = """
> **【v2.9 supplement (round 49: locating the crossing point of 0.25 — the **two opposite curves** of H/N versus N)】** The previous block left two falsifiable predictions. This round scans along (2,4,L) with GAP and **refines** that block's criterion.
>
> · **The crossing point is bracketed**: along (2,4,L) (one direction of length 2) — **(2,4,4) N=32: 0.2834** ([0.272,0.295], too high) ⟶ **(2,4,6) N=48: 0.2208** ([0.211,0.231], too low) ⟶ (2,4,8) N=64: 0.1802 ⟶ **(2,4,10) N=80: 0.1571** ⟶ **(2,4,12) N=96: 0.1338**. ⟹ **the crossing point of 0.25 lies in N ∈ (32, 48)**, and H/N is **monotone decreasing** within the group. ⚠️ **No lattice "hits" 0.25** in this round (no 95% interval contains it) ⟹ only a **bracket** can be given.
> · **Structural finding of this round: the two groups move in opposite directions with N.** With **≥ 2 directions of length 2**, H/N **rises**: 0.4335 (N=16) ⟶ 0.4510 (24) ⟶ **0.4802** (40) ⟶ **0.5041** (48) ⟶ **0.5170** (56) ⟶ 0.5307 (64); with **≤ 1 such direction** it **falls**: 0.2834 (32) ⟶ 0.2208 (48) ⟶ 0.1802 / 0.1839 (64) ⟶ **0.1652** (72, (2,6,6)) ⟶ 0.1571 (80) ⟶ 0.1338 / 0.1484 (96). ⟹ **the criterion of the previous block must be refined: the number of length-2 directions selects the group, while H/N inside a group is governed mainly by N.**
> · **Prediction PA holds ✓**: (2,6,6) (one length-2 direction) ⟹ **H/N = 0.1652 ± 0.0042** (|G| = 9.396×10⁴⁵, orbits 1.5×10¹⁴ – 3.4×10¹⁷) ⟹ it does belong to the "≤ 1 degenerate direction" group.
> · **Prediction PB is refuted by its own formulation (not by a GAP failure)**: PB asked for (6,6,6) ≈ 0.1839 as in (4,4,4), but since **H/N falls steeply with N**, the N=216 of (6,6,6) is far larger than the N=64 of (4,4,4) ⟹ the premise "same group ⟹ same value" fails. Moreover **degree ≈ 216 is close to GAP's practical limit** (≈200 s per single configuration).
> · **Shape still has a small independent effect** (H/N is not a function of N alone): at fixed N=96 — (2,4,12) (one degenerate direction) = 0.1338 vs **(4,4,6) (none) = 0.1484 ± 0.0053**; |Δ| = 0.0146 exceeds the combined 95% tolerance 0.0123 ⟹ **incompatible**.
> · **⚠️ A tooling defect (fixed; all earlier values remain valid)**: (6,6,6) once reported `list index out of range`; the real cause is that **GAP wraps very long integers** (|G| has 223 digits) ⟹ the "ORDER" line carries no second token. Fixed by adding `SetPrintFormattingStatus("*stdout*", false)` and by making the parser **concatenate the digit fragments between markers**. ⚠️ This only triggers above ~78 digits ⟹ **no value of round 48 or this round is affected** (the longest was 46 digits, for (2,6,6)).
> · **Verdict**: 0.25 is **not approached asymptotically but crossed once** ⟹ reproducing the area law would require a **mechanism pinning N (or the shape), which does not exist yet**. The problem thereby passes from "a dead end" to "**solvable but with no mechanism**".
> ⚠️ **Honest limits**: all N ≤ 216, some ~180 orders of magnitude below the macroscopic N_c³ ≈ 6.1×10¹⁸² ⟹ **do not extrapolate**; sample sizes differ across cases (S = 40/30/24/20/12) with standard errors reported; k is fixed at N/2; only the (2,2,L) and (2,4,L) series plus five scattered lattices were scanned ⟹ the "two opposite curves" are a **trend, not a fitted law** (**no power-law fit in N was attempted, by design**).
> 🔧 **Next**: ① densify between N = 32 and 48 ((4,6,4), (6,6,4), …) to narrow the bracket; ② add a third shape at N = 96 to quantify the size of the "shape correction"; ③ (6,6,6) costs ≈200 s per sample ⟹ poor value for money, deferred.
"""

sub_once(ZH, ZH_A, ZH_A + ZH_BLOCK, "ZH 插入第 49 轮块")
sub_once(EN, EN_A, EN_A + EN_BLOCK, "EN 插入第 49 轮块")

print()
print("=" * 70)
print("论文补丁：成功 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
print("=" * 70)
sys.exit(0 if N_FAIL[0] == 0 else 1)
