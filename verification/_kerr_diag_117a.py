# -*- coding: utf-8 -*-
"""第 117 轮诊断 a：核验第 116 轮的「条件半宽」到底等于谁 ——
exact ΔlnL(Δδ) = ½⟨Δh|Δh⟩ = 2∫(Δh)²/S_n dt（直接内积）
vs ρ²(1−M)（M = |2∫w e^{i2Δδω}|/ρ²）
"""
import io, os, numpy as np
BASE = r'[WORKSPACE]'
src = io.open(os.path.join(BASE, 'outputs', '_emri_waveform.py'), encoding='utf-8').read()
ns = {}
exec(src[:src.index('print("="*78)')], ns)
G, c2, MSUN, YEAR, GPC = ns['G'], ns['c2'], ns['MSUN'], ns['YEAR'], ns['GPC']
Sn, evolve_pm, waveform, snr = ns['Sn'], ns['evolve_pm'], ns['waveform'], ns['snr']

KREL = lambda e: 1.0 / 3.0 + e * e / 12.0
# C1 case (与第 116 轮一致)
M, mu, D, e0 = 1e6 * MSUN, 10 * MSUN, 3 * GPC, 0.3
a0 = 16.5 * G * 1e6 * MSUN / c2
T_obs = 2 * YEAR
t, a, e, lam, wperi, f_gw = evolve_pm(M, mu, a0, e0, T_obs)
xp0 = G * M / (c2 * a0 * (1 - e0 ** 2))
d_true = KREL(e0) * xp0
print('C1: xp0=%.5f kappa=%.5f d_true=%.6f  w_GR(T)=%.0f' % (xp0, KREL(e0), d_true, wperi[-1]))

h_true = waveform(t, a, e, lam, wperi, M, mu, D, d_true, 0.0)
rho = snr(t, h_true, f_gw)
H = 4 * (G * mu / c2) * (G * M / (c2 * a)) / D * (1 + 0.8 * e ** 2)
wgt = H * H / Sn(f_gw)                  # 权重 H²/S_n
rho2 = 2 * np.trapezoid(wgt, t)
print('rho=%.4f rho2=%.2f' % (rho, rho2))

def exact_dlnL(dlt):
    h2 = waveform(t, a, e, lam, wperi, M, mu, D, d_true - dlt, 0.0)
    return 0.5 * 4 * np.trapezoid((h_true - h2) ** 2 / Sn(f_gw), t)

def Mst(dlt):
    return abs(2 * np.trapezoid(wgt * np.exp(1j * (2 * dlt * wperi)), t)) / rho2

print('')
print('  Δδ         ΔlnL_exact    ρ²(1−M)    比值    (exact/quad_<w2>)')
m1 = np.trapezoid(wgt * wperi, t) / np.trapezoid(wgt, t)
m2 = np.trapezoid(wgt * wperi ** 2, t) / np.trapezoid(wgt, t)
var = m2 - m1 ** 2
quad_w2 = 2 * rho2 * m2     # 精确式的二次系数
quad_var = 2 * rho2 * var   # M 式的二次系数
print('  权重矩: <w>=%.1f  <w^2>=%.4e  Var=%.4e  <w^2>/Var=%.2f' % (m1, m2, var, m2 / var))
for dlt in (1e-7, 1e-6, 3e-6, 1e-5, 1e-4, 1e-3):
    ex = exact_dlnL(dlt)
    mm = rho2 * (1 - Mst(dlt))
    print('  %-9.1e  %9.4f   %9.4f  %6.2f    %8.2f' %
          (dlt, ex, mm, ex / mm if mm > 0 else np.nan, ex / (quad_w2 * dlt ** 2)))

# 精确半宽（exact 曲线上找 ΔlnL=0.5）+ M 曲线半宽
def half(f):
    lo, hi = 0.0, 1e-4
    for _ in range(90):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0.5: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

s_ex = half(exact_dlnL); s_M = half(lambda d: rho2 * (1 - Mst(d)))
print('')
print('  ⟹ exact 曲线半宽 = %.3e （预测 1/(2ρ√<w²>) = %.3e）' % (s_ex, 1 / (2 * rho * np.sqrt(m2))))
print('  ⟹ M 曲线半宽     = %.3e （预测 1/(2ρ√Var)  = %.3e）' % (s_M, 1 / (2 * rho * np.sqrt(var))))
print('  ⟹ Fisher 1/√Γ_δδ = %.3e' % (1 / (2 * rho * np.sqrt(m2))))
