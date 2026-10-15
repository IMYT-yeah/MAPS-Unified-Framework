# -*- coding: utf-8 -*-
"""第 104 轮（甲-5）补丁 a：论文中英同步。

铁律 74：长行锚点一律用「行首前缀定位 + 动态取整行」，或整行 replace（唯一性先断言）。
"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
OK, BAD = [], []


def sub(path, old, new, tag):
    t = io.open(path, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        BAD.append("{}（命中 {}）".format(tag, n))
        print("  [XX] {:<26} 命中 {} 次 —— 拒绝".format(tag, n)); return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    OK.append(tag); print("  [OK] {:<26}".format(tag))


def repl_line(path, prefix, new, tag, must_contain=None):
    """整行替换：按行首前缀定位（唯一性先断言），保留行尾换行由 join 处理。"""
    t = io.open(path, encoding="utf-8").read()
    L = t.split("\n")
    cand = [i for i, s in enumerate(L) if s.startswith(prefix)]
    if len(cand) != 1:
        BAD.append("{}（行首命中 {}）".format(tag, len(cand)))
        print("  [XX] {:<26} 行首命中 {} 次 —— 拒绝".format(tag, len(cand))); return
    i = cand[0]
    if must_contain and must_contain not in L[i]:
        BAD.append("{}（行内容校验失败）".format(tag))
        print("  [XX] {:<26} 行内容不含校验串".format(tag)); return
    L[i] = new
    io.open(path, "w", encoding="utf-8").write("\n".join(L))
    OK.append(tag); print("  [OK] {:<26}".format(tag))


def insert_after_line(path, prefix, block, tag):
    t = io.open(path, encoding="utf-8").read()
    L = t.split("\n")
    cand = [i for i, s in enumerate(L) if s.startswith(prefix)]
    if len(cand) != 1:
        BAD.append("{}（行首命中 {}）".format(tag, len(cand)))
        print("  [XX] {:<26} 行首命中 {} 次 —— 拒绝".format(tag, len(cand))); return
    i = cand[0]
    L = L[:i + 1] + [""] + block.split("\n") + L[i + 1:]
    io.open(path, "w", encoding="utf-8").write("\n".join(L))
    OK.append(tag); print("  [OK] {:<26}".format(tag))


print("=" * 90)
print("第 104 轮补丁 a（论文中英同步）")
print("=" * 90)

# ---------------- ① 中文稿 §4.9 三行就地更正 ----------------
print("\n[① 中文稿 §4.9]")
repl_line(ZH, "**现在平面选择命题（N1–N4）【v1.3 补充】**",
    "**现在平面选择命题（N1–N4）【v1.3 补充】**：O1 的动力学基础——为何观测者恰好对齐一个时间平面"
    "（⚠️ **第 104 轮**：四项严格性**各不相同**，原用一个【本框架设定】标签覆盖全部 —— "
    "见下方**第 104 轮块**的分级表）：",
    "ZH-N1N4标题", must_contain="O1 的动力学基础")

repl_line(ZH, "- **N1（存在性）**",
    "- **N1（存在性）**：稳态涡需相位累积 4π 整数倍【本框架设定】⟹ 必须锁定旋转轴 ⟹ 至少一个平面"
    "（⚠️ **第 104 轮**：**4π 不是自由参数** —— `R(2π) = −I`、`R(4π) = +I`（`j = 1/2`），"
    "即 **SU(2) 旋量单值性**，由 SU(2) 的**最低非平凡自旋 1/2** 给出；但「4π」的**两种读法未写明**"
    "（绕数取偶数 vs 旋量任意，最小涡荷差 **2 倍**）—— **C-68**）；",
    "ZH-N1")

repl_line(ZH, "- **N2（唯一性）**",
    "- **N2（唯一性）**：0 平面退化（无涡）、2 平面冲突（共享轴拍频）、3 平面各向同性——恰好一个"
    "（⚠️ **第 104 轮升级为定理**：「锁定」$=$「**本征态** ＋ 非零本征值」；设 $[A,B] = iC \\ne 0$，"
    "若 $\\psi$ 同时锁定两平面（$A\\psi = a\\psi$、$B\\psi = b\\psi$，$a,b \\ne 0$），"
    "则 $iC\\psi = [A,B]\\psi = 0 \\Rightarrow C\\psi = 0$，再 $iA\\psi = [B,C]\\psi = -b\\,C\\psi = 0 "
    "\\Rightarrow \\boxed{a = 0}$，**矛盾** ⟹ **双平面锁定在 su(2) 代数下无解**"
    "（$j = 0,\\frac12,\\ldots,5$ 穷举 ＋ 可约表示均验证；这就是「共享轴拍频」的严格形式）。"
    "⚠️ 原注「数值：稳定性 **0.00/1.00/0.30/0.05**」为**启发式**评分（备忘录自承「缺严格动力学证明」），"
    "且产生它的脚本 `_now_numeric.py` **已丢失** ⟹ **不得作为独立证据引用** —— **C-69**）；",
    "ZH-N2")

# ---------------- ② 中文稿 §4.9 第 104 轮块 ----------------
BLOCK_ZH = "\n".join([
    "> **【v2.9 补充（第 104 轮：N2 的 4π 相位锁定相容性方程 —— 从启发式评分到 su(2) 定理）】**"
    "＝第 99 轮四源清点的「甲-5」＝ §10.2#7 的剩余严格化。脚本 `_n2phase_104.py`"
    "（**NP-1 … NP-14，23 项 0 失败**）。",
    "> ① ✅ **相容性方程写出，且它的解是「无解」**：把「涡锁定平面 $i$」形式化为「涡态 $\\psi$ 是 $J_i$ 的"
    "**本征态**且本征值 $\\ne 0$」。设 $[A,B] = iC \\ne 0$，若 $\\psi$ 同时锁定两平面，则 "
    "① $iC\\psi = [A,B]\\psi = 0 \\Rightarrow C\\psi = 0$；② $iA\\psi = [B,C]\\psi = -b\\,C\\psi = 0 "
    "\\Rightarrow \\boxed{a = 0}$，与 $a \\ne 0$ **矛盾** ⟹ **双平面锁定不可能**。",
    "> ② ✅ **数值穷举**：$j = 0,\\frac12,1,\\frac32,2,\\frac52,3,4,5$（9 个不可约表示）**全部无解**"
    "（$j = 0$ 有共同本征态但本征值全为 0 ⟹ 无涡）；**可约表示** $0 \\oplus \\frac12 \\oplus 1 \\oplus \\frac32$"
    "（10 维）同样 **0 个** ⟹ **结论不依赖不可约性**。",
    "> ③ ✅ **反面检验**：**单**平面锁定**存在**（每个 $j \\ge 1/2$ 有 $2j + 1 - [j \\in \\mathbb{Z}]$ 个"
    "非零 $J_z$ 本征态）⟹ 四档判定落地：**0 平面与 3 平面退化**（无旋转荷）、**1 平面存在**、"
    "**2 平面不可能**。",
    "> ④ ⭐ **「4π」不是自由参数**：`R(2π) = −I`、`R(4π) = +I`（$j = 1/2$）⟹ 「4π 整数倍」"
    "＝ **SU(2) 旋量单值性**，而 SU(2) 的**最低非平凡自旋 = 1/2** ⟹ 表示论必然。"
    "**相容性方程的框架特有输入 0 个、自由参数 0 个**（甲-5 判据满足）。",
    "> ⑤ ⚠️ **判据必须是「本征态」，不是「期望值非零」**：$H = \\omega_1 J_1 + \\omega_2 J_2$ 的本征态给出 "
    "$\\langle J_1 \\rangle = 0.447214$、$\\langle J_2 \\rangle = 0.894427$ —— **两个都非零**，"
    "但它对 $J_1$、$J_2$ **都不是**本征态（残差 $0.632$ / $0.316$）⟹ 用「期望值」会**误判双平面可行**；"
    "「拍频」的严格含义 ＝ **两个不对易的相位不能同时有确定值**。",
    "> ⑥ ⚠️ **三处更正**：**C-68** ——「4π」有两种都自洽的读法（A：$\\varphi$ 单值 ⟹ 绕数取**偶数**、"
    "最小涡荷 2；B：序参量为旋量 ⟹ 绕数任意、最小涡荷 1），**论文未写明是哪一种**，下游引用「最小涡荷」"
    "会有 **2 倍**歧义；**C-69** —— 上方 N2 行原注的那组「稳定性 0.00/1.00/0.30/0.05」"
    "（a）产生它的脚本 `_now_numeric.py` **已丢失**、（b）备忘录**自承**其为**启发式**"
    "（数值定性、缺严格动力学证明），论文未带此限定；**C-70** —— 英文稿**同一处两个口径**（§1 写"
    "【Derivation】、§4.9 写【Framework assumption】），已同步修正。",
    "> ⑦ ⚠️ **诚实边界**：「锁定 ＝ 本征态」是**约定**（依据 N1 的相位条件，而 N1 标【本框架设定】）；"
    "本轮严格化的是**上界**（**不可能 2 个**），**「至少一个」仍用 N1 的原文主张**；"
    "**N4 的初始微扰来源仍未推导**；本轮**不声称**复现那组启发式数值（脚本已丢失，无法复现）。"
    "详见《甲5结项_N2的4π相位锁定相容性方程》。",
])
insert_after_line(ZH, "- **N4（动力学机制）**", BLOCK_ZH, "ZH-第104轮块")

# ---------------- ③ 英文稿 §4.9 三行同步 ----------------
print("\n[② 英文稿 §4.9]")
repl_line(EN, "**Present-plane selection propositions (N1–N4)**",
    "**Present-plane selection propositions (N1–N4)**: dynamical basis of O1 — why the observer aligns "
    "with exactly one temporal plane (⚠️ **round 104**: the four items have **different** levels of rigor; "
    "the single【Framework assumption】label previously covered all of them — see the **round-104 block** below):",
    "EN-N1N4标题", must_contain="dynamical basis of O1")

repl_line(EN, "- **N1 (existence)**",
    "- **N1 (existence)**: a steady vortex requires phase accumulation of integer multiples of 4π"
    "【Framework assumption】⟹ must lock a rotation axis ⟹ at least one plane"
    " (⚠️ **round 104**: **4π is not a free parameter** — `R(2π) = −I` and `R(4π) = +I` at $j = 1/2$, "
    "i.e. **SU(2) spinor single-valuedness**, fixed by SU(2)'s **lowest non-trivial spin 1/2**; "
    "but the **two readings of \"4π\" are not specified** (even winding vs. arbitrary spinor winding — "
    "the minimal vortex charge differs by a **factor of 2**) — **C-68**);",
    "EN-N1")

repl_line(EN, "- **N2 (uniqueness)**",
    "- **N2 (uniqueness)**: 0 planes degenerate (no vortex), 2 planes conflict (shared-axis beating), "
    "3 planes isotropic — exactly one (⚠️ **upgraded to a theorem in round 104**: \"locking\" $=$ "
    "\"**eigenstate** with non-zero eigenvalue\"; with $[A,B] = iC \\ne 0$, if $\\psi$ locks two planes "
    "($A\\psi = a\\psi$, $B\\psi = b\\psi$, $a,b \\ne 0$) then $iC\\psi = [A,B]\\psi = 0 \\Rightarrow C\\psi = 0$, "
    "and $iA\\psi = [B,C]\\psi = -b\\,C\\psi = 0 \\Rightarrow \\boxed{a = 0}$, **a contradiction** ⟹ "
    "**two-plane locking is impossible in su(2)** (verified by exhaustive $j = 0,\\frac12,\\ldots,5$ plus "
    "reducible representations; this is the rigorous form of \"shared-axis beating\"). "
    "⚠️ The old note \"numerically: stabilities **0.00/1.00/0.30/0.05**\" was a **heuristic** score "
    "(the memo itself says \"lacking a rigorous dynamical proof\") **and the script that produced it "
    "(`_now_numeric.py`) is lost** ⟹ **must not be cited as independent evidence** — **C-69**);",
    "EN-N2")

BLOCK_EN = "\n".join([
    "> **【v2.9 supplement (round 104: N2's 4π phase-locking compatibility equation — from a heuristic score "
    "to an su(2) theorem)】** = item 甲-5 of the round-99 four-source inventory = the remaining rigorization "
    "of §10.2#7. Script `_n2phase_104.py` (**NP-1 … NP-14, 23 items 0 failures**).",
    "> ① ✅ **The compatibility equation is written, and its solution is \"no solution\"**: formalize "
    "\"the vortex locks plane $i$\" as \"the vortex state $\\psi$ is an **eigenstate** of $J_i$ with "
    "non-zero eigenvalue\". With $[A,B] = iC \\ne 0$, if $\\psi$ locks two planes then "
    "① $iC\\psi = [A,B]\\psi = 0 \\Rightarrow C\\psi = 0$; ② $iA\\psi = [B,C]\\psi = -b\\,C\\psi = 0 "
    "\\Rightarrow \\boxed{a = 0}$, contradicting $a \\ne 0$ ⟹ **two-plane locking is impossible**.",
    "> ② ✅ **Numerical exhaustion**: $j = 0,\\frac12,1,\\frac32,2,\\frac52,3,4,5$ (9 irreducible "
    "representations) **all have no solution** ($j = 0$ has a joint eigenstate but with all eigenvalues "
    "zero ⟹ no vortex); the **reducible** representation $0 \\oplus \\frac12 \\oplus 1 \\oplus \\frac32$ "
    "(dim 10) likewise gives **0** ⟹ the conclusion **does not rely on irreducibility**.",
    "> ③ ✅ **Counter-check**: **single**-plane locking **does exist** (each $j \\ge 1/2$ has "
    "$2j + 1 - [j \\in \\mathbb{Z}]$ non-zero $J_z$ eigenstates) ⟹ all four cases land: "
    "**0 and 3 planes degenerate** (no rotational charge), **1 plane exists**, **2 planes impossible**.",
    "> ④ ⭐ **\"4π\" is not a free parameter**: `R(2π) = −I` and `R(4π) = +I` at $j = 1/2$ ⟹ "
    "\"integer multiples of 4π\" $=$ **SU(2) spinor single-valuedness**, and SU(2)'s **lowest non-trivial "
    "spin is 1/2** ⟹ a representation-theoretic necessity. The compatibility equation has "
    "**0 framework-specific inputs and 0 free parameters** (item 甲-5's criterion is met).",
    "> ⑤ ⚠️ **The criterion must be \"eigenstate\", not \"non-zero expectation value\"**: the eigenstate of "
    "$H = \\omega_1 J_1 + \\omega_2 J_2$ gives $\\langle J_1 \\rangle = 0.447214$ and "
    "$\\langle J_2 \\rangle = 0.894427$ — **both non-zero** — yet it is an eigenstate of **neither** "
    "$J_1$ nor $J_2$ (residuals $0.632$ / $0.316$) ⟹ using \"expectation values\" would **falsely admit** "
    "two-plane locking; \"beating\" rigorously means **two non-commuting phases cannot both be definite**.",
    "> ⑥ ⚠️ **Three corrections**: **C-68** — \"4π\" has two self-consistent readings (A: $\\varphi$ "
    "single-valued ⟹ **even** winding, minimal vortex charge 2; B: spinor order parameter ⟹ arbitrary "
    "winding, minimal charge 1) and the paper **does not say which** ⟹ any downstream citation of the "
    "\"minimal vortex charge\" is ambiguous by a **factor of 2**; **C-69** — the group of numbers "
    "\"stabilities 0.00/1.00/0.30/0.05\" in the N2 line above (a) was produced by `_now_numeric.py`, "
    "**which is lost**, and (b) was **self-declared heuristic** (the memo: \"lacking a rigorous dynamical "
    "proof\") without that qualifier being carried into the paper; **C-70** — the English draft carried "
    "**two different labels for the same place** (§1:【Derivation】, §4.9:【Framework assumption】), "
    "now synchronized.",
    "> ⑦ ⚠️ **Honest boundaries**: \"locking = eigenstate\" is a **convention** (based on N1's phase "
    "condition, and N1 is labelled【Framework assumption】); what is rigorized here is the **upper bound** "
    "(**two planes impossible**) while **\"at least one\" still rests on N1's original claim**; "
    "**N4's perturbation origin remains underived**; and this round **does not claim** to reproduce the "
    "heuristic score (its script is lost). See 《甲5结项_N2的4π相位锁定相容性方程》.",
])
insert_after_line(EN, "- **N4 (dynamical mechanism)**", BLOCK_EN, "EN-第104轮块")

# ---------------- ④ 英文稿 §1 口径修正（C-70） ----------------
print("\n[③ 英文稿 §1 口径修正]")
sub(EN,
    '**Why the "present plane" is selected**【Derivation, proposition chain in §4.9】:',
    '**Why the "present plane" is selected**【Framework assumption + proposition chain in §4.9; '
    '⚠️ **round 104**: N2 is upgraded to a theorem while N1/N4 remain assumptions — see the round-104 block】:',
    "EN-§1口径")

# ---------------- ⑤ §10.2#7 收口 ----------------
print("\n[④ §10.2#7 收口]")
sub(ZH,
    "剩余严格化：N2 的 4π 相位锁定相容性方程（深度开放）；",
    "剩余严格化：**~~N2 的 4π 相位锁定相容性方程~~ ✅ 第 104 轮结项**"
    "（方程可写、**自由参数 0 个**、结论 ＝ **双平面锁定在 su(2) 代数下无解**"
    "（三行代数 ＋ $j \\le 5$ 穷举 ＋ 可约表示）；⚠️ 同时登记 **C-68**（「4π」两种读法未写明）／"
    "**C-69**（原启发式评分脚本已丢失）／**C-70**（英文稿【Derivation】 vs 【Framework assumption】冲突）；"
    "N4 的微扰来源仍未推导）；",
    "ZH-§10.2#7")

sub(EN,
    "remaining rigorization: N2's 4π phase-locking compatibility equation (deeply open);",
    "remaining rigorization: **~~N2's 4π phase-locking compatibility equation~~ ✅ closed in round 104** "
    "(the equation can be written, has **zero free parameters**, and its solution is that **two-plane "
    "locking is impossible in su(2)** (three-line algebra + exhaustive $j \\le 5$ + reducible "
    "representations); ⚠️ with **C-68** (the two readings of \"4π\" are unspecified) / **C-69** "
    "(the heuristic-score script is lost) / **C-70** (EN【Derivation】vs【Framework assumption】conflict); "
    "N4's perturbation origin remains underived);",
    "EN-§10.2#7")

print("\n" + "=" * 90)
print("OK {} 项，BAD {} 项".format(len(OK), len(BAD)))
if BAD:
    print("失败：" + " ｜ ".join(BAD))
print("=" * 90)
