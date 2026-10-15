# -*- coding: utf-8 -*-
"""
甲-3（第 102 轮）：2+1D toric code + 横向 X 场 —— 相变点的精确值

【模型】（与 `_p03_torus.py` 严格同约定，故结果可直接对照）
    H(h) = −J Σ_v A_v − K Σ_p B_p − h Σ_e X_e
    · 每条边是 qubit；A_v = Π_{e∋v} X_e（顶点 4 边）；B_p = Π_{e∈∂p} Z_e（面 4 边）
    · 环面 nx×ny：顶点 nx·ny 个、面 nx·ny 个、边 n = 2·nx·ny
    · 当年用 J=K=1、扫 h；文档自注「X 场版本，文献 h_c≈0.328 同约定」

【本轮关键技术：A_v = +1 扇区】
    ⚠️ **`[A_v, H] = 0`**（A_v 与 ΣB_p 在两个共享边上各有一个 X-Z 反对易，净对易；
       与 ΣX_e 显然对易）⟹ A_v 是好量子数，且 **J 项在扇区内退化为常数** -J·V。
    ⟹ 相变**不依赖 J**（这是本轮的一个结构性结论，见报告）。
    ⟹ 在**X 基**下 A_v 对角 ⟹ 扇区 = {w ∈ {0,1}^n : Π_{e∋v}(-1)^{w_e} = +1 ∀v}
       = GF(2) 零空间，维数 2^{n − rank(C)}。**2×2→32、3×3→1024、4×4→2^17**
       （全空间分别是 2^8／2^18／2^32 ⟹ **4×4 以前根本做不了**）。

【X 基下的 H（本文件实现）】
    对角：−J·V_periodic − h·S(w)，  S(w) = Σ_e (−1)^{w_e}
    非对角：−K·Σ_p |w ⊕ f_p⟩（f_p = 面 p 的边掩码）
⟹ 任意 X 算符的矩都是**对角**的 ⟹ Binder 累积量极便宜（不需额外内积）。

【序参量】
    m = (1/n) Σ_e ⟨X_e⟩（对角的"横向磁化"）
    ⚠️ 论文已记：m 的**交叉点 m=0.5 不是相变点**（"半极化点"）。本轮**不**用 m=0.5，
       改用 **Binder 累积量 U = 1 − ⟨m⁴⟩/(3⟨m²⟩²) 的跨尺寸交叉**（尺寸无关点 = h_c）。
"""
import sys
import time
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh


# ------------------------------------------------------------------ 掩码
def build_torus_masks(nx, ny, verbose=False):
    n = 2 * nx * ny
    hb = lambda i, j: i * ny + j
    vb = lambda i, j: nx * ny + i * ny + j
    vmasks, fmasks = [], []
    for i in range(nx):
        for j in range(ny):
            vmasks.append((1 << hb((i - 1) % nx, j)) | (1 << hb(i, j))
                          | (1 << vb(i, (j - 1) % ny)) | (1 << vb(i, j)))
    for i in range(nx):
        for j in range(ny):
            fmasks.append((1 << hb(i, j)) | (1 << hb(i, (j + 1) % ny))
                          | (1 << vb(i, j)) | (1 << vb((i + 1) % nx, j)))
    if verbose:
        print("  {}×{}: n={} 边, V={} 顶点, P={} 面".format(nx, ny, n, len(vmasks), len(fmasks)))
    return n, vmasks, fmasks


# ------------------------------------------------------------------ GF(2) 零空间
def gf2_nullspace(rows, ncols):
    """rows: 约束行（每行一个 bitmask，表示涉及哪些列）。
    先化 RREF（**完整向上消元**），再由自由列构造零空间基。
    ⚠️ 关键：只做"行阶梯"而不做向上消元，则逐个自由列 XOR 时会**互相污染其他 pivot 列**
       （第一版就是这么写的，靠下面的自检 assert 兜住）。
    返回 (basis: list[int], rank)。
    """
    R = [r for r in rows if r]
    if not R:
        return [1 << c for c in range(ncols)], 0
    r = 0
    pivots = []
    for c in range(ncols):
        sel = None
        for i in range(r, len(R)):
            if (R[i] >> c) & 1:
                sel = i
                break
        if sel is None:
            continue
        R[r], R[sel] = R[sel], R[r]
        for i in range(len(R)):                 # ← 向上消元：所有非主元行都消掉 c 列
            if i != r and ((R[i] >> c) & 1):
                R[i] ^= R[r]
        pivots.append(c)
        r += 1
        if r == len(R):
            break
    rank = len(pivots)
    pivset = set(pivots)
    free = [c for c in range(ncols) if c not in pivset]
    basis = []
    for f in free:
        v = 1 << f
        for i, p in enumerate(pivots):
            if (R[i] >> f) & 1:
                v |= 1 << p
        for rr in rows:                          # 自检：必须满足全部原始约束
            if bin(v & rr).count("1") & 1:
                raise AssertionError("零空间基向量不满足约束 —— GF(2) 消元有误")
        basis.append(v)
    return basis, rank


# ------------------------------------------------------------------ 扇区模型
class SectorToric:
    def __init__(self, nx, ny, J=1.0, K=1.0):
        self.nx, self.ny = nx, ny
        self.J, self.K = J, K
        self.n, self.vmasks, self.fmasks = build_torus_masks(nx, ny)
        basis, rank = gf2_nullspace(self.vmasks, self.n)
        self.rank, self.nullity = rank, len(basis)
        self.dim = 1 << self.nullity
        if self.dim > 1 << 21:
            raise MemoryError("扇区维数 {} 过大".format(self.dim))
        # 枚举扇区（code → 构型）
        conf = np.zeros(self.dim, dtype=np.int64)
        for code in range(self.dim):
            w = 0
            c = code
            k = 0
            while c:
                if c & 1:
                    w ^= basis[k]
                c >>= 1
                k += 1
            conf[code] = w
        self.conf = conf
        self.index = {int(w): i for i, w in enumerate(conf)}
        assert len(self.index) == self.dim, "扇区内出现重复构型 —— 基不独立"
        # 预计算对角项与翻转索引
        self.Sw = np.zeros(self.dim)            # S(w) = Σ_e (-1)^{w_e}
        for i, w in enumerate(conf):
            self.Sw[i] = self.n - 2 * bin(int(w)).count("1")
        self.flip = np.zeros((self.dim, len(self.fmasks)), dtype=np.int64)
        for p, fm in enumerate(self.fmasks):
            for i, w in enumerate(conf):
                self.flip[i, p] = self.index[int(w) ^ fm]   # ⚠️ 若报 KeyError 说明 f_p 不保持扇区

    def H(self, h):
        diag = -self.J * len(self.vmasks) - h * self.Sw
        fl = self.flip
        K = self.K
        dim = self.dim

        def mv(v):
            out = diag * v
            acc = np.zeros(dim)
            for p in range(fl.shape[1]):
                acc += v[fl[:, p]]
            out -= K * acc
            return out

        return LinearOperator((dim, dim), matvec=mv, dtype=np.float64)

    def observables(self, v):
        """返回 (m, m2, m4)：m = Σ_e X_e / n（对角）"""
        p = v ** 2
        x = self.Sw / self.n
        m = float(p @ x)
        m2 = float(p @ (x ** 2))
        m4 = float(p @ (x ** 4))
        return m, m2, m4


def binder(m2, m4):
    return 1.0 - m4 / (3.0 * m2 ** 2) if m2 > 1e-12 else np.nan


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "verify"
    if mode == "verify":
        print("=" * 84)
        print("扇区构造自检：维数 vs 2^(n−rank)（与全空间 2^n 对照）")
        print("=" * 84)
        for nx, ny in [(2, 2), (2, 3), (3, 3), (3, 4), (4, 4)]:
            n, vm, fm = build_torus_masks(nx, ny)
            basis, rank = gf2_nullspace(vm, n)
            print("  {}×{}: n={:>2} V={:>2} rank={:>2} nullity={:>2} ⟹ 扇区维={:>8} "
                  "（全空间 2^n = {:.3e}，压缩 {:.1e}×）".format(
                      nx, ny, n, len(vm), rank, len(basis), 1 << len(basis),
                      2.0 ** n, 2.0 ** n / (1 << len(basis))))
