# -*- coding: utf-8 -*-
"""第 76 轮论文补丁（中英同步 4 项）：§7.2 判别力标注 ＋ §7.4 块链末插【第 76 轮】块"""
import io, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(ROOT, "MAPS-Unified-Framework", "paper", "history")
TAG = "2026-10-02第76轮前"

for p in (ZH, EN):
    b = os.path.join(HIST, os.path.basename(p).replace(".md", "_备份_{}.md".format(TAG)))
    shutil.copy2(p, b)
    print("  [BK] {}".format(os.path.basename(b)))


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<30} 命中 {} 次 —— 拒绝".format(tag, n))
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<30} 已改".format(tag))


# ── 1. ZH §7.2 判别力标注 ────────────────────────────────
ZH_A = "**数值验证**：Bell 态 |ψ⁻⟩ + 最优测量基 ⟹ S = −2.8284 = −2√2 ✓；路径态内积 a 时 V²+I² = 1 ✓。"
ZH_A_NEW = ZH_A + """

> **【第 76 轮判别力标注】** 上式 `S = −2√2` 的复现**只用到 2 个 qubit 与 Pauli 矩阵** —— `tick` / 弦网 / `A_v` / `B_p` / 通量 / 格点**一个都没有出现** ⟹ 它是 **Tsirelson 定理**（算子代数上的代数事实），**不是框架特有的结果**；本节命题的形式是「**若**含 `{Π_μ,Π_ν}≠0` **则** CHSH = 2√2」，**前提已把结论塞进去**。框架自有非交换元素的逐条判定见 §7.4 末【第 76 轮】块。"""
sub_once(ZH, ZH_A, ZH_A_NEW, "ZH §7.2 判别力标注")

# ── 2. EN §7.2 discriminator annotation ──────────────────
EN_A = "**Numerical verification**: Bell state |ψ⁻⟩ + optimal measurement basis ⟹ S = −2.8284 = −2√2 ✓; path-state inner product gives V²+I² = 1 ✓."
EN_A_NEW = EN_A + """

> **【Round-76 discriminating-power annotation】** The reproduction of `S = −2√2` above uses **only 2 qubits and Pauli matrices** — `tick` / string net / `A_v` / `B_p` / flux / lattice **appear nowhere** ⟹ it is the **Tsirelson theorem** (an algebraic fact about operator algebras), **not a framework-specific result**; the proposition of this subsection has the form "**if** `{Π_μ,Π_ν}≠0` **then** CHSH = 2√2", i.e. **the premise already contains the conclusion**. An item-by-item verdict on the framework's own non-commutative elements is given in the round-76 block at the end of §7.4."""
sub_once(EN, EN_A, EN_A_NEW, "EN §7.2 annotation")

# ── 3. ZH §7.4 块链末插【第 76 轮】块 ────────────────────
ZH_ANCHOR = "> ⚠️ **五条诚实边界**：① **强版依赖「𝒜 就是全部」这一设定**"
ZH_BLOCK = """
---

> **【v2.9 补充（第 76 轮：§7 量子力学基础审计 —— 非交换化是「外加」的，判别力 = 0）】** 本轮是**审计 ＋ 引文取证 ＋ 数值**（脚本 `_qm_audit_76.py`，**QM-1 … QM-12，12 项 0 失败**）。§7 是**唯一未被审计过的大章**：去掉已登记的轮次块后**仅 15 行非空正文**（70 行里 41 行是第 57 / 68 轮块）。
>
> · ⭐ **本轮唯一的正面产出（§7.1 可升级为定理）**：枚举全部 2⁴ = 16 个确定性局域策略，**max CHSH = 2**（5000 组随机混合权重的 max 为 1.0879，凸组合不越界）⟹ §7.1 的主张可从「断言」升级为**引用 Fine 定理（1982）的推论**：**若可观测代数交换（允许联合概率分布），则 CHSH ≤ 2** ⟹ 与 CHSH = 2√2 相容的理论，其可观测代数**必然非交换**。这是框架内**唯一一条有严格外部定理支撑的「必然性」论证**。⚠️ 但它证明的是「**若**交换则不可能」，**不是**「框架的可观测代数交换」—— 后者是 §7.1 的**前提**（未证），也正是 §7.2 用「升级为算子代数」这个**动作**绕过去的地方。
>
> · **§7.2 的命题是条件命题（零内容）**：用 **2 个 qubit** 完整复现 `S = −2.8284 = −2√2`，而**用到的输入只有 4 个 Pauli 矩阵与一个 2-qubit 态** ⟹ 结论是 **Tsirelson 定理**，**前提已把结论塞进去**；§7.2 自称的「数值验证」证明的是标准 QM 的教科书结果。
>
> · ⭐ **「框架已有非交换元素」4 条逐条判定**：只有 **Clifford 投影**真非交换（`‖[Π_1,Π_2]‖_max = 0.5`、`‖{Π_1,Π_2}‖_max = 0.7071`、`(Π_μ)² = Π_μ`）—— 而它是 §5.2 的**表示论记号**（内空间 4 分量），不是动力学；`(−1)^N_exchange` 是**阿贝尔相位**（±1 对角权重；**Fock / 二次量子化 / 产生算符 / 湮灭算符 / 交换算符 / 置换算符在全文各 0 处**）；「叠加态几何起源（全局等价）」是**等式**；「量子直线」是**通道**。
>   ⭐ 附带（数值）：**弦网代数（`A_v` / `B_p`）完全交换** —— 顶点与面共享**恰好 2 条边** ⟹ 反对易 2 次 ⟹ 净交换；Pauli 辛表示与 L=2 的 **256 维全矩阵**两法一致（`‖AB−BA‖_max = 0`），在 **2×2 / 3×3 / 2×4** 三个格点上不交换对数均为 **0**。⟹ §7.2 的 4 条里**没有一条是弦网**，而弦网是框架**唯一**有严格哈密顿量与数值验证（§5.7）的部分。
>
> · **判别力 = 0（§7.4 自认）**：§7 正文的全部物理数值 = `{2√2, ½, −2.8284}`，**全为教科书常数**；§7.4 自己写着「一旦非交换化，框架的量子部分与标准 QM **数学上重合**」⟹ 与 **N-29**（宇宙学：`ΛCDM ⊂ 框架`）**同族**：**解释力 ≠ 判别力**（第 61 轮建立）。
>
> · ⚠️ **与 I-16 同构**：那边是「三层没有一层同时有**位置 ＋ 能量 ＋ 位置是 q-数**」；这边是「**框架自有结构里没有一层提供非交换**」—— **同一个「分层」失败形态**。而 §7.2 的动作（「把事件流状态从经典概率分布**升级**为算子代数」）正是在**分层之上再叠一层假设** ⟹ 与陷阱 23（**公设上移 = 无穷回归**）同族。
>
> · **四类判定**：§7.1「必须非交换化」= **postdiction**（被 1982 年起的 CHSH 实验逼出；Fine 定理使其严格）｜§7.2「非交换 ⇒ CHSH = 2√2」= **失败（零内容）**｜§7.3 量子游走 σ~t vs √t = **一致性构造**｜§7.4 = **自认**｜候选池 3 的 `D = ℏ/(3m)` = **恒等式**。**真预言 0 条、判别性输出 0 条。**
>
> · **候选池 3 结项（I-21）＋ 两条更正 ＋ 两条负面**：**C-22** —— 候选池 3 的全部锚点词（`Nelson` / `随机力学` / `ℏ/(3m)` / `ℏ/(2m)` / `持续长度` / `λ_C` / `p_rev`）**在论文里各 0 处**，其真实出处是第 18/21 轮的备忘录 `配对机制_湮灭等于相邻格点的对换.md`。**C-23** —— 「`(−1)^N_exchange`（交换符号）」**记号歧义**（组态权重 vs 费米子算符），而框架**无 Fock 空间** ⟹ 只能读作前者。**N-31 / N-32** 见清单。
>   ⚠️ **`D = ℏ/(3m)` 是恒等式**：把**牛顿常数 G 缩放 ×0.25 / ×1 / ×4**（`l_P ∝ √G`、`m_P ∝ 1/√G`，而 **`l_P·m_P ≡ ℏ/c` 与 G 无关**）⟹ **D 完全不变**（三次相对差均为 0）⟹ `l_P`、`m_P` 被消掉，`D = ℏ/(3m)` 只是 `λ_C = ℏ/(mc)` 的重述，而 `λ_C` 又是 `p_rev = m/m_P` 的**定义式反解**。
>   且「差 1.5 倍 = 维度因子」**不成立**：框架的 `1/d` 是 d 维各向同性扩散的几何因子，Nelson 的 `ℏ/(2m)` **与维度无关** ⟹ 扫维度只有 **d = 2** 重合（d = 1 / 3 / 4 分别差 2 / 1.5 / 2 倍）⟹ 那是**把 d=3 的『3』与 2m 的『2』摆在一起的数字巧合**，**不构成判别点**。
>
> ⚠️ **五条诚实边界**：① **QM-5 是「解释力」不是「判别力」**；② **QM-6 的「不需要框架元素」是充分性论证**（说明 §7.2 的证明**可以**不用框架完成），**不等于**「框架不能给出别的证明」；③ **QM-7 只验证 Z₂ 弦网**（§5.7 的 B1–B5 用的就是 Z₂）；§5.7 的 **S₃ 非阿贝尔面模型**不在此列 —— 那里的「非交换」是**群乘法的非交换**，且是**另一个模型（3+1D 面模型）**，**不等于**框架衬底的性质；④ C-22 / C-23 是**口径问题**，不是物理错误；⑤ 本轮**不改 §7.1–§7.4 的正文措辞**，只追加本块与 §7.2 的一条判别力标注。
"""
txt = io.open(ZH, encoding="utf-8").read()
i = txt.find(ZH_ANCHOR)
if i < 0:
    print("  [XX] ZH §7.4 锚点未找到")
else:
    # 锚点所在行 = 第 68 轮块的末行；在其**整行之后**插入
    j = txt.find("\n", i)
    txt = txt[:j + 1] + ZH_BLOCK + txt[j + 1:]
    io.open(ZH, "w", encoding="utf-8").write(txt)
    print("  [OK] {:<30} 已插块".format("ZH §7.4 【第 76 轮】块"))

# ── 4. EN §7.4 insert Round-76 block ─────────────────────
EN_ANCHOR = "> ⚠️ **Five honest boundaries**: ① **the strong version rests on the stipulation"
EN_BLOCK = """
---

> **【v2.9 supplement (round 76: audit of §7, foundations of quantum mechanics — non-commutativization is *externally added*, discriminating power = 0)】** This round is an **audit + citation check + numerics** (script `_qm_audit_76.py`, **QM-1 … QM-12, 12 items, 0 failures**). §7 is the **only major chapter never audited**: after removing the already-registered round blocks it has **only 15 non-empty lines of body text** (41 of its 70 lines are the round-57 / round-68 blocks).
>
> · ⭐ **This round's only positive output (§7.1 can be upgraded to a theorem)**: enumerating all 2⁴ = 16 deterministic local strategies gives **max CHSH = 2** (the max over 5000 random convex mixtures is 1.0879), so §7.1's claim can be upgraded from an **assertion** to **a corollary of Fine's theorem (1982)**: *if the observable algebra is commutative (a joint probability distribution exists), then CHSH ≤ 2* ⟹ any theory compatible with CHSH = 2√2 must have a **non-commutative** observable algebra. This is **the only "necessity" argument in the framework backed by a rigorous external theorem**. ⚠️ But what it proves is "**if** commutative **then** impossible" — **not** "the framework's observable algebra is commutative", which is §7.1's **premise** (unproved) and precisely what §7.2 sidesteps by the *act* of "upgrading to an operator algebra".
>
> · **The §7.2 proposition is a conditional proposition (zero content)**: `S = −2.8284 = −2√2` is fully reproduced with **2 qubits**, whose **only inputs are four Pauli matrices and one 2-qubit state** ⟹ the conclusion is the **Tsirelson theorem**, i.e. **the premise already contains the conclusion**; the "numerical verification" claimed in §7.2 verifies a textbook result of standard QM.
>
> · ⭐ **Item-by-item verdict on the 4 "non-commutative elements already in the framework"**: only the **Clifford projections** are genuinely non-commutative (`‖[Π_1,Π_2]‖_max = 0.5`, `‖{Π_1,Π_2}‖_max = 0.7071`, `(Π_μ)² = Π_μ`) — and they are **representation-theoretic notation** (§5.2, internal-space 4 components), not dynamics; `(−1)^N_exchange` is an **Abelian phase** (±1 diagonal weight; **Fock / second quantization / creation operator / annihilation operator / exchange operator / permutation operator each occur 0 times in the whole paper**); "geometric origin of superposition (global equivalence)" is an **equality**; "quantum straight line" is a **channel**.
>   ⭐ Additional (numerical): **the string-net algebra (`A_v` / `B_p`) is fully commutative** — a vertex and a face share **exactly 2 edges** ⟹ two anticommutations ⟹ net commutation; the Pauli symplectic representation and the 256-dimensional full-matrix check agree (`‖AB−BA‖_max = 0`), with **0 non-commuting pairs** on each of **2×2 / 3×3 / 2×4**. ⟹ **None of the 4 items is the string net**, even though the string net is the **only** part of the framework with a rigorous Hamiltonian and numerical verification (§5.7).
>
> · **Discriminating power = 0 (self-declared in §7.4)**: every physical number in the §7 body is `{2√2, ½, −2.8284}`, **all textbook constants**; §7.4 itself states that "once non-commutativized, the framework's quantum part **mathematically coincides** with standard QM" ⟹ same family as **N-29** (cosmology: `ΛCDM ⊂ framework`): **explanatory power ≠ discriminating power** (established in round 61).
>
> · ⚠️ **Isomorphic to I-16**: there it was "no layer has *position + energy + position as a q-number* simultaneously"; here it is "**no layer of the framework's own structure supplies non-commutativity**" — the **same "stratification" failure mode**. And §7.2's act ("upgrading the event-flow state from a classical probability distribution to an operator algebra") is precisely **stacking one more assumption on top of the stratification** ⟹ same family as trap 23 (**postulate escalation = infinite regress**).
>
> · **Four-way verdicts**: §7.1 "must non-commutativize" = **postdiction** (forced by CHSH experiments since 1982; Fine's theorem makes it rigorous) | §7.2 "non-commutative ⇒ CHSH = 2√2" = **failure (zero content)** | §7.3 quantum walk σ~t vs √t = **consistency construction** | §7.4 = **self-declared** | candidate 3's `D = ℏ/(3m)` = **an identity**. **True predictions: 0.**
>
> · **Candidate 3 closed (I-21) + two corrections + two negatives**: **C-22** — all anchor terms of candidate 3 (`Nelson` / `stochastic mechanics` / `ℏ/(3m)` / `ℏ/(2m)` / `persistence length` / `λ_C` / `p_rev`) occur **0 times in the paper**; their real source is the round-18/21 memo `配对机制_湮灭等于相邻格点的对换.md`. **C-23** — the notation "`(−1)^N_exchange` (exchange sign)" is **ambiguous** (configuration weight vs fermionic operator), and since the framework **has no Fock space**, only the former reading is available. See the checklist for **N-31 / N-32**.
>   ⚠️ **`D = ℏ/(3m)` is an identity**: rescaling **Newton's constant G by ×0.25 / ×1 / ×4** (`l_P ∝ √G`, `m_P ∝ 1/√G`, while **`l_P·m_P ≡ ℏ/c` is G-independent**) leaves **D exactly unchanged** (relative difference 0 in all three cases) ⟹ `l_P` and `m_P` cancel, and `D = ℏ/(3m)` merely restates `λ_C = ℏ/(mc)`, itself obtained by inverting the **definitional** `p_rev = m/m_P`.
>   Moreover "a factor 1.5 = a dimensional factor" **does not hold**: the framework's `1/d` is the geometric factor of isotropic diffusion in d dimensions, whereas Nelson's `ℏ/(2m)` is **dimension-independent** ⟹ scanning dimensions, only **d = 2** coincides (d = 1 / 3 / 4 differ by 2 / 1.5 / 2) ⟹ that is a **numerical coincidence of putting d=3's "3" next to 2m's "2"**, and **constitutes no discriminating point**.
>
> ⚠️ **Five honest boundaries**: ① **QM-5 is "explanatory power", not "discriminating power"**; ② **QM-6's "no framework elements needed" is a sufficiency argument** (it shows §7.2's proof **can** be done without the framework), **not** that "the framework cannot give another proof"; ③ **QM-7 verifies only the Z₂ string net** (which is what §5.7's B1–B5 use); §5.7's **S₃ non-Abelian surface model** is not covered — there the "non-commutativity" is that of **group multiplication**, and it is **a different model (3+1D surface model)**, **not** a property of the framework's substrate; ④ C-22 / C-23 are **notation issues**, not physics errors; ⑤ this round **does not alter the wording of §7.1–§7.4**, adding only this block plus one discriminating-power annotation in §7.2.
"""
txt = io.open(EN, encoding="utf-8").read()
i = txt.find(EN_ANCHOR)
if i < 0:
    print("  [XX] EN §7.4 锚点未找到")
else:
    j = txt.find("\n", i)
    txt = txt[:j + 1] + EN_BLOCK + txt[j + 1:]
    io.open(EN, "w", encoding="utf-8").write(txt)
    print("  [OK] {:<30} 已插块".format("EN §7.4 round-76 block"))

# ── 自查 ─────────────────────────────────────────────────
print()
for p, nm in ((ZH, "ZH"), (EN, "EN")):
    L = io.open(p, encoding="utf-8").read().split("\n")
    bad_pipe = sum(1 for s in L if "\\|" in s and not s.lstrip().startswith("|"))
    frag = [i + 1 for i, s in enumerate(L) if s.strip().startswith(("，", ","))]
    print("  {} 行数 {}；非表格反斜杠竖线 {}；残片行 {}".format(nm, len(L), bad_pipe, frag))
print("  ZH 第 76 轮 =", io.open(ZH, encoding="utf-8").read().count("第 76 轮"))
print("  EN Round 76 =", io.open(EN, encoding="utf-8").read().count("Round 76"))
