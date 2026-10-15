# -*- coding: utf-8 -*-
"""I-25 独立数值核验：
   (a) GR 侧：测地线积分 vs 【精确椭圆积分闭式】(eccentric Schwarzschild)
   (b) 两个度规的 S(e) = lim_{y->0} (Delta_phi/(2pi) - 1 - 3y)/y^2
   (c) 与解析式 S_GR = 27/2 + 3e^2/4 , S_FW = 29/2 + e^2 对照
   (d) 与第 112 轮 kappa_rel 表对照
"""
import mpmath as mp

mp.mp.dps = 40
M = mp.mpf(1)
TWOPI = 2 * mp.pi


def mk(tag):
    if tag == 'GR':
        def f(r):
            a = (2 * r - M) / (2 * r + M)
            return a * a

        def df(r):
            a = (2 * r - M) / (2 * r + M)
            return 8 * M * a / (2 * r + M) ** 2

        def h(r):
            return (1 + M / (2 * r)) ** 4

        def dh(r):
            return -2 * M * (1 + M / (2 * r)) ** 3 / r ** 2
    else:
        def f(r):
            return mp.e ** (-2 * M / r)

        def df(r):
            return 2 * M * f(r) / r ** 2

        def h(r):
            return mp.e ** (2 * M / r)

        def dh(r):
            return -2 * M * h(r) / r ** 2
    return f, df, h, lambda r: r * r * h(r), lambda r: 2 * r * h(r) + r * r * dh(r)


MODELS = {t: mk(t) for t in ('GR', 'FW')}


def dphi(model, rp, ra):
    f, df, h, rho2, drho2 = model
    Ap, Bp = 1 / f(rp), 1 / rho2(rp)
    Aa, Ba = 1 / f(ra), 1 / rho2(ra)
    det = -Ap * Ba + Bp * Aa
    E2 = (Bp - Ba) / det
    L2 = (Ap - Aa) / det
    L = mp.sqrt(L2)
    dra = ra - rp
    Wp = lambda r: -E2 * df(r) / f(r) ** 2 + L2 * drho2(r) / rho2(r) ** 2

    def Q(r):
        W = E2 / f(r) - 1 - L2 / rho2(r)
        d1, d2 = r - rp, ra - r
        if d1 > mp.mpf('1e-30') and d2 > mp.mpf('1e-30'):
            return W / (d1 * d2)
        return Wp(rp) / dra if d1 <= d2 else -Wp(ra) / dra

    g = lambda th: (lambda r: L * mp.sqrt(h(r) / Q(r)) / rho2(r))(rp + dra * mp.sin(th / 2) ** 2)
    return 2 * mp.quad(g, [0, mp.pi])


def dphi_gr_exact(rp, ra):
    """史瓦西（面积半径）偏心轨道的【精确闭式】：4K(k)/sqrt(2M(u3-ua)), k^2=(up-ua)/(u3-ua)"""
    up, ua = 1 / rp, 1 / ra
    u3 = 1 / (2 * M) - up - ua
    k = mp.sqrt((up - ua) / (u3 - ua))
    return 4 * mp.ellipk(k ** 2) / mp.sqrt(2 * M * (u3 - ua))


def turning(tag, R):
    rho2 = MODELS[tag][3]
    return mp.findroot(lambda r: mp.sqrt(rho2(r)) - R, R)


def S_num(tag, q, Rps):
    rows = []
    for Rp in Rps:
        Rp = mp.mpf(Rp)
        Ra = q * Rp
        rp, ra = turning(tag, Rp), turning(tag, Ra)
        d = dphi(MODELS[tag], rp, ra)
        p = 2 * Rp * Ra / (Rp + Ra)
        y = M / p
        rows.append((y, (d / TWOPI - 1 - 3 * y) / y ** 2))
    return rows


def extrap(rows):
    """拟合 S(y) = S0 + a1 y + a2 y^2 （最后三点），返回 S0 与残差"""
    pts = rows[-3:]
    A = mp.matrix([[1, y, y ** 2] for y, _ in pts])
    b = mp.matrix([s for _, s in pts])
    sol = mp.lu_solve(A, b)
    res = max(abs(s - (sol[0] + sol[1] * y + sol[2] * y ** 2)) for y, s in rows)
    return sol[0], res, sol[1]


print('=' * 88)
print('(a) GR：测地线积分 vs 精确椭圆积分闭式（偏心轨道）')
print('=' * 88)
print('  q     Rp     y          dphi(quad)             dphi(exact)          相对差')
for q in (mp.mpf(2), mp.mpf(5), mp.mpf(9)):
    for Rp in (mp.mpf(100), mp.mpf(1000)):
        Ra = q * Rp
        rp, ra = turning('GR', Rp), turning('GR', Ra)
        dq = dphi(MODELS['GR'], rp, ra)
        de = dphi_gr_exact(rp, ra)
        print('  %-4s %-6s %.3e  %.20f  %.20f  %.2e'
              % (q, Rp, 1 / (2 * Rp * Ra / (Rp + Ra)), dq, de, dq / de - 1))

print('')
print('=' * 88)
print('(b)(c) S(e) 的数值外推 vs 解析式')
print('=' * 88)
RP = (100, 200, 400, 800, 1600)
TAB = [(2, mp.mpf(1) / 3, mp.mpf(27) / 2 + mp.mpf(3) / 4 / 9, mp.mpf(29) / 2 + mp.mpf(1) / 9),
       (3, mp.mpf(1) / 2, mp.mpf(27) / 2 + mp.mpf(3) / 4 / 4, mp.mpf(29) / 2 + mp.mpf(1) / 4),
       (5, mp.mpf(2) / 3, mp.mpf(27) / 2 + mp.mpf(3) / 4 * mp.mpf(4) / 9, mp.mpf(29) / 2 + mp.mpf(4) / 9),
       (7, mp.mpf(3) / 4, mp.mpf(27) / 2 + mp.mpf(3) / 4 * mp.mpf(9) / 16, mp.mpf(29) / 2 + mp.mpf(9) / 16),
       (9, mp.mpf(4) / 5, mp.mpf(27) / 2 + mp.mpf(3) / 4 * mp.mpf(16) / 25, mp.mpf(29) / 2 + mp.mpf(16) / 25)]
print('  e       S_GR(num)          S_GR(解析)        差        S_FW(num)          S_FW(解析)        差')
for q, e, sgr_a, sfw_a in TAB:
    rgr = S_num('GR', q, RP)
    rfw = S_num('FW', q, RP)
    sgr_n, resg, _ = extrap(rgr)
    sfw_n, resf, _ = extrap(rfw)
    print('  %-6.4f  %-18.10f %-18.10f %-8.1e %-18.10f %-18.10f %-8.1e'
          % (float(e), float(sgr_n), float(sgr_a), float(sgr_n - sgr_a),
             float(sfw_n), float(sfw_a), float(sfw_n - sfw_a)))
print('  （GR 侧残差 %.1e / FW 侧 %.1e）' % (float(resg), float(resf)))
print('')
print('=' * 88)
print('(d) kappa_rel(e) = (S_FW-S_GR)/3 与第 112 轮数值表的对照')
print('=' * 88)
D4 = {2: 0.34394, 3: 0.35547, 4: 0.36463, 5: None, 6: 0.37716, 9: 0.38985, 10: 0.39045}
print('  e        q     解析 1/3+e^2/12    数值外推        第112轮表     解析-表')
for q, e in ((mp.mpf(6), mp.mpf(5) / 7), (mp.mpf(2), mp.mpf(1) / 3), (mp.mpf(4), mp.mpf(3) / 5),
             (mp.mpf(10), mp.mpf(9) / 11), (mp.mpf(50), mp.mpf(49) / 51)):
    rgr = extrap(S_num('GR', q, RP))[0]
    rfw = extrap(S_num('FW', q, RP))[0]
    kn = (rfw - rgr) / 3
    ka = mp.mpf(1) / 3 + e ** 2 / 12
    print('  %-8.6f %-6s %-16.10f %-14.10f %-14s %s'
          % (float(e), q, float(ka), float(kn),
             ('%.5f' % D4[int(q)]) if int(q) in D4 and D4[int(q)] else '--',
             ('%+.5f' % float(ka - D4[int(q)])) if int(q) in D4 and D4[int(q)] else '--'))
