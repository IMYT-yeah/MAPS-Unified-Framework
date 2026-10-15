# -*- coding: utf-8 -*-
"""
第 44 轮论文补丁（中英同步，2 项）。

在【诚实边界（8.6.7）】之前插入【v2.9 补充（第 44 轮：两点关联亦不可判 —— T-7 收口）】块：
  · 三档「随机性来源」的对照（真随机源 / 高质量确定性 / 低质量确定性）
  · 空间关联不可判（0.14σ）、时间关联只判「质量」
  · 周期性判据失效（位移不按驱动周期重复）
  · T-7 最终口径：框架内不可判定

锚点必须恰好命中一次，否则拒绝改动。
"""

import io
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
STAMP = "2026-09-21第44轮前"

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


os.makedirs(HIST, exist_ok=True)
for src, stem in ((ZH, "论文初稿_v2.9"), (EN, "Paper_v2.9_EN")):
    shutil.copy2(src, os.path.join(HIST, "{}_备份_{}.md".format(stem, STAMP)))
    print("  备份 ->", os.path.basename(os.path.join(HIST, "{}_备份_{}.md".format(stem, STAMP))))
print()

ANCHOR_ZH = "**【诚实边界（8.6.7）】**"
ANCHOR_EN = "**【Honest boundary (8.6.7)】**"

BLOCK_ZH = """**【v2.9 补充（第 44 轮：两点关联亦不可判 —— T-7 收口）】** 第 43 轮判否单体输运量后指出「若有差别只能藏在多体关联里」。本轮把关联算出来，**关联同样不可判**。

⚠️ **方法前提**：**数值模拟里的「真随机」也只能是伪随机**（除非用 `os.urandom`）。故本轮比较三档：
`sys` = 真随机源（H1 的严格版本）；`indep` = MT19937（**确定性但高质量**，H2 的好代理）；`lcg` = 线性同余发生器（**确定性且低质量**，H2 的差代理）。

**空间关联**（`C = ⟨Δ_i·Δ_j⟩/⟨r²⟩`，完整格点 L = 6、n = 1200、5 种子）：

| 模式 | C_near(d=1) | C_far(d≥3) |
|---|---|---|
| 真随机源（H1） | **−0.03943** | −0.00460 |
| MT19937（H2 好代理） | **−0.03368** | −0.00245 |
| LCG（H2 差代理） | **−0.06014** | +0.00128 |

⟹ 真随机源 vs 高质量确定性差 **0.14σ**；vs 低质量确定性差 **0.42σ** —— **均在噪声内**。
关键：关联量**不为零**（≈ −0.04）⟹ 置换的排他性确实产生位移关联 ⟹ 「不可判」**不是因为可观测量太弱**。

**时间关联**（`C(τ) = ⟨Δ(t)Δ(t+τ)⟩/⟨Δ²⟩`，L = 4、n = 4000）：

| 模式 | C(τ=1) |
|---|---|
| 真随机源 | −0.0090 |
| MT19937（高质量） | **−0.0009**（与真随机源一致） |
| LCG（低质量） | **−0.3339**（≈ 真随机源的 37 倍） |

⟹ 时间关联能区分**低质量**生成器，**区分不了高质量**生成器 ⟹ 它判的是
**伪随机数发生器的质量**，而**不是**「随机性是否外生」。

⚠️ **周期性判据失效**（本轮的负面发现）：设 H2 的相位与轴**都**由有限状态生成器驱动（周期 256 tick），
则自相关在 τ = 256 处为 **−0.3269**，而严格周期的标志应是 **C(T) ≈ +1**。
⟹ **位移序列不按驱动周期重复**：位移 = 位置之差，而诸元位置持续演化、不会回到起点
⟹ 驱动序列的周期**不会原样传递**到位移上。（保留：τ = 256 处的 |C| = 0.327 仍远大于真随机源水平
⟹ 相关结构在长时标留下痕迹 ⟹ 低质量 H2 仍可区分。）

**T-7 最终口径**：已判否的入口为 ① 熵密度（第 42 轮）、② 扩散系数 D（第 43 轮）、
③ **空间**两点关联（本轮 0.14σ）、④ **周期性**（本轮，被状态演化掩盖）；
唯一成功的 ⑤ **时间**关联只对低质量生成器有效。⟹ 按第 37 轮四类判定，
**T-7 归为「框架内不可判定」**：它退化为伪随机数发生器的质量问题，**不是一个物理问题** ——
框架没有、也不可能规定 tick 用的是哪一档生成器。**现行表述（H1）下 = 不可预测**
（未来不是当前状态的函数）。

"""

BLOCK_EN = """**【v2.9 supplement (round 44: two-point correlations are also undecidable — T-7 is closed)**】** After round 43 ruled out single-body transport and noted that "any difference must hide in many-body correlations", this round computes those correlations: they are **equally undecidable**.

⚠️ **Methodological premise**: **"true randomness" in a numerical simulation is itself pseudo-random** (unless one uses `os.urandom`). This round therefore compares three tiers: `sys` = a true random source (the strict version of H1); `indep` = MT19937 (**deterministic but high-quality**, a good proxy for H2); `lcg` = a linear congruential generator (**deterministic and low-quality**, a poor proxy for H2).

**Spatial correlations** (`C = ⟨Δ_i·Δ_j⟩/⟨r²⟩`, full lattice L = 6, n = 1200, 5 seeds):

| mode | C_near(d=1) | C_far(d≥3) |
|---|---|---|
| true random source (H1) | **−0.03943** | −0.00460 |
| MT19937 (good H2 proxy) | **−0.03368** | −0.00245 |
| LCG (poor H2 proxy) | **−0.06014** | +0.00128 |

⟹ true source versus high-quality determinism differs by **0.14σ**; versus low-quality determinism by **0.42σ** — **both within noise**. Crucially, the correlation is **not zero** (≈ −0.04): the exclusion inherent in a transposition does produce displacement correlations ⟹ "undecidable" is **not** due to a weak observable.

**Temporal correlations** (`C(τ) = ⟨Δ(t)Δ(t+τ)⟩/⟨Δ²⟩`, L = 4, n = 4000):

| mode | C(τ=1) |
|---|---|
| true random source | −0.0090 |
| MT19937 (high-quality) | **−0.0009** (agrees with the true source) |
| LCG (low-quality) | **−0.3339** (≈ 37× the true source) |

⟹ Temporal correlations distinguish **low-quality** generators but **not high-quality** ones ⟹ they test the **quality of the pseudo-random generator**, **not** whether the randomness is exogenous.

⚠️ **The periodicity test fails** (a negative finding of this round): driving **both** the phases and the axis by a finite-state generator (period 256 ticks) gives an autocorrelation of **−0.3269** at τ = 256, whereas strict periodicity requires **C(T) ≈ +1**. ⟹ **The displacement sequence does not repeat with the driving period**: displacement is a difference of positions, and positions keep evolving without ever returning to the start ⟹ the period of the driving sequence is **not transferred verbatim** to the displacement. (Caveat: |C| = 0.327 at τ = 256 still far exceeds the true-source level ⟹ correlation structure does leave a trace at long lags ⟹ low-quality H2 remains distinguishable.)

**Final T-7 position**: the ruled-out entrances are ① entropy density (round 42), ② the diffusion coefficient D (round 43), ③ **spatial** two-point correlations (this round, 0.14σ), and ④ **periodicity** (this round, masked by state evolution); the only successful test, ⑤ **temporal** correlations, works only for low-quality generators. ⟹ Under the four-way verdict of round 37, **T-7 is "undecidable within the framework"**: it degenerates into a question about the quality of a pseudo-random generator, **not a physical question** — the framework does not, and cannot, stipulate which tier of generator the tick uses. **Under the current formulation (H1) the answer is: unpredictable** (the future is not a function of the present state).

"""

sub_once(ZH, ANCHOR_ZH, BLOCK_ZH + ANCHOR_ZH, "ZH 插入第 44 轮块")
sub_once(EN, ANCHOR_EN, BLOCK_EN + ANCHOR_EN, "EN 插入第 44 轮块")

print()
print("=" * 70)
print("补丁汇总：成功 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
print("=" * 70)
