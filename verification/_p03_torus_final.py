# -*- coding: utf-8 -*-
"""
P0-3b 终版: 环面 κ_c 精确化
(1) 框架约定 (0.5 系数) 补 2x4 环面 (65536 态, L=2.828) → 4 点 FSS: 2x2/2x3/2x4/3x3
(2) 对称约定 (J_A=J_B=1) 2x2/2x3/3x3 → 直接对标文献 h_c≈0.328
说明: 3x4 环面 (1677 万态) 全空间对角化每 matvec ~15-25s, 需 MPS/DMRG, 超出本环境; 诚实标注.
"""
import numpy as np, time
from _p03_torus import TorusLattice, crossing

def scan_fw(nx, ny, kappas, method="eigsh"):
    """框架约定 (0.5 系数)"""
    lat = TorusLattice(nx, ny)
    print(f"\n--- 环面 {nx}x{ny} [框架约定]: {lat.n} 边, 2^{lat.n}={lat.N:,} 态 ---", flush=True)
    ms, E0s = [], []
    for k in kappas:
        t0 = time.time()
        if method == "eigsh":
            evals, evecs = lat.eigs(k, k=2)
            E0, v = float(evals[0]), evecs[:, 0]
            dg = float(evals[1]-evals[0])
        else:
            E0, v = lat.ground_state(k, 300)
            dg = None
        m = lat.order_param(v)
        ms.append(m); E0s.append(E0)
        print(f"  κ={k:.3f}: E0={E0:+.4f} m=⟨X⟩={m:.4f}" + (f" Δ={dg:.4f}" if dg is not None else "") + f" ({time.time()-t0:.0f}s)", flush=True)
    kc = crossing(kappas, ms)
    print(f"  ⟹ κ*(m=0.5) = {kc:.4f}" if kc else "  ⟹ 无交叉", flush=True)
    return ms, kc

def scan_std(nx, ny, hs):
    """对称约定 (J_A=J_B=1)"""
    from _p03_torus_std import SymTorus
    lat = SymTorus(nx, ny)
    print(f"\n--- 环面 {nx}x{ny} [对称约定]: {lat.n} 边, 2^{lat.n}={lat.N:,} 态 ---", flush=True)
    ms, E0s = [], []
    for h in hs:
        t0 = time.time()
        evals, evecs = lat.eigs(h, k=2)
        E0, v = float(evals[0]), evecs[:, 0]
        dg = float(evals[1]-evals[0])
        m = lat.order_param(v)
        ms.append(m); E0s.append(E0)
        print(f"  h={h:.3f}: E0={E0:+.4f} m=⟨X⟩={m:.4f} Δ={dg:.4f} ({time.time()-t0:.0f}s)", flush=True)
    kc = crossing(hs, ms)
    print(f"  ⟹ h*(m=0.5) = {kc:.4f}" if kc else "  ⟹ 无交叉", flush=True)
    return ms, kc

def fss(points, label, lit=None):
    print(f"\n--- FSS 外推: {label} ---")
    pts = []
    for (nx, ny), kc in points.items():
        if kc is not None:
            L = (nx*ny)**0.5
            pts.append((1.0/L, kc))
            print(f"  {nx}x{ny}: L={L:.3f}, κ*={kc:.4f}")
    if len(pts) >= 3:
        xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
        A = np.vstack([xs, np.ones_like(xs)]).T
        (slope, intercept), *_ = np.linalg.lstsq(A, ys, rcond=None)
        print(f"  线性拟合: κ*(L) = {intercept:.4f} + {slope:.3f}/L")
        print(f"  ⟹ κ_c(∞) = {intercept:.4f}")
        if lit:
            print(f"  vs 文献 {lit}: 偏差 {(intercept-lit)/lit*100:+.1f}%")
        return intercept, slope
    return None, None


if __name__ == "__main__":
    print("="*70)
    print("P0-3b (候选 C): 环面 κ_c 精确化 — 终版")
    print("="*70)

    # (1) 框架约定: 2x2/2x3 已有 (0.1942/0.2017); 补 2x4
    kappas = [0.0, 0.05, 0.10, 0.15, 0.18, 0.20, 0.22, 0.25, 0.30, 0.35, 0.40, 0.50]
    ms24, kc24 = scan_fw(2, 4, kappas)
    fw = {(2,2): 0.1942, (2,3): 0.2017, (2,4): kc24, (3,3): 0.1994}
    kc_fw, slope_fw = fss(fw, "框架约定 (0.5 系数)")

    # (2) 对称约定: 2x2/2x3/3x3
    hs = [0.0, 0.10, 0.20, 0.25, 0.28, 0.30, 0.32, 0.34, 0.36, 0.40, 0.45, 0.50]
    std = {}
    ms, kc = scan_std(2, 2, hs); std[(2,2)] = kc
    ms, kc = scan_std(2, 3, hs); std[(2,3)] = kc
    ms, kc = scan_std(3, 3, hs); std[(3,3)] = kc
    kc_std, slope_std = fss(std, "对称约定 (J_A=J_B=1)", lit=0.328)

    print("\n" + "="*70)
    print("汇总")
    print("="*70)
    print(f"框架约定: κ_c(∞) ≈ {kc_fw:.4f} (环面, 4 点 FSS)  | 开边界 P0-3: 0.23–0.27 | 文献对标见对称约定")
    print(f"对称约定: h_c(∞) ≈ {kc_std:.4f} vs 文献 0.328")
