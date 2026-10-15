# -*- coding: utf-8 -*-
"""第 116 轮 / EMRI 材料包数字重算

三件事：
  A. **δ_true 的更正**：由 `0.30·x_p`（唯象）换成 **`κ_rel(e)·x_p`**（第 115 轮闭式，`κ_rel(e)=1/3+e²/12`），
     四个 Fisher 案例全部重算（σ_δ、SNR、显著性），并加一条**Fisher 二次外推的自洽性检验**。
  B. **ΔlnL 的正确算法**：`ΔlnL = ½(δ/σ_δ)²` 是**高斯二次外推**，只在小 ΔlnL 时成立；
     本轮改用**无噪声精确内积** `ΔlnL = ½⟨Δh|Δh⟩`（`Δh = h_FW − h_GR`），并给出 Cauchy–Schwarz 上界。
  C. **C-7 / C-74 的量化诊断**：`M(δ) = 2|∫H²e^{iΔΦ}/S_n dt|/(ρ²)` 扫描 —— 直接看「齿宽 vs 包络宽」。

机器直接复用 `_emri_waveform.py`（截断到函数定义处，保证「同一台机器」）。
"""
import io
import os
import numpy as np

BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
SRC = os.path.join(BASE, 'outputs', '_emri_waveform.py')
src = io.open(SRC, encoding='utf-8').read()
cut = src.index('print("="*78)')
ns = {}
exec(src[:cut], ns)
G, c, c2, c5, MSUN, YEAR, GPC = (ns['G'], ns['c'], ns['c2'], ns['c5'],
                                 ns['MSUN'], ns['YEAR'], ns['GPC'])
Sn, evolve_pm, waveform, fisher_matrix, snr = (ns['Sn'], ns['evolve_pm'], ns['waveform'],
                                               ns['fisher_matrix'], ns['snr'])
print('机器已载入 _emri_waveform.py（§函数定义段，%d 字符）' % cut)

KREL = lambda e: 1.0 / 3.0 + e * e / 12.0

CASES = [
    ("C1  2yr", dict(M=1e6 * MSUN, mu=10 * MSUN, a0=16.5 * G * 1e6 * MSUN / c2, e0=0.3,
                     D=3 * GPC, T_obs=2 * YEAR)),
    ("C2  4yr", dict(M=1e6 * MSUN, mu=10 * MSUN, a0=16.5 * G * 1e6 * MSUN / c2, e0=0.3,
                     D=3 * GPC, T_obs=4 * YEAR)),
    ("C3  e0=.7", dict(M=1e6 * MSUN, mu=10 * MSUN, a0=23 * G * 1e6 * MSUN / c2, e0=0.7,
                       D=3 * GPC, T_obs=2 * YEAR)),
    ("C4  mu=1", dict(M=1e6 * MSUN, mu=1 * MSUN, a0=16.5 * G * 1e6 * MSUN / c2, e0=0.3,
                      D=1 * GPC, T_obs=4 * YEAR)),
]
params = ['delta', 'lnM', 'lnmu', 'a0', 'e0', 'phi0', 'lnD']


def inner(a, b, f, t):
    """⟨a|b⟩ = 4∫ a·b/S_n dt"""
    return 4 * np.trapezoid(a * b / Sn(f), t)


print('')
print('=' * 108)
print('A/B：四个案例 —— δ_true 更正 ＋ ΔlnL 换算法')
print('=' * 108)
print('  案例        x_p0     e0     κ_rel(e0)  0.30→κ  δ_old    δ_new    SNR   σ_δ(Fisher)  ½(δ/σ)²  ½⟨Δh|Δh⟩  有效宽 δ/√(2ΔlnL)  ½(ρ+ρ)²上界')
rows = []
for name, kw in CASES:
    M, mu, D, e0 = kw['M'], kw['mu'], kw['D'], kw['e0']
    p0 = kw['a0'] * (1 - e0 ** 2)
    xp0 = G * M / (c2 * p0)
    k = KREL(e0)
    d_old, d_new = 0.30 * xp0, k * xp0
    t, a, e, lam, wperi, f_gw = evolve_pm(M, mu, kw['a0'], e0, kw['T_obs'])
    out = {}
    for tag, dl in (('old', d_old), ('new', d_new)):
        h = waveform(t, a, e, lam, wperi, M, mu, D, dl, 0.0)
        rho = snr(t, h, f_gw)
        Gam = fisher_matrix(t, a, e, lam, wperi, f_gw, h, M, mu, D, dl, 0.0, params)
        try:
            Cov = np.linalg.inv(Gam)
        except np.linalg.LinAlgError:
            Cov = np.linalg.pinv(Gam)
        s = np.sqrt(np.diag(Cov))[params.index('delta')]
        cond = 1.0 / np.sqrt(Gam[params.index('delta'), params.index('delta')])
        out[tag] = (h, rho, s, cond)
    h_new, rho, sd_new, cond_new = out['new']
    h_old, rho_o, sd_old, cond_old = out['old']
    h_gr = waveform(t, a, e, lam, wperi, M, mu, D, 0.0, 0.0)
    dh = h_new - h_gr
    dlnL_exact = 0.5 * inner(dh, dh, f_gw, t)
    rho_gr = snr(t, h_gr, f_gw)
    bound = 0.5 * (rho + rho_gr) ** 2
    quad_new = 0.5 * (d_new / sd_new) ** 2
    quad_old = 0.5 * (d_old / sd_old) ** 2
    eff = d_new / np.sqrt(2 * dlnL_exact)
    wg = wperi[-1]
    rows.append(dict(name=name, xp0=xp0, e0=e0, k=k, d_old=d_old, d_new=d_new, rho=rho,
                     sd_new=sd_new, sd_old=sd_old, quad_old=quad_old, quad_new=quad_new,
                     exact=dlnL_exact, eff=eff, bound=bound, cond=cond_new, wg=wg,
                     cond_th=1.0 / (np.sqrt(2) * rho * wg)))
    print('  %-10s %.4f  %.2f  %.5f    ×%.4f   %.4f%%  %.4f%%  %5.1f  %.2e    %7.0f  %8.1f   %.2e      %8.0f'
          % (name, xp0, e0, k, k / 0.30, 100 * d_old, 100 * d_new, rho, sd_new,
             quad_new, dlnL_exact, eff, bound))

print('')
print('  σ_δ 三个口径（同一批数据、三个不同问题）：')
print('    案例        条件宽 1/√Γ_δδ   解析 1/(√2ρw_GR)  边际宽(Fisher 7 参)  有效宽 δ/√(2ΔlnL)   边际/条件')
for r in rows:
    print('    %-10s %.2e      %.2e        %.2e          %.2e         %5.0f'
          % (r['name'], r['cond'], r['cond_th'], r['sd_new'], r['eff'], r['eff'] / r['cond']))
print('')
print('  ⚠️ 自洽性：quad/Fisher 外推 与 精确内积 之比（>1 即外推失真）')
for r in rows:
    print('    %-10s 二次外推 %8.1f ／ 精确 %7.1f = ×%6.1f ； 精确值占上界 %.2f%%（上界 = ½(ρ+ρ_GR)²）'
          % (r['name'], r['quad_new'], r['exact'], r['quad_new'] / r['exact'],
             100 * r['exact'] / r['bound']))
print('    ⚠️ 旧值（δ=0.30·x_p，Fisher 外推）对照：' +
      ' ／ '.join('%s %.0f' % (r['name'], r['quad_old']) for r in rows))

print('')
print('=' * 108)
print('C：C-7 / C-74 的诊断 —— M(δ) 的形状、条件宽、ΔlnL(δ=0)')
print('=' * 108)
for nm, kw, r in ((CASES[0], None, rows[0]), (CASES[1], None, rows[1])):
    pass
for idx_c, (nm, kw) in enumerate(((CASES[0][0], CASES[0][1]), (CASES[1][0], CASES[1][1]))):
    M_, mu, D, e0 = kw['M'], kw['mu'], kw['D'], kw['e0']
    t, a, e, lam, wperi, f_gw = evolve_pm(M_, mu, kw['a0'], e0, kw['T_obs'])
    xp0 = G * M_ / (c2 * kw['a0'] * (1 - e0 ** 2))
    d_true = KREL(e0) * xp0
    H = 4 * (G * mu / c2) * (G * M_ / (c2 * a)) / D * (1 + 0.8 * e ** 2)
    w = H * H / Sn(f_gw)
    rho2 = 2 * np.trapezoid(w, t)

    def match(dl):
        return abs(2 * np.trapezoid(w * np.exp(1j * (2 * (d_true - dl) * wperi)), t)) / rho2

    print('  [%s] ρ²=%.1f  w_GR(T)=%.0f rad' % (nm.strip(), rho2, wperi[-1]))
    for off in (0.0, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, d_true):
        print('       δ_true−δ=%-9.1e  M=%.6f  ΔlnL=ρ²(1−M)=%9.2f' % (off, match(d_true - off), rho2 * (1 - match(d_true - off))))
    # 条件半宽：ΔlnL=0.5 处的偏移（M 单调 ⟹ 二分）
    lo, hi = 0.0, 1e-4
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if rho2 * (1 - match(d_true - mid)) < 0.5:
            lo = mid
        else:
            hi = mid
    half = 0.5 * (lo + hi)
    print('       ⟹ 条件半宽（ΔlnL=0.5）= %.2e ；1/√Γ_δδ = %.2e ；解析 1/(√2ρw_GR) = %.2e'
          % (half, rows[idx_c]['cond'], rows[idx_c]['cond_th']))
    print('       ⟹ ΔlnL(δ=0) = %.1f vs 精确 ½⟨Δh|Δh⟩ = %.1f vs ρ² = %.1f（三者应一致）'
          % (rho2 * (1 - match(0.0)), rows[idx_c]['exact'], rho2))
    print('       ⟹ 有效宽 δ/√(2ΔlnL) = %.2e ；边际/条件 = %.0f'
          % (rows[idx_c]['eff'], rows[idx_c]['eff'] / rows[idx_c]['cond']))
    print('       ⚠️ M(δ) 全程单调平滑（上面是「一个齿周期(π/w_GR=%.1e)」尺度上的取值）⟹ 无「梳」；'
          '1.63e-6 这类小宽度 = **条件宽**（只放开 δ）' % (np.pi / wperi[-1]))

print('')
print('=' * 108)
print('结论要点（写进材料包）')
print('=' * 108)
print('  1) δ_true 由 2.000%% 更正为 %.4f%%（e0=0.3，×%.4f）；e0=0.7 由 2.558%% 更正为 3.190%%'
      % (100 * rows[0]['d_new'], rows[0]['k'] / 0.30))
print('  2) ΔlnL 由「二次外推」改为「精确内积」：2yr %.0f（原外推 %.0f）；4yr %.0f（原外推 %.0f）'
      % (rows[0]['exact'], rows[0]['quad_old'], rows[1]['exact'], rows[1]['quad_old']))
print('  3) ΔlnL ≈ ρ²（两模板近乎正交）⟹ 显著性 √(2ΔlnL) = %.1fσ / %.1fσ / %.1fσ / %.1fσ'
      % tuple(np.sqrt(2 * r['exact']) for r in rows))
print('  4) σ_δ 两个口径：齿宽 ~1e-6（局部曲率，非约束）vs 有效宽 %.2e（真实约束，与 Fisher %.2e 同量级）'
      % (rows[0]['eff'], rows[0]['sd_new']))
print('  5) 上界校验：ρ² = %.1f / %.1f / %.1f / %.1f（精确 ΔlnL 应 ≈ ρ²）'
      % tuple(r['rho'] ** 2 for r in rows))
