# -*- coding: utf-8 -*-
"""
P0-3: κ_c 有限尺寸标度 (FSS) — 拓扑序→禁闭真相变定位
复用 _scale_extrap3.py (正确几何 X 场版本, 电荷禁闭 σ_E≈2κ)
H(κ) = -ΣA_v - ΣB_p - κ ΣX_e
序参量: m(κ,L) = Σ_e ⟨X_e⟩/E (X 场平均: 0=拓扑序, 1=极化/禁闭相)
交叉点: m=0.5 的 κ*(L) (线性内插)
外推: κ*(L) = κ_c(∞) + c/L → κ_c(∞)
对照: toric code + 横向场文献 h_c ≈ 0.328 (J=1)
"""
import numpy as np, time
from _scale_extrap3 import Lattice, hidx

def order_param(v, lat):
    """m = Σ_e ⟨X_e⟩ / E (基态 X 场平均)"""
    N = lat.N
    total = 0.0
    for e in range(lat.n):
        flip = np.arange(N, dtype=np.int64) ^ (1 << e)
        total += float(np.dot(v, v[flip]))
    return total / lat.n

def scan(lat, kappas, iters=120, verbose=True):
    """κ 扫描: 返回 (kappas, ms, E0s)"""
    ms, E0s = [], []
    t0 = time.time()
    for k in kappas:
        E0, v = lat.ground_state(k, iters)
        m = order_param(v, lat)
        ms.append(m); E0s.append(E0)
        if verbose:
            print(f"    {lat.nx}x{lat.ny} κ={k:.2f}: E0={E0:+.4f} m=⟨X⟩={m:.4f} ({time.time()-t0:.0f}s)", flush=True)
    return ms, E0s

def crossing(kappas, ms, target=0.5):
    """m 穿过 target 的 κ 值 (线性内插)"""
    for i in range(len(kappas)-1):
        if (ms[i]-target)*(ms[i+1]-target) <= 0:
            frac = (target - ms[i]) / (ms[i+1] - ms[i])
            return kappas[i] + frac*(kappas[i+1]-kappas[i])
    return None

print("=" * 70)
print("P0-3: κ_c 有限尺寸标度 (FSS)")
print("=" * 70)
kappas = [k*0.05 for k in range(0, 21)]  # 0..1.0 步长 0.05

sizes = [(2,3), (3,3), (2,4)]
results = {}
for (nx, ny) in sizes:
    print(f"\n--- {nx}x{ny} 格点 ({Lattice(nx,ny).n} 边, {Lattice(nx,ny).N:,} 态) ---")
    lat = Lattice(nx, ny)
    ms, E0s = scan(lat, kappas)
    kc = crossing(kappas, ms)
    results[(nx,ny)] = (ms, kc)
    print(f"  ⟹ κ*(m=0.5) = {kc:.4f}" if kc else "  ⟹ 无交叉")

print("\n" + "=" * 70)
print("3×4 格点 (17 边, 131072 态) — 较大尺寸数据点")
print("=" * 70)
lat34 = Lattice(3, 4)
kappas34 = [k*0.1 for k in range(0, 11)]  # 0..1.0 步长 0.1
ms34, E034 = scan(lat34, kappas34, iters=150)
kc34 = crossing(kappas34, ms34)
results[(3,4)] = (ms34, kc34)
print(f"  ⟹ κ*(m=0.5) = {kc34:.4f}" if kc34 else "  ⟹ 无交叉")

print("\n" + "=" * 70)
print("有限尺寸标度外推")
print("=" * 70)
# L = 线性尺寸 (取短边 √(面积) 或 min(nx,ny))
pts = []
for (nx, ny), (ms, kc) in results.items():
    if kc is not None:
        L = (nx*ny) ** 0.5  # 平均线性尺寸
        pts.append((1.0/L, kc))
        print(f"  {nx}x{ny}: L={L:.3f}, κ*={kc:.4f}")
if len(pts) >= 3:
    # 线性拟合 κ*(L) = κ_c + c/L
    xs = np.array([p[0] for p in pts])
    ys = np.array([p[1] for p in pts])
    A = np.vstack([xs, np.ones_like(xs)]).T
    (slope, intercept), res, *_ = np.linalg.lstsq(A, ys, rcond=None)
    kc_inf = intercept
    print(f"\n  线性拟合: κ*(L) = {kc_inf:.4f} + {slope:.3f}/L")
    print(f"  ⟹ κ_c(∞) = {kc_inf:.4f}")
    print(f"  文献对照 (toric code + 横向场): h_c ≈ 0.328")
    print(f"  偏差: {(kc_inf-0.328)/0.328*100:+.1f}%")
    # 预测 4x4 外推点
    pred_44 = kc_inf + slope/np.sqrt(16)
    print(f"  预测 4×4 κ* ≈ {pred_44:.4f}")
