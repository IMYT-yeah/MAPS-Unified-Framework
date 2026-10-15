# -*- coding: utf-8 -*-
"""
Friedmann 的两条路（2026-09-17 凌晨）
======================================
BX-J  框架其实**已经导出**了平直 Friedmann 方程：由 R_c=c/H + F3 + T_GH + 等分 E=N k_B T
      直接解出 ρ = 3H²/(8πG)。全程只用定义，未用 Friedmann。
BX-K  微观路径：ε_eff = 1/N = (l_P/R_H)² ⟹ ρ = ρ_P/N = c²H²/G ⟹ **ρ ∝ H²**，
      λ = 8π/3 ≈ 8.378（**标度对，系数差 8.4 倍**）
BX-L  朴素绝对估计：Γ·ε·E_P/H vs ρ_crit —— 差多少？（宇宙学常数问题的框架版）
BX-M  微观模型的 λ 是否红移无关（⟹ 平坦性稳定）
"""
import math

c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
kB = 1.380649e-23
lP = math.sqrt(hbar * G / c ** 3)
tP = lP / c
Mpc = 3.0856775814913673e22
H0 = 67.66 * 1e3 / Mpc
EP = hbar / tP                       # 普朗克能量 J
rhoP_E = EP / lP ** 3                # 普朗克能量密度 J/m³


def line(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


def chk(name, got, want, tol=1e-9):
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    print("  [%s] %-46s got=%.10g  want=%.10g" % ("OK" if ok else "XX", name, got, want))
    return ok


# ---------------------------------------------------------------- BX-J
line("BX-J  框架已导出平直 Friedmann（不预设 Friedmann，只用定义）")
print("  输入：R_c = c/H；N = π R_c²/l_P²（F3）；k_B T = ℏH/(2π)（因果视界 κ=cH）")
print("  等分：E = N k_B T，其中 E = (4π/3) ρ R_c³ c²（Misner-Sharp 质量，定义）")
H = H0
Rc = c / H
# 由等分解 ρ：
# (4π/3) ρ Rc³ c² = π Rc²/l_P² · ℏH/(2π)
rho_solved = (math.pi * Rc ** 2 / lP ** 2) * (hbar * H / (2 * math.pi)) / ((4 * math.pi / 3) * Rc ** 3 * c ** 2)
rho_fried = 3 * H ** 2 / (8 * math.pi * G)          # 平直 Friedmann 的 ρ（质量密度 kg/m³）
print("  解出 ρ = %.10g kg/m³" % rho_solved)
print("  平直 Friedmann 给 ρ = %.10g kg/m³" % rho_fried)
chk("等分解出的 ρ ≡ 3H²/(8πG)", rho_solved, rho_fried, 1e-12)
print("  ⟹ **H² = 8πGρ/3 是输出，不是输入**。等分账直接给出平直 Friedmann。")
print("  ⟹ 09-11 起一直记为「框架未导出 Friedmann」—— 现在应改为：")
print("     **已导出平直(k=0)约束方程；仍未导出的是加速度方程与连续性方程（动力学）。**")

# ---------------------------------------------------------------- BX-K
line("BX-K  微观路径：泄漏 ε_eff = 1/N ⟹ ρ ∝ H²（标度对，系数差 8.4 倍）")
N = (Rc / lP) ** 2
eps_eff = 1.0 / N
rho_micro_E = rhoP_E * eps_eff                      # 能量密度 J/m³
rho_micro = rho_micro_E / c ** 2                    # 质量密度 kg/m³
lam_micro = rho_micro / rho_fried
print("  N = (R_H/l_P)² = %.6g ；ε_eff = 1/N = %.6g" % (N, eps_eff))
print("  ρ_P = %.6g J/m³ ；ρ_micro = ρ_P/N = %.6g kg/m³" % (rhoP_E, rho_micro))
print("  解析：ρ_micro = ρ_P(l_P/R_H)² = H²/G   （ρ_P = ℏc/l_P⁴，l_P² = ℏG/c³，R_H = c/H）")
chk("ρ_micro = H²/G", rho_micro, H ** 2 / G, 1e-12)
chk("λ_micro = 8π/3", lam_micro, 8 * math.pi / 3, 1e-12)
print("  ⟹ **λ = 8π/3 ≈ %.4f，红移无关（常数）** —— 标度对了，系数差 %.2f 倍"
      % (8 * math.pi / 3, 8 * math.pi / 3))
print("  ⟹ 微观路径给出 ρ ∝ H²（**平坦性稳定的关键**）；系数由全息等分钉为 λ=1。")

# ---------------------------------------------------------------- BX-L
line("BX-L  朴素绝对估计：不做全息稀释会差多少（CC 问题的框架版）")
Gamma = c / lP ** 4                                 # 事件率密度 1/(m³·s)
eps0 = 7.7e-20                                      # A2 的 ε₀（高能端）
rho_naive_E = Gamma * eps0 * EP / H                 # 累积一个哈勃时
rho_naive = rho_naive_E / c ** 2
print("  Γ = c/l_P⁴ = %.6g m⁻³s⁻¹ ；E_P = %.6g J" % (Gamma, EP))
print("  ρ_naive = Γ·ε₀·E_P/H = %.6g kg/m³" % rho_naive)
print("  ρ_crit  = %.6g kg/m³" % rho_fried)
print("  ⟹ 超出 %.3g 倍（约 10^%d）" % (rho_naive / rho_fried,
                                        round(math.log10(rho_naive / rho_fried))))
print("  ⟹ 框架的 50:50 必须提供这个量级的抵消，**且必须精确到 10^-%.0f**"
      % round(math.log10(rho_naive / rho_fried)))
print("  ⟹ 这就是宇宙学常数问题，框架尚未解决，只是换了套语言表述。")

# ---------------------------------------------------------------- BX-M
line("BX-M  微观模型 λ 的红移无关性（⟹ 平坦性稳定，不是巧合）")
print("  z        H(z)/H0      λ_micro       λ_全息等分")
for z in (0.0, 0.5, 1.0, 3.0, 1100.0):
    Hz = H0 * math.sqrt(0.3111 * (1 + z) ** 3 + 9.2e-5 * (1 + z) ** 4 + 0.6889)
    Rz = c / Hz
    Nz = (Rz / lP) ** 2
    rho_mz = (rhoP_E / Nz) / c ** 2
    rho_fz = 3 * Hz ** 2 / (8 * math.pi * G)
    print("  %-8.1f %-12.4f %-13.10f 1.0000000000" % (z, Hz / H0, rho_mz / rho_fz))
print("  ⟹ λ_micro 恒为 8π/3，与 z 无关 ⟹ **ρ ∝ H² 保证平坦性不随时间漂移**。")

line("结论")
print("""  1. **框架已导出平直 Friedmann 方程**（ρ = 3H²/8πG 是输出）。
     09-11 起记为缺口，应更正为「已导出约束方程，缺动力学（加速度 + 连续性）」。
  2. **微观泄漏给出 ρ ∝ H²**（λ = 8π/3，红移无关）—— 平坦性稳定有了机制。
  3. 两条路差 8π/3 = 8.378 倍：微观给系数 8.4，全息等分给 1。
     ⟹ 分工：微观管**标度**（ρ ∝ H²），全息管**归一化**（λ = 1）。
  4. 绝对量级仍未解决（10^157），框架继承了宇宙学常数问题，未解决它。
""")
