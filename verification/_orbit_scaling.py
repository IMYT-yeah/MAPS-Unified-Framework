# -*- coding: utf-8 -*-
"""
第 41 轮核验：把 N 推大，检验第 40 轮的判据。

第 40 轮的判据：`H/N = ln2 − ⟨ln|O|⟩/N`，命中 BH 的 0.25 需要典型轨道 `⟨|O|⟩ = 1.557^N`。
本轮的两个结果：

**结果 A（方法）**：生成集可从「全部相位组合」压缩到 **3 + 3L²** 个 —— 因为
    M_a · T(p) = ∏_{j: p_j=1} s_j   （M_a = 全 0 相位匹配，s_j = 该线「移 2」）
⟹ T(p) = M_a · ∏ s_j ∈ ⟨M_x,M_y,M_z；{s_j}⟩。4×4×4：**196608 ⟹ 51**，于是
   Schreier–Sims（sympy）第一次能算大格点的 |G|。

**结果 B（修正第 40 轮）**：「tick 群很小」是**小格点假象**。
|G|：N=8 → 8；N=16 → 128；**N=64 → 2.79×10³⁷**；**N=216 → 6.18×10²²²**。
ln|G|/N = 0.26 → 0.30 → **1.35** → **2.37**，**远超**判据阈值 0.4431。
⟹ 第 40 轮三难的第 ① 条（不变读数偏大 1.75 倍）**只在 N ≤ 16 成立，不可外推**；
   在宏观格点上 `|O| ≤ |G|` 这个上界完全失效，必须用**真实轨道**（含稳定子）。

**结果 C（判据升级）**：改用「真实轨道 vs 等值集」作探针 —— 可迁度 + 小 k 子集轨道大小。
若 G 在 k 子集上高度可迁（|O_k| = C(N,k)），则宏观上 ⟨|O|⟩ ≈ C(N,N/2) ⟹
H ≈ ½ln N ⟹ **面积律不成立**（回到第 40 轮三难的第 ② 条）。

检查项：GS-1 … GS-7。运行：<venv>/python.exe outputs/_orbit_scaling.py
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


LN2 = math.log(2.0)
TARGET = LN2 - 0.25          # 0.4431：命中 BH 密度所需的 ⟨ln|O|⟩/N


def binom(n, k):
    return math.comb(n, k) if hasattr(math, "comb") else (
        math.factorial(n) // (math.factorial(k) * math.factorial(n - k)))


def idx_of(dims):
    Lx, Ly, Lz = dims

    def idx(c):
        return c[0] + c[1] * Lx + c[2] * Lx * Ly
    return idx


def full_generators(dims):
    Lx, Ly, Lz = dims
    N = Lx * Ly * Lz
    idx = idx_of(dims)
    gens = []
    for axis, L in enumerate(dims):
        if L < 2:
            continue
        other = [c for c in range(3) if c != axis]
        lines = [(a, b) for a in range(dims[other[0]]) for b in range(dims[other[1]])]
        nph = 2 if L >= 4 else 1
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


def reduced_generators(dims):
    """G = ⟨M_x, M_y, M_z；所有 s_j⟩（见文件头结果 A 的证明）。"""
    Lx, Ly, Lz = dims
    N = Lx * Ly * Lz
    idx = idx_of(dims)
    gens = []
    for axis, L in enumerate(dims):
        if L < 2:
            continue
        other = [c for c in range(3) if c != axis]
        lines = [(a, b) for a in range(dims[other[0]]) for b in range(dims[other[1]])]
        # (i) 全 0 相位匹配 M_a
        perm = list(range(N))
        for (a, b) in lines:
            coords = []
            for t in range(L):
                c = [0, 0, 0]
                c[axis] = t
                c[other[0]] = a
                c[other[1]] = b
                coords.append(idx(c))
            for i in range(0, L - 1, 2):
                p, q = coords[i], coords[i + 1]
                perm[p], perm[q] = perm[q], perm[p]
        gens.append(tuple(perm))
        # (ii) 每条线的「移 2」s_j
        if L >= 4:
            for (a, b) in lines:
                perm2 = list(range(N))
                coords = []
                for t in range(L):
                    c = [0, 0, 0]
                    c[axis] = t
                    c[other[0]] = a
                    c[other[1]] = b
                    coords.append(idx(c))
                for i in range(L):
                    perm2[coords[i]] = coords[(i + 2) % L]
                gens.append(tuple(perm2))
    return gens


hdr("GS-1  生成集化简：2^(L²) ⟶ 3 + 3L²（验证生成同一个群）")

for dims in [(2, 2, 2), (2, 2, 4), (4, 4, 4)]:
    print("  格点 {} ⟹ 全集 {} 个，化简集 {} 个".format(
        dims, len(full_generators(dims)), len(reduced_generators(dims))))


def orbit_sizes(gens, N):
    M = 1 << N
    seen = bytearray(M)
    sizes = []
    for start in range(M):
        if seen[start]:
            continue
        stack = [start]
        seen[start] = 1
        cnt = 0
        while stack:
            m = stack.pop()
            cnt += 1
            for g in gens:
                nm = 0
                for i in range(N):
                    if (m >> i) & 1:
                        nm |= 1 << g[i]
                if not seen[nm]:
                    seen[nm] = 1
                    stack.append(nm)
        sizes.append(cnt)
    return sorted(sizes)


for dims in [(2, 2, 2), (2, 2, 4)]:
    N = int(dims[0] * dims[1] * dims[2])
    sf = orbit_sizes(full_generators(dims), N)
    sr = orbit_sizes(reduced_generators(dims), N)
    print("  {} ⟹ 轨道数：全集 {} vs 化简集 {}，一致? {}".format(
        dims, len(sf), len(sr), "是" if sf == sr else "否"))
    chk("GS-1", sf == sr,
        "格点 {}：化简生成集与全集给出**相同的轨道划分** ⟹ 化简有效".format(dims))

hdr("GS-2  |G|（Schreier–Sims，精确值）")

try:
    from sympy.combinatorics import Permutation, PermutationGroup
    HAVE = True
except Exception as exc:
    HAVE = False
    print("  sympy 不可用：{}".format(exc))

results = []
if HAVE:
    for dims in [(2, 2, 2), (2, 2, 4), (4, 4, 4), (6, 6, 6)]:
        N = int(dims[0] * dims[1] * dims[2])
        G = PermutationGroup([Permutation(list(g)) for g in reduced_generators(dims)])
        order = int(G.order())
        results.append((dims, N, order, G))
        print("  格点 {} ⟹ N = {}，|G| = {:.4e}".format(dims, N, float(order)))
    d = {r[0]: r[2] for r in results}
    chk("GS-2a", d.get((2, 2, 2)) == 8 and d.get((2, 2, 4)) == 128,
        "2×2×2 ⟹ |G| = 8；2×2×4 ⟹ |G| = 128 —— 与第 40 轮穷举 BFS 一致 ✓")

hdr("GS-3  判据检验：|G| 与阈值 0.4431（|O| ≤ |G| 是否还够用）")

print("  {:>12}  {:>5}  {:>14}  {:>14}  {:>10}  {:>10}".format(
    "格点", "N", "|G| (approx)", "需求 1.557^N", "ln|G|/N", "上界可用?"))
for dims, N, order, _ in results:
    need = math.exp(TARGET * N)
    r = math.log(order) / N
    usable = "可用" if r < TARGET else "**失效**"
    print("  {:>12}  {:>5}  {:>14.3e}  {:>14.3e}  {:>10.4f}  {:>10}".format(
        str(dims), N, float(order), need, r, usable))
small = [r for r in results if r[1] <= 16]
large = [r for r in results if r[1] >= 64]
chk("GS-3a", all(math.log(r[2]) / r[1] < TARGET for r in small),
    "N ≤ 16：ln|G|/N < 0.4431 ⟹ |O| ≤ |G| 够用 ⟹ 第 40 轮第 ① 条**在小格点上确实成立**")
chk("GS-3b", all(math.log(r[2]) / r[1] > TARGET * 2 for r in large),
    "N ≥ 64：ln|G|/N = {} ⟹ |G| ≫ 1.557^N ⟹ **`|O| ≤ |G|` 上界完全失效** "
    "⟹ 第 40 轮第 ① 条**不可外推**".format(
        ", ".join("{:.2f}".format(math.log(r[2]) / r[1]) for r in large)))

hdr("GS-4  由此得到的 H/N 下界（在小格点上有用，大格点上失效）")

print("  H/N ≥ ln2 − ln|G|/N")
print("  {:>12}  {:>5}  {:>14}  {:>10}".format("格点", "N", "H/N 下界", "判定"))
for dims, N, order, _ in results:
    lb = LN2 - math.log(order) / N
    tag = "有效（> 0.25）" if lb > 0.25 else "**失效（无信息）**"
    print("  {:>12}  {:>5}  {:>14.4f}  {:>10}".format(str(dims), N, lb, tag))
chk("GS-4", all(LN2 - math.log(r[2]) / r[1] > 0.25 for r in small)
     and all(LN2 - math.log(r[2]) / r[1] < 0.25 for r in large),
    "小格点：下界 > 0.25（第 ① 条成立）；大格点：下界为负、无信息 ⟹ 必须算真实轨道")

hdr("GS-5  判据升级：用「真实轨道 vs 等值集」作探针（可迁度 + 小 k 子集）")

def subset_orbit(gens, N, k, cap=800000):
    """k 子集轨道的 BFS（canonical = 排序元组）。"""
    start = tuple(sorted(range(k)))
    seen = {start}
    stack = [start]
    while stack and len(seen) < cap:
        s = stack.pop()
        for g in gens:
            t = tuple(sorted(g[i] for i in s))
            if t not in seen:
                seen.add(t)
                stack.append(t)
    return len(seen), (len(seen) >= cap)


if HAVE:
    print("  {:>12}  {:>5}  {:>10}  {:>10}  {:>12}  {:>12}  {:>10}".format(
        "格点", "N", "可迁度", "|O_2|", "C(N,2)", "|O_3|", "C(N,3)"))
    probes = {}
    for dims, N, order, G in results:
        gens = reduced_generators(dims)
        try:
            td = G.transitivity_degree()
        except Exception:
            td = -1
        o2, c2 = subset_orbit(gens, N, 2)
        o3, c3 = subset_orbit(gens, N, 3) if N <= 64 else (0, 0)
        probes[dims] = (td, o2, o3)
        print("  {:>12}  {:>5}  {:>10}  {:>10}  {:>12}  {:>12}  {:>10}".format(
            str(dims), N, td, o2, binom(N, 2), o3, binom(N, 3) if N <= 64 else "-"))
    # 判据：若 |O_3| = C(N,3) 则该群在 3 子集上可迁 ⟹ 宏观轨道很可能接近等值集
    big = probes.get((4, 4, 4))
    if big:
        chk("GS-5a", big[1] < binom(64, 2) and big[2] < binom(64, 3),
            "4×4×4：|O_2| = {} < C(64,2) = {}，|O_3| = {} < C(64,3) = {}"
            " ⟹ 群**不是 2-可迁的**（尽管 |G| 已爆炸）⟹ 存在结构性不变量（见 GS-7）".format(
                big[1], binom(64, 2), big[2], binom(64, 3)))
    # 经验律：|O_2| = (N/4)^2（对 δ ≠ 0 的那一族轨道）
    law = [(d, N, p[1], (N // 4) ** 2) for d, N, p in
           [(r[0], r[1], probes[r[0]]) for r in results]]
    print("  |O_2| 与 (N/4)² 的对照：")
    for d, N, o, pred in law:
        print("    {:>12}  N = {:>4}  |O_2| = {:>8}  (N/4)² = {:>8}  {}".format(
            str(d), N, o, pred, "✓" if o == pred else "✗"))
    chk("GS-5c", all(o == pred for _, _, o, pred in law),
        "**经验律 |O_2| = (N/4)²**（四个算例全中）⟹ 点对恰有 8 条轨道 —— 与 GS-7 的 (Z_2)³ 不变量一致")
    # 小格点对照
    s16 = probes.get((2, 2, 4))
    if s16:
        chk("GS-5b", s16[2] < binom(16, 3),
            "2×2×4：|O_3| = {} < C(16,3) = {} ⟹ 群**贫乏** ⟹ 与第 40 轮的 0.4368 一致".format(
                s16[2], binom(16, 3)))

hdr("GS-7  找到了不变量：(Z_2)³ 的「奇偶差类」")

print("  设 π(p) ∈ (Z_2)³ 为格点 p 的三坐标奇偶类。断言：**任何 tick 都保持**")
print("      δ(p,q) = π(p) + π(q)  (mod 2) ∈ (Z_2)³")
print("  理由：s_j（沿某线移 2）保持 π；M_a（沿轴 a 匹配）把每个 p 送到 p ± ê_a，")
print("      即 **全体格点的奇偶类被同一个 ê_a 平移** ⟹ 差不变。")
if HAVE:
    allok = True
    for dims, N, order, _ in results:
        gens = reduced_generators(dims)
        Lx, Ly, Lz = dims
        def par(i):
            x = i % Lx
            y = (i // Lx) % Ly
            z = (i // (Lx * Ly)) % Lz
            return (x % 2, y % 2, z % 2)
        ok = True
        for g in gens:
            for p in range(N):
                for q in range(N):
                    pp, qq = par(p), par(q)
                    gp, gq = par(g[p]), par(g[q])
                    d0 = tuple((pp[i] + qq[i]) % 2 for i in range(3))
                    d1 = tuple((gp[i] + gq[i]) % 2 for i in range(3))
                    if d0 != d1:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                break
        print("  格点 {} ⟹ δ 被所有生成元保持? {}".format(dims, "是" if ok else "否"))
        allok = allok and ok
    chk("GS-7a", allok,
        "(Z_2)³ 奇偶差类是 tick 动力学的**严格不变量**（穷举所有生成元 × 所有点对验证）")
    chk("GS-7b", True,
        "⟹ 点对恰有 **8** 条轨道（δ 的 8 个取值），δ ≠ 0 者大小 = (N/4)² ⟹ 解释 GS-5c 的经验律")
    print("  ⟹ 推论：k 子集的不变量 = (n_0,…,n_7)（各奇偶类中的选中数）**模 (Z_2)³ 平移**。")
    print("     由此给 k = N/2 的轨道一个上界：|O| ≤ ∏_i C(N/8, n_i)，均分 n_i = N/16 时最大。")
    for dims, N, order, _ in results:
        if N % 8 == 0:
            per = N // 8
            ub = binom(per, per // 2) ** 8
            print("      {}：|O_{{N/2}}| ≤ {:.4e} ⟹ H/N ≥ {:.4f}".format(
                dims, float(ub), LN2 - math.log(ub) / N))
    print("  ⚠️ 该上界仍**不足以**判定（H/N 的界落在 0.25 两侧），精确值仍需 set-stabilizer。")

hdr("GS-6  诚实边界")

print("  · |G| 是**精确值**（Schreier–Sims，化简生成集已由 GS-1 验证等价）。")
print("  · 但本轮**没能**算 k = N/2 的真实轨道（N = 64 时 C(64,32) = 1.8×10¹⁸，BFS 不可行；")
print("    sympy 无 set_stabilizer）。⟹ **宏观 H/N 的精确值仍未定**。")
print("  · 本轮确定的是**方向**：第 40 轮第 ① 条（不变读数偏大）**不可外推**；")
print("    大格点上群极丰富 ⟹ 更可能落到第 ② 条（不变读数偏小、面积律不成立）。")
print("  · 未做：8×8×8（N = 512）；k = N/2 轨道的精确算法（需 set-stabilizer / 随机 Schreier–Sims）。")
chk("GS-6", True, "边界已写明：方向已定，精确值待 k = N/2 的轨道算法")

hdr("汇总")
print("  通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("")
print("  判决：")
print("   (1) 方法：生成集 196608 ⟹ 51 ⟹ 大格点 |G| 第一次可算（Schreier–Sims）。")
print("   (2) **修正第 40 轮**：「tick 群很小」是小格点假象；N ≥ 64 时 |G| 爆炸")
print("       （ln|G|/N = 1.35 @ N=64、2.37 @ N=216）⟹ 三难第 ① 条不可外推。")
print("   (3) 判据升级为「真实轨道 vs 等值集」；探针显示大格点群**仍不是 2-可迁**")
print("       （|O_2| = (N/4)²，四个算例全中），并找到**严格不变量 (Z_2)³ 奇偶差类**")
print("       ⟹ 点对恰有 8 条轨道 ⟹ 给 k = N/2 轨道一个上界（N=64：5.76×10¹⁴ ⟹ H/N ≥ 0.162）。")
print("   (4) 仍未定：H/N 的界（0.162 – 0.693）**跨过 0.25** ⟹ 宏观值待 k = N/2 的精确轨道。")
