# -*- coding: utf-8 -*-
"""
Ω_Λ 的 23.76 倍缺口：能补吗？（2026-09-17）
==============================================
OM-1  β 敏感度：d ln Ω_Λ / d β = -4 ln ε₀ / β² ≈ 465
      ⟹ β 改 1.1% 就让 Ω_Λ 变 24 倍 —— 这个公式**病态敏感**
OM-2  ε₀ 敏感度：d ln Ω_Λ / d ln ε₀ = 4/β ≈ 6.5
OM-3  天然前置因子枚举：8π / 4! / e^π / π⁴/4 … 谁最接近 23.76？
OM-4  判决：能补吗？
OM-5  替代识别：ρ_P/N、ρ_P ε₀/N … 各给多少 Ω_Λ？
"""
import math

c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
eV = 1.602176634e-19
lP = math.sqrt(hbar * G / c ** 3)
Mpc = 3.0856775814913673e22
H0 = 67.66 * 1e3 / Mpc

EP = math.sqrt(hbar * c ** 5 / G)
MPL_eV = EP / eV
eps0, beta = 7.7e-20, 0.615
rho_crit = 3 * H0 ** 2 / (8 * math.pi * G)
rho_crit_E = rho_crit * c ** 2
RH = c / H0
N = (RH / lP) ** 2
OM_L_obs = 0.6889


def OmL(eps0_=None, beta_=None):
    e = eps0 if eps0_ is None else eps0_
    b = beta if beta_ is None else beta_
    return (8 * math.pi / 3) * N * e ** (4.0 / b)


def line(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


base = OmL()
gap = OM_L_obs / base

# ---------------------------------------------------------------- OM-1
line("OM-1  β 敏感度（病态）")
d = -4 * math.log(eps0) / beta ** 2
print("  Ω_Λ = (8π/3)(R_H/l_P)² ε₀^(4/β)")
print("  d ln Ω_Λ / d β = -4 ln ε₀ / β² = %.2f" % d)
print("  ⟹ **β 每变 1%%，Ω_Λ 变 %.0f%%**" % (100 * (math.exp(0.01 * d) - 1)))
# 反解需要的 β
b_need = 4.0 / (math.log(OM_L_obs / ((8 * math.pi / 3) * N)) / math.log(eps0))
print("  反解：匹配 Ω_Λ=%.4f 需 β = %.6f（当前 %.3f，差 %.2f%%）"
      % (OM_L_obs, b_need, beta, 100 * (b_need - beta) / beta))
print("  要让 Ω_Λ 精度在 10%% 内，β 必须精确到 %.3f%%" % (100 * 0.10 / d))
print("  ⟹ 要么 β 被微调到 0.02%%，要么**这个公式是错的**。后者可能性大得多。")

# ---------------------------------------------------------------- OM-2
line("OM-2  ε₀ 敏感度")
print("  d ln Ω_Λ / d ln ε₀ = 4/β = %.3f" % (4 / beta))
e_need = eps0 * gap ** (beta / 4)
print("  匹配 Ω_Λ 需 ε₀ = %.6g（当前 %.6g，需放大 %.2f 倍）"
      % (e_need, eps0, e_need / eps0))
print("  ⟹ ε₀ 要改 63%% —— 也不是小修。且 ε₀ 还被用来配 η(1 TeV)，改它会连带动 η。")
print("  连带检验：ε₀ 改成 %.4g 后 ε(1 TeV) = %.4g（原 6.02e-10，观测 η=6.14e-10）"
      % (e_need, e_need * (MPL_eV / 1e12) ** beta))

# ---------------------------------------------------------------- OM-3
line("OM-3  天然前置因子枚举（需 %.4f）" % gap)
cands = [("8π", 8 * math.pi), ("4! = 24", 24.0), ("e^π", math.exp(math.pi)),
         ("π⁴/4", math.pi ** 4 / 4), ("6π", 6 * math.pi), ("2π²", 2 * math.pi ** 2),
         ("π⁴/4 · (3/2)", math.pi ** 4 / 4 * 1.5), ("(4π/3)²", (4 * math.pi / 3) ** 2),
         ("8π/3 · 3 = 8π", 8 * math.pi), ("ln2 · 34.3", 34.3 * math.log(2))]
for name, v in cands:
    print("  %-16s = %-12.4f  偏差 %+7.2f%%" % (name, v, 100 * (v - gap) / gap))
print("  ⟹ 最接近的是 4! = 24（+1.0%%）与 e^π（−2.6%%），但都没有物理动机。")
print("  ⟹ **数值凑合得了的不少，能给出机制的没有。**")

# ---------------------------------------------------------------- OM-4
line("OM-4  判决")
print("""  ρ_Λ = E_c⁴/(ℏc)³ 这条识别**应当放弃，而不是补**：

   · 它对 β 的敏感度是 d ln Ω/dβ ≈ 465 —— 一个用来定能标的指数，不该有这么大的杠杆。
   · 补它需要 β 微调到 0.02%%，或 ε₀ 改 63%%（还会连带动已配好的 η）。
   · 天然因子虽然有几个凑得近（4!、e^π），但都是数值巧合，没有机制。

  ⟹ **能标对了（meV 量级由 E_c 锁定，这个结论保住），
     但把 ρ_Λ 直接等同于 E_c⁴ 是错的。** 需要换一个 ρ_Λ 的构造。""")

# ---------------------------------------------------------------- OM-5
line("OM-5  替代构造：各给多少 Ω_Λ？")
rhoP_E = EP / lP ** 3
alts = [
    ("E_c⁴/(ℏc)³（当前）", (MPL_eV * eps0 ** (1 / beta) * eV) ** 4 / (hbar * c) ** 3),
    ("ρ_P/N（微观全息稀释）", rhoP_E / N),
    ("ρ_P·ε₀/N", rhoP_E * eps0 / N),
    ("ρ_P·ε₀", rhoP_E * eps0),
    ("H²/G·c²（= ρ_P/N）", (H0 ** 2 / G) * c ** 2),
]
print("  构造                          ρ (J/m³)          Ω        与观测比")
for name, r in alts:
    om = r / rho_crit_E
    print("  %-28s %-16.6g %-10.5g %.4g" % (name, r, om, om / OM_L_obs))
print("""
  ⟹ 微观那条（ρ_P/N）给 Ω = 8.378 —— 比观测**大 12.2 倍**；
    E_c⁴ 那条给 0.029 —— 比观测**小 23.8 倍**。
  ⟹ 两者相差 %.0f 倍，观测值 %.4f 夹在中间偏上。**两条路都还差一个 O(10) 的因子。**"""
      % (8.378 / 0.0290, OM_L_obs))

# ---------------------------------------------------------------- OM-6
line("OM-6  两参数联立：A2 能否同时配住 η 与 Ω_Λ？")
eta_obs = 6.14e-10
L1 = math.log(MPL_eV / 1e12)              # ln(M_Pl/1TeV)
L2 = math.log((8 * math.pi / 3) * N)
# ln ε₀ = ln η - β L1          （η 约束）
# ln ε₀ = (β/4)(ln Ω - L2)     （Ω_Λ 约束）
beta_fit = math.log(eta_obs) / (L1 + 0.25 * math.log(OM_L_obs) - 0.25 * L2)
eps0_fit = math.exp(math.log(eta_obs) - beta_fit * L1)
print("  联立解得：β = %.6f（当前 %.3f，+%.2f%%）"
      % (beta_fit, beta, 100 * (beta_fit - beta) / beta))
print("            ε₀ = %.6g（当前 %.6g，%.1f%%）"
      % (eps0_fit, eps0, 100 * (eps0_fit - eps0) / eps0))
print("  回代检验：ε(1 TeV) = %.6g（观测 η = %.6g）"
      % (eps0_fit * (MPL_eV / 1e12) ** beta_fit, eta_obs))
print("            Ω_Λ     = %.6f（观测 %.4f）" % (OmL(eps0_fit, beta_fit), OM_L_obs))
Ec_fit = MPL_eV * eps0_fit ** (1 / beta_fit)
print("  此时 E_c = %.4f meV（原 1.0181 meV）" % (Ec_fit * 1e3))
print("""
  ⟹ **能配住**，但两个参数都要动：β 0.615 → %.4f（**%+.2f%%**），
     ε₀ 7.7e-20 → %.4g（**%+.1f%%**）。尤其 ε₀ 要砍掉四成。
  ⟹ 但代价是**微调**：d ln Ω/dβ = %.0f ⟹ 要让 Ω_Λ 精度在 10%% 内，
     β 必须精确到 %.3f%%（即 β = %.4f ± %.4f）。
  ⟹ 两个参数配两个观测量，本就没有预言力；再加这个敏感度，
     **ρ_Λ = E_c⁴ 这条识别不具备可信度**。

  ✅ 保住的结论：**暗能量能标在 meV 量级**（联立解下 E_c = %.2f meV，仍是 meV）。
  ❌ 放弃的结论：把 ρ_Λ 直接等同于 E_c⁴。"""
      % (beta_fit, 100 * (beta_fit - beta) / beta, eps0_fit,
         100 * (eps0_fit - eps0) / eps0,
         d, 100 * 0.10 / d, beta_fit, 0.10 / d, Ec_fit * 1e3))
