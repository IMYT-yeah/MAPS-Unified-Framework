# -*- coding: utf-8 -*-
"""
β = 1/(2π) 框架推导 —— 数值核验（2026-09-16）
================================================
核验四件事：
  BX-A  2π 的来源：F3 熵公式 S = k_B A/(4 l_P²) + 第一定律 dE = T dS
        ⟹ T_BH = ℏc³/(8πGMk_B)，其中 1/(2π) 为框架自有结果（非外部输入）
  BX-B  因果视界 R_c = c/H（ recession v = Hr = c ），表面引力 κ = c²/R_c = cH
        ⟹ k_B T = ℏH/(2π) ⟹ β = 1/(2π)，且与 λ 无关
  BX-C  全息能账 E = N k_B T 在 R_c 上给出 λ = 1（Ω_K = 0，k = 0）
  BX-D  对照：改用「表观视界」R_A = c/(H√λ) ⟹ 能账退化为恒等式（零预言力）；
        改用 Kodama 动力学表面引力 ⟹ λ = (1-3w)²/16，被 Planck+BAO 否证

仅依赖标准库 math。
"""
import math

c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
kB = 1.380649e-23
lP2 = hbar * G / c ** 3
lP = math.sqrt(lP2)
Mpc = 3.0856775814913673e22
Msun = 1.98892e30

H0 = 67.66 * 1e3 / Mpc          # Planck 2018, s^-1
OM_m, OM_r, OM_L = 0.3111, 9.2e-5, 0.6889


def line(t):
    print("\n" + "=" * 66)
    print(t)
    print("=" * 66)


def chk(name, got, want, tol=1e-9):
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    print("  [%s] %-42s got=%.10g  want=%.10g" % ("OK" if ok else "XX", name, got, want))
    return ok


# ---------------------------------------------------------------- BX-A
line("BX-A  2π 的来源：F3 熵 + 第一定律（框架自有，无外部输入）")
M_bh = Msun
Rs = 2 * G * M_bh / c ** 2
A = 4 * math.pi * Rs ** 2
S_over_kB = A / (4 * lP2)
T_firstlaw_over_kB = c ** 6 * lP2 / (8 * math.pi * kB * G ** 2 * M_bh)   # c²/(dS_phys/dM)
T_hawking_over_kB = hbar * c ** 3 / (8 * math.pi * G * M_bh * kB)
print("  太阳质量黑洞: Rs = %.4f km" % (Rs / 1e3))
print("  S/k_B = %.6g  (README 记 1.05e77)" % S_over_kB)
chk("S/k_B 与 README 1.05e77 一致", S_over_kB, 1.05e77, 5e-3)
chk("第一定律 T = c²/(dS/dM)", T_firstlaw_over_kB, T_hawking_over_kB, 1e-9)
print("  ⟹ T_BH = ℏc³/(8πGMk_B) = ℏκ/(2πck_B), κ = c⁴/(4GM)")
print("  ⟹ 1/(2π) 由 F3 + dE=TdS 锁定，是框架内的量，不是借来的")

# ---------------------------------------------------------------- BX-B
line("BX-B  因果视界 R_c = c/H ⟹ β = 1/(2π)（与 λ 无关）")
Rc = c / H0
kappa = c ** 2 / Rc
T_over_kB = hbar * kappa / (2 * math.pi * c * kB)
beta = T_over_kB * kB / (hbar * H0)
print("  H0 = %.6g s^-1 ; R_c = %.4f Gly" % (H0, Rc / 9.4607e24))
print("  κ = c²/R_c = cH = %.6g m/s²" % kappa)
print("  T = %.6g K" % T_over_kB)
chk("κ = cH", kappa, c * H0, 1e-12)
chk("β ≡ k_BT/(ℏH) = 1/(2π)", beta, 1 / (2 * math.pi), 1e-12)

# ---------------------------------------------------------------- BX-C
line("BX-C  全息能账 E = N k_B T 在 R_c 上 ⟹ λ = 1")
rho_c = 3 * H0 ** 2 / (8 * math.pi * G)
M_enc = (4.0 / 3) * math.pi * rho_c * Rc ** 3
N = math.pi * (Rc / math.sqrt(lP2)) ** 2          # = A/(4 l_P²)
E_grav = M_enc * c ** 2
E_therm = N * kB * T_over_kB
lam = E_therm * 2 * G * H0 / c ** 5
print("  ρ_c = %.6g kg/m³ ; M(<R_c) = %.6g kg" % (rho_c, M_enc))
print("  N = π(R_c/l_P)² = A/(4l_P²) = %.6g" % N)
print("  E_grav  = M c²        = %.10g J" % E_grav)
print("  E_therm = N k_B T     = %.10g J" % E_therm)
chk("E_grav / E_therm = 1  ⟹ λ = 1", E_grav / E_therm, 1.0, 1e-12)
chk("λ = 1", lam, 1.0, 1e-12)
chk("R_s(M) / R_c = λ = 1", 2 * G * M_enc / c ** 2 / Rc, 1.0, 1e-12)
print("  ⟹ Ω_K = 1 - λ = 0，k = 0，哈勃球 = 表观视界 = 史瓦西半径（黑洞宇宙）")

# ---------------------------------------------------------------- BX-D1
line("BX-D1  对照：若用「表观视界」R_A = c/(H√λ)，能账退化为恒等式")
print("  λ        R_A/R_c      ε/(ℏH)        1/(2π)·√λ     E/(N k_B T)")
for lam_t in (0.3, 0.6, 1.0, 3.0):
    RA = c / (H0 * math.sqrt(lam_t))
    N_A = math.pi * (RA / math.sqrt(lP2)) ** 2
    rho = lam_t * rho_c
    E_A = (4.0 / 3) * math.pi * rho * RA ** 3 * c ** 2
    eps = E_A / N_A / (hbar * H0)
    TA_over_kB = hbar * (c ** 2 / RA) / (2 * math.pi * c * kB)
    ratio = E_A / (N_A * kB * TA_over_kB)
    print("  %-8.2f %-12.6f %-15.10f %-13.10f %.12f"
          % (lam_t, RA / Rc, eps, math.sqrt(lam_t) / (2 * math.pi), ratio))
print("  ⟹ β = √λ/(2π) 与 κ = c²/R_A 给出的温度**恒等相等**：任取 λ 都成立")
print("  ⟹ 用表观视界做能账 = 与 Friedmann 等价，**对 λ 零预言力**（不是错的，是空的）")


# ---------------------------------------------------------------- BX-D2
line("BX-D2  对照：Kodama 动力学表面引力 ⟹ λ = (1-3w)²/16，被观测否证")
def w_eff(z):
    Ez2 = OM_m * (1 + z) ** 3 + OM_r * (1 + z) ** 4 + OM_L
    return (OM_r * (1 + z) ** 4 / 3 - OM_L) / Ez2


sig = 0.0019
print("  z        w_eff      Ω_K(Kodama)   Ω_K(本推导)  偏离(σ)   观测")
for z in (0, 0.5, 1, 3, 1100):
    w = w_eff(z)
    OK = 1 - (1 - 3 * w) ** 2 / 16
    print("  %-8d %-10.4f %-13.6f %-13.6f %-10.0f 0.0007±0.0019" % (z, w, OK, 0.0, OK / sig))
print("  ⟹ Kodama 处方在 z=0 就偏离 217σ；框架的温度必须取因果视界的 de Sitter 型 κ = cH")

# ---------------------------------------------------------------- BX-E
line("BX-E  必须诚实标注：代数能账 ≠ 微分第一定律（开放项）")
# 在 k=0 上 R_A = R_c = 1/H，两个面重合。检验 Cai-Kim 型微分定律 dE = TdS + W dV
# 是否与代数式 E = TS 相容（取 G=c=1 单位，ρ = 3H²/(8πG)）
print("  取 w, 用 E=(4π/3)ρR³, S=π/(GH²), T=H/(2π), W=(ρ-p)/2, R=1/H:")
print("  w        dE/dt            TdS/dt           WdV/dt           (TdS+WdV)/dE")
for w in (-1.0, -0.6889, 0.0, 1.0 / 3):
    Hd = -1.5 * (1 + w)          # Ḣ/H² = -(3/2)(1+w)
    rho = 3.0 / (8 * math.pi * G)     # H=1 单位下的 ρ/H²
    dE = 3 * (1 + w) / (4 * G)
    TdS = 1.5 * (1 + w) / G
    WdV = 9 * (1 - w) * (1 + w) / (8 * G)
    tot = TdS + WdV
    print("  %-8.4f %-16.6g %-16.6g %-16.6g %.6f"
          % (w, dE, TdS, WdV, tot / dE if dE else float('nan')))
print("  ⟹ 比值恒 ≠ 1（w=-1 为 de Sitter 退化点除外），两者**不是同一条方程**。")
print("  解 (TdS+WdV)/dE = 1 得 w = 5/3 —— 非物理。")
print("  ⟹ 本推导用的是**代数等分 E = N k_B T**（Verlinde/Padmanabhan 型，写在因果视界上），")
print("     不是 Cai-Kim 的微分第一定律（那条写在表观视界上，且与 Friedmann 等价）。")
print("     二者在 λ=1 时面重合但方程不重合 —— 这是框架的实质主张，必须单独检验。")

# ---------------------------------------------------------------- 汇总
line("结论")
print("""  链条（不再循环、不再空洞）：
    F3: S = k_B A/(4l_P²)  ──dE=TdS──▶  T = ℏκ/(2πck_B)      [2π 的来源]
    A1: 风暴微观速度 = c；v_rec = Hr  ──▶  因果视界 R_c = c/H   [任意 k 成立]
    ─▶ κ = c²/R_c = cH  ──▶  k_B T = ℏH/(2π)  ──▶  β = 1/(2π)  [与 λ 无关]
    ─▶ E = N k_B T ⟹ λ = 1 ⟹ Ω_K = 0 ⟹ k = 0 ⟹ 黑洞宇宙
""")
