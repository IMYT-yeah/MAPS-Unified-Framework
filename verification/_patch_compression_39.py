# -*- coding: utf-8 -*-
"""
第 39 轮论文补丁（中英同步）。

内容：
  (1) §4.8 追加【v2.9 补充（第 39 轮：压缩因子的机制审查）】块；
  (2) 顺带清掉排队 5 轮以上的两处积压：
      · §4.9「六处 4 同源」——「每 4 面元 1 比特」既漏改单位、标注也错位（应 1 纳特；
        出处可由 ③ 的 packing 命题推出，非【设定】），「表面诸元 4 邻居」的标注亦错位
        （实据为 §4.9 引理 1【设定】，非「本框架推论」）；
      · §4.10 定理 1 证明末的覆盖半径数值仍是随机搜索的旧值（90.05° / 70.291°），
        改为解析值 90.0000° / arccos(1/3) = 70.5288°。

锚点要求恰好命中一次，否则拒绝改动。
运行：<venv>/python.exe outputs/_patch_compression_39.py
"""

import io
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
STAMP = "2026-09-20第39轮前"

N_OK = [0]
N_FAIL = [0]


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<26} 命中 {} 次 —— 拒绝".format(tag, n))
        N_FAIL[0] += 1
        return
    txt = txt.replace(old, new, 1)
    io.open(path, "w", encoding="utf-8").write(txt)
    print("  [OK] {:<26} 已改".format(tag))
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

# ---------------------------------------------------------------- ZH：第 39 轮块
ZH_ANCHOR = "而这依赖 T-6 裁决的简单立方（其平面截面为方格）。"
ZH_BLOCK = "\n".join([
    "> **【v2.9 补充（第 39 轮：压缩因子的机制审查 —— 判为伪问题）】** 第 35 轮登记的「剩余压缩 "
    "**5.545** 无机制」经四路审查后**判为伪问题**：它不是等待机制的物理因子，而是**两个不同口径的"
    "计数之比**（分子 = 衬底的槽位数，**以比特计**；分母 = 观测熵，**以纳特计**）。",
    "> · **次二元引理**：BH 要求的熵密度 `1/4 纳特/面元 = 0.3607 比特/面元`，**小于 1 比特**"
    "（一个二元自由度最大熵 ln2 = 0.6931 纳特）；等效态数 `e^{1/4} = 1.2840`（非整数）"
    "⟹ 它**从一开始就不是计数**。",
    "> · **枚举 no-go**：若观测熵写成 `m` 个态的对数，温度比 `T_m/T_BH = 0.25/ln m` —— 面元级"
    "最近者 m = 2 偏 **−63.93%**；块级最近者 m = 3 偏 **−8.98%**（m = 2 即原稿「1 bit/块」，"
    "**+44.27%**，与第 15 轮的裁决数逐位一致）⟹ **`1/4` 纳特/面元与 `1` 纳特/块都不可能来自枚举**"
    "（e 非整数）。第 19 轮已觉察「相干约束是统计性的」，本轮把它**由「奇怪」升级为 no-go**。",
    "> · **几何审查**：立方格穿越键密度 = **1.000 条/l_P²**（轴向面，L=8 数值 64 键 / 64 l_P²）、"
    "**1.500 条/l_P²**（各向同性平均 `Σ_a⟨|n_a|⟩ = 3 × 1/2`）。最保守读法（1 条穿越键/l_P²、"
    "每条 1 bit）给 0.6931 纳特/l_P² ⟹ 仍**超出 ln16 = 2.7726 倍**；而所有自然几何因子"
    "（1/2、3/4、3/2、2、4/3…）都是 O(1) ⟹ **供给充足，缺口不在「数量不够」而在「谁算进熵」**。",
    "> · **不受观测约束**：Hawking 温度检验 `T = ℏc³/(8πGMk_B)` 复算得 **6.168678×10⁻⁸ K**，"
    "**该式不含压缩因子、也不含任何衬底计数** —— 原始计数取 16 / 8 / 4 bits，温度都是同一个数"
    "⟹ 观测只约束**分母**（1 纳特/4l_P²）。⟹ **压缩因子不是可观测量，而是两个独立量的比值**；"
    "要求一个比值「有自然机制」，是把比值当成了独立物理量。",
    "> · **动力学不能产生压缩**：tick 映射在构型空间上是**双射**（L=2 立方、256 个构型穷举验证，"
    "3 个轴全过）、L=6 下 500 tick 后**全局标记多重集完全守恒** ⟹ 底层零熵产生（第 21 轮）；"
    "而固定 2×2×2 块的**读数熵随时间涨落**（均值 0.624262、极差 0.693147 纳特）⟹ 压缩只能是"
    "**粗粒化映射**的性质，与「等分账必须是结构性的」（第 21 / 26 轮）一致。",
    "> ⟹ **判定**：`16 ln2 = 2`（键共享，**有机制**，第 35 轮）`× 5.545` 中的 **5.545 既无枚举机制、"
    "也无几何机制，且不受任何观测约束** —— 它是「以比特计的离散计数 ÷ 以纳特计的热力学熵」，"
    "必然含 ln2，其「自然性」是**伪问题**。真正该问的是**观测者为何只取 1 纳特/4l_P²**，"
    "那是 **B5 观测者模型的分辨率公设**，不属衬底层。",
    "> ⚠️ **状态改判（比数值更重要）**：压缩因子 11.0904 是由「16 态」与「1 纳特/块」**反解**出来的"
    "（第 19 轮原文：「它由 16 态与 1 纳特/块两个已知数逼出」）⟹ **该链条对 S = A/4 无预言力**："
    "这是**一致性构造**，不是推导；B5 的表述应改为「与 S = A/4 一致（在分辨率取 1 纳特/4l_P² 时）」。"
    "（S = A/4 本身的其它路径 —— F3 形式与 §4.10 的 packing/下界定理 —— **不受本轮影响**，"
    "它们不经过压缩因子。）",
    "> ⚠️ **口径补注**：`16 ln2 = 2 × 8 ln2` 的分解取**体内**口径（2 条独立键/面元，渐近值）。"
    "**2×2 块只有 4 个面元却触及 12 条不同键**（含 8 条与外部共享的边界键）⟹ 3.00 键/面元，"
    "而体内是 2.00 ⟹ **因子 2 不是强度量**，在相干块尺度上不成立。",
    "> ⚠️ **本轮未做**：观测者分辨率的机制（三个候选方向一个都没算）；「穿越键」读法（把熵归给"
    "穿越面积元的键而非面元上的槽位）的合法性未独立论证；`e^{1/4}` 的连分数逼近（9/7 = 1.2857，"
    "+0.132%）与 `0.25 = 1/log₂16` 等数值接近**全部登记为无机制**，按项目规约不得用作证据。",
    "",
])

sub_once(ZH, ZH_ANCHOR, ZH_ANCHOR + "\n" + ZH_BLOCK, "ZH §4.8 第 39 轮块")

# ---------------------------------------------------------------- ZH：六处 4 同源
sub_once(
    ZH,
    "表面诸元 4 邻居（观测者几何，本框架推论）",
    "表面诸元 4 邻居（观测者几何；**实据为 §4.9 引理 1【本框架设定】**，"
    "原标「本框架推论」已更正）",
    "ZH 六处4·表面邻居标注",
)
sub_once(
    ZH,
    "每 4 面元 1 比特（本框架设定）",
    "每 4 面元 **1 纳特**【**v2.9 单位更正**：原写「1 比特」，按 §4.8 的 Hawking 温度裁决更正；"
    "原标【本框架设定】亦更正 —— 可由 ③ 的 packing 命题推出】",
    "ZH 六处4·单位与标注",
)

# ---------------------------------------------------------------- ZH：覆盖半径
sub_once(
    ZH,
    "（数值：k=3 最优覆盖半径 = 90.05°，k=4 = 70.291°）",
    "（解析值：k=3 ⟹ 覆盖半径 = **90.0000°**，最坏点取平面法线；k=4 ⟹ **arccos(1/3) "
    "= 70.5288°**，最坏点取 Voronoi 顶点。旧值 90.05° / 70.291° 系随机搜索未穷尽所致，"
    "已更正）",
    "ZH §4.10 覆盖半径",
)

# ---------------------------------------------------------------- EN：第 39 轮块
EN_ANCHOR = "and it rests on the simple cubic lattice of the T-6 verdict (whose planar section is a square lattice)."
EN_BLOCK = "\n".join([
    "> **【v2.9 supplement (round 39: mechanism audit of the compression factor — declared a "
    "pseudo-problem)】** The open item registered in round 35 (\"the residual compression **5.545** "
    "has no mechanism\") is judged a **pseudo-problem**: it is not a physical factor awaiting a "
    "mechanism but the **ratio of two counts in two different accounting conventions** (numerator = "
    "substrate slots, **counted in bits**; denominator = observed entropy, **counted in nats**).",
    "> · **Sub-binary lemma**: the BH entropy density `1/4 nat per plaquette = 0.3607 bit per "
    "plaquette` is **less than one bit** (a binary degree of freedom carries at most ln2 = 0.6931 "
    "nat); the equivalent number of states is `e^{1/4} = 1.2840` (non-integer) ⟹ **it was never a "
    "count to begin with**.",
    "> · **Enumerative no-go**: if the observed entropy were the logarithm of `m` states, the "
    "temperature ratio would be `T_m/T_BH = 0.25/ln m` — at plaquette level the closest integer "
    "m = 2 is off by **−63.93%**; at block level the closest, m = 3, is off by **−8.98%** (m = 2 is "
    "the original \"1 bit per block\", **+44.27%**, matching the round-15 verdict digit for digit). "
    "⟹ **neither `1/4` nat per plaquette nor `1` nat per block can come from enumeration** (e is not "
    "an integer). Round 19 already sensed that \"the coherent constraint is statistical\"; this round "
    "upgrades that from \"odd\" to a **no-go**.",
    "> · **Geometric audit**: the crossing-bond density of the cubic lattice is **1.000 per l_P²** "
    "(axis-aligned plane; L = 8 numerics: 64 bonds / 64 l_P²) and **1.500 per l_P²** (isotropic "
    "average, `Σ_a⟨|n_a|⟩ = 3 × 1/2`). The most conservative reading (1 crossing bond per l_P², "
    "1 bit each) still gives 0.6931 nat/l_P², i.e. **overshoots by ln16 = 2.7726×**; and every "
    "natural geometric factor (1/2, 3/4, 3/2, 2, 4/3, …) is O(1) ⟹ **the supply is ample — the gap "
    "is not \"not enough\", it is \"what gets counted\"**.",
    "> · **Constrained by no observation**: the Hawking-temperature check `T = ℏc³/(8πGMk_B)` "
    "recomputes to **6.168678×10⁻⁸ K** and **contains neither the compression factor nor any "
    "substrate count** — taking the raw count as 16 / 8 / 4 bits leaves the temperature unchanged "
    "⟹ observation constrains only the **denominator** (1 nat per 4l_P²). ⟹ **the compression factor "
    "is not an observable but the ratio of two independent quantities**; demanding a \"natural "
    "mechanism\" for it mistakes a ratio for an independent physical quantity.",
    "> · **Dynamics cannot generate the compression**: the tick map is a **bijection** on "
    "configuration space (exhaustive check over all 256 configurations of the L = 2 cube, all three "
    "axes), and on L = 6 the **global label multiset is exactly conserved** over 500 ticks ⟹ zero "
    "entropy production at the bottom layer (round 21); meanwhile the **readout entropy of a fixed "
    "2×2×2 block fluctuates in time** (mean 0.624262, range 0.693147 nat) ⟹ the compression can only "
    "be a property of the **coarse-graining map**, consistent with \"equipartition must be "
    "structural\" (rounds 21 / 26).",
    "> ⟹ **Verdict**: in `16 ln2 = 2` (key sharing, **mechanised**, round 35) `× 5.545`, the residual "
    "**5.545 has no enumerative mechanism, no geometric mechanism, and is constrained by no "
    "observation** — it is \"a discrete count in bits divided by a thermodynamic entropy in nats\", "
    "so it necessarily carries ln2, and its \"naturalness\" is a **pseudo-problem**. The real question "
    "is **why the observer reads only 1 nat per 4l_P²** — that is the **resolution postulate of the "
    "B5 observer model** and does not belong to the substrate layer.",
    "> ⚠️ **Status reclassification (more important than the numbers)**: the compression factor "
    "11.0904 was **reverse-engineered** from \"16 states\" and \"1 nat per block\" (round 19 states "
    "verbatim that \"it is forced by the two known numbers 16 states and 1 nat per block\") ⟹ **this "
    "chain has no predictive power for S = A/4**: it is a **consistency construction, not a "
    "derivation**, and B5 should say \"consistent with S = A/4 (for resolution 1 nat per 4l_P²)\". "
    "(Other routes to S = A/4 — the F3 form and the packing/lower-bound theorem of §4.10 — are "
    "**unaffected**: they do not pass through the compression factor.)",
    "> ⚠️ **Accounting caveat**: the decomposition `16 ln2 = 2 × 8 ln2` uses the **bulk** convention "
    "(2 independent keys per plaquette, the asymptotic value). **A 2×2 block has only 4 plaquettes "
    "but touches 12 distinct keys** (8 of them boundary keys shared with the outside) ⟹ 3.00 keys per "
    "plaquette in the block versus 2.00 in the bulk ⟹ **the factor 2 is not intensive** and does not "
    "hold at coherent-block scale.",
    "> ⚠️ **Not done this round**: any mechanism for the observer's resolution (none of the three "
    "candidate directions was computed); the legitimacy of the \"crossing-bond\" reading (attributing "
    "entropy to bonds crossing the area element rather than to slots lying on it) is not argued "
    "independently; the continued-fraction approximations to `e^{1/4}` (9/7 = 1.2857, +0.132%) and "
    "the coincidence `0.25 = 1/log₂16` are **all registered as mechanism-free** and must not be used "
    "as evidence.",
    "",
])

sub_once(EN, EN_ANCHOR, EN_ANCHOR + "\n" + EN_BLOCK, "EN §4.8 round-39 block")

# ---------------------------------------------------------------- EN：六处 4 同源
sub_once(
    EN,
    "surface plaquette 4 neighbors (observer geometry, framework corollary)",
    "surface plaquette 4 neighbors (observer geometry; **the source is §4.9 Lemma 1, a "
    "【framework assumption】** — the earlier label \"framework corollary\" is corrected)",
    "EN six-fours·neighbour label",
)
sub_once(
    EN,
    "= 1 bit per 4 plaquettes (framework assumption) = Kakeya packing 1/4",
    "= **1 nat** per 4 plaquettes【**v2.9 unit correction**: originally \"1 bit\", changed per the "
    "Hawking-temperature verdict of §4.8; the earlier label 【framework assumption】 is also "
    "corrected — it follows from item ③'s packing proposition】 = Kakeya packing 1/4",
    "EN six-fours·unit and label",
)

# ---------------------------------------------------------------- EN：覆盖半径
sub_once(
    EN,
    "(Numerically: k=3 optimal covering radius = 90.05°, k=4 = 70.291°)",
    "(Analytic values: k = 3 ⟹ covering radius = **90.0000°**, worst point the plane normal; "
    "k = 4 ⟹ **arccos(1/3) = 70.5288°**, worst point a Voronoi vertex. The old numbers "
    "90.05° / 70.291° came from incomplete random search and are corrected.)",
    "EN §4.10 covering radius",
)

print("")
print("通过 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
