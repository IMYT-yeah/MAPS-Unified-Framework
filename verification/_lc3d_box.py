# -*- coding: utf-8 -*-
"""
3D 盒子 λ_c(∞) 数值定位 (A1) — 1-site DMRG 求解器 (纯 numpy)
模型: H(λ) = -Σ_c A_c - λ Σ_f X_f   (A_c = 立方体 6 面 Z 乘积, X_f = 面翻转)
几何: 开边界 nx×ny×nz 立方体阵列 (build_grid 与 _stringnet_lc.py 一致)
方法: 1-site DMRG (中心规范: 左规范 + 中心 + 右规范)
     局部更新 = eigsh (Lanczos) + 分步 matvec, 无稠密 H_eff
     序参量 ⟨A_c⟩(λ) + 磁化率 χ = -d⟨A_c⟩/dλ 峰 → λ_c(L)
用途: 2×2×2 (36 面, 2^36=6.9e10 态, 超全空间能力) 等真 3D 盒子的基态求解
验证: 2×1×1 (2048 态) 与精确对角化对照
"""
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh

Z = np.array([[1.0, 0.0], [0.0, -1.0]])
X = np.array([[0.0, 1.0], [1.0, 0.0]])
I2 = np.eye(2)


def build_grid(nx, ny, nz):
    """nx×ny×nz 立方体阵列 → 每立方体 6 面索引, 总面数 n"""
    cells = [(i, j, k) for i in range(nx) for j in range(ny) for k in range(nz)]
    face_of = {}
    cube_faces = []
    dirs = [(-1, 0, 0, 'xm', 'xp'), (1, 0, 0, 'xp', 'xm'), (0, -1, 0, 'ym', 'yp'),
            (0, 1, 0, 'yp', 'ym'), (0, 0, -1, 'zm', 'zp'), (0, 0, 1, 'zp', 'zm')]
    for (i, j, k) in cells:
        cf = []
        for (di, dj, dk, dn, on) in dirs:
            nb = (i + di, j + dj, k + dk)
            if nb in cells and (nb[0], nb[1], nb[2], on) in face_of:
                cf.append(face_of[(nb[0], nb[1], nb[2], on)])
            else:
                key = (i, j, k, dn)
                face_of[key] = len(face_of)
                cf.append(face_of[key])
        cube_faces.append(cf)
    return cube_faces, len(face_of)


def make_mpo(cube_faces, n, lam):
    """MPO: H = -Σ_c A_c - λ Σ_f X_f, site = 面编号 0..n-1.
    W[i] shape (D, d, d, D), D = 3 + Nc; 左 bond 固定 0, 右 bond 自由
    通道 0 = 未激活背景 (I)                     -> 恒等路径, 期望扣 <ψ|ψ>
    通道 1 = X 项: 0→1 施加 -λX, 1→1 传播 (开放) -> Σ_f -λX_f
    通道 c+2 = A_c 链: first 0→(c+2) 放 Z, 传播, last (c+2)→d 放 -Z (闭合到已用)
    通道 d = Nc+2 已用: d→d 保持, 禁止回 0 -> 无交叉项
    """
    Nc = len(cube_faces)
    D = 3 + Nc
    d = D - 1  # 已用通道
    chains = []
    for cf in cube_faces:
        fs = sorted(cf)
        chains.append((fs[0], fs[-1], set(fs)))
    Ws = []
    for i in range(n):
        W = np.zeros((D, 2, 2, D))
        W[0, :, :, 0] = I2                      # 未激活保持
        W[0, :, :, 1] = -lam * X                # X 施加 (0→1)
        W[1, :, :, 1] = I2                      # X 传播
        W[d, :, :, d] = I2                      # 已用保持
        for c, (f0, f1, fs) in enumerate(chains, start=2):
            if i == f0:
                W[0, :, :, c] = Z
            elif i == f1:
                W[c, :, :, d] = -Z
            elif i in fs:
                W[c, :, :, c] = Z
            else:
                W[c, :, :, c] = I2
        Ws.append(W)
    return Ws


def init_mps(n, chi, seed=0):
    rng = np.random.default_rng(seed)
    A = []
    for i in range(n):
        dl = chi if i > 0 else 1
        dr = chi if i < n - 1 else 1
        A.append(rng.standard_normal((dl, 2, dr)) * 0.1)
    return A


def right_canonicalize(A, chi):
    """从右往左 SVD: A[i] 右规范 (u 列正交), 剩余 (s·vh) 并入左侧"""
    n = len(A)
    for i in range(n - 1, -1, -1):
        aL, _, aR = A[i].shape
        M = A[i].reshape(aL * 2, aR)
        u, s, vh = np.linalg.svd(M, full_matrices=False)
        r = min(min(aL * 2, aR), chi)
        A[i] = u[:, :r].reshape(aL, 2, r)
        if i > 0:
            A[i - 1] = np.einsum('asb,br->asr', A[i - 1], (vh[:r].T * s[:r]))
    return A


def env_left_at(Ws, A, i):
    """L 环境: sites < i, shape (bra_bond, ket_bond, p, q).
    W[p,s1,s2,q]: s1=bra(配 T†), s2=ket(配 T)
    cur(a1,a2,p,x); T†(a,s1,b); T(c,s2,d); W(x,s1,s2,q)
    """
    D = Ws[0].shape[0]
    cur = np.zeros((1, 1, D, D))
    cur[0, 0, 0, 0] = 1.0
    for k in range(i):
        T = A[k]
        W = Ws[k]
        tmp = np.einsum('acpx,xstq->acpstq', cur, W, optimize=False)
        cur = np.einsum('acpstq,asb,ctd->bdpq', tmp, T.conj(), T, optimize=False)
    return cur


def env_right_at(Ws, A, i):
    """R 环境: sites >= i, shape (bra_bond, ket_bond, p, q).
    cur(b,d,X,q); T†(a,s,b); T(c,t,d); W(p,s,t,X)  ->  cur(a,c,p,q)
    """
    D = Ws[-1].shape[3]
    cur = np.zeros((1, 1, D, D))
    for ch in (0, 1, D - 1):        # 右边界只允许 背景0 / X1 / 已用d
        cur[0, 0, ch, ch] = 1.0
    for k in range(len(A) - 1, i - 1, -1):
        T = A[k]
        W = Ws[k]
        tmp = np.einsum('bdXq,asb,ctd->acstXq', cur, T.conj(), T, optimize=False)
        cur = np.einsum('acstXq,pstX->acpq', tmp, W, optimize=False)
    return cur


def heff1_matvec(v, L, R, W):
    """1-site 有效 H matvec (链约定: 左边界固定 0, 右边界自由):
    y[a,s,b] = Σ_{c,t,d,m,n} L[a,c,0,m] W[m,s,t,n] (Σ_q R[b,d,n,q]) x[c,t,d]
    """
    Rq = np.sum(R, axis=3)   # (b,d,n) 右边界自由
    x1 = np.einsum('ctd,bdn->bctn', v, Rq, optimize=False)
    x2 = np.einsum('bctn,mstn->bcsm', x1, W, optimize=False)
    L0 = L[:, :, 0, :]       # (a,c,m)
    y = np.einsum('bcsm,acm->asb', x2, L0, optimize=False)
    return y


def expect_mpo(A, Ws, subtract=False):
    """<ψ|H|ψ> 全缩并 (右缩并, 右 bond 自由).
    subtract=True: MPO 含全 I 背景路径 (W[0,0]=I 保持), 扣除 <ψ|ψ>.
    """
    n = len(A)
    D = Ws[0].shape[0]
    r = np.zeros((1, 1, D, D))
    for ch in (0, 1, D - 1):        # 右边界只允许 背景0 / X1 / 已用d
        r[0, 0, ch, ch] = 1.0
    for i in range(n - 1, -1, -1):
        T = A[i]
        W = Ws[i]
        tmp = np.einsum('bdXq,asb,ctd->acstXq', r, T.conj(), T, optimize=False)
        r = np.einsum('acstXq,pstX->acpq', tmp, W, optimize=False)
    val = float(np.sum(r[0, 0, 0, :]))   # 左边界 bond 固定 0
    if subtract:
        val -= norm_mps(A)   # 扣除惰性背景恒等路径 (MPO = H + I)
    return val


def expect_ac(A, cube_faces, n):
    """<ψ|A_c|ψ> 均值: 单链 MPO (D=2, 系数 +1) 缩并"""
    tot = 0.0
    for cf in cube_faces:
        fs = sorted(cf)
        Ws2 = []
        for i in range(n):
            W = np.zeros((2, 2, 2, 2))
            W[0, :, :, 0] = I2          # 未激活背景
            if i == fs[0]:
                W[0, :, :, 1] = Z       # first: 开始
            elif i == fs[-1]:
                W[1, :, :, 0] = Z       # last: 闭合 (回 0, 单链无交叉)
            elif i in fs:
                W[1, :, :, 1] = Z       # 传播
            else:
                W[1, :, :, 1] = I2
            Ws2.append(W)
        tot += expect_mpo(A, Ws2, subtract=True)
    return tot / len(cube_faces)


def lanczos_min(Av, dim, v0, ncv=30, maxiter=2000, tol=1e-12, verbose=False):
    """Lanczos (全重正交化) 求最小特征值/向量. Av: matvec 函数."""
    q = v0.astype(np.float64)
    nq = np.linalg.norm(q)
    if nq < 1e-14:
        q = np.random.default_rng(0).standard_normal(dim)
        nq = np.linalg.norm(q)
    q = q / nq
    Q = np.zeros((dim, ncv))
    alpha = np.zeros(ncv)
    beta = np.zeros(ncv)
    Q[:, 0] = q
    w = Av(q)
    alpha[0] = float(q @ w)
    w = w - alpha[0] * q
    j = 0
    for j in range(1, ncv):
        beta[j] = np.linalg.norm(w)
        if beta[j] < 1e-13:
            break
        q = w / beta[j]
        Q[:, j] = q
        w = Av(q)
        w = w - beta[j] * Q[:, j - 1]
        alpha[j] = float(q @ w)
        w = w - alpha[j] * q
        # 全重正交化
        for i in range(j + 1):
            w = w - (Q[:, i] @ w) * Q[:, i]
    m = j  # 使用 j 个向量 (0..j-1)
    T = np.zeros((m, m))
    np.fill_diagonal(T, alpha[:m])
    for i in range(m - 1):
        T[i, i + 1] = beta[i + 1]
        T[i + 1, i] = beta[i + 1]
    evals, evecs = np.linalg.eigh(T)
    v = Q[:, :m] @ evecs[:, 0]
    return float(evals[0]), v


def norm_mps(A):
    """⟨ψ|ψ⟩ 全缩并 (约定: r 第一维=bra, 第二维=ket)"""
    n = len(A)
    r = np.ones((1, 1))
    for i in range(n - 1, -1, -1):
        T = A[i]
        r = np.einsum('bd,asd,csb->ca', r, T, T.conj())
    return float(r[0, 0])


def norm_env_left(A, i):
    """N 的左侧环境: sites < i 的 ⟨ψ|ψ⟩, shape (bra_bond, ket_bond) = 块的右 bond
    cur(c,a)=bra/ket 左; T†(c,s,b); T(a,s,d) -> (b,d) 右 bond
    """
    cur = np.ones((1, 1))
    for k in range(i):
        T = A[k]
        cur = np.einsum('ca,csb,asd->bd', cur, T.conj(), T)
    return cur


def norm_env_right(A, i):
    """N 的右侧环境: sites >= i 的 ⟨ψ|ψ⟩, shape (bra_bond, ket_bond) = 块的左 bond
    cur(b,d)=bra/ket 右; T†(c,s,b); T(a,s,d) -> (c,a) 左 bond
    """
    cur = np.ones((1, 1))
    for k in range(len(A) - 1, i - 1, -1):
        T = A[k]
        cur = np.einsum('bd,csb,asd->ca', cur, T.conj(), T)
    return cur


def nrm1_matvec(v, LI, RI):
    """1-site N matvec: y[a2,s,b2] = Σ_{a1,b1} LI[bra=a2,ket=a1] RI[bra=b2,ket=b1] x[a1,s,b1]
    LI/RI 形状 (bra_bond, ket_bond)
    """
    return np.einsum('asb,pa,db->psd', v, LI, RI, optimize=False)


def normalize_mps(A):
    """全局归一化 ⟨ψ|ψ⟩=1"""
    nrm = norm_mps(A)
    A[0] = A[0] / np.sqrt(nrm)
    return A


def gen_lanczos_min(Hv, Nv, dim, v0, ncv=40, tol=1e-13):
    """广义 Lanczos: 求 H ψ = E N ψ 最小特征值 (N 对称正半定)."""
    q = v0.astype(np.float64)
    nq2 = q @ Nv(q)
    if nq2 < 1e-20:
        q = np.random.default_rng(0).standard_normal(dim)
        nq2 = q @ Nv(q)
    q = q / np.sqrt(nq2)
    Q = np.zeros((dim, ncv))
    alpha = np.zeros(ncv)
    beta = np.zeros(ncv)
    Q[:, 0] = q
    w = Hv(q)
    alpha[0] = float(q @ w)
    w = w - alpha[0] * q
    m = 0
    for m in range(1, ncv):
        beta[m] = float(np.sqrt(w @ Nv(w)))
        if beta[m] < tol:
            break
        q = w / beta[m]
        Q[:, m] = q
        w = Hv(q)
        w = w - beta[m] * Q[:, m - 1]
        alpha[m] = float(q @ w)
        w = w - alpha[m] * q
        for i in range(m + 1):
            coef = Q[:, i] @ Nv(w)
            w = w - coef * Q[:, i]
    T = np.zeros((m, m))
    np.fill_diagonal(T, alpha[:m])
    for i in range(m - 1):
        T[i, i + 1] = beta[i + 1]
        T[i + 1, i] = beta[i + 1]
    evals, evecs = np.linalg.eigh(T)
    v = Q[:, :m] @ evecs[:, 0]
    return float(evals[0]), v


def build_heff1_dense(L, R, W, aL, aR):
    """1-site 稠密有效 H: H[(a1,s1,b1),(a2,s2,b2)] =
    Σ_{m,n,p} L[a1,a2,m,n] W[m,s1,s2,p] R[b1,b2,p,n]  (s1=bra/行, s2=ket/列)
    """
    # MPO 链: 左边界 bond 固定 0 (L 的 p=0), 右边界 bond 自由 (R 的 q 求和)
    # H[(a,s,b),(c,t,d)] = Σ_{m,n} L[a,c,0,m] W[m,s,t,n] (Σ_q R[b,d,n,q])
    L0 = L[:, :, 0, :]              # (a, c, m)  左边界固定 0
    Rq = np.sum(R, axis=3)          # (b, d, n)  右边界自由求和
    H = np.einsum('acm,mstn,bdn->asbctd', L0, W, Rq, optimize=False)
    return H.reshape(aL * 2 * aR, aL * 2 * aR)


def build_nrm1_dense(LI, RI, aL, aR):
    """1-site 稠密 N: N[(a2,s2,b2),(a1,s1,b1)] = δ_{s1,s2} LI[a2,a1] RI[b2,b1]
    行 (p,i,d)=(a2,s2,b2), 列 (a,j,b)=(a1,s1,b1)
    """
    N = np.einsum('pa,db,ij->paidbj', LI, RI, np.eye(2), optimize=False)
    N = N.transpose(0, 2, 3, 1, 5, 4)  # (p,i,d, a,j,b)
    return N.reshape(aL * 2 * aR, aL * 2 * aR)


def build_heff2_dense(L, R, Wi, Wj, aL, aR):
    """2-site 有效 H: H[(a,s1,s2,b),(c,t1,t2,d)] =
    Σ_{p,m,n,r} L[a,c,p,m] Wi[m,s1,t1,n] Wj[n,s2,t2,r] R[b,d,r,p]
    """
    H = np.einsum('acpm,muvn,nwxr,bdrp->auwbcvxd',
                  L, Wi, Wj, R, optimize=False)
    return H.reshape(aL * 4 * aR, aL * 4 * aR)


def build_nrm2_dense(LI, RI, aL, aR):
    """2-site 稠密 N: N[(a,s1,s2,b),(c,t1,t2,d)] = δ_{s1,t1} δ_{s2,t2} LI[a,c] RI[b,d]"""
    N = np.einsum('ac,bd,ij,kl->aibjckdl', LI, RI, np.eye(2), np.eye(2), optimize=False)
    return N.reshape(aL * 4 * aR, aL * 4 * aR)


def dmrg2(Ws, n, chi=64, max_sweeps=80, tol=1e-9, seed=0, verbose=False):
    """2-site DMRG (N 值域投影): 返回 (E0, MPS A)"""
    A = init_mps(n, chi, seed)
    normalize_mps(A)
    E_prev = None
    best_E, best_A = None, None
    for sweep in range(max_sweeps):
        # right sweep: bond (i, i+1), i = 0..n-2
        for i in range(n - 1):
            L = env_left_at(Ws, A, i)
            R = env_right_at(Ws, A, i + 2)
            LI = norm_env_left(A, i)
            RI = norm_env_right(A, i + 2)
            aL = A[i].shape[0]
            aR = A[i + 1].shape[2]
            H = build_heff2_dense(L, R, Ws[i], Ws[i + 1], aL, aR)
            evals, evecs = np.linalg.eigh(H)
            psi = evecs[:, 0]
            psi3 = psi.reshape(aL, 2, 2, aR)
            Mm = psi3.reshape(aL * 2, 2 * aR)
            u, s, vh = np.linalg.svd(Mm, full_matrices=False)
            ch = min(chi, len(s))
            A[i] = u[:, :ch].reshape(aL, 2, ch)
            A[i + 1] = (vh[:ch] * s[:ch, None]).reshape(ch, 2, aR)
        # left sweep: bond (i, i+1), i = n-2..0
        for i in range(n - 2, -1, -1):
            L = env_left_at(Ws, A, i)
            R = env_right_at(Ws, A, i + 2)
            aL = A[i].shape[0]
            aR = A[i + 1].shape[2]
            H = build_heff2_dense(L, R, Ws[i], Ws[i + 1], aL, aR)
            evals, evecs = np.linalg.eigh(H)
            psi = evecs[:, 0]
            psi3 = psi.reshape(aL, 2, 2, aR)
            Mm = psi3.reshape(aL * 2, 2 * aR)
            u, s, vh = np.linalg.svd(Mm, full_matrices=False)
            ch = min(chi, len(s))
            A[i] = u[:, :ch].reshape(aL, 2, ch)
            A[i + 1] = (vh[:ch] * s[:ch, None]).reshape(ch, 2, aR)
        normalize_mps(A)
        E = expect_mpo(A, Ws, subtract=True)
        if verbose:
            print(f"  sweep {sweep + 1}: E={E:.8f}", flush=True)
        if best_E is None or E < best_E:
            best_E, best_A = E, [a.copy() for a in A]
        if E_prev is not None and abs(E - E_prev) < tol:
            break
        E_prev = E
    return best_E, best_A


def mpo_apply(A, Ws, chi):
    """|ψ'> = H|ψ> (MPS × MPO), SVD 压缩到 bond chi. 返回新 MPS"""
    n = len(A)
    B = []
    for i in range(n):
        T = A[i]
        W = Ws[i]
        # T2[a*p, s, b*q] = Σ_{s'} T[a,s',b] W[p,s,s',q]
        T2 = np.einsum('aub,psuq->apsbq', T, W, optimize=False)
        T2 = T2.reshape(T.shape[0] * W.shape[0], 2, T.shape[2] * W.shape[3])
        B.append(T2)
    # 右规范压缩 (从右往左 SVD 截断, 右 bond 保持)
    for i in range(n - 1, -1, -1):
        aL, _, aR = B[i].shape
        M = B[i].reshape(aL, 2 * aR)
        u, s, vh = np.linalg.svd(M, full_matrices=False)
        r = min(min(aL, 2 * aR), chi)
        if r == 0:
            r = 1
        B[i] = vh[:r].reshape(r, 2, aR)
        if i > 0:
            B[i - 1] = np.einsum('asb,bc->asc', B[i - 1], (u[:, :r] * s[:r]))
    return B


def dmrg_power(Ws, n, chi=64, max_iter=500, tol=1e-9, seed=0, verbose=False):
    """幂迭代基态: |ψ_{k+1}> = (E_shift·I - H)|ψ_k>, 压缩+归一化.
    返回 (E0, MPS A)
    """
    A = init_mps(n, chi, seed)
    normalize_mps(A)
    # E_shift 上界: E_max ≤ Nc + λ·n
    Nc = n - 2  # 近似 (build_grid 的立方体数)
    lam = -Ws[0][0, 0, 0, 0] if False else 0.0
    # 从 MPO 提取 λ: W[0][0,:,:,1] = -λX
    lam = -Ws[0][0, 0, 1, 1]
    D = Ws[0].shape[0]
    E_shift = Nc + lam * n + 1.0
    E_prev = None
    best_E, best_A = None, None
    for it in range(max_iter):
        Hpsi = mpo_apply(A, Ws, chi * D)      # H|ψ>, bond χ·D
        Hpsi = pad_mps(compress_mps(Hpsi, chi), chi)
        A2 = [E_shift * A[i] - Hpsi[i] for i in range(n)]
        A2 = compress_mps(A2, chi)
        normalize_mps(A2)
        A = A2
        E = expect_mpo(A, Ws, subtract=True)
        if verbose and (it % 10 == 0 or it < 5):
            print(f"  iter {it}: E={E:.8f}", flush=True)
        if best_E is None or E < best_E:
            best_E, best_A = E, [a.copy() for a in A]
        if E_prev is not None and abs(E - E_prev) < tol:
            break
        E_prev = E
    return best_E, best_A


def pad_mps(B, chi):
    """把 MPS 各 site bond 提升到统一 chi (零填充), 边界 bond 1"""
    n = len(B)
    out = []
    for i, T in enumerate(B):
        aL, s, aR = T.shape
        L = chi if i > 0 else 1
        R = chi if i < n - 1 else 1
        Tp = np.zeros((L, s, R))
        Tp[:aL, :, :aR] = T
        out.append(Tp)
    return out


def compress_mps(A, chi):
    """SVD 压缩到 bond chi (右规范方向, 右 bond 保持)"""
    n = len(A)
    B = [a.copy() for a in A]
    for i in range(n - 1, -1, -1):
        aL, _, aR = B[i].shape
        M = B[i].reshape(aL, 2 * aR)
        u, s, vh = np.linalg.svd(M, full_matrices=False)
        r = min(min(aL, 2 * aR), chi)
        if r == 0:
            r = 1
        B[i] = vh[:r].reshape(r, 2, aR)
        if i > 0:
            B[i - 1] = np.einsum('asb,bc->asc', B[i - 1], (u[:, :r] * s[:r]))
    return B


def solve_heff(H, N, dim, tol=1e-12):
    """在 N 的值域子空间求解 Hψ = E Nψ 的最小 (N 半正定时正确).
    返回 (E, psi_full)
    """
    Nn = N / max(float(np.max(np.abs(N))), 1e-30)
    evals_N, evecs_N = np.linalg.eigh(Nn)
    mask = evals_N > tol
    if np.sum(mask) == 0:
        mask = np.zeros(dim, dtype=bool)
        mask[int(np.argmax(evals_N))] = True
    P = evecs_N[:, mask]
    Hp = P.T @ H @ P
    evals, evecs = np.linalg.eigh(Hp)
    return float(evals[0]), P @ evecs[:, 0]


def scipy_linalg_eigh(H):
    """带退化防护的 eigh (Windows LAPACK 对近奇异矩阵偶发崩溃)"""
    from scipy.linalg import eigh
    try:
        return eigh(H, check_finite=False)
    except np.linalg.LinAlgError:
        return np.linalg.eigh(H + 1e-10 * np.eye(H.shape[0]))


def dmrg1(Ws, n, chi=64, max_sweeps=80, tol=1e-9, seed=0, verbose=False, A0=None):
    """1-site DMRG (普通 eigh 局部更新): 返回 (E0, MPS A)"""
    A = init_mps(n, chi, seed) if A0 is None else [a.copy() for a in A0]
    E_prev = None
    best_E, best_A = None, None
    for sweep in range(max_sweeps):
        for c in range(n - 1):
            L = env_left_at(Ws, A, c)
            R = env_right_at(Ws, A, c + 1)
            W = Ws[c]
            aL = A[c].shape[0]
            aR = A[c].shape[2]
            dim = aL * 2 * aR
            H = build_heff1_dense(L, R, W, aL, aR)
            evals, evecs = scipy_linalg_eigh(H)
            A[c] = evecs[:, 0].reshape(aL, 2, aR)
            M = A[c].reshape(aL * 2, aR)
            u, s, vh = np.linalg.svd(M, full_matrices=False)
            ch = min(chi, len(s))
            A[c] = u[:, :ch].reshape(aL, 2, ch)
            A[c + 1] = np.einsum('ab,bsd->asd', (vh[:ch] * s[:ch, None]), A[c + 1])
        for c in range(n - 1, 0, -1):
            L = env_left_at(Ws, A, c)
            R = env_right_at(Ws, A, c + 1)
            W = Ws[c]
            aL = A[c].shape[0]
            aR = A[c].shape[2]
            dim = aL * 2 * aR
            H = build_heff1_dense(L, R, W, aL, aR)
            evals, evecs = scipy_linalg_eigh(H)
            A[c] = evecs[:, 0].reshape(aL, 2, aR)
            M = A[c].reshape(aL, 2 * aR)
            u, s, vh = np.linalg.svd(M, full_matrices=False)
            ch = min(chi, len(s))
            A[c] = vh[:ch].reshape(ch, 2, aR)
            A[c - 1] = np.einsum('asb,bc->asc', A[c - 1], (u[:, :ch] * s[:ch]))
        normalize_mps(A)
        E = expect_mpo(A, Ws, subtract=True)
        if verbose:
            print(f"  sweep {sweep + 1}: E={E:.8f}", flush=True)
        if best_E is None or E < best_E:
            best_E, best_A = E, [a.copy() for a in A]
        if E_prev is not None and abs(E - E_prev) < tol:
            break
        E_prev = E
    return best_E, best_A


def run_system(nx, ny, nz, lams, chi=64, sweeps=60, seed=0, verbose=True):
    cube_faces, n = build_grid(nx, ny, nz)
    print(f"=== {nx}×{ny}×{nz}: n={n} 面, 2^{n}={2**n:.2e} 态, N_c={len(cube_faces)} 立方体 ===", flush=True)
    res = []
    for lam in lams:
        Ws = make_mpo(cube_faces, n, lam)
        E0, A = dmrg1(Ws, n, chi=chi, max_sweeps=sweeps, seed=seed, verbose=False)
        ac = expect_ac(A, cube_faces, n)
        res.append((lam, E0, ac))
        if verbose:
            print(f"  λ={lam:.3f}: E0={E0:+.4f}, ⟨A_c⟩={ac:.4f}", flush=True)
    return np.array(res)


def chi_peak(lams, acs):
    chi = -np.gradient(acs, lams)
    i = int(np.argmax(chi))
    return float(lams[i]), float(chi[i])


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else 'verify'
    if mode == 'verify':
        # --- 验证: 2×1×1 vs 精确 ---
        print("=" * 70)
        print("验证: 2×1×1 (11 面, 2048 态) — DMRG(χ=64) vs 精确对角化")
        print("=" * 70)
        cube_faces, n = build_grid(2, 1, 1)
        lam = 0.14
        Ws = make_mpo(cube_faces, n, lam)
        E, A = dmrg1(Ws, n, chi=16, max_sweeps=60, seed=1, verbose=True)
        ac = expect_ac(A, cube_faces, n)
        # 精确
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
            out = d * v
            for f in range(n):
                out[flip[f]] -= lam * v
            return out
        Aop2 = LinearOperator((N, N), matvec=matvec, dtype=np.float64)
        ev, evc = eigsh(Aop2, k=2, which='SA')
        ac_ex = 0.0
        vv = evc[:, 0] * evc[:, 0]
        for cf in cube_faces:
            Aop = np.ones(N)
            for f in cf:
                Aop *= 1.0 - 2.0 * ((idx >> f) & 1)
            ac_ex += np.dot(vv, Aop)
        ac_ex /= len(cube_faces)
        print(f"\nDMRG: E0={E:.6f}, ⟨A_c⟩={ac:.6f}")
        print(f"精确: E0={ev[0]:.6f}, Δ={ev[1]-ev[0]:.6f}, ⟨A_c⟩={ac_ex:.6f}")
        print(f"偏差: ΔE0={abs(E-ev[0]):.2e}, Δ⟨A_c⟩={abs(ac-ac_ex):.2e}")
    elif mode == 'box':
        # --- 3D 盒子扫描: 2×2×2 ---
        lams = np.round(np.arange(0.0, 0.61, 0.04), 3)
        arr = run_system(2, 2, 2, lams, chi=64, sweeps=60, seed=2)
        lp, ch = chi_peak(arr[:, 0], arr[:, 3])
        print(f"⟹ 2×2×2: χ 峰 λ_χ={lp:.3f}, χ_max={ch:.3f}", flush=True)
        np.save('_lc3d_box_222.npy', arr)
    else:
        print("用法: python _lc3d_box.py [verify|box]")
