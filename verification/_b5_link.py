# -*- coding: utf-8 -*-
"""
B5 最后一环：观测者计数 vs F3 归一化，差一个 ln2（2026-09-17）
=================================================================
两端：
  【因果/观测者端】B5_观测者模型（原文 1651–1653 页）
      面元数 = A/l_P²；可读 4 bits/面元；相干块 = 4 面元 × 4 方向 = 16；
      每相干块 1 **bit** ⟹ 熵密度 0.25 bit/面元 ⟹ S/k_B = (A/4l_P²)·ln2
  【统计/F3 端】通量管相干块计数 + Bekenstein-Hawking 归一化
      S/k_B = A/(4l_P²)     ⟹ 每 4l_P² 是 1 **nat**（不是 1 bit）

BL-1  两端数值对比（太阳质量黑洞）
BL-2  用 Hawking 温度裁决：哪个对？
BL-3  若保 B5 的比特计数，压缩因子必须是多少？
BL-4  若保 16 倍压缩，每面元的原始计数必须是多少？
BL-5  判决与修正方案
"""
import math

c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
kB = 1.380649e-23
lP2 = hbar * G / c ** 3
Msun = 1.98892e30
LN2 = math.log(2)


def line(t):
    print("\n" + "=" * 74)
    print(t)
    print("=" * 74)


def chk(name, got, want, tol=1e-9):
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    print("  [%s] %-48s got=%.10g  want=%.10g" % ("OK" if ok else "XX", name, got, want))
    return ok


M = Msun
Rs = 2 * G * M / c ** 2
A = 4 * math.pi * Rs ** 2
n_cell = A / lP2                       # 面元数 A/l_P²
n_block = A / (4 * lP2)                # 相干块数 = 面元数/4

# ---------------------------------------------------------------- BL-1
line("BL-1  两端数值对比（太阳质量黑洞，Rs = %.4f km）" % (Rs / 1e3))
print("  A = %.6g m² ；面元数 A/l_P² = %.6g ；相干块数 A/(4l_P²) = %.6g"
      % (A, n_cell, n_block))
S_bh = n_block                          # S/k_B = A/(4l_P²)，单位：nat
S_obs = n_block * LN2                   # B5 观测者端：块数 × 1 bit = 块数 × ln2 nat
print()
print("  【统计/F3 端】S/k_B = A/(4l_P²)          = %.6g nat   （每块 1 nat）" % S_bh)
print("  【观测者端】  S/k_B = (A/4l_P²)·ln2      = %.6g nat   （每块 1 bit）" % S_obs)
print("  ⟹ 比值 = %.6f = ln2 ⟹ **两端差一个 ln2 = %.4f**" % (S_obs / S_bh, LN2))
print()
print("  注：README 写『S = A/(4l_P²)·ln2 ⇒ 太阳黑洞 1.05e77 纳特』——")
print("      公式带 ln2，但数字 %.4g 是不带 ln2 的。**README 自身就自相矛盾。**" % S_bh)

# ---------------------------------------------------------------- BL-2
line("BL-2  用 Hawking 温度裁决")
T_std = hbar * c ** 3 / (8 * math.pi * G * M * kB)
T_from_bh = c ** 6 * lP2 / (8 * math.pi * kB * G ** 2 * M)          # 由 S=A/(4l_P²) 反推
T_from_obs = c ** 6 * lP2 / (8 * math.pi * kB * G ** 2 * M * LN2)   # 由 S=(A/4l_P²)ln2 反推
print("  标准 Hawking：T = ℏc³/(8πGMk_B) = %.6g K" % T_std)
print("  由 S = A/(4l_P²)（每块 1 nat）   ⟹ T = %.6g K   偏差 %+.2f%%"
      % (T_from_bh, 100 * (T_from_bh - T_std) / T_std))
print("  由 S = (A/4l_P²)ln2（每块 1 bit）⟹ T = %.6g K   偏差 %+.2f%%"
      % (T_from_obs, 100 * (T_from_obs - T_std) / T_std))
print()
chk("每块 1 nat ⟹ 正确 Hawking 温度", T_from_bh, T_std, 1e-12)
print("  ⟹ **裁决：每 4l_P² 是 1 纳特，不是 1 比特。**")
print("     观测者端的『每相干块 1 bit』必须改为『每相干块 1 nat』，")
print("     否则 Hawking 温度高 %.1f%%。" % (100 * (T_from_obs - T_std) / T_std))

# ---------------------------------------------------------------- BL-3
line("BL-3  若保留『4 bits/面元』的原始计数，压缩因子必须是多少？")
target_nat_per_cell = 1.0 / 4                      # BH: 0.25 nat/面元
target_bit_per_cell = target_nat_per_cell / LN2    # 换成比特单位
raw_bits = 4.0                                     # B5 的可读计数
comp_need = raw_bits / target_bit_per_cell
print("  目标（BH）：0.25 nat/面元 = 0.25/ln2 = %.6f bit/面元" % target_bit_per_cell)
print("  原始可读：%.0f bits/面元（4 方向）" % raw_bits)
print("  ⟹ 需要的压缩因子 = 4/%.6f = **%.6f**" % (target_bit_per_cell, comp_need))
print("  对照 B5 声称的 16 ；比值 = %.6f = **16·ln2**" % (comp_need / 16))
print("  ⟹ 压缩因子不是 16，而是 **16 ln2 = %.4f**（若坚持用比特为单位）。" % comp_need)

# ---------------------------------------------------------------- BL-4
line("BL-4  若保留『16 倍压缩』，原始计数必须是多少？")
raw_need = 16 * 0.25                               # 16 × 0.25 = 4
print("  目标 0.25 nat/面元 × 16 = **%.4f nat/面元**" % raw_need)
print("  即：原始可读应为『4 **纳特**/面元』，不是『4 比特/面元』")
print("  （4 nat/面元 ⟹ 每面元 e⁴ ≈ %.1f 个微观态）" % math.exp(4))
print()
print("  ⚠️ 两种修法都不漂亮：")
print("     (i) 保比特计数 ⟹ 压缩因子 16ln2 = 11.09，失去『4×4=16』的优雅")
print("     (ii) 保 16 压缩 ⟹ 原始计数变『4 纳特/面元』，失去『4 方向 = 4 比特』的自然性")

# ---------------------------------------------------------------- BL-5
line("BL-5  判决")
print("""  ✅ **最后一环找到了，而且是一个可裁决的分歧，不是"说不清"。**
     · 观测者端（B5）给 S/k_B = (A/4l_P²)·ln2（每相干块 1 bit）
     · 统计端（F3/BH）给 S/k_B = A/(4l_P²)（每相干块 1 nat）
     · **两者差 ln2 = %.4f**；README 自身也自相矛盾（公式带 ln2、数字不带）
     · **Hawking 温度裁决：每块必须是 1 纳特**（否则 T 高 44%%）""" % LN2)
print("""
  ⟹ 修正方案（建议取 ii 的变体）：
     把 B5 的『每相干块 1 bit』改为『每相干块 1 纳特』，
     并相应把『4 bits/面元 + 16 倍压缩』改写为
     『4 纳特/面元 + 16 倍压缩』（或等价地『4 bit/面元 + 16ln2 倍压缩』）。

  ⚠️ 代价：B5 那条『可读 4 方向 ⟹ 4 bits ⟹ 相干 16 倍 ⟹ 0.25 bit』的
     数字链条有一环要改。**但换来的是与 Hawking 温度、与 F3、与 β=1/(2π) 全链一致。**

  ⟹ 这不算把 B5 推翻 —— B5 的**方法**（体=表面投影 ⟹ 面积律；相干压缩 ⟹ 每 4 面元一个单位）
     全部保留，只是那个「单位」是**纳特**而非**比特**。
""")
