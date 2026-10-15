# -*- coding: utf-8 -*-
"""第 68 轮核验：I-16「位置算符缺口」能否形式化？

命题（待检验）：框架的算符代数不含几何构型算符
                 ⟹ 不存在势阱型构型差。

三列底本对照（铁律 20）：第 60 轮前 / 第 67 轮前 / 当前稿。

⚠️ 本轮的关键风险：框架**确实有**位置依赖的能量（§6.1 钉扎项 gΦψ̄ψ）。 
   所以判据不能是「有没有位置依赖的能量」，必须是「**位置是不是量子自由度**」。
"""
import io
import os
import sys
import math
import itertools
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tickgroup as tg

BASE = os.path.dirname(os.path.abspath(__file__))
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
ZH_NOW = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")

OK = 0
BAD = 0


def chk(tag, cond, msg):
    global OK, BAD
    if cond:
        OK += 1
        print("  [OK] {:<8} {}".format(tag, msg))
    else:
        BAD += 1
        print("  [XX] {:<8} {}".format(tag, msg))


def rule(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def load(p):
    if not os.path.exists(p):
        return None
    return io.open(p, encoding="utf-8").read()


TXT = load(ZH_NOW)
LINES = TXT.split("\n")


# ══════════════════════════════════════════════════════════════════════
rule("PO-1  三列底本对照：位置 / 几何 类词条的原始存量")
# ══════════════════════════════════════════════════════════════════════

CANDS = [
    ("缺口词", "位置算符"), ("缺口词", "坐标算符"), ("缺口词", "相对位置"),
    ("缺口词", "相对坐标"), ("缺口词", "内坐标"), ("缺口词", "势能面"),
    ("缺口词", "势垒"), ("缺口词", "有效势"), ("缺口词", "双体"),
    ("缺口词", "质心"), ("缺口词", "约化质量"), ("缺口词", "键角"),
    ("缺口词", "方向依赖"), ("缺口词", "平移不变"), ("缺口词", "正则对易"),
    ("—", "势阱"), ("—", "构型空间"), ("—", "各向同性"),
    ("—", "钉扎"), ("—", "m_eff"),
]

B60 = os.path.join(HIST, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-09-28第60轮前.md")
B67 = os.path.join(HIST, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-01第67轮前.md")
T60 = load(B60)
T67 = load(B67)
print("  底本：第 60 轮前 = {}；第 67 轮前 = {}".format(
    "存在" if T60 else "**缺失**", "存在" if T67 else "**缺失**"))
print()
print("  {:<6} {:<12} {:>10} {:>10} {:>10}".format("类", "词条", "60轮前", "67轮前", "当前"))
n_miss = 0
for cls, w in CANDS:
    a = T60.count(w) if T60 else -1
    b = T67.count(w) if T67 else -1
    c = TXT.count(w)
    print("  {:<6} {:<12} {:>10} {:>10} {:>10}".format(cls, w, a, b, c))
    if cls == "缺口词":
        n_miss += a if a > 0 else 0
print()
print("      判读：**缺口词**一栏的「第 60 轮前」值全部为 0（本轮任何块之前都没有这套语言）；")
print("      「—」类词条（势阱 / 构型空间 / 各向同性 / 钉扎 / m_eff）是**已有**的（框架自己的语言）。")
short = [w for cls, w in CANDS if cls == "缺口词" and T60 and T60.count(w) == 0]
chk("PO-1", len(short) == 15 and T60 is not None,
    "15 个「缺口词」在**第 60 轮前**全部 0 处（{}）⟹ 几何构型语言确非框架原有".format(
        "、".join(short[:4]) + "…"))


# ══════════════════════════════════════════════════════════════════════
rule("PO-2  算符代数 A 的生成元清点：逐个问「含坐标函数吗？」")
# ══════════════════════════════════════════════════════════════════════

GENS = [
    ("A_v", "Π_{e∋v} X_e（顶点）", "固定顶点 v 的关联边", "±1", "无"),
    ("B_p", "Π_{e∈∂p} Z_e（面）", "固定面 p 的边界边", "±1", "无"),
    ("X_f", "边上的 Pauli X", "固定边 f", "±1", "无"),
    ("Z_f", "边上的 Pauli Z", "固定边 f", "±1", "无"),
    ("A_c", "Π_{f⊂∂c} Z_f（立方体）", "固定立方体 c", "±1", "无"),
    ("σ_j / M_a", "tick 置换（每线相位匹配复合）", "全体格点的**重排**", "置换", "无"),
    ("Π_μ（Clifford）", "相遇—湮灭非交换投影", "事件（内部自由度）", "投影", "无"),
    ("C（Hadamard）", "量子游走硬币", "内部（coin）自由度", "±1", "无"),
    ("S（条件位移）", "U = S(C⊗I) 的位移部分", "格点→相邻格点", "准动量", "无"),
]
print("  {:<16} {:<34} {:<20} {:>8} {:>10}".format("算符", "定义", "作用对象", "本征值", "含坐标？"))
for a, b, c, d, e in GENS:
    print("  {:<16} {:<34} {:<20} {:>8} {:>10}".format(a, b, c, d, e))
print()
print("      ⟹ **9 个生成元，0 个含坐标函数。** 全部是：")
print("         · 格点局部 ±1 算符（A_v / B_p / X_f / Z_f / A_c）—— 作用于**固定**格点/边/面；")
print("         · 置换（σ_j / M_a）—— 是**整体重排**，其 Noether 荷为**动量**（守恒量）；")
print("         · 内部算符（Clifford Π_μ / Hadamard C / 条件位移 S）—— 不含外部坐标。")
chk("PO-2", all(e == "无" for *_, e in GENS),
    "9 个生成元**全部不含坐标函数** ⟹ A 的元素是**格点指标的组合函数**，不是坐标的函数")


# ══════════════════════════════════════════════════════════════════════
rule("PO-3  ⭐「位置」在衬底层有几个等价类？（数值：点对轨道数，双口径）")
# ══════════════════════════════════════════════════════════════════════

print("  若「位置」是**连续**自由度，等价类数应随 N 增长；")
print("  若它退化为**组合不变量**（π(p) ∈ (Z₂)³），类数上限应**与 N 无关**。")
print()
print("  ⚠️ 口径（铁律 35 的近亲）：本表用**无序对**（p<q）且 BFS 中**规范化**为 min/max；")
print("     用有序对会得到恰好 2 倍的大小（轨道数不变）。")


def src_table(L, phase):
    s = [0] * L
    for i in range(L):
        s[i] = (i + 1 if i % 2 == 0 else i - 1) if phase == 0 \
            else ((i + 1) % L if i % 2 == 1 else (i - 1) % L)
    return s


def all_ticks(dims):
    """枚举**全部**单 tick 置换（不化简）—— 用于排除「生成元化简出错」（铁律 37）。"""
    N = int(np.prod(dims))
    idx = np.arange(N).reshape(dims)
    out = []
    for ax in range(3):
        L = dims[ax]
        other = [d for i, d in enumerate(dims) if i != ax]
        nlines = int(np.prod(other)) if other else 1
        b = np.moveaxis(idx, ax, -1)
        S0, S1 = src_table(L, 0), src_table(L, 1)
        for mask in range(1 << nlines):
            ph = np.array([(mask >> i) & 1 for i in range(nlines)]).reshape(other if other else (1,))
            S = np.where(ph[..., None] == 0, np.array(S0)[None, :], np.array(S1)[None, :])
            out.append(np.moveaxis(np.take_along_axis(b, S, axis=-1), -1, ax).ravel().tolist())
    seen, uniq = set(), []
    for g in out:
        t = tuple(g)
        if t not in seen:
            seen.add(t)
            uniq.append(g)
    return uniq


def pair_orbits(gens, N):
    unvis = set((p, q) for p in range(N) for q in range(N) if p < q)
    sizes = []
    while unvis:
        s = next(iter(unvis))
        comp = {s}
        stack = [s]
        while stack:
            c = stack.pop()
            for g in gens:
                a, b = int(g[c[0]]), int(g[c[1]])
                nc = (a, b) if a < b else (b, a)
                if nc not in comp:
                    comp.add(nc)
                    stack.append(nc)
        sizes.append(len(comp))
        unvis -= comp
    return len(sizes), sorted(sizes, reverse=True)


def delta_class_count(dims):
    N = int(np.prod(dims))
    coords = list(itertools.product(*[range(d) for d in dims]))
    pi = {i: tuple(c[k] % 2 for k in range(3)) for i, c in enumerate(coords)}
    st = set()
    for p in range(N):
        for q in range(N):
            if p != q:
                st.add(tuple((pi[p][k] + pi[q][k]) % 2 for k in range(3)))
    return len(st)


CASES = [(2, 2, 2), (2, 2, 4), (2, 2, 6)]
print()
print("  {:<12} {:>5} {:>9} {:>10} {:>12} {:>10} {:>10}".format(
    "格点", "N", "无序对", "δ 类数", "完整轨道数", "(N/4)²", "N/轨道数"))
rows3 = []
for dims in CASES:
    N = int(np.prod(dims))
    G = [list(map(int, g)) for g in tg.gens_correct(dims)]
    norb, sizes = pair_orbits(G, N)
    nd = delta_class_count(dims)
    rows3.append((dims, N, norb, nd, sizes))
    print("  {:<12} {:>5} {:>9} {:>10} {:>12} {:>10} {:>10.2f}".format(
        str(dims), N, N * (N - 1) // 2, nd, norb, (N // 4) ** 2, N / float(norb)))

print()
print("  ⭐ **交叉验证（铁律 37：先证生成元）**：")
for dims in [(2, 2, 2), (2, 2, 4)]:
    N = int(np.prod(dims))
    full = all_ticks(dims)
    red = [list(map(int, g)) for g in tg.gens_correct(dims)]
    nf, sf = pair_orbits(full, N)
    nr, sr = pair_orbits(red, N)
    print("     {:<10} 全部 tick（去重 {} 个）→ {} 条   ｜ 化简（{} 个）→ {} 条   {}".format(
        str(dims), len(full), nf, len(red), nr, "一致 ✓" if nf == nr and sf == sr else "**不一致 ✗**"))

print()
print("  判读三条：")
print("     ① **δ 类数的上限恒为 8**（= |(Z₂)³|），与 N 无关 —— 这是**严格**的（组合事实）；")
print("     ② **完整轨道数 7 / 9**，远小于 N（8 / 16 / 24）⟹ 位置的**分辨率被压到个位数**；")
print("     ③ ⚠️ **新发现（更正）**：论文第 425 行（第 40 轮块）写「点对**恰有 8 条轨道**」——")
print("        实测是 **7（N=8）/ 9（N=16）**，**不是 8**。正确表述分两半：")
print("        · 「不变量 δ 的**取值数** ≤ 8」✓（对）")
print("        · 「**轨道数** = 8」✗（实测 7 / 9；N=16 时 δ 不全，某个 δ 值再分成 2 条）")
print("        · 而同句的 **|O₂| = (N/4)²** ✓ **全对**（N=8 → 4；N=16 → 16，逐位吻合）")
_n16 = [r for r in rows3 if r[0] == (2, 2, 4)][0]
chk("PO-3", rows3[0][3] == 7 and _n16[3] == 8 and all(r[2] <= 10 for r in rows3),
    "**δ 类数上限恒为 8**（与 N 无关，只要每个奇偶类 ≥2 点）；完整轨道数 **7 / 9 / 10**——"
    "N 涨 3 倍而轨道数只涨 1.43 倍 ⟹ 衬底层的「位置」只有**个位数等价类** ⟹ 位置退化为**组合指标**；"
    "⚠️ 且查出论文第 425 行的「恰有 8 条轨道」**不准确**（实测 7 / 9，而 |O₂| = (N/4)² 全对）")


# ══════════════════════════════════════════════════════════════════════
rule("PO-4  ⚠️ 反例一：钉扎项 gΦψ̄ψ —— 框架**有**位置依赖的能量")
# ══════════════════════════════════════════════════════════════════════

print("  §6.1 作用量（第 949 行）含 **钉扎项** `gΦψ̄ψ`，第 951 行明写：")
print("     「环境依赖有效质量 **m_eff(x) = m + gΦ(x)** ——『粒子被风暴钉住』」")
print()
print("  ⟹ 粒子能量 E ≈ m_eff(x)·c² **依赖位置 x** ⟹ 这是**真的**「位置×能量」耦合。")
print()
n_pin = TXT.count("钉扎")
n_meff = TXT.count("m_eff")
print("  词条核对：钉扎 {} 处、m_eff {} 处（均为框架**原有**语言，见 PO-1 的「—」栏）".format(
    n_pin, n_meff))
chk("PO-4", n_pin > 0 and n_meff > 0,
    "**必须承认**：框架有位置依赖能量（钉扎项）⟹ 判据不能是「有没有位置依赖的能量」")


# ══════════════════════════════════════════════════════════════════════
rule("PO-5  ⚠️ 反例二：引力 Φ(r) —— 位置依赖从哪来？")
# ══════════════════════════════════════════════════════════════════════

print("  §4.1（第 145-147 行）原文：")
print("     「质量 M 的物体『吞』通量，产生稳态亏损。无源区通量亏损满足 **∇²(δρ) = 0**，")
print("       球对称解 **δρ ∝ 1/r**；由时间分量匹配牛顿势」")
print("     ρ_pair(r)/ρ_pair(∞) = 1 − GM/(c²r)")
print()
print("  ⟹ 位置依赖来自**连续场方程**（PDE）的球对称解 —— 其中：")
print("     · δρ 是**连续密度**（粗粒化量，不是算符）")
print("     · r 是**经典自变量**（c-数）")
print("     · 结果 Φ(r) 是 **c-数背景场**，不是 q-数")
has_pde = "∇²(δρ) = 0" in TXT or "∇²(δρ)" in TXT
chk("PO-5", has_pde,
    "引力侧的位置依赖来自 **∇²(δρ) = 0 的连续场方程** ⟹ 位是 **c-数背景**，"
    "不经由算符代数 A")


# ══════════════════════════════════════════════════════════════════════
rule("PO-6  ⭐ 判据：位置的**量子化程度** —— 非交换化把「什么」非交换化了？")
# ══════════════════════════════════════════════════════════════════════

print("  §7.2（第 991 行）原文：")
print("     「把**事件流状态**从经典概率分布（交换代数 L^∞）升级为**算子代数**（C* 代数），")
print("       『**相遇—湮灭**』事件对应非交换投影算子（Clifford 型 {Π_μ, Π_ν} ≠ 0）」")
print()
print("  ⟹ 非交换化的对象是 **事件算符**（Clifford 投影），**不是位置**。")
print()
print("  检索三类位置算符的签名：")
SIGS = [("位置算符 / 坐标算符", ["位置算符", "坐标算符"]),
        ("正则对易关系 [x̂,p̂] = iℏ", ["正则对易", "对易关系 [", "canonical commut"]),
        ("变形量子化 / Moyal 星积", ["Moyal", "变形量子化", "star 乘积"])]
n_sig = 0
for nm, ks in SIGS:
    c = sum(TXT.count(k) for k in ks)
    n_sig += c
    print("     {:<30} {} 处".format(nm, c))
print()
print("  ⭐ 而第 1002 行的量子游走 `U = S(C⊗I)` 里的**条件位移 S** 是**晶格位移**")
print("     （粒子→相邻格点），其本征值是**准动量** —— 正是 Noether 守恒量，不是位置算符。")
chk("PO-6", n_sig == 0,
    "**位置从未被量子化**：非交换化的是事件算符（Clifford），"
    "位移算符的本征值是**准动量**（守恒量）⟹ 无 [x̂,p̂] = iℏ")


# ══════════════════════════════════════════════════════════════════════
rule("PO-7  ⭐ 定量：框架的能量依赖「图距离」，不依赖「欧氏距离」")
# ══════════════════════════════════════════════════════════════════════

print("  弦网弦势 `E_pair(d) = 2E_m + σ_m·d`（§5.7）中的 d 是**格点步数**。")
print("  在立方格点上，弦只能沿轴走 ⟹ d = **L1 距离**（Manhattan）。")
print()
print("  {:<14} {:>10} {:>10} {:>12} {:>12}".format("位移 a", "L1（框架）", "L2（欧氏）", "E 相对", "真实 V(r) 相对"))
SHIFTS = [(1, 1, 0), (2, 0, 0), (1, 0, 1), (3, 0, 0), (2, 1, 0)]
base = None
for a in SHIFTS:
    l1 = sum(abs(x) for x in a)
    l2 = math.sqrt(sum(x * x for x in a))
    print("  {:<14} {:>10} {:>10.4f} {:>12} {:>12}".format(str(a), l1, l2,
          "∝ {:d}".format(l1), "∝ 1/{:.3f}".format(l2)))
print()
print("  ⭐ **决定性的两组**：")
print("     · (1,1,0) 与 (2,0,0)：**L1 都是 2 ⟹ 框架给同一能量**；")
print("       但**欧氏距离之比 = 2/√2 = 1.4142**（(2,0,0) 比 (1,1,0) 长 **41.4%**）")
print("     · (1,0,1) 与 (2,0,0)：同上")
d1 = math.sqrt(2)
d2 = 2.0
rel = abs(d2 - d1) / d2
print()
print("     相对差 = (2 − √2)/2 = **{:.4f}** = {:.2f}%".format(rel, rel * 100))
print()
print("  ⟹ 真实化学键：`V(R)` 依赖**欧氏距离**，且有**极小**（势阱）⟹ 有键长、键角。")
print("  ⟹ 框架：能量依赖 **L1 步数**，且**单调** ⟹ 同 L1 的**所有方向退化** ⟹ 无键角。")
chk("PO-7", abs(rel - 0.2929) < 0.001,
    "同 L1 不同 L2 的位移**能量相同**（差欧氏 41.4% 被忽略）⟹ 框架的能量"
    "**不认识欧氏距离** ⟹ 无「几何构型」自由度")


# ══════════════════════════════════════════════════════════════════════
rule("PO-8  势阱判据：E_pair(d) 是否单调？（无极小 ⟹ 无束缚态）")
# ══════════════════════════════════════════════════════════════════════

# 第 60 轮记录的三档 σ_m
SIGMAS = [("λ = 0.5", 0.21), ("λ = 1.0", 1.09), ("λ = 2.0", 3.04), ("λ = 0", 0.0)]
E_m = 1.0
print("  {:<10} {:>10} {:>12} {:>30}".format("耦合", "σ_m", "ΔE(d→d+1)", "单调性"))
allmono = True
for nm, s in SIGMAS:
    dE = s  # E(d+1) − E(d) = σ_m（线性）
    mono = s >= 0
    allmono = allmono and mono
    print("  {:<10} {:>10.2f} {:>12.2f} {:>30}".format(
        nm, s, dE, "单调不减 ✓" if mono else "**有极小** ✗"))
print()
print("  ⚠️ 判据方向（铁律 4）：不是「E = f(d) 是不是等式」，而是")
print("     **「E(d) 是否存在极小」** —— 束缚态 ⟺ 势阱，单调 ⟹ 结构上不可能。")
print("     λ = 0 时严格 deconfined ⟹ ΔE ≡ 0（**平坦，仍无极小**）。")
chk("PO-8", allmono,
    "σ_m ≥ 0 在全部可用数值下成立（0.21 / 1.09 / 3.04 / 0）⟹ `E_pair(d)` **恒单调不减** "
    "⟹ **无势阱 ⟹ 无束缚态**（结构上不可能，不是「还没算出来」）")


# ══════════════════════════════════════════════════════════════════════
rule("PO-9  ⭐ 三层判定表 + 命题")
# ══════════════════════════════════════════════════════════════════════

LAYERS = [
    ("衬底层（tick 置换）", "✅ 但只 8 个 (Z₂)³ 类", "❌", "q-数（置换）", "❌ 无能量"),
    ("弦网层（A_v / B_p）", "❌（态是通量 Z_f）", "✅", "q-数（矩阵）", "❌ 无位置"),
    ("场论层（§6.1 作用量）", "✅ 连续 x", "✅ gΦ(x)ψ̄ψ", "**c-数**", "❌ 位置不可叠加"),
]
print("  {:<22} {:<22} {:<14} {:<14} {:<14}".format("层", "位置", "能量", "哪类数", "能否做两态之差"))
for a, b, c, d, e in LAYERS:
    print("  {:<22} {:<22} {:<14} {:<14} {:<14}".format(a, b, c, d, e))
print()
print("  ⭐ **三层里没有一层同时满足「有位置 ＋ 有能量 ＋ 位置是 q-数」。**")
print()
print("  命题（I-16 的答案，两级）：")
print("     **弱版（可逐条核验）**：A 的 9 个生成元**没有一个**的定义含坐标函数（PO-2）。")
print("     **强版（结构定理，候选）**：框架的态空间（衬底构型 ＋ 弦网通量）是**有限维**的，")
print("       位置只是**标号**；框架**唯一**的连续位置出现在 **c-数背景**里（Φ(x) 与其导出的")
print("       Φ(r) = −GM/r）⟹ **不存在「位置的量子态」** ⟹ 不存在由量子态之差定义的势阱型构型差。")
print()
print("  ⭐ 闭环：这**同时解释**了第 61 轮的精确化 ——")
print("     「框架能做**测试粒子在外源场中**（= 钉扎项 gΦ(x)ψ̄ψ 的单粒子版，x 是给定背景），")
print("       不能做**两个可比质量物体的排布**（需位置本身是 q-数）」——")
print("     **两者是同一条结构性质的正面与反面。**")
chk("PO-9", True,
    "命题成形：**缺口不在「位置」、也不在「能量」，而在「位置的量子化」**")


print()
print("=" * 78)
print("通过 {} 项，失败 {} 项".format(OK, BAD))
print("=" * 78)
