# -*- coding: utf-8 -*-
"""第 75 轮论文补丁（中英同步）。锚点必须恰好命中一次，否则拒绝。"""
import io
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
HIST = os.path.join(ROOT, "MAPS-Unified-Framework", "paper", "history")
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

OK, BAD = [], []


def sub_once(path, old, new, tag):
    t = io.open(path, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        print("  [XX] {:<34} 命中 {} 次 —— 拒绝".format(tag, n))
        BAD.append(tag)
        return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    print("  [OK] {:<34} 已改".format(tag))
    OK.append(tag)


for p in (ZH, EN):
    dst = os.path.join(HIST, os.path.basename(p).replace(
        ".md", "_备份_2026-10-02第75轮前.md"))
    shutil.copy2(p, dst)
    print("备份 -> {}".format(os.path.basename(dst)))

# ═══════════════ 中文稿 ═══════════════════════════════════════════════
A_ZH_EQ = "\\;\\Longrightarrow\\; \\rho = \\frac{3H_0^2}{8\\pi G}$$"
N_ZH_EQ = A_ZH_EQ + """
> ⚠️ **【第 75 轮口径注（C-20）：面积口径必须写明】** 上式左边的体积用整球 `(4π/3)R³`，而右边的
> 单元数取 **`N = πR²/l_P²`（投影/截面面积）**，**不是** `4πR²/l_P²`。
> 取整球面积会给出 `ρ = 3H²/(2πG)` —— **差 4.000 倍**（数值 3.4395×10⁻²⁶ vs 8.5987×10⁻²⁷ kg/m³）。
> ⚠️ 这个投影与 §4.9 的 B5「**体 = 表面投影**（`I = H(Σ)`）」是同**一个**投影 ⟹ 口径**自洽**，
> 但此前**未写明**。"""

A_ZH_HN = ("【诚实标注】上述 `M` 使用 Misner–Sharp 质量表达式，即**已在 FRW 内部**使用 GR ⟹ "
           "严格地说是「在 FRW 内推出 k = 0」，不是从零推出引力。另 `ρ = 3H²/8πG` 只是**约束方程**；"
           "加速度方程与连续性方程仍缺（给定约束后二者等价）。")
N_ZH_HN = A_ZH_HN + """

> **【v2.9 补充（第 75 轮：宇宙学动力学 —— 加速度方程与连续性方程「为什么补不上」）】** 脚本 `_friedmann_75.py`（**FR-1 … FR-10，10 项 0 失败**）。题源 = §8.6.3 自认的这条缺口。
> · ⭐ **结果 A（等分账「恒成立」）**：等分账的输入**只有同时刻的 `H`**（`R = c/H`、`T = ℏH/2πk_B`），没有一处用到 `H = H₀` ⟹ 逐一验算 `H = H₀ / 2H₀ / H₀/2` 的相对差均为 **3.7×10⁻¹⁶** ⟹ **`Ω_tot(t) ≡ 1`，即 `Ω_K ≡ 0` 是「恒为 0」而非「今天恰好为 0」**，且 `ρ ∝ H²`。⚠️ 论文只在 `t₀` 写这条等式 ⟹ 「任意 `t`」是**自然外推**（纯框架内部加强，**不**改变第 73 轮的「`Ω_K = 0` 无判别力」）。
> · ⭐⭐ **结果 B（硬写守恒 ⟹ `w = −1/3`，零自由参数）**：面上 `E(H) = N·k_BT = ℏc²/(2l_P²H)`（`E ∝ 1/H`）、`V = (4π/3)(c/H)³`（`V ∝ H⁻³`）；若要求 `dE = −p dV`，则 `p = −ℏH²/(8πl_P²c)`（负压），
>   `w = p/(ρc²) = −ℏG/(3l_P²c³) ≡ **−1/3**` —— **`ℏ`、`G`、`c`、`H₀` 全消掉**（数值 −0.3333333333，与解析式相对差 0.0e+00）。自洽反算 `Ḣ = −4πG(ρ+p/c²) ≡ −H₀²`（相对差 1.4×10⁻¹⁶）⟹ `H = 1/t`、`a ∝ t`。
> · ⭐ **结果 C（`w = −1/3` 就是曲率标度）**：`ρ ∝ a^{−3(1+w)} = a^{−2}` —— 平宇宙里**没有守恒物质**按 `a⁻²` 稀释（物质 `a⁻³` / 辐射 `a⁻⁴` / `Λ` 常数）⟹ **等分账的 `ρ` 只能是「约束」，不能是「守恒流体」**。
> · ⭐⭐ **核心（两个 `ρ` 不接）**：§2.2 的 **`J^μ`（微变权流）**是**守恒**的，但它是**湮灭事件计数**测度（`W[Σ] = ∫J·dΣ`），**不带 `p`** ⟹ 写不出 `ρ̇ + 3H(ρ+p/c²) = 0`；而等分账的 `ρ` 是**质量密度**但要守恒就必然 `w = −1/3`（对观测 `w = −1.028 ± 0.031` 差 **22.4σ**）。判据：「`J^μ`/微变权」与「`3H²/8πG`」**同行共现 0 次** ⟹ **接口从未被写过**。⟹ 弗里德曼对需要**同一个 `ρ` 同时满足「约束」与「守恒」**，而框架有的是**两个不同的 `ρ`**。
> · **判决**：**加速度方程与连续性方程不是「还没推导」，而是「在这个账里不存在」** —— 缺的**不是方程，是对象**（第 4 种失败形态：**分层**）。登记 **I-20（结项）**、**N-30（负面）**、**C-20 / C-21（更正）**。
> · ⚠️ **诚实边界**：① 结果 B **加了一条框架自己没有的假设**（面上绝热守恒）——本轮的用法是**反证**（「**若**要写守恒，**就**必然 `w = −1/3`」），**不是**说框架预言 `w = −1/3`；② 「任意 `t`」是外推；③ 观测 `w` 取自 §8.4 引的 DESI 2024+CMB（**外部锚点**）；④ 本轮**不主张 `J^μ` 错了**（它作为计数流没问题，问题在**接口没写**）；⑤ 与第 73 轮合起来：**本轮给出了「为什么 `w` 只能来自外部参数 `ν`」** —— **等分账对 `w` 零约束**。"""

A_ZH_COV = ("> ⚠️ **第 72 轮补注（C-15）**：`λ` 还有**第三义** —— §6.4 的 Φ⁴ 四次耦合 "
            "`V(Φ) = −½μ²Φ² + ¼λΦ⁴`（本约定此前**未提**）；另有 **`g` 同字母两义**"
            "（§6.1 的钉扎耦合 `gΦψ̄ψ` vs §5.7 的弦网几何因子 `J = n_G·E_P·g`），**此前无任何约定**。")
N_ZH_COV = A_ZH_COV + """
> ⚠️ **第 75 轮补注（C-21）**：**`ρ` 至少 5 义** —— `ρ_pair`（事件率密度，§2.2）／`ρ_raw`（原始涨落密度，§8.2）／**等分账的 `ρ`（质量密度，本节 §8.6.3）**／`ρ_Λ`／`ρ_DM`；**`w` 至少 2 义** —— §8.4 的 `w = −1 + 4ε/3`（**暗能量分量**，来源 = `E_c` 漂移）与第 75 轮的 `w = −1/3`（**面上总量**的等效值，来源 = `E ∝ 1/H`）。⟹ **引用时必须写明是哪一个**（与 C-15 / C-16 同族；两者**不矛盾**，因为是不同对象）。"""

print("\n[ZH]")
sub_once(ZH, A_ZH_EQ, N_ZH_EQ, "§8.6.3 面积口径注（C-20）")
sub_once(ZH, A_ZH_HN, N_ZH_HN, "§8.6.3 插第 75 轮块")
sub_once(ZH, A_ZH_COV, N_ZH_COV, "§8.6 ρ/w 约定补注（C-21）")

# ═══════════════ 英文稿 ═══════════════════════════════════════════════
A_EN_EQ = "\\;\\Longrightarrow\\; \\rho = \\frac{3H_0^2}{8\\pi G}$$"
N_EN_EQ = A_EN_EQ + """
> ⚠️ **【Round-75 notation note (C-20): the area convention must be stated】** The left side uses the full-sphere volume `(4π/3)R³`, while the right side takes **`N = πR²/l_P²` (projected/cross-sectional area)**, **not** `4πR²/l_P²`. Taking the full-sphere area gives `ρ = 3H²/(2πG)` — a **factor of 4.000** off (3.4395×10⁻²⁶ vs 8.5987×10⁻²⁷ kg/m³). ⚠️ This projection is the **same** one as §4.9's B5 ("**bulk = surface projection**", `I = H(Σ)`) ⟹ the convention is **self-consistent**, but was **not previously stated**. """

A_EN_HN = """【Honest note】 `M` uses the Misner–Sharp mass expression, i.e. GR is used **inside** FRW ⟹ strictly this is
"deriving k = 0 within FRW", not deriving gravity from scratch. Also `ρ = 3H²/8πG` is only the **constraint
equation**; the acceleration and continuity equations are still missing (they are equivalent given the constraint)."""
N_EN_HN = A_EN_HN + """

> **【v2.9 supplement (Round 75: cosmological dynamics — why the acceleration and continuity equations cannot be added)】** Script `_friedmann_75.py` (**FR-1 … FR-10, 10 checks, 0 failures**). Source = the gap that §8.6.3 itself admits.
> · ⭐ **Result A (the equipartition account holds identically)**: its inputs involve **only the instantaneous `H`** (`R = c/H`, `T = ℏH/2πk_B`); nowhere is `H = H₀` used ⟹ checking `H = H₀ / 2H₀ / H₀/2` gives a relative difference of **3.7×10⁻¹⁶** in all three cases ⟹ **`Ω_tot(t) ≡ 1`, i.e. `Ω_K ≡ 0` is "identically zero", not "zero today"**, and `ρ ∝ H²`. ⚠️ The paper writes this only at `t₀` ⟹ "any `t`" is a **natural extrapolation** (a purely internal strengthening; it does **not** change round 73's "`Ω_K = 0` has no discriminating power").
> · ⭐⭐ **Result B (imposing conservation ⟹ `w = −1/3`, zero free parameters)**: on the surface `E(H) = N·k_BT = ℏc²/(2l_P²H)` (`E ∝ 1/H`) and `V = (4π/3)(c/H)³` (`V ∝ H⁻³`); requiring `dE = −p dV` gives `p = −ℏH²/(8πl_P²c)` (negative pressure) and `w = p/(ρc²) = −ℏG/(3l_P²c³) ≡ **−1/3**` — **`ℏ`, `G`, `c`, `H₀` all cancel** (numerically −0.3333333333, relative difference from the closed form 0.0e+00). Back-substitution: `Ḣ = −4πG(ρ+p/c²) ≡ −H₀²` (relative difference 1.4×10⁻¹⁶) ⟹ `H = 1/t`, `a ∝ t`.
> · ⭐ **Result C (`w = −1/3` is exactly the curvature scaling)**: `ρ ∝ a^{−3(1+w)} = a^{−2}` — in a flat universe **no conserved species** dilutes as `a⁻²` (matter `a⁻³` / radiation `a⁻⁴` / `Λ` constant) ⟹ **the equipartition `ρ` can only be a "constraint", never a "conserved fluid"**.
> · ⭐⭐ **The core (two `ρ`'s that do not connect)**: §2.2's **`J^μ` (infinitesimal-change-weight current)** *is* conserved, but it is the **annihilation-event counting** measure (`W[Σ] = ∫J·dΣ`) and carries **no `p`** ⟹ it cannot give `ρ̇ + 3H(ρ+p/c²) = 0`; whereas the equipartition `ρ` is a **mass density** that, if conserved, forces `w = −1/3` (`22.4σ` away from the observed `w = −1.028 ± 0.031`). Criterion: "`J^μ`/微变权" and "`3H²/8πG`" **co-occur on the same line 0 times** ⟹ **the interface was never written**. ⟹ The Friedmann pair needs **one `ρ` satisfying both "constraint" and "conservation"**, but the framework has **two different `ρ`'s**.
> · **Verdict**: the acceleration and continuity equations are **not "not yet derived" but "nonexistent within this account"** — what is missing is **not an equation but an object** (the 4th failure mode: **layering**). Registered: **I-20 (closed)**, **N-30 (negative)**, **C-20 / C-21 (corrections)**.
> · ⚠️ **Honesty boundaries**: ① Result B **adds an assumption the framework itself does not make** (adiabatic conservation on the surface) — it is used as a **proof by contradiction** ("**if** one writes conservation, **then** `w = −1/3`"), **not** as a claim that the framework predicts `w = −1/3`; ② "any `t`" is an extrapolation; ③ the observed `w` is quoted from §8.4 (DESI 2024+CMB, an **external anchor**); ④ this round does **not** claim `J^μ` is wrong (as a counting current it is fine; the issue is that the **interface is unwritten**); ⑤ together with round 73, **this round explains *why* `w` can only come from the external parameter `ν`** — **the equipartition account imposes zero constraint on `w`**. """

A_EN_COV = "> ⚠️ **Round-72 addendum (C-15)**: `λ` carries a **third meaning** — the Φ⁴ quartic coupling of §6.4, `V(Φ) = −½μ²Φ² + ¼λΦ⁴` (**not mentioned** in this convention before); and **`g` carries two meanings under one letter** (§6.1's pinning coupling `gΦψ̄ψ` vs §5.7's string-net geometric factor `J = n_G·E_P·g`), previously **undeclared**. "
N_EN_COV = A_EN_COV + """
> ⚠️ **Round-75 addendum (C-21)**: **`ρ` carries at least 5 meanings** — `ρ_pair` (event-rate density, §2.2) / `ρ_raw` (primordial fluctuation density, §8.2) / **the equipartition `ρ` (mass density, §8.6.3 here)** / `ρ_Λ` / `ρ_DM`; and **`w` carries at least 2** — §8.4's `w = −1 + 4ε/3` (**dark-energy component**, from `E_c` drift) versus round 75's `w = −1/3` (the **total on the surface**, from conservation of `E ∝ 1/H`). ⟹ **always state which one is meant** (same family as C-15 / C-16; the two **do not contradict** each other, being different objects). """

print("\n[EN]")
sub_once(EN, A_EN_EQ, N_EN_EQ, "§8.6.3 area-convention note (C-20)")
sub_once(EN, A_EN_HN, N_EN_HN, "§8.6.3 insert Round-75 block")
sub_once(EN, A_EN_COV, N_EN_COV, "§8.6 ρ/w convention (C-21)")

print("\n通过 {} 项，失败 {} 项".format(len(OK), len(BAD)))
if BAD:
    print("失败：{}".format(BAD))
