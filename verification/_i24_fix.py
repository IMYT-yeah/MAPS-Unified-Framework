# -*- coding: utf-8 -*-
"""I-24 决定性复核：Γ(eps) 的 eps→y 换式必须让 GR 复现 (1-6y)^{-1/2}"""
import sympy as sp

r, r0 = sp.symbols('r r0', positive=True)
eps, y = sp.symbols('eps y', positive=True)
N = 12


def get(tag):
    x = 1 / r
    if tag == 'GR':
        return ((1 - x / 2) / (1 + x / 2)) ** 2, (1 + x / 2) ** 4
    return sp.exp(-2 * x), sp.exp(2 * x)


def gamma_eps(tag, order=9):
    f, h = get(tag)
    fs = sp.series(f, r, sp.oo, N).removeO()
    hs = sp.series(h, r, sp.oo, N).removeO()
    bs = sp.series(r ** 2 * h, r, sp.oo, N).removeO()
    E2, L2 = sp.symbols('E2 L2', positive=True)
    V = E2 / fs - 1 - L2 / bs
    sol = sp.solve([V.subs(r, r0), sp.diff(V, r).subs(r, r0)], [E2, L2], dict=True)[0]
    phi2 = sp.series((sol[L2] / bs.subs(r, r0) ** 2).subs(r0, 1 / eps), eps, 0, order).removeO()
    V2 = sp.diff(V, r, 2).subs({E2: sol[E2], L2: sol[L2]})
    omr2 = sp.series((-V2.subs(r, r0) / (2 * hs.subs(r, r0))).subs(r0, 1 / eps), eps, 0, order).removeO()
    G = sp.series(sp.sqrt(phi2 / omr2), eps, 0, order).removeO()
    # y(eps) = 1/R = eps/sqrt(h)
    yeps = sp.series((1 / (sp.sqrt(hs) / eps * 0 + 1)) * eps / sp.sqrt(hs), eps, 0, order).removeO()
    yeps = sp.series(eps / sp.sqrt(hs), eps, 0, order).removeO()
    return G, yeps


def to_y(G, yeps, order=6):
    # 解 eps = y*(1 + b1 y + ... b_{order-2} y^{order-2})，未知数 n，方程 n
    n = order - 2
    b = sp.symbols('b1:%d' % (n + 1))
    eser = y * (1 + sum(b[i - 1] * y ** i for i in range(1, n + 1)))
    resid = sp.series(yeps.subs(eps, eser) - y, y, 0, n + 1).removeO()
    eqs = [sp.expand(resid).coeff(y, k) for k in range(1, n + 1)]
    sol = sp.solve(eqs, b, dict=True)[0]
    eps_y = sp.series(eser.subs(sol), y, 0, n + 1).removeO()
    return sp.series(G.subs(eps, eps_y), y, 0, 4).removeO(), eps_y


print("换式 eps(y)：")
for tag in ('GR', 'FW'):
    G, yeps = gamma_eps(tag)
    Gy, ey = to_y(G, yeps)
    print("  [" + tag + "] eps = " + str(sp.series(ey, y, 0, 4)))
    print("       Γ-1 = " + str(sp.simplify(Gy - 1)))
print("")
print("GR 闭式 (1-6y)^{-1/2}-1 = " + str(sp.series((1 - 6 * y) ** sp.Rational(-1, 2) - 1, y, 0, 4)))
