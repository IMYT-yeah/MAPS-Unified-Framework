# -*- coding: utf-8 -*-
"""
遗留四项进攻：数值复核
1) beta_ppn 符号复核：玻尔兹曼分布 rho/rho_inf = e^{-x} 的展开
2) k 单位澄清：纳特 e^{1/4} vs 比特 2^{1/4}
3) 玻尔兹曼分布的物理检验
"""
import math

print("="*70)
print("1) beta_ppn 符号复核（关键！）")
print("="*70)
# PPN (Will 约定, U>0): g_00 = -(1 - 2U/c^2 + 2*beta*(U/c^2)^2) = -(1 - 2x + 2*beta*x^2)
# 框架: g_00 = -(rho/rho_inf)^2
# 若 rho/rho_inf = 1 - x + a*x^2:
#   g_00 = -(1 - 2x + (2a+1)x^2)  ->  2*beta = 2a+1  ->  beta = a + 1/2
print("PPN 约定: g_00 = -(1 - 2x + 2*beta*x^2),  x = U/c^2 = GM/(c^2 r)")
print("框架: g_00 = -(rho/rho_inf)^2")
print("若 rho/rho_inf = 1 - x + a*x^2:")
print("  g_00 = -(1 - 2x + (2a+1)x^2)")
print("  对照: 2*beta = 2a+1  =>  beta = a + 1/2")
print("  要 beta=1: a = +1/2  (不是 -3/2!)")
print()
print("--- 玻尔兹曼分布检验: rho/rho_inf = e^{-x} ---")
def taylor_exp(n):
    # e^{-x} 展开到 n 阶
    return sum((-1)**k * x**k/math.factorial(k) for k in range(n+1))
x = 0.1
print(f"x=0.1: e^(-x) = {math.exp(-x):.6f}")
print(f"       1-x+x^2/2 = {1-x+x**2/2:.6f}  (二阶近似)")
print(f"       (e^{-x})^2 = e^(-2x) = {math.exp(-2*x):.6f}")
print(f"       1-2x+2x^2 = {1-2*x+2*x**2:.6f}  (对应 beta=1)")
print(f"       1-2x = {1-2*x:.6f}  (无二阶项, beta=0)")
print()
print("=> 玻尔兹曼分布 rho/rho_inf = e^{-x} 给出:")
print("   g_00 = -e^{-2x} = -(1 - 2x + 2x^2 - (4/3)x^3 + ...)")
print("   2*beta = 2  =>  beta = 1  ✓✓✓")
print("   二阶系数 a = +1/2 (e^{-x} 展开: 1 - x + x^2/2)")
print()
print("=== 重要更正: P3-D 报告中的 a=-3/2 有符号错误 ===")
print("   正确: a = +1/2, 来自玻尔兹曼分布 rho ∝ e^{-Phi/c^2}")
print("   物理: 通量密度按引力势的玻尔兹曼权重衰减!")
print("   连接: 热力学(玻尔兹曼) -> 引力几何(PPN beta=1) - 与 P3-A 的 Jacobson 路径统一")

print()
print("="*70)
print("2) k 单位澄清: 纳特 vs 比特")
print("="*70)
# S = A/(4 l_P^2) 是纳特(无量纲, k_B 吸收)
# 若用比特: S_bit = A/(4 l_P^2 * ln 2)
# 每面元: N = A/l_P^2, ln k = 1/4 (纳特) 或 ln k = ln 2 / 4 (比特)
k_nat = math.exp(0.25)
k_bit = 2**0.25
print(f"纳特版本: ln k = 1/4 => k = e^(1/4) = {k_nat:.4f}")
print(f"比特版本: ln k = (ln 2)/4 => k = 2^(1/4) = {k_bit:.4f}")
print(f"每 4 个普朗克面积: 纳特 {0.25:.4f} nat = {0.25/math.log(2):.4f} bit")
print(f"原文'每 4 个普朗克面积 1 比特'= 比特版本 (k=2^(1/4))")
print(f"S_BH = A/(4l_P^2) 是纳特; 换算比特: S_bit = S_nat/ln 2")
print()
print("--- 1/4 与框架 4 分量结构的可能连接 ---")
print("框架: 4 分量 = 时间双向(2) x 手性双向(2), Clifford 代数")
print("候选: '每 4 个普朗克面积 1 比特' 中的 4 = 4 分量单元的面积")
print("  - 一个完整 4 分量耦合单元(时间x手性全确定)占用 4 个普朗克面元")
print("  - 每个单元携带 1 比特(相位符号)")
print("  => S = (A/4l_P^2) * ln 2 (比特), 即 k = 2^(1/4)")

print()
print("="*70)
print("3) 玻尔兹曼分布的物理自洽检验")
print("="*70)
# rho/rho_inf = e^{-Phi/c^2}, Phi = GM/r
# 引力红移: f(r)/f_inf = sqrt(-g00) = e^{-x} (与玻尔兹曼权重一致!)
# 检验: 太阳表面
G = 6.674e-11; M_sun = 1.989e30; R_sun = 6.957e8; c = 3e8
x_sun = G*M_sun/(c**2*R_sun)
print(f"太阳表面 x = GM/(c^2 R) = {x_sun:.3e}")
print(f"e^(-x) - (1-x) = {math.exp(-x_sun)-(1-x_sun):.3e}  (二阶差, 极小)")
print(f"相对论修正量级: e^(-2x) vs (1-2x) 差 = {math.exp(-2*x_sun)-(1-2*x_sun):.3e}")
print(f"PPN beta 检验: beta = (2a+1)/2, a=1/2 => beta = 1.0")
print()
print("--- 玻尔兹曼 vs Schwarzschild 精确 ---")
print("e^{-2x} = 1-2x+2x^2-... (有全部高阶项)")
print("Schwarzschild 坐标 g_00 = -(1-2x) (精确, 无高阶项)")
print("两者 PPN 参数相同 (beta=1), 但精确形式不同")
print("框架主张: 通量密度按玻尔兹曼分布 -> g_00 = -e^{-2Phi/c^2}")
print("这是框架可检验的新预测: 强场 g_00 与 Schwarzschild 的偏离")
x_bh = 0.3  # 中子星表面
print(f"中子星 (x=0.3): e^(-2*0.3) = {math.exp(-0.6):.4f} vs (1-0.6) = {1-0.6:.4f} (差 {(1-0.6)-math.exp(-0.6):.4f})")
print(f"  差异 ~{abs((1-0.6)-math.exp(-0.6))/math.exp(-0.6)*100:.1f}% -> 强场可检验!")
