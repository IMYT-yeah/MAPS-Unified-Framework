# -*- coding: utf-8 -*-
"""
EMRI 完整波形模板 (后续工作④) — Fisher 矩阵精度分析
构建: 框架度规下椭圆 EMRI 的绝热演化波形 + LISA 噪声 + Fisher 矩阵
  · 轨道: Peters-Mathews 绝热演化 (a(t), e(t)), quadrupole 辐射
  · 波形: 主导谐波 h(t) = h0·cos(2λ(t) + 2ω_peri(t) + φ0)
  · 框架修正: 近日点进动 ω_peri 含 (1+δ) 因子, δ=0.30·x_p (2PN g_rr 33% 分叉)
  · LISA 噪声: Barack-Cutler 2004 解析拟合 S_n(f)
  · Fisher: 参数 {δ, lnM, lnμ, a0, e0, φ0, lnD} ⟹ σ_δ (框架进动差测量精度)
  · 模型选择: GR(δ=0) vs 框架(δ_true) 的可区分性
"""
import numpy as np

G = 6.674e-11
c = 2.998e8
c2 = c*c
c5 = c**5
MSUN = 1.989e30
YEAR = 3.156e7
PC = 3.086e16
GPC = PC*1e9

# ---------- LISA 噪声 (Barack-Cutler 2004) ----------
def Sn(f):
    """功率谱密度 [Hz^-1], f in Hz"""
    f = np.abs(f)
    return 9.18e-52*f**-4 + 1.59e-41 + 9.18e-38*f**2

# ---------- Peters-Mathews 绝热演化 ----------
def evolve_pm(M, mu, a0, e0, T_obs, n=4000):
    """返回时间序列 t, a, e, λ(平均经度), ω_peri(进动角), 瞬时 GW 频率"""
    Mtot = M+mu
    t = np.linspace(0, T_obs, n)
    a = np.empty(n); e = np.empty(n); lam = np.empty(n); wperi = np.empty(n)
    a[0], e[0] = a0, e0
    lam[0], wperi[0] = 0.0, 0.0
    beta = (64.0/5)*(G**3*M*mu*Mtot)/c5
    for i in range(n-1):
        dt = t[i+1]-t[i]
        f1 = (1+(73.0/24)*e[i]**2+(37.0/96)*e[i]**4)/(1-e[i]**2)**3.5
        g1 = (1+(121.0/304)*e[i]**2)/(1-e[i]**2)**2.5
        da = -beta/a[i]**3*f1
        de = -(304.0/15)*(G**3*M*mu*Mtot)/c5/a[i]**4*e[i]*g1
        a[i+1] = max(a[i]+da*dt, 0.0)
        e[i+1] = max(e[i]+de*dt, 0.0)
        w_orb = np.sqrt(G*M/a[i]**3)
        # 每圈进动 (GR 1PN + 2PN 修正近似)
        p = a[i]*(1-e[i]**2)
        xp = G*M/(c2*p)
        dw_peri_GR = 6*np.pi*xp*(1 + 0.5*3.0*xp/(1-e[i]**2))   # 1PN+2PN
        T_orb = 2*np.pi/w_orb
        lam[i+1] = lam[i] + w_orb*dt
        wperi[i+1] = wperi[i] + dw_peri_GR*(dt/T_orb)
    f_gw = 2*np.sqrt(G*M/a**3)/(2*np.pi)   # 主导谐波频率 f=2f_orb
    return t, a, e, lam, wperi, f_gw

# ---------- 波形 ----------
def waveform(t, a, e, lam, wperi, M, mu, D, delta, phi0):
    """h(t) = h0(a,e)·cos(2λ + 2(1+δ)ω_peri + φ0)   (进动差 δ 注入)"""
    Mtot = M+mu
    # quadrupole 振幅 (椭圆轨道近似, 主导谐波)
    p = a*(1-e*e)
    x_a = G*M/(c2*a)
    h0 = 4*(G*mu/c2)*x_a/D * (1 + 0.8*e**2)   # quadrupole 振幅 (含相对论势因子 x_a)
    Phi = 2*lam + 2*(1+delta)*wperi + phi0
    return h0*np.cos(Phi)

# ---------- Fisher 矩阵 ----------
def fisher_matrix(t, a, e, lam, wperi, f_gw, h, M, mu, D, delta, phi0, params):
    """噪声加权内积 Γ_ij = 4∫ (∂ᵢh)(∂ⱼh)/S_n(f) dt (窄带近似)"""
    k = len(params)
    dhdth = np.zeros((k, len(t)))
    Mtot = M+mu
    # 参数: [delta, lnM, lnmu, a0, e0, phi0, lnD]
    # h = h0 cosΦ;  ∂h/∂p = (∂h0/∂p)cosΦ - h0 sinΦ (∂Φ/∂p)
    p = a*(1-e*e); xp = G*M/(c2*p); x_a = G*M/(c2*a)
    h0 = 4*(G*mu/c2)*x_a/D*(1+0.8*e**2)
    Phi = 2*lam + 2*(1+delta)*wperi + phi0
    cosP, sinP = np.cos(Phi), np.sin(Phi)
    # ∂Φ/∂δ = 2·ω_peri
    dPhi_dd = 2*wperi
    # ∂Φ/∂lnM ~ 2λ 对 M 的导数 (轨道频率 √(GM/a³): ∂λ/∂lnM ~ 0.5λ) + 进动项
    dPhi_dlnM = lam + 2*(1+delta)*wperi*1.0   # 进动 ∝ xp ∝ M
    dPhi_dlnmu = 0.0                           # μ 不直接进相位 (quadrupole)
    dPhi_da0 = 0.0; dPhi_de0 = 0.0             # 初值经演化隐式含入 (简化: 只留直接依赖)
    dPhi_dphi0 = 1.0
    # 振幅对数导数
    dlnh0_dlnM = 1.0; dlnh0_dlnmu = 1.0; dlnh0_dlnD = -1.0
    dlnh0_de0 = 2*0.8*e/(1+0.8*e**2)*e*0 + 0.0  # 简化: 忽略 e0 直接导数
    dlnh0_da0 = 0.0
    derivs = {
        'delta': h0*sinP*dPhi_dd*(-1),
        'lnM':   h0*(cosP*dlnh0_dlnM - sinP*dPhi_dlnM),
        'lnmu':  h0*(cosP*dlnh0_dlnmu - sinP*dPhi_dlnmu),
        'a0':    h0*(cosP*dlnh0_da0 - sinP*dPhi_da0),
        'e0':    h0*(cosP*dlnh0_de0 - sinP*dPhi_de0),
        'phi0':  h0*(-sinP),
        'lnD':   h0*(cosP*dlnh0_dlnD),
    }
    for i, pname in enumerate(params):
        dhdth[i] = derivs[pname]
    # 瞬时噪声 (窄带: f 变化缓慢)
    sn = Sn(f_gw)
    Gamma = np.zeros((k, k))
    for i in range(k):
        for j in range(i, k):
            Gamma[i, j] = Gamma[j, i] = 4*np.trapezoid(dhdth[i]*dhdth[j]/sn, t)
    return Gamma

# ---------- SNR ----------
def snr(t, h, f_gw):
    return np.sqrt(4*np.trapezoid(h*h/Sn(f_gw), t))

print("="*78)
print("EMRI 完整波形模板 — Fisher 精度分析 (后续工作④)")
print("框架进动差 δ 的测量精度 + GR vs 框架模型选择")
print("="*78)

cases = [
    ("M=10⁶, μ=10, e0=0.3, a0=16.5GM/c², D=3Gpc, 2yr",
     dict(M=1e6*MSUN, mu=10*MSUN, a0=16.5*G*1e6*MSUN/c2, e0=0.3, D=3*GPC, T_obs=2*YEAR)),
    ("M=10⁶, μ=10, e0=0.3, a0=16.5GM/c², D=3Gpc, 4yr",
     dict(M=1e6*MSUN, mu=10*MSUN, a0=16.5*G*1e6*MSUN/c2, e0=0.3, D=3*GPC, T_obs=4*YEAR)),
    ("M=10⁶, μ=10, e0=0.7, a0=23GM/c², D=3Gpc, 2yr",
     dict(M=1e6*MSUN, mu=10*MSUN, a0=23*G*1e6*MSUN/c2, e0=0.7, D=3*GPC, T_obs=2*YEAR)),
    ("M=10⁶, μ=1,  e0=0.3, a0=16.5GM/c², D=1Gpc, 4yr",
     dict(M=1e6*MSUN, mu=1*MSUN, a0=16.5*G*1e6*MSUN/c2, e0=0.3, D=1*GPC, T_obs=4*YEAR)),
]
params = ['delta', 'lnM', 'lnmu', 'a0', 'e0', 'phi0', 'lnD']
for name, kw in cases:
    M, mu, D = kw['M'], kw['mu'], kw['D']
    p0 = kw['a0']*(1-kw['e0']**2)
    xp0 = G*M/(c2*p0)
    delta_true = 0.30*xp0   # 框架进动差 (B3 校准)
    t, a, e, lam, wperi, f_gw = evolve_pm(M, mu, kw['a0'], kw['e0'], kw['T_obs'])
    h = waveform(t, a, e, lam, wperi, M, mu, D, delta_true, 0.0)
    rho = snr(t, h, f_gw)
    Gam = fisher_matrix(t, a, e, lam, wperi, f_gw, h, M, mu, D, delta_true, 0.0, params)
    try:
        Cov = np.linalg.inv(Gam)
        sig = np.sqrt(np.diag(Cov))
    except np.linalg.LinAlgError:
        Cov = np.linalg.pinv(Gam); sig = np.sqrt(np.diag(Cov))
    s_delta = sig[params.index('delta')]
    s_lnM = sig[params.index('lnM')]
    # 模型选择: ΔlnL ≈ 0.5(δ_true/σ_δ)²
    dlnL = 0.5*(delta_true/s_delta)**2
    print(f"\n=== {name} ===")
    print(f"  x_p0={xp0:.4f}, δ_true={delta_true*100:.2f}%, SNR={rho:.1f}")
    print(f"  σ_δ = {s_delta:.2e}  (δ 测量精度; δ_true/σ_δ = {delta_true/s_delta:.1f}σ)")
    print(f"  σ_lnM = {s_lnM:.2e} (M 精度 {s_lnM*100:.2f}%)")
    print(f"  模型选择: ΔlnL = {dlnL:.1f} (GR 排除显著性 ~{np.sqrt(2*dlnL):.1f}σ)")
    print(f"  末态: a_f={a[-1]/(G*M/c2):.2f} GM/c², e_f={e[-1]:.3f}, f_final={f_gw[-1]*1e3:.1f} mHz")
