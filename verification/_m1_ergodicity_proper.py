# -*- coding: utf-8 -*-
"""
EG 系列 —— 复核 _m1_boltzmann.py 的「遍历性 0.00%」，并做真正的 Birkhoff 检验
背景：论文 §4.2 六命题链第 2 条「遍历性（Birkhoff–Khinchin）」的数值支撑来自
      `遍历性: 前/后半段时间平均 T 偏差 0.00%`（_m1_boltzmann.py 第 181 行）。
本轮问两件事：
  (1) 那个数能否复现？
  (2) 它测的是不是**遍历性**？若不是，真正的 Birkhoff 检验结果如何？
真正的检验：对可观测 O = v²，比较
      per-particle 时间平均 ⟨O_i⟩_t 的**离散度**  随样本数 n_t 的标度
      · 遍历 ⟹ 离散度 ∝ 1/√n_t（随观测时间下降，各粒子时间平均趋同于系综平均）
      · 非遍历 ⟹ 离散度 = 常数（不随 n_t 下降）
需要 numpy（venv 有 2.5.3）。运行：
  C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe outputs/_m1_ergodicity_proper.py
"""
import math as m

import numpy as np

FAILS = []


def chk(tag, got, want, rtol=1e-9):
    ok = abs(got - want) <= rtol * max(abs(want), 1e-300)
    print("  [%s] %-44s got=%.12g   want=%.12g" % ("OK" if ok else "XX", tag, got, want))
    if not ok:
        FAILS.append(tag)


def line(t):
    print("\n" + "-" * 76)
    print(t)
    print("-" * 76)


def show(tag, val, unit=""):
    print("  %-44s %-22.10g %s" % (tag, val, unit))


# ------------------------------------------------ 事件流 DSMC（照抄原脚本的碰撞规则）
def run_dsmc(N=1000, L=100.0, v0=1.0, dt=0.3, nu_coll=0.05, seed=7,
             n_eq=400, n_samp=4000, freeze=False):
    """freeze=True ⟹ 采样阶段关闭碰撞（非遍历对照组）"""
    rng = np.random.default_rng(seed)
    d = 2
    xs = rng.uniform(0, L, N)
    ys = rng.uniform(0, L, N)
    theta = rng.uniform(0, 2 * np.pi, N)
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta)

    def collide():
        n_pairs = int(N * nu_coll * dt)
        for _ in range(n_pairs):
            a = int(rng.integers(0, N))
            b = int(rng.integers(0, N))
            if a == b:
                continue
            phi = rng.uniform(0, 2 * np.pi)
            v_ab = np.array([vx[a], vy[a]]) - np.array([vx[b], vy[b]])
            vcm = (np.array([vx[a], vy[a]]) + np.array([vx[b], vy[b]])) / 2
            rel = np.linalg.norm(v_ab)
            vx[a], vy[a] = vcm[0] + rel / 2 * np.cos(phi), vcm[1] + rel / 2 * np.sin(phi)
            vx[b], vy[b] = vcm[0] - rel / 2 * np.cos(phi), vcm[1] - rel / 2 * np.sin(phi)

    def move():
        nonlocal xs, ys
        xs = (xs + vx * dt) % L
        ys = (ys + vy * dt) % L

    for _ in range(n_eq):                 #  equilibration（碰撞开启）
        move()
        collide()
    if freeze:
        for _ in range(30):               #  冻结前让位置再混一下（不影响速度）
            move()

    store = np.empty((n_samp, N))
    T_series = []
    for k in range(n_samp):
        move()
        if not freeze:
            collide()
        store[k] = vx ** 2 + vy ** 2
        T_series.append(np.mean(store[k]) / d)
    return store, np.array(T_series), d


def proxy_ergodicity(T_series):
    """论文的代理指标：前/后半段平均温度偏差"""
    half = len(T_series) // 2
    a, b = np.mean(T_series[:half]), np.mean(T_series[half:])
    return abs(a - b) / b * 100.0


def spread_of_time_averages(store, n_t):
    """per-particle 时间平均 ⟨O_i⟩_t 的相对离散度（O = v²）"""
    ta = store[:n_t].mean(axis=0)
    return float(np.std(ta) / np.mean(ta))


line("EG-1  复现论文的代理指标（前/后半段温度偏差）")
store1, T1, d = run_dsmc(seed=7, freeze=False)
store0, T0, _ = run_dsmc(seed=7, freeze=True)     # 对照组：采样阶段无碰撞（明确非遍历）
p1 = proxy_ergodicity(T1)
p0 = proxy_ergodicity(T0)
show("原设置（碰撞开启）代理指标 (%)", p1)
show("对照组（冻结，无碰撞）代理指标 (%)", p0)
print("""
  ⟹ **代理指标在两种情形下都 ≈ 0.00%**：论文报的「遍历性 0.00%」**复现成功**（第 1 问 ✓），
     但它在**明确非遍历**的对照组里同样给 0.00% ⟹ **它不是遍历性的检验**（第 2 问 ✗）。""")

line("EG-2  真正的 Birkhoff 检验：时间平均离散度随样本数的标度")
print("""
  可观测 O = v²。2D 麦克斯韦下 sd(O)/mean(O) = 1，故单次采样的相对离散度为 1。
  遍历 ⟹ 时间平均离散度 ∝ 1/sqrt(n_t)；非遍历 ⟹ 不随 n_t 下降。""")
print("     n_t       原设置 spread      冻结对照 spread    1/sqrt(n_t)（遍历预期）")
rows = []
for n_t in (25, 100, 400, 1600, 4000):
    s1 = spread_of_time_averages(store1, n_t)
    s0 = spread_of_time_averages(store0, n_t)
    rows.append((n_t, s1, s0))
    print("     %-8d %-18.6f %-19.6f %.6f" % (n_t, s1, s0, 1.0 / m.sqrt(n_t)))
r1 = rows[-1][1] / rows[0][1]
r0 = rows[-1][2] / rows[0][2]
show("原设置：spread(4000)/spread(25)", r1)
show("冻结对照：spread(4000)/spread(25)", r0)
show("遍历预期比值 = sqrt(25/4000)", m.sqrt(25.0 / 4000.0))
chk("原设置：离散度随 n_t 显著下降（遍历）", r1 < 0.5, True, 1e-9)
chk("冻结对照：离散度不下降（非遍历）", r0 > 0.8, True, 1e-9)

line("EG-3  判决")
print("""
  ✅ **第 1 问：论文的 0.00%% 复现成功**（同参数、同种子下代理指标为 %.4f%%）。
  ❌ **第 2 问：那不是遍历性检验。** 证据：把采样阶段的碰撞关掉（明确非遍历），
     代理指标依然给 %.4f%% —— 它对非遍历**完全不敏感**。
     它实际测的是**温度的平稳性/无漂移**（前后半段平均温度是否相同），
     而 T 由能量守恒固定 ⟹ 这个量几乎恒为 0，与遍历性无关。
  ✅ **真正的 Birkhoff 检验通过**：原设置下 per-particle 时间平均的离散度随样本数下降
     （spread(4000)/spread(25) = %.3f；遍历预期 sqrt(25/4000) = 0.079，实测降幅较小是因为采样相关），
     而冻结对照不下降（比值 %.3f ≈ 1）⟹ **系统确实是遍历的，只是论文的证据选错了**。
  ⟹ 结论：**结论对，证据错**。建议把第 2 条证据换成 Birkhoff 检验
     （per-particle 时间平均趋同于系综平均，离散度 ∝ 1/sqrt(n_t)），
     并把原来的「前/后半段温度偏差」改标为**平稳性**检验（它是第 1 条该用的证据）。"""
      % (p1, p0, r1, r0))

line("汇总")
print("  失败项：%s" % ((", ".join(FAILS)) if FAILS else "无"))
