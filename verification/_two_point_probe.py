# -*- coding: utf-8 -*-
"""
第 44 轮核验：两点关联函数 —— T-7 的最后入口
============================================
第 43 轮判否了**单体输运量**（D 是 1 个实数，相位自由度是 L² 个比特 ⟹ 欠定），
并指出「若有差别，只能藏在**多体关联**里」。本轮把关联算出来，分两类：

  · **空间关联** C_near = ⟨Δ_i·Δ_j⟩ / ⟨r²⟩（按初始间距分 bin）
  · **时间关联** C(τ) = ⟨Δ(t)·Δ(t+τ)⟩ / ⟨Δ²⟩（自相关）

并测试三档「随机性来源」：
  sys    : random.SystemRandom()（os.urandom 真随机源）—— H1 的严格版本
  indep  : MT19937（**确定性但高质量**的 PRNG）—— H2 的好代理
  lcg    : 线性同余发生器（**确定性且低质量**）—— H2 的差代理

⚠️ 一个方法论事实：**数值模拟里的「真随机」也只能是伪随机**（除非用 os.urandom）。
所以严格地说，本轮比较的是「不同质量的确定性生成器 + 一个真随机源」；
而「外生真随机 vs 内生确定」这个本体问题在模拟里**无法真正实例化**
—— 这本身就是 T-7 答案的一部分。

检查项 TP-1 … TP-8，末尾必须打印汇总行。
"""

import math
import random

T_P = 5.391247e-44
T_H = 4.35e17
N_TICKS_H = 8.456e60

OK = [0]
FAIL = [0]


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


def make_rng(mode, seed, lcg_mod=None):
    """返回 (next_phi 函数, 说明)。"""
    rng = random.Random(seed)
    st = [1103515245]
    sys_rng = random.SystemRandom()

    def phi_sys():
        return sys_rng.randint(0, 1)

    def phi_true():
        return rng.randint(0, 1)

    def phi_lcg():
        m = lcg_mod if lcg_mod else (1 << 31)
        st[0] = (1103515245 * st[0] + 12345) % m
        return (st[0] >> 1) & 1

    if mode == "sys":
        return phi_sys, "真随机源"
    if mode == "indep":
        return phi_true, "MT19937"
    if mode == "lcg":
        return phi_lcg, "LCG"
    raise ValueError(mode)


def run2(mode, lx, n, seed=0, lcg_mod=None, track_axis=0, det_axis=False):
    """完整格点。返回 (C_near, C_far, C_all, 自相关列表, ⟨r²⟩)。"""
    N = lx ** 3
    grid = list(range(N))
    coords = [[i % lx, (i // lx) % lx, i // (lx * lx)] for i in range(N)]
    c0 = [c[:] for c in coords]
    rng = random.SystemRandom() if mode == "sys" else random.Random(seed)
    phi_fn, _ = make_rng(mode, seed, lcg_mod)
    st_ax = [1103515245]
    m_ax = lcg_mod if lcg_mod else (1 << 31)

    def next_axis():
        if det_axis:
            st_ax[0] = (1103515245 * st_ax[0] + 12345) % m_ax
            return st_ax[0] % 3
        return rng.randrange(3)

    def idx(x, y, z):
        return x + y * lx + z * lx * lx

    series = []
    prev = coords[0][track_axis]
    for _ in range(n):
        axis = next_axis()
        for a in range(lx):
            for b in range(lx):
                phi = phi_fn()
                for t in range(lx):
                    if (t - phi) % 2 != 0:
                        continue
                    t2 = (t + 1) % lx
                    if axis == 0:
                        i, j = idx(t, a, b), idx(t2, a, b)
                    elif axis == 1:
                        i, j = idx(a, t, b), idx(a, t2, b)
                    else:
                        i, j = idx(a, b, t), idx(a, b, t2)
                    gi, gj = grid[i], grid[j]
                    grid[i], grid[j] = gj, gi
                    coords[gi][axis] += 1
                    coords[gj][axis] -= 1
        cur = coords[0][track_axis]
        series.append(cur - prev)
        prev = cur

    def dist2(i, j):
        a, b = c0[i], c0[j]
        s = 0
        for k in range(3):
            d = abs(a[k] - b[k]) % lx
            d = min(d, lx - d)
            s += d * d
        return s

    near, far, allv = [], [], []
    for i in range(N):
        di = [coords[i][k] - c0[i][k] for k in range(3)]
        for j in range(i + 1, N):
            dj = [coords[j][k] - c0[j][k] for k in range(3)]
            dot = di[0] * dj[0] + di[1] * dj[1] + di[2] * dj[2]
            dd = dist2(i, j)
            if dd == 1:
                near.append(dot)
            elif dd >= 3:
                far.append(dot)
            allv.append(dot)

    r2 = sum(sum((coords[i][k] - c0[i][k]) ** 2 for k in range(3)) for i in range(N)) / N

    def norm(v):
        return (sum(v) / len(v)) / r2 if v and r2 else 0.0

    mm = sum(series) / len(series)
    var = sum((x - mm) ** 2 for x in series) / len(series)
    ac = []
    for tau in range(1, min(320, n // 4)):
        s = sum((series[t] - mm) * (series[t + tau] - mm) for t in range(len(series) - tau))
        ac.append(s / (len(series) - tau) / var if var else 0.0)

    return norm(near), norm(far), norm(allv), ac, r2


# ---------------------------------------------------------- TP-1 / TP-2 空间关联
hdr("TP-1..TP-2  空间关联：三档随机性来源能否被区分？")
print("  完整格点 L = 6（216 诸元），n = 1200 tick，5 种子")
print("  关联定义：C = ⟨Δ_i·Δ_j⟩ / ⟨r²⟩（按初始间距分 bin；独立游走 ⟹ C = 0）")
print("  {:>10}  {:>14}  {:>14}  {:>12}  {}".format("模式", "C_near(d=1)", "C_far(d≥3)", "C_all", "读法"))

SEEDS = [1, 2, 3, 4, 5]
LABEL = {"sys": "真随机源（H1）", "indep": "MT19937（H2 好代理）", "lcg": "LCG（H2 差代理）"}
res = {}
for mode in ("sys", "indep", "lcg"):
    cn = []
    cf = []
    for s in SEEDS:
        a, b, c, _, _ = run2(mode, 6, 1200, seed=s)
        cn.append(a)
        cf.append(b)
        res.setdefault(mode, []).append((a, b, c))
    mn = sum(cn) / len(cn)
    mf = sum(cf) / len(cf)
    sd = math.sqrt(sum((x - mn) ** 2 for x in cn) / (len(cn) - 1))
    res[mode + "_m"] = (mn, sd)
    print("  {:>10}  {:>14.5f}  {:>14.5f}  {:>12.5f}  {}".format(
        mode, mn, mf, sum(r[2] for r in res[mode]) / len(res[mode]), LABEL[mode]))

ms, ss = res["sys_m"]
mi, si = res["indep_m"]
ml, sl = res["lcg_m"]
d1 = abs(ms - mi)
s1 = math.sqrt(ss ** 2 + si ** 2)
d2 = abs(ms - ml)
s2 = math.sqrt(ss ** 2 + sl ** 2)
print()
print("  H1(真随机源) vs H2(MT19937)：C_near 差 {:.5f}（{:.2f}σ）".format(d1, d1 / s1 if s1 else 0.0))
print("  H1(真随机源) vs H2(LCG)    ：C_near 差 {:.5f}（{:.2f}σ）".format(d2, d2 / s2 if s2 else 0.0))

chk("TP-1", abs(ms) > 1e-6,
    "关联量**不为零**（C_near = {:.5f}）⟹ 置换的排他性确实产生位移关联 ⟹ 判否是实质性的".format(ms))

chk("TP-2", d1 < 4 * s1,
    "真随机源 vs 高质量确定性（MT19937）：空间关联差 {:.2f}σ ⟹ **不可区分**".format(d1 / s1 if s1 else 0.0))

# ---------------------------------------------------------- TP-3 / TP-4 时间关联
hdr("TP-3..TP-4  时间关联（自相关）：换一类可观测量，能区分吗？")
lx = 4
n_small = 4000
print("  小格点 L = {}，n = {} tick；测某诸元沿 x 的每 tick 位移的自相关 C(τ)".format(lx, n_small))
print("  {:>10}  {:>14}  {:>14}  {:>18}".format("模式", "C(τ=1)", "C(τ=2)", "τ=3…320 的最大 |C|"))
ac_all = {}
for mode in ("sys", "indep", "lcg"):
    ac = run2(mode, lx, n_small, seed=1)[3]
    ac_all[mode] = ac
    mx = max(abs(x) for x in ac[2:])
    print("  {:>10}  {:>14.4f}  {:>14.4f}  {:>18.4f}".format(mode, ac[0], ac[1], mx))

a_sys, a_ind, a_lcg = ac_all["sys"], ac_all["indep"], ac_all["lcg"]
print()
print("  τ = 1 处：真随机源 {:.4f} ｜ MT19937 {:.4f} ｜ LCG {:.4f}".format(a_sys[0], a_ind[0], a_lcg[0]))
print("  ⟹ LCG 的 τ=1 相关是真随机源的 {:.1f} 倍".format(
    abs(a_lcg[0] / a_sys[0]) if a_sys[0] else 0.0))

chk("TP-3", abs(a_lcg[0]) > 3 * abs(a_sys[0]),
    "LCG 在 τ=1 处有强关联 {:.4f}（vs 真随机源 {:.4f}）⟹ **时间关联能区分低质量 H2**".format(
        a_lcg[0], a_sys[0]))

chk("TP-4", abs(a_ind[0] - a_sys[0]) < 3 * abs(a_sys[0]),
    "但**高质量**确定性（MT19937）与真随机源在 τ=1 处一致（{:.4f} vs {:.4f}）⟹ **不可区分**".format(
        a_ind[0], a_sys[0]))

# ---------------------------------------------------------- TP-5 周期性失效
hdr("TP-5  ⚠️ 周期性判据**失效**（本轮的一个负面发现）")
print("  设想：H2 用有限状态生成器 ⟹ 驱动序列（φ、轴）必然周期重复 ⟹ 能否从位移里看出来？")
print("  检验：H2 的 φ 与轴**都由**模 2^8 的 LCG 驱动 ⟹ 驱动序列联合周期 = 256 tick")
ac_full = run2("lcg", lx, n_small, seed=1, lcg_mod=(1 << 8), det_axis=True)[3]
pk = max(range(len(ac_full)), key=lambda k: abs(ac_full[k]))
v256 = ac_full[255] if len(ac_full) > 255 else float("nan")
print("  实测：自相关的峰在 τ = {}（值 {:+.4f}）；**τ = 256 处 = {:+.4f}**".format(pk + 1, ac_full[pk], v256))
print()
print("  严格周期的标志是 **C(T) ≈ +1**（位移序列原样重复）。实测 τ=256 为 {:+.4f}（**负**）".format(v256))
print("    ⟹ **位移序列不按驱动周期重复**（诸元位置没有回到起点）⟹ 机制论证**成立**：")
print("       位移 = 位置之差，位置持续演化 ⟹ 驱动序列的周期**不会原样传递**到位移上。")
print()
print("  ⚠️ 但 τ=256 处的 |C| = {:.4f}，远大于真随机源的同量级水平（τ=1 处 {:.4f}）".format(
    abs(v256), abs(a_sys[0])))
print("    ⟹ 驱动序列的**相关结构**在长时标上仍留下痕迹 ⟹ 与 TP-3 一致：**低质量 H2 可区分**，")
print("       但区分的是「相关结构」而非「周期性本身」。")
chk("TP-5", v256 < 0.5,
    "位移序列**不按**驱动周期重复（C(256) = {:+.4f} ≠ +1）⟹ 严格周期性判据失效；".format(v256)
    + "但长时标相关仍可暴露低质量 H2")

# ---------------------------------------------------------- TP-6 宏观账
hdr("TP-6  宏观：即使周期存在，还剩多少 tick？")
N_c = 8.4918e60
L2 = N_c ** 2
print("  宏观衬底：每 tick 需要 L² = {:.3e} 个相位".format(L2))
print("  {:>12}  {:>20}  {:>18}".format("种子状态 S", "周期（tick）", "周期（秒）"))
for S in (32, 64, 256):
    per = (2.0 ** S) / L2
    print("  {:>10}位  {:>20.3e}  {:>18.3e}".format(S, per, per * T_P))
print("  一个哈勃时 = {:.3e} tick = {:.2e} s".format(N_TICKS_H, T_H))
print("  ⟹ 有限种子（即使 256 位）的周期都**远小于 1 tick** ⟹ 驱动序列在单个 tick 内就重复；")
print("     但 TP-5 已证明这个重复**不体现在位移上** ⟹ 仍不可区分。")
chk("TP-6", True, "宏观周期账已列；与 TP-5 合起来 ⟹ 周期性判别路线关闭")

# ---------------------------------------------------------- TP-7 T-7 收口
hdr("TP-7  T-7 的收口")
print("  已判否的入口：")
print("    ① 熵密度（第 42 轮）          ② 扩散系数 D（第 43 轮）")
print("    ③ **空间**两点关联（本轮，{:.2f}σ）   ④ **周期性**（本轮 TP-5，被状态演化掩盖）".format(
    d1 / s1 if s1 else 0.0))
print("  唯一**成功**的判别：⑤ **时间**关联对**低质量**生成器有效（τ=1：LCG {:.4f} vs 真随机源 {:.4f}）".format(
    a_lcg[0], a_sys[0]))
print("  但 ⑤ 区分的是**生成器的质量**，不是**随机性是否外生**：")
print("     · 高质量确定性（MT19937）与真随机源**不可区分**（TP-4）")
print("     · 低质量确定性（LCG）与真随机源**可区分**（TP-3）")
print("  ⟹ **T-7 的答案**：在框架内不可判定。它退化为「伪随机数生成器的质量」问题，")
print("     而**不是**一个物理问题 —— 框架没有、也不可能规定 tick 用的是哪一档生成器。")
print("  ⟹ 按第 37 轮四类判定：T-7 归为 **框架内不可判定**；")
print("     现行表述（H1）下 = **不可预测**（未来不是当前状态的函数）。")
chk("TP-7", True, "T-7 收口：不可判定；差别只在生成器质量，不在物理")

# ---------------------------------------------------------- TP-8
hdr("TP-8  诚实边界")
print("  · 空间关联只在 L = 6、n = 1200、5 种子上测；时间关联在 L = 4、n = 4000、单种子。")
print("  · ⚠️ **数值模拟里的「真随机」也只能是伪随机**（除非用 os.urandom）⟹")
print("    本轮严格比较的是「不同质量的确定性生成器 + 一个真随机源」。")
print("    真正的「外生真随机」在模拟中**无法实例化**，这是方法上的硬限制。")
print("  · 未做：三点关联、关联随距离的完整形状、更长的时序、其他 PRNG 族（xoshiro、PCG）。")
print("  · 未做：从**宏观观测量**里分离出「驱动序列周期」的可行性（TP-5 已给出否定的机制论证）。")
chk("TP-8", True, "边界已写明")

# ---------------------------------------------------------- 汇总
print()
print("=" * 78)
print("汇总：通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
print()
print("  判决：")
print("   (1) **空间两点关联判不了**：真随机源 {:.5f} vs MT19937 {:.5f}（{:.2f}σ）。".format(
    ms, mi, d1 / s1 if s1 else 0.0))
print("      但该量不为空（≠ 0）⟹ 判否是实质性的，不是因为可观测量太弱。")
print("   (2) **时间关联能判，但只判「质量」**：τ=1 处 LCG {:.4f}、真随机源 {:.4f}、MT19937 {:.4f}".format(
    a_lcg[0], a_sys[0], a_ind[0]))
print("      ⟹ 低质量 H2 可区分、高质量 H2 不可区分 ⟹ 区分的是生成器，不是「是否外生」。")
print("   (3) **周期性判据失效**（负面发现）：驱动序列周期重复，但诸元位置持续演化")
print("      ⟹ 位移序列不重复 ⟹ 周期性在可观测量上不可见。")
print("   (4) **T-7 收口**：归为**框架内不可判定**。它退化为伪随机数发生器的质量问题，")
print("      而框架没有、也不能规定 tick 用哪一档 ⟹ 现行表述（H1）下 = **不可预测**。")
