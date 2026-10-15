# -*- coding: utf-8 -*-
"""
从 A2 推组分比例（2026-09-17）
================================
A2: ε(E) = ε₀ (M_Pl c²/E)^β,  ε₀ = 7.7e-20, β = 0.615

CM-1  **E_c 的推导（无自由参数）**：ε = 1 的饱和能标
      E_c = M_Pl c² · ε₀^{1/β}   —— 只由 ε₀、β 决定
CM-2  η 的复算：ε(1 TeV) vs 观测 η
CM-3  Ω_Λ 的定量检验：ρ_Λ = E_c⁴/(ℏc)³ ⟹ Ω_Λ = ?
      框架闭式：Ω_Λ = (8π/3)(R_H/l_P)² ε₀^{4/β}
CM-4  反解：要匹配观测 Ω_Λ，需要多高的 E / 多大的前置因子
CM-5  组分-能标对应表：每个 Ω_i 反解出它的 ε 能标
"""
import math

c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
kB = 1.380649e-23
eV = 1.602176634e-19
lP = math.sqrt(hbar * G / c ** 3)
Mpc = 3.0856775814913673e22
H0 = 67.66 * 1e3 / Mpc

EP = hbar * c ** 5 / G
EP = math.sqrt(hbar * c ** 5 / G)          # 普朗克能量 J
MPL_eV = EP / eV                            # M_Pl c² in eV
eps0 = 7.7e-20
beta = 0.615
rho_crit = 3 * H0 ** 2 / (8 * math.pi * G)  # kg/m³
rho_crit_E = rho_crit * c ** 2              # J/m³

# 观测值（Planck 2018）
OM_b, OM_cdm, OM_L, OM_m = 0.0493, 0.2618, 0.6889, 0.3111
eta_obs = 6.14e-10
h = 0.6766


def eps(E_eV):
    """ε(E)，E 以 eV 计"""
    return eps0 * (MPL_eV / E_eV) ** beta


def E_of_eps(target):
    """反解：ε(E) = target 的 E（eV）"""
    return MPL_eV * (eps0 / target) ** (1.0 / beta)


def line(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


def chk(name, got, want, tol=1e-9):
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    print("  [%s] %-46s got=%.10g  want=%.10g" % ("OK" if ok else "XX", name, got, want))
    return ok


# ---------------------------------------------------------------- CM-1
line("CM-1  E_c 的推导：ε 饱和（ε=1）的能标，只由 ε₀ 与 β 决定")
Ec_eV = MPL_eV * eps0 ** (1.0 / beta)
print("  M_Pl c² = %.6g eV" % MPL_eV)
print("  ε₀^(1/β) = %.6g" % (eps0 ** (1.0 / beta)))
print("  E_c = M_Pl c² · ε₀^(1/β) = %.6g eV = **%.4f meV**" % (Ec_eV, Ec_eV * 1e3))
print("  框架独立声称的 E_c ≈ 1.01 meV")
chk("E_c 与框架声称值一致", Ec_eV * 1e3, 1.01, 0.01)
print("  ⟹ **A2 的两个参数决定了暗能量能标**，这是本轮最硬的结果（无自由参数）。")
print("  ⟹ 亦说明：ε 在 E ≤ E_c 时饱和到 1，暗能量就是「饱和的泄漏」。")

# ---------------------------------------------------------------- CM-2
line("CM-2  η 的复算：ε(1 TeV) vs 观测重子-光子比")
for ETeV in (0.5, 1.0, 2.0):
    print("  ε(%4.1f TeV) = %.6g" % (ETeV, eps(ETeV * 1e12)))
print("  观测 η = %.6g" % eta_obs)
chk("ε(1 TeV) ≈ η（2%% 内）", eps(1e12), eta_obs, 0.05)
print("  ⚠️ 诚实：E = 1 TeV 是**选来配 η 的**，不是推出来的。这是复算，不是预言。")
print("  ⟹ 若要它成为预言，框架必须独立推出为什么重子能标是 ~1 TeV。")

# ---------------------------------------------------------------- CM-3
line("CM-3  Ω_Λ 的定量检验：ρ_Λ = E_c⁴/(ℏc)³")
Ec_J = Ec_eV * eV
rhoL_E = Ec_J ** 4 / (hbar * c) ** 3
OM_L_frame = rhoL_E / rho_crit_E
print("  E_c = %.6g J ；(ℏc)³ = %.6g J³m³" % (Ec_J, (hbar * c) ** 3))
print("  ρ_Λ(框架) = E_c⁴/(ℏc)³ = %.6g J/m³" % rhoL_E)
print("  ρ_crit    = %.6g J/m³" % rho_crit_E)
print("  Ω_Λ(框架) = %.6f   ｜ Ω_Λ(观测) = %.4f   ⟹ 差 %.2f 倍"
      % (OM_L_frame, OM_L, OM_L / OM_L_frame))
# 闭式核验
RH = c / H0
N = (RH / lP) ** 2
OM_L_closed = (8 * math.pi / 3) * N * eps0 ** (4.0 / beta)
print("  框架闭式核验：Ω_Λ = (8π/3)(R_H/l_P)² ε₀^(4/β) = %.6f" % OM_L_closed)
chk("闭式 = 直接计算", OM_L_closed, OM_L_frame, 1e-9)
print("  ⟹ **能标对了（meV 量级 ✓），系数差 %.1f 倍 ✗**" % (OM_L / OM_L_frame))

# ---------------------------------------------------------------- CM-4
line("CM-4  反解：要匹配观测 Ω_Λ，需要什么")
E_need_eV = (OM_L * rho_crit_E * (hbar * c) ** 3) ** 0.25 / eV
print("  若 ρ_Λ = E⁴/(ℏc)³，匹配 Ω_Λ=%.4f 需 E = %.4f meV" % (OM_L, E_need_eV * 1e3))
print("  ⟹ E_need / E_c = %.4f  （ρ 差 %.2f 倍）"
      % (E_need_eV / Ec_eV, (E_need_eV / Ec_eV) ** 4))
print("  候选前置因子：8π = %.4f （需 %.2f，差 %.1f%%）"
      % (8 * math.pi, (OM_L / OM_L_frame), 100 * abs(8 * math.pi - OM_L / OM_L_frame) / (OM_L / OM_L_frame)))
print("  ⟹ 8π 是最接近的「天然」因子，但仍差 ~5%%，不足以救。")

# ---------------------------------------------------------------- CM-5
line("CM-5  组分-能标对应表：每个 Ω_i 反解出它的 ε 能标")
print("  组分        Ω        需要的 ε      对应能标 E")
for name, om in (("暗能量", OM_L), ("总物质", OM_m), ("重子", OM_b), ("暗物质", OM_cdm)):
    E = E_of_eps(om)
    print("  %-10s %-9.4f %-13.6g %.4g eV = %.4f meV" % (name, om, om, E, E * 1e3))
E_eta = E_of_eps(eta_obs)
print("  %-10s %-9.4g %-13.6g %.4g eV = %.4f TeV"
      % ("η(b/γ)", eta_obs, eta_obs, E_eta, E_eta / 1e12))
print()
print("  ⟹ 暗能量与总物质都落在 **meV 量级**（与 E_c 同量级，符合「都在饱和端」）。")
print("  ⟹ η 落在 **TeV 量级** —— 相差约 10^15，由 β=0.615 的陡峭性跨越：")
print("     ε 从 1 (meV) 降到 6e-10 (TeV) 需要 (E_c/E)^β = 6e-10 ⟹ E ~ %.3g TeV"
      % (Ec_eV * (1 / eta_obs) ** (1 / beta) / 1e12))

line("结论")
print("""  ✅ **E_c = M_Pl c² ε₀^(1/β) = 1.017 meV** —— 无自由参数，与框架独立声称的
     1.01 meV 一致（0.7%）。A2 的两个参数锁定了暗能量能标。这是本轮最硬的结果。
  ⚠️ ε(1 TeV) = 6.02e-10 ≈ η_obs（2%）—— 但 E=1TeV 是**选的**，是复算不是预言。
  ❌ Ω_Λ：ρ = E_c⁴/(ℏc)³ 给 0.0288，观测 0.689，**差 23.9 倍**。
     能标对、系数不对。8π 是最接近的天然因子（差 5%），仍救不回来。

  ⟹ **A2 目前给出的是「能标」，不是「组分比例」。** 真正缺的三件事：
     (a) Ω_Λ 的 24 倍系数来源；
     (b) 为什么重子能标是 ~1 TeV（否则 η 只是拟合）；
     (c) 暗物质（Ω_cdm = 0.262）在框架里对应什么能标/机制 —— 目前完全空白。
""")
