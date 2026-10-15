# -*- coding: utf-8 -*-
"""第 30 轮补丁：T-6 裁决落地
  ① §4.2 数密度/碰撞率恢复 1/l_P³ 与 1/t_P（撤回第 27 轮的金刚石修正）
  ② §8.6.8 整节改写为「外空间 6 方向 ⟹ 简单立方」（撤回金刚石）
中英同步。"""
import io
import sys

BASE = "C:/Users/Administrator/Desktop/2026-08-20-21-43-34/outputs/"
ZH = BASE + "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN = BASE + "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
ACTIONS = []

def patch(path, old, new, tag, expect=1):
    s = io.open(path, encoding="utf-8").read()
    n = s.count(old)
    if n != expect:
        print("  [XX] %-34s 锚点命中 %d 次（期望 %d）—— 拒绝改动" % (tag, n, expect))
        ACTIONS.append((tag, False))
        return
    io.open(path, "w", encoding="utf-8").write(s.replace(old, new))
    print("  [OK] %-34s 已替换" % tag)
    ACTIONS.append((tag, True))

# ---------------------------------------------------------------- ZH-1
zh_1_old = ("- **① 速度空间弛豫（快）**：**金刚石结构**衬底的数密度 n = **0.6495/l_P³**（见 §8.6.8）、"
            "截面 σ = l_P²、速率 c ⟹ 碰撞率 nσv = **0.6495/t_P = 1.20×10⁴³ s⁻¹**、"
            "平均自由程 = **1.5396 l_P**，")
zh_1_new = ("- **① 速度空间弛豫（快）**：满占位衬底（**简单立方**，见 §8.6.8）的数密度 n = **1/l_P³**、"
            "截面 σ = l_P²、速率 c ⟹ 碰撞率 nσv = **1/t_P = 1.85×10⁴³ s⁻¹**、"
            "平均自由程 = **l_P**，")
patch(ZH, zh_1_old, zh_1_new, "ZH-1 §4.2 数密度恢复")

# ---------------------------------------------------------------- ZH-2
zh_new_sec = """#### 8.6.8 衬底格点几何：外空间 6 方向 ⟹ 简单立方（T-6 裁决，第 30 轮）

> **【v2.9 裁决：撤回本小节初稿的「金刚石」】** 初稿（第 27 轮）据「配位数 = 方向簇 k = 4」定为金刚石结构。
> 第 30 轮追溯后发现该步**不成立**：§4.10 论证 4 明确区分两套方向 ——「正四面体 4 方向 = **内空间**分量结构；
> **八面体 6 方向 = 外空间轴结构（3 轴 ±）**；熵编码用内空间分量 ⟹ 方向簇数 4」。
> ⟹ **格点衬底在外空间 ⟹ 配位数 6 ⟹ 简单立方**；「方向簇 k = 4」属**内空间/熵编码**层面，不决定格点配位数。
> §4.9 引理 1「平面内 4 方向 + 平面外 2 方向被卷曲」正是"6 个邻居中 4 个可用于信息传递"的说法，两者自洽。

**(a) 硬约束（保留）**：一个 tick 里的全部相邻对换构成一个**完美匹配**（每顶点恰覆盖一次）。若要求每个方向都能轮到（各向同性），则全部边要被 d 个完美匹配覆盖 ⟹ 图必须是 **d-正则二分图**；由 **König 边着色定理**，其边恰可 d 色染色，每种颜色是一个完美匹配。

**(b) 裁决后的几何**：外空间轴结构 = 3 轴 ± ⟹ **简单立方格**，配位数 **6**、二分（棋盘格着色）。数值（L = 8）：n = 512、A = B = 256、m = 3n = 1536。

**(c) König 边着色的具体实现**：**3 轴 × 2 相位 = 6 个完美匹配**（每个格点恰覆盖一次，6 × n/2 = m ✓）。每 tick 随机选 (轴, 相位)，沿该轴按相位做 odd–even 配对并交换。

**(d) 数密度与碰撞率（恢复原值）**：简单立方格距 = l_P ⟹ n = **1/l_P³**、碰撞率 nσv = **1/t_P**（σ = l_P²；残差 1.2×10⁻⁷ 来自 l_P、t_P 各自舍入到 7 位）、平均自由程 = **l_P**。
⟹ 初稿基于金刚石改的 0.6495/l_P³、0.6495/t_P、1.5396 l_P **一并撤回**；同时"键长 = l_P ⟹ 数密度依赖嵌入（0.6495 与 5.196 相差 8 倍）"那个歧义**在简单立方上根本不存在**。

**(e) 数值验证**（L = 8、N = 512、1500 tick、5 种子）：⟨x²⟩ = 498.95、⟨y²⟩ = 493.42、⟨z²⟩ = 506.70（期望各 n/3 = 500）、⟨r²⟩ = 1499.07（期望 n = 1500）、真空事件 0、非置换 tick 0。

**(f) ⚠️ 匹配必须局域随机化**：只用"每 tick 全局选一个方向、沿该方向交换所有边"会让整个衬底**刚性平移**，因为所有状态共享同一条方向序列。修复：**每条线独立抽取 odd–even 相位**。⟹ **「全局同步 = 整体刚性平移，不是随机游走」**，在简单立方与金刚石两种几何上独立重现。

**(g) 6-正则二分图同样非平面**：二分平面图要求 `m ≤ 2n − 4`，而 6-正则给 `m = 3n` ⟹ 矛盾（n = 512、m = 1536、上界 1020）。⟹ **四色定理（只对平面图说话）对衬底图不适用**；若当"地图"看，色数按 Heawood 由**亏格**定，与配位数无关（见 §4.10 的 LST/Borsuk 辨析）。

**【诚实边界（8.6.8）】**

| 项 | 性质 |
|---|---|
| 结构约束（d-正则二分 + König）、简单立方的 6 个完美匹配、tick 数值 | 【推导 + 数值】 |
| 「外空间 6 方向 ⟹ 简单立方」 | 【判定】，依据 §4.10 论证 4 + §4.9 引理 1 的**原文**；但论文未明说"格点 = 简单立方" |
| 格距 = l_P | 【本框架设定的自然选择】（l_P 是唯一长度标度），非强制推导 |
| 「全局同步 = 刚性」 | 【数值观察】，两种几何上重现，无解析证明 |
| 「每线独立相位」 | 【数值必要条件】 |
| 格点是否必须是周期排列的"格" | **未论证**（框架只给了"外空间 3 轴 ±"） |
| 「平面外 2 方向被卷曲」的具体含义 | 【本框架设定】，本文读作"6 个邻居中 4 个可用于信息传递" |

"""

# ---------------------------------------------------------------- EN-1
en_1_old = ('- **① velocity-space relaxation (fast)**: in the **diamond-structure** substrate '
            'n = **0.6495/l_P³** (see §8.6.8), σ = l_P², v = c ⟹ collision rate '
            'nσv = **0.6495/t_P = 1.20×10⁴³ s⁻¹**, mean free path = **1.5396 l_P**;')
en_1_new = ('- **① velocity-space relaxation (fast)**: in the fully occupied (**simple-cubic**) substrate '
            '(see §8.6.8) n = **1/l_P³**, σ = l_P², v = c ⟹ collision rate '
            'nσv = **1/t_P = 1.85×10⁴³ s⁻¹**, mean free path = **l_P**;')
patch(EN, en_1_old, en_1_new, "EN-1 §4.2 density restored")

# ---------------------------------------------------------------- EN-2
en_new_sec = """#### 8.6.8 Substrate lattice geometry: 6 exterior-space directions ⟹ simple cubic (T-6 verdict, round 30)

> **【v2.9 verdict: the "diamond" of the earlier draft is withdrawn】** The earlier draft of this subsection (round 27) fixed the diamond structure from "coordination number = direction-cluster number k = 4". Round 30 traced this back and found that step **does not hold**: §4.10 Argument 4 explicitly separates two direction sets — "regular-tetrahedron 4 directions = **interior-space** component structure; **octahedral 6 directions = exterior-space axis structure (3 axes ±)**; entropy encoding uses interior-space components ⟹ direction-cluster number 4".
> ⟹ **The substrate lattice lives in exterior space ⟹ coordination number 6 ⟹ simple cubic**; the "direction-cluster k = 4" belongs to the **interior-space / entropy-encoding** level and does not fix the lattice coordination number.
> §4.9 Lemma 1 ("4 in-plane directions + 2 out-of-plane directions curled up") is exactly the statement "4 of the 6 neighbours are available for information transfer" — the two are consistent.

**(a) Hard constraints (retained)**: all nearest-neighbour transpositions within one tick form a **perfect matching** (every vertex covered exactly once). Requiring every direction to occur (isotropy) means the edges must be covered by d perfect matchings ⟹ the graph must be **d-regular and bipartite**; by **König's edge-colouring theorem** its edges are exactly d-colourable, each colour being a perfect matching.

**(b) Geometry after the verdict**: exterior-space axis structure = 3 axes ± ⟹ **simple-cubic lattice**, coordination number **6**, bipartite (checkerboard colouring). Numerics (L = 8): n = 512, A = B = 256, m = 3n = 1536.

**(c) König edge-colouring realised**: **3 axes × 2 phases = 6 perfect matchings** (each vertex covered exactly once; 6 × n/2 = m ✓). Each tick draws an (axis, phase) at random and swaps along that axis in odd–even pairs.

**(d) Number density and collision rate (original values restored)**: simple-cubic lattice spacing = l_P ⟹ n = **1/l_P³**, collision rate nσv = **1/t_P** (σ = l_P²; residual 1.2×10⁻⁷ from l_P and t_P each being rounded to 7 digits), mean free path = **l_P**.
⟹ The diamond-based 0.6495/l_P³, 0.6495/t_P and 1.5396 l_P of the earlier draft are **withdrawn together**; and the ambiguity "bond length = l_P ⟹ density depends on the embedding (0.6495 vs 5.196, a factor 8 apart)" **does not arise for simple cubic**.

**(e) Numerical verification** (L = 8, N = 512, 1500 ticks, 5 seeds): ⟨x²⟩ = 498.95, ⟨y²⟩ = 493.42, ⟨z²⟩ = 506.70 (expected n/3 = 500 each), ⟨r²⟩ = 1499.07 (expected n = 1500), zero vacuum events, zero non-permutation ticks.

**(f) ⚠️ The matching must be locally randomised**: using only "pick one direction globally per tick and swap along all its edges" makes the entire substrate **rigidly translate**, because all states share one direction sequence. Fix: **draw an odd–even phase independently per line**. ⟹ **"Global synchrony = rigid translation, not a random walk"**, reproduced independently on both simple cubic and diamond.

**(g) A 6-regular bipartite graph is non-planar too**: a bipartite planar graph requires `m ≤ 2n − 4`, while 6-regularity gives `m = 3n` ⟹ contradiction (n = 512, m = 1536, bound 1020). ⟹ **The four-colour theorem (which speaks only of planar graphs) does not apply to the substrate**; regarded as a "map", the chromatic number is set by Heawood from the **genus**, independently of the coordination number (see the LST/Borsuk analysis in §4.10).

**【Honest boundary (8.6.8)】**

| Item | Nature |
|---|---|
| structural constraints (d-regular bipartite + König), the 6 perfect matchings of simple cubic, tick numerics | 【Derivation + numerics】 |
| "6 exterior-space directions ⟹ simple cubic" | 【verdict】 from the **text** of §4.10 Argument 4 + §4.9 Lemma 1; but the paper never explicitly says "lattice = simple cubic" |
| lattice spacing = l_P | 【natural choice within the framework assumption】(l_P is the only length scale), not a forced derivation |
| "global synchrony = rigidity" | 【numerical observation】, reproduced on two geometries, no analytic proof |
| "independent phase per line" | 【numerical necessary condition】 |
| whether the sites must form a periodic lattice at all | **not argued** (the framework only supplies "3 exterior-space axes ±") |
| the precise meaning of "2 out-of-plane directions curled up" | 【framework assumption】, read here as "4 of the 6 neighbours available for information transfer" |

"""

# ---------------------------------------------------------------- 整节替换
def replace_section(path, head, tail, new_sec, tag):
    s = io.open(path, encoding="utf-8").read()
    i = s.find(head)
    j = s.find(tail)
    if i < 0 or j < 0 or j <= i:
        print("  [XX] %-34s 定位失败（head=%d, tail=%d）—— 拒绝改动" % (tag, i, j))
        ACTIONS.append((tag, False))
        return
    io.open(path, "w", encoding="utf-8").write(s[:i] + new_sec + s[j:])
    print("  [OK] %-34s 已替换（%d → %d 字符）" % (tag, j - i, len(new_sec)))
    ACTIONS.append((tag, True))

replace_section(ZH, "#### 8.6.8 衬底格点几何", "**【诚实边界汇总】**", zh_new_sec, "ZH-2 §8.6.8 改写")
replace_section(EN, "#### 8.6.8 Substrate lattice geometry", "**【Honest-boundary summary】**",
                en_new_sec, "EN-2 §8.6.8 rewrite")

print("\n" + "=" * 58)
ok = sum(1 for _, v in ACTIONS if v)
print("补丁动作 %d 项，成功 %d，失败 %d" % (len(ACTIONS), ok, len(ACTIONS) - ok))
sys.exit(0 if ok == len(ACTIONS) else 1)
