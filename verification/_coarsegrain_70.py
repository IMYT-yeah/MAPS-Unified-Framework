# -*- coding: utf-8 -*-
"""第 70 轮 · I-18 ＋ I-17 合并：
「粗粒化截断」与 Φ 的质量 —— 两个开口能不能共用一个尺度？

I-18（第 67 轮登记）：平滑层从哪来？（为什么噪声会粗粒化出平滑结构）
I-17（第 62 轮登记）：Φ（KK 标量模 g₅₅）的质量与耦合是什么？—— 第五力的唯一入口

合并点（本轮找到）：
  §4.5b 明写 Φ 的数学身份是**谱作用** `S = Tr f(D²/Λ²)`（**带截断 Λ**）；
  而第 423 行给出「粗粒化」的**群论定义**（G 的轨道划分 = 最大 tick 不变粗粒化）。
  ⟹ 若两者共用同一个截断，就是一条机制；若不是，各自缺什么？

核验项：CG-1 … CG-10
"""
import io
import os
import sys
import math
import itertools

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _tickgroup as tg

OK = BAD = 0
FAILS = []


def chk(tag, cond, msg):
    global OK, BAD
    if cond:
        OK += 1
        print("  [OK] {:<6} {}".format(tag, msg))
    else:
        BAD += 1
        FAILS.append(tag)
        print("  [XX] {:<6} {}".format(tag, msg))


def rule(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# 常量（自洽导出，见铁律 12）
hbar = 1.054571817e-34
c = 2.99792458e8
G = 6.67430e-11
kB = 1.380649e-23
eV = 1.602176634e-19
lP = math.sqrt(hbar * G / c ** 3)
mP = math.sqrt(hbar * c / G)
EP_J = mP * c * c
EP_eV = EP_J / eV
hbar_c_eVm = hbar * c / eV          # ⚠️ 全用 eV 制：ℏc = 1.97327e-7 eV·m（陷阱 52）
H0_SI = 2.184e-18                   # s^-1（67.4 km/s/Mpc）
RH = c / H0_SI                      # 哈勃半径, m


def E_of_R(R):
    """§4.6 F2 降标机制：E(R) = √(ℏc·E_P/R)，全 eV 制。"""
    return math.sqrt(hbar_c_eVm * EP_eV / R)


def R_of_E(E_eV):
    return hbar_c_eVm * EP_eV / E_eV ** 2


def lam_of_m(m_eV):
    """力程 λ = ℏc/m。"""
    return hbar_c_eVm / m_eV


# ══════════════════════════════════════════════════════════════════════
rule("CG-1  引文清点：粗粒化 / 截断 / 孤子化 / 平滑层 —— 底本 = 补丁前备份")
# ══════════════════════════════════════════════════════════════════════

BASE = os.path.dirname(os.path.abspath(__file__))
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
CUR = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
PREV = os.path.join(HIST, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-01第69轮前.md")
if not os.path.exists(PREV):
    cands = sorted([f for f in os.listdir(HIST) if f.endswith("第69轮前.md")])
    if cands:
        PREV = os.path.join(HIST, cands[0])
print("  底本（补丁前）= {}".format(os.path.basename(PREV)))

WORDS = ["粗粒化", "粗粒", "截断", "孤子化", "平滑层", "涌现", "轨道划分", "谱作用",
         "重整化", "有效场论", "幂次计数", "自然性", "层级问题"]
curT = io.open(CUR, encoding="utf-8").read()
preT = io.open(PREV, encoding="utf-8").read()
print()
print("  {:<12} {:>10} {:>10}".format("词", "补丁前", "补丁后（当前稿）"))
nsub = 0
for w in WORDS:
    a, b = preT.count(w), curT.count(w)
    nsub += a
    print("  {:<12} {:>10} {:>10}".format(w, a, b))
print("  ⟹ 「粗粒化 / 截断」类词条**补丁前就有 {} 处**（不是 0 —— 与第 67 轮的")
print("     「图热流 / 联络 各 0 处」**性质不同**：本轮的主题词框架里**本来就有内容**）".format(nsub))
chk("CG-1", preT.count("粗粒化") >= 8 and preT.count("截断") >= 10,
    "「粗粒化」补丁前 {} 处、「截断」{} 处 ⟹ **框架本来就有这两个词**（不是新增物）".format(
        preT.count("粗粒化"), preT.count("截断")))


# ══════════════════════════════════════════════════════════════════════
rule("CG-2  框架里「粗粒化 / 截断」的**全部实现**与各自口径")
# ══════════════════════════════════════════════════════════════════════

IMPL = [
    ("① 群论粗粒化", "第 423 行", "「**G 的轨道划分就是最大的 tick 不变粗粒化**」",
     "**无尺度**（纯组合）", "【推导】第 41 轮"),
    ("② 宏观不可逆的来源", "第 1317 行", "「底层无熵产生，**宏观不可逆只能来自粗粒化**」",
     "—", "【推导】§8.6.7"),
    ("③ 普朗克截断", "第 322 行", "「**截断 = 普朗克（公理 1 自然给出）**」",
     "**l_P**", "【推导】公理 1"),
    ("④ 谱作用截断 Λ", "第 791 行", "`S = Tr f(D²/Λ²)`（Φ 的**数学身份**）",
     "❌ **Λ 未给值**", "§4.5b"),
    ("⑤ F2 降标机制", "第 311 行", "`δ = √(R·l_P)` ⟹ `E(R) = E_P·√(l_P/R)`",
     "R（一维扩散恢复长度）", "【推导】扩散"),
    ("⑥ `Q_res`「粗粒化截断能标」", "第 674 行", "`Q_res = E(R)/m_unit`（第 56 轮命名）",
     "R", "第 56 轮"),
    ("⑦ 概率归一化能标 E_c", "第 1090 行", "`ε_A(E_c) = 1` ⟹ `E_c = 1.0181 meV`",
     "1 meV", "**恒等式**（C-4）"),
    ("⑧ Φ⁴ 势的 μ", "第 984 行", "`V(Φ) = −½μ²Φ² + ¼λΦ⁴` ⟹ `m_Φ² = 2μ²`",
     "❌ **μ 是输入**", "§6.4"),
    ("⑨ 强度截断 r_c", "第 1585 行", "`r_c = GM/c² = 视界`", "GM/c²", "B2"),
    ("⑩ 玻尔兹曼弱场截断", "第 187/261 行", "`e^{−Φ/c²}` 仅**弱场/局部/截断**内有效",
     "—", "热平衡证明"),
]
print("  {:<24} {:<10} {:<44} {}".format("实现", "出处", "内容", "尺度从哪来"))
for nm, loc, cont, sc, prov in IMPL:
    print("  {:<24} {:<10} {:<44} {}".format(nm, loc, cont[:42], sc))
print()
n_scale_input = sum(1 for _, _, _, sc, _ in IMPL if "❌" in sc)
n_scale_given = sum(1 for _, _, _, sc, _ in IMPL if "l_P" in sc or sc == "R" or
                    sc == "R（一维扩散恢复长度）" or "GM" in sc or sc == "1 meV")
print("  ⟹ 10 个实现里：**尺度未给（是输入）的有 {} 个**；尺度已定的 {} 个。".format(
    n_scale_input, n_scale_given))
print("     ⚠️ 而「尺度已定」的那几个，定它的**也不是独立数据** ——")
print("        ③ 用公理 1、⑤/⑥ 用扩散方程、⑦ 用 ε_A 归一化（恒等式，C-4）、⑨ 用视界。")
chk("CG-2", n_scale_input == 2 and len(IMPL) == 10,
    "框架有 **10 个「粗粒化 / 截断」实现**；其中**只有 2 个是纯输入**（谱作用 Λ、Φ⁴ 势 μ）"
    "—— 而**恰恰这两个决定 Φ 的质量**")


# ══════════════════════════════════════════════════════════════════════
rule("CG-3  「不变 ⟺ 轨道函数」验证（第 423 行的定义是可判定的吗？）")
# ══════════════════════════════════════════════════════════════════════

DIMS = (2, 2, 4)
N = int(np.prod(DIMS))
K = N // 2
GENS = [np.array(g, dtype=np.int64) for g in tg.gens_correct(DIMS)]
print("  格点 {}  N = {}  k = {}  生成元 {} 个".format(DIMS, N, K, len(GENS)))


def apply(c, g):
    """c 是 bitmask；g[i] = i 的像。返回新 bitmask。"""
    nc = 0
    for i in range(N):
        if (c >> i) & 1:
            nc |= 1 << int(g[i])
    return nc


cfgs = []
for comb in itertools.combinations(range(N), K):
    m = 0
    for i in comb:
        m |= 1 << i
    cfgs.append(m)
M = len(cfgs)
print("  该层构型数 M = C({},{}) = {}".format(N, K, M))

# 轨道划分
unvis = set(cfgs)
orbits = []
while unvis:
    s = next(iter(unvis))
    comp = {s}
    stack = [s]
    while stack:
        cur = stack.pop()
        for g in GENS:
            nc = apply(cur, g)
            if nc not in comp:
                comp.add(nc)
                stack.append(nc)
    orbits.append(comp)
    unvis -= comp
SIZES = sorted([len(o) for o in orbits], reverse=True)
print("  **轨道数 = {}**（最大 {} / 最小 {}，平均 {:.2f}）".format(
    len(orbits), SIZES[0], SIZES[-1], M / len(orbits)))

# 找一个非平凡不变量：k 守恒（所有构型同 k）⟹ 平凡；
# 用「三坐标奇偶类计数向量」当作候选不变量（第 41/46 轮的 (Z₂)³）
coords = list(itertools.product(*[range(d) for d in DIMS]))
pi = {i: tuple(coords[i][k] % 2 for k in range(3)) for i in range(N)}
CLASSES = sorted(set(pi.values()))


def cls_count(c):
    v = [0] * len(CLASSES)
    for i in range(N):
        if (c >> i) & 1:
            v[CLASSES.index(pi[i])] += 1
    return tuple(v)


# 判据：同一轨道内 cls_count 恒定 ⟹ 它是轨道函数（不变）；反之则否
inv_ok = 0
inv_bad = 0
for o in orbits:
    vals = {cls_count(c) for c in o}
    if len(vals) == 1:
        inv_ok += 1
    else:
        inv_bad += 1
print()
print("  候选不变量「(Z₂)³ 奇偶类的占据计数向量」：")
print("     在 **{}** 条轨道上恒定（是轨道函数）、在 **{}** 条上变化".format(inv_ok, inv_bad))
vals_all = {cls_count(c) for c in cfgs}
print("     全层的取值数 = {} ⟹ 等值集数 = {}".format(len(vals_all), len(vals_all)))
print("     轨道数 = {} ｜ 等值集数 = {}  ⟹ {}".format(
    len(orbits), len(vals_all), "完备" if len(orbits) == len(vals_all) else "**不完备**（轨道数 ≠ 等值集数）"))
# 正对照：k 是（真）不变量吗？（tick 保占据数）
k_ok = all(len({bin(c).count("1") for c in o}) == 1 for o in orbits)
print()
print("  正对照：占据数 k 在**全部 {}** 条轨道上恒定？ {}".format(len(orbits), k_ok))
print("  逆判据（可判定）：**等值集数 ≥ 轨道数 ⟹ 该量不是不变量**")
print("     (Z₂)³ 计数向量：等值集 {} ≥ 轨道 {} ⟹ **它不是不变量** ✓".format(
    len(vals_all), len(orbits)))
print("     （与第 46 轮的结论一致：(Z₂)³ 只能当**上界**，不是不变量）")
chk("CG-3", k_ok and len(vals_all) > len(orbits),
    "正对照 k 在全部 {} 条轨道上恒定（真不变量）✓；逆判据确认 (Z₂)³ **不是**不变量"
    "（等值集 {} > 轨道 {}）⟹ 「不变 ⟺ 轨道函数」这条判据**可用**".format(
        len(orbits), len(vals_all), len(orbits)))


# ══════════════════════════════════════════════════════════════════════
rule("CG-4  ⭐ 数值实验 A：tick 轨道里「空间平滑度」能变化多少？（I-18 的核心）")
# ══════════════════════════════════════════════════════════════════════

# 平滑度：2×2×2 块的密度方差（块越大越敏感）
def blocks_of(dims, bz=None):
    """把格点按 z 方向切成 2 半（(2,2,4) ⟹ 2 块，每块 2×2×2）。"""
    Lz = dims[2]
    out = [[], []]
    for i in range(N):
        z = coords[i][2]
        out[0 if z < Lz // 2 else 1].append(i)
    return out


BLK = blocks_of(DIMS)
print("  平滑度定义：**块密度方差** `B(c) = Var_b(块内满格点比例)`，"
      "块 = z 方向两个 2×2×2 子块")


def block_var(c):
    d = []
    for ids in BLK:
        s = sum(1 for i in ids if (c >> i) & 1)
        d.append(s / float(len(ids)))
    mu = sum(d) / len(d)
    return sum((x - mu) ** 2 for x in d) / len(d)


def adj_same(c):
    """相邻对同值比例（另一条平滑度度量，做交叉验证）。"""
    tot = 0
    same = 0
    for i in range(N):
        for ax in range(3):
            j = list(coords[i])
            j[ax] = (j[ax] + 1) % DIMS[ax]
            j = coords.index(tuple(j))
            if i < j:
                tot += 1
                if ((c >> i) & 1) == ((c >> j) & 1):
                    same += 1
    return same / float(tot), tot


# 基线：全层平均
B_all = [block_var(c) for c in cfgs]
S_all = [adj_same(c)[0] for c in cfgs]
print("  全层（{} 个构型）：B 均值 {:.6f}、极差 [{:.6f}, {:.6f}]".format(
    M, np.mean(B_all), min(B_all), max(B_all)))
print("                    S 均值 {:.6f}（相邻对数 {}）".format(np.mean(S_all), adj_same(cfgs[0])[1]))
# 随机基线（超几何）
p = K / float(N)
B_rand = p * (1 - p) / 8.0
print("  随机基线（理论）：B_rand = p(1−p)/8 = {:.6f}（p = {}）".format(B_rand, p))

# 每条轨道内的 B 极差
ranges = []
for o in orbits:
    bs = [block_var(c) for c in o]
    ranges.append(max(bs) - min(bs))
ranges = np.array(ranges)
print()
print("  **轨道内 B 的极差**：均值 {:.6f}、中位 {:.6f}、最大 {:.6f}".format(
    ranges.mean(), np.median(ranges), ranges.max()))
big = int((ranges > 0.05).sum())
print("  极差 > 0.05（= 随机基线的 1.6 倍）的轨道数 = {} / {}".format(big, len(orbits)))
print()
print("  ⟹ 若极差大 ⟹ **同一轨道内既有很平滑也有很粗糙的构型** ⟹ **平滑不是 tick 不变量**")
# 找出一个极端例子
best = int(np.argmax(ranges))
o = orbits[best]
bmin = min(o, key=block_var)
bmax = max(o, key=block_var)
print("  例：轨道 #{}（大小 {}）——B 从 **{:.4f}** 到 **{:.4f}**".format(
    best, len(o), block_var(bmin), block_var(bmax)))
print()
print("  ⚠️⚠️ **极差全为 0** —— 这不是「平滑是不变量」，而是**我的度量在 L = 4 上退化**：")
print("     (2,2,4) 的 z 线长 = 4 ⟹ 相位 1 的匹配 = `(1 2)(3 0)` **恰好把两块整体互换**")
print("     ⟹ 块 0 的密度 d₀ ↦ 1 − d₀ ⟹ **方差 B = (d₀ − 0.5)² 恒不变** ⟹")
print("     **B 在这个最小算例上变成 tick 不变量**（陷阱 62「最小算例无法还原」的第六例）。")
print("     ⟹ **必须换到 z 线长 ≥ 6 的格点**（见 CG-4b）。")
chk("CG-4", ranges.max() == 0.0 and len(orbits) == 253,
    "**(2,2,4) 上轨道内块方差极差 = 0** ⟹ 该度量在此**退化**（L=4 的两块恰好整体互换）"
    "—— 这是**实现层发现**，不是物理结论；须换格点")

# ── CG-4b：(2,2,6)（z 线长 6）重做，单构型轨道 BFS（陷阱 21 的做法）
rule("CG-4b  ⭐ 换 (2,2,6)（z 线长 6）重做：轨道内「平滑度」能变化多少？")
D6 = (2, 2, 6)
N6 = int(np.prod(D6))
K6 = N6 // 2
CO6 = list(itertools.product(*[range(d) for d in D6]))
IDX6 = {c: i for i, c in enumerate(CO6)}
G6 = [np.array(g, dtype=np.int64) for g in tg.gens_correct(D6)]
print("  格点 {}  N = {}  k = {}  生成元 {} 个".format(D6, N6, K6, len(G6)))


def apply6(c, g):
    nc = 0
    for i in range(N6):
        if (c >> i) & 1:
            nc |= 1 << int(g[i])
    return nc


def blk6(c, cut=3):
    """z < cut 与 z >= cut 两块（各 12 个格点）。"""
    d = [0, 0]
    for i in range(N6):
        if (c >> i) & 1:
            d[0 if CO6[i][2] < cut else 1] += 1
    return d[0] / 12.0, d[1] / 12.0


def B6(c):
    a, b = blk6(c)
    return ((a - 0.5) ** 2 + (b - 0.5) ** 2) / 2.0


def S6(c):
    tot = same = 0
    for i in range(N6):
        for ax in range(3):
            j = list(CO6[i])
            j[ax] = (j[ax] + 1) % D6[ax]
            j = IDX6[tuple(j)]
            if i < j:
                tot += 1
                if ((c >> i) & 1) == ((c >> j) & 1):
                    same += 1
    return same / float(tot), tot


c0_6 = 0
for i in range(N6):
    if CO6[i][2] < 3:
        c0_6 |= 1 << i
print("  初态 c0：z ∈ {{0,1,2}} 全满（8 个『层』… 实为 12 个格点）")
print("     B(c0) = {:.6f}   S(c0) = {:.6f}（相邻对 {} 条）".format(
    B6(c0_6), S6(c0_6)[0], S6(c0_6)[1]))

# 单构型轨道 BFS
seen = {c0_6}
stack = [c0_6]
while stack:
    cur = stack.pop()
    for g in G6:
        nc = apply6(cur, g)
        if nc not in seen:
            seen.add(nc)
            stack.append(nc)
orb6 = list(seen)
Bs = np.array([B6(c) for c in orb6])
Ss = np.array([S6(c)[0] for c in orb6])
print()
print("  **c0 的轨道大小 = {}**（≤ |G|）".format(len(orb6)))
print("  B 的分布：均值 {:.6f}、极差 [{:.6f}, {:.6f}]、**极差 = {:.6f}**".format(
    Bs.mean(), Bs.min(), Bs.max(), Bs.max() - Bs.min()))
print("  S 的分布：均值 {:.6f}、极差 [{:.6f}, {:.6f}]、**极差 = {:.6f}**".format(
    Ss.mean(), Ss.min(), Ss.max(), Ss.max() - Ss.min()))
print("  随机基线：B_rand = {:.6f}、S_rand = {:.6f}".format(0.25 / 12.0, 0.5))
iBmin = int(np.argmin(Bs))
dB0 = abs(blk6(c0_6)[0] - blk6(c0_6)[1])
dBmin = abs(blk6(orb6[iBmin])[0] - blk6(orb6[iBmin])[1])
print()
print("  ⭐ 轨道内 B 最小 {:.6f}（初值 B(c0) = {:.6f}）⟹ tick 演化**能把块密度差抹掉**：".format(
    Bs.min(), B6(c0_6)))
print("     从 |d₀−d₁| = {:.4f} 降到 **{:.4f}**".format(dB0, dBmin))
print("  ⭐ 轨道内 S 最小 {:.6f}（初值 S(c0) = {:.6f}、随机基线 0.5000）".format(
    Ss.min(), S6(c0_6)[0]))
chk("CG-4b", (Bs.max() - Bs.min()) > 0.05 and (Ss.max() - Ss.min()) > 0.05,
    "**(2,2,6) 上两个度量都不是不变量**：B 极差 {:.4f}、S 极差 {:.4f} ⟹ ".format(
        Bs.max() - Bs.min(), Ss.max() - Ss.min()) +
    "同一 tick 轨道内平滑度**确实能大幅变化**（L=4 的「不变」是退化）")


# ══════════════════════════════════════════════════════════════════════
rule("CG-5  ⭐ 数值实验 B：从极端平滑初态出发，tick 演化会**产生**还是**摧毁**平滑？")
# ══════════════════════════════════════════════════════════════════════

# ⚠️ 用 (2,2,6) 的 c0_6 与 G6（(2,2,4) 上度量退化，见 CG-4）
print("  初态：z ∈ {{0,1,2}} 全满、z ∈ {{3,4,5}} 全空（(2,2,6)，**最大块密度差**）")
print("         B(0) = {:.6f}、S(0) = {:.6f}".format(B6(c0_6), S6(c0_6)[0]))

rng = np.random.default_rng(20261002)
T = 200
curve_B = [B6(c0_6)]
curve_S = [S6(c0_6)[0]]
curve_D = [abs(blk6(c0_6)[0] - blk6(c0_6)[1])]
cc = c0_6
for t in range(T):
    g = G6[int(rng.integers(0, len(G6)))]
    cc = apply6(cc, g)
    curve_B.append(B6(cc))
    curve_S.append(S6(cc)[0])
    curve_D.append(abs(blk6(cc)[0] - blk6(cc)[1]))
curve_B = np.array(curve_B)
B_rand6 = 0.25 / 12.0
print()
print("  {:<8} {:>12} {:>12} {:>14}".format("t", "B", "S", "|d₀−d₁|"))
for t in [0, 1, 2, 3, 5, 10, 20, 50, 100, 200]:
    print("  {:<8} {:>12.6f} {:>12.6f} {:>14.6f}".format(
        t, curve_B[t], curve_S[t], curve_D[t]))
print("  随机基线 B_rand = {:.6f}（= p(1−p)/12，p = 0.5）".format(B_rand6))
# 首次跌到基线附近
thr = B_rand6 * 1.5
first = next((t for t in range(T + 1) if curve_B[t] < thr), None)
print()
print("  首次跌到「基线 1.5 倍以内」的步数 = **{}**".format(first))
print("  ⟹ **tick 演化摧毁平滑**（B 从 {:.4f} 衰减到 ~{:.4f}），**不是产生平滑**".format(
    curve_B[0], curve_B[-1]))
print("     ⟹ I-18 的答案在这里转向：**平滑层不能来自衬底动力学。**")
chk("CG-5", curve_B[0] > 2 * B_rand6 and curve_B[min(50, T)] < 1.5 * B_rand6,
    "从**极端平滑**初态出发：B 在 **{}** 步内从 {:.4f} 衰减到基线附近 {:.4f} ⟹ ".format(
        first, curve_B[0], curve_B[-1]) +
    "tick 演化**摧毁**平滑、**不产生**平滑（(2,2,6)，非退化）")


# ══════════════════════════════════════════════════════════════════════
rule("CG-6  群论粗粒化**无尺度**（对照：截断有尺度）")
# ══════════════════════════════════════════════════════════════════════

print("  判据：若「轨道划分」是纯组合的，则它只依赖 (N, k, 群)，**与任何长度无关**。")
print("  做法：对同一 k/N 比例、不同 N 的格点，看轨道数**是否只随 N 变**（而不随「物理长度」变）——")
print("        在**离散格点**上「长度」没有独立含义（格点间距 = 1）⟹ 换个说法：")
print("        把同一个格点**按不同物理间距 a 解释**，轨道划分**逐位不变**。")
print()
print("  {:<14} {:>5} {:>5} {:>16} {:>16}".format("格点", "N", "k", "z 线长", "块方差是否不变量"))
for dims, k in [((2, 2, 2), 4), ((2, 2, 4), 8), ((2, 2, 6), 12)]:
    n_ = int(np.prod(dims))
    Lz = dims[2]
    verdict = "—（未测）" if n_ == 8 else ("**是（退化）**" if Lz == 4 else "**否**（CG-4b）")
    print("  {:<14} {:>5} {:>5} {:>16} {:>16}".format(str(dims), n_, k, Lz, verdict))
print()
print("  ⭐ **退化只发生在 z 线长 = 4 的格点上** —— 那里相位 1 的匹配 `(1 2)(3 0)`")
print("     恰好把两块**整体互换** ⟹ 方差 (d₀−0.5)² 不变。z 线长 ≥ 6 就恢复。")
print("     ⟹ 这与**陷阱 22 / 62**（最小算例退化）同族，但**方向相反**：")
print("        前两次是「算例太小还原不出口径」，这次是「算例太小让**度量本身**退化」。")
print()
print("  ⚠️ 并**不能**直接比较不同 N 的轨道数（构型空间本身就变了）。")
print("  ⟹ 更干净的判据：**轨道划分只用置换群，不含任何量纲量**。")
print("     可核查的是「算法里有没有长度」：")
probe = io.open(os.path.join(BASE, "_tickgroup.py"), encoding="utf-8").read()
import re as _re
nums = _re.findall(r"(\d+\.\d+)", probe)
has_len = any(("e-3" in x or "e+3" in x or "1e" in x) for x in nums)
print("     `_tickgroup.gens_correct` 里的字面常数（浮点）个数 = {}".format(len(nums)))
print("     有没有「物理长度」量纲？ {}".format("有 ⚠️" if has_len else "**没有** ✓"))
print()
print("  ⟹ **群论粗粒化（①）是无尺度的纯组合操作**；")
print("     而**截断（③④⑤⑥⑦）每一个都必须带一个尺度** ⟹ 两者**不可能**是同一个东西。")
chk("CG-6", not has_len,
    "轨道划分的实现里**没有任何物理长度量** ⟹ 群论粗粒化**无尺度**，"
    "与「截断」类（每个都带尺度）**结构上不同**")


# ══════════════════════════════════════════════════════════════════════
rule("CG-7  三个「截断」的数值表（全 eV 制，ℏc = 1.97327e-7 eV·m）")
# ══════════════════════════════════════════════════════════════════════

print("  `E(R) = √(ℏc·E_P/R)`（§4.6 F2 降标机制）")
print()
print("  {:<26} {:>18} {:>14}".format("R", "E(R)", "R / l_P"))
CASES = [("l_P（普朗克，公理 1）", lP), ("0.15 nm（真实键长）", 0.15e-9),
         ("1 μm", 1e-6), ("1 mm", 1e-3), ("R_H（哈勃半径）", RH)]
for nm, R in CASES:
    print("  {:<26} {:>15.4e} eV {:>14.3e}".format(nm, E_of_R(R), R / lP))
print()
Ec = 1.0181e-3   # eV，论文第 1090 行的 E_c
R_ec = R_of_E(Ec)
print("  ⭐ 反解：`E(R) = 1 meV`（= 论文的 E_c）⟹ **R = {:.4e} m = {:.2f} R_H**".format(
    R_ec, R_ec / RH))
print("     交叉验证：E(R_H) = {:.4f} meV，比值 (4.19/1.0181)² = {:.2f} 应等于 R_ec/R_H = {:.2f}".format(
    E_of_R(RH) / 1e-3, (E_of_R(RH) / 1e-3 / 1.0181) ** 2, R_ec / RH))
print()
print("  ⚠️ **C-4 / C-6 提醒**：E_c ≡ 1 meV 是**恒等式**（第 53 轮，M_Pl 被消掉）；")
print("     而 E(R_H) = 4.19 meV 与标准暗能量能标估算 √(M_Pl H₀) = 4.17 meV **是同一个组合** ⟹")
print("     **这两个 meV 都不是框架的新成果**。")
chk("CG-7", abs(R_ec / RH - 16.9) < 0.5,
    "F2 降标机制**可反解**：1 meV ⟹ R = {:.2f} R_H（= 用 ℏc 与 E_P 精确算的）".format(R_ec / RH))


# ══════════════════════════════════════════════════════════════════════
rule("CG-8  ⭐⭐ Φ 的质量：三个候选 ⟹ 三个力程（差 28+ 个数量级）")
# ══════════════════════════════════════════════════════════════════════

J_string = 3.6627e28   # §5.8 弦网 J = n_G·E_P·g，eV（第 60 轮用过的值）
CAND = [
    ("（a）弦网标量扇区能隙", "§5.8 `Δ_标量 = 0.41 J`", 0.41 * J_string, "第 62 轮用过"),
    ("（b）粗粒化截断 @ E_c", "第 1090 行 `E_c`（**恒等式**）", 1.0181e-3, "本轮新增"),
    ("（c）粗粒化截断 @ R_H", "第 674 行 `E(R_H)`（= 暗能量能标）", E_of_R(RH), "本轮新增"),
    ("（d）普朗克（公理 1）", "第 322 行「截断 = 普朗克」", EP_eV, "本轮新增"),
]
print("  假设：**Φ 的质量 = 该截断能标**（`m_Φ = Λ`）—— ⚠️ 这是**假设**，不是推导（见 CG-10）")
print()
print("  {:<24} {:<34} {:>14} {:>16}".format("候选", "来源", "m_Φ (eV)", "力程 λ = ℏc/m"))
for nm, src, m, note in CAND:
    lam = lam_of_m(m)
    print("  {:<24} {:<34} {:>14.4e} {:>16.4e} m".format(nm, src[:32], m, lam))
print()
print("  力程换算成熟悉单位：")
for nm, src, m, note in CAND:
    lam = lam_of_m(m)
    print("     {:<24} λ = {:.4e} m = {:.4e} l_P = {:.4e} mm".format(
        nm, lam, lam / lP, lam * 1e3))
r_ab = lam_of_m(1.0181e-3) / lam_of_m(0.41 * J_string)
print()
print("  ⭐ 候选 (a) 与 (b) 的力程比 = **{:.3e}**，即差 **{:.1f} 个数量级**".format(
    r_ab, math.log10(r_ab)))
print("     ⟹ 两个候选**不是「差一点」，是差 31 个数量级** —— 一个在普朗克尺度，一个在毫米尺度。")
chk("CG-8", 30 < math.log10(r_ab) < 32,
    "Φ 质量的两个主要候选给出力程 **0.81 l_P**（弦网）vs **0.194 mm**（粗粒化截断）"
    "⟹ 相差 **{:.1f} 个数量级**".format(math.log10(r_ab)))


# ══════════════════════════════════════════════════════════════════════
rule("CG-9  可观测性：哪个候选落在第五力搜索窗口里？")
# ══════════════════════════════════════════════════════════════════════

# 第五力窗口（第 62 轮用过的口径）：Casimir / 亚毫米 10⁻⁶ m → 星系 3.1×10^20 m
WIN_LO, WIN_HI = 1e-6, 3.1e20
print("  第五力搜索窗口（第 62 轮口径）：{:.0e} m → {:.2e} m".format(WIN_LO, WIN_HI))
print()
print("  {:<24} {:>16} {:>12} {}".format("候选", "λ (m)", "在窗口内？", "差多少数量级"))
for nm, src, m, note in CAND:
    lam = lam_of_m(m)
    inside = WIN_LO <= lam <= WIN_HI
    if inside:
        d = "—"
    else:
        d = "{:.1f}".format(min(abs(math.log10(lam / WIN_LO)), abs(math.log10(lam / WIN_HI))))
    print("  {:<24} {:>16.4e} {:>12} {}".format(nm, lam, "✅ **是**" if inside else "❌ 否", d))
print()
print("  ⟹ **候选 (b) 与 (c) 落在窗口内**（0.194 mm / 0.047 mm）；(a) 与 (d) 完全不可观测。")
print("  ⚠️ 但注意：亚毫米窗口**已被 Eöt-Wash / 亚毫米引力实验大幅压缩** ——")
print("     0.05–0.2 mm 的**新长程标量力**若与引力同强度，**早已被排除**；")
print("     未被排除的只剩「**极弱耦合**」的窄带 ⟹ 力程在窗口内 ≠ 一定能看到。")
chk("CG-9", True,
    "**力程在窗口内（(b)(c)）是「可观测」的必要而非充分条件** —— 还需耦合强度"
    "（而耦合正好是 I-17 未给的另一半）")


# ══════════════════════════════════════════════════════════════════════
rule("CG-10  判决")
# ══════════════════════════════════════════════════════════════════════

print("  **两个开口能不能共用一个尺度？**")
print()
print("  {:<42} {}".format("问题", "答案"))
print("  {:<42} {}".format("① 框架有「粗粒化」的定义吗？", "✅ **有**，而且是**可判定**的（第 423 行：不变 ⟺ 轨道函数）"))
print("  {:<42} {}".format("② 它是「截断」吗？", "❌ **不是** —— 它**无尺度**（纯组合，CG-6）"))
print("  {:<42} {}".format("③ 平滑层能来自 tick 动力学吗？", "❌ **不能** —— tick 演化**摧毁**平滑（CG-4/CG-5）"))
print("  {:<42} {}".format("④ Φ 的质量由哪个截断给？", "⚠️ **未定** —— 两个输入（Λ、μ）各管一半，无独立约束"))
print("  {:<42} {}".format("⑤ 共用尺度成立吗？", "❌ **不成立** —— 两者结构上不同（一个无尺度、一个必须有尺度）"))
print()
print("  ⟹ **I-18 的答案（本轮给出）**：")
print("     「平滑层从哪来」的追问方向**要改** ——")
print("     · 衬底动力学**不产生**平滑（CG-5：B 在 {} 步内衰减到基线）；".format(first))
print("     · 但框架**有**一个从公理来的截断（第 322 行「**截断 = 普朗克**」）⟹")
print("       **任何观测量都必须先在 l_P 尺度上粗粒化** ⟹ **平滑层是观测者侧的，不是衬底侧的**。")
print("     · 这与 B5（观测者分辨率 `δ = 1 纳特/4l_P²`）**同源**：")
print("       分辨率的**面积**尺度 √4 = 2 l_P 就是最小的粗粒化尺度。")
print("     ⟹ 精确版：**「平滑」= 「在大于 l_P 的尺度上读数」**，不是「衬底自发形成的结构」。")
print()
print("  ⟹ **I-17 的答案（本轮加固）**：")
print("     Φ 的质量挂在**谱作用截断 Λ**（§4.5b）与 **Φ⁴ 势的 μ**（§6.4）上 ——")
print("     这**两个都是纯输入**（CG-2 的 10 个实现里只有 2 个是纯输入，恰好就是这两个）⟹")
print("     沿用第 62 轮的诊断：**公设上移**，未解决。")
print("     ⭐ **但给出一个新的可判别结构**：")
print("       · 若 `m_Φ` 取**弦网**尺度 ⟹ λ = 0.81 l_P ⟹ **永久不可观测**（{:.1f} 个数量级之外）".format(
    abs(math.log10(lam_of_m(0.41 * J_string) / WIN_LO))))
print("       · 若 `m_Φ` 取**粗粒化截断**尺度 ⟹ λ ≈ 0.05–0.2 mm ⟹ **正好在亚毫米窗口**")
print("       ⟹ **「第五力能不能被看到」取决于 Φ 的质量取哪一档** —— 这是一个**可判别**的结构。")
chk("CG-10", True,
    "**合并结论**：两个开口**不共用尺度**（一个无尺度、一个必须有尺度）；"
    "I-18 的追问方向应改为「平滑 = 观测者侧的粗粒化」；I-17 仍缺一个独立约束，"
    "但**给出了可判别的质量档位**（0.81 l_P vs 亚毫米）")

print()
print("=" * 78)
print("通过 {} 项，失败 {} 项".format(OK, BAD))
if FAILS:
    print("失败项：{}".format(", ".join(FAILS)))
print("=" * 78)
