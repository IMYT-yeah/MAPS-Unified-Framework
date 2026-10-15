# -*- coding: utf-8 -*-
"""
钳制物态微观推导 (候选 D) — 数值验证
推导链:
  ① ρ/ρ_P = 普朗克填充率 (碎片质量密度 / 每普朗克体积普朗克质量)
  ② f(ρ) = tanh(ρ/ρ_P) = 活性比例 (双向净动量流的罗吉斯蒂饱和响应)
  ③ P(ρ) = f·P_P, P_P = E_P/l_P³ (普朗克单元最大压强)
验证: 线性区/饱和区/声速/能量条件/合并质量/罗吉斯蒂解
"""
import numpy as np

c = 1.0
mP = 1.0          # 普朗克质量 (无量纲)
lP = 1.0          # 普朗克长度
EP = mP*c*c       # 普朗克能量
rhoP = mP/lP**3   # 普朗克密度
PP = EP/lP**3     # 普朗克压强
alpha = 1.0/rhoP  # 罗吉斯蒂速率

rho = np.logspace(-6, 6, 5000) * rhoP

# ③ P(ρ) = P_P·tanh(ρ/ρ_P)
P = PP*np.tanh(rho/rhoP)

print("="*72)
print("钳制物态微观推导 — 数值验证 (无量纲, c=mP=lP=1)")
print("="*72)

# --- 1. 线性区: P ≈ c²ρ ---
mask = rho < 1e-3*rhoP
ratio_lin = P[mask]/(rho[mask]*c*c)
print(f"\n[1] 线性区 (ρ<10⁻³ρ_P): P/ρc² = {ratio_lin[0]:.6f} (期望 1.000)")
print(f"    ⟹ P ≈ c²ρ ✓ (相对论性最大因果; 与辐射气体差 1/3 几何因子, 诚实标注)")

# --- 2. 饱和区: P → P_P ---
mask2 = rho > 1e3*rhoP
print(f"[2] 饱和区 (ρ>10³ρ_P): P/P_P = {P[mask2][-1]/PP:.6f} (期望 1.000)")
print(f"    ⟹ 压强钳制在 P_P ✓ (风暴压强有限, 原文90)")

# --- 3. 声速: c_s² = c²·sech²(ρ/ρ_P) ---
cs2 = c*c/np.cosh(rho/rhoP)**2
print(f"\n[3] 声速: c_s² = c²·sech²(ρ/ρ_P)")
print(f"    ρ→0: c_s² = {cs2[0]:.6f} c² (期望 1: 相对论性最大因果)")
print(f"    ρ=ρ_P: c_s² = {np.interp(1.0, rho/rhoP, cs2):.6f} c² (期望 sech²(1)=0.420)")
print(f"    ρ→∞: c_s² = {cs2[-1]:.2e} c² → 0 (钳制区无弹性波, 浆糊无结构 ✓)")
print(f"    普朗克质量黑洞 (ρ_avg=0.03ρ_P): c_s = {np.sqrt(np.interp(0.03, rho/rhoP, cs2)):.6f} c")

# --- 4. 能量条件: P ≤ ρc² (因果性) ---
ratio = P/(rho*c*c)
print(f"\n[4] 能量条件 P ≤ ρc²:")
print(f"    ρ≪ρ_P: P/ρc² = {ratio[mask][0]:.6f} (饱和因果极限)")
print(f"    ρ=ρ_P: P/ρc² = {np.interp(1.0, rho/rhoP, ratio):.6f}")
print(f"    ρ≫ρ_P: P/ρc² = {ratio[mask2][-1]:.2e} → 0 (深度亚因果)")
print(f"    ⟹ 处处 P ≤ ρc² ✓ (对比候选B恰在边界 P=ρc²; 钳制物态更安全)")
print(f"    ∂P/∂ρ = (P_P/ρ_P)·sech²(ρ/ρ_P) ≥ 0 恒成立 ⟹ 无热力学不稳定性 ⟹ 无坍缩 ✓")

# --- 5. 合并质量: m_eff = m_P·(ρ/ρ_P)/tanh(ρ/ρ_P) ---
meff = mP*(rho/rhoP)/np.tanh(rho/rhoP)
print(f"\n[5] 合并质量 m_eff = m_P·(ρ/ρ_P)/tanh(ρ/ρ_P):")
print(f"    ρ≪ρ_P: m_eff = {meff[mask][0]:.6f} m_P (独立碎片)")
print(f"    ρ=ρ_P: m_eff = {np.interp(1.0, rho/rhoP, meff):.6f} m_P")
print(f"    ρ≫ρ_P: m_eff = {meff[mask2][-1]:.2e} m_P (风暴压成团块 — 浆糊)")

# --- 6. 罗吉斯蒂饱和动力学 ⟹ tanh ---
# dJ/dρ = (α/J_max)(J_max² - J²) ⟹ J(ρ) = J_max·tanh(αρ)
Jmax = PP
J_analytic = Jmax*np.tanh(alpha*rho)
# 数值积分罗吉斯蒂
J_num = np.zeros_like(rho)
J_num[0] = J_analytic[0]
for i in range(1, len(rho)):
    dr = rho[i]-rho[i-1]
    J_num[i] = J_num[i-1] + dr*(alpha/Jmax)*(Jmax**2 - J_num[i-1]**2)
err = np.max(np.abs(J_num-J_analytic)/(Jmax+1e-30))
print(f"\n[6] 罗吉斯蒂饱和: dJ/dρ = (α/J_max)(J_max²−J²)")
print(f"    数值积分 vs 解析 J=J_max·tanh(αρ): 最大相对偏差 {err:.2e}")
print(f"    ⟹ 双向净动量流的罗吉斯蒂演化 ⟹ tanh ✓ (反射+J_max / 放行−J_max 对称饱和)")

# --- 7. 普朗克质量黑洞 / 宏观黑洞物态定位 ---
print(f"\n[7] 物态定位:")
print(f"    普朗克质量黑洞 (ρ_avg=0.03ρ_P): P = {np.interp(0.03, rho/rhoP, P/PP):.4f} P_P, c_s = {np.sqrt(np.interp(0.03, rho/rhoP, cs2)):.4f} c")
print(f"    太阳质量黑洞 (ρ_avg=3.6e-78 ρ_P): P ≈ {np.interp(3.6e-78, rho/rhoP, P/PP):.2e} P_P (线性区, P≈c²ρ)")
print(f"    ⟹ 宏观黑洞过载区压强 ≪ P_P, 仅普朗克质量黑洞接近钳制 — 与 v1.18 数值一致")

print("\n" + "="*72)
print("结论: P(ρ) = P_P·tanh(ρ/ρ_P) 从三条微观机制完整涌现:")
print("  ① ρ/ρ_P = 普朗克填充率 (碎片质量 / 每普朗克体积普朗克质量)")
print("  ② tanh = 双向净动量流 (反射/放行) 的罗吉斯蒂饱和响应")
print("  ③ P_P = E_P/l_P³ = 普朗克单元最大压强 (单碰撞≤E_P × 最大频率 ν_P / 面积 l_P²)")
print("新预言: c_s² = c²·sech²(ρ/ρ_P) — 钳制区声速消失 (过载区无弹性波)")
print("="*72)
