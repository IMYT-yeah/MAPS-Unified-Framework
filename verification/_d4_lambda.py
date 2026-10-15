# -*- coding: utf-8 -*-
"""D4 决定性实验：进动的 2PN 系数是否对【g_rr 的 x^2 系数】敏感？
   族：h(r) = (1 + M/2r)^4 + lam*(M/r)^2 , rho^2 = r^2 h, f 保持 GR
   lam=0 -> GR（g_rr = 1+2x+1.5x^2+...）；lam=0.5 -> g_rr = 1+2x+2x^2+...（= 框架的 2PN 值）
   两者 1PN 相同（gamma=1）⟹ 若进动 2PN 系数只由 (beta,gamma) 定，则两者进动应【完全相同】到 2PN。
"""
import mpmath as mp

mp.mp.dps = 40
M = mp.mpf(1)
TWOPI = 2 * mp.pi


def make(lam):
    def m(r):
        x = M / r
        a = (1 - x / 2) / (1 + x / 2)
        f = a ** 2
        df = 8 * M * a / (2 * r + M) ** 2
        # h = (1+x/2)^4 + lam*x^2
        h = (1 + x / 2) ** 4 + lam * x ** 2
        # dh/dr
        dh = -2 * M * (1 + x / 2) ** 3 / r ** 2 - 2 * lam * M ** 2 / r ** 3
        rho2 = r ** 2 * h
        drho2 = 2 * r * h + r ** 2 * dh
        return f, df, h, rho2, drho2
    return m


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
        if d1 > 1e-16 and d2 > 1e-16:
            return W / (d1 * d2)
        return Wp(rp) / dra if d1 <= d2 else -Wp(ra) / dra

    def g(th):
        r = rp + dra * mp.sin(th / 2) ** 2
        f_, df_, h_, rho2_, drho2_ = model(r)
        return L * mp.sqrt(h_ / Q(r)) / rho2_

    return 2 * mp.quad(g, [0, mp.pi])


print("lam 扫描：同一 (rp,ra)（各向同性标签）下 Δφ 之差")
print("  若 2PN 系数对 lam 不敏感 => 进动 2PN 系数只由 (beta,gamma) 定")
for q in (2, 4):
    for rp in (500, 2000):
        ra = q * rp
        d0 = dphi(make(mp.mpf(0)), mp.mpf(rp), mp.mpf(ra))
        d5 = dphi(make(mp.mpf('0.5')), mp.mpf(rp), mp.mpf(ra))
        p = 2 * rp * ra / (rp + ra)
        y = mp.mpf(1) / p
        print("  q=%-2d rp=%-5d y=%.3e  Δφ_lam0-2π=%.14e  Δφ_lam.5-2π=%.14e  相对差=%.3e  (y^2=%.3e)"
              % (q, rp, float(y), float(d0 - TWOPI), float(d5 - TWOPI),
                 float((d5 - d0) / (d0 - TWOPI)), float(y ** 2)))
