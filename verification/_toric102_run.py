# -*- coding: utf-8 -*-
"""
甲-3 驱动器（第 102 轮）：扇区 vs 全空间交叉验证 + h 扫描

用法：
    python _toric102_run.py verify                # 扇区 vs 全空间（E0, m 逐点对比）
    python _toric102_run.py scan <nx> <ny> <h_lo> <h_hi> <dh> <tag>
"""
import sys
import time
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh

from _toric102 import build_torus_masks, SectorToric, binder


# ------------------------------------------------------------------ 全空间参照（不限制 A_v 扇区）
class FullToric:
    """H = −J Σ A_v − K Σ B_p − h Σ X_e 在 2^n 全空间（X 基）。
    ⚠️ 仅供小尺寸交叉验证；2×2=256、2×3=4096、3×3=262144 可用，4×4 不可用。
    """

    def __init__(self, nx, ny, J=1.0, K=1.0):
        self.nx, self.ny, self.J, self.K = nx, ny, J, K
        self.n, self.vmasks, self.fmasks = build_torus_masks(nx, ny)
        self.dim = 1 << self.n
        # A_v 对角项：A_v(w) = Π_{e∈v}(−1)^{w_e} = (−1)^{popcount(w & vmask)}
        S = np.zeros(self.dim)
        for w in range(self.dim):
            s = 0
            for vm in self.vmasks:
                s += -1.0 if (bin(w & vm).count("1") & 1) else 1.0
            S[w] = s
        self.Asum = S                                  # Σ_v A_v
        xs = np.array([self.n - 2 * bin(w).count("1") for w in range(self.dim)], float)
        self.xsum = xs                                 # Σ_e x_e（= Σ_e X_e 的本征值）

    def H(self, h):
        diag = -self.J * self.Asum - h * self.xsum
        n = self.n
        fm = self.fmasks
        K = self.K
        dim = self.dim

        def mv(v):
            out = diag * v
            # 每个面翻转 4 条边 ⟹ 索引 = w ^ fmask
            idx = np.arange(dim)
            for f in fm:
                out -= K * v[idx ^ f]
            return out

        return LinearOperator((dim, dim), matvec=mv, dtype=np.float64)

    def obs(self, v):
        p = v ** 2
        x = self.xsum / self.n
        return float(p @ x), float(p @ x ** 2), float(p @ x ** 4)


def solve(model, h, k=2):
    H = model.H(h)
    ev, evec = eigsh(H, k=k, which="SA", tol=1e-10, maxiter=5000)
    order = np.argsort(ev)
    return float(ev[order[0]]), evec[:, order[0]], (float(ev[order[1]] - ev[order[0]]) if k > 1 else None)


def mps_overlap(a, b):
    return float(abs(np.dot(a, b)))


# ------------------------------------------------------------------ 验证
def do_verify():
    print("=" * 92)
    print("扇区 vs 全空间 交叉验证（H = −ΣA_v − ΣB_p − hΣX_e）")
    print("=" * 92)
    bad = 0
    for nx, ny in [(2, 2), (2, 3), (3, 3)]:
        full = FullToric(nx, ny)
        sec = SectorToric(nx, ny)
        print("\n--- {}×{} : 全空间 {} ：扇区 {} ---".format(nx, ny, full.dim, sec.dim))
        print("{:>7} | {:>18} {:>10} | {:>18} {:>10} | {:>9} {:>9}".format(
            "h", "E0(全空间)", "m(全)", "E0(扇区)", "m(扇区)", "ΔE0", "Δm"))
        for h in [0.0, 0.2, 0.3, 0.35, 0.5, 1.0]:
            E1, v1, _ = solve(full, h, k=1)
            m1 = full.obs(v1)[0]
            E2, v2, _ = solve(sec, h, k=1)
            m2 = sec.observables(v2)[0]
            dE, dm = abs(E1 - E2), abs(m1 - m2)
            flag = ""
            if dE > 1e-6 or dm > 1e-5:
                flag = "  ⚠️"
                bad += 1
            print("{:>7.3f} | {:>18.10f} {:>10.6f} | {:>18.10f} {:>10.6f} | {:>9.2e} {:>9.2e}{}".format(
                h, E1, m1, E2, m2, dE, dm, flag), flush=True)
    print()
    print("⟹ 交叉验证{}".format("全部通过 ✓" if bad == 0 else "有 {} 项不符 ✗".format(bad)))
    return bad


# ------------------------------------------------------------------ 扫描
def do_scan(nx, ny, lo, hi, dh, tag):
    t0 = time.time()
    sec = SectorToric(nx, ny)
    hs = np.round(np.arange(lo, hi + 1e-9, dh), 5)
    print("=== {}×{} : 扇区维 {}（全空间 2^{} = {:.3e}）｜{} 点 h∈[{},{}] step {} ===".format(
        nx, ny, sec.dim, sec.n, 2.0 ** sec.n, len(hs), lo, hi, dh), flush=True)
    print("{:>8} {:>16} {:>10} {:>10} {:>10} {:>8} {:>10} {:>8}".format(
        "h", "E0", "Δ=E1−E0", "m", "<m²>", "Binder", "F", "s"))
    rows = []
    prev = None
    for h in hs:
        E0, v, dg = solve(sec, h, k=2)
        m, m2, m4 = sec.observables(v)
        U = binder(m2, m4)
        F = mps_overlap(prev, v) if prev is not None else np.nan
        rows.append((h, E0, dg, m, m2, m4, U, F))
        print("{:>8.4f} {:>16.9f} {:>10.5f} {:>10.5f} {:>10.5f} {:>8.4f} {:>10.6f} {:>8.0f}".format(
            h, E0, dg if dg else 0, m, m2, U, F, time.time() - t0), flush=True)
        prev = v
    arr = np.array(rows)
    np.savez("_toric102_{}.npz".format(tag), rows=arr, dims=(nx, ny), dim=sec.dim)
    print("⟹ 已保存 _toric102_{}.npz".format(tag), flush=True)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "verify"
    if mode == "verify":
        do_verify()
    elif mode == "scan":
        do_scan(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]),
                float(sys.argv[5]), float(sys.argv[6]), sys.argv[7])
