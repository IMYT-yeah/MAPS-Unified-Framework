# -*- coding: utf-8 -*-
"""I-24 / Plan A：解析求 κ_rel(e=0)（近圆极限）
   方法：圆轨道上的径向/角向本轮频率之比 Γ = ω_φ/ω_r；近日点进动 = 2π(Γ-1)。
   Γ 与 κ_rel(0) 都是 y = M/R_0（面积半径）的级数 ⟹ 可解析展开。
"""
import sympy as sp

sp.init_printing(False)
r, r0 = sp.symbols('r r0', positive=True)
eps = sp.symbols('eps', positive=True)
y = sp.symbols('y', positive=True)


def mk(name):
    x = 1 / r
    if name == 'GR':
        return ((1 - x / 2) / (1 + x / 2)) ** 2, (1 + x / 2) ** 4
    return sp.exp(-2 * x), sp.exp(2 * x)


def ser_in_eps(expr, N=10):
    return sp.series(sp.simplify(expr).subs(r0, 1 / eps), eps, 0, N).removeO()


def run(name, N=10):
    f, h = mk(name)
    rho2 = r ** 2 * h
    fs = sp.series(f, r, sp.oo, N + 2).removeO()
    hs = sp.series(h, r, sp.oo, N + 2).removeO()
    bs = sp.series(rho2, r, sp.oo, N + 2).removeO()
    E2, L2 = sp.symbols('E2 L2', positive=True)
    V = E2 / fs - 1 - L2 / bs
    V1 = sp.diff(V, r)
    sol = sp.solve([V.subs(r, r0), V1.subs(r, r0)], [E2, L2], dict=True)[0]
    # ω_φ² = (L/ρ²)²
    phi2 = ser_in_eps(sol[L2] / bs.subs(r, r0) ** 2, N)
    # ω_r² = -V''/(2h)
    V2 = sp.diff(V, r, 2).subs({E2: sol[E2], L2: sol[L2]})
    omr2 = ser_in_eps(-V2.subs(r, r0) / (2 * hs.subs(r, r0)), N)
    G2 = sp.series(phi2 / omr2, eps, 0, N).removeO()
    G = sp.series(sp.sqrt(G2), eps, 0, N).removeO()
    # y = M/R_0，R_0 = r0*sqrt(h) ⟹ eps 与 y 的换式（再反演）
    yy = ser_in_eps(1 / (r0 * sp.sqrt(hs)), N)          # y(eps)
    eps_of_y = sp.series(sp.solve(sp.Eq(yy, y), eps)[0], y, 0, N).removeO() \
        if False else None
    # 用级数反演：eps = y*(c0 + c1*y + ...)
    a = sp.symbols('a1:9')
    e_series = y * (1 + sum(a[i - 1] * y ** i for i in range(1, 7)))
    expr = sp.series(yy.subs(eps, e_series) - y, y, 0, 8).removeO()
    eqs = [sp.expand(expr).coeff(y, k) for k in range(1, 8)]
    sols = sp.solve(eqs, a, dict=True)[0]
    eps_y = sp.series(e_series.subs(sols), y, 0, 8).removeO()
    G_y = sp.series(G.subs(eps, eps_y), y, 0, 6).removeO()
    return G_y


GR = run('GR')
FW = run('FW')
print("Γ_GR - 1 =")
print(sp.series(GR - 1, y, 0, 5))
print("")
print("Γ_FW - 1 =")
print(sp.series(FW - 1, y, 0, 5))
print("")
print("相对超额 R(y) = (Γ_FW-Γ_GR)/(Γ_GR-1) =")
R = sp.series((FW - GR) / (GR - 1), y, 0, 4)
print(R)
print("")
k = sp.limit((FW - GR) / (GR - 1) / y, y, 0)
print("κ_rel(0) = lim R/y =", sp.simplify(k), "=", sp.nsimplify(sp.simplify(k)), "=", float(k))
print("1/3 =", float(sp.Rational(1, 3)))
