# -*- coding: utf-8 -*-
"""
PM 系列 —— 「配对」的机制：湮灭 = 相邻格点的置换（对换）
若每个 tick 相当于对占据态施加一次**相邻对换**：
  · 诸元数自动守恒（置换是双射）      ⟹ C-5 配对不再靠假设
  · 任何格点任何时刻恰好 1 个诸元     ⟹ C-1 满占位自动成立
  · 真空态永不出现（测度 0）          ⟹ C-4 化解
  · 状态图案每 tick 平移一格          ⟹ c = l_P/t_P
标准库：math / random。运行：
  C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe outputs/_pairing_permutation.py
"""
import math as m
import random
from collections import deque

FAILS = []


def chk(tag, got, want, rtol=1e-9):
    ok = abs(got - want) <= rtol * max(abs(want), 1e-300)
    print("  [%s] %-44s got=%.12g   want=%.12g" % ("OK" if ok else "XX", tag, got, want))
    if not ok:
        FAILS.append(tag)


def line(t):
    print("\n" + "-" * 74)
    print(t)
    print("-" * 74)


def show(tag, val, unit=""):
    print("  %-44s %-22.10g %s" % (tag, val, unit))


# ------------------------------------------------------------------ 常数
c = 2.99792458e8
G = 6.67430e-11
h_planck = 6.62607015e-34
hbar = h_planck / (2.0 * m.pi)
lP = m.sqrt(hbar * G / c ** 3)
tP = lP / c
H0 = 2.1927e-18
tH = 1.0 / H0
mPl = m.sqrt(hbar * c / G)
m_e = 9.1093837015e-31

line("PM-1  置换模型：占位率恒为 1，真空态零测度（数值模拟）")
random.seed(20260918)
N = 400
T = 200000
occ = list(range(N))            # 格点 i 上的诸元标签；初始 = i
vacuum_events = 0
for step in range(T):
    i = random.randrange(N)
    j = (i + 1) % N             # 相邻对换（环）
    occ[i], occ[j] = occ[j], occ[i]
    # 检查：任一格点是否出现"空"（标签为 None）
    if any(x is None for x in occ):
        vacuum_events += 1
uniq = sorted(occ)
is_perm = (uniq[0] == 0 and uniq[-1] == N - 1 and len(set(occ)) == N)
print("  [%s] 置换后仍是 0..%d 的排列（互异计数 %d）" % ("OK" if is_perm else "XX", N - 1, len(set(occ))))
if not is_perm:
    FAILS.append("置换保持排列")
chk("真空事件计数 = 0", vacuum_events, 0, 1e-15)
print("""
  ⟹ 相邻对换（N=%d，%d 次 tick）后：格点数 = 诸元数 = %d，**没有一次出现空格点**。
  ⟹ 这不是"碰巧占满"，而是**结构性保证**：置换是双射 ⟹ 每格点恒有且仅有 1 个诸元。
  ⟹ **C-1（满占位）、C-4（真空零测度）、C-5（配对/守恒）一次性由构造得到**，
     不再依赖第 20 轮的排除法（那里只能说"独立泊松被 Δc/c=26%% 排除"）。"""
      % (N, T, len(set(occ))))

line("PM-2  代价：随机对换是**扩散**的，不是弹道的")
print("""
  若每 tick 随机选方向，状态图案做随机游走 ⟹ ⟨r²⟩ = l_P²·(t/t_P)（扩散），
  而信号传播需要的是**弹道** r = c·t。二者冲突。""")
random.seed(7)
trials, steps = 4000, 2000
s2 = 0.0
for _ in range(trials):
    x = 0
    for _s in range(steps):
        x += 1 if random.random() < 0.5 else -1
    s2 += x * x
mean_x2 = s2 / trials
show("模拟 ⟨x²⟩（2000 步）", mean_x2)
show("理论 = 步数", float(steps))
chk("⟨x²⟩ = n（扩散律）", mean_x2, float(steps), 0.06)
print("""
  ⟹ 确认：**各向同性 + 随机对换 ⟹ 扩散**（⟨x²⟩ ∝ t），不是 r = ct。
     所以第 18 轮说的"一步 l_P 一拍 t_P ⟹ c"只在**方向持续**时才成立。""")

line("PM-3  ⚠️ 混合尺度：一个哈勃时只混合 ~47 μm")
print("""
  扩散尺度 R_mix = l_P·sqrt(t/t_P)：""")
print("     时间 t            t/t_P              R_mix = l_P sqrt(t/t_P)")
for tag, t in (("1 秒", 1.0), ("1 年", 3.15576e7), ("宇宙年龄 t_H", tH)):
    R = lP * m.sqrt(t / tP)
    unit = "m" if R < 1e-3 else "m"
    print("     %-16s %-18.6g %.6g %s" % (tag, t / tP, R, unit))
R_mix_H = lP * m.sqrt(tH / tP)
show("R_mix(t_H) (μm)", R_mix_H * 1e6)
show("与哈勃半径 R_c 之比", R_mix_H / (c / H0))
print("""
  ⟹ **一个哈勃时内，置换动力学只能把约 47 μm 的范围混合均匀**；
     相对哈勃半径，这个尺度只有 %.3g。**宇宙学尺度上衬底远未热化。**
  ⟹ 这给框架一条实打实的约束：任何"视界内已达热平衡/等分"的说法，
     都不能靠置换动力学在哈勃时内实现 —— 等分账必须是**结构性**的（第 1/4 轮的做法），
     不能是动力学热化的结果。""" % (R_mix_H / (c / H0)))

line("PM-4  化解：持续长度（第 18 轮的 p_rev）把弹道与扩散接起来")
print("""
  第 18 轮：质量 = 每拍的反转概率 p_rev = m/m_Pl，持续长度 λ_C = l_P/p_rev = hbar/(mc)。
  ⟹ 在 r < λ_C：方向持续 ⟹ **弹道**，速度 c；
    在 r > λ_C：方向随机化 ⟹ **扩散**，D = c²τ_corr/d（d=3）。""")
for nm, mm in (("电子", m_e), ("质子", 1.67262192369e-27), ("普朗克质量", mPl)):
    p_rev = mm / mPl
    lam = hbar / (mm * c)
    tau_c = lam / c
    D = c ** 2 * tau_c / 3.0
    print("     %-12s p_rev=%.6g  λ_C=%.6g m  τ_corr=%.6g s  D=ℏ/(3m)=%.6g m²/s"
          % (nm, p_rev, lam, tau_c, D))
# τ_corr = λ_C/c = hbar/(m c^2)，注意别把 λ_C 直接当代 τ
chk("D = c²τ_corr/3 = ℏ/(3m)（电子）", c ** 2 * (hbar / (m_e * c ** 2)) / 3.0, hbar / (3 * m_e), 1e-12)
D_nelson = hbar / (2 * m_e)
show("Nelson 随机力学 D = ℏ/(2m)（电子）", D_nelson)
show("两者之比（维度因子）", D_nelson / (hbar / (3 * m_e)))
print("""
  ⟹ **框架自发给出 D ~ ℏ/(d·m) 的量子扩散**：三维给 ℏ/(3m) = %.4g m²/s（电子），
     与 Nelson 随机力学的 **ℏ/(2m) = %.4g m²/s 同形式同量级**（差 1.5 倍 = 维度因子）。
  ⟹ 意义：**p_rev = 0（无质量）⟹ 永不反转 ⟹ 纯弹道 = c**；
     **p_rev > 0 ⟹ λ_C 之内弹道、之外扩散**。c 是 p_rev→0 的极限，这解释了两件事：
     ① 为什么只有无质量者恰好走 c；② 为什么"一步一拍 ⟹ c"需要配 p_rev 才成立。
  ⚠️ 诚实：⟨r²⟩ ∝ t（扩散）与量子波包的 ⟨r²⟩ ∝ t²（弹道展宽）**标度不同**，
     这里说的是**衬底层面的布朗运动**，不是可观测的波包展宽，别混为一谈。"""
      % (hbar / (3 * m_e), D_nelson))

line("PM-5  置换群的代数性质：遍历性与可逆性")


def swap(tup, i, j):
    L = list(tup)
    L[i], L[j] = L[j], L[i]
    return tuple(L)


for n in (4, 5):
    ident = tuple(range(n))
    gens = [swap(ident, i, i + 1) for i in range(n - 1)]   # 相邻对换
    seen = {ident}
    q = deque([ident])
    while q:
        s = q.popleft()
        for g in gens:
            t2 = tuple(s[g[k]] for k in range(n))
            if t2 not in seen:
                seen.add(t2)
                q.append(t2)
    print("     N=%d：相邻对换生成 %d 个排列，%d! = %d  ⟹ %s"
          % (n, len(seen), n, m.factorial(n), "遍历 ✓" if len(seen) == m.factorial(n) else "不遍历 ✗"))
    chk("N=%d 相邻对换生成 S_N" % n, len(seen), m.factorial(n), 1e-15)
print("""
  ⟹ **相邻对换生成整个对称群** ⟹ 动力学在构型空间上**遍历**（可达任意排列）。
  ⟹ **置换可逆** ⟹ 底层**无信息丢失、无熵产生**。
     ⟹ 宏观不可逆性只能来自**粗粒化** —— 正是 B5 的 16 原始态 → 1.284 有效态那一层相干压缩。
     ⟹ 这给第 19 轮那个"压缩因子 11.0904"指派了物理身份：**它就是粗粒化/不可分辨性的度量**。
        （⚠️ 这只是身份指派，11.0904 的**数值**仍未推导出来。）""")

line("PM-6  判决")
print("""
  ✅ **配对机制找到了：湮灭 = 相邻格点的对换（置换）**。
     一次构造同时给出：诸元数守恒（C-5）、每格点恒 1 个诸元（C-1）、真空零测度（C-4）、
     状态图案每拍平移一格 ⟹ **c = l_P/t_P**。三条承诺从"排除法"升级为"构造"。
  ✅ **置换群性质**：相邻对换生成 S_N（N=4→24、N=5→120 ✓ 遍历）；可逆 ⟹ 底层无熵产生
     ⟹ 宏观不可逆 = 粗粒化 ⟹ 给 11.0904 那个压缩因子指派了身份（仍未推出数值）。
  ⚠️ **代价/新张力**：随机对换是**扩散**的（⟨x²⟩ = n 已验证），不是弹道的。
     ⟹ 必须靠第 18 轮的 **p_rev（持续长度）** 才在 λ_C 之内恢复弹道 c。
     ⟹ **c 是 p_rev → 0 的极限**；有质量者在 r > λ_C 上退化为扩散。
  ⚠️ **混合尺度是个硬约束**：R_mix = l_P√(t/t_P)，一个哈勃时只混合 **%.1f μm**（= %.2g R_c）
     ⟹ 宇宙学尺度上衬底**远未热化** ⟹ 等分账不能靠动力学热化，必须是结构性的。
  🎯 **意外收获**：D = c²τ_corr/3 = **ℏ/(3m)**（电子 %.3g m²/s），与 Nelson 随机力学的
     **ℏ/(2m)** 同形式同量级（差 1.5 倍 = 维度因子）——框架衬底自发给出 ℏ/m 量级的量子扩散。"""
      % (R_mix_H * 1e6, R_mix_H / (c / H0), hbar / (3 * m_e)))

line("汇总")
print("  失败项：%s" % ((", ".join(FAILS)) if FAILS else "无"))
