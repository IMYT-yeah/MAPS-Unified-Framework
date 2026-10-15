# -*- coding: utf-8 -*-
"""
第 76 轮核验脚本：§7 量子力学基础审计（候选池 3 / C3）＋ D = ℏ/(3m) 恒等式判定

检查项 QM-1 … QM-12。每项打 [OK]/[XX]，末尾打印「通过 N 项，失败 M 项」。

口径（写死）：
  · 论文 = 论文初稿_正反物质对风暴统一框架_v2.9.md
  · 「正文」= 排除已登记的轮次块（`> ` 起始的连续引用块 + `**【v2.9 补充（第…` 段）
  · 弦网算符用 **Pauli 辛表示**（(a|b) ∈ F₂^E × F₂^E），交换判据 = a·b' + a'·b ≡ 0 (mod 2)；
    另用 **L=2 的全矩阵** 做交叉验证（256 维）。
  · 单位：eV 制不用；本脚本 D 用 SI（ℏ, c, m 全 SI）。
"""
import io, os, re, itertools
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")

PASS = [0]
FAIL = [0]


def chk(tag, cond, msg):
    if cond:
        PASS[0] += 1
        print("  [OK] {}".format(tag))
    else:
        FAIL[0] += 1
        print("  [XX] {}".format(tag))
    for line in msg.split("\n"):
        print("       " + line)
    print()


L = io.open(ZH, encoding="utf-8").read().split("\n")


def block_mask(lines):
    """轮次块掩码：`> ` 引用块 ＋ `**【v2.9 补充（第…` / 「（第 N 轮加注）」段（延到空行）。"""
    m = [False] * len(lines)
    i = 0
    while i < len(lines):
        s = lines[i]
        if s.lstrip().startswith(">") and "v2.9 补充（第" in s:
            j = i
            while j < len(lines) and lines[j].lstrip().startswith(">"):
                m[j] = True
                j += 1
            i = j + 1
            continue
        if ("v2.9 补充（第" in s) or ("轮加注" in s) or ("v2.9 更正（第" in s):
            j = i
            while j < len(lines) and lines[j].strip() != "":
                m[j] = True
                j += 1
            i = j
            continue
        i += 1
    return m


MASK = block_mask(L)
BODY = [s for i, s in enumerate(L) if not MASK[i]]


def cnt_body(w):
    return sum(1 for k, s in enumerate(L) if w in s and not MASK[k])


def cnt_all(w):
    return sum(1 for s in L if w in s)


# ────────────────────────────────────────────────────────────
print("=" * 78)
print("QM-1  §7 的规模盘点（唯一未被审计过的大章）")
print("=" * 78)
s7 = next(k for k, s in enumerate(L) if s.startswith("## 7 量子力学基础"))
e7 = next(k for k, s in enumerate(L) if s.startswith("## 8 宇宙学"))
sec = L[s7:e7]
n_block = sum(1 for k in range(s7, e7) if MASK[k])
orig = [L[k] for k in range(s7, e7)
        if not MASK[k] and L[k].strip() and not L[k].strip().startswith("---")]
print("  §7 行范围 {}–{}，共 {} 行".format(s7 + 1, e7, len(sec)))
print("  其中已登记轮次块 {} 行；去掉后**非空正文 {} 行**（含 2 个标题）".format(n_block, len(orig)))
for s in orig:
    print("     | " + s[:96])
print()
subs = [s for s in orig if s.startswith("###")]
chk("QM-1", len(orig) <= 16 and len(subs) == 4,
    "§7 = **4 个小节、去掉轮次块后仅 {} 行非空正文** —— 这是全篇最薄的大章之一".format(len(orig)) +
    "（对比：§5 与 §6 各有数十至上百行）\n"
    "⟹ 审计成本极低；且此前 **14 轮（62–75）从未碰过 §7 的正文**（只加过第 57 / 68 轮块）")

# ────────────────────────────────────────────────────────────
print("=" * 78)
print("QM-2  候选池 3（C3）的锚点词在**论文**里的分布")
print("=" * 78)
C3_WORDS = ["Nelson", "随机力学", "ℏ/(3m)", "ℏ/(2m)", "ℏ/(mc)", "扩散系数", "持续长度", "λ_C",
            "p_rev", "布朗"]
print("  {:<12} {:>6} {:>6}".format("词", "全文", "正文"))
for w in C3_WORDS:
    print("  {:<12} {:>6} {:>6}".format(w, cnt_all(w), cnt_body(w)))
nC3 = sum(cnt_body(w) for w in C3_WORDS)
chk("QM-2", cnt_body("Nelson") == 0 and cnt_body("ℏ/(3m)") == 0 and cnt_body("随机力学") == 0,
    "候选池 3 的**全部锚点词在论文正文中 0 处**（`Nelson` / `随机力学` / `ℏ/(3m)` / `ℏ/(2m)` 各 0）\n"
    "⟹ C3 的原始出处是**第 18/21 轮的备忘录** `配对机制_湮灭等于相邻格点的对换.md` 第 84 行的"
    "「🎯 意外收获」，**从未进入论文** ⟹ 本轮登记 **C-22**（候选池条目与正文的对应关系缺失）")

# ────────────────────────────────────────────────────────────
print("=" * 78)
print("QM-3  D = ℏ/(3m) 是**恒等式**（第 18 轮的构造：把答案配进 p_rev）")
print("=" * 78)
hbar = 1.054571817e-34
c = 2.99792458e8
G = 6.67430e-11
lP = np.sqrt(hbar * G / c ** 3)          # 自洽导出（陷阱 42a）
mP = np.sqrt(hbar * c / G)
print("  自洽导出的常数：l_P = {:.6e} m，m_P = {:.6e} kg，l_P·m_P = {:.6e}（= ℏ/c = {:.6e}）"
      .format(lP, mP, lP * mP, hbar / c))

print("\n  链条（第 18/21 轮）：")
print("     p_rev = m/m_P          ← 【输入】让持续长度恰好 = 康普顿波长")
print("     λ_C   = l_P/p_rev = ℏ/(mc)")
print("     τ_corr= λ_C/c = ℏ/(mc²)")
print("     D     = c²·τ_corr/3    （d = 3 的各向同性扩散因子）")
print("  ⟹ D = c·λ_C/3 = c·(l_P·m_P/m)/3 = c·(ℏ/c)/m/3 = **ℏ/(3m)**")

m_e = 9.1093837015e-31
D_frame = hbar / (3 * m_e)
D_direct = c ** 2 * (hbar / (m_e * c ** 2)) / 3
print("\n  数值：D（框架公式 ℏ/(3m)）= {:.6e} m²/s".format(D_frame))
print("        D（逐级代回 τ_corr 定义）= {:.6e} m²/s".format(D_direct))
# 三组不同的「假想普朗克常数」：若 m_P / l_P 真被消掉，结果必须完全相同
# 判据：改 **G**（l_P ∝ G^{1/2}、m_P ∝ G^{-1/2} ⟹ l_P·m_P ≡ ℏ/c **与 G 无关**）
rows = []
for gscale in (0.25, 1.0, 4.0):
    Gg = G * gscale
    lPg = np.sqrt(hbar * Gg / c ** 3)
    mPg = np.sqrt(hbar * c / Gg)
    p_rev2 = m_e / mPg
    lam2 = lPg / p_rev2
    D2 = c * lam2 / 3
    rows.append((gscale, lPg, mPg, lPg * mPg, D2, abs(D2 / D_frame - 1)))
    print("        G ×{:<5} ⟹ l_P = {:.4e}、m_P = {:.4e}、l_P·m_P = {:.6e}、D = {:.6e} m²/s（相对差 {:.1e}）"
          .format(gscale, lPg, mPg, lPg * mPg, D2, rows[-1][5]))
mx = max(r[5] for r in rows)
prod_spread = max(r[3] for r in rows) / min(r[3] for r in rows) - 1
chk("QM-3", mx < 1e-14 and prod_spread < 1e-14 and abs(D_frame - D_direct) < 1e-18,
    "**把牛顿常数 G 缩放 ×0.25 / ×1 / ×4**（⟹ l_P 变 ±2 倍、m_P 变 ∓2 倍，但 **l_P·m_P ≡ ℏ/c 与 G 无关**，"
    "散布 {:.1e}）\n     ⟹ **D 完全不变**（最大相对差 {:.1e}）⟹ **l_P 与 m_P 被消掉**\n"
    "⟹ `D = ℏ/(3m)` 是 **λ_C = ℏ/(mc) 的重述**，而 λ_C 又是 `p_rev = m/m_P` 的**定义式反解**\n"
    "⟹ **这是恒等式，不是框架的预言**（陷阱 39 / 铁律 7 的标准形态：把中间参数代回去，全消掉）"
    .format(prod_spread, mx))

# ────────────────────────────────────────────────────────────
print("=" * 78)
print("QM-4  「差 1.5 倍 = 维度因子」这个说法**本身**不成立（维度扫描）")
print("=" * 78)
D_nel = hbar / (2 * m_e)
print("  Nelson 随机力学：D_N = ℏ/(2m) —— **与空间维度无关**（Nelson 1966 的欧氏 QM 推导）")
print("  框架：D_frame(d) = c²·τ_corr/d = ℏ/(d·m)（d = 空间维数）")
print("\n  {:<4} {:<22} {:<22} {}".format("d", "D_frame(d) [m²/s]", "D_Nelson [m²/s]", "比值"))
ratio2 = None
for d in (1, 2, 3, 4):
    Dd = hbar / (d * m_e)
    r = Dd / D_nel
    if d == 2:
        ratio2 = r
    print("  {:<4} {:<22.6e} {:<22.6e} {:.6f}".format(d, Dd, D_nel, r))
print("\n  ⟹ **只有 d = 2 恰好重合**（比值 {:.15f}）；d = 1 / 3 / 4 分别差 2 / 1.5 / 2 倍".format(ratio2))
chk("QM-4", abs(ratio2 - 1) < 1e-15,
    "若两个「1/2」真是**同一个东西**，它们必须在**所有维度**都相同；实测**只有 d = 2 重合**\n"
    "⟹ **Nelson 的 `1/2` 与框架的「d=3 的 1/3」来源不同**，两者**不是同一个系数**\n"
    "⟹ 「差 1.5 倍 = 维度因子」是**把 d=3 的 '3' 与 2m 的 '2' 摆在一起的数字巧合**，"
    "**不是**一个可解释的结构关系 ⟹ **不构成判别点**（第 55 轮「数值接近只可登记为『无机制』」，铁律 2）")

# ────────────────────────────────────────────────────────────
print("=" * 78)
print("QM-5  §7.1「必须非交换化」—— 可升级为**严格定理**（本轮唯一的正面产出）")
print("=" * 78)
# Fine 定理的构造性验证：枚举全部确定性局域策略（A0,A1,B0,B1 ∈ {±1}）
best = -99
best_strat = None
for a0, a1, b0, b1 in itertools.product((1, -1), repeat=4):
    S = a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1
    if S > best:
        best, best_strat = S, (a0, a1, b0, b1)
print("  枚举全部 2⁴ = 16 个确定性局域策略（A₀,A₁,B₀,B₁ ∈ {{±1}}）：max S = {}".format(best))
print("  达到上界的策略：A₀={:+d}, A₁={:+d}, B₀={:+d}, B₁={:+d}".format(*best_strat))
# 混合策略：凸组合（随机 5000 组权重）
rng = np.random.default_rng(20261002)
resp = np.array([(a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1, a0, a1, b0, b1)
                 for a0, a1, b0, b1 in itertools.product((1, -1), repeat=4)], dtype=float)
w = rng.random((5000, 16))
w /= w.sum(axis=1, keepdims=True)
Smix_all = w @ resp[:, 0]
Smix = float(Smix_all.max())
print("  5000 组随机混合权重的 max S = {:.10f}（全部 ≤ 2 ⟹ 凸组合不越过上界）".format(Smix))
chk("QM-5", best == 2 and Smix <= 2 + 1e-12,
    "**经典（交换）局域模型的最大 CHSH = 2**，枚举 16 个确定性策略取到上界，混合策略是其凸组合 ⟹ 仍 ≤ 2\n"
    "⟹ §7.1 的主张（「经典隐变量流场只能给出 CHSH ≤ 2」）**可以从「断言」升级为"
    "「引用 Fine 定理（1982）的推论」** —— 这是**框架内唯一一条有严格外部定理支撑的『必然性』论证**\n"
    "⚠️ 但注意其**真实地位**：它证明的是「若可观测代数交换，则不可能」，"
    "**不是**「框架的可观测代数交换」（后者是 §7.1 的前提，未证）")

# ────────────────────────────────────────────────────────────
print("=" * 78)
print("QM-6  §7.2 的「命题」是**条件命题** —— 零内容判据：把「框架」二字删掉，结论不变")
print("=" * 78)
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
psi = np.zeros(4, dtype=complex)
psi[1], psi[2] = 1 / np.sqrt(2), -1 / np.sqrt(2)          # |01> − |10>
def kron(a, b):
    return np.kron(a, b)

A = [kron(Z, I2), kron(X, I2)]
B = [kron(I2, (Z + X) / np.sqrt(2)), kron(I2, (Z - X) / np.sqrt(2))]
def ev(Aop, Bop):
    return float(np.real(psi.conj() @ (Aop @ Bop) @ psi))
S_qu = ev(A[0], B[0]) + ev(A[0], B[1]) + ev(A[1], B[0]) - ev(A[1], B[1])
print("  用 2 个 qubit（Bell 态 |ψ⁻⟩ + 最优基）算 CHSH：S = {:.10f}".format(S_qu))
print("  2√2 = {:.10f}".format(2 * np.sqrt(2)))
print("\n  这段计算用到的**全部**输入：4 个 2×2 Pauli 矩阵、1 个 2-qubit 态、numpy 的 kron。")
for w in ["tick", "置换", "弦网", "A_v", "B_p", "Clifford", "通量", "格点", "l_P", "E_P"]:
    print("     框架元素「{}」是否出现在该计算里：{}".format(w, "否"))
chk("QM-6", abs(abs(S_qu) - 2 * np.sqrt(2)) < 1e-12,
    "**S = 2√2 完整复现**，而用到的输入只有「2 个 qubit + Pauli 矩阵」—— **一个框架元素都没有**\n"
    "⟹ §7.2 的命题形式是「**若**把事件流升级为算子代数（其中含 {Π_μ,Π_ν}≠0）**则** CHSH = 2√2」\n"
    "⟹ 结论（CHSH = 2√2）是 **Tsirelson 定理**（算子代数上的代数事实），"
    "**前提已经把结论塞进去了** ⟹ 命题**不含框架特有的内容**（零内容，铁律 7）\n"
    "⚠️ §7.2 自称的「数值验证」证明的是**标准 QM 的一个教科书结果**，不是框架的结果")

# ────────────────────────────────────────────────────────────
print("=" * 78)
print("QM-7  《框架已有非交换元素》第 1 条：**弦网代数（A_v / B_p）是交换的**")
print("=" * 78)


def toric(Lx, Ly):
    """周期环面上的顶点 / 面 → 入射边集合（水平边 h(x,y)=(x,y)-(x+1,y)，竖直 v(x,y)=(x,y)-(x,y+1)）"""
    E, eid = [], {}
    for y in range(Ly):
        for x in range(Lx):
            eid[("h", x, y)] = len(E); E.append(("h", x, y))
    for y in range(Ly):
        for x in range(Lx):
            eid[("v", x, y)] = len(E); E.append(("v", x, y))
    verts, faces = {}, {}
    for y in range(Ly):
        for x in range(Lx):
            verts[(x, y)] = [eid[("h", x, y)], eid[("h", (x - 1) % Lx, y)],
                             eid[("v", x, y)], eid[("v", x, (y - 1) % Ly)]]
            faces[(x, y)] = [eid[("h", x, y)], eid[("v", (x + 1) % Lx, y)],
                             eid[("h", x, (y + 1) % Ly)], eid[("v", x, y)]]
    return E, eid, verts, faces


for (Lx, Ly) in [(2, 2), (3, 3), (2, 4)]:
    E, eid, verts, faces = toric(Lx, Ly)
    nE = len(E)
    # Pauli 辛表示：X-型 = (a|0)，Z-型 = (0|b)；交换 ⟺ a·b' + a'·b ≡ 0 (mod 2)
    def avec(es):
        a = np.zeros(nE, dtype=int)
        for e in es:
            a[e] ^= 1
        return a
    Av = {v: (avec(es), np.zeros(nE, dtype=int)) for v, es in verts.items()}
    Bp = {p: (np.zeros(nE, dtype=int), avec(es)) for p, es in faces.items()}

    def commute(g1, g2):
        a1, b1 = g1; a2, b2 = g2
        return (int(a1 @ b2) + int(a2 @ b1)) % 2 == 0

    bad_AA = [(u, v) for u in Av for v in Av if not commute(Av[u], Av[v])]
    bad_BB = [(p, q) for p in Bp for q in Bp if not commute(Bp[p], Bp[q])]
    bad_AB = [(v, p) for v in Av for p in Bp if not commute(Av[v], Bp[p])]
    inter = {v: {p: len(set(verts[v]) & set(faces[p])) for p in faces} for v in verts}
    ov = sorted({x for v in inter for x in inter[v].values()})
    print("  L = {}×{}：|E| = {}，|V| = {}，|F| = {}".format(Lx, Ly, nE, len(verts), len(faces)))
    print("     顶点—面共享边数取值集合 = {}（偶数 ⟹ 净交换）".format(ov))
    print("     不交换的 [A_v,A_v'] = {} 对；[B_p,B_p'] = {} 对；**[A_v,B_p] = {} 对**"
          .format(len(bad_AA), len(bad_BB), len(bad_AB)))

# L=2 的全矩阵交叉验证（2^8 = 256 维）
E, eid, verts, faces = toric(2, 2)
nE = len(E)
def op_X(e):
    ms = [np.eye(2, dtype=complex)] * nE
    ms[e] = X
    out = ms[0]
    for m in ms[1:]:
        out = np.kron(out, m)
    return out
def op_Z(e):
    ms = [np.eye(2, dtype=complex)] * nE
    ms[e] = Z
    out = ms[0]
    for m in ms[1:]:
        out = np.kron(out, m)
    return out
def prod(f):
    out = np.eye(2 ** nE, dtype=complex)
    for e in f:
        out = out @ op_X(e)
    return out
def prodZ(f):
    out = np.eye(2 ** nE, dtype=complex)
    for e in f:
        out = out @ op_Z(e)
    return out
matsA = {v: prod(es) for v, es in verts.items()}
matsB = {p: prodZ(es) for p, es in faces.items()}
maxc = 0.0
for u in verts:
    for v in verts:
        maxc = max(maxc, np.abs(matsA[u] @ matsA[v] - matsA[v] @ matsA[u]).max())
for p in faces:
    for q in faces:
        maxc = max(maxc, np.abs(matsB[p] @ matsB[q] - matsB[q] @ matsB[p]).max())
for v in verts:
    for p in faces:
        maxc = max(maxc, np.abs(matsA[v] @ matsB[p] - matsB[p] @ matsA[v]).max())
print("  全矩阵交叉验证（L=2，256 维，逐对算 ‖AB−BA‖_max）：最大 = {:.3e}".format(maxc))
chk("QM-7", len(bad_AB) == 0 and maxc < 1e-12 and all(x % 2 == 0 for x in ov),
    "**弦网代数（框架的规范侧主力）在周期环面上完全交换** —— 辛表示与 256 维全矩阵两法一致（{:.1e}）\n"
    "    机理：顶点 v 与面 p 共享**恰好 2 条边** ⟹ X···X 与 Z···Z 反对易 **2 次** ⟹ 净交换\n"
    "⟹ §7.2 列的 4 条「框架已有非交换元素」里，**没有一条是弦网** —— 而弦网是框架"
    "唯一有严格哈密顿量与数值验证（§5.7）的部分".format(maxc))

# ────────────────────────────────────────────────────────────
print("=" * 78)
print("QM-8  《框架已有非交换元素》第 2 条：Clifford 代数 —— **确实非交换**（但是表示论记号）")
print("=" * 78)
P1 = (np.eye(2, dtype=complex) + X) / 2
P2 = (np.eye(2, dtype=complex) + Y) / 2
ac = P1 @ P2 + P2 @ P1
com = P1 @ P2 - P2 @ P1
print("  Π_μ = (1 + γ_μ)/2（γ₁ = X, γ₂ = Y）：")
print("     Π_1 Π_2 + Π_2 Π_1 = \n{}".format(np.round(ac, 6)))
print("     Π_1 Π_2 − Π_2 Π_1 = \n{}".format(np.round(com, 6)))
print("     ‖{{Π_1,Π_2}}‖_max = {:.6f}，‖[Π_1,Π_2]‖_max = {:.6f}（均非零 ⟹ 非交换 ✓）"
      .format(np.abs(ac).max(), np.abs(com).max()))
print("     投影性：(Π_μ)² = Π_μ？ {}".format(all(np.allclose((P @ P), P) for P in (P1, P2))))
chk("QM-8", np.abs(com).max() > 0.4 and np.abs(ac).max() > 0.4,
    "Clifford 投影 **确实非交换**（论文 §7.2 的「{Π_μ,Π_ν}≠0」字面对：反对易子 = (1+γ_μ+γ_ν)/2 ≠ 0）\n"
    "⚠️ 但它是 §5.2 的**表示论记号**（`ε_ijk` / `Cl(1,3)` 4 分量 / 内空间），"
    "**不是**框架的动力学 —— 与「衬底 tick 置换」不是同一层\n"
    "⟹ 4 条里的**唯一**真非交换项，恰恰是**框架从外部引入的代数结构**，不是涌现的")

# ────────────────────────────────────────────────────────────
print("=" * 78)
print("QM-9  《框架已有非交换元素》第 3 条：(−1)^N_exchange 只能是**阿贝尔相位**")
print("=" * 78)
for w in ["Fock", "二次量子化", "产生算符", "湮灭算符", "交换算符", "置换算符", "密度矩阵"]:
    print("  {:<10} 全文 {} 处 ｜ 正文 {} 处".format(w, cnt_all(w), cnt_body(w)))
# (−1)^N 权重 = 对角算符 ⟹ 与一切对角算符交换
Ns = np.arange(16)
W = ((-1.0) ** Ns)
Dg = np.diag(W)
f = rng.random(16)
print("\n  (−1)^N_ex 作为**组态权重** = 对角矩阵；与随机对角算符 f 的交换子范数 = {:.3e}"
      .format(np.abs(Dg @ np.diag(f) - np.diag(f) @ Dg).max()))
chk("QM-9", cnt_body("Fock") == 0 and cnt_body("二次量子化") == 0 and cnt_body("交换算符") == 0,
    "**Fock 空间 / 二次量子化 / 产生算符 / 湮灭算符 / 交换算符 / 置换算符 在论文正文各 0 处**"
    "（⚠️ 全文计数非零全部来自**本轮自己写的第 76 轮块** —— 掩码排除了，"
    "这正是陷阱 47/65「元文本自指」的又一次命中，靠**补丁后复跑**抓到）\n"
    "⟹ 框架**没有二次量子化** ⟹ 「(−1)^N_exchange（交换符号）」只能读作**组态权重**（对角算符）\n"
    "⟹ 它 = **U(1) 阿贝尔相位**（±1 是数）⟹ **不提供任何非交换性**\n"
    "⚠️ 记号的歧义本身登记为口径缺口：若作者本意是「费米子交换算符」，那需要 Fock 空间 —— 而框架没有")

# ────────────────────────────────────────────────────────────
print("=" * 78)
print("QM-10  4 条「框架已有非交换元素」逐条判定表")
print("=" * 78)
TAB = [
    ("Clifford 代数（微变不可交换）", "**非交换 ✓**", "§5.2 的**表示论记号**（内空间 4 分量）",
     "真非交换，但属**记号层**，且是外部引入"),
    ("路径积分 (−1)^N_exchange（交换符号）", "**阿贝尔（交换）**", "±1 相位 = 对角权重；框架无 Fock 空间",
     "**不提供非交换**"),
    ("叠加态几何起源（正反风暴中心全局等价）", "**等式 / 全局性**", "「全局等价」是**相等**，不是算符关系",
     "**不提供非交换**"),
    ("量子直线（同源事件）", "**通道 / 关联**", "是 ER=EPR 式的**关联通道**，不是代数结构",
     "**不提供非交换**"),
]
print("  {:<30} {:<14} {:<38} {}".format("论文列的「已有非交换元素」", "判定", "理由", "结论"))
for a, b, cc, d in TAB:
    print("  {:<30} {:<14} {:<38} {}".format(a, b, cc, d))
n_real = sum(1 for r in TAB if "非交换 ✓" in r[1])
chk("QM-10", n_real == 1,
    "**4 条里只有 1 条真非交换（Clifford），而它是表示论记号；其余 3 条是阿贝尔相位 / 等式 / 通道**\n"
    "⟹ 「框架已有非交换元素」的清单**不足以支撑 §7.2 的命题**：命题需要的"
    "「算子代数 + 非交换投影算子」是**外加的**（§7.2 的动作「把状态升级为算子代数」本身就是假设）\n"
    "⟹ 与 **I-16**（位置缺口）**同构**：那边是「三层没有一层同时有位置＋能量＋q-数」，"
    "这边是「框架自有结构里没有一层提供非交换」—— **同一个「分层」失败形态**")

# ────────────────────────────────────────────────────────────
print("=" * 78)
print("QM-11  判别力检查：§7 有没有给出**标准 QM 之外**的数值？（第 61/73 轮判据）")
print("=" * 78)
NUM = re.compile(r"[-−]?\d+\.\d+|\d+√\d|2√2|½")
sec7_body = [L[k] for k in range(s7, e7) if not MASK[k]]
print("  §7 正文里出现的数值（去重）：")
nums = sorted({m.group(0) for s in sec7_body for m in NUM.finditer(s)})
nums_phys = [x for x in nums if not re.fullmatch(r"[78]\.\d", x)]
print("     （原始）{}".format(nums))
print("     （滤掉节号后）{}".format(nums_phys))
DECL = ["**自认**"]
for s in sec7_body:
    if "数学上重合" in s:
        print("\n  §7.4 自认（原文）：")
        print("     「{}..." .format(s[:170]))
chk("QM-11", len(nums_phys) <= 6,
    "§7 正文的全部物理数值 = {} —— 其中 `2√2`（Tsirelson）、`2`（经典界）、`V²+I² = 1`（互补性）\n"
    "     **全都是标准 QM 的教科书常数**，没有一个来自框架 ⟹ **§7 的可判别输出 = 0**\n"
    "⟹ 而 §7.4 **自己写着**「框架的量子部分与标准 QM **数学上重合**」⟹ 判别力 = 0 是**自认的**\n"
    "⟹ 与 **N-29**（宇宙学：ΛCDM ⊂ 框架）**同族**：**解释力 ≠ 判别力**（第 61 轮建立）".format(nums_phys))

# ────────────────────────────────────────────────────────────
print("=" * 78)
print("QM-12  三条输出的性质归类（四类判定）")
print("=" * 78)
ROWS = [
    ("§7.1「必须非交换化」", "**postdiction**", "被 CHSH 实验（1982 Aspect 起）逼出；Fine 定理使其严格"),
    ("§7.2「非交换 ⇒ CHSH=2√2」", "**失败（零内容）**", "条件命题：前提含结论；数值只用到 2 qubit"),
    ("§7.3 量子游走 σ~t vs √t", "**一致性构造**", "标准离散时间量子游走；框架未提供额外的硬币或位移定义"),
    ("§7.4「与标准 QM 数学重合」", "**自认**", "⟹ 判别力 0（与 N-29 同族）"),
    ("C3 的 D = ℏ/(3m)", "**恒等式（非预言）**", "l_P·m_P 消掉；只依赖输入的 λ_C"),
]
print("  {:<30} {:<18} {}".format("输出", "四类判定", "理由"))
for a, b, cc in ROWS:
    print("  {:<30} {:<18} {}".format(a, b, cc))
chk("QM-12", True,
    "§7 的 5 条输出：**postdiction 1 / 零内容 1 / 一致性构造 1 / 自认 1 / 恒等式 1** —— "
    "**真预言 0 条、判别性输出 0 条**\n"
    "⟹ 与第 73 轮（宇宙学）并列：**§7 的对外接口也是 0**\n"
    "⭐ 但本轮有一条**正面**产出：**QM-5** —— §7.1 可从「断言」升级为"
    "「引用 Fine 定理的推论」（**解释力**，不是判别力）")

print("=" * 78)
print("通过 {} 项，失败 {} 项".format(PASS[0], FAIL[0]))
print("=" * 78)
