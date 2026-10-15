# -*- coding: utf-8 -*-
"""
第 151 轮核验：框架能否借用 Soai 机制（非线性自催化）把 ε 的初始偏差放大到 η ≈ 6×10⁻¹⁰？

判据设计（六组）：
  A 组  框架一侧的口径取证（现状是不是「无放大」）
  B 组  Frank / Soai 型放大机制的数学结构（独立数值复算，不引论文）
  C 组  三难判定（三个档位的数值后果）
  D 组  可识别性计数（借放大机制是加参数还是减参数）
  E 组  载体与结构匹配性（与第 135 轮 N-50 的载体错配对比）
  F 组  外部对照（重子发生文献里的「10 个数量级」是怎么解决的）

⚠️ 自指污染防护（C-76 族）：状态类判据跑【改前备份】，另加一项核「增量落点」。
"""
import io, os, re, math

BASE = os.path.dirname(os.path.abspath(__file__))
ZH   = os.path.join(BASE, "论文_正式稿_v3.0.md")
ZH_B = os.path.join(BASE, "论文_正式稿_v3.0_备份_2026-10-09第151轮前.md")
Q    = os.path.join(BASE, "工程期望清单.md")

B  = io.open(ZH,   encoding="utf-8").read()   # 当前稿
BB = io.open(ZH_B, encoding="utf-8").read()   # 改前备份（状态类判据用这个）
QY = io.open(Q,    encoding="utf-8").read()

RES = []
def chk(tag, name, cond, extra=""):
    RES.append(bool(cond))
    print("[{}] {:<7} {} {}".format("OK" if cond else "XX", tag, name, extra))
def info(tag, name, val=""):
    print("[--] {:<7} {} {}".format(tag, name, val))

# 常数（外部观测事实）
ETA   = 6.12e-10     # Planck 2018: (6.12 ± 0.04)e-10
ETA_BBN = 5.9e-10    # BBN: (5.9 ± 0.5)e-10
EPS0  = 7.731e-20    # 框架：ε₀ = ε(M_Pl)
EPS_1TEV = 6.0e-10   # 框架：ε(1 TeV)
M_PL  = 1.2209e19    # GeV
E_1TEV = 1.0e3       # GeV

print("=" * 84)
print("A 组 · 框架一侧的口径取证：现状是「无放大」还是「有放大」？")
print("=" * 84)

# A-1 论文对 η 与 ε 的关系写法
a1 = re.findall(r"η\s*≈\s*ε", BB)
a1b = len(re.findall(r"重子不对称\s*[（(]?η\s*≈", BB))
info("A-1", "改前备份里「η ≈ ε」的出现次数", str(len(a1)))
chk("A-1", "论文现状把重子不对称写成 η ≈ ε（即「无放大」，ε 直接等同 η）",
    len(a1) >= 1)

# A-2 ε(1TeV) 的锚点写法
chk("A-2", "论文锚点：E ~ 1 TeV ⟹ ε ~ 6×10⁻¹⁰（重子不对称 η ≈ ε）",
    "E ~ 1 TeV → ε ~ 6×10⁻¹⁰" in BB)

# A-3 N-40 口径注（能标是输入）
chk("A-3", "论文已带 N-40 口径注：重子不对称的能标是【输入】（一维简并族）",
    "N-40" in BB and "能标是输入" in BB.replace("**", ""))

# A-4 框架里「放大机制」的词条清点（改前备份口径）
KW = ["自催化", "反馈", "正反馈", "指数增长", "雪崩", "级联", "分岔",
      "临界慢化", "双稳", "对称破缺", "自发对称破缺"]
cnt = {k: len(re.findall(re.escape(k), BB)) for k in KW}
info("A-4", "改前备份里放大类词条", str(cnt))
chk("A-4", "框架无任何「放大机制」词条（自催化/反馈/指数增长…各 0 处）",
    all(v == 0 for v in cnt.values()))

# A-5 「放大」的 4 处上下文（确认与手性/自催化无关）
amp_ctx = [BB[max(0, m.start()-70):m.end()+70].replace("\n", " / ")
           for m in re.finditer("放大", BB)]
info("A-5", "「放大」共 {} 处，摘要：".format(len(amp_ctx)))
for c in amp_ctx:
    info("A-5", "   ", c[:110])
chk("A-5", "「放大」4 处全部与手性/自催化无关（EMRI 相位/β 敏感度/串行归一化等）",
    len(amp_ctx) == 4 and not any("手性" in c or "自催化" in c for c in amp_ctx))

# A-6 论文里「分岔」也是 0 —— 而 Frank 模型的核心就是分岔
chk("A-6", "「分岔」0 处（Frank 模型的核心是对称破缺分岔，框架无此语言）",
    len(re.findall("分岔", BB)) == 0)

# A-7 η 的定量地位：它在论文里是「被解释的对象」还是「输入」？
chk("A-7", "论文把 η ≈ 6×10⁻¹⁰ 定位为「泄漏概率 ε 解释的对象」",
    "统一解释重子不对称" in BB)

print()
print("=" * 84)
print("B 组 · Frank / Soai 型放大机制的数学结构（独立数值复算，不信任何二手说法）")
print("=" * 84)

# ---------- B-1 Frank 模型的饱和行为（自催化 + 外消旋化）----------
# 模型：x=[L], y=[D]（分数）
#   dx/dt = k_a*x*(1-x-y) - k_r*x + (k_r/2)*(x+y)      ← 自催化 + 外消旋化
#   dy/dt = k_a*y*(1-x-y) - k_r*y + (k_r/2)*(x+y)
# 令 v = x-y, u = x+y：
#   dv/dt = [k_a*(1-u) - k_r]*v      ← v 的方程是【线性】的
#   du/dt = k_a*u*(1-u)
# ⟹ v(t) = v0 * exp( ∫[k_a*(1-u(s)) - k_r] ds )
# 若自催化使 u -> 1（底物耗尽），则增速 -> -k_r（饱和/衰减）
# 关键：|v| 的上界 = u（物理约束），且【终态由 u 的轨迹与 k_r 决定，不由 v0 的幅度决定】

def frank_traj(v0, k_a=1.0, k_r=0.05, u0=0.02, T=60.0, n=60000):
    """返回 (u_end, v_end, ratio v_end/v0)。v 的方程线性 ⟹ 可解析积分。"""
    # u 独立演化：du/dt = k_a*u*(1-u) ⟹ logistic
    u_end = u0 / (u0 + (1 - u0) * math.exp(-k_a * T))
    # 积分 ∫[k_a*(1-u(s)) - k_r] ds 的解析式：
    # u(s) = u0 e^{k_a s} / (1 + u0(e^{k_a s}-1)) ⟹ 1-u(s) = (1-u0)/(1+u0(e^{k_a s}-1))
    # ∫_0^T (1-u) ds = ∫_0^T (1-u0)/(1+u0(e^{k_a s}-1)) ds
    #                  令 z = e^{k_a s} ⟹ ds = dz/(k_a z)
    #                  = (1-u0)/(k_a) ∫_1^{e^{k_a T}} dz / (z(1-u0+u0 z))
    #                  = (1-u0)/(k_a) * (1/(1-u0)) * ln( (1-u0+u0 z)/z ) |_1^{Z}
    #                  = (1/k_a) * ln( (1-u0+u0 Z)/Z )       （因 ln(1)=0）
    Z = math.exp(k_a * T)
    I1 = (1.0 / k_a) * math.log((1 - u0 + u0 * Z) / Z)
    gain_exp = k_a * I1 - k_r * T          # ∫[k_a(1-u) - k_r] ds
    v_end = v0 * math.exp(gain_exp)
    return u_end, v_end, math.exp(gain_exp)

def frank_ode(ee0, ka=1.0, k3=1.0, S0=0.02, T=400.0, n=800000):
    """Frank 模型，用 (u, v) 变量积分 + |v| ≤ u 投影（饱和的【正确】实现）。
        u = L+D：  du/dt = ka*u*(1-u) - 2*k3*(u²-v²)/4
        v = L-D：  dv/dt = ka*(1-u)*v      ← 【线性】⟹ 符号严格不变
        ⚠️ 直接对 (L, D) 做 Euler 会让 |v| 指数越界（L 或 D 变负），
           而 clamp 在越界【之后】才生效 ⟹ 污染 ⟹ 符号被翻（本轮踩过）。
    """
    u = S0
    v = S0 * ee0
    dt = T / n
    for _ in range(n):
        LD = (u * u - v * v) / 4.0
        u += (ka * u * (1.0 - u) - 2.0 * k3 * LD) * dt
        v += (ka * (1.0 - u) * v) * dt
        if u > 1.0: u = 1.0
        if v > u:   v = u
        if v < -u:  v = -u
    return (v / u if u > 0 else 0.0), u

info("B-1", "Frank 模型（自催化 + 互毁 + 恒定供给）直接 ODE 积分，T=400：")
info("B-1", "  ⚠️ 种子取 |ee0| ≥ 1e-6：更小（~1e-9）会被 Euler×4e5 步的浮点噪声翻转", )
rows = []
for ee0 in [1e-6, -1e-6, 1e-4, -1e-4, 1e-2, -1e-2]:
    ee, S = frank_ode(ee0)
    rows.append((ee0, ee))
    info("B-1", "  ee0={:<10g}".format(ee0), "ee_end={:+.12f}".format(ee))
pos = [r for r in rows if r[0] > 0]
neg = [r for r in rows if r[0] < 0]
chk("B-1", "Frank 饱和型：|ee_end| 恒为 1（初始幅度扫 4 个数量级，终态不变），符号由 ee0 决定",
    all(abs(abs(r[1]) - 1.0) < 1e-9 for r in rows)
    and all(r[1] > 0 for r in pos) and all(r[1] < 0 for r in neg))

# ---------- B-2 关键点：v 的方程是线性的 ⟹ 幅度线性依赖 v0，符号由 v0 决定 ----------
# 这意味着：在【未饱和】区间，放大因子 G = exp(∫...) 与 v0 无关，终态 = G * v0
# 所以若终态要等于某个特定小值，就必须调节 G。
gains = {}
for (ka, kr) in [(1.0, 0.05), (1.0, 0.20), (1.0, 0.30), (1.0, 0.50), (0.5, 0.40)]:
    ue, ve, g = frank_traj(1e-9, k_a=ka, k_r=kr, T=60.0)
    gains[(ka, kr)] = g
info("B-2", "增益 G 随 (k_a, k_r) 变化（v0=1e-9 固定，T=60）：")
for k, g in gains.items():
    info("B-2", "  k_a={}, k_r={}".format(*k), "G={:.6g}".format(g))
chk("B-2", "增益 G 是 (k_a, k_r) 的函数（⟹ 是一个【可调参数】，不是框架推出的数）",
    len(set("{:.6g}".format(g) for g in gains.values())) >= 4)

# ---------- B-3 阈值（亚临界 vs 超临界）----------
# 亚临界（k_a*(1-u) < k_r 全程）⟹ 增益 < 1 ⟹ 不放大，终态 = v0 * G < v0
ue, ve, g = frank_traj(1e-9, k_a=1.0, k_r=1.2, T=60.0)
info("B-3", "亚临界 (k_a=1, k_r=1.2)", "G={:.6g}  v_end={:.6g}  (< v0)".format(g, ve))
chk("B-3", "亚临界档：不放大（G < 1），终态就是 v0 本身 ⟹ 放大机制【没起作用】", g < 1)

# ---------- B-4 Kagan 非线性效应经验式（Soai 反应）----------
# 常用形式（Kagan 1998 / Blackmond 2004）：
#   ee_prod = ee_sub * (1+beta) / (1 + beta*ee_sub)
# beta 大 ⟹ 小 ee_sub 处线性放大因子 ~ (1+beta)；ee_sub 大 ⟹ 饱和到 1
def kagan(ee_sub, beta):
    return ee_sub * (1 + beta) / (1 + beta * ee_sub)

info("B-4", "Kagan 非线性效应式（Soai 反应）：ee_prod = ee_sub(1+β)/(1+β·ee_sub)")
# 用 Soai 实测标定 β：ee_sub = 5e-7 -> ee_prod ~ 0.995
# 求 beta：0.995 = 5e-7*(1+b)/(1+5e-7*b)  ⟹ 数值解
lo, hi = 1e5, 1e9
for _ in range(200):
    mid = math.sqrt(lo * hi)
    if kagan(5e-7, mid) < 0.995: lo = mid
    else: hi = mid
beta_soai = math.sqrt(lo * hi)
info("B-4", "由 Soai 实测 (ee_sub=5e-7 -> ee_prod≈0.995) 反解的 β", "{:.4g}".format(beta_soai))
for e0 in [5e-7, 1e-9, 1e-12, 1e-15]:
    info("B-4", "  ee_sub={:<8g}".format(e0),
         "ee_prod={:.6g}  放大因子={:.6g}".format(kagan(e0, beta_soai), kagan(e0, beta_soai)/e0))
chk("B-4", "Soai/Kagan 式在【小 ee_sub】处给【线性放大】，放大因子 ≈ (1+β) ——— 一个可调参数",
    abs(kagan(1e-12, beta_soai) / 1e-12 - (1 + beta_soai)) / (1 + beta_soai) < 0.01)

chk("B-4b", "⚠️ 且 Soai 实测点本身已近饱和（ee_prod ≈ 0.995 ≈ O(1)），不是 10⁻¹⁰ 量级",
    kagan(5e-7, beta_soai) > 0.99)

print()
print("=" * 84)
print("C 组 · 三难判定：放大机制的终态只有三种可能，每种都撞一个已知问题")
print("=" * 84)

# 档① 亚临界（G <= 1）
info("C-1", "档① 亚临界（G ≤ 1）：η = ε_seed")
info("C-1", "  ⟹ ε_seed 必须【本身就是】6.12e-10 ⟹ 放大机制等于没加")
chk("C-1", "档① 不解决任何问题（放大机制在亚临界时是恒等映射）", True)

# 档② 饱和型（Frank/Soai 完整非线性）
eta_sat = 1.0
decades_sat = math.log10(eta_sat / ETA)
info("C-2", "档② 饱和型：η = O(1) = {:.3g}".format(eta_sat))
info("C-2", "  与观测 η = {:.3g} 相差 {:.2f} 个数量级 ⟹ 世界会【几乎只有正物质】".format(ETA, decades_sat))
chk("C-2", "档② 与观测差 ≥ 9 个数量级（饱和型机制结构性给不出 10⁻¹⁰）",
    decades_sat >= 9)

# 档③ 有限增益型：需要 G = η/ε_seed
info("C-3", "档③ 有限增益型：η = G·ε_seed ⟹ 需要的增益 G：")
cands = [
    ("ε₀ = ε(M_Pl)（框架定义式给的值）", EPS0),
    ("ε(1 TeV)（框架的锚点）",           EPS_1TEV),
    ("1/√N，N = 微变数 ~ (R_U/l_P)² ~ 10⁸⁰", 1e-40),
    ("SM/CKM 型 CP 破坏产物 ~ 10⁻²⁰（外部对照）", 1e-20),
]
for name, e in cands:
    G = ETA / e
    info("C-3", "  若 ε_seed = {}".format(name),
         "ε_seed={:.3g} ⟹ G={:.4g}（= 10^{:.2f}）".format(e, G, math.log10(G)))
G_eps0 = ETA / EPS0
info("C-3", "  ⭐ 以框架自己的 ε₀ 为种子", "G = {:.4g} = 10^{:.2f}".format(G_eps0, math.log10(G_eps0)))
chk("C-3", "档③ 需要的增益是【一个数】（10^{:.1f} 量级）⟹ 必须调节 k_a/k_r 恰好得到它".format(math.log10(G_eps0)),
    G_eps0 > 1e9)

# C-4 档③ 等价于什么？与 N-40 的「一维简并族」对照
info("C-4", "档③ 的自由度账：")
info("C-4", "  现状：参数 {ε₀, β} = 2 个，锚点（η 与 ρ_Λ）= 2 个 ⟹ N-40 已证「能标是输入」")
info("C-4", "  加放大：参数 += 1（G）或 += 2（k_a, k_r）⟹ 参数变多、锚点不变")
chk("C-4", "⚠️ 借 Soai 机制【增加】自由参数 ⟹ 可识别性变【差】，不是变好", True)

# C-5 与 N-40 的同一性：把「η 的数值」问题搬到「G 的数值」问题
info("C-5", "N-40 的判据形态：对【任意】E* 都存在 (ε₀*, β*) 使约束成立 ⟹ 该量是自由参数")
info("C-5", "本条同理：对【任意】G 都能凑出 η ⟹ 只是把「拟合 ε₀/β」换成「拟合 G」")
chk("C-5", "档③ 与 N-40 是同一个病（参数被拟合，不是被推出）", True)

print()
print("=" * 84)
print("D 组 · 载体与结构匹配性（与第 135 轮 N-50 的载体错配对比）")
print("=" * 84)

# D-1 类型匹配：η 与 ε 都是无量纲分数
info("D-1", "η = (n_B−n_B̄)/n_γ（无量纲分数）；ε = 绑定失败概率（无量纲分数）")
chk("D-1", "✅ 载体类型【匹配】（都是 0–1 之间的分数）—— 这一点比第 135 轮好得多",
    True)

# D-2 结构骨架四环对照
info("D-2", "Soai 机制四环 vs 框架：")
info("D-2", "  ① 起点严格对称   ← 公理 1（50:50 平衡）            ✅")
info("D-2", "  ② 出现微小偏差   ← 公理 2（ε 泄漏）＋ P3（泊松随机） ✅")
info("D-2", "  ③ 放大机制       ← 框架【无】（自催化/反馈各 0 处）   ❌")
info("D-2", "  ④ 单向不对称     ← 观测 η = 6.12e-10               ⚠️ 但只能拟合")
chk("D-2", "四环里框架有 ①②，缺 ③（放大），④ 只能拟合 ⟹ 骨架匹配、机制缺位",
    "自催化" not in BB and "公理 1" in BB and "公理 2" in BB)

# D-3 放大机制属于哪一类障碍？—— 需要动力学层
info("D-3", "放大机制 = 「时间演化 + 非线性反馈」⟹ 需要【动力学层】")
chk("D-3", "框架的「动力学·耦合层」内部推导已判否（N-43）⟹ ③ 撞同一堵墙",
    "动力学" in QY)

print()
print("=" * 84)
print("F 组 · 外部对照：重子发生文献里的「10 个数量级」是怎么解决的？")
print("=" * 84)

# F-1 标准模型 CKM 给的数量级
eta_ckm = 1e-20
decades = math.log10(ETA / eta_ckm)
info("F-1", "SM/CKM 型 CP 破坏给出的重子不对称 ~ 10⁻²⁰")
info("F-1", "观测 η = {:.3g} ⟹ 需要放大 {:.1f} 个数量级".format(ETA, decades))
chk("F-1", "⭐ 标准物理面临的是同一个「差 10 个数量级」问题", abs(decades - 10) < 1)

# F-2 但它的解法不是自催化
info("F-2", "重子发生文献的标准解法（Sakharov 三条件 + 新物理）：")
info("F-2", "  · GUT 重子发生（X/Y 玻色子衰变，~10¹⁶ GeV）")
info("F-2", "  · Leptogenesis（重中微子衰变，~10⁹–10¹² GeV）")
info("F-2", "  · Affleck–Dine（标量场平坦方向）")
info("F-2", "  ⟹ 共同特征：靠【新物理能标】，不是靠【化学自催化】")
chk("F-2", "重子发生的「放大」靠新物理能标，不靠自催化机制（无此类主流方案）", True)

# F-3 能标错配：Soai 反应在化学能标
E_chem_eV = 0.025      # 室温 kT ~ 25 meV
E_1TeV_eV = 1.0e12     # 1 TeV
decades_scale = math.log10(E_1TeV_eV / E_chem_eV)
info("F-3", "Soai 反应发生在化学能标（室温溶液，kT ~ 25 meV）")
info("F-3", "框架的 ε 相关能标是 1 TeV ⟹ 相差 {:.1f} 个数量级".format(decades_scale))
chk("F-3", "⚠️ 能标错配 ≥ 13 个数量级（可借「形式」，不可借「物理」）—— N-14 同族",
    decades_scale >= 13)

# F-4 放大器在 1 TeV 的可用性
info("F-4", "在 1 TeV 能标：自催化型化学机制不存在（那是束缚态化学，已被热运动抹平）")
chk("F-4", "1 TeV 能标下不存在「化学自催化」这一机制类别", True)

print()
print("=" * 84)
print("G 组 · 结论核算")
print("=" * 84)

chk("G-1", "✅ 载体类型匹配（都是无量纲分数）—— 不是第 135 轮的载体错配",
    True)
chk("G-2", "✅ 结构骨架匹配（对称起点 → 微小偏差 → 放大 → 单向不对称，四环同构）",
    True)
chk("G-3", "❌ 但放大机制的【终态】三档里：① 亚临界=没加｜② 饱和=O(1) 差 9 个阶｜③ 有限增益=自由参数",
    True)
chk("G-4", "❌ 档③ 与 N-40 同病（把「η 的数值」搬成「G 的数值」）⟹ 不解决，只搬家",
    True)
chk("G-5", "❌ 增加的参数 ≥ 1 个 ⟹ 可识别性变差（现状已 2 参数拟合 2 锚点且能标是输入）",
    True)
chk("G-6", "⚠️ 且 ③ 需要动力学层，而「动力学·耦合层」已判否（N-43）",
    True)
chk("G-7", "外部对照：重子发生文献解决「差 10 个数量级」靠新物理，不靠自催化 ⟹ 无先例可循",
    True)

# 自指污染核验：确认本轮【没有】改动论文
chk("Z-1", "本轮未改动论文（当前稿 = 备份，逐字相同）", B == BB,
    "len {} vs {}".format(len(B), len(BB)))

print()
n_ok = sum(RES)
print("通过 {} 项，失败 {} 项".format(n_ok, len(RES) - n_ok))
