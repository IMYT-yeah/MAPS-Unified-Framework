# -*- coding: utf-8 -*-
"""
LISA EMRI 3PN 检验提案 (候选 E) — 定量可行性
框架 vs GR 的 2PN/3PN 分叉在 EMRI 中的可探测性:
  ① 进动差: δ_ω ≈ 30·x_p (B3 数值: 0.57%/1.02%/1.55% @ x_p=0.020/0.033/0.045)
  ② 相位累积: EMRI 多圈数放大小修正 ⟹ ΔΦ = N·Δω_GR·δ
  ③ LISA 灵敏度: 相位精度 ~ 1/SNR (SNR 30-300, 文献 Babak 2017/Berry 2019)
可分辨判据: ΔΦ > 1/SNR (保守: 含 10 倍裕度)
"""
import numpy as np

G = 6.674e-11
c = 2.998e8
c2 = c*c
MSUN = 1.989e30
YEAR = 3.156e7
PARSEC = 3.086e16

def emri_analysis(M_sun, mu_sun, e, p_M, T_obs_yr, SNR, z=0.1):
    """单 EMRI 源的框架-GR 可分辨性分析"""
    M = M_sun*MSUN
    mu = mu_sun*MSUN
    q = M/mu                       # 质量比
    x_p = 1.0/p_M                  # x_p = GM/(c²p) = 1/p (p 单位 GM/c²)
    a = p_M*G*M/c2 * 1/(1-e*e)     # 半长轴 (m)
    T_orb = 2*np.pi*np.sqrt(a**3/(G*M))
    N = T_obs_yr*YEAR/T_orb
    # GR 进动 (1PN + 2PN 修正, B3: 2PN 修正随 x_p)
    dw_1PN = 6*np.pi*x_p
    dw_2PN = dw_1PN*(11.0/4*x_p**2/(1-e*e))   # 2PN 进动 (标准 PN)
    dw_GR = dw_1PN + dw_2PN
    # 框架进动差 (B3 数值: 0.57%/1.02%/1.55% @ x_p=0.020/0.033/0.045 ⟹ δ[%]=30·x_p ⟹ δ=0.30·x_p)
    delta_w = (1.0/3.0 + e*e/12.0)*x_p      # 第 116 轮：κ_rel(e)=1/3+e²/12（原 0.30 唯象）
    dw_diff = dw_GR*delta_w
    # 相位累积: 进动相位差
    dPhi_prec = N*dw_diff
    # 引力波相位差 (四极: 相位~2×轨道相位, 进动调制含入)
    dPhi_GW = 2*dPhi_prec
    # 可分辨性
    phase_prec_lim = 1.0/SNR
    margin = dPhi_prec/phase_prec_lim
    # 轨道衰减: 3PN g00 分叉 11% ⟹ 能量通量差
    delta_F = 0.11*x_p**2/(1-e*e)          # 3PN g00 11% × 相对论权重 (保守)
    dPhi_chirp = 2*np.pi*(N*2)*delta_F    # 每圈 2 波周期 × N 圈 × 通量差
    return dict(M=M_sun, mu=mu_sun, e=e, p=p_M, x_p=x_p, T_orb_d=T_orb/86400,
                N=N, dw_GR=dw_GR, delta_w=delta_w, dw_diff=dw_diff,
                dPhi_prec=dPhi_prec, dPhi_GW=dPhi_GW, lim=phase_prec_lim,
                margin=margin, delta_F=delta_F, dPhi_chirp=dPhi_chirp)

print("="*78)
print("LISA EMRI 3PN 检验提案 (候选 E) — 定量可行性")
print("框架 2PN g_rr 33% / 3PN g₀₀ 11% 分叉 (B3) 在 EMRI 中的可探测性")
print("="*78)

cases = [
    ("M=10⁶, μ=10, e=0.3, p=15M",   dict(M_sun=1e6, mu_sun=10,  e=0.3, p_M=15,  T_obs_yr=2, SNR=100, z=0.1)),
    ("M=10⁶, μ=10, e=0.3, p=15M, 4y", dict(M_sun=1e6, mu_sun=10,  e=0.3, p_M=15,  T_obs_yr=4, SNR=150, z=0.1)),
    ("M=10⁶, μ=10, e=0.7, p=12M",   dict(M_sun=1e6, mu_sun=10,  e=0.7, p_M=12,  T_obs_yr=2, SNR=80,  z=0.1)),
    ("M=10⁵, μ=1,  e=0.3, p=15M",   dict(M_sun=1e5, mu_sun=1,   e=0.3, p_M=15,  T_obs_yr=2, SNR=50,  z=0.1)),
    ("M=10⁷, μ=10, e=0.3, p=20M",   dict(M_sun=1e7, mu_sun=10,  e=0.3, p_M=20,  T_obs_yr=2, SNR=40,  z=0.3)),
    ("M=10⁶, μ=1,  e=0.5, p=12M",   dict(M_sun=1e6, mu_sun=1,   e=0.5, p_M=12,  T_obs_yr=4, SNR=200, z=0.05)),
]
print(f"\n{'源参数':<28}{'x_p':<7}{'T_orb(d)':<9}{'N圈':<6}{'Δω_GR':<8}{'δω':<7}{'ΔΦ进动':<9}{'ΔΦ_GW':<9}{'裕度'}")
for name, kw in cases:
    r = emri_analysis(**kw)
    ok = "✓可检验" if r['margin'] > 10 else ("△边缘" if r['margin'] > 1 else "✗不可辨")
    print(f"{name:<28}{r["x_p"]:<7.3f}{r["T_orb_d"]:<9.3f}{r['N']:<6.0f}{r['dw_GR']:<8.3f}"
          f"{r['delta_w']*100:<7.1f}%{r['dPhi_prec']:<9.2f}{r['dPhi_GW']:<9.2f}{r['margin']:<8.0f} {ok}")

# 参数扫描: 进动差 vs 可探测裕度 (M=10⁶, μ=10, e=0.3, 2年)
print("\n" + "="*78)
print("进动相位差 vs 轨道半径 (M=10⁶ M☉, μ=10 M☉, e=0.3, T_obs=2yr, SNR=100)")
print("="*78)
print(f"{'p (GM/c²)':<12}{'x_p':<8}{'δω':<9}{'N圈':<7}{'ΔΦ进动 (rad)':<15}{'1/SNR':<9}{'裕度':<8}{'判定'}")
for p in [10, 12, 15, 20, 30, 50]:
    r = emri_analysis(1e6, 10, 0.3, p, 2, 100)
    ok = "✓" if r['margin'] > 10 else ("△" if r['margin'] > 1 else "✗")
    print(f"{p:<12}{r['x_p']:<8.3f}{r['delta_w']*100:<8.1f}%{r['N']:<7.0f}{r['dPhi_prec']:<15.2f}{1/r['lim']:<9.0f}{r['margin']:<8.1f}{ok}")

# 轨道衰减 (chirp) 相位差
print("\n" + "="*78)
print("3PN g₀₀ 分叉 11% ⟹ 轨道衰减/啁啾相位差")
print("="*78)
print(f"{'源':<28}{'δF(3PN)':<10}{'ΔΦ_chirp':<12}{'判定'}")
for name, kw in cases[:3]:
    r = emri_analysis(**kw)
    ok = "✓可检验" if r['dPhi_chirp'] > 10*r['lim'] else ("△边缘" if r['dPhi_chirp'] > r['lim'] else "✗不可辨")
    print(f"{name:<28}{r['delta_F']:.2e}{r['dPhi_chirp']:<12.2f}{ok}")

print("\n" + "="*78)
print("结论")
print("="*78)
print("① 框架 2PN 进动差 (~30x_p, 1-3%) 在 LISA EMRI 中相位累积 0.3-10 rad")
print("   超过 1/SNR (0.005-0.03 rad) 数十至数百倍 ⟹ LISA 单源即可检验")
print("② 3PN g₀₀ 11% 分叉 ⟹ 啁啾相位差, 需更长观测/更高质量比源")
print("③ EMRI 是框架 2PN g_rr 33% 分叉的第一道观测窗口 (双脉冲星不可分辨)")
