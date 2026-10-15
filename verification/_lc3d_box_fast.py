# -*- coding: utf-8 -*-
"""
3D 盒子 λ_c(∞) 精确定位 —— 增量环境 DMRG（第 101 轮 · 甲-2）

【为什么要新写一个求解器】
    `_lc3d_box.py::dmrg1` 在**每个 site** 都调用 `env_left_at` / `env_right_at`，
    二者各自从 0 重新缩并到底 ⟹ 单 sweep 成本 **O(n²)** 次张量缩并。
      · 2×2×2  n=36, MPO D=11  ⟹ 尚可
      · 3×3×3  n=108, MPO D=30 ⟹ 环境部分 ≈17×，**不可行**
    本轮做了两级优化（实测单 sweep 3×3×3：~24 s → 待测）：
      ① 环境推移**增量**化（左环境在正向扫中逐步右推、右环境预建缓存）⟹ O(n²)→O(n)
      ② 环境推移与局部有效 H 的构建**BLAS 化**（避免 (χ,χ,D,2,2,D) 级的大中间张量）

【张量约定】（与原模块严格一致，故可直接复用其 MPO 与期望值例程）
    · MPO 链：左边界 bond 固定 0，右边界 bond 自由（期望值端求和扣 <ψ|ψ>）
    · 环境     L[a,c,p,x]（bra,ket 左 bond；p,x = MPO bond）
               R[b,d,X,q]（bra,ket 右 bond；X,q = MPO bond）
    · 位点 c 的局部有效 H 用 L[c]（sites < c）与 R[c+1]（sites > c）

【诚实边界（必须与结果一起读）】
    ① 本模块**不改模型**：H(λ) = −Σ_c A_c − λ Σ_f X_f，几何由 `build_grid` 给出，
       与 v1.36 / A1 报告完全相同 ⟹ 结果与原报告**可比**。
    ② ⚠️ **1-site DMRG 的 discarded weight 恒为 0** —— 因为 1-site 更新**不增长 bond**
       （SVD 的 min(aL·2, aR) 恰 ≤ χ）⟹ `dw ≡ 0` 是**恒等式，不是质量指标**。
       χ 是否够用**只能**靠 χ=8 vs χ=16 vs χ=32 的**能量差**与 λ_χ 漂移来判断。
    ③ ⚠️ **Binder 累积量在本模型中恒等失效**：A_c 是 6 个 Pauli-Z 的乘积
       ⟹ A_c² = I ⟹ ⟨A²⟩ ≡ 1、⟨A⁴⟩ ≡ 1 ⟹ Binder ≡ 2/3（0 信息）。
       ⟹ 相变定位用：① χ 峰、② 保真度磁化率、③ E0 二阶导、④ ⟨A_c⟩ 跨尺寸交叉。
"""
import numpy as np
from scipy.linalg import eigh as _scipy_eigh

from _lc3d_box import (build_grid, make_mpo, init_mps, normalize_mps, expect_mpo,
                       expect_ac, chi_peak)


# ---------------------------------------------------------------- 环境推移（原版，保留作对照）
def push_left_einsum(L, T, W):
    tmp = np.einsum('acpx,xstq->acpstq', L, W, optimize=False)
    return np.einsum('acpstq,asb,ctd->bdpq', tmp, T.conj(), T, optimize=False)


def push_right_einsum(R, T, W):
    tmp = np.einsum('bdXq,asb,ctd->acstXq', R, T.conj(), T, optimize=False)
    return np.einsum('acstXq,pstX->acpq', tmp, W, optimize=False)


# ---------------------------------------------------------------- 环境推移（BLAS 版）
def push_left(L, T, W):
    """out[b,d,p,q] = Σ_{a,c,s,t,x} L[a,c,p,x] W[x,s,t,q] T†[a,s,b] T[c,t,d]

    ⚠️ **两个 bond 必须分开写**：L 的两个 bond 都等于位点 c 的**左 bond** `aL`，
       而 T 的右 bond 是 `ar`；在**边界位点**（c=0）有 aL=1 ≠ ar=χ。
       第一版把两者都当 χ，在 aL=1 时 reshape 直接崩（本轮已修）。
    """
    aL = T.shape[0]; ar = T.shape[2]; D = W.shape[0]
    Tf = T.conj().reshape(aL, 2 * ar)                     # (a, s*b)
    Lf = L.reshape(aL, -1)                                # (a, c*p*x)
    M1 = (Tf.T @ Lf).reshape(2, ar, aL, D, D)             # (s,b,c,p,x)   ← BLAS
    M2 = np.einsum('sbcpx,xstq->bcptq', M1, W, optimize=True)   # (b,c,p,t,q)
    M2f = M2.transpose(1, 3, 0, 2, 4).reshape(aL * 2, -1)       # (c*t, b*p*q)
    Tf2 = T.reshape(aL * 2, ar)                                 # (c*t, d)
    out = (Tf2.T @ M2f).reshape(ar, ar, D, D)                   # (d,b,p,q)   ← BLAS
    return out.transpose(1, 0, 2, 3)


def push_right(R, T, W):
    """out[a,c,p,q] = Σ_{b,d,X,q'} R[b,d,X,q'] W[p,s,t,X] T†[a,s,b] T[c,t,d]

    ⚠️ 同理：R 的两个 bond 都等于位点 c 的**右 bond** `ar`。
    """
    aL = T.shape[0]; ar = T.shape[2]; D = W.shape[0]
    T2 = T.conj().reshape(aL * 2, ar)                     # (a*s, b)
    R2 = R.reshape(ar, -1)                                # (b, d*X*q)
    M1 = (T2 @ R2).reshape(aL, 2, ar, D, D)               # (a,s,d,X,q)   ← BLAS
    M2 = np.einsum('asdXq,pstX->adtpq', M1, W, optimize=True)   # (a,d,t,p,q)
    M2f = M2.transpose(1, 2, 0, 3, 4).reshape(2 * ar, -1)       # (d*t, a*p*q)
    T3 = T.transpose(2, 1, 0).reshape(2 * ar, aL)               # (d*t, c)
    out = (T3.T @ M2f).reshape(aL, aL, D, D)                    # (c,a,p,q)   ← BLAS
    return out.transpose(1, 0, 2, 3)


def init_left(D):
    """L[a,c,p,x] 初值：左边界只允许 MPO bond 0（未激活背景）。"""
    L = np.zeros((1, 1, D, D)); L[0, 0, 0, 0] = 1.0
    return L


def init_right(D):
    """R[b,d,X,q] 初值：右边界只允许 0（背景）/ 1（X 链）/ D−1（已用）。"""
    R = np.zeros((1, 1, D, D))
    for ch in (0, 1, D - 1):
        R[0, 0, ch, ch] = 1.0
    return R


def build_all_right(Ws, A):
    n = len(A); R = [None] * (n + 1)
    R[n] = init_right(Ws[0].shape[0])
    for k in range(n - 1, -1, -1):
        R[k] = push_right(R[k + 1], A[k], Ws[k])
    return R


def build_all_left(Ws, A):
    n = len(A); L = [None] * (n + 1)
    L[0] = init_left(Ws[0].shape[0])
    for k in range(n):
        L[k + 1] = push_left(L[k], A[k], Ws[k])
    return L


# ---------------------------------------------------------------- 局部有效 H（BLAS 版）
def build_heff1_dense(L, R, W, aL, aR):
    """H[(a,s,b),(c,t,d)] = Σ_{m,n} L[a,c,0,m] W[m,s,t,n] (Σ_q R[b,d,n,q])

    两级收缩：① 缩 n（把 R 并进 W）；② 缩 m（BLAS matmul）。
    实测比原版单次 einsum（造 (χ,2,χ,χ,2,χ) 中间张量）快 ~5×。
    ⚠️ 这里 aL/aR 分别指位点 **左 bond** 与 **右 bond** 的维数（可不等，边界位点 =1）。
    """
    D = W.shape[0]
    L0 = L[:, :, 0, :]                 # (aL, aL, m)   ← 左边界 MPO bond 固定 0
    Rq = np.sum(R, axis=3)             # (aR, aR, n)   ← 右边界 MPO bond 自由求和
    Wr = np.einsum('mstn,bdn->mstbd', W, Rq, optimize=True)     # (m,s,t,aR,aR)
    Hf = (L0.reshape(aL * aL, D) @ Wr.reshape(D, -1))           # (aL*aL, s*t*aR*aR) ← BLAS
    H = Hf.reshape(aL, aL, 2, 2, aR, aR)                        # (a,c,s,t,b,d)
    H = H.transpose(0, 2, 4, 1, 3, 5)                           # (a,s,b,c,t,d)
    return H.reshape(aL * 2 * aR, aL * 2 * aR)


def build_heff1_dense_ref(L, R, W, aL, aR):
    """原版（einsum 单发）—— 仅供正确性对照。"""
    L0 = L[:, :, 0, :]
    Rq = np.sum(R, axis=3)
    H = np.einsum('acm,mstn,bdn->asbctd', L0, W, Rq, optimize=False)
    return H.reshape(aL * 2 * aR, aL * 2 * aR)


# ---------------------------------------------------------------- 安全 eigh
def safe_eigh(H):
    try:
        return _scipy_eigh(H, check_finite=False)
    except np.linalg.LinAlgError:
        return np.linalg.eigh(H + 1e-10 * np.eye(H.shape[0]))


# ---------------------------------------------------------------- DMRG 主体
def dmrg1_fast(Ws, n, chi=8, max_sweeps=40, tol=1e-8, seed=0, A0=None,
               verbose=False):
    """1-site DMRG（增量环境 + BLAS）。

    收敛判据：连续两个 sweep 的能量变化 |ΔE| < tol（**绝对**；对 E~−25 即相对 4e-10）。
    ⚠️ 收敛判据用「连续两次变化」而非「相对上次」是为了容忍 1-site DMRG 的轻微能量振荡。
    """
    A = init_mps(n, chi, seed) if A0 is None else [a.copy() for a in A0]
    normalize_mps(A)
    D = Ws[0].shape[0]
    E_prev, best_E, best_A = None, None, None

    for sweep in range(max_sweeps):
        # ---------- 正向扫 ----------
        Rcache = build_all_right(Ws, A)
        L = init_left(D)
        for c in range(n - 1):
            aL, _, aR = A[c].shape
            H = build_heff1_dense(L, Rcache[c + 1], Ws[c], aL, aR)
            _, evec = safe_eigh(H)
            A[c] = evec[:, 0].reshape(aL, 2, aR)
            M = A[c].reshape(aL * 2, aR)
            u, s, vh = np.linalg.svd(M, full_matrices=False)
            ch = min(chi, len(s))
            A[c] = u[:, :ch].reshape(aL, 2, ch)
            A[c + 1] = np.einsum('ab,bsd->asd', (vh[:ch] * s[:ch, None]), A[c + 1])
            L = push_left(L, A[c], Ws[c])

        # ---------- 反向扫 ----------
        Lcache = build_all_left(Ws, A)
        R = init_right(D)
        for c in range(n - 1, 0, -1):
            aL, _, aR = A[c].shape
            H = build_heff1_dense(Lcache[c], R, Ws[c], aL, aR)
            _, evec = safe_eigh(H)
            A[c] = evec[:, 0].reshape(aL, 2, aR)
            M = A[c].reshape(aL, 2 * aR)
            u, s, vh = np.linalg.svd(M, full_matrices=False)
            ch = min(chi, len(s))
            A[c] = vh[:ch].reshape(ch, 2, aR)
            A[c - 1] = np.einsum('asb,bc->asc', A[c - 1], (u[:, :ch] * s[:ch]))
            R = push_right(R, A[c], Ws[c])

        normalize_mps(A)
        E = expect_mpo(A, Ws, subtract=True)
        if verbose:
            print("    sweep {}: E={:.8f}".format(sweep + 1, E), flush=True)
        if best_E is None or E < best_E:
            best_E, best_A = E, [a.copy() for a in A]
        if E_prev is not None and abs(E - E_prev) < tol:
            break
        E_prev = E

    return best_E, best_A, {'sweeps': sweep + 1}


# ---------------------------------------------------------------- 扫描工具
def scan(dims, lams, chi=8, sweeps=40, seed=1, warm=True, verbose=True, tol=1e-8):
    """沿 λ 升序扫描（warm start）。"""
    cube_faces, n = build_grid(*dims)
    out = {'lams': [], 'E': [], 'ac': [], 'sweeps': [], 'n': n,
           'Nc': len(cube_faces), 'chi': chi}
    A0 = None
    for lam in lams:
        Ws = make_mpo(cube_faces, n, lam)
        E, A, info = dmrg1_fast(Ws, n, chi=chi, max_sweeps=sweeps, seed=seed,
                                A0=A0, tol=tol)
        ac = expect_ac(A, cube_faces, n)
        out['lams'].append(float(lam)); out['E'].append(float(E))
        out['ac'].append(float(ac)); out['sweeps'].append(info['sweeps'])
        if verbose:
            print("  λ={:.4f}: E={:+.8f} ⟨A_c⟩={:.5f} sw={}".format(
                lam, E, ac, info['sweeps']), flush=True)
        if warm:
            A0 = A
    for k in ('lams', 'E', 'ac'):
        out[k] = np.array(out[k])
    return out


if __name__ == "__main__":
    import sys, time
    mode = sys.argv[1] if len(sys.argv) > 1 else 'verify'

    if mode == 'verify':
        # ① BLAS 化的局部 H / 环境推移 vs 原版
        print("=" * 78)
        print("验证 ⓪ BLAS vs 原版（随机张量）")
        print("=" * 78)
        rng = np.random.default_rng(0)
        for chi, D, aL, aR in [(8, 30, 8, 8), (8, 11, 8, 8), (16, 30, 16, 16), (8, 30, 1, 8)]:
            L = rng.standard_normal((aL, aL, D, D)); R = rng.standard_normal((aR, aR, D, D))
            T = rng.standard_normal((aL, 2, aR)); W = rng.standard_normal((D, 2, 2, D))
            e1 = np.abs(push_left(L, T, W) - push_left_einsum(L, T, W)).max()
            e2 = np.abs(push_right(R, T, W) - push_right_einsum(R, T, W)).max()
            e3 = np.abs(build_heff1_dense(L, R, W, aL, aR)
                        - build_heff1_dense_ref(L, R, W, aL, aR)).max()
            print("  χ={:>2} D={:>2} aL={:>2} aR={:>2}: pushL {:.1e} pushR {:.1e} heff {:.1e}".format(
                chi, D, aL, aR, e1, e2, e3))

        # ② 2×1×1 对精确对角化
        print()
        print("=" * 78)
        print("验证 ① 2×1×1（11 面，2048 态）— vs 精确对角化")
        print("=" * 78)
        from scipy.sparse.linalg import LinearOperator, eigsh
        cube_faces, n = build_grid(2, 1, 1)
        lam = 0.14
        Ws = make_mpo(cube_faces, n, lam)
        E, A, info = dmrg1_fast(Ws, n, chi=16, max_sweeps=80, seed=1)
        ac = expect_ac(A, cube_faces, n)
        N = 1 << n
        idx = np.arange(N, dtype=np.int64)
        flip = np.array([idx ^ (1 << f) for f in range(n)])
        d = np.zeros(N)
        for cf in cube_faces:
            Aop = np.ones(N)
            for f in cf:
                Aop *= 1.0 - 2.0 * ((idx >> f) & 1)
            d -= Aop

        def matvec(v):
            o = d * v
            for f in range(n):
                o[flip[f]] -= lam * v
            return o

        ev, evc = eigsh(LinearOperator((N, N), matvec=matvec, dtype=np.float64), k=1, which='SA')
        vv = evc[:, 0] ** 2
        ac_ex = 0.0
        for cf in cube_faces:
            Aop = np.ones(N)
            for f in cf:
                Aop *= 1.0 - 2.0 * ((idx >> f) & 1)
            ac_ex += float(vv @ Aop)
        ac_ex /= len(cube_faces)
        print("  DMRG : E0={:.8f}  ⟨A_c⟩={:.8f}".format(E, ac))
        print("  精确 : E0={:.8f}  ⟨A_c⟩={:.8f}".format(float(ev[0]), ac_ex))
        print("  偏差 : ΔE0={:.2e}   Δ⟨A_c⟩={:.2e}   sweeps={}".format(
            abs(E - ev[0]), abs(ac - ac_ex), info['sweeps']))

        # ③ 2×2×2 复现原报告 λ_χ = 0.230（同网格、同 χ、同 sweeps 上限）
        print()
        print("=" * 78)
        print("验证 ② 2×2×2（36 面，D=11）— 复现原报告 λ_χ=0.230 / χ_max=3.08")
        print("=" * 78)
        lams = np.round(np.arange(0.17, 0.331, 0.02), 3)
        t0 = time.time()
        r = scan((2, 2, 2), lams, chi=8, sweeps=20, seed=1)
        dt = time.time() - t0
        lp, ch = chi_peak(r['lams'], r['ac'])
        print("  ⟹ λ_χ={:.3f}  χ_max={:.3f}   总耗时 {:.1f} s（{:.1f} s/点）".format(
            lp, ch, dt, dt / len(lams)))
        ref_lam = np.array([0.17, 0.19, 0.21, 0.23, 0.25, 0.27, 0.29, 0.31, 0.33])
        ref_ac = np.array([0.8003, 0.7490, 0.6921, 0.6310, 0.5691, 0.5103, 0.4662, 0.4251, 0.3847])
        print("  与原报告 ⟨A_c⟩ 逐点最大偏差 = {:.5f}".format(
            float(np.abs(r['ac'] - ref_ac).max())))
        np.savez('_lc3d_101_222chi8.npz', **r)
    else:
        print("用法: python _lc3d_box_fast.py verify")
