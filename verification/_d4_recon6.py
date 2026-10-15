# -*- coding: utf-8 -*-
"""D4 侦查 6：改用【面积半径】定义膨胀参数 y = M/p（p = 面积半径半通径）—— 坐标无关、可标定
   标定：GR（= 史瓦西）应给 b = 27pi = 84.82300164692441
"""
import mpmath as mp

mp.mp.dps = 40
M = mp.mpf(1)
SIXPI = 6 * mp.pi
TWOPI = 2 * mp.pi


def gr(r):
    a = (2 * r - M) / (2 * r + M)
    f = a ** 2
    df = 8 * M * a / (2 * r + M) ** 2
    h = (1 + M / (2 * r)) ** 4
    dh = -2 * M * (1 + M / (2 * r)) ** 3 / r ** 2
    rho2 = r ** 2 * h
    drho2 = 2 * r * h + r ** 2 * dh
    return f, df, h, rho2, drho2


def fw(r):
    f = mp.e ** (-2 * M / r)
    df = 2 * M * f / r ** 2
    h = mp.e ** (2 * M / r)
    dh = -2 * M * h / r ** 2
    rho2 = r ** 2 * h
    drho2 = 2 * r * h + r ** 2 * dh
    return f, df, h, rho2, drho2


def areal(model, r):
    """面积半径 R = sqrt(rho2)"""
    return mp.sqrt(model(r)[3])


def iso_from_areal(model, Rp):
    return mp.findroot(lambda r: areal(model, r) - Rp, Rp)


def advance(model, rp, ra):
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
        if d1 > 1e-14 and d2 > 1e-14:
            return W / (d1 * d2)
        return Wp(rp) / dra if d1 <= d2 else -Wp(ra) / dra

    def g(th):
        r = rp + dra * mp.sin(th / 2) ** 2
        f_, df_, h_, rho2_, drho2_ = model(r)
        return L * mp.sqrt(h_ / Q(r)) / rho2_

    half = mp.quad(g, [0, mp.pi])
    return 2 * half - TWOPI


def b_of(model, q, Rp):
    Ra = q * Rp
    rp = iso_from_areal(model, Rp)
    ra = iso_from_areal(model, Ra)
    p = 2 * Rp * Ra / (Rp + Ra)          # 面积半径半通径
    y = M / p
    adv = advance(model, rp, ra)
    return y, adv, (adv / y - SIXPI) / y


if __name__ == "__main__":
    print("标定 b_GR 应 = 27pi = %.12f" % float(27 * mp.pi))
    for q in (1.5, 2, 4, 10):
        out = []
        for Rp in (2000, 10000, 50000):
            y, a, b = b_of(gr, mp.mpf(q), mp.mpf(Rp))
            out.append("y=%.3e b=%.8f" % (float(y), float(b)))
        print("   GR q=%-5s %s" % (q, " | ".join(out)))
    print("")
    print("k_rel = (b_FW-27pi)/(6pi) * A,  A=(1+q)/(2q)")
    print("q       A       k_rel@y1     k_rel@y2     k_rel@y3    -> 外推")
    for q in (1.5, 2, 4, 10, 20, 50, 100, 200, 1000):
        A = (1.0 + q) / (2.0 * q)
        vals = []
        for Rp in (2000, 10000, 50000):
            yf, af, bf = b_of(fw, mp.mpf(q), mp.mpf(Rp))
            vals.append(float((bf - 27 * mp.pi) / SIXPI) * A)
        # 线性外推 y->0：用最小的两个点
        y1, y2 = 4.0/ (2000*2/(1+q)) if False else 0, 0
        print("%-6s %.4f  %.6f   %.6f   %.6f" % (q, A, vals[0], vals[1], vals[2]))
