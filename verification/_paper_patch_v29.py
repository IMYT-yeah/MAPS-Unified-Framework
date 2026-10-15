# -*- coding: utf-8 -*-
"""
论文 v2.8 -> v2.9 补丁（中英同步）
依据：outputs/论文增补_§8收口与新8.6视界热力学.md（第 17 轮）
      outputs/_paper_sec8_check.py（PA-1…PA-7，失败项：无）

用法：
  [TOOLCHAIN]/binaries/python/versions/3.13.12/python.exe outputs/_paper_patch_v29.py

设计原则：
  · 每个锚点必须**恰好命中一次**，否则报错退出（宁可不动，不可乱改）；
  · 不覆盖 v2.8 原文件（原文件已备份进 paper/history/），产出 *_v2.9* 新文件。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
FAIL = []


def rep(tag, text, old, new):
    """要求 old 恰好出现一次"""
    n = text.count(old)
    if n != 1:
        FAIL.append("%s：锚点命中 %d 次（应为 1）" % (tag, n))
        print("  [XX] %-34s 锚点命中 %d 次" % (tag, n))
        return text
    OUT.append(tag)
    print("  [OK] %-34s 替换完成" % tag)
    return text.replace(old, new, 1)


def insert_before(tag, lines, anchor_pred, block):
    """在首个满足 anchor_pred 的行之前插入 block（list of str）"""
    idx = [i for i, L in enumerate(lines) if anchor_pred(L)]
    if len(idx) != 1:
        FAIL.append("%s：定位命中 %d 处" % (tag, len(idx)))
        print("  [XX] %-34s 定位命中 %d 处" % (tag, len(idx)))
        return lines
    i = idx[0]
    OUT.append(tag)
    print("  [OK] %-34s 在第 %d 行前插入" % (tag, i + 1))
    return lines[:i] + block + lines[i:]


# ============================================================ 中文
ZH_SEC86 = """
### 8.6 视界热力学与平坦性

> **符号约定（重要）**：本节**不使用 λ** 表示密度比 —— `λ` 在本文 §5 中已被弦网哈密顿量的耦合常数
> 与临界值 λ_c ≈ 0.14 占用（§5 有 11 行含 λ，全文 26 行；§8 此前为 0 行）。此处统一使用标准符号
> **`Ω_tot ≡ ρ/ρ_crit`**，配套 `Ω_K = 1 − Ω_tot`。副作用是有益的：早前记录中的「λ = 1」即
> **`Ω_tot = 1`**，也就是平坦性本身。

#### 8.6.1 热力学面 = 平流停滞面

【推导】框架的微观组分以 c 传播。均匀膨胀中存在与 k 无关的精确关系 `v_rec = Hr`，故风暴成分无法向外回传的界面位于

$$R_c = c/H_0 = 14.4516\\ \\text{Gly}\\qquad (H_0 = 2.1927\\times10^{-18}\\,\\mathrm{s^{-1}})$$

该面表面引力取 `κ = c²/R_c = cH₀`，由 Unruh 温度给出

$$k_BT = \\frac{\\hbar H_0}{2\\pi} \\;\\Longrightarrow\\; T = 2.66558\\times10^{-30}\\ \\mathrm{K}$$

【假设 B5（准定理）】**热力学面取上述平流停滞面**。它不是 GR 的表观视界，也不是事件视界；判别见 8.6.5。

【诚实标注】该面**不是零表面**：`dR_c/dt = (1+q₀)c`，ΛCDM 的 q₀ = −0.5333 ⟹ 面以 **0.4667c** 外移，是 timelike 面；仅在纯 de Sitter（w = −1）极限下才是零表面。**因此不能表述为「观测者因果补丁的边界」。** 支持它的正确理由是 8.6.4 的时间尺分离。

#### 8.6.2 β = 1/(2π) 与 2π 的来源

【推导】每 Planck 面元 `l_P²` 的平均能量为 `k_BT = ℏH₀/(2π)`，即

$$\\beta \\equiv \\frac{\\text{每bit能量}}{k_BT_{GH}} = \\frac{1}{2\\pi}$$

**该系数与 Ω_tot 无关**；其来源可追溯至 F3 熵公式：由 `S = k_BA/(4l_P²)` 与 `dE = TdS` 直接得 `T = ℏc³/(8πGMk_B)`，太阳质量黑洞算得 6.1687×10⁻⁸ K，与标准 Hawking 温度偏差 < 10⁻⁹。**即 1/(2π) 源自 F3 中那个「4」**，不是从 QFT 借来的。

【诚实标注】`S = k_BA/(4l_P²)` 的系数 1/4 是 Bekenstein–Hawking 值（已由太阳黑洞 S/k_B = 1.0494×10⁷⁷ 独立核验），属标准物理输入，非本框架推导。

#### 8.6.3 等分账 ⟹ 平直 Friedmann 约束方程

【推导】在该面上写代数等分 `E = Nk_BT`，`N = A/(4l_P²) = πR_c²/l_P²`：

$$\\frac{4\\pi}{3}\\rho\\left(\\frac{c}{H_0}\\right)^3 c^2 \\;=\\; \\frac{\\pi(c/H_0)^2}{l_P^2}\\cdot\\frac{\\hbar H_0}{2\\pi}
\\;\\Longrightarrow\\; \\rho = \\frac{3H_0^2}{8\\pi G}$$

**输入全部为定义或框架既有结果，未预设 Friedmann。** 数值 `ρ = 8.5983×10⁻²⁷ kg/m³`。

⟹ **`Ω_tot = 1`，即 `Ω_K = 0`，即 k = 0**；且

```
M = c³/(2GH₀) = 9.20550×10⁵² kg ； R_S = 2GM/c² = R_c （精确，相对误差 <10⁻¹²）
```

故 **哈勃球 = 史瓦西半径**：「黑洞宇宙」在此获得机制说明，不再是数值巧合。

【诚实标注】上述 `M` 使用 Misner–Sharp 质量表达式，即**已在 FRW 内部**使用 GR ⟹ 严格地说是「在 FRW 内推出 k = 0」，不是从零推出引力。另 `ρ = 3H²/8πG` 只是**约束方程**；加速度方程与连续性方程仍缺（给定约束后二者等价）。

#### 8.6.4 为什么两端数的是同一批相干块（时间尺分离论证）

【前置结论】观测者端的相干块单位与统计端一致：**每 4l_P² 为 1 纳特，不是 1 比特**（由 Hawking 温度裁决：取 1 bit 会给 8.8995×10⁻⁸ K，偏差 +44.27%）。余下的问题是两端是否数同一批块。

【推导】块分解是**瞬时量**——由风暴当前的微观结构定义，不带历史。风暴以 `ν = 1/t_P = 1.85486×10⁴³ s⁻¹` 刷新，视界几何只以 H₀ 变化：

$$\\frac{\\nu}{H_0} = \\frac{R_c}{l_P} = 8.45924\\times10^{60},\\qquad H_0t_P = 1.18214\\times10^{-61}$$

一个哈勃时内每个面元被刷新 **8.46×10⁶⁰ 次**，故两种分解之差的上界为 `O(H₀t_P) = 1.18×10⁻⁶¹`。

⟹ **「同一批块」在 O(10⁻⁶¹) 精度上成立**。对照组：**若 ν → 0（冻结微观结构），失配为 O(1+q₀) = 0.47，即 20%~47% 的块数误差** —— A1 的 `ν ~ 1/t_P` 正是让这条链接成立的东西。

【诚实标注】这是**上界论证**而非构造性证明，依赖两个未独立证明的前提：(i) 两端计数都是瞬时的（若任一端是历史累积量则失效）；(ii) 刷新率为 1/t_P。

#### 8.6.5 为什么不是别的面（判别表）

由 8.6.3 的一般形式（面在半径 R 处）得 `Ω_tot = (R/R_c)²`（温度由 H₀ 定）或 `= R/R_c`（温度由该面表面引力定）：

| 候选面 | R/R_c | Ω_tot | Ω_K | 判决 |
|---|---|---|---|---|
| 表观视界 + Kodama 温度 | — | 0.59 | +0.41 | ❌ 偏离 **217σ** |
| 表观视界（λ_micro = 8π/3） | 0.3455 | 0.1194 | +0.881 | ❌ 差 O(1) |
| 事件视界（乙式） | 1.1473 | 1.1473 | −0.1473 | ❌ 78σ（Planck+BAO）/ **5.7σ**（Planck 单独） |
| 事件视界（甲式） | 1.1473 | 1.3163 | −0.3163 | ❌ 167σ / 15.1σ |
| **平流停滞面 c/H** | **1.0000** | **1.0000** | **0.0000** | ✅ |

（`R_EH/R_c = 1.147288`，即 16.5802 Gly；Ω_K 观测参照：Planck+BAO 0.0007±0.0019，Planck 单独 −0.044±0.018。）

⟹ 在自然候选面中 **`R_c = c/H` 是唯一幸存者**。

【诚实标注】该「唯一性」是用 Ω_K 观测量排除出来的 ⟹ **B5 带有数据成分，不是纯先验推导**。其先验支持来自涌现次序：`R_c = c/H` 只需 (c, H)，而 `R_A = c/(H√Ω_tot)` 需要 G —— G 在框架中是涌现量。

#### 8.6.6 关于 α–β 路的说明（为什么它不算证据）

早前记录中有 `Ω_tot = 4α²β²`（α = 4π/ξ 来自熵系数，β = ξ/(8π) 由第一定律反解）。核验表明：

$$4\\alpha^2\\beta^2 = 4\\cdot\\frac{16\\pi^2}{\\xi^2}\\cdot\\frac{\\xi^2}{64\\pi^2} = 1 \\quad \\text{对任意 }\\xi\\text{ 恒成立}$$

ξ = 1, 2, 3, 4, 4ln2, 8, 16 全部给出 `1.000000000000`。**该式看不见 R**，对任何面的选择都不敏感 ⟹ 既不能挑面，也**不能作为「Ω_tot = 1 已获验证」的独立证据**。早前记为「ξ-稳健性」的这一性质应降调为**一致性检查**：它不是稳健，它是重言式。

**有内容的只有一条**：等分账写在 `R_c = c/H` 上 ⟹ 解出 `ρ = 3H²/(8πG)`（8.6.3）。

**【诚实边界汇总】**

| 项 | 性质 |
|---|---|
| 平流停滞面 `R_c = c/H`、温度 `T = ℏH₀/(2πk_B)` | 【推导】 |
| `ρ = 3H²/(8πG)`、`Ω_tot = 1`、`R_S = R_c` | 【推导 + 数值】，但用了 Misner–Sharp ⟹ 在 FRW 内部成立 |
| 「同一批相干块」 | 上界论证，非构造性证明 |
| B5 的唯一性 | **含数据成分**（用 Ω_K 排除竞争者） |
| `α = π`、`β = 1/(2π)` 的数值 | 标准物理输入；框架原创性在于把它们用在 `R_c` 上 |
| 绝对密度量级 | **未解决**（继承宇宙学常数问题） |

""".splitlines()

ZH_ROW9 = ("| **S-C1** | **视界热力学联合检验：`wa = 0` 且 `Ω_K = 0`（§8.6）** —— 框架对空间曲率是硬预测：\n"
           "平流停滞面给出 `Ω_tot = 1`；若改用事件视界则 `Ω_K = −0.15 ~ −0.32`（已被 Planck+BAO 排除 78–167σ） | \n"
           "DESI DR2 / Euclid 2026-10（BAO+CMB 联合） | **框架硬预测，可与 wa 检验并行** |")

ZH_VER = """> **v2.9**：§8 宇宙学收口 + 新增 §8.6（视界热力学与平坦性，第 17 轮）——
- ❌ §8.2 修正：`f_space ≈ 0.014` → **`1/32.000`**（由观测量解出，非自由参数；旧值小 2.23 倍），并标注该机制**零预言力**；
- ❌ §8.3 修正：镜像支作暗物质主体**已被否证**（读法 A 低 5.31 倍、读法 B 高 3.82 倍，方向相反）⟹ 降为开放问题；
- ✅ §8.1 精度：`E_c = 1.01 meV` → **1.0181 meV**，并补 β 敏感度（β +1% ⟹ E_c 变 2.0 倍）；
- ✅ **新增 §8.6**：平流停滞面 / β = 1/(2π) 与 2π 的来源 / 等分账⟹平直 Friedmann 约束方程 /
  时间尺分离论证（残差 O(10⁻⁶¹)）/ 候选面判别表 / α–β 路降调为一致性检查；
- ⚠️ **符号**：宇宙学密度比一律用 **`Ω_tot ≡ ρ/ρ_crit`**（`λ` 已被 §5 弦网耦合占用）；
- ✅ §9 新增 S-C1：视界热力学的 `wa = 0 ∧ Ω_K = 0` 联合检验。
（核验脚本 `verification/_paper_sec8_check.py`，PA-1…PA-7 无失败项。）
"""

# ------------------------------------------------------------ 英文
EN_SEC86 = """
### 8.6 Horizon thermodynamics and flatness

> **Notation (important)**: this section does **not** use λ for the density ratio — `λ` is already taken in §5
> by the string-net Hamiltonian coupling and its critical value λ_c ≈ 0.14 (11 lines in §5, 26 in the whole
> paper; §8 had none). We use the standard symbol **`Ω_tot ≡ ρ/ρ_crit`**, with `Ω_K = 1 − Ω_tot`.
> A useful side effect: the earlier note "λ = 1" is revealed to be **`Ω_tot = 1`** — i.e. flatness itself.

#### 8.6.1 The thermodynamic surface = the advection-stall surface

【Derivation】 The microscopic constituents propagate at c. In uniform expansion the relation `v_rec = Hr` holds
exactly and independently of k, so the interface beyond which storm components cannot be advected back lies at

$$R_c = c/H_0 = 14.4516\\ \\text{Gly}\\qquad (H_0 = 2.1927\\times10^{-18}\\,\\mathrm{s^{-1}})$$

Taking `κ = c²/R_c = cH₀` and the Unruh temperature gives

$$k_BT = \\frac{\\hbar H_0}{2\\pi} \\;\\Longrightarrow\\; T = 2.66558\\times10^{-30}\\ \\mathrm{K}$$

【Assumption B5 (quasi-theorem)】 **The thermodynamic surface is the advection-stall surface above.** It is
neither the GR apparent horizon nor the event horizon; see 8.6.5 for the discrimination.

【Honest note】 The surface is **not a null surface**: `dR_c/dt = (1+q₀)c`, and q₀ = −0.5333 for ΛCDM ⟹ it
moves outward at **0.4667c** (timelike); it is null only in the pure de Sitter (w = −1) limit. **It must
therefore not be described as "the boundary of the observer's causal patch."** The correct supporting argument
is the timescale separation of 8.6.4.

#### 8.6.2 β = 1/(2π) and the origin of 2π

【Derivation】 The mean energy per Planck cell `l_P²` is `k_BT = ℏH₀/(2π)`, i.e.

$$\\beta \\equiv \\frac{\\text{energy per bit}}{k_BT_{GH}} = \\frac{1}{2\\pi}$$

**This coefficient is independent of Ω_tot.** Its origin traces back to the F3 entropy formula: combining
`S = k_BA/(4l_P²)` with `dE = TdS` gives `T = ℏc³/(8πGMk_B)`, which yields 6.1687×10⁻⁸ K for a solar-mass black
hole, within 10⁻⁹ of the standard Hawking temperature. **1/(2π) therefore originates in the "4" of F3** — it is
not borrowed from QFT.

【Honest note】 The coefficient 1/4 in `S = k_BA/(4l_P²)` is the Bekenstein–Hawking value (independently verified
by the solar-black-hole entropy S/k_B = 1.0494×10⁷⁷); it is standard-physics input, not a framework derivation.

#### 8.6.3 Equipartition ⟹ the flat Friedmann constraint

【Derivation】 Writing the algebraic equipartition `E = Nk_BT` on this surface, with `N = A/(4l_P²) = πR_c²/l_P²`:

$$\\frac{4\\pi}{3}\\rho\\left(\\frac{c}{H_0}\\right)^3 c^2 \\;=\\; \\frac{\\pi(c/H_0)^2}{l_P^2}\\cdot\\frac{\\hbar H_0}{2\\pi}
\\;\\Longrightarrow\\; \\rho = \\frac{3H_0^2}{8\\pi G}$$

**All inputs are definitions or previously derived framework results; Friedmann is not presupposed.**
Numerically `ρ = 8.5983×10⁻²⁷ kg/m³`.

⟹ **`Ω_tot = 1`, i.e. `Ω_K = 0`, i.e. k = 0**; and

```
M = c³/(2GH₀) = 9.20550×10⁵² kg ;  R_S = 2GM/c² = R_c (exact, relative error <10⁻¹²)
```

Hence **the Hubble sphere equals the Schwarzschild radius**: the "black-hole universe" acquires a mechanism here
and is no longer a numerical coincidence.

【Honest note】 `M` uses the Misner–Sharp mass expression, i.e. GR is used **inside** FRW ⟹ strictly this is
"deriving k = 0 within FRW", not deriving gravity from scratch. Also `ρ = 3H²/8πG` is only the **constraint
equation**; the acceleration and continuity equations are still missing (they are equivalent given the constraint).

#### 8.6.4 Why the two ends count the same coherent blocks (timescale separation)

【Preliminary】 The coherent-block unit is the same on both ends: **1 nat per 4l_P², not 1 bit** (decided by the
Hawking temperature: 1 bit would give 8.8995×10⁻⁸ K, a +44.27% deviation). The remaining question is whether the
two ends count the *same* blocks.

【Derivation】 The block decomposition is **instantaneous** — defined by the storm's current microstructure, not
by history. The storm refreshes at `ν = 1/t_P = 1.85486×10⁴³ s⁻¹` while the horizon geometry changes only at H₀:

$$\\frac{\\nu}{H_0} = \\frac{R_c}{l_P} = 8.45924\\times10^{60},\\qquad H_0t_P = 1.18214\\times10^{-61}$$

Each cell is refreshed **8.46×10⁶⁰ times** per Hubble time, so the difference between the two decompositions is
bounded by `O(H₀t_P) = 1.18×10⁻⁶¹`.

⟹ **The "same blocks" statement holds to O(10⁻⁶¹).** Control case: **if ν → 0 (frozen microstructure), the
mismatch is O(1+q₀) = 0.47, i.e. a 20%–47% error in the block count** — the A1 postulate `ν ~ 1/t_P` is
precisely what makes this link work.

【Honest note】 This is a **bounding argument**, not a constructive proof; it rests on two unproven premises:
(i) both counts are instantaneous (it fails if either end accumulates history); (ii) the refresh rate is 1/t_P.

#### 8.6.5 Why not another surface (discrimination table)

From the general form of 8.6.3 (surface at radius R): `Ω_tot = (R/R_c)²` (temperature set by H₀) or `= R/R_c`
(temperature set by that surface's gravity):

| Candidate surface | R/R_c | Ω_tot | Ω_K | Verdict |
|---|---|---|---|---|
| Apparent horizon + Kodama temperature | — | 0.59 | +0.41 | ❌ **217σ** off |
| Apparent horizon (λ_micro = 8π/3) | 0.3455 | 0.1194 | +0.881 | ❌ O(1) off |
| Event horizon (variant B) | 1.1473 | 1.1473 | −0.1473 | ❌ 78σ (Planck+BAO) / **5.7σ** (Planck alone) |
| Event horizon (variant A) | 1.1473 | 1.3163 | −0.3163 | ❌ 167σ / 15.1σ |
| **Advection-stall surface c/H** | **1.0000** | **1.0000** | **0.0000** | ✅ |

(`R_EH/R_c = 1.147288`, i.e. 16.5802 Gly; Ω_K references: Planck+BAO 0.0007±0.0019, Planck alone −0.044±0.018.)

⟹ Among natural candidates, **`R_c = c/H` is the only survivor**.

【Honest note】 This "uniqueness" was obtained by excluding competitors with Ω_K observations ⟹ **B5 carries a
data component and is not a purely a-priori derivation.** Its a-priori support comes from the emergence ordering:
`R_c = c/H` needs only (c, H), whereas `R_A = c/(H√Ω_tot)` needs G — and G is an emergent quantity in this framework.

#### 8.6.6 On the α–β route (why it is not evidence)

An earlier note records `Ω_tot = 4α²β²` (α = 4π/ξ from the entropy coefficient, β = ξ/(8π) from inverting the
first law). Verification shows:

$$4\\alpha^2\\beta^2 = 4\\cdot\\frac{16\\pi^2}{\\xi^2}\\cdot\\frac{\\xi^2}{64\\pi^2} = 1 \\quad \\text{identically for any }\\xi$$

ξ = 1, 2, 3, 4, 4ln2, 8, 16 all give `1.000000000000`. **This expression does not see R**, so it is insensitive to
the choice of surface ⟹ it can neither select a surface nor serve as independent evidence that "Ω_tot = 1 has been
verified". The property earlier recorded as "ξ-robustness" should be downgraded to a **consistency check**: it is
not robustness, it is a tautology.

**Only one route carries content**: equipartition written on `R_c = c/H` ⟹ `ρ = 3H²/(8πG)` (8.6.3).

**【Honest-boundary summary】**

| Item | Status |
|---|---|
| Advection-stall surface `R_c = c/H`, temperature `T = ℏH₀/(2πk_B)` | 【Derivation】 |
| `ρ = 3H²/8πG`, `Ω_tot = 1`, `R_S = R_c` | 【Derivation + numerical】, but uses Misner–Sharp ⟹ valid inside FRW |
| "Same coherent blocks" | bounding argument, not a constructive proof |
| Uniqueness of B5 | **contains a data component** (Ω_K excludes competitors) |
| Values `α = π`, `β = 1/(2π)` | standard-physics input; the framework's originality is applying them on `R_c` |
| Absolute density scale | **unsolved** (the cosmological-constant problem is inherited) |

""".splitlines()

EN_ROW9 = ("| **S-C1** | **Joint horizon-thermodynamics test: `wa = 0` and `Ω_K = 0` (§8.6)** — the framework makes a hard\n"
           "prediction for spatial curvature: the advection-stall surface gives `Ω_tot = 1`, while the event horizon would\n"
           "give `Ω_K = −0.15 … −0.32` (already excluded by Planck+BAO at 78–167σ) | DESI DR2 / Euclid 2026-10 (BAO+CMB) |\n"
           "**hard framework prediction; runs in parallel with the wa test** |")

EN_VER = """> **v2.9**: §8 cosmology cleanup + new §8.6 (horizon thermodynamics and flatness, round 17) —
- ❌ §8.2 corrected: `f_space ≈ 0.014` → **`1/32.000`** (solved from observations, not a free parameter; the old
  value is 2.23× too small), and the mechanism is flagged as **zero predictive power**;
- ❌ §8.3 corrected: mirror-branch dark matter as the dominant component is **falsified** (reading A 5.31× too
  low, reading B 3.82× too high, opposite directions) ⟹ downgraded to an open problem;
- ✅ §8.1 precision: `E_c = 1.01 meV` → **1.0181 meV**, plus the β sensitivity (β +1% ⟹ E_c changes by 2.0×);
- ✅ **New §8.6**: advection-stall surface / β = 1/(2π) and the origin of 2π / equipartition ⟹ flat Friedmann
  constraint / timescale-separation argument (residual O(10⁻⁶¹)) / candidate-surface discrimination table /
  the α–β route downgraded to a consistency check;
- ⚠️ **Notation**: the cosmological density ratio is always **`Ω_tot ≡ ρ/ρ_crit`** (`λ` is taken by the §5
  string-net coupling);
- ✅ §9 new S-C1: joint `wa = 0 ∧ Ω_K = 0` test.
(Verification script `verification/_paper_sec8_check.py`, PA-1…PA-7, no failures.)
"""


# ============================================================ 执行
def patch(path, sec86, row9, ver, anchors):
    print("\n" + "=" * 72)
    print(path)
    print("=" * 72)
    txt = open(path, encoding="utf-8").read()
    for tag, old, new in anchors:
        txt = rep(tag, txt, old, new)
    lines = txt.splitlines()

    # 1) 在 §9 之前插入 §8.6：定位 "## 9 ..." 前最后一个 "---"
    def is_h9(L):
        return L.startswith("## 9 ")

    idx = [i for i, L in enumerate(lines) if is_h9(L)]
    if len(idx) != 1:
        FAIL.append("%s：§9 定位命中 %d 处" % (path, len(idx)))
        return None
    j = idx[0] - 1
    while j >= 0 and lines[j].strip() != "---":
        j -= 1
    if j < 0:
        FAIL.append("%s：未找到 §9 前的分隔线" % path)
        return None
    lines = lines[:j] + sec86 + lines[j:]
    OUT.append("%s: 插入 §8.6" % os.path.basename(path))
    print("  [OK] %-34s 在 §9 前插入 §8.6（%d 行）" % ("§8.6", len(sec86)))

    # 2) §9 表格末尾追加一行：在 "## 10" 之前的最后一个非空行之后
    idx10 = [i for i, L in enumerate(lines) if L.startswith("## 10 ")]
    if len(idx10) != 1:
        FAIL.append("%s：§10 定位命中 %d 处" % (path, len(idx10)))
        return None
    k = idx10[0] - 1
    while k >= 0 and lines[k].strip() == "":
        k -= 1
    lines = lines[:k + 1] + row9.splitlines() + lines[k + 1:]
    OUT.append("%s: §9 追加 S-C1" % os.path.basename(path))
    print("  [OK] %-34s §9 表格追加 S-C1" % ("S-C1",))

    # 3) 附录 C：在 "## 参考文献/References" 之前追加 v2.9 版本说明
    idxref = [i for i, L in enumerate(lines) if L.startswith("## ")]
    # 取最后一个标题（参考文献）
    last = [i for i, L in enumerate(lines) if L.startswith("## ")]
    i_ref = None
    for i in last:
        if "参考文献" in lines[i] or "References" in lines[i]:
            i_ref = i
    if i_ref is None:
        FAIL.append("%s：未找到参考文献标题" % path)
        return None
    lines = lines[:i_ref] + ver.splitlines() + [""] + lines[i_ref:]
    OUT.append("%s: 附录C v2.9" % os.path.basename(path))
    print("  [OK] %-34s 附录 C 追加 v2.9 条目" % ("v2.9 note",))

    return "\n".join(lines) + "\n"


jobs = [
    (os.path.join(HERE, "论文初稿_正反物质对风暴统一框架_v2.8.md"),
     os.path.join(HERE, "论文初稿_正反物质对风暴统一框架_v2.9.md"),
     ZH_SEC86, ZH_ROW9, ZH_VER,
     [("§8.1 E_c 精度+敏感度",
       "**截断能标**【推导】：概率归一化 ε_A(E_c) = 1 ⟹ E_c = M_Pl·ε₀^{1/β} = **1.01 meV**——与暗能量特征能标 2.3 meV 同量级（(E_c)⁴ 差 27 倍，O(1) 系数待定）。",
       "**截断能标**【推导】：概率归一化 ε_A(E_c) = 1 ⟹ E_c = M_Pl·ε₀^{1/β} = **1.0181 meV**——与暗能量特征能标 2.3 meV 同量级（(E_c)⁴ 差 27 倍，O(1) 系数待定）。\n"
       "\n"
       "**【v2.9 诚实标注】E_c 对 β 极度敏感**：β 增加 1% ⟹ E_c = 2.068 meV（放大 2.0 倍）；增加 2% ⟹ 4.14 meV（4.1 倍）。\n"
       "因此 **meV 量级**是稳健结论，而 **E_c 的数值**完全绑定于 β = 0.615 的取值——这与 §8.4 中 Ω_Λ 定量路失败同源（`dlnΩ_Λ/dβ = 465`）。"),
      ("§8.2 f_space 修正",
       "（与观测 2.3×10⁻²⁷ 差 ~70 倍——**【待验证】**需 f_space ≈ 0.014 或机制修正）",
       "（与观测 2.3×10⁻²⁷ 差 ~70 倍）。\n"
       "\n"
       "**【v2.9 修正】**在全息稀释 `ε_eff = (l_P/R_c)² = 1.3975×10⁻¹²²` 下，`⟨f_space⟩` 不是待定 knob，而是**被观测量唯一解出**：\n"
       "`⟨f_space⟩ = ρ_DM/(ε_eff·ρ_P) = 2.2511×10⁻²⁷ / 7.2037×10⁻²⁶ = 0.031250073 = **1/32.000**`\n"
       "（早期「≈0.014」为不同 ε_eff 取值下的结果，小了 2.23 倍，作废）。\n"
       "**【诚实标注】**该式目前是**拟合式而非预言**：把它读成空洞体积分数则与实测 50–80% 差 16–26 倍；\n"
       "读成速率抑制因子则缺一条无自由参数的抑制律 `f_space(ρ_m)`（四种自洽律给出四个答案）。\n"
       "⟹ **暗物质的定量解释在本框架中仍是空白**。"),
      ("§8.3 镜像支否证",
       "- 镜像支投影：κ_extra ~ Ω_mirror/Ω_total ≈ 0.5（引力跨支共享，电磁/强/弱被支界过滤）⟹ ρ ~ 4×10⁻²⁷ kg/m³ **与观测同量级**——**暗物质主体可能来自镜像支引力投影**【待验证】；",
       "- 镜像支投影：**【v2.9 修正：已被否证】** 原判「与观测同量级」不成立。50:50 的两种自然读法给出方向相反的偏差：\n"
       "  读法 A（只有引力跨支共享、其余被支界过滤 ⟹ Ω_dm = Ω_b = 0.0493）**低 5.31 倍**；\n"
       "  读法 B（沿用 κ_extra ≈ Ω_mirror/Ω_total ≈ 0.5 ⟹ Ω_dm ~ 1）**高 3.82 倍**——两者均远超误差棒。\n"
       "  ⟹ 镜像支作暗物质**主体**的判断撤回，本节降为开放问题；void-CPT-κ 异常仅在该机制被重建后才成立。"),
      ]),
    (os.path.join(HERE, "Paper_MatterAntimatterPairStorm_v2.8_EN.md"),
     os.path.join(HERE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md"),
     EN_SEC86, EN_ROW9, EN_VER,
     [("§8.1 E_c precision + sensitivity",
       "**Cutoff scale**【Derivation】: probability normalization ε_A(E_c) = 1 ⟹ E_c = M_Pl·ε₀^{1/β} = **1.01 meV** — of the same order as the dark-energy characteristic scale 2.3 meV ((E_c)⁴ differs by a factor 27; O(1) coefficient undetermined).",
       "**Cutoff scale**【Derivation】: probability normalization ε_A(E_c) = 1 ⟹ E_c = M_Pl·ε₀^{1/β} = **1.0181 meV** — of the same order as the dark-energy characteristic scale 2.3 meV ((E_c)⁴ differs by a factor 27; O(1) coefficient undetermined).\n"
       "\n"
       "**【v2.9 honest note】 E_c is extremely sensitive to β**: β +1% ⟹ E_c = 2.068 meV (2.0× larger); β +2% ⟹ 4.14 meV (4.1×).\n"
       "Hence the **meV order of magnitude** is a robust conclusion, while the **numerical value of E_c** is entirely tied to β = 0.615 — the same root cause as the failure of the quantitative Ω_Λ route in §8.4 (`dlnΩ_Λ/dβ = 465`)."),
      ("§8.2 f_space correction",
       "(differs from the observed 2.3×10⁻²⁷ by ~70× — **【To be verified】** requires f_space ≈ 0.014 or mechanism correction).",
       "(differs from the observed 2.3×10⁻²⁷ by ~70×).\n"
       "\n"
       "**【v2.9 correction】** Under the holographic dilution `ε_eff = (l_P/R_c)² = 1.3975×10⁻¹²²`, `⟨f_space⟩` is not a knob — it is **uniquely solved from observations**:\n"
       "`⟨f_space⟩ = ρ_DM/(ε_eff·ρ_P) = 2.2511×10⁻²⁷ / 7.2037×10⁻²⁶ = 0.031250073 = **1/32.000**`\n"
       "(the earlier \"≈0.014\" came from a different ε_eff choice and is 2.23× too small; it is withdrawn).\n"
       "**【Honest note】** This relation is currently a **fit, not a prediction**: read as a void volume fraction it\n"
       "differs from the measured 50–80% by 16–26×; read as a rate-suppression factor it lacks any parameter-free\n"
       "suppression law `f_space(ρ_m)` (four self-consistent laws give four answers).\n"
       "⟹ **The quantitative explanation of dark matter remains a blank in this framework.**"),
      ("§8.3 mirror-branch falsified",
       "- Mirror-branch projection: κ_extra ~ Ω_mirror/Ω_total ≈ 0.5 (gravity shared across branches; EM/strong/weak filtered by the branch boundary) ⟹ ρ ~ 4×10⁻²⁷ kg/m³ **same order as observation** — **the bulk of dark matter may come from mirror-branch gravitational projection**【To be verified】;",
       "- Mirror-branch projection: **【v2.9 correction: falsified】** the earlier \"same order as observation\" claim fails. The two natural readings of 50:50 give opposite-direction discrepancies:\n"
       "  reading A (only gravity shared across branches, the rest filtered ⟹ Ω_dm = Ω_b = 0.0493) is **5.31× too low**;\n"
       "  reading B (keeping κ_extra ≈ Ω_mirror/Ω_total ≈ 0.5 ⟹ Ω_dm ~ 1) is **3.82× too high** — both far outside the error bar.\n"
       "  ⟹ The claim that the mirror branch supplies the **bulk** of dark matter is withdrawn; this subsection is downgraded to an open problem, and the void-CPT-κ anomaly holds only if the mechanism is rebuilt."),
      ]),
]

for src, dst, sec86, row9, ver, anchors in jobs:
    if not os.path.exists(src):
        FAIL.append("源文件不存在: %s" % src)
        continue
    new = patch(src, sec86, row9, ver, anchors)
    if new:
        open(dst, "w", encoding="utf-8").write(new)
        print("  → 写出 %s（%d 行，%d 字节）" % (os.path.basename(dst), len(new.splitlines()), len(new.encode("utf-8"))))

print("\n" + "=" * 72)
print("完成动作 %d 项" % len(OUT))
for o in OUT:
    print("  ·", o)
print("失败：%s" % (("；".join(FAIL)) if FAIL else "无"))
sys.exit(1 if FAIL else 0)
