# -*- coding: utf-8 -*-
"""第 117 轮诊断 b：验证「2.54e-6 = φ0 剖面宽」这个解释。
对噪音-free 数据，直接数值求 max_φ0 lnL(δ, φ0)，看半宽是否 = 2.54e-6（=1/(2ρ√Var)），
以及 lnL(δ, φ0_true) 的半宽 = 1.23e-6（=1/(2ρ√<w²>) = Fisher）。
"""
import io, os, numpy as np
BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
src = io.open(os.path.join(BASE, 'outputs', '_emri_waveform.py'), encoding='utf-8').read()
ns = {}
exec(src[:src.index('print("="*78)')], ns)
G, c2, MSUN, YEAR, GPC = ns['G'], ns['c2'], ns['MSUN'], ns['YEAR'], ns['GPC']
Sn, evolve_pm, waveform, snr = ns['Sn'], ns['evolve_pm'], ns['waveform'], ns['snr']

KREL = lambda e: 1.0 / 3.0 + e * e / 12.0
M, mu, D, e0 = 1e6 * MSUN, 10 * MSUN, 3 * GPC, 0.3
a0 = 16.5 * G * 1e6 * MSUN / c2
T_obs = 2 * YEAR
t, a, e, lam, wperi, f_gw = evolve_pm(M, mu, a0, e0, T_obs)
xp0 = G * M / (c2 * a0 * (1 - e0 ** 2))
d_true = KREL(e0) * xp0
sub = np.arange(0, len(t), 3)   # 抽稀以加速相位扫描
d_true_v = d_true
print('C1: d_true=%.6f  w(T)=%.0f  抽稀 %d/%d' % (d_true, wperi[-1], len(sub), len(t)))

def ll_free(dlt, phi0):
    """噪音-free 似然：-0.5*4∫(h_true - h(δ,φ0))²/S_n dt  ⟹ 用 2∫ 省一半"""
    h2 = waveform(t, a, e, lam, wperi, M, mu, D, d_true - dlt, phi0)
    h1 = waveform(t, a, e, lam, wperi, M, mu, D, d_true, 0.0)
    return -0.5 * 4 * np.trapezoid((h1 - h2) ** 2 / Sn(f_gw), t)

def half(f, lo=0.0, hi=1e-4):
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0.5: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

# ① φ0 固定 = 0 的似然半宽（= 条件宽）
s_cond = half(lambda d: -ll_free(d, 0.0))
# ② φ0 剖面：对每个 δ 扫 φ0 取最大
phig = np.linspace(-np.pi, np.pi, 721)
def ll_prof(dlt):
    v = [ll_free(dlt, p) for p in phig]
    return -max(v)     # 深度 = min_φ0 ΔlnL = -max_φ0 lnL
s_prof = half(ll_prof)
# ③ M 曲线半宽（第 116 轮的公式）
H = 4 * (G * mu / c2) * (G * M / (c2 * a)) / D * (1 + 0.8 * e ** 2)
wgt = H * H / Sn(f_gw)
rho2 = 2 * np.trapezoid(wgt, t)
def s_M():
    lo, hi = 0.0, 1e-4
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        Mv = abs(2 * np.trapezoid(wgt * np.exp(1j * (2 * mid * wperi)), t)) / rho2
        if rho2 * (1 - Mv) < 0.5: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)
sM = s_M()

m1 = np.trapezoid(wgt * wperi, t) / np.trapezoid(wgt, t)
m2 = np.trapezoid(wgt * wperi ** 2, t) / np.trapezoid(wgt, t)
var = m2 - m1 ** 2
rho = np.sqrt(rho2)
print('')
print('  φ0 固定（条件）半宽        = %.4e   （Fisher 1/(2ρ√<w²>) = %.4e）' % (s_cond, 1/(2*rho*np.sqrt(m2))))
print('  φ0 剖面（数值 max）半宽    = %.4e   （第116轮「M 曲线」半宽 = %.4e）' % (s_prof, sM))
print('  ─ 预测 1/(2ρ√Var)         = %.4e' % (1/(2*rho*np.sqrt(var))))
print('  ⟹ 比值 剖面/条件 = %.3f' % (s_prof / s_cond))
# 直接检查：数值剖面的 lnL 深度曲线 vs 公式 rho2(1-|M|)
print('')
print('  δ        lnL_cond(0)  深度   lnL_prof 深度   rho2(1−|M|)')
for dlt in (1e-6, 3e-6, 1e-5):
    print('  %-8.1e  %10.4f  %10.4f  %10.4f' %
          (dlt, -ll_free(dlt, 0.0), ll_prof(dlt), rho2 * (1 - abs(2*np.trapezoid(wgt*np.exp(1j*(2*dlt*wperi)), t))/rho2)))
