# -*- coding: utf-8 -*-
"""
P0-3b (候选 C): 周期边界 (环面 toric code + 横向场) — κ_c 精确化
开边界 FSS (P0-3) 偏差 17–31% 主要源于边界效应; 环面消除边界, κ*(L) 应更快收敛到 κ_c(∞).
H(κ) = -ΣA_v - ΣB_p - κ ΣX_e   (X 场版本, 与 P0-3 同约定, 文献 h_c≈0.328 同约定)
环面: nx×ny 顶点 + nx×ny 面, 边数 n=2·nx·ny, 态数 2^n
  h(i,j): 顶点 (i,j)-(i+1 mod nx, j)    [i∈0..nx-1, j∈0..ny-1]
  v(i,j): 顶点 (i,j)-(i, j+1 mod ny)    [i∈0..nx-1, j∈0..ny-1]
  A_v = Π_{e∋v} X_e (顶点 4 边翻转);  B_p = Π_{e∈∂p} Z_e (面 4 边奇偶, 对角 ±1)
序参量: m(κ,L) = Σ_e ⟨X_e⟩/E ; 交叉点 κ*(m=0.5); 1/L 外推 κ_c(∞)
判据交叉验证: 能隙 Δ(κ)=E1-E0 最小点 κ_Δ
"""
import numpy as np, time

def hbit(nx, ny, i, j): return i*ny + j
def vbit(nx, ny, i, j): return nx*ny + i*ny + j

def build_torus(nx, ny):
    """环面: 返回 n, N, vertex_masks, face_masks"""
    n = 2*nx*ny
    N = 1 << n
    vertices = []
    for i in range(nx):
        for j in range(ny):
            m = 0
            m |= 1 << hbit(nx, ny, (i-1) % nx, j)   # 左
            m |= 1 << hbit(nx, ny, i, j)            # 右
            m |= 1 << vbit(nx, ny, i, (j-1) % ny)   # 下
            m |= 1 << vbit(nx, ny, i, j)            # 上
            vertices.append(m)
    faces = []
    for i in range(nx):
        for j in range(ny):
            m = 0
            m |= 1 << hbit(nx, ny, i, j)                    # 底边
            m |= 1 << hbit(nx, ny, i, (j+1) % ny)           # 顶边
            m |= 1 << vbit(nx, ny, i, j)                    # 左边
            m |= 1 << vbit(nx, ny, (i+1) % nx, j)           # 右边
            faces.append(m)
    return n, N, vertices, faces

class TorusLattice:
    def __init__(self, nx, ny):
        self.nx, self.ny = nx, ny
        self.n, self.N, self.vertices, self.faces = build_torus(nx, ny)
        self.idx = np.arange(self.N, dtype=np.int64)
        self.zph = []
        for e in range(self.n):
            self.zph.append(1.0 - 2.0 * ((self.idx >> e) & 1).astype(np.float64))
        self.face_keep = []
        for m in self.faces:
            par = (np.bitwise_count(self.idx & m) & 1).astype(bool)
            self.face_keep.append(par == False)

    def apply_H(self, v, kappa):
        """H|v⟩ = -ΣA_v|v⟩ - ΣB_p|v⟩ - κΣX_e|v⟩ (A_v: 顶点4边翻转; B_p: 对角; X_e: 单边翻转)"""
        out = np.zeros_like(v)
        out -= 0.5 * len(self.vertices) * v
        for m in self.vertices:
            out[self.idx ^ m] -= 0.5 * v
        for keep in self.face_keep:
            out[keep] -= v[keep]
        for e in range(self.n):
            out[self.idx ^ (1 << e)] -= kappa * v
        return out

    def ground_state(self, kappa, iters, tol=1e-10):
        """幂迭代求基态 (E0, v); 简并时收敛到对称组合"""
        rng = np.random.default_rng(7)
        v = rng.random(self.N); v /= np.linalg.norm(v)
        E0_prev = 0.0
        for _ in range(iters):
            w = self.apply_H(v, kappa)
            nm = np.linalg.norm(w)
            if nm < 1e-300: break
            v = w / nm
            E0 = float(np.dot(v, w))
            if abs(E0 - E0_prev) < tol: break
            E0_prev = E0
        w = self.apply_H(v, kappa)
        E0 = float(np.dot(v, w))
        return E0, v

    def eigs(self, kappa, k=2, tol=1e-7, maxiter=3000):
        """Lanczos (scipy eigsh, LinearOperator) 求最小 k 个特征值/向量 — 大格点用"""
        from scipy.sparse.linalg import LinearOperator, eigsh
        n = self.N
        A = LinearOperator((n, n), matvec=lambda x: self.apply_H(x, kappa), dtype=np.float64)
        evals, evecs = eigsh(A, k=k, which="SA", tol=tol, maxiter=maxiter)
        return evals, evecs

    def order_param(self, v):
        """m = Σ_e ⟨X_e⟩ / n"""
        total = 0.0
        for e in range(self.n):
            flip = self.idx ^ (1 << e)
            total += float(np.dot(v, v[flip]))
        return total / self.n

    def gap(self, kappa, k=3, iters=800):
        """能隙 Δ=E1-E0: 从随机第二态做正交幂迭代 (块幂迭代, 取前 2 特征值)"""
        rng = np.random.default_rng(11)
        V = rng.random((self.N, k)); 
        V = V / np.linalg.norm(V, axis=0, keepdims=True)
        for _ in range(iters):
            W = np.zeros_like(V)
            for a in range(k):
                W[:, a] = self.apply_H(V[:, a], kappa)
            # 正交化 (Gram-Schmidt)
            for a in range(k):
                for b in range(a):
                    W[:, a] -= np.dot(V[:, b], W[:, a]) * V[:, b]
                nm = np.linalg.norm(W[:, a])
                if nm > 1e-300: W[:, a] /= nm
            V = W
        # Rayleigh-Ritz 在 V 上
        Hm = np.array([[np.dot(V[:, a], self.apply_H(V[:, b], kappa)) for b in range(k)] for a in range(k)])
        evals = np.linalg.eigvalsh(Hm)
        return evals[1] - evals[0], evals[0], evals[1]


def crossing(kappas, ms, target=0.5):
    for i in range(len(kappas)-1):
        if (ms[i]-target)*(ms[i+1]-target) <= 0:
            frac = (target - ms[i]) / (ms[i+1] - ms[i])
            return kappas[i] + frac*(kappas[i+1]-kappas[i])
    return None


def scan_torus(nx, ny, kappas, iters=150, do_gap=False, method="power"):
    lat = TorusLattice(nx, ny)
    print(f"\n--- 环面 {nx}x{ny}: {lat.n} 边, 2^{lat.n}={lat.N:,} 态 [method={method}] ---", flush=True)
    ms, E0s = [], []
    for k in kappas:
        t0 = time.time()
        if method == "eigsh":
            evals, evecs = lat.eigs(k, k=2, tol=1e-7)
            E0 = float(evals[0]); v = evecs[:, 0]
            dg = float(evals[1] - evals[0])
        else:
            E0, v = lat.ground_state(k, iters)
            dg = None
        m = lat.order_param(v)
        ms.append(m); E0s.append(E0)
        extra = f" Δ={dg:.4f}" if dg is not None else ""
        if do_gap and dg is None:
            dg, e0, e1 = lat.gap(k, iters=300)
            extra = f" Δ={dg:.4f} (E1={e1:.4f})"
        print(f"  κ={k:.3f}: E0={E0:+.4f} m=⟨X⟩={m:.4f}{extra} ({time.time()-t0:.0f}s)", flush=True)
    kc = crossing(kappas, ms)
    print(f"  ⟹ κ*(m=0.5) = {kc:.4f}" if kc else "  ⟹ 无交叉", flush=True)
    return lat, ms, E0s, kc


def fss_extrap(results, h_lit=0.328):
    print("\n" + "="*70)
    print("有限尺寸标度外推 (环面)")
    print("="*70)
    pts = []
    for (nx, ny), kc in results.items():
        if kc is not None:
            L = (nx*ny) ** 0.5
            pts.append((1.0/L, kc))
            print(f"  环面 {nx}x{ny}: L={L:.3f}, κ*={kc:.4f}")
    if len(pts) >= 3:
        xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
        A = np.vstack([xs, np.ones_like(xs)]).T
        (slope, intercept), *_ = np.linalg.lstsq(A, ys, rcond=None)
        kc_inf = intercept
        print(f"\n  线性拟合: κ*(L) = {kc_inf:.4f} + {slope:.3f}/L")
        print(f"  ⟹ κ_c(∞) = {kc_inf:.4f}")
        print(f"  文献对照 h_c ≈ {h_lit}: 偏差 {(kc_inf-h_lit)/h_lit*100:+.1f}%")
        return kc_inf, slope
    return None, None


if __name__ == "__main__":
    print("="*70)
    print("P0-3b (候选 C): 周期边界环面 — κ_c 精确化")
    print("H(κ) = -ΣA_v - ΣB_p - κΣX_e · 文献 h_c≈0.328 (toric code + 横向场)")
    print("="*70)

    # 小环面: 2x2 (256 态, 精确验证) / 2x3 (4096 态)
    kappas_small = [k*0.05 for k in range(0, 15)]   # 0..0.70
    results = {}
    lat22, ms22, E22, kc22 = scan_torus(2, 2, kappas_small, iters=200)
    results[(2,2)] = kc22
    # 基态验证: κ=0 简并 4 重 (|G|²=4), m=0; E0=-(N_v+N_p)=-8 (2x2 环面)
    print(f"  [验证] 环面 2x2: E0(κ=0)={E22[0]:+.4f} (期望 -8), m(κ=0)={ms22[0]:.4f} (期望 0)", flush=True)

    lat23, ms23, E23, kc23 = scan_torus(2, 3, kappas_small, iters=250)
    results[(2,3)] = kc23

    # 中等环面 3x3 (262144 态) + 能隙判据 — Lanczos
    kappas_mid = [0.0, 0.10, 0.20, 0.25, 0.30, 0.32, 0.34, 0.36, 0.40, 0.45, 0.50, 0.60]
    lat33, ms33, E33, kc33 = scan_torus(3, 3, kappas_mid, method="eigsh", do_gap=True)
    results[(3,3)] = kc33

    # 大环面 3x4 (1677 万态) — Lanczos (LinearOperator, 稀疏内存)
    kappas_large = [0.20, 0.25, 0.28, 0.30, 0.32, 0.34, 0.36, 0.40]
    lat34, ms34, E34, kc34 = scan_torus(3, 4, kappas_large, method="eigsh", do_gap=True)
    results[(3,4)] = kc34

    print("\n" + "="*70)
    kc_inf, slope = fss_extrap(results)

    # 开边界对照 (P0-3): 0.23–0.27; 文献 0.328
    print("\n对照: 开边界 FSS (P0-3) κ_c≈0.23–0.27 · 文献 h_c≈0.328")
    print("环面应显著缩小与文献偏差 (消除边界效应)")
