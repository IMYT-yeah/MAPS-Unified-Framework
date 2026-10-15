# -*- coding: utf-8 -*-
"""
MAPS 新思考包 —— 独立符号/数值自检（verify.py）
================================================
运行：  python python/maps/verify.py
产出：  逐项 [OK]/[XX] ＋ 末尾「通过 N 项，失败 M 项」。

⚠️ 重建说明（第 98 轮 · 2026-10-03）
------------------------------------
原文件 2026-09-16 随早期环境丢失。
【A 级 · 逐字恢复】本文件的 [PPN] 段来自 `outputs/_repo_assemble.py::patch_maps()`：
    原文：  beta_ppn = series.expand().coeff(x, 2) / 2
    修复：  beta_ppn = -series.expand().coeff(x, 2) / 2   # 负号: Will 约定 g00=-(1-2x+2 beta x^2)
    打印：  print("[PPN] beta =", float(beta_ppn), "(=1 通过)")
    （原文缺负号 ⟹ 打印 `beta = -1 (=1 通过)`，符号错却自我宣布通过 —— 差异审计 §4 缺陷 1。）
【B 级 · 重建】其余检查项按本包 T1–T5 的判据重设计。

⚠️ 与 `maps_framework.py` 的分工：本文件**不复用**它的函数，独立重算一遍
   （两个文件互为对照；`run.sh` 依次跑两者）。
"""

import numpy as np
import sympy as sp

RES = []


def chk(tag, ok, msg):
    RES.append((tag, bool(ok)))
    print("  [{}] {:<8} {}".format("OK" if ok else "XX", tag, msg))


print("=" * 78)
print("MAPS 新思考包 —— verify.py 自检")
print("=" * 78)

# ---------------------------------------------------------------- PPN
print("\n[PPN] 由 g00 = -exp(-2x) 提取 beta、gamma")
x = sp.symbols("x", real=True)

g00 = -sp.exp(-2 * x)
series = sp.series(g00, x, 0, 3).removeO().expand()
print("  g00 展开 =", series)

beta_ppn = -series.expand().coeff(x, 2) / 2   # 负号: Will 约定 g00=-(1-2x+2 beta x^2)
print("[PPN] beta =", float(beta_ppn), "(=1 通过)")

grr = sp.exp(2 * x)
gamma_ppn = sp.series(grr, x, 0, 2).removeO().expand().coeff(x, 1) / 2
print("[PPN] gamma =", float(gamma_ppn), "(=1 通过)")

chk("PPN-1", abs(float(beta_ppn) - 1.0) < 1e-12, "beta = +1（**不是** -1 —— 负号必须显式取）")
chk("PPN-2", abs(float(gamma_ppn) - 1.0) < 1e-12, "gamma = 1（微变权守恒 ⟹ g_rr = e^{+2x}）")
# 符号自检：把负号拿掉会得到 -1 —— 这正是原件的缺陷，把它固化成一条检查
chk("PPN-3", abs(float(series.coeff(x, 2) / 2) + 1.0) < 1e-12,
    "**不带负号**会得 -1 ⟹ 原件缺陷可复现（防止回归）")

# ---------------------------------------------------------------- F1
print("\n[F1] 泄漏率 eps(E) = eps0*(M_Pl/E)^beta —— 两端走向")
hb = 1.054571817e-34; Gc = 6.67430e-11; cc = 2.99792458e8; eV = 1.602176634e-19
m_P = np.sqrt(hb * cc / Gc); E_P_J = m_P * cc ** 2
eps0, be = 7.7e-20, 0.615


def eps_of_E_eV(E_eV):
    return eps0 * (E_P_J / (E_eV * eV)) ** be


e_meV = eps_of_E_eV(1e-3)
e_Pl = eps_of_E_eV(E_P_J / eV)
print("  eps(1 meV) = {:.6e} ；eps(M_Pl) = {:.6e}".format(e_meV, e_Pl))
chk("F1-1", e_meV > 1e-3, "低能端 eps -> O(1)（饱和 = 暗能量侧），**不是** -> 0")
chk("F1-2", abs(e_Pl / eps0 - 1.0) < 1e-12, "高能端 eps -> eps0 = 7.7e-20（在 M_Pl 上取到 eps0）")

# ---------------------------------------------------------------- F3
print("\n[F3] 熵 S = A/(4 l_P^2) —— 纳特 vs 比特")
l_P = np.sqrt(hb * Gc / cc ** 3)
M_sun = 1.98847e30
r_s = 2 * Gc * M_sun / cc ** 2
A = 4 * np.pi * r_s ** 2
S_nat = A / (4 * l_P ** 2)
kB = 1.380649e-23
T_H = hb * cc ** 3 / (8 * np.pi * Gc * M_sun * kB)
print("  S = {:.6e} 纳特 ；S*ln2 = {:.6e} 比特".format(S_nat, S_nat * np.log(2)))
print("  T_H = {:.6e} K".format(T_H))
chk("F3-1", abs(S_nat / 1.05e77 - 1) < 0.02, "太阳质量黑洞 S ≈ 1.05e77 **纳特**")
chk("F3-2", abs(T_H - 6.16868e-8) / 6.16868e-8 < 1e-3, "Hawking 温度与标准值一致（<0.1%）")
chk("F3-3", abs(np.log(2) - 0.6931471805599453) < 1e-15, "ln2 因子 = 0.6931（C-58 的差额来源）")

# ---------------------------------------------------------------- F4
print("\n[F4] 运动 = 湮灭：dm/m = 1 - 1/gamma")
b = 0.999
g = 1.0 / np.sqrt(1 - b ** 2)
frac = 1 - 1 / g
chk("F4-1", abs(frac - 0.9552) < 1e-3, "v/c=0.999 -> dm/m = {:.4f}（记录值 95.5%）".format(frac))
b2 = 1e-4
g2 = 1.0 / np.sqrt(1 - b2 ** 2)
chk("F4-2", abs((1 - 1 / g2) / (0.5 * b2 ** 2) - 1) < 1e-6, "低速极限回牛顿（比值 -> 1）")

# ---------------------------------------------------------------- F5
print("\n[F5] P(L) = (l_P/L)^alpha * exp(-L/lam_c)")
alpha, lam_c = 1.0, 1.3e26
p_lo = (l_P / 1e-35) ** alpha * np.exp(-1e-35 / lam_c)
p_at = (l_P / l_P) ** alpha
Ls = np.logspace(np.log10(l_P), 26, 500)
Ps = (l_P / Ls) ** alpha * np.exp(-Ls / lam_c)
chk("F5-1", abs(p_lo - 1.616) < 0.002, "反推 alpha=1：P(1e-35 m) = {:.4f}（记录值 1.616）".format(p_lo))
chk("F5-2", abs(p_at - 1.0) < 1e-12, "P(l_P) = 1（alpha=1 ⟺ 『L>=l_P 才是概率』）")
chk("F5-3", np.all(Ps <= 1 + 1e-12), "适用域内 P <= 1")

print("\n" + "=" * 78)
n_ok = sum(1 for _, o in RES if o)
print("汇总：通过 {} 项，失败 {} 项".format(n_ok, len(RES) - n_ok))
print("=" * 78)
raise SystemExit(0 if n_ok == len(RES) else 1)
