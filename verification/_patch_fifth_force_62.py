# -*- coding: utf-8 -*-
"""第 62 轮论文补丁（中英同步）：① §5.5 加「第五力的位置」注；② 插入【第 62 轮】块。"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

OK = 0
BAD = 0


def sub_once(path, old, new, tag):
    global OK, BAD
    t = io.open(path, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        print("  [XX] {:<32} 命中 {} 次 —— 拒绝".format(tag, n))
        BAD += 1
        return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    print("  [OK] {:<32} 已改".format(tag))
    OK += 1


# ── ① §5.5 加「第五力的位置」注 ─────────────────────────────────────────
ZH_NOTE = "\n".join([
    "",
    "**第五力的位置（第 62 轮加注）**：「四力」之后，两个**结构化**的扩展位都被封死 ——",
    "① **自旋 1 的额外规范群**：由 §5.2 的 `n ≥ 4` 排除（3 维空间里 `ε_ijkl ≡ 0`，因为 `C(3,4) = 0`）；",
    "② **自旋 ≥ 3**：由 **Weinberg–Witten 定理**（平坦时空中无质量 `j > 2` 不可能）封死，",
    "而同一条 **Weinberg 软定理**的分类也把自旋 3 挡在门外（自旋 2 是边界）。",
    "",
    "⚠️ **关键判据：本表的「自旋」栏等价于「软极限的奇异幂次」栏** ——",
    "**「力」= 被 Weinberg 软定理强制的普适耦合**：自旋 2（软极限 ∝ 1/q ⟹ 等价原理）与",
    "自旋 1（∝ 1/q ⟹ 守恒荷）**被强制**，而**自旋 0 的软极限 ∝ q⁰ 不奇异 ⟹ 不强制任何守恒荷**",
    "⟹ **自旋 0 天生不是「基本力」** —— 这正是本表把 Φ 标为「Higgs/模场」的深层理由。",
    "",
    "⚠️ 但软定理**没有**禁止「**非普适**的长程标量耦合」（标准物理里的第五力正是如此），",
    "而框架恰好把一个自旋 0 分量写成 **Φ = KK 标量模场（g₅₅）的低能投影**（§4.5b）——",
    "那在标准 KK 里正是 **radion / dilaton**，即**公认的第五力载体**。框架对 Φ 只写了一句",
    "「VEV 决定耦合常数与质量」，**未给质量与耦合** ⟹ **该位置的状态 = 未定义**（登记 **I-17**）。",
    "若假设 Φ 继承 §5.8 的弦网标量扇区能隙（`Δ_标量 = 0.41 J`），则 `m = 1.50×10²⁸ eV`、",
    "力程 **`λ = 0.81 l_P`** ⟹ 与第五力搜索窗口（微米–星系）相差 **29–55 个数量级**（完全不可观测）。",
    "",
])
sub_once(ZH, "\n### 5.6 量子双代数：框架规范结构（v1.19 新增）",
         ZH_NOTE + "### 5.6 量子双代数：框架规范结构（v1.19 新增）", "ZH §5.5 第五力加注")

EN_NOTE = "\n".join([
    "",
    "**Where a fifth force would sit (added in round 62)**: after the four forces, both **structural** extension slots are closed —",
    "(1) **an extra gauge group at spin 1**: excluded by §5.2's `n >= 4` (in 3 dimensions `ε_ijkl ≡ 0`, since `C(3,4) = 0`);",
    "(2) **spin >= 3**: excluded by the **Weinberg–Witten theorem** (no massless `j > 2` in flat spacetime),",
    "and the same **Weinberg soft theorem** classification bars spin 3 as well (spin 2 is the boundary).",
    "",
    "⚠️ **Key criterion: this table's \"spin\" column is equivalent to a \"singular power of the soft limit\" column** —",
    "**a \"force\" is a universal coupling *enforced* by the Weinberg soft theorem**: spin 2 (soft limit ∝ 1/q ⟹ equivalence principle) and",
    "spin 1 (∝ 1/q ⟹ conserved charge) are **enforced**, whereas **the spin-0 soft limit ∝ q⁰ is non-singular ⟹ it enforces no conserved charge**",
    "⟹ **spin 0 is intrinsically not a \"fundamental force\"** — this is the deeper reason the table labels Φ as \"Higgs / modulus field\".",
    "",
    "⚠️ But the soft theorem does **not** forbid a **non-universal** long-range scalar coupling (which is exactly what a fifth force is in standard physics),",
    "and the framework happens to write one spin-0 component as **Φ = the low-energy projection of a KK scalar modulus field (g₅₅)** (§4.5b) —",
    "which in standard KK is precisely a **radion / dilaton**, i.e. a **recognized fifth-force carrier**. The framework says only one sentence about Φ",
    "(\"its VEV determines the coupling constants and masses\") and **gives neither its mass nor its coupling** ⟹ **that slot's status = undefined** (registered as **I-17**).",
    "If one assumes Φ inherits the string-net scalar-sector gap (`Δ_scalar = 0.41 J`), then `m = 1.50×10²⁸ eV` and the range is",
    "**`λ = 0.81 l_P`** ⟹ **29–55 orders of magnitude** away from the fifth-force search windows (micron to galactic) — utterly unobservable.",
    "",
])
sub_once(EN, "\n### 5.6 Quantum-double algebra: the framework's gauge structure (v1.19)",
         EN_NOTE + "### 5.6 Quantum-double algebra: the framework's gauge structure (v1.19)", "EN §5.5 fifth-force note")

# ── ② 插入【第 62 轮】块（§4.8 链末）────────────────────────────────────
ZH_BLOCK = "\n".join([
    "",
    "> **【v2.9 补充（第 62 轮：第五种力在框架里有位置吗？—— 三个候选位：两个封死，一个未定义）】** 词条清点：「第五力 / 五力 / fifth force / spin-3」**全文 0 处** —— 本轮是**首次**处理（脚本 `_fifth_force_62.py`，FF-1…FF-8，**8 项 0 失败**）。",
    ">",
    "> · **「第五种力」有两个意思，答案不同**：① 作为**第五个基本相互作用**（结构化、普适耦合）⟹ **不可能**；② 作为**新的长程标量力**（唯象、非普适）⟹ **未定义**。",
    ">",
    "> · **三个候选位逐一判定**（框架的「四力」= §5.5 的分波分解 × §5.2 的配对阶数，四个位置无空位）：",
    ">   ① **自旋 1 的额外规范群** ⟹ **封死**：§5.2 的 `n ≥ 4` 排除，依据是**维数论证**（`ε_ijkl` 在 3 维空间 ≡ 0，因为独立分量数 `C(3,4) = 0`）；",
    ">   ② **自旋 ≥ 3** ⟹ **封死**：**Weinberg–Witten 定理**（平坦时空中无质量 `j > 2` 不可能）+ 同一条 **Weinberg 软定理**分类（自旋 2 是边界）；",
    ">   ③ **自旋 0 的新轻标量** ⟹ ⚠️ **未定义**：见下。",
    ">",
    "> · ⭐ **关键判据（本轮把 §5.8 的软定理接到分波表上）**：**「力」= 被 Weinberg 软定理强制的普适耦合** —— 自旋 2（软极限 ∝ 1/q ⟹ 等价原理）与自旋 1（∝ 1/q ⟹ 守恒荷）**被强制**，而**自旋 0 的软极限 ∝ q⁰ 不奇异 ⟹ 不强制任何守恒荷** ⟹ 自旋 0 **天生不是「基本力」**。**这解释了 §5.5 为什么把 Φ 标为「Higgs/模场」而非「力」。**",
    ">",
    "> · ⚠️ **但缺口在这里**：软定理**没有**禁止「非普适的长程标量耦合」（标准物理的第五力正是如此）；而框架把一个自旋 0 分量写成 **`Φ = KK 标量模场（g₅₅）的低能投影`**（§4.5b）—— 那在标准 KK 里正是 **radion / dilaton**，**公认的第五力载体**。框架对 Φ 只写一句「VEV 决定耦合常数与质量」，**未给质量、未给耦合、未说明它与弦网能隙的关系** ⟹ 登记 **I-17**。",
    ">",
    "> · **数值**：若假设 Φ 继承 §5.8 的弦网标量扇区能隙（`Δ_标量 = 0.41 J`），则 `m = 0.41 J = 1.50×10²⁸ eV`、力程 **`λ = ℏc/m = 1.31×10⁻³⁵ m = 0.81 l_P`** ⟹ 与第五力搜索窗口（Casimir/微米 10⁻⁶ m → 星系 3.1×10²⁰ m）相差 **28.9 – 55.4 个数量级**（完全不可观测）。",
    ">",
    "> · **诚实标注**：「位①封死」用的是 §5.2 的**维数论证**（论文原有）与本轮的组合核验；「位②封死」与「自旋 0 不是基本力」是**引用** Weinberg–Witten 与 Weinberg 软定理（**不是框架推出的**）；**未**核验 `Δ_标量 = 0.41`（引用 v1.34 结果）；标准物理侧的第五力上界数字来自**网络检索（聚合来源）**，**未经一手文献核实**，故只保留量级。",
    "",
])
sub_once(ZH, "\n---\n\n## 5 规范群结构", ZH_BLOCK + "\n---\n\n## 5 规范群结构", "ZH 插入第 62 轮块")

EN_BLOCK = "\n".join([
    "",
    "> **【v2.9 supplement (round 62: is there room for a fifth force in the framework? — three candidate slots: two closed, one undefined)】** Terminology count: \"fifth force / 五力 / spin-3\" occurs **0 times** in the whole paper — this round is the **first** treatment (script `_fifth_force_62.py`, FF-1…FF-8, **8 pass / 0 fail**).",
    ">",
    "> · **\"Fifth force\" has two meanings, with different answers**: (1) as a **fifth fundamental interaction** (structural, universal coupling) ⟹ **impossible**; (2) as a **new long-range scalar force** (phenomenological, non-universal) ⟹ **undefined**.",
    ">",
    "> · **The three candidate slots, adjudicated one by one** (the framework's \"four forces\" = §5.5's partial-wave decomposition × §5.2's pairing order, with no vacant positions):",
    ">   (1) **an extra gauge group at spin 1** ⟹ **closed**: excluded by §5.2's `n >= 4` via a **dimensionality argument** (`ε_ijkl ≡ 0` in 3 dimensions, since the number of independent components is `C(3,4) = 0`);",
    ">   (2) **spin >= 3** ⟹ **closed**: the **Weinberg–Witten theorem** (no massless `j > 2` in flat spacetime) + the same **Weinberg soft theorem** classification (spin 2 is the boundary);",
    ">   (3) **a new light scalar at spin 0** ⟹ ⚠️ **undefined**: see below.",
    ">",
    "> · ⭐ **Key criterion (this round connects §5.8's soft theorem to the partial-wave table)**: **a \"force\" is a universal coupling *enforced* by the Weinberg soft theorem** — spin 2 (soft limit ∝ 1/q ⟹ equivalence principle) and spin 1 (∝ 1/q ⟹ conserved charge) are **enforced**, whereas **the spin-0 soft limit ∝ q⁰ is non-singular ⟹ it enforces no conserved charge** ⟹ spin 0 is **intrinsically not a \"fundamental force\"**. **This explains why §5.5 labels Φ as a \"Higgs / modulus field\" rather than a \"force\".**",
    ">",
    "> · ⚠️ **But the gap is here**: the soft theorem does **not** forbid a **non-universal** long-range scalar coupling (exactly what a fifth force is in standard physics); and the framework writes one spin-0 component as **`Φ = the low-energy projection of a KK scalar modulus field (g₅₅)`** (§4.5b) — which in standard KK is a **radion / dilaton**, a **recognized fifth-force carrier**. The framework says only one sentence about Φ (\"its VEV determines the coupling constants and masses\") and gives **neither its mass, nor its coupling, nor its relation to the string-net gap** ⟹ registered as **I-17**.",
    ">",
    "> · **Numbers**: if one assumes Φ inherits §5.8's string-net scalar-sector gap (`Δ_scalar = 0.41 J`), then `m = 0.41 J = 1.50×10²⁸ eV` and the range is **`λ = ℏc/m = 1.31×10⁻³⁵ m = 0.81 l_P`** ⟹ **28.9 – 55.4 orders of magnitude** away from the fifth-force search windows (Casimir/micron 10⁻⁶ m → galactic 3.1×10²⁰ m) — utterly unobservable.",
    ">",
    "> · **Honest notes**: \"slot (1) closed\" rests on §5.2's **dimensionality argument** (pre-existing) plus this round's combinatorial check; \"slot (2) closed\" and \"spin 0 is not a fundamental force\" are **citations** of Weinberg–Witten and the Weinberg soft theorem (**not derived from the framework**); `Δ_scalar = 0.41` was **not re-verified** (cited from v1.34); and the fifth-force bounds on the standard-physics side come from a **web search (aggregator sources)**, **not checked against primary literature**, so only orders of magnitude are retained.",
    "",
])
sub_once(EN, "\n---\n## 5 Gauge-Group Structure", EN_BLOCK + "\n---\n## 5 Gauge-Group Structure", "EN insert round-62 block")

print()
print("通过 {} 项，失败 {} 项".format(OK, BAD))
