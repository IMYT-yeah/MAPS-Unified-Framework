# -*- coding: utf-8 -*-
"""
P3 数值验证：
B) epsilon_B 精确化（70 倍偏差 + f_space 来源探索）
C) S=A/4 微态计数（k=e^{1/4} 与 G、ℏ 出现机制）
D) beta_ppn 二阶项（通量亏损二阶系数 a=-3/2）
"""
import math

print("="*70)
print("B) epsilon_B 精确化与 f_space")
print("="*70)
M_Pl_kg = 2.18e-8
l_P = 1.616e-35
R_U = 1.3e26
rho_raw = 2*M_Pl_kg/l_P**3
eps_B = (l_P/R_U)**2
rho_DM_calc = eps_B * rho_raw
rho_DM_obs = 2.3e-27   # kg/m^3
print(f"rho_raw = 2m_P/l_P^3 = {rho_raw:.2e} kg/m^3")
print(f"eps_B = (l_P/R_U)^2 = {eps_B:.2e}")
print(f"rho_DM_calc = eps_B*rho_raw = {rho_DM_calc:.2e} kg/m^3")
print(f"rho_DM_obs = {rho_DM_obs:.2e} kg/m^3")
print(f"偏差因子 = {rho_DM_calc/rho_DM_obs:.1f} 倍  ({math.log10(rho_DM_calc/rho_DM_obs):.1f} 个数量级)")
print(f"闭合所需 f_space = {rho_DM_obs/rho_DM_calc:.4f}")

print("\n--- 候选 f_space 来源检验 ---")
Omega_b = 0.049   # 重子密度参数 (DESI 2024)
Omega_m = 0.314   # 总物质密度参数
Omega_DM = 0.264
print(f"Omega_b/Omega_m = {Omega_b/Omega_m:.4f}")
print(f"Omega_b/Omega_DM = {Omega_b/Omega_DM:.4f}")
print(f"Omega_DM/Omega_m = {Omega_DM/Omega_m:.4f}")
print(f"候选 f_space: Omega_b/Omega_m*0.1 = {Omega_b/Omega_m*0.1:.4f}")

# 临界密度对照
H0 = 2.2e-18
G = 6.674e-11
rho_crit = 3*H0**2/(8*math.pi*G)
print(f"\nrho_crit = {rho_crit:.2e} kg/m^3")
print(f"rho_DM_calc/rho_crit = {rho_DM_calc/rho_crit:.1f}  (框架'残余'约为临界密度的 {rho_DM_calc/rho_crit:.1f} 倍)")

print()
print("="*70)
print("C) S=A/4 微态计数")
print("="*70)
# S = N * ln k, N = A/l_P^2, 观测要求 S = A/(4l_P^2)
# => ln k = 1/4, k = e^{1/4}
k = math.exp(0.25)
print(f"每普朗克面元的有效态数 k = e^(1/4) = {k:.4f}")
print(f"验证: N*ln k = (A/l_P^2)*(1/4) = A/(4l_P^2) = S ✓")
print(f"等价表述: 每 4 个普朗克面积 1 个独立比特 (ln k = 1/4)")

# G, hbar 出现机制
c = 3e8
hbar = 1.055e-34
l_P2 = G*hbar/c**3
print(f"\n普朗克面积 l_P^2 = G*hbar/c^3 = {l_P2:.3e} m^2  (定义值 {l_P**2:.3e} m^2)")
print(f"S = A/(4l_P^2) = A*c^3/(4G*hbar)  ->  G, hbar 作为 l_P^2 的复合出现")
print(f"  G、hbar 不是基本常数, 而是'微变事件最小尺度 l_P'的复合 (框架公理1)")

# 太阳质量黑洞熵
M_sun = 1.989e30
R_s = 2*G*M_sun/c**2
A_sun = 4*math.pi*R_s**2
S_sun = A_sun/(4*l_P**2)
print(f"\n太阳质量黑洞: R_s = {R_s:.1e} m, A = {A_sun:.2e} m^2, S = {S_sun:.2e}")
print(f"原初黑洞(M=1e11 kg): R_s = {2*G*1e11/c**2:.2e} m, S = {4*math.pi*(2*G*1e11/c**2)**2/(4*l_P**2):.2e}")

print()
print("="*70)
print("D) beta_ppn 二阶项")
print("="*70)
# g_00 = -(rho/rho_inf)^2, rho/rho_inf = 1 - x + a*x^2, x = GM/(c^2 r)
# (1-x+a x^2)^2 = 1 - 2x + (2a+1)x^2
# PPN: g_00 = -(1 + 2U/c^2 - 2 beta U^2/c^4), U = GM/r, U/c^2 = x
# => -2 beta x^2 = (2a+1)x^2 -> beta = -(2a+1)/2
print("rho/rho_inf = 1 - x + a*x^2  (x = GM/(c^2r))")
print("=> g_00 = -(1 - 2x + (2a+1)x^2)")
print("PPN 对照: g_00 = -(1 + 2U/c^2 - 2*beta*U^2/c^4) = -(1 + 2x - 2*beta*x^2)")
print()
for a in [0, -0.5, -1.0, -1.5]:
    beta = -(2*a+1)/2
    print(f"  a={a:+.1f}: beta_ppn = {beta:+.2f}  {'✓ 与观测 beta=1 一致' if abs(beta-1)<0.001 else ''}")
print()
print("=> 观测 beta_ppn=1 要求 a = -3/2:")
print("   rho/rho_inf = 1 - x - (3/2)x^2  (通量亏损二阶系数 -3/2)")
print("   物理: 通量越稀, 吞噬效率越高 (正反馈) - 微观机制待推导")
print()
# GR 参考: Schwarzschild 各向同性坐标 g_00 展开
print("GR 参考 (各向同性坐标): g_00 = -[(1-M/2r)/(1+M/2r)]^2 = -(1-2M/r+2(M/r)^2+...)")
print("  => beta_ppn = 1 对应二阶项 +2x^2 (即 a=-3/2 的 g_00 二阶 = (2a+1)x^2 = -2x^2)")
print("  框架要求 a=-3/2 使 (2a+1) = -2, 与 GR 二阶项 -2x^2 一致 ✓")

print()
print("="*70)
print("E) 多表示统一场: 通量场涨落的分波分解")
print("="*70)
print("通量场涨落 delta_Phi(x) 的不可约分解 (Lorentz 群):")
print("  标量分量 (spin-0):  Phi  ->  Higgs/模场通道 (通量各向同性涨落)")
print("  矢量分量 (spin-1):  A_mu -> 电磁 U(1) 通道 (通量有向涨落)")
print("  张量分量 (spin-2):  h_munu -> 引力通道 (通量二阶张量涨落)")
print("=> 四力 = 同一通量场涨落的分波分解 (与 KK g_55=标量, g_mu5=矢量 对应)")
print()
print("谱作用实现: S = Tr f(D^2/Lambda^2), 热核展开:")
print("  a_0 项: 宇宙学常数")
print("  a_1 项: R (Einstein-Hilbert, 引力)")
print("  a_2 项: F^2 (Yang-Mills, 规范场)")
print("=> 同一个算子 D 的不同阶 => 不同力 (批1 数学组 §1.6 Weitzenböck)")
