# -*- coding: utf-8 -*-
"""第 116 轮核验：EMRI 数字重算（E116-1 … E116-13）

数值部分**只重算 C1（2 yr）**（够判据）＋ 文档部分全查；「修复型」项一律两段式（底本 = 备份）。
"""
import io
import os
import numpy as np

BASE = r'[WORKSPACE]'
OUT = os.path.join(BASE, 'outputs')
HIST = os.path.join(BASE, 'MAPS-Unified-Framework', 'paper', 'history')
MAT = os.path.join(OUT, 'EMRI材料包_给LISA组的S-E1-E4.md')
MAT_PRE = os.path.join(OUT, 'EMRI材料包_给LISA组的S-E1-E4_备份_2026-10-04第116轮前.md')
ZH = os.path.join(OUT, '论文初稿_正反物质对风暴统一框架_v2.9.md')
EN = os.path.join(OUT, 'Paper_MatterAntimatterPairStorm_v2.9_EN.md')
ZH_PRE = os.path.join(HIST, '论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-04第116轮前.md')
LP = os.path.join(OUT, '项目台账.md')
HO = os.path.join(BASE, '环境说明.md')
PROP = os.path.join(OUT, '_emri_proposal_116.log')
MEM = os.path.join(BASE, '.workbuddy', 'memory', 'MEMORY.md')
rd = lambda p: io.open(p, encoding='utf-8').read()
n_ok = n_bad = 0


def chk(tag, cond, msg):
    global n_ok, n_bad
    if cond:
        n_ok += 1
        print('  [OK] %-9s %s' % (tag, msg))
    else:
        n_bad += 1
        print('  [XX] %-9s %s' % (tag, msg))


print('=' * 100)
print('第 116 轮核验')
print('=' * 100)

# ---------------- 数值侧（C1，同一台机器） ----------------
src = rd(os.path.join(OUT, '_emri_waveform.py'))
ns = {}
exec(src[:src.index('print("="*78)')], ns)
G, c2, MSUN, YEAR, GPC = ns['G'], ns['c2'], ns['MSUN'], ns['YEAR'], ns['GPC']
Sn, evolve_pm, waveform, fisher_matrix, snr = (ns['Sn'], ns['evolve_pm'], ns['waveform'],
                                               ns['fisher_matrix'], ns['snr'])
M, mu, D, e0, a0, T = 1e6 * MSUN, 10 * MSUN, 3 * GPC, 0.3, 16.5 * G * 1e6 * MSUN / c2, 2 * YEAR
t, a, e, lam, wperi, f_gw = evolve_pm(M, mu, a0, e0, T)
xp0 = G * M / (c2 * a0 * (1 - e0 ** 2))
KREL = 1 / 3 + e0 ** 2 / 12
d_new, d_old = KREL * xp0, 0.30 * xp0
h_new = waveform(t, a, e, lam, wperi, M, mu, D, d_new, 0.0)
h_gr = waveform(t, a, e, lam, wperi, M, mu, D, 0.0, 0.0)
rho = snr(t, h_new, f_gw)
inner = lambda x, y: 4 * np.trapezoid(x * y / Sn(f_gw), t)
dh = h_new - h_gr
dlnL = 0.5 * inner(dh, dh)
rho2 = inner(h_new, h_new)
Mmatch = 1 - dlnL / rho2
bound = 0.5 * (rho + snr(t, h_gr, f_gw)) ** 2

print('=== E116-1/2/3 数值（C1：2 yr、e₀=0.3）===')
chk('E116-1', abs(d_new - 0.0227) < 1e-6 and abs(d_new / d_old - 1.136111) < 1e-4,
    'δ_true: %.4f%%（旧 %.4f%%），κ_rel(0.3)=%.5f，比值 ×%.4f'
    % (100 * d_new, 100 * d_old, KREL, d_new / d_old))
chk('E116-2', abs(dlnL / rho2 - 1) < 0.01,
    'ΔlnL = %.1f ≈ ρ² = %.1f（差 %.2f%%）⟹ M = %.2e ⟹ 近乎正交'
    % (dlnL, rho2, 100 * abs(dlnL / rho2 - 1), Mmatch))
t4, a4, e4, lam4, wp4, f4 = evolve_pm(M, mu, a0, e0, 4 * YEAR)
h4 = waveform(t4, a4, e4, lam4, wp4, M, mu, D, d_new, 0.0)
h4g = waveform(t4, a4, e4, lam4, wp4, M, mu, D, 0.0, 0.0)
b4 = 0.5 * (snr(t4, h4, f4) + snr(t4, h4g, f4)) ** 2
chk('E116-3', 13929.7 > b4 * 10 and abs(b4 - 1132) / 1132 < 0.05,
    '4 yr 旧值 13930 vs 该档 Cauchy–Schwarz 上界 ½(ρ+ρ_GR)² = %.1f ⟹ 超 %.1f 倍（撤回依据；2 yr 上界 = %.1f）'
    % (b4, 13929.7 / b4, bound))

# 条件宽（ΔlnL=0.5 半宽）＋ 解析式
w = (4 * (G * mu / c2) * (G * M / (c2 * a)) / D * (1 + 0.8 * e ** 2)) ** 2 / Sn(f_gw)
rho2b = 2 * np.trapezoid(w, t)
lo, hi = 0.0, 1e-4
for _ in range(60):
    mid = 0.5 * (lo + hi)
    dm = abs(2 * np.trapezoid(w * np.exp(1j * (2 * mid * wperi)), t)) / rho2b
    if rho2b * (1 - dm) < 0.5:
        lo = mid
    else:
        hi = mid
half = 0.5 * (lo + hi)
H2 = (4 * (G * mu / c2) * (G * M / (c2 * a)) / D * (1 + 0.8 * e ** 2)) ** 2 / Sn(f_gw)
mean = np.trapezoid(H2 * wperi, t) / np.trapezoid(H2, t)
m2 = np.trapezoid(H2 * wperi ** 2, t) / np.trapezoid(H2, t)
var = m2 - mean ** 2
s_var = 1 / (2 * rho * np.sqrt(var))
s_m2 = 1 / (2 * rho * np.sqrt(m2))
print('=== E116-4/5 σ 三口径 ===')
chk('E116-4a', abs(half / s_var - 1) < 0.02,
    '实测似然半宽 %.3e vs 解析 1/(2ρ√Var) = %.3e（差 %.2f%%）'
    % (half, s_var, 100 * abs(half / s_var - 1)))
chk('E116-4b', abs(s_m2 / 1.23e-6 - 1) < 0.05 and abs(s_var / s_m2 - 2.06) < 0.05,
    'Fisher 1/(2ρ√⟨w²⟩) = %.2e（= 文中 1.23e-6）；σ_似然/σ_Fisher = %.2f（⟨w²⟩/Var = %.2f）'
    % (s_m2, s_var / s_m2, m2 / var))
gam = fisher_matrix(t, a, e, lam, wperi, f_gw, h_new, M, mu, D, d_new, 0.0,
                    ['delta', 'lnM', 'lnmu', 'a0', 'e0', 'phi0', 'lnD'])
cond_f = 1 / np.sqrt(gam[0, 0])
marg = np.sqrt(np.diag(np.linalg.pinv(gam))[0])
eff = d_new / np.sqrt(2 * dlnL)
chk('E116-5', cond_f < marg and abs(eff / marg - 1) < 0.6,
    '条件 %.2e < 边际 %.2e ≈ 有效 %.2e（有效/边际 = %.2f；比值 有效/条件 = %.0f）'
    % (cond_f, marg, eff, eff / marg, eff / cond_f))

# ---------------- 文档侧 ----------------
print('=== E116-6/7 材料包与论文 ===')
Mk = rd(MAT)
chk('E116-6a', '### 2.2d 【第 116 轮】' in Mk, '材料包含 §2.2d')
chk('E116-6b', '\\kappa_{rel}(e)' in Mk.replace('\\\\', '\\') or 'κ_{rel}(e)' in Mk or 'κ_rel(e)' in Mk,
    '§一 的预言式已换成 κ_rel(e)')
chk('E116-6c', '2.270%' in Mk and '881.7' in Mk and '1763.5' in Mk, '新数字落地（δ/相位）')
chk('E116-6d', '234' in Mk and '569' in Mk and '13930' in Mk and 'Cauchy' in Mk,
    'ΔlnL 新值 ＋ 13930 带撤回标记')
chk('E116-6e', '1.05×10⁻³' in Mk and '1.23×10⁻⁶' in Mk, 'σ 三口径落地')
chk('E116-6f', '1.63×10⁻⁶' in Mk and '条件宽' in Mk, '旧 σ 已被标为条件宽')
Z, E = rd(ZH), rd(EN)
chk('E116-7a', Z.count('第 116 轮：EMRI 数字重算') == 1, '论文中文含第 116 轮注')
chk('E116-7b', E.count('round 116: EMRI numbers recomputed') == 1, '论文英文含第 116 轮注')
chk('E116-7c', Z.count('√2·ρ') >= 1 and E.count('√2·ρ') >= 1, '中英都含「显著性 ≤ √2·ρ」判据')

print('=== E116-8/9 清单与交接说明 ===')
L, H = rd(LP), rd(HO)
chk('E116-8a', L.count('C-80') >= 2, '清单含 C-80（%d 处）' % L.count('C-80'))
chk('E116-8b', '**79 条**（**C-80' in L, '撤回/更正计数 78 → 79')
chk('E116-8c', L.count('第 116 轮') >= 2, '清单零表含第 116 轮行')
chk('E116-8d', 'C-7 收口' in L and 'C-74 收口' in L, '清单登记 C-7/C-74 收口')
chk('E116-9', H.count('第 116 轮后') >= 1, '交接说明 §七 含第 116 轮条目')

print('=== E116-10 相位累积复算（提案脚本）===')
P = rd(PROP)
chk('E116-10', '881.74' in P and '1763.48' in P and '776.00' not in P and '1552' not in P,
    '提案复算给 ΔΦ_prec = 881.74 / 1763.48 rad（旧的 776/1552 已不在输出中）')

print('=== E116-11/12 底本对比与符号 ===')
pre = rd(MAT_PRE)
chk('E116-11', ('0.30\\,x_p' in pre or '0.30·x_p' in pre) and '§2.2d' not in pre,
    '两段式：底本含唯象式且无 §2.2d；当前稿相反')
greek = set('αβγδεζηθικλμνξπρστυφχψωΓΔΘΛΞΠΣΦΨΩ')
i = Z.index('第 116 轮：EMRI 数字重算')
blk = Z[i:Z.index('\n\n', i)]
miss = sorted(ch for ch in set(blk) if ch in greek and ch not in rd(ZH_PRE))
chk('E116-12', not miss, '新注希腊字母 %s 全在底本中出现（新增 = %s）'
    % (sorted(ch for ch in set(blk) if ch in greek), miss or '无'))

print('=== E116-13 结构：114→115→116 三注次序 ===')
i112 = Z.index('口径注（第 112 轮')
i113 = Z.index('口径注（第 113 轮')
i115 = Z.index('口径注（第 115 轮')
i116 = Z.index('口径注（第 116 轮')
chk('E116-13', i112 < i113 < i115 < i116 and Z[i113:i115].count('\n\n') == 0
    and Z[i115:i116].count('\n\n') == 0,
    '四个注按 112→113→115→116 连续排列（各块内无空行）')
chk('E116-14', len(rd(MEM)) < 3000, 'MEMORY 仍在限额内（%d 字符）' % len(rd(MEM)))

print('')
print('通过 %d 项，失败 %d 项' % (n_ok, n_bad))
