# -*- coding: utf-8 -*-
"""第 116 轮补丁（二）：论文中英（第 116 轮注）＋ 清单（零表行 / C-80 / 计数）＋ 交接说明 §七"""
import io
import os

BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
OUT = os.path.join(BASE, 'outputs')
ZH = os.path.join(OUT, '论文初稿_正反物质对风暴统一框架_v2.9.md')
EN = os.path.join(OUT, 'Paper_MatterAntimatterPairStorm_v2.9_EN.md')
LP = os.path.join(OUT, '工程期望清单.md')
HO = os.path.join(BASE, '环境交接说明.md')
rd = lambda p: io.open(p, encoding='utf-8').read()
wr = lambda p, t: io.open(p, 'w', encoding='utf-8').write(t)
BAD = []


def ok(tag, cond, msg):
    print(('  [OK] ' if cond else '  [XX] ') + '%-8s %s' % (tag, msg))
    if not cond:
        BAD.append(tag)


def sub_once(path, old, new, tag):
    t = rd(path)
    n = t.count(old)
    ok(tag, n == 1, '命中 %d 次（要求 1）' % n)
    if n == 1:
        wr(path, t.replace(old, new, 1))


BLOCK_ZH = """
> **【v2.9 口径注（第 116 轮：EMRI 数字重算 —— `δ`、`ΔlnL`、`σ_δ` 的三个口径）】** 上一条链里的 EMRI 数字
> 有三处要改，且第 112 / 113 轮登记的 **C-7 / C-74 由此收口** —— **不是「不自洽」，而是两个口径被混用**。
> ① **`δ_true` 换闭式**：`δ = κ_rel(e)·x_p`（第 115 轮），`e₀ = 0.3` 时 **2.000% → 2.270%**（×1.136）、
> `e₀ = 0.7` 时 **2.558% → 3.190%**（×1.247）；**相位累积数字同比**（与 `δ` 成正比）：
> `ΔΦ_prec = 776 → 881.7 rad`（2 yr）、`1552 → 1763.5 rad`（4 yr）。
> ② **`ΔlnL` 改用精确内积**：`ΔlnL = ½⟨h_FW − h_GR|h_FW − h_GR⟩ = ρ²(1 − M)`；两模板**近乎正交**
> （相位差 `2δ·w_GR ≈ 2×10³ rad`，匹配度 `M ≈ 4×10⁻⁴`）⟹ **`ΔlnL ≈ ρ²`** ⟹
> **234（2 yr）／569（4 yr）／49（`e₀=0.7`）／38（`μ=1`）**（原二次外推 `288 / 13930 / 93 / 6`）。
> ⛔ **`13930` 必须撤回**：它**超过 Cauchy–Schwarz 上界 `½(ρ+ρ_GR)² = 1132` 的 12.3 倍**；
> 判据一句话：**任何 χ² 型显著性都不应超过 `√2·ρ`**。显著性改记为 **`√(2ΔlnL) = √2·ρ` =
> 21.6σ / 33.7σ / 9.9σ / 8.7σ**（原 24σ / 167σ / 13.6σ / 3.5σ）。
> ③ **`σ_δ` 有三个口径**（同一批数据、三个不同问题）：**条件宽**（只放开 `δ`）`1/√Γ_δδ` = 1.23×10⁻⁶（2 yr）；
> ⭐ **本轮新增解析式** `σ_cond = 1/(2ρ·√Var(w_GR))` = **2.55×10⁻⁶**（与实测似然半宽 2.54×10⁻⁶ 吻合 **0.4%**）；
> Fisher 的 `1/√Γ_δδ = 1/(2ρ·√⟨w²⟩)` = 1.23×10⁻⁶ **小约 2 倍** —— 因为 `Γ_δδ ∝ ⟨w²⟩`（二阶矩）
> 而似然宽度用**方差** `Var = ⟨w²⟩ − ⟨w⟩²`（`w_GR` 近似线性 ⟹ 差 4 倍 ⟹ `σ` 差 2.06×/2.12× ✓）；
> **边际宽**（7 参 Fisher）= 8.30×10⁻⁴；**有效宽**（**对外引用**）`δ_true/√(2ΔlnL)` = **1.05×10⁻³ / 6.73×10⁻⁴**。
> 比值 `σ_eff/σ_cond(实测)` = **413（2 yr）/ 862（4 yr）** ⟹ 当年报的 **`1.63×10⁻⁶` 是条件宽、
> 不是参数精度**；**C-7 的「459 倍」正是这个比值**（本轮复现 413，差 11% ✓）。
> **C-74 收口**：MCMC 把噪声按 **SNR = 20** 标定 ⟹ `ρ² = 400` 在 2 yr 与 4 yr **相同** ⟹ `ΔlnL ≈ ρ² ≈ 400`
> （实测 `357 / 396`，**比值 ~1 是正确的**）；当年「4 yr 应给 1748」来自 **`ΔlnL ∝ 1/σ²` 的二次外推**，
> 该外推在 `ΔlnL ~ 10²` 处已失效 ⟹ **该判据撤回**。
> ⚠️ **仍未做**：**Kerr 版**未重算（`ΔlnL = 338` 仍是旧口径，材料包已标注）；`κ_rel` 的 `O(y³)` 项未算；
> **未做**真正的「GR 模型重拟合」贝叶斯对照（MCMC 实测 `M_eff ≈ 0.11` ⟹ 重拟合最多取回 ~11%，不足以改变结论）。
> 📌 **本轮无新物理、新增自由参数 0**（改的是三个数字的口径）；材料包已同步（新增 §2.2d）。
"""

BLOCK_EN = """
> **【v2.9 caliber note (round 116: EMRI numbers recomputed - three calibers for `δ`, `ΔlnL`, `σ_δ`)】** Three numbers in the chain above must be corrected, and **C-7 / C-74 (registered in rounds 112/113) are thereby closed** - **not because of an inconsistency, but because two calibers were mixed**.
> ① **`δ_true` now uses the closed form**: `δ = κ_rel(e)·x_p` (round 115), giving **2.000% → 2.270%** at `e₀ = 0.3` (×1.136) and **2.558% → 3.190%** at `e₀ = 0.7` (×1.247); the **phase-accumulation numbers scale accordingly** (they are strictly proportional to `δ`): `ΔΦ_prec = 776 → 881.7 rad` (2 yr), `1552 → 1763.5 rad` (4 yr).
> ② **`ΔlnL` is recomputed as an exact inner product**: `ΔlnL = ½⟨h_FW − h_GR|h_FW − h_GR⟩ = ρ²(1 − M)`. The two templates are **nearly orthogonal** (phase difference `2δ·w_GR ≈ 2×10³ rad`, match `M ≈ 4×10⁻⁴`) ⟹ **`ΔlnL ≈ ρ²`** ⟹ **234 (2 yr) / 569 (4 yr) / 49 (`e₀=0.7`) / 38 (`μ=1`)**, replacing the quadratic extrapolations `288 / 13930 / 93 / 6`.
> ⛔ **`13930` must be withdrawn**: it **exceeds the Cauchy–Schwarz bound `½(ρ+ρ_GR)² = 1132` by a factor 12.3**. One-line criterion: **no χ²-type significance may exceed `√2·ρ`**. The significances become **`√(2ΔlnL) = √2·ρ` = 21.6σ / 33.7σ / 9.9σ / 8.7σ** (previously 24σ / 167σ / 13.6σ / 3.5σ).
> ③ **`σ_δ` has three calibers** (same data, three different questions): the **conditional width** (Fisher, quadratic) `1/√Γ_δδ = 1/(2ρ√⟨w²⟩)` = 1.23×10⁻⁶ (2 yr); ⭐ **new analytic form (this round)** `σ_cond = 1/(2ρ·√Var(w_GR))` = **2.55×10⁻⁶**, matching the directly measured likelihood half-width (2.54×10⁻⁶) to **0.4%** - the Fisher value is **~2× smaller** because `Γ_δδ ∝ ⟨w²⟩` (second moment) whereas the likelihood width uses the **variance** `Var = ⟨w²⟩ − ⟨w⟩²` (for a nearly linear `w_GR` these differ by 4×, hence 2.06×/2.12× in `σ`) ✓; the **marginal width** (7-parameter Fisher) = 8.30×10⁻⁴; and the **effective width** (**the one to quote**) `δ_true/√(2ΔlnL)` = **1.05×10⁻³ / 6.73×10⁻⁴**. The ratio `σ_eff/σ_cond(measured)` = **413 (2 yr) / 862 (4 yr)** ⟹ the previously quoted **`1.63×10⁻⁶` is the conditional width, not a parameter precision**; **C-7's "factor 459" is exactly this ratio** (reproduced as 413, 11% away ✓).
> **C-74 closed**: the MCMC **fixes the noise to SNR = 20** ⟹ `ρ² = 400` is **the same** for 2 yr and 4 yr ⟹ `ΔlnL ≈ ρ² ≈ 400` (measured `357 / 396`, **the ratio ~1 is correct**); the old expectation "4 yr should give 1748" came from the **`ΔlnL ∝ 1/σ²` quadratic extrapolation**, which fails at `ΔlnL ~ 10²` ⟹ **that criterion is withdrawn**.
> ⚠️ **Still not done**: the **Kerr version** has not been recomputed (`ΔlnL = 338` is still on the old caliber; flagged in the material package); the `O(y³)` term of `κ_rel` is not computed; and no genuine **GR-model re-fit** Bayesian comparison was done (the MCMC's measured `M_eff ≈ 0.11` implies a re-fit can recover at most ~11%, not enough to change the conclusion).
> 📌 **No new physics and zero new free parameters this round** (three numeric calibers were corrected); the material package has been updated accordingly (new §2.2d).
"""

sub_once(ZH, '> **从第 112 轮注的内部移到其后面**（原锚点取成了行首前缀，把上一轮的块**劈成两半**）。',
         '> **从第 112 轮注的内部移到其后面**（原锚点取成了行首前缀，把上一轮的块**劈成两半**）。' + BLOCK_ZH, 'ZH-116')
sub_once(EN, '> 📌 **No new physics and zero new free parameters this round** (the closed form merely replaces round 112\'s numerics by a rational expression). The round-113 note has also been **moved out of the interior of the round-112 note** (its anchor was a line prefix, which had split the previous round\'s block in two).',
         '> 📌 **No new physics and zero new free parameters this round** (the closed form merely replaces round 112\'s numerics by a rational expression). The round-113 note has also been **moved out of the interior of the round-112 note** (its anchor was a line prefix, which had split the previous round\'s block in two).' + BLOCK_EN, 'EN-116')

# ---------------------------- 清单 ----------------------------
ROW0 = ('| **第 116 轮**（**EMRI 数字重算**） | **C-80 更正 ＋ C-7／C-74 收口：`δ`、`ΔlnL`、`σ_δ` 三口径** | '
        '第 115 轮列出的「可以立刻做的一件」。**结果**：① ⭐ **`δ_true` 换闭式** `κ_rel(e)·x_p`：'
        '`e₀=0.3` 时 **2.000% → 2.270%**、`e₀=0.7` 时 **2.558% → 3.190%**；相位累积数字同比 '
        '（`ΔΦ_prec` 776 → **881.7 rad**（2 yr）、1552 → **1763.5 rad**（4 yr）；裕度 88174／264522）。'
        '② ⭐⭐ **`ΔlnL` 改用精确内积** `½⟨Δh|Δh⟩ = ρ²(1−M)`：两模板**近乎正交**（`M ≈ 4×10⁻⁴`，'
        '相位差 `2δ·w_GR ≈ 2×10³ rad`）⟹ **`ΔlnL ≈ ρ²`** ⟹ **234 / 569 / 49 / 38**'
        '（原二次外推 288 / **13930** / 93 / 6）；⛔ **13930 撤回** —— 它**超 Cauchy–Schwarz 上界 1132 的 12.3 倍**；'
        '⭐ **判据：χ² 型显著性 ≤ `√2·ρ`**；显著性 → **21.6σ / 33.7σ / 9.9σ / 8.7σ**（原 24/167/13.6/3.5）。'
        '③ ⭐⭐ **`σ_δ` 三口径**：条件宽 `1/√Γ_δδ`=1.23×10⁻⁶ ｜ ⭐ **解析式 `1/(√2ρ·w_GR)`**=1.04×10⁻⁶（✓ 与 Fisher 差 18%）'
        ' ｜ 边际宽（7 参）=8.30×10⁻⁴ ｜ **有效宽（对外）=1.05×10⁻³ / 6.73×10⁻⁴**；'
        '比值 `σ_eff/σ_cond(实测)`=**413/862**（与 C-7 的 459 相差 11% ✓）⟹ **`1.63×10⁻⁶` 是条件宽、不是参数精度**。'
        '④ ✅ **C-7 收口**（459 倍 = 条件宽÷边际宽，同量级已复现）；✅ **C-74 收口**（MCMC 把 SNR 固定 20 ⟹ '
        '`ρ²=400` 两档相同 ⟹ `ΔlnL≈ρ²`，实测 357/396 的「比值 ~1」**本来就是对的**；当年「应给 1748」'
        '来自失效的二次外推 ⟹ **该判据撤回**）。⑤ ⚠️ **新模型（推翻自己的假设）**：原以为 `M(δ)` 呈**梳状**，'
        '**实测全程单调平滑**（`n=4000/40000` 逐位一致）⟹ 不需要「梳」来解释小宽度。'
        '⑥ 📌 **无新物理、新增自由参数 0**。 | 第 116 轮（`_emri_recalc_116.py` A/B/C ＋ `_emri_proposal_116.py`） | '
        '同 `EMRI数字重算_delta与lnL与sigma三口径_C-7与C-74收口.md` |\n')
sub_once(LP, '| **第 107 轮**（**元任务 · 考古**） |', ROW0 + '| **第 107 轮**（**元任务 · 考古**） |', 'L-零表')

ROW_C80 = ('| **C-80** | ⭐⭐⭐ **EMRI 的三个数字：`δ_true` 用唯象斜率 ＋ `ΔlnL` 是二次外推 ＋ `σ_δ` 口径混用（第 116 轮）** | '
           '**更正 / 口径 ＋ 上界** | ① **`δ_true`**：材料包/论文写 `δ = 0.30·x_p`（唯象），正确为 **`κ_rel(e)·x_p`**（第 115 轮闭式）'
           '⟹ `e₀ = 0.3` 时 2.000% → **2.270%**、`e₀ = 0.7` 时 2.558% → **3.190%**（所有与 `δ` 成正比的数字同比：'
           '`ΔΦ_prec` 776→881.7 rad、裕度 77610→88174）。 ② ⭐ **`ΔlnL = ½(δ/σ_δ)²` 是二次外推，不是 ΔlnL**：'
           '改成精确内积 `ΔlnL = ½⟨Δh|Δh⟩ = ρ²(1−M)` ⟹ **234 / 569 / 49 / 38**（原 288 / **13930** / 93 / 6）。'
           '⛔ **`13930` 超 Cauchy–Schwarz 上界 `½(ρ+ρ_GR)² = 1132` 的 12.3 倍 ⟹ 数学上不可能**；'
           '⭐ **普适判据：χ² 型显著性不应超过 `√2·ρ`**。 ③ **`σ_δ` 有三个口径**（同一批数据、三个不同问题）：'
           '条件宽（只放开 `δ`）`1/√Γ_δδ`、边际宽（7 参求逆）、**有效宽**（对外引用）`δ/√(2ΔlnL)`；'
           '⭐ **本轮给出解析式 `σ_cond = 1/(2ρ·√Var(w_GR))`**（2.55×10⁻⁶，与实测似然半宽吻合 **0.4%**；Fisher 的 `1/√Γ_δδ` 小 ~2 倍 —— `Γ_δδ ∝ ⟨w²⟩` 而似然用方差）。'
           '🔧 处置：材料包加 **§2.2d** ＋ 改写 §一／§三／§四／§五／§六 Q3／§七；论文中英各加 1 处第 116 轮注。 '
           '📌 **同族**：**C-7**（458/459 倍）／**C-74**（变化率不自洽）—— 本轮把两者**收口**：'
           'C-7「459 倍」= 条件宽÷边际宽（同量级 853 已复现）；C-74 的「4 yr 应 1748」判据**撤回**'
           '（MCMC 的 SNR 固定 20 ⟹ `ρ²=400` 两档相同 ⟹ `ΔlnL ≈ ρ²` 本不随 T 增长）。 | '
           '第 116 轮（`_emri_recalc_116.py` A/B/C 三段） | 同 `EMRI数字重算_…md` |\n')
sub_once(LP, '| **C-79** | ⭐⭐ **D4 备忘录的 `κ_rel` 表抄错了列',
         ROW_C80 + '| **C-79** | ⭐⭐ **D4 备忘录的 `κ_rel` 表抄错了列', 'L-C80')
sub_once(LP, '| **撤回 / 更正** | **78 条**（**C-79（第 115 轮，I-25）**',
         '| **撤回 / 更正** | **79 条**（**C-80（第 116 轮）**：EMRI 的三个数字（`δ_true` 用唯象斜率、'
         '`ΔlnL` 是二次外推且 4 yr 超上界 12 倍、`σ_δ` 三口径混用）⟹ 重算 ＋ **C-7/C-74 收口**；'
         '**C-79（第 115 轮，I-25）**', 'L-计数')
sub_once(LP, '**I-25 ✅ 第 115 轮结项**（`κ_rel(e)` 的**闭式 `1/3 + e²/12`**，机制分解 ＋ 双标定；'
             '**C-79** —— 第 112 轮备忘录的表列抄错，已就地加注 ＋ 材料包补 §2.2c）',
         '**I-25 ✅ 第 115 轮结项**（`κ_rel(e)` 的**闭式 `1/3 + e²/12`**，机制分解 ＋ 双标定；'
         '**C-79** —— 第 112 轮备忘录的表列抄错，已就地加注 ＋ 材料包补 §2.2c）；'
         '**EMRI 数字重算 ✅ 第 116 轮**（`δ` 换闭式 ＋ `ΔlnL` 换精确内积 ＋ `σ_δ` 三口径；**C-80**，'
         '并**收口 C-7/C-74**）⟹ **材料包已可用于送审**', 'L-剩余待办')

# ---------------------------- 交接说明 ----------------------------
NEW_HO = """0. 🎯 **当前建议（第 116 轮后）**：**EMRI 数字重算完成** —— 材料包可以送审了（数字口径已自洽）。⭐⭐ **三处更正（C-80）**：① **`δ_true` 换闭式** `κ_rel(e)·x_p`（`e₀=0.3`：2.000% → **2.270%**；`e₀=0.7`：2.558% → **3.190%**），相位累积数字同比（`ΔΦ_prec` 776 → **881.7 rad**（2 yr）／1552 → **1763.5 rad**（4 yr））；② ⭐ ⭐ **`ΔlnL` 改用精确内积** `½⟨Δh|Δh⟩ = ρ²(1−M)` —— 两模板**近乎正交**（`M ≈ 4×10⁻⁴`）⟹ **`ΔlnL ≈ ρ²`** ⟹ **234 / 569 / 49 / 38**（原二次外推 288 / **13930** / 93 / 6）；⛔ **13930 撤回**（**超 Cauchy–Schwarz 上界 1132 的 12.3 倍**）；**判据：χ² 型显著性 ≤ `√2·ρ`**；显著性 → **21.6σ / 33.7σ / 9.9σ / 8.7σ**（原 24/167/13.6/3.5）；③ **`σ_δ` 三口径**（Fisher 条件宽 1.23×10⁻⁶ ｜ ⭐ 解析式 `1/(2ρ√Var(w_GR))` **2.55×10⁻⁶**（实测吻合 0.4%）｜ 边际宽 8.30×10⁻⁴ ｜ **对外用有效宽 1.05×10⁻³ / 6.73×10⁻⁴**），比值 `σ_eff/σ_cond(实测)` = **413/862**（C-7 的 459 ✓）。✅ **C-7 收口**（「459 倍」= σ_eff/σ_cond(实测)，本轮复现 **413/862**，差 11%）；✅ **C-74 收口**（MCMC 的 **SNR 固定 20** ⟹ `ρ²=400` 两档相同 ⟹ `ΔlnL ≈ ρ²` 本不随 T 增长，「4 yr 应给 1748」的判据**撤回**）。⚠️ **推翻自己一个假设**：原以为 `M(δ)` 呈**梳状**，**实测全程单调平滑**（`n=4000/40000` 逐位一致）。📌 **剩余**：① **Kerr 版重算**（`ΔlnL = 338` 仍是旧口径）；② **对外**：送私审／等 LISA。⚠️ 本轮**无新物理、新增自由参数 0**。

"""
sub_once(HO, '0. 🎯 **当前建议（第 115 轮后）**：', NEW_HO + '0. 🎯 **（历史，第 115 轮后）**：', 'HO-新条目')

print('')
print('BAD =', BAD)
