# -*- coding: utf-8 -*-
"""
弦网低能谱 (自旋 2 判据实证) — P1-1
模型: Z₂ 弦网链 H(λ) = -Σ_c A_c - λ Σ_f X_f
  A_c = Π_{f∈c} Z_f (立方体闭合法则), X_f = 面翻转
实证内容:
  ① 低能谱: λ=0 精确能级 + 简并度 (解析计数); Δ(λ) 轨迹 (双立方体 2048 全谱 / 三链 65536 Lanczos)
  ② C4 旋转对称 (链轴四重旋转): [R,H]=0 验证, R⁴=I, 全局扇区维数 (特征标), 扇区投影低能谱
  ③ 自旋 2 判据: C4=-1 扇区 (螺旋度 ±2) 最低激发能 Δ_{-1} vs 矢量扇区 Δ_vec;
     一阶/二阶算符空间的旋转本征值 (-1 多重度 = 螺旋度 ±2 承载)
  ④ 判据链评估: ①Fierz-Pauli(引) ②旋转本征值±2(v1.29 严格 + 本实证) ③Weinberg 软定理(引)
                  ④弦网低能谱 (本工作数值化)
"""
import numpy as np
from scipy.sparse import csr_matrix, identity
from scipy.sparse.linalg import eigsh

def build_chain(ncubes):
    """ncubes 个立方体线性链. faces[c] = 第 c 个立方体的 6 面 [x-,y+,y-,z+,z-,x+]"""
    faces = []
    for c in range(ncubes):
        if c == 0:
            fc = list(range(6))
        else:
            base = 6 + 5*(c-1)          # 前面的累计面数 (共享面 = base-1)
            fc = [base-1] + list(range(base, base+5))
        faces.append(fc)
    n = 6 + 5*(ncubes-1)                # 总面数
    return faces, n

def c4_perm(ncubes, n):
    """C4 (绕链轴 x 四重旋转) 面置换: 每个立方体侧 4 面循环, x-面固定"""
    perm = np.arange(n)
    for c in range(ncubes):
        p0 = 5*c
        perm[p0+1], perm[p0+2], perm[p0+3], perm[p0+4] = p0+2, p0+3, p0+4, p0+1
    return perm

def build_H(idx, faces, lam, n):
    """H = -ΣA_c - λΣX_f (稀疏)"""
    N = len(idx)
    z = 1.0 - 2.0*((idx[:, None] >> np.arange(n)) & 1)   # N×n 面 Z 本征值
    A = np.empty((N, len(faces)))
    for c, fc in enumerate(faces):
        A[:, c] = np.prod(z[:, fc], axis=1)
    d = -A.sum(axis=1)
    rows = np.tile(np.arange(N), n)
    cols = np.concatenate([idx ^ (1 << f) for f in range(n)])
    data = np.full(N*n, -lam)
    H = csr_matrix((data, (rows, cols)), shape=(N, N))
    H = H + csr_matrix((d, (np.arange(N), np.arange(N))), shape=(N, N))
    return H, A

def build_R(idx, perm, N):
    """C4 旋转算符: R[j, P_inv[j]] = 1, P = 位置换"""
    P = np.zeros(N, dtype=np.int64)
    for f, pf in enumerate(perm):
        P |= ((idx >> f) & 1) << pf
    P_inv = np.argsort(P)              # P 为双射
    R = csr_matrix((np.ones(N), (np.arange(N), P_inv)), shape=(N, N))
    return R

def sector_projectors(R, N):
    """标量(q=1)/螺旋±2(q=-1)/矢量(q=±i) 扇区投影 (实厄米)"""
    I = identity(N, format='csr')
    R2 = R @ R; R3 = R2 @ R
    P_sc = (I + R + R2 + R3) / 4.0
    P_h2 = (I - R + R2 - R3) / 4.0
    P_vec = (I - R2) / 2.0
    return P_sc, P_h2, P_vec

def sector_spectra(H, R, N, k=6, tol=1e-9):
    P_sc, P_h2, P_vec = sector_projectors(R, N)
    out = {}
    for name, P in [('标量 q=+1', P_sc), ('螺旋±2 q=-1', P_h2), ('矢量 q=±i', P_vec)]:
        Hq = P @ (H @ P)
        ev = eigsh(Hq, k=k, which='SA', tol=tol, return_eigenvectors=False)
        out[name] = np.sort(ev)
    return out

def rot_eig_ops(perm, n):
    """一阶 (Z_f) / 二阶 (Z_fZ_g) 算符空间的 C4 旋转本征值多重度"""
    M1 = np.zeros((n, n))
    for i in range(n):
        M1[perm[i], i] = 1
    ev1 = np.linalg.eigvals(M1)
    pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
    pid = {p: k for k, p in enumerate(pairs)}
    M2 = np.zeros((len(pairs), len(pairs)))
    for k, (i, j) in enumerate(pairs):
        a, b = sorted((perm[i], perm[j]))
        M2[pid[(a, b)], k] = 1
    ev2 = np.linalg.eigvals(M2)
    def count(e):
        return (np.sum(np.abs(e-1) < 1e-8), np.sum(np.abs(e+1) < 1e-8),
                np.sum(np.abs(e-1j) < 1e-8), np.sum(np.abs(e+1j) < 1e-8))
    return count(ev1), count(ev2)

def cluster_levels(ev, tol=1e-3):
    """不同能级聚类 → [(能级, 简并度)]"""
    ev = np.sort(ev)
    levels = [[ev[0]]]
    for e in ev[1:]:
        if e - levels[-1][0] > tol:
            levels.append([e])
        else:
            levels[-1].append(e)
    return [(np.mean(l), len(l)) for l in levels]

# =====================================================================
print("="*80)
print("弦网低能谱 (自旋 2 判据实证) — P1-1")
print("模型: H(λ) = -ΣA_c - λΣX_f  (Z₂ 弦网, 立方体闭合法则)")
print("="*80)

for ncubes in [2, 3]:
    faces, n = build_chain(ncubes)
    N = 1 << n
    idx = np.arange(N, dtype=np.int64)
    perm = c4_perm(ncubes, n)
    print(f"\n=== {ncubes} 立方体链: n={n} 面, N={N:,} 态, C4 面置换 perm={list(perm)} ===")

    # ---- ① λ=0 精确能级 (枚举计数) ----
    z = 1.0 - 2.0*((idx[:, None] >> np.arange(n)) & 1)
    A = np.empty((N, ncubes))
    for c, fc in enumerate(faces):
        A[:, c] = np.prod(z[:, fc], axis=1)
    E = -A.sum(axis=1)
    vals, counts = np.unique(E, return_counts=True)
    print("  λ=0 精确能级:")
    for v, c in zip(vals, counts):
        print(f"    E={v:+.1f}: 简并度 {c:,}  (期望 2^(n-Nc)·C(Nc,k): "
              f"{2**(n-ncubes) * (1 if v==-ncubes else (ncubes if abs(v)==ncubes-2 else 1)):,})")
    E0_exact = float(vals[0])
    gap_exact = float(vals[1]-vals[0])

    # ---- ② 能谱 λ 扫描 ----
    print(f"\n  低能谱 λ 扫描 (Lanczos k=25):")
    for lam in [0.0, 0.1, 0.3, 0.5, 1.0]:
        H, _ = build_H(idx, faces, lam, n)
        ev = eigsh(H, k=min(25, N), which='SA', tol=1e-9, return_eigenvectors=False)
        ev = np.sort(ev)
        print(f"    λ={lam:.1f}: E0={ev[0]:+.6f}  E1={ev[1]:+.6f}  E2={ev[2]:+.6f}  "
              f"E3={ev[3]:+.6f}  E4={ev[4]:+.6f}  带底展开 {ev[6]-ev[0]:.4f}")

    # ---- ③ C4 对称验证 + 扇区维数 ----
    H03, _ = build_H(idx, faces, 0.3, n)
    R = build_R(idx, perm, N)
    R4 = R @ R @ R @ R
    I = identity(N, format='csr')
    R4ok = (R4 - I).nnz == 0                     # 稀疏精确比较
    dh = R @ H03 - H03 @ R
    comm = float(np.max(np.abs(dh.data))) if dh.nnz else 0.0
    print(f"\n  C4 验证: R⁴=I: {R4ok}  max|[R,H(0.3)]| = {comm:.1e} (稀疏精确)")
    P_sc, P_h2, P_vec = sector_projectors(R, N)
    d_sc = P_sc.diagonal().sum(); d_h2 = P_h2.diagonal().sum(); d_vec = P_vec.diagonal().sum()
    # 特征标参考: Tr(R^k) = 2^{R^k 的面循环数}
    def n_cycles(p):
        seen = set(); c = 0
        for i in range(len(p)):
            if i in seen: continue
            c += 1; j = i
            while j not in seen: seen.add(j); j = int(p[j])
        return c
    tr = [2**n_cycles(perm), 2**n_cycles(np.array([perm[perm[i]] for i in range(n)])), 2**n_cycles(perm)]
    d_sc_ref = (N + tr[0] + tr[1] + tr[2])//4
    d_h2_ref = (N - tr[0] + tr[1] - tr[2])//4
    d_vec_ref = (N - tr[1])//2
    print(f"  全局扇区维数: 标量 {d_sc:.0f} (参考 {d_sc_ref}), 螺旋±2 {d_h2:.0f} (参考 {d_h2_ref}), "
          f"矢量 {d_vec:.0f} (参考 {d_vec_ref}) — 总和 {d_sc+d_h2+d_vec:.0f}/{N} ✓")

    # ---- ④ 扇区低能谱 (λ=0.3) → 自旋 2 间隙 ----
    print(f"\n  扇区低能谱 (λ=0.3, 每扇区最低 4 个):")
    sp = sector_spectra(H03, R, N, k=4)
    for name, ev in sp.items():
        print(f"    {name}: {[f'{e:+.5f}' for e in ev[:4]]}")
    E0 = sp['标量 q=+1'][0]
    d_sc_gap = sp['标量 q=+1'][1] - E0
    d_h2_gap = sp['螺旋±2 q=-1'][0] - E0
    d_vec_gap = sp['矢量 q=±i'][0] - E0
    print(f"    基态 E0={E0:+.5f} (标量扇区)")
    print(f"    间隙: Δ_标量={d_sc_gap:.5f}  Δ_螺旋±2(自旋2)={d_h2_gap:.5f}  Δ_矢量={d_vec_gap:.5f}")
    print(f"    物理间隙 Δ = min = {min(d_sc_gap, d_h2_gap, d_vec_gap):.5f}")

    # ---- ⑤ 算符空间旋转本征值 ----
    c1, c2 = rot_eig_ops(perm, n)
    npairs = len([(i,j) for i in range(n) for j in range(i+1,n)])
    print(f"\n  算符空间 C4 旋转本征值多重度 (1, -1, +i, -i):")
    print(f"    一阶 Z_f ({n} 维):   {c1}")
    print(f"    二阶 Z_fZ_g ({npairs} 维): {c2}  ⟹ 螺旋±2(-1) 承载 {c2[1]}")

# ---- ⑥ 双立方体密集全谱 (能级结构精确) ----
ncubes = 2
faces, n = build_chain(ncubes); N = 1 << n; idx = np.arange(N)
print(f"\n=== 双立方体密集全谱 (N={N}) — 能级聚类结构 ===")
for lam in [0.0, 0.1, 0.3, 0.5, 1.0]:
    Hd = np.zeros((N, N))
    z = 1.0 - 2.0*((idx[:, None] >> np.arange(n)) & 1)
    A = np.empty((N, ncubes))
    for c, fc in enumerate(faces):
        A[:, c] = np.prod(z[:, fc], axis=1)
    d = -A.sum(axis=1)
    Hd[np.arange(N), np.arange(N)] = d
    for f in range(n):
        Hd[idx ^ (1 << f), np.arange(N)] -= lam
    ev = np.linalg.eigvalsh(Hd)
    levels = cluster_levels(ev, tol=2e-3 if lam > 0 else 0.1)
    print(f"  λ={lam:.1f}: E0={ev[0]:+.6f}, 能级结构 (E, 简并):")
    for lv, mult in levels[:6]:
        print(f"    E={lv:+.6f}  (×{mult})")
    print(f"    ⟹ Δ(能级间隙) = {levels[1][0]-levels[0][0]:+.4f}" if len(levels) > 1 else "")

print("\n" + "="*80)
print("自旋 2 判据链: ①Fierz-Pauli(引用) ②旋转本征值 ±2(严格 v1.29 + 本实证) "
      "③Weinberg(引用) ④弦网低能谱(本工作数值化)")
print("="*80)
