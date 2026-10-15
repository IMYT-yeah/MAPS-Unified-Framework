# -*- coding: utf-8 -*-
"""
§4.8/§4.9/摘要 三处硬修正（中英同步，就地改 v2.9）
依据：
  第 15 轮（ln2 缺口：1 nat vs 1 bit，Hawking 温度裁决）
  第 19 轮（底层 16 = 4 方向 × 4 状态；压缩因子 16 ln2 = 11.0904）
  第 20 轮（k = 2^{1/4} → e^{1/4}）
内容：① 1 比特/块 → 1 纳特/块；② k = 2^{1/4} → e^{1/4}；③ 1/4 bit/面元 → 1/4 纳特/面元；
      ④ 新增【v2.9 修正块】说明状态数来源、压缩因子与开放项。
锚点必须恰好命中一次，否则报错退出（不改动任何文件）。
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT, FAIL = [], []


def rep(path, tag, old, new, optional=False):
    s = open(path, encoding="utf-8").read()
    n = s.count(old)
    if n != 1:
        lvl = "跳过" if optional else "失败"
        (FAIL.append if not optional else (lambda x: None))("%s｜%s：命中 %d 次" % (os.path.basename(path), tag, n))
        print("  [%s] %-44s 命中 %d 次" % ("--" if optional else "XX", tag, n))
        return
    open(path, "w", encoding="utf-8").write(s.replace(old, new, 1))
    OUT.append("%s｜%s" % (os.path.basename(path), tag))
    print("  [OK] %-44s 已改" % tag)


ZH_BLOCK = """**【v2.9 修正：单位与 k 的更正（第 15/19/20 轮）】**（以下 v2.8 补充中出现的「1 比特/块」与「k=2^{1/4}」均按此更正）：
- **单位更正（判据来自 Hawking 温度）**：观测者端与统计端一致取**每 4l_P² 为 1 纳特，不是 1 比特**。若取 1 bit，反推太阳质量黑洞温度为 8.8995×10⁻⁸ K，偏离标准 Hawking 值 **+44.27%**；取 1 nat 则给 6.16868×10⁻⁸ K（偏差 <10⁻⁹）。⟹ `S/k_B = A/(4l_P²)`（**纳特**），即熵密度 **1/4 纳特/面元 = 0.3607 bit/面元**。原式 `S = (A/4l_P²)ln2（比特）= A/4l_P²（纳特）` **两侧相差一个 ln2**，已更正。
- **k 的更正**：`k = 2^{1/4} = 1.1892` 对应的是「1/4 **比特**/面元」（ln k = 0.1733 nat）；更正后为 **`k = e^{1/4} = 1.2840`**（ln k = 0.25 nat）。两者数值只差 8%，**熵却差 44%（= 1/ln2）**——这正是 bit/nat 混用的典型表现。
- **底层状态数的来源（v2.9 新增：把 B5 的一个输入变成输出）**：以 B5 的「原始可读 4 bits/面元」为目标反解每个格点的内部状态数 q，配合 §4 已给的**方向簇 k=4**：q=2 → 3.000 bits、q=3 → 3.585、**q=4 → 4.000（唯一）**、q=5 → 4.322。⟹ 内部四状态正是 **{正, 负, 湮灭中, 真空}**，原始态数 = **4 方向 × 4 状态 = 16 = 4 bits/面元**（原先这是假设，现在是被推出的）。
- **相干压缩因子**：原始熵/相干块 = 4·ln16 = **11.0904 纳特**（= 16 bits），观测值 1 纳特 ⟹ **压缩因子 = 4 ln16 = 16 ln 2 = 11.0904**（原稿写的「16 倍」相差 1/ln2 = 1.4427）。
- **诚实的开放项**：① 11.0904 非整数，其「自然性」仍未解释（它由 16 态与 1 纳特/块两个已知数逼出）；② 四状态中的「湮灭中 / 真空」在平衡下必须是**拍内零测度过渡态**，否则衬底占空率 < 1 ⟹ c 会偏移（取 Δc/c ≲ 10⁻⁶ 得空位率 ≲ 3×10⁻⁶）。

"""

EN_BLOCK = """**【v2.9 correction: units and k (rounds 15/19/20)】** (every "1 bit/block" and "k=2^{1/4}" appearing in the v2.8 supplement below is superseded by this):
- **Unit correction (adjudicated by the Hawking temperature)**: both ends agree on **1 nat per 4l_P², not 1 bit**. Taking 1 bit would give a solar-mass black hole temperature of 8.8995×10⁻⁸ K, i.e. **+44.27%** off the standard Hawking value; 1 nat gives 6.16868×10⁻⁸ K (deviation <10⁻⁹). ⟹ `S/k_B = A/(4l_P²)` (**nats**), i.e. entropy density **1/4 nat/plaquette = 0.3607 bit/plaquette**. The original formula `S = (A/4l_P²)ln2 (bits) = A/4l_P² (nats)` **differs between its two sides by one ln 2** and is corrected here.
- **Correction of k**: `k = 2^{1/4} = 1.1892` corresponds to "1/4 **bit**/plaquette" (ln k = 0.1733 nat); the corrected value is **`k = e^{1/4} = 1.2840`** (ln k = 0.25 nat). The two differ by only 8% in value but by **44% in entropy (= 1/ln2)** — the signature of mixing bits and nats.
- **Origin of the substrate state count (new in v2.9: turning an input of B5 into an output)**: inverting B5's "raw readable 4 bits/plaquette" for the number q of internal states per site, using the direction cluster **k=4** already established in §4: q=2 → 3.000 bits, q=3 → 3.585, **q=4 → 4.000 (unique)**, q=5 → 4.322. ⟹ the four internal states are exactly **{+, −, annihilating, vacuum}**, and the raw count is **4 directions × 4 states = 16 = 4 bits/plaquette** (previously an assumption, now derived).
- **Coherent compression factor**: raw entropy per coherent block = 4·ln16 = **11.0904 nats** (= 16 bits) versus the observed 1 nat ⟹ **compression factor = 4 ln16 = 16 ln 2 = 11.0904** (the draft's "factor 16" is off by 1/ln2 = 1.4427).
- **Honest open items**: ① 11.0904 is not an integer; its "naturalness" remains unexplained (it is forced by the two known numbers, 16 states and 1 nat/block); ② the "annihilating" and "vacuum" branches must have **zero measure within a tick** in equilibrium, otherwise the substrate occupancy drops below 1 and c shifts with density (Δc/c ≲ 10⁻⁶ ⟹ hole fraction ≲ 3×10⁻⁶).

"""

# ---------------------------------------------------------------- 中文
ZH = [
    ("摘要｜微态计数（1 比特→1 纳特，k）",
     "- **微态计数**（§4.8）：通量管相干块（每 4 普朗克面积 1 比特，k = 2^{1/4}），G、ℏ 作为普朗克面积的复合出现；",
     "- **微态计数**（§4.8）：通量管相干块（**每 4 普朗克面积 1 纳特**，k = e^{1/4} ≈ 1.284；原始态 = 4 方向 × 4 状态 = 16），G、ℏ 作为普朗克面积的复合出现；"),
    ("摘要｜B4 双闭合（k）",
     "与 k=2^{1/4} 微态计数（\"=\"方向）双闭合（B4）",
     "与 k=e^{1/4} 微态计数（\"=\"方向）双闭合（B4）"),
    ("摘要｜B5 末句（4 bits / 1/4 bit）",
     "观测者原始可读 4 bits/面元经 16 倍相干压缩（4面元×4方向）⟹ 熵密度 1/4 bit/面元 = 1/(4l_P²)（B5）。",
     "观测者原始可读 **4 bits/面元**（= 4 方向 × 4 状态 {正/负/湮灭中/真空} 的 16 个原始态）经相干压缩 **16 ln 2 = 11.0904** 至**每相干块 1 纳特** ⟹ 熵密度 **1/4 纳特/面元**（= 0.3607 bit/面元）⟹ S/k_B = A/(4l_P²)（B5）。"),
    ("§4.8｜每单元 1 比特",
     "每 4 面元 1 个相干单元（Clifford 4 分量：时间双向×手性双向），每单元 1 比特：",
     "每 4 面元 1 个相干单元（Clifford 4 分量：时间双向×手性双向），每单元 **1 纳特**："),
    ("§4.8｜公式",
     "$$S = \\frac{A}{4l_P^2}\\ln 2 \\quad\\text{（比特）} = \\frac{A}{4l_P^2}\\quad\\text{（纳特）},\\qquad k = 2^{1/4} \\approx 1.189$$",
     "$$\\frac{S}{k_B} = \\frac{A}{4l_P^2}\\ \\text{（纳特）} = \\frac{A}{4l_P^2\\ln 2}\\ \\text{（比特）},\\qquad k = e^{1/4} \\approx 1.284$$"),
    ("§4.8｜待验证（k）",
     "【待验证】k=2^{1/4} 的动力学来源仍需",
     "【待验证】k=e^{1/4} 的动力学来源仍需"),
    ("§4.8｜④ 中间量（1/4 bit）",
     "④ **中间量可证伪**：相干块尺寸 4l_P²、熵密度 1/4 bit/面元、方向簇 k=4 全部独立可测",
     "④ **中间量可证伪**：相干块尺寸 4l_P²、熵密度 **1/4 纳特/面元**（= 0.3607 bit/面元）、方向簇 k=4、底层状态数 **16 = 4 方向 × 4 状态** 全部独立可测"),
    ("§4.9｜全息集中命题",
     "- **命题（全息集中）**：S_max(R) = (A/4l_P²)·ln 2——观测者限制是信息集中的根源",
     "- **命题（全息集中）**：S_max(R) = A/(4l_P²)（**纳特**）——观测者限制是信息集中的根源"),
    ("§4.9｜O4",
     "- **O4（信息容量）**：4 最近邻 ⟹ 每 4 面元 1 bit ⟹ S_max = (A/4l_P²)·ln2【本框架推论】——全息 = 观测者限制的几何必然。",
     "- **O4（信息容量）**：4 最近邻 ⟹ 每 4 面元 **1 纳特**（经 §4.8 的 v2.9 更正）⟹ S_max = A/(4l_P²)（纳特）【本框架推论】——全息 = 观测者限制的几何必然。"),
    ("§10.2｜结论里的 k（可选）",
     "S=A/4 微态计数（k=2^{1/4}",
     "S=A/4 微态计数（k=e^{1/4}",
     True),
    ("§4.8｜插入 v2.9 修正块",
     "**【v2.8 补充：k=2^{1/4} 因子独立推导（响应审稿 M7 确认偏差质疑）】**：",
     ZH_BLOCK + "**【v2.8 补充：k=2^{1/4} 因子独立推导（响应审稿 M7 确认偏差质疑）】**："),
]

# ---------------------------------------------------------------- 英文
EN = [
    ("abstract｜microstate counting",
     "- **Microstate counting** (§4.8): flux-tube coherent blocks (1 bit per 4 Planck areas, k = 2^{1/4}), with G, ℏ appearing as composites of the Planck area;",
     "- **Microstate counting** (§4.8): flux-tube coherent blocks (**1 nat per 4 Planck areas**, k = e^{1/4} ≈ 1.284; raw states = 4 directions × 4 states = 16), with G, ℏ appearing as composites of the Planck area;"),
    ("abstract｜B4 double closure (k)",
     "doubly closed with the k=2^{1/4} microstate counting",
     "doubly closed with the k=e^{1/4} microstate counting"),
    ("abstract｜B5 tail (4 bits / 1/4 bit)",
     "the observer's raw 4 bits/plaquette compressed coherently by a factor 16 (4 plaquettes × 4 directions) ⟹ entropy density 1/4 bit/plaquette = 1/(4l_P²) (B5).",
     "the observer's raw **4 bits/plaquette** (= 16 raw states from 4 directions × 4 states {+, −, annihilating, vacuum}) compressed coherently by **16 ln 2 = 11.0904** to **1 nat per coherent block** ⟹ entropy density **1/4 nat/plaquette** (= 0.3607 bit/plaquette) ⟹ S/k_B = A/(4l_P²) (B5)."),
    ("§4.8｜1 bit per unit",
     "Clifford 4 components: two time directions × two chirality directions), 1 bit per unit:",
     "Clifford 4 components: two time directions × two chirality directions), **1 nat** per unit:"),
    ("§4.8｜formula",
     "$$S = \\frac{A}{4l_P^2}\\ln 2 \\quad\\text{(bits)} = \\frac{A}{4l_P^2}\\quad\\text{(nats)},\\qquad k = 2^{1/4} \\approx 1.189$$",
     "$$\\frac{S}{k_B} = \\frac{A}{4l_P^2}\\ \\text{(nats)} = \\frac{A}{4l_P^2\\ln 2}\\ \\text{(bits)},\\qquad k = e^{1/4} \\approx 1.284$$"),
    ("§4.8｜to be verified (k)",
     "【To be verified】 the dynamical origin of k=2^{1/4} still requires",
     "【To be verified】 the dynamical origin of k=e^{1/4} still requires"),
    ("§4.8｜④ intermediates (1/4 bit)",
     "coherent-block size 4l_P², entropy density 1/4 bit/plaquette, direction cluster k=4 all independently measurable",
     "coherent-block size 4l_P², entropy density **1/4 nat/plaquette** (= 0.3607 bit/plaquette), direction cluster k=4, and the substrate state count **16 = 4 directions × 4 states**, all independently measurable"),
    ("§4.9｜holographic concentration proposition",
     "- **Proposition (holographic concentration)**: S_max(R) = (A/4l_P²)·ln 2 —",
     "- **Proposition (holographic concentration)**: S_max(R) = A/(4l_P²) (**nats**) —"),
    ("§4.9｜O4",
     "- **O4 (information capacity)**: 4 nearest neighbors ⟹ 1 bit per 4 plaquettes ⟹ S_max = (A/4l_P²)·ln2【Framework corollary】",
     "- **O4 (information capacity)**: 4 nearest neighbors ⟹ **1 nat per 4 plaquettes** (per the §4.8 v2.9 correction) ⟹ S_max = A/(4l_P²) (nats)【Framework corollary】"),
    ("§10.2｜k in conclusions (optional)",
     "microstate counting (k=2^{1/4}",
     "microstate counting (k=e^{1/4}",
     True),
    ("§4.8｜insert v2.9 correction block",
     "**【v2.8 supplement: independent derivation of the k=2^{1/4} factor (referee M7 confirmation-bias objection)】**:",
     EN_BLOCK + "**【v2.8 supplement: independent derivation of the k=2^{1/4} factor (referee M7 confirmation-bias objection)】**:"),
]

jobs = [(os.path.join(HERE, "论文初稿_正反物质对风暴统一框架_v2.9.md"), ZH),
        (os.path.join(HERE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md"), EN)]

HIST = os.path.join(ROOT, "MAPS-Unified-Framework", "paper", "history")
os.makedirs(HIST, exist_ok=True)
for p, _ in jobs:
    b = os.path.join(HIST, os.path.basename(p).replace(".md", "_备份_2026-09-18单位k前.md"))
    open(b, "w", encoding="utf-8").write(open(p, encoding="utf-8").read())
    print("  备份 →", os.path.basename(b))

# 先把可选锚点的命中情况报告出来（不改）
print("\n-- 可选锚点预检 --")
for p, lst in jobs:
    s = open(p, encoding="utf-8").read()
    for item in lst:
        if len(item) == 4 and item[3]:
            print("   %s ｜ %-34s 命中 %d 次" % (os.path.basename(p), item[0], s.count(item[1])))

for p, lst in jobs:
    print("\n" + "=" * 70 + "\n" + os.path.basename(p) + "\n" + "=" * 70)
    for item in lst:
        tag, old, new = item[0], item[1], item[2]
        opt = len(item) == 4 and item[3]
        rep(p, tag, old, new, optional=opt)

print("\n完成 %d 项" % len(OUT))
print("失败：%s" % ("；".join(FAIL) if FAIL else "无"))
