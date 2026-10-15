# -*- coding: utf-8 -*-
"""M3-A 细网格版：对称约定 4 尺寸细扫，计算 m(h)/Δ(h)/χ(h) 与判据校准"""
import numpy as np
import sys
sys.path.insert(0, '.')
src = open('_p03_torus_std.py', encoding='utf-8').read()
exec(src[:src.index('if __name__') if 'if __name__' in src else len(src)])

HS = np.round(np.arange(0.05, 0.561, 0.01), 2)
print('h 网格:', len(HS), '点, [0.05, 0.56]')

results = {}
for (nx, ny) in [(2, 2), (2, 3), (2, 4), (3, 3)]:
    lat = SymTorus(nx, ny)
    L = np.sqrt(nx * ny)
    hs, ms, ds, es = [], [], [], []
    for h in HS:
        evals, evecs = lat.eigs(float(h), k=2)
        ms.append(lat.order_param(evecs[:, 0]))
        ds.append(evals[1] - evals[0])
        es.append(evals[0])
        hs.append(h)
    hs, ms, ds, es = map(np.array, (hs, ms, ds, es))
    chi = np.gradient(ms, hs)
    results[(nx, ny)] = dict(h=hs, m=ms, d=ds, e=es, chi=chi, L=L)
    np.savez(f'_m3_torus_{nx}x{ny}.npz', h=hs, m=ms, d=ds, e=es)
    print(f'{nx}x{ny}: 完成, L={L:.2f}, N={lat.N}', flush=True)

# ---- 判据分析 ----
H_C_LIT = 0.3285
print(f"\n文献 h_c(iPEPS) = {H_C_LIT}\n")

def peak(xs, ys):
    i = int(np.argmax(ys))
    # 二次插值细化
    if 0 < i < len(xs) - 1:
        a, b, c = ys[i-1], ys[i], ys[i+1]
        denom = a - 2*b + c
        if abs(denom) > 1e-14:
            dx = 0.5*(a - c)/denom
            return xs[i] + dx*(xs[1]-xs[0])
    return xs[i]

rows = []
for key, r in results.items():
    h, m, d, chi = r['h'], r['m'], r['d'], r['chi']
    L = r['L']
    # m=0.5 交叉
    i05 = np.argmin(np.abs(m - 0.5))
    h05 = h[i05]
    # χ 峰（细网格）
    h_chi = peak(h, chi)
    chi_max = chi.max()
    # Δ 判据: 排除 h=0 简并区，取 Δ 最小非零处（相变点能隙闭合候选）
    mask = h > 0.10
    i_gap = int(np.argmin(d[mask]))
    h_gap = h[mask][i_gap]
    # m(h_c)
    m_hc = np.interp(H_C_LIT, h, m)
    rows.append((L, h05, h_chi, h_gap, m_hc, chi_max))
    print(f"{key[0]}x{key[1]} (L={L:.2f}): m=0.5→{h05:.3f} | χ峰→{h_chi:.3f} (χ={chi_max:.2f}) | Δ最小(h>0.1)→{h_gap:.3f} | m(h_c)={m_hc:.3f}")

print()
print("判据 1/L 外推 vs 文献:")
for col, name in [(1, 'm=0.5'), (2, 'χ峰'), (3, 'Δ最小')]:
    pts = sorted((r[0], r[col]) for r in rows)
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    A = np.vstack([xs, np.ones_like(xs)]).T
    (slope, intercept), *_ = np.linalg.lstsq(A, ys, rcond=None)
    dev = (intercept - H_C_LIT)/H_C_LIT*100
    print(f"  {name:<6}: h_c(∞) = {intercept:.4f}  (vs 文献 {H_C_LIT}: {dev:+.1f}%)")

# m(h_c) 随 L 收敛性
print("\nm(h_c=0.3285) 随 L 收敛（真相变点处序参量应随 L 收缩→0 或趋常）:")
for r in sorted(rows):
    print(f"  L={r[0]:.2f}: m(h_c)={r[4]:.3f}")
