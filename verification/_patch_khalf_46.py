# -*- coding: utf-8 -*-
"""
第 46 轮论文补丁（中英同步，2 项）。

在 §4.8 第 41 轮块（"仍未定：H/N 的界为 0.162 – 0.693"）之后插入
【v2.9 补充（第 46 轮：k=N/2 的精确轨道 —— 不变量不完备，H/N 饱和在 ≈0.433）】块。

锚点必须恰好命中一次。
"""

import io
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
STAMP = "2026-09-22第46轮前"

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

ANCHOR_ZH = "> ⚠️ **仍未定**：H/N 的界为 **0.162 – 0.693**"
ANCHOR_EN = "> ⚠️ **Still open**: the bracket for H/N is **0.162 – 0.693**"

BLOCK_ZH = """
> **【v2.9 补充（第 46 轮：k = N/2 的精确轨道 —— 不变量不完备，H/N 饱和在 ≈ 0.433）】** 上一条把问题归结为「需要 k = N/2 的真实轨道」，并用 (Z₂)³ 奇偶差类不变量给出上界。本轮用**精确轨道划分**检验该不变量是否**完备**。

> · **完备性判据**：不变量在轨道上不变 ⟹ **轨道细分等值集** ⟹ **轨道数 == 等值集数 ⟺ 完备**（严格判据）。

| 格点 | N | C(N,N/2) | \\|G\\| | 轨道数 | 等值集数 | 完备？ | ⟨ln\\|O\\|⟩/N | **H/N** |
|---|---|---|---|---|---|---|---|---|
| (2,2,2) | 8 | 70 | 8 | 14 | 14 | ✅ **完备** | 0.2253 | **0.4679** |
| (2,2,4) | 16 | 12 870 | 128 | 253 | 155 | ❌ 不完备 | 0.2597 | **0.4335** |
| (2,2,6) | 24 | 2 704 156 | 648 | 6 224 | 1 050 | ❌ 不完备 | 0.2602 | **0.4330** |

> · **判决 1（负面）**：**(Z₂)³ 不变量不完备**。N=8 上的 14 = 14 是**偶然**（每个奇偶类只有 1 个点，不变量退化）；N ≥ 16 立即不完备，且**急剧加剧**（N=24：6224 vs 1050）。⟹ 上一条的公式 `|O| = |[n]|·∏ C(N/8,n_i)` 在宏观格点上**不能用**。
> · **判决 2（公式方向）**：公式确为**上界**，且高估倍数随 N 增长 —— 抽查中位数：N=8 **1.00** ⟶ N=16 **2.00** ⟶ N=24 **9.00** ⟹ 上一条的 5.76×10¹⁴ 只是弱上界，**H/N ≥ 0.162 是弱下界**。
> · **判决 3（正面，本轮最有用）**：**H/N 饱和在 ≈ 0.433**（0.4679 ⟶ 0.4335 ⟶ 0.4330；N=16→24 只动 0.0005）。⟹ **面积律要求的 0.25 未被命中**，实测偏大 ≈ 1.73 倍 ⟹ **第 ① 条（不变读数偏大 ~1.75 倍）在本轮能算的所有格点上成立，且不是小格点假象**。
> ⚠️ **口径限制**：三个算例都是 **(2,2,L) 系列**（两方向长度为 2，细长格点），**不代表各向同性三维宏观格点**；(4,4,4) 的 C(64,32) = 1.83×10¹⁸ 不可穷举、(2,4,4) 的 C(32,16) = 6.01×10⁸ 亦超出本轮方法 ⟹ **真实的 3D 宏观值仍未定**，需要 GAP 的 set-stabilizer 或新的采样算法。**不得把 0.433 外推到 N ~ 10¹⁸²**（第 41 轮教训）。
> · **副产品**：不完备度（轨道数/等值集数）= 1.00 ⟶ 1.63 ⟶ **5.93**，随 N 增长 ⟹ 该比值本身可能是有结构的量，已列入候选池。

"""

BLOCK_EN = """
> **【v2.9 supplement (round 46: the exact orbit at k = N/2 — the invariant is incomplete, and H/N saturates at ≈ 0.433)**】** The previous block reduced the question to "the true orbit at k = N/2" and supplied an upper bound via the (Z₂)³ parity-class invariant. This round tests whether that invariant is **complete**, using **exact orbit partitions**.

> · **Completeness criterion**: an invariant is constant on orbits ⟹ **orbits refine the level sets** ⟹ **(#orbits == #level sets) ⟺ complete** (a strict criterion).

| lattice | N | C(N,N/2) | \\|G\\| | #orbits | #level sets | complete? | ⟨ln\\|O\\|⟩/N | **H/N** |
|---|---|---|---|---|---|---|---|---|
| (2,2,2) | 8 | 70 | 8 | 14 | 14 | ✅ **complete** | 0.2253 | **0.4679** |
| (2,2,4) | 16 | 12 870 | 128 | 253 | 155 | ❌ incomplete | 0.2597 | **0.4335** |
| (2,2,6) | 24 | 2 704 156 | 648 | 6 224 | 1 050 | ❌ incomplete | 0.2602 | **0.4330** |

> · **Verdict 1 (negative)**: the **(Z₂)³ invariant is incomplete**. The 14 = 14 at N=8 is **accidental** (each parity class holds a single site, so the invariant degenerates); from N ≥ 16 it fails at once and worsens sharply (N=24: 6224 vs 1050). ⟹ the formula `|O| = |[n]|·∏ C(N/8,n_i)` of the previous block **cannot be used** on macroscopic lattices.
> · **Verdict 2 (direction of the formula)**: it is an **upper bound**, and the overestimate grows with N — median over 600 sampled configurations: N=8 **1.00** ⟶ N=16 **2.00** ⟶ N=24 **9.00** ⟹ the previous 5.76×10¹⁴ is only a weak upper bound and **H/N ≥ 0.162 is a weak lower bound**.
> · **Verdict 3 (positive, the most useful result here)**: **H/N saturates at ≈ 0.433** (0.4679 ⟶ 0.4335 ⟶ 0.4330; from N=16 to 24 it moves by only 0.0005). ⟹ **the 0.25 demanded by the area law is not met**; the measured value is larger by ≈ 1.73× ⟹ **item ① (invariant readouts too large by ~1.75×) holds on every lattice this round can compute, and is not a small-lattice artefact**.
> ⚠️ **Caveat on scope**: all three lattices are of the **(2,2,L) family** (two directions of length 2, i.e. elongated), and **do not represent an isotropic three-dimensional macroscopic lattice**; C(64,32) = 1.83×10¹⁸ for (4,4,4) and C(32,16) = 6.01×10⁸ for (2,4,4) both exceed this round's method ⟹ **the true 3D macroscopic value remains open**, and needs GAP's set-stabilizer or a new sampling algorithm. **Do not extrapolate 0.433 to N ~ 10¹⁸²** (lesson of round 41).
> · **By-product**: the incompleteness ratio (#orbits / #level sets) = 1.00 ⟶ 1.63 ⟶ **5.93** grows with N ⟹ this ratio may itself be a structured quantity; it has been added to the candidate pool.

"""

sub_once(ZH, ANCHOR_ZH, ANCHOR_ZH + BLOCK_ZH, "ZH 插入第 46 轮块")
sub_once(EN, ANCHOR_EN, ANCHOR_EN + BLOCK_EN, "EN 插入第 46 轮块")

print()
print("=" * 70)
print("补丁汇总：成功 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
print("=" * 70)
