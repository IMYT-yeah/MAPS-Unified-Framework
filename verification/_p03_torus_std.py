# -*- coding: utf-8 -*-
"""
P0-3b 辅助: 对称约定 (J_A=J_B=1) 环面 toric code + 横向场
H = -ΣA_v - ΣB_p - h ΣX_e   (标准文献约定, 对标 h_c≈0.328)
框架约定 (0.5 系数) 的结果在 _p03_torus.py; 本脚本检验两约定的对应关系.
"""
import numpy as np, time
from _p03_torus import TorusLattice, crossing

class SymTorus(TorusLattice):
    def apply_H(self, v, h):
        """H = -ΣA_v - ΣB_p - hΣX_e (对称约定, 无 0.5 系数)"""
        out = np.zeros_like(v)
        for m in self.vertices:
            out[self.idx ^ m] -= v
        for keep in self.face_keep:
            out[keep] -= v[keep]
        for e in range(self.n):
            out[self.idx ^ (1 << e)] -= h * v
        return out

    def eigs(self, h, k=2, tol=1e-7, maxiter=3000):
        from scipy.sparse.linalg import LinearOperator, eigsh
        n = self.N
        A = LinearOperator((n, n), matvec=lambda x: self.apply_H(x, h), dtype=np.float64)
        evals, evecs = eigsh(A, k=k, which="SA", tol=tol, maxiter=maxiter)
        return evals, evecs


def scan_std(nx, ny, hs):
    lat = SymTorus(nx, ny)
    print(f"\n--- 环面 {nx}x{ny} [对称约定 J_A=J_B=1]: {lat.n} 边, 2^{lat.n}={lat.N:,} 态 ---", flush=True)
    ms, E0s = [], []
    for h in hs:
        t0 = time.time()
        evals, evecs = lat.eigs(h, k=2)
        E0, v = float(evals[0]), evecs[:, 0]
        dg = float(evals[1] - evals[0])
        m = lat.order_param(v)
        ms.append(m); E0s.append(E0)
        print(f"  h={h:.3f}: E0={E0:+.4f} m=⟨X⟩={m:.4f} Δ={dg:.4f} ({time.time()-t0:.0f}s)", flush=True)
    kc = crossing(hs, ms)
    print(f"  ⟹ h*(m=0.5) = {kc:.4f}" if kc else "  ⟹ 无交叉", flush=True)
    return ms, E0s, kc


if __name__ == "__main__":
    print("="*70)
    print("对称约定 (J_A=J_B=1): H = -ΣA_v - ΣB_p - hΣX_e 对标文献 h_c≈0.328")
    print("="*70)
    hs = [0.0, 0.10, 0.20, 0.25, 0.28, 0.30, 0.32, 0.34, 0.36, 0.40, 0.45, 0.50]
    results = {}
    for (nx, ny) in [(2,2), (2,3), (3,3)]:
        ms, E0s, kc = scan_std(nx, ny, hs)
        results[(nx, ny)] = kc
    print("\n" + "="*70)
    print("有限尺寸标度 (对称约定)")
    print("="*70)
    pts = []
    for (nx, ny), kc in results.items():
        if kc is not None:
            L = (nx*ny) ** 0.5
            pts.append((1.0/L, kc))
            print(f"  环面 {nx}x{ny}: L={L:.3f}, h*={kc:.4f}")
    if len(pts) >= 3:
        xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
        A = np.vstack([xs, np.ones_like(xs)]).T
        (slope, intercept), *_ = np.linalg.lstsq(A, ys, rcond=None)
        print(f"\n  线性拟合: h*(L) = {intercept:.4f} + {slope:.3f}/L")
        print(f"  ⟹ h_c(∞) = {intercept:.4f} vs 文献 0.328 → 偏差 {(intercept-0.328)/0.328*100:+.1f}%")
