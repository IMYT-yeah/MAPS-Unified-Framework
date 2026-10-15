# -*- coding: utf-8 -*-
"""
χ 收敛测试（第 101 轮 · 甲-2）—— 判断 χ=8 的 λ_χ 能否引用

⚠️ 为什么必须做这个：
    ① 1-site DMRG 的 discarded weight **恒为 0**（不增长 bond）⟹ 「dw=0」**不是**质量指标。
    ② 3D 盒子的 MPS 纠缠熵 ∝ L²，χ=8 很可能**严重不足**。
    ③ 判据只有一个：**同一 λ 下 χ=8 vs 16（vs 32）的 E 与 ⟨A_c⟩ 差**。
       若 ⟨A_c⟩ 随 χ 显著漂移 ⟹ 由 χ=8 得到的 λ_χ **不可引用**，必须整体降级为
       「χ=8 层面上的数值，未做 χ 外推」。

用法：python _lc3d_chitest.py <nx> <ny> <nz> <lam1,lam2,...> <chi1,chi2,...> <sweeps>
"""
import sys
import time
import numpy as np

from _lc3d_box import build_grid, make_mpo, expect_ac
from _lc3d_box_fast import dmrg1_fast


def main():
    nx, ny, nz = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    lams = [float(x) for x in sys.argv[4].split(",")]
    chis = [int(x) for x in sys.argv[5].split(",")]
    sweeps = int(sys.argv[6]) if len(sys.argv) > 6 else 20

    cube_faces, n = build_grid(nx, ny, nz)
    Nc = len(cube_faces)
    print("=== {}×{}×{}  n={} 面 N_c={} MPO D={} ===".format(nx, ny, nz, n, Nc, 3 + Nc), flush=True)
    print("λ 点位: {}｜χ 序列: {}｜sweeps={}".format(lams, chis, sweeps), flush=True)
    print()
    print("{:>7} | {:>5} | {:>18} {:>10} {:>10} | {:>8}".format(
        "λ", "χ", "E0", "⟨A_c⟩", "ΔE vs prev", "s/点"))
    print("-" * 78)

    rows = []
    for lam in lams:
        Ws = make_mpo(cube_faces, n, lam)
        prev_E = None
        for chi in chis:
            t0 = time.time()
            E, A, info = dmrg1_fast(Ws, n, chi=chi, max_sweeps=sweeps, seed=1)
            ac = expect_ac(A, cube_faces, n)
            dt = time.time() - t0
            d = "" if prev_E is None else "{:+.2e}".format(E - prev_E)
            print("{:>7.3f} | {:>5} | {:>18.10f} {:>10.5f} {:>10} | {:>8.1f}".format(
                lam, chi, E, ac, d, dt), flush=True)
            rows.append((lam, chi, E, ac))
            prev_E = E
        # 该 λ 处的 χ 外推估计（两点线性，χ^{-3} 标度常见于有限 χ 误差）
        if len(chis) >= 2:
            a1, a2 = rows[-2], rows[-1]
            x1, x2 = 1.0 / a1[1] ** 3, 1.0 / a2[1] ** 3     # 假定误差 ∝ χ^{-3}
            m = (a2[3] - a1[3]) / (x2 - x1)
            ac_inf = a1[3] - m * x1
            print("        └ 按 ⟨A_c⟩ ∝ ⟨A_c⟩_∞ + c/χ³ 外推（2 点）：⟨A_c⟩_∞ = {:.5f}"
                  "（相对 χ={} 的修正 {:.2%}）".format(ac_inf, chis[-1],
                                                     abs(ac_inf - a2[3]) / max(abs(a2[3]), 1e-9)),
                  flush=True)
        print()

    print("=" * 78)
    print("汇总：⟨A_c⟩ 随 χ 的漂移")
    print("=" * 78)
    for lam in lams:
        rs = [r for r in rows if abs(r[0] - lam) < 1e-12]
        if len(rs) < 2:
            continue
        span = max(r[3] for r in rs) - min(r[3] for r in rs)
        print("  λ={:.3f}: ⟨A_c⟩ 最大跨度 = {:.5f}（相对 {:.2%}）".format(
            lam, span, span / max(abs(rs[-1][3]), 1e-9)))


if __name__ == "__main__":
    main()
