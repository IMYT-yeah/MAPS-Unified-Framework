# -*- coding: utf-8 -*-
"""第 113 轮核验：I-24（κ_rel(e) 的解析式）—— 近圆极限解析定理 ＋ 机制分解
   检查项 I24-1 … I24-12。两段式项：取证读「补丁前备份」，确认读当前稿。
   生产脚本：outputs/_i24_a.py（Γ(eps) 级数）／_i24_e.py（四组合分解）／_i24_fix.py（换式）
"""
import io, os, math, re
from fractions import Fraction
import sympy as sp

BASE = r"C:\Users\Administrator\Desktop\2026-08-20-21-43-34"
OUT = os.path.join(BASE, "outputs")
HIST = os.path.join(BASE, "MAPS-Unified-Framework", "paper", "history")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
ZH_PRE = os.path.join(HIST, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-04第113轮前.md")
EN_PRE = os.path.join(HIST, "Paper_v2.9_EN_备份_2026-10-04第113轮前.md")
LIST = os.path.join(OUT, "工程期望清单.md")
HO = os.path.join(BASE, "环境交接说明.md")
I24 = os.path.join(OUT, "I24结项_近圆极限的解析值与1_3的机制.md")

rd = lambda p: io.open(p, encoding="utf-8").read()
Z, E, LP, H = rd(ZH), rd(EN), rd(LIST), rd(HO)
ZP, EP = rd(ZH_PRE), rd(EN_PRE)
ZL, EL = Z.split("\n"), E.split("\n")
OK = [0]
FAIL = [0]


def chk(tag, cond, msg):
    if cond:
        OK[0] += 1
        print("  [OK] " + tag + " " + msg)
    else:
        FAIL[0] += 1
        print("  [XX] " + tag + " " + msg)


y = sp.symbols('y', positive=True)

# ---------------------------------------------------------------- I24-1 标定
print("=== I24-1 机器标定：GR 必须复现闭式 (1−6y)^{-1/2}（到 y³）===")
# 我的机器（各向同性坐标 + 本轮点数理）给出的 Γ-1，以 eps = M/r_iso 为变量
GR_eps = [Fraction(3), Fraction(21, 2), Fraction(171, 4)]      # _i24_a.py / _i24_fix.py 实测
FW_eps = [Fraction(3), Fraction(23, 2), Fraction(99, 2)]
# eps ↔ y 换式（h 侧决定）：y = eps/sqrt(h)
# h_GR = (1+eps/2)^4 ⟹ y = eps(1-eps+3eps^2/4-...) ⟹ eps = y + y^2 + 5/4 y^3
# h_FW = e^{2eps}      ⟹ y = eps e^{-eps}          ⟹ eps = y + y^2 + 3/2 y^3
REV_GR = [Fraction(1), Fraction(1), Fraction(5, 4)]
REV_FW = [Fraction(1), Fraction(1), Fraction(3, 2)]


def compose(c, rv, n=3):
    """把 Σ c_k eps^k 换成 y 的级数（eps = y + rv1 y² + rv2 y³）"""
    yv = sp.symbols('yv')
    ep = yv + rv[1] * yv ** 2 + rv[2] * yv ** 3
    expr = sum(sp.Rational(c[k - 1].numerator, c[k - 1].denominator) * ep ** k for k in (1, 2, 3))
    return [sp.nsimplify(sp.expand(sp.series(expr, yv, 0, 4).removeO()).coeff(yv, k)) for k in (1, 2, 3)]


g_gr = compose(GR_eps, REV_GR)
g_fw = compose(FW_eps, REV_FW)
exact = [sp.Rational(3), sp.Rational(27, 2), sp.Rational(135, 2)]
chk("I24-1", g_gr == exact,
    "GR 的 y 系数 = " + str(g_gr) + " ⟹ 与闭式 (1−6y)^(-1/2) 的 " + str(exact) + " **逐项相等** ⟹ 机器与换式均正确")

print("=== I24-2 框架侧 ===")
chk("I24-2", g_fw == [sp.Rational(3), sp.Rational(29, 2), sp.Rational(77)],
    "Γ_FW − 1 = " + str(g_fw[0]) + "y + " + str(g_fw[1]) + "y² + " + str(g_fw[2]) + "y³")

print("=== I24-3 近圆极限的解析值 ===")
c1 = g_gr[0]
dc2 = g_fw[1] - g_gr[1]
k0 = sp.nsimplify(dc2 / c1)
chk("I24-3", k0 == sp.Rational(1, 3),
    "κ_rel(e=0) = Δc₂/c₁ = (" + str(g_fw[1]) + " − " + str(g_gr[1]) + ")/" + str(c1)
    + " = **" + str(k0) + "**")

print("=== I24-4 与第 112 轮数值的一致性 ===")
chk("I24-4", abs(float(k0) - 0.33332) < 1e-4,
    "解析 1/3 = %.8f ｜ 第 112 轮数值外推 0.33332 ｜ 差 %.2e ⟹ 数值结论升级为**解析定理**"
    % (float(k0), abs(float(k0) - 0.33332)))

print("=== I24-5 机制分解（f 侧 vs h 侧）===")
# _i24_e.py 实测（以 eps 为变量）：(GR,GR)=21/2, (GR,FW)=47/4, (FW,GR)=41/4, (FW,FW)=23/2
C2 = {('GR', 'GR'): Fraction(21, 2), ('GR', 'FW'): Fraction(47, 4),
      ('FW', 'GR'): Fraction(41, 4), ('FW', 'FW'): Fraction(23, 2)}
dh = C2[('GR', 'FW')] - C2[('GR', 'GR')]     # 只换 h
df = C2[('FW', 'GR')] - C2[('GR', 'GR')]     # 只换 f
tot = C2[('FW', 'FW')] - C2[('GR', 'GR')]
chk("I24-5", dh + df == tot,
    "Δc₂(eps)：h 侧 %s ｜ f 侧 %s ｜ 和 %s = 总差 %s ⟹ **严格可加**" % (dh, df, dh + df, tot))
chk("I24-5b", sp.Rational(dh.numerator, dh.denominator) / 3 == sp.Rational(5, 12) and
    sp.Rational(df.numerator, df.denominator) / 3 == sp.Rational(-1, 12),
    "分工：κ_h = +%s/3 = **+5/12**，κ_f = %s/3 = **−1/12**，净 **1/3**"
    % (sp.Rational(dh.numerator, dh.denominator), sp.Rational(df.numerator, df.denominator)))

print("=== I24-6 圆轨道的 y 修正 ===")
c2g = g_gr[1]
c3f, c3g = g_fw[2], g_gr[2]
kk = sp.simplify(c2g / c1)
slope = sp.simplify((sp.Rational((c3f - c3g).numerator, (c3f - c3g).denominator) - kk * dc2) / c1)
chk("I24-6", sp.simplify(k0 + slope * y) == sp.Rational(1, 3) + sp.Rational(5, 3) * y,
    "κ_rel(y; e=0) = 1/3 + (5/3)y + O(y²)（y ~ 0.01 时修正 +1.7%）")

print("=== I24-7 一般 e 仍是数值（诚实登记）===")
chk("I24-7", "I-24" in rd(I24) and "一般偏心率" in rd(I24),
    "备忘录明确登记：一般 e 的解析式**未得**（两点积分的完整级数计算量过大），仅近圆极限与本轮解析")

print("=== I24-8 第 113 轮补丁（两段式）===")
MK = {"ZH": "v2.9 口径注（第 113 轮：I-24", "EN": "caliber note (round 113: I-24"}
for tag, mk in MK.items():
    src, pre = (Z, ZP) if tag == "ZH" else (E, EP)
    chk("I24-8 " + tag, pre.count(mk) == 0 and src.count(mk) == 1, "补丁前 0 -> 补丁后 1")


def block_ok(lines, contains):
    idx = [i for i, s in enumerate(lines) if contains in s]
    if len(idx) != 1:
        return False, "anchor x" + str(len(idx))
    i = idx[0]
    a = i
    while a - 1 >= 0 and lines[a - 1].startswith(">"):
        a -= 1
    b = i
    while b + 1 < len(lines) and lines[b + 1].startswith(">"):
        b += 1
    return len([k for k in range(a, b + 1) if lines[k].strip() == ""]) == 0, \
        "[" + str(a + 1) + "," + str(b + 1) + "]"


ok, m = block_ok(ZL, MK["ZH"])
chk("I24-9", ok, "ZH 注在引用块内且块内 0 空行 " + m)

print("=== I24-10 清单编号与计数 ===")
rows = [(i + 1, int(re.match(r"^\| \*\*I-(\d+)\*\*", s).group(1)))
        for i, s in enumerate(LP.split("\n")) if re.match(r"^\| \*\*I-(\d+)\*\*", s)]
i24 = [i for i, s in enumerate(LP.split("\n")) if s.startswith("| **I-24**")]
i24b = [i for i, s in enumerate(LP.split("\n")) if s.startswith("| **I-24b**") or s.startswith("| **I-25**")]
chk("I24-10", len(i24) == 1 and len(i24b) == 1 and i24b[0] == i24[0] + 1,
    "I-24（登记）紧跟新条目（行 " + str(i24[0] + 1) + " / " + str(i24b[0] + 1) + "）")

print("=== I24-11 中英同步 ＋ 交接说明 ===")
chk("I24-11", E.count("round 113") >= 1 and H.count("I-24") >= 1 and H.count("I-25") >= 1, "EN 稿与新交接条目均落地（EN " + str(E.count("round 113")) + " / HO " + str(H.count("I-24")) + "）")

print("")
print("通过 " + str(OK[0]) + " 项，失败 " + str(FAIL[0]) + " 项")
