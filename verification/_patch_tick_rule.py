# -*- coding: utf-8 -*-
"""
第 26 轮补丁：tick 归一化
  ① §4.2「两个时标的分离」的 47 μm 加口径补注（并行归一化；串行值为 2.7e-96 m）
  ② §8.6 新增 8.6.7「衬底置换模型与 tick 归一化」（含机制、三条排除判据、实现、
     47 μm 口径归属、C-2 升级、诚实边界）
  ③ 修掉 §4.2 悬空的「置换模型（§8.6，第 21 轮）」引用 → 指向 §8.6.7
中英同步。锚点必须恰好命中一次，否则拒绝改动。
"""
import io
import sys

BASE = "C:/Users/Administrator/Desktop/2026-08-20-21-43-34/outputs/"
ZH = BASE + "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN = BASE + "Paper_MatterAntimatterPairStorm_v2.9_EN.md"

ACTIONS = []

def patch(path, old, new, tag):
    s = io.open(path, encoding="utf-8").read()
    n = s.count(old)
    if n != 1:
        print("  [XX] %-46s 锚点命中 %d 次（要求恰好 1 次）——拒绝改动" % (tag, n))
        ACTIONS.append((tag, False))
        return
    io.open(path, "w", encoding="utf-8").write(s.replace(old, new))
    print("  [OK] %-46s 已替换" % tag)
    ACTIONS.append((tag, True))

# ---------------------------------------------------------------- ZH-1
zh_r191 = ("- **② 衬底构型混合（慢）**：R_mix = l_P·√(t/t_P)，"
           "一个哈勃时仅 ≈ 4.7×10⁻⁵ m（**47 μm**，≈ 3.4×10⁻³¹ R_c）。")
zh_r191_new = zh_r191 + (
    "**（v2.9 口径补注）**：该值对应 **并行归一化** —— 每 tick 每个格点恰好一次对换，"
    "即每个诸元的事件率为 1/t_P，与 A1 的 `ν ~ 1/t_P` 同口径（见 §8.6.7）。"
    "若误取「每 tick 全局仅一次对换」的串行归一化，同一公式给出 **2.7×10⁻⁹⁶ m**"
    "（小于 l_P 约 61 个量级，物理上不可接受）。")
patch(ZH, zh_r191, zh_r191_new, "ZH-1 47 μm 口径补注")

# ---------------------------------------------------------------- ZH-2
zh_ref_old = "置换模型（§8.6，第 21 轮）给出两个相差约 10³⁰ 倍的时标"
zh_ref_new = "置换模型（§8.6.7）给出两个相差约 10³⁰ 倍的时标"
patch(ZH, zh_ref_old, zh_ref_new, "ZH-2 修悬空的 §8.6 引用")

# ---------------------------------------------------------------- ZH-3
zh_anchor = "**【诚实边界汇总】**"
zh_867 = """#### 8.6.7 衬底置换模型与 tick 归一化

【推导 + 数值】§4.2 命题链中「配对的湮灭-再生在 50:50 下与弹性散射动力学等价」需要一个具体机制；本小节给出它，并同时固定其**归一化**。

**(a) 机制**：把一个 tick 视为对占据态施加一次**相邻对换**（对称群 S_N 的相邻生成元）。置换是双射 ⟹ 诸元数自动守恒、每格点恒有且仅有 1 个诸元、真空态永不出现（它是逻辑态，不是占据态）；相邻对换生成整个 S_N，且可逆 ⟹ **底层无熵产生，宏观不可逆只能来自粗粒化**。相邻对换 = 全同粒子交换身份 = 一维等质量弹性碰撞（速度互换），故多体层面与弹性散射不可区分。

**(b) tick 归一化（v2.9 新增，重要）**：真正需要裁定的是**每 tick 发生几次对换**，而不是是否同步。A1 的 `ν ~ 1/t_P` 是**每个诸元**的事件率（不是整个系统的事件率），因此

$$\\text{每 tick 每个格点恰好一次事件}\\qquad(\\text{并行归一化})$$

是唯一与 A1 同口径的选择。取「每 tick 全局仅一次对换」（串行归一化）会与三条独立判据冲突：

| 判据 | 并行 | 串行 | 判决 |
|---|---|---|---|
| A1 的 per-诸元事件率 `1/t_P` | `1/t_P` ✓ | `2/(N_c t_P)`，差 `10^182.5` 倍 ✗ | 排除串行 |
| A2 的泄漏份额 `ε₀ = 7.7×10⁻²⁰`（per-事件量） | 直接可用 ✓ | 需放大 `3.06×10¹⁸²` 倍 ⟹ ε₀ ≫ 1 ✗ | 排除串行 |
| §4.2 速度空间弛豫 ~4 次对换 | 4 t_P 内恰 4 次 ✓ | 4 t_P 内被交换概率 `1.3×10⁻¹⁸²` ✗ | 排除串行 |

（`N_c = R_c/l_P = 8.4918×10⁶⁰`、`N_c³ = 6.1236×10¹⁸²`。）

**(c) 实现**：并行归一化下「每个格点恰参与一次」要求把格点按**二分图完美匹配**成对（3D 立方格是二分图；沿所选轴做 odd–even 配对即可）。要同时满足**各向同性**与**真扩散**，必须随机化两件事：

- **轴随机**（每 tick 在 x/y/z 中随机选轴）——固定轴只给一维扩散，另两轴冻结；
- **相位随机**（每条线独立、每 tick 重抽）——相位固定时粒子在轴上的奇偶角色被锁定：走一步即翻转奇偶，下一步便换回另一端，形成二周期振荡、位移有界（数值：⟨r²⟩ = 2，而扩散值为 600）。

数值验证（L = 10、N = 1000 格点、2000 tick）：⟨r²⟩ = 1981.3（= n，偏差 0.9%）、⟨x²⟩:⟨y²⟩:⟨z²⟩ = 672.9 : 694.2 : 614.2（各 ≈ n/3，3σ 内）、真空事件数 = 0、每 tick 保持置换、无净漂移。

**(d) 47 μm 属于哪个口径**：§4.2「两个时标的分离」中慢时标 `R_mix = l_P√(t/t_P) = 47 μm`（一个哈勃时）**正是并行归一化的值**（每 t_P 每诸元一个 l_P 步）。若误取串行归一化，同一表达式变成 `l_P√(2t/(N_c³ t_P)) = 2.7×10⁻⁹⁶ m`，比普朗克长度还小 61 个量级，物理上不可接受。故 47 μm 与 (b) 的裁定互为支撑。

**(e) 代价**：并行归一化定义了**全局同时的 tick**，即衬底存在一个优先参照系。这使 C-2（普朗克尺度的绝对性不得泄漏到 1PN；§4.5b 的 PPN 参数 ξ, α₁, α₂, α₃ 全为 0）成为**必要条件**：A1 的 50:50 与各向同性必须负责抹掉衬底的绝对性。并行使 C-2 从「可选」升为「必需」。

**【诚实边界（8.6.7）】**

| 项 | 性质 |
|---|---|
| 相邻对换机制、置换群性质 | 【推导 + 数值】 |
| 并行归一化的三条排除判据 | 【推导 + 数值】，但依赖「A1 的 ν 为 per-诸元速率」这一读法 |
| 二分图完美匹配 + 轴/相位随机 | 【实现选择】：亦可取「每对独立决定是否交换」（有效移动率 1/2），标度律不变而扩散系数改变；本文取与 A1 同口径者 |
| ⟨r²⟩ = n l_P² | 数值（2D/3D 立方格 + 周期边界，L = 10）；框架未规定格点几何 |
| 「有效自由度 < 格点数」 | 观察（固定轴下种子散布 375~630，远超独立样本 3σ = 27），未做关联长度定量 |
| 相邻性（为何是相邻对换而非三循环） | **未论证**，来自「手递手」图像 |

"""
patch(ZH, zh_anchor, zh_867 + zh_anchor, "ZH-3 新增 §8.6.7")

# ---------------------------------------------------------------- EN-1
en_r186 = ("- **② substrate configurational mixing (slow)**: R_mix = l_P·√(t/t_P), "
           "only ≈ 4.7×10⁻⁵ m (**47 μm**, ≈ 3.4×10⁻³¹ R_c) per Hubble time.")
en_r186_new = en_r186 + (
    " **(v2.9 normalization note)**: this value corresponds to the **parallel normalization** — "
    "exactly one transposition per site per tick, i.e. a per-element event rate of 1/t_P, on the same "
    "footing as A1's `ν ~ 1/t_P` (see §8.6.7). Under the serial normalization (one global transposition "
    "per tick) the same expression gives **2.7×10⁻⁹⁶ m**, some 61 orders below l_P — physically unacceptable.")
patch(EN, en_r186, en_r186_new, "EN-1 47 μm normalization note")

# ---------------------------------------------------------------- EN-2
en_anchor = "**【Honest-boundary summary】**"
en_867 = """#### 8.6.7 Substrate permutation model and the tick normalization

【Derivation + numerics】The claim in §4.2 that "pair annihilation–regeneration under 50:50 is dynamically equivalent to elastic scattering" requires a concrete mechanism; this subsection supplies it and fixes its **normalization**.

**(a) Mechanism**: treat one tick as applying a single **nearest-neighbour transposition** to the occupancy (an adjacent generator of the symmetric group S_N). A transposition is a bijection ⟹ the number of elements is automatically conserved, every site carries exactly one element, and the vacuum state never occurs (it is a logical state, not an occupancy); adjacent transpositions generate all of S_N and are invertible ⟹ **no entropy is produced at the fundamental level, so macroscopic irreversibility must come from coarse-graining**. Nearest-neighbour transposition = identical particles exchanging identity = 1D equal-mass elastic collision (velocity exchange), hence indistinguishable from elastic scattering at the many-body level.

**(b) Tick normalization (new in v2.9; important)**: what actually needs adjudication is **how many transpositions occur per tick**, not whether they are synchronous. A1's `ν ~ 1/t_P` is the event rate **per element** (not for the whole system), so

$$\\text{exactly one event per site per tick}\\qquad(\\text{parallel normalization})$$

is the only choice on the same footing as A1. Taking "one global transposition per tick" (serial normalization) conflicts with three independent criteria:

| Criterion | Parallel | Serial | Verdict |
|---|---|---|---|
| A1 per-element event rate `1/t_P` | `1/t_P` ✓ | `2/(N_c t_P)`, off by `10^182.5` ✗ | serial excluded |
| A2 leakage fraction `ε₀ = 7.7×10⁻²⁰` (per event) | directly usable ✓ | must be amplified by `3.06×10¹⁸²` ⟹ ε₀ ≫ 1 ✗ | serial excluded |
| §4.2 velocity-space relaxation ~4 transpositions | exactly 4 within 4 t_P ✓ | probability `1.3×10⁻¹⁸²` within 4 t_P ✗ | serial excluded |

(`N_c = R_c/l_P = 8.4918×10⁶⁰`, `N_c³ = 6.1236×10¹⁸²`.)

**(c) Implementation**: under parallel normalization, "every site participates exactly once per tick" requires pairing sites into a **bipartite perfect matching** (the 3D cubic lattice is bipartite; odd–even pairing along the chosen axis suffices). Isotropy and true diffusion require randomizing two things:

- **random axis** (x/y/z chosen at random each tick) — a fixed axis gives one-dimensional diffusion with the other two axes frozen;
- **random phase** (independently redrawn per line each tick) — with a fixed phase, a particle's parity role on that axis is locked: one step flips its parity, so the next step sends it back, producing a two-cycle oscillation with bounded displacement (numerically ⟨r²⟩ = 2 against a diffusive value of 600).

Numerical verification (L = 10, N = 1000 sites, 2000 ticks): ⟨r²⟩ = 1981.3 (= n, deviation 0.9%), ⟨x²⟩:⟨y²⟩:⟨z²⟩ = 672.9 : 694.2 : 614.2 (each ≈ n/3, within 3σ), zero vacuum events, permutation preserved every tick, no net drift.

**(d) Which normalization the 47 μm belongs to**: the slow timescale `R_mix = l_P√(t/t_P) = 47 μm` per Hubble time in §4.2 **is the parallel-normalization value** (one l_P step per element per t_P). Under the serial normalization the same expression becomes `l_P√(2t/(N_c³ t_P)) = 2.7×10⁻⁹⁶ m`, sixty-one orders below the Planck length — physically unacceptable. The 47 μm figure and the ruling in (b) therefore support each other.

**(e) Price**: parallel normalization defines a **globally simultaneous tick**, i.e. a preferred frame for the substrate. This makes C-2 (Planck-scale absoluteness must not leak into 1PN; the PPN parameters ξ, α₁, α₂, α₃ all vanish in §4.5b) a **necessary condition**: A1's 50:50 and isotropy must be what erases the substrate's absoluteness. Parallel updating promotes C-2 from optional to required.

**【Honest boundary (8.6.7)】**

| Item | Nature |
|---|---|
| nearest-neighbour transposition mechanism, permutation-group properties | 【Derivation + numerics】 |
| the three exclusion criteria for parallel normalization | 【Derivation + numerics】, but rely on reading A1's ν as a per-element rate |
| bipartite perfect matching + random axis/phase | 【implementation choice】: "each pair independently decides whether to swap" (effective mobility 1/2) is also viable — scaling law unchanged, diffusion coefficient changed; we take the A1-commensurate one |
| ⟨r²⟩ = n l_P² | numerics (2D/3D cubic lattice + periodic boundaries, L = 10); the framework does not fix the lattice geometry |
| "effective degrees of freedom < number of sites" | observation (fixed-axis seed spread 375–630, far beyond the independent-sample 3σ = 27); no quantitative correlation length yet |
| adjacency (why nearest-neighbour rather than a 3-cycle) | **not argued**, inherited from the "hand-to-hand" picture |

"""
patch(EN, en_anchor, en_867 + en_anchor, "EN-2 新增 §8.6.7")

# ---------------------------------------------------------------- 汇总
print("\n" + "=" * 70)
ok = sum(1 for _, v in ACTIONS if v)
bad = len(ACTIONS) - ok
print("补丁动作 %d 项，成功 %d，失败 %d" % (len(ACTIONS), ok, bad))
for t, v in ACTIONS:
    if not v:
        print("  [XX] %s" % t)
sys.exit(0 if bad == 0 else 1)
