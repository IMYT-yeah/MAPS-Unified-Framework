# -*- coding: utf-8 -*-
"""3+1D 弦网 λ_c 相变 — 细扫 [0, 0.6] 定位 χ 峰 (P1-3)"""
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh
# 从 _stringnet_lc.py 提取函数定义 (跳过主程序)
_src = open('_stringnet_lc.py', encoding='utf-8').read()
exec(_src[:_src.index('print("="*80)')])

def run_system_fine(nx, ny, nz, lams, k=2, tol=1e-9, maxiter=600):
    cube_faces, n = build_grid(nx, ny, nz)
    N = 1 << n
    idx = np.arange(N, dtype=np.int64)
    flip = np.array([idx ^ (1 << f) for f in range(n)])
    d = diag_A(cube_faces, n, N, idx)
    print(f"\n=== {nx}×{ny}×{nz}: n={n} 面, N={N:,} 态, N_c={len(cube_faces)} ===", flush=True)
    res = []
    for lam in lams:
        def matvec(v, lam=lam):
            out = d*v
            for f in range(n):
                out[flip[f]] -= lam*v
            return out
        Aop = LinearOperator((N, N), matvec=matvec, dtype=np.float64)
        ev, evc = eigsh(Aop, k=k, which='SA', tol=tol, maxiter=maxiter)
        ac = order_param(cube_faces, n, N, idx, evc[:, 0])
        res.append((lam, ev[0], ev[1]-ev[0], ac))
        print(f"  λ={lam:.3f}: E0={ev[0]:+.4f}, Δ={ev[1]-ev[0]:.4f}, ⟨A_c⟩={ac:.4f}", flush=True)
    return np.array(res)

def chi_peak_internal(lams, acs):
    """χ 峰 (内部中心差分, 排除边界)"""
    chi = -np.gradient(acs, lams)
    i = int(np.argmax(chi))
    return float(lams[i]), float(chi[i]), i, len(lams)

if __name__ == "__main__":
    print("="*80)
    print("3+1D 弦网 λ_c 相变 — 细扫定位 χ 峰 (P1-3)")
    print("="*80)
    lams = np.round(np.arange(0.0, 0.601, 0.02), 3)
    for (nx, ny, nz) in [(2,1,1), (3,1,1), (2,2,1)]:
        arr = run_system_fine(nx, ny, nz, lams)
        lp, ch, i, Ln = chi_peak_internal(arr[:, 0], arr[:, 3])
        L = (nx*ny*nz)**(1.0/3.0)
        print(f"  ⟹ {nx}x{ny}x{nz}: L={L:.2f}, χ 峰 λ_χ={lp:.3f}, χ_max={ch:.3f} (峰在边界?" + ("是" if i<=1 or i>=Ln-2 else "否") + ")")
