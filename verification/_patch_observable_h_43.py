# -*- coding: utf-8 -*-
"""
第 43 轮论文补丁（中英同步，两处 × 2 语言 = 4 项）。

A 段：修正 §8.6.7(c) 的数值表述 —— 第 26 轮原文「⟨r²⟩ 塌到 n 的 29.7% / 42.5%（两个种子）」
      经本轮 20 种子复测为**非自平均**（均值 1.32 n、散布 65%），「塌到」方向亦误。
      物理结论（每线独立为必需条件）不变。
B 段：在【诚实边界（8.6.7）】之前插入【v2.9 补充（第 43 轮：h 不可观测）】块。

锚点必须恰好命中一次，否则拒绝改动。
"""

import io
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
STAMP = "2026-09-21第43轮前"

N_OK = [0]
N_FAIL = [0]


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<34} 命中 {} 次 —— 拒绝".format(tag, n))
        N_FAIL[0] += 1
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<34} 已改".format(tag))
    N_OK[0] += 1


# ---------------------------------------------------------------- 备份
os.makedirs(HIST, exist_ok=True)
for src, stem in ((ZH, "论文初稿_v2.9"), (EN, "Paper_v2.9_EN")):
    dst = os.path.join(HIST, "{}_备份_{}.md".format(stem, STAMP))
    shutil.copy2(src, dst)
    print("  备份 ->", os.path.basename(dst))
print()

# ---------------------------------------------------------------- A 段：修正第 26 轮数值
A_OLD_ZH = ("⟨r²⟩ 塌到 n 的 29.7% / 42.5%（两个种子），而每线独立时为 100.0%。"
            "**故「每线独立」是必需条件，不是实现偏好。**")
A_NEW_ZH = ("⟨r²⟩ 偏离 n 且**不自平均**（第 43 轮用 20 个种子复测：均值 **1.32 n**、"
            "相对散布 **65%**、范围 [0.364, 3.444]；而每线独立时为 **1.001 ± 0.027**，散布仅 **3%**）。"
            "**故「每线独立」是必需条件，不是实现偏好。**"
            "（原文所引「29.7% / 42.5%（两个种子）」系未自平均量的噪声，且「塌到」的方向亦误 —— "
            "该模式下 ⟨r²⟩ 的均值大于 n 而散布巨大。第 43 轮已修正。）")

A_OLD_EN = ("collapsing ⟨r²⟩ to 29.7% / 42.5% of n (two seeds), versus 100.0% for "
            "independent per-line phases. **Per-line independence is therefore a requirement, "
            "not an implementation preference.**")
A_NEW_EN = ("⟨r²⟩ deviating from n and being **not self-averaging** (retested in round 43 with "
            "20 seeds: mean **1.32 n**, relative scatter **65%**, range [0.364, 3.444], versus "
            "**1.001 ± 0.027**, scatter **3%**, for independent per-line phases). "
            "**Per-line independence is therefore a requirement, not an implementation preference.** "
            "(The original figures \"29.7% / 42.5% (two seeds)\" were noise from a non-self-averaging "
            "quantity, and the direction of \"collapsing\" was also wrong: in this mode ⟨r²⟩ has a mean "
            "above n with a huge scatter. Corrected in round 43.)")

print("A 段  修正第 26 轮的相位数值（中 / 英）")
sub_once(ZH, A_OLD_ZH, A_NEW_ZH, "ZH §8.6.7(c) 相位数值")
sub_once(EN, A_OLD_EN, A_NEW_EN, "EN 8.6.7(c) phase figures")
print()

# ---------------------------------------------------------------- B 段：插入第 43 轮块
ANCHOR_ZH = "**【诚实边界（8.6.7）】**"
ANCHOR_EN = "**【Honest boundary (8.6.7)】**"

BLOCK_ZH = """**【v2.9 补充（第 43 轮：h 不可观测 —— T-7 降至「实现亦不可判」，熵增源头改写）】** 第 42 轮设想「§8.6.7 的两种实现给不同扩散系数 ⟹ 用 D 反推 h」。本轮把这个「唯一可观测出口」算到底。

**四类相位模式**（简单立方 L³、周期边界、一次 tick = 沿随机轴的完美匹配；每条线一个相位 φ）：

| 相位模式 | ⟨r²⟩/n（完整格点 L=10, n=2000） | 读法 |
|---|---|---|
| 每线独立随机（主实现） | **1.0310** | 每 tick 恰走一步 ⟹ 扩散 |
| 全局固定（常数相位） | **0.0010**（⟨r²⟩ = 2.00） | **严格有界**（复核第 26 轮 (i)） |
| 每线固定 | 0.3406 | 受抑但非零（第 26 轮未单列） |
| 全局统一（每 tick 重抽） | 0.6130（单种子） | **非自平均**，见下 |
| **确定性 LCG**（H2 的代理） | **1.0075** | 与真随机**同值** |

⚠️ **方法要点**：**单标记轨迹看不出「每线独立」与「全局共享」的差别** —— 标记只见到自己那条线的 φ（实测两者均为 0.9933，逐位相同）。相位共享**只在多诸元关联里**显现 ⟹ 用「单个粒子的输运」判相位模式是无效的。

⚠️ **20 种子统计（3D, L=10, n=2000）**：每线独立 ⟹ 均值 **1.001 ± 0.027**（相对散布 **3%**，自平均）；全局统一 ⟹ 均值 **1.317**、范围 [0.364, 3.444]（相对散布 **65%**，**非自平均**）。⟹ **「30–40%」不是结构值，而是未自平均量的噪声**（据此修正 (c) 段，见上）。

**判决（四条）**：

1. **`h` 不是可观测量**：可观测 = D（**1 个实数**）；微观自由度 = 每 tick 每条线的相位 = **L² 个比特**（宏观 ≈ 7.2×10¹²¹）⟹ **L² 个比特 → 1 个实数**，是欠定而非"难测"。
2. **T-7 的判别入口关闭**：真随机相位（D = 0.9700）与确定性 LCG 相位（D = 1.0704）差 **0.1005 = 1.51σ**（噪声内），而二者 h 差 **120 个数量级**（4.998×10¹²¹ vs 44.36 纳特一次性）⟹ 「用扩散系数交叉检验 h」**不成立**。
3. **D 的判别力边界**：相位「全局固定」（有界）与「全局统一」（非自平均）**可判** ⟹ 第 26 轮排除两种「偷懒」是**可观测的**排除；但**「随机性从哪来」在输运层面完全不可见**。移动率 p 可判（D ∝ p：p = 1/2 ⟹ 0.4727，p = 1/4 ⟹ 0.2487），而 A1 已把 p 钉为 1。
4. **熵增源头改写**：第 42 轮的「熵增源头 = **外生 tick 随机性**」应改为「熵增源头 = **无知**（系综熵）」；「无知从哪来」（**真空抛硬币** H1 还是**我们不知道种子** H2）**在框架内不可判定**。这与第 39 轮「熵增 = 粗粒化 / 不可分辨性的度量」**合流**：注入与粗粒化在可观测层面是同一件事的两种叙事。

⚠️ **T-7 最终口径**：H1 与 H2 在框架的**全部输运预言**上等价 ⟹ T-7 从「本体不可判、实现可判」（第 42 轮）降为「**本体不可判、实现亦不可判**」。唯一还剩的入口是**两点关联函数**（表 2 已指出差别只藏在多体关联里）；若该量亦相同，T-7 可结项。

"""

BLOCK_EN = """**【v2.9 supplement (round 43: h is not observable — T-7 falls to "the implementation is also undecidable", and the source of entropy growth is restated)**】** Round 42 proposed that "the two implementations of §8.6.7 give different diffusion coefficients ⟹ use D to infer h". This round computes that "only observable exit" to the end.

**Four phase modes** (simple cubic L³, periodic boundaries, one tick = perfect matching along a random axis; one phase φ per line):

| Phase mode | ⟨r²⟩/n (full lattice, L=10, n=2000) | Reading |
|---|---|---|
| independent per line (main implementation) | **1.0310** | exactly one step per tick ⟹ diffusion |
| globally fixed (constant phase) | **0.0010** (⟨r²⟩ = 2.00) | **strictly bounded** (matches round 26 (i)) |
| fixed per line | 0.3406 | suppressed but non-zero (not listed in round 26) |
| globally shared (redrawn each tick) | 0.6130 (single seed) | **not self-averaging**, see below |
| **deterministic LCG** (proxy for H2) | **1.0075** | **same value** as true randomness |

⚠️ **Methodological point**: **a single-marker trajectory cannot see the difference between "independent per line" and "globally shared"** — the marker only ever meets the φ of its own line (measured: 0.9933 for both, bit-for-bit). Phase sharing shows up **only in multi-element correlations** ⟹ judging phase modes from the transport of a single particle is invalid.

⚠️ **20-seed statistics (3D, L=10, n=2000)**: independent per line gives mean **1.001 ± 0.027** (relative scatter **3%**, self-averaging); globally shared gives mean **1.317**, range [0.364, 3.444] (relative scatter **65%**, **not self-averaging**). ⟹ **"30–40%" is not a structural value but noise from a non-self-averaging quantity** (the (c) paragraph above is corrected accordingly).

**Rulings (four)**:

1. **`h` is not observable**: the observable is D (**one real number**); the microscopic degrees of freedom are the per-line phases = **L² bits per tick** (macroscopically ≈ 7.2×10¹²¹) ⟹ **L² bits → 1 real number** — underdetermined, not merely "hard to measure".
2. **T-7's discriminating exit is closed**: true-random phases (D = 0.9700) versus deterministic LCG phases (D = 1.0704) differ by **0.1005 = 1.51σ** (within noise), while their h differ by **120 orders of magnitude** (4.998×10¹²¹ versus 44.36 nats once and for all) ⟹ "cross-check h with the diffusion coefficient" **fails**.
3. **Boundary of D's discriminating power**: "globally fixed" (bounded) and "globally shared" (non-self-averaging) **are** distinguishable ⟹ round 26's exclusion of the two shortcuts is an **observable** exclusion; but **"where the randomness comes from" is completely invisible at the transport level**. The mobility p is distinguishable (D ∝ p: p = 1/2 ⟹ 0.4727, p = 1/4 ⟹ 0.2487), and A1 already pins p = 1.
4. **Source of entropy growth restated**: round 42's "source of entropy growth = **exogenous tick randomness**" becomes "source of entropy growth = **ignorance** (ensemble entropy)"; and "where the ignorance comes from" (**a coin flipped in the vacuum**, H1, or **our not knowing the seed**, H2) is **undecidable within the framework**. This **merges** with round 39's "entropy growth = a measure of coarse-graining / indistinguishability": injection and coarse-graining are two narratives of one thing at the observable level.

⚠️ **Final T-7 position**: H1 and H2 agree on **all transport predictions** of the framework ⟹ T-7 falls from "ontology undecidable, implementation decidable" (round 42) to "**ontology undecidable, implementation also undecidable**". The only remaining entrance is the **two-point correlation function** (Table 2 shows the difference lives in multi-body correlations only); if that too agrees, T-7 can be closed.

"""

print("B 段  插入第 43 轮块（中 / 英）")
sub_once(ZH, ANCHOR_ZH, BLOCK_ZH + ANCHOR_ZH, "ZH 插入第 43 轮块")
sub_once(EN, ANCHOR_EN, BLOCK_EN + ANCHOR_EN, "EN 插入第 43 轮块")

print()
print("=" * 70)
print("补丁汇总：成功 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
print("=" * 70)
