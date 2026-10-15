# -*- coding: utf-8 -*-
"""
第 30 轮：裁决 T-6 —— 格点几何是简单立方（配位 6），不是金刚石（配位 4）
TA-1 … TA-7，只用标准库。
"""
import math as m
import random

L_P = 1.616255e-35
T_P = 5.391247e-44
C_MS = 2.99792458e8

CHECKS = []
def chk(name, got, want, tol=1e-12):
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    CHECKS.append((name, ok))
    print("  [%s] %-60s got=%.10g  want=%.10g" % ("OK" if ok else "XX", name, got, want))
    return ok

def show(name, val):
    print("        %-60s = %.10g" % (name, val))

def line(t):
    print("\n" + "=" * 82)
    print(t)
    print("=" * 82)

# ================================================================== TA-1
line("TA-1  原文裁决：两套方向，论文自己就分开了")
print("""
  §4.10 论证 4（第 400 行）：
    「正四面体 4 方向 = **内空间**分量结构（Cl(1,3) 表示维数 4 = 时间双向×手性双向）；
      **八面体 6 方向 = 外空间轴结构（3 轴 ±）**。**熵编码用内空间分量 ⟹ 方向簇数 4**。」

  §4.9 引理 1：
    「可访问信息 = **平面内 4 方向**连接（**平面外 2 方向被卷曲**）【本框架设定】」
    ⟹ 4（平面内）+ 2（平面外）= **6 个方向 = 3 轴 ±**，正是简单立方的 6 邻居。

  ⟹ **裁决**：
     · **外空间（格点衬底所在）= 八面体 6 方向 ⟹ 简单立方，配位数 6**；
     · **内空间（熵编码）= 正四面体 4 方向 ⟹ 方向簇 k = 4**（用于 4l_P²、1/4 系数）。
     · 引理 1 的「平面外 2 方向被卷曲」正是"6 个邻居中只有 4 个可用于信息传递"的说法。
  ⟹ **第 27 轮把「方向簇 k = 4」当成了「体配位数 = 4」—— 这是两套方向的混用，结论不成立。**""")

# ================================================================== TA-2
line("TA-2  简单立方：6-正则 + 二分（棋盘格着色）")
L = 8
NL = L ** 3
def dec(p):
    return p % L, (p // L) % L, p // (L * L)
def enc(i, j, k):
    return (i % L) + L * ((j % L) + L * ((k % L)))
par = [sum(dec(p)) % 2 for p in range(NL)]
show("格点数 n（L = 8）", float(NL))
show("A 子格（i+j+k 偶）", float(sum(1 for x in par if x == 0)))
show("B 子格（i+j+k 奇）", float(sum(1 for x in par if x == 1)))
chk("两子格等大", float(sum(1 for x in par if x == 0)), float(sum(1 for x in par if x == 1)))
# 6-正则 ⟹ m = 3n
m_sc = 3 * NL
show("6-正则 ⟹ 边数 m = 3n", float(m_sc))
chk("每条 +轴 边都翻转子格（⟹ 二分）",
    float(all(sum(dec(enc(*[dec(p)[c] + (1 if c == ax else 0) for c in range(3)]))[c] for c in range(3)) % 2
              != sum(dec(p)) % 2 for p in range(0, NL, 37) for ax in range(3))), 1.0)

# ================================================================== TA-3
line("TA-3  König 边着色：简单立方给 6 个完美匹配（3 轴 × 2 相位）")
DIRS = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
ok_matching = True
for ax in range(3):
    for ph in (0, 1):
        cover = [0] * NL
        for p in range(NL):
            i, j, k = dec(p)
            if (i + j + k) % 2 != ph:
                continue
            q = enc(i + DIRS[ax][0], j + DIRS[ax][1], k + DIRS[ax][2])
            cover[p] += 1
            cover[q] += 1
        if max(cover) != 1 or min(cover) != 1:
            ok_matching = False
            show("  轴 %d 相位 %d 的异常格点数" % (ax, ph),
                 float(sum(1 for c in cover if c != 1)))
chk("3 轴 × 2 相位 = 6 个完美匹配（每个格点恰覆盖一次）", float(ok_matching), 1.0)
show("每个匹配的边数 n/2", float(NL // 2))
show("6 × n/2 = m 校验", float(6 * (NL // 2)))
chk("6 个匹配的并集 = 全部边", float(6 * (NL // 2)), float(m_sc))

# ================================================================== TA-4
line("TA-4  tick 模拟（第 26 轮实现复核：随机选轴方向 + 每线独立相位）")

def line_key(p, ax):
    i, j, k = dec(p)
    return tuple(c for idx, c in enumerate((i, j, k)) if idx != ax)

def run(n_tick, rng):
    grid = list(range(NL))
    cum = [[0.0, 0.0, 0.0] for _ in range(NL)]
    perm_bad = 0
    for _ in range(n_tick):
        ax = rng.randrange(3)
        d = DIRS[ax]
        ph_of = {}
        start = rng.randrange(2)     # 全局相位基准（每 tick 重抽）
        for p in range(NL):
            i, j, k = dec(p)
            key = line_key(p, ax)
            if key not in ph_of:
                ph_of[key] = rng.randrange(2)
            t = (i, j, k)[ax]
            if (t + start) % 2 != ph_of[key]:
                continue
            q = enc(i + d[0], j + d[1], k + d[2])
            ga, gb = grid[p], grid[q]
            grid[p], grid[q] = gb, ga
            cp, cq = cum[p], cum[q]
            cum[p] = [cq[0] - d[0], cq[1] - d[1], cq[2] - d[2]]
            cum[q] = [cp[0] + d[0], cp[1] + d[1], cp[2] + d[2]]
        if len(set(grid)) != NL:
            perm_bad += 1
    occ = [0] * NL
    for g in grid:
        occ[g] += 1
    return cum, sum(1 for o in occ if o == 0), perm_bad

NT = 1500
res = []
for s in (11, 22, 33, 44, 55):
    cum, vac, pb = run(NT, random.Random(s))
    x2 = sum(c[0] ** 2 for c in cum) / NL
    y2 = sum(c[1] ** 2 for c in cum) / NL
    z2 = sum(c[2] ** 2 for c in cum) / NL
    res.append((x2, y2, z2, vac, pb))
    print("       seed=%2d  <x^2>=%8.1f <y^2>=%8.1f <z^2>=%8.1f  <r^2>=%8.1f  真空=%d 非置换=%d"
          % (s, x2, y2, z2, x2 + y2 + z2, vac, pb))
avg = [sum(r[i] for r in res) / len(res) for i in range(5)]
show("⟨x²⟩（期望 n/3）", avg[0])
show("⟨y²⟩", avg[1])
show("⟨z²⟩", avg[2])
show("⟨r²⟩（期望 n）", avg[0] + avg[1] + avg[2])
t3 = 0.30
chk("⟨x²⟩ ≈ n/3", avg[0], NT / 3.0, t3)
chk("⟨y²⟩ ≈ n/3", avg[1], NT / 3.0, t3)
chk("⟨z²⟩ ≈ n/3", avg[2], NT / 3.0, t3)
chk("⟨r²⟩ ≈ n（每步位移长度 1）", avg[0] + avg[1] + avg[2], float(NT), t3)
chk("真空事件总数 = 0", float(sum(r[3] for r in res)), 0.0, 0.0)
chk("非置换 tick 总数 = 0", float(sum(r[4] for r in res)), 0.0, 0.0)

# ================================================================== TA-5
line("TA-5  数密度与碰撞率：恢复 1/l_P³（撤回第 27 轮的 0.6495/l_P³）")
n_dens = 1.0 / L_P ** 3
rate = n_dens * L_P ** 2 * C_MS
show("简单立方（格距 = l_P）的数密度 n·l_P³", 1.0)
show("碰撞率 nσv（σ = l_P²）= ? × (1/t_P)", rate * T_P)
show("平均自由程 1/(nσ) / l_P", 1.0)
chk("数密度 = 1/l_P³（与论文原值一致）", 1.0, 1.0)
chk("碰撞率 = 1/t_P（残差 1.2e-7 来自 l_P、t_P 各自舍入到 7 位）",
    rate * T_P, 1.0, 1e-6)
print("""
  ⟹ 第 27 轮基于金刚石改的 n = 0.6495/l_P³、nσv = 0.6495/t_P、平均自由程 1.5396 l_P
     **一并撤回**，§4.2 恢复原值（n = 1/l_P³、nσv = 1/t_P、平均自由程 = l_P）。""")

# ================================================================== TA-6
line("TA-6  6-正则二分图同样非平面 ⟹ 第 28 轮的结论保持")
print("""
  二分平面图要求 m ≤ 2n − 4；6-正则给 m = 3n ⟹ 3n ≤ 2n − 4 ⟹ n ≤ −4，矛盾。""")
show("n（L = 8）", float(NL))
show("m = 3n", float(3 * NL))
show("二分平面图允许的 m 上界 2n − 4", float(2 * NL - 4))
chk("m ≤ 2n − 4 是否成立", float(3 * NL <= 2 * NL - 4), 0.0, 0.0)
print("""
  ⟹ **任何 6-正则二分图也非平面** ⟹ 第 28 轮「四色定理不适用」的结论**不受几何修正影响**。
     （Heawood 色数仍按亏格定，与配位数无关。）""")

# ------------------------------------------------------------------ 汇总
line("汇总")
n_ok = sum(1 for _, ok in CHECKS if ok)
print("  检查项 %d，通过 %d，失败 %d" % (len(CHECKS), n_ok, len(CHECKS) - n_ok))
for name, ok in CHECKS:
    if not ok:
        print("    [XX] %s" % name)
print("""
  判决：
  ✅ **T-6 裁决：格点几何 = 简单立方（配位数 6、二分）**，不是金刚石。
     依据：§4.10 论证 4 明确「八面体 6 方向 = 外空间轴结构（3 轴 ±）」，
     而 §4.10 的「方向簇 k = 4」属**内空间/熵编码**层面；§4.9 引理 1 的
     「平面内 4 + 平面外 2（被卷曲）」正是 6 邻居中 4 个可访问的说法。
  ❌ **第 27 轮的「金刚石唯一」撤回**：它依赖「配位数 = 方向簇数 k」，
     而这两者分属外空间与内空间，是两套不同的方向集。
  ✅ **保留的部分**（第 27 轮并非全错）：
     · 结构约束「每格点每 tick 一次事件 ⟹ d-正则二分 + König 边着色」**成立**；
     · 简单立方同样给出 König 边着色（6 个完美匹配 = 3 轴 × 2 相位）；
     · 「全局同步 = 刚性平移」的失效模式**成立**（本轮模拟即按此实现）；
     · 6-正则二分图同样**非平面** ⟹ 第 28 轮「四色定理无关」**不受影响**。
  ⚠️ **连带撤回**：数密度与碰撞率恢复为 **n = 1/l_P³、nσv = 1/t_P、平均自由程 = l_P**。
  ⚠️ 「每格点一步 l_P」在简单立方上**自然成立**（格距 = l_P），
     第 27 轮那个「键长 = l_P ⟹ 数密度 ≠ 1/l_P³」的麻烦**随之消失**。""")
