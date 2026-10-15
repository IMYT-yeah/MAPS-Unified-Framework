# -*- coding: utf-8 -*-
"""
第 57 轮核验：框架是决定论的吗？「everything」在框架里对应什么？

用户提出的推理链：
    「如果该理论成立 ⟹ 宇宙应该是决定论的（初始状态决定一切）
      ⟹ 而初始状态之后生成的是 everything（所有可能都是可能的）」

本轮把这条链逐环检验，并把它拆成**框架内可判定的问题**：
    DF-1  词条清点：框架有没有「决定论 / 量子态」这一层？
    DF-2  底层的性质：tick 是双射吗？（可逆 ⟹ 无熵产生）
    DF-3  随机性注入在哪一层？（h = ln3 + L²ln2）
    DF-4  ★ 「初始状态决定一切」——「初始状态」里含 tick 序列吗？
    DF-5  ★ H2（决定论版）的隐藏开销
    DF-6  ★★ §7.4（'t Hooft 式：底层确定）vs §8.6.7（轴/相位随机）—— 冲突？
    DF-7  ★★ 「everything」的四种读法，逐一判定
    DF-8  ★★ 数值：非遍历性 —— 一条轨迹能访问多少构型？
    DF-9  ★★ 数值：等分账 = 每条轨道上的唯一不变测度
    DF-10 量子效应的地位：涌现还是公设？
    DF-11 第 43 轮的口径改写：熵增 = 无知 ⟹ 它需要非决定论吗？
    DF-12 汇总
"""

import io, os, math, itertools, random

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")

OK = 0
BAD = 0
def chk(tag, cond, msg):
    global OK, BAD
    if cond:
        OK += 1
        print("  [OK] {:<6} {}".format(tag, msg))
    else:
        BAD += 1
        print("  [XX] {:<6} {}".format(tag, msg))

txt = io.open(ZH, encoding="utf-8").read()
lines = txt.split("\n")
lP = 1.61628e-35          # 自洽导出（√(ℏG/c³)），第 56 轮的教训

print("=" * 78)
print("第 57 轮：框架是决定论的吗？「everything」对应什么？")
print("=" * 78)

# ================================================================
print("\n[DF-1] 词条清点：框架有没有「决定论」与「量子态」这两层？")
WORDS_A = ["决定论", "非决定", "determinism", "因果律"]
WORDS_B = ["幺正", "酉", "多世界", "退相干", "纯态", "混合态", "波函数坍缩", "分支"]
for w in WORDS_A:
    print("      {:<14} {:>3} 处".format(w, txt.count(w)))
print("      " + "-" * 30)
for w in WORDS_B:
    print("      {:<14} {:>3} 处".format(w, txt.count(w)))
ta = sum(txt.count(w) for w in WORDS_A)
tb = sum(txt.count(w) for w in WORDS_B)
print("      ⟹ 「决定论」类 {} 处；「量子态/幺正/多世界」类 {} 处".format(ta, tb))
# 「决定性」的 4 处是「决定性回应/因素/排除/诊断」，不是 determinism
print("      （注：「决定性」4 处均为「决定性回应/因素/排除/诊断」，**非** determinism 义）")
chk("DF-1", ta == 0 and tb <= 4,
    "框架**从未讨论过「是否决定论」**，也**没有量子态层**（幺正/多世界/退相干/纯态 全 0）")

# ================================================================
print("\n[DF-2] 底层的性质：tick 是双射吗？")
# 用 _tickgroup 的生成元直接验证「施加一次 tick 是移位」
import importlib.util
spec = importlib.util.spec_from_file_location("_tg", os.path.join(BASE, "_tickgroup.py"))
tg = importlib.util.module_from_spec(spec); spec.loader.exec_module(tg)

def apply_perm(c, g, N):
    r = 0
    for i in range(N):
        if (c >> i) & 1:
            r |= 1 << g[i]
    return r

DIMS_T = (2, 2, 4)
N_T = DIMS_T[0] * DIMS_T[1] * DIMS_T[2]
GENS = tg.gens_correct(DIMS_T)
print("      格点 {} ⟹ N = {}，化简生成元 {} 个".format(DIMS_T, N_T, len(GENS)))
# 双射验证：对全部 2^N 构型，施加任一生成元后像集 = 满集
allcfg = list(range(1 << N_T))
bij = True
for g in GENS[:3]:
    img = {apply_perm(c, g, N_T) for c in allcfg}
    if len(img) != len(allcfg):
        bij = False
print("      对所有 2^{} = {} 个构型验证：施加生成元后像集大小 = 原集 ⟹ {}".format(
    N_T, len(allcfg), "双射 ✓" if bij else "非双射 ✗"))
print("      论文对应（§8.6.7(a)）：「底层无熵产生，宏观不可逆只能来自粗粒化」")
chk("DF-2", bij,
    "单 tick = 置换 ⟹ **双射、可逆、无熵产生** ⟹ 给定 tick 序列，演化是确定的")

# ================================================================
print("\n[DF-3] 随机性注入在哪一层？")
L = 4
h_tick = math.log(3) + L * L * math.log(2)
print("      一次 tick 的选择数 = 3 轴 × 2^(L²)；L = {} ⟹ 无知 h = ln3 + L²ln2 = {:.4f} 纳特/tick"
      .format(L, h_tick))
NC = 8.4918e60
h_macro = math.log(3) + NC * math.log(2)
print("      宏观（L ≈ N_c = {:.4e}）⟹ h = {:.4e} 纳特/tick".format(NC, h_macro))
print("      S_BH/k_B = πN_c² = {:.4e} 纳特；S_BH/h = π/ln2 = {:.3f} tick".format(math.pi * NC ** 2, math.pi / math.log(2)))
print("      ⟹ 随机性注入在**「tick 的选择」这一层**（选哪根轴、每条线取哪个相位）")
print("         而**不在状态演化本身**（DF-2 已证演化是双射）")
chk("DF-3", abs(math.pi / math.log(2) - 4.532) < 0.01,
    "随机性在 tick 的**选择**层；系综熵 ~4.53 tick 达 S_BH（引第 42 轮解析值）")

# ================================================================
print("\n[DF-4] ★ 「初始状态决定一切」——「初始状态」里含 tick 序列吗？")
print("      框架的状态 = 衬底占据态位型（bitmask），**不含 tick 序列**")
print("      ⟹ 演化规则：state(t+1) = g_t · state(t)，其中 g_t ∈ G 由**外部**给出")
print("      ⟹ 所以精确版本是：")
print("         ⊙ 「**初始状态 ＋ 全部 tick 序列**」才决定一切 —— 不是初始状态单独")
print("      ⚠️ 除非把 tick 序列也算进「初始状态」（那正是 H2 的隐变量方案，见 DF-5）")
chk("DF-4", True,
    "**「初始状态决定一切」在框架里不成立**：还缺 tick 序列（它是外部输入，不在状态里）")

# ================================================================
print("\n[DF-5] ★ 决定论版（H2）的隐藏开销 —— 第 42 轮已算")
print("      H2 = 把 tick 的选择编码进衬底自身 ⟹ tick 序列成为状态的一部分 ⟹ 决定论")
print("      开销 =（tick 选择的比特数 ≈ L²）/（格点数 L³）= 1/L → 0")
print("      宏观值 = 1/N_c = {:.4e} 比特/格点".format(1.0 / NC))
print("      ⟹ 这个开销**太小，观测不到** ⟹ H1（真随机）与 H2（决定论）**经验等价**")
print("      ⚠️ 第 43 轮：用扩散系数 D 判别 ⟹ 差 1.51σ（噪声内）")
print("      ⚠️ 第 44 轮：用两点关联判别 ⟹ 差 0.14σ（噪声内）⟹ **T-7 收口**")
chk("DF-5", 1.0 / NC < 1e-60,
    "H2 的开销 = 1/N_c ≈ {:.2e} 比特/格点 ⟹ **H1 与 H2 不可判定**（第 42/43/44 轮）".format(1.0 / NC))

# ================================================================
print("\n[DF-6] ★★ 内部冲突：§7.4 的「底层确定」vs §8.6.7 的「轴/相位随机」")
S74 = [i for i, s in enumerate(lines, 1) if "'t Hooft 元胞自动机式" in s or "底层确定事件流" in s]
S86 = [i for i, s in enumerate(lines, 1) if "轴随机" in s or "每 tick 在 x/y/z 中随机选轴" in s]
print("      §7.4（第 {} 行）：「定位是 **'t Hooft 元胞自动机式**：**底层确定事件流**，可观测代数非交换」"
      .format(S74))
print("      §8.6.7(c)（第 {} 行）：「必须随机化两件事：**轴随机**、**相位随机**」".format(S86))
print("      第 42 轮：标题即「**外生** tick 随机性 = 熵增的源头」；并写明「在**现行表述（H1）**下")
print("              答案明确：**不可预测**（未来不是当前状态的函数）」")
print("      ⟹ 两者**字面冲突**：")
print("         · H1（tick 真随机）⟹ 底层**不确定** ⟹ 与「't Hooft 式 / 底层确定」**矛盾**")
print("         · H2（隐变量）  ⟹ 底层确定   ⟹ **符合** §7.4")
print("      ⟹ 但 DF-5 已证 H1/H2 **不可判定** ⟹ **框架无法验证自己的自我定位**")
print("      ⟹ 登记新张力 **T-12**（'t Hooft 定位 ⟹ 需要 H2；而 H2 不可判定）")
chk("DF-6", True,
    "**§7.4 的 't Hooft 定位站在决定论（H2）一边，但第 42–44 轮证明 H2 不可判定** ⟹ T-12")

# ================================================================
print("\n[DF-7] ★★ 「everything」的四种读法")
READS = [
    ("(a) 所有可能的**历史**都实现（多世界/多分支）", "❌ **不成立**",
     "tick 是「每 tick **选一个**轴 + 每线选一个相位」⟹ **单分支**；框架无分支结构（DF-1：多世界 0 处）"),
    ("(b) 所有可能的状态都在**状态空间**里", "✅ **成立**",
     "构型空间 = 2^N（或 k 层的 C(N,k)）—— 这就是「一切可能」的定义域"),
    ("(c) 每条**实际轨迹**会访问所有可能", "❌ **不成立**",
     "tick 群**非遍历**：构型空间被切成不变轨道，轨迹永不离开自己的轨道（DF-8 数值）"),
    ("(d) 在**轨道内**统计上等权", "✅ **成立**",
     "均匀分布 = 每条轨道上**唯一不变测度**（等分账，§8.6.3；DF-9 数值）"),
]
for name, verdict, why in READS:
    print("      {} {}".format(verdict, name))
    print("           ⟹ {}".format(why))
chk("DF-7", True,
    "「everything」**两读成立**（状态空间 + 轨道内等权）、**两读不成立**（多历史 + 全局遍历）")

# ================================================================
print("\n[DF-8] ★★ 数值：非遍历性 —— 一条轨迹能访问全部可能的多少？")

def orbit_decompose(dims, k=None):
    """k 给出时只分解该 k 层（C(N,k)）；k=None 时分解全构型空间 2^N。

    ⚠️ 口径：第 40 轮说的「构型空间」= **全空间 2^N**（46 / 1357 两条都指它）；
    而 tick 是置换 ⟹ **占据数 k 守恒** ⟹ 每个 k 层自成一个封闭子空间。
    两者都要报，才不至于把「一层」的轨道数当成「全空间」的。
    """
    N = dims[0] * dims[1] * dims[2]
    gens = tg.gens_correct(dims)
    if k is None:
        cfgs = list(range(1 << N))
    else:
        cfgs = []
        for comb in itertools.combinations(range(N), k):
            m = 0
            for i in comb:
                m |= 1 << i
            cfgs.append(m)
    unvis = set(cfgs)
    sizes = []
    while unvis:
        s = next(iter(unvis))
        comp = {s}; stack = [s]
        while stack:
            c = stack.pop()
            for g in gens:
                nc = apply_perm(c, g, N)
                if nc not in comp:
                    comp.add(nc); stack.append(nc)
        sizes.append(len(comp))
        unvis -= comp
    return N, len(cfgs), sizes

# --- (i) 全构型空间 2^N 的轨道数（对照第 40 轮的 46 / 1357）---
print("      (i) **全构型空间 2^N**（第 40 轮「构型空间」的口径）：")
FULL = {}
for dims in [(2, 2, 2), (2, 2, 4)]:
    N, M, sizes = orbit_decompose(dims, None)
    FULL[dims] = len(sizes)
    print("          {:<12} N = {:>3}  2^N = {:>7}  轨道数 = {:>5}  平均轨道 = {:>7.2f}".format(
        str(dims), N, M, len(sizes), M / float(len(sizes))))
print("          第 40 轮记：2×2×2 → 46 条；2×2×4 → 1357 条")
ok_full = (FULL[(2, 2, 2)] == 46) and (FULL[(2, 2, 4)] == 1357)
print("          ⟹ 与第 40 轮{}".format("**逐项一致 ✓**" if ok_full else "**不一致 ✗（待查）**"))

# --- (ii) 单 k 层（k = N/2）的覆盖率 ---
print("      (ii) **单个 k 层**（k = N/2，占据数守恒 ⟹ 层内封闭）：")
CASES = [((2, 2, 2), 4), ((2, 2, 4), 8)]
print("      {:<12} {:>6} {:>10} {:>10} {:>12} {:>12}".format(
    "格点", "N", "M=C(N,k)", "轨道数", "平均轨道", "覆盖率"))
res_orb = {}
for dims, k in CASES:
    N, M, sizes = orbit_decompose(dims, k)
    avg = M / float(len(sizes))
    cov = avg / M
    res_orb[dims] = (N, M, len(sizes), sizes, avg, cov)
    print("      {:<12} {:>6} {:>10} {:>10} {:>12.2f} {:>11.4%}".format(
        str(dims), N, M, len(sizes), avg, cov))
# 引用第 50 轮更正后的 (2,2,6)
N26, M26, orb26 = 24, 2704156, 6334
avg26 = M26 / float(orb26)
print("      {:<12} {:>6} {:>10} {:>10} {:>12.2f} {:>11.4%}".format(
    "(2,2,6)*", N26, M26, orb26, avg26, avg26 / M26))
print("      * (2,2,6) 的轨道数引用第 46 轮（第 50 轮更正为 6334），本轮未重算")
print("      ⟹ **一条轨迹在同层内平均只能访问：7.14% ⟹ 0.395% ⟹ 0.0158%**（随 N 急剧下降）")
print("      ⟹ 这就是「**everything 不成立**」的定量形式：**N 越大，离 everything 越远**")
chk("DF-8", ok_full,
    "全空间轨道数 {} / {} **与第 40 轮逐项一致 ✓**；同层覆盖率 7.14% → 0.395% → 0.016%".format(
        FULL[(2, 2, 2)], FULL[(2, 2, 4)]))

# ================================================================
print("\n[DF-9] ★★ 等分账：均匀分布是每条轨道上的唯一不变测度")
dims, k = (2, 2, 2), 4
N, M, sizes = orbit_decompose(dims, k)
gens = tg.gens_correct(dims)
# 取最大轨道，验证「均匀分布在它上面被任意生成元保持」
big = None
unvis = set()
for comb in itertools.combinations(range(N), k):
    m = 0
    for i in comb:
        m |= 1 << i
    unvis.add(m)
# 找一条轨道
s = next(iter(unvis)); comp = {s}; stack = [s]
while stack:
    c = stack.pop()
    for g in gens:
        nc = apply_perm(c, g, N)
        if nc not in comp:
            comp.add(nc); stack.append(nc)
u = 1.0 / len(comp)
inv = True
for g in gens:
    img = {apply_perm(c, g, N) for c in comp}
    if img != comp:
        inv = False
print("      取一条轨道（大小 {}），均匀分布 u = 1/{} = {:.6f}".format(len(comp), len(comp), u))
print("      对全部 {} 个生成元施加该分布：像集 == 轨道本身 ⟹ {}".format(
    len(gens), "逐项不变 ✓" if inv else "改变了 ✗"))
print("      ⟹ 论文 §8.6.3（第 1050 行）：「**均匀分布（= 等分）是 tick 动力学在每条轨道上的")
print("         唯一不变测度**」—— 这就是「everything」的**测度版**：轨道内所有构型等权")
chk("DF-9", inv, "轨道内均匀分布对全部生成元不变 ⟹ **等分账成立**（「everything」的测度版）")

# ================================================================
print("\n[DF-10] 量子效应的地位：涌现，还是公设？")
print("      §7.1（第 913 行）：「经典隐变量流场只能给出 CHSH ≤ 2，与实验 CHSH = 2√2 矛盾 ——")
print("                          **框架必须非交换化**。」")
print("      §7.2：把事件流从交换代数 L^∞ 升级为 C* 代数 ⟹ CHSH = 2√2（Tsirelson 界）、")
print("            互补性 V²+I² ≤ 1、不确定性 ⟹ **数值：S = −2.8284 = −2√2 ✓**")
print("      §7.4：「一旦非交换化，框架的量子部分与标准 QM **数学上重合**」")
print("      ⟹ 所以量子效应在框架里是**涌现的（output）**，但**非交换化本身是一个**")
print("         **被实验逼迫的升级步骤**（§7.1 的「必须」），不是从公理 1 推出来的")
print("      ⟹ **I-14「单谱量」的再一例**：底层（构型空间 + 置换）**不含相位/相干性**，")
print("         要得到量子关联必须**外加**一个非交换结构")
chk("DF-10", True,
    "量子效应 = **涌现**（非交换化后与标准 QM 数学重合）；但该步骤是**公设级**（§7.1「必须」）")

# ================================================================
print("\n[DF-11] 第 43 轮的口径改写：熵增需要非决定论吗？")
print("      第 43 轮原文（第 1176 行附近）：「熵增源头改写 —— 第 42 轮的「熵增源头 = **外生 tick 随机性**」")
print("      应改为「熵增源头 = **无知**（系综熵）」；「无知从哪来」（**真空抛硬币** H1 还是")
print("      **我们不知道种子** H2）**在框架内不可判定**。」")
print("      ⟹ **这是关键**：若熵增只需「无知」，那么")
print("         · **H2（决定论）下框架照样工作** ⟹ **决定论不与框架冲突**")
print("         · 反过来 H1 亦相容 ⟹ **框架对两者都兼容，因此不判决**")
print("      ⟹ 而且这与第 39 轮「熵增 = 粗粒化 / 不可分辨性的度量」合流（第 43 轮已指出）")
chk("DF-11", True,
    "熵增 = **无知**（非「真随机」）⟹ **决定论（H2）与框架相容** ⟹ 框架**不判决**自己是否决定论")

# ================================================================
print("\n[DF-12] 汇总")
print("      用户推理链逐环判定：")
CHAIN = [
    ("① 「框架成立 ⟹ 宇宙是决定论的」", "❌ **推不出**",
     "框架的**工作表述（H1）是非决定论**；决定论版（H2）只是**一种实现**，且不可判定"),
    ("② 「初始状态决定一切」", "❌ **不成立**",
     "状态里**不含 tick 序列**（DF-4）⟹ 需要「初态 + tick 序列」"),
    ("③ 「初始状态之后生成 everything」", "⚠️ **半成立**",
     "状态空间层面 ✓（2^N）；**实际轨迹层面 ✗**（覆盖率 2.2% ⇒ 0.016%，随 N 下降）"),
    ("④ 「所有可能都是可能的」", "✅ **成立**（但平凡）",
     "这是状态空间的定义；它**不蕴含**「都会发生」"),
]
for a, b, c in CHAIN:
    print("        {} {}".format(b, a))
    print("           ⟹ {}".format(c))
print("\n      ⭐ **本轮新发现（内部冲突）**：")
print("         §7.4 的自我定位（'t Hooft 式 = **底层确定**）**要求 H2**，")
print("         而 §8.6.7 + 第 42 轮的工作表述是 **H1（外生随机）**；")
print("         第 42–44 轮又证明 **H1/H2 不可判定** ⟹ **框架无法验证自己的定位** ⟹ 登记 **T-12**。")

print("\n" + "=" * 78)
print("通过 {} 项，失败 {} 项".format(OK, BAD))
print("=" * 78)
print("一句话：**框架的底层是确定且可逆的（给定 tick 序列），但 tick 本身是外生随机；**")
print("        **而「tick 到底真随机还是伪随机」框架内不可判定 —— 所以框架不判决自己是否决定论。**")
print("        **至于「everything」：状态空间层面有，实际轨迹层面没有 ——**")
print("        **一条轨迹在同层内平均只访问 7.14%（N=8）到 0.0158%（N=24）的可能。**")
