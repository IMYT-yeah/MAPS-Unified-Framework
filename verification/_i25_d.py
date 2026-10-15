# -*- coding: utf-8 -*-
"""I-25 主结果（终版）：四个 f/h 组合的 S(e)，以及 kappa_rel(e) 的机制分解"""
import sys
sys.path.insert(0, r'[WORKSPACE]\outputs')
from fractions import Fraction as F
import _i25_b as M

COMBOS = [('GR', 'GR'), ('GR', 'FW'), ('FW', 'GR'), ('FW', 'FW')]
EVALS = [F(1, 3), F(1, 2), F(2, 3), F(3, 4), F(4, 5), F(5, 6), F(12, 13)]

res = {}
for c in COMBOS:
    key = c[0][:2] + '/' + c[1][:2]
    res[key] = []
    for e in EVALS:
        a1, S2, a3 = M.S_of(c, e)
        assert a1 == 3, ('1PN 系数不是 3', c, e, a1)
        res[key].append(S2)

print('=' * 92)
print('S(e) = 系数 of eps^2 in Delta_phi/(2pi) = 1 + 3 eps + S(e) eps^2 + ...  (eps = M/p_areal)')
print('=' * 92)
print('  e      ' + ''.join('%-16s' % k for k in res))
for i, e in enumerate(EVALS):
    print('  %-6s ' % e + ''.join('%-16s' % res[k][i] for k in res))

print('')
print('--- 对 E=e^2 的线性拟合： S = a0 + b E ---')
STAR = {'GR/GR': F(27, 2), 'FW/FW': F(29, 2), 'GR/FW': F(27, 2) + F(5, 4), 'FW/GR': F(27, 2) - F(1, 4)}
for k in res:
    pts = list(zip(EVALS, res[k]))
    (e1, s1), (e2, s2) = pts[0], pts[1]
    b = (s2 - s1) / (e2 ** 2 - e1 ** 2)
    a = s1 - b * e1 ** 2
    hit = all(s == a + b * e ** 2 for e, s in pts)
    print('  %-6s S = %-14s + (%-8s) e^2      全部 %d 点命中=%s   [e=0 期望 %s]'
          % (k, a, b, len(pts), hit, STAR[k]))

print('')
print('--- 机制分解（在 y^2 系数上，按 I-24 的单侧替换法）---')
print('  e       Delta_S(总)=S_FW-S_GR   h侧=GR/FW-GR/GR   f侧=FW/GR-GR/GR   h+f')
for i, e in enumerate(EVALS):
    tot = res['FW/FW'][i] - res['GR/GR'][i]
    hh = res['GR/FW'][i] - res['GR/GR'][i]
    ff = res['FW/GR'][i] - res['GR/GR'][i]
    print('  %-6s %-20s %-16s %-16s %-8s' % (e, tot, hh, ff, hh + ff))

print('')
print('--- 主结果 ---')
for i, e in enumerate(EVALS):
    dS = res['FW/FW'][i] - res['GR/GR'][i]
    kk = dS / 3
    print('  e=%-6s  Delta_S = %-10s  kappa_rel = %-12s = %.10f   [1/3+e^2/12 = %.10f]'
          % (e, dS, kk, float(kk), float(F(1, 3) + e ** 2 / 12)))
