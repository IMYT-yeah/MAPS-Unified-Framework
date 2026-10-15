# -*- coding: utf-8 -*-
"""
环境推移的 BLAS 化改造 —— 正确性 + 速度基准（第 101 轮 · 甲-2）

原实现的问题：`einsum('acpx,xstq->acpstq')` 先造出一个 (χ,χ,D,2,2,D) 的中间张量
（χ=8, D=30 时 = 230400 元素），再缩；且在 Python 循环里对**每个 site** 调用一次。
⟹ 单 sweep 4n 次推移，每次 ~12M 乘加 + 大中间张量 ⟹ 慢。

新实现：把 (a,s) 与 c/t 两侧的收缩交给 **BLAS matmul**，只有中间 (s,x) 那一步留给 einsum。
中间张量降到 (2,χ,χ,D,D)=56448，乘加降到 ~3.3M。
"""
import time
import numpy as np

from _lc3d_box_fast import (push_left_einsum as push_left_ein,
                            push_right_einsum as push_right_ein,
                            push_left as push_left_blas_,
                            init_left, init_right, build_all_left, build_all_right)


def push_left_blas(L, T, W):
    """out[b,d,p,q] = Σ_{a,c,s,t,x} L[a,c,p,x] W[x,s,t,q] T†[a,s,b] T[c,t,d]"""
    chi = L.shape[0]
    D = W.shape[0]
    # ① (a) 与 T† 缩 —— BLAS
    Tf = T.conj().reshape(chi, 2 * chi)                  # (a, s*b)
    Lf = L.reshape(chi, -1)                              # (a, c*p*x)
    M1 = (Tf.T @ Lf).reshape(2, chi, chi, D, D)          # (s, b, c, p, x)
    # ② 缩 (s, x) 与 W
    M2 = np.einsum('sbcpx,xstq->bcptq', M1, W, optimize=True)   # (b, c, p, t, q)
    # ③ (c,t) 与 T 缩 —— BLAS
    M2f = M2.transpose(1, 3, 0, 2, 4).reshape(chi * 2, -1)      # (c*t, b*p*q)
    Tf2 = T.transpose(0, 1, 2).reshape(chi * 2, chi)            # (c*t, d)
    out = (Tf2.T @ M2f).reshape(chi, chi, D, D)                 # (d, b, p, q)
    return out.transpose(1, 0, 2, 3)                            # (b, d, p, q)


def push_right_blas(R, T, W):
    """out[a,c,p,q] = Σ_{b,d,X,q'} R[b,d,X,q'] W[p,s,t,X] T†[a,s,b] T[c,t,d]"""
    chi = R.shape[0]
    D = W.shape[0]
    # ① (b) 缩 R 与 T† —— BLAS
    T2 = T.conj().reshape(chi * 2, chi)                  # (a*s, b)
    R2 = R.reshape(chi, -1)                              # (b, d*X*q)
    M1 = (T2 @ R2).reshape(chi, 2, chi, D, D)            # (a, s, d, X, q)
    # ② 缩 (s, X) 与 W
    M2 = np.einsum('asdXq,pstX->adtpq', M1, W, optimize=True)   # (a, d, t, p, q)
    # ③ (d,t) 缩 T —— BLAS（用 (d,t) 序与 M2 对齐）
    M2f = M2.transpose(1, 2, 0, 3, 4).reshape(2 * chi, -1)      # (d*t, a*p*q)
    T3 = T.transpose(2, 1, 0).reshape(2 * chi, chi)             # (d*t, c)
    out = (T3.T @ M2f).reshape(chi, chi, D, D)                  # (c, a, p, q)
    return out.transpose(1, 0, 2, 3)                            # (a, c, p, q)


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    print("=" * 88)
    print("正确性对照（随机张量）")
    print("=" * 88)
    for chi, D in [(8, 11), (8, 30), (16, 30)]:
        L = rng.standard_normal((chi, chi, D, D))
        R = rng.standard_normal((chi, chi, D, D))
        T = rng.standard_normal((chi, 2, chi))
        W = rng.standard_normal((D, 2, 2, D))
        a = push_left_ein(L, T, W); b = push_left_blas(L, T, W)
        c = push_right_ein(R, T, W); d = push_right_blas(R, T, W)
        print("χ={:>2} D={:>2}: push_left  Δmax={:.2e} ｜ push_right Δmax={:.2e}  (尺度 {:.2e})".format(
            chi, D, np.abs(a - b).max(), np.abs(c - d).max(), np.abs(a).max()))

    print()
    print("=" * 88)
    print("速度基准")
    print("=" * 88)
    for chi, D in [(8, 11), (8, 21), (8, 30), (16, 30)]:
        L = rng.standard_normal((chi, chi, D, D))
        T = rng.standard_normal((chi, 2, chi))
        W = rng.standard_normal((D, 2, 2, D))
        reps = 50
        t0 = time.time()
        for _ in range(reps):
            push_left_ein(L, T, W)
        t_e = (time.time() - t0) / reps
        t0 = time.time()
        for _ in range(reps):
            push_left_blas(L, T, W)
        t_b = (time.time() - t0) / reps
        print("push_left  χ={:>2} D={:>2}: 原 {:.4f} s → 新 {:.4f} s = 提速 {:>5.1f}×".format(
            chi, D, t_e, t_b, t_e / t_b))

    print()
    print("=" * 88)
    print("端到端：单 sweep 耗时（含 build_all + 局部更新）")
    print("=" * 88)
    from _lc3d_box import build_grid, make_mpo
    from _lc3d_box_fast import dmrg1_fast
    for dims in [(2, 2, 2), (3, 2, 2), (3, 3, 2), (3, 3, 3)]:
        cube_faces, n = build_grid(*dims)
        Ws = make_mpo(cube_faces, n, 0.20)
        t0 = time.time()
        dmrg1_fast(Ws, n, chi=8, max_sweeps=1, seed=1)
        dt = time.time() - t0
        print("  {}  n={:>3} D={:>2}: {:.2f} s/sweep".format(dims, n, 3 + len(cube_faces), dt))
