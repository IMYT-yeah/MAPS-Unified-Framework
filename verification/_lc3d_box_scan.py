# -*- coding: utf-8 -*-
"""2×2×2 盒子 λ_c 扫描 (A1): χ 峰定位"""
import numpy as np
import _lc3d_box as M

cube_faces, n = M.build_grid(2, 2, 2)
print(f"=== 2×2×2: n={n} 面, N_c={len(cube_faces)}, 2^{n}={2**n:.2e} 态 ===", flush=True)

def scan(lams, chi, sweeps, seed=1, warm=True):
    res = []
    A0 = None
    for lam in lams:
        Ws = M.make_mpo(cube_faces, n, lam)
        E, A = M.dmrg1(Ws, n, chi=chi, max_sweeps=sweeps, seed=seed, verbose=False, A0=A0)
        ac = M.expect_ac(A, cube_faces, n)
        res.append((lam, E, ac))
        print(f"  λ={lam:.3f}: E={E:+.6f} ⟨A_c⟩={ac:.4f}", flush=True)
        if warm:
            A0 = A
    return np.array(res)

# 粗扫 [0, 0.6] 步 0.05
lams_coarse = np.round(np.arange(0.0, 0.601, 0.05), 3)
arr = scan(lams_coarse, chi=8, sweeps=20, seed=1)
np.save('_lc3d_box_222_coarse.npy', arr)

# χ 峰
lp, ch = M.chi_peak(arr[:, 0], arr[:, 2])
print(f"\n⟹ 粗扫 χ 峰 λ_χ={lp:.3f} χ_max={ch:.3f}", flush=True)

# 峰区细扫
if 0.0 <= lp <= 0.6:
    lo = max(0.0, lp - 0.08)
    hi = min(0.6, lp + 0.08)
    lams_fine = np.round(np.arange(lo, hi + 0.011, 0.02), 3)
    arr2 = scan(lams_fine, chi=8, sweeps=20, seed=1, warm=True)
    np.save('_lc3d_box_222_fine.npy', arr2)
    lp2, ch2 = M.chi_peak(arr2[:, 0], arr2[:, 2])
    print(f"⟹ 细扫 χ 峰 λ_χ={lp2:.3f} χ_max={ch2:.3f}", flush=True)
print("扫描完成", flush=True)
