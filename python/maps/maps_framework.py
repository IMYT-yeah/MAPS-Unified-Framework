# -*- coding: utf-8 -*-
"""
MAPS 新思考计算包 —— T1–T5 锚点验证（maps_framework.py）
=========================================================
运行：  python python/maps/maps_framework.py
产出：  T1–T5 五个锚点的数值 + 逐条判据（PASS/FAIL），末尾打印通过/失败计数。

⚠️ 重建说明（第 98 轮 · 2026-10-03）
------------------------------------
原文件 2026-09-16 随早期环境丢失。本文件按 `python/maps/README.md` 的 T1–T5 恢复规格重建，
并吸收 `outputs/_repo_assemble.py::patch_maps()` 中**逐字保留**的原代码片段。

【分级标注】（引用时须区分 —— 与 A1/Lean 资产恢复同一规范）
  A. 【逐字恢复】—— 下列行来自 `_repo_assemble.py` 做替换时的原文/新文，逐字一致：
       · T5 的 `lam_c = 1.3e26` 与 `P = (l_P / L_vals) ** alpha * np.exp(-L_vals / lam_c)`；
       · T5 的打印串（含「L>=l_P 才为概率…」说明）；
       · F1 注释的两处修正文本（高能/低能两端的 ε 走向）。
  B. 【重建 · 待核对】—— T1–T4 的实现：公式与判据有规格，**原实现的函数名/打印格式未入任何记录**。
  C. 【重设计】—— `run.sh`（原文件未在日志中留下任何内容）。
  ⚠️ 本文件**不是**原件；T1–T5 的**数值判据**已与项目既有记录对过（见 `_maps_a2_98.py`），
     但**打印格式与内部结构**不可复现。

⚠️ 符号警告：本包的 `alpha`（F5 幂指数）≠ 论文 §4.8 的 `alpha`（视界系数，熵一致性锁定为 1）。
"""

import numpy as np
import sympy as sp

from formula import F1, F2, F3, F4, F5        # noqa: F401  （同目录，只用于打印）

# ============================================================================
# 常数（一律**自洽导出**，不各取独立 CODATA 值 —— 见项目技能「陷阱 42(a)」）
# ============================================================================
G = 6.67430e-11
c = 2.99792458e8
hbar = 1.054571817e-34
kB = 1.380649e-23
eV = 1.602176634e-19

l_P = np.sqrt(hbar * G / c ** 3)             # 1.61626e-35 m
m_P = np.sqrt(hbar * c / G)                  # 2.17643e-8 kg
E_P = m_P * c ** 2                           # 普朗克能（J）

M_sun = 1.98847e30                           # kg
EPS0 = 7.7e-20                               # ε₀（F1）
BETA_EPS = 0.615                             # β（F1）
MEV_J = 1e-3 * eV

ALPHA_F5 = 1.0                               # F5 幂指数（两条独立反推 ⟹ 1，见 formula.py）
LAM_C = 1.3e26                               # λ_c（m，宇宙学尺度候选）

RESULT = []


def chk(tag, ok, msg):
    RESULT.append((tag, bool(ok)))
    print("      [{}] {} —— {}".format("OK" if ok else "XX", tag, msg))
    return bool(ok)


# ============================================================================
# T1 · PPN：由 g₀₀ = −e^{−2x} 展开 ⟹ γ = 1、β = 1（1PN 与 GR 不可区分）
# ============================================================================
def T1():
    print("[T1] PPN：由 g00 = -exp(-2x) 展开")
    x = sp.symbols("x", real=True)

    g00 = -sp.exp(-2 * x)
    ser00 = sp.series(g00, x, 0, 3).removeO().expand()
    # Will 约定：g00 = -(1 - 2x + 2*beta*x^2)  ⟹  二次项系数 = -2*beta
    coef2 = sp.expand(ser00).coeff(x, 2)
    beta_ppn = -coef2 / 2
    print("      g00 展开 = {}".format(sp.expand(ser00)))
    print("      beta_ppn = {}  (=1 通过)".format(beta_ppn))

    # 空间分量：微变权守恒 ⟹ g_rr = e^{+2x}；Will 约定 g_rr = 1 + 2*gamma*x
    grr = sp.exp(2 * x)
    gamma_ppn = sp.series(grr, x, 0, 2).removeO().expand().coeff(x, 1) / 2
    print("      g_rr = exp(+2x)  ⟹  gamma_ppn = {}  (=1 通过)".format(gamma_ppn))

    # 其余 1PN 参数（静态扇区）：本包不构造动态度规 ⟹ 只声明静态扇区结论
    chk("T1.a", sp.simplify(beta_ppn - 1) == 0, "beta_ppn == 1（符号：coeff2 = -2β）")
    chk("T1.b", sp.simplify(gamma_ppn - 1) == 0, "gamma_ppn == 1（指数度规 ⟹ g_rr = e^{+2x}）")
    print("      ⚠️ 范围限定：上两条是**静态扇区**结论；ξ/α₁/α₂/α₃/ζ 系为**运动型参数**，")
    print("         静态 ansatz 对它们是盲区（论文 §4.5b；清单 N-38 / 第 93 轮）。")
    return True


# ============================================================================
# T2 · 玻尔兹曼：湮灭-再生动力学把速度分布推向 M-B 分布（toy MC）
# ============================================================================
def T2(seed=20261003, n=3000, steps=12000):
    print("[T2] 玻尔兹曼：湮灭-再生 toy MC ⟹ 收敛到 M-B 分布")
    rng = np.random.default_rng(seed)
    # 初态：双峰（明显非平衡），看动力学能否把它推到 Maxwell 分布
    v = np.empty((n, 3))
    v[:, 0] = np.concatenate([rng.normal(-1.0, 0.12, n // 2), rng.normal(+1.0, 0.12, n - n // 2)])
    v[:, 1] = rng.normal(0.0, 0.12, n)
    v[:, 2] = rng.normal(0.0, 0.12, n)

    # ⚠️ 关键：碰撞必须真正交换"动量"而不是交换"速度"。
    #    1D 等质量弹性碰撞 = 交换速度 = 置换 ⟹ 经验分布**严格不变**、永不弛豫（我第一版就栽在这）。
    #    3D 里相对速度绕碰面法向镜面反射 ⟹ 分布弛豫到 Maxwell。这就是湮灭-再生在速度空间的效应。
    for _ in range(steps):
        # ⚠️ 必须用**置换配对**（每步每粒子至多碰一次）。
        #    若用「随机 i、j 有放回」，同一索引在一批里被写多次 ⟹ numpy 的 fancy indexing
        #    非原子 ⟹ 后写覆盖前写 ⟹ 能量系统性流失（我第二版实测 <v²> 从 1.014 掉到 0.060）。
        pm = rng.permutation(n)
        i, j = pm[0::2], pm[1::2]
        g = v[i] - v[j]
        nx = rng.normal(size=(i.size, 3))
        nx /= np.linalg.norm(nx, axis=1, keepdims=True)
        gn = np.einsum("ij,ij->i", g, nx)
        g2 = g - 2.0 * gn[:, None] * nx            # 镜面反射：|g2| = |g| ⟹ 动量、能量都守恒
        V = 0.5 * (v[i] + v[j])
        v[i] = V + 0.5 * g2
        v[j] = V - 0.5 * g2

    # ⚠️ 口径：np.mean(v**2) 已经是**每分量**的 <v_x²>（对 3n 个分量取平均）
    #    ⟹ 不要再除 3（我第二版多除了一次，把 <v²> 报成真值的 1/3，看起来像"能量在流失"）。
    v2c = float(np.mean(v ** 2))
    sig = np.sqrt(v2c)
    # 逐分量对 1D Maxwell（高斯）
    devs = []
    for k in range(3):
        h, e = np.histogram(v[:, k], bins=31, range=(-3.5 * sig, 3.5 * sig), density=True)
        c0 = 0.5 * (e[1:] + e[:-1])
        th = np.exp(-c0 ** 2 / (2 * v2c)) / np.sqrt(2 * np.pi * v2c)
        devs.append(np.max(np.abs(h - th) / np.max(th)))
    dev = max(devs)
    sp = np.linalg.norm(v, axis=1)
    skew = float(np.mean((sp - sp.mean()) ** 3) / (sp.std() ** 3 + 1e-30))
    # ⚠️ Maxwell 速率分布的**偏度**解析值 = 2√2(4−π)/π^{3/2} ≈ 0.4360。
    #    （`2√(2/π) = 1.5958` 是它的**均值**，不是偏度 —— 我第一版把两者混了，
    #     于是把已经收敛的分布判成"没收敛"。统计矩不能混用。）
    skew_mb = 2.0 * np.sqrt(2.0) * (4.0 - np.pi) / np.pi ** 1.5
    print("      每分量 <v^2> = {:.6f}；直方图对 Maxwell 的最大相对偏差 = {:.2f}%".format(v2c, dev * 100))
    print("      速率分布偏度 = {:+.4f}（Maxwell 解析值 {:+.4f}）".format(skew, skew_mb))
    chk("T2.a", dev < 0.15, "直方图对 Maxwell 的最大相对偏差 < 15%（实测 {:.2f}%）".format(dev * 100))
    chk("T2.b", abs(skew - skew_mb) < 0.12,
        "速率分布偏度 = {:+.4f}，Maxwell 解析值 = {:.4f}".format(skew, skew_mb))
    print("      ⚠️ 层级：本包只做 toy MC；层级方程级的验证在 `_a2_bbgky_verify.py`")
    print("         （配对守恒 ΣC、动量/能量 ∫vC/∫½v²C、细致平衡 max|Q(f*)|）。")
    print("      ⚠️ 诚实边界：原包记录的偏差「0.075% / 0.048%」**无法从规格复现**")
    print("         （那两个数只在差异审计备忘里出现过一次，未写测试条件）⟹ 不声称已还原。")
    return True


# ============================================================================
# T3 · 熵：S = A/(4l_P²)  —— 纳特；乘 ln2 = 比特（两者都打印）
# ============================================================================
def T3(M=None):
    M = M_sun if M is None else M
    print("[T3] 熵：S = A/(4 l_P^2)  （太阳质量黑洞）")
    r_s = 2 * G * M / c ** 2
    A = 4 * np.pi * r_s ** 2
    S_nat = A / (4 * l_P ** 2)                 # 纳特（= S/k_B）
    S_bit = S_nat * np.log(2)
    T_H = hbar * c ** 3 / (8 * np.pi * G * M * kB)
    print("      r_s = {:.6e} m；A = {:.6e} m^2".format(r_s, A))
    print("      S = {:.6e} 纳特   ( = {:.6e} 比特 ，即 ×ln2 )".format(S_nat, S_bit))
    print("      自洽判据 Hawking 温度 T = {:.6e} K（标准 BH 值）".format(T_H))
    chk("T3.a", abs(S_nat / 1.05e77 - 1) < 0.02,
        "纳特数 ≈ 1.05e77（实测 {:.4e}）".format(S_nat))
    chk("T3.b", abs(S_nat - A / (4 * l_P ** 2)) < 1e-6 * S_nat, "恒等式自检：S = A/(4l_P²)")
    print("      ⚠️ C-58：README 的 T3 行把 **比特公式**（×ln2）与 **纳特数值**（1.05e77）并列，")
    print("         两者差 0.693。论文 §4.8【单位更正】用 Hawking 温度已裁决 = **纳特**")
    print("         （取比特则 T 偏 +44.27%）。本函数两个都打印，不替读者选。")
    return True


# ============================================================================
# T4 · 运动 = 湮灭：Δm = m(1 − 1/γ)
# ============================================================================
def T4():
    print("[T4] 运动 = 湮灭：Δm = m(1 - 1/gamma)")
    for b in (0.0, 0.1, 0.5, 0.9, 0.99, 0.999):
        g = 1.0 / np.sqrt(1 - b ** 2)
        print("      v/c = {:.3f} -> gamma = {:9.4f}, dM/m = {:8.5f}".format(b, g, 1 - 1 / g))
    g = 1.0 / np.sqrt(1 - 0.999 ** 2)
    frac = 1 - 1 / g
    chk("T4.a", abs(frac - 0.9552) < 1e-3, "v/c = 0.999 时 dM/m ≈ 95.5%（实测 {:.4%}）".format(frac))
    # 低速极限：Δm/m → ½(v/c)²  ⟹ 回到牛顿动能簿记 K = ½mv²
    for b in (1e-2, 1e-3, 1e-4):
        g = 1.0 / np.sqrt(1 - b ** 2)
        lhs, rhs = 1 - 1 / g, 0.5 * b ** 2
        print("      低速 v/c = {:.0e}: (1-1/gamma) = {:.6e} vs 0.5(v/c)^2 = {:.6e}".format(b, lhs, rhs))
    b = 1e-4
    g = 1.0 / np.sqrt(1 - b ** 2)
    chk("T4.b", abs((1 - 1 / g) / (0.5 * b ** 2) - 1) < 1e-6, "低速极限回牛顿（比值 -> 1）")
    print("      ⚠️ F4 是动能的标准簿记（K = (gamma-1)mc^2）的恒等重排 ⟹ 作为公式零新意；")
    print("         新意全在『这段动能 = 局域静质量的湮灭消耗』这一**解释层**，")
    print("         而静质量是洛伦兹标量、共动系内 dM ≡ 0 ⟹ 该解释需协变重述")
    print("         （改用 4-动量账：P^mu = (gamma*m, gamma*m*v)，见并轨备忘录 §5.3）。")
    return True


# ============================================================================
# T5 · 溶解/涌现：P(L) = (l_P/L)^alpha · exp(−L/λ_c)
# ============================================================================
def T5():
    print("[T5] 溶解/涌现：P(L) = (l_P/L)^alpha * exp(-L/lam_c)")
    alpha = ALPHA_F5
    for L in (1e-40, 1e-35, 1e-30, 1e-20, 1.0, 1e10, 1e20, 1e26):
        p = (l_P / L) ** alpha * np.exp(-L / LAM_C)
        note = ""
        if L < l_P:
            note = "  <-- L < l_P: 非概率（凝结强度/普朗克率）"
        print("      [T5] L={:.2e} m -> P_emerge = {:.3e}{}".format(L, p, note))
    # alpha = 1 的两条独立反推（第 98 轮取证）
    p_1e35 = (l_P / 1e-35) ** alpha
    chk("T5.a", abs(p_1e35 - 1.616) < 0.002,
        "反推 alpha=1：P(1e-35 m) = {:.4f}（审计记录的运行值 1.616）".format(p_1e35))
    Ls = np.logspace(np.log10(l_P), 26, 200)
    Ps = (l_P / Ls) ** alpha * np.exp(-Ls / LAM_C)
    chk("T5.b", np.all(Ps <= 1.0 + 1e-12), "L >= l_P 区间内 P <= 1（概率合法）")
    chk("T5.c", abs(1.0 - (l_P / l_P) ** alpha) < 1e-12, "P(l_P) = 1 恰好（alpha=1 的边界）")
    print("      ⚠️ 原实现丢了 exp(-L/lam_c) 因子且未声明适用域 ⟹ L=1e-35 m 时输出 1.616>1。")
    print("         本函数已补齐指数因子，并对 L < l_P 打印『非概率』说明（README 要求）。")
    print("      ⚠️ 规格缺口：lambda_c 是**候选值**（1.3e26 m，宇宙学尺度），alpha 来自反推；")
    print("         两者的**第一性来源**在包内不存在（并轨备忘录 §7 已登记为 O3）。")
    return True


# ============================================================================
def main():
    print("=" * 78)
    print("MAPS 新思考计算包 —— T1-T5 锚点验证")
    print("=" * 78)
    print("常数（自洽导出）：l_P = {:.6e} m, m_P = {:.6e} kg, E_P = {:.6e} J".format(l_P, m_P, E_P))
    print("")
    T1(); print("")
    T2(); print("")
    T3(); print("")
    T4(); print("")
    T5(); print("")
    n_pass = sum(1 for _, ok in RESULT if ok)
    n_fail = len(RESULT) - n_pass
    print("=" * 78)
    print("汇总：通过 {} 项，失败 {} 项".format(n_pass, n_fail))
    print("=" * 78)
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
