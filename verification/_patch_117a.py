# -*- coding: utf-8 -*-
"""第 117 轮补丁（一）：论文中英
① 116 块内：两处更正指针（C-81）＋「仍未做」标完成
② 正文 §4.5b：Kerr 数值的更正指针
③ 追加第 117 轮块（中英同步）
"""
import io, os
BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
ZH = os.path.join(BASE, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md')
EN = os.path.join(BASE, 'outputs', 'Paper_MatterAntimatterPairStorm_v2.9_EN.md')
BAD = []

def sub_once(path, old, new, tag):
    t = io.open(path, encoding='utf-8').read()
    n = t.count(old)
    if n != 1:
        print('  [XX] %-22s 命中 %d 次 —— 拒绝' % (tag, n)); BAD.append(tag); return
    io.open(path, 'w', encoding='utf-8').write(t.replace(old, new, 1))
    print('  [OK] %-22s 已改' % tag)

def insert_after(path, pred, new_lines, tag):
    L = io.open(path, encoding='utf-8').read().split('\n')
    idx = [k for k, s in enumerate(L) if pred(s)]
    if len(idx) != 1:
        print('  [XX] %-22s 定位 %d 处 —— 拒绝' % (tag, len(idx))); BAD.append(tag); return
    L[idx[0] + 1:idx[0] + 1] = new_lines
    io.open(path, 'w', encoding='utf-8').write('\n'.join(L))
    print('  [OK] %-22s 已插入 %d 行（行 %d 后）' % (tag, len(new_lines), idx[0] + 1))

print('=== ZH 论文 ===')
# ① §4.5b 正文：v1.32 三个数的更正指针
sub_once(ZH, '（Kerr 下稳健）**；GR 数据对照',
         '（Kerr 下稳健）**〔**第 117 轮**：Kerr 版已重算 —— `ΔlnL = 399`（期望 = `ρ²`，上界 810 的 49%）；'
         '`σ_δ = 9.7×10⁻⁴` **撤回**（粗网格拟合伪影）；见该轮注〕**；GR 数据对照',
         'ZH-L269指针')
# ② 116 块：σ 解释更正（插一行）
insert_after(ZH,
    lambda s: '差 4 倍 ⟹ `σ` 差 2.06×/2.12× ✓）；' in s,
    ['> ⚠️ **【第 117 轮更正（C-81）】** 上一行的「实测似然半宽 / `⟨w²⟩` vs `Var`」解释**不成立**：`2.54×10⁻⁶` 是 **φ₀ 剖面宽**，'
     '真·似然半宽（φ₀ 固定）`= 1.23×10⁻⁶ = Fisher 值`（两者本应相等，「小约 2 倍」是误判）；原因是**条件 vs 剖面**。详见下条注 ②。'],
    'ZH-116块-σ解释')
# ③ 116 块：比值更正（插一行）
insert_after(ZH,
    lambda s: '（本轮复现 413，差 11% ✓）。' in s,
    ['> ⚠️ **【第 117 轮更正】** 上一段应读作：`413/862` = `σ_eff/σ_φ0剖面`；`σ_eff/σ_条件` = **853/1810**；'
     '**C-7 的 459** 本轮用 a–δ 管线自己的两个数精确复现 = **459.2**（`7.481×10⁻⁴ ÷ 1.629×10⁻⁶`，差 0.04%）'
     '—— 原「413，差 11%」是**跨案例**比较。详见下条注 ②。'],
    'ZH-116块-比值')
# ④ 「仍未做」标完成
sub_once(ZH, '**仍未做**：**Kerr 版**未重算（`ΔlnL = 338` 仍是旧口径，材料包已标注）；',
         '**仍未做**：~~**Kerr 版**未重算（`ΔlnL = 338` 仍是旧口径，材料包已标注）~~（**✅ 第 117 轮已完成**，见下条注）；',
         'ZH-仍未做')
# ⑤ 追加第 117 轮块
ZH117 = [
 '> **【v2.9 口径注（第 117 轮：Kerr 版 EMRI 重算 ＋ 上条注 ③ 的条件/剖面口径更正）】** 上条的「仍未做」项已完成；上条注 ③ 的「原因」更正（**C-81**），另登记 **C-82**。',
 '> ① **Kerr 版重算**（`_kerr_emri_bayes.py` 家族；圆轨道 `r₀ = 15 GM/c²`、`a = 0.9`、白噪声 SNR = 20、种子 7）：',
 '> **`δ_true` 2.000% → 2.222%**（`κ_rel(e=0) = 1/3` 解析，取代唯象 `0.30`）；**`ΔlnL` 338.4 → 399.2**',
 '> （精确内积 `½⟨Δh|Δh⟩` 的期望值 `= ρ²`；占 Cauchy–Schwarz 上界 `½(ρ+ρ_GR)² = 810` 的 49%；',
 '> 种子 7 实现值 385.9，噪声投影 ±28 —— **应报期望值**）；显著性 **26σ → 28.3σ**。',
 '> **`σ_δ` 三口径**：条件（φ₀ 固定）**7.90×10⁻⁷**（解析 `1/(2ρ√⟨ω²⟩)` = 8.03×10⁻⁷，差 1.6%）／',
 '> φ₀ 剖面 **1.588×10⁻⁶**（解析 `1/(2ρ√Var)` 吻合 0.0%）／有效（对外）**7.87×10⁻⁴**（= `δ/√(2ΔlnL)`）。',
 '> ⛔ **旧报 `σ_δ = 9.65×10⁻⁴` 撤回**：它是「平台 + 噪声」的**二次拟合伪影** —— 12 个种子重做，',
 '> `δ̂` 散布整个区间 `[0.0039, 0.058]`、`ΔlnL(粗网格)` 散布 13–97、**5/12 给 NaN**。',
 '> ⚠️ **结构性发现（Kerr 链与 a–δ 链共有）**：δ 似然是**针状**的 —— 针宽 ~10⁻⁶（= 条件宽），',
 '> 而**粗网格（400 点，步长 1.75×10⁻⁴）会整段错过针**（`δ̂` 随机）；旧结果能「精确恢复 `δ = 0.02`」',
 '> 是因为 **0.02 恰为格点**（`−0.01 + 171×0.07/399`）。细网格（±3×10⁻⁶）恢复到 ≲1σ_cond。',
 '> `dt/T_carrier = 23`（欠采样）对**积分类量**无碍（n = 3×10³ vs 3×10⁴：`ΔlnL` 差 1.7%、条件宽差 0.02%）；GR 对照无假阳性 ✓。',
 '> ② **上条注 ③ 的口径更正（C-81）**：`2.54×10⁻⁶` **不是**「实测似然半宽」，而是 **φ₀ 剖面宽**；',
 '> 真·似然半宽（φ₀ 固定）`= 1.23×10⁻⁶` **= Fisher `1/√Γ_δδ`**（两者本应相等 —— 上条注以为「Fisher 小 2 倍」是误判）。',
 '> 直接数值验证：数值 `max_φ₀` 半宽 **2.5416×10⁻⁶** vs 公式 `1/(2ρ√Var)` **2.5396×10⁻⁶**（差 0.08%）✓。',
 '> ⟹ **原因是条件 vs 剖面**（比值 2.065 ⟹ 等效 `|ρ(δ,φ₀)| = 0.875`，与 a–δ 联合 MCMC 实测 ≈0.85 一致），',
 '> **不是** `⟨w²⟩` vs `Var` 的矩之别。下游比值重记：`σ_eff/σ_cond` = **853 / 1810**（原 413/862 应读作 `σ_eff/σ_φ0剖面`）。',
 '> **C-7 的「459」本轮以 a–δ 管线自己的两个数**（`7.481×10⁻⁴ ÷ 1.629×10⁻⁶`）**精确复现为 459.2（差 0.04%）**',
 '> —— 原「413，差 11%」是跨案例比较。',
 '> ③ **旁注（C-82）**：`_emri_ad_mcmc.py` 总结句「`σ_δ(1D) = 1/(2wGR_T) ≈ 1e-5`」与其**自身** step① 实测',
 '> `s1 = 1.63×10⁻⁶`（= φ₀ 剖面口径）不符（该式缺 `ρ` 因子，给出 9.17×10⁻⁶，偏 5.6 倍；「虚高 ~100×」应为 ~600×）——脚本文本更正。',
 '> 📌 **本轮无新物理、新增自由参数 0**；材料包新增 §2.2e、§五行更新；清单 C-81/C-82。',
]
insert_after(ZH,
    lambda s: s.startswith('> 📌 **本轮无新物理、新增自由参数 0**（改的是三个数字的口径）'),
    ZH117, 'ZH-117块')

print('')
print('=== EN paper ===')
sub_once(EN, 'GR control shows no false positive.',
         'GR control shows no false positive **[round 117: the Kerr version has been recomputed — `ΔlnL = 399` (expectation = `ρ²`); '
         '`σ_δ = 9.7×10⁻⁴` withdrawn (coarse-grid fit artifact); see the round-117 note]**.',
         'EN-L264指针')
insert_after(EN,
    lambda s: 'hence 2.06×/2.12× in `σ`) ✓;' in s,
    ['> ⚠️ **【Round-117 correction (C-81)】** The explanation on the line above (measured likelihood half-width / `⟨w²⟩` vs `Var`) '
     '**does not hold**: `2.54×10⁻⁶` is the **φ₀-profiled width**, whereas the true (φ₀-fixed) likelihood half-width is '
     '`1.23×10⁻⁶ = the Fisher value` (they should be equal; the "~2× smaller" was a misreading). The cause is **conditional vs profiled**. See item ② of the note below.'],
    'EN-116块-σ解释')
sub_once(EN, """**C-7's "factor 459" is exactly this ratio** (reproduced as 413, 11% away ✓).""",
         """**C-7's "factor 459" is exactly this ratio** (reproduced as 413, 11% away ✓). """
         """[Round-117 correction: `413/862` should read `σ_eff/σ_prof`; `σ_eff/σ_cond` = **853/1810**; """
         """**C-7's "459" is exactly reproduced as 459.2** using the a-δ pipeline's own numbers (`7.481×10⁻⁴ ÷ 1.629×10⁻⁶`, 0.04% away) — """
         """the "413, 11% away" was a cross-case comparison. See item ② of the note below.]""",
         'EN-116块-比值')
sub_once(EN, '⚠️ **Still not done**: the **Kerr version** has not been recomputed (`ΔlnL = 338` is still on the old caliber; flagged in the material package);',
         '⚠️ **Still not done** ~~: the **Kerr version** has not been recomputed (`ΔlnL = 338` is still on the old caliber; flagged in the material package)~~ (**✅ done in round 117**, see the note below);',
         'EN-仍未做')
EN117 = [
 '> **【v2.9 caliber note (round 117: Kerr-version EMRI recomputation ＋ correction of the conditional/profiled caliber in note ③ above)】** The "still not done" item is now done; the cause given in note ③ is corrected (**C-81**), and **C-82** is registered.',
 '> ① **Kerr recomputation** (`_kerr_emri_bayes.py` family; circular orbit `r₀ = 15 GM/c²`, spin `a = 0.9`, white noise SNR = 20, seed 7):',
 '> **`δ_true` 2.000% → 2.222%** (`κ_rel(e=0) = 1/3` analytic, replacing the phenomenological `0.30`); **`ΔlnL` 338.4 → 399.2**',
 '> (the expectation of the exact inner product `½⟨Δh|Δh⟩`, `= ρ²`; 49% of the Cauchy–Schwarz bound `½(ρ+ρ_GR)² = 810`;',
 '> seed-7 realized value 385.9 with ±28 noise projection — **quote the expectation**); significance **26σ → 28.3σ**.',
 '> **`σ_δ` three calibers**: conditional (φ₀ fixed) **7.90×10⁻⁷** (analytic `1/(2ρ√⟨ω²⟩)` = 8.03×10⁻⁷, 1.6% apart) /',
 '> φ₀-profiled **1.588×10⁻⁶** (analytic `1/(2ρ√Var)` matching to 0.0%) / effective (to quote) **7.87×10⁻⁴** (`δ/√(2ΔlnL)`).',
 '> ⛔ **The previously quoted `σ_δ = 9.65×10⁻⁴` is withdrawn**: it is a "plateau + noise" **parabola-fit artifact** — over 12 seeds,',
 '> `δ̂` scatters across the whole interval `[0.0039, 0.058]`, `ΔlnL(coarse)` scatters over 13–97, and **5/12 return NaN**.',
 '> ⚠️ **Structural finding (shared by the Kerr and a-δ chains)**: the δ-likelihood is **needle-like** — needle width ~10⁻⁶ (= the conditional width),',
 '> whereas a **coarse grid (400 points, step 1.75×10⁻⁴) misses the needle entirely** (`δ̂` becomes random); the old "exact recovery of `δ = 0.02`"',
 '> worked only because **0.02 happened to be a grid point** (`−0.01 + 171×0.07/399`). A fine grid (±3×10⁻⁶) recovers to ≲1σ_cond.',
 '> `dt/T_carrier = 23` (undersampled) does **not** affect integral-type quantities (n = 3×10³ vs 3×10⁴: `ΔlnL` differs by 1.7%, conditional width by 0.02%); GR control shows no false positive ✓.',
 '> ② **Caliber correction to note ③ (C-81)**: `2.54×10⁻⁶` is **not** the "directly measured likelihood half-width" but the **φ₀-profiled width**;',
 '> the true (φ₀-fixed) likelihood half-width is `1.23×10⁻⁶` **= the Fisher `1/√Γ_δδ`** (they should be equal — the "Fisher is ~2× smaller" was a misreading).',
 '> Direct numerical check: numerical `max_φ₀` half-width **2.5416×10⁻⁶** vs the formula `1/(2ρ√Var)` **2.5396×10⁻⁶** (0.08% apart) ✓.',
 '> ⟹ The cause is **conditional vs profiled** (ratio 2.065 ⟹ equivalent `|ρ(δ,φ₀)| = 0.875`, consistent with the a-δ MCMC\'s ≈0.85),',
 '> **not** a `⟨w²⟩` vs `Var` moment difference. Downstream ratios: `σ_eff/σ_cond` = **853 / 1810** (413/862 should be read as `σ_eff/σ_prof`).',
 '> **C-7\'s "459" is reproduced exactly as 459.2** using the a-δ pipeline\'s own numbers (`7.481×10⁻⁴ ÷ 1.629×10⁻⁶`, 0.04% apart)',
 '> — the earlier "413, 11% away" was a cross-case comparison.',
 '> ③ **Side note (C-82)**: the a-δ script\'s concluding formula "`σ_δ(1D) = 1/(2wGR_T) ≈ 1e-5`" does not match its **own** step-① measurement',
 '> (`s1 = 1.63×10⁻⁶`, the φ₀-profiled caliber; the formula lacks a `ρ` factor and gives 9.17×10⁻⁶, 5.6× off) — a script-text correction.',
 '> 📌 **No new physics, zero new free parameters this round**; the material package gains §2.2e and an updated row in §五; checklist C-81/C-82.',
]
insert_after(EN,
    lambda s: s.startswith('> 📌 **No new physics and zero new free parameters this round** (three numeric calibers were corrected)'),
    EN117, 'EN-117块')

print('')
print('BAD =', BAD)
print('total bad =', len(BAD))
