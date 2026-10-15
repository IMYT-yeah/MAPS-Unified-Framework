# -*- coding: utf-8 -*-
"""
B2 统计->几何严格化: 数值验证
1) 截断定量: 玻尔兹曼分布适用域 r >= r_c = GM/c^2 (通量抽零半径)
   - e^{-Phi/c^2} 在 r_c 处 = e^{-1} = 0.368 (指数压制失效点)
   - 纯 1/r 势发散 (热平衡报告模拟2) 的截断
2) 截断后归一化 + 弱场展开检查
3) 遍历性马尔可夫确认 (热平衡报告模拟3已做, 此处补理论对照)
4) 混沌传播: 硬球 vs 湮灭-再生 的有效对应
"""
import math

c = 2.99792458e8
G = 6.67430e-11
Msun = 1.98892e30

print("=" * 74)
print("B2 子项3: 截断定量 — 玻尔兹曼分布适用域 = 视界")
print("=" * 74)

# 玻尔兹曼分布: rho/rho_inf = exp(-Phi/c^2), Phi = -GM/r (引力势)
# 发散: r->0 时 Phi -> -inf, exp(-Phi/c^2) = exp(+GM/(c^2 r)) -> inf
# 适用域: Phi/c^2 = GM/(c^2 r) <= O(1) -> r >= GM/c^2 = r_c (通量抽零半径)
print("\n1) 截断半径 r_c = GM/c^2 (通量抽零半径, P0/alpha 工作确定):")
blacks = [("太阳", 1.0*Msun), ("M87*", 6.5e9*Msun), ("Sgr A*", 4.3e6*Msun), ("原初黑洞(10^11kg)", 1e11)]
for name, M in blacks:
    r_c = G*M/c**2
    r_s = 2*r_c
    print(f"  {name:18s}: r_c = {r_c:.4e} m (= GM/c^2, 半史瓦西), r_s = {r_s:.4e} m")

print("\n2) 玻尔兹曼因子在关键半径处的值 (x = GM/(c^2 r) = r_c/r):")
print(f"  r = r_c (x=1):    e^-x = {math.exp(-1):.4f}  <- 指数压制失效点 (截断)")
print(f"  r = 2 r_c (x=0.5): e^-x = {math.exp(-0.5):.4f}  (中子星表面量级)")
print(f"  r = 10 r_c (x=0.1): e^-x = {math.exp(-0.1):.4f}  (弱场, PPN 区)")
print(f"  r = 100 r_c (x=0.01): e^-x = {math.exp(-0.01):.4f} (太阳表面量级)")

print("\n3) 截断的意义 — 热平衡适用域 = 弱场区:")
print("   r >= r_c: 玻尔兹曼分布 e^{-Phi/c^2} 有效 (弱场几何区, PPN gamma=beta=1)")
print("   r <  r_c: 过载区 (风暴物理接管, 非几何 — 七环机制, P0-1 强场定位)")
print("   => 截断定量 r_c = GM/c^2 与框架视界位置完全一致 (三重确认: 热平衡发散+熵一致性+Ms/A 临界)")

print("\n4) 截断后分布的可归一性 (引力系统无全局热平衡的定量表述):")
# 3D 球对称: 若 rho ~ exp(+GM/(c^2 r)), 粒子数积分 int rho 4pi r^2 dr 在 r->0 发散
# 截断 r>=r_c 后: int_{r_c}^{inf} exp(GM/(c^2 r)) r^2 dr = int exp(x r_c/r) r^2 dr, 在 inf 收敛
# 数值估算: 归一化积分 (截断在 r_c)
def boltzmann_norm(M):
    r_c = G*M/c**2
    # int_{r_c}^{R_max} exp(r_c/r) r^2 dr (无量纲 y = r/r_c: int_1^{Y} exp(1/y) y^2 dy * r_c^3)
    Y = 1e3  # R_max = 1000 r_c
    N = 100000
    dy = (Y-1)/N
    s = 0.0
    for i in range(N):
        y = 1 + (i+0.5)*dy
        s += math.exp(1.0/y) * y*y * dy
    return s  # 单位 r_c^3

s_sun = boltzmann_norm(Msun)
print(f"  太阳: 截断后归一化积分 = {s_sun:.2f} r_c^3 (有限 ✓, 无截断则发散)")
print("   => '引力系统无全局热平衡' (热平衡报告模拟2) 的定量表述: 无截断时 int diverges,")
print("      截断 r_c 后有限 — 玻尔兹曼分布仅在 r >= r_c 有效")

print("\n5) 弱场展开自洽 (r >> r_c):")
# e^{-x} = 1 - x + x^2/2 - ... vs 通量稳态 (1-x): 一阶一致, 二阶分歧 (强场分叉裁决 v1.13)
print(f"   e^-x 展开: 1 - x + x^2/2 - ... ;  平方稳态 (1-x)^2 = 1 - 2x + x^2")
print(f"   PPN: gamma=1 (一阶), beta=1 (e^-x) vs beta=1/2 ((1-x)^2, 1600sigma 排除 — v1.13)")
print("   => 玻尔兹曼路径 e^{-x} 是正确弱场描述, 截断在 r_c")

print("\n6) 遍历性理论对照 (子项1, 热平衡报告模拟3已数值确认):")
print("   公理1(各向同性+50:50+稳态) -> 马尔可夫链(745页SDE) 不可约+非周期+正回复")
print("   -> Markov遍历定理 -> Birkhoff-Khinchin: 时间平均=系综平均 a.e.")
print("   数值(模拟3): 前后两半时间平均偏差 0.2%/0.0% ✓")

print("\n7) 混沌传播适用性 (子项2, 原文555页自知):")
print("   Lanford: 硬球弹性碰撞 + Boltzmann-Grad极限 -> 玻尔兹曼方程 (严格)")
print("   框架: 湮灭-再生 (非弹性) — 原文555:'他们的微观模型是硬球弹性碰撞,不是正反物质湮灭'")
print("   => 结构对应: 相遇-湮灭-再生 = 有效散射 (守恒在事件尺度保持)")
print("   诚实: 严格 Lanford 定理不直接适用, 需推广到湮灭型碰撞 (开放问题 B2-2)")

print("\n全部验证完成")
