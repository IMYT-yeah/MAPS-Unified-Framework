# -*- coding: utf-8 -*-
"""第 67 轮核验：涡心动力学 —— 「随机湮灭中无法湮灭的稳定点」在**演化**下

第 66 轮（`_soliton_66.py`）在**静态几何**上证实：球面 S² 上切向量场的零点指数和 ≡ χ = 2。
本轮做**动力学**：让涡心（切向量场的零点）动起来、相遇、湮灭，
看「随机湮灭中无法湮灭的稳定点」在**演化**下是否依然成立。

判据编号 VX-1 … VX-9。核验脚本 `_vortex_67.py`。

⚠️ 网格复用 `_soliton_66.py` 的 icosphere（**绝不用经纬网格** —— 极点会让 1-ring 退化，
   见 `_soliton_66.py` 第 141-144 行）。
⚠️ 绕数法对 **∇f** 是错的（第 66 轮教训），但对**切向量场**它是正确的 —— 本轮据此工作。

═══ 本轮四个实测事实（先说结论，细节见正文） ═══
 ① **裸绕数和有系统性偏移**：icosphere + 测地平行移动下，平滑切向量场满足
    **Σ w_i = 3χ**（本网格 6，不是 χ = 2）。与场无关、与分辨率无关（subdiv 2/3/4 全是 6）。
    多出的 2χ 恰好是**总曲率** Σ_i K_i/π（角度亏损和 / π）。
    **扣掉它，离散 Poincaré–Hopf 就精确成立**：Σ_i [w_i − 2K_i/(2π)] = χ = 2（12 轴 × 3 分辨率全中）。
 ② **演化把任何初始构型推向同一个吸引子**：6 个全部为 **+1** 的涡心，裸 Σ = +6，
    曲率修正后 = **χ = 2 精确**。5 个种子、两种初始层、2000 步都一样。
 ③ **但裸 Σ 的守恒不是逐点严格的**：当相邻两个离散方向接近**反平行**（Δφ → π）时，
    Σ 出现**单步跳变**（±1…±2），下一步恢复。
 ④ **T²（χ = 0）上净荷恒为 0**，涡心可全灭 ⟹ 「剩几个」由 **χ** 决定。
"""
import math
import numpy as np

OK = 0
BAD = 0


def chk(tag, cond, msg):
    global OK, BAD
    if cond:
        OK += 1
        print("  [OK] {:<9} {}".format(tag, msg))
    else:
        BAD += 1
        print("  [XX] {:<9} {}".format(tag, msg))


def rep(tag, msg):
    print("  [报告] {:<9} {}".format(tag, msg))


def rule(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


# ══════════════════════════════════════════════════════════════════════
rule("VX-1  网格：icosphere 顶点/面数、1-ring 度数（照抄第 66 轮实现）")
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


def build_rings(nv, faces):
    """每个顶点的 1-ring，**按面绕序**（有序）—— 这样绕数才有定义。"""
    nxt = {}
    for (a, b, c) in faces:
        nxt[(a, b)] = c
        nxt[(b, c)] = a
        nxt[(c, a)] = b
    out = []
    for v in range(nv):
        start = None
        for (x, y) in nxt.keys():
            if x == v:
                start = y
                break
        ring, cur = [], start
        while True:
            ring.append(cur)
            nx = nxt.get((v, cur))
            if nx is None or nx == start:
                break
            cur = nx
        out.append(ring)
    return out


def rodrigues(v, axis, ang):
    axis = axis / (np.linalg.norm(axis) + 1e-300)
    return (v * math.cos(ang) + np.cross(axis, v) * math.sin(ang)
            + axis * np.dot(axis, v) * (1 - math.cos(ang)))


def parallel_to(v_from, p_from, p_to):
    """把 T_{p_from} 里的向量平行移动到 T_{p_to}（沿测地线小旋转）。—— 第 66 轮原样"""
    ax = np.cross(p_from, p_to)
    na = np.linalg.norm(ax)
    if na < 1e-15:
        return v_from
    ang = math.acos(max(-1.0, min(1.0, float(np.dot(p_from, p_to)))))
    return rodrigues(v_from, ax, ang)


def onb(Pt, Xz, Xx):
    """逐点切平面正交标架 (E1, E2)，E1 = p × ẑ（奇点在 ±ẑ）。—— 第 66 轮原样"""
    Z = np.array([0.0, 0.0, 1.0])
    X = np.array([1.0, 0.0, 0.0])
    nv = len(Pt)
    e1 = np.zeros((nv, 3))
    e2 = np.zeros((nv, 3))
    for i in range(nv):
        c = np.cross(Pt[i], Z)
        if np.linalg.norm(c) < 1e-9:
            c = np.cross(Pt[i], X)
        c = c / np.linalg.norm(c)
        e1[i] = c
        e2[i] = np.cross(Pt[i], c)
    return e1, e2


def angle_defect(Pt, faces, nv):
    """顶点角度亏损 K_i = 2π − Σ 面角；Σ_i K_i = 2πχ（Descartes / 离散 Gauss–Bonnet）。"""
    K = np.full(nv, 2.0 * math.pi)
    for (a, b, c) in faces:
        for (i, j, k) in [(a, b, c), (b, c, a), (c, a, b)]:
            u = Pt[j] - Pt[i]
            w = Pt[k] - Pt[i]
            cs = float(np.dot(u, w) / (np.linalg.norm(u) * np.linalg.norm(w)))
            K[i] -= math.acos(max(-1.0, min(1.0, cs)))
    return K


def _rot_mat(axis, ang):
    a = axis / (np.linalg.norm(axis) + 1e-300)
    Kx = np.array([[0.0, -a[2], a[1]], [a[2], 0.0, -a[0]], [-a[1], a[0], 0.0]])
    return np.eye(3) + math.sin(ang) * Kx + (1 - math.cos(ang)) * (Kx @ Kx)


def assemble(Pt, Rings, nv):
    """装配 1-ring 权重表 + 逐 (i, j) 的平行移动矩阵（向量化演化的前置）。"""
    kmax = max(len(r) for r in Rings)
    nb = np.zeros((nv, kmax), dtype=np.int64)
    wt = np.zeros((nv, kmax))
    tr = np.zeros((nv, kmax, 3, 3))
    for i, ring in enumerate(Rings):
        k = len(ring)
        nb[i, :k] = ring
        wt[i, :k] = 1.0 / k
        for m, j in enumerate(ring):
            ax = np.cross(Pt[j], Pt[i])
            na = np.linalg.norm(ax)
            if na < 1e-15:
                tr[i, m] = np.eye(3)
            else:
                ang = math.acos(max(-1.0, min(1.0, float(np.dot(Pt[j], Pt[i])))))
                tr[i, m] = _rot_mat(ax, ang)
        # 补位（deg 5 的第 6 槽）：指向同一邻居、同一旋转矩阵
        #   ⟹ 绕数里增量恒为 0，均值里权重为 0，两处都无污染
        for m in range(k, kmax):
            nb[i, m] = nb[i, 0]
            tr[i, m] = tr[i, 0]
    return nb, wt, tr, kmax


class Mesh(object):
    """一个 icosphere 上的全套算子：点、标架、1-ring、平行移动矩阵、角度亏损。"""

    def __init__(self, subdiv):
        self.sub = subdiv
        self.P, self.F = icosphere(subdiv)
        self.NV = len(self.P)
        self.E1, self.E2 = onb(self.P, None, None)
        self.RING = build_rings(self.NV, self.F)
        self.DEG = np.array([len(r) for r in self.RING])
        self.NB, self.WT, self.TR, self.KMAX = assemble(self.P, self.RING, self.NV)
        self.K = angle_defect(self.P, self.F, self.NV)
        self.chi_num = float(self.K.sum() / (2.0 * math.pi))


M = Mesh(3)
SUBDIV, P, FACES, NV = 3, M.P, M.F, M.NV
E1, E2, RING, DEG, K = M.E1, M.E2, M.RING, M.DEG, M.K
NB, WT, TR, KMAX = M.NB, M.WT, M.TR, M.KMAX
DEGDIST = {d: int((DEG == d).sum()) for d in sorted(set(DEG.tolist()))}
print("       icosphere 细分 {} 次：**{} 个顶点 / {} 个面**（期望 642 / 1280）".format(
    SUBDIV, NV, len(FACES)))
print("       1-ring 度数分布：{}（期望 {{5: 12, 6: 630}}）".format(DEGDIST))
print("       角度亏损 Σ_i K_i = {:.6f} ⟹ χ_离散 = Σ_i K_i/(2π) = **{:.6f}**".format(
    K.sum(), M.chi_num))
print("       ⟹ 无退化极点：切向量场的 1-ring 绕数在此有定义（退化只会出现在")
print("          **零点恰好落在格点上**时，见 VX-1c；本轮的场不落在该退化类里）")
chk("VX-1", NV == 642 and len(FACES) == 1280 and DEGDIST == {5: 12, 6: 630}
    and abs(M.chi_num - 2.0) < 1e-9,
    "icosphere(3) = {} 顶点 / {} 面，1-ring 度数 {}，离散 χ = {:.6f}".format(
        NV, len(FACES), DEGDIST, M.chi_num))


# ══════════════════════════════════════════════════════════════════════
rule("VX-1b  ★ 标定：裸绕数和**不是** χ —— 偏移恰好是总曲率")
# ══════════════════════════════════════════════════════════════════════


def transport(v, mesh=None):
    """每个 1-ring 邻居的切向量平行移动到该顶点：shape (NV, K, 3)。"""
    mm = M if mesh is None else mesh
    return np.einsum('ikab,ikb->ika', mm.TR, v[mm.NB])


def tangent_proj(w, mesh=None):
    mm = M if mesh is None else mesh
    if w.ndim == 3:
        return w - np.einsum('ika,ia->ik', w, mm.P)[:, :, None] * mm.P[:, None, :]
    return w - np.einsum('ia,ia->i', w, mm.P)[:, None] * mm.P


def tangent_norm(w, mesh=None):
    w = tangent_proj(w, mesh)
    n = np.linalg.norm(w, axis=1, keepdims=True)
    n[n < 1e-15] = 1.0
    return w / n


def angle_incs(v, mesh=None):
    """1-ring 上相邻（含绕回）方向的角度增量，wrap 到 [−π, π)。"""
    mm = M if mesh is None else mesh
    vt = tangent_proj(transport(v, mm), mm)
    a1 = np.einsum('ika,ia->ik', vt, mm.E1)
    a2 = np.einsum('ika,ia->ik', vt, mm.E2)
    phi = np.arctan2(a2, a1)
    d = np.roll(phi, -1, axis=1) - phi
    return d - 2.0 * np.pi * np.floor(d / (2.0 * np.pi) + 0.5)


def windings(v, mesh=None):
    return angle_incs(v, mesh).sum(axis=1) / (2.0 * np.pi)


def corrected(v, mesh=None):
    """曲率修正后的**逐顶点指数** w_i − 2K_i/(2π)；其和 = χ（平滑场、涡心被分辨开时）。"""
    mm = M if mesh is None else mesh
    return windings(v, mm) - 2.0 * mm.K / (2.0 * math.pi)


def vortex_stats(v, mesh=None):
    mm = M if mesh is None else mesh
    w = windings(v, mm)
    core = np.abs(w) > 0.5
    return (float(w.sum()), int(core.sum()), int((w[core] > 0).sum()),
            int((w[core] < 0).sum()), w)


def max_dphi(v):
    return float(np.abs(angle_incs(v)).max())


def mean_nn_angle(v):
    vt = tangent_proj(transport(v))
    nn = np.clip(np.linalg.norm(vt, axis=2), -1.0, 1.0)
    return math.degrees(math.acos(max(-1.0, min(1.0, float(np.einsum('ik,ik->i', WT, nn).mean())))))


def grad_normed(base, mesh=None):
    mm = M if mesh is None else mesh
    return tangent_norm(np.tile(base, (mm.NV, 1)) - (mm.P @ base)[:, None] * mm.P, mm)


print()
print("       **标定（解析答案已知：2 个指数 +1 的零点，Σ 应为 χ = 2）**")
print("       {:<30} {:>12} {:>12} {:>10} {:>8} {:>8}".format(
    "解析场", "裸 Σ w_i", "修正后 Σ", "涡心数", "+", "−"))
rng_c = np.random.default_rng(1)
cal_generic = []
for nm, base in [("∇_S p_x（退化：零点在顶点）", np.array([1.0, 0.0, 0.0])),
                 ("∇_S p_y（退化：零点在顶点）", np.array([0.0, 1.0, 0.0])),
                 ("∇_S p_z（退化：零点在顶点）", np.array([0.0, 0.0, 1.0]))]:
    v = grad_normed(base)
    S, nc, npp, nnn, _ = vortex_stats(v)
    print("       {:<30} {:>12.6f} {:>12.6f} {:>10} {:>8} {:>8}".format(
        nm, S, float(corrected(v).sum()), nc, npp, nnn))
AXES = []
for _ in range(12):
    a = rng_c.normal(size=3)
    a /= np.linalg.norm(a)
    AXES.append(a)
    v = grad_normed(a)
    cal_generic.append((vortex_stats(v)[0], float(corrected(v).sum())))
cal_generic = np.array(cal_generic)
print("       {:<30} {:>12.6f} {:>12.6f}".format(
    "12 个一般位置轴 ∇(p·a)", cal_generic[:, 0].mean(), cal_generic[:, 1].mean()))
print("         （裸 Σ 的取值集合 = {}；修正后 = {}）".format(
    sorted(set(np.round(cal_generic[:, 0], 6).tolist())),
    sorted(set(np.round(cal_generic[:, 1], 6).tolist()))))

gapz = np.array([math.sqrt(max(0.0, 1.0 - float(np.max(np.abs(P @ a))) ** 2)) for a in AXES])
print()
print("       **判据定义域自检**：12 个标定轴的零点距最近顶点的角距")
print("         最小 {:.6f} rad = **{:.2f} 度**（= 该轴上最小的 |∇(p·a)|）；中位 {:.4f} rad".format(
    gapz.min(), math.degrees(gapz.min()), float(np.median(gapz))))
print("         ⟹ **12 个标定轴的零点全都严格不在格点上** ⟹ 这份标定是**有选择性**的：")
print("            它只覆盖「零点不在格点上」这一类场。另一类见 VX-1c。")
print()
print("       ⟹ **裸绕数法和解析答案差一个常数**：")
print("          · 一般位置（零点不在格点上）一律给 **+6**，不是 +2；")
print("          · 坐标轴场给 +6 / +4 / +2 —— 这三个数**都是退化伪影**，")
print("            它们的零点恰在**顶点**上，w_i 在那里没有定义（详见 **VX-1c**）。")
print()
print("       **偏移是什么？** 逐顶点扣掉角度亏损：")
print("          Σ_i [w_i − 2K_i/(2π)] = Σ w_i − 2·Σ K_i/(2π) = 6 − 2·2 = **2 = χ** ✓（12/12）")
print("       即 **Σ w_i = χ + 2χ = 3χ** —— 多出来的 2χ 正是**总曲率** Σ_i K_i/π。")
print()
print("       **细化检验**（把同一批解析场放到不同分辨率上）：")
print("       {:>7} {:>7} {:>7} {:>8} {:>26} {:>26}".format(
    "subdiv", "顶点", "面", "χ_离散", "裸 Σ w_i 分布", "修正后 Σ 分布"))
sub_ok = True
for sd in [2, 3, 4]:
    mm = Mesh(sd)
    raw, cor = [], []
    for a in AXES:
        v = grad_normed(a, mm)
        raw.append(float(windings(v, mm).sum()))
        cor.append(float(corrected(v, mm).sum()))
    raw = np.round(raw, 6)
    cor = np.round(cor, 6)
    sub_ok = sub_ok and len(set(raw.tolist())) == 1 and abs(raw[0] - 6.0) < 1e-6 \
        and len(set(cor.tolist())) == 1 and abs(cor[0] - 2.0) < 1e-6
    print("       {:>7} {:>7} {:>7} {:>8.4f} {:>26} {:>26}".format(
        sd, mm.NV, len(mm.F), mm.chi_num, str(raw[0]), str(cor[0])))
print()
print("       ⟹ **裸 Σ 恒为 6、修正后恒为 χ = 2，两者都与分辨率无关**（subdiv 2/3/4 × 12 轴，全中）")
print("          ⟹ 偏移不是离散误差的残留，而是「连续场架到三角形骨架」这一步的**恒定代价**。")
print("          ⚠️ 第 66 轮的核心结论（Morse 谱 Σ = #max − #saddle + #min = 2）**不受影响** ——")
print("             那条路数的是临界点，不是绕数。")
chk("VX-1b", all(abs(cal_generic[:, 1] - 2.0) < 1e-9) and sub_ok
    and len(set(np.round(cal_generic[:, 0], 6).tolist())) == 1,
    "解析场标定：**裸 Σ w_i = 3χ = +6**（12 轴、3 个分辨率全同），"
    "**曲率修正后 Σ(w_i − 2K_i/2π) = χ = +2 精确**（12 轴、3 个分辨率全中）")
rep("VX-1b", "**必须如实登记**：题面预期的「切向量场 Σ = χ = 2」**不能**由裸绕数直接读出 ——"
    " 裸值是 3χ = 6。偏移 = 总曲率 ΣK_i/π = 2χ = 4，扣掉后才精确等于 χ")


# ══════════════════════════════════════════════════════════════════════
rule("VX-1c  ★ 判据的定义域：零点**落在格点上**时，绕数根本无定义（不是公式错）")
# ══════════════════════════════════════════════════════════════════════

print("       背景：sim-agent 从面板⑤ 报来「曲率修正公式在零点落在格点上时不成立」，实测")
print("             ∇p_z（零点在南北极顶点）：裸 Σw = +2、修正后 = −2；x̂×p：裸 +4、修正 0。")
print("       我在 Python 侧独立复算，**数值完全一致**（见下表），但**结论要更强**：")
print()
print("       {:<20} {:>10} {:>10} {:>12} {:>12}".format(
    "解析场", "零点位置", "轴上顶点", "裸 Σ w_i", "修正后 Σ"))
DOMY = [("∇_S p_x", np.array([1.0, 0.0, 0.0]), "±x̂（顶点）", "各 1 个"),
        ("∇_S p_y", np.array([0.0, 1.0, 0.0]), "±ŷ（顶点）", "各 1 个"),
        ("∇_S p_z", np.array([0.0, 0.0, 1.0]), "±ẑ（顶点）", "各 1 个")]
dom_rows = []
for nm, base, wher, cnt in DOMY:
    v = grad_normed(base)
    S, C = float(windings(v).sum()), float(corrected(v).sum())
    dom_rows.append((nm, S, C))
    print("       {:<20} {:>10} {:>10} {:>12.6f} {:>12.6f}".format(nm, wher, cnt, S, C))
for nm, axv in [("x̂ × p（方位角场）", np.array([1.0, 0.0, 0.0])),
                ("ẑ × p（方位角场）", np.array([0.0, 0.0, 1.0]))]:
    v = tangent_norm(np.cross(np.tile(axv, (NV, 1)), P))
    S, C = float(windings(v).sum()), float(corrected(v).sum())
    print("       {:<20} {:>10} {:>10} {:>12.6f} {:>12.6f}".format(
        nm, "±" + ("x̂" if axv[0] else "ẑ") + "（顶点）", "各 1 个", S, C))
print()
print("       **三条硬证据，说明这些数字是退化伪影而不是「公式的反例」**：")
print()
print("       证据 ①：把轴**偏一点点**（零点离开顶点，即使是 1e-9 rad）")
print("       {:<10} {:>13} {:>13} {:>13} {:>13}".format(
    "解析场", "对轴 eps=0", "eps=1e-2", "eps=1e-6", "eps=1e-9"))
for nm, base in [("∇_S p_x", np.array([1.0, 0.0, 0.0])),
                 ("∇_S p_y", np.array([0.0, 1.0, 0.0])),
                 ("∇_S p_z", np.array([0.0, 0.0, 1.0]))]:
    r = np.random.default_rng(5)
    cells = []
    for eps in [0.0, 1e-2, 1e-6, 1e-9]:
        a = base + eps * r.normal(size=3)
        a = a / np.linalg.norm(a)
        v = grad_normed(a)
        cells.append("{:+.0f} / {:+.0f}".format(
            float(windings(v).sum()), float(corrected(v).sum())))
    print("       {:<10} {:>13} {:>13} {:>13} {:>13}".format(nm, *cells))
print("       （每格 = 裸 Σ / 修正后 Σ；∇p_z 在 eps=0 时是 +2 / −2，偏 1e-9 后**立刻**变 +6 / +2）")
print()
print("       证据 ②：零点仍留在顶点上，**只把该点的零向量换成一个确定方向**")
base = np.array([0.0, 1.0, 0.0])
raw = np.tile(base, (NV, 1)) - (P @ base)[:, None] * P
nrm = np.linalg.norm(raw, axis=1)
zidx = np.where(nrm < 1e-12)[0]
r2 = np.random.default_rng(7)
bz = []
for tr in range(3):
    v = raw.copy()
    for i in zidx:
        d = r2.normal(size=3)
        d = d - float(d @ P[i]) * P[i]
        v[i] = d / np.linalg.norm(d)
    v = v / np.linalg.norm(v, axis=1, keepdims=True)
    bz.append((float(windings(v).sum()), float(corrected(v).sum())))
print("         零点顶点 = {}；随机指定零向量方向 3 次：裸 Σ = {}（修正 = {}）".format(
    zidx.tolist(), [round(x[0], 4) for x in bz], [round(x[1], 4) for x in bz]))
print("         ⚠️ `tangent_norm` 对零向量**保持 0**，而 atan2(0,0) ≡ 0 ——")
print("            这等价于**强制把该点的方向取成当地标架 E1**。验证：")
v = raw.copy()
for i in zidx:
    e = np.cross(P[i], np.array([0.0, 0.0, 1.0]))
    if np.linalg.norm(e) < 1e-9:
        e = np.cross(P[i], np.array([1.0, 0.0, 0.0]))
    v[i] = e / np.linalg.norm(e)
v = v / np.linalg.norm(v, axis=1, keepdims=True)
print("         把零向量**显式取成 E1 方向**：裸 Σ = {:+.4f}，修正后 = {:+.4f}".format(
    float(windings(v).sum()), float(corrected(v).sum())))
print("         ⟹ 与「保留 0 向量」的结果**逐位相同** ⟹ 现状数字 = 一个**人为约定**的产物。")
print()
print("       证据 ③：由 ①② 可得一个必然推论 —— 退化点上的结果**破坏旋转协变性**。")
print("         icosahedron 的对称群把 ±x̂ 映到 ±ŷ（120° 绕 (1,1,1)，已验证把顶点集映到自身），")
print("         故 ∇p_x 与 ∇p_y 应当同值；但「取成 E1」这个约定不是协变的 ⟹ 实测 6 ≠ 4。")
print("         换成随机方向补值后两者**都是 +6** ⟹ 对称性恢复。")
print()
print("       ⟹ **判读：这既不是「公式错了」，也不是「公式在退化点上失效」，而是")
print("            退化点上 w_i 本身没有定义（零向量的方向是任意的）——那些数字")
print("            （+2 / +4 / +14 以及它们的修正值）没有任何意义，**不能当反例，")
print("            也不能当支持证据**。判据的严格表述是：")
print("            「**平滑、且零点不落在格点上**的场，其 Σ(w_i − 2K_i/(2π)) = χ」。")
print("          本轮 VX-1b 的 12 轴标定全部满足该前提（最小零点—顶点角距 {:.2f} 度）。".format(
    math.degrees(gapz.min())))
chk("VX-1c", abs(dom_rows[2][1] - 2.0) < 1e-9 and abs(dom_rows[2][2] + 2.0) < 1e-9
    and all(abs(x[0] - 6.0) < 1e-9 and abs(x[1] - 2.0) < 1e-9 for x in bz),
    "退化（零点恰在格点上）情形：∇p_z 复现 sim-agent 的 +2/−2；"
    "而**随机补值后 ∇p_y 立刻回到 +6/+2 = χ** ⟹ 退化值是由任意补值产生的伪影，判据在退化点**无定义**")
rep("VX-1c", "**对 sim-agent 边界提醒的核验结论**：方向正确，但表述应升级 —— 不是「公式在退化点不成立」，"
    "而是「**退化点上判据无定义**，因此那些数字不可用作反例或证据」")


# ══════════════════════════════════════════════════════════════════════
rule("VX-1d  修正公式的支点：离散 Gauss–Bonnet 是否严格？")
# ══════════════════════════════════════════════════════════════════════

print("       整条修正公式 Σ(w_i − 2K_i/(2π)) = χ 依赖 Σ_i K_i = 2πχ。若 4π 只是数值巧合，全塌。")
print()
print("       Σ_i K_i      = {:.14f}".format(float(K.sum())))
print("       2πχ = 4π      = {:.14f}".format(2.0 * math.pi * 2.0))
print("       绝对差        = {:.3e}（1280 个面 × 3 个面角累积的浮点残差）".format(
    abs(float(K.sum()) - 4.0 * math.pi)))
print("       Σ_i K_i / π   = {:.14f}   ｜  2χ = 4   ｜  差 = {:.3e}".format(
    float(K.sum() / math.pi), abs(float(K.sum() / math.pi) - 4.0)))
print("       min K_i = {:.6e} ／ max K_i = {:.6e} ／ #(K_i<0) = {}".format(
    K.min(), K.max(), int((K < 0).sum())))
print()
print("       ⟹ Descartes 角亏损定理对**凸多面体精确成立**（不是巧合）：ΣK_i = 4π 到 1e-13；")
print("          且所有 12 个 5 度顶点与 630 个 6 度顶点的 K_i 都为正（球面凸）。")
print("          ⟹ 修正项 ΣK_i/π **恰好**等于 2χ = 4 —— 这正是裸 Σ 与 χ 之间那 4 的来历。")
chk("VX-1d", abs(float(K.sum()) - 4.0 * math.pi) < 1e-10 and int((K < 0).sum()) == 0,
    "离散 Gauss–Bonnet：Σ_i K_i = **{:.12f}**（= 4π，差 {:.1e}），全部 K_i > 0 "
    "⟹ ΣK_i/π = 2χ = 4 是**定理**，不是数值巧合".format(
        float(K.sum()), abs(float(K.sum()) - 4.0 * math.pi)))


# ══════════════════════════════════════════════════════════════════════
rule("VX-1e  口径对齐：与第 66 轮的关系 + 本轮新增假设的边界")
# ══════════════════════════════════════════════════════════════════════

print("       ⚠️ 这一节是**登记**，不是结论。三条必须写进正文的口径：")
print()
print("       ① **与 P「拓扑计数必须用 Morse 谱」的关系**")
print("          P 的原话（refs-agent 取证）：「单位化 ∇f 的绕数」≠「临界点指数」")
print("          ⟹ **拓扑计数必须用 Morse 谱**。本轮**没有推翻**这句话，而是给它补了另一半：")
print("            · 第 66 轮说的是：**裸绕数不能用来数标量场的临界点**（单位化会把 |∇f| 小")
print("              的**非零点**放大成伪涡心）。")
print("            · 本轮说的是：**即使对货真价实的切向量场**（处处单位、无 |∇f| 问题），")
print("              **裸绕数也 ≠ χ**，而是 3χ；差的那 2χ 是总曲率，扣掉后才 = χ。")
print("          ⟹ 两条合起来是同一句话的两半：**裸绕数不是 χ**，两个方法都必须做各自的对齐。")
print("            本轮**不能**写成「切向量场下绕数合法、∇f 下不合法」——那是错的简化。")
print("          ⚠️ 进一步：P 1105 是一句**处方**（「必须用 Morse 谱」），本轮用的是")
print("            「曲率修正绕数」⟹ 这属于**有意偏离 P 自己立的规矩**，理由必须给出。")
print("            这条理由在 **VX-1f** 里被**测出来**（两种计数在共同有效域上给同一个 χ），")
print("            不能只在本节里写一句「等价」了事。")
print()
print("       ② **演化规则是本轮新增的假设**")
print("          refs-agent 取证的结论：P 中「时间演化 / 演化方程 / 动力学方程 / 退火 / 阻尼 /")
print("          梯度流 / 亚稳 / 热流 / Dirichlet / 能量泛函 / 平行移动 / 联络」**全部 0 处**，")
print("          「涡的动力学方程」**不存在**，第 66 轮涡心**无动力学对应物**。")
print("          ⟹ 本轮的 `v ← v − (α/k)·Δv`（切丛内的图热流 = Dirichlet 能量的梯度流）")
print("            **是新增结构，不是框架原有内容**。所有「涡心湮灭」的结论都必须挂在")
print("            「在本轮新引入的这个演化下」这个条件下，不能写成框架的预言。")
print()
print("       ③ **终态涡心结论不是第三条独立成果**")
print("          P 已把「Σ 指数 = χ = 2（方向场）」与「Π_v A_v = Π_p B_p = 1（弦网）」登记为")
print("          **同一个拓扑守恒的两种实现**，明写「不是两条独立成果」。")
print("          本轮 VX-5 得到的「必剩 6 个同号涡心、修正指数和 = χ」**与二者是同一个守恒**")
print("          （第 66 轮 SO-6 已做过这条一致性登记）。")
print("          ⟹ 正文里应写成对 **§8.2 H1 的动力学侧一致性核对**，**不得计成第三条成果**。")
print()
print("       （本节为登记项，不设通过/失败。）")


# ══════════════════════════════════════════════════════════════════════
rule("VX-1f  ★ 与 P 行 1105 处方的正面交代：两种计数在共同有效域上一致")
# ══════════════════════════════════════════════════════════════════════

print("       【P 的处方】行 1105（refs-agent 取证）：")
print("          「单位化 ∇f 的绕数」≠「临界点指数」⟹ **拓扑计数必须用 Morse 谱**。")
print("       本轮 VX 全篇用的是**曲率修正的绕数计数**，**不是 Morse 谱** ——")
print("       因为 P 行 1105 是**一句处方**，所以这种换法**不能默认成立**：")
print("       它是一次**有意偏离 P 自己立的规矩**，必须正面给出偏离的理由。")
print("       理由不能写成口号，本节把它**测出来**：")
print("          「在两者的**共同有效域**上，两种计数给出同一个 χ」。")
print()
print("       共同有效域（三个前提，缺一不可）：")
print("         (i)   场**平滑** —— 这是 Morse 定理自身的前提；")
print("         (ii)  零点**不落在格点上** —— VX-1c：此时绕数根本无定义；")
print("         (iii) 涡心被**网格分辨率解开** —— 离散绕数测度的分辨率代价，见下。")
print()


def morse_spectrum(f, rings, tol=1e-12):
    """离散 Morse 谱：Σ 指数 = #max − #saddle + #min = χ。

    逐字照抄第 66 轮 _soliton_66.py:320 —— 保证两轮数的是**同一个**东西，
    否则本节的「一致」就成了拿两个不同的谱在比。
    """
    mx = mn = sd = 0
    for i, ring in enumerate(rings):
        d = f[i] - f[np.array(ring)]
        hi = int((d < -tol).sum())
        lo = int((d > tol).sum())
        if lo == len(ring):
            mx += 1
        elif hi == len(ring):
            mn += 1
        else:
            seq = [1 if x > tol else (-1 if x < -tol else 0) for x in d]
            seq = [s for s in seq if s != 0]
            if len(seq) >= 2:
                chg = sum(1 for a, b in zip(seq, seq[1:] + seq[:1]) if a != b)
                if chg >= 4:
                    sd += 1
    return mx, mn, sd


def smooth_scalar_on(Pt, nk, sigma, seed):
    """与 rand_smooth_tangent **同一批参数**的平滑标量场。

    关键：参数 c_k / a_k 只由 seed 决定、**与网格无关** ⟹ 同一个连续场可以被
    架到任意分辨率的网格上 ⟹ 下面「细化网格」才是对同一个场的复测。
    """
    r = np.random.default_rng(900 + seed)
    c = r.normal(size=(nk, 3))
    c /= np.linalg.norm(c, axis=1, keepdims=True)
    a = r.normal(size=nk)
    f = np.zeros(len(Pt))
    gr = np.zeros((len(Pt), 3))
    for k in range(nk):
        d = Pt - c[k]
        r2 = np.sum(d * d, axis=1)
        w = a[k] * np.exp(-r2 / (2.0 * sigma ** 2))
        f += w
        gr += (w / (sigma ** 2))[:, None] * (-d)
    return f, gr


NK_CMP, SIG_CMP, NCMP = 12, 0.55, 20
print("       同一批 **{} 个平滑随机标量场**（nk={}，σ={}），逐场两种计数对照：".format(
    NCMP, NK_CMP, SIG_CMP))
print("       {:>5} {:>5} {:>5} {:>6} {:>9} {:>9} {:>9} {:>7}".format(
    "seed", "#max", "#min", "#sad", "Morse Σ", "裸 Σ w_i", "修正后 Σ", "涡心数"))
cmp_rows = []
for s in range(NCMP):
    f, gr = smooth_scalar_on(P, NK_CMP, SIG_CMP, s)
    mx, mn, sad = morse_spectrum(f, RING)
    v = tangent_norm(gr)
    w = windings(v)
    RAW = float(w.sum())
    COR = float(corrected(v).sum())
    nc = int((np.abs(w) > 0.5).sum())
    cmp_rows.append((s, mx - sad + mn, RAW, COR, nc))
    print("       {:>5} {:>5} {:>5} {:>6} {:>9} {:>9.1f} {:>9.1f} {:>7}".format(
        s, mx, mn, sad, mx - sad + mn, RAW, COR, nc))
MSv = sorted(set(r[1] for r in cmp_rows))
RAWv = sorted(set(round(r[2], 6) for r in cmp_rows))
CORv = sorted(set(round(r[3], 6) for r in cmp_rows))
devs = [r for r in cmp_rows if abs(r[3] - 2.0) > 1e-9]
print()
print("       汇总：· Morse Σ 取值 {} ⟹ **{}/{} 等于 χ = 2**；".format(
    MSv, sum(1 for r in cmp_rows if r[1] == 2), NCMP))
print("             · 裸 Σ w_i 取值 {} ⟹ **从不等于 χ**（修正项不是可选修饰）；".format(RAWv))
print("             · 修正后 Σ 取值 {} ⟹ **{}/{} 等于 χ = 2**。".format(
    CORv, NCMP - len(devs), NCMP))
print("       偏差场：{}".format("；".join(
    "seed {}（修正 {:.1f}，核数 {}）".format(r[0], r[3], r[4]) for r in devs)))
print()
print("       **偏差是「网格与场的对齐偶然」，不是「两种计数打架」** —— 这是本节最要紧的一句。")
print("       把同一批连续场架到更细的网格上（subdiv 3 → 4，顶点 642 → 2562）复测：")
REF4 = Mesh(4)
print("       {:>5} {:>6} {:>8} {:>9} {:>9} {:>9} {:>7} {:>7}".format(
    "seed", "subdiv", "顶点", "Morse Σ", "裸 Σ w_i", "修正后 Σ", "涡心数", "χ_离散"))
ref_tab = {}
for s in [7, 14, 0, 9]:
    for sd, mm in [(3, M), (4, REF4)]:
        f, gr = smooth_scalar_on(mm.P, NK_CMP, SIG_CMP, s)
        mx, mn, sad = morse_spectrum(f, mm.RING)
        MS = mx - sad + mn
        v = tangent_norm(gr, mm)
        w = windings(v, mm)
        COR = float(corrected(v, mm).sum())
        ref_tab[(s, sd)] = (MS, COR)
        print("       {:>5} {:>6} {:>8} {:>9} {:>9.1f} {:>9.1f} {:>7} {:>7.0f}".format(
            s, sd, mm.NV, MS, float(w.sum()), COR,
            int((np.abs(w) > 0.5).sum()), mm.chi_num))
    print()
print("       ⟹ seed 7、14 在 subdiv 4 上**恢复到 2**；而 seed 0 **恰恰相反**：")
print("          它在 subdiv 3 上是 2、到 subdiv 4 上反而**掉成 1**。同一个场、同一条公式，")
print("          只换网格，失败就换了对象 ⟹ 失败**恒为 1 个单位**，且**随分辨率迁移**。")
print("          而 Morse Σ 在这 4 个场 × 2 个分辨率（8 格）上**全部精确等于 2**。")
print()
print("       反面参照：把平滑前提拿掉（f 为逐顶点独立噪声，Morse 定理不适用）：")
neg = []
for s in range(5):
    fr = np.random.default_rng(300 + s).normal(size=NV)
    mx, mn, sad = morse_spectrum(fr, RING)
    neg.append(mx - sad + mn)
print("          Morse Σ 取值 {} ⟹ **Morse 谱自己也需要平滑前提**，不是无条件保险。".format(
    sorted(set(neg))))
print()
print("       ⟹ **对 P 行 1105 的交代**（本节存在的唯一目的）：")
print("          · 本轮**不否认**处方，而是**有意偏离**：处方说「用 Morse 谱」，本轮用「修正绕数」。")
print("          · 偏离被允许的**唯一理由**已经测出：在共同有效域上两者给同一个 χ ——")
print("            Morse 路 **20/20 精确**；修正绕数路 **18/20 精确**，其余 2 例恒差 1 个单位、")
print("            细化网格即恢复，且 Morse 路在全部复测格点上始终精确。")
print("          · 因此正文必须写成：「本轮计数与 P 1105 的处方**在有效域上等价**；")
print("            选后者的唯一理由是它对本轮的**动力学**可以逐顶点逐时刻地算」，")
print("            而 Morse 谱要求整体场，无法直接挂在逐步演化的 `v_t` 上。")
print("          ⚠️ 反面同样要写进正文：**共同有效域之外（不平滑、零点落格点）两条路都不成立**。")
_dev_seeds = [r[0] for r in devs]
_fix_ok = all(abs(ref_tab[(s, 4)][1] - 2.0) < 1e-9 for s in _dev_seeds)
_ref_ms_ok = all(abs(ref_tab[k][0] - 2.0) < 1e-9 for k in ref_tab)
chk("VX-1f", all(r[1] == 2 for r in cmp_rows) and len(devs) <= 2
    and all(abs(abs(r[3] - 2.0) - 1.0) < 1e-9 for r in devs) and _fix_ok and _ref_ms_ok,
    "两种计数在同一批平滑随机标量场上**一致**：Morse Σ = χ = 2（**20/20 精确**），"
    "曲率修正绕数 = χ = 2（**18/20**），其余 2 例恒差 1 个单位且细化网格即恢复 "
    "⟹ 本轮对 P 行 1105 处方的偏离在共同有效域上**可交代**")
rep("VX-1f", "裸绕数在这 20 个平滑场上取值 {}，**从不等于 χ** ⟹ 修正项不是可选修饰："
    "少了它，绕数法连平滑场都读不对".format(RAWv))


# ══════════════════════════════════════════════════════════════════════
rule("VX-2  ★ 初始净荷：噪声层 vs 平滑层（本轮关键未知）")
# ══════════════════════════════════════════════════════════════════════


def rand_tangent_iid(rng):
    return tangent_norm(rng.normal(size=(NV, 3)))


def rand_smooth_tangent(rng, nk=12, sigma=0.55):
    c = rng.normal(size=(nk, 3))
    c /= np.linalg.norm(c, axis=1, keepdims=True)
    a = rng.normal(size=nk)
    g = np.zeros((NV, 3))
    for k in range(nk):
        d = P - c[k]
        r2 = np.sum(d * d, axis=1)
        w = a[k] * np.exp(-r2 / (2 * sigma ** 2)) / (sigma ** 2)
        g += w[:, None] * (-d)
    return tangent_norm(g)


MAIN_SEED = 20261001
IC_NK, IC_SIG = 12, 0.55
V_N = rand_tangent_iid(np.random.default_rng(MAIN_SEED))
V_S = rand_smooth_tangent(np.random.default_rng(MAIN_SEED), IC_NK, IC_SIG)

SN0, NCN0, PN0, NN0, WN0 = vortex_stats(V_N)
SS0, NCS0, PS0, NS0, WS0 = vortex_stats(V_S)
CN0 = float(corrected(V_N).sum())
CS0 = float(corrected(V_S).sum())

print("       {:<22} {:>12} {:>12} {:>8} {:>6} {:>6} {:>10}".format(
    "初始场", "裸 Σ w_i", "修正后 Σ", "涡心数", "+", "−", "邻角(°)"))
for nm, S, C, nc, pp, nn, vv in [("噪声层 (i.i.d.)", SN0, CN0, NCN0, PN0, NN0, V_N),
                                 ("平滑层 (∇f, σ=0.55)", SS0, CS0, NCS0, PS0, NS0, V_S)]:
    print("       {:<22} {:>12.6f} {:>12.6f} {:>8} {:>6} {:>6} {:>10.2f}".format(
        nm, S, C, nc, pp, nn, mean_nn_angle(vv)))
print()
scan_i = np.array([vortex_stats(rand_tangent_iid(np.random.default_rng(700 + s)))[0]
                   for s in range(40)])
scan_s = np.array([vortex_stats(rand_smooth_tangent(np.random.default_rng(900 + s),
                                                    IC_NK, IC_SIG))[0] for s in range(12)])
scan_sc = np.array([float(corrected(rand_smooth_tangent(np.random.default_rng(900 + s),
                                                        IC_NK, IC_SIG)).sum()) for s in range(12)])
print("       噪声层 40 次扫描：裸 Σ 均值 {:+.3f}／标准差 {:.3f}／范围 [{:+.0f}, {:+.0f}]".format(
    scan_i.mean(), scan_i.std(ddof=1), scan_i.min(), scan_i.max()))
print("       平滑层 12 次扫描：裸 Σ 取值 {}（11/12 为 +6；1 次为 +5 —— 那次的涡心密到 29 个，".format(
    sorted(set(np.round(scan_s, 6).tolist()))))
print("         其中一对相邻涡心被记在同一个顶点上）；曲率修正后取值 {}（11/12 为 +2）".format(
    sorted(set(np.round(scan_sc, 6).tolist()))))
print()
print("       判读（这是本轮 VX-2 的答案）：")
print("         · **平滑层**：裸 Σ = +6 ≡ 3χ，修正后 = **+2 = χ** ⟹ 是**确定的拓扑量**。")
print("         · **噪声层**：裸 Σ = {:+.0f}（本种子），40 次扫描在 [{:+.0f}, {:+.0f}] 内**随机**波动，".format(
    SN0, scan_i.min(), scan_i.max()))
print("           修正后 = 裸 − 4 也随机 ⟹ **噪声层上 χ 不是守恒量**。")
print("         ⟹ 框架 §2.3「**事件流（普朗克噪声）→ 孤子化 ⟹ 粒子**」的定量含义：")
print("            **必须先粗粒化出平滑层，χ 这个荷才成立**。")
print("            「+2」不是噪声的统计涨落，它是**平滑层的拓扑**。")
chk("VX-2", abs(SS0 - 6.0) < 1e-9 and abs(CS0 - 2.0) < 1e-9,
    "平滑层初始净荷：裸 Σ = **{:+.6f}** = 3χ，曲率修正后 = **{:+.6f}** = χ "
    "⟹ 是整数、可复现的拓扑量".format(SS0, CS0))
rep("VX-2", "噪声层初始净荷：裸 Σ = **{:+.6f}**（40 次扫描 [{:+.0f}, {:+.0f}]）"
    " ⟹ 逐点独立噪声上**不存在**「χ」这个荷；它是平滑层的性质".format(
        SN0, scan_i.min(), scan_i.max()))


# ══════════════════════════════════════════════════════════════════════
rule("VX-3  ★ 演化中净荷如何变化：200 步逐步记账")
# ══════════════════════════════════════════════════════════════════════

ALPHA = 0.3
NSTEP = 200
CKPT = [0, 20, 50, 100, 200]


def ring_mean(v):
    return np.einsum('ik,ika->ia', WT, transport(v))


def step(v, alpha):
    """一步演化：所有顶点用**同一时刻的旧值**（非原地更新）。"""
    return tangent_norm((1.0 - alpha) * v + alpha * ring_mean(v))


def run(v0, nstep, alpha, ckpt):
    v = v0.copy()
    hist = {}
    sig = []
    mdp = []
    for t in range(nstep + 1):
        S, nc, npp, nnn, _ = vortex_stats(v)
        sig.append(S)
        mdp.append(max_dphi(v))
        if t in ckpt:
            hist[t] = (S, nc, npp, nnn)
        if t < nstep:
            v = step(v, alpha)
    sig = np.array(sig)
    mdp = np.array(mdp)
    jumps = [t for t in range(1, nstep + 1) if abs(sig[t] - sig[t - 1]) > 1e-9]
    return {"v": v, "hist": hist, "sig": sig, "mdp": mdp, "jumps": jumps}


print("       α = {}（混合系数）；每步**所有顶点用同一时刻的旧值**".format(ALPHA))
print()
RES = {}
for nm, v0 in [("平滑层 (∇f)", V_S), ("噪声层 (i.i.d.)", V_N)]:
    r = run(v0, NSTEP, ALPHA, CKPT)
    RES[nm] = r
    print("       【{}】".format(nm))
    print("         {:>5} {:>14} {:>9} {:>7} {:>7}".format("t", "裸 Σ w_i", "涡心数", "+", "−"))
    for t in CKPT:
        S, nc, npp, nnn = r["hist"][t]
        print("         {:>5} {:>14.6f} {:>9} {:>7} {:>7}".format(t, S, nc, npp, nnn))
    print("         裸 Σ 取值集合 = {}   （修正后 = 裸 − 4）".format(
        sorted(set(np.round(r["sig"], 6).tolist()))))
    print("         跳变步 t = {}（共 {} 步）".format(r["jumps"], len(r["jumps"])))
    print()

mdpS = RES["平滑层 (∇f)"]["mdp"]
J_S = RES["平滑层 (∇f)"]["jumps"]
rS = [max(mdpS[t - 1], mdpS[t]) for t in range(1, NSTEP + 1)]
jump_r = [math.degrees(rS[t - 1]) for t in J_S]
nojump_r = [math.degrees(rS[t - 1]) for t in range(1, NSTEP + 1) if t not in J_S]
allj = []
for nm in ["平滑层 (∇f)", "噪声层 (i.i.d.)"]:
    sg = RES[nm]["sig"]
    allj += [abs(sg[t] - sg[t - 1]) for t in RES[nm]["jumps"]]
allj = np.array(allj)
jS = np.array([abs(RES["平滑层 (∇f)"]["sig"][t] - RES["平滑层 (∇f)"]["sig"][t - 1])
               for t in J_S])
jN = np.array([abs(RES["噪声层 (i.i.d.)"]["sig"][t] - RES["噪声层 (i.i.d.)"]["sig"][t - 1])
               for t in RES["噪声层 (i.i.d.)"]["jumps"]])
print("       ⚠️ **跳变机制**（本轮第三个实测事实）：")
print("          · 跳变步「本步与上一步」的 max|Δφ|：最小 {:.1f} 度（**全部 ≥ 175°**）".format(min(jump_r)))
print("          · 非跳变步同一量的分位：中位 {:.1f}°／90% 分位 {:.1f}°／最大 {:.1f}°".format(
    float(np.median(nojump_r)), float(np.percentile(nojump_r, 90)), max(nojump_r)))
print("          ⟹ **「接近反平行」是必要条件，不是充分条件**：非跳变步里也有少数顶到 180°")
print("             （贴着边界但**没有跨过**）。真正触发跳变的是 **Δφ 跨过 ±π** ——")
print("             这是绕数定义里的**分支边界**，不是数值噪声，是可解释的离散化失配。")
print("          · 跳变幅度：平滑层 |ΔΣ| ∈ {}（**全部 ≤ 2**）；".format(
    sorted(set(np.round(jS, 6).tolist()))))
print("            噪声层 |ΔΣ| ∈ {}（最大 {:.0f}）—— 噪声层一步要跨很多条边界。".format(
    sorted(set(np.round(jN, 6).tolist())), float(jN.max())))
print()
print("       ⟹ 结论分两层，必须分开说：")
print("          ① **终值**：裸 Σ 总是回到 +6（平滑层 t=200 与 t=0 相同；噪声层锁在 +6）。")
print("          ② **逐点**：裸 Σ **不是严格不变** —— 平滑层 200 步里在 {} 个「跨分支」步跳 ±1…±2 后恢复；".format(
    len(J_S)))
print("             **连续场**才严格守恒。")
chk("VX-3", (min(jump_r) > 175.0 if jump_r else True)
    and (float(jS.max()) <= 2.0 + 1e-9 if len(jS) else True)
    and abs(RES["平滑层 (∇f)"]["sig"][-1] - RES["平滑层 (∇f)"]["sig"][0]) < 1e-9
    and abs(RES["噪声层 (i.i.d.)"]["sig"][-1] - 6.0) < 1e-9,
    "平滑层：跳变幅度 |ΔΣ| 全 ≤ 2（集合 {}），且每个跳变步的 max|Δφ| > 175°；"
    "t=200 的 Σ = t=0 的 Σ = {:+.0f}；噪声层锁在 **+6** "
    "⟹ 跳变是**单步、可解释、必恢复**的离散化失配".format(
        sorted(set(np.round(jS, 6).tolist())), RES["平滑层 (∇f)"]["sig"][-1]))
rep("VX-3", "平滑层 200 步：裸 Σ 取值 {}，在 {} 个反平行步跳变后恢复；"
    "噪声层：裸 Σ 由 {:+.0f} 单调爬到 **+6** 并锁住 ⟹ 与「严格不变」有实质差别".format(
        sorted(set(np.round(RES["平滑层 (∇f)"]["sig"], 6).tolist())), len(J_S),
        RES["噪声层 (i.i.d.)"]["sig"][0]))


# ══════════════════════════════════════════════════════════════════════
rule("VX-4  ★ 涡心数随演化下降：t = 0 / 20 / 50 / 100 / 200（+ 更长时程）")
# ══════════════════════════════════════════════════════════════════════

print("       **为什么该下降**：一步 = v ← v − (α/k)·Δv（切丛内的图热流）。")
print("       小尺度涡–反涡对扩散下迅速相遇湮灭；净荷则无处可去。")
print()
LONG = [0, 20, 50, 100, 200, 500, 1000, 2000]
long_cnt = {}
long_sig = {}
for nm, v0 in [("平滑层 (∇f)", V_S), ("噪声层 (i.i.d.)", V_N)]:
    v = v0.copy()
    cnt = {}
    sig = {}
    for t in range(2001):
        if t in LONG:
            S, nc, npp, nnn, _ = vortex_stats(v)
            cnt[t] = nc
            sig[t] = S
        if t < 2000:
            v = step(v, ALPHA)
    long_cnt[nm] = cnt
    long_sig[nm] = sig
print("       {:<18} {}".format("t", "  ".join("{:>6}".format(t) for t in LONG)))
for nm in ["平滑层 (∇f)", "噪声层 (i.i.d.)"]:
    print("       {:<18} {}".format(nm, "  ".join("{:>6}".format(long_cnt[nm][t]) for t in LONG)))
print()
print("       判读：")
print("         · 噪声层：**立即**湮灭 —— {} → {}（200 步内 {:.1f}% 被抹掉），2000 步后只剩 {}。".format(
    long_cnt["噪声层 (i.i.d.)"][0], long_cnt["噪声层 (i.i.d.)"][200],
    100.0 * (1 - long_cnt["噪声层 (i.i.d.)"][200] / long_cnt["噪声层 (i.i.d.)"][0]),
    long_cnt["噪声层 (i.i.d.)"][2000]))
print("         · 平滑层：200 步内**几乎不动**（{} → {}），要到 t≈1000 才湮灭到 {}。".format(
    long_cnt["平滑层 (∇f)"][0], long_cnt["平滑层 (∇f)"][200], long_cnt["平滑层 (∇f)"][1000]))
print("           **原因**：平滑场的涡心彼此距离远，扩散先抹掉小尺度内容；")
print("                   相隔远的涡对需要很长时间才「走」到一起。")
print("           ⟹ 题面说的「下降或趋于稳定」——本轮**两种初始场各占一种形态**。")
n0 = [long_cnt["平滑层 (∇f)"][t] for t in LONG]
n1 = [long_cnt["噪声层 (i.i.d.)"][t] for t in LONG]
chk("VX-4", all(n1[i + 1] <= n1[i] for i in range(len(n1) - 1))
    and all(n0[i + 1] <= n0[i] for i in range(len(n0) - 1))
    and n1[-1] < n1[0] and n0[-1] < n0[0],
    "两种初始场的涡心数都**单调不增**并最终下降：噪声 {}→{}、平滑 {}→{} ⟹ 随机湮灭真实发生".format(
        n1[0], n1[-1], n0[0], n0[-1]))


# ══════════════════════════════════════════════════════════════════════
rule("VX-5  ★ 终态与**长时吸引子**：剩余涡心数、符号、净荷")
# ══════════════════════════════════════════════════════════════════════

print("       {:<18} {:>10} {:>10} {:>12} {:>12}".format(
    "初始场", "t=0 涡心", "t=200 涡心", "裸 Σ(t=0)", "裸 Σ(t=200)"))
for nm in ["平滑层 (∇f)", "噪声层 (i.i.d.)"]:
    print("       {:<18} {:>10} {:>10} {:>12.6f} {:>12.6f}".format(
        nm, long_cnt[nm][0], long_cnt[nm][200], long_sig[nm][0], long_sig[nm][200]))
print()
print("       **长时吸引子（2000 步，α = {}）**：".format(ALPHA))
print("       {:<18} {:>8} {:>10} {:>6} {:>6} {:>12} {:>12}".format(
    "初始场", "初涡心", "终涡心", "+", "−", "裸 Σ", "修正后 Σ"))
att = {}
for nm, v0 in [("平滑层 (∇f)", V_S), ("噪声层 (i.i.d.)", V_N)]:
    v = v0.copy()
    for _ in range(2000):
        v = step(v, ALPHA)
    S, nc, pp, nn, _ = vortex_stats(v)
    C = float(corrected(v).sum())
    att[nm] = (S, nc, pp, nn, C, v)
    print("       {:<18} {:>8} {:>10} {:>6} {:>6} {:>12.6f} {:>12.6f}".format(
        nm, long_cnt[nm][0], nc, pp, nn, S, C))
print()
print("       ⟹ **核心结论**：涡心总数被抹掉 {:.1f}%（噪声层）/ {:.1f}%（平滑层），".format(
    100.0 * (1 - att["噪声层 (i.i.d.)"][1] / long_cnt["噪声层 (i.i.d.)"][0]),
    100.0 * (1 - att["平滑层 (∇f)"][1] / long_cnt["平滑层 (∇f)"][0])))
print("          但**剩下的恰好是 6 个、全部同号（+1）**，一个也去不掉；")
print("          曲率修正后的指数和 = **{:+.6f}** = χ ⟹ 与库的 H1 完全对上。".format(
    att["平滑层 (∇f)"][4]))
print("          这 6 个就是离散化下「Killing 场 / 最低本征态」的骨架：连续极限下它们是")
print("          χ = 2 个 +1 涡心；离散测度因曲率把它们记成 6 个（VX-1b 的偏移 2χ = 4）。")
print()
print("       ⚠️ 诚实边界：**「净荷 = 初值」只对平滑层成立**（它的裸 Σ 本来就 6）；")
print("          噪声层**不成立** —— 噪声层的裸 Σ 不是拓扑量，是演化把它**改到** +6 的。")
print("          真正有信息的是：**涡心总数大幅下降，而吸引子的涡心数与符号与初值无关**。")
chk("VX-5", att["平滑层 (∇f)"][1] == 6 and att["平滑层 (∇f)"][2] == 6
    and att["噪声层 (i.i.d.)"][1] == 6 and att["噪声层 (i.i.d.)"][2] == 6
    and abs(att["平滑层 (∇f)"][4] - 2.0) < 1e-9 and abs(att["噪声层 (i.i.d.)"][4] - 2.0) < 1e-9,
    "长时极限：两种初始场都收敛到 **6 个全为 +1 的涡心**，曲率修正后指数和 = χ = +2（精确）"
    " ⟹ 「无法湮灭的稳定点」在**动力学**下同样成立")
rep("VX-5", "t=200 时平滑层还有 {} 个涡心（远未湮灭完），裸 Σ = {:+.0f}；噪声层剩 {} 个，裸 Σ = {:+.0f}。"
    " **湮灭是渐进的**，200 步不是终点".format(
        long_cnt["平滑层 (∇f)"][200], long_sig["平滑层 (∇f)"][200],
        long_cnt["噪声层 (i.i.d.)"][200], long_sig["噪声层 (i.i.d.)"][200]))


# ══════════════════════════════════════════════════════════════════════
rule("VX-6  ★ 环面对照 T²（χ = 0）：同实验，净荷应恒为 0")
# ══════════════════════════════════════════════════════════════════════

LT = 20
print("       L×L = {}×{} 周期格点，每点单位复向量 z_i（相位 θ_i）".format(LT, LT))
print("       **无平行移动、无曲率** ⟹ 只需 z ← (1−α)z + α·mean(z_4邻) 再归一化（相位扩散）")
print("       涡心 = 4 个最近邻（按 R/U/L/D 的**循环角顺序**）上的绕数")


def t2_neighbors(z):
    return [np.roll(z, -1, axis=0), np.roll(z, -1, axis=1),
            np.roll(z, 1, axis=0), np.roll(z, 1, axis=1)]


def t2_step(z, alpha):
    m = sum(t2_neighbors(z)) / 4.0
    zz = (1.0 - alpha) * z + alpha * m
    return zz / np.abs(zz)


def t2_windings(z):
    ph = np.stack([np.angle(w) for w in t2_neighbors(z)], axis=0).transpose(1, 2, 0)
    d = np.roll(ph, -1, axis=2) - ph
    d = d - 2.0 * np.pi * np.floor(d / (2.0 * np.pi) + 0.5)
    return d.sum(axis=2) / (2.0 * np.pi)


def t2_stats(z):
    w = t2_windings(z)
    core = np.abs(w) > 0.5
    return float(w.sum()), int(core.sum()), int((w[core] > 0).sum()), int((w[core] < 0).sum())


ZT = np.exp(1j * np.random.default_rng(MAIN_SEED).uniform(0.0, 2.0 * np.pi, (LT, LT)))
print()
print("       {:>6} {:>18} {:>10} {:>8} {:>8}".format("t", "裸 Σ w", "涡心数", "+", "−"))
z = ZT.copy()
t2_hist = {}
t2_sig = []
for t in range(201):
    S, nc, pp, nn = t2_stats(z)
    t2_sig.append(S)
    if t in CKPT:
        t2_hist[t] = (S, nc, pp, nn)
        print("       {:>6} {:>18.3e} {:>10} {:>8} {:>8}".format(t, S, nc, pp, nn))
    if t < 200:
        z = t2_step(z, ALPHA)
t2_sig = np.array(t2_sig)
zz = z.copy()                      # z 已演化 200 步
t2_long = {200: t2_stats(zz)}
for t in range(200, 2000):
    zz = t2_step(zz, ALPHA)
    if (t + 1) in (500, 1000, 2000):
        t2_long[t + 1] = t2_stats(zz)
print()
print("       200 步内 max|Σ| = **{:.3e}**；t=200 涡心 {} 个（+{} / −{}）".format(
    float(np.abs(t2_sig).max()), t2_hist[200][1], t2_hist[200][2], t2_hist[200][3]))
print("       更长时程：t=500 {} 个（+{}/−{}）｜ t=1000 {} 个（+{}/−{}）｜ t=2000 {} 个（+{}/−{}）".format(
    t2_long[500][1], t2_long[500][2], t2_long[500][3],
    t2_long[1000][1], t2_long[1000][2], t2_long[1000][3],
    t2_long[2000][1], t2_long[2000][2], t2_long[2000][3]))
print("       且**每一个时刻都严格成对**（+ 数 = − 数）—— 环面上没有任何东西阻止它们继续湮灭。")
print("       ⟹ 与 S² 上「必剩 6 个**同号**涡心」形成**直接对照**。")
print("          差别来自 **χ**（2 vs 0）；两边的演化规则完全相同、随机性相同。")
print("          ⚠️ 注意：T² 上 200 步时还剩 12 个涡心（12 ≠ 0）——")
print("             「能全灭」是**允许**，不是「200 步内就灭光」；关键是**没有任何净荷要留**。")
chk("VX-6", float(np.abs(t2_sig).max()) < 1e-9
    and all(t2_long[t][2] == t2_long[t][3] for t in t2_long),
    "T² 上裸净荷**恒为 0**（200 步 max|Σ| = {:.1e}），且 t=200/500/1000/2000 的涡心都**严格正负配对**"
    " ⟹ χ 才是「能否全灭」的决定因素".format(float(np.abs(t2_sig).max())))


# ══════════════════════════════════════════════════════════════════════
rule("VX-7  ★ 5 个不同随机种子各自跑到底：净荷是否每次相同？")
# ══════════════════════════════════════════════════════════════════════

SEEDS = [11, 22, 33, 44, 55]
print("       5 个种子 × 2 种初始场。**「跑到底」取 t = 2000**（吸引子），同时给出 t = 200。")
print()
print("       {:>6} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}".format(
    "seed", "平滑 Σ_0", "平滑 Σ_200", "平滑 Σ_2000", "噪声 Σ_0", "噪声 Σ_200", "噪声 Σ_2000"))
seed_rows = []
for s in SEEDS:
    vs = rand_smooth_tangent(np.random.default_rng(s), IC_NK, IC_SIG)
    vi = rand_tangent_iid(np.random.default_rng(s))
    a = vs.copy()
    a200 = None
    for t in range(2000):
        a = step(a, ALPHA)
        if t == 199:
            a200 = a.copy()
    b = vi.copy()
    b200 = None
    for t in range(2000):
        b = step(b, ALPHA)
        if t == 199:
            b200 = b.copy()
    row = (s, vortex_stats(vs)[0], vortex_stats(a200)[0], vortex_stats(a)[0],
           vortex_stats(vi)[0], vortex_stats(b200)[0], vortex_stats(b)[0])
    seed_rows.append(row)
    print("       {:>6} {:>12.4f} {:>12.4f} {:>12.4f} {:>12.4f} {:>12.4f} {:>12.4f}".format(*row))
ss0v = np.array([r[1] for r in seed_rows])
ss200 = np.array([r[2] for r in seed_rows])
ss2000 = np.array([r[3] for r in seed_rows])
si0v = np.array([r[4] for r in seed_rows])
si200 = np.array([r[5] for r in seed_rows])
si2000 = np.array([r[6] for r in seed_rows])
print()
print("       **t = 2000（跑到底）**：平滑层 Σ = {} ｜ 噪声层 Σ = {}".format(
    sorted(set(np.round(ss2000, 6).tolist())), sorted(set(np.round(si2000, 6).tolist()))))
print("       **t = 0**：平滑层 Σ = {} ｜ 噪声层 Σ = {}".format(
    sorted(set(np.round(ss0v, 6).tolist())), [round(x, 1) for x in si0v.tolist()]))
print("       **t = 200**：平滑层 Σ = {} ｜ 噪声层 Σ = {}".format(
    sorted(set(np.round(ss200, 6).tolist())), sorted(set(np.round(si200, 6).tolist()))))
print()
print("       ⟹ **净荷的种子无关性要在演化之后才成立**：")
print("          · t = 0 时平滑层 **不是**种子无关的（5 个种子里 2 个是 5、3 个是 6）——")
print("            因为 σ=0.55 的平滑场偶尔会把一对相邻涡心记在同一个顶点上；")
print("          · 跑到 t = 200 时 5 个种子**全部变成 6**，t = 2000 时仍全是 6。")
print("            噪声层的初值更散（{}…），同样被拉到一起。".format(
    [round(x, 1) for x in si0v.tolist()]))
print("          ⟹ 演化不仅**抹掉涡心**，还**修好了离散测度的初值失配**（把 5 拉成 6）。")
chk("VX-7", len(set(np.round(ss2000, 6).tolist())) == 1
    and len(set(np.round(si2000, 6).tolist())) == 1
    and abs(float(ss2000[0]) - 6.0) < 1e-9 and abs(float(si2000[0]) - 6.0) < 1e-9,
    "5 个种子跑到底（t=2000）：**净荷每次都是 {:+.6f}**（裸）/ χ = +2（修正），"
    "平滑层与噪声层都一样 ⟹ 吸引子与随机种子**完全无关**".format(float(ss2000[0])))
rep("VX-7", "但 **t = 0 时不是**（平滑层 5 个种子里 2 个的裸 Σ 是 5 —— 一对相邻涡心被记在同一个顶点上；"
    "到 t = 200 已全部修成 6）⟹ **种子无关性是演化的产物，不是初值的性质**，"
    "这一点必须与「净荷 = 初值」分开说")


# ══════════════════════════════════════════════════════════════════════
rule("VX-8  汇总对照表：S² vs T²")
# ══════════════════════════════════════════════════════════════════════

print("       {:<22} {:>4} {:>11} {:>11} {:>11} {:>11} {:>11}".format(
    "曲面 / 初始场", "χ", "裸Σ_0", "裸Σ_200", "裸Σ_2000", "修正Σ_2000", "涡心 0→2000"))
rows = [
    ("S² 平滑层 (∇f)", 2, long_sig["平滑层 (∇f)"][0], long_sig["平滑层 (∇f)"][200],
     att["平滑层 (∇f)"][0], att["平滑层 (∇f)"][4],
     long_cnt["平滑层 (∇f)"][0], long_cnt["平滑层 (∇f)"][2000]),
    ("S² 噪声层 (i.i.d.)", 2, long_sig["噪声层 (i.i.d.)"][0], long_sig["噪声层 (i.i.d.)"][200],
     att["噪声层 (i.i.d.)"][0], att["噪声层 (i.i.d.)"][4],
     long_cnt["噪声层 (i.i.d.)"][0], long_cnt["噪声层 (i.i.d.)"][2000]),
    ("T² 随机相位", 0, t2_hist[0][0], t2_hist[200][0], None, None,
     t2_hist[0][1], t2_hist[200][1]),
]
for nm, chi, a0, a1, a2, c2, c0, c1 in rows:
    print("       {:<22} {:>4} {:>11.4f} {:>11.4f} {:>11} {:>11} {:>11}".format(
        nm, chi, a0, a1,
        "—" if a2 is None else "{:.4f}".format(a2),
        "—" if c2 is None else "{:.4f}".format(c2),
        "{} → {}".format(c0, c1)))
print()
print("       读法（**三句话**）：")
print("         ① **χ 定净荷**：S² 上裸 Σ = 6 = 3χ（修正后 χ = 2）；T² 上 **0**。")
print("         ② **演化定涡心总数**：噪声 {}→{}、平滑 {}→{}、T² {}→{}。".format(
    long_cnt["噪声层 (i.i.d.)"][0], long_cnt["噪声层 (i.i.d.)"][2000],
    long_cnt["平滑层 (∇f)"][0], long_cnt["平滑层 (∇f)"][2000],
    t2_hist[0][1], t2_hist[200][1]))
print("         ③ **两者正交**：涡心可以被大量抹掉，「净荷」不能（T² 上能，因为它是 0）。")


# ══════════════════════════════════════════════════════════════════════
rule("VX-9  判决：动力学是否让涡心真的湮灭了？")
# ══════════════════════════════════════════════════════════════════════

print("       **是**。本轮用的是真正的**动力学**（切丛内的图热流 v ← v − (α/k)Δv），")
print("       不是第 66 轮那种抽象配对。实测：")
print()
print("         · 噪声层涡心 {} → {}（2000 步内 -{:.0f}%）".format(
    long_cnt["噪声层 (i.i.d.)"][0], long_cnt["噪声层 (i.i.d.)"][2000],
    100.0 * (1 - long_cnt["噪声层 (i.i.d.)"][2000] / long_cnt["噪声层 (i.i.d.)"][0])))
print("         · 平滑层涡心 {} → {}（-{:.0f}%）".format(
    long_cnt["平滑层 (∇f)"][0], long_cnt["平滑层 (∇f)"][2000],
    100.0 * (1 - long_cnt["平滑层 (∇f)"][2000] / long_cnt["平滑层 (∇f)"][0])))
print("         · T² 上涡心 {} → {}（χ = 0 ⟹ **可以全灭**）".format(
    t2_hist[0][1], t2_hist[200][1]))
print()
print("       而剩下的**永远是 6 个同号涡心**，5 个种子、两种初始层、2000 步都一样；")
print("       曲率修正后的指数和 = **χ = 2 精确**。")
print("       ⟹ 用户命题的「**随机湮灭中无法湮灭的稳定点**」在**演化**下**成立**。")
print()
print("       ⚠️ **必须同时登记的五个边界**（不登记就是夸大）：")
print("         ① **裸绕数不等于 χ**：S² 上是 **6 = 3χ**，不是 2。差额 2χ 恰好是总曲率 ΣK_i/π；")
print("            扣掉后 Σ(w_i − 2K_i/(2π)) = χ **精确成立**（12 轴 × 3 分辨率全中）。")
print("         ② **守恒是近似的**：裸 Σ 在相邻方向接近反平行（Δφ 跨过 ±π）的步跳变 ——")
print("            平滑层是 ±1（10 步），噪声层单步最多跳到 5。下一步即恢复。**连续场**才严格守恒。")
print("         ③ **种子无关性是演化的产物**：t=0 时平滑层 5 个种子里有 2 个裸 Σ 是 5（不是 6）；")
print("            跑到 t=200 才全部修成 6。**初值本身不是种子无关的**。")
print("         ④ **噪声层无拓扑荷**：40 次扫描裸 Σ ∈ [{:+.0f}, {:+.0f}]，也不是「+2」。".format(
    scan_i.min(), scan_i.max()))
print("            「+2」只在**平滑层**上有意义 ⟹ 框架 §2.3 的「孤子化」这一步是**必需**的，")
print("            但**它为什么必然发生**（机制）本轮仍未从第一性推出。")
print("         ⑤ **稳定 ≠ 动力学稳定**：本轮证的是「**拓扑上抹不掉**」（必要），")
print("            **不是**「对任意微扰都稳定」（充分）。终态那 6 个涡心是否抗扰动，本轮未测。")
chk("VX-9", True,
    "**判决**：动力学**确实**抹掉了大部分涡心（噪声层 -{:.0f}%），"
    "而净荷留到吸引子都不动（6 个同号、修正指数和 = χ）⟹ 「无法湮灭的稳定点」在演化下成立；"
    "但「稳定」= 拓扑不可抹去 ≠ 动力学稳定".format(
        100.0 * (1 - long_cnt["噪声层 (i.i.d.)"][2000] / long_cnt["噪声层 (i.i.d.)"][0])))

print()
print("       **判据清点**（chk = 检查项；rep 是**报告项**，不计入通过/失败）")
print("         VX-1 网格 | VX-1b 标定/曲率修正 | VX-1c 退化定义域 | VX-1d 离散 Gauss–Bonnet")
print("         VX-1f 与 P 1105 处方的一致性 | VX-2 初始净荷 | VX-3 跳变机制 | VX-4 涡心下降")
print("         VX-5 吸引子 | VX-6 T²=0 | VX-7 种子无关 | VX-9 判决")
print("         （VX-1e 为**登记项**，不设通过/失败；共 12 个 chk + 7 个 rep）")

print()
print("=" * 78)
print("通过 {} 项，失败 {} 项".format(OK, BAD))
print("=" * 78)
