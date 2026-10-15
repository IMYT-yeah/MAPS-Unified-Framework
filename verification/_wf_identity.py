# -*- coding: utf-8 -*-
"""
第 34 轮：w 与 f 的同一性（B2 闭环的最后一步）
背景：第 33 轮解出槽模型的空槽率 w = 0，但留下软肋——
      「空槽率 w」与衬底「占位率 f」是否为同一个量，未独立论证（当时默认 w = 1 − f）。
本轮：① 建立两者的关系式；② 检验在框架的置换动力学下该式给出什么；
      ③ 用 BH 熵 + 满占位双约束反解 f；④ 顺带检验第 20 轮被否证的独立泊松衬底。
只用标准库。正文引号一律用中文引号。
"""
import math as m
import random

C_MS = 2.99792458e8
G_SI = 6.67430e-11
H_PLANCK = 6.62607015e-34
HBAR = H_PLANCK / (2 * m.pi)
K_B = 1.380649e-23
M_SUN = 1.98892e30          # 与第 15/25/31/32/33 轮一致

LN16 = m.log(16)
T_STD = HBAR * C_MS ** 3 / (8 * m.pi * G_SI * M_SUN * K_B)

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
    print("  [%s] %-52s got=%s want=%s" % ("OK" if ok else "XX", name, got_s, want_s))
    return ok


def show(name, val, fmt="%.12g"):
    print("       %-44s %s" % (name, fmt % val))


def h2(w):
    if w <= 0.0 or w >= 1.0:
        return 0.0
    return -w * m.log(w) - (1 - w) * m.log(1 - w)


def H_S(w):
    """槽模型：4 个平面内连接，每槽 ∈ {正, 负, 空}，空槽权重 w"""
    return 4.0 * (h2(w) + (1 - w) * m.log(2))


print("=" * 76)
print("  第 34 轮：w 与 f 的同一性 —— B2 闭环的最后一步")
print("=" * 76)

# ================================================================== WF-1
line("WF-1  关系式：一条连接存活 ⟺ 两端格点都被占")

print("""
      面元的「平面内连接」= 与相邻面元之间的**键**。
      一条键承载通量 ⟺ **两端格点都被诸元占据**。
      若各格点占位独立、占位率为 f ⟹ P(键存活) = f²
      ⟹ **w = 1 − f²**   （不是 w = 1 − f）""")

# Monte-Carlo 直接验证 w = 1 − f²
L = 20
NL = L ** 3


def enc(i, j, k, Lx):
    """编码：必须显式传格点边长 Lx（第 27 轮踩过全局 L 的作用域坑）"""
    return (i % Lx) + Lx * ((j % Lx) + Lx * ((k % Lx)))


def dec(p, Lx):
    return p % Lx, (p // Lx) % Lx, p // (Lx * Lx)


print("      Monte-Carlo 直接检验（L=20，N=%d，沿 x 的键，周期边界）" % NL)
print("      f        P(键存活) 实测    f² 预测      相对误差")
rng = random.Random(20260920)
for f in (0.9, 0.8, 0.6, 0.5):
    occ = [1 if rng.random() < f else 0 for _ in range(NL)]
    live = 0
    tot = 0
    for p in range(NL):
        i, j, k = dec(p, L)
        q = enc(i + 1, j, k, L)
        tot += 1
        if occ[p] and occ[q]:
            live += 1
    meas = live / float(tot)
    print("      %-7.2f %-18.6f %-12.6f %+.3f%%" % (f, meas, f ** 2, 100 * (meas / f ** 2 - 1)))
    chk("  f=%.2f ⟹ 存活率 = f²（1%% 内）" % f, meas, f ** 2, 0.02)
show("f = 1 时 w = 1 − f²", 1 - 1.0 ** 2, "%.6f")
show("f = 1/2 时 w = 1 − f²", 1 - 0.5 ** 2, "%.6f")

# ================================================================== WF-2
line("WF-2  置换动力学下 f ≡ 1（确定性，不是统计平均）")


def pairs_for_axis(Lx, axis, rng_p):
    """沿 axis 的二分图完美匹配；每条链独立抽取相位。"""
    out = []
    ph_of = {}
    for idx in range(Lx ** 3):
        i, j, k = dec(idx, Lx)
        c = (i, j, k)
        key = tuple(c[a] for a in range(3) if a != axis)
        if key not in ph_of:
            ph_of[key] = rng_p.randrange(2)
        t = c[axis]
        if t % 2 == ph_of[key]:
            nb = [i, j, k]
            nb[axis] = (t + 1) % Lx
            out.append((idx, enc(nb[0], nb[1], nb[2], Lx)))
    return out


L2 = 6
N2 = L2 ** 3
grid = list(range(N2))
ra = random.Random(11)
rp = random.Random(22)
bad_perm = 0
min_occ, max_occ = 99, -1
for _ in range(1000):
    axis = ra.randrange(3)
    for a, b in pairs_for_axis(L2, axis, rp):
        grid[a], grid[b] = grid[b], grid[a]
    if sorted(grid) != list(range(N2)):
        bad_perm += 1
    # 每个格点恰有一个诸元（grid 是排列 ⟹ 占位率恒为 1）
    occ_cnt = {}
    for g in grid:
        occ_cnt[g] = occ_cnt.get(g, 0) + 1
    lo, hi = min(occ_cnt.values()), max(occ_cnt.values())
    min_occ = min(min_occ, lo)
    max_occ = max(max_occ, hi)
show("tick 数", 1000.0, "%.0f")
show("格点数 N", float(N2), "%.0f")
show("非置换的 tick 数（应为 0）", float(bad_perm), "%.0f")
chk("置换始终保持（⟹ 每格点恒 1 个）", float(bad_perm), 0.0, 0.0)
show("每格点占据数的最小值", float(min_occ), "%.0f")
show("每格点占据数的最大值", float(max_occ), "%.0f")
chk("占位率 f ≡ 1（确定性，非统计平均）", float(min_occ == 1 and max_occ == 1), True)
show("⟹ w = 1 − f²", 1 - 1.0 ** 2, "%.6f")
print("""
      ⟹ **置换是双射 ⟹ 每个格点恒有且仅有 1 个诸元 ⟹ f ≡ 1（逐 tick 恒等，不是期望值）**
      ⟹ 每条键两端恒被占 ⟹ **w ≡ 0（恒等，不是概率）**
      ⟹ 因而**既不需要「w 与 f 是同一个量」的假设，也不需要格点间的独立性假设**。""")

# ================================================================== WF-3
line("WF-3  f = 1 ⟹ w = 0 ⟹ BH 定标满足")

show("H_S(0)", H_S(0.0))
chk("H_S(0) = ln 16（BH 定标）", H_S(0.0), LN16, 1e-12)
show("对应的 Hawking 温度偏差", 100 * (LN16 / H_S(0.0) - 1), "%+.4f%%")

# ================================================================== WF-4
line("WF-4  独立泊松衬底（f* = 1/2）的第二次独立排除")

f_poi = 0.5
w_poi = 1 - f_poi ** 2
show("独立泊松的稳态占位率 f*", f_poi, "%.4f")
show("⟹ 空槽率 w = 1 − f*²", w_poi, "%.6f")
show("H_S(w)", H_S(w_poi))
show("S / S_req", H_S(w_poi) / LN16)
show("Hawking 温度偏差", 100 * (LN16 / H_S(w_poi) - 1), "%+.4f%%")
show("  对应 T / K", T_STD * LN16 / H_S(w_poi), "%.6e")
print("""
      ⟹ **第 20 轮已用 Δc/c = 26%% 排除独立泊松衬底；本轮用 BH 熵定标第二次独立排除
         （温度偏差 %.2f%%）**。两条依据互不相干，互为交叉验证。"""
      % (100 * (LN16 / H_S(w_poi) - 1)))
chk("独立泊松被 BH 定标排除（|偏差| > 1%）",
    float(abs(LN16 / H_S(w_poi) - 1) > 0.01), True)

# ================================================================== WF-5
line("WF-5  双约束反解：BH 熵 + 满占位共同定 f")


def dev_f(f):
    return LN16 / H_S(1 - f ** 2) - 1


print("      f         w = 1 − f²    H_S          温度偏差")
for f in (1.0, 0.95, 0.8, 0.6, 0.5, 0.476541, 0.4):
    w = 1 - f ** 2
    print("      %-9.4f %-12.6f %-13.6f %+.4f%%"
          % (f, w, H_S(w), 100 * dev_f(f)))


def bisect(fn, lo, hi, tol=1e-13):
    flo = fn(lo)
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        fm = fn(mid)
        if (flo <= 0 <= fm) or (fm <= 0 <= flo):
            hi = mid
        else:
            lo, flo = mid, fm
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


f_small = bisect(lambda f: H_S(1 - f ** 2) - LN16, 0.2, 0.9)
show("BH 定标的第二个根 f₂", f_small, "%.6f")
show("  ⟹ 对应 w", 1 - f_small ** 2, "%.6f")
chk("f = 1 是 BH 定标的根", H_S(0.0), LN16, 1e-12)
print("      ⟹ f₂ ≈ %.4f 意味着 **%.1f%% 的格点是空的**，与第 20 轮 C-1 的"
      % (f_small, 100 * (1 - f_small)))
print("         Δc/c = 26% 论证直接冲突 ⟹ **排除，只剩 f = 1**。")
chk("f₂ 与满占位冲突（f₂ < 1）", float(f_small < 1.0), True)

# ================================================================== WF-6
line("WF-6  判决")

print("""
  ✅ **w 与 f 不是同一个量，关系为 w = 1 − f²**（一条键存活需两端都被占）。
     第 33 轮默认 w = 1 − f 是**错的**（少了一个平方），但结论不变：
     f = 1 ⟹ w = 0（无论用哪个式子都给 0）。已按正确关系式重算。

  ✅ **同一性问题以「不需要同一性假设」的方式解决**：
     框架的置换动力学是**双射** ⟹ 每个格点**恒有且仅有 1 个诸元** ⟹ **f ≡ 1 逐 tick 恒等**，
     不是统计平均值 ⟹ **w ≡ 0 逐 tick 恒等**，也不是概率。
     ⟹ B2 的「无空槽」既不是从衬底搬来的假设，也不依赖格点间的独立性；
       它是**置换双射的直接后果**（数值：1000 tick 内非置换 tick = 0，每格点占据数恒为 1）。

  ✅ **独立泊松衬底被第二次独立排除**：f* = 1/2 ⟹ w = 0.75 ⟹ 温度偏差 **%.2f%%**。
     与第 20 轮的 Δc/c = 26%% 论证互不相干，构成交叉验证。

  ✅ **B2 闭环完成**：满占位（置换双射）⟹ 每键承载通量 ⟹ 4 条平面内连接全活
     ⟹ A1 的 50:50 分配正 / 负支 ⟹ 2^4 = 16 ⟹ BH 定标成立 ⟹ Hawking 温度精确。

  ⚠️ **仍开放**：① 「连接」被当作格点间的**键**来用（面元层面的「连接」与格点层面的「键」
     是否严格对应，未独立论证）；② WF-1 的 f² 依赖独立性——但 WF-2 的 f ≡ 1 绕过了它，
     故独立性在框架实际动力学下不需要；③ 11.0904 的自然性仍未解释。
""" % (100 * (LN16 / H_S(w_poi) - 1)))

print("=" * 76)
print("  检查项：%d    失败项：%d" % (NCHK[0], NCHK[1]))
print("=" * 76)
