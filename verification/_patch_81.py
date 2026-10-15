# -*- coding: utf-8 -*-
"""第 81 轮论文补丁（中英同步）：
  ① §8.6.5 —— 【第 81 轮】`8π/3` 这个待办**没有对象**（H1 收口）
  ② §8.6.7 —— 【第 81 轮】「关联长度」的定量（H4：关联函数二分 + N_eff = L²）
⚠️ 改前备份；改后复跑核验脚本。
"""
import io, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
TAG = "_备份_2026-10-02第81轮前.md"

OK = [0]
BAD = [0]


def chk(tag, cond, msg):
    if cond:
        OK[0] += 1
        print("  [OK] {:<6} {}".format(tag, msg))
    else:
        BAD[0] += 1
        print("  [XX] {:<6} {}  <-- 失败".format(tag, msg))


def backup(p):
    d = os.path.join(HIST, os.path.basename(p).replace(".md", TAG))
    shutil.copy2(p, d)
    print("  备份 → {}".format(os.path.basename(d)))


def sub_once(p, old, new, tag):
    t = io.open(p, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        print("  [XX] {:<26} 锚点命中 {} 次".format(tag, n))
        BAD[0] += 1
        return False
    io.open(p, "w", encoding="utf-8").write(t.replace(old, new, 1))
    print("  [OK] {:<26} 已插入".format(tag))
    OK[0] += 1
    return True


print("=" * 78)
print("第 81 轮论文补丁（中英同步）")
print("=" * 78)
backup(ZH)
backup(EN)

# ================================================================
print("\n[ZH-1] §8.6.5：`8π/3` 这个待办**没有对象**（H1）")
Z_A = "⟹ 在自然候选面中 **`R_c = c/H` 是唯一幸存者**。"
Z_NEW = Z_A + """

> **【v2.9 收口（第 81 轮：`8π/3` 这个待办**没有对象**）】** 交接清单的老编号里有「**消掉 `8π/3`**」（第 17 轮登记）。本轮把它算清（脚本 `_h1h4_81.py`，**H1-1 … H4-3，9 项 0 失败**）。
>
> · **复现**：`ρ_micro = ρ_P/N`（`N = (R_H/l_P)²`，`ε_eff = 1/N`）`= H²/G`；`ρ_holo = 3H²/(8πG)` ⟹ `λ ≡ ρ_micro/ρ_holo = **8π/3 = 8.37758041**`（相对差 **2.2×10⁻¹⁶** ✓）。
> · **三条出路全部算清**：① 把 `N` 换成 **`πR²/l_P²`**（第 75 轮 C-20 判定 B5 必须用**投影面积**）⟹ `λ = **8/3 = 2.666667**`（与第 17 轮原文记的 2.67 一致）；② 全息路不变（`λ = 1`）；③ 要再消掉剩下的 `8/3`，**只能改 `ε_eff`** —— 那是**自由输入** ⟹ **那是「配」，不是推导**。⚠️ 剩余因子 `8/3` 来自 GR 的 `3/(8πG)`（`8π` = 引力耦合的立体角、`3` = 空间维数），而微观路的 `ρ_P/N` 里**根本没有 `4π` 或 `8π`**。
> · ⟹ **判决**：`8π/3` 是「**微观事件率密度**」与「**引力约束密度**」的比值，而这两者在框架里**从未被要求相等**（第 17 轮自己写「**这不是矛盾，是分工**」）⟹ **「消掉 `8π/3`」这个待办没有对象** ⟹ 登记 **N-35**（与第 77 轮「`g` 的精确值没有对象」**同构**）。
> · ⚠️ ⭐ **顺带查出 C-32（符号撞车，第 4 次）**：符号 **`N` 有两义** —— `N_micro = (R_H/l_P)²`（第 17 轮，**无 π**）vs `N_B5 = A/(4l_P²) = πR²/l_P²`（第 75 轮 C-20，**有 π**）；比值**恰为 π**，正是 `8π/3 → 8/3` 的那一步。⚠️ 两者**都被用在「全息稀释 `ε_eff = 1/N`」这同一件事上** ⟹ 与 C-15 / C-16 / C-21 同族（**同名不同义**），引用时必须写明是哪一个。"""
sub_once(ZH, Z_A, Z_NEW, "ZH §8.6.5 收口块")

print("\n[EN-1] §8.6.5: the `8π/3` task has **no object** (H1)")
E_A = "⟹ Among natural candidates, **`R_c = c/H` is the only survivor**."
E_NEW = E_A + """

> **【v2.9 close-out (round 81: the `8π/3` task has **no object**)】** The handover list kept an old item "**eliminate `8π/3`**" (registered in round 17). This round settles it (script `_h1h4_81.py`, **H1-1 … H4-3, 9 checks, 0 failures**).
>
> · **Reproduced**: `ρ_micro = ρ_P/N` (with `N = (R_H/l_P)²`, `ε_eff = 1/N`) `= H²/G`; `ρ_holo = 3H²/(8πG)` ⟹ `λ ≡ ρ_micro/ρ_holo = **8π/3 = 8.37758041**` (relative error **2.2×10⁻¹⁶** ✓).
> · **All three escape routes computed**: ① replace `N` by **`πR²/l_P²`** (round 75's C-20 verdict: B5 must use the **projected area**) ⟹ `λ = **8/3 = 2.666667**` (matching round 17's recorded 2.67); ② the holographic route is unchanged (`λ = 1`); ③ eliminating the remaining `8/3` requires **changing `ε_eff`** — a **free input** ⟹ that is **fitting, not derivation**. ⚠️ The residual `8/3` comes from GR's `3/(8πG)` (`8π` = solid angle of the gravitational coupling, `3` = spatial dimension), whereas the microscopic route's `ρ_P/N` contains **no `4π` or `8π` at all**.
> · ⟹ **Verdict**: `8π/3` is the ratio of a "**microscopic event-rate density**" to a "**gravitational constraint density**", and the framework **never required these two to be equal** (round 17 itself wrote "**this is not a contradiction, it is a division of labour**") ⟹ **the task "eliminate `8π/3`" has no object** ⟹ registered as **N-35** (isomorphic to round 77's "the exact value of `g` has no object").
> · ⚠️ ⭐ **Incidentally found C-32 (notation collision, the 4th)**: the symbol **`N` carries two meanings** — `N_micro = (R_H/l_P)²` (round 17, **no π**) versus `N_B5 = A/(4l_P²) = πR²/l_P²` (round 75, C-20, **with π**); their ratio is **exactly π**, which is precisely the `8π/3 → 8/3` step. ⚠️ Both are used for **the same job — holographic dilution `ε_eff = 1/N`** ⟹ same family as C-15 / C-16 / C-21 (**same name, different meaning**); citations must state which one."""
sub_once(EN, E_A, E_NEW, "EN §8.6.5 close-out block")

# ================================================================
print("\n[ZH-2] §8.6.7： 「关联长度」的定量（H4）")
Z2_A = "⚠️ **与第 21 轮并存**：单个 tick 仍是双射 ⟹ **状态的信息严格守恒**；本轮算的是**系综（无知）熵**的增长。二者不矛盾——「无信息丢失」说的是状态，「熵增」说的是我们对状态的无知。"
Z2_NEW = Z2_A + """

> **【v2.9 补完（第 81 轮：「关联长度」的定量 —— 它不是一个新量，已经被写进 `h` 里了）】** 老编号里有「**关联长度定量**」（第 22 轮的观察：固定轴下各种子散布远超独立样本估计 ⟹ **有效自由度 < 格点数**，当时明标「**未做**」）。本轮做完（脚本 `_h1h4_81.py`）。
>
> **口径**：沿 x 轴一次 tick，**每条 x 线一个独立相位**（框架原样：A1 的每线独立相位）。可观测 `u_i = ±1`（格点 i 被交换到 +x 还是 −x）。
>
> | 量 | 结果 |
> |---|---|
> | **沿轴关联** `C∥(d)` | `= (−1)^d` —— **逐位精确**（**全枚举**，零噪声）：**周期 2、永不衰减** |
> | **垂直轴关联** `C⊥` | 单实现偏差**精确等于 `1/L`**（0.2500 / 0.1667 / 0.1250 @ L = 4/6/8）；**300 个相位实现平均后 `max|C⊥| = 0.0204`** ⟹ **异线独立（0）** |
> | **有效自由度** | `N_eff = **L²**`（**线数**），而非 `L³`（格点数）—— MC：16.09 / 36.46 / 65.83 / 144.77 vs `L²` = 16 / 36 / 64 / 144 ✓ |
>
> ⟹ ⭐ **「关联长度」没有有限值，而是二分的**：沿轴 `ξ∥ = ∞`（带 `(−1)^d` 调制）、垂直轴 `ξ⊥ = 0`。
> **机制**：tick 的**随机性单元是「线」**（1D 对象，每线一个相位 bit），**不是格点**。
> ⟹ ⭐ **它不是新量 —— 它已经写在 `h = ln3 + L²ln2` 里了**：那个 **`L²` 就是线数**。本轮给出的只是它的**空间表现**（各向异性二分的关联函数）。这同时给出了第 22 轮「`N_eff` ~ 线数」的**机制解释**（不是统计涨落的偶然，是「随机性单元是线」的结构性后果）。
> ⚠️ **诚实收口（N-36）**：**不要**把 `h` 的 `L²`（面积标度）读作「框架推出了面积律」—— 它是 `h` 的**定义式**；而「格点离散结构 ↔ 面积律」已在第 80 轮正式**登记为框架不覆盖**、B5 与衬底之间只有一条松不等式（**N-13**）⟹ **本条不提供新支撑**（与第 77 轮「把定义当发现」**同类**）。"""
sub_once(ZH, Z2_A, Z2_NEW, "ZH §8.6.7 关联长度块")

print("\n[EN-2] §8.6.7: quantifying the \"correlation length\" (H4)")
E2_A = "⚠️ **Coexists with round 21**: a single tick is still a bijection ⟹ the information of the *state* is strictly conserved; what this round computes is the growth of the *ensemble* (ignorance)"
t = io.open(EN, encoding="utf-8").read()
cand = [ln for ln in t.split("\n") if ln.startswith(E2_A)]
assert len(cand) == 1, len(cand)
E2_A_FULL = cand[0]
E2_NEW = E2_A_FULL + """

> **【v2.9 completion (round 81: quantifying the "correlation length" — it is not a new quantity, it is already written into `h`)】** An old list item read "**quantify the correlation length**" (round 22's observation: with a fixed axis the spread across seeds far exceeds the independent-sample estimate ⟹ **effective d.o.f. < number of sites**; marked "**not done**" at the time). This round completes it (script `_h1h4_81.py`).
>
> **Caliber**: one tick along the x axis, **one independent phase per x-line** (exactly the framework's A1). Observable `u_i = ±1` (site i is exchanged towards +x or −x).
>
> | Quantity | Result |
> |---|---|
> | **Along-axis** correlation `C∥(d)` | `= (−1)^d` — **bit-exact** (**full enumeration**, zero noise): **period 2, never decaying** |
> | **Transverse** correlation `C⊥` | single-realization deviation is **exactly `1/L`** (0.2500 / 0.1667 / 0.1250 at L = 4/6/8); after averaging over **300 phase realizations `max|C⊥| = 0.0204`** ⟹ **different lines are independent (0)** |
> | **Effective d.o.f.** | `N_eff = **L²**` (**number of lines**), not `L³` (number of sites) — MC: 16.09 / 36.46 / 65.83 / 144.77 vs `L²` = 16 / 36 / 64 / 144 ✓ |
>
> ⟹ ⭐ **The "correlation length" has no finite value; it is dichotomous**: along the axis `ξ∥ = ∞` (with a `(−1)^d` modulation), perpendicular to it `ξ⊥ = 0`.
> **Mechanism**: the tick's **randomness unit is the "line"** (a 1D object, one phase bit per line), **not the site**.
> ⟹ ⭐ **It is not a new quantity — it is already written into `h = ln3 + L²ln2`**: that **`L²` is the number of lines**. What this round supplies is only its **spatial manifestation** (an anisotropic, dichotomous correlation function). This also gives the **mechanism** behind round 22's "`N_eff` ~ number of lines" (not a statistical accident but a structural consequence of "the randomness unit is a line").
> ⚠️ **Honest close-out (N-36)**: do **not** read the `L²` in `h` (an area scaling) as "the framework derives the area law" — it is `h`'s **defining expression**; and "lattice discretization ↔ area law" was formally **registered as NOT COVERED** in round 80, with only a loose inequality between B5 and the substrate (**N-13**) ⟹ **this entry provides no new support** (same type as round 77's "mistaking a definition for a discovery")."""
sub_once(EN, E2_A_FULL, E2_NEW, "EN §8.6.7 correlation-length block")

print("")
print("=" * 78)
print("  通过 {} 项，失败 {} 项".format(OK[0], BAD[0]))
print("=" * 78)
