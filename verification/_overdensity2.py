# -*- coding: utf-8 -*-
"""
过载区径向密度分布与辐射传输 (遗留②③) — 均匀模型
核心论证:
  ① 等温球 (线性区 P≈c²ρ 静水平衡): ρ(r)=c²/(2πGr²), M(r)=2c²r/G
     ⟹ M(r_h)=4M 恒定超重 (奇异等温球无标度自相似) ⟹ 与总质量守恒矛盾
  ② 框架机制: 视界=通量=0 等势面, 内部风暴压制 (七环环1) ⟹ 内部无净通量梯度
     ⟹ 无引力梯度 (引力=通量遮挡) ⟹ dP/dr=0 ⟹ P=常数 ⟹ ρ=常数 (钳制物态单调)
  ③ 均匀密度: ρ̄ = M/(4πr_h³/3) = 3c⁶/(32πG³M²) (总质量+体积锁定, 唯一自洽解)
辐射传输: τ = (ρ̄/m_P)·l_P²·r_h (碎片散射截面~l_P²), 透射率 T=e^{-τ}
"""
import numpy as np

G = 6.674e-11
c = 2.998e8
hbar = 1.055e-34
lP = 1.616e-35
mP = 2.176e-8
rhoP = mP/lP**3
PP = c**7/(hbar*G**2)
c2 = c*c

def analyze(M, label):
    r_h = 2*G*M/c2
    rho_avg = 3*c2**3/(32*np.pi*G**3*M*M)   # = M/(4πr_h³/3)
    x = rho_avg/rhoP
    P = PP*np.tanh(x)
    cs2 = c2/np.cosh(x)**2
    tau = (rho_avg/mP)*lP*lP*r_h
    T = np.exp(-tau)
    # 等温球对照
    A_iso = c2/(2*np.pi*G)
    rho_h_iso = A_iso/r_h**2
    M_iso_rh = 2*c2*r_h/G   # = 4M
    print(f"\n=== {label}: M={M:.2e} kg, r_h={r_h:.2e} m ===")
    print(f"  均匀密度 ρ̄ = {rho_avg:.3e} kg/m³ = {x:.3e} ρ_P")
    print(f"  均匀压强 P = {P:.2e} Pa = {P/PP:.3e} P_P (P≈c²ρ̄: {P/(rho_avg*c2):.4f})")
    print(f"  声速 c_s = {np.sqrt(cs2)/c:.6f} c")
    print(f"  光学深度 τ = {tau:.3e}, 透射率 T = {T:.3e}")
    print(f"  [对照] 等温球 ρ(r_h) = {rho_h_iso:.3e} kg/m³, M_iso(r_h) = {M_iso_rh:.2e} kg = {M_iso_rh/M:.1f}×M (超重!)")
    print(f"  [对照] 等温球 ρ=ρ_P 半径 r_P = {np.sqrt(A_iso/rhoP):.2e} m = {np.sqrt(A_iso/rhoP)/lP:.2f} l_P")
    return dict(rho=rho_avg, P=P, cs=np.sqrt(cs2), tau=tau, T=T, x=x)

print("="*72)
print("过载区均匀模型 + 等温球对照 (遗留②③)")
print("核心: 等温球超重 4M ⟹ 内部无引力梯度 ⟹ 均匀密度")
print("="*72)

sols = {}
for name, M in [("太阳质量", 1.989e30), ("Sgr A*", 4.3e36), ("M87*", 6.5e39),
                ("原初10^11kg", 1e11), ("原初10^13kg", 1e13), ("普朗克质量", mP)]:
    sols[name] = analyze(M, name)

print("\n" + "="*72)
print("汇总: 均匀过载区 vs v1.18 体积平均")
print("="*72)
print(f"{'对象':<12}{'ρ̄ (kg/m³)':<14}{'ρ̄/ρ_P':<12}{'P/P_P':<10}{'c_s/c':<10}{'τ':<10}{'T'}")
for name, s in sols.items():
    print(f"{name:<12}{s['rho']:<14.3e}{s['x']:<12.3e}{s['P']/PP:<10.3e}{s['cs']/c:<10.6f}{s['tau']:<10.3e}{s['T']:.3e}")

print("\n" + "="*72)
print("关键结论")
print("="*72)
print("① 等温球 (线性区静水平衡) 在 r_h 处 M(r_h)=4M 恒定超重 — 与总质量守恒矛盾")
print("   ⟹ 过载区内部无净引力梯度 (视界通量=0 压制, 七环环1) ⟹ dP/dr=0 ⟹ 均匀")
print("② 均匀密度 ρ̄ = 3c⁶/(32πG³M²) — 与 v1.18 ρ_avg 精确一致 (太阳 1.8e19 kg/m³)")
print("③ 光学深度: 宏观黑洞 τ~10⁻⁴⁰ (全透明), 普朗克质量 τ~0.06 (临界窗口)")
print("④ 过载区不吸收/不发射辐射的定量原因 = 光学透明 (碎片截面 l_P² 极小), 非仅\"无结构\"")
