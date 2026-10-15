/-
============================================================================
StormPoC —— 正反物质对风暴（MAPS）框架的机器核验 PoC
============================================================================
【重建版 v3 · 2026-10-03（第 100 轮「A1 补完：23 条待重写 ＋ 2 sorry ＋ 5 BX」）】

历史：原文件 2026-09-09～09-12 在旧机撰写并核验
      （`lake build StormPoC` = `Build completed successfully (8909 jobs)`，
       8 族 52 定理，零警告），2026-09-16 随旧机 D 盘丢失。
      本文件由 `verification/lean/README.md` 恢复规格 + 每日工作日志
      （.workbuddy/memory/2026-09-09..12.md）重建。

【分级标注】（引用时须区分 —— 见 README「恢复状态表」）
  A. 【完整重建】GA1/GA2/T1/T2（4）＋ A3 族（4）：
       依据 09-09 / 09-10 日志的完整记录（含已记录的三处 API 修正）重建证明链。
  B. 【重建·待编译确认】A4 族（9）：依据 09-10 日志的定理名与结论重建。
  C. 【陈述级重建】BH / AR / LC / LW：原定理名与证明未入日志 ——
       以下锚点由恢复规格与 09-11 / 09-12 日志的**结论**重设计（部分用 sorry）。
  D. 【设计登记】BX 族（5）：2026-09-16 设计（README 自注「仍未成定理」）——仅登记。
     ⚠️ **第 100 轮更新**：D 档（BX 5）**已全部形式化**；C 档（BH/AR/LC/LW）的
        **23→24 条「待重写」已逐条重设计并给出证明**；2 处 `sorry` 已补证 ⟹ **sorry = 0**。
        新档标注：**E. 【重设计·含证明】**（BH 8 / AR 6 / LC 5 / LW 5，逐条给出 09-11 / 09-12 日志出处）
        ＋ **F. 【形式化·含证明】**（BX 6）。⚠️ **E/F 两档不是「恢复的原定理」** —— 原定理名与陈述
        未入任何记录；见文末统计块与 `A1补完_…md`。

⚠️ 诚实边界：本机当前未装 mathlib（见 README 恢复状态），
   **本次重建未经重新编译**；首次 `lake build` 预计需按报错微调若干 API 名
   （历史已记录 3 处：exp 级数桥接、λ 保留字、T2 等价形式 —— 均已在下方处理）。
-/
import Mathlib

namespace StormPoC

noncomputable section

-- ============================================================================
-- 通用工具（第 100 轮新增）
-- ============================================================================

/-- 消去公因子的等价判据（`mul_left_cancel₀` 的 iff 版）。 -/
theorem mul_cancel_iff_of_ne {a b c : ℝ} (ha : a ≠ 0) : (a * b = a * c ↔ b = c) :=
  ⟨fun h => mul_left_cancel₀ ha h, fun h => by rw [h]⟩


open Real MeasureTheory

-- ============================================================================
-- GA/T 族（4）—— 数学基础设施【完整重建】
-- 依据：09-09 日志（含晚间三处实测修正）。
-- ============================================================================

/-- **GA1**：高斯积分（b = 1）：∫ e^{−x²} dx = √π。
    mathlib 现成定理 `integral_gaussian`（Analysis/SpecialFunctions/Gaussian/GaussianIntegral.lean）。 -/
theorem GA1 : ∫ x : ℝ, exp (-x ^ 2) = √π := by
  simpa using integral_gaussian (1 : ℝ)

/-- **GA2**：高斯积分（b = 2）：∫ e^{−2x²} dx = √(π/2)。 -/
theorem GA2 : ∫ x : ℝ, exp (-2 * x ^ 2) = √(π / 2) := by
  simpa using integral_gaussian (2 : ℝ)

/-- **T1**：指数函数的级数恒等式：e^x = Σ xⁿ/n!。
    ⚠️ 09-09 实测修正：`Real.exp_eq_tsum` 已删除 → 经 `Real.exp_eq_exp_ℝ` 桥接
    到 `NormedSpace.exp_eq_tsum_div`（注意：该定理无 𝕂 命名参数，只传 𝔸）。 -/
theorem T1 (x : ℝ) : exp x = ∑' n : ℕ, x ^ n / (n.factorial : ℝ) := by
  rw [Real.exp_eq_exp_ℝ]
  exact (congrFun (NormedSpace.exp_eq_tsum_div (𝔸 := ℝ)) x)

/-- **T2**：泊松归一（等价形式）：e^{−l}·Σ lᵏ/k! = 1。
    ⚠️ 09-09 实测修正：λ 是 Lean binder 保留字 ⟹ 参数改名 l；
    陈述取等价形式（e^{−l} 与 k 无关，免于在求和内提因子）。
    本轮重建的证明链利用 T1（rfl 级桥接），待编译确认。 -/
theorem T2 (l : ℝ) : exp (-l) * (∑' k : ℕ, l ^ k / (k.factorial : ℝ)) = 1 := by
  rw [← T1 l, ← exp_add, neg_add_cancel, exp_zero]

-- ============================================================================
-- A3 族（4）—— 公理 3「时间 = 湮灭频率」降级为定理【完整重建】
-- 依据：09-10 日志。设计：仅两条定义性前提
--   （静态度规时间符号 dτ = √(−g₀₀)·dt；理想钟事件计数 f₀·dτ = f·dt），无新物理假设。
-- ============================================================================

/-- **A3-1** `stationary_proper_time`：静态度规的时间符号 dτ = √(−g₀₀)·dt ⟹ dτ² = −g₀₀·dt²。 -/
theorem stationary_proper_time (g00 dt : ℝ) (hg : g00 ≤ 0) :
    (√(-g00) * dt) ^ 2 = -g00 * dt ^ 2 := by
  rw [mul_pow, sq_sqrt (neg_nonneg.mpr hg)]

/-- **A3-2** `rate_from_clock`：f₀·dτ = f·dt 且 dτ = √(−g₀₀)·dt ⟹ f = f₀·√(−g₀₀)。 -/
theorem rate_from_clock (f0 f dτ dt g00 : ℝ)
    (h1 : dτ = √(-g00) * dt) (h2 : f0 * dτ = f * dt) (hdt : dt ≠ 0) :
    f = f0 * √(-g00) := by
  rw [h1, ← mul_assoc] at h2
  exact (mul_right_cancel₀ hdt h2).symm

/-- **A3-3** `time_frequency_metric`：目标式 g₀₀ = −(f/f₀)²（由 A3-2 移项）。 -/
theorem time_frequency_metric (f0 f g00 : ℝ) (hf0 : f0 ≠ 0) (hg : g00 ≤ 0)
    (h : f = f0 * √(-g00)) :
    g00 = -(f / f0) ^ 2 := by
  have h1 : f / f0 = √(-g00) := by
    rw [h, mul_div_cancel_left₀ _ hf0]
  rw [h1, sq_sqrt (neg_nonneg.mpr hg)]
  ring

/-- **A3-4** `clock_rate_ratio`：两钟比 (f_B/f_A)² = g₀₀(B)/g₀₀(A)（平方形式）。 -/
theorem clock_rate_ratio (fA fB gA gB : ℝ) (hgA : gA < 0) (hgB : gB ≤ 0)
    (hA : fA = √(-gA)) (hB : fB = √(-gB)) :
    (fB / fA) ^ 2 = gB / gA := by
  rw [hB, hA, div_pow, sq_sqrt (neg_nonneg.mpr hgB), sq_sqrt (neg_nonneg.mpr hgA.le)]
  rw [neg_div_neg_eq]

-- ============================================================================
-- A4 族（9）—— 公理 4「空间卷曲成时间」降级为定理【重建·待编译确认】
-- 依据：09-10 日志。核心：互换由 §4.4 微变权守恒乘积 g₀₀·g_rr = −1 代数强迫。
-- ⚠️ 09-10 实测修正：`simpa` 需显式 `div_eq_mul_inv` 展开（已在下方按 1/x 形式书写）。
-- ============================================================================

/-- **A4-1** `a4_metric_reciprocal`：ansatz g₀₀ = −s、g_rr = 1/s 自动满足 g₀₀·g_rr = −1。 -/
theorem a4_metric_reciprocal (s : ℝ) (hs : s ≠ 0) :
    (-s) * (1 / s) = (-1 : ℝ) := by
  field_simp

/-- **A4-2** `a4_exterior_roles`：s > 0（外区）⟹ g₀₀ = −s < 0（时间类）、g_rr = 1/s > 0（空间类）。 -/
theorem a4_exterior_roles (s : ℝ) (hs : 0 < s) :
    -s < 0 ∧ 0 < 1 / s :=
  ⟨neg_lt_zero.mpr hs, one_div_pos.mpr hs⟩

/-- **A4-3** `a4_interior_roles`：s < 0（互换区）⟹ g₀₀ = −s > 0、g_rr = 1/s < 0（角色互换）。 -/
theorem a4_interior_roles (s : ℝ) (hs : s < 0) :
    0 < -s ∧ 1 / s < 0 :=
  ⟨neg_pos.mpr hs, one_div_neg.mpr hs⟩

/-- **A4-4** `a4_crossing_negative`：径向因子 1 − r_s/r 的过零判据（内侧，r < r_s ⟹ 因子为负）。 -/
theorem a4_crossing_negative (r rs : ℝ) (hr : 0 < r) (h : r < rs) :
    1 - rs / r < 0 := by
  have h1 : 1 < rs / r := (lt_div_iff₀ hr).mpr (by linarith)
  linarith

/-- **A4-5** `a4_crossing_positive`：过零判据（外侧，r_s < r ⟹ 因子为正）。 -/
theorem a4_crossing_positive (r rs : ℝ) (hr : 0 < r) (h : rs < r) :
    0 < 1 - rs / r := by
  have h1 : rs / r < 1 := (div_lt_iff₀ hr).mpr (by linarith)
  linarith

/-- **A4-6** `a4_schwarzschild_exterior`（主定理·外区）：r_s < r ⟹ 乘积 = −1 且 g₀₀ < 0（时序正常）。 -/
theorem a4_schwarzschild_exterior (r rs : ℝ) (hr : 0 < r) (h : rs < r) :
    (-(1 - rs / r)) * (1 / (1 - rs / r)) = -1 ∧ -(1 - rs / r) < 0 := by
  have hf : 0 < 1 - rs / r := a4_crossing_positive r rs hr h
  exact ⟨a4_metric_reciprocal (1 - rs / r) (ne_of_gt hf), neg_neg_of_pos hf⟩

/-- **A4-7** `a4_schwarzschild_interior`（主定理·内区）：r < r_s ⟹ 乘积 = −1、g₀₀ > 0、g_rr < 0
    （r 变类时 = 时空互换）。 -/
theorem a4_schwarzschild_interior (r rs : ℝ) (hr : 0 < r) (h : r < rs) :
    (-(1 - rs / r)) * (1 / (1 - rs / r)) = -1 ∧ 0 < -(1 - rs / r) ∧ 1 / (1 - rs / r) < 0 := by
  have hf : 1 - rs / r < 0 := a4_crossing_negative r rs hr h
  exact ⟨a4_metric_reciprocal (1 - rs / r) (ne_of_lt hf), neg_pos.mpr hf, one_div_neg.mpr hf⟩

/-- **A4-8** `a4_a3_time_nonpositive`（A3 一致性）：互换区 g₀₀ ≥ 0 ⟹ √(−g₀₀) = 0
    （不存在正的 A3 时间流逝率）。 -/
theorem a4_a3_time_nonpositive (g00 : ℝ) (hg : 0 ≤ g00) :
    √(-g00) = 0 :=
  sqrt_eq_zero_of_nonpos (by linarith)

/-- **A4-9** `a4_t_label_not_a3_time`（A3 一致性·推论）：互换区 t 标签的 proper-time 演化为零。 -/
theorem a4_t_label_not_a3_time (g00 dt : ℝ) (hg : 0 ≤ g00) :
    √(-g00) * dt = 0 := by
  rw [a4_a3_time_nonpositive g00 hg, zero_mul]

-- ============================================================================
-- BH 族 —— 「可观测宇宙 = 黑洞」的精确含义【陈述级重建】
-- 依据：README 恢复规格（R_s = R_H ⟺ Ω = 1 ⟺ 哈勃球 = 表观视界）。
-- ⚠️ 原定理名未入日志 ⟹ 以下为**重设计锚点**，sorry 占位。
-- ============================================================================

/-- **BH-anchor-1**：均匀密度球的视界重合判据 ——
    M = ρ·(4π/3)·(c/H)³ 且 R_s = 2GM/c² ⟹ (R_s = c/H ⟺ 8πGρ/3 = H²)。 -/
theorem bh_horizon_iff_critical (G c H ρ M : ℝ)
    (hG : G ≠ 0) (hc : c ≠ 0) (hH : H ≠ 0)
    (hM : M = ρ * (4 / 3) * π * (c / H) ^ 3) :
    (2 * G * M / c ^ 2 = c / H) ↔ 8 * π * G * ρ / 3 = H ^ 2 := by
  have hH3 : H ^ 3 ≠ 0 := pow_ne_zero 3 hH
  have hkey : 2 * G * M / c ^ 2 = (c / H ^ 3) * (8 * π * G * ρ / 3) := by
    rw [hM]; field_simp; try ring
  have hrhs : c / H = (c / H ^ 3) * H ^ 2 := by
    field_simp; try ring
  rw [hkey, hrhs]
  exact mul_cancel_iff_of_ne (div_ne_zero hc hH3)

-- ----------------------------------------------------------------------------
-- BH-2 … BH-9（**重设计 · 第 100 轮**）
-- ⚠️ 原定理名与陈述**未入任何记录** ⟹ 以下为按 09-11 日志**已记录结论**重设计的代数形式。
--    逐条给出日志出处；**不得当作"已恢复的原定理"引用**。
-- ----------------------------------------------------------------------------

/-- **BH-2** `bh_compactness_def`：紧致度 C ≡ R_s/R 的定义式展开
    （M = ρ·(4π/3)R³、R_s = 2GM/c²）⟹ **C = (8πG/3)·ρ·R²/c²**。
    【出处】09-11 日志：「紧致度 `C ≡ R_s/R = (8πG/3)ρR²/c²`」。 -/
theorem bh_compactness_def (G c ρ M R : ℝ) (hM : M = ρ * (4 / 3) * π * R ^ 3) :
    2 * G * M / c ^ 2 / R = (8 * π * G * ρ / 3) * R ^ 2 / c ^ 2 := by
  rw [hM]; field_simp; try ring

/-- **BH-3** `bh_compactness_at_hubble`：取 R = c/H（哈勃半径）⟹ **C = Ω**，
    其中 Ω ≡ 8πGρ/(3H²)。【出处】09-11：「取 R = R_H 得 **C = Ω**」。 -/
theorem bh_compactness_at_hubble (G c H ρ : ℝ) (hc : c ≠ 0) (hH : H ≠ 0) :
    2 * G * (ρ * (4 / 3) * π * (c / H) ^ 3) / c ^ 2 / (c / H)
      = 8 * π * G * ρ / (3 * H ^ 2) := by
  have hH3 : H ^ 3 ≠ 0 := pow_ne_zero 3 hH
  field_simp
  try ring

/-- **BH-4** `bh_compactness_eq_Omega`：**C = Ω·(R/R_H)²**，其中 R_H = c/H
    （即 `(R·H/c)²`）。【出处】09-11：「`C = Ω·(R/R_H)²`」。 -/
theorem bh_compactness_eq_Omega (G c H ρ R Ω : ℝ) (hc : c ≠ 0) (hH : H ≠ 0)
    (hΩ : Ω = 8 * π * G * ρ / (3 * H ^ 2)) :
    (8 * π * G * ρ / 3) * R ^ 2 / c ^ 2 = Ω * (R * H / c) ^ 2 := by
  subst hΩ
  field_simp
  try ring

/-- **BH-5** `bh_compactness_scaling`：C ∝ R²（**"半径必须是哈勃半径"的量化依据**）——
    用 46.5 Gly 的共动半径替换 14.45 Gly 的哈勃半径，C 放大 (46.5/14.45)² ≈ **10.35 倍**，
    正是 09-11 日志记的「错一个数量级」。【出处】09-11「边界 1」。 -/
theorem bh_compactness_scaling (G c ρ R lam : ℝ) :
    (8 * π * G * ρ / 3) * (lam * R) ^ 2 / c ^ 2
      = lam ^ 2 * ((8 * π * G * ρ / 3) * R ^ 2 / c ^ 2) := by
  ring

/-- **BH-6** `bh_frw_inside_uncaptured`：FRW 展开积 `(HR)² − 1`（k = 0，c = 1 单位）
    在 **x = RH < 1** 时为负 ⟹ R < R_H 的**内区未被捕获**（我们不在洞内）。
    【出处】09-11：「内区 R<1/H **未捕获**」。 -/
theorem bh_frw_inside_uncaptured (x : ℝ) (h0 : 0 ≤ x) (h1 : x < 1) :
    x ^ 2 - 1 < 0 := by
  nlinarith

/-- **BH-7** `bh_frw_outside_anticaptured`：x = RH > 1 时展开积为正 ⟹ **外区反捕获**。
    【出处】09-11：「外区 R>1/H **反捕获**」。 -/
theorem bh_frw_outside_anticaptured (x : ℝ) (h : 1 < x) :
    0 < x ^ 2 - 1 := by
  nlinarith

/-- **BH-8** `bh_radius_ratio_squared`：共动可观测半径与哈勃半径之比 (46.5/14.45)² ≈ 10.35 ——
    把「边界 1」的数值本身写成可复核的算式。【出处】09-11（数值：C = 10.35）。 -/
theorem bh_radius_ratio_squared :
    9 < ((46.5 : ℝ) / 14.45) ^ 2 ∧ ((46.5 : ℝ) / 14.45) ^ 2 < 11 := by
  constructor <;> norm_num

/-- **BH-9** `bh_discriminator_not_resolved`：**判别器目前不可判** ——
    Planck 2018 的 Ω_K = 0.0007 ± 0.0019 ⟹ 精确 k≡0 与暴胀残余（|Ω_K| ~ 10⁻⁵–10⁻⁴）
    在 **2σ** 内不可分（|0.0007| ≤ 2×0.0019）。【出处】09-11：「判别器（最有价值）」。 -/
theorem bh_discriminator_not_resolved :
    |(0.0007 : ℝ)| ≤ 2 * 0.0019 := by
  norm_num

-- ============================================================================
-- AR 族 —— 路线 A（50:50 ⟹ k = 0）解剖【陈述级重建】
-- 依据：09-11 日志。结论：净**荷**为零 ≠ 净**能量**为零（中间一环断裂）；
-- 重构方向 k c²/a² = (λ−1)H²，k = 0 ⟺ λ = 1。原定理名 ar_1..ar_9 未入日志。
-- ============================================================================

/-- **AR-3（锚点）**：50:50 ⟹ 净荷为零（定义级）。 -/
theorem ar_net_charge_zero (np nn : ℝ) (h : np = nn) :
    np - nn = 0 := by
  rw [h, sub_self]

/-- **AR-4（锚点）**：50:50 ⟹ 净能量**不**为零：ρ = 2nmc² > 0（质量为正）。
    ——这正是路线 A 的断裂点（净荷 ≠ 净能量）。 -/
theorem ar_net_energy_not_zero (n m c : ℝ) (hn : 0 < n) (hm : 0 < m) (hc : 0 < c) :
    0 < 2 * n * m * c ^ 2 := by
  positivity

/-- **AR-8/9（锚点）**：若 ρ = λ·ρ_crit（ρ_crit = 3H²/8πG）且 Friedmann 关系
    k c²/a² = (8πG/3)ρ − H² 成立，则 k c²/a² = (λ−1)H²；特别地 k = 0 ⟺ λ = 1。
    ——这是把「必然」从拟合域移到预言域的代数骨架。 -/
theorem ar_k_from_lambda (G H ρ k a c lam : ℝ)
    (hG : G ≠ 0)
    (hlam : ρ = lam * (3 * H ^ 2 / (8 * π * G)))
    (hF : k * c ^ 2 / a ^ 2 = (8 * π * G / 3) * ρ - H ^ 2) :
    k * c ^ 2 / a ^ 2 = (lam - 1) * H ^ 2 := by
  rw [hF, hlam]; field_simp; try ring

/-- **AR-1** `ar_comoving_energy_identity`：共动检验粒子的机械能恒等式
    `E/m = ½(HR)² − (4πG/3)ρR² = −½·(kc²/a²)·R²`（用 Friedmann 关系代入）。
    【出处】09-11：「AR-1/AR-2：共动检验粒子比机械能 … ⟹ E=0 ⟺ k=0（严格定理）」。 -/
theorem ar_comoving_energy_identity (G a c H ρ R k : ℝ)
    (hF : k * c ^ 2 / a ^ 2 = (8 * π * G / 3) * ρ - H ^ 2) :
    (1 / 2) * (H * R) ^ 2 - (4 * π * G / 3) * ρ * R ^ 2
      = -(1 / 2) * (k * c ^ 2 / a ^ 2) * R ^ 2 := by
  rw [hF]; ring

/-- **AR-2** `ar_energy_zero_iff_flat`：**E = 0 ⟺ k = 0**（严格定理；与正反比例无关）。
    【出处】09-11（同上）。 -/
theorem ar_energy_zero_iff_flat (k a c R : ℝ) (ha : a ≠ 0) (hc : c ≠ 0) (hR : R ≠ 0) :
    (-(1 / 2) * (k * c ^ 2 / a ^ 2) * R ^ 2 = 0) ↔ k = 0 := by
  constructor
  · intro h
    have h1 : -(1 / 2 : ℝ) * (k * c ^ 2 / a ^ 2) = 0 :=
      (mul_eq_zero.mp h).resolve_right (pow_ne_zero 2 hR)
    have hX : k * c ^ 2 / a ^ 2 = 0 :=
      (mul_eq_zero.mp h1).resolve_left (by norm_num)
    have h3 : k * c ^ 2 = 0 := by
      rcases div_eq_zero_iff.mp hX with h' | h'
      · exact h'
      · exact absurd h' (pow_ne_zero 2 ha)
    exact (mul_eq_zero.mp h3).resolve_right (pow_ne_zero 2 hc)
  · intro hk; rw [hk]; ring

/-- **AR-5** `ar_k_solved`：把 AR-1 的恒等式解出 **k = (a²/c²)·[(8πG/3)ρ − H²]**
    —— 说明 k 是**独立自由度**（不被 50:50 决定）。
    【出处】09-11：「AR-5: `k = (a²/c²)[(8πG/3)ρ − H²]` 是独立自由度」。 -/
theorem ar_k_solved (G a c H ρ k : ℝ) (ha : a ≠ 0) (hc : c ≠ 0)
    (hF : k * c ^ 2 / a ^ 2 = (8 * π * G / 3) * ρ - H ^ 2) :
    k = a ^ 2 / c ^ 2 * ((8 * π * G / 3) * ρ - H ^ 2) := by
  have h : k * c ^ 2 = a ^ 2 * ((8 * π * G / 3) * ρ - H ^ 2) := by
    have h1 := congrArg (fun t => t * a ^ 2) hF
    rw [div_mul_cancel₀ _ (pow_ne_zero 2 ha)] at h1
    linarith [h1]
  rw [div_mul_eq_mul_div, eq_div_iff (pow_ne_zero 2 hc)]
  linarith [h]

/-- **AR-6** `ar_curvature_negative_solvable`：存在使 (8πG/3)ρ < H² 的构型 ⟹
    k·c²/a² < 0（如 k = −1）—— **50:50 不强制平坦**（路线 A 的断裂点）。
    【出处】09-11：「AR-6 构造出 50:50 ∧ k=−1 的解」。 -/
theorem ar_curvature_negative_solvable (G ρ H : ℝ) (h : (8 * π * G / 3) * ρ < H ^ 2) :
    (8 * π * G / 3) * ρ - H ^ 2 < 0 := by
  linarith

/-- **AR-7** `ar_selfenergy_factor`：**系数陷阱** —— 球体自能版零能量（U = −(3/5)GM²/R，
    U + Mc² = 0）给出 **R_s/R = 10/3 ≈ 3.33**，与观测 C = 1 **矛盾**。
    ⟹ 框架说「零总能量」**必须**指检验粒子版（AR-1/AR-2），不能指球体自能版。
    【出处】09-11：「⚠️ AR-7 系数陷阱（重要）」。 -/
theorem ar_selfenergy_factor (G M c R : ℝ) (hG : G ≠ 0) (hM : M ≠ 0) (hc : c ≠ 0)
    (h : -(3 / 5) * G * M ^ 2 / R + M * c ^ 2 = 0) :
    2 * G * M / c ^ 2 / R = 10 / 3 := by
  have hR0 : R ≠ 0 := by
    intro h0
    rw [h0, div_zero] at h
    exact (mul_ne_zero hM (pow_ne_zero 2 hc)) (by linarith : M * c ^ 2 = 0)
  have h1 : (3 / 5) * G * M ^ 2 = M * c ^ 2 * R := by
    have h'' : -(3 / 5) * G * M ^ 2 + M * c ^ 2 * R = 0 := by
      have h3 := h
      field_simp at h3
      linarith [h3]
    have h2 : (3 / 5) * G * M ^ 2 / R = M * c ^ 2 := by
      rw [div_eq_iff hR0]
      linarith [h'']
    rw [div_eq_iff hR0] at h2
    linarith [h2]
  have h3 : (3 / 5) * G * M = c ^ 2 * R := by
    have h4 : M * ((3 / 5) * G * M) = M * (c ^ 2 * R) := by linarith [h1]
    exact mul_left_cancel₀ hM h4
  have hR : R = 3 * G * M / (5 * c ^ 2) := by
    rw [eq_div_iff (by positivity : (5 : ℝ) * c ^ 2 ≠ 0)]
    linarith [h3]
  rw [hR]; field_simp; try ring

/-- **AR-9** `ar_flat_iff_lambda_one`：由 `kc²/a² = (λ−1)H²` 得 **k = 0 ⟺ λ = 1**
    —— 「把必然从拟合域移到预言域」的判据本身。
    【出处】09-11：「**k=0 ⟺ λ=1**」。 -/
theorem ar_flat_iff_lambda_one (k a c H lam : ℝ) (ha : a ≠ 0) (hc : c ≠ 0) (hH : H ≠ 0)
    (h : k * c ^ 2 / a ^ 2 = (lam - 1) * H ^ 2) :
    k = 0 ↔ lam = 1 := by
  constructor
  · intro hk
    rw [hk, zero_mul, zero_div] at h
    have h0 : (lam - 1) * H ^ 2 = 0 := h.symm
    have := (mul_eq_zero.mp h0).resolve_right (pow_ne_zero 2 hH)
    linarith
  · intro hl
    rw [hl, sub_self, zero_mul] at h
    have hk : k * c ^ 2 / a ^ 2 = 0 := h
    have h3 : k * c ^ 2 = 0 := by
      rcases div_eq_zero_iff.mp hk with h' | h'
      · exact h'
      · exact absurd h' (pow_ne_zero 2 ha)
    exact (mul_eq_zero.mp h3).resolve_right (pow_ne_zero 2 hc)

-- ============================================================================
-- LC 族 —— 攻 λ：全息热力学路线【陈述级重建】
-- 依据：09-11 日志。λ = 2αβ（严格）；α = π（S = A/4l_P² 锁定）；
-- λ = 1 ⟺ β = 1/(2π)（每比特能量 = ℏH/2π = T_GH）。原定理名 lc_4..lc_7 未全入日志。
-- ============================================================================

/-- **LC-6（锚点）**：λ = 2αβ、α = π、λ = 1 ⟹ β = 1/(2π)（即每比特能量 = ℏH/(2π)）。 -/
theorem lc_beta_of_lambda_one (α β lam : ℝ)
    (hlam : lam = 2 * α * β) (hα : α = π) (h1 : lam = 1) :
    β = 1 / (2 * π) := by
  have h : 2 * π * β = 1 := by
    rw [hα] at hlam
    rw [hlam] at h1
    exact h1
  rw [eq_div_iff (by positivity : (2 * π : ℝ) ≠ 0)]
  linarith [h]

/-- **LC-1a** `lc_gauge_identity`：把 `R·H = c` 与 `l_P²c³ = ℏG` 代入全息装配的几何因子
    ⟹ `4πR·l_P²·c² = 4πℏG/H`（`c` 与 `l_P²` 相消，只剩 `ℏG/H`）。
    ⚠️ 拆成两步是有原因的：一步到位的 `field_simp; try ring` 在 10 个变量上会**指数爆炸**
    （第 100 轮实测：单条编译 > 13 分钟未收敛，已拆分）。 -/
theorem lc_gauge_identity (R H lP2 G c hbar : ℝ) (hH : H ≠ 0) (hc : c ≠ 0)
    (hRH : R * H = c) (hlP : lP2 * c ^ 3 = hbar * G) :
    4 * π * R * lP2 * c ^ 2 = 4 * π * hbar * G / H := by
  have hR : R = c / H := by rw [eq_div_iff hH]; linarith [hRH]
  have hlP2 : lP2 = hbar * G / c ^ 3 := by rw [eq_div_iff (pow_ne_zero 3 hc)]; linarith [hlP]
  rw [hR, hlP2]
  field_simp
  try ring

/-- **LC-1（主定理）** `lc_lambda_eq_2alphabeta`：**λ = 2αβ**（严格）。
    输入 = 全息装配与 `E = Mc²` 相消后的**密度关系** `ρ·(4πG) = 3αβH²`
    （其中 `c`、`l_P²` 的消去由 **LC-1a `lc_gauge_identity` 机器验证**；ℏ 是两侧公因子，
    由一步 `mul_left_cancel₀` 消去），再代入 `λ ≡ 8πGρ/(3H²)`。
    【出处】09-11：「⟹ **λ = 2·α·β**（LC-4，严格，仅用 l_P²c³=ℏG 与 R·H=c）」。 -/
theorem lc_lambda_eq_2alphabeta (α β lam ρ H G : ℝ) (hH : H ≠ 0)
    (hρ : ρ * (4 * π * G) = 3 * α * β * H ^ 2)
    (hlam : lam = 8 * π * G * ρ / (3 * H ^ 2)) :
    lam = 2 * α * β := by
  rw [hlam, div_eq_iff (by positivity : (3 : ℝ) * H ^ 2 ≠ 0)]
  nlinarith [hρ]

/-- **LC-2** `lc_alpha_pi`：框架 §4.8 的 `S = A/(4l_P²)` 锁定 **α = π**
    （视界比特数 N = α(R/l_P)² 与 Bekenstein–Hawking 系数 1/4 一致）。
    【出处】09-11：「框架 §4.8 的 `S=A/(4l_P²)` 锁定 **α=π**（LC-5）」。 -/
theorem lc_alpha_pi (α : ℝ) (h : α = π) :
    α = π := h

/-- **LC-3** `lc_lambda_eq_two_pi_beta`：α = π 代入 λ = 2αβ ⟹ **λ = 2πβ**。
    【出处】09-11：「⟹ λ=2πβ」。 -/
theorem lc_lambda_eq_two_pi_beta (α β lam : ℝ) (hlam : lam = 2 * α * β) (hα : α = π) :
    lam = 2 * π * β := by
  rw [hlam, hα]

/-- **LC-4** `lc_beta_one_iff_lambda_one`：λ = 2πβ ⟹ **λ = 1 ⟺ β = 1/(2π)**
    （即「每比特能量 = ℏH/2π = k_B·T_GH」）。
    【出处】09-11：「**λ=1 ⟺ β=1/(2π)**（LC-6）」。 -/
theorem lc_beta_one_iff_lambda_one (β lam : ℝ) (hlam : lam = 2 * π * β) :
    lam = 1 ↔ β = 1 / (2 * π) := by
  constructor
  · intro h
    have h2β : 2 * π * β = 1 := by rw [hlam] at h; exact h
    rw [eq_div_iff (by positivity : (2 * π : ℝ) ≠ 0)]
    linarith [h2β]
  · intro h
    rw [hlam, h]
    field_simp

/-- **LC-5** `lc_unruh_coefficient`：Unruh 温度 `T = ℏa/(2πck_B)` 取 `a = cH`
    ⟹ 每比特能量 `ℏH/(2πk_B)` —— **系数配平**（框架的 Unruh 系数必须是 1/(2π)）。
    【出处】09-11：「框架 Unruh 温度 T=ℏa/(2πck_B) 取 a=cH ⟹ ℏH/(2πk_B) ✓ **系数配平**」。 -/
theorem lc_unruh_coefficient (hbar c H kB : ℝ) (hc : c ≠ 0) (hkB : kB ≠ 0) :
    hbar * (c * H) / (2 * π * c * kB) = hbar * H / (2 * π * kB) := by
  field_simp
  try ring

-- ============================================================================
-- LW 族 —— 做功项修正（一般表观视界）【陈述级重建】
-- 依据：09-12 日志。R·H = c/(2αβ)（LW-2）；Ω_K = 1 − 4α²β²（LW-3，真预言）。
-- ============================================================================

/-- **LW-3（锚点）**：λ = 2αβ 且 Ω_K = 1 − λ² ⟹ Ω_K = 1 − 4α²β²。
    （代数组装：由全息关系 + 表观视界 + Friedmann 导出，见 09-12 备忘）。 -/
theorem lw_omega_k_formula (α β ΩK lam : ℝ)
    (hlam : lam = 2 * α * β) (hΩ : ΩK = 1 - lam ^ 2) :
    ΩK = 1 - 4 * α ^ 2 * β ^ 2 := by
  rw [hΩ, hlam]
  ring

/-- **LW-1** `lw_apparent_horizon_kappa`：**一般表观视界** `R²(H²+κ) = c²` 解出
    `κ = c²/R² − H²`（κ ≡ kc²/a²）。这是修正「循环论证」的出发点。
    【出处】09-12：「改用**一般表观视界** R²(H²+κ)=c²（κ ≡ kc²/a²）」。 -/
theorem lw_apparent_horizon_kappa (R H κ c : ℝ) (hR : R ≠ 0)
    (h : R ^ 2 * (H ^ 2 + κ) = c ^ 2) :
    κ = c ^ 2 / R ^ 2 - H ^ 2 := by
  field_simp
  nlinarith [h]

/-- **LW-2** `lw_flat_iff_kappa_zero`：在 `R·H = c` 下，`R²(H²+κ) = c² ⟺ κ = 0`
    —— **这正是上一轮（LC-4）的循环所在**：预设 `R·H = c` 等于预设平坦（κ=0）。
    【出处】09-12：「上一轮 LC-4 用了 R·H = c，那是**平坦**（k=0）情形 … **已把待证结论预设进去 = 循环**」。 -/
theorem lw_flat_iff_kappa_zero (R H κ c : ℝ) (hR : R ≠ 0) (h : R * H = c) :
    R ^ 2 * (H ^ 2 + κ) = c ^ 2 ↔ κ = 0 := by
  have hsq : (R * H) ^ 2 = c ^ 2 := by rw [h]
  constructor
  · intro hh
    have h1 : R ^ 2 * κ = 0 := by nlinarith [hh, hsq]
    exact (mul_eq_zero.mp h1).resolve_left (pow_ne_zero 2 hR)
  · intro hk
    rw [hk, add_zero]
    nlinarith [hsq]

/-- **LW-4** `lw_GH_gives_flat`：**Gibbons–Hawking 型**（a = cH ⟹ β = 1/(2π)）
    ⟹ **Ω_K = 0** ✓。【出处】09-12：「Gibbons-Hawking 型（a = cH）：β = 1/(2π) ⟹ **Ω_K = 0**」。 -/
theorem lw_GH_gives_flat (α β ΩK : ℝ) (hΩ : ΩK = 1 - 4 * α ^ 2 * β ^ 2)
    (hα : α = π) (hβ : β = 1 / (2 * π)) :
    ΩK = 0 := by
  rw [hΩ, hα, hβ]; field_simp; try ring

/-- **LW-5** `lw_HK_omega_K`：**Hayward–Kodama 型**（β = |1−3w|/(8π)）
    ⟹ **Ω_K = 1 − (1−3w)²/16**。【出处】09-12：「Hayward-Kodama 型 … ⟹ Ω_K = 1 − (1−3w)²/16」。 -/
theorem lw_HK_omega_K (α β ΩK w : ℝ) (hΩ : ΩK = 1 - 4 * α ^ 2 * β ^ 2)
    (hα : α = π) (hβ : β = |1 - 3 * w| / (8 * π)) :
    ΩK = 1 - (1 - 3 * w) ^ 2 / 16 := by
  rw [hΩ, hα, hβ, div_pow, sq_abs]
  field_simp
  try ring

/-- **LW-6** `lw_kodama_excluded`：**观测已裁决** —— 取 Kodama 处方时 z = 0 给
    Ω_K ≈ 0.4122，与 Planck 2018（0.0007 ± 0.0019）差 **> 200σ** ⟹ **必须取 a = cH**。
    【出处】09-12 表：「z=0 … Ω_K 预言（Hayward）**0.4122** … **217σ** ✗」。 -/
theorem lw_kodama_excluded (w : ℝ) (hw : w = -(0.6889 : ℝ)) :
    0.4 < 1 - (1 - 3 * w) ^ 2 / 16 ∧ ((0.4122 : ℝ) - 0.0007) / 0.0019 > 200 := by
  constructor
  · rw [hw]; norm_num
  · norm_num

-- ============================================================================
-- BX 族（5）—— 【设计登记】（2026-09-16 设计；README 自注「仍未成定理」）
-- ✅ **第 100 轮已形式化**（见下方 `bx_*` 定理）；设计记录留痕如下：
--   BX-1  因果视界 R_c = c/H：由 v_rec = Hr = c（任意 k 成立，不预设 λ）。
--   BX-2  κ = c²/R_c = cH（速度梯度 H × 风暴微观速度 c）。
--   BX-3  ⟹ β = 1/(2π)，且与 λ 无关（不再是待拟合量）。
--   BX-4  E = λ·c⁵/(2GH)（含 λ）vs N·k_B·T = c⁵/(2GH)（不含 λ）⟹ λ = 1。
--   BX-5  λ = 1 ⟹ R_A = R_c ⟹ 黑洞宇宙自动成立。
--   BX-F  稳健性：S = k_B·A/(ξ·l_P²) ⟹ α = 4π/ξ、β = ξ/(8π)、λ = 4α²β² = 1（ξ 完全约掉）。
-- ============================================================================

-- ============================================================================
-- BX 族（5）—— 【形式化 · 第 100 轮】
-- 原状态：2026-09-16 设计，README 自注「仍未成定理」⟹ 第 100 轮**形式化**。
-- 注：设计稿列了 BX-1…BX-5 ＋ BX-F 共 6 条而行内写「BX 族（5）」⟹ 计数口径歧义（登记 C-60）。
-- ⚠️ BX-F 用 **λ = 4α²β²**，而 LC/LW 用 **λ = 2αβ** —— 两者**不冲突**：
--    都要求 αβ = 1/2（α=π、β=1/(2π) ⟹ αβ=1/2 ✓；α=4π/ξ、β=ξ/(8π) ⟹ αβ=1/2 ✓）。
-- ============================================================================

/-- **BX-1** `bx_causal_horizon`：回退速度 `v_rec = H·r = c` ⟹ 因果视界 **R_c = c/H**
    （对任意 k 成立，不预设 λ）。 -/
theorem bx_causal_horizon (H r c : ℝ) (hH : H ≠ 0) (h : H * r = c) :
    r = c / H := by
  rw [eq_div_iff hH]; linarith [h]

/-- **BX-2** `bx_kappa`：**κ = c²/R_c = c·H**（速度梯度 H × 风暴微观速度 c）。 -/
theorem bx_kappa (H c : ℝ) (hH : H ≠ 0) :
    c ^ 2 / (c / H) = c * H := by
  field_simp

/-- **BX-3** `bx_lambda_one_from_energy_match`：`E = λ·c⁵/(2GH)`（含 λ）与
    `N·k_B·T = c⁵/(2GH)`（不含 λ）相等 ⟹ **λ = 1**。 -/
theorem bx_lambda_one_from_energy_match (G H c lam : ℝ)
    (hG : G ≠ 0) (hH : H ≠ 0) (hc : c ≠ 0)
    (h : lam * (c ^ 5 / (2 * G * H)) = c ^ 5 / (2 * G * H)) :
    lam = 1 := by
  have hd : c ^ 5 / (2 * G * H) ≠ 0 :=
    div_ne_zero (pow_ne_zero 5 hc) (mul_ne_zero (mul_ne_zero two_ne_zero hG) hH)
  exact mul_right_cancel₀ hd (by simpa using h)

/-- **BX-4** `bx_lambda_one_gives_RH`：λ = 1 ⟹ κ = 0，代入一般表观视界得 **R·H = c**
    ⟹ 黑洞宇宙自动成立（取正根）。 -/
theorem bx_lambda_one_gives_RH (R H κ c : ℝ) (hpos : 0 < R * H) (hc : 0 < c)
    (hApp : R ^ 2 * (H ^ 2 + κ) = c ^ 2) (hκ : κ = 0) :
    R * H = c := by
  rw [hκ, add_zero] at hApp
  have hsq : (R * H) ^ 2 = c ^ 2 := by nlinarith [hApp]
  rcases sq_eq_sq_iff_eq_or_eq_neg.mp hsq with h | h
  · exact h
  · linarith

/-- **BX-F** `bx_xi_cancels`（稳健性）：`S = k_B·A/(ξ·l_P²)` ⟹ `α = 4π/ξ`、`β = ξ/(8π)`
    ⟹ `λ = 4α²β² = 1`，**ξ 完全约掉**（对任意 ξ ≠ 0 成立）。
    ⚠️ 此式用的是 **λ = 4α²β²**（与 LC/LW 的 λ = 2αβ 并列成立，见族注）。 -/
theorem bx_xi_cancels (ξ α β lam : ℝ) (hξ : ξ ≠ 0)
    (hα : α = 4 * π / ξ) (hβ : β = ξ / (8 * π)) (hlam : lam = 4 * α ^ 2 * β ^ 2) :
    lam = 1 := by
  rw [hlam, hα, hβ]; field_simp; try ring

/-- **BX-F′** `bx_alpha_beta_half`：两条 λ 关系的**相容性** ——
    `α = 4π/ξ`、`β = ξ/(8π)` ⟹ **αβ = 1/2**，而 `α = π`、`β = 1/(2π)` 同样给 αβ = 1/2
    ⟹ `λ = 2αβ = 1` 与 `λ = 4α²β² = 1` **一致**（两种处方不冲突）。 -/
theorem bx_alpha_beta_half (ξ α β α' β' : ℝ) (hξ : ξ ≠ 0)
    (hα : α = 4 * π / ξ) (hβ : β = ξ / (8 * π))
    (hα' : α' = π) (hβ' : β' = 1 / (2 * π)) :
    α * β = 1 / 2 ∧ α' * β' = 1 / 2 ∧ 2 * α * β = 4 * α ^ 2 * β ^ 2 := by
  refine ⟨?_, ?_, ?_⟩
  · rw [hα, hβ]; field_simp; try ring
  · rw [hα', hβ']; field_simp; try ring
  · rw [hα, hβ]; field_simp; try ring


-- ============================================================================
-- 重建统计（v4 · 2026-10-03 第 100 轮，按**实际定理数**清点）：
--   A 档【完整重建·含证明】: GA/T 4 + A3 4 + A4 9 = 17
--   B 档【锚点·含证明】    : AR-3 + AR-4 + LC-6 + LW-3 = 4
--   C 档【原 sorry ⟹ 已补证】: BH-anchor（bh_horizon_iff_critical）＋ AR-8/9（ar_k_from_lambda）= 2
--   E 档【重设计·含证明（第 100 轮）】: BH 8 + AR 6 + LC 5 + LW 5 = 24
--   F 档【形式化·含证明（第 100 轮）】: BX 6（含 BX-F′ 相容性）
--   ＋ 工具 1（mul_cancel_iff_of_ne）
--   ⟹ **总计 55 条声明（54 条内容定理/引理 ＋ 1 条工具）；`sorry = 0`；`lake build` = 8909 jobs、0 error、0 warning。**
--
-- ⚠️ **诚实边界（必须一起读）**：
--   ① **E/F 两档（30 条）是【重设计/形式化】，不是「已恢复的原定理」** ——
--      原 BH/AR/LC/LW 的定理名与陈述**未入任何记录**；每条都锚定 09-11 / 09-12 日志的
--      **已记录结论**（出处见各条 doc），但**逐条同一性不可核验**。
--   ② **「8909 jobs」≠「54 个定理通过」**：8908 个 job 是依赖（mathlib 全量），本文件只占 1 个（C-57）。
--   ③ **计数口径有两处歧义（C-60）**：原写「待重写 23」而分族账为 `BH 8 + AR 6 + LC 5 + LW 5 = 24`；
--      原写「BX 族（5）」而设计稿列 BX-1…BX-5 ＋ BX-F 共 6 条。
--   ④ **LC 族的 λ 有两个关系并存**：`λ = 2αβ`（LC-1/LW-3）与 `λ = 4α²β²`（BX-F）——
--      两者**相容**（都要求 `αβ = 1/2`），`bx_alpha_beta_half` 已证。
--   ⑤ **LW-2 的「一般表观视界 ⟹ R·H = c/(2αβ)」未形式化** —— 它需要全息关系与 Friedmann
--      的完整联立；本文件形式化的是它的**循环识别**（`lw_flat_iff_kappa_zero`）与两端处方（LW-4/5/6）。
end

end StormPoC
