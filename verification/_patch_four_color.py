# -*- coding: utf-8 -*-
"""第 28 轮补丁：四色定理辨析 + LST/Borsuk 出处 + 修正第 27 轮的一处依赖
  ① §4.10 定理 1 加 LST/Borsuk 出处注与解析覆盖半径
  ② §4.10「六处 4 同源」加分级修正注
  ③ §8.6.8(b) 修正依赖（表面 4 邻居 → 方向簇 k = 4）
  ④ §8.6.8 新增 (h)：4-正则二分图必非平面 + 与四色定理划界
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
        print("  [XX] %-38s 锚点命中 %d 次 —— 拒绝改动" % (tag, n))
        ACTIONS.append((tag, False))
        return
    io.open(path, "w", encoding="utf-8").write(s.replace(old, new))
    print("  [OK] %-38s 已替换" % tag)
    ACTIONS.append((tag, True))

# ---------------------------------------------------------------- ZH-1 定理 1 出处注
zh_t1 = "**定理 1（方向簇数下界 k ≥ 4）【新证·严格】**：设方向集 V⊂S² 为量子直线端点方向簇。若覆盖半径严格 < 90°（挂谷\"包全方向\"要求，无零信息余量方向），则 k ≥ 4。"
zh_t1_new = zh_t1 + """

> **【v2.9 出处注】**：本定理是 **Lusternik–Schnirelmann 定理**在 S² 上的特例（LS 范畴 = 3），并与 **Borsuk 定理**（R³ 的 Borsuk 数 = 4：任何有界集可分成 4 个直径更小的子集，且 4 最优）同源。下方独立证明的价值在于给出框架语言下的构造性版本；**建议正文引用 LST/Borsuk**，以免被审稿人指出重复发明。覆盖半径的解析值为 **k = 3 ⟹ 90.0000°**（最坏点取平面法线）、**k = 4 ⟹ arccos(1/3) = 70.5288°**（最坏点取 Voronoi 顶点）；原文的 90.05° / 70.291° 系随机搜索未穷尽所致。"""
patch(ZH, zh_t1, zh_t1_new, "ZH-1 定理1 出处注")

# ---------------------------------------------------------------- ZH-2 六处 4 同源加注
zh_6 = "= 正四面体 4-方向簇（Tammes n=4）——**观测者能编码的信息结构 = 内空间结构 = 表面信息密度的倒数**，全息集中与微态计数无缝衔接。"
zh_6_new = zh_6 + """

> **【v2.9 分级修正注】**：「同源」需要分级。至少「**表面诸元 4 邻居**」与「**正四面体 4-方向簇**」**不同源**：前者出自 §4.9 引理 1【本框架设定】的"平面内 4 方向"（= 2D 平面内 2 轴 × 2 向，对应**可平面的 2D 方格网**），后者出自 §4.10 定理 1（S² 覆盖半径 ≥ 90°，即 **Lusternik–Schnirelmann 定理**）。两者数值都是 4，机制独立。其余四处（4l_P² 相干截面、每 4 面元 1 比特、Clifford 4 分量、挂谷 1/4）的出处亦应各自复查。建议本表述降调为"**六处数值均为 4，其中若干同源、若干独立**"。"""
patch(ZH, zh_6, zh_6_new, "ZH-2 六处4同源加注")

# ---------------------------------------------------------------- ZH-3 §8.6.8(b) 修正依赖
zh_b = "配位数 4 不是本节新引入的：§4.10「六处「4」同源」第一条即「**表面诸元 4 邻居**（观测者几何，本框架推论）」，而定理 2 已证「4 点最优构型 = 正四面体」。**把这两条既有设定与 tick 的二分要求放在一起，几何被唯一确定。**"
zh_b_new = ("配位数 4 不是本节新引入的：**§4.10 定理 1+2**（严格）给出「方向簇 k ≥ 4」且「k = 4 的最优构型 = 正四面体」；"
            "若每个方向对应一条键，则每格点 4 条键 ⟹ **体配位数 = 4**。**把它与 tick 的二分要求放在一起，几何被唯一确定。**\n"
            "⚠️ **（v2.9 修正）**：初稿此处曾以 §4.10「六处 4 同源」中的「**表面诸元 4 邻居**」为支撑 —— **该引用不成立**："
            "那一条出自 §4.9 引理 1【本框架设定】的「平面内 4 方向」（2D 平面内 2 轴 × 2 向），是**观测者平面内的计数**"
            "（对应可平面的 2D 方格网），**不是体配位数**。支撑已改用上句「方向簇 k = 4」（定理而非设定），**结论不变**。")
patch(ZH, zh_b, zh_b_new, "ZH-3 8.6.8(b) 修正依赖")

# ---------------------------------------------------------------- ZH-4 §8.6.8 新增 (h)
zh_g_end = "按「**最近邻即键**」判据取前者 ⟹ (上述 ①) 的碰撞率相应修正为 **0.6495/t_P**、平均自由程 **1.5396 l_P**（量级结论「O(1/t_P)、O(l_P)」不变）。\n"
zh_h = zh_g_end + """
**(h) 4-正则二分图必非平面 —— 与四色定理划清界限**：若 4-正则二分图能嵌入平面，则 Euler 给 `f = m − n + 2`，二分给每个面长度 ≥ 4 故 `2m ≥ 4f`，合并得 `m ≤ 2n − 4`；但 4-正则给 `m = 2n`，**矛盾**（数值：n = 512、m = 1024、上界 1020，缺口 4）。⟹ **四色定理（只对平面图说话）对衬底图不适用**。金刚石图的亏格恰为 1：环面上 `f = m − n = 512`、`2m = 2048 = 4f` **恰好饱和**（每个面都是四边形）；若把它当"地图"看，按 Heawood 公式其色数是 **7**（g = 1），不是 4。⟹ **四色定理与框架的「4」既不同源、数值也对不上**。（对照：2D 方格网 n = 64、m = 112、f = 50，`2m = 224 ≥ 4f = 200` ⟹ **可平面** —— 表面 4 邻居网格与体 4-正则衬底因此是**平面/非平面两回事**。）

"""
patch(ZH, zh_g_end, zh_h, "ZH-4 8.6.8 新增 (h)")

# ---------------------------------------------------------------- EN-1
en_t1 = '**Theorem 1 (direction-cluster-number lower bound k ≥ 4)【New proof, rigorous】**: Let V⊂S² be the direction cluster of quantum-line endpoints. If the covering radius is strictly < 90° (Kakeya "covers all directions" requirement, no zero-information-residual direction), then k ≥ 4.'
en_t1_new = en_t1 + """

> **【v2.9 provenance note】** This theorem is a special case of the **Lusternik–Schnirelmann theorem** on S² (LS category = 3), and shares its origin with the **Borsuk theorem** (Borsuk number of R³ = 4: any bounded set splits into 4 subsets of smaller diameter, and 4 is optimal). The independent proof below is valuable as a constructive version in the framework's language; **citing LST/Borsuk in the main text is recommended**, to avoid a referee noting that the wheel was reinvented. The analytic covering radii are **k = 3 ⟹ 90.0000°** (worst point = plane normal) and **k = 4 ⟹ arccos(1/3) = 70.5288°** (worst point = Voronoi vertex); the earlier 90.05° / 70.291° came from incomplete random search."""
patch(EN, en_t1, en_t1_new, "EN-1 Theorem 1 note")

# ---------------------------------------------------------------- EN-2
en_6 = '= regular-tetrahedron 4-direction cluster (Tammes n=4) — **the information structure encodable by the observer = interior-space structure = the inverse of surface information density**; holographic concentration and microstate counting connect seamlessly.'
en_6_new = en_6 + """

> **【v2.9 graded correction note】** "Same source" needs grading. At least "**4 neighbours of a surface element**" and "**regular-tetrahedron 4-direction cluster**" are **NOT the same source**: the former comes from §4.9 Lemma 1【framework assumption】"4 in-plane directions" (= 2 axes × 2 directions in 2D, corresponding to the **planar** 2D square lattice), the latter from §4.10 Theorem 1 (covering radius of S² ≥ 90°, i.e. the **Lusternik–Schnirelmann theorem**). Both numbers are 4, but the mechanisms are independent. The provenance of the remaining four (4l_P² coherent cross-section, 1 bit per 4 plaquettes, Clifford 4 components, Kakeya 1/4) should also be re-checked individually. Recommend downgrading this statement to "**all six numbers are 4; some share a source, some are independent**"."""
patch(EN, en_6, en_6_new, "EN-2 six 4s note")

# ---------------------------------------------------------------- EN-3
en_b = 'Coordination 4 is not introduced here: §4.10\'s "six occurrences of 4" already lists "**4 neighbours of a surface element** (observer geometry, framework corollary)", and Theorem 2 proves "optimal 4-point configuration = regular tetrahedron". **Combining these two pre-existing statements with the tick\'s bipartiteness requirement fixes the geometry.**'
en_b_new = ('Coordination 4 is not introduced here: **§4.10 Theorems 1+2** (rigorous) give "direction-cluster number k ≥ 4" and "the optimal k = 4 configuration = regular tetrahedron"; '
            'if each direction corresponds to one bond then every site has 4 bonds ⟹ **bulk coordination number = 4**. **Combining this with the tick\'s bipartiteness requirement fixes the geometry.**\n'
            '⚠️ **(v2.9 correction)**: an earlier draft cited "**4 neighbours of a surface element**" from §4.10\'s "six occurrences of 4" as the support — **that citation does not hold**: it comes from §4.9 Lemma 1【framework assumption】"4 in-plane directions" (2 axes × 2 directions in 2D), an **observer in-plane count** (corresponding to the planar 2D square lattice), **not the bulk coordination number**. The support has been changed to "direction-cluster k = 4" (a theorem, not an assumption); **the conclusion is unchanged**.')
patch(EN, en_b, en_b_new, "EN-3 8.6.8(b) fix")

# ---------------------------------------------------------------- EN-4
en_g_end = 'Using the "**nearest neighbour = bond**" criterion we take the former ⟹ the collision rate in ① becomes **0.6495/t_P** and the mean free path **1.5396 l_P** (the order-of-magnitude conclusions "O(1/t_P), O(l_P)" are unchanged).\n'
en_h = en_g_end + """
**(h) A 4-regular bipartite graph is necessarily non-planar — drawing the line against the four-colour theorem**: if a 4-regular bipartite graph embedded in the plane, Euler gives `f = m − n + 2` and bipartiteness gives every face length ≥ 4 hence `2m ≥ 4f`; combining yields `m ≤ 2n − 4`, but 4-regularity gives `m = 2n` — **contradiction** (numerics: n = 512, m = 1024, bound 1020, gap 4). ⟹ **The four-colour theorem (which speaks only about planar graphs) does not apply to the substrate.** The diamond graph has genus exactly 1: on the torus `f = m − n = 512` and `2m = 2048 = 4f` **exactly saturated** (every face a quadrilateral); regarded as a "map" its chromatic number by Heawood's formula is **7** (g = 1), not 4. ⟹ **The four-colour theorem's "4" and the framework's "4" are neither co-sourced nor numerically equal.** (Contrast: the 2D square lattice 8×8 has n = 64, m = 112, f = 50, `2m = 224 ≥ 4f = 200` ⟹ **planar** — so the surface 4-neighbour lattice and the bulk 4-regular substrate are genuinely different: one planar, one not.)

"""
patch(EN, en_g_end, en_h, "EN-4 8.6.8 add (h)")

print("\n" + "=" * 62)
ok = sum(1 for _, v in ACTIONS if v)
print("补丁动作 %d 项，成功 %d，失败 %d" % (len(ACTIONS), ok, len(ACTIONS) - ok))
sys.exit(0 if ok == len(ACTIONS) else 1)
