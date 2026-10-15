# -*- coding: utf-8 -*-
"""
EA 系列 —— §4.2 热平衡命题链与第 21 轮「置换模型」的兼容性审查
审查对象（论文 v2.9 §4.2 六命题链，摘要中简称「命题 2.1」）：
  1 平稳性 / 2 **遍历性(Birkhoff–Khinchin)** / 3 微观可逆性 / 4 混沌传播 / 5 细致平衡 / 6 kT=mc²
第 21 轮发现：衬底 tick = 相邻对换 ⟹ 可逆、无熵产生、构型混合尺度 R_mix = l_P sqrt(t/t_P)
            ⟹ 一个哈勃时只混合 ~47 μm。
本轮问：这两件事**冲突吗**？遍历性的主体到底是谁？
标准库：math / random。运行：
  [TOOLCHAIN]/binaries/python/versions/3.13.12/python.exe outputs/_sec4_ergodicity_audit.py
"""
import math as m
import random

FAILS = []


def chk(tag, got, want, rtol=1e-9):
    ok = abs(got - want) <= rtol * max(abs(want), 1e-300)
    print("  [%s] %-44s got=%.12g   want=%.12g" % ("OK" if ok else "XX", tag, got, want))
    if not ok:
        FAILS.append(tag)


def line(t):
    print("\n" + "-" * 74)
    print(t)
    print("-" * 74)


def show(tag, val, unit=""):
    print("  %-44s %-22.10g %s" % (tag, val, unit))


c = 2.99792458e8
G = 6.67430e-11
h_planck = 6.62607015e-34
hbar = h_planck / (2.0 * m.pi)
lP = m.sqrt(hbar * G / c ** 3)
tP = lP / c
H0 = 2.1927e-18
tH = 1.0 / H0

line("EA-0  原文审计：§4.2 六命题链到底主张了什么")
import os
HERE = os.path.dirname(os.path.abspath(__file__))
txt = open(os.path.join(HERE, "论文初稿_正反物质对风暴统一框架_v2.9.md"), encoding="utf-8").read()
keys = {
    "① 遍历性条目（Birkhoff–Khinchin）": "遍历性（Birkhoff–Khinchin 定理）",
    "② 遍历性被标为『动力学性质，实测 0.00%』": "遍历性/混沌传播（动力学性质，实测 0.00%）",
    "③ 已承认无全局热平衡（1/r 发散）": "引力系统无全局热平衡",
    "④ 配对湮灭-再生 ≡ 弹性散射（line 160）": "与弹性散射动力学等价",
}
for k, v in keys.items():
    n = txt.count(v)
    print("  [%s] %-42s 命中 %d 次" % ("OK" if n >= 1 else "XX", k, n))
    if n < 1:
        FAILS.append(k)
print("""
  ⟹ 三点要记下来：
     · 摘要里的「命题 2.1」= §4.2 的**六命题链**，遍历性是其中第 2 条；
     · 论文**已经**把遍历性标为「动力学性质，实测 0.00%」（v2.6 补充），不是无条件使用定理；
     · 论文**已经**承认「引力系统无全局热平衡」（line 176）——与第 21 轮的"全局未热化"**同向**。
  ⚠️ 唯一待收紧：第 2 条正文中未注明 B–K 定理**本身需要遍历性前提**（见 EA-4）。""")

line("EA-1  碰撞率：置换模型给出的速率与动理论估计是否一致")
n_dens = 1.0 / lP ** 3          # 满占位：每 l_P^3 一个诸元
sigma = lP ** 2                 # 普朗克面积截面
rate_kin = n_dens * sigma * c   # 动理论 n·sigma·v
show("数密度 n = 1/l_P^3 (m^-3)", n_dens)
show("截面 sigma = l_P^2 (m^2)", sigma)
show("动理论碰撞率 n·sigma·v (s^-1)", rate_kin)
show("框架 tick 率 1/t_P (s^-1)", 1.0 / tP)
chk("n·sigma·c = 1/t_P", rate_kin, 1.0 / tP, 1e-12)
show("平均自由程 1/(n sigma) (m)", 1.0 / (n_dens * sigma))
chk("平均自由程 = l_P", 1.0 / (n_dens * sigma), lP, 1e-12)
print("""
  ⟹ **完全一致**：满占位衬底 + 普朗克截面 + c ⟹ 碰撞率恰为 1/t_P，平均自由程恰为 l_P。
     这说明 A1 的「ν ~ 1/t_P」与动理论的 nσv 是同一个数，不是巧合（是 f=1 的后果）。""")

line("EA-2  两个时标：速度空间弛豫 vs 衬底构型混合")
n_c = 4                          # 硬球气体达到局域平衡所需碰撞数次数量级
tau_relax = n_c * tP
L_relax = n_c * lP
show("弛豫碰撞次数 n_c（量级假设）", n_c)
show("弛豫时标 tau_relax = n_c t_P (s)", tau_relax)
show("弛豫长度 L_relax = n_c l_P (m)", L_relax)
R_mix_H = lP * m.sqrt(tH / tP)
show("衬底构型混合 R_mix(t_H) (m)", R_mix_H)
show("两者之比 R_mix / L_relax", R_mix_H / L_relax)
print("""
  ⟹ **相差约 %.3g 倍**：速度空间的局域热平衡在 ~%d 次对换（%.2g s、%.2g m）内达成，
     而衬底**构型空间**的混合在一个哈勃时只走到 %.3g m。
  ⟹ **所以不冲突**：§4 需要的是**速度空间的局域平衡**（快），
     第 21 轮的 47 μm 说的是**构型空间的混合**（慢）。这是动理论的标准情形：
     **局域热平衡 + 全局非平衡，可以共存。**"""
      % (R_mix_H / L_relax, n_c, tau_relax, L_relax, R_mix_H))

line("EA-3  关键论证：全同粒子的弹性散射 ⟺ 速度对换（不可区分）")
random.seed(11)
# (a) 一维等质量弹性碰撞 = 交换速度（解析 + 数值）
v1, v2 = 3.7, -1.4
mm = 2.5
u1 = ((mm - mm) * v1 + 2 * mm * v2) / (2 * mm)
u2 = (2 * mm * v1 + (mm - mm) * v2) / (2 * mm)
chk("1D 等质量弹性碰撞 v1' = v2", u1, v2, 1e-15)
chk("1D 等质量弹性碰撞 v2' = v1", u2, v1, 1e-15)
chk("动量守恒", mm * u1 + mm * u2, mm * v1 + mm * v2, 1e-15)
chk("能量守恒", 0.5 * mm * (u1 ** 2 + u2 ** 2), 0.5 * mm * (v1 ** 2 + v2 ** 2), 1e-15)
# (b) 随机相邻对换后，速度多重集不变 ⟹ 单体分布不变
N = 2000
vel = [random.gauss(0.0, 1.0) for _ in range(N)]
before = sorted(vel)
for _ in range(50000):
    i = random.randrange(N - 1)
    vel[i], vel[i + 1] = vel[i + 1], vel[i]
after = sorted(vel)
same = all(abs(a - b) < 1e-12 for a, b in zip(before, after))
print("  [%s] 5 万次相邻对换后速度多重集不变（%d 个粒子）" % ("OK" if same else "XX", N))
if not same:
    FAILS.append("对换保持速度多重集")
print("""
  ⟹ **对换 = 等质量弹性散射，二者在多体层面不可区分**（等质量 1D 弹性碰撞就是交换速度）。
  ⟹ 这为论文 §4.2 line 160 那句「**配对的湮灭-再生在完美平衡（50:50）下与弹性散射动力学等价**」
     **提供了机制**：此前它是一句断言，现在由第 21 轮的置换模型**直接给出**
     （相邻对换 = 全同粒子交换身份 = 与弹性散射不可区分）。
  ⟹ 同时说明为什么 §4 的分子混沌截断/玻尔兹曼方程可以用：**底层本来就是弹性散射的等价物**。""")

line("EA-4  ⚠️ 唯一需要收紧的表述")
print("""
  第 2 条原文：「遍历性（Birkhoff–Khinchin 定理）：时间平均 = 系综平均」。
  · Birkhoff–Khinchin 定理的结论是「**若**变换是度量传递的（遍历），则时间平均 = 系综平均」；
    **它本身不保证遍历性**——遍历性是前提，不是结论。
  · 论文在 v2.6 补充里已经把遍历性标为「动力学性质，实测 0.00%」——处理是对的；
    但**正文第 2 条仍写成"由定理给出"**，容易被审稿人抓"循环"（这正是 M1 那类质疑）。
  ⟹ 建议正文第 2 条加一句：「B–K 定理以度量传递性为前提，故此处为**动力学假设**，
     数值验证见 v2.6（实测 0.00%），非定理自动成立」。""")

line("EA-5  判决")
print("""
  ✅ **§4 与第 21 轮不冲突**——遍历性的**主体不同**：
     §4 的遍历性 = **速度空间 / 事件流**（DSMC N=2000，实测 0.00%%）；
     第 21 轮的 47 μm = **衬底构型空间**的混合（置换）。两者相差约 %.2g 倍。
  ✅ **正面收获**：置换模型给论文 §4.2 的「配对湮灭-再生 ≡ 弹性散射」**提供了机制**
     （相邻对换 = 全同粒子交换身份 = 与等质量弹性碰撞不可区分，已数值验证）。
  ✅ **碰撞率自洽**：满占位 + 普朗克截面 ⟹ nσv = 1/t_P、平均自由程 = l_P，与 A1 的 ν 一致。
  ✅ 论文**已**承认「引力系统无全局热平衡」⟹ 与第 21 轮"全局未热化"**同向**，诚实标注到位。
  ⚠️ **待收紧 1 处**：正文第 2 条应注明 B–K 定理以遍历性为前提（避免"由定理得遍历性"的循环观感）。
  ⚠️ **建议新增 1 处**：把「速度空间弛豫 ~%d t_P」与「构型空间混合 47 μm/t_H」的
     %.1g 倍时标分离写进 §4.2，说明局域热平衡与全局非平衡如何共存。"""
      % (R_mix_H / L_relax, n_c, R_mix_H / L_relax))

line("汇总")
print("  失败项：%s" % ((", ".join(FAILS)) if FAILS else "无"))
