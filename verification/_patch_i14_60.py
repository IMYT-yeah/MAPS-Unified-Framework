# -*- coding: utf-8 -*-
"""第 60 轮论文补丁：I-14 的裁决（中英同步）。
锚点：§5 标题（在它前面的 `---` 之前插入新块，使新块留在 §4.8 的 v2.9 补充链末尾）。"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

OK = 0
BAD = 0


def sub_once(path, old, new, tag):
    global OK, BAD
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<30} 命中 {} 次 —— 拒绝".format(tag, n))
        BAD += 1
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<30} 已改".format(tag))
    OK += 1


# ══════════════════════════════════════════════════════════════════════
ZH_ANCHOR = "\n---\n\n## 5 规范群结构"
ZH_BLOCK = "\n".join([
    "",
    "> **【v2.9 补充（第 60 轮：I-14 的裁决 —— 框架的差是「谱内差」，不是「构型差」）】** 第 56 轮登记 I-14，表述为「框架的全部定量输出**没有一个「两态之差」**」。本轮做**可判定版**（脚本 `_i14_60.py`，I14-1…I14-10，**10 项 0 失败**）：结论是**原表述字面错误、但方向对**，修订后更强。",
    ">",
    "> · **原表述被否**：λ=0 弦网凝聚的激发能隙 **Δ = 2**（§5.8，**严格**）**就是**「两态之差」（基态 vs 激发态）⟹ 正确的问法不是「有没有差」，而是**差的是什么**。",
    ">",
    "> · **必须排除的元文本（本轮新踩的坑）**：第 56 轮块**自己列举了**「解离 / 束缚能」等词，使它们从 0 处变成 2 处 ⟹ **引文清点必须先排除已登记的轮次块**（判据：`> ` 起始的连续引用块）。排除后：中文 **0** 处、英文 **0** 处（16 + 11 个关键词）。",
    ">",
    "> · **三个反例候选，逐个判掉**：",
    ">   ① **弦网能隙 Δ** —— 2+1D 环面 L=2 与 L=3（解析公式 + 256 态数值**逐项一致**）；3+1D 复现 §5.8 的 `E0 = −N_c`、简并 `2^(n−N_c) = 512/1024/512`、`Δ = 2` ✓。⟹ 它是**谱内差**（同一格点、**同一参数**下的两个本征值），差的是**通量构型**，不含物质排布信息；",
    ">   ② **禁闭弦势 `E_pair(d) = 2E_m + σ_m·d`**（§5.7）⟹ 这是框架里**唯一**随「位置」变化的能量。但 **σ_m ≥ 0 在所有可用数值里成立**（0.21 / 1.09 / 3.04 @ λ = 0.5/1.0/2.0；λ=0 严格 deconfined 时 dE 与 d **无关**）⟹ 弦势**恒单调不减 ⟹ 没有极小 ⟹ 不存在势阱**。**束缚态的判据就是「势有极小」⟹ 单调势 ⟹ 无束缚态**（结构上不可能，不是「还没算出来」）。且它的物理身份是**禁闭**（§5.7「胶球 = 通量自束缚」，BESIII X(2370) 锚点），**不是化学键**；",
    ">   ③ **空间平移 → 动量**（守恒律表）⟹ Noether 给的是**守恒量**，**不是势能面 V(R)**；且它是**格点背景**的对称性，不是「物质可在其中移动并改变相对距离」的自由度。（框架**继承**的引力束缚 / EMRI 同属「继承 + 天体尺度」，不同类。）",
    ">",
    "> · ⭐ **核心判据（本轮主结论）：位置与能量在框架里分层居住** ——",
    ">   **衬底层**（tick 置换群）的态是 k-子集 = k 个格点的**空间分布**（**有位置**），但框架只给它 **H/N（熵密度），无能量**；",
    ">   **弦网层**（`H_F` / `H(λ)`）**有哈密顿量与能量谱**，但它的态是面变量 `Z_f`（**通量**，不是位置）。",
    ">   ⟹ **有位置的层没有能量；有能量的层没有位置。** 而化学键恰恰要求 **能量 × 位置 的耦合**（`E` 随核间距 `R` 变化）—— 框架没有这一项。",
    ">   ⟹ 框架能说「哪个排布更无序」（(2,2,L) 系列 H/N = 0.4679 / 0.4335 / 0.4334 / 0.4617），**不能说「哪个排布能量更低」**。",
    ">",
    "> · **三类差的总表**：**谱内差**（Δ、Δ±2）｜**参数差**（E0(λ)、m(κ) —— 那是**相图**，不是两个态）｜**弦势差**（无极小）。**三类都成立，但都不等价于「束缚能」。**",
    ">",
    "> · **边界扩大**：**化学键 / 键能**（需 `V(R)` 势阱）、**相变潜热**（需两相自由能差 —— 框架**有相变** `λ_c ∈ [0.21, 0.23]`、`κ_c ∈ [0.25, 0.32]`，但「自由能 / 潜热 / 化学势」**实质各 0 处** ⟹ **有相变 ≠ 有潜热**）、**电离能**（需「一个电子被移走后的排布差」）**一并落在框架语言之外**。尺度：`J = n_G·E_P·g ≈ 3.6627×10²⁸ eV` vs 化学键 1.4798 eV ⟹ **28.4 个数量级**；且弦势的单位是「1 个格点」，换物理长度还需**格点间距 a**（**未给**）⟹ **两个换算因子都缺**。",
    ">",
    "> · **一句话**：**框架的能量语言是「禁闭档」（无势阱、普朗克标度），化学键是「势阱档」（有极小、Å 尺度）—— 两者缺的不是精度，是「势」本身。**",
    ">",
    "> · ⚠️ **待核实（本轮顺带发现）**：§5.7 记「能隙 **Δ = 1**」，而本轮 2+1D 环面（2×2 与 3×3、解析与数值四个算例）**一律给 Δ = 4J**（3+1D 的 Δ = 2 已复现 ✓）。结构理由：3+1D 的 `A_c` 共享面出现 2 次 ⟹ `Z² = 1` ⟹ **无约束** ⟹ 可独立翻转（2J）；2+1D 的 `A_v` 共享边 ⟹ `Π_v A_v = 1` **构成约束** ⟹ 激发**必须成对**（4J）。**仅登记，不改数值。**",
    ">",
    "> · **诚实标注**：「谱内差 ≠ 构型差」这个**区分**是本轮**自拟**的（**非定理**）；「束缚态 ⟺ 势有极小」用在**离散格点**上是**类比**；**未证明**「框架不可能涌现出势阱型构型差」—— 本轮只证明**现有的四个哈密顿量**里没有。⟹ **I-14 不撤销，改修订版。**",
    "",
])
sub_once(ZH, ZH_ANCHOR, ZH_BLOCK + ZH_ANCHOR, "ZH §4.8 链末（第 60 轮块）")

# ══════════════════════════════════════════════════════════════════════
EN_ANCHOR = "\n---\n## 5 Gauge-Group Structure"
EN_BLOCK = "\n".join([
    "",
    "> **【v2.9 supplement (round 60: adjudicating I-14 — the framework's differences are *spectral*, not *configurational*)】** Round 56 registered I-14 as \"every quantitative output of the framework (spectrum / gap / degeneracy / order parameter / chi / string tension / entropy / exponent) contains **not one two-state difference**\". This round runs the **decidable version** (script `_i14_60.py`, I14-1…I14-10, **10 pass / 0 fail**): the original statement is **literally wrong, but its direction is right** — and the revised version is stronger.",
    ">",
    "> · **The original statement is refuted**: the excitation gap of the lambda=0 string-net condensate, **Delta = 2** (§5.8, **rigorous**), **is** a two-state difference (ground vs excited) ⟹ the right question is not *whether* a difference exists but **what it differs over**.",
    ">",
    "> · **Meta-text must be excluded (a trap newly hit this round)**: the round-56 block **itself lists** the words \"dissociation / binding energy\", turning them from 0 occurrences into 2 ⟹ **citation counting must first exclude the already-registered round blocks** (criterion: contiguous quote blocks starting with `> `). After exclusion: **0 occurrences in Chinese, 0 in English** (16 + 11 keywords).",
    ">",
    "> · **Three counter-example candidates, each adjudicated**:",
    ">   ① **The string-net gap Delta** — 2+1D torus L=2 and L=3 (analytic formula + 256-state numerics, **matching term by term**); 3+1D reproduces §5.8's `E0 = -N_c`, degeneracy `2^(n-N_c) = 512/1024/512`, `Delta = 2` ✓. ⟹ It is a **spectral difference** (two eigenvalues on the *same* lattice at the *same* parameters): what differs is the **flux configuration**, which carries no matter-arrangement information;",
    ">   ② **The confinement string potential `E_pair(d) = 2E_m + sigma_m*d`** (§5.7) ⟹ the framework's **only** position-dependent energy. But **sigma_m >= 0 holds in every available number** (0.21 / 1.09 / 3.04 at lambda = 0.5/1.0/2.0; at lambda=0, strictly deconfined, dE is **independent of d**) ⟹ the string potential is **monotonically non-decreasing ⟹ has no minimum ⟹ no potential well exists**. **The criterion for a bound state is precisely \"the potential has a minimum\" ⟹ a monotonic potential ⟹ no bound state** (structurally impossible, not merely \"not yet computed\"). And its physical identity is **confinement** (§5.7, \"glueball = flux self-bound state\", BESIII X(2370) anchor), **not a chemical bond**;",
    ">   ③ **Spatial translation -> momentum** (conservation-law table) ⟹ Noether gives a **conserved charge**, **not a potential energy surface V(R)**; and it is a symmetry of the **lattice background**, not the freedom of \"matter moving within it and changing its relative separation\". (The gravitational binding / EMRI that the framework **inherits** is likewise \"inherited + astrophysical scale\" — a different class.)",
    ">",
    "> · **Core criterion (this round's main conclusion): position and energy live in separate layers** —",
    ">   The **substrate layer** (tick permutation group) has states that are k-subsets = the **spatial distribution** of k lattice sites (**it has position**), yet the framework gives it only **H/N (an entropy density), no energy**;",
    ">   the **string-net layer** (`H_F` / `H(lambda)`) **has a Hamiltonian and an energy spectrum**, but its states are face variables `Z_f` (**flux**, not position).",
    ">   ⟹ **The layer with position has no energy; the layer with energy has no position.** A chemical bond requires precisely the **coupling of energy with position** (`E` varying with the internuclear distance `R`) — the framework has no such term.",
    ">   ⟹ The framework can say *which arrangement is more disordered* ((2,2,L) series H/N = 0.4679 / 0.4335 / 0.4334 / 0.4617) but **cannot say which arrangement has lower energy**.",
    ">",
    "> · **Summary of the three classes of difference**: **spectral** (Delta, Delta_pm2) | **parametric** (E0(lambda), m(kappa) — that is a **phase diagram**, not two states) | **string-potential** (no minimum). **All three hold, none of them is a binding energy.**",
    ">",
    "> · **The boundary widens**: **chemical bonds / bond energies** (need a `V(R)` well), **latent heat of phase transitions** (need a free-energy difference between phases — the framework **has transitions** at `lambda_c in [0.21, 0.23]` and `kappa_c in [0.25, 0.32]`, yet \"free energy / latent heat / chemical potential\" occur **0 times in substance** ⟹ **a transition is not a latent heat**), and **ionization energies** (need the arrangement difference of \"one electron removed\") — **all three fall outside the framework's language**. Scale: `J = n_G*E_P*g ~ 3.6627e28 eV` vs a chemical bond at 1.4798 eV ⟹ **28.4 orders of magnitude**; moreover the string potential is measured in \"1 lattice site\", so converting to a physical length still needs the **lattice spacing a** (**not given**) ⟹ **both conversion factors are missing**.",
    ">",
    "> · **In one line**: **the framework's energy language is the \"confinement tier\" (no well, Planck scale); a chemical bond is the \"well tier\" (has a minimum, Angstrom scale) — what separates them is not precision, but the potential itself.**",
    ">",
    "> · ⚠️ **To be verified (found in passing this round)**: §5.7 records a gap of **Delta = 1**, whereas this round's 2+1D torus (2x2 and 3x3; four independent analytic and numerical cases) **uniformly gives Delta = 4J** (the 3+1D Delta = 2 was reproduced ✓). Structural reason: in 3+1D each `A_c` shares a face that appears **twice** ⟹ `Z^2 = 1` ⟹ **no constraint** ⟹ independent flips (2J); in 2+1D the `A_v` share edges ⟹ `Pi_v A_v = 1` **is a constraint** ⟹ excitations **must come in pairs** (4J). **Recorded only; the number is not changed.**",
    ">",
    "> · **Honest notes**: the *distinction* between \"spectral difference ≠ configurational difference\" is **self-formulated** here (**not a theorem**); \"bound state ⟺ the potential has a minimum\" is, on a **discrete lattice**, an **analogy**; and it is **not proved** that the framework *cannot* ever produce a well-type configurational difference — this round shows only that the **four existing Hamiltonians** do not. ⟹ **I-14 is not withdrawn; it is revised.**",
    "",
])
sub_once(EN, EN_ANCHOR, EN_BLOCK + EN_ANCHOR, "EN §4.8 chain end (round-60 block)")

print()
print("通过 {} 项，失败 {} 项".format(OK, BAD))
