# -*- coding: utf-8 -*-
"""D4 关键测量：框架度规 vs GR 的【相对进动超额】系数 kappa_rel
   在信号远大于求积噪声的区间（y = 7.5e-4 ~ 7.5e-3）测量，并外推 y -> 0。
   同一 (R_p, R_a) 面积半径；两度规用同一台机器。
"""
import mpmath as mp

mp.mp.dps = 40
M = mp.mpf(1)
TWOPI = 2 * mp.pi


def gr(r):
    a = (2 * r - M) / (2 * r + M)
    f = a ** 2
    df = 8 * M * a / (2 * r + M) ** 2
    h = (1 + M / (2 * r)) ** 4
    dh = -2 * M * (1 + M / (2 * r)) ** 3 / r ** 2
    rho2 = r ** 2 * h
    return f, df, h, rho2, 2 * r * h + r ** 2 * dh


def fw(r):
    f = mp.e ** (-2 * M / r)
    df = 2 * M * f / r ** 2
    h = mp.e ** (2 * M / r)
    dh = -2 * M * h / r ** 2
    rho2 = r ** 2 * h
    return f, df, h, rho2, 2 * r * h + r ** 2 * dh


def dphi(model, rp, ra):
    Ap, Bp = 1 / model(rp)[0], 1 / model(rp)[3]
    Aa, Ba = 1 / model(ra)[0], 1 / model(ra)[3]
    det = -Ap * Ba + Bp * Aa
    E2 = (Bp - Ba) / det
    L2 = (Ap - Aa) / det
    L = mp.sqrt(L2)
    dra = ra - rp

    def Wp(r):
        f_, df_, h_, rho2_, drho2_ = model(r)
        return -E2 * df_ / f_ ** 2 + L2 * drho2_ / rho2_ ** 2

    def Q(r):
        f_, df_, h_, rho2_, drho2_ = model(r)
        W = E2 / f_ - 1 - L2 / rho2_
        d1, d2 = r - rp, ra - r
        if d1 > 1e-18 and d2 > 1e-18:
            return W / (d1 * d2)
        return Wp(rp) / dra if d1 <= d2 else -Wp(ra) / dra

    def g(th):
        r = rp + dra * mp.sin(th / 2) ** 2
        f_, df_, h_, rho2_, drho2_ = model(r)
        return L * mp.sqrt(h_ / Q(r)) / rho2_

    return 2 * mp.quad(g, [0, mp.pi])


def kappa_rel(q, Rp):
    Ra = q * Rp
    rp_g = mp.findroot(lambda r: mp.sqrt(gr(r)[3]) - Rp, Rp)
    ra_g = mp.findroot(lambda r: mp.sqrt(gr(r)[3]) - Ra, Ra)
    rp_f = mp.findroot(lambda r: mp.sqrt(fw(r)[3]) - Rp, Rp)
    ra_f = mp.findroot(lambda r: mp.sqrt(fw(r)[3]) - Ra, Ra)
    ag = dphi(gr, rp_g, ra_g) - TWOPI
    af = dphi(fw, rp_f, ra_f) - TWOPI
    p = 2 * Rp * Ra / (Rp + Ra)
    y = M / p
    return y, (af / ag - 1) / y


print("q      Rp      y         kappa_rel = R/y")
rows = {}
for q in (2, 4, 10):
    rows[q] = []
    for Rp in (100, 200, 500, 1000):
        y, k = kappa_rel(mp.mpf(q), mp.mpf(Rp))
        rows[q].append((float(y), float(k)))
        print("  %-4s %-6d %.4e  %.6f" % (q, Rp, float(y), float(k)))
    print("")

print("外推 y->0（用最小两点线性外推）")
for q in rows:
    (y1, k1), (y2, k2) = rows[q][-2], rows[q][-1]
    k0 = k2 - (k2 - k1) / (y2 - y1) * y2
    print("  q=%-4s kappa_rel(0) = %.6f    1/3=0.333333   0.30" % (q, k0))
