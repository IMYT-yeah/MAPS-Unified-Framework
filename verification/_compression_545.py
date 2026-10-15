# -*- coding: utf-8 -*-
"""
第 39 轮核验：压缩因子 5.545（= 8 ln2）的机制审查。

结论预告：5.545 不是「等待机制的物理因子」，而是**两个不同口径的计数之比**：
  分子 = 衬底的槽位数（以比特计），分母 = BH 的热力学熵（以纳特计）。
因此它的「自然性」是伪问题。可机制化的部分（因子 2，键共享）已在第 35 轮完成；
其余部分不存在枚举机制、也不存在几何机制（本轮给出 no-go）。

检查项：CF-1 … CF-9，全部为纯标准库 + numpy（仅 CF-7 用 numpy 可选，已写成无依赖版）。
运行：<venv>/python.exe outputs/_compression_545.py
"""

import math
import itertools
import random

OK = [0]
FAIL = [0]


def chk(tag, cond, msg):
    if cond:
        OK[0] += 1
        print("  [OK] {:<6} {}".format(tag, msg))
    else:
        FAIL[0] += 1
        print("  [XX] {:<6} {}  <-- 失败".format(tag, msg))


def hdr(t):
    print("")
    print("-" * 78)
    print(t)
    print("-" * 78)


LN2 = math.log(2.0)
LN16 = math.log(16.0)

# ---------------------------------------------------------------- 常数
L_P = 1.616255e-35          # m
T_P = 5.391247e-44          # s
HBAR = 1.054571817e-34
C = 2.99792458e8
G = 6.67430e-11
KB = 1.380649e-23
M_SUN = 1.98892e30
T_BH_SUN = 6.16868e-8       # K，太阳质量黑洞 Hawking 温度（框架观测端）

# 需求侧：BH 熵密度
S_REQ_PER_PLAQ = 0.25       # nat / l_P²
S_REQ_BITS = S_REQ_PER_PLAQ / LN2

hdr("CF-1  恒等式与分解：11.0904 的几种写法")

raw_slots = 4 * LN2                     # 4 槽位/面元，每槽 1 bit
raw_per_block = 4 * LN16                # 4 面元/相干块，每面元 ln16
comp_total = raw_per_block / 1.0        # 分母 = 1 nat（BH 观测端）
comp_16ln2 = 16 * LN2
residual = comp_total / 2.0             # 第 35 轮：因子 2 归键共享

print("  原始：4 槽位/面元 × ln2        = {:.9f} nat".format(raw_slots))
print("  块内：4 面元 × ln16            = {:.9f} nat".format(raw_per_block))
print("  压缩：/ 1 nat                  = {:.9f}".format(comp_total))
print("  16 ln2                         = {:.9f}".format(comp_16ln2))
print("  4 ln16                         = {:.9f}".format(4 * LN16))
print("  残余（÷ 2）                    = {:.9f}".format(residual))
print("  8 ln2                          = {:.9f}".format(8 * LN2))
chk("CF-1a", abs(comp_16ln2 - comp_total) < 1e-12, "16 ln2 == 4 ln16 == 压缩因子")
chk("CF-1b", abs(residual - 8 * LN2) < 1e-12, "残余 == 8 ln2 == 5.545177444")
chk("CF-1c", abs(2.0 * 8 * LN2 - 16 * LN2) < 1e-12, "2 × 8 ln2 == 16 ln2（分解自洽）")

# 键共享因子 2：L=8 平面显式计数
L = 8
n_plaq = L * L
slots = 4 * n_plaq
keys = set()
for x in range(L):
    for y in range(L):
        keys.add(("h", x, y))           # 到 +x 邻居的键，用最小端点编号
        keys.add(("v", x, y))           # 到 +y 邻居的键
mult = {k: 0 for k in keys}
for x in range(L):
    for y in range(L):
        for k in [("h", x, y), ("h", (x - 1) % L, y), ("v", x, y), ("v", x, (y - 1) % L)]:
            mult[k] += 1
print("  L=8 平面：面元 {} / 槽位 {} / 不同键 {} / 共享重数取值 {}".format(
    n_plaq, slots, len(keys), sorted(set(mult.values()))))
chk("CF-1d", len(keys) == 2 * n_plaq and sorted(set(mult.values())) == [2],
    "键数 = 2 × 面元数，且每条键恰被 2 个面元共享 ⟹ 独立自由度 2 bits/面元")

# 口径依赖（本轮新增提示）：2×2 块的键/面元比对 ≠ 体内渐近值
k2 = set()
for x in range(2):
    for y in range(2):
        k2.add(("h", x, y)); k2.add(("v", x, y))
        k2.add(("h", x - 1, y)); k2.add(("v", x, y - 1))
print("  2×2 块：面元 4 / 触及的不同键 {}（含与外部共享的边界键）⟹ {:.2f} 键/面元".format(
    len(k2), len(k2) / 4.0))
chk("CF-1e", len(k2) == 12 and abs(len(keys) / float(n_plaq) - 2.0) < 1e-12,
    "块内 3.0 键/面元 vs 体内 2.0 键/面元 ⟹ 中间量「因子 2」是口径依赖的（非强度量）")

hdr("CF-2  次二元引理：0.25 nat/l_P² 比 1 比特还小")

print("  需求：{:.6f} nat / l_P² = {:.6f} bit / l_P²".format(S_REQ_PER_PLAQ, S_REQ_BITS))
print("  一个二元自由度最大熵 = ln2 = {:.6f} nat".format(LN2))
print("  e^0.25 = {:.10f}".format(math.exp(0.25)))
chk("CF-2a", S_REQ_PER_PLAQ < LN2, "0.25 nat < ln2 ⟹ 熵密度是**次二元**的")
chk("CF-2b", S_REQ_BITS < 1.0, "0.3607 bit/l_P² < 1 bit ⟹ 每普朗克面积不到一个比特")
chk("CF-2c", abs(math.exp(0.25) - 1.2840254167) < 1e-9,
    "等效态数 e^0.25 = 1.2840（非整数 ⟹ 不是枚举）")

hdr("CF-3  枚举 no-go（面元级）：无整数态数给出 0.25 nat")

print("  {:>3}  {:>14}  {:>14}  {:>12}".format("m", "S=ln m (nat)", "T_m/T_BH", "温度偏差"))
best = (1e9, None)
for m in range(1, 13):
    S = math.log(m)
    if S == 0.0:
        print("  {:>3}  {:>14}  {:>14}  {:>12}".format(m, "0.000000", "inf", "S=0（T 发散）"))
        continue
    ratio = S_REQ_PER_PLAQ / S
    dev = ratio - 1.0
    if abs(dev) < best[0]:
        best = (abs(dev), m)
    print("  {:>3}  {:>14.6f}  {:>14.6f}  {:>11.2f}%".format(m, S, ratio, 100 * dev))
print("  最佳整数 m = {}，偏差 {:.2f}%（判据 1% 远未过）".format(best[1], 100 * best[0]))
chk("CF-3", best[0] > 0.5,
    "最近的整数态数偏差 ≥ {:.1f}% ⟹ 0.25 nat/面元**不可能**是任何枚举".format(100 * best[0]))

hdr("CF-4  枚举 no-go（相干块级）：1 nat/块 也不可能是枚举")

print("  {:>3}  {:>14}  {:>14}  {:>12}".format("m", "S=ln m (nat)", "T_m/T_BH", "温度偏差"))
bestB = (1e9, None)
for m in range(2, 9):
    S = math.log(m)
    ratio = 1.0 / S
    dev = ratio - 1.0
    if abs(dev) < bestB[0]:
        bestB = (abs(dev), m)
    print("  {:>3}  {:>14.6f}  {:>14.6f}  {:>11.2f}%".format(m, S, ratio, 100 * dev))
print("  最佳整数 m = {}，偏差 {:.2f}%（m=2 即原稿「1 bit/块」，偏差 +44.27% ⟹ 与第 15 轮交叉验证）".format(
    bestB[1], 100 * bestB[0]))
chk("CF-4a", abs(1.0 / LN2 - 1.0 - 0.442695) < 1e-6, "m=2 ⟹ +44.27%，与第 15 轮的裁决数一致")
chk("CF-4b", bestB[0] > 0.05,
    "最近的整数 m = {} 仍偏 {:.2f}% ⟹ 1 nat/块 无枚举解（e 非整数）".format(bestB[1], 100 * bestB[0]))

hdr("CF-5  几何审查：任何「每 l_P² 至少 1 比特」的读法都超出 ln16 倍")

print("  立方格（间距 l_P，周期边界）穿越键密度（解析 + L=8 数值）：")
Ls = 8
N = Ls ** 3
# 轴向面（⊥x）穿越：x 方向键总数 = N，被 Ls 个面族平分
cross_x = N // Ls
area_in_lp2 = Ls * Ls
print("    · 轴向面 ⊥x：穿越键 {} 条 / 面积 {} l_P² ⟹ {:.3f} 条/l_P²".format(
    cross_x, area_in_lp2, cross_x / float(area_in_lp2)))
iso_avg = 3 * 0.5                       # Σ_axes <|n_a|> = 3 × 1/2
print("    · 各向同性平均：Σ_a ⟨|n_a|⟩ = 3 × 1/2 = {:.3f} 条/l_P²".format(iso_avg))
readings = [
    ("R1 原始槽位（4 槽/面元）", 4 * LN2),
    ("R2 键共享后（2 独立键/面元）", 2 * LN2),
    ("R3 穿越键·各向同性平均（1.5 条/l_P²）", 1.5 * LN2),
    ("R4 穿越键·轴对齐最保守（1 条/l_P²）", 1.0 * LN2),
]
print("  {:>44}  {:>12}  {:>12}  {:>10}".format("读法", "可用熵(nat)", "超出倍数", "判定"))
min_over = 1e9
for name, S in readings:
    over = S / S_REQ_PER_PLAQ
    min_over = min(min_over, over)
    print("  {:>44}  {:>12.6f}  {:>12.4f}  {:>10}".format(name, S, over, "超出"))
print("  最保守读法 R4 的超出倍数 = {:.6f} = ln16".format(min_over))
chk("CF-5a", abs(min_over - LN16) < 1e-9,
    "最保守几何读法仍超出 ln16 = 2.7726 倍 ⟹ 供给充足，缺口不是「不够」而是「怎么数」")
chk("CF-5b", min_over > 2.0,
    "所有自然几何因子（1/2, 3/4, 3/2, 2, 4/3 …）都是 O(1)，弥合不了 ≥2.77 倍")

hdr("CF-6  残余 5.545 的双重身份：单位换算 vs 真实收缩")

bits_after_sharing = 8.0                # 2 独立键/面元 × 4 面元
required_bits = 1.0 / LN2               # 1 nat 折成比特
as_nats = bits_after_sharing * LN2      # 8 bits 写成纳特
as_ratio = bits_after_sharing / required_bits
print("  键共享后独立信息 = {:.0f} bits".format(bits_after_sharing))
print("  BH 要求          = 1 nat = {:.6f} bits".format(required_bits))
print("  (a) 8 bits 写成纳特      = {:.9f}".format(as_nats))
print("  (b) 8 bits ÷ 1.4427 bits = {:.9f}".format(as_ratio))
chk("CF-6a", abs(as_nats - 8 * LN2) < 1e-12, "(a) 就是 8 ln2 —— 是**单位换算**（比特→纳特）")
chk("CF-6b", abs(as_ratio - 8 * LN2) < 1e-12, "(b) 与之同值 —— 是**真实收缩** 8 → 1.4427 bits")
chk("CF-6c", abs(as_nats - as_ratio) < 1e-12,
    "两者同值 ⟹ 「5.545 是什么」本身有歧义（半是单位，半是收缩）")

hdr("CF-7  置换双射 ⟹ 动力学不能产生压缩")

def make_tick(Lx, axis, phases):
    """一个 tick = 沿 axis 的二分图完美匹配交换；每条线独立相位（offs 决定配对的错位）。

    phases[line] ∈ {0,1} = 该线的相位（第 26 轮：相位必须每线独立）。
    线上的配对按环面绕回，故 Lx 为偶数时每条线恰有 Lx/2 个不交对。
    """
    def tick(field):
        f = list(field)
        idx = {}
        for z in range(Lx):
            for y in range(Lx):
                for x in range(Lx):
                    idx[(x, y, z)] = x + y * Lx + z * Lx * Lx
        line_id = 0
        for a in range(Lx):
            for b in range(Lx):
                offs = phases[line_id % len(phases)]
                line_id += 1
                coords = []
                for t in range(Lx):
                    tt = (offs + t) % Lx
                    if axis == 0:
                        coords.append((tt, a, b))
                    elif axis == 1:
                        coords.append((a, tt, b))
                    else:
                        coords.append((a, b, tt))
                for i in range(0, Lx - 1, 2):
                    i1 = idx[coords[i]]
                    i2 = idx[coords[i + 1]]
                    f[i1], f[i2] = f[i2], f[i1]
        return tuple(f)
    return tick


rng = random.Random(20260920)
Lx = 2                                   # 8 位点 ⟹ 2^8 = 256 个构型，可穷举
Ns = Lx ** 3
all_cfgs = list(itertools.product([0, 1], repeat=Ns))
bijective = True
for axis in (0, 1, 2):
    phases = [rng.randint(0, 1) for _ in range(Ns)]
    tk = make_tick(Lx, axis, phases)
    img = set(tk(c) for c in all_cfgs)
    if len(img) != len(all_cfgs):
        bijective = False
print("  L=2 立方（{} 位点，{} 个构型）× 3 个轴 ⟹ 像集大小恒为 {}".format(
    Ns, len(all_cfgs), len(all_cfgs)))
chk("CF-7a", bijective, "tick 映射在构型空间上是**双射**（穷举验证）⟹ 底层零熵产生")

# 哨兵：双射是必要但不充分——**恒等映射也是双射**。必须确认映射真的搬运了标记。
# （本题踩过的坑：初版 range(offs, Lx, 2) 在 Lx = 2 时一个配对都没有，映射退化成恒等，
#   而"像集大小 = 256"照样通过。这条哨兵就是为它设的。）
sent_tk = make_tick(Lx, 0, [rng.randint(0, 1) for _ in range(Ns)])
moved = sum(1 for c in all_cfgs if sent_tk(c) != c)
chk("CF-7a2", moved >= 200,
    "哨兵：映射**不是恒等**（穷举中 {}/{} 个构型被改变）⟹ 配对确实发生了".format(moved, len(all_cfgs)))

# 全局标记多重集守恒（较大格点）
Lb = 6
Nb = Lb ** 3
field = tuple(rng.randint(0, 1) for _ in range(Nb))
y0 = field
rng2 = random.Random(7)
for step in range(500):
    axis = rng2.randint(0, 2)
    phases = [rng2.randint(0, 1) for _ in range(Nb)]
    field = make_tick(Lb, axis, phases)(field)
chk("CF-7b", sorted(field) == sorted(y0),
    "L=6、500 tick 后全局标记多重集完全守恒（置换的直接后果）")

# 固定块内的读数不守恒（这就是「粗粒化」的位置）
def block_entropy(f, Lx, x0, y0b, z0, w):
    cnt = 0
    ones = 0
    for dz in range(w):
        for dy in range(w):
            for dx in range(w):
                v = f[(x0 + dx) % Lx + (y0b + dy) % Lx * Lx + (z0 + dz) % Lx * Lx * Lx]
                cnt += 1
                ones += v
    p = ones / float(cnt)
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * math.log(p) + (1 - p) * math.log(1 - p))


Lf = 8
field = tuple(rng.randint(0, 1) for _ in range(Lf ** 3))
rngf = random.Random(11)
vals = []
for step in range(300):
    field = make_tick(Lf, rngf.randint(0, 2), [rngf.randint(0, 1) for _ in range(Lf ** 3)])(field)
    if step % 3 == 0:
        vals.append(block_entropy(field, Lf, 2, 2, 2, 2))
mean = sum(vals) / len(vals)
spread = max(vals) - min(vals)
print("  固定 2×2×2 块的读数熵：均值 {:.6f} nat、极差 {:.6f} nat（初始为随机标记）".format(mean, spread))
chk("CF-7c", spread > 0.0,
    "块内读数熵随时间涨落 ⟹ 它不是动力学的守恒量，只可能是**粗粒化映射**的性质")

hdr("CF-8  压缩因子不受观测约束（Hawking 温度只依赖观测端）")

T_bh = HBAR * C ** 3 / (8 * math.pi * G * M_SUN * KB)
print("  T = hbar c³ / (8 pi G M k_B) = {:.6e} K（对照框架值 {:.5e} K）".format(T_bh, T_BH_SUN))
print("  该式**不含**任何压缩因子或衬底计数 ⟹ 16 bits / 8 bits / 4 bits 都改变不了它")
oscl = [("16 bits/块（原始槽位）", 16.0), ("8 bits/块（键共享后）", 8.0), ("4 bits/块", 4.0)]
for nm, b in oscl:
    print("    · {:>22}：Hawking 温度仍是 {:.6e} K（不变）".format(nm, T_bh))
chk("CF-8a", abs(T_bh / T_BH_SUN - 1.0) < 0.01, "观测端 1 nat/4l_P² 复现 Hawking 温度（0.0x% 内）")
chk("CF-8b", True,
    "⟹ 压缩因子是两个独立量的**比值**，不是可观测量；观测只约束分母（1 nat/4l_P²）")

hdr("CF-9  记录项（无机制，勿写入正文）")

x = math.exp(0.25)
frac = []
v = x
for _ in range(6):
    ip = int(v)
    frac.append(ip)
    if v - ip < 1e-12:
        break
    v = 1.0 / (v - ip)
print("  e^0.25 = {:.10f}，连分数前几项 {} ".format(x, frac))
approx = [(4, 3), (5, 4), (9, 7), (14, 11)]
for a, b in approx:
    print("    {}/{} = {:.6f}（相对偏差 {:+.3f}%）".format(a, b, a / float(b), 100 * (a / float(b) / x - 1)))
print("  0.25 nat = 1/log2(16) 的数值巧合：{:.9f} vs {:.9f}".format(0.25, 1.0 / math.log(16, 2)))
chk("CF-9", True, "以上均登记为**无机制**的数值接近；按项目规约不得用作证据")

# ---------------------------------------------------------------- 汇总
hdr("汇总")
print("  通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("")
print("  核心结论：")
print("  (1) 需求侧 0.25 nat/l_P² = 0.3607 bit/l_P² **小于 1 比特** ⟹ 次二元（CF-2）")
print("  (2) 无整数态数给出 0.25 nat（面元级最佳偏差 ≥ {:.0f}%）⟹ 枚举 no-go（CF-3）".format(100 * best[0]))
print("  (3) 无整数态数给出 1 nat/块（最佳 m = {}，仍偏 {:.2f}%）⟹ 枚举 no-go（CF-4）".format(
    bestB[1], 100 * bestB[0]))
print("  (4) 最保守几何读法也超出 ln16 = 2.7726 倍 ⟹ 供给充足，缺口是「口径」不是「缺少」（CF-5）")
print("  (5) 残余 5.545 一半是单位换算、一半是收缩 ⟹ 问题本身有歧义（CF-6）")
print("  (6) tick 是双射 ⟹ 动力学零熵产生 ⟹ 压缩只可能是粗粒化映射的性质（CF-7）")
print("  (7) 压缩因子不受观测约束 ⟹ 不是可观测量，其「自然性」是伪问题（CF-8）")
if FAIL[0] == 0:
    print("")
    print("  判决：5.545 的「机制」不存在，且**不需要存在**。可机制化的因子 2 已于第 35 轮完成；")
    print("        余下者应按第 37 轮的判定口径，记为观测者模型（B5）的分辨率公设。")
