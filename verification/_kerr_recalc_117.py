# -*- coding: utf-8 -*-
"""第 117 轮 / Kerr 版 EMRI 数字重算（材料包 §五 第三行的 `ΔlnL = 338`）

四件事：
  A. δ_true：0.30·x_p（唯象）→ κ_rel(0)·x_p = (1/3)·x_p（第 113 轮解析：圆轨道 κ_rel ≡ 1/3）。
  B. ΔlnL：实现值（单噪声实现）→ 「精确内积期望值」+ Cauchy–Schwarz 上界校验。
  C. σ_δ 口径：条件宽（φ0 固定）/ φ0 剖面宽 / 有效宽；并对旧 `9.65e-4` 做多种子去伪。
  D. 采样与网格的稳健性：dt/T_carrier = 23（欠采样）；针状似然（针宽 ~1e-6）vs 粗网格。
机器直接复用 `_kerr_emri_bayes.py`（截断到函数定义处）。
"""
import io
import os
import numpy as np

BASE = r'[WORKSPACE]'
src = io.open(os.path.join(BASE, 'outputs', '_kerr_emri_bayes.py'), encoding='utf-8').read()
cut = src.index('print("="*78)')
ns = {}
exec(src[:cut], ns)
G, c, c2, MSUN, YEAR, GPC = ns['G'], ns['c'], ns['c2'], ns['MSUN'], ns['YEAR'], ns['GPC']
kerr_omega, evolve_kerr, waveform, loglike = (ns['kerr_omega'], ns['evolve_kerr'],
                                              ns['waveform'], ns['loglike'])
print('机器已载入 _kerr_emri_bayes.py（函数定义段，%d 字符）' % cut)

# ---- 与旧脚本完全相同的参数 ----
M = 1e6 * MSUN; mu = 10 * MSUN
a = 0.9 * G * M / c2
r0 = 15 * G * M / c2
D0 = 3 * GPC
T_obs = 2 * YEAR
phi_true = 0.3
snr_target = 20.0
x_p0 = G * M / (c2 * r0)
d_old = 0.30 * x_p0
d_new = (1.0 / 3.0) * x_p0          # κ_rel(e=0) = 1/3（第 113 轮解析）
t, r, lam, wperi, f_gw = evolve_kerr(M, mu, a, r0, T_obs)
n = len(t)
dt = T_obs / n
f0 = 2 * kerr_omega(r0, M, a) / (2 * np.pi)
print('')
print('n=%d  dt=%.4e s  f_carrier=%.4e Hz  dt/T_carrier=%.2f  %s' %
      (n, dt, f0, dt * f0, '⚠ 欠采样' if dt * f0 > 0.5 else 'ok'))
print('x_p0=%.6f  w_peri(T)=%.0f rad  r_end/r0=%.4f' % (x_p0, wperi[-1], r[-1] / r0))
print('δ_old = 0.30·x_p = %.6f (%.3f%%)   δ_new = (1/3)·x_p = %.6f (%.3f%%)' %
      (d_old, 100 * d_old, d_new, 100 * d_new))


def make_data(dt_true, seed):
    h = waveform(t, r, lam, wperi, M, mu, a, D0, dt_true, phi_true)
    h2 = np.trapezoid(h * h, t)
    sig = np.sqrt(h2 / (snr_target ** 2 * dt))
    rng = np.random.default_rng(seed)
    d = h + rng.normal(0, sig, t.size)
    return h, sig, d


def inner(u, v, sig):
    return np.sum(u * v) / sig ** 2


def bisect_half(fn, lo=0.0, hi=1e-4, it=90):
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        if fn(mid) < 0.5:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


h_old, sig_old, dat_old = make_data(d_old, 7)
h_new, sig_new, dat_new = make_data(d_new, 7)
h_gr = waveform(t, r, lam, wperi, M, mu, a, D0, 0.0, phi_true)
rho = np.sqrt(inner(h_new, h_new, sig_new))
rho_gr = np.sqrt(inner(h_gr, h_gr, sig_new))
bound = 0.5 * (rho + rho_gr) ** 2

print('')
print('=' * 100)
print('A：δ 与 ΔlnL —— 旧口径 vs 精确内积（种子 7，与旧脚本同一噪声实现）')
print('=' * 100)
print('  ρ=%.3f（=SNR 目标 20）  ρ_GR=%.3f  Cauchy–Schwarz 上界 ½(ρ+ρ_GR)²=%.1f' % (rho, rho_gr, bound))
resA = {}
for tag, dtru, h_t, sig, dat in (('old δ=2.000%', d_old, h_old, sig_old, dat_old),
                                 ('new δ=2.222%', d_new, h_new, sig_new, dat_new)):
    Dh = h_t - h_gr
    exact = 0.5 * inner(Dh, Dh, sig)
    Mx = inner(h_t, h_gr, sig) / rho ** 2
    # 实现值：在 δ_true 邻域 ±3e-6 的细网格上找似然峰（针宽 ~1e-6）
    g = dtru + np.linspace(-3e-6, 3e-6, 601)
    lls = np.array([loglike(dat, waveform(t, r, lam, wperi, M, mu, a, D0, dd, phi_true), sig)
                    for dd in g])
    im = int(np.argmax(lls))
    ll_gr = loglike(dat, h_gr, sig)
    real = lls[im] - ll_gr
    resA[tag] = dict(exact=exact, real=real, dhat=g[im], M=Mx, dh=Dh, sig=sig, dat=dat, dtru=dtru)
    print('  [%s] 匹配度 M=%.2e  ΔlnL(精确) = %.2f（占上界 %.1f%%）  ΔlnL(实现, 细网格) = %.2f'
          % (tag, Mx, exact, 100 * exact / bound, real))
    print('        δ̂(细网格) = %.8f（真值 %.8f，偏差 %.2e）' % (g[im], dtru, g[im] - dtru))
# 旧脚本粗网格实现值（引用 _kerr_old_117.log）
print('  ⚠️ 旧脚本粗网格（400 点）在 old δ 下报：δ̂=0.02000（格点恰好=真值）、ΔlnL(实现)=338.4')
print('  ⟹ 338.4 与「精确期望 %.1f」的关系：差额 %.1f = 该噪声实现的投影项（σ≈%.0f）'
      % (resA['old δ=2.000%']['exact'], 338.4 - resA['old δ=2.000%']['exact'],
         np.sqrt(2 * resA['old δ=2.000%']['exact'])))

print('')
print('=' * 100)
print('B：σ_δ 口径（Kerr 版）—— 条件宽（φ0 固定）/ φ0 剖面宽 / 有效宽')
print('=' * 100)
w = wperi
m1 = np.mean(w)
m2 = np.mean(w ** 2)
var = m2 - m1 ** 2
s_cond_an = 1.0 / (2 * rho * np.sqrt(m2))
s_prof_an = 1.0 / (2 * rho * np.sqrt(var))
print('  ω 的矩（以 h0²/σ² 加权 = 均匀）：<ω>=%.1f  <ω²>=%.4e  Var=%.4e  <ω²>/Var=%.2f'
      % (m1, m2, var, m2 / var))


def depth_cond(dlt, dtru):
    """φ0 固定的 ΔlnL(Δδ)（噪音-free，直接内积）"""
    h2 = waveform(t, r, lam, wperi, M, mu, a, D0, dtru - dlt, phi_true)
    h1 = waveform(t, r, lam, wperi, M, mu, a, D0, dtru, phi_true)
    return 0.5 * inner(h1 - h2, h1 - h2, sig_new)


s_cond_num = bisect_half(lambda d: depth_cond(d, d_new), hi=1e-5)
# φ0 剖面：公式 depth = ρ²(1 − |ΣW e^{iθ}|/ΣW)，W = h0²/σ²（h0 常数 ⟹ 均匀）
Wt = np.ones_like(t)
def Mprof(dlt):
    return abs(np.mean(Wt * np.exp(1j * (2 * dlt * w)))) / np.mean(Wt)
s_prof_num = bisect_half(lambda d: rho ** 2 * (1 - Mprof(d)), hi=1e-4)
# 交叉校验公式：直接对 φ0 扫描取 max（3 个 δ 点）
print('  剖面曲线公式 vs 直接 φ0 扫描（抽 3 点校验）：')
for dlt in (1e-6, 3e-6, 1e-5):
    h0v = waveform(t, r, lam, wperi, M, mu, a, D0, d_new, phi_true)
    vv = []
    for p in np.linspace(-np.pi, np.pi, 181):
        hp = waveform(t, r, lam, wperi, M, mu, a, D0, d_new - dlt, p)
        vv.append(0.5 * inner(h0v - hp, h0v - hp, sig_new))
    print('    δ=%.1e : 公式 %.4f  vs 直接 max_φ0 %.4f' % (dlt, rho ** 2 * (1 - Mprof(dlt)), min(vv)))
s_eff = d_new / np.sqrt(2 * resA['new δ=2.222%']['exact'])
print('')
print('  ┌ 条件宽（φ0 固定）解析 1/(2ρ√<ω²>) = %.3e ；数值半个宽 = %.3e （差 %.1f%%）'
      % (s_cond_an, s_cond_num, 100 * abs(s_cond_num / s_cond_an - 1)))
print('  ├ φ0 剖面宽 解析 1/(2ρ√Var)       = %.3e ；数值半个宽 = %.3e （差 %.1f%%）'
      % (s_prof_an, s_prof_num, 100 * abs(s_prof_num / s_prof_an - 1)))
print('  ├ 剖面/条件 = %.3f  ⟹ 等效 δ–φ0 相关 |ρ| = %.3f' % (s_prof_num / s_cond_num,
      np.sqrt(1 - 1 / (s_prof_num / s_cond_num) ** 2)))
print('  └ 有效宽（对外引用）δ/√(2ΔlnL) = %.3e' % s_eff)

print('')
print('  ⚠️ 旧 σ_d=9.65e-4 的去伪：粗网格（400 点、±0.008 掩模、二次拟合）多种子重做')
print('     种子   δ̂(粗网格)     ΔlnL(粗)    σ_d(拟合)')
sd_list = []
dgrid = np.linspace(-0.01, 0.06, 400)
for seed in range(1, 13):
    h_s, sig_s, dat_s = make_data(d_new, seed)
    lls = np.array([loglike(dat_s, waveform(t, r, lam, wperi, M, mu, a, D0, dd, phi_true), sig_s)
                    for dd in dgrid])
    im = int(np.argmax(lls))
    msk = (dgrid > dgrid[im] - 0.008) & (dgrid < dgrid[im] + 0.008)
    cf = np.polyfit(dgrid[msk], lls[msk], 2)
    sd = np.sqrt(-1 / (2 * cf[0]))
    sd_list.append(sd)
    dl = lls[im] - loglike(dat_s, waveform(t, r, lam, wperi, M, mu, a, D0, 0.0, phi_true), sig_s)
    print('     %-5d  %+.5f      %8.1f    %.2e' % (seed, dgrid[im], dl, sd))
sd_arr = np.array(sd_list)
print('     ⟹ σ_d 散布：中位 %.2e，范围 [%.2e, %.2e]，共 %d 个种子'
      % (np.median(sd_arr), sd_arr.min(), sd_arr.max(), len(sd_arr)))
print('     ⟹ 有效宽 %.2e 作对照（同量级）；σ_d 既非条件宽也非剖面宽 —— 它是「平台+噪声」的拟合伪影'
      % s_eff)

print('')
print('=' * 100)
print('C：采样稳健性（n=3000 欠采样 vs n=30000）')
print('=' * 100)
for nn in (3000, 30000):
    t2, r2, lam2, wp2, f2 = evolve_kerr(M, mu, a, r0, T_obs, n=nn)
    h2n = waveform(t2, r2, lam2, wp2, M, mu, a, D0, d_new, phi_true)
    gr2 = waveform(t2, r2, lam2, wp2, M, mu, a, D0, 0.0, phi_true)
    sig2 = np.sqrt(np.trapezoid(h2n * h2n, t2) / (snr_target ** 2 * (T_obs / nn)))
    rho2n = np.sum(h2n * h2n) / sig2 ** 2
    ex = 0.5 * np.sum((h2n - gr2) ** 2) / sig2 ** 2
    mm2 = np.mean(wp2 ** 2); vv2 = np.mean(wp2 ** 2) - np.mean(wp2) ** 2
    print('  n=%-6d w(T)=%.0f  ρ²=%.1f  ΔlnL(精确)=%.2f  条件宽解析=%.3e  剖面宽解析=%.3e'
          % (nn, wp2[-1], rho2n, ex, 1 / (2 * np.sqrt(rho2n) * np.sqrt(mm2)),
             1 / (2 * np.sqrt(rho2n) * np.sqrt(vv2))))

print('')
print('=' * 100)
print('D：粗网格 vs 细网格（针状似然）')
print('=' * 100)
print('  旧 δ=2.000% 时 δ_t 恰好是格点（−0.01+171×0.07/399 = 0.020000）⟹ 针被「命中」；')
print('  新 δ=2.222% 时 δ_t/(步长) = 183.66 ⟹ 不在格点上。看上面 §B 的种子表：δ̂ 散布在整段区间。')
print('  细网格恢复演示（±3e-6，步长 1e-8）：')
for seed in (3, 5, 7):
    h_s, sig_s, dat_s = make_data(d_new, seed)
    g = d_new + np.linspace(-3e-6, 3e-6, 601)
    lls = np.array([loglike(dat_s, waveform(t, r, lam, wperi, M, mu, a, D0, dd, phi_true), sig_s)
                    for dd in g])
    print('     种子 %d: δ̂ = %.8f  偏差 = %+.2e' % (seed, g[int(np.argmax(lls))],
          g[int(np.argmax(lls))] - d_new))

print('')
print('=' * 100)
print('E：GR 对照（数据由 δ=0 注入）—— 无假阳性检查')
print('=' * 100)
h_gr0, sig_g, dat_g = make_data(0.0, 23)
g = np.linspace(-3e-6, 3e-6, 601)
lls = np.array([loglike(dat_g, waveform(t, r, lam, wperi, M, mu, a, D0, dd, phi_true), sig_g)
                for dd in g])
print('  δ̂ = %.3e（应含 0）；ΔlnL(δ=0 vs 最优) = %.2f (≈噪声级)' % (g[int(np.argmax(lls))],
      lls.max() - loglike(dat_g, waveform(t, r, lam, wperi, M, mu, a, D0, 0.0, phi_true), sig_g)))

print('')
print('=' * 100)
print('结论要点（写进材料包 §2.2e）')
print('=' * 100)
print('  1) δ_true: 2.000%% → %.3f%%（×(1/3)/0.30 = %.4f）' % (100 * d_new, (1 / 3) / 0.30))
print('  2) ΔlnL: 旧实现值 338.4 → 精确期望 %.1f（= ρ²(1−M)，占上界 %.1f%%）；'
      % (resA['new δ=2.222%']['exact'], 100 * resA['new δ=2.222%']['exact'] / bound))
print('     新实现值（种子 7）= %.1f；读数应报期望值 ±≈%.0f（噪声投影）'
      % (resA['new δ=2.222%']['real'], np.sqrt(2 * resA['new δ=2.222%']['exact'])))
print('  3) σ_δ：条件 %.2e ／ φ0 剖面 %.2e ／ 有效（对外）%.2e；旧 9.65e-4 = 拟合伪影' %
      (s_cond_num, s_prof_num, s_eff))
print('  4) 显著性 √(2ΔlnL) = %.1fσ' % np.sqrt(2 * resA['new δ=2.222%']['exact']))
print('  5) 网格/采样：欠采样 dt/T=%.1f 对积分类量无碍（χ 相位泛化平均）；' % (dt * f0))
print('     但针宽 ~%.1e ⟹ 粗网格会错过针（δ̂ 随机）；细网格恢复到 ~1e-7' % s_cond_num)
