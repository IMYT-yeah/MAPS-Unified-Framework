# -*- coding: utf-8 -*-
"""
第 40 轮论文补丁（中英同步）。

三处：
  (1) §4.8（第 39 轮块之后）：追加【v2.9 补充（第 40 轮：观测者读数不是 tick 不变量）】
      —— 三难表、判据 ⟨|O|⟩ = 1.557^N、|G| 与轨道数、诚实边界；
  (2) §8.6.3 等分账：等分 = 唯一不变测度（不需热化），但动力学保持轨道 ⟹ 等分是结构性/初值的；
  (3) §4.2 ② 衬底构型混合：47 μm 限制的是**空间输运**，不限制统计测度 ⟹ 第 21/26 轮担心解除。

锚点要求恰好命中一次，否则拒绝改动。正文引号一律用「」。
"""

import io
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
STAMP = "2026-09-20第40轮前"

N_OK = [0]
N_FAIL = [0]


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<30} 命中 {} 次 —— 拒绝".format(tag, n))
        N_FAIL[0] += 1
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<30} 已改".format(tag))
    N_OK[0] += 1


# ---------------------------------------------------------------- 备份
print("备份：")
for src, dst in [
    (ZH, os.path.join(HIST, "论文初稿_v2.9_备份_%s.md" % STAMP)),
    (EN, os.path.join(HIST, "Paper_v2.9_EN_备份_%s.md" % STAMP)),
]:
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
        print("  [OK] {}".format(os.path.basename(dst)))
    else:
        print("  [--] {}（跳过）".format(os.path.basename(dst)))

# ---------------------------------------------------------------- (1) §4.8 第 40 轮块
ZH_A = "按项目规约不得用作证据。"
ZH_B40 = "\n".join([
    "> **【v2.9 补充（第 40 轮：观测者读数**不是** tick 不变量）】** 上一条把问题改派给观测者模型之后，"
    "本轮做最便宜的一次判别：**这个读数能否是 tick 动力学的不变量？** 结论是**不能**。",
    "> · **方法**：把「一次 tick = 沿某轴的完美匹配（轴随机、每线独立随机相位，§8.6.7）」的**全部**选择枚举，"
    "它们在构型空间上生成一个置换群 **G**；**G 的轨道划分就是最大的 tick 不变粗粒化**"
    "（任何不变的读数都必须是轨道的函数）。其熵 `H = ln M − Σ_O(|O|/M)ln|O|` 就是"
    "「不变的读数最多能带多少熵」。",
    "> · **结果 1（tick 群很小）**：1D 环（长度 L）⟹ |G| = **L**（两个匹配的乘积是「移 2」，"
    "生成 L 阶二面体子群，非 2L）；2×2×2 ⟹ |G| = 8；**2×2×4（16 位点）⟹ |G| = 128**。"
    "⟹ 构型空间被切成大量**不变轨道**（2×2×2 → 46 条；**2×2×4 → 1357 条**）⟹ **动力学保持轨道、非遍历**。",
    "> · **结果 2（不变的读数熵太多）**：轨道划分的熵密度在全部算例中为 **0.42 – 0.49 纳特/格点**"
    "（2×2×4：0.4368），而 BH 要求 **0.25 纳特/l_P²**（1 格点 ↔ 1 l_P² 是第 35 轮的约定）⟹ **偏大约 1.75 倍**。",
    "> · **结果 3（反方向也不行）**：若 tick 群高度可迁（如第 21 轮的串行动力学 ⟹ S_N），"
    "唯一不变量是全局计数，熵 ≈ ½ln(πeN/2) ⟹ N = 10⁶ 时仅 7.63 纳特，而面积律要求 2.5×10⁵"
    "⟹ **次广延，给不出面积律**。",
    "> ⟹ **三难**：tick 不变的读数**要么熵太多（≈ 0.44）、要么熵太少（→ ½ln N）**；"
    "时间平均路线给 `τ = t_P/(δ²e²)`，**一个方程两个未知量 ⟹ 零预言力**。"
    "⟹ 剩下的只有**瞬时读数 + 观测者自身的分辨率 δ（或积分时间 τ）**，即 **B5 的公设**。",
    "> 🎯 **可证伪判据**：`H/N = ln2 − ⟨ln|O|⟩/N` ⟹ 要恰好命中 0.25，需要典型轨道大小"
    "**`⟨|O|⟩ = e^{0.4431N} = 1.557^N`**。并行 tick 动力学在 N = 16 上给的典型轨道 ≈ 60，"
    "而 `1.557^16 ≈ 1.2×10³` ⟹ **差约 20 倍**。",
    "> ⚠️ **诚实边界**：|G| 与轨道结构只在 **N ≤ 16** 上穷举；格子越大、每线相位自由度越多"
    "（4×4×4 有 513 个生成元）⟹ 群可能大得多 ⟹ **H/N 的 N → ∞ 极限未定**。"
    "但上述判据与 N 无关、可直接检验。本轮**没有**给出观测者分辨率的任何机制。",
    "",
])
sub_once(ZH, ZH_A, ZH_B40, "ZH §4.8 第 40 轮块")

EN_A = ("are **all registered as mechanism-free** and must not be used as evidence.")
EN_B40 = "\n".join([
    "> **【v2.9 supplement (round 40: the observer readout is NOT a tick invariant)】** After round 39 "
    "re-assigned the question to the observer model, this round performs the cheapest discriminator: "
    "**can the readout be invariant under the tick dynamics?** The answer is **no**.",
    "> · **Method**: enumerate **all** choices of \"one tick = perfect matching along one axis "
    "(random axis, independent per-line phase, §8.6.7)\"; they generate a permutation group **G** on "
    "configuration space; **the orbit partition of G is the largest tick-invariant coarse-graining** "
    "(any invariant readout must be a function of the orbit). Its entropy "
    "`H = ln M − Σ_O(|O|/M)ln|O|` is \"the most an invariant readout can carry\".",
    "> · **Result 1 (the tick group is small)**: 1D ring (length L) ⟹ |G| = **L** (the product of the "
    "two matchings is \"shift by 2\", generating a dihedral subgroup of order L, not 2L); 2×2×2 ⟹ "
    "|G| = 8; **2×2×4 (16 sites) ⟹ |G| = 128**. ⟹ configuration space is cut into many **invariant "
    "orbits** (2×2×2 → 46; **2×2×4 → 1357**) ⟹ **the dynamics preserves orbits: it is non-ergodic**.",
    "> · **Result 2 (an invariant readout carries too much entropy)**: the entropy density of the orbit "
    "partition is **0.42 – 0.49 nat per site** in every case computed (2×2×4: 0.4368), whereas BH "
    "requires **0.25 nat per l_P²** (1 site ↔ 1 l_P² is the convention of round 35) ⟹ **too large by "
    "about 1.75×**.",
    "> · **Result 3 (the opposite extreme fails too)**: if the tick group were highly transitive (e.g. "
    "the serial dynamics of round 21 ⟹ S_N), the only invariant would be the global count, with "
    "entropy ≈ ½ln(πeN/2) ⟹ only 7.63 nat at N = 10⁶ against the 2.5×10⁵ required by the area law "
    "⟹ **sub-extensive: no area law**.",
    "> ⟹ **Trilemma**: an invariant readout carries **either too much entropy (≈ 0.44) or too little "
    "(→ ½ln N)**; the time-averaging route gives `τ = t_P/(δ²e²)`, **one equation with two unknowns ⟹ "
    "zero predictive power**. ⟹ What remains is an **instantaneous readout plus the observer's own "
    "resolution δ (or integration time τ)**, i.e. the **postulate of B5**.",
    "> 🎯 **Falsifiable criterion**: `H/N = ln2 − ⟨ln|O|⟩/N` ⟹ hitting 0.25 exactly requires a typical "
    "orbit size **`⟨|O|⟩ = e^{0.4431N} = 1.557^N`**. The parallel tick dynamics gives ≈ 60 at N = 16, "
    "whereas `1.557^16 ≈ 1.2×10³` ⟹ **off by about a factor 20**.",
    "> ⚠️ **Honest limits**: |G| and the orbit structure are exhaustive only for **N ≤ 16**; larger "
    "lattices carry far more per-line phase freedom (4×4×4 has 513 generators), so the group may be "
    "much larger and **the N → ∞ limit of H/N is undetermined**. The criterion above is N-independent "
    "and directly testable. This round provides **no mechanism** for the observer's resolution.",
    "",
])
sub_once(EN, EN_A, EN_A + "\n" + EN_B40, "EN §4.8 round-40 block")

# ---------------------------------------------------------------- (2) §8.6.3 等分账
ZH_EQA = "\\;\\Longrightarrow\\; \\rho = \\frac{3H_0^2}{8\\pi G}$$"
ZH_EQB = "\n".join([
    "",
    "> **【v2.9 补充（第 40 轮：等分账的地位）】** 本轮给出等分账的机制层说明：",
    "> · **均匀分布（= 等分）是 tick 动力学在每条轨道上的唯一不变测度** —— "
    "数值：把均匀分布施加任意 tick 后**逐项不变** ⟹ **等分不需要动力学热化**；",
    "> · 但轨道有**很多条**（2×2×4 上 1357 条，见 §4.8 第 40 轮块）⟹ **动力学保持轨道**，"
    "不能把系统带到等分 ⟹ **等分是结构性 / 初值的**，与第 21 / 26 轮的结论一致，"
    "本轮给出了机制层理由（不变量的存在）。",
    "> ⚠️ 外推未验证：上述只在 N ≤ 16 上穷举。",
    "",
])
sub_once(ZH, ZH_EQA, ZH_EQA + "\n" + ZH_EQB, "ZH §8.6.3 等分账地位")

EN_EQA = "\\;\\Longrightarrow\\; \\rho = \\frac{3H_0^2}{8\\pi G}$$"
EN_EQB = "\n".join([
    "",
    "> **【v2.9 supplement (round 40: the status of equipartition)】** This round supplies the "
    "mechanism-level account of the equipartition ledger:",
    "> · **The uniform distribution (= equipartition) is the unique invariant measure of the tick "
    "dynamics on each orbit** — numerically, applying any tick to the uniform distribution leaves it "
    "**invariant term by term** ⟹ **equipartition needs no dynamical thermalisation**;",
    "> · but there are **many orbits** (1357 on 2×2×4, see the round-40 block in §4.8) ⟹ **the "
    "dynamics preserves orbits** and cannot bring the system to equipartition ⟹ **equipartition is "
    "structural / an initial condition**, consistent with rounds 21 / 26; this round supplies the "
    "mechanism-level reason (the existence of invariants).",
    "> ⚠️ Extrapolation not verified: the above is exhaustive only for N ≤ 16.",
    "",
])
sub_once(EN, EN_EQA, EN_EQA + "\n" + EN_EQB, "EN §8.6.3 equipartition status")

# ---------------------------------------------------------------- (3) §4.2 47 μm 澄清
ZH_47A = "（小于 l_P 约 61 个量级，物理上不可接受）。"
ZH_47B = ("（小于 l_P 约 61 个量级，物理上不可接受）。**【v2.9 澄清（第 40 轮）】** "
          "该值限制的是**诸元的空间输运**；而统计测度的不变性是**瞬时的、与输运无关**的"
          "（置换 ⟹ 熵守恒 ⟹ 均匀分布自动不变，见 §8.6.3 的第 40 轮补充）⟹ "
          "**等分账可以结构性成立，同时空间上远未热化**，第 21 / 26 轮的担心**解除**。")
sub_once(ZH, ZH_47A, ZH_47B, "ZH §4.2 47μm 澄清")

EN_47A = "some 61 orders below l_P — physically unacceptable."
EN_47B = ("some 61 orders below l_P — physically unacceptable. **【v2.9 clarification (round 40)】** "
          "This value constrains the **spatial transport of the elements**; the invariance of the "
          "statistical measure, by contrast, is **instantaneous and transport-independent** "
          "(a permutation conserves entropy, so the uniform distribution is automatically invariant — "
          "see the round-40 supplement in §8.6.3) ⟹ **equipartition can hold structurally while the "
          "substrate is far from thermalised in space**; the worry of rounds 21 / 26 is **removed**.")
sub_once(EN, EN_47A, EN_47B, "EN §4.2 47 μm clarification")

print("")
print("通过 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
