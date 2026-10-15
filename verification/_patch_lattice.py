# -*- coding: utf-8 -*-
"""第 27 轮补丁：格点几何 = 金刚石结构
  ① 修正 §4.2 的数密度/碰撞率（金刚石结构给 0.6495/l_P³）
  ② §8.6 新增 8.6.8「衬底格点几何」
中英同步；锚点必须恰好命中一次。"""
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
        print("  [XX] %-40s 锚点命中 %d 次 —— 拒绝改动" % (tag, n))
        ACTIONS.append((tag, False))
        return
    io.open(path, "w", encoding="utf-8").write(s.replace(old, new))
    print("  [OK] %-40s 已替换" % tag)
    ACTIONS.append((tag, True))

# ---------------------------------------------------------------- ZH-1
zh_old = ("- **① 速度空间弛豫（快）**：满占位衬底的数密度 n = 1/l_P³、截面 σ = l_P²、速率 c ⟹ "
          "碰撞率 nσv = **1/t_P = 1.85×10⁴³ s⁻¹**、平均自由程 = **l_P**，")
zh_new = ("- **① 速度空间弛豫（快）**：**金刚石结构**衬底的数密度 n = **0.6495/l_P³**（见 §8.6.8）、"
          "截面 σ = l_P²、速率 c ⟹ 碰撞率 nσv = **0.6495/t_P = 1.20×10⁴³ s⁻¹**、"
          "平均自由程 = **1.5396 l_P**，")
patch(ZH, zh_old, zh_new, "ZH-1 §4.2 数密度修正")

# ---------------------------------------------------------------- ZH-2
zh_868 = """#### 8.6.8 衬底格点几何：4 邻居 + 二分性唯一锁定金刚石结构

【推导 + 数值】§8.6.7 把 tick 归一化定为「每 tick 每个格点恰好一次事件」之后，格点几何不再是自由选择：本小节说明它被**结构性地**定下来。

**(a) 硬约束**：一个 tick 里的全部相邻对换构成一个**完美匹配**（每顶点恰覆盖一次）。若要求每个方向都能轮到（各向同性），则全部边要被 d 个完美匹配覆盖 ⟹ 图必须是 **d-正则二分图**；由 **König 边着色定理**，其边恰可 d 色染色，每种颜色是一个完美匹配。两条纯结构约束：① 配位数 d = 方向数 k；② 邻接图必须**二分**（否则完美匹配不保证覆盖全部顶点）。

**(b) 唯一候选**：配位数 × 二分性筛选——

| 几何 | 配位数 | 二分? | 与 k = 4 相容? |
|---|---|---|---|
| 简单立方 | 6 | ✓ | ✗ |
| 体心立方 | 8 | ✓ | ✗ |
| 面心立方 | 12 | ✗（含三角形） | ✗ |
| 蜂巢 | 3 | ✓ | ✗ |
| **金刚石** | **4** | **✓** | **✓ 唯一** |

配位数 4 不是本节新引入的：§4.10「六处「4」同源」第一条即「**表面诸元 4 邻居**（观测者几何，本框架推论）」，而定理 2 已证「4 点最优构型 = 正四面体」。**把这两条既有设定与 tick 的二分要求放在一起，几何被唯一确定。**

**(c) 构造与 König 边着色**：取两子格 A = {(i,j,k) : i+j+k 偶}（fcc 的整数表示）、B = {奇}，键沿正四面体 4 方向 d₁=(1,1,1)、d₂=(1,−1,−1)、d₃=(−1,1,−1)、d₄=(−1,−1,1)。数值（L = 8，512 格点）：|A| = |B| = 256；A 沿任一 dᵤ 必落到 B（二分）；**4 个方向的边集各是一个完美匹配**（König 的具体实现）。

**(d) 各向同性内建**：Σ_μ d_μ ⊗ d_μ = 4·I（非对角元全为 0）⟹ 方向等概率时位移二阶矩自动各向同性，无需额外假设。键方向夹角 arccos(−1/3) = **109.4712206°**，与定理 2 的 Tammes 值逐位相同。

**(e) 数值验证**（L = 8、N = 512、1500 tick、5 种子）：⟨x²⟩ = 1487.3、⟨y²⟩ = 1438.6、⟨z²⟩ = 1441.9（期望各 n = 1500）、⟨r²⟩ = 4367.8（期望 3n = 4500）、真空事件 0、非置换 tick 0。

**(f) ⚠️ 匹配必须局域随机化**：只用「每 tick 全局选一个键方向、沿该方向交换所有边」，会让整个衬底**刚性平移**（5 种子 ⟨r²⟩/3n 在 0.13~1.09 间乱跳、分量比可达 5.3），因为所有状态共享同一条方向序列。修复办法与 §8.6.7 同源：**每条链独立抽取 odd–even 相位**。⟹ **「全局同步 = 整体刚性平移，不是随机游走」**，在两种几何上独立重现。

**(g) ⚠️ 数密度与嵌入**：要求「一步 l_P / 一拍 t_P ⟹ v = c」即**键长 = l_P**。标准金刚石（8 原子/晶胞，a = 4l_P/√3）给 n = 3√3/(8l_P³) = **0.6495/l_P³**；ℤ³ 对角键嵌入给 5.196/l_P³（相差 8 倍）。按「**最近邻即键**」判据取前者 ⟹ (上述 ①) 的碰撞率相应修正为 **0.6495/t_P**、平均自由程 **1.5396 l_P**（量级结论「O(1/t_P)、O(l_P)」不变）。

**【诚实边界（8.6.8）】**

| 项 | 性质 |
|---|---|
| 结构约束（d-正则二分 + König）、构造、夹角、Σd⊗d = 4I | 【推导 + 数值】，精确 |
| 「配位 4 + 二分 ⟹ 金刚石」 | 【推导 + 数值】，但**依赖「表面 4 邻居 = 体配位数」这一步**（§4.10 那句写在表面/观测者几何层面） |
| tick 模拟数值 | 【数值】（立方坐标 + 周期边界，L = 8） |
| 「全局同步 = 刚性」 | 【数值观察】，两种几何上重现，无解析证明 |
| 数密度 0.6495/l_P³ | 【依赖嵌入选择】，判据是「最近邻即键」（物理偏好，非证明） |
| **相邻性（对换 vs 三循环）** | **仍未论证** |

"""
patch(ZH, "**【诚实边界汇总】**", zh_868 + "**【诚实边界汇总】**", "ZH-2 新增 §8.6.8")

# ---------------------------------------------------------------- EN-1
en_old = ("- **① velocity-space relaxation (fast)**: with a fully occupied substrate, n = 1/l_P³, "
          "σ = l_P², v = c ⟹ collision rate nσv = **1/t_P = 1.85×10⁴³ s⁻¹**, mean free path = **l_P**;")
en_new = ("- **① velocity-space relaxation (fast)**: in the **diamond-structure** substrate "
          "n = **0.6495/l_P³** (see §8.6.8), σ = l_P², v = c ⟹ collision rate "
          "nσv = **0.6495/t_P = 1.20×10⁴³ s⁻¹**, mean free path = **1.5396 l_P**;")
patch(EN, en_old, en_new, "EN-1 §4.2 density fix")

# ---------------------------------------------------------------- EN-2
en_868 = """#### 8.6.8 Substrate lattice geometry: 4 neighbours + bipartiteness uniquely fix diamond

【Derivation + numerics】Once §8.6.7 fixes the tick normalization to "exactly one event per site per tick", the lattice geometry is no longer a free choice — this subsection shows it is fixed **structurally**.

**(a) Hard constraints**: all nearest-neighbour transpositions within one tick form a **perfect matching** (every vertex covered exactly once). Requiring every direction to occur (isotropy) means the edges must be covered by d perfect matchings ⟹ the graph must be **d-regular and bipartite**; by **König's edge-colouring theorem** its edges are exactly d-colourable, each colour being a perfect matching. Two purely structural constraints: (i) coordination number d = number of directions k; (ii) the adjacency graph must be **bipartite** (otherwise a perfect matching need not cover all vertices).

**(b) Unique candidate**: filtering by coordination number × bipartiteness —

| Geometry | Coordination | Bipartite? | Compatible with k = 4? |
|---|---|---|---|
| simple cubic | 6 | ✓ | ✗ |
| body-centred cubic | 8 | ✓ | ✗ |
| face-centred cubic | 12 | ✗ (contains triangles) | ✗ |
| honeycomb | 3 | ✓ | ✗ |
| **diamond** | **4** | **✓** | **✓ unique** |

Coordination 4 is not introduced here: §4.10's "six occurrences of 4" already lists "**4 neighbours of a surface element** (observer geometry, framework corollary)", and Theorem 2 proves "optimal 4-point configuration = regular tetrahedron". **Combining these two pre-existing statements with the tick's bipartiteness requirement fixes the geometry.**

**(c) Construction and König edge-colouring**: take sublattices A = {(i,j,k) : i+j+k even} (an integer representation of fcc) and B = {odd}, with bonds along the four tetrahedral directions d₁=(1,1,1), d₂=(1,−1,−1), d₃=(−1,1,−1), d₄=(−1,−1,1). Numerics (L = 8, 512 sites): |A| = |B| = 256; A always lands in B along any dᵤ (bipartite); **the edges of each of the 4 directions form a perfect matching** (König realised).

**(d) Isotropy is built in**: Σ_μ d_μ ⊗ d_μ = 4·I (all off-diagonal entries zero) ⟹ with directions equiprobable the second moment of the displacement is automatically isotropic, with no extra assumption. The bond angle arccos(−1/3) = **109.4712206°** matches Theorem 2's Tammes value digit for digit.

**(e) Numerical verification** (L = 8, N = 512, 1500 ticks, 5 seeds): ⟨x²⟩ = 1487.3, ⟨y²⟩ = 1438.6, ⟨z²⟩ = 1441.9 (expected n = 1500 each), ⟨r²⟩ = 4367.8 (expected 3n = 4500), zero vacuum events, zero non-permutation ticks.

**(f) ⚠️ The matching must be locally randomised**: using only "pick one bond direction globally per tick and swap along all its edges" makes the entire substrate **rigidly translate** (5 seeds give ⟨r²⟩/3n scattered over 0.13–1.09, component ratio up to 5.3), because all states share one direction sequence. The fix is the same as in §8.6.7: **draw an odd–even phase independently per chain**. ⟹ **"Global synchrony = rigid translation, not a random walk"**, reproduced independently on two different geometries.

**(g) ⚠️ Number density depends on the embedding**: "one l_P step per t_P ⟹ v = c" requires **bond length = l_P**. Standard diamond (8 atoms per cell, a = 4l_P/√3) gives n = 3√3/(8l_P³) = **0.6495/l_P³**; the ℤ³ diagonal-bond embedding gives 5.196/l_P³ (a factor 8 apart). Using the "**nearest neighbour = bond**" criterion we take the former ⟹ the collision rate in ① becomes **0.6495/t_P** and the mean free path **1.5396 l_P** (the order-of-magnitude conclusions "O(1/t_P), O(l_P)" are unchanged).

**【Honest boundary (8.6.8)】**

| Item | Nature |
|---|---|
| structural constraints (d-regular bipartite + König), construction, angle, Σd⊗d = 4I | 【Derivation + numerics】, exact |
| "coordination 4 + bipartite ⟹ diamond" | 【Derivation + numerics】, but relies on the step "**surface 4 neighbours = bulk coordination number**" (§4.10 states it at the surface/observer level) |
| tick simulation numbers | 【numerics】 (cubic coordinates + periodic boundaries, L = 8) |
| "global synchrony = rigidity" | 【numerical observation】, reproduced on two geometries, no analytic proof |
| density 0.6495/l_P³ | 【depends on the embedding choice】; criterion is "nearest neighbour = bond" (a physical preference, not a proof) |
| **adjacency (transposition vs 3-cycle)** | **still unargued** |

"""
patch(EN, "**【Honest-boundary summary】**", en_868 + "**【Honest-boundary summary】**", "EN-2 add 8.6.8")

print("\n" + "=" * 66)
ok = sum(1 for _, v in ACTIONS if v)
print("补丁动作 %d 项，成功 %d，失败 %d" % (len(ACTIONS), ok, len(ACTIONS) - ok))
sys.exit(0 if ok == len(ACTIONS) else 1)
