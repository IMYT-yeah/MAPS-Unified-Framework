# -*- coding: utf-8 -*-
"""
第 0 批（0.3 + 0.4）补丁：

0.3  ε 的能标标注规范
   ① §8.1 加「符号约定（重要）」—— 区分**泄漏概率** vs **Levi-Civita 张量**，
      并规定「凡引用泄漏 ε 的数值必须写明能标」
   ② 第 201 行的 `ε~10⁻⁵⁰` 加**待核实**标注（按 §8.1 公式在 LHC 能标应为 1.47×10⁻¹⁰，差 40 个数量级）
0.4  「轨道等权」残留对账 —— 给两处脚本加**口径注释**（不改数值）
   ① `_fix_run_48.py` 的 `h_over_n`：**确认是错误口径**（全层枚举 + 轨道等权，第 50 轮已查明）
   ② `_gap_orbit_48.py` 的两处：**实际正确**（GAP 随机构型采样天然构型等权），须标注以防未来被误"修"
"""
import io, os

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
        print("  [XX] {:<34} 命中 {} 次 —— 拒绝".format(tag, n))
        BAD += 1
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<34} 已改".format(tag))
    OK += 1

print("第 0 批补丁（0.3 ε 的 @E 规范 ＋ 0.4 脚本口径注释）")

# ================================================================
# 0.3① ZH §8.1 加符号约定
OLD = "### 8.1 泄漏机制的能标依赖（ε_A）"
NEW = """### 8.1 泄漏机制的能标依赖（ε_A）

> **符号约定（重要）**：本文的 `ε` 有**两个互不相干的含义**，必须区分 ——
> ① **泄漏概率** `ε(E)`（本章 §8.1 / §8.2，**能标依赖**，定义式 `ε(E) = ε₀(M_Pl/E)^β`）：
>    本节及 §8.2 里的 `ε`、`ε₀`、`ε_A`、`ε_B`、`ε_topo`、`ε_eff` **均属此义**；
> ② **Levi-Civita 全反对称张量** `ε_ijk` / `ε^ij`（§5.2 的表示论记号，**与能标无关**）。
> ⟹ **凡引用 ① 的数值，必须同时写明能标**（如 `ε(1 TeV) = 6.0×10⁻¹⁰`）；
>    **跨能标引用 = 无意义** —— 这正是第 53 轮判 S-E5 失败的原因（**N-14**：把
>    `ε₀ = ε(M_Pl) = 7.7×10⁻²⁰` 搬到 FQH 能标（0.1–15 meV）用，而那里应为 `O(1)`，
>    差 **18–21 个数量级**）。
> ⟹ 本条为**第 0 批（2026-09-28）**登记的**口径卫生规范**：此后凡出现能标依赖量
>    （`ε`、`α`、`λ_c`…），一律紧跟 `(@E)` 标注。
> （同类撞车已在 §8.6 对 `λ` 声明过，见该节「符号约定（重要）」。）"""
sub_once(ZH, OLD, NEW, "0.3① ZH §8.1 符号约定")

OLDE = "### 8.1 Energy-scale dependence of the leakage mechanism (ε_A)"
NEWE = """### 8.1 Energy-scale dependence of the leakage mechanism (ε_A)

> **Notation convention (important)**: the symbol `ε` carries **two unrelated meanings** in this paper, and they must be distinguished —
> ① **leakage probability** `ε(E)` (this chapter, §8.1 / §8.2, **energy-scale dependent**, defined by `ε(E) = ε₀(M_Pl/E)^β`):
>    `ε`, `ε₀`, `ε_A`, `ε_B`, `ε_topo`, `ε_eff` in this section and §8.2 **all carry this meaning**;
> ② **Levi-Civita totally antisymmetric tensor** `ε_ijk` / `ε^ij` (the representation-theoretic notation of §5.2, **energy-scale independent**).
> ⟹ **Whenever a value of ① is quoted, the energy scale must be stated** (e.g. `ε(1 TeV) = 6.0×10⁻¹⁰`);
>    **cross-scale quotation is meaningless** — this is precisely why round 53 failed S-E5 (**N-14**: `ε₀ = ε(M_Pl) = 7.7×10⁻²⁰`
>    was carried over to the FQH scale (0.1–15 meV), where it should be `O(1)` — a gap of **18–21 orders of magnitude**).
> ⟹ This is the **notation-hygiene rule registered in batch 0 (2026-09-28)**: from now on, every energy-scale-dependent quantity
>    (`ε`, `α`, `λ_c`, …) must be followed by an `(@E)` annotation.
> (A parallel collision was already declared for `λ` in §8.6; see "Notation convention (important)" there.)"""
sub_once(EN, OLDE, NEWE, "0.3① EN §8.1 notation convention")

# ================================================================
# 0.3② 第 201 行的 ε~10⁻⁵⁰ 加待核实标注
OLD2 = "泄漏 ε~10⁻⁵⁰ 不产生 LHC 信号"
NEW2 = ("泄漏 ε~10⁻⁵⁰（⚠️ **待核实**〔第 0 批，2026-09-28〕：按 §8.1 的 `ε(E) = ε₀(M_Pl/E)^β`，"
        "LHC 能标（10⁴ GeV）下应为 **1.47×10⁻¹⁰**，与本处 **差 40 个数量级**；"
        "10⁻⁵⁰ 的来源尚未查明，**暂不改数值**）不产生 LHC 信号")
sub_once(ZH, OLD2, NEW2, "0.3② ZH LHC 处加待核实")

OLDE2 = "leakage ε~10⁻⁵⁰ produces no LHC signal"
NEWE2 = ("leakage ε~10⁻⁵⁰ (⚠️ **to be verified** [batch 0, 2026-09-28]: per §8.1's `ε(E) = ε₀(M_Pl/E)^β`, "
         "at the LHC scale (10⁴ GeV) it should be **1.47×10⁻¹⁰** — a **40 order-of-magnitude** discrepancy; "
         "the origin of 10⁻⁵⁰ is not yet identified, and the value is **not changed for now**) produces no LHC signal")
sub_once(EN, OLDE2, NEWE2, "0.3② EN LHC 处加待核实")

# ================================================================
# 0.4① _fix_run_48.py：确认错误口径，加警告注释
P48 = os.path.join(BASE, "_fix_run_48.py")
OLD3 = """def h_over_n(sizes, N):
    avg = sum(math.log(s) for s in sizes) / len(sizes)
    return LN2 - avg / N, avg"""
NEW3 = """def h_over_n(sizes, N):
    # ⚠️⚠️ 口径警告（第 50 轮 R-2 / C-2 查明，第 0 批 2026-09-28 加注）：
    #   本函数用「**轨道等权**」：avg = Σ ln|O| / #轨道；
    #   而第 40 轮的**权威定义**是「**构型等权**」：avg = Σ |O|·ln|O| / Σ |O|（|O| 越大权重越大）。
    #   两者在 N = 8 / 16 / 24 上差 0.0520 / 0.0318 / 0.0176。
    #   ⟹ 本脚本产出的 H/N **不可直接引用**；正确值见第 50 轮更正（(2,2,6) 的 0.4334，原报 0.4510）。
    #   ⟹ 本函数只适用于「**全层枚举**」场景；GAP 的**随机构型采样**天然是构型等权，不受此限。
    avg = sum(math.log(s) for s in sizes) / len(sizes)
    return LN2 - avg / N, avg"""
sub_once(P48, OLD3, NEW3, "0.4① _fix_run_48 口径警告")

# 0.4② _gap_orbit_48.py：两处「看似等权、实为构型等权」，加保护性注释
P48B = os.path.join(BASE, "_gap_orbit_48.py")
OLD4 = "avg44 = sum(math.log(s) for s in sizes44) / len(sizes44)"
NEW4 = ("# ✅ 口径说明（第 0 批 2026-09-28 加注）：sizes44 来自**随机采样的 S 个构型**（每构型一个轨道大小），\n"
        "#    故 Σ ln|O(c)| / S **就是构型等权**（第 50 轮确认：GAP 采样天然正确）。\n"
        "#    ⚠️ 它**看上去**像「轨道等权」，但采样使每个构型等权 ⟹ **不是**错误口径，**请勿「修正」**。\n"
        "avg44 = sum(math.log(s) for s in sizes44) / len(sizes44)")
sub_once(P48B, OLD4, NEW4, "0.4② gap_orbit_48 (4,4) 加保护注释")

OLD5 = "avg444 = sum(math.log(s) for s in sizes444) / len(sizes444)"
NEW5 = ("# ✅ 口径说明（同 0.4②）：随机采样 ⟹ 构型等权，**不是**错误口径，请勿「修正」。\n"
        "    avg444 = sum(math.log(s) for s in sizes444) / len(sizes444)")
sub_once(P48B, OLD5, NEW5, "0.4② gap_orbit_48 (4,4,4) 加保护注释")

print("\n通过 {} 项，失败 {} 项".format(OK, BAD))
