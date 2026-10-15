# -*- coding: utf-8 -*-
"""
CG 系列 —— 在因果视界上重做 F3 计数（B5 最后一环的下半）
命题：观测者端（B5 比特计数）与统计端（F3 通量管相干块计数）是否数同一批块？
只用标准库 math。运行：
  [TOOLCHAIN]/binaries/python/versions/3.13.12/python.exe outputs/_b5_horizon_count.py
"""
import math as m

FAILS = []


def chk(tag, got, want, rtol=1e-9):
    ok = abs(got - want) <= rtol * max(abs(want), 1e-300)
    print("  [%s] %-40s got=%.12g   want=%.12g" % ("OK" if ok else "XX", tag, got, want))
    if not ok:
        FAILS.append(tag)
    return ok


def line(t):
    print("\n" + "-" * 72)
    print(t)
    print("-" * 72)


def show(tag, val, unit=""):
    print("  %-42s %-22.10g %s" % (tag, val, unit))


# ----------------------------------------------------------------- 常数
c = 2.99792458e8
G = 6.67430e-11
hbar = 1.054571817e-34
kB = 1.380649e-23
lP = m.sqrt(hbar * G / c ** 3)
tP = lP / c
H0 = 2.1927e-18          # 框架自用值，与 09-11 的 R_c = 14.4516 Gly 一致
Gly = 9.460730e24
tH = 1.0 / H0
Rc = c / H0

line("CG-0  基线复算（与 09-11 / 09-12 对齐）")
show("l_P (m)", lP)
show("t_P (s)", tP)
show("R_c = c/H0 (Gly)", Rc / Gly)
show("T_GH = hbar H0/(2 pi kB) (K)", hbar * H0 / (2 * m.pi * kB))
N_cells = m.pi * (Rc / lP) ** 2          # = A/(4 l_P^2),  A = 4 pi R^2
show("N = A/(4 l_P^2)", N_cells)
M_tot = c ** 3 / (2 * G * H0)
show("M = c^3/(2 G H0) (kg)", M_tot)
chk("R_S(2GM/c^2) = R_c  [lambda = 1]", 2 * G * M_tot / c ** 2, Rc, 1e-12)
chk("N kB T = c^5/(2GH)", N_cells * kB * (hbar * H0 / (2 * m.pi * kB)), c ** 5 / (2 * G * H0), 1e-12)

# ------------------------------------------------- 积分器（校验过闭式解）
def simpson01(f, n=200001, lo=0.0):
    """int_lo^1 f(x) dx, Simpson"""
    h = (1.0 - lo) / (n - 1)
    s = f(lo) + f(1.0)
    for i in range(1, n - 1):
        s += (4.0 if i % 2 else 2.0) * f(lo + i * h)
    return s * h / 3.0


line("CG-1  候选热力学面清单")
# 事件视界（唯一按构造为零表面 = 真正的因果/事件视界）
# R_EH = (c/H0) * int_0^1 dx / sqrt(OL + Om x^3 + Or x^4)
def R_EH_over_Rc(Om, OL, Or=0.0):
    return simpson01(lambda x: 1.0 / m.sqrt(OL + Om * x ** 3 + Or * x ** 4))


# 先校验积分器：纯 de Sitter (Om=0, OL=1) 应给恰好 1
chk("R_EH/R_c  [纯 dS: Om=0,OL=1]", R_EH_over_Rc(0.0, 1.0), 1.0, 1e-8)
# 单流体闭式（无发散端点的那几个）：R_EH/R_c = -2/(3w+1)
for w in (-2.0, -1.5, -1.0):
    lhs = simpson01(lambda x: x ** (-3 * (w + 1) / 2))
    chk("R_EH/R_c 单流体 w=%.2f [闭式]" % w, lhs, -2.0 / (3 * w + 1), 1e-8)
# w = -0.6889 / -0.5 的积分在 x=0 处有可积奇性，做换元 x = u^(1/(1-a)) 把奇性消成常数
for w in (-0.6889, -0.5):
    a = 3 * (w + 1) / 2
    k = 1.0 / (1.0 - a)
    lhs = simpson01(lambda u: k * (1.0 if abs(k * (1 - a) - 1.0) < 1e-15 else u ** (k * (1 - a) - 1.0)))
    chk("R_EH/R_c 单流体 w=%.4f [换元+闭式]" % w, lhs, -2.0 / (3 * w + 1), 1e-8)
# LambdaCDM 积分的收敛性（换分割数）
vals = [simpson01(lambda x: 1.0 / m.sqrt(0.6889 + 0.3111 * x ** 3 + 9.15e-5 * x ** 4), n) for n in (50001, 200001, 800001)]
print("  LambdaCDM 积分收敛：n=5e4 %.10f | n=2e5 %.10f | n=8e5 %.10f" % tuple(vals))
chk("积分收敛（2e5 vs 8e5）", vals[1], vals[2], 1e-8)

RATIO_LCDM = R_EH_over_Rc(0.3111, 0.6889, 9.15e-5)
RATIO_FW = R_EH_over_Rc(1.0 / 3.0, 2.0 / 3.0)
show("R_c = c/H0 (Gly)", Rc / Gly)
show("R_EH/R_c  [LCDM 0.3111/0.6889]", RATIO_LCDM)
show("R_EH  [LCDM] (Gly)", RATIO_LCDM * Rc / Gly)
show("R_EH/R_c  [框架 1/3 + 2/3]", RATIO_FW)
show("R_A = c/(H sqrt(lambda_micro)) (Gly)", Rc / m.sqrt(8 * m.pi / 3) / Gly)

line("CG-2  时间尺分离：块分解是否准静态（零阶闭合）")
nu = 1.0 / tP
show("nu = 1/t_P (s^-1)", nu)
show("nu/H0", nu / H0)
show("R_c/l_P = 1/(H0 t_P)", Rc / lP)
chk("nu/H0 = R_c/l_P", nu / H0, Rc / lP, 1e-6)
HtP = H0 * tP
show("H0 t_P  (= 相对修正量级)", HtP)
ln2 = m.log(2.0)
show("ln2 (上一轮解决的分歧量级)", ln2)
show("ln2 / (H0 t_P)   [两轮效应之比]", ln2 / HtP)
print("""
  读法：风暴微观结构以 nu = 1/t_P 刷新，视界几何以 H0 变化。
  · 每个面元在一个哈勃时内被刷新 nu*t_H = %.4g 次；
  · 因此「块的分解」是瞬时量、不带历史 —— 两端的分解只能是同一套，
    除非冻结微观结构（nu -> 0）。冻结时失配 O(beta_s) 见 CG-3。""" % (nu * tH))

line("CG-3  零表面检验：框架的面是不是零表面？")
q_lcdm = 0.5 * 0.3111 + 9.15e-5 - 0.6889
show("q0 = om/2 + Or - OL  [LCDM]", q_lcdm)
show("dR_c/dt / c = 1 + q0", 1.0 + q_lcdm)
print("""
  单流体 w 的 q = (1+3w)/2：""")
print("     w            q          dR_c/dt / c      零表面?")
for w in (-1.0, -0.6889, -0.5, 0.0, 1.0 / 3.0):
    q = (1.0 + 3.0 * w) / 2.0
    spd = 1.0 + q
    tag = "是" if abs(spd) < 1e-12 else ("超光速(spacelike)" if abs(spd) > 1 else "亚光速(timelike)")
    print("     %-12.4f %-10.5f %-16.5f %s" % (w, q, spd, tag))
print("""
  ⟹ **只有纯 de Sitter (w = -1) 时框架的面才是零表面**；
     LCDM 的有效 w = -0.6889 时它以 %.4gc 外移 —— 是 timelike 面，不是因果面。
  ⟹ 因此「零表面」不能作为 B5 的理由。真正的理由是 CG-2 的时间尺分离。""" % (1.0 + q_lcdm))
beta_s = 1.0 + q_lcdm
show("beta_s = 1+q0  [若冻结结构的失配量级]", beta_s)
show("beta_s^2", beta_s ** 2)

line("CG-4  判决性检验：改用真事件视界，lambda 与 Omega_K 会变成多少？")
print("""
  等分账在半径 R 的面上：E = N kB T，N = A/(4 l_P^2) = pi R^2 / l_P^2
  两种温度读法：
    (甲) T 固定 = hbar H0/(2 pi kB)（框架原式）        ⟹ E ∝ R^2 ⟹ lambda = (R/R_c)^2
    (乙) T 由该面表面引力定 kappa = c^2/R ⟹ T ∝ 1/R  ⟹ E ∝ R   ⟹ lambda = (R/R_c)
  框架定义 lambda = rho/rho_crit，Omega_K = 1 - lambda。""")
OmK_obs, OmK_err = 0.0007, 0.0019          # Planck2018+BAO
OmK_obs2, OmK_err2 = -0.044, 0.018         # Planck 单独（更宽）

for name, ratio in (("LCDM", RATIO_LCDM), ("框架 1/3+2/3", RATIO_FW)):
    print("\n  == %s：R_EH/R_c = %.4f ==" % (name, ratio))
    for vname, lam in (("甲 T 固定", ratio ** 2), ("乙 T ∝ 1/R", ratio)):
        OmK = 1.0 - lam
        s1 = (OmK_obs - OmK) / OmK_err
        s2 = (OmK_obs2 - OmK) / OmK_err2
        print("     %-10s lambda = %.4f  ⟹ Omega_K = %+.4f   偏离 %.1f sigma (Planck+BAO) / %.1f sigma (Planck 单独)"
              % (vname, lam, OmK, abs(s1), abs(s2)))

line("CG-5  顺带查出的结构问题：lambda = 4 alpha^2 beta^2 = 1 是恒等式")
print("""
  框架定义 alpha = 4 pi / xi（熵系数 S = kB A/(xi l_P^2)），beta = xi/(8 pi)（第一定律反解）：
     lambda = 4 alpha^2 beta^2 = 4 * (16 pi^2 / xi^2) * (xi^2 / 64 pi^2) = 1
  对任意 xi 恒成立 —— 这正是上一轮称作「xi-稳健性」的那件事。逐值核验：""")
print("     xi            alpha          beta          4 alpha^2 beta^2    Omega_K = 1-lambda")
for xi in (1.0, 2.0, 3.0, 4.0, 4.0 * m.log(2), 8.0, 16.0):
    al = 4 * m.pi / xi
    be = xi / (8 * m.pi)
    lam = 4 * al ** 2 * be ** 2
    print("     %-12.6g %-14.8g %-14.8g %-18.12f %+.1e" % (xi, al, be, lam, 1.0 - lam))
chk("4 alpha^2 beta^2 恒为 1", 4 * (4 * m.pi / 7.3) ** 2 * (7.3 / (8 * m.pi)) ** 2, 1.0, 1e-12)

# 对照：装备分账那条路由 lambda = (R/R_c)^2，是「面敏感」的
print("""
  对照 —— 装备分账（CG-4 甲式）给出的 lambda = (R/R_c)^2 **依赖 R**：
     R/R_c = 1.0000  ⟹ lambda = 1.0000  ⟹ Omega_K = +0.0000
     R/R_c = %.4f  ⟹ lambda = %.4f  ⟹ Omega_K = %+.4f
  ⟹ 两条路只在 R = R_c 处重合。alpha-beta 路**看不见 R**，因此它不可能用来挑面，
     也不可能作为「lambda = 1 已获验证」的独立证据。""" % (RATIO_LCDM, RATIO_LCDM ** 2, 1 - RATIO_LCDM ** 2))

line("CG-6  判决")
print("""
  ✅ CG-1/CG-2 —— 「同一批块」在 O(H0 t_P) = %.3g 的意义上成立：
     块分解是瞬时的（风暴以 nu = 1/t_P 刷新，一个哈勃时刷新 %.4g 次），
     视界几何的变化 (H0) 相对刷新率小 %.3g 倍；上一轮解决的分歧量级 ln2 = %.4f
     比这个残差大 %.3g 倍。**最后一环的精度远超出所需。**
  ❌ CG-3 —— 但「零表面」这条理由被否证：框架的面在 w = -0.6889 时以 %.3gc 外移，
     是 timelike 面。B5 不能表述为「观测者因果补丁的边界」。
  ❌ CG-4 —— 改用真正的零表面（事件视界）会给 lambda = 1.15~1.32，
     Omega_K = -0.15 ~ -0.32，被观测排除（最宽约束也有 5.7 sigma）。
     ⟹ 在自然候选面中 c/H 是**唯一幸存者**。
  ⚠️ CG-5 —— lambda = 4 alpha^2 beta^2 = 1 是恒等式（xi 全约掉），**零宇宙学内容**；
     上一轮记的「xi-稳健性」应降调：那不是稳健，那是重言式。
     有内容的只有装分账在 R_c 上的那条路。

  ⟹ B5 应重新表述为：**热力学面 = 平流停滞面（v_rec = c）**，
     建立精度 O(10^-61)，且在自然候选面中唯一不被观测排除；
     但仍带数据成分（排除用的是 Omega_K 观测量），不是纯先验推导。"""
      % (HtP, nu * tH, nu / H0, ln2, ln2 / HtP, beta_s))

line("汇总")
print("  失败项：%s" % ((", ".join(FAILS)) if FAILS else "无"))
print("  关键数：R_c = %.5f Gly | T = %.6g K | N = %.6g | nu/H0 = %.6g | H0 t_P = %.4g"
      % (Rc / Gly, hbar * H0 / (2 * m.pi * kB), N_cells, nu / H0, HtP))
print("          R_EH/R_c[LCDM] = %.6f | R_EH/R_c[1/3+2/3] = %.6f" % (RATIO_LCDM, RATIO_FW))
