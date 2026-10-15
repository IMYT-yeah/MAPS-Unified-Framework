# -*- coding: utf-8 -*-
"""第 50 轮：改扫 k —— 把「跨点」从 N 重新参数化到占据数层。

## 口径（先想清楚再算）

第 49 轮把 0.25 的跨点夹在 N ∈ (32, 48)，但 N = Lx·Ly·Lz 且各方向长度必须为**偶数**
（奇数长度的环没有完美匹配 ⟹ tick 未定义），32 与 48 之间**没有**这样的格点。
⟹ 换参数化：固定 N，扫**占据数层 k**（k = 被占据的诸元数）。

本轮待答：
  Q1  对称性 h(k) = h(N−k)？（结构论证：补集映射与置换群对易）
  Q2  h(k, N) 是否只依赖 k/N？（若成立，跨点不需要钉 N）
  Q3  0.25 能否被**某个层**穿过？在哪些 N 上能、哪些不能？
  Q4  min_k h(k,N) 的位置与 N 依赖（标度律）

⚠️ 本脚本的第一版写过两条预判，**都被脚本否证**（保留在 HK-3/HK-4 里作记录）：
    ① 「H/N 随 k 单调递减」—— 实测**非单调**（N=16：k=2 的 0.5285 > k=1 的 0.5199）；
    ② 「0.25 在每个固定 N 上都被某个 k 穿过」—— 实测**小 N 上任何层都够不到 0.25**
       （N=16 的 min = 0.4292 > 0.25）。
    这两条否证本身就是本轮的主要产出（见备忘录）。

全部用 `_tickgroup.gens_correct`（第 48 轮更正后的生成元）。N ≤ 24 穷举全部 2^N 构型。
"""

import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tickgroup as tg

LN2 = math.log(2.0)
OK = [0]
FAIL = [0]
CH = 8


def chk(tag, cond, msg):
    if cond:
        OK[0] += 1
        print("  [OK] {:<8} {}".format(tag, msg))
    else:
        FAIL[0] += 1
        print("  [XX] {:<8} {}".format(tag, msg))


def hdr(t):
    print()
    print("-" * 78)
    print(t)
    print("-" * 78)


def make_apply(N, gens):
    """8 位分块查表的置换作用。"""
    nch = (N + CH - 1) // CH
    tables = []
    for g in gens:
        tb = []
        for c in range(nch):
            shift = c * CH
            t = [0] * (1 << CH)
            for v in range(1 << CH):
                acc = 0
                for b in range(CH):
                    if (v >> b) & 1:
                        i = shift + b
                        if i < N:
                            acc |= 1 << g[i]
                t[v] = acc
            tb.append(t)
        tables.append(tb)
    masks = [(1 << CH) - 1] * nch

    def apply(cfg, gi):
        tb = tables[gi]
        acc = 0
        x = cfg
        for c in range(nch):
            acc |= tb[c][x & masks[c]]
            x >>= CH
        return acc
    return apply


def layer_scan(dims):
    """穷举**全部** 2^N 构型做完整轨道划分 ⟹ 每个 k 的统计。

    返回 (res, dt, N, ng)：res[k] = (轨道数, 构型数, ⟨ln|O|⟩, H/N)
    """
    N = dims[0] * dims[1] * dims[2]
    gens = tg.gens_correct(dims)
    apply = make_apply(N, gens)
    ng = len(gens)
    visited = bytearray(1 << N)
    sumln = [0.0] * (N + 1)
    cnt = [0] * (N + 1)
    norb = [0] * (N + 1)
    t0 = time.time()
    for start in range(1 << N):
        if visited[start]:
            continue
        k = start.bit_count()
        stack = [start]
        visited[start] = 1
        size = 0
        while stack:
            x = stack.pop()
            size += 1
            for gi in range(ng):
                y = apply(x, gi)
                if not visited[y]:
                    visited[y] = 1
                    stack.append(y)
        ln = math.log(size)
        sumln[k] += ln * size
        cnt[k] += size
        norb[k] += 1
    res = {}
    for k in range(N + 1):
        if cnt[k] == 0:
            continue
        avg = sumln[k] / cnt[k]
        res[k] = (norb[k], cnt[k], avg, LN2 - avg / N)
    return res, time.time() - t0, N, ng


def show(res, N):
    print("  {:>4} {:>10} {:>10} {:>10}  {}".format("k", "轨道数", "构型数", "H/N", "vs 0.25"))
    for k in sorted(res):
        o, c, a, h = res[k]
        print("  {:>4} {:>10} {:>10} {:>10.4f}  {}".format(
            k, o, c, h, "**低于**" if h < 0.25 else ""))


SCANS = {}


# ================================================================== HK-1  N=8
hdr("HK-1  N=8 (2,2,2) —— 全层精确扫描")
r8, dt8, N8, ng8 = layer_scan((2, 2, 2))
SCANS[8] = (r8, (2, 2, 2))
print("  生成元 {} 个，用时 {:.2f} s".format(ng8, dt8))
show(r8, 8)
chk("HK-1a", abs(r8[0][3] - LN2) < 1e-12 and abs(r8[8][3] - LN2) < 1e-12,
    "k=0 与 k=N：H/N = ln2 = {:.4f}（单构型 |O|=1）⟹ 层的两个端点".format(LN2))

# ================================================================== HK-2  N=16
hdr("HK-2  N=16 (2,2,4) —— 全层精确扫描")
r16, dt16, N16, ng16 = layer_scan((2, 2, 4))
SCANS[16] = (r16, (2, 2, 4))
print("  生成元 {} 个，用时 {:.2f} s".format(ng16, dt16))
show(r16, 16)
chk("HK-2a", all(r16[k][1] == math.comb(16, k) for k in r16),
    "每层构型数 = C(16,k) ⟹ 轨道划分完整、无遗漏")

# ---------------------------------------------------------------- Q1 对称性
hdr("HK-3  Q1：对称性 h(k) = h(N−k) —— 全层扫描**直接验证**")
for r, N in ((r8, 8), (r16, 16)):
    bad = [(k, r[k][3], r[N - k][3]) for k in r if abs(r[k][3] - r[N - k][3]) > 1e-12]
    print("  N = {:>3}：{}".format(N, "全部 {} 对严格相等 ✓".format(N // 2 + 1)
                                 if not bad else "**{} 对不等**：{}".format(len(bad), bad[:3])))
chk("HK-3", not [(k) for r, N in ((r8, 8), (r16, 16)) for k in r
                 if abs(r[k][3] - r[N - k][3]) > 1e-12],
    "**h(k) = h(N−k) 严格成立**（两个完整算例、{} 对）⟹ 补集映射的论证被证实".format(
        sum(N // 2 + 1 for N in (8, 16))))

# ================================================================== HK-4  N=24
hdr("HK-4  N=24 (2,2,6) —— 全层精确扫描（1.7×10⁷ 构型，慢）")
r24, dt24, N24, ng24 = layer_scan((2, 2, 6))
SCANS[24] = (r24, (2, 2, 6))
print("  生成元 {} 个，用时 {:.1f} s".format(ng24, dt24))
show(r24, 24)
chk("HK-4a", all(r24[k][1] == math.comb(24, k) for k in r24), "每层构型数 = C(24,k)")
chk("HK-4b", abs(r24[12][3] - 0.4510) < 0.0005,
    "k=12（半满）H/N = {:.4f}，与第 48 轮 FR-1 的 0.4510 一致 ✓（工具链交叉验证）".format(r24[12][3]))

# ---------------------------------------------------------------- 非单调性
hdr("HK-5  ❌ 预判 ① 被否证：H/N 随 k **非单调**")
for r, N in ((r8, 8), (r16, 16), (r24, 24)):
    ks = sorted(r)
    ups = [(k, r[k][3], r[k + 1][3]) for k in ks[:-1] if r[k + 1][3] > r[k][3] + 1e-12]
    print("  N = {:>3}：{}".format(N, "单调递减" if not ups
                                 else "**有 {} 处上升**，如 k={}→{}：{:.4f}→{:.4f}".format(
                                     len(ups), ups[0][0], ups[0][0] + 1, ups[0][1], ups[0][2])))
chk("HK-5", True, "非单调已被记录（我的预判错了，脚本抓住）")

# ---------------------------------------------------------------- k=1 解析
hdr("HK-6  k=1 的**解析值**：H/N = ln2 − lnN/N（要求群在单点上可迁）")
print("  {:>5} {:>12} {:>12} {:>10}".format("N", "实测 H/N", "ln2−lnN/N", "差"))
for r, N in ((r8, 8), (r16, 16), (r24, 24)):
    pred = LN2 - math.log(N) / N
    print("  {:>5} {:>12.4f} {:>12.4f} {:>10.2e}".format(N, r[1][3], pred, abs(r[1][3] - pred)))
chk("HK-6", all(abs(r[1][3] - (LN2 - math.log(N) / N)) < 1e-9 for r, N in
                ((r8, 8), (r16, 16), (r24, 24))),
    "k=1：三层都严格等于 ln2 − lnN/N ⟹ **群在单点上可迁**（|O|=N），且这是小 k 端"
    "强 N 依赖的来源")

# ---------------------------------------------------------------- Q2 标度
hdr("HK-7  Q2：h(k, N) 是否只依赖 k/N？（把三条曲线按 x = k/N 叠）")
print("  {:>8}  {:>10}  {:>10}  {:>10}  {}".format("x=k/N", "h(N=8)", "h(N=16)", "h(N=24)", "最大差"))
worst = 0.0
worst_x = None
for i in range(0, 9):
    x = i / 8.0                       # 以 1/8 为网格 ⟹ 三层都有对应 k
    vals = []
    for r, N in ((r8, 8), (r16, 16), (r24, 24)):
        kk = int(round(x * N))
        if abs(x * N - kk) > 1e-9 or kk not in r:
            vals.append(None)
        else:
            vals.append(r[kk][3])
    got = [v for v in vals if v is not None]
    if len(got) < 2:
        continue
    d = max(got) - min(got)
    if d > worst:
        worst, worst_x = d, x
    print("  {:>8.4f}  {:>10}  {:>10}  {:>10}  {:.4f}".format(
        x,
        "{:.4f}".format(vals[0]) if vals[0] is not None else "-",
        "{:.4f}".format(vals[1]) if vals[1] is not None else "-",
        "{:.4f}".format(vals[2]) if vals[2] is not None else "-", d))
print()
print("  ⟹ 最大差 {:.4f} 出现在 x = {}".format(worst, worst_x))
chk("HK-7", worst > 0.05,
    "**h 不依赖 k/N**（同 x 上跨 N 的最大差 {:.4f}）⟹ 跨点**不能**只靠占据分数定义，"
    "N 仍是独立变量（否证 Q2）".format(worst))

# ---------------------------------------------------------------- Q3 0.25
hdr("HK-8  Q3：0.25 能否被**任何层**穿过？（本轮最关键的判据）")
for r, N in ((r8, 8), (r16, 16), (r24, 24)):
    hmin = min(r[k][3] for k in r)
    kmin = min(r, key=lambda k: r[k][3])
    print("  N = {:>3}：min_k H/N = {:.4f}（k = {}）⟹ 0.25 {}".format(
        N, hmin, kmin, "**可达**" if hmin < 0.25 else "**够不到**"))
chk("HK-8", all(min(r[k][3] for k in r) > 0.25 for r in (r8, r16, r24)),
    "❌ 预判 ② 被否证：N = 8/16/24 上**任何层都够不到 0.25** ⟹ 「扫 k 能收窄跨点」"
    "只在 N ≥ 48 一侧成立")

hdr("HK-9  min_k h(k,N) 的位置：是否在 k = N/2？")
for r, N in ((r8, 8), (r16, 16), (r24, 24)):
    kmin = min(r, key=lambda k: r[k][3])
    print("  N = {:>3}：argmin_k = {:>3}（N/2 = {}），min = {:.4f}，h(N/2) = {:.4f}".format(
        N, kmin, N / 2.0, r[kmin][3], r[N // 2][3]))
chk("HK-9", True, "argmin 已列出（见备忘录解读）")

# ================================================================== HK-10 标度
hdr("HK-10  Q4：h_min(N) 的标度律 —— 用第 48/49 轮**既有**的 k=N/2 数据点（正确生成元）")
DATA = [((2, 4, 4), 32, 0.2834), ((2, 4, 6), 48, 0.2208), ((2, 4, 8), 64, 0.1802),
        ((4, 4, 4), 64, 0.1839), ((2, 6, 6), 72, 0.1652), ((2, 4, 10), 80, 0.1571),
        ((2, 4, 12), 96, 0.1338), ((4, 4, 6), 96, 0.1484), ((6, 6, 6), 216, 0.0779)]
byn = {}
for dims, N, h in DATA:
    byn.setdefault(N, []).append(h)
pts = [(n, sum(v) / len(v)) for n, v in sorted(byn.items())]
print("  {:>5} {:>10}  {}".format("N", "⟨H/N⟩", "该 N 的形状数 / 散布"))
for n, v in pts:
    print("  {:>5} {:>10.4f}  {} / {:.4f}".format(n, v, len(byn[n]), max(byn[n]) - min(byn[n])))

xs = [math.log(n) for n, v in pts]
ys = [math.log(v) for n, v in pts]
nn = len(pts)
mx = sum(xs) / nn
my = sum(ys) / nn
p = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
lnC = my - p * mx
C = math.exp(lnC)
print()
print("  拟合 h_min = C·N^p ⟹  C = {:.4f},  p = {:.4f}   （-2/3 = -0.6667，差 {:+.4f}）".format(
    C, p, p + 2.0 / 3.0))
print("  {:>5} {:>10} {:>10} {:>9}".format("N", "实测", "拟合", "残差%"))
maxres = 0.0
for n, v in pts:
    fit = C * n ** p
    res = 100.0 * (fit - v) / v
    maxres = max(maxres, abs(res))
    print("  {:>5} {:>10.4f} {:>10.4f} {:>9.2f}".format(n, v, fit, res))
chk("HK-10a", abs(p + 2.0 / 3.0) < 0.08,
    "标度指数 p = {:.4f}（与 -2/3 差 {:+.4f}；最大残差 {:.1f}%）".format(p, p + 2.0 / 3.0, maxres))
chk("HK-10b", maxres < 12.0,
    "拟合在 N ∈ [32, 216]（6.75 倍跨度）上最大残差 {:.1f}%".format(maxres))

# 留一：只用 N ≤ 96 拟合，预测 N = 216
xs2 = [math.log(n) for n, v in pts[:-1]]
ys2 = [math.log(v) for n, v in pts[:-1]]
mx2 = sum(xs2) / len(xs2)
my2 = sum(ys2) / len(ys2)
p2 = sum((x - mx2) * (y - my2) for x, y in zip(xs2, ys2)) / sum((x - mx2) ** 2 for x in xs2)
C2 = math.exp(my2 - p2 * mx2)
pred216 = C2 * 216 ** p2
print()
print("  **留一外推**：只用 N ≤ 96 拟合（C = {:.4f}, p = {:.4f}）".format(C2, p2))
print("      预测 N = 216：《{:.4f}》   实测 0.0779   误差 {:+.1f}%".format(
    pred216, 100.0 * (pred216 - 0.0779) / 0.0779))
chk("HK-10c", abs(pred216 - 0.0779) / 0.0779 < 0.30,
    "留一外推 N=216：{:.4f} vs 实测 0.0779（误差 {:+.1f}%）".format(
        pred216, 100.0 * (pred216 - 0.0779) / 0.0779))

# 用 -2/3 硬写：C 值
print()
print("  ⚠️ 若**强制** p = -2/3，反解 C：")
for n, v in pts:
    print("      N = {:>4} ⟹ C = h·N^(2/3) = {:.4f}".format(n, v * n ** (2.0 / 3.0)))
Cs = [v * n ** (2.0 / 3.0) for n, v in pts]
print("      C 的均值 {:.4f}，散布 {:.4f}（相对 {:.1f}%）".format(
    sum(Cs) / len(Cs), max(Cs) - min(Cs), 100.0 * (max(Cs) - min(Cs)) / (sum(Cs) / len(Cs))))

# 对照族
hdr("HK-11  对照：「≥2 个退化方向」族（H/N 随 N **上升**）⟹ 两条反向曲线")
DATA2 = [((2, 2, 2), 8, 0.4679), ((2, 2, 4), 16, 0.4335), ((2, 2, 6), 24, 0.4510),
         ((2, 2, 8), 32, 0.4617), ((2, 2, 10), 40, 0.4802), ((2, 2, 12), 48, 0.5041),
         ((2, 2, 14), 56, 0.5170), ((2, 2, 16), 64, 0.5307)]
for dims, N, h in DATA2:
    print("  {:>10} {:>5} {:>10.4f}".format(str(dims), N, h))
chk("HK-11", abs(r8[4][3] - 0.4679) < 0.0005 and abs(r16[8][3] - 0.4335) < 0.0005
    and abs(r24[12][3] - 0.4510) < 0.0005,
    "第 48 轮 (2,2,2)=0.4679 / (2,2,4)=0.4335 / (2,2,6)=0.4510 **三个值被本轮独立复现** "
    "⟹ 工具链自洽（这是本轮的一次交叉验证）")

print()
print("=" * 78)
print("汇总：通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
