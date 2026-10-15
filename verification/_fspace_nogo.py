# -*- coding: utf-8 -*-
"""
抑制律 f_space(ρ_m)：不只是"还没找到"，而是**结构上不可能**（2026-09-17）
==========================================================================
上一轮结论：机制 B 需 ⟨f_space⟩ = 1/32，且 f_space 是自由函数 ⟹ 零预言力。
本轮加一条更硬的约束：**局部密度抑制律 + 原文自己的"空洞处 f_space≈1"
⟹ ⟨f_space⟩ 有下界，且该下界远大于 1/32。**

FN-1  需要的 ⟨f_space⟩（= 1/32）
FN-2  **下界定理**：⟨f_space⟩ ≳ (空洞体积分数) × f_space(空洞)
FN-3  四个自然抑制律的数值评估（全部差 30 倍以上）
FN-4  消耗型模型需要多大的截面？⟹ 荒谬
FN-5  判决：机制 B 的物理图像被否证，不是"待补"
"""
import math

c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
lP = math.sqrt(hbar * G / c ** 3)
tP = lP / c
mP = math.sqrt(hbar * c / G)
Mpc = 3.0856775814913673e22
H0 = 67.66 * 1e3 / Mpc

rhoP = mP / lP ** 3
rho_crit = 3 * H0 ** 2 / (8 * math.pi * G)
RH = c / H0
N = (RH / lP) ** 2
eps_eff = 1.0 / N
OM_b, OM_cdm, OM_m = 0.0493, 0.2618, 0.3111
rho_DM_obs = OM_cdm * rho_crit
rho_bare = eps_eff * rhoP
f_need = rho_DM_obs / rho_bare
n_b = OM_b * rho_crit / 1.67262192e-27          # 重子数密度 m^-3


def line(t):
    print("\n" + "=" * 74)
    print(t)
    print("=" * 74)


# ---------------------------------------------------------------- FN-1
line("FN-1  需要的 ⟨f_space⟩")
print("  ρ_bare = ε_eff·ρ_P = %.6g kg/m³" % rho_bare)
print("  ρ_DM(观测)        = %.6g kg/m³" % rho_DM_obs)
print("  ⟹ ⟨f_space⟩ = **%.8f = 1/%.2f**" % (f_need, 1 / f_need))

# ---------------------------------------------------------------- FN-2
line("FN-2  **下界定理**（本轮核心）")
print("  前提 (a)：原文自己说『在真空地带 f_space ≈ 1』（批05 §2.3）")
print("  前提 (b)：若 f_space 是**局部物质密度**的函数 f_space(ρ_m)，则它在空洞里取 1")
print("  前提 (c)：观测——空洞占体积 **50–80%**")
print()
print("  则 (b)+(c) ⟹")
print("     ⟨f_space⟩ = ⟨f_space(ρ_m)⟩ ≥ V_void/V · f_space(ρ_void)")
print("                                    ≈ 0.5–0.8 × 1 = **0.5–0.8**")
print()
print("  但需要的是 %.5f，比下界小 **%.0f–%.0f 倍**。" % (f_need, 0.5 / f_need, 0.8 / f_need))
print()
print("  ⟹ **对任何『局部密度抑制律』，⟨f_space⟩ 都不可能低到 1/32。**")
print("     这不是「律还没找到」，是**满足前提的律不存在**。")

# ---------------------------------------------------------------- FN-3
line("FN-3  四个自然抑制律的数值评估（全球平均）")
print("  律                          全球 ⟨f_space⟩      与 1/32 之比")
laws = []
# (1) 位点占据：孤子占普朗克元胞
f1 = 1 - n_b * lP ** 3
laws.append(("位点占据 1−n_b l_P³", f1))
# (2) 消耗型：截面 = 普朗克面积
sigma_P = lP ** 2
f2 = 1.0 / (1 + n_b * sigma_P * c * tP)
laws.append(("消耗型 σ = l_P²", f2))
# (3) 通量绑定：f = 1 − ρ_m/ρ_bare
f3 = 1 - OM_m * rho_crit / rho_bare
laws.append(("通量绑定 1−ρ_m/ρ_bare", f3))
# (4) 线性正比：f = ρ_m/ρ_bare
f4 = OM_m * rho_crit / rho_bare
laws.append(("正比 ρ_m/ρ_bare", f4))
for name, v in laws:
    print("  %-28s %-19.8g %.4g" % (name, v, v / f_need))
print("  ⟹ 前三个都 ≈ 1（差 30 倍以上）；第四个 0.037 差 19%%，且**没有机制**。")

# ---------------------------------------------------------------- FN-4
line("FN-4  消耗型模型要凑出 1/32，需要多大的截面？")
sigma_need = (1 / f_need - 1) / (n_b * c * tP)
print("  f_space = 1/(1 + n_b σ c t_P) = %.5f ⟹ n_b σ c t_P = %.2f" % (f_need, 1 / f_need - 1))
print("  ⟹ σ = %.4g m²" % sigma_need)
print("  对照：普朗克面积 l_P² = %.4g m²" % sigma_P)
print("  ⟹ 需要比普朗克面积大 **%.3g 倍** —— 荒谬。" % (sigma_need / sigma_P))
print()
print("  反推：若 σ 取自然的 l_P²，则 n_b σ c t_P = %.4g ⟹ f_space = 1（完全无抑制）"
      % (n_b * sigma_P * c * tP))

# ---------------------------------------------------------------- FN-5
line("FN-5  判决")
print("""  ❌ **机制 B 的物理图像被否证，不是「待补」。**

   · 需要 ⟨f_space⟩ = {:.5f}，而**任何局部密度抑制律**给的下界是 **0.5–0.8**（FN-2）
   · 四个自然律分别给 {:.4g} / {:.4g} / {:.6g} / {:.5g}，均差 19%–35 倍
   · 消耗型模型要凑数需截面比普朗克面积大约 10¹⁰⁶ 倍""".format(
    f_need, f1, f2, f3, f4) + """


  ⟹ 原文的图像（『真空活跃度高、物质区低』⟹ 低 ⟨f_space⟩）**在算术上不成立**：
     因为空洞占了大半体积，而空洞的 f_space 恰恰是 1。

  ✅ 唯一能救的出路（诚实列出）：
     (i) 放弃"局部密度抑制"图像 —— 但那样就没有 f_space(ρ_m)，原文描述即错；
     (ii) 让 ε 不是 1/N（改变 ρ_bare）—— 但那会牵动前面已定的全息链条；
     (iii) 承认 f_space 是**非局部的**（依赖视界尺度）—— 需要全新机制，等于重写这一块。

  ⟹ 结论：**暗物质定量解释 = 框架的第四个空白**，这一条现在有了结构性论证，不只是"未解决"。
""")
