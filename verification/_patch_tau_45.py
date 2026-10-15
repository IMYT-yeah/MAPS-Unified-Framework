# -*- coding: utf-8 -*-
"""
第 45 轮论文补丁（中英同步，2 项）。

在 §4.9 的 N1–N4 之后、P1–P4 之前插入【v2.9 补充（第 45 轮：观测者周期 τ 判否）】块：
  · N1 只给「相位累积 4π 整数倍」的**量子化条件**，不给 τ 的值
  · 三个候选 τ 各带一个新未知量（R / m / ω）
  · **新判据**：δ ≤ 1 ⟹ τ ≥ t_P/e² = 7.30×10⁻⁴⁵ s
  · 自洽候选 τ = 2π t_P（= l_P 涡周期 = m_Pl 康普顿周期，恒等式）⟹ δ = 0.1468
  · **公设上移 = 无穷回归** ⟹ 建议 B5 停在层 0（δ）

锚点必须恰好命中一次。
"""

import io
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
STAMP = "2026-09-21第45轮前"

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
    dst = os.path.join(HIST, "{}_备份_{}.md".format(stem, STAMP))
    shutil.copy2(src, dst)
    print("  备份 ->", os.path.basename(dst))
print()

ANCHOR_ZH = "**初始微扰来源命题（P1–P4）【v1.5 补充】**"
ANCHOR_EN = "**Initial-perturbation origin propositions (P1–P4)**"

BLOCK_ZH = """**【v2.9 补充（第 45 轮：观测者自身的周期 τ —— 判否，与公设上移的无穷回归）】** 第 40 轮把 B5（观测者读数分辨率 δ）的三条来源全部排除，只留下「观测者自身的周期 τ」（§4.9 N1–N4 的涡动力学）作为唯一入口。本轮攻这个入口。

**① N1 给的是量子化条件，不是 τ 的值**：N1 只说「稳态涡的相位必须累积 4π 的整数倍」，而 τ = 涡走完一个相位周期的时间。三个候选都带新未知量：

| 候选 τ | 新引入的未知量 |
|---|---|
| 涡旋转 `2πR/c`（或 `4πR/c`） | **涡半径 R** |
| 康普顿周期 `h/(mc²)` | **观测者质量 m** |
| 相位累积 `4π/ω` | **角频率 ω** |

⟹ §4.9 **不足以定出 τ**。

**② 新的定量判据**：δ 是读数的可分辨间隔，读数落在 [0,1] ⟹ **δ ≤ 1** ⟹

$$\\tau \\;\\ge\\; \\frac{t_P}{e^2} \\;=\\; 7.2963\\times10^{-45}\\ {\\rm s} \\;=\\; 0.1353\\,t_P$$

（若额外要求 τ ≥ t_P，则 δ ≤ 1/e = 0.3679。）⟹ 任何 τ < t_P/e² 都要求 δ > 1，物理上无意义。

**③ 一个自洽候选（但它是恒等式，不是预言）**：

| 解释 | τ |
|---|---|
| (a) 涡以 c 绕半径 l_P 一圈 | 2π t_P = 3.387420×10⁻⁴³ s |
| (b) 普朗克质量的康普顿周期 | h/(m_Pl c²) = 3.387421×10⁻⁴³ s |

比值 (a)/(b) = **0.999999945** ⟹ 两者是同一个数（因 `m_Pl c² = ℏ/t_P` ⟹ `h/(m_Pl c²) = 2π t_P` 是恒等式）。
取此候选：N_t = 2π ⟹ **δ = 0.146763**，可分辨态数 = e ✓ 自洽。
⚠️ 按第 37 轮四类判定，这归为**一致性**，**不是推导**：任何把观测者取作普朗克尺度孤子的选择都会落到这里。
（对照：若观测者取电子/质子质量的孤子，δ 分别为 9.49×10⁻¹³ / 4.07×10⁻¹¹ —— δ 完全由「观测者是什么」决定。）

**④ 主要结论：公设上移 = 无穷回归**

| 层 | 内容 | 未知量 |
|---|---|---|
| 0 | B5 = 观测者的读数分辨率 δ | {δ} |
| 1 | 时间平均方程 `τ = t_P/(δ²e²)` | {τ}（替换 δ） |
| 2 | 涡动力学 `τ = 2πR/c` 或 `h/(mc²)` | {R} 或 {m}（替换 τ） |
| 3 | R 或 m 由什么定？ | {…} |

每一层都是**一个方程、两个未知量** ⟹ 上移一层**不减少**未知量的个数，只是换一个名字 ⟹ **无穷回归**。
⟹ **B5 不能被推导掉，只能被上移**；要终止回归必须在某一层停下（= 接受该层为公设）。
**本轮建议停在层 0（δ）**：停在其他层没有增益，且 δ 是唯一直接出现在可观测量里的量。

⚠️ 附带：这一条**从根上封死了**上移路线 —— 第 44 轮已证明 tick 的随机性来源不可判定
⟹ 块读数的时间序列性质不可判定 ⟹ 时间平均公式所需的**自相关修正原则上也算不出来**。

"""

BLOCK_EN = """**【v2.9 supplement (round 45: the observer's own period τ — ruled out, and the infinite regress of "moving the postulate up")**】** Round 40 excluded all three sources of B5 (the observer's readout resolution δ) and left only "the observer's own period τ" (the vortex dynamics of §4.9 N1–N4) as the sole entrance. This round attacks that entrance.

**① N1 gives a quantisation condition, not the value of τ**: N1 says only that "a steady vortex must accumulate phase in integer multiples of 4π", whereas τ is the time for the vortex to complete one phase period. All three candidates carry a new unknown:

| candidate for τ | new unknown introduced |
|---|---|
| vortex rotation `2πR/c` (or `4πR/c`) | **vortex radius R** |
| Compton period `h/(mc²)` | **observer mass m** |
| phase accumulation `4π/ω` | **angular frequency ω** |

⟹ §4.9 is **insufficient to fix τ**.

**② A new quantitative criterion**: δ is the distinguishable interval of the readout, and the readout lies in [0,1] ⟹ **δ ≤ 1** ⟹

$$\\tau \\;\\ge\\; \\frac{t_P}{e^2} \\;=\\; 7.2963\\times10^{-45}\\ {\\rm s} \\;=\\; 0.1353\\,t_P$$

(If one additionally demands τ ≥ t_P, then δ ≤ 1/e = 0.3679.) ⟹ any τ < t_P/e² requires δ > 1 and is physically meaningless.

**③ A self-consistent candidate (but it is an identity, not a prediction)**:

| reading | τ |
|---|---|
| (a) vortex going once around radius l_P at speed c | 2π t_P = 3.387420×10⁻⁴³ s |
| (b) Compton period of the Planck mass | h/(m_Pl c²) = 3.387421×10⁻⁴³ s |

Ratio (a)/(b) = **0.999999945** ⟹ the same number (since `m_Pl c² = ℏ/t_P` ⟹ `h/(m_Pl c²) = 2π t_P` is an identity).
Taking this candidate: N_t = 2π ⟹ **δ = 0.146763**, distinguishable states = e ✓ self-consistent.
⚠️ Under the four-way verdict of round 37 this counts as **consistency**, **not a derivation**: any choice that takes the observer to be a Planck-scale soliton lands here.
(Contrast: if the observer were an electron- or proton-mass soliton, δ would be 9.49×10⁻¹³ or 4.07×10⁻¹¹ — δ is entirely fixed by "what the observer is".)

**④ Main conclusion: moving the postulate up is an infinite regress**

| level | content | unknown |
|---|---|---|
| 0 | B5 = observer readout resolution δ | {δ} |
| 1 | time-average equation `τ = t_P/(δ²e²)` | {τ} (replaces δ) |
| 2 | vortex dynamics `τ = 2πR/c` or `h/(mc²)` | {R} or {m} (replaces τ) |
| 3 | what fixes R or m? | {…} |

Every level is **one equation with two unknowns** ⟹ moving up one level does **not** reduce the number of unknowns, it merely renames them ⟹ **infinite regress**.
⟹ **B5 cannot be derived away, only moved up**; ending the regress requires stopping at some level (i.e. accepting that level as a postulate).
**This round recommends stopping at level 0 (δ)**: other levels give no gain, and δ is the only quantity that appears directly in an observable (the readout).

⚠️ Corollary: this **closes the move-up route at its root** — round 44 showed the source of tick randomness is undecidable ⟹ the time-series properties of block readouts are undecidable ⟹ the **autocorrelation correction** needed by the time-average formula is in principle uncomputable.

"""

sub_once(ZH, ANCHOR_ZH, BLOCK_ZH + ANCHOR_ZH, "ZH 插入第 45 轮块")
sub_once(EN, ANCHOR_EN, BLOCK_EN + ANCHOR_EN, "EN 插入第 45 轮块")

print()
print("=" * 70)
print("补丁汇总：成功 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
print("=" * 70)
