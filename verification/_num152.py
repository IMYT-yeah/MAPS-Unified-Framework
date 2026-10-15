# -*- coding: utf-8 -*-
"""
第 152 轮核验：论文数值恒等式的【独立对账】

缘起：用户问「找找还有什么是能算的」。
方法：论文 539 处含数字的断言（去重 334 种）→ 挑出【可从第一原理独立重算】的，
      逐条用 Python 重算，与论文所写比对。铁律 61（解析式须与直接测量比对）。

判据分组：
  A 组  R_c / l_P 的取值一致性（发现 C-94）
  B 组  E_c 的可复现性（发现 C-95）
  C 组  其余数值恒等式的独立验算
  D 组  登记状态与影响评估
  Z 组  论文零改动
"""
import io, os, re, math

BASE = os.path.dirname(os.path.abspath(__file__))
ZH   = os.path.join(BASE, "论文_正式稿_v3.0.md")
ZH_B = os.path.join(BASE, "论文_正式稿_v3.0_备份_2026-10-09第151轮前.md")
Q    = os.path.join(BASE, "项目台账.md")
HAND = os.path.join(BASE, "..", "环境说明.md")

B  = io.open(ZH,   encoding="utf-8").read()
BB = io.open(ZH_B, encoding="utf-8").read()
QY = io.open(Q,    encoding="utf-8").read()

RES = []
def chk(tag, name, cond, extra=""):
    RES.append(bool(cond))
    print("[{}] {:<6} {} {}".format("OK" if cond else "XX", tag, name, extra))
def info(tag, name, val=""):
    print("[--] {:<6} {} {}".format(tag, name, val))

# ---- 物理常数（外部标准值）----
c    = 2.99792458e8          # m/s
Mpc  = 3.0856775814913673e22 # m
tP   = 5.391247e-44          # s (CODATA 2018)
ly   = 9.4607304725808e15    # m
M_PL = 1.220910e19           # GeV

nu = 1.0 / tP
def H0_si(h0_kms):  return h0_kms * 1000.0 / Mpc     # s^-1

print("=" * 82)
print("A 组 · R_c/l_P：同一个比值，两个值？（铁律 10「口径写死」）")
print("=" * 82)

v_a = 8.45924e60   # §8.6.5 的写法
v_b = 8.4918e60    # §4.9 的写法
info("A-1", "ν = 1/t_P", "%.6e s^-1".format(nu))
h0a = nu / v_a * Mpc / 1000.0
h0b = nu / v_b * Mpc / 1000.0
info("A-2", "8.45924e60（§8.6.5）反推 H₀", "%.3f km/s/Mpc".format(h0a))
info("A-3", "8.4918e60（§4.9）反推 H₀",  "%.3f km/s/Mpc".format(h0b))
chk("A-1", "论文里 R_c/l_P 出现【两个不同数值】，且都未标注 H₀ 取值",
    abs(v_a - v_b) / v_b > 1e-3, "相对差 {:.3%}".format((v_b - v_a) / v_b))
chk("A-2", "两值分别精确对应 H₀ = 67.66 与 67.40 km/s/Mpc（Planck 2018 的两种组合）",
    abs(h0a - 67.66) < 0.05 and abs(h0b - 67.40) < 0.05,
    "{:.2f} / {:.2f}".format(h0a, h0b))

# A-3 论文 §8.6.1 的 R_c 与 H₀ 是否与 8.45924 自洽（= 67.66）
rc_gly = c / H0_si(67.66) / ly / 1e9
info("A-3", "c/H₀（H₀=67.66）", "{:.4f} Gly（论文 §8.6.1 写 14.4516 Gly）".format(rc_gly))
chk("A-3", "§8.6.1 的 R_c = 14.4516 Gly 与 H₀ = 2.1927e-18 自洽（⟹ 用的是 67.66）",
    abs(rc_gly - 14.4516) < 0.001 and abs(H0_si(67.66) - 2.1927e-18) / 2.1927e-18 < 1e-3)

# A-4 §8.6.5 内部自洽性
info("A-4", "H₀t_P（H₀=67.66）", "{:.5e}（论文写 1.18214e-61）".format(H0_si(67.66) * tP))
chk("A-4", "§8.6.5 内部自洽（8.45924e60 与 H₀t_P=1.18214e-61 同为 67.66）",
    abs(H0_si(67.66) * tP - 1.18214e-61) / 1.18214e-61 < 1e-3)

# A-5 下游量用的是哪一个？
info("A-5", "下游量实际所用 N_c（反推）：")
piNc2 = math.pi * v_b ** 2
h_val = v_b ** 2 * math.log(2.0)
info("A-5", "  用 8.4918e60 ⟹ πN_c²", "{:.4e}（论文写 2.265e122）".format(piNc2))
info("A-5", "  用 8.45924e60 ⟹ πN_c²", "{:.4e}".format(math.pi * v_a ** 2))
info("A-5", "  用 8.4918e60 ⟹ h = N_c²ln2", "{:.4e}（论文写 4.998e121）".format(h_val))
chk("A-5", "πN_c² 与 h 都用【8.4918e60】，而 §8.6.5 用 8.45924e60 ⟹ 同一稿内混用",
    abs(piNc2 - 2.265e122) / 2.265e122 < 0.01
    and abs(h_val - 4.998e121) / 4.998e121 < 0.01)
info("A-6", "混用的量级后果：0.38% 的输入差 ⟹ πN_c² 差 {:.2%}、N_c³ 差 {:.2%}".format(
    (math.pi * v_b**2 - math.pi * v_a**2) / (math.pi * v_b**2),
    (v_b**3 - v_a**3) / v_b**3))

print()
print("=" * 82)
print("B 组 · E_c = 1.0181 meV 能否用论文自己声明的数复现？")
print("=" * 82)

def Ec_meV(beta, eps0, M=M_PL):
    return M * eps0 ** (1.0 / beta) * 1e12   # GeV -> meV

info("B-1", "论文声明：β = 0.615；ε₀ 已统一为 7.731e-20；E_c = M_Pl·ε₀^(1/β)")
info("B-1", "  用 β=0.615、ε₀=7.731e-20 ⟹ E_c", "{:.4f} meV".format(Ec_meV(0.615, 7.731e-20)))
info("B-1", "  用 β=0.614790（精确）  ⟹ E_c", "{:.4f} meV".format(Ec_meV(0.614790, 7.731e-20)))
info("B-1", "  论文写", "1.0181 meV")
info("B-2", "  用【旧的】ε₀=7.7e-20、β=0.615 ⟹ E_c",
     "{:.4f} meV".format(Ec_meV(0.615, 7.7e-20)))
chk("B-1", "用【统一后的】ε₀=7.731e-20 复现不出 1.0181 meV（偏 0.66%）",
    abs(Ec_meV(0.615, 7.731e-20) - 1.0181) / 1.0181 > 0.004)
chk("B-2", "用【旧的】ε₀=7.7e-20 复现出 1.0178 meV ≈ 1.0181（偏 0.03%）⟹ 确认用了旧值",
    abs(Ec_meV(0.615, 7.7e-20) - 1.0181) / 1.0181 < 0.001)

# B-3 论文自己声明的纪律
chk("B-3", "⚠️ 论文 §8.1 自己写明「E_c 对 ε₀ 敏感，故此项须唯一」—— 它自设了这条纪律",
    "E_c 对 ε₀ 敏感" in BB and "此项须唯一" in BB)
# B-4 ε₀ 的统一声明
chk("B-4", "§8.1 同段声明 ε₀ 已「统一为由定义式算得的值」（= 7.731e-20）",
    "现统一为" in BB and "7.731" in BB)

# B-5 正解应是多少
info("B-5", "⟹ 若严格执行自设纪律，E_c 应为",
     "{:.4f} meV（论文写 1.0181）".format(Ec_meV(0.615, 7.731e-20)))

print()
print("=" * 82)
print("C 组 · 其余数值恒等式的独立验算（全部应通过）")
print("=" * 82)

# C-1 16 ln2
info("C-1", "16 ln 2", "{:.5f}（论文 11.0904）".format(16 * math.log(2)))
chk("C-1", "16 ln 2 = 11.0904", abs(16 * math.log(2) - 11.0904) < 5e-5)
# C-2 0.3607 bit/面元
info("C-2", "1/4 纳特 → 比特", "{:.5f}（论文 0.3607）".format(0.25 / math.log(2)))
chk("C-2", "0.3607 = (1/4 nat)/ln2", abs(0.25 / math.log(2) - 0.3607) < 5e-5)
# C-3 k = e^{1/4}
info("C-3", "e^(1/4) / 2^(1/4)", "{:.5f} / {:.5f}（论文 1.2840 / 1.1892）".format(
    math.exp(0.25), 2 ** 0.25))
chk("C-3", "k = e^(1/4) = 1.2840 且 2^(1/4) = 1.1892", abs(math.exp(0.25) - 1.2840) < 5e-5)
# C-4 π/ln2
info("C-4", "π/ln 2", "{:.5f}（论文 4.532）".format(math.pi / math.log(2)))
chk("C-4", "π/ln 2 = 4.532", abs(math.pi / math.log(2) - 4.532) < 5e-4)
# C-5 2e
info("C-5", "2e", "{:.5f}（论文 b_min = 5.436 GM/c²）".format(2 * math.e))
chk("C-5", "2e = 5.436（论文为 3 位有效数字写法）", abs(2 * math.e - 5.436) < 1e-3)
# C-6 N_c³
info("C-6", "N_c³（8.4918e60）", "{:.5e}（论文 6.1236e182）".format(v_b ** 3))
chk("C-6", "N_c³ = 6.1236e182", abs(v_b ** 3 - 6.1236e182) / 6.1236e182 < 1e-3)
# C-7 串行归一化的倍数
r_serial = 2.0 / v_b ** 3
info("C-7", "2/N_c³（每个格点每 tick 被碰概率）", "{:.4e}".format(r_serial))
info("C-7", "  其倒数", "{:.4e}（论文写 3.06e182）".format(1 / r_serial))
chk("C-7", "1/(2/N_c³) = 3.06e182 ⟹ 论文串行判据组内部自洽",
    abs(1 / r_serial - 3.06e182) / 3.06e182 < 0.02)
# C-8 4 t_P 内交换概率
info("C-8", "4 × (2/N_c³)", "{:.4e}（论文写 1.3e-182）".format(4 * r_serial))
chk("C-8", "4 t_P 内被交换概率 = 1.3e-182", abs(4 * r_serial - 1.3e-182) / 1.3e-182 < 0.05)
# C-9 ḣ = h/t_P
info("C-9", "h/t_P（h=4.998e121）", "{:.4e}（论文 9.27e164）".format(4.998e121 / tP))
chk("C-9", "ḣ = h/t_P = 9.27e164", abs(4.998e121 / tP - 9.27e164) / 9.27e164 < 0.01)
# C-10 β
info("C-10", "β = log10(6e-10)/log10(1e-15)", "{:.6f}（论文 0.615）".format(
    math.log10(6e-10) / math.log10(1e-15)))
chk("C-10", "β = 0.615（三位）与精确 0.614790 一致", abs(math.log10(6e-10)/math.log10(1e-15) - 0.61479) < 1e-5)
# C-11 ε₀
eps0_calc = 6e-10 / (M_PL / 1e3) ** (math.log10(6e-10) / math.log10(1e-15))
info("C-11", "ε₀ = ε(1TeV)/(M_Pl/1TeV)^β", "{:.4e}（论文 7.731e-20）".format(eps0_calc))
chk("C-11", "ε₀ = 7.73e-20", abs(eps0_calc - 7.731e-20) / 7.731e-20 < 5e-3)
# C-12 b_min 与 EHT 比较
info("C-12", "5.436 vs EHT 5.2±0.3", "偏 {:.2%}".format((2*math.e - 5.2) / 5.2))
chk("C-12", "b_min 偏 EHT 中心值 +4.55%", abs((2*math.e - 5.2)/5.2 - 0.0455) < 5e-4)

print()
print("=" * 82)
print("D 组 · 登记状态")
print("=" * 82)

chk("D-1", "C-94 尚未登记（清单里无 'C-94'）", "C-94" not in QY)
info("D-2", "论文里 '8.4918' 出现次数", str(B.count("8.4918")))
chk("D-2", "论文里 '8.4918' 出现 2 处、'8.459' 出现 1 处", B.count("8.4918") == 2 and B.count("8.459") == 1)
chk("D-3", "论文里没有任何一处写明 H₀ 的取值（'67.4'/'67.66' 各 0 处）",
    "67.4" not in B and "67.66" not in B)

print()
print("=" * 82)
print("Z 组 · 底本状态")
print("=" * 82)
chk("Z-1", "本轮未改动论文（当前稿 = 备份，逐字相同）", B == BB, "len {} vs {}".format(len(B), len(BB)))

print()
n_ok = sum(RES)
print("通过 {} 项，失败 {} 项".format(n_ok, len(RES) - n_ok))
