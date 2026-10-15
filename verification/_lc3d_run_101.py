# -*- coding: utf-8 -*-
"""
3D 盒子 λ 扫描驱动（第 101 轮 · 甲-2）

用法：
    python _lc3d_run_101.py <nx> <ny> <nz> <chi> <sweeps> <lo> <hi> <dlam> <seed> <tag>

输出 `_lc3d_101_<tag>.npz`：
    lams, E, ac, fid, sweeps, n, Nc, chi, dims

⚠️ 与 `_lc3d_box_fast.scan` 的差异：本驱动额外记录 **保真度** F(λ_i, λ_{i+1}) = |⟨ψ_i|ψ_{i+1}⟩|
   —— 保真度磁化率 χ_F = −2 lnF/δλ² 是比 χ 峰更尖锐的相变判据，且**不需要对序参量做数值微分**。
   （warm start 保证相邻 λ 的波函数在同一规范分支上平滑演化，重叠才有意义。）
⚠️ **不记录 discarded weight**：1-site DMRG 的 1-site 更新**不增长 bond** ⟹ dw ≡ 0 是**恒等式**，
   不是质量指标（这是本模型的特殊性质，写成输出会误导）。χ 是否够用只能靠 χ=8/16/32 的能量差判断。
⚠️ **保真度的第一个点为 nan**（无前驱）；且若某个 λ 的基态简并（如 λ=0），
   相邻态的 F 可能≈0（跳到简并空间另一分支）⟹ 分析时**必须从 F≈0 处切断**。
"""
import sys
import numpy as np

from _lc3d_box import build_grid, make_mpo, expect_ac
from _lc3d_box_fast import dmrg1_fast


def mps_overlap(A, B):
    """⟨ψ_A|ψ_B⟩（要求两 MPS 的物理位点一致；bond 维可不同）"""
    r = np.ones((1, 1))
    for aA, aB in zip(A, B):
        r = np.einsum('ab,asc,bsd->cd', r, aA.conj(), aB, optimize=False)
    return float(np.real(r[0, 0]))


def main():
    nx, ny, nz = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    chi = int(sys.argv[4]); sweeps = int(sys.argv[5])
    lo, hi, dlam = float(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8])
    seed = int(sys.argv[9]); tag = sys.argv[10]

    cube_faces, n = build_grid(nx, ny, nz)
    Nc = len(cube_faces)
    lams = np.round(np.arange(lo, hi + 1e-9, dlam), 4)

    print("=== {}×{}×{} : n={} 面, N_c={}, MPO D={}, 2^{}={:.2e} 态 ===".format(
        nx, ny, nz, n, Nc, 3 + Nc, n, 2.0 ** n), flush=True)
    print("chi={} sweeps={} λ∈[{},{}] step {} seed={} | {} 点".format(
        chi, sweeps, lo, hi, dlam, seed, len(lams)), flush=True)

    E_a, ac_a, fid_a, sw_a = [], [], [], []
    A0, Aprev = None, None
    for lam in lams:
        Ws = make_mpo(cube_faces, n, lam)
        E, A, info = dmrg1_fast(Ws, n, chi=chi, max_sweeps=sweeps, seed=seed, A0=A0)
        ac = expect_ac(A, cube_faces, n)
        fid = mps_overlap(Aprev, A) if Aprev is not None else np.nan
        E_a.append(float(E)); ac_a.append(float(ac))
        fid_a.append(float(fid)); sw_a.append(info['sweeps'])
        print("  λ={:.4f}: E={:+.8f} ⟨A_c⟩={:.5f} F={:.6f} sw={}".format(
            lam, E, ac, fid, info['sweeps']), flush=True)
        A0, Aprev = A, A

    out = dict(lams=np.array(lams), E=np.array(E_a), ac=np.array(ac_a),
               fid=np.array(fid_a), sweeps=np.array(sw_a),
               n=n, Nc=Nc, chi=chi, dims=(nx, ny, nz))
    fn = '_lc3d_101_{}.npz'.format(tag)
    np.savez(fn, **out)
    print("⟹ 已保存 {}｜E(λ_0)={:.6f}（应 = −N_c = {}）".format(fn, E_a[0], -Nc), flush=True)


if __name__ == "__main__":
    main()
