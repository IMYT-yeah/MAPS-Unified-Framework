# -*- coding: utf-8 -*-
"""
第 26 轮：tick 的更新规则 —— 「每 tick 几次对换」的口径裁定
UP-1 … UP-8
只用标准库。
"""
import math as m
import random

# ------------------------------------------------------------------ 常量
L_P = 1.616255e-35
T_P = 5.391247e-44
C_MS = 2.99792458e8
H0 = 67.4e3 / 3.0856775814913673e22          # s^-1 (67.4 km/s/Mpc)
R_C = C_MS / H0
T_H = 1.0 / H0
N_CELL = R_C / L_P                            # 哈勃球半径 / 普朗克长度
N_CELL3 = N_CELL ** 3                         # 哈勃球内的格点数

CHECKS = []
def chk(name, got, want, tol):
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    CHECKS.append((name, ok))
    print("  [%s] %-56s got=%.10g  want=%.10g"
          % ("OK" if ok else "XX", name, got, want))
    return ok

def show(name, val):
    print("        %-56s = %.10g" % (name, val))

def line(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)

# ================================================================== UP-1
line("UP-1  口径辩识：47 μm 反推出的步数是多少？")
print("""
  第 21 轮的 R_mix = l_P·sqrt(t/t_P) 隐含「每 t_P 移动一步」。
  反过来问：哪个口径下「每 t_P 一步」才成立？""")
show("t_H / t_P", T_H / T_P)
show("N_cell = R_c/l_P（哈勃球半径上的格点数）", N_CELL)
show("N_cell^3（哈勃球内的格点数）", N_CELL3)
R_47 = 4.70e-5
n_implied = (R_47 / L_P) ** 2
show("由 47 μm 反推的步数 n", n_implied)
chk("n 与 t_H/t_P 一致（⟹ 每 t_P 一步 ⟹ 每元每次）", n_implied, T_H / T_P, 0.02)

# ================================================================== UP-2
line("UP-2  三种归一化下的混合尺度（相差 N 倍）")
n_tick_total = T_H / T_P                      # 总 tick 数（每 tick 耗时 t_P）
show("总 tick 数 = t_H/t_P", n_tick_total)

R_par = L_P * m.sqrt(n_tick_total)                       # 每元每 tick 一步
R_half = L_P * m.sqrt(0.5 * n_tick_total)                # 每元每 2 tick 一步
R_ser = L_P * m.sqrt(2.0 * n_tick_total / N_CELL3)       # 每 tick 全局一对 ⟹ 每元参与率 2/N
show("并行（每格点每 tick 一次）：R_mix / m", R_par)
show("  同值 / μm", R_par * 1e6)
show("半速（每格点每 2 tick 一次）：R_mix / μm", R_half * 1e6)
show("串行（每 tick 全局一次）：R_mix / m", R_ser)
show("串行 R_mix / 普朗克长度", R_ser / L_P)
chk("并行口径复现 47 μm", R_par * 1e6, 47.0, 0.03)
print("""
  ⟹ **47 μm 是并行口径的数**（每格点每 tick 一次事件），不是串行。
     第 21 轮把它标成"串行（每 tick 一次对换）"，标反了：
     真正的串行值比它小 sqrt(N_cell^3/2) 倍 —— 小于普朗克长度 61 个量级，荒谬。""")

# ================================================================== UP-3
line("UP-3  判据一：A1 的事件率是「每个诸元 1/t_P」，不是「整个宇宙 1/t_P」")
nu_per = 1.0 / T_P
nu_ser = 2.0 * n_tick_total / N_CELL3 / T_H
show("A1 的 per-元 事件率 ν / s^-1", nu_per)
show("串行下每元的实际事件率 / s^-1", nu_ser)
show("两者之比（差多少个量级）", m.log10(nu_per / nu_ser))
chk("串行与 A1 差 N/2 倍", nu_per / nu_ser, N_CELL3 / 2.0, 0.05)
print("""
  ν ~ 1/t_P 是**单诸元**的速率（A1 原文：每个诸元每 t_P 湮灭-再生一次）。
  若每 tick 全局只发生一次对换，单个诸元平均要等 N_cell^3/2 拍才轮到一次
  ⟹ 事件率差 10^182 倍 ⟹ 串行被 A1 直接排除。""")

# ================================================================== UP-4
line("UP-4  判据二：A2 的泄漏率标定（ε0 也是 per-元 量）")
eps0 = 7.7e-20
show("ε0", eps0)
show("并行下每元每 t_P 一次泄漏机会 ⟹ 单次泄漏概率", eps0)
show("串行下单次泄漏概率需放大 / 倍", N_CELL3 / 2.0)
print("""
  A2 的 ε0 = 7.7e-20 是「一次事件里的泄漏份额」。
  若事件率被串行压低 10^182 倍，则要维持同样的宏观泄漏率，
  单次份额必须放大 10^182 倍 ⟹ ε0 >> 1，非物理。**串行被 A2 排除。**""")

# ================================================================== UP-5
line("UP-5  判据三：§4 的速度空间弛豫时标 ~4 t_P")
n_c = 4.0
show("§4 需要的碰撞数 n_c", n_c)
show("并行：4 t_P 内每元被交换次数", n_c * 1.0)
p_ser = 2.0 * n_c / N_CELL3
show("串行：4 t_P 内某元被交换的概率", p_ser)
show("  该概率的 log10", m.log10(p_ser))
chk("并行满足 n_c（4 次）", n_c * 1.0, n_c, 1e-12)
chk("串行概率远小于 1（被排除）", p_ser < 1e-100, True, 0.0)
print("""
  §4.2 的遍历性证据（麦克斯韦化 7.02%）要求每个粒子在 ~4 次对换内弛豫。
  并行：4 t_P 内恰好 4 次 ⟹ 满足。
  串行：4 t_P 内每元被交换的概率 10^-182 ⟹ 宇宙年龄内都热化不了 ⟹ **§4 被推翻**。
  ⟹ 保住 §4 就必须并行。三条独立论证同向。""")

# ================================================================== UP-6
line("UP-6  并行的实现：二分图完美匹配 + 轴随机 + 相位随机")

def decode(idx, L):
    i = idx % L
    j = (idx // L) % L
    k = idx // (L * L)
    return i, j, k

def encode(i, j, k, L):
    return (i % L) + L * ((j % L) + L * ((k % L)))

def pairs_for_axis(L, axis, phase, per_line=False, rng=None):
    """沿 axis 的 odd-even 完美匹配（周期边界）。
    per_line=False：全局统一相位（全系统同向）；
    per_line=True ：**每条线独立相位**（局域，无长程同步）—— 本轮采用。
    返回 (a, b)，a 是其线上 t%2==相位的一端，沿 +axis 移动。"""
    N = L ** 3
    out = []
    phase_of = {}
    for idx in range(N):
        i, j, k = decode(idx, L)
        coord = (i, j, k)
        if per_line:
            key = tuple(coord[a] for a in range(3) if a != axis)
            if key not in phase_of:
                phase_of[key] = rng.getrandbits(1)
            ph = phase_of[key]
        else:
            ph = phase
        t = coord[axis]
        if t % 2 == ph:
            nb = [i, j, k]
            nb[axis] = (t + 1) % L
            out.append((idx, encode(nb[0], nb[1], nb[2], L)))
    return out

L = 10
N = L ** 3
ok_cov = True
for axis in range(3):
    for per_line in (False, True):
        rng_c = random.Random(11)
        pr = pairs_for_axis(L, axis, 0, per_line=per_line, rng=rng_c)
        cov = {}
        for a, b in pr:
            cov[a] = cov.get(a, 0) + 1
            cov[b] = cov.get(b, 0) + 1
        if len(pr) != N // 2 or len(cov) != N or max(cov.values()) != 1:
            ok_cov = False
show("配对总数（每种模式）= N/2", float(N // 2))
chk("完美匹配：每个格点恰好出现一次", ok_cov, True, 0.0)
print("""
  ⟹ 两种相位模式都是完美匹配。本轮采用**每线独立相位**：
     全局统一相位 = 一个 tick 内全系统同侧，把衬底绑成刚性块（非局域）；
     每条线独立相位才符合"手递手"的局域图像，也无长程同步。""")

def run(n_tick, L, ra, rp, fix_axis=None, fix_phase_all=None, mode="per_line"):
    """ra: 选轴 RNG；rp: 相位 RNG。
    mode="per_line"        ：每线独立相位（本轮采用）
    mode="global_resample" ：每 tick 全局重抽一个相位（对照：会各向异性）"""
    N = L ** 3
    grid = list(range(N))
    cum = [[0, 0, 0] for _ in range(N)]
    vacuum = 0
    perm_bad = 0
    for _ in range(n_tick):
        axis = ra.randrange(3) if fix_axis is None else fix_axis
        if fix_phase_all is not None:
            pr = pairs_for_axis(L, axis, fix_phase_all)
        elif mode == "global_resample":
            pr = pairs_for_axis(L, axis, rp.randrange(2))
        else:
            pr = pairs_for_axis(L, axis, 0, per_line=True, rng=rp)
        for a, b in pr:
            ga, gb = grid[a], grid[b]
            grid[a], grid[b] = gb, ga
            ca, cb = cum[a], cum[b]
            na = [cb[0], cb[1], cb[2]]
            nb = [ca[0], ca[1], ca[2]]
            na[axis] -= 1        # 来自 b 的状态沿 -axis 移动一步
            nb[axis] += 1        # 来自 a 的状态沿 +axis 移动一步
            cum[a], cum[b] = na, nb
        if len(set(grid)) != N:
            perm_bad += 1
    occ = [0] * N
    for g in grid:
        occ[g] += 1
    vacuum = sum(1 for o in occ if o == 0)
    return cum, vacuum, perm_bad

ra = random.Random(20260918)
rp = random.Random(777)
NT = 2000
cum, vacuum, perm_bad = run(NT, L, ra, rp)
show("模拟 tick 数", float(NT))
show("格点数 = 诸元数", float(N))
chk("真空事件数（空格点计数）", float(vacuum), 0.0, 0.0)
chk("置换保持（每 tick 都是排列）", float(perm_bad), 0.0, 0.0)
rx2 = sum(c[0] ** 2 for c in cum) / N
ry2 = sum(c[1] ** 2 for c in cum) / N
rz2 = sum(c[2] ** 2 for c in cum) / N
show("<x^2>（格^2）", rx2)
show("<y^2>（格^2）", ry2)
show("<z^2>（格^2）", rz2)
show("<r^2> = <x^2>+<y^2>+<z^2>", rx2 + ry2 + rz2)
tol3 = 3.0 * m.sqrt(2.0 / N)          # 单分量的 3σ 相对标准误
show("单分量 <x^2> 的 3σ 相对标准误（N 个粒子）", tol3)
chk("<r^2> = n（扩散律，每 tick 一步）", rx2 + ry2 + rz2, float(NT), 0.03)
chk("各向同性：<x^2> = n/3（3σ 内）", rx2, NT / 3.0, tol3)
chk("各向同性：<y^2> = n/3（3σ 内）", ry2, NT / 3.0, tol3)
chk("各向同性：<z^2> = n/3（3σ 内）", rz2, NT / 3.0, tol3)
mx = sum(c[0] for c in cum) / N
show("<x>（净漂移，格）", mx)
chk("无净漂移：|<x>| < 5 sqrt(<x^2>/N)", 1.0 if abs(mx) < 5 * m.sqrt(rx2 / N) else 0.0, 1.0, 0.0)

# ================================================================== UP-6b
line("UP-6b 为什么相位必须「每线独立」：全局统一相位 ⟹ 系统性各向异性")
print("""
  对照：把相位改成「每 tick 全局重抽一个值」（同一 tick 内所有线同相位）。""")
r2_glob = []
for sa, sp in ((1, 2), (3, 4)):
    cg, _, _ = run(NT, L, random.Random(sa), random.Random(sp), mode="global_resample")
    gx = sum(c[0] ** 2 for c in cg) / N
    gy = sum(c[1] ** 2 for c in cg) / N
    gz = sum(c[2] ** 2 for c in cg) / N
    print("     种子(%d,%d)：<x^2>=%7.0f  <y^2>=%7.0f  <z^2>=%7.0f  <r^2>=%7.0f（各分量期望 %.0f）"
          % (sa, sp, gx, gy, gz, gx + gy + gz, NT / 3.0))
    r2_glob.append(gx + gy + gz)
show("全局统一相位：<r^2>/n（种子 1,2）", r2_glob[0] / NT)
show("全局统一相位：<r^2>/n（种子 3,4）", r2_glob[1] / NT)
show("对照：每线独立相位 <r^2>/n ≈ 1.00", 1.0)
chk("全局统一相位 ⟹ <r^2> 塌到 n 的 60% 以下（被钉住，被排除）",
    max(r2_glob) / NT, 0.0, 0.60)
print("""
  ⟹ 结论：**相位必须每线独立**。全局统一相位下，一个 tick 内同一轴上的所有线同侧，
     相位与「轴」耦合成了系统性取向模式（粒子倾向停在奇/偶层）⟹ 分量比可达 10³。
     （另做的 2×2 对照进一步显示：决定性因素是「每线独立相位」，
      与「轴/相位是否共用同一个 RNG」无关 —— 两种 RNG 安排下分量都不均。）""")

# ================================================================== UP-7
line("UP-7  两个必要条件（各向同性需轴随机；扩散需相位随机）")
NT7 = 600
cum_f, vac_f, _ = run(NT7, L, random.Random(4), random.Random(14), fix_axis=0)
y2_fa = sum(c[1] ** 2 for c in cum_f) / N
z2_fa = sum(c[2] ** 2 for c in cum_f) / N
seeds = (14, 15, 16, 17, 18)
x2_list = []
for s in seeds:
    c_, _, _ = run(NT7, L, random.Random(4), random.Random(s), fix_axis=0)
    x2_list.append(sum(c[0] ** 2 for c in c_) / N)
print("     固定轴 = x：各种子 <x^2> = %s" % ", ".join("%.1f" % v for v in x2_list))
x2_fa = sum(x2_list) / len(x2_list)
show("固定轴 = x：5 种子均值 <x^2>（期望 n）", x2_fa)
show("固定轴 = x：<y^2>（应为 0）", y2_fa)
show("固定轴 = x：<z^2>（应为 0）", z2_fa)
chk("固定轴 ⟹ 沿该轴扩散（5 种子均值 ≈ n，±20%）", x2_fa, float(NT7), 0.20)
chk("固定轴 ⟹ 另两轴冻结 <y^2> = 0", y2_fa, 0.0, 1e-12)
chk("固定轴 ⟹ 另两轴冻结 <z^2> = 0", z2_fa, 0.0, 1e-12)
print("""
  ⚠️ 数值注意：固定轴下各种子 <x^2> 散布（375~630）远大于「独立样本」的 3σ = 27。
     原因是同一条线上的 10 个粒子通过配对强关联 ⟹ **有效自由度 < 格点数**
     （这里 N_eff ~ 线数 = 100，故相对散布 ~14%，实测 18%）。
     ⟹ 衬底动力学的关联长度不短于线长；这也解释了三轴随机时散布自动变小
       （每粒子在三个方向都留位移，线内关联被打散）。""")

ra2, rp2 = random.Random(5), random.Random(15)
cum_fp, _, _ = run(NT7, L, ra2, rp2, fix_phase_all=0)
r2_fp = sum(c[0] ** 2 + c[1] ** 2 + c[2] ** 2 for c in cum_fp) / N
show("固定相位 = 0（轴随机）：<r^2>（600 tick）", r2_fp)
show("  实测 / 理论扩散值", r2_fp / NT7)
chk("固定相位 ⟹ 扩散被钉住（<r^2> << n）", r2_fp, 0.0, 0.09 * NT7)
print("""
  ⟹ 轴随机是**各向同性**的必要条件（固定轴 ⟹ 只沿一维扩散，另两轴冻结）。
     相位随机是**真扩散**的必要条件：固定相位下，粒子在轴上的奇偶角色被锁定，
     走一步就翻转奇偶 ⟹ 下一步换回另一端 ⟹ 二周期振荡，位移有界（上述 <r^2> = 2）。
     ⟹ tick 规则必须同时随机化「轴」与「相位」。""")

# ================================================================== UP-8
line("UP-8  连带结论：与第 18 轮 / §4 / C-2 的关系")
show("微观速度 l_P/t_P / (m/s)", L_P / T_P)
show("光速 c / (m/s)", C_MS)
show("相对偏差（l_P、t_P 各自舍入到 7 位所致）", (L_P / T_P) / C_MS - 1.0)
chk("每 tick 一步 ⟹ 微观速率恰为 c（第 18 轮的假设获得机制）", L_P / T_P, C_MS, 1e-6)
n_c_par = 4.0
show("§4 弛豫 4 次对换 / 并行下所需时间", n_c_par * T_P)
print("""
  · 第 18 轮「诸元微观恒以 c 运动」= 并行规则下「每 tick 每诸元走一步」⟹ 机制而非假设；
    「p_rev = m/m_Pl」= 相邻对换方向反转的概率，两者接上。
  · §4 的弛豫时标 ~4 t_P = 4 个 tick ⟹ 与 §4 完全自洽。
  · 并行更新定义了**全局同时的 tick** ⟹ 衬底优先参照系 ⟹ 这正是第 18 轮 C-2 要抹掉的东西。
    ⟹ **并行使 C-2 从「可选」升为「必需」**：A1 的 50:50 + 各向同性必须负责抹掉衬底绝对性。""")

# ------------------------------------------------------------------ 汇总
line("汇总")
n_ok = sum(1 for _, ok in CHECKS if ok)
n_bad = len(CHECKS) - n_ok
print("  检查项 %d，通过 %d，失败 %d" % (len(CHECKS), n_ok, n_bad))
for name, ok in CHECKS:
    if not ok:
        print("    [XX] %s" % name)
print("""
  判决：
  ✅ tick 的更新规则定为 **并行归一化：每 tick 每个格点恰好一次事件**
     （实现 = 沿随机轴的二分图完美匹配交换 + 随机相位；每格点恒有且仅有 1 个诸元、
      真空零测度、置换可逆、各向同性、⟨r²⟩ = n l_P²）。
  ❌ 串行（每 tick 全局一次对换）被三条独立判据排除：
     A1 的 per-元 事件率 1/t_P、A2 的泄漏率标定 ε0、§4 的速度弛豫时标 4 t_P。
  ✅ **47 μm 保住**：它本来就是并行口径的值（第 21 轮贴错标签，数值无需改）。
  ⚠️ 并行引入全局同时的 tick ⟹ 衬底优先系 ⟹ C-2 由「可选」升为「必需」。""")
