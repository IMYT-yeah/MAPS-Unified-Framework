# -*- coding: utf-8 -*-
"""I-24 收尾：κ_rel(e=0) 解析值 ＋ 机制分解（与 _i24_a.py 同参数，已实测可跑通）"""
import sympy as sp

r, r0 = sp.symbols('r r0', positive=True)
eps = sp.symbols('eps', positive=True)
y = sp.symbols('y', positive=True)
N = 10


def get(tag, r_):
    x = 1 / r_
    if tag == 'GR':
        return ((1 - x / 2) / (1 + x / 2)) ** 2, (1 + x / 2) ** 4
    return sp.exp(-2 * x), sp.exp(2 * x)


def ser_eps(expr, n=N):
    return sp.series(sp.simplify(expr).subs(r0, 1 / eps), eps, 0, n).removeO()


def run(tagf, tagh):
    f, _ = get(tagf, r)
    _, h = get(tagh, r)
    fs = sp.series(f, r, sp.oo, N + 2).removeO()
    hs = sp.series(h, r, sp.oo, N + 2).removeO()
    bs = sp.series(r ** 2 * h, r, sp.oo, N + 2).removeO()
    E2, L2 = sp.symbols('E2 L2', positive=True)
    V = E2 / fs - 1 - L2 / bs
    sol = sp.solve([V.subs(r, r0), sp.diff(V, r).subs(r, r0)], [E2, L2], dict=True)[0]
    phi2 = ser_eps(sol[L2] / bs.subs(r, r0) ** 2)
    V2 = sp.diff(V, r, 2).subs({E2: sol[E2], L2: sol[L2]})
    omr2 = ser_eps(-V2.subs(r, r0) / (2 * hs.subs(r, r0)))
    G = sp.series(sp.sqrt(sp.series(phi2 / omr2, eps, 0, N).removeO()), eps, 0, N).removeO()
    yy = ser_eps(1 / (r0 * sp.sqrt(hs)))
    a = sp.symbols('a1:7')
    eser = y * (1 + sum(a[i - 1] * y ** i for i in range(1, 7)))
    resid = sp.series(yy.subs(eps, eser) - y, y, 0, 8).removeO()
    eqs = [sp.expand(resid).coeff(y, k) for k in range(1, 8)]
    sols = sp.solve(eqs, a, dict=True)[0]
    eps_y = sp.series(eser.subs(sols), y, 0, 8).removeO()
    return sp.series(G.subs(eps, eps_y), y, 0, 5).removeO()



for combo in (("GR","FW"),("FW","GR")):
    G = run(*combo)
    c1 = sp.nsimplify(sp.expand(G).coeff(y, 1)); c2 = sp.nsimplify(sp.expand(G).coeff(y, 2))
    print(combo, c1, c2, flush=True)
