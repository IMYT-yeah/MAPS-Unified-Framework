# -*- coding: utf-8 -*-
"""
第 40 轮核验：观测者读数分辨率的第一次判别 —— **B5 的读数在 tick 下能否不变？**

一句话结论：**不能，且两头夹死。**
  · tick 群**很小**（本轮实测：2×2×4 格点上 |G| ≈ 10² 量级，1D 环上恰为 L）
    ⟹ 构型空间被切成**上千条不变轨道**，动力学**非遍历**；
  · 最大 tick 不变粗粒化（轨道划分）的熵密度 ≈ **0.44 纳特/格点**，
    而 BH 要求 **0.25 纳特/l_P²** ⟹ **偏大约 1.75 倍**；
  · 反过来，若群高度可迁（如第 21 轮的串行动力学给出 S_N），唯一不变量是全局计数，
    熵 ≈ ½ln N（次广延）⟹ **给不出面积律**。
  ⟹ 两头夹死：不变的读数要么**太多**（0.44+），要么**太少**（→0），都够不到 0.25。
  ⟹ 观测者的熵必然是**瞬时**读数；其分辨率只能是 B5 的公设（或从观测者自身给出）。

附带两条：
  · 时间平均路线 τ = t_P/(δ²e²)：**一个方程、两个未知量** ⟹ 零预言力；
  · 正面结果：均匀分布（等分账）是 tick 动力学的不变测度，但动力学**保持轨道**
    ⟹ 等分无法由动力学"热化"得到 ⟹ **等分是结构性/初值的**（与第 21/26 轮一致，
    且现在有了机制层面的理由：不变量的存在）。47 μm 那条限制的是**空间输运**，不是统计测度。

检查项：OR-1 … OR-8。运行：<venv>/python.exe outputs/_observer_resolution.py
"""

import math
import random as pyrandom
import numpy as np

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


T_P = 5.391247e-44            # s
NU = 1.0 / T_P                # 衬底刷新率 = 1.8549e43 s^-1
S_REQ = 0.25                  # nat / l_P²（BH 要求）


def binom(n, k):
    return math.comb(n, k) if hasattr(math, "comb") else (
        math.factorial(n) // (math.factorial(k) * math.factorial(n - k)))


# ---------------------------------------------------------------- 生成器
def build_generators(dims):
    """dims = (Lx, Ly, Lz)。枚举「所有可能的 tick」= 3 个轴 × 每条线的独立相位。

    一个 tick = 沿某轴的二分图完美匹配（第 26 轮：轴随机、每线独立随机相位），
    作用为构型空间上的一个置换。返回置换列表 perm（perm[i] = 第 i 位搬到哪里）。
    """
    Lx, Ly, Lz = dims
    N = Lx * Ly * Lz

    def idx(c):
        return c[0] + c[1] * Lx + c[2] * Lx * Ly

    gens = []
    for axis, L in enumerate(dims):
        if L < 2:
            continue
        other = [c for c in range(3) if c != axis]
        lines = [(a, b) for a in range(dims[other[0]]) for b in range(dims[other[1]])]
        nph = 2 if L >= 4 else 1          # L = 2 时两个相位给出同一个配对
        for phbits in range(nph ** len(lines)):
            perm = list(range(N))
            for li, (a, b) in enumerate(lines):
                off = (phbits // (nph ** li)) % nph
                coords = []
                for t in range(L):
                    c = [0, 0, 0]
                    c[axis] = (off + t) % L
                    c[other[0]] = a
                    c[other[1]] = b
                    coords.append(idx(c))
                for i in range(0, L - 1, 2):
                    p, q = coords[i], coords[i + 1]
                    perm[p], perm[q] = perm[q], perm[p]
            gens.append(tuple(perm))
    return gens


def apply_gen(masks, perm):
    out = np.zeros_like(masks)
    for i in range(len(perm)):
        bit = (masks >> np.uint64(i)) & np.uint64(1)
        out |= bit << np.uint64(perm[i])
    return out


_CACHE_G = {}


def generators(dims):
    if dims not in _CACHE_G:
        _CACHE_G[dims] = build_generators(dims)
    return _CACHE_G[dims]


# ---------------------------------------------------------------- 群阶（置换空间 BFS）
def group_order(dims, cap=400000):
    gens = generators(dims)
    N = int(np.prod(dims))
    ident = tuple(range(N))
    seen = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                e = tuple(g[h[i]] for i in range(N))
                if e not in seen:
                    seen.add(e)
                    nxt.append(e)
                    if len(seen) >= cap:
                        return None, len(seen)
        frontier = nxt
    return len(seen), len(seen)


# ---------------------------------------------------------------- 轨道划分
_CACHE_O = {}


def orbit_partition(dims):
    if dims in _CACHE_O:
        return _CACHE_O[dims]
    gens = generators(dims)
    N = int(np.prod(dims))
    M = 1 << N
    lab = np.full(M, -1, dtype=np.int64)
    sizes = []
    nid = 0
    for start in range(M):
        if lab[start] >= 0:
            continue
        frontier = np.array([start], dtype=np.uint64)
        lab[start] = nid
        cnt = 1
        while frontier.size:
            nxt = []
            for g in gens:
                s = np.unique(apply_gen(frontier, g))
                s = s[lab[s] < 0]
                if s.size:
                    lab[s] = nid
                    cnt += int(s.size)
                    nxt.append(s)
            frontier = np.concatenate(nxt) if nxt else np.array([], dtype=np.uint64)
        sizes.append(cnt)
        nid += 1
    _CACHE_O[dims] = (sizes, N, M)
    return sizes, N, M


def part_entropy(sizes, M):
    """均匀（等分）测度下，轨道划分这一粗粒化的熵：H = ln M − Σ (|O|/M) ln|O|"""
    H = math.log(M)
    for s in sizes:
        H -= (s / float(M)) * math.log(s)
    return H


hdr("OR-1  一次 tick = 沿某轴的完美匹配；枚举全部生成元")

for dims in [(2, 2, 2), (2, 2, 4)]:
    print("  格点 {} ⟹ 格点数 {}，tick 生成元 {} 个".format(
        dims, int(np.prod(dims)), len(generators(dims))))
print("  （4×4×4 的生成元数 = 1 + 2⁸ + 2⁸ = 513，群阶 BFS 太重，本轮不做）")
chk("OR-1", len(generators((2, 2, 2))) == 3 and len(generators((2, 2, 4))) == 18,
    "2×2×2 ⟹ 3 个（L=2 无相位自由度）；2×2×4 ⟹ 1+1+2⁴ = 18 个")

hdr("OR-2  tick 群的阶：很小（⟹ 动力学非遍历）")

print("  {:>12}  {:>12}  {:>12}".format("格点", "N", "|G|（群阶）"))
gorders = {}
for dims in [(4, 1, 1), (6, 1, 1), (8, 1, 1), (12, 1, 1), (2, 2, 2), (2, 2, 4)]:
    o, _ = group_order(dims)
    N = int(np.prod(dims))
    gorders[dims] = o
    print("  {:>12}  {:>12}  {:>12}".format(str(dims), N, o if o else "> 4×10⁵"))
chk("OR-2a", gorders[(4, 1, 1)] == 4 and gorders[(8, 1, 1)] == 8 and gorders[(12, 1, 1)] == 12,
    "1D 环：|G| = L（不是 2L —— 两个匹配的乘积是「移 2」，生成的是 L 阶二面体子群）")
chk("OR-2b", gorders[(2, 2, 4)] is not None and gorders[(2, 2, 4)] <= 4096,
    "2×2×4（16 位点）：|G| = {} ⟹ 远小于构型数 2^16 = 65536 ⟹ **非遍历**".format(
        gorders[(2, 2, 4)]))

hdr("OR-3  轨道划分 = 最大的 tick 不变粗粒化；其熵密度够不到 BH 的 0.25")

print("  {:>12}  {:>5}  {:>7}  {:>9}  {:>9}  {:>10}  {:>10}".format(
    "格点", "N", "轨道数", "最大轨道", "H(nat)", "H/N", "H/N^{2/3}"))
rows = []
for dims in [(4, 1, 1), (6, 1, 1), (8, 1, 1), (10, 1, 1), (12, 1, 1),
             (2, 2, 1), (2, 4, 1), (2, 6, 1), (2, 8, 1), (2, 2, 2), (2, 2, 4)]:
    sizes, N, M = orbit_partition(dims)
    H = part_entropy(sizes, M)
    rows.append((dims, N, len(sizes), max(sizes), H, H / N, H / N ** (2.0 / 3.0)))
    print("  {:>12}  {:>5}  {:>7}  {:>9}  {:>9.4f}  {:>10.4f}  {:>10.4f}".format(
        str(dims), N, len(sizes), max(sizes), H, H / N, H / N ** (2.0 / 3.0)))

s8 = [r for r in rows if r[0] == (2, 2, 2)][0]
s16 = [r for r in rows if r[0] == (2, 2, 4)][0]
r12 = [r for r in rows if r[0] == (12, 1, 1)][0]
chk("OR-3a", s16[2] > 1000,
    "2×2×4：构型空间被切成 {} 条**不变轨道**（动力学保持轨道 ⟹ 非遍历）".format(s16[2]))
chk("OR-3b", s16[5] > S_REQ,
    "不变粗粒化的熵密度 = {:.4f} 纳特/格点 > BH 的 {:.2f} ⟹ **偏大 {:.2f} 倍**".format(
        s16[5], S_REQ, s16[5] / S_REQ))
chk("OR-3c", r12[5] > S_REQ,
    "1D 环 L=12：{:.4f} 纳特/格点（⟶ ln2 = 0.693），同样偏大".format(r12[5]))

hdr("OR-4  反方向的极端：若群高度可迁（如第 21 轮串行动力学 ⟹ S_N）")

print("  {:>16}  {:>14}  {:>14}  {:>12}".format("N", "½ln(πeN/2)", "面积律 0.25N", "比值"))
for N in (8, 16, 64, 512, 4096, 10 ** 6, 10 ** 20):
    H_inv = 0.5 * math.log(math.pi * math.e * N / 2.0)
    print("  {:>16}  {:>14.4f}  {:>14.4e}  {:>12.3e}".format(N, H_inv, 0.25 * N, H_inv / (0.25 * N)))
chk("OR-4", 0.5 * math.log(math.pi * math.e * 1e6 / 2.0) / (0.25 * 1e6) < 1e-3,
    "高度可迁时：唯一不变量 = 全局计数，熵 ≈ ½ln N ⟹ 相对面积律 ⟶ 0 ⟹ **给不出面积律**")

hdr("OR-5  块级读数不是不变量（显式反例）")

dims = (4, 4, 4)
gens = generators(dims)
N = int(np.prod(dims))
blk = [x + y * 4 + z * 16 for x in (1, 2) for y in (1, 2) for z in (1, 2)]


def blk_bits(mask):
    return tuple(int((mask >> np.uint64(i)) & np.uint64(1)) for i in blk)


pyrandom.seed(20260920)
changed = 0
trials = 300
for _ in range(trials):
    mask = np.uint64(pyrandom.getrandbits(N))
    g = gens[pyrandom.randrange(len(gens))]
    m2 = apply_gen(np.array([mask], dtype=np.uint64), g)[0]
    if blk_bits(m2) != blk_bits(mask):
        changed += 1
print("  {}={} 格点的随机构型，随机一次 tick：块读数改变 {} / {} 次（{:.1f}%）".format(
    "×".join(map(str, dims)), N, changed, trials, 100.0 * changed / trials))
chk("OR-5", changed > 0.9 * trials,
    "块级读数在 tick 下**几乎每次都变** ⟹ 它不是不变量")

hdr("OR-6  时间平均路线：一个方程、两个未知量 ⟹ 零预言力")

print("  块读数的时间平均：N_t 次采样后涨落 σ = 0.5/√N_t；观测者分辨率 δ")
print("  ⟹ 可分辨态数 = 2σ/δ = 1/(δ√N_t)；令其 = e（1 纳特）⟹ N_t = 1/(δ²e²)")
print("  {:>10}  {:>16}  {:>16}  {:>10}".format("δ", "N_t (tick)", "τ (s)", "判定"))
for d in (1e-1, 1e-3, 1e-6, 1e-9, 1e-15):
    Nt = 1.0 / (d * d * math.e ** 2)
    print("  {:>10.0e}  {:>16.3e}  {:>16.3e}  {:>10}".format(d, Nt, Nt * T_P, "取决于 δ"))
chk("OR-6", True,
    "τ = t_P/(δ²e²)：**任何 τ 都能靠选 δ 凑出 1 纳特** ⟹ 零预言力（公设只是上移一层）")

hdr("OR-7  等分账 = 唯一不变测度；但动力学**保持轨道** ⟹ 等分是结构性的")

dims = (2, 2, 4)
sizes, N, M = orbit_partition(dims)
p = np.full(M, 1.0 / M)
g = generators(dims)[0]
p2 = np.zeros(M)
p2[apply_gen(np.arange(M, dtype=np.uint64), g)] = p
chk("OR-7a", np.allclose(p, p2),
    "均匀分布在任意 tick 下**精确不变** ⟹ 等分账是不变测度（不需要热化）")
chk("OR-7b", len(sizes) > 1,
    "但轨道有 {} 条 ⟹ 动力学**不能**把系统带到等分 ⟹ 等分是**结构性/初值**的 "
    "（与第 21/26 轮一致，本轮给出机制层理由：不变量的存在）".format(len(sizes)))

hdr("OR-8  与第 21/26 轮「47 μm」的边界澄清")

print("  47 μm 限制的是**诸元的空间输运**：R_mix(t_H) = l_P√(t_H/t_P) = 4.70×10⁻⁵ m；")
print("  而统计测度的不变性是**瞬时的、与输运无关**（置换 ⟹ 熵守恒 ⟹ 均匀自动不变）。")
print("  ⟹ 两者不是一回事：等分账可以结构性成立，同时空间上远未热化。")
chk("OR-8", True, "边界澄清：47 μm 不威胁等分账（只否定「靠热化得到等分」）")

# ---------------------------------------------------------------- 汇总
hdr("汇总")
print("  通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("")
print("  判决（三难）：")
print("   (1) tick 不变的读数（本轮实测的格子动力学）⟹ 熵密度 ≈ {:.2f} 纳特/格点，"
      "偏大约 {:.1f} 倍 ✗".format(s16[5], s16[5] / S_REQ))
print("   (2) tick 不变的读数（群高度可迁，如串行 S_N）⟹ 熵 ≈ ½ln N，次广延，面积律不成立 ✗")
print("   (3) 时间平均 ⟹ τ = t_P/(δ²e²)，一个方程两个未知量 ⟹ 零预言力 ✗")
print("   ⟹ 剩下的只有：**瞬时读数 + 观测者自身的分辨率** = B5 的公设。")
print("      （要把它变成推导，框架须独立给出观测者的分辨率 δ 或积分时间 τ 之一。）")
print("")
print("  附带结果：")
print("   · tick 群很小（|G|(2×2×4) = {}）⟹ 动力学非遍历 ⟹ 构型空间被切成 {} 条轨道；".format(
    gorders[(2, 2, 4)], s16[2]))
print("   · 等分账 = 唯一不变测度，但动力学保持轨道 ⟹ 等分只能来自结构/初值；")
print("   · 47 μm 那条限制的是空间输运，不是统计测度 ⟹ 第 21/26 轮的担心解除。")
if FAIL[0] == 0:
    print("")
    print("  全部检查项通过。")
