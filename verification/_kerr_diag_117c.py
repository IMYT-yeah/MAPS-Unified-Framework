# -*- coding: utf-8 -*-
"""第 117 轮旁注：a–δ 脚本自述「σ_δ(1D) = 1/(2wGR_T) ≈ 1e-5」的口径核对。
用 _emri_ad_mcmc.py 自己的机器（inspiral/loglike_prof/sigma_halfwidth）复现其 step ①。
"""
import io, os, numpy as np
BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
src = io.open(os.path.join(BASE, 'outputs', '_emri_ad_mcmc.py'), encoding='utf-8').read()
cut = src.index('print("="*80)')
ns = {}
exec(src[:cut], ns)
G, c2, c3, c5, MSUN, YEAR, GPC = (ns['G'], ns['c2'], ns['c3'], ns['c5'],
                                  ns['MSUN'], ns['YEAR'], ns['GPC'])
inspiral, loglike_prof, sigma_halfwidth = ns['inspiral'], ns['loglike_prof'], ns['sigma_halfwidth']

M = 1e6 * MSUN; mu = 10 * MSUN
r0 = 15 * G * M / c2; D0 = 3 * GPC
a_true = 0.9; dt = 400.0; rng = np.random.default_rng(7)
x_p0 = G * M / (c2 * r0)
d_true = 0.30 * x_p0
for T_obs, tag in ((2 * YEAR, '2yr'), (4 * YEAR, '4yr')):
    t, r, lam, wGR, W = inspiral(M, mu, a_true, r0, T_obs, dt)
    h0 = 4 * (G * mu / c2) * (G * M / (c2 * r[0])) / D0
    Ph_t = 2 * lam + 2 * (1 + d_true) * wGR + 2 * a_true * W
    h_true = h0 * np.cos(Ph_t + 0.3)
    sig = np.sqrt(np.trapezoid(h_true ** 2, t) / (20.0 ** 2 * dt))
    rho = np.sqrt(np.sum(h_true ** 2) / sig ** 2)
    d = h_true + rng.normal(0, sig, t.size)
    m2 = np.mean(wGR ** 2); var = m2 - np.mean(wGR) ** 2
    s_cond = 1 / (2 * rho * np.sqrt(m2)); s_prof = 1 / (2 * rho * np.sqrt(var))
    # 他们的 step ① 复现
    dg_c = np.linspace(0.02 - 0.006, 0.02 + 0.006, 201)
    ll_c = np.array([loglike_prof(d, 2 * lam + 2 * (1 + dd) * wGR + 2 * a_true * W, h0, sig)
                     for dd in dg_c])
    dc_hat = dg_c[int(np.argmax(ll_c))]
    dg_f = np.linspace(dc_hat - 5e-4, dc_hat + 5e-4, 1201)
    ll_f = np.array([loglike_prof(d, 2 * lam + 2 * (1 + dd) * wGR + 2 * a_true * W, h0, sig)
                     for dd in dg_f])
    dh1 = dg_f[int(np.argmax(ll_f))]
    s1 = sigma_halfwidth(dg_f, ll_f)
    print('[%s] wGR(T)=%.0f  ρ=%.1f' % (tag, wGR[-1], rho))
    print('     解析：条件 1/(2ρ√<ω²>) = %.3e ；剖面 1/(2ρ√Var) = %.3e' % (s_cond, s_prof))
    print('     脚本自述：1/(2wGR_T)      = %.3e' % (1 / (2 * wGR[-1])))
    print('     其 step① 复现：dc_hat=%.5f（真 %.5f）  dh1=%.5f  s1(sigma_halfwidth)=%.3e'
          % (dc_hat, d_true, dh1, s1))
    print('     针是否落在细窗内：|dc_hat−δ_t| = %.2e vs 窗半宽 5e-4 ⟹ %s'
          % (abs(dc_hat - d_true), '在' if abs(dc_hat - d_true) < 5e-4 else '不在'))
