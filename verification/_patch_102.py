# -*- coding: utf-8 -*-
"""第 102 轮补丁（甲-3 结项 → 论文中英 + 台账 + 交接 + MEMORY）"""
import io
import os

ROOT = r"C:/Users/Administrator/Desktop/2026-08-20-21-43-34"
ZH = os.path.join(ROOT, "outputs/论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(ROOT, "outputs/Paper_MatterAntimatterPairStorm_v2.9_EN.md")
LIST = os.path.join(ROOT, "outputs/工程期望清单.md")
HAND = os.path.join(ROOT, "环境交接说明.md")
MEM = os.path.join(ROOT, ".workbuddy/memory/MEMORY.md")
OK, BAD = [], []


def sub(path, old, new, tag):
    s = io.open(path, encoding="utf-8").read()
    n = s.count(old)
    if n != 1:
        BAD.append("{} :: 命中 {}\n     锚点前 110 字: {}".format(tag, n, old[:110]))
        return
    io.open(path, "w", encoding="utf-8").write(s.replace(old, new))
    OK.append(tag)


# ============================================================ 中文稿
# ① C-64：v1.23 的「X 场 0.32」错误
sub(ZH,
    "**文献对照修正（v1.23，重要）**：h_c=0.328474(3) 是 **σ^z 场（Z 场/磁通凝聚版本）** 的临界值"
    "（对偶 2+1D 横向场 Ising，Trebst 2007/Blöte-Deng 2002/Wu 2012）；框架 **X 场版本（σ^x 场/电荷凝聚）"
    "应对标 h_xc≈0.32**（Trebst 2007/Vidal 2009，经 arXiv:1304.0780 核实）——v1.22 引用的"
    "「h_c≈0.328 同量级」系两版本混用，已修正；",
    "**文献对照（v1.23 原文已被第 102 轮更正 —— C-64）**：v1.23 曾写「`h_c=0.328474(3)` 是 **σ^z 场**的临界值，"
    "框架 **X 场版本应对标 `h_xc≈0.32`**」。**该更正本身是错的**，第 102 轮核实（arXiv 1309.7438 引 "
    "Trebst 2007／Vidal 2009／Tupitsyn 2010；arXiv 2603.14098）：**`h_x^c ≈ 0.328`（当 `h_z = 0`，即 **X 场**）；"
    "`h_x^c ≈ 0.34` 是「**自对偶线 `h_z = h_x`**」上的值 —— 那是**另一条线**。**X ↔ Z 加对偶格是模型的严格对偶"
    "（arXiv 2011.06611）⟹ 两个纯场版本同值**。且该模型正是 `H ≡ −Σ_v A_v − Σ_p B_p − h Σ_ℓ X_ℓ`（**环面**）"
    "—— 与本框架模型**逐项一致**。⟹ **X 场版本 = 0.328474，不是 0.32**；⚠️ 当年脚本 `_p03_torus.py` 的文档"
    "本来就写对了（「X 场版本…文献 h_c≈0.328 同约定」）；",
    "ZH-C64")

# ② C-65 / C-66：§5.7 的 J/K 段（第一处）
sub(ZH,
    "相变点 h_c = K/J = 1/3（与 h_xc≈0.32 交叉验证，详见 §10.2 #11）。",
    "相变点 h_c = K/J = 1/3（详见 §10.2 #11）。"
    "⚠️ **【第 102 轮口径注（C-65）】**：**相变不依赖 J** —— `A_v = Π_{e∋v}X_e` 是 X 型 ⟹ "
    "**`[A_v, Σ_e X_e] = 0` 是算符恒等式** ⟹ A_v 守恒 ⟹ 在 A_v = +1 扇区内 J 项退化为常数 `−J·V`。"
    "**数值验证（机器精度）**：J=1 vs J=3，E0 恰好平移 `(J−1)V`（3×3 差 18、3×4 差 24），而 "
    "**m 与能隙完全不变（Δm ~ 1e-12）**。⟹ 「J/K = 3 ⟹ h_c = K/J」这一步的「⟹」**无推导**；"
    "其 1.5% 的数值接近与 **C-62**（3D Ising `β_c` 轴混淆）**同族**（两个不同量的数值巧合）。",
    "ZH-C65-第一处")

# ③ C-65 / C-66：§10.2#11 的长段
sub(ZH,
    "预言相变点 **h_c = K/J = 1/3 ≈ 0.333** 与 h_xc≈0.32（差 4%）、σ^z 场 h_c=0.328（差 1.6%）、"
    "P0-3b κ_c∈[0.25,0.32] 交叉验证；",
    "预言相变点 **h_c = K/J = 1/3 ≈ 0.333**；"
    "⚠️ **【第 102 轮更正（C-64＋C-65＋C-66）】**：① 原句的「与 h_xc≈0.32（差 4%）、σ^z 场 h_c=0.328（差 1.6%）」"
    "**口径错误** —— 文献的 **X 场版本本身就是 0.328474**（见 §5.7 的 C-64 更正），故**唯一合法的比较是 "
    "`1/3 = 0.3333` vs `0.328474`，差 1.6%**；② **「h_c = K/J」缺机制**（相变与 J 无关，见 §5.7 的 C-65 注）；"
    "③ 原句把**框架约定**的 `P0-3b κ_c∈[0.25,0.32]` 与文献 `h_xc` 并列交叉验证 —— **两个约定（0.5 系数 vs "
    "J_A=J_B=1）差一个未给的换算因子**（当年脚本自注：只有**对称约定**才「直接对标文献」）⟹ **跨约定不可混比**（**C-66**）；"
    "④ **第 102 轮数值（A_v=+1 扇区，尺寸到 4×4）**：Binder 交叉给 `h_c = 0.31±0.02`，保真度磁化率给 0.3683，"
    "**两判据跨度 0.31–0.377** ⟹ **`1/3` 与 `0.3285` 都落在区间内，本法不能判别**（详见 §10.1b）；",
    "ZH-C65-10.2#11")

# ④ 第 102 轮块（插在 §10.1b 的甲-2 块之后）
sub(ZH,
    "详见《甲2结项_λc∞未定位_判据分辨率不足的量化》。",
    "详见《甲2结项_λc∞未定位_判据分辨率不足的量化》。\n\n"
    "**【第 102 轮（甲-3）toric code 相变点：数值不能判别 `1/3` 与 `0.3285`，而「h_c = K/J」缺机制】**"
    "（脚本 `_toric102.py`／`_toric102_run.py`／`_toric102_analyze.py`；**扇区 vs 全空间交叉验证** "
    "ΔE₀~1e-14、Δm~1e-13；3×3 的 m(h=0.35)=**0.376308** 与当年记录一致）——**四条**：\n"
    "① ⭐ **工程（可复用）**：`[A_v, H] = 0` ⟹ 在 **A_v = +1 扇区**工作，维数从 **2^(2L²) 降到 2^(n−V+1)**："
    "3×3 → 1024（压缩 2.6e2×）、3×4 → 8192（2.0e3×）、**4×4 → 131072（3.3e4×，全空间 4.3e9）** "
    "⟹ **4×4 首次可算**（31 个 h 点 204 s）；且 X 基下任意 X 算符的矩都是对角的 ⟹ **Binder 零额外成本**。\n"
    "② ⚠️ **结构性结论（C-65）**：**相变不依赖 J**（机器精度验证：J=1 vs 3，E0 恰平移 `(J−1)V`、m 与能隙不变）"
    "⟹ 「J/K = 3 ⟹ h_c = K/J」的「⟹」**无推导**。\n"
    "③ ⚠️ **数值结果（诚实负结论）**：**Binder 交叉**（L≥3 的三组一致）**0.2975／0.3213／≈0.317／≈0.310** ⟹ "
    "**0.31 ± 0.02**；**保真度磁化率**峰 **0.3683（4×4）**；**两判据跨度 0.31–0.377**。"
    "文献精确值 **0.328474** 与框架的 **0.3333** **都落在跨度内** ⟹ **本法不能判别 1.5% 的差**"
    "（判据系统分歧 > 待测效应，与甲-2 同族）。⚠️ 含 L=2 的 7 组配对给 0.35–0.47，是 L=2 太小所致，**不可用**。\n"
    "④ ⚠️ **一条判据作废**：**能隙 Δ=E1−E0 的极小点**在本模型**无信息** —— h=0 时 toric code 基态 **4 重简并** "
    "⟹ Δ(0)=0 ⟹ 极小恒落在区间边界（实测全在 h=0.20）。**选判据前先问它在极限处是否退化**"
    "（与甲-2 的「dw≡0 是恒等式」同族）。",
    "ZH-第102轮块")

# ============================================================ 英文稿
sub(EN,
    "  - **Literature-comparison correction (v1.23, important)**: h_c=0.328474(3) is the critical value of the "
    "**σ^z field (Z field / flux-condensation version)** (dual 2+1D transverse-field Ising, Trebst 2007/Blöte–Deng 2002/"
    "Wu et al. 2012); the framework's **X-field version (σ^x field / charge condensation) should be compared with "
    "h_xc≈0.32** (Trebst 2007/Vidal 2009, verified via arXiv:1304.0780) — the v1.22 citation \"h_c≈0.328 same order\" "
    "mixed the two versions, now corrected;",
    "  - **Literature comparison (the v1.23 text was itself wrong — corrected in round 102, C-64)**: v1.23 claimed that "
    "`h_c=0.328474(3)` is the **σ^z-field** value and that the framework's **X-field version should be compared with "
    "`h_xc≈0.32`**. **That correction was wrong.** Round 102 verification (arXiv 1309.7438 citing Trebst 2007 / "
    "Vidal 2009 / Tupitsyn 2010; arXiv 2603.14098): **`h_x^c ≈ 0.328` when `h_z = 0` (i.e. the X field)**, whereas "
    "**`h_x^c ≈ 0.34` belongs to the self-dual line `h_z = h_x`** — a different line. **X ↔ Z with the dual lattice is an "
    "exact duality of the model (arXiv 2011.06611) ⟹ the two pure-field versions have the same value.** Moreover the "
    "model is exactly `H ≡ −Σ_v A_v − Σ_p B_p − h Σ_ℓ X_ℓ` (**on the torus**), matching this framework's model "
    "term-by-term. ⟹ **the X-field version is 0.328474, not 0.32**; ⚠️ the original script `_p03_torus.py` had it right "
    "(its own docstring says \"X-field version … same convention as the literature h_c≈0.328\");",
    "EN-C64")

sub(EN,
    "transition point h_c = K/J = 1/3 (cross-validated against h_xc≈0.32; see §10.2 #11).",
    "transition point h_c = K/J = 1/3 (see §10.2 #11). "
    "⚠️**【Round-102 caliber note (C-65)】**: the transition **does not depend on J** — `A_v = Π_{e∋v}X_e` is X-type ⟹ "
    "**`[A_v, Σ_e X_e] = 0` is an operator identity** ⟹ A_v is conserved ⟹ inside the A_v = +1 sector the J term "
    "degenerates to the constant `−J·V`. **Machine-precision check**: J=1 vs J=3 leaves E0 shifted by exactly `(J−1)V` "
    "(18 for 3×3, 24 for 3×4) while **m and the gap are unchanged (Δm ~ 1e-12)**. ⟹ the arrow in 「J/K = 3 ⟹ h_c = K/J」 "
    "**has no derivation**; its 1.5% numerical proximity is the same family as **C-62** (3D Ising `β_c`, axis confusion).",
    "EN-C65-第一处")

sub(EN,
    "transition point h_c = K/J = 1/3 ≈ 0.333 (vs h_xc≈0.32, 4% apart; σ^z field 0.328, 1.6% apart; "
    "P0-3b κ_c∈[0.25,0.32], cross-validated ✓);",
    "transition point h_c = K/J = 1/3 ≈ 0.333; "
    "⚠️**【Round-102 corrections (C-64＋C-65＋C-66)】**: ① the original clause 「vs h_xc≈0.32 (4% apart); σ^z field 0.328 "
    "(1.6% apart)」 **mixes up calibers** — the literature's **X-field value is itself 0.328474** (see the C-64 correction "
    "in §5.7), so the **only legitimate comparison is `1/3 = 0.3333` vs `0.328474`, 1.6% apart**; ② **「h_c = K/J」 has no "
    "mechanism** (the transition is J-independent, see the C-65 note in §5.7); ③ the original clause placed the "
    "**framework-convention** `P0-3b κ_c∈[0.25,0.32]` alongside the literature `h_xc` for cross-validation — the two "
    "conventions (0.5 coefficient vs J_A=J_B=1) differ by an **unsupplied conversion factor** (the original script notes "
    "that only the **symmetric convention** can \"be compared with the literature directly\") ⟹ **cross-convention "
    "comparison is invalid (C-66)**; ④ **round-102 numerics (A_v = +1 sector, sizes up to 4×4)**: the Binder crossing gives "
    "`h_c = 0.31±0.02`, the fidelity susceptibility gives 0.3683, so the **two-criterion span is 0.31–0.377** ⟹ "
    "**both `1/3` and `0.3285` lie inside the span; this method cannot discriminate them** (see §10.1b);",
    "EN-C65-10.2#11")

sub(EN,
    "See the memo 《甲2结项_λc∞未定位_判据分辨率不足的量化》.",
    "See the memo 《甲2结项_λc∞未定位_判据分辨率不足的量化》.\n\n"
    "**【Round 102 (item 甲-3) toric-code transition: the numerics cannot discriminate `1/3` from `0.3285`, and "
    "「h_c = K/J」 has no mechanism】** (scripts `_toric102.py` / `_toric102_run.py` / `_toric102_analyze.py`; "
    "**sector-vs-full-space cross-check** ΔE₀~1e-14, Δm~1e-13; m(h=0.35)=**0.376308** on 3×3 matches the earlier record) — "
    "**four points**:\n"
    "① ⭐ **Engineering (reusable)**: `[A_v, H] = 0` ⟹ work in the **A_v = +1 sector**, reducing the dimension from "
    "**2^(2L²) to 2^(n−V+1)**: 3×3 → 1024 (2.6e2×), 3×4 → 8192 (2.0e3×), **4×4 → 131072 (3.3e4×; full space 4.3e9)** "
    "⟹ **4×4 becomes computable for the first time** (31 h-points in 204 s); and in the X basis every moment of X-operators "
    "is diagonal ⟹ **the Binder cumulant costs nothing extra**.\n"
    "② ⚠️ **Structural result (C-65)**: the transition **does not depend on J** (machine-precision: J = 1 vs 3 shifts E0 by "
    "exactly `(J−1)V`, leaving m and the gap unchanged) ⟹ the arrow in 「J/K = 3 ⟹ h_c = K/J」 **has no derivation**.\n"
    "③ ⚠️ **Numerical result (an honest negative)**: the **Binder crossing** (three L ≥ 3 pairs, mutually consistent) gives "
    "**0.2975 / 0.3213 / ≈0.317 / ≈0.310** ⟹ **0.31 ± 0.02**; the **fidelity-susceptibility** peak is **0.3683 (4×4)**; the "
    "**two-criterion span is 0.31–0.377**. The literature value **0.328474** and the framework's **0.3333** **both lie inside "
    "the span** ⟹ **this method cannot discriminate a 1.5% difference** (criterion systematics > the effect to be measured — "
    "same family as item 甲-2). ⚠️ The seven pairs involving L = 2 give 0.35–0.47 and are **unusable** (L = 2 too small).\n"
    "④ ⚠️ **One criterion retired**: the **gap minimum Δ = E1−E0** carries **no information** here — at h = 0 the toric-code "
    "ground state is **four-fold degenerate** ⟹ Δ(0) = 0 ⟹ the minimum always sits at the interval boundary (measured: all at "
    "h = 0.20). **Before choosing a criterion, ask whether it degenerates in the limit** (same family as item 甲-2's \"dw ≡ 0 "
    "is an identity\").",
    "EN-第102轮块")

# ============================================================ 台账
sub(LIST,
    "| **第 101 轮**（**甲-2 执行**） |",
    "| **第 102 轮**（**甲-3 执行**） | **C-64/65/66 更正** ＋ **甲-3 结项：toric code 相变点** | "
    "第 99 轮清点点选的「甲-3」：**2+1D toric code 相变点的精确值**（框架 `h_c = K/J = 1/3` vs 文献 `0.32/0.328`）。"
    "⭐ **结果**：① **数值不能判别** —— Binder 交叉（L≥3 三组一致）给 **0.31±0.02**、保真度磁化率给 **0.3683**，"
    "**跨度 0.31–0.377**，文献 **0.328474** 与框架 **0.3333** **都在区间内**（判据分歧 > 待判别效应）；"
    "② ⭐⭐ **结构性结论**：**相变不依赖 J**（`[A_v, ΣX_e] = 0` 是算符恒等式；J=1 vs 3 实测 E0 恰平移 `(J−1)V`、"
    "**m 与能隙不变 Δ~1e-12**）⟹ 「J/K = 3 ⟹ h_c = K/J」的「⟹」**无推导**（**C-65**）；"
    "③ ⚠️ **文献口径更正**：**X 场版本本身就是 0.328474**（不是 0.32），**0.34 属自对偶线**（**C-64**）；"
    "④ **跨约定不可混比**（**C-66**）。⭐ **工程**：`A_v = +1` 扇区把维数压 **3.3e4×** ⟹ **4×4 首次可算**。 |\n"
    "| **第 101 轮**（**甲-2 执行**） |",
    "LIST-§零-第102轮")

sub(LIST,
    "| **C-61** | ⭐⭐ **A1 的「`λ_c(∞) ∈ [0.21, 0.23]`」是过度解读（第 101 轮；甲-2）** |",
    "| **C-64** | ⭐⭐ **论文 v1.23 的「X 场 0.32 ／ σ^z 场 0.328」区分错误（第 102 轮；甲-3）** | **更正 / 口径** | "
    "论文 §5.7 标「重要」的 v1.23 段称「`h_c=0.328474(3)` 是 **σ^z 场**值，框架 **X 场版本应对标 `h_xc≈0.32`**」。"
    "**该更正本身是错的**：文献（arXiv 1309.7438 引 Trebst 2007／Vidal 2009／Tupitsyn 2010）给 "
    "**`h_x^c ≈ 0.328`（`h_z = 0`，即 X 场）**；**`h_x^c ≈ 0.34` 属「自对偶线 `h_z = h_x`」**（arXiv 2603.14098 的模型 "
    "`H = −ΣA_v − ΣB_p − hΣX_ℓ`（环面）**与框架逐项一致**）；**X↔Z 加对偶格是严格对偶（arXiv 2011.06611）⟹ 两纯场版本同值**。"
    "⚠️ 当年脚本 `_p03_torus.py` 的文档本就写对（「X 场版本…文献 h_c≈0.328」）。🔧 处置：**改回 X 场 = 0.328474**，"
    "0.34 归自对偶线。 | 第 102 轮（WebSearch 核实 + `_toric102_*`） | 同 `甲3结项_…md` |\n"
    "| **C-65** | ⭐⭐ **「h_c = K/J」缺机制（第 102 轮；甲-3）** | **机制缺失 / 更正** | "
    "`A_v = Π_{e∋v}X_e` 是 X 型 ⟹ **`[A_v, Σ_e X_e] = 0` 是算符恒等式** ⟹ A_v 守恒 ⟹ A_v=+1 扇区内 **J 项退化为常数** `−J·V` "
    "⟹ **相变不依赖 J**。**数值验证（机器精度）**：J=1 vs 3，E0 恰平移 `(J−1)V`（3×3 差 18、3×4 差 24）、**m 与能隙不变（Δm~1e-12）**。"
    "⟹ 「J/K = 3 ⟹ h_c = K/J」的「⟹」**无推导**；其与 0.3285 的 1.5% 接近属**两个不同量的数值巧合**（同族 **C-62**）。 "
    "| 第 102 轮 | 同 `甲3结项_…md` |\n"
    "| **C-66** | ⭐ **跨约定比较（第 102 轮；甲-3）** | **口径** | 论文 §5.7／§10.2#11 把**框架约定**（0.5 系数）的 "
    "`κ*≈0.20±0.01`／`m(h=0.32)≈0.84`／`κ_c≈0.25–0.32` 与文献 `h_xc` **并列交叉验证**，而两约定（0.5 系数 vs `J_A=J_B=1`）"
    "**差一个未给的换算因子**（`_p03_torus_final.py` 自注：只有**对称约定**才「直接对标文献 `h_c≈0.328`」）。"
    "🔧 处置：加「两个约定不可混比；对标文献一律用对称约定」注。 | 第 102 轮 | 同 `甲3结项_…md` |\n"
    "| **C-61** | ⭐⭐ **A1 的「`λ_c(∞) ∈ [0.21, 0.23]`」是过度解读（第 101 轮；甲-2）** |",
    "LIST-C64-66")

sub(LIST, "| **撤回 / 更正** | **62 条**", "| **撤回 / 更正** | **65 条**", "LIST-计数")

sub(LIST,
    "**~~甲-2 `λ_c(∞)` 精确定位~~ ✅ 第 101 轮结项（结论 = 未定位，方法学不足；C-61/62/63）**；",
    "**~~甲-2 `λ_c(∞)` 精确定位~~ ✅ 第 101 轮结项（结论 = 未定位，方法学不足；C-61/62/63）**；"
    "**~~甲-3 相变点精确值~~ ✅ 第 102 轮结项（结论 = 数值不能判别；且「h_c = K/J」缺机制；C-64/65/66）**；",
    "LIST-剩余待办-102")

# ============================================================ 交接说明
sub(HAND,
    "0. 🎯 **当前建议（第 101 轮后）**：**甲-2（`λ_c(∞)` 精确定位）已结项",
    "0. 🎯 **当前建议（第 102 轮后）**：**甲-3（toric code 相变点）已结项** —— 结论三条："
    "① **数值不能判别** `1/3` 与 `0.3285`（Binder 交叉 0.31±0.02 vs 保真度 0.3683，**跨度 0.31–0.377**，两值都在内）；"
    "② **相变不依赖 J**（`[A_v, ΣX_e]=0`，机器精度验证）⟹ 「h_c = K/J」**缺机制**；"
    "③ **文献口径更正**（X 场 = **0.328474**，0.34 属自对偶线）。"
    "📌 **剩余**：**甲-4**（麦克斯韦谱严格化）／**甲-5**（4π 相位方程）；乙类并轨 **O1–O5**；丙类 EMRI 材料包／私审准备包。"
    "⚠️ 要判别 `1/3` vs `0.3285`，须换 **QMC**（本模型无符号问题，文献值即 QMC 所得）或换判据（Wilson 环周长–面积律）。\n"
    "\n0. 🎯 **（历史，第 101 轮后）**：**甲-2（`λ_c(∞)` 精确定位）已结项",
    "HAND-§七")

sub(HAND,
    "**第 101 轮新增（甲-2：`λ_c(∞)` 精确定位 —— 结论 = 未定位，方法学不足）**：",
    "**第 102 轮新增（甲-3：toric code 相变点 —— 数值不能判别 ＋ 「h_c = K/J」缺机制）**："
    "脚本 `_toric102.py`（扇区求解器）／`_toric102_run.py`（验证+扫描）／`_toric102_analyze.py`（判据）。\n"
    "① ⭐ **工程**：`A_v = Π_{e∋v}X_e` ⟹ **`[A_v, H] = 0`** ⟹ **A_v = +1 扇区**把维数从 2^(2L²) 压到 2^(n−V+1)："
    "3×3→1024、3×4→8192、**4×4→131072（3.3e4×，全空间 4.3e9）** ⟹ **4×4 首次可算**；X 基下 X 算符的矩全对角 ⟹ Binder 零成本。\n"
    "② **验证**：扇区 vs 全空间（2×2／2×3／3×3，6 个 h 点）ΔE₀~1e-14、Δm~1e-13；3×3 的 m(h=0.35)=0.376308 与当年一致。\n"
    "③ ⚠️ **数值**：Binder 交叉（L≥3 三组）**0.2975／0.3213／≈0.317／≈0.310** ⟹ **0.31±0.02**；保真度磁化率 **0.3683**；"
    "**跨度 0.31–0.377** ⟹ 文献 **0.328474** 与框架 **0.3333** **都在内** ⟹ **不能判别**。"
    "⚠️ 含 L=2 的 7 组给 0.35–0.47，**不可用**。\n"
    "④ ⭐⭐ **结构性结论（C-65）**：**相变不依赖 J**（J=1 vs 3 实测 E0 恰平移 `(J−1)V`、m 与能隙不变 Δ~1e-12）"
    "⟹ 「J/K = 3 ⟹ h_c = K/J」**无推导**。\n"
    "⑤ ⚠️ **C-64**：文献核实（WebSearch）——模型 `H = −ΣA_v − ΣB_p − hΣX_ℓ`（**环面**）与框架**逐项一致**；"
    "**X 场版本 = 0.328474**（不是 0.32）；**0.34 属自对偶线 `h_z=h_x`**；**X↔Z 严格自对偶**。\n"
    "⑥ ⚠️ **C-66**：两个约定（0.5 系数 vs `J_A=J_B=1`）**差未给的换算因子** ⟹ 跨约定不可混比。\n"
    "⑦ ⚠️ **一条判据作废**：**能隙极小**在 h=0 处因 **4 重简并**（Δ(0)=0）而恒落边界 ⟹ 无信息。\n"
    "\n**第 101 轮新增（甲-2：`λ_c(∞)` 精确定位 —— 结论 = 未定位，方法学不足）**：",
    "HAND-第102轮段")

# ============================================================ MEMORY
sub(MEM, "**进度：101**", "**进度：102**", "MEM-进度")
sub(MEM,
    "（甲-1 ✅100、**甲-2 ✅101＝未定位**）。",
    "（甲-1 ✅100、甲-2 ✅101＝未定位、**甲-3 ✅102＝数值不能判别＋「h_c=K/J」缺机制**）。",
    "MEM-清点")
sub(MEM, "**C-6…C-63**", "**C-6…C-66**", "MEM-更正范围")
sub(MEM, "陷阱 1–98", "陷阱 1–99", "MEM-陷阱范围")
sub(MEM,
    "## 四、已判死",
    "48 ⭐⭐⭐ **「判据在极限处是否退化」先查，再选它**（102 轮 **甲-3**）：\n"
    "  ① **能隙极小点**在 toric code **无信息**（h=0 基态 **4 重简并** ⟹ Δ(0)=0 ⟹ 极小恒落区间边界）。\n"
    "  ② ⭐⭐ **相变不依赖 J**（`[A_v, ΣX_e] = 0` 是算符恒等式 ⟹ J 项退化为常数 `−J·V`；J=1 vs 3 实测 **m 与能隙不变 Δ~1e-12**）\n"
    "     ⟹ 「J/K = 3 ⟹ h_c = K/J」**无推导**（与铁律 47④ 同族：**比较前先问是不是同一个量/同一个轴**）。\n"
    "  ③ ⭐ **对称性可把维数降几个量级**：toric code 的 **A_v=+1 扇区**压 **3.3e4×** ⟹ **4×4 首次可算**\n"
    "     （全空间 2^{2L²}=4.3e9 → 扇区 131072）。📌 **动手前先找守恒量/好量子数。**\n"
    "  ④ ⚠️ **选判据前问「它在极限处退化吗」**；**算之前先问「N 个点是不是独立标度点」**（甲-2 的 2×2/3×2×2 同病）。\n"
    "\n## 四、已判死",
    "MEM-铁律48")

print("== OK ==")
for x in OK:
    print("  ", x)
print("== BAD ==")
for x in BAD:
    print("  ", x)
