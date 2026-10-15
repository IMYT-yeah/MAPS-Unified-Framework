# -*- coding: utf-8 -*-
"""第 73 轮论文补丁（中英同步）。锚点必须恰好命中一次，否则拒绝。"""
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
        print("  [XX] {:<32} 命中 {} 次 —— 拒绝".format(tag, n))
        BAD.append(tag)
        return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    print("  [OK] {:<32} 已改".format(tag))
    OK.append(tag)


for p in (ZH, EN):
    dst = os.path.join(HIST, os.path.basename(p).replace(
        ".md", "_备份_2026-10-02第73轮前.md"))
    shutil.copy2(p, dst)
    print("备份 -> {}".format(os.path.basename(dst)))

# ══════════════════════ 中文稿 ════════════════════════════════════════
A55 = "⟹ 在自然候选面中 **`R_c = c/H` 是唯一幸存者**。"

BLOCK_ZH = """
> **【v2.9 补充（第 73 轮：宇宙学判别力审计 —— 「找框架与 ΛCDM 的判别点」这个目标本身错了）】** 脚本 `_cosmo_audit_73.py`（**CD-1 … CD-10，10 项 0 失败**）。
> · **9 条宇宙学输出逐条对照标准侧**（O1 `Ω_K = 0`｜O2 `ρ = 3H²/8πG`｜O3 `M = c³/(2GH₀)`、`R_S = R_c`｜O4 `T = ℏH₀/2π`｜O5 面 = `c/H`｜O6 `w = −1 + 4ε/3`、`w_a = 0`｜O7 `ρ_Λ ~ E_c⁴`｜O8 暗物质｜O9 `H₀`）：**判别力为 0 的 8 条**（同值 / 恒等式 / 后选择 / 已否证 / 输入），剩下的 O7 是「**若当预言即被排除 117.8σ**」（`Ω_Λ = 0.0290` vs `0.6889 ± 0.0056`）⟹ **可判别的宇宙学输出 = 0 条**。⚠️ 另一条更基础的事实：ΛCDM 的主判别面（**功率谱 / 转移函数 / σ₈ / n_s / 暴胀 / 张量标量比**）在**正文里各 0 处** ⟹ 框架从未进入扰动层。
> · ⭐ **结构性结论（本轮的要点）**：框架的宇宙学输出写成**一个统一的形态** —— `{ Ω_K = 0, w_a = 0, w₀ = −1 + 2ν（ν 自由）, ρ = 3H²/8πG, T = ℏH₀/2π }`；而 **ΛCDM 是它 `ν = 0` 处的特例** ⟹ **ΛCDM ⊂ 框架** ⟹ 框架允许的观测集 **⊇** ΛCDM 的 ⟹ **凡是 ΛCDM 拟合得住的数据，框架一定也拟合得住** ⟹ **判别点在原则上不存在**（不是「还没找到」）。
> · ⚠️ **与第 51 轮同一个病（判据方向错了）**：第 51 轮找 `H/N = 0.25` 的**等式**跨点 —— 实为**不等式**（**N-13**）；本轮找框架与 ΛCDM 的**判别点** —— 实为**包含关系**（**N-29**）。⟹ **铁律 4 的又一例**：写下「可区分」之前先问**是什么关系**。
> · ⚠️ **A. 精确平坦性不可判**：框架 `Ω_K ≡ 0` vs 暴胀类 `|Ω_K| ≲ 10⁻⁵`，差 **5.3×10⁻³ σ**（比当前精度小 **8 个数量级**），且**没有 `σ < 10⁻⁵` 的路线图**。
> · ⚠️ **B. `w_a = 0` 不是框架独有**：ΛCDM 同样给 `w_a = 0` ⟹ DESI DR2 那 3.3σ 压力是**框架与 ΛCDM 共同承担**的，**不能读作「框架被已有数据判别」**（见 §8.4 的本轮标注）。
> · ⚠️ **C. `ε` 的第三义（C-16）**：§8.4 的 `E_c(z) = E_c,0(1+z)^ε`（**漂移指数**）与 §8.1 的**泄漏概率**同名，而 §8.1 的符号约定范围只写「本节及 §8.2」⟹ **未覆盖 §8.4**；若强行同义，取 §8.1 自己的 `ε(1 meV) ~ 1` 会给出 **`w = +0.333`**，与 DESI+CMB 差 **43.9σ** ⟹ 二者**必须不同义**。**D. 「哈勃球 = 史瓦西半径」是恒等式（C-17）**：见 §8.6.3 的本轮标注。
> · **判决**：**N-29**（负面：把「框架与 ΛCDM 的判别点」当作可达目标 —— 判否）、**C-16 / C-17**（更正）、**S-12 结项** ⟹ 由「★★★ 硬预测」→（第 61 轮）「解释性（非判别）」→（本轮）「**框架不覆盖宇宙学判别**」（与 **T-10** 同类）。⭐ 与第 61/62/72 轮合起来：**框架的对外接口在四个方向（工程 / 新力 / 宇宙学判别 / 凝聚态）上都已探到底，唯一剩下的 = EMRI**。
> · ⚠️ **诚实边界四条**：① 本轮只有**引文取证 ＋ 代数 ＋ 算术**，无新数值；② `Ω_Λ = 0.0290` 取自第 2 轮的账、σ 取 Planck 2018（**外部锚点**）；③ **`ν` 是否被框架固定本轮未定** —— 若将来能**唯一**定出 `ν ≠ 0`，`w = −1 + 2ν` 会成为**真判别点**，故正确表述是「**在框架目前的表述下**」不存在判别点；④ §8.6.3 的等分账推出 `ρ = 3H²/8πG`（平坦性）**仍是有内容的**（它不假设 Friedmann）—— 本轮更正的只是「**黑洞宇宙 = 机制说明**」这一句话。
"""

A_63 = "故 **哈勃球 = 史瓦西半径**：「黑洞宇宙」在此获得机制说明，不再是数值巧合。"
N_ZH_63 = A_63 + """
> ⚠️ **【第 73 轮标注（C-17）：这是恒等式，不是机制说明】** 代回去：`R_S = 2G·[c³/(2GH₀)]/c² = c/H₀ ≡ R_c` —— **`G` 与 `H₀` 全被消掉**，对**任意** `H₀` 恒成立（数值验证三个任意 `H₀`：相对差 0.0e+00 / 2.3e−16 / 0.0e+00）。⟹ 它**不是「巧合被解释」，而是比巧合更弱：恒等式、零内容**（与第 53 轮 `E_c ≡ 1 meV`（**C-4**）同一病症：把中间参数代回去，结论里什么都不剩）。**有内容的只有等分账本身**（`ρ = 3H²/8πG`，它不假设 Friedmann）。"""

A_84 = "**框架预测 w = const（wa=0）**——DESI DR2/Euclid 可直接检验。"
N_ZH_84 = A_84 + """ ⚠️**【第 73 轮判别力标注】** 该「预言」**不是框架独有的** —— **ΛCDM 同样给 `w_a = 0`**（`w = −1` 精确 ⟹ `w_a = 0`）；框架只是把 `w₀ = −1` 松弛成 `w₀ = −1 + 2ν`（`ν` 自由）⟹ **ΛCDM 是框架 `ν = 0` 处的特例**。因此下面那句 3.3σ 压力是**框架与 ΛCDM 共同承担**的，**不能读作「框架暗能量预言正被已有数据判别」**；**唯一的真判别机会**是「框架能否**唯一**定出 `ν ≠ 0`」—— 目前没有（见 §8.6.5 第 73 轮块）。"""

A_81 = ">    本节及 §8.2 里的 `ε`、`ε₀`、`ε_A`、`ε_B`、`ε_topo`、`ε_eff` **均属此义**；"
N_ZH_81 = A_81 + """
>    ⚠️ **第 73 轮补注（C-16）**：`ε` 还有**第三义** —— §8.4 的**漂移指数**（`E_c(z) = E_c,0(1+z)^ε` ⟹ `w = −1 + 4ε/3`），而本约定的范围（「本节及 §8.2」）**不含 §8.4**。⚠️ 若强行同义，取下面的边界条件 `ε(1 meV) ~ 1` 会给出 `w = +0.333`，与 DESI+CMB（`w = −1.028 ± 0.031`）差 **43.9σ** ⟹ **二者必须不同义**；正式声明见 §8.6.5 第 73 轮块。"""

print("\n[ZH]")
sub_once(ZH, A55, A55 + BLOCK_ZH, "§8.6.5 插第 73 轮块")
sub_once(ZH, A_63, N_ZH_63, "§8.6.3 恒等式标注（C-17）")
sub_once(ZH, A_84, N_ZH_84, "§8.4 判别力标注")
sub_once(ZH, A_81, N_ZH_81, "§8.1 ε 第三义补注（C-16）")

# ══════════════════════ 英文稿 ════════════════════════════════════════
B55 = "⟹ Among natural candidates, **`R_c = c/H` is the only survivor**."

BLOCK_EN = """
> **【v2.9 supplement (Round 73: cosmological discriminating-power audit — the goal of finding "a discriminating point vs ΛCDM" is itself wrong)】** Script `_cosmo_audit_73.py` (**CD-1 … CD-10, 10 checks, 0 failures**).
> · **All 9 cosmological outputs compared item by item against the standard side** (O1 `Ω_K = 0` | O2 `ρ = 3H²/8πG` | O3 `M = c³/(2GH₀)`, `R_S = R_c` | O4 `T = ℏH₀/2π` | O5 surface = `c/H` | O6 `w = −1 + 4ε/3`, `w_a = 0` | O7 `ρ_Λ ~ E_c⁴` | O8 dark matter | O9 `H₀`): **8 of 9 have zero discriminating power** (same value / identity / post-selection / already refuted / input); the remaining O7 is "**excluded at 117.8σ if treated as a prediction**" (`Ω_Λ = 0.0290` vs `0.6889 ± 0.0056`) ⟹ **discriminating cosmological outputs = 0**. ⚠️ A more basic fact: ΛCDM's main discriminating surfaces (**power spectrum / transfer function / σ₈ / n_s / inflation / tensor-to-scalar ratio**) appear **0 times each in the body** ⟹ the framework never enters the perturbation level.
> · ⭐ **Structural conclusion (the point of this round)**: the framework's cosmological outputs form **one uniform shape** — `{ Ω_K = 0, w_a = 0, w₀ = −1 + 2ν (ν free), ρ = 3H²/8πG, T = ℏH₀/2π }` — and **ΛCDM is its special case at `ν = 0`** ⟹ **ΛCDM ⊂ framework** ⟹ the framework's allowed observation set **⊇** ΛCDM's ⟹ **whatever data ΛCDM can fit, the framework can fit too** ⟹ **a discriminating point does not exist in principle** (not "not found yet").
> · ⚠️ **The same disease as round 51 (wrong direction of the criterion)**: round 51 looked for the **equality** crossing `H/N = 0.25` — it is actually an **inequality** (**N-13**); this round looks for a **discriminating point** between the framework and ΛCDM — it is actually an **inclusion relation** (**N-29**). ⟹ **Iron rule 4, once more.**
> · ⚠️ **A. Exact flatness is undecidable**: framework `Ω_K ≡ 0` vs inflation-type `|Ω_K| ≲ 10⁻⁵` — the difference is **5.3×10⁻³ σ** (**8 orders of magnitude** below current precision), with **no roadmap for `σ < 10⁻⁵`**.
> · ⚠️ **B. `w_a = 0` is not framework-specific**: ΛCDM also gives `w_a = 0` ⟹ the 3.3σ DESI DR2 pressure is **borne jointly** by the framework and ΛCDM and **must not be read as "the framework is being discriminated by existing data"** (see this round's annotation in §8.4).
> · ⚠️ **C. The third meaning of `ε` (C-16)**: §8.4's `E_c(z) = E_c,0(1+z)^ε` (a **drift exponent**) shares its symbol with §8.1's **leakage probability**, while §8.1's notation convention scopes itself to "this section and §8.2" ⟹ **it does not cover §8.4**; forcing them to coincide and using §8.1's own `ε(1 meV) ~ 1` would give **`w = +0.333`**, i.e. **43.9σ** away from DESI+CMB ⟹ they **must differ**. **D. "Hubble sphere = Schwarzschild radius" is an identity (C-17)**: see this round's annotation in §8.6.3.
> · **Verdict**: **N-29** (negative: treating "a discriminating point vs ΛCDM" as an attainable goal — ruled out), **C-16 / C-17** (corrections), **S-12 closed** ⟹ from "★★★ hard prediction" → (round 61) "explanatory (non-discriminating)" → (this round) "**the framework does not cover cosmological discrimination**" (same class as **T-10**). ⭐ Together with rounds 61/62/72: **the framework's external interfaces have been probed to the bottom in four directions (engineering / new force / cosmological discrimination / condensed matter) — the only one left is EMRI**.
> · ⚠️ **Four honesty boundaries**: ① this round is **citation + algebra + arithmetic only**, no new numerics; ② `Ω_Λ = 0.0290` comes from round 2's ledger and σ from Planck 2018 (**external anchor**); ③ **whether `ν` is fixed by the framework is left open** — if it can later be **uniquely** fixed to `ν ≠ 0`, then `w = −1 + 2ν` becomes a **genuine discriminating point**; the correct statement is therefore "**under the framework's present formulation**"; ④ the equipartition derivation of `ρ = 3H²/8πG` (flatness) in §8.6.3 **still carries content** (it does not assume Friedmann) — what is corrected here is only the sentence "**the black-hole universe = a mechanism explanation**".
"""

B_63a = 'Hence **the Hubble sphere equals the Schwarzschild radius**: the "black-hole universe" acquires a mechanism here'
B_63b = "and is no longer a numerical coincidence."
N_EN_63 = B_63a + B_63b + """
> ⚠️ **【Round-73 annotation (C-17): this is an identity, not a mechanism】** Substituting back: `R_S = 2G·[c³/(2GH₀)]/c² = c/H₀ ≡ R_c` — **both `G` and `H₀` cancel**, identically for **any** `H₀` (numerically checked at three arbitrary `H₀`: relative differences 0.0e+00 / 2.3e−16 / 0.0e+00). ⟹ It is **not "a coincidence explained", but something weaker than a coincidence: an identity with zero content** (the same disease as `E_c ≡ 1 meV` (**C-4**) in round 53: substitute the intermediate parameters back and nothing remains). **Only the equipartition account itself carries content** (`ρ = 3H²/8πG`, which does not assume Friedmann)."""

B_84 = "**The framework predicts w = const (wa=0)** — directly testable with DESI DR2/Euclid."
N_EN_84 = B_84 + """ ⚠️**【Round-73 discriminating-power annotation】** This "prediction" is **not framework-specific** — **ΛCDM also gives `w_a = 0`** (`w = −1` exactly ⟹ `w_a = 0`); the framework merely relaxes `w₀ = −1` to `w₀ = −1 + 2ν` (`ν` free) ⟹ **ΛCDM is the framework's special case at `ν = 0`**. Hence the 3.3σ pressure mentioned below is **borne jointly** by the framework and ΛCDM and **must not be read as "the framework's dark-energy prediction is being discriminated by existing data"**; the **only genuine discriminating opportunity** is "can the framework **uniquely** fix `ν ≠ 0`?" — currently it cannot (see the round-73 block in §8.6.5)."""

B_81 = ">    `ε`, `ε₀`, `ε_A`, `ε_B`, `ε_topo`, `ε_eff` in this section and §8.2 **all carry this meaning**;"
N_EN_81 = B_81 + """
>    ⚠️ **Round-73 annotation (C-16)**: `ε` carries a **third meaning** — the **drift exponent** of §8.4 (`E_c(z) = E_c,0(1+z)^ε` ⟹ `w = −1 + 4ε/3`), which this convention's scope ("this section and §8.2") **does not cover**. ⚠️ Forcing them to coincide and using the boundary condition below (`ε(1 meV) ~ 1`) would give `w = +0.333`, i.e. **43.9σ** away from DESI+CMB (`w = −1.028 ± 0.031`) ⟹ **they must differ**; the formal declaration is in the round-73 block of §8.6.5."""

print("\n[EN]")
sub_once(EN, B55, B55 + BLOCK_EN, "§8.6.5 insert Round-73 block")
sub_once(EN, B_63a, N_EN_63, "§8.6.3 identity annotation (C-17)")
sub_once(EN, B_84, N_EN_84, "§8.4 discriminating-power note")
sub_once(EN, B_81, N_EN_81, "§8.1 third meaning of ε (C-16)")

print("\n通过 {} 项，失败 {} 项".format(len(OK), len(BAD)))
if BAD:
    print("失败：{}".format(BAD))
