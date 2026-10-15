# -*- coding: utf-8 -*-
"""
第 32 轮：裁决读法 A / B（B5「原始可读 4 bits/面元」的结构）
  读法 A（第 19 轮）：1-of-4 方向 × 4 内部态 {正,负,湮灭中,真空} = 16
  读法 B（原文 1651 字面）：4 个平面内「连接状态」，每槽二元 ⟹ 2^4 = 16
判别约束：
  C-a  原始可读 = 4 bits/面元（B5 原文 1651）
  C-b  满占位 f = 1（第 20/26 轮 C-1）⟹ 「真空」不占权重
  C-c  「湮灭中」= 拍内零测度过渡态（第 20 轮 C-4）⟹ 不占权重
  C-d  方向数 = 4（第 31 轮：§4.9 引理 1 的平面内 4）
  C-e  A1 的 50:50 ⟹ 正 / 负两分支等概率
只用标准库。正文引号一律用中文引号。
"""
import itertools
import math as m

C_MS = 2.99792458e8
G_SI = 6.67430e-11
H_PLANCK = 6.62607015e-34
HBAR = H_PLANCK / (2 * m.pi)
K_B = 1.380649e-23
M_SUN = 1.98892e30          # 与第 15/25/31 轮一致

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
    print("       %-44s %s" % (name, fmt % val))


print("=" * 76)
print("  第 32 轮：裁决读法 A / B —— B5「4 bits/面元」的结构")
print("=" * 76)

# ================================================================== AB-1
line("AB-1  候选模型枚举：哪些能给出恰好 16 态（4 bits）")

# 读法 A 族：1-of-4 方向 × 内部态集合
A_FULL = ["正", "负", "湮灭中", "真空"]
A_LIVE = ["正", "负"]            # C-b / C-c 剔除后仍占权重的态
# 读法 B 族：4 个平面内槽，每槽 s 值
models = [
    ("A   1-of-4 方向 × {正,负,湮灭中,真空}", 4 * len(A_FULL), "第 19 轮原读法"),
    ("A′  1-of-4 方向 × {正,负}（真空/湮灭中不占权重）", 4 * len(A_LIVE), "叠加 C-b + C-c"),
    ("B1  4 槽 × {连接, 不连接}", 2 ** 4, "原文 1651 字面（二元连接位）"),
    ("B2  4 槽 × {正支, 负支}", 2 ** 4, "4 连接，各承载正/负分支"),
    ("B3  4 槽 × {正,负,湮灭中,真空}", 4 ** 4, "每槽四值"),
    ("C   外空间 6 槽 × 二元", 2 ** 6, "第 31 轮已排除"),
]
print("      模型                                                态数   bits/面元   = 4 bits?")
for name, nst, note in models:
    print("      %-48s %-6d %-10.6f %s"
          % (name, nst, m.log(nst, 2), "✅" if abs(nst - 16) < 1e-12 else ""))
chk("给出 16 态的模型恰有 A / B1 / B2 三个",
    sum(1 for _, n, _ in models if n == 16), 3.0, 0.0)

# ================================================================== AB-2
line("AB-2  读法 B2 的 16 态显式枚举（4 槽 × 正/负支）")

slots = list(itertools.product(["正", "负"], repeat=4))
show("枚举出的态数", float(len(slots)), "%.0f")
chk("4 个二元槽 ⟹ 2^4 = 16 个态", float(len(slots)), 16.0, 0.0)
for s in slots[:4]:
    print("        例：%s" % " ".join(s))
print("        …… （共 16 个）")
# A1 的 50:50 ⟹ 16 态等概率 ⟹ 熵 = ln 16
p_uni = 1.0 / len(slots)
S_uni = -sum(p_uni * m.log(p_uni) for _ in slots)
show("等概率下的熵 / nats（= ln 16）", S_uni)
chk("等概率熵 = ln 16 = 4 bits", S_uni, m.log(16), 1e-12)
show("  = bits", S_uni / m.log(2), "%.6f")

# ================================================================== AB-3
line("AB-3  五条约束的打分矩阵（✓ / ✗）")

# 对每个模型给 (C-a, C-b, C-c, C-d, C-e)
score = {
    "A  1-of-4 × {正,负,湮灭中,真空}": (True, False, False, True, True),
    "A′ 1-of-4 × {正,负}":            (False, True, True, True, True),
    "B1 4 槽 × {连接,不连接}":         (True, False, True, True, False),
    "B2 4 槽 × {正支,负支}":           (True, True, True, True, True),
    "B3 4 槽 × 四值":                 (False, False, False, True, True),
    "C  6 槽 × 二元":                 (False, True, True, False, True),
}
hdr = ["C-a 4bits", "C-b f=1", "C-c 零测度", "C-d 方向4", "C-e 50:50"]
print("      模型                                     %s   全过"
      % "  ".join("%-9s" % h for h in hdr))
allpass = []
for name, flags in score.items():
    cells = "  ".join("%-9s" % ("✓" if f else "✗") for f in flags)
    ok = all(flags)
    if ok:
        allpass.append(name)
    print("      %-38s %s   %s" % (name, cells, "✅" if ok else ""))
print("      （C-b：满占位 ⟹ 「真空」不占权重；C-c：「湮灭中」为拍内零测度过渡态 ⟹ 不占权重）")
chk("唯一全过五条约束的模型数 = 1", float(len(allpass)), 1.0, 0.0)
chk("全过者 = B2（4 槽 × 正/负支）", "B2" in allpass[0] if allpass else False, True)

# ================================================================== AB-4
line("AB-4  读法 A 为何落选：真空 / 湮灭中不该占权重")

print("      读法 A 把内部四态等权 ⟹ 真空占 1/4、湮灭中占 1/4 的权重。")
print("      但第 20 轮 C-1（满占位 f=1）说**没有空格点**；")
print("      C-4 说「湮灭中 / 真空」是**拍内零测度过渡态**。⟹ 二者不应进入熵的计数。")
w_vac = 0.25
show("读法 A 赋予「真空」的权重", w_vac, "%.4f")
show("读法 A 赋予「湮灭中」的权重", w_vac, "%.4f")
print("      ⟹ 剔除后有效内部态 = {正, 负}，读法 A 退化为 A′：4 × 2 = %d 态 = %.4f bits ✗"
      % (4 * len(A_LIVE), m.log(4 * len(A_LIVE), 2)))
chk("A′ 给 8 态（3 bits），与 4 bits/面元不符", m.log(8, 2), 3.0, 1e-12)

# 量化 A′ 的后果：沿用压缩因子 11.0904 时温度偏多少
NAT_PER_FACE = 0.25
comp16 = 4 * m.log(16)
ln8 = m.log(8)
ratio = (ln8 / comp16) / NAT_PER_FACE          # 每面元实际纳特 / 0.25
show("A′ 的每面元熵 / nat（= ln8 / 11.0904）", ln8 / comp16)
show("  与 BH 要求 0.25 nat/面元 之比", ratio)
T_std = HBAR * C_MS ** 3 / (8 * m.pi * G_SI * M_SUN * K_B)
T_A = T_std / ratio
show("标准 Hawking 温度（太阳质量）/ K", T_std, "%.6e")
show("A′ 情形下的 T / K", T_A, "%.6e")
show("  偏差", 100 * (T_A / T_std - 1), "%+.4f%%")
print("      对照：第 31 轮 N=24 的偏差 −12.76%；第 15 轮比特/纳特混淆 +44.27%。")
chk("A′ 被 Hawking 温度排除（偏差 > 10%）", float(abs(T_A / T_std - 1) > 0.10), True)

# ================================================================== AB-5
line("AB-5  B2 与既有链条的自洽性（压缩因子、熵密度、方向数）")

show("B2 的原始熵 / nats per 面元", m.log(16))
show("所需压缩因子 4·ln16 = 16 ln2", comp16)
chk("压缩因子仍为 11.0904（与第 19/25/31 轮一致）", comp16, 16 * m.log(2), 1e-12)
show("压缩后熵密度 / nat per 面元", m.log(16) / comp16)
chk("= 1/4 nat/面元（BH 熵）", m.log(16) / comp16, NAT_PER_FACE, 1e-12)
print("""
      ⟹ **B2 不改变任何已落的数值**：16 态、4 bits、0.25 nat/面元、
         压缩因子 11.0904 全部照旧。变的是「16 是怎么数出来的」：
           旧（读法 A）：4 方向 × 4 内部态（含真空、湮灭中）
           新（读法 B2）：4 个平面内连接，各承载**正支 / 负支** ⟹ 2^4
      ⟹ 且 B2 **直接把 A1 的 50:50 用上了**（每槽正 / 负等概率），
         而读法 A 里 50:50 只体现为「四态等权」，与 A1 无关。""")

# ================================================================== AB-6
line("AB-6  判决")

print("""
  ✅ **读法 B2 胜出**：4 个平面内连接，每个承载正支或负支 ⟹ 2^4 = 16 = 4 bits/面元。
     它是**唯一同时满足五条约束**的模型：
       C-a 原始可读 4 bits ✓ ｜ C-b 满占位 f=1（无空槽）✓ ｜ C-c 湮灭中零测度 ✓
       C-d 方向数 = 4（§4.9 引理 1 平面内 4）✓ ｜ C-e A1 的 50:50 直接落在每槽上 ✓

  ❌ **读法 A 落选**（第 19 轮的原读法）：它把「真空」与「湮灭中」当作
     与「正 / 负」等权的内部态，而第 20 轮的 C-1（满占位）与 C-4（零测度过渡态）
     要求这两者**不占权重**。剔除后 A 退化为 4 × 2 = 8 态 = 3 bits，
     与 4 bits/面元冲突；若硬沿用压缩因子 11.0904，Hawking 温度偏差 **+33.4%**。

  ⚠️ **代价（诚实）**：读法 B2 下，用户的四个状态 {正, 负, 湮灭中, 真空}
     **只有「正 / 负」进入熵的计数**；「湮灭中 / 真空」退为拍内零测度的过渡态
     （与第 20 轮 C-4 一致，但不再以「q = 4 唯一解」的形式出现）。
     ⟹ 第 19 轮「内部四态是唯一解」这一条**撤回**；改为「四态是**代数**状态空间，
        其中只有正 / 负两态携带权重」。

  ⚠️ **B1（连接 / 不连接）与 B2 仍能区分吗？** 能：B1 不含正 / 负分支，
     与 A1 的 50:50 无关（C-e 不过）。但 B1 是原文 1651「连接状态」更字面的读法，
     若将来框架给出「连接 = 分支标签」的机制，两者将合并。**目前取 B2（约束更严）。**

  ❗ **仍未解**：11.0904 的自然性；「连接」是否等价于「分支标签」；
     读法 B2 要求每条平面内连接都恒有通量（满占位的推论），这一推论本身待独立核验。
""")

print("=" * 76)
print("  检查项：%d    失败项：%d" % (NCHK[0], NCHK[1]))
print("=" * 76)
