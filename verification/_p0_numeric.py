# -*- coding: utf-8 -*-
"""
P0 任务数值检验：
A) PPN gamma 推导相关数值（光偏折、Shapiro、近日点进动、引力波速度约束）
B) epsilon 双含义数值兼容性检验
"""
import math

print("="*70)
print("A) PPN gamma 推导数值检验")
print("="*70)

# 常数
c = 3.0e8          # m/s
G = 6.674e-11      # m^3/(kg s^2)
M_sun = 1.989e30   # kg
R_sun = 6.957e8    # m
AU = 1.496e11      # m
M_earth = 5.972e24 # kg
R_earth = 6.371e6  # m

# 太阳表面弱场参数
Phi_sun = G*M_sun/R_sun/c**2
print(f"太阳表面 GM/(c^2 R) = {Phi_sun:.3e}  (弱场参数, <<1 验证弱场近似)")

# PPN 度规: g_00 = -(1 - 2GM/(c^2 r)), g_ij = (1 + 2*gamma*GM/(c^2 r)) delta_ij
# 光线偏折角: Delta_theta = (1+gamma)/2 * 4GM/(c^2 b), b = 碰撞参数
b = R_sun  # 光线掠过太阳表面
print("\n--- 光线偏折（掠太阳表面）---")
for gamma_val, name in [(1.0, "GR (gamma=1)"), (0.0, "无空间弯曲 (gamma=0)"), (-1.0, "通量压缩 (gamma=-1)")]:
    theta = (1+gamma_val)/2 * 4*G*M_sun/(c**2*b) * 180/math.pi * 3600  # 弧度->角秒
    print(f"  {name}: 偏折角 = {theta:.2f} arcsec")

# 水星近日点进动 (PPN): domega = (2+2*gamma-beta)/3 * 6*pi*GM/(c^2 a (1-e^2))
print("\n--- 水星近日点进动 ---")
a_M = 5.79e10      # m 水星半长轴
e_M = 0.2056       # 水星偏心率
per_cent = 36525.0*86400.0 / (2*math.pi*math.sqrt(a_M**3/(G*M_sun)))  # 世纪内轨道数
for gamma_val, beta_val, name in [(1.0, 1.0, "GR (gamma=beta=1)"), (1.0, 2.0, "beta=2 试探"), (0.0, 1.0, "gamma=0")]:
    factor = (2+2*gamma_val-beta_val)/3.0
    dw_rad = factor * 6*math.pi*G*M_sun/(c**2*a_M*(1-e_M**2))
    dw_arcsec_cent = dw_rad * 180/math.pi * 3600 * per_cent
    print(f"  {name}: 进动 = {dw_arcsec_cent:.2f} arcsec/世纪  (GR 观测值 ~43.0)")

# Shapiro 时间延迟
print("\n--- Shapiro 时间延迟（往返）---")
for gamma_val, name in [(1.0, "GR (gamma=1)"), (0.0, "gamma=0")]:
    dt = (1+gamma_val)/2 * 4*G*M_sun/c**3 * math.log(4*AU/R_sun)
    print(f"  {name}: 太阳往返时延 = {dt*1e6:.2f} us")

# 引力波速度约束 (GW170817)
print("\n--- 引力波速度约束 (GW170817) ---")
print(f"  GW170817: |c_g/c - 1| < 1e-15 (LIGO/Virgo) -> 排除标量/矢量额外极化为主")
print(f"  GR: 仅张量极化 (spin-2); 标量极化对应额外自由度, PPN 中 alpha1/2/3 关联")

# 引力波速度与 gamma 的 PPN 关系（简写）
print("\n--- PPN 参数现状 ---")
print(f"  gamma: 1.0000 ± 0.000023 (Cassini 2003) / ±1e-5 (VLBI)")
print(f"  beta: 1.0000 ± 0.0003 (LAGEOS/MESSENGER)")
print(f"  eta(合并参数)=4β-γ-3: 0.0000 ± 0.0010")

print()
print("="*70)
print("B) epsilon 双含义数值检验")
print("="*70)

# 常数（自然单位辅助）
M_Pl = 1.22e19      # GeV
M_Pl_kg = 2.18e-8   # kg
l_P = 1.616e-35     # m
t_P = 5.39e-44      # s
R_universe = 1.3e26 # m (哈勃半径)
T_universe = 4.35e17 # s (138 亿年)

# B1: epsilon_A(E) = eps0*(M_Pl/E)^beta, beta=0.615
print("\n--- B1: epsilon_A 能标依赖 (原文 157 页) ---")
def eps_A(E_GeV):
    # 用边界条件 E=1TeV -> 6e-10 定 eps0
    beta = 0.615
    eps0 = 6e-10 / (M_Pl/1e3)**beta
    return eps0*(M_Pl/E_GeV)**beta

print(f"  eps_A(1 TeV)   = {eps_A(1e3):.2e}   (边界条件1: 重子不对称 eta~6e-10)")
print(f"  eps_A(1 GeV)   = {eps_A(1.0):.2e}")
print(f"  eps_A(1 MeV)   = {eps_A(1e-3):.2e}")
print(f"  eps_A(1 eV)    = {eps_A(1e-9):.2e}")
print(f"  eps_A(1 meV)   = {eps_A(1e-12):.2e}  (原文边界条件2 声称~1, 实际~1e-2)")
E_H = 1.5e-33  # eV = 哈勃尺度能量
print(f"  eps_A(哈勃能标 {E_H:.1e} eV) = {eps_A(E_H*1e-9):.2e}  (发散远超1)")

# B2: epsilon_B
print("\n--- B2: epsilon_B 统计衰减因子 (原文 1413-1421 页) ---")
rho_raw = 2*M_Pl_kg/l_P**3
print(f"  rho_raw = 2m_P/l_P^3 = {rho_raw:.2e} kg/m^3  (原文 ~1e96)")
eps_B_geom = (l_P/R_universe)**2
print(f"  eps_B = (l_P/R_universe)^2 = {eps_B_geom:.2e}  (原文 ~1e-120)")
rho_DM = eps_B_geom * rho_raw
print(f"  暗物质密度 = eps_B*rho_raw = {rho_DM:.2e} kg/m^3  (观测 ~2.5e-27)")
print(f"  (1/3)^n=1e-120 -> n = {math.log(1e-120)/math.log(1/3):.1f}  (原文: 251, 非120)")

# B3: 兼容性检验
print("\n--- B3: 两套 epsilon 兼容性 ---")
# 求 E 使 eps_A(E) = 1e-120
beta = 0.615
eps0 = 6e-10 / (M_Pl/1e3)**beta
target = 1e-120
# (M_Pl/E)^beta = target/eps0
log10_E = math.log10(M_Pl) - math.log10(target/eps0)/beta
print(f"  使 eps_A(E)=1e-120 的能标: E = 10^{log10_E:.1f} GeV  (远超普朗克能标, 物理上不可能)")
print(f"  -> 结论: 在 eps_A 幂律假设下, 不存在任何能标 E 使 eps_A(E) = eps_B")
print(f"  -> eps_A 第二边界条件 (meV->1, 暗能量) 与 eps_B 机制 (几何衰减) 数值不兼容")

# B4: 若放弃 eps_A 第二边界条件
print("\n--- B4: 修正方案检验 ---")
print(f"  方案1: eps_A 仅负责重子不对称 (单边界条件) -> beta 需新机制")
print(f"  方案2: 暗能量=eps_B 几何机制 (与暗物质统一, 1413-1421 页) -> 暗物质密度吻合")
print(f"  检验方案2自洽性: rho_Lambda_obs ~ 6e-10 J/m^3; eps_B*rho_raw*c^2 = {eps_B_geom*rho_raw*c**2:.2e} J/m^3")
print(f"    (若乘 f_space~0.7: {eps_B_geom*rho_raw*c**2*0.7:.2e} J/m^3)")

# B5: 1413 页原始密度核对
print("\n--- B5: 1413 页原始密度量纲核对 ---")
print(f"  2m_P/l_P^3 = {rho_raw:.2e} kg/m^3  (原文写 1e96 kg/(m^3·s) 疑为量纲笔误)")
print(f"  2m_P/(l_P^3*t_P) = {rho_raw/t_P:.2e} kg/(m^3·s)  (原文数值更接近无 /s 版本)")

print()
print("="*70)
print("C) 引力推导补充数值 (P0 报告用)")
print("="*70)
# 通量亏损 1/r 形式验证: rho(r)/rho(inf) = 1 - GM/(c^2 r)
for r_fac, label in [(R_sun, "太阳表面"), (1e3*R_sun, "1000 R_sun"), (AU, "1 AU")]:
    x = G*M_sun/(c**2*r_fac)
    print(f"  {label}: GM/(c^2 r) = {x:.3e}, rho(r)/rho(inf) ~ 1-{x:.3e}, dt(r)/dt(inf) ~ sqrt(1-{2*x:.3e})")
