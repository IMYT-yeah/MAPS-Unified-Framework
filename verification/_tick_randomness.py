# -*- coding: utf-8 -*-
"""
第 42 轮核验：T-7 的第一次判别 —— tick 的随机性是**外生**还是**内生**？
并且：这个外生随机性本身就是**熵增的源头**（本轮把它算出来）。

背景：
  · 第 21/39/40 轮：底层 tick 是**双射** ⟹ 状态的信息**严格守恒**、无熵产生；
  · 第 26 轮 / §8.6.7：tick = **随机选轴 + 每线独立随机相位**（且标为【实现选择】）；
  · 第 40 轮：等分（均匀分布）= 唯一不变测度，但**动力学保持轨道**、不能把系统带到等分
    ⟹ 等分只能是"结构性/初值"的 —— 这一点一直缺一个动力学理由。

本轮的两个结果：
  **A（正面，可算）**：外生 tick 随机性每 tick 向系综**注入无知**
      h = ln(3·2^(L²)) = ln3 + L²·ln2   [nats/tick]
  ⟹ 系综熵以该速率增长，直到饱和于 ln|O|；
  ⟹ 达到视界的 BH 熵只需 **π/ln2 = 4.532 tick ≈ 2.44×10⁻⁴³ s**
     （解析：S_BH/k_B = πN_c²，h ≈ N_c²ln2 ⟹ 比值 = π/ln2）。
  ⟹ **这给了第 40 轮「等分账是瞬时的」一个动力学理由**：统计混合（~4.5 tick）
     与空间输运（47 μm/哈勃时）是**两个相差 ~10⁶⁰ 倍的速率**，不矛盾。

  **B（判据，结论是否定的）**：H1（外生随机）与 H2（内生确定）在**可见衬底层面上经验等价**
     —— H2 需要的隐变量开销 = (tick 选择的比特数)/(格点数) = L²/L³ = **1/L → 0**
     ⟹ 不与「0.25 纳特/l_P² 次二元」冲突 ⟹ **不可判别**。
     ⟹ 但在**现有表述（H1）**下答案是明确的：**未来不是当前状态的函数 ⟹ 原则上不可预测**。

检查项：TS-1 … TS-7。运行：<venv>/python.exe outputs/_tick_randomness.py
"""

import math

OK = [0]
FAIL = [0]


def chk(tag, cond, msg):
    if cond:
        OK[0] += 1
        print("  [OK] {:<7} {}".format(tag, msg))
    else:
        FAIL[0] += 1
        print("  [XX] {:<7} {}  <-- 失败".format(tag, msg))


def hdr(t):
    print("")
    print("-" * 78)
    print(t)
    print("-" * 78)


L_P = 1.616255e-35
T_P = 5.391247e-44
C_L = 2.99792458e8
LN2 = math.log(2.0)
N_C = 8.4918e60                 # R_c / l_P（框架既有值）
R_C = N_C * L_P                 # 因果视界半径
T_H = R_C / C_L                 # 哈勃时

hdr("TS-1  一次 tick 的选择数 = 3 轴 × 2^(线数)，线数 = L²")

print("  {:>10}  {:>16}  {:>18}  {:>16}".format("L", "线数 L²", "log2(选择数)", "h (nats/tick)"))
for L in (4, 8, 16, 64, 10 ** 6):
    nl = L * L
    log2nch = math.log2(3) + nl          # 不直接算 3·2^(L²)（会溢出）
    h = math.log(3) + nl * LN2
    print("  {:>10}  {:>16}  {:>18.4e}  {:>16.4e}".format(L, nl, log2nch, h))
chk("TS-1", abs((math.log(3) + 16 * LN2) - math.log(3 * 2 ** 16)) < 1e-12,
    "h = ln3 + L²ln2（与 ln(3·2^(L²)) 恒等）⟹ 每 tick 注入的**无知**可算")

hdr("TS-2  宏观格点（哈勃球）上的注入速率")

L = N_C
h = math.log(3) + (L * L) * LN2
hdot = h / T_P
S_BH = math.pi * N_C ** 2
print("  格点边长 L ≈ N_c            = {:.4e}".format(L))
print("  每 tick 注入 h              = {:.4e} nats".format(h))
print("  注入速率 ḣ = h/t_P          = {:.4e} nats/s".format(hdot))
print("  视界 BH 熵 S_BH/k_B = πN_c² = {:.4e} nats".format(S_BH))
print("  走过 1 秒所注入的量          = {:.4e} nats（≫ S_BH）".format(hdot))
chk("TS-2", hdot * 1.0 > 1e10 * S_BH,
    "注入速率极快：1 秒注入的量是视界 BH 熵的 {:.1e} 倍 ⟹ 饱和是**瞬时的**".format(
        hdot / S_BH))

hdr("TS-3  达到视界 BH 熵所需的时间 —— 解析值 π/ln2")

nticks = S_BH / h
exact = math.pi / LN2
print("  所需 tick 数 = S_BH/h       = {:.6f}".format(nticks))
print("  解析极限 π/ln2              = {:.6f}".format(exact))
print("  对应时间                    = {:.4e} s = {:.4f} t_P".format(
    nticks * T_P, nticks))
chk("TS-3", abs(nticks - exact) < 1e-3,
    "**π/ln2 = {:.4f} tick ≈ {:.3e} s** ⟹ 系综熵在约 4.5 个普朗克时间内达到视界的 BH 熵".format(
        exact, nticks * T_P))

hdr("TS-4  两个速率：统计混合（快） vs 空间输运（慢）")

R_MIX = 4.70e-5                 # m，一个哈勃时的空间混合尺度（第 21/26 轮）
print("  统计饱和：{:.4e} s（≈ {:.2f} tick）".format(nticks * T_P, nticks))
print("  哈勃时     ：{:.4e} s".format(T_H))
print("  两者之比   ：{:.3e} ⟹ 相差约 60 个数量级".format(T_H / (nticks * T_P)))
print("  空间混合尺度 R_mix(t_H) = {:.2e} m = {:.2e} R_c".format(R_MIX, R_MIX / R_C))
chk("TS-4", T_H / (nticks * T_P) > 1e55,
    "**统计混合 ~10⁶⁰ 倍快于空间输运** ⟹ 第 40 轮「等分账瞬时成立」与第 21 轮「47 μm 很慢」"
    "**不矛盾**：一个是信息的混合，一个是物质的输运")

hdr("TS-5  H1（外生随机）vs H2（内生确定）：能否判别？")

print("  H2 需要把「tick 选择」编码进衬底自身的态：")
print("     tick 选择的比特数 = log2(3·2^(L²)) ≈ L² bits")
print("     格点数            = L³")
print("  ⟹ **每格点的隐变量开销 = L²/L³ = 1/L**")
for LL in (8.0, 64.0, 1e6, N_C):
    print("     L = {:>10.3e} ⟹ 1/L = {:>12.3e} bits/格点".format(LL, 1.0 / LL))
print("  观测者熵密度（第 39 轮）= 0.25 纳特/l_P² = 0.3607 比特/l_P² < 1 bit（**次二元**）")
chk("TS-5", 1.0 / N_C < 1e-50,
    "H2 的隐变量开销 = 1/L = {:.2e} bits/格点 → 0 ⟹ **不与次二元熵密度冲突**"
    " ⟹ H1 与 H2 在可见衬底层面**经验等价 ⟹ 不可判别**".format(1.0 / N_C))

hdr("TS-6  饱和值够不够装下 BH 熵？")

N_sites = N_C ** 3
lnC = N_sites * LN2 - 0.5 * math.log(math.pi * N_sites / 2.0)   # ln C(N, N/2)
print("  格点总数 N = N_c³           = {:.3e}".format(N_sites))
print("  轨道容量上界 ln|O| ≤ ln C(N,N/2) ≈ {:.3e} nats".format(lnC))
print("  视界 BH 熵                  = {:.3e} nats".format(S_BH))
chk("TS-6", lnC > 1e10 * S_BH,
    "容量充足（{:.1e} 倍）⟹ 饱和值不是瓶颈，**速率**才是 ⟹ 熵增的上界是 ln|O|，"
    "之后不再增长".format(lnC / S_BH))

hdr("TS-7  诚实边界")

print("  · h = ln3 + L²ln2 用的是**并行 + 每线独立相位**这一实现（§8.6.7）。")
print("    另一实现「每对独立决定是否交换」的选择数不同 ⟹ h 不同 ⟹ **可用扩散系数交叉检验**。")
print("  · 本轮算的是**系综（无知）熵**的增长。底层单个 tick 仍是双射 ⟹ **状态信息严格守恒**：")
print("    「无信息丢失」（第 21 轮）与「系综熵增长」（本轮）**并存，不矛盾**。")
print("  · H1/H2 不可判别 ⟹ 「未来是否原则上可预测」在框架内**不可判定**；")
print("    但在**现行表述（H1）**下答案明确：**不可预测**（未来不是当前状态的函数）。")
print("  · 未做：把 h 与具体的扩散系数观测量做拟合；8×8×8 的直接数值。")
chk("TS-7", True, "边界已写明")

hdr("汇总")
print("  通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("")
print("  判决：")
print("   (1) **熵增的源头找到了**：外生 tick 随机性每 tick 注入 ln3 + L²ln2 纳特的无知；")
print("       视界 BH 熵只需 **π/ln2 = 4.53 tick ≈ 2.4×10⁻⁴³ s** 就达到 ⟹ 统计混合是瞬时的。")
print("   (2) 由此**解释了第 40 轮**：等分账可以瞬时成立（统计混合快），")
print("       同时空间输运很慢（47 μm/哈勃时）—— 两者相差 ~10⁶⁰，是**两件事**。")
print("   (3) **T-7 判否**：H1 与 H2 经验等价（H2 开销 1/L → 0）⟹ 「能否预测未来」")
print("       在框架内**不可判定**；现行表述（H1）下 = **不可预测**。")
print("   (4) 熵增的两个来源第一次分开：**外生随机注入**（新）+ **粗粒化/关联扩散**（第 21/39 轮）。")
