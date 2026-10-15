# -*- coding: utf-8 -*-
"""
动力学缺口探针（2026-09-17）
================================
DY-1  给定约束方程 ρ=3H²/8πG，**连续性方程 ⟺ 加速度方程**（缺口从两条减为一条）
DY-2  对 E = T·S 求导：是恒等式，给不出新方程（此路不通）
DY-3  微观生产率的**自洽性检查**：Π vs 3Hρ，差多少？（⟹ 必须有复合过程）
DY-4  若复合时标 τ = t_P ⟹ 稳态 ρ = Π·t_P = ρ_P/N（与微观模型**精确一致**）
DY-5  准静态条件 3H t_P ≪ 1
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
EP = hbar / tP
rhoP_E = EP / lP ** 3


def line(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


def chk(name, got, want, tol=1e-9):
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    print("  [%s] %-48s got=%.10g  want=%.10g" % ("OK" if ok else "XX", name, got, want))
    return ok


# ---------------------------------------------------------------- DY-1
line("DY-1  给定 ρ=3H²/8πG，连续性 ⟺ 加速度（缺口两条 → 一条）")
print("  由 ρ = 3H²/(8πG) 求导 ⟹ ρ̇ = 3HḢ/(4πG)")
print("  代入连续性 ρ̇ = -3H(ρ+p/c²) = -3Hρ(1+w)：")
print("     3HḢ/(4πG) = -3H(1+w)·3H²/(8πG)  ⟹  Ḣ = -(3/2)(1+w)H²")
print("  加速度 ä/a = Ḣ + H² = -(1/2)(1+3w)H² = -(4πG/3)(ρ+3p/c²) ✓")
for w in (-1.0, -0.6889, 0.0, 1.0 / 3):
    H = H0
    rho = 3 * H ** 2 / (8 * math.pi * G)
    Hdot_cont = -1.5 * (1 + w) * H ** 2                    # 由连续性
    addot_a_cont = Hdot_cont + H ** 2
    addot_a_std = -(4 * math.pi * G / 3) * rho * (1 + 3 * w)   # 标准加速度方程
    print("    w=%-8.4f ä/a(连续性)=%.6e  ä/a(加速度方程)=%.6e  比=%.12f"
          % (w, addot_a_cont, addot_a_std, addot_a_cont / addot_a_std))
print("  ⟹ **两者等价**。框架只需要再补一条（任取其一），缺口不是两条。")

# ---------------------------------------------------------------- DY-2
line("DY-2  对 E = T·S 求导：恒等式，无新信息（此路不通）")
H = H0
Rc = c / H
Hdot = -1.5 * (1 + (-0.6889)) * H ** 2
Rdot = -c * Hdot / H ** 2
E = (4 * math.pi / 3) * (3 * H ** 2 / (8 * math.pi * G)) * Rc ** 3 * c ** 2
S = kB * math.pi * Rc ** 2 / lP ** 2
T = hbar * H / (2 * math.pi * kB)
Edot = (c ** 4 / (2 * G)) * Rdot * 0  # 占位，下面用解析式
Edot = 3 * H * Hdot * c ** 2 / (4 * math.pi * G) * (4 * math.pi / 3) * Rc ** 3 / 1.0  # 见下注释
# 直接用 ρ̇ 与 R 的变化：
rho_E = 3 * H ** 2 * c ** 2 / (8 * math.pi * G)
rho_Edot = 3 * H * Hdot * c ** 2 / (4 * math.pi * G)
Edot = (4 * math.pi / 3) * (rho_Edot * Rc ** 3 + 3 * rho_E * Rc ** 2 * Rdot)
Sdot = 2 * kB * math.pi * Rc * Rdot / lP ** 2
Tdot = hbar * Hdot / (2 * math.pi * kB)
lhs = Edot
rhs = T * Sdot + S * Tdot
print("  dE/dt            = %.10g" % lhs)
print("  T dS/dt + S dT/dt = %.10g" % rhs)
chk("dE = TdS + SdT（E=T·S 的微分，恒等）", lhs / rhs, 1.0, 1e-12)
print("  ⟹ 对 E = T·S 求导只是它的微分，**不产生新方程**。这条路封死。")
print("  ⟹ 动力学必须由别处来：组分状态方程 / A2 泄漏率。")

# ---------------------------------------------------------------- DY-3
line("DY-3  微观生产率自洽性检查：Π vs 稀释率 3Hρ")
N = (Rc / lP) ** 2
eps_eff = 1.0 / N
Gamma = c / lP ** 4
Pi = Gamma * eps_eff * EP                      # J m^-3 s^-1
rho_E = 3 * H ** 2 * c ** 2 / (8 * math.pi * G)
dilution = 3 * H * rho_E
print("  Γ = c/l_P⁴ = %.6g m⁻³s⁻¹ ；ε_eff = 1/N = %.6g" % (Gamma, eps_eff))
print("  Π = Γ·ε_eff·E_P = %.6g J m⁻³ s⁻¹" % Pi)
print("  3Hρ_E（稀释率）  = %.6g J m⁻³ s⁻¹" % dilution)
print("  ⟹ Π / (3Hρ_E) = %.4g   （约 10^%d 倍）"
      % (Pi / dilution, round(math.log10(Pi / dilution))))
print("  ⟹ **若无复合过程，生产率超出 61 个量级**，模型不自洽。")

# ---------------------------------------------------------------- DY-4
line("DY-4  引入复合时标 τ = t_P ⟹ 稳态 ρ = Π·t_P = ρ_P/N（与微观模型精确一致）")
for tau_name, tau in (("t_P（普朗克时标）", tP), ("1/H（哈勃时标）", 1 / H)):
    w = 0.0
    rho_ss = Pi * tau / (1 + 3 * H * tau * (1 + w))
    print("  τ = %-16s 稳态 ρ_E = %.6g J/m³   = %.6f × ρ_crit"
          % (tau_name, rho_ss, rho_ss / rho_E))
rho_micro = rhoP_E / N
print("  ρ_P/N（微观模型）= %.6g J/m³" % rho_micro)
chk("Π·t_P = ρ_P/N", Pi * tP, rho_micro, 1e-12)
print("  ⟹ **框架需要一个普朗克时标的复合过程**，否则微观模型自相矛盾。")
print("  ⟹ 物理读法：风暴以速率 Π 处理能量、每份只停留 t_P ⟹ 存量 ρ = Π·t_P。")

# ---------------------------------------------------------------- DY-5
line("DY-5  准静态条件")
print("  3H·t_P = %.6g  ≪ 1 ✓  ⟹ 稳态近似 ρ ≈ Π·τ 极好（修正 O(10^-61)）" % (3 * H * tP))
print("  H·t_P  = %.6g  = l_P/R_c = 1/√N  ⟹ 所有 H 依赖都是这个无量纲量的幂次"
      % (H * tP))

line("结论")
print("""  1. **缺口从两条减为一条**：给定已导出的约束方程，连续性 ⟺ 加速度。
  2. **对 E = T·S 求导是恒等式**，不产生新方程 —— 此路封死，别再试。
  3. 微观模型**自洽需要一个 t_P 时标的复合过程**；有它则 ρ = Π·t_P = ρ_P/N 精确成立，
     没有它则生产率超出 61 个量级。
  4. ⟹ 真正缺的是**组分与状态方程**（ρ 如何随 a 稀释），不是"动力学"本身。
     框架目前从标准物理借状态方程（w=0 / 1/3 / -1），不是从 A1/A2 推出来的。
""")
