# -*- coding: utf-8 -*-
"""
微分第一定律张力：真问题还是我算错了？（2026-09-16 夜）
==========================================================
在平直 ΛCDM 上（λ=1 ⟹ R_A = R_c = c/H，两个面重合）逐项数值检验：

  dE/dt  ?=  T dS/dt  +  W dV/dt

约定（全部显式写出，便于他人复核/挑错）：
  E  = (4π/3) ρ_E R³        ρ_E = ρ c² 为能量密度
  ρ̇_E = -3H(ρ_E + p)        连续性方程（标准）
  R  = c/H                  平直情形 R_A = R_c
  Ṙ  = -c Ḣ / H²
  S  = k_B A/(4 l_P²) = k_B π R²/l_P²
  T  = ℏ H /(2π k_B) = ℏ c /(2π k_B R)     （两种写法等价）
  W  = (ρ_E - p)/2            Hayward 工作密度（另一常见约定 W = -p 也一并检验）
  dV/dt = 4π R² Ṙ
"""
import math

c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
kB = 1.380649e-23
lP2 = hbar * G / c ** 3
Mpc = 3.0856775814913673e22
H0 = 67.66 * 1e3 / Mpc
OM_m, OM_r, OM_L = 0.3111, 9.2e-5, 0.6889


def w_eff(z):
    Ez2 = OM_m * (1 + z) ** 3 + OM_r * (1 + z) ** 4 + OM_L
    return (OM_r * (1 + z) ** 4 / 3 - OM_L) / Ez2


def line(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


line("逐项数值检验（平直 ΛCDM，w_eff 随时间变）")
print("  z      w_eff    dE/dt          TdS/dt         WdV/dt         (TdS+WdV)/dE")
for z in (0.0, 0.5, 1.0, 3.0):
    Ez2 = OM_m * (1 + z) ** 3 + OM_r * (1 + z) ** 4 + OM_L
    H = H0 * math.sqrt(Ez2)
    w = w_eff(z)
    # Ḣ 由 Friedmann 微分式给出（不额外假设）: Ḣ = -4πG(ρ_E+p)/c² ... 用 (1+z) 演化数值求导
    # 这里直接解析：Ḣ = -(3/2)(1+w)H² （平直、连续性方程）
    Hdot = -1.5 * (1 + w) * H ** 2
    R = c / H
    Rdot = -c * Hdot / H ** 2
    rhoE = 3 * H ** 2 * c ** 2 / (8 * math.pi * G)      # ρ_E = ρ_c c² （λ=1）
    p = w * rhoE
    rhoEdot = -3 * H * (rhoE + p)
    Edot = (4 * math.pi / 3) * (rhoEdot * R ** 3 + 3 * rhoE * R ** 2 * Rdot)
    S = kB * math.pi * R ** 2 / lP2
    Sdot = 2 * kB * math.pi * R * Rdot / lP2
    T = hbar * H / (2 * math.pi * kB)
    TdS = T * Sdot
    W = (rhoE - p) / 2                                  # 约定 A：Hayward
    Vdot = 4 * math.pi * R ** 2 * Rdot
    WdV = W * Vdot
    print("  %-6.1f %-8.4f %-14.6g %-14.6g %-14.6g %.6f"
          % (z, w, Edot, TdS, WdV, (TdS + WdV) / Edot))

print()
print("  对照约定 B：W = -p")
for z in (0.0, 1.0):
    Ez2 = OM_m * (1 + z) ** 3 + OM_r * (1 + z) ** 4 + OM_L
    H = H0 * math.sqrt(Ez2)
    w = w_eff(z)
    Hdot = -1.5 * (1 + w) * H ** 2
    R = c / H
    Rdot = -c * Hdot / H ** 2
    rhoE = 3 * H ** 2 * c ** 2 / (8 * math.pi * G)
    p = w * rhoE
    rhoEdot = -3 * H * (rhoE + p)
    Edot = (4 * math.pi / 3) * (rhoEdot * R ** 3 + 3 * rhoE * R ** 2 * Rdot)
    Sdot = 2 * kB * math.pi * R * Rdot / lP2
    TdS = (hbar * H / (2 * math.pi * kB)) * Sdot
    W = -p
    WdV = W * 4 * math.pi * R ** 2 * Rdot
    print("  z=%.1f  (TdS + WdV)/dE = %.6f" % (z, (TdS + WdV) / Edot))

line("检验 1：E = T·S 是否逐点成立（框架代数等分）")
for z in (0.0, 1.0, 3.0):
    Ez2 = OM_m * (1 + z) ** 3 + OM_r * (1 + z) ** 4 + OM_L
    H = H0 * math.sqrt(Ez2)
    R = c / H
    rhoE = 3 * H ** 2 * c ** 2 / (8 * math.pi * G)
    E = (4 * math.pi / 3) * rhoE * R ** 3
    S = kB * math.pi * R ** 2 / lP2
    T = hbar * H / (2 * math.pi * kB)
    print("  z=%.1f   E/(T·S) = %.12f" % (z, E / (T * S)))

line("检验 2：框架等分所隐含的有效工作密度 W_frame = S·dT/dV")
for z in (0.0, 1.0):
    Ez2 = OM_m * (1 + z) ** 3 + OM_r * (1 + z) ** 4 + OM_L
    H = H0 * math.sqrt(Ez2)
    w = w_eff(z)
    Hdot = -1.5 * (1 + w) * H ** 2
    R = c / H
    Rdot = -c * Hdot / H ** 2
    S = kB * math.pi * R ** 2 / lP2
    Tdot = hbar * Hdot / (2 * math.pi * kB)
    Vdot = 4 * math.pi * R ** 2 * Rdot
    W_frame = S * Tdot / Vdot
    rhoE = 3 * H ** 2 * c ** 2 / (8 * math.pi * G)
    W_GR = (rhoE - w * rhoE) / 2
    print("  z=%.1f   W_frame = %.6g   = %.6f × ρ_E  ｜  W_GR(Hayward) = %.6f × ρ_E"
          % (z, W_frame, W_frame / rhoE, W_GR / rhoE))

line("结论")
print("""  1. E = T·S **逐点严格成立**（比值 1.000000000000）—— 框架代数等分自洽。
  2. 但 dE = TdS + WdV **不成立**（两种 W 约定都失败），且比值随 z 变化。
  3. 框架等分隐含 W_frame = -ρ_E/3（**负号**），而 GR 的 W = (ρ_E-p)/2 > 0。
     ⟹ 分歧在**符号**：框架是「视界膨胀降温」(SdT<0)，标准定律是「压强做正功」(WdV>0)。
  4. de Sitter (w=-1) 是退化点：Ḣ=0 ⟹ 两边全零，0=0 成立。
""")
