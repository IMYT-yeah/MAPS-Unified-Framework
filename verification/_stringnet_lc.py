# -*- coding: utf-8 -*-
"""
3+1D 弦网 λ_c 相变 (P1-3) — 凝聚相稳定性边界
模型: H(λ) = -Σ_c A_c - λ Σ_f X_f   (A_c = 立方体 6 面 Z 乘积, X_f = 面翻转)
物理: λ=0 弦网凝聚 (拓扑序) → λ→∞ 面极化 (平凡相) — 临界点 λ_c = 冷凝点
      (框架语言【原文 54-55】: 相变 = 通量场湍流态↔各向同性稳态的冷凝)
方法: 序参量 ⟨A_c⟩(λ) + 磁化率 χ = -d⟨A_c⟩/dλ (峰 → λ_c(L)) + 能隙 Δ(λ)
      + 1/L 有限尺寸标度外推 λ_c(∞)
系统: 2×1×1 (11 面 2048 精确) / 3×1×1 (16 面 65536) / 2×2×1 板 (20 面 1e6)
      / 4×1×1 (21 面 2.1e6) — 全部 Lanczos (LinearOperator 免建矩阵)
"""
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh

def build_grid(nx, ny, nz):
    """nx×ny×nz 立方体阵列 → 每立方体 6 面索引 [x-,x+,y-,y+,z-,z+], 总面数 n"""
    cells = [(i, j, k) for i in range(nx) for j in range(ny) for k in range(nz)]
    face_of = {}
    cube_faces = []
    dirs = [(-1,0,0,'xm','xp'), (1,0,0,'xp','xm'), (0,-1,0,'ym','yp'),
            (0,1,0,'yp','ym'), (0,0,-1,'zm','zp'), (0,0,1,'zp','zm')]
    for (i, j, k) in cells:
        cf = []
        for (di, dj, dk, dn, on) in dirs:
            nb = (i+di, j+dj, k+dk)
            if nb in cells and (nb[0], nb[1], nb[2], on) in face_of:
                cf.append(face_of[(nb[0], nb[1], nb[2], on)])
            else:
                key = (i, j, k, dn)
                face_of[key] = len(face_of)
                cf.append(face_of[key])
        cube_faces.append(cf)
    return cube_faces, len(face_of)

def diag_A(cube_faces, n, N, idx):
    """-Σ_c A_c 对角 (预计算)"""
    d = np.zeros(N)
    for cf in cube_faces:
        A = np.ones(N, dtype=np.float64)
        for f in cf:
            A *= 1.0 - 2.0*((idx >> f) & 1)
        d -= A
    return d

def order_param(cube_faces, n, N, idx, v):
    """基态 ⟨A_c⟩ (弦网凝聚序参量)"""
    ac = 0.0
    vv = v*v
    for cf in cube_faces:
        A = np.ones(N, dtype=np.float64)
        for f in cf:
            A *= 1.0 - 2.0*((idx >> f) & 1)
        ac += np.dot(vv, A)
    return ac/len(cube_faces)

def run_system(nx, ny, nz, lams, k=2, tol=1e-9, maxiter=600):
    cube_faces, n = build_grid(nx, ny, nz)
    N = 1 << n
    idx = np.arange(N, dtype=np.int64)
    flip = np.array([idx ^ (1 << f) for f in range(n)])   # 每面翻转索引 (n×N)
    d = diag_A(cube_faces, n, N, idx)
    print(f"\n=== {nx}×{ny}×{nz}: n={n} 面, N={N:,} 态, N_c={len(cube_faces)} 立方体 ===", flush=True)
    res = []
    for lam in lams:
        def matvec(v, lam=lam):
            out = d*v
            for f in range(n):
                out[flip[f]] -= lam*v
            return out
        Aop = LinearOperator((N, N), matvec=matvec, dtype=np.float64)
        ev, evc = eigsh(Aop, k=k, which='SA', tol=tol, maxiter=maxiter)
        E0, E1 = ev[0], ev[1]
        ac = order_param(cube_faces, n, N, idx, evc[:, 0])
        res.append((lam, E0, E1-E0, ac))
        print(f"  λ={lam:.2f}: E0={E0:+.4f}, Δ={E1-E0:.4f}, ⟨A_c⟩={ac:.4f}", flush=True)
    return np.array(res), cube_faces, n

def chi_peak(lams, acs):
    """磁化率 χ=-d⟨A⟩/dλ 峰 (中心差分)"""
    chi = -np.gradient(acs, lams)
    return float(lams[int(np.argmax(chi))]), float(chi.max())

if __name__ != "__main__":
    raise RuntimeError("import 保护: 请直接运行脚本")

print("="*80)
print("3+1D 弦网 λ_c 相变 (P1-3) — 凝聚相稳定性边界")
print("H(λ) = -ΣA_c - λΣX_f; λ=0 凝聚(拓扑序) → λ→∞ 极化(平凡)")
print("="*80)

# λ 扫描 (粗: 0→2.4 步 0.2, 相变区由 χ 峰确定后细扫)
lams = np.round(np.arange(0.0, 2.41, 0.2), 2)

systems = [(2,1,1), (3,1,1), (2,2,1), (4,1,1)]
results = {}
for (nx, ny, nz) in systems:
    tag = f"{nx}x{ny}x{nz}"
    arr, _, _ = run_system(nx, ny, nz, lams)
    results[tag] = arr
    lp, chmax = chi_peak(arr[:, 0], arr[:, 3])
    L = (nx*ny*nz)**(1.0/3.0)
    print(f"  ⟹ {tag}: L={L:.2f}, χ 峰 λ_χ={lp:.2f}, χ_max={chmax:.3f}", flush=True)

print("\n" + "="*80)
print("有限尺寸标度: λ_c(L) = λ_c(∞) + a/L")
print("="*80)
pts = []
for (nx, ny, nz) in systems:
    tag = f"{nx}x{ny}x{nz}"
    arr = results[tag]
    lp, _ = chi_peak(arr[:, 0], arr[:, 3])
    L = (nx*ny*nz)**(1.0/3.0)
    pts.append((1.0/L, lp))
xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
A = np.vstack([xs, np.ones_like(xs)]).T
(slope, intercept), *_ = np.linalg.lstsq(A, ys, rcond=None)
for (x, y) in zip(xs, ys):
    print(f"  1/L={x:.4f} (L={1/x:.2f}): λ_χ={y:.3f}")
print(f"  ⟹ 一阶外推 λ_c(∞) ≈ {intercept:.3f} ± (斜率 {slope:.2f}/L)")
print(f"  ⟹ 3+1D Z₂ 弦网相变点 λ_c ≈ {intercept:.2f} (凝聚↔极化)")
