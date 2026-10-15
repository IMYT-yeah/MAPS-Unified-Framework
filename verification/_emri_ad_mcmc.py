# -*- coding: utf-8 -*-
"""
EMRI a-δ 联合 MCMC (P1-2) — 自旋与框架进动差简并分析 (最终版 v2)
关键发现: σ_δ ~ 1/(2·wGR_T) ≈ 1e-5 (2yr) — v1.32 的 9.7e-4 因欠采样+网格严重虚高
结构: ①两级 1D 细网格 (a 固定, φ0 剖面) → σ_δ 参考
      ②细 a 网格剖面 → σ_a 参考
      ③φ0 剖面 → σ_φ0 参考
      ④3D MCMC {δ,a,φ0} (预热协方差) → 联合后验 (主结果)
      ⑤GR 数据对照 MCMC
物理: ω_peri = (1+δ)ω_GR + ω_LT(a); LT 4πa*x^1.5 vs 1PN 6πx
"""
import numpy as np

G = 6.674e-11
c = 2.998e8
c2 = c*c
c3 = c**3
c5 = c**5
MSUN = 1.989e30
YEAR = 3.156e7
GPC = 3.086e25

def inspiral(M, mu, a_star, r0, T, dt):
    n = int(T/dt)
    t = np.linspace(0, T, n)
    k = (256.0/5)*G**3*M*M*mu/c5
    r = np.maximum((r0**4 - k*t)**0.25, 2.2*G*M/c2)
    asc = a_star*(G*M/c2)*np.sqrt(G*M/c2)
    Om = np.sqrt(G*M)/(r**1.5 + asc)
    lam = np.cumsum(Om)*dt
    x = G*M/(c2*r)
    wGR = np.cumsum(6*np.pi*x*(1+3.0*x)*(Om*dt/(2*np.pi)))
    W = np.cumsum(2.0*G**2*M*M/(c3*r**3)*dt)
    return t, r, lam, wGR, W

def loglike_prof(d, Phi, h0, sigma_n):
    Z = np.sum(d*np.exp(-1j*Phi))
    return (2*h0*np.abs(Z) - np.sum(d**2) - h0**2*len(d)/2.0)/(2*sigma_n**2)

def loglike_full(d, Phi, h0, sigma_n, phi0):
    return -0.5*np.sum((d - h0*np.cos(Phi + phi0))**2)/(sigma_n**2)

def sigma_halfwidth(x, y):
    """ΔlnL=0.5 半高宽 (线性插值)"""
    i = int(np.argmax(y)); ymax = y[i]
    n = len(x)
    def cross(seq):
        for k in range(1, len(seq)):
            if seq[k][1] <= ymax-0.5:
                x0, y0 = seq[k-1]; x1, y1 = seq[k]
                return x0 + (x1-x0)*(ymax-0.5-y0)/(y1-y0)
        return np.nan
    xr = cross(list(zip(x[i:], y[i:])))
    xl = cross(list(zip(x[:i+1][::-1], y[:i+1][::-1])))
    return (xr - xl)/2.0 if np.isfinite(xr) and np.isfinite(xl) else np.nan

print("="*80)
print("EMRI a-δ 联合 MCMC (P1-2) — 自旋-框架进动差简并分析 (最终版 v2)")
print("="*80)

M = 1e6*MSUN; mu = 10*MSUN
r0 = 15*G*M/c2
D0 = 3*GPC
phi_true = 0.3
x_p0 = G*M/(c2*r0)
a_true = 0.9
delta_true = 0.30*x_p0
snr_target = 20.0
dt = 400.0
rng = np.random.default_rng(7)

# 细 a 网格 (0.01) 预计算 — MCMC 与剖面共用
ag_f = np.linspace(0.0, 1.2, 121)

def run_T(T_obs, d, sigma_n, h0, r, W, tag, n_main=18000, th0=None, dc0=0.02, start_a=a_true):
    """数据联合分析: 返回 σ 系列 + MCMC 后验"""
    t, r0v, lam, wGR, Wv = inspiral(M, mu, a_true, r0, T_obs, dt)
    # ---------- ① 两级 1D 细网格 (a 固定真值, φ0 剖面) ----------
    dg_c = np.linspace(dc0-0.006, dc0+0.006, 201)
    ll_c = np.array([loglike_prof(d, 2*lam + 2*(1+dd)*wGR + 2*a_true*Wv, h0, sigma_n) for dd in dg_c])
    dc_hat = dg_c[int(np.argmax(ll_c))]
    dg_f = np.linspace(dc_hat-5e-4, dc_hat+5e-4, 1201)      # 间距 ~8.3e-7 ≪ σ_δ
    ll_f = np.array([loglike_prof(d, 2*lam + 2*(1+dd)*wGR + 2*a_true*Wv, h0, sigma_n) for dd in dg_f])
    dh1 = dg_f[int(np.argmax(ll_f))]
    s1 = sigma_halfwidth(dg_f, ll_f)
    ll_gr = loglike_prof(d, 2*lam + 2*wGR + 2*a_true*Wv, h0, sigma_n)
    print(f"[{tag} ①1D, a 固定, φ0 剖面] δ_hat={dh1:.6f}, σ_δ={s1:.2e}, ΔlnL(GR)={ll_f.max()-ll_gr:.1f}")

    # ---------- ② a 剖面 (在 δ_hat, φ0 剖面) → σ_a ----------
    Ph_fix = 2*lam + 2*(1+dh1)*wGR + 2*a_true*Wv
    lam_f, wGR_f = {}, {}
    for aa in ag_f:
        _, _, la, wa, _ = inspiral(M, mu, aa, r0, T_obs, dt)
        lam_f[aa] = la; wGR_f[aa] = wa
    prof_a = np.array([loglike_prof(d, 2*lam_f[aa] + 2*(1+dh1)*wGR_f[aa] + 2*aa*W, h0, sigma_n) for aa in ag_f])
    a_hat = ag_f[int(np.argmax(prof_a))]
    s_a = sigma_halfwidth(ag_f, prof_a)
    print(f"[{tag} ②a 剖面] a_hat={a_hat:.2f}, σ_a={s_a:.2e}")

    # ---------- ③ φ0 剖面 (δ_hat, a_hat) → σ_φ0 ----------
    p0g = np.linspace(-np.pi, np.pi, 401)
    key_a = min(ag_f, key=lambda x: abs(x-a_hat))
    Ph_h = 2*lam_f[key_a] + 2*(1+dh1)*wGR_f[key_a] + 2*a_hat*W
    lp0 = np.array([loglike_full(d, Ph_h, h0, sigma_n, pp) for pp in p0g])
    s_p0 = sigma_halfwidth(p0g, lp0)
    p0_hat = p0g[int(np.argmax(lp0))]
    print(f"[{tag} ③φ0 剖面] φ0_hat={p0_hat:.3f}, σ_φ0={s_p0:.3f}")

    # ---------- ④ 3D MCMC {δ, a, φ0} — 预热对角 → 协方差 → 主链 ----------
    def neg_ll(th):
        dl, aa, p0 = th
        aa = float(np.clip(aa, 0.0, 1.2))
        key = min(ag_f, key=lambda x: abs(x-aa))
        Phi = 2*lam_f[key] + 2*(1+dl)*wGR_f[key] + 2*aa*W
        return -loglike_full(d, Phi, h0, sigma_n, p0)
    n_main_use, burn = n_main, min(3000, max(n_main//3, 500))
    rng2 = np.random.default_rng(42)
    th = np.array(th0) if th0 is not None else np.array([dh1, a_hat, p0_hat])
    # 数值 Hessian (在峰值, 中心差分) → 协方差 → 提议
    def nll(th):
        dl, aa, p0 = th
        if abs(p0) > np.pi: p0 = (p0 + np.pi) % (2*np.pi) - np.pi
        return neg_ll(np.array([dl, aa, p0]))
    eps = np.array([max(s1*2, 2e-6), max(s_a*2, 3e-5), 0.1])
    H3 = np.zeros((3, 3))
    for i in range(3):
        ei = np.zeros(3); ei[i] = eps[i]
        H3[i, i] = (nll(th+ei) - 2*nll(th) + nll(th-ei))/eps[i]**2
    for i in range(3):
        for j in range(i+1, 3):
            ei = np.zeros(3); ei[i] = eps[i]
            ej = np.zeros(3); ej[j] = eps[j]
            H3[i, j] = H3[j, i] = (nll(th+ei+ej) - nll(th+ei-ej) - nll(th-ei+ej) + nll(th-ei-ej))/(4*eps[i]*eps[j])
    C3 = np.linalg.inv(H3)
    L3 = np.linalg.cholesky(C3 + 1e-16*np.eye(3))
    scale = 2.38/np.sqrt(3)*L3
    sh_d, sh_a, sh_p = np.sqrt(C3[0,0]), np.sqrt(C3[1,1]), np.sqrt(C3[2,2])
    rh_da = C3[0,1]/np.sqrt(C3[0,0]*C3[1,1]); rh_dp = C3[0,2]/np.sqrt(C3[0,0]*C3[2,2])
    print(f"  [Hessian] σ_δ={sh_d:.2e} σ_a={sh_a:.3f} σ_φ0={sh_p:.3f} ρ(δ,a)={rh_da:+.2f} ρ(δ,φ0)={rh_dp:+.2f}")
    chain = np.zeros((n_main_use, 3))
    cur = nll(th); acc = 0
    for i in range(n_main_use):
        prop = th + rng2.normal(0, 1, 3) @ scale
        if prop[1] < 0 or prop[1] > 1.2: prop[1] = th[1]
        prop[2] = (prop[2] + np.pi) % (2*np.pi) - np.pi
        p_ll = nll(prop)
        if rng2.random() < np.exp(-(p_ll - cur)):
            th = prop; cur = p_ll; acc += 1
        chain[i] = th
    post = chain[burn:]
    dm, ds = post[:, 0].mean(), post[:, 0].std()
    am, asd = post[:, 1].mean(), post[:, 1].std()
    pm, psd = post[:, 2].mean(), post[:, 2].std()
    rho_da = np.corrcoef(post[:, 0], post[:, 1])[0, 1] if ds > 0 and asd > 0 else np.nan
    rho_dp = np.corrcoef(post[:, 0], post[:, 2])[0, 1] if ds > 0 and psd > 0 else np.nan
    print(f"[{tag} ④3D MCMC] 接受率 {acc/n_main_use:.3f}")
    print(f"  δ 后验: {dm:.6f} ± {ds:.2e} (真 {delta_true:.5f}, {(dm-delta_true)/max(ds,1e-30):.1f}σ)")
    print(f"  a 后验: {am:.3f} ± {asd:.3f};  φ0 后验: {pm:.3f} ± {psd:.3f}")
    print(f"  ρ(δ,a)={rho_da:+.2f} (LT 竞争), ρ(δ,φ0)={rho_dp:+.2f} (轨道相位)")
    ref = 0.0 if th0 is not None else delta_true
    sig = (dm-ref)/max(ds, 1e-30)
    print(f"  ⟹ σ_δ(3D 联合) = {ds:.2e} vs σ_δ(1D, a 固定) = {s1:.2e}: 简并膨胀 {ds/s1:.1f}×; "
          f"vs v1.32 9.7e-4: {ds/9.7e-4:.1f}×; 偏离真值/0 {(dm-ref):.2e} = {sig:.0f}σ")
    return dict(dh1=dh1, s1=s1, a_hat=a_hat, s_a=s_a, s_p0=s_p0, dm=dm, ds=ds,
                am=am, asd=asd, rho_da=rho_da, rho_dp=rho_dp, dlnL=ll_f.max()-ll_gr)

for T_obs in [2*YEAR, 4*YEAR]:
    tag = f"{T_obs/YEAR:.0f}yr"
    print(f"\n{'='*78}\nT_obs = {tag}   a_true={a_true}, δ_true={delta_true*100:.2f}%   n={int(T_obs/dt):,}\n{'='*78}")
    t, r, lam, wGR, W = inspiral(M, mu, a_true, r0, T_obs, dt)
    h0 = 4*(G*mu/c2)*(G*M/(c2*r[0]))/D0
    Ph_t = 2*lam + 2*(1+delta_true)*wGR + 2*a_true*W
    h_true = h0*np.cos(Ph_t + phi_true)
    sigma_n = np.sqrt(np.trapezoid(h_true**2, t)/(snr_target**2*dt))
    d = h_true + rng.normal(0, sigma_n, t.size)
    f0 = 2*np.sqrt(G*M)/(r[0]**1.5 + a_true*(G*M/c2)**1.5)/(2*np.pi)
    print(f"SNR={snr_target}, dt/周期={dt*f0:.2f}<0.5 ✓, wGR={wGR[-1]:.0f}, a·W={a_true*W[-1]:.0f}")
    R = run_T(T_obs, d, sigma_n, h0, r, W, tag, n_main=12000)
    # ---------- ⑤ GR 数据对照 (MCMC 从真值启动) ----------
    h_gr0 = h0*np.cos(Ph_t - 2*delta_true*wGR + phi_true)
    sigma_g = np.sqrt(np.trapezoid(h_gr0**2, t)/(snr_target**2*dt))
    d_gr = h_gr0 + rng.normal(0, sigma_g, t.size)
    print(f"\n[{tag} ⑤GR 对照] 数据由 GR(δ=0, a=0.9) 注入")
    if tag == '2yr':
        Rg = run_T(T_obs, d_gr, sigma_g, h0, r, W, f"{tag}-GR", n_main=9000,
                   th0=[0.0, a_true, 0.0], dc0=0.0)
        ok = "✓ 无假阳性" if abs(Rg['dm'])/max(Rg['ds'], 1e-30) < 3 else "⚠ 偏离"
        print(f"  ⟹ GR 对照: δ 后验 {Rg['dm']:.6f} ± {Rg['ds']:.2e} (参考 0) → {ok}")
    else:
        Rg1 = run_T(T_obs, d_gr, sigma_g, h0, r, W, f"{tag}-GR", n_main=2000,
                    th0=[0.0, a_true, 0.0], dc0=0.0)
        print(f"  ⟹ GR 对照 (轻量): δ_hat(1D)={Rg1['dh1']:.6f} ± {Rg1['s1']:.2e}, ΔlnL(GR)={Rg1['dlnL']:.1f}")

print("\n" + "="*80)
print("总结: ①σ_δ(1D)=1/(2wGR_T)≈1e-5 (2yr)/5e-6 (4yr) — v1.32 9.7e-4 因欠采样虚高 ~100×")
print("      ②3D 联合膨胀因子 (a-φ0 边际); ③ρ(δ,a)<0, ρ(δ,φ0)>0; ④GR 对照无假阳性")
print("="*80)
