# -*- coding: utf-8 -*-
"""
判决性检验：我的约定对不对？
==============================
在 **λ≠1（Ω_K≠0）** 的宇宙里，标准第一定律 dE = TdS + W dV 应当写在**表观视界**
R_A = c/(H√λ) 上。若用同一套约定它成立 ⟹ 约定没错 ⟹ R_c 上的失败是真发现。
数值沿 z 微分（dt = -dz/((1+z)H)）。
"""
import math

c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
kB = 1.380649e-23
lP2 = hbar * G / c ** 3
Mpc = 3.0856775814913673e22
H0 = 67.66 * 1e3 / Mpc
OM_m, OM_L = 0.3111, 0.6889


def line(t):
    print("\n" + "=" * 74)
    print(t)
    print("=" * 74)


def state(z, OK0, w):
    """返回 (H, λ=1-Ω_K, R_A, E, S, T, W, V)"""
    Ez2 = OM_m * (1 + z) ** 3 + OK0 * (1 + z) ** 2 + OM_L
    H = H0 * math.sqrt(Ez2)
    OK = OK0 * (1 + z) ** 2 / Ez2
    lam = 1.0 - OK
    RA = c / (H * math.sqrt(lam))
    E = RA * c ** 4 / (2 * G)                       # Misner-Sharp（在 R_A 上恒等）
    S = kB * math.pi * RA ** 2 / lP2
    T = hbar * c / (2 * math.pi * kB * RA)
    rhoE = 3 * H ** 2 * c ** 2 / (8 * math.pi * G) * lam   # ρ = λ ρ_c
    p = w * rhoE
    W = (rhoE - p) / 2
    V = (4 * math.pi / 3) * RA ** 3
    return H, lam, RA, E, S, T, W, V


def d_dt(f, z, h, OK0, w):
    """对 t 的中心差分：dt = -dz/((1+z)H)；f 为一元 callable(z)"""
    zp, zm = z + h, z - h
    fp = f(zp)
    fm = f(zm)
    Hp = H0 * math.sqrt(OM_m * (1 + zp) ** 3 + OK0 * (1 + zp) ** 2 + OM_L)
    Hm = H0 * math.sqrt(OM_m * (1 + zm) ** 3 + OK0 * (1 + zm) ** 2 + OM_L)
    dtp = -h / ((1 + zp) * Hp)      # t(z-h) - t(z+h) 的一半…用两点斜率
    dtm = -h / ((1 + zm) * Hm)
    # dt(zp) - dt(zm) 近似用 |dt/dz| * 2h
    dtdz = 1.0 / ((1 + z) * H0 * math.sqrt(OM_m * (1 + z) ** 3 + OK0 * (1 + z) ** 2 + OM_L))
    return (fp - fm) / (2 * h * dtdz)


def run(OK0, w, label):
    print("\n  --- %s  (Ω_K0 = %+.3f, w = %.3f) ---" % (label, OK0, w))
    print("  z      λ        R_A/R_c      dE/dt         TdS/dt        WdV/dt        (TdS+WdV)/dE")
    for z in (0.5, 1.0, 2.0):
        H, lam, RA, E, S, T, W, V = state(z, OK0, w)
        Rc = c / H
        f = lambda zz, o=OK0, ww=w, i=None: state(zz, o, ww)[i]
        dE = d_dt(lambda zz: state(zz, OK0, w)[3], z, 1e-4, OK0, w)
        dS = d_dt(lambda zz: state(zz, OK0, w)[4], z, 1e-4, OK0, w)
        dV = d_dt(lambda zz: state(zz, OK0, w)[7], z, 1e-4, OK0, w)
        TdS = T * dS
        WdV = W * dV
        print("  %-6.1f %-8.4f %-12.6f %-13.6g %-13.6g %-13.6g %.6f"
              % (z, lam, RA / Rc, dE, TdS, WdV, (TdS + WdV) / dE))


line("判决性检验：表观视界上的标准第一定律（用我上一份脚本的同一套约定）")
run(0.0, 0.0, "平直 · 物质为主（w=0，理想化）")
run(0.1, 0.0, "开宇宙 λ<1")
run(-0.1, 0.0, "闭宇宙 λ>1")
run(0.1, -1.0, "开宇宙 · w=-1")

line("判读")
print("""  若上表 (TdS+WdV)/dE ≈ 1 ⟹ 我的约定正确 ⟹ 标准定律确实写在 R_A 上，
  而框架把热力学写到 R_c 上并取 T=ℏH/(2πk_B)，必然与之分歧 —— 分歧是**真发现**。

  若上表也 ≈ 3~4.5 ⟹ 我的约定（W 或 dV 或 T）有误 ⟹ 上一份脚本的"张力"结论需撤回重算。
""")
