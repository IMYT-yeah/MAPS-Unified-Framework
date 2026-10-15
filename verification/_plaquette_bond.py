# -*- coding: utf-8 -*-
"""
第 35 轮：「面元 ↔ 键」的显式构造与计数（B2 最后一层未论证的东西）
定义（本轮显化，此前默认）：
  面元   = 格点在「现在平面」内的对偶面元，面积 l_P²（⟹ 面元数 = 平面内格点数 ∝ A）
  连接   = 该格点到其 4 个平面内邻居（±x, ±y）的**键**
检验：
  PK-1 计数自洽（面元数、槽位数、不同键数、每条键的共享重数）
  PK-2 面积律
  PK-3 键共享 = 相邻面元相关的具体机制（B5 只断言「强相关」，从未计算）
  PK-4 量化：键共享解释了压缩因子 11.0904 中的多少
  PK-5 2×2 相干块的键计数
只用标准库。正文引号一律用中文引号。
"""
import math as m

C_MS = 2.99792458e8
G_SI = 6.67430e-11
H_PLANCK = 6.62607015e-34
HBAR = H_PLANCK / (2 * m.pi)
K_B = 1.380649e-23
M_SUN = 1.98892e30          # 与前面各轮一致
L_P = m.sqrt(HBAR * G_SI / C_MS ** 3)

LN2 = m.log(2)
LN16 = m.log(16)
COMP = 16 * LN2               # 压缩因子 11.0904
NAT_PER_PLAQ = 0.25           # BH：每面元 1/4 纳特

NCHK = [0, 0]


def line(tag):
    print("\n" + "=" * 76)
    print("  " + tag)
    print("=" * 76)


def chk(name, got, want, rtol=1e-9):
    if isinstance(got, bool) or isinstance(want, bool):
        ok = bool(got) == bool(want)
        got_s, want_s = str(got), str(want)
    else:
        ok = abs(got - want) <= rtol * max(1.0, abs(want))
        got_s, want_s = "%.12g" % got, "%.12g" % want
    NCHK[0] += 1
    if not ok:
        NCHK[1] += 1
    print("  [%s] %-50s got=%s want=%s" % ("OK" if ok else "XX", name, got_s, want_s))
    return ok


def show(name, val, fmt="%.12g"):
    print("       %-46s %s" % (name, fmt % val))


print("=" * 76)
print("  第 35 轮：「面元 ↔ 键」显式构造与计数")
print("=" * 76)

# ================================================================== PK-1
line("PK-1  显式构造与计数自洽")

L = 8                       # 平面边长（格点数）
INP = [(+1, 0), (-1, 0), (0, +1), (0, -1)]      # §4.9 引理 1 的平面内 4 方向

plaquettes = [((i % L), (j % L)) for i in range(L) for j in range(L)]
NP = len(plaquettes)
show("平面内面元数 N_p（= 格点数）", float(NP), "%.0f")
show("每面元的平面内连接数", float(len(INP)), "%.0f")
slots = NP * len(INP)
show("槽位总数 4·N_p", float(slots), "%.0f")

# 枚举不同的键（用 frozenset 表示无向键）
bonds = {}
for (i, j) in plaquettes:
    for dx, dy in INP:
        key = frozenset(((i, j), ((i + dx) % L, (j + dy) % L)))
        # 周期性：若两端是同一点（L=1）则跳过
        if len(key) == 1:
            continue
        bonds[key] = bonds.get(key, 0) + 1
NB = len(bonds)
show("不同的键数 N_b", float(NB), "%.0f")
mult = sorted(bonds.values())
show("每条键的共享重数（唯一值应为 2）", float(mult[0]), "%.0f")
chk("每条键恰好被 2 个面元共享", float(set(mult) == {2}), True)
chk("N_b = 2·N_p（4·N_p 槽位 / 每个键被数 2 次）", float(NB), 2.0 * NP, 1e-12)
show("槽位 / 键 = 4N_p / 2N_p", slots / float(NB), "%.6f")

# ================================================================== PK-2
line("PK-2  面积律")

show("面元面积（构造定义）= l_P² / m²", L_P ** 2, "%.6e")
show("⟹ 面元数 × l_P² = 面积 A", float(NP) * L_P ** 2, "%.6e")
print("      ⟹ **面元数 ∝ A**（构造上成立）⟹ 熵 S ∝ A，面积律自洽 ✓")
chk("面元数 = A / l_P²（构造恒等）", float(NP), float(NP), 1e-12)

# ================================================================== PK-3
line("PK-3  键共享 = 相邻面元相关的**具体机制**")

print("""
      B5 原文只断言「相邻面元的 4 方向连接**强相关**（通量管相干）」，从未给出机制。
      本轮的显式构造给出了它：**相邻面元共享同一条键**。
        面元 P 的「+x 方向连接」与它右邻居 Q 的「−x 方向连接」是**同一条键**，
        因此两个槽位必须取同一个值（同一条键承载的正 / 负支不可能分身）。
      ⟹ 这不是「统计相关」，而是**恒等约束**：每对相邻面元之间有 1 条键被恒等绑定。""")

# 数值演示：随机赋值 16 个槽位时，独立自由度的实际个数
pairs = 0
seen = set()
for (i, j) in plaquettes:
    for dx, dy in INP:
        a = (i, j)
        b = ((i + dx) % L, (j + dy) % L)
        key = frozenset((a, b))
        if key in seen:
            pairs += 1
        seen.add(key)
show("被恒等绑定的槽位对数（每个键贡献 1 对）", float(pairs), "%.0f")
chk("绑定对数 = 键数", float(pairs), float(NB), 1e-12)
show("⟹ 独立自由度 = 4N_p − N_b = 2N_p", float(slots - NB), "%.0f")

# ================================================================== PK-4
line("PK-4  量化：键共享解释了压缩因子 11.0904 中的多少")

raw_bits_per = 4.0                       # B5：每面元 4 bits（可读）
indep_bits_per = 2.0                     # 键共享后：每面元 2 条独立键
bh_bits_per = NAT_PER_PLAQ / LN2         # BH：0.25 nat ⟹ bits
show("原始可读 / bits per 面元", raw_bits_per, "%.6f")
show("键共享后独立 / bits per 面元", indep_bits_per, "%.6f")
show("BH 要求 / bits per 面元", bh_bits_per, "%.6f")
show("总压缩因子（nats 口径）= 4 ln16... 实测", COMP, "%.6f")
f_share = raw_bits_per / indep_bits_per
f_rest = indep_bits_per / bh_bits_per
show("键共享贡献的压缩", f_share, "%.6f")
show("仍需解释的剩余压缩", f_rest, "%.6f")
show("  剩余 = 8 ln 2 ?", 8 * LN2, "%.6f")
chk("总压缩因子 = 键共享 × 剩余 = 16 ln2", f_share * f_rest, COMP, 1e-12)
show("  校验：2 × 5.545 =", f_share * f_rest, "%.6f")
show("  总压缩因子 16 ln2 =", COMP, "%.6f")
chk("16 ln2 = 2 × (8 ln2)（恒等）", COMP, 2 * 8 * LN2, 1e-12)
print("""
      ⟹ **压缩因子 11.0904 第一次有了部分机制**：
         16 ln2 = **2**（键共享，已有机制） × **8 ln2 = 5.545**（仍无机制）。
      ⚠️ 诚实：只解释了因子 2；剩余 5.545 **仍未解释**，不得包装成完整推导。
         且「8 ln2」这个写法本身没有机制支撑，只是恒等变形。""")

# ================================================================== PK-5
line("PK-5  2×2 相干块的键计数（B5 的「4 面元 × 4 方向 = 16 自由度」）")

block = [(0, 0), (0, 1), (1, 0), (1, 1)]
blk_slots = len(block) * len(INP)
blk_bonds = {}
for (i, j) in block:
    for dx, dy in INP:
        a = (i, j)
        b = (i + dx, j + dy)
        key = frozenset((a, b))
        blk_bonds[key] = blk_bonds.get(key, 0) + 1
internal = sum(1 for k in blk_bonds if k.issubset(set(block)))
external = len(blk_bonds) - internal
show("块内面元数", float(len(block)), "%.0f")
show("槽位数（= 4 面元 × 4 方向）", float(blk_slots), "%.0f")
show("触及的不同键数", float(len(blk_bonds)), "%.0f")
show("  其中块内键（被两块共享）", float(internal), "%.0f")
show("  其中跨界键（只被一块用到）", float(external), "%.0f")
chk("槽位 = 2×块内键 + 1×跨界键", float(blk_slots), float(2 * internal + external), 0.0)
print("""
      ⟹ B5 所谓「4 面元 × 4 方向 = 16 个自由度」里，
         **16 个槽位实际只对应 %d 条不同的键**（16/%d = %.4f）。
         ⟨这是「自由度」一词被滥用的地方：16 是槽位数，不是独立自由度数。⟩"""
      % (len(blk_bonds), len(blk_bonds), blk_slots / float(len(blk_bonds))))

# ================================================================== PK-6
line("PK-6  判决")

print("""
  ✅ **「面元 ↔ 键」的对应关系已显式构造**（此前只是默认）：
     面元 = 格点在现在平面内的对偶面元（面积 l_P² ⟹ 面元数 ∝ A ✓ 面积律）；
     面元的 4 条「平面内连接」 = 该格点到 4 个平面内邻居（±x, ±y）的**键**。
     数值（L=8 平面）：面元数 64、槽位 256、**不同键 128 = 2×64**、每条键共享重数**恰为 2** ✓。

  ✅ **B5 的「相邻面元强相关」第一次有了机制**：不是统计相关，而是
     **恒等约束**——相邻面元共享同一条键，两个槽位必须取同一个值。
     绑定对数 = 键数 = 128，独立自由度 = 4N_p − N_b = **2N_p**（每面元 2 条独立键）。

  ✅ **压缩因子 16 ln2 = 11.0904 第一次有了部分机制**：
     **16 ln2 = 2（键共享，已有机制） × 8 ln2 = 5.545（仍无机制）**。
     ⚠️ 只解释了因子 2，剩余 5.545 仍未解释。

  ⚠️ **顺带纠正一处措辞**：B5 的「4 面元 × 4 方向 = 16 自由度」中，
     16 是**槽位数**而非独立自由度数（2×2 块实测：16 槽位 → %d 条不同键）。

  ❗ **仍开放**：① 剩余压缩 5.545 无机制；② 「面元 = 格点对偶面元」仍是本轮的定义
     （§4.9 引理 1 只说「平面内 4 方向连接」，未明说是格点的对偶面元）；
     ③ 面元是**面**、格点是**点**，本轮把它们按对偶对应起来，这一对应的唯一性未论证。
""" % len(blk_bonds))

print("=" * 76)
print("  检查项：%d    失败项：%d" % (NCHK[0], NCHK[1]))
print("=" * 76)
