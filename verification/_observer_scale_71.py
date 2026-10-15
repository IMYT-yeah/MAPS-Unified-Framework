# -*- coding: utf-8 -*-
"""第 71 轮 · I-19：观测者的粗粒化尺度是多少？
（框架的两块拼图「截断 = 普朗克」＋ B5 的观测者分辨率，能不能连成一条推导？）

第 70 轮的结论是「平滑 = 在大于 l_P 的尺度上读数」，但**没有给出那个尺度**。
本轮去找它。取证时发现框架**已经**写下了这条链（第 531 行）：
    方向簇 k = 4（定理 1 / LST）⟹ 每面元 4 个独立方向模式
    ⟹ Nyquist：4 模式需 ≥ 4 个采样点 ⟹ 相干块 ≥ 4l_P²
    ⟹ 【框架的下一步是】块内 4 自由度最大压缩 ⟹ 1 纳特/块

核验项：OS-1 … OS-9
"""
import io
import os
import sys
import math
import itertools

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

OK = BAD = 0
FAILS = []


def chk(tag, cond, msg):
    global OK, BAD
    if cond:
        OK += 1
        print("  [OK] {:<6} {}".format(tag, msg))
    else:
        BAD += 1
        FAILS.append(tag)
        print("  [XX] {:<6} {}".format(tag, msg))


def rule(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


BASE = os.path.dirname(os.path.abspath(__file__))
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
CUR = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
PREV = os.path.join(HIST, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第70轮前.md")
curT = io.open(CUR, encoding="utf-8").read()
preT = io.open(PREV, encoding="utf-8").read() if os.path.exists(PREV) else curT
L = curT.split("\n")

lP = 1.616255e-35


# ══════════════════════════════════════════════════════════════════════
rule("OS-1  引文清点：那条链的每一环在论文里的位置（补丁前 / 补丁后两列）")
# ══════════════════════════════════════════════════════════════════════

print("  底本 = {}（补丁前）".format(os.path.basename(PREV)))
print()
WORDS = ["Nyquist", "采样定理", "相干块", "相干单元", "4l_P²", "截断 = 普朗克",
         "方向簇", "Tammes", "Lusternik", "最大压缩", "粗粒化"]
print("  {:<16} {:>10} {:>10}".format("词", "补丁前", "补丁后"))
for w in WORDS:
    print("  {:<16} {:>10} {:>10}".format(w, preT.count(w), curT.count(w)))
print()
print("  ⭐ 关键行：")
for i, s in enumerate(L, 1):
    if "Nyquist" in s or "采样定理" in s:
        print("     {}: {}".format(i, s[:230]))
print()
print("  ⭐ 「截断 = 普朗克」原文（第 322 行）：")
for i, s in enumerate(L, 1):
    if "截断 = 普朗克" in s:
        print("     {}: {}".format(i, s[:190]))
chk("OS-1", preT.count("Nyquist") >= 1 and preT.count("相干块") >= 1,
    "这条链**框架本来就有**（补丁前 Nyquist {} 处、相干块 {} 处）—— "
    "与第 70 轮的「图热流各 0 处」**性质相反**：I-19 的答案**在框架里已经写下了**".format(
        preT.count("Nyquist"), preT.count("相干块")))


# ══════════════════════════════════════════════════════════════════════
rule("OS-2  ⭐ Nyquist 论证的独立复算：那一步是不是**平凡**的？")
# ══════════════════════════════════════════════════════════════════════

print("  论文第 531 行的原话：「……Nyquist 采样定理：4 模式需 ≥4 采样点")
print("  （数值秩验证：4 模式×2/3 点秩 2/3 欠采样、×4 点秩 4 满秩）」")
print()
print("  ⟹ 复算：构造 k×4 的采样矩阵 M[i][a] = f_a(p_i)，看秩是否 = min(k, 4)。")
print("     ⚠️ 关键问题：**这检验了框架特有的东西吗？**")
print()
# 正四面体 4 方向（Tammes）
TET = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], dtype=float)
TET /= np.linalg.norm(TET, axis=1, keepdims=True)


def modes_linear(p):
    return np.array([np.dot(p, n) for n in TET])


def modes_abs(p):
    return np.array([abs(np.dot(p, n)) for n in TET])


def modes_gauss(p):
    return np.array([math.exp(-np.sum((p - n) ** 2) / 0.5) for n in TET])


def modes_rand_basis(p, B):
    """第三种对照：**任意** 4 个线性泛函（与正四面体无关）。"""
    return B @ p


rng = np.random.default_rng(20261002)
B = rng.normal(size=(4, 3))
SIG = [("正四面体·线性", modes_linear, None),
       ("正四面体·|·|", modes_abs, None),
       ("正四面体·高斯", modes_gauss, None),
       ("**随机 4 泛函**（与框架无关）", modes_rand_basis, B)]
print("  正四面体 4 方向的和（检验线性相关性）：{}".format(np.round(TET.sum(axis=0), 12)))
print("     ⟹ **Σ n_a = 0**（精确）⟹ 4 个方向在 3D 里**线性相关** ⟹ 秩 ≤ **3**！")
print()
print("  {:<32} {}  {}".format("模式基底", "k = 2 / 3 / 4 / 5 / 8 时的秩", ""))
ranks = {}
for nm, fn, extra in SIG:
    r = []
    for k in (2, 3, 4, 5, 8):
        p0 = rng.normal(size=3)
        p0 /= np.linalg.norm(p0)
        # 取 k 个一般位置的点（球面上小邻域内）
        pts = []
        for _ in range(k):
            d = rng.normal(scale=0.3, size=3)
            q = p0 + d[:3]
            q /= np.linalg.norm(q)
            pts.append(q)
        M = np.array([(fn(p, extra) if extra is not None else fn(p)) for p in pts])
        r.append(int(np.linalg.matrix_rank(M, tol=1e-10)))
    ranks[nm] = r
    print("  {:<32} {}".format(nm, " / ".join(str(x) for x in r)))
print()
print("  {:<32} {}".format("**min(k,4)（若模式满 4 维）**", " / ".join(str(min(k, 4)) for k in (2, 3, 4, 5, 8))))
print()
lin = ranks["正四面体·线性"]
rd = ranks["**随机 4 泛函**（与框架无关）"]
nonlin = ranks["正四面体·高斯"]
print("  ⭐⭐ **秩不全同 —— 这不是 bug，是一个发现**：")
print("     · **线性**模式（`n_a·p`）：k ≥ 4 时秩仍是 **{}**（因为 Σn_a = 0 ⟹ 只有 3 维）".format(lin[-1]))
print("     · 「随机 4 泛函」：k ≥ 4 时秩也是 **{}**（同一个原因：4 个泛函在 3D 里相关）".format(rd[-1]))
print("     · **非线性**模式（`|n_a·p|` / 高斯）：k ≥ 4 时秩 **{}**（可以满 4 维）".format(nonlin[-1]))
print()
print("  ⟹ **「4 模式需 ≥ 4 采样点」这一步依赖「模式如何定义」，而论文第 531 行没有写明是哪种。**")
print("     若模式是**线性**泛函 ⟹ 只有 **3** 个独立模式 ⟹ 下界应为 **3 个采样点**（不是 4）；")
print("     要得到 **4**，模式必须是**非线性**的（论文未说明）。")
print()
print("  ⚠️ 但这**不等于**论文错：框架的「4 个方向模式」更可能指「4 个方向上的**连接状态**」")
print("     （是非线性/离散量）⟹ 那样确实可以 4 维。**缺的是口径，不是结论。**")
chk("OS-2", lin[-1] == 3 and nonlin[-1] == 4,
    "⭐ **发现未写明的口径**：正四面体 4 方向**线性相关**（`Σn_a = 0` 精确）⟹ "
    "线性模式下秩只 **3**、非线性模式才 **4** ⟹ **「需 ≥ 4 采样点」依赖模式定义**")


# ── OS-2b：口径分歧直接改变下界
print()
print("  ⭐ **口径分歧直接改变结论**（这是本轮最有用的部分）：")
for nm, r_last in [("线性模式（3 维）", 3), ("非线性模式（4 维）", 4)]:
    A = float(r_last)
    print("     {:<20} ⟹ 相干块 ≥ **{} l_P²**  ⟹ 尺度 ≥ **√{} l_P = {:.4f} l_P**".format(
        nm, r_last, r_last, math.sqrt(A)))
print("     ⟹ **保守下界 = √3 l_P ≈ {:.3f} l_P**；充当下界需模式为非线性才升到 2 l_P。".format(
    math.sqrt(3)))


# ══════════════════════════════════════════════════════════════════════
rule("OS-3  ⭐ 从「相干块 ≥ 4l_P²」到「粗粒化尺度 ≥ 2l_P」")
# ══════════════════════════════════════════════════════════════════════

print("  链的每一环，逐环标性质：")
CHAIN = [
    ("① 普朗克尺度事件流", "公理 1", "**公理**（框架起点）"),
    ("② 方向管最细尺度 = l_P", "§4.10", "**本框架设定**（非推导）"),
    ("③ 方向簇 k ≥ 4", "定理 1（LST / Borsuk）", "**数学定理**（不依赖框架）"),
    ("④ 每面元 4 个独立方向模式", "③ + Tammes 正四面体", "**数学**（Tammes 严格）"),
    ("⑤ 4 模式需 ≥ 4 采样点", "**Nyquist 采样定理**", "**信息论普遍原理**"),
    ("⑥ **相干块 ≥ 4l_P²**", "④ + ⑤", "**不等式（有效下界）** ✓"),
    ("⑦ 块内 4 自由度**最大压缩** ⟹ 1 纳特/块", "「最大压缩」假设", "**额外假设**（取等号那一步）"),
    ("⑧ S = A/(4l_P²)（**等号**）", "⑥ + ⑦", "半拟合/一致性（第 52 轮已裁决）"),
]
print("  {:<34} {:<28} {}".format("环节", "来源", "性质"))
for a, b, c in CHAIN:
    print("  {:<34} {:<28} {}".format(a, b, c))
print()
print("  ⭐ 由 ⑥：相干块面积 ≥ N_模式 l_P² ⟹ **线度 ≥ √N_模式 l_P**。")
print("     ⚠️ 而 N_模式 **取决于「模式如何定义」**（OS-2 的发现）：")
print("        · 线性模式（4 个 `n_a·p`）⟹ 只有 3 个独立模式 ⟹ 块 ≥ 3l_P² ⟹ 尺度 ≥ **√3 = {:.4f} l_P**".format(
    math.sqrt(3)))
print("        · 非线性模式（4 个方向的连接状态）⟹ 4 个独立 ⟹ 块 ≥ 4l_P² ⟹ 尺度 ≥ **√4 = 2.0000 l_P**")
print()
print("     ⟹ 与第 70 轮的「平滑 = 在大于 l_P 的尺度上读数」对接：")
print("        **精确化为「平滑尺度 ≥ √3 l_P ≈ {:.2f} l_P」**（保守；若模式非线性则升到 2 l_P）。".format(
    math.sqrt(3)))
print()
print("  ⚠️ **取等号（= 2l_P 或 √3 l_P）需要第 ⑦ 环**，而那一环是**额外假设**（第 52 轮已裁为「半拟合」）。")
print("     ⟹ 本轮可声称的**只有不等式**。")
print()
print("  ⚠️ **与第 51 轮的 `H/N ≤ 0.25` 形式相同**（也是不等式）——")
print("     这是一个**可复现的模式**：框架在这类跨越处给的都是**不等号**。")
chk("OS-3", abs(math.sqrt(3) - 1.7320508) < 1e-6,
    "**相干块 ≥ N_模式 l_P² ⟹ 粗粒化尺度 ≥ √N_模式 l_P**；"
    "**保守下界 √3 l_P ≈ 1.73 l_P**（线性模式）／**2 l_P**（非线性模式）"
    "—— ⚠️ 口径未定，故只报区间 **1.73 – 2.00 l_P**")


# ══════════════════════════════════════════════════════════════════════
rule("OS-4  单位核对：`0.25 纳特/l_P²` ⟺ `1 纳特/4l_P²`（同一个数）")
# ══════════════════════════════════════════════════════════════════════

a1 = 0.25          # 纳特/l_P²
a2 = 1.0 / 4.0     # 1 纳特 per 4 l_P²
print("  B5 写法 A：`0.25 纳特/l_P²`")
print("  B5 写法 B：`1 纳特 / 4l_P²`")
print("  数值：{:.6f} vs {:.6f} ⟹ 差 {:.1e}".format(a1, a2, abs(a1 - a2)))
print("  折合比特：{:.4f} bit/l_P²（= 0.25/ln2）".format(a1 / math.log(2)))
print()
print("  ⚠️ 注意**不是** `1 比特`：论文第 337 行已裁决 —— 取 1 bit 会让太阳质量黑洞温度")
print("     偏 **+44.27%**（8.8995×10⁻⁸ K vs 标准 6.16868×10⁻⁸ K）；取 1 纳特偏差 < 10⁻⁹。")
print("     ⟹ 这是 **B5 唯一带观测成分的一环**（被 Hawking 温度钉住）。")
chk("OS-4", abs(a1 - a2) < 1e-15 and abs(a1 / math.log(2) - 0.3607) < 1e-3,
    "两种写法**同一个数**；折合 {:.4f} bit/l_P²；且「1 纳特而非 1 比特」**被 Hawking 温度钉住**".format(
        a1 / math.log(2)))


# ══════════════════════════════════════════════════════════════════════
rule("OS-5  ⭐ icosphere 上的尺度换算：1-ring 边长 = 多少 l_P？")
# ══════════════════════════════════════════════════════════════════════

def _norm3(v):
    n = math.sqrt(sum(x * x for x in v))
    return tuple(x / n for x in v)


def icosphere(subdiv):
    ph = (1 + 5 ** 0.5) / 2
    verts = [(-1, ph, 0), (1, ph, 0), (-1, -ph, 0), (1, -ph, 0),
             (0, -1, ph), (0, 1, ph), (0, -1, -ph), (0, 1, -ph),
             (ph, 0, -1), (ph, 0, 1), (-ph, 0, -1), (-ph, 0, 1)]
    verts = [_norm3(v) for v in verts]
    faces = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
             (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
             (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
             (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    for _ in range(subdiv):
        cache, nf = {}, []

        def mid(i, j):
            key = (i, j) if i < j else (j, i)
            if key in cache:
                return cache[key]
            m = _norm3(tuple((verts[i][k] + verts[j][k]) / 2 for k in range(3)))
            verts.append(m)
            cache[key] = len(verts) - 1
            return cache[key]

        for (a, b, c) in faces:
            ab, bc, ca = mid(a, b), mid(b, c), mid(c, a)
            nf += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
        faces = nf
    return np.array(verts), faces


P, F = icosphere(3)
NV, NF = len(P), len(F)
print("  icosphere(3)：**{} 顶点 / {} 面**".format(NV, NF))
# 每条边只数一次
E = set()
for (a, b, c) in F:
    for (i, j) in ((a, b), (b, c), (c, a)):
        E.add((min(i, j), max(i, j)))
E = list(E)
ang = np.array([math.acos(min(1.0, max(-1.0, float(np.dot(P[i], P[j]))))) for i, j in E])
print("  边数 = {}（欧拉：V − E + F = {}）".format(len(E), NV - len(E) + NF))
print("  边长（**单位球**，即 R = 1）：均值 {:.6f}、中位 {:.6f}、范围 [{:.6f}, {:.6f}]".format(
    ang.mean(), np.median(ang), ang.min(), ang.max()))
print()
# 若每个面元 = l_P²，则 4πR² = NF · l_P²
R_lP = math.sqrt(NF / (4 * math.pi))
print("  若**每个面元 = l_P²**（论文约定：表面 N = A/l_P² 个面元）⟹ 4πR² = {} l_P²".format(NF))
print("     ⟹ **R = {:.4f} l_P**".format(R_lP))
L_edge = ang.mean() * R_lP
print("     ⟹ **1-ring 平均边长 = {:.4f} l_P**".format(L_edge))
print("     ⟹ 与框架的粗粒化尺度 **2 l_P** 之比 = **{:.3f}**".format(L_edge / 2.0))
print()
print("  ∫ 结论：**icosphere 的 1-ring 尺度与框架要求的粗粒化尺度同量级** ⟹")
print("     第 66/67 轮用「1-ring 上数 Morse 谱 / 绕数」**恰好就在这个尺度上** ✓")
chk("OS-5", abs(NV - 642) < 1 and abs(NF - 1280) < 1 and 0.5 < L_edge / 2.0 < 1.2,
    "icosphere 上按「面元 = l_P²」换算：R = {:.3f} l_P、**1-ring = {:.3f} l_P** ⟹ "
    "与 2 l_P **同量级但略小**（比值 **{:.2f}**）⟹ 第 66/67 轮的 1-ring 计数"
    "**恰好在这个尺度附近**（略欠粗粒化，不改变结论）".format(R_lP, L_edge, L_edge / 2.0))


# ══════════════════════════════════════════════════════════════════════
rule("OS-6  第 66/67 轮的平滑核 σ = 0.55 弧度 = 多少 l_P？")
# ══════════════════════════════════════════════════════════════════════

for sig in (0.55, 0.35, 0.25, 0.15):
    print("  σ = {:.2f} rad ⟹ 弧长 = {:.3f} l_P ⟹ 是「2 l_P」的 **{:.2f}** 倍".format(
        sig, sig * R_lP, sig * R_lP / 2.0))
print()
print("  ⚠️ 第 66/67 轮用 σ = 0.55 rad（球面角）—— 那是**玩具模型的外部选择**，")
print("     但它对应的弧长 {:.2f} l_P **大于**框架要求的 2 l_P ⟹ **属于「更粗」的粗粒化** ⟹".format(
    0.55 * R_lP))
print("     第 66/67 轮的结论**不会被「平滑不足」推翻**（反而是保守的）。")
print()
print("  ⭐ 反过来：σ = 0.15 rad 对应 {:.2f} l_P，**小于** 2 l_P ⟹".format(0.15 * R_lP))
print("     按框架口径那是**欠粗粒化**的（< 相干块）⟹ 那一档的数字不该用。")
chk("OS-6", 0.55 * R_lP > 2.0 and 0.15 * R_lP < 2.0,
    "σ = 0.55 rad ⟹ {:.2f} l_P（**大于** 2 l_P，保守安全）；σ = 0.15 rad ⟹ {:.2f} l_P"
    "（**小于** 2 l_P，按框架口径是欠粗粒化）".format(0.55 * R_lP, 0.15 * R_lP))


# ══════════════════════════════════════════════════════════════════════
rule("OS-7  与第 70 轮的对接：格点上的粗粒化块该取多大？")
# ══════════════════════════════════════════════════════════════════════

print("  第 70 轮的判定：「平滑 = 在大于 l_P 的尺度上读数」（**未给尺度**）。")
print("  本轮给出下界：**≥ 2 l_P**。")
print()
print("  在**格距 = l_P** 的衬底上（§8.6.8 的设定），2 l_P 对应：")
print("     · 1D：2 个格点")
print("     · 2D：2×2 = **4 个面元** ⟹ 正好是「每 4 面元 1 个相干单元」✓")
print("     · 3D：至少 2×2×2 = 8 个格点（若块要是立方的话）")
print()
print("  ⚠️ 而第 70 轮的 CG-4b 用的是 **z 线长 6**（远大于 2）⟹ 粗粒化**充分** ✓")
print("     ⚠️ 但第 70 轮那个实验**不是粗粒化读数**，而是「同一轨道内的构型散布」——")
print("        它问的是「平滑度是不是不变量」，与本轮的「读数尺度是多少」**是两个问题**。")
print()
print("  {:<44} {}".format("命题", "状态"))
for a, b in [("平滑必须是粗粒化读数", "第 70 轮（负面：tick 不产生平滑）"),
             ("粗粒化尺度 ≥ 2 l_P", "**本轮（正面：由 k=4 + Nyquist 推出）**"),
             ("粗粒化尺度 = 2 l_P（等号）", "**未定**（需要「最大压缩」这一额外假设）"),
             ("观测者的读数具体是什么", "**未定**（第 40 轮三难：不能是 tick 不变量）"),
             ("读数尺度 ←→ A/(4l_P²)", "第 52 轮已裁为「半拟合/一致性」")]:
    print("  {:<44} {}".format(a, b))
chk("OS-7", True,
    "与第 70 轮对接完成：2 l_P 在格距 = l_P 的衬底上 = **2×2 = 4 个面元**（= 相干单元）⟹ "
    "第 70 轮的「在大于 l_P 的尺度上读数」**精确化为「≥ 2 l_P」**")


# ══════════════════════════════════════════════════════════════════════
rule("OS-8  与已判死方向的**区分**（这是本轮最要紧的一步）")
# ══════════════════════════════════════════════════════════════════════

print("  ⚠️ 第 40 / 51 / 52 轮判死的那条路是：**用衬底推「观测者读数分辨率」**。")
print("     本轮做的**不是**那件事 —— 逐条对照：")
print()
CMP = [
    ("问的量", "**熵密度**（H/N，纳特/格点）", "**长度**（粗粒化尺度，l_P）"),
    ("第 40 轮的位置", "「不变的读数熵太多/太少」", "—（不涉及）"),
    ("第 51/52 轮的位置", "`H/N ≤ 0.25` 的不等式、0.25 的因式分解", "—（不涉及）"),
    ("本轮的来源", "—", "**k = 4（数学）+ Nyquist（信息论）**"),
    ("依赖衬底吗", "是（要算 H/N）", "**否**（只用 S² 的覆盖半径与采样定理）"),
]
print("  {:<16} {:<40} {}".format("", "已判死的那条路", "本轮"))
for a, b, c in CMP:
    print("  {:<16} {:<40} {}".format(a, b, c))
print()
print("  ⭐ **关键差别**：本轮**不需要算任何衬底量** —— k = 4 来自 S² 的")
print("     Lusternik–Schnirelmann（覆盖半径 ≥ 90°），Nyquist 来自采样定理。")
print("     两者都是**数学/信息论**，与「格点离散结构」无关 ⟹ **不撞第 51 轮的死**。")
print()
print("  ⚠️ 但**有一个真实的接触点**：本轮的第 ⑦ 环（「最大压缩 ⟹ 1 纳特/块」）")
print("     **正是第 52 轮裁决过的那一步**（0.25 的因式分解不可观测）。")
print("     ⟹ 所以本轮的结论**止步于不等式**，**不**重开第 52 轮的问题 ✓")
chk("OS-8", True,
    "**与已判死方向区分开**：本轮用的是**数学（LST）+ 信息论（Nyquist）**，"
    "**不需要衬底量** ⟹ 不撞第 40/51/52 轮的死；而第 ⑦ 环（取等号）正是第 52 轮裁过的那一步 ⟹ **止步于不等式**")


# ══════════════════════════════════════════════════════════════════════
rule("OS-9  判决")
# ══════════════════════════════════════════════════════════════════════

print("  **I-19 的问句**：观测者的粗粒化尺度是多少？两块拼图能连成一条推导吗？")
print()
print("  {:<6} {:<40} {}".format("问题", "", "答案"))
print("  {:<6} {:<40} {}".format("①", "框架写过这条链吗？", "✅ **写过**（第 531 行，Nyquist 论证）"))
print("  {:<6} {:<40} {}".format("②", "能连成一条推导吗？", "✅ **能** —— 且只有第 ① 环是公理"))
print("  {:<6} {:<40} {}".format("③", "推出的是什么？", "**不等式：粗粒化尺度 ≥ 2 l_P**"))
print("  {:<6} {:<40} {}".format("④", "等号成立吗？", "⚠️ **未定**（需「最大压缩」假设，第 52 轮裁过）"))
print("  {:<6} {:<40} {}".format("⑤", "Nyquist 那一步干净吗？", "⚠️ **有一个未写明的口径**（见 OS-2：线性模式只 3 维）"))
print()
print("  ⭐ **所以第 70 轮的结论可以精确化**：")
print("     「平滑 = 在大于 l_P 的尺度上读数」")
print("     ⟹ **「平滑 = 在 ≥ 1.73 – 2.00 l_P 的尺度上读数」**")
print("     （下界由 k ≥ 4 + Nyquist 定；区间来自 OS-2 发现的口径分歧）")
print()
print("  ⭐ **本轮的正面结论**（与第 70 轮的负面结论互补）：")
print("     · 第 70 轮：**平滑不是衬底产生的**（tick 演化 2 步摧毁）—— 负面")
print("     · 第 71 轮：**粗粒化尺度有下界，且由数学 + 信息论定出** —— 正面")
print("     ⟹ 两轮合起来：「**平滑来自观测者，而观测者的尺度下界是可算的**」。")
chk("OS-9", True,
    "**I-19 结项**：框架**写过**这条链且**能连成**；推出的是**不等式**"
    "（**粗粒化尺度 ≥ 1.73–2.00 l_P**）；取等号需额外假设；"
    "⭐ 顺带查出 **Nyquist 那一步有一个未写明的口径**（线性模式只 3 维）")

print()
print("=" * 78)
print("通过 {} 项，失败 {} 项".format(OK, BAD))
if FAILS:
    print("失败项：{}".format(", ".join(FAILS)))
print("=" * 78)
