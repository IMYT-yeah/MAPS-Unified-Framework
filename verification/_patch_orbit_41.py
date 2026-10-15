# -*- coding: utf-8 -*-
"""
第 41 轮论文补丁（中英同步）。

一处（但很关键）：§4.8 在第 40 轮块之后追加【v2.9 补充（第 41 轮）】，内容包括
  · 生成集化简（196608 ⟹ 51）⟹ Schreier–Sims 第一次能算大格点 |G|；
  · **修正第 40 轮**：「tick 群很小」是小格点假象；N ≥ 64 时 |G| 爆炸
    ⟹ 第 40 轮三难的第 ① 条（不变读数偏大 1.75 倍）**不可外推**；
  · 新不变量：(Z_2)³ 奇偶差类 ⟹ 点对恰 8 条轨道、|O_2| = (N/4)²；
  · 由此给 k = N/2 轨道的上界与 H/N 的界（仍跨 0.25，未定）。

锚点要求恰好命中一次。正文引号一律用「」。
"""

import io
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
STAMP = "2026-09-20第41轮前"

N_OK = [0]
N_FAIL = [0]


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<28} 命中 {} 次 —— 拒绝".format(tag, n))
        N_FAIL[0] += 1
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<28} 已改".format(tag))
    N_OK[0] += 1


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

ZH_A = "本轮**没有**给出观测者分辨率的任何机制。"
ZH_B41 = "\n".join([
    "> **【v2.9 补充（第 41 轮：把 N 推大 —— 上一条的第 ① 条不可外推）** "
    "上一条的诚实边界写的是「只在 N ≤ 16 上穷举」。本轮把它推进，结果是**修正**：",
    "> · **方法（生成集化简）**：一次 tick = 沿某轴的完美匹配、每条线独立相位，"
    "其全部选择有 Σ_轴 2^(线数) 个（4×4×4 = **196608**）。但由 "
    "`M_a·T(p) = ∏_{j:p_j=1} s_j`（M_a = 全 0 相位匹配，s_j = 该线「移 2」）得 "
    "**T(p) = M_a·∏ s_j** ⟹ **G = ⟨M_x, M_y, M_z；所有 s_j⟩**，生成元降到 **3 + 3L²**"
    "（4×4×4：**51**）。已验证：化简集与全集在 2×2×2 / 2×2×4 上给出**逐条相同的轨道划分**。",
    "> · **修正（|G| 爆炸）**：|G| = 8（N=8）⟶ 128（N=16）⟶ **2.794×10³⁷（N=64）** "
    "⟶ **6.176×10²²²（N=216）**（Schreier–Sims 精确值；前两个与第 40 轮穷举 BFS 逐位一致）。"
    "ln|G|/N = 0.26 ⟶ 0.30 ⟶ **1.35** ⟶ **2.37**，**远超**判据阈值 0.4431。",
    "> ⟹ **上一条的第 ① 条（不变读数偏大约 1.75 倍）只在 N ≤ 16 成立**："
    "N ≥ 64 时 |G| 已远大于需求 `1.557^N`（N=64：2.79×10³⁷ vs 2.08×10¹²），"
    "`|O| ≤ |G|` 这个上界**完全失效**，该结论**不可外推**到宏观格点。",
    "> · **新不变量（本轮正面产出）**：设 π(p) ∈ (Z₂)³ 为三坐标奇偶类，则任何 tick 都保持 "
    "**δ(p,q) = π(p)+π(q) (mod 2)**（s_j 保持 π；M_a 把全体格点的奇偶类**同一个** ê_a 平移）。"
    "穷举全部生成元 × 全部点对验证通过。⟹ **点对恰有 8 条轨道**，且实测 "
    "**|O₂| = (N/4)²**（N = 8/16/64/216 四算例全中），|O₃| = 1792 ≪ C(64,3) = 41664 "
    "⟹ 群**不是 2-可迁的**（尽管 |G| 已爆炸）。",
    "> · **由此给 k = N/2 轨道的上界**：不变量 = 各奇偶类选中数 `(n_0,…,n_7)` **模 (Z₂)³ 平移** "
    "⟹ `|O| ≤ ∏_i C(N/8, n_i)`，均分时最大 ⟹ N=64：5.76×10¹⁴ ⟹ **H/N ≥ 0.162**。",
    "> ⚠️ **仍未定**：H/N 的界为 **0.162 – 0.693**，**跨过 0.25** ⟹ 宏观精确值待 "
    "k = N/2 的**真实轨道**（需要 set-stabilizer；sympy 目前不提供）。"
    "⟹ 上一条的「三难」应改写为「**两难 + 一个结构**」：不变的读数既非「太多」（第 ① 条不可外推）、"
    "也非「太少」（群非高度可迁），而是**受 (Z₂)³ 不变量约束**。",
    "",
])
sub_once(ZH, ZH_A, ZH_B41, "ZH §4.8 第 41 轮块")

EN_A = "This round provides **no mechanism** for the observer's resolution."
EN_B41 = "\n".join([
    "> **【v2.9 supplement (round 41: pushing N up — item ① of the previous block does not "
    "extrapolate)】** The honest limit of the previous block says \"exhaustive only for N ≤ 16\". "
    "This round pushes it forward, and the result is a **correction**:",
    "> · **Method (generator reduction)**: one tick = a perfect matching along one axis with an "
    "independent per-line phase, so the full set has Σ_axis 2^(#lines) elements (4×4×4: **196608**). "
    "But from `M_a·T(p) = ∏_{j:p_j=1} s_j` (M_a = all-zero-phase matching, s_j = \"shift by 2\" on "
    "that line) we get **T(p) = M_a·∏ s_j** ⟹ **G = ⟨M_x, M_y, M_z; all s_j⟩**, reducing the "
    "generators to **3 + 3L²** (4×4×4: **51**). Verified: the reduced set and the full set give "
    "**identical orbit partitions** on 2×2×2 and 2×2×4.",
    "> · **Correction (|G| explodes)**: |G| = 8 (N=8) ⟶ 128 (N=16) ⟶ **2.794×10³⁷ (N=64)** ⟶ "
    "**6.176×10²²² (N=216)** (exact Schreier–Sims values; the first two agree digit for digit with "
    "the round-40 exhaustive BFS). ln|G|/N = 0.26 ⟶ 0.30 ⟶ **1.35** ⟶ **2.37**, **far above** the "
    "criterion threshold 0.4431.",
    "> ⟹ **Item ① of the previous block (invariant readout too large by ≈ 1.75×) holds only for "
    "N ≤ 16**: at N ≥ 64, |G| already far exceeds the requirement `1.557^N` (N=64: 2.79×10³⁷ vs "
    "2.08×10¹²), so the bound `|O| ≤ |G|` **fails completely** and that conclusion **cannot be "
    "extrapolated** to macroscopic lattices.",
    "> · **New invariant (this round's positive output)**: let π(p) ∈ (Z₂)³ be the parity class of "
    "the three coordinates; then every tick preserves **δ(p,q) = π(p)+π(q) (mod 2)** (s_j preserves "
    "π; M_a translates the parity classes of *all* sites by the *same* ê_a). Verified exhaustively "
    "over all generators × all pairs. ⟹ **pairs have exactly 8 orbits**, and measurement gives "
    "**|O₂| = (N/4)²** (all four cases N = 8/16/64/216), with |O₃| = 1792 ≪ C(64,3) = 41664 "
    "⟹ the group is **not 2-transitive** (even though |G| has exploded).",
    "> · **An upper bound for the k = N/2 orbit follows**: the invariant is the vector of selection "
    "counts `(n_0,…,n_7)` **modulo (Z₂)³ translation** ⟹ `|O| ≤ ∏_i C(N/8, n_i)`, maximal when "
    "spread evenly ⟹ N=64: 5.76×10¹⁴ ⟹ **H/N ≥ 0.162**.",
    "> ⚠️ **Still open**: the bracket for H/N is **0.162 – 0.693**, which **straddles 0.25** ⟹ the "
    "macroscopic value awaits the **true orbit at k = N/2** (a set-stabilizer is needed; sympy does "
    "not provide one). ⟹ The \"trilemma\" of the previous block should be rewritten as \"**a "
    "dilemma plus one structure**\": the invariant readout is neither \"too much\" (item ① does not "
    "extrapolate) nor \"too little\" (the group is not highly transitive); it is **constrained by "
    "the (Z₂)³ invariant**.",
    "",
])
sub_once(EN, EN_A, EN_A + "\n" + EN_B41, "EN §4.8 round-41 block")

print("")
print("通过 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
