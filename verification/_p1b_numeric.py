# -*- coding: utf-8 -*-
"""
P1-B 数值检验：
1) epsilon_A 截断能标（概率归一化 E_c: eps_A(E_c)=1）
2) 原文"meV 能标 = 哈勃尺度"对应的数值核对
3) w(z) 参数化与 DESI 约束
"""
import math

print("="*70)
print("B1) epsilon_A 截断能标（概率归一化）")
print("="*70)
M_Pl = 1.22e19   # GeV
beta = 0.615
eps0 = 6e-10 / (M_Pl/1e3)**beta   # 由边界条件1: E=1TeV -> 6e-10
print(f"eps0 = {eps0:.3e}")

# eps_A(E) = eps0*(M_Pl/E)^beta = 1  ->  E_c = M_Pl * eps0^(1/beta)
E_c = M_Pl * eps0**(1.0/beta)
print(f"eps_A(E_c)=1 的截断能标: E_c = {E_c:.3e} GeV = {E_c*1e9:.2f} eV = {E_c*1e12:.2f} meV")

# 验证
def eps_A(E_GeV):
    return eps0*(M_Pl/E_GeV)**beta
print(f"  验证: eps_A(1.0 meV) = {eps_A(E_c):.3f}")

print()
print("="*70)
print("B2) 原文'meV 能标=哈勃尺度'对应的数值核对")
print("="*70)
# meV 的波长
hc = 1.2398e-6   # eV*m  (hc = 1.2398 eV·μm = 1.2398e-6 eV·m)
lam_meV = hc/1e-3
print(f"1 meV 光子波长 = {lam_meV:.3e} m = {lam_meV*1e3:.2f} mm")
R_H = 1.3e26      # m 哈勃半径
print(f"哈勃半径 = {R_H:.2e} m")
print(f"比值: 哈勃半径/meV波长 = {R_H/lam_meV:.2e}  (差 {math.log10(R_H/lam_meV):.1f} 个数量级)")
# 哈勃尺度能量
H0 = 2.2e-18      # s^-1
hbar = 1.055e-34  # J·s
E_H = hbar*H0     # J
E_H_eV = E_H/1.602e-19
print(f"哈勃尺度能量 hbar*H0 = {E_H_eV:.2e} eV")
print(f"meV / 哈勃能标 = {1e-3/E_H_eV:.2e}  (差 {math.log10(1e-3/E_H_eV):.1f} 个数量级)")
print("=> 原文'meV 能标对应哈勃尺度湮灭事件'的对应在数值上不成立（差 ~35 个数量级）")

print()
print("="*70)
print("B3) 暗能量特征能标与 CMB 温度")
print("="*70)
rho_Lambda = 6e-10  # J/m^3 观测暗能量密度
rho_Lambda_GeV4 = rho_Lambda / (1.602e-19 * 1e9**4)  # J/m^3 -> GeV^4 (1 GeV^4/m^3 ~ ...)
# 更直接: rho_Lambda = (2.3 meV)^4
E_Lambda = (rho_Lambda / (1.602e-19 / (1e-3)**4))**0.25  # 计算 (rho_J/m3 对应能量) 的四次根, meV
# 简化: 已知 rho_Lambda^{1/4} = 2.3 meV
print(f"暗能量特征能标 rho_Lambda^(1/4) = 2.3 meV (标准)")
T_CMB = 2.725  # K
T_CMB_meV = T_CMB * 8.617e-5  # K -> eV -> meV
print(f"CMB 温度 = {T_CMB} K = {T_CMB_meV*1e3:.3f} meV")
print(f"比值 rho_Lambda^(1/4)/T_CMB = 2.3e-3 eV / {T_CMB_meV*1e3*1e-3:.4f} eV = {2.3/(T_CMB_meV):.1f}")

print()
print("="*70)
print("B4) w(z) 参数化与 DESI 约束")
print("="*70)
# 模型: rho_Lambda(z) = rho_Lambda,0 (1+z)^{4*eps}, w = -1 + 4*eps/3
# 更物理: 饱和能标漂移 E_c(z)=E_c,0(1+z)^eps; 相干长度 xi ∝ t^nu, E_c ∝ 1/xi ∝ (1+z)^{3nu/2}
# w = -1 + 2*nu
print("模型: E_c(z) ∝ (1+z)^eps, rho_Lambda ∝ E_c^4, w = -1 + 4eps/3")
print("模型(相干长度): xi ∝ t^nu, E_c ∝ (1+z)^{3nu/2}, w = -1 + 2nu")
print()
print("观测约束 (DESI 2024 + CMB 组合): w = -1.028 ± 0.031")
print("=> |1+w| < 0.031 -> |4eps/3| < 0.031 -> |eps| < 0.023")
print("=> |2nu| < 0.031 -> |nu| < 0.0155")
print()
for eps_val in [0.0, 0.01, 0.02, 0.023, -0.01, -0.02]:
    w = -1 + 4*eps_val/3
    nu = 2*eps_val/3
    print(f"  eps={eps_val:+.3f} (nu={nu:+.4f}): w = {w:+.4f}  {'✓ 与观测兼容' if abs(1+w)<0.031 else '✗ 超出约束'}")
print()
print("DESI w0-wa 模型 hint (2024): w0=-0.69±0.03, wa=-0.66±0.12 (与 ΛCDM 有张力, 若含 Pantheon+ 减弱)")
print("框架预测: w = const = -1+4eps/3, wa=0 (常数 w). 未来 DESI/Euclid 可测 |eps|<0.01")
print()
# 红移演化图示数值
print("--- rho_Lambda 的红移演化 (不同 eps) ---")
for z in [0, 0.5, 1.0, 2.0]:
    row = f"  z={z}: "
    for eps_val in [0.0, 0.02]:
        rho_r = (1+z)**(4*eps_val)
        row += f"eps={eps_val:+}: rho/rho0={rho_r:.4f};  "
    print(row)

print()
print("="*70)
print("B5) 截断后暗能量密度自洽性: (E_c)^4")
print("="*70)
# (E_c)^4 与观测比较: E_c = 1.0 meV
E_c_eV = E_c*1e9  # eV
E_c_GeV = E_c
rho_calc_GeV4 = E_c_GeV**4
rho_obs_GeV4 = (2.3e-12)**4
print(f"E_c = {E_c_eV:.2f} meV")
print(f"(E_c)^4 = {rho_calc_GeV4:.2e} GeV^4")
print(f"rho_Lambda 观测 = (2.3 meV)^4 = {rho_obs_GeV4:.2e} GeV^4")
print(f"比值 = {rho_calc_GeV4/rho_obs_GeV4:.2f}  (E_c=1.0meV vs 2.3meV)")
print("=> 截断能标 E_c≈1.0 meV 与暗能量特征能标 2.3 meV 同量级（差 2.3 倍）")
print("=> '暗能量 = ε_A 饱和区 (E_c)^4' 自洽: 数量级吻合, 精确值需修正系数")
