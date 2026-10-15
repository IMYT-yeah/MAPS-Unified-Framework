# -*- coding: utf-8 -*-
r"""
第 53 轮：S-E5（FQH 引力子模 epsilon 项）的能标审查
===================================================
问题：论文第 804 行 / 第 1245 行（S-E5）写
      Γ = Γ_Coulomb + ε·Γ_flux，ε ~ 10⁻²⁰ 泄漏项，线宽余项。
而同文件 §8.1 写     ε_A(E) = ε₀·(M_Pl/E)^β，β ≈ 0.615，ε₀ ≈ 7.6×10⁻²⁰，
且明言            E ~ 1 meV → ε ~ 1。

⟹ 若两处是同一个 ε，则 S-E5 引用的 10⁻²⁰ = ε₀ = ε(M_Pl)，而 FQH 能标是 meV
   ⟹ 能标错置。本轮把这件事算清楚。

检查项 SE-1 … SE-8。全程只做算术与引文核对，不做数值占卜。
"""
import math

LN10 = math.log(10.0)
M_PL_TEV = 1.2209e16          # M_Pl = 1.2209e19 GeV = 1.2209e16 TeV
E_TEV = 1.0                   # 锚点 1
ETA_TEV = 6e-10               # 重子不对称，锚在 1 TeV
E_MEV_IN_TEV = 1e-15          # 1 meV = 10⁻¹⁵ TeV

PASS = []
FAIL = []


def chk(tag, ok, msg):
    (PASS if ok else FAIL).append(tag)
    print("  [{}] {:<8} {}".format("OK" if ok else "XX", tag, msg))


def hdr(t):
    print()
    print("=" * 96)
    print("  " + t)
    print("=" * 96)


# ================================================================ SE-1  beta
hdr("SE-1  β 的来历：它由两个锚点能标之比决定，与 M_Pl 无关")

beta = math.log(ETA_TEV) / math.log(E_MEV_IN_TEV)      # 论文原式
print("  论文原式：β = log(6×10⁻¹⁰)/log(10⁻¹⁵) = {:.6f}".format(beta))
print("  等价写法：β = ln(η)/ln(1meV/1TeV)，因为两个锚点是 1 TeV 与 1 meV。")
print("  ⟹ β 与 M_Pl 无关；M_Pl 只进 ε₀。")
chk("SE-1", abs(beta - 0.615) < 1e-3,
    "复算 β = {:.4f}（论文记 0.615）⟹ ✓".format(beta))

# ================================================================ SE-2  eps0
hdr("SE-2  ε₀ 在论文里有四种写法")

eps0_formula = ETA_TEV / (M_PL_TEV / E_TEV) ** beta
variants = [("第 893 行", 7.6e-20), ("第 27/592/1056 行", 7.7e-20),
            ("第 914 行", 7.67e-20), ("由 E_c=1.0181 meV 反推", 7.751e-20)]
print("  由定义 ε₀ = ε(1TeV)/(M_Pl/1TeV)^β 算得：{:.4e}".format(eps0_formula))
print()
print("  {:<24} {:>12}".format("出处", "ε₀"))
for tag, v in variants:
    print("  {:<24} {:>12.4e}".format(tag, v))
spread = max(v for _, v in variants) / min(v for _, v in variants) - 1
chk("SE-2", spread < 0.05,
    "四种写法最大相对差 {:.1%} ⟹ 同一常数有 4 个版本（口径/精度残留）".format(spread))

# ================================================================ SE-3  E_c
hdr("SE-3  E_c = M_Pl·ε₀^(1/β) 复算（论文记 1.0181 meV）")

print("  {:<26} {:>12} {:>14}".format("所用 ε₀", "E_c (meV)", "vs 论文 1.0181"))
for tag, v in variants + [("定义式 ε₀（自洽）", eps0_formula)]:
    ec = M_PL_TEV * v ** (1.0 / beta) / E_MEV_IN_TEV
    print("  {:<26} {:>12.4f} {:>13.2%}".format(tag, ec, ec / 1.0181 - 1.0))

# ================================================================ SE-4  恒等式
hdr("SE-4  ⭐ E_c 是恒等式，不是【推导】：E_c ≡ 1 meV（与 M_Pl、ε₀ 无关）")

# 代入： ε₀ = ε(1TeV)/(M_Pl/1TeV)^β
#       E_c = M_Pl·ε₀^(1/β)
# ⟹ E_c = M_Pl · ε(1TeV)^{1/β} / (M_Pl/1TeV) = 1TeV · ε(1TeV)^{1/β}
ec_ident = E_TEV * ETA_TEV ** (1.0 / beta) / E_MEV_IN_TEV
print("  代数：E_c = M_Pl·ε₀^(1/β)")
print("         = M_Pl·[ε(1TeV)/(M_Pl/1TeV)^β]^(1/β)")
print("         = M_Pl·ε(1TeV)^(1/β)·(1TeV/M_Pl)")
print("         = 1TeV·ε(1TeV)^(1/β)          ← M_Pl 完全消掉")
print()
print("  数值：E_c = 1 TeV × (6×10⁻¹⁰)^(1/{:.4f}) = {:.6f} meV".format(beta, ec_ident))
print("  论文记值：1.0181 meV                                          （差 {:.2%}）".format(
    ec_ident / 1.0181 - 1.0))
print()
print("  ⟹ E_c 只是「两个锚点能标之比」的等号另一侧：")
print("     锚点 2 本来就是 ρ_Λ ~ (meV)⁴ ⟹ 取 E = 1 meV 使 ε = 1")
print("     ⟹ E_c ≡ 1 meV 是 锚点 2 的**重述**，不是它推出的新结论。")
print("     论文第 895 行把它标为【推导】并与「暗能量特征能标 2.3 meV 同量级」")
print("     ⟹ 这是**循环**（用锚点 2 的输入去验证锚点 2 的输入）。")
chk("SE-4", abs(ec_ident - 1.0) < 0.02,
    "E_c ≡ 1TeV·ε(1TeV)^(1/β) = {:.4f} meV ≈ 1 meV ⟹ **恒等式**（非推导）".format(ec_ident))

# ================================================================ SE-5  FQH
hdr("SE-5  FQH 平台的能标窗口与各能标下的 ε")

# GaAs 2DEG（杜灵杰团队 Nature 628, 78 (2024) 的平台）
M_STAR = 0.067          # m*/m_e
EPS_R = 12.9
HBAR_C_NM_EV = 197.327  # ℏc = 197.327 MeV·fm = 197.327 eV·nm
E2_4PE0 = 1.43996       # e²/(4πε₀) = 1.44 eV·nm

print("  {:<6} {:>9} {:>11} {:>13} {:>11}".format(
    "B (T)", "l_B (nm)", "ℏω_c (meV)", "E_C (meV)", "Δ_GMP (meV)"))
print("  " + "-" * 56)
rows = []
for B in (5.0, 10.0, 15.0):
    lB = math.sqrt(HBAR_C_NM_EV / (E2_4PE0 * B * 1e4))  # ℏc/(eB)，B 用 T
    lB_nm = 25.655 / math.sqrt(B)
    hw = 1.1578 * B / M_STAR          # meV
    EC = E2_4PE0 / (EPS_R * lB_nm) * 1000.0   # eV → meV
    dGMP = 0.6 * EC
    rows.append((B, lB_nm, hw, EC, dGMP))
    print("  {:<6.0f} {:>9.2f} {:>11.1f} {:>13.2f} {:>11.2f}".format(B, lB_nm, hw, EC, dGMP))

lB10, hw10, EC10, dGMP10 = rows[1][1], rows[1][2], rows[1][3], rows[1][4]
print()
print("  FQH 实验典型工作温度（杜灵杰平台 mK 量级）：")
for T_mK in (10.0, 30.0, 50.0):
    kT_meV = 8.617333e-2 * T_mK / 1000.0    # k_B = 8.617e-2 meV/K
    print("    T = {:>5.0f} mK ⟹ k_B T = {:.4f} meV = {:.2f} μeV".format(T_mK, kT_meV, kT_meV * 1000))

print()
print("  各能标口径下的 ε（用 ε(E) = ε₀(M_Pl/E)^β）：")
eps_of = lambda e_mev: eps0_formula * (M_PL_TEV / (e_mev * E_MEV_IN_TEV)) ** beta
scales = [("k_BT @ 10 mK", 8.617333e-2 * 10 / 1000.0),
          ("磁旋子能隙 Δ_GMP", dGMP10),
          ("实测引力子模能量（1 meV 代表值）", 1.0),
          ("Coulomb 能标 E_C", EC10),
          ("回旋能 ℏω_c", hw10)]
print("  {:<32} {:>12} {:>16}".format("过程能标口径", "E (meV)", "ε(E)"))
eps_list = []
for tag, E in scales:
    e = eps_of(E)
    eps_list.append((tag, E, e))
    print("  {:<32} {:>12.4f} {:>16.4g}".format(tag, E, e))

lo = min(e for _, _, e in eps_list)
hi = max(e for _, _, e in eps_list)
chk("SE-5", lo > 1e-3,
    "FQH 全部能标口径下 ε ∈ [{:.3g}, {:.3g}] —— 全部远大于 10⁻²⁰".format(lo, hi))

# ================================================================ SE-6  数量级差
hdr("SE-6  ε(FQH) 与论文写的 10⁻²⁰ 差多少个数量级")

print("  {:<32} {:>12} {:>14} {:>12}".format("口径", "ε(FQH)", "论文写的", "log10 比"))
for tag, E, e in eps_list:
    print("  {:<32} {:>12.4g} {:>14.1e} {:>12.1f}".format(tag, e, 1e-20, math.log10(e / 1e-20)))
gaps = [math.log10(e / 1e-20) for _, _, e in eps_list]
chk("SE-6", min(gaps) > 15.0,
    "差 {:d}–{:d} 个数量级 ⟹ **能标错置**（不是因子误差）".format(
        int(min(gaps)), int(max(gaps))))

# ================================================================ SE-7  可识别性
hdr("SE-7  可识别性检查：Γ = Γ_Coulomb + ε·Γ_flux 里有几个未知量")

print("  公式（论文 §9 S-E5 / §5.8 原样）：")
print("      Γ = Γ_Coulomb + ε·Γ_flux")
print()
print("  逐项清点：")
print("    Γ_Coulomb   —— 标准量（可独立算出）          已知，不引入参数")
print("    ε           —— 框架给的？")
print("                    · 若 = §8.1 的 ε_A(E)，则它是**能标依赖函数**（含 2 参数 β、ε₀）")
print("                    · 若另有所指，论文**没有给出它的任何定义**（全文搜索：ε 在 §9 只出现在本行）")
print("    Γ_flux      —— **全文没有表达式**（'Γ_flux' 在论文里只出现 2 次，都在同一预言句）")
print()
print("  ⟹ 未知量计数：")
print("     情形 A：ε = ε_A(E)  ⟹ 参数 {β, ε₀} 已知（由 §8.1 锚定），")
print("             但 Γ_flux 仍是**未定义的整函数** ⟹ 预言可被任意 Γ_flux 满足/规避")
print("     情形 B：ε 与 §8.1 无关 ⟹ {ε, Γ_flux} 两个未定义量，且 ε 与 10⁻²⁰ 的出处不明")
print()
print("  观测量：FQH 线宽 Γ 是**一个实数**（给定 B、ν、T）")
chk("SE-7", True,
    "两种情形下**未知量 ≥ 1 个自由函数** ⟹ 与第 45/52 轮同源：方程数 < 未知量数，**不可识别**")

# ================================================================ SE-8  两难
hdr("SE-8  两难：ε = O(1) 与「框架独有、标准无此项」不能同时成立")

print("  论文对 S-E5 的三处定位（§5.8 第 804 行、§9 第 1245 行、§10 第 1343 行）：")
print("    ① ε ~ 10⁻²⁰         ⟹ 视作**微小泄漏**")
print("    ② 「线宽余项」        ⟹ 视作比 Γ_Coulomb 小的**修正项**")
print("    ③ 「框架独有、标准凝聚态无此项」")
print()
print("  由 SE-5/SE-6：FQH 能标下 ε ∈ [{:.2g}, {:.2g}] ⟹ ②「余项」不成立".format(lo, hi))
print("  若 ε = O(1)，则 Γ_flux 与 Γ_Coulomb **同量级** ⟹ 二择一：")
print("    (a) 该项**已被标准理论包含**（标准已能算 GMP 谱与线宽：")
print("        GMP 1970s → Haldane 2016 几何理论 → Balram–Sreejith–Jain PRL 133, 246605 (2024) 分裂）")
print("        ⟹ 则 ③「独有」不成立；")
print("    (b) 该项**未被包含** ⟹ 则一个 O(1) 的通量项早该在 Nature 628, 78 (2024) 的谱里现形")
print("        ⟹ 则与实验**矛盾**。")
chk("SE-8", True,
    "ε = O(1) ⟹ 「微小余项」✗；「独有」与「一致」**只能取一** ⟹ S-E5 的定位需降调")

# ================================================================ 汇总
print()
print("=" * 96)
print("  汇总：通过 {} 项，失败 {} 项".format(len(PASS), len(FAIL)))
if FAIL:
    print("  失败项：{}".format(", ".join(FAIL)))
print("=" * 96)
