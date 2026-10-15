# -*- coding: utf-8 -*-
"""
过载区径向密度分布与辐射传输 (遗留②③)
静水平衡 + 钳制物态: dP/dr = -ρ·GM(r)/r², P(ρ)=P_P·tanh(ρ/ρ_P)
dP/dρ = c²·sech²(ρ/ρ_P) ⟹ dρ/dr = -ρ·GM(r)/(r²·c²·sech²(ρ/ρ_P))
中心积分 + 二分 ρ_c 使 M(r_h)=M (总质量条件)
辐射传输: τ = ∫(ρ/m_P)·l_P² dr (碎片散射截面 ~ l_P² 普朗克单元), 透射率 T=e^{-τ}
"""
import numpy as np

# 常数
G = 6.674e-11
c = 2.998e8
hbar = 1.055e-34
lP = 1.616e-35          # 普朗克长度
mP = 2.176e-8           # 普朗克质量 (kg)
rhoP = mP/lP**3         # 普朗克密度 5.2e96 kg/m³
PP = c**7/(hbar*G**2)   # 普朗克压强 4.6e113 Pa
c2 = c*c

def integrate(rho_c, M, r_h, n=4000):
    """从中心积分: 返回 r[], rho[], P[], M[], cs[], tau 直到 r_h"""
    r_min = max(r_h*1e-8, 1e-4*lP)  # 中心截断 (数值)
    r = np.logspace(np.log10(r_min), np.log10(r_h), n)
    rho = np.empty(n); Mv = np.empty(n); P = np.empty(n); cs = np.empty(n)
    rho[0] = rho_c; Mv[0] = 0.0
    for i in range(n-1):
        dr = r[i+1] - r[i]
        # RK4 对 (rho, M)
        def derivs(rr, rho_, M_):
            sech2 = 1.0/np.cosh(rho_/rhoP)**2
            drho = -rho_*G*M_/(rr*rr*c2*max(sech2, 1e-30)) if rr > 0 else 0.0
            dM = 4*np.pi*rr*rr*rho_
            return drho, dM
        k1r, k1M = derivs(r[i], rho[i], Mv[i])
        k2r, k2M = derivs(r[i]+dr/2, rho[i]+dr*k1r/2, Mv[i]+dr*k1M/2)
        k3r, k3M = derivs(r[i]+dr/2, rho[i]+dr*k2r/2, Mv[i]+dr*k2M/2)
        k4r, k4M = derivs(r[i]+dr, rho[i]+dr*k3r, Mv[i]+dr*k3M)
        rho[i+1] = rho[i] + dr*(k1r+2*k2r+2*k3r+k4r)/6
        Mv[i+1] = Mv[i] + dr*(k1M+2*k2M+2*k3M+k4M)/6
        if rho[i+1] < 1e-3*rho_c and Mv[i+1] < 0.999*M:
            # 密度掉太快, 提前截断 (不会发生: 等温球 r^-2 尾部)
            pass
    P = PP*np.tanh(rho/rhoP)
    cs2 = c2/np.cosh(rho/rhoP)**2
    # 光学深度 τ = ∫ (ρ/m_P)·l_P² dr
    tau = np.trapezoid((rho/mP)*lP*lP, r)
    return r, rho, P, Mv, np.sqrt(np.clip(cs2,0,None)), tau

def solve(M, label):
    r_h = 2*G*M/c2
    # 二分 ρ_c: 使 M(r_h) = M
    lo, hi = rhoP*1e-12, rhoP*1e6
    for _ in range(60):
        mid = np.sqrt(lo*hi)
        r, rho, P, Mv, cs, tau = integrate(mid, M, r_h)
        if Mv[-1] < M: lo = mid
        else: hi = mid
    rho_c = np.sqrt(lo*hi)
    r, rho, P, Mv, cs, tau = integrate(rho_c, M, r_h)
    rho_h = rho[-1]; P_h = P[-1]
    M_err = abs(Mv[-1]-M)/M
    # 等温球外区拟合: ρ ~ A/r² (取后半段)
    half = len(r)//2
    A = np.median(rho[half:]*r[half:]**2)
    # 核心饱和半径 (ρ = rhoP 处)
    r_sat = np.interp(np.log10(rhoP), np.log10(rho[::-1]), r[::-1]) if (rho[0]>rhoP>rho[-1]) else np.nan
    print(f"\n=== {label}: M={M:.2e} kg, r_h={r_h:.2e} m ===")
    print(f"  中心密度 ρ_c = {rho_c:.3e} kg/m³ = {rho_c/rhoP:.3e} ρ_P")
    print(f"  边缘密度 ρ(r_h) = {rho_h:.3e} kg/m³, 边缘压强 P(r_h) = {P_h:.2e} Pa = {P_h/PP:.2e} P_P")
    print(f"  总质量守恒: M(r_h)/M = {Mv[-1]/M:.6f} (误差 {M_err:.1e})")
    print(f"  核心饱和半径 r(ρ=ρ_P) = {r_sat:.3e} m = {r_sat/r_h:.2e} r_h" if np.isfinite(r_sat) else "  核心未达饱和")
    print(f"  外区 ρ~A/r² 拟合: A = {A:.3e} (等温球 A_iso=c²/2πG={c2/(2*np.pi*G):.2e})")
    print(f"  光学深度 τ = {tau:.3e}, 透射率 T = e^(-τ) = {np.exp(-tau):.3e}")
    print(f"  声速: 中心 c_s = {cs[0]/c:.4f} c, 边缘 c_s = {cs[-1]/c:.4f} c")
    # 质量分布: 核心 vs 外壳
    i_sat = np.argmin(np.abs(rho - rhoP))
    M_in = Mv[i_sat]
    print(f"  饱和核内质量 M(r<r_sat) = {M_in:.2e} kg = {M_in/M*100:.1f}% M")
    return dict(r=r, rho=rho, P=P, Mv=Mv, cs=cs, tau=tau, rho_c=rho_c, r_sat=r_sat)

print("="*72)
print("过载区径向密度分布与辐射传输 (遗留②③)")
print("钳制物态 P=P_P·tanh(ρ/ρ_P) + 静水平衡 + 总质量守恒")
print("="*72)

# 求解各质量黑洞
sol_sun  = solve(1.989e30, "太阳质量黑洞")
sol_sgr  = solve(4.3e36, "Sgr A*")
sol_m87  = solve(6.5e39, "M87*")
sol_pbh  = solve(1e11, "原初黑洞 10^11 kg")
sol_planck = solve(mP, "普朗克质量黑洞")

# 密度剖面形状验证: 中心平台 vs 外区 r^-2
print("\n" + "="*72)
print("密度剖面形状 (太阳质量黑洞, 采样)")
print("="*72)
r, rho, P, Mv, cs, tau = sol_sun['r'], sol_sun['rho'], sol_sun['P'], sol_sun['Mv'], sol_sun['cs'], sol_sun['tau']
for frac in [0.001, 0.01, 0.1, 0.5, 1.0]:
    i = int(frac*(len(r)-1))
    print(f"  r={frac:.3f} r_h: ρ={rho[i]:.3e} kg/m³ ({rho[i]/rhoP:.2e} ρ_P), P={P[i]:.2e} Pa, c_s={cs[i]/c:.4f} c, M(r)/M={Mv[i]/Mv[-1]:.4f}")

# 光学深度汇总
print("\n" + "="*72)
print("辐射传输汇总 (光学深度 τ, 透射率 T)")
print("="*72)
for name, s in [("太阳", sol_sun), ("Sgr A*", sol_sgr), ("M87*", sol_m87), ("原初10^11", sol_pbh), ("普朗克", sol_planck)]:
    t = s['tau']; print(f"  {name}: τ={t:.3e}, T={np.exp(-t):.3e}, ρ_c={s['rho_c']/rhoP:.2e} ρ_P")
