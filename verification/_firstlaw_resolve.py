# -*- coding: utf-8 -*-
"""
修正 BX-E：微分第一定律到底选定哪个温度？（2026-09-16 夜）
============================================================
上一版我把"代数等分 vs 微分定律"的张力误框定为"两条定律不相容"。
真正的结构是：微分第一定律 **确实成立**，但它选定的温度是 **Kodama 温度**，
不是框架的 GH 温度 ℏH/(2πk_B)。

约定（与上两份脚本一致）：
  E = R c⁴/(2G)（Misner-Sharp，在表观视界上恒等）
  S = k_B A/(4 l_P²) = k_B π R²/l_P²
  W = (ρ_E - p)/2
  dV/dt = 4π R² Ṙ
检验三个候选温度哪个让 dE = T dS + W dV 成立：
  T_GH     = ℏH/(2πk_B)              （框架用的）
  T_Kodama = ℏH(3w-1)/(8π k_B)       （Hayward-Kodama 表面引力）
  T_A      = ℏc/(2π k_B R_A)         （= T_GH 当 λ=1）
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
    print("\n" + "=" * 76)
    print(t)
    print("=" * 76)


def check(OK0, w, label):
    print("\n  --- %s (Ω_K0=%+.3f, w=%.3f) ---" % (label, OK0, w))
    print("  z      λ        R_A/R_c    T_GH闭合    T_Kodama闭合   T_A闭合")
    for z in (0.5, 1.0, 2.0):
        Ez2 = OM_m * (1 + z) ** 3 + OK0 * (1 + z) ** 2 + OM_L
        H = H0 * math.sqrt(Ez2)
        OK = OK0 * (1 + z) ** 2 / Ez2
        lam = 1.0 - OK
        RA = c / (H * math.sqrt(lam))
        rhoE = 3 * H ** 2 * c ** 2 / (8 * math.pi * G) * lam
        p = w * rhoE
        # 解析导数（平直以外的曲率演化已含在 λ(z) 里）
        Hdot = -1.5 * (1 + w) * H ** 2          # 由 Friedmann 微分式（平直主导项）
        lam_dot = 0.0 if abs(OK0) < 1e-12 else None
        # 用有限差分求 R_A 对 t 的导数（稳妥）
        def RA_of(zz):
            E2 = OM_m * (1 + zz) ** 3 + OK0 * (1 + zz) ** 2 + OM_L
            Hh = H0 * math.sqrt(E2)
            OKk = OK0 * (1 + zz) ** 2 / E2
            return c / (Hh * math.sqrt(1.0 - OKk))
        hh = 1e-5
        dtdz = 1.0 / ((1 + z) * H)
        Rdot = (RA_of(z + hh) - RA_of(z - hh)) / (2 * hh * dtdz)
        # E, S, V 导数
        dE = c ** 4 / (2 * G) * Rdot
        dS = 2 * kB * math.pi * RA / lP2 * Rdot
        dV = 4 * math.pi * RA ** 2 * Rdot
        W = (rhoE - p) / 2
        T_GH = hbar * H / (2 * math.pi * kB)
        T_K = hbar * H * (3 * w - 1) / (8 * math.pi * kB)
        T_A = hbar * c / (2 * math.pi * kB * RA)
        r_gh = (T_GH * dS + W * dV) / dE
        r_k = (T_K * dS + W * dV) / dE
        r_a = (T_A * dS + W * dV) / dE
        print("  %-6.1f %-8.4f %-10.6f %-11.6f %-14.6f %.6f"
              % (z, lam, RA / (c / H), r_gh, r_k, r_a))


line("哪个温度让 dE = T dS + W dV 成立？（比值应为 1）")
check(0.0, 0.0, "平直 · w=0")
check(0.0, -1.0, "平直 · de Sitter")
check(0.1, 0.0, "开宇宙 · w=0")
check(-0.1, 1.0 / 3, "闭宇宙 · 辐射")

line("判读")
print("""  T_Kodama 一列若为 1 ⟹ **微分第一定律选定的温度是 Kodama 温度，不是 GH 温度**。
  这一发现把上一版的"张力"改写成一条清晰的结构性结论：

    · 标准包：T = T_Kodama，dE = TdS + WdV ⟺ Friedmann。λ **不受约束**（初始条件）。
    · 框架包：T = T_GH = ℏH/(2πk_B)，代数等分 E = T·S 写在因果视界 R_c 上 ⟹ **λ = 1**。
      但此时热/功形式的微分定律 **不成立**（需要 W = -ρ_E/3，非物理）。

  ⟹ 两个包是**不同的热力学结构**，不是谁算错了。
  ⟹ 框架取后者 ⟹ 预言 λ=1，但**放弃了"由视界热力学推出 Friedmann"这条路**。
  ⟹ 与「框架未导出 Friedmann」的现状自洽 —— 而且说明：
     **Friedmann 必须从 A1/A2 微观物理推，视界热力学这条路是走不通的。**
""")
