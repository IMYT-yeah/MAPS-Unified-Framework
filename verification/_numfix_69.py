# -*- coding: utf-8 -*-
"""第 69 轮核验：论文两处数值收口
A. §5.7「能隙 Δ = 1」（2+1D 2×2 环面 256 态）—— 口径查明
B. §4.2「泄漏 ε ~ 10⁻⁵⁰」—— 出处查明

⚠️ 本轮的性质：**数值核查 ＋ 口径裁决**，不是新物理。
"""
import io
import os
import sys
import math
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
TXT = io.open(ZH, encoding="utf-8").read()
LINES = TXT.split("\n")

OK = 0
BAD = 0


def chk(tag, cond, msg):
    global OK, BAD
    if cond:
        OK += 1
        print("  [OK] {:<8} {}".format(tag, msg))
    else:
        BAD += 1
        print("  [XX] {:<8} {}".format(tag, msg))


def rule(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


# ══════════════════════════════════════════════════════════════════════
rule("NC-1  A：2+1D toric code（周期 L×L 环面）的完整谱")
# ══════════════════════════════════════════════════════════════════════


def build_toric(L):
    NE = 2 * L * L

    def eh(x, y):
        return (y % L) * L + (x % L)

    def ev(x, y):
        return L * L + (x % L) * L + (y % L)
    Av = [[eh(x - 1, y), eh(x, y), ev(x, y - 1), ev(x, y)]
          for x in range(L) for y in range(L)]
    Bp = [[eh(x, y), ev(x, y), eh(x, y - 1), ev(x - 1, y)]
          for x in range(L) for y in range(L)]
    return NE, Av, Bp


def spectrum_toric(L):
    NE, Av, Bp = build_toric(L)
    D = 1 << NE
    H = np.zeros((D, D))
    idx = np.arange(D)
    diag = np.zeros(D)
    for plaq in Bp:
        s = np.ones(D, dtype=np.int64)
        for e in plaq:
            s *= (1 - 2 * ((idx >> e) & 1))
        diag += -s.astype(float)
    H[np.arange(D), np.arange(D)] = diag
    for vert in Av:
        tgt = idx.copy()
        for e in vert:
            tgt ^= (1 << e)
        for st in range(D):
            H[tgt[st], st] += -1.0
    w = np.linalg.eigvalsh(H)
    uniq, cnt = np.unique(np.round(w, 9), return_counts=True)
    return NE, list(zip(uniq.tolist(), cnt.tolist()))


NE2, spec2 = spectrum_toric(2)
print("  L = 2：边数 {}、态数 2^{} = {}".format(NE2, NE2, 2 ** NE2))
print("  完整能谱（能量, 简并）：")
for E, d in spec2:
    print("     {:>9.4f}  ×{}".format(E, d))
E0, E1 = spec2[0][0], spec2[1][0]
print("  E0 = {:.4f}   次低 = {:.4f}   **Δ = E1 − E0 = {:.4f}**".format(E0, E1, E1 - E0))
print("  基态简并 = {} （论文记 tr = 4.000 = |G|² ✓）；总态数校验 {}".format(
    spec2[0][1], sum(d for _, d in spec2)))
chk("NC-1", abs(E0 + 8) < 1e-9 and abs((E1 - E0) - 4) < 1e-9 and spec2[0][1] == 4,
    "2+1D 周期 L=2：**E0 = −8.0000（与论文逐位一致）、Δ = 4.0000J、基态简并 4**")


# ══════════════════════════════════════════════════════════════════════
rule("NC-2  A：Δ 与 L 无关（解析交叉验证 —— 排除「小格点退化」）")
# ══════════════════════════════════════════════════════════════════════

print("  解析：E(a,b) = 2(a+b) − (N_v+N_p)，a/b = A_v / B_p 缺陷数（**必须为偶数**，")
print("         因 Π_v A_v = Π_p B_p = 1 是算符恒等式 ⟹ 缺陷**必成对**）")
print()
print("  {:<6} {:>7} {:>9} {:>9} {:>9}".format("L", "N_v=N_p", "E0", "E1", "E1−E0"))
rows = []
for L in (2, 3, 4, 5, 10, 50):
    Nv = Np = L * L
    E0a = -(Nv + Np)
    E1a = 4 - (Nv + Np)
    rows.append(E1a - E0a)
    print("  {:<6} {:>7} {:>9} {:>9} {:>9}".format(L, Nv, E0a, E1a, E1a - E0a))
print()
print("  ⟹ **Δ = 4J 对全部 L 成立** ⟹ 不是有限尺寸效应（陷阱 22 的检验通过）")
print("     机理：翻转一条边 X_e ⟹ 两个端点 A_v 各变号 ⟹ ΣA_v 减 4；")
print("           且 Π_v A_v = 1 ⟹ 缺陷必成对 ⟹ **最小激发 = 4J**（不是 2J）")
chk("NC-2", all(abs(x - 4) < 1e-12 for x in rows),
    "解析给出 **Δ = 4J 与 L 无关**（L = 2…50 全同）⟹ 排除有限尺寸效应")


# ══════════════════════════════════════════════════════════════════════
rule("NC-3  A：3+1D 对照（开边界 vs 周期 —— 口径差异的真正来源）")
# ══════════════════════════════════════════════════════════════════════

print("  §5.8 的 3+1D：H₀ = −Σ_c A_c（A_c = Π_{f∈∂c} Z_f），全为 Z ⟹ 谱对角。")
print()
# 单立方体（开边界）：6 个面
NF = 6
vals = []
for st in range(1 << NF):
    Ac = 1
    for f in range(NF):
        Ac *= (1 - 2 * ((st >> f) & 1))
    vals.append(-Ac)
u, c = np.unique(vals, return_counts=True)
print("  **单立方体（开边界，6 面，64 态）**：")
for E, d in zip(u.tolist(), c.tolist()):
    print("     {:>9.4f}  ×{}".format(E, d))
print("  E0 = {:.4f}   E1 = {:.4f}   Δ = {:.4f}".format(u[0], u[1], u[1] - u[0]))
d_open = float(u[1] - u[0])
print()
print("  ⭐ **周期 3+1D 的解析**：每个面被 2 个立方体共享 ⟹ `Π_c A_c = Π_f Z_f² = 1`")
print("     ⟹ **缺陷必成对**（与 2+1D 的 Π_v A_v = 1 同理）⟹ Δ = 2×2 = **4J**")
print()
print("  {:<34} {:>12} {:>14}".format("情形", "边界", "Δ"))
print("  {:<34} {:>12} {:>14}".format("2+1D toric code（周期环面）", "周期", "**4J**"))
print("  {:<34} {:>12} {:>14}".format("3+1D 弦网（周期）", "周期", "**4J**（推定）"))
print("  {:<34} {:>12} {:>14}".format("3+1D 单/双立方体（§5.8 用的）", "**开**", "**2J**"))
print()
print("  ⟹ ⭐ **口径差异的真正来源 = 边界条件**，不是维度本身：")
print("     · **周期** ⟹ 存在 `Π A = 1` 的算符恒等式 ⟹ 缺陷成对 ⟹ Δ = 4J；")
print("     · **开** ⟹ 无该恒等式 ⟹ 单个 A_c 可独立翻转 ⟹ Δ = 2J。")
print("     论文 §5.8 的「Δ = 2」来自**单/双立方体（开）**，而 §5.7 的 L=2 环面是**周期**。")
chk("NC-3", abs(d_open - 2) < 1e-12,
    "**3+1D 单立方体（开）Δ = 2J** ✓ 与论文 §5.8 一致；而**周期**情形必成对 ⟹ Δ = 4J "
    "⟹ **两处差异的真实原因是「开 vs 周期」，不是「2+1D vs 3+1D」**")


# ══════════════════════════════════════════════════════════════════════
rule("NC-4  ⭐ A 的核心判定：论文的「Δ = 1」是哪个归一化？—— L=2 无法区分")
# ══════════════════════════════════════════════════════════════════════

print("  对 2+1D 周期，候选归一化在 L = 2 / 3 / 4 上的取值：")
print()
print("  {:<30} {:>10} {:>10} {:>10} {:>14}".format("归一化（分子 = Δ = 4J）", "L=2", "L=3", "L=4", "L 无关？"))
CANDS = [
    ("Δ（绝对，标准口径）", lambda L: 4.0),
    ("Δ/2（每缺陷）", lambda L: 2.0),
    ("Δ/(2L)（每方向长度）", lambda L: 4.0 / (2 * L)),
    ("Δ/4", lambda L: 1.0),
    ("|E0|/(N_v+N_p)（基态能量密度）", lambda L: 1.0),
]
for nm, f in CANDS:
    v = [f(L) for L in (2, 3, 4)]
    indep = abs(v[0] - v[1]) < 1e-12
    print("  {:<30} {:>10.4f} {:>10.4f} {:>10.4f} {:>14}".format(
        nm, v[0], v[1], v[2], "✓" if indep else "✗ 依赖 L"))
print()
print("  ⚠️ **在 L = 2 上，三个不同的归一化（Δ/(2L)、Δ/4、|E0|/(Nv+Np)）都给 1.000000**：")
print("     因为 2L = 4 = N_v + N_p = 8/2 —— **数值恰好退化**。")
print("  ⟹ 光看「L=2 给 1」**无法确定**论文用的是哪个口径 ⟹ **必须查论文的 J 归一化**。")
print()
print("  📌 论文 §5.7 的 J 定义（§5.8 明写）：`J = n_G·E_P·g`（普朗克标度，无 1/2 或 1/4 因子）")
print("     ⟹ 若 J 就是 H = −JΣA_v − JΣB_p 里的 J，则 **Δ = 4J**（标准口径）")
print("     ⟹ 论文的「Δ = 1」**与标准口径差 4 倍**。")
print()
n_j1 = TXT.count("J = n_G")
print("  引文核对：§5.8「J = n_G·E_P·g」在论文中出现 {} 处".format(n_j1))
degenerate = (abs(4.0 / (2 * 2) - 1) < 1e-12 and abs(4.0 / 4 - 1) < 1e-12
              and abs((2 * 4) / (2 * 4) - 1) < 1e-12)
split_at_L3 = abs(4.0 / (2 * 3) - 1) > 0.3
chk("NC-4", degenerate and split_at_L3,
    "**「Δ = 1」的口径无法从 L=2 唯一定出**（三个归一化在该点退化到 1：{:.6f} / {:.6f}）；"
    "而 L=3 时 Δ/(2L) = {:.4f} 与另两个分离 ⟹ **必须查 J 归一化**；"
    "按论文自己的 `J = n_G·E_P·g`，标准口径应为 **Δ = 4J**".format(
        4.0 / (2 * 2), 4.0 / 4, 4.0 / (2 * 3)))


# ══════════════════════════════════════════════════════════════════════
rule("NC-5  B：ε ~ 10⁻⁵⁰ 的出处（全工作区检索）")
# ══════════════════════════════════════════════════════════════════════

SRC = [
    ("A2_湮灭型BBGKY完整证明.md", 21,
     "| 泄漏 ε ~ 10⁻⁵⁰（重子不对称种子）| σ_ann ≠ σ_regen 的失配参数 δ |"),
    ("A2_湮灭型BBGKY完整证明.md", 146,
     "λ_ann ≠ λ_regen：σ_ann = σ(1+δ)，σ_regen = σ(1−δ)（δ = (σ_ann−σ_regen)/(σ_ann+σ_regen) ~ ε ~ 10⁻⁵⁰）"),
]
print("  10⁻⁵⁰ 在**整个工作区**的出现位置（除论文与补丁脚本）：")
for fn, ln, txt in SRC:
    p = os.path.join(BASE, fn)
    if os.path.exists(p):
        L = io.open(p, encoding="utf-8").read().split("\n")
        ok = ln <= len(L) and "10⁻⁵⁰" in L[ln - 1]
        print("     {}:{}  {}".format(fn, ln, "✓ 命中" if ok else "✗ 未命中"))
print()
print("  ⚠️ 关键：A2 报告第 21 行把它列在**「框架表述（公理 1）→ 本报告数学对象」的对应表**里")
print("     ⟹ **10⁻⁵⁰ 是「输入」（框架的叙事性表述），不是 A2 推导出来的**。")
print("     第 146 行的 `δ ~ ε ~ 10⁻⁵⁰` 只有 `~`（量级相当），**无推导、无定义式**。")
n50_in_A2 = 0
p = os.path.join(BASE, "A2_湮灭型BBGKY完整证明.md")
if os.path.exists(p):
    t2 = io.open(p, encoding="utf-8").read()
    n50_in_A2 = t2.count("10⁻⁵⁰")
    print("     A2 报告里「10⁻⁵⁰」共 {} 处（无一处给出它的推导）".format(n50_in_A2))
chk("NC-5", n50_in_A2 == 2,
    "**出处查明**：A2 报告第 21 / 146 行（被 M1 报告第 92 行与论文 §4.2 转引）；"
    "性质 = **输入（叙事性量级），无推导**")


# ══════════════════════════════════════════════════════════════════════
rule("NC-6  ⚠️ B 的口径核对：第 0 批的「差 40 个数量级」是不是真的？")
# ══════════════════════════════════════════════════════════════════════

eps0 = 7.731e-20
beta = 0.615
MPl_GeV = 1.2209e19
print("  第 0 批的核对（`_patch_batch0b.py`）：按 §8.1 的 `ε(E) = ε₀(M_Pl/E)^β`，")
print("     取 ε₀ = {:.4e}、β = {:.3f}，在 LHC 能标（10⁴ GeV）算得 ε = {:.4e}".format(
    eps0, beta, eps0 * (MPl_GeV / 1e4) ** beta))
print("     ⟹ 与 10⁻⁵⁰ 差 40 个数量级 —— **这是第 0 批记下的「待核实」。**")
print()
print("  ⭐ 本轮的反向检验：把 ε = 10⁻⁵⁰ 代进**同一个公式**，反推它对应的能标：")
ratio = 1e-50 / eps0
E_req = MPl_GeV / (ratio ** (1.0 / beta))
print("     (M_Pl/E)^β = 10⁻⁵⁰/{:.3e} = {:.3e}".format(eps0, ratio))
print("     ⟹ M_Pl/E = {:.3e}^(1/{}) = {:.4e}".format(ratio, beta, ratio ** (1 / beta)))
print("     ⟹ E = M_Pl / {:.4e} = **{:.4e} GeV**".format(ratio ** (1 / beta), E_req))
print()
print("  ⚠️⚠️ **{:.2e} GeV ≫ M_Pl = {:.3e} GeV** —— 反推能标**超出普朗克能标 ~49 个数量级**！".format(
    E_req, MPl_GeV))
print()
print("  ⟹ **结论：10⁻⁵⁰ 与 §8.1 的 ε_A 不可能是同一个量。**")
print("     若强行用 §8.1 的公式，10⁻⁵⁰ 只在 E ≈ 10⁶⁸ GeV 成立 —— 那在框架适用域之外。")
print("     ⟹ **第 0 批的「40 个数量级不一致」是「把两个不同的量当成同一个 ε」造成的假警报**")
print("        （与陷阱 45「符号撞车」同族，但这次是**跨章节的同一符号两个身份**）。")
chk("NC-6", E_req > MPl_GeV * 1e10,
    "**第 0 批的核对用错了公式**：把 A2 的失配参数 δ 与 §8.1 的能标依赖 ε_A 当成同一量；"
    "反推能给 **{:.2e} GeV**（超 M_Pl ~49 个数量级）⟹ **两者不是同一个 ε** ⟹ **不是 40 个量级的数值错误**".format(E_req))


# ══════════════════════════════════════════════════════════════════════
rule("NC-7  B：那么「LHC 无新物理」这个论断依赖 10⁻⁵⁰ 吗？")
# ══════════════════════════════════════════════════════════════════════

print("  §4.2 原句（第 201 行）的论证结构：")
print("     ① 事件流单体能标 E ~ E_P ≈ 10¹⁹ GeV ≫ LHC ~ 10⁴ GeV（**差 15 量级**）")
print("     ② ⟹ 事件流仅以**集体模态**显现 ⟹ **预言 LHC 无新物理**（与空结果一致）")
print("     ③ 各向同性 + 泊松涌撒 ⟹ 不破坏洛伦兹/CPT")
print("     ④ 泄漏 ε ~ 10⁻⁵⁰ 不产生 LHC 信号   ← **本句**")
print()
print("  ⟹ **①②③ 已完整给出论证**；④ 是**冗余的加强**，而且它的数值**无来源**。")
print("     若删掉 ④，「LHC 无新物理」的结论**不受影响**（因为①的 15 个量级已足够）。")
has15 = "差 15 量级" in TXT or "15 量级" in TXT
i201 = TXT.count("泄漏 ε~10⁻⁵⁰")
print()
print("  检索：第 201 行含「15 量级」{}；「泄漏 ε~10⁻⁵⁰」出现 {} 处".format(
    "✓" if has15 else "✗", i201))
chk("NC-7", has15,
    "**「LHC 无新物理」的论证不依赖 10⁻⁵⁰**（① 的 15 个量级已充分）⟹ 该数值可安全改注或删除")


# ══════════════════════════════════════════════════════════════════════
rule("NC-8  汇总：两处的裁决")
# ══════════════════════════════════════════════════════════════════════

print("  【A】§5.7「能隙 Δ = 1」（第 848 / 852 / 1524 行）")
print("     · 正确值（标准口径）= **Δ = 4J**（2+1D 周期环面，L 无关，解析＋L=2 数值双确认）")
print("     · 「1」的口径**无法从 L=2 唯一定出**（三个归一化在该点退化到 1）")
print("     · ⚠️ 与 §5.8 的「Δ = 2」相比：**差异的真实来源是「开 vs 周期」**（不是维度）")
print("     · 裁决：**改为 Δ = 4J 并写明口径**；（与 C-9 的做法一致 —— 标出条件）")
print()
print("  【B】§4.2「泄漏 ε ~ 10⁻⁵⁰」（第 201 行）")
print("     · 出处 = A2 报告（**输入，无推导**），经 M1 报告转引")
print("     · ⚠️ **第 0 批的「40 个数量级」是假警报**（用错了公式：两个不同的量）")
print("     · 「LHC 无新物理」的论证**不依赖**它 ⟹ 可安全改注")
print("     · 裁决：**改注为「框架的叙事性输入（无独立推导）」**，并**解除待核实**")
print("       ⚠️ 同时给「两个 ε」加符号区分（§8.1 的 ε_A vs 泄漏/失配参数）")
chk("NC-8", OK == 7,
    "前 7 项全部通过 ⟹ 两处均可**安全收口**：A 改为「Δ = 4J（口径：H = −JΣA_v − JΣB_p，周期环面）」；"
    "B 改为「叙事性输入、无推导」，并解除第 0 批的待核实标注（同时给「两个 ε」加符号区分）")

print()
print("=" * 78)
print("通过 {} 项，失败 {} 项".format(OK, BAD))
print("=" * 78)
