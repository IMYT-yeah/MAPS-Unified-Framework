# -*- coding: utf-8 -*-
"""
P0-1 数值复核: Z 场版 H(λ) = -ΣA_v - ΣB_p - λΣZ_e (正确几何)
复核对象:
  1) 端点势报告: 磁通对(m-m)线性势 σ_m ≈ 2λ (旧报 0.82/1.91/3.95 @ λ=0.5/1.0/2.0, 3x3)
  2) ε项报告: 拓扑序→禁闭相变 λ_c ≈ 0.12-0.15 (环面简并 4→1 + 弦密度)
双几何: 开边界 (与 _scale_extrap3 一致的修正 hidx/vidx) + 环面 (mod 索引)
"""
import numpy as np, time

# ============ 正确几何索引 (开边界) ============
def hidx(nx, ny, i, j): return i*ny + j
def vidx(nx, ny, i, j): return (nx-1)*ny + j*nx + i

def build_open(nx, ny):
    n = nx*(ny-1) + ny*(nx-1)
    N = 1 << n
    vertices = []
    for i in range(nx):
        for j in range(ny):
            m = 0
            if i > 0:   m |= 1 << hidx(nx,ny,i-1,j)
            if i < nx-1: m |= 1 << hidx(nx,ny,i,j)
            if j > 0:   m |= 1 << vidx(nx,ny,i,j-1)
            if j < ny-1: m |= 1 << vidx(nx,ny,i,j)
            vertices.append(m)
    faces = []
    for i in range(nx-1):
        for j in range(ny-1):
            m = (1<<hidx(nx,ny,i,j)) | (1<<hidx(nx,ny,i,j+1)) | (1<<vidx(nx,ny,i,j)) | (1<<vidx(nx,ny,i+1,j))
            faces.append(m)
    return n, N, vertices, faces

class OpenLattice:
    """开边界 Z 场版"""
    def __init__(self, nx, ny):
        self.nx, self.ny = nx, ny
        self.n, self.N, self.vertices, self.faces = build_open(nx, ny)
        self.idx = np.arange(self.N, dtype=np.int64)
        self.pop = np.bitwise_count(self.idx).astype(np.float64)
        self.face_keep = []
        for m in self.faces:
            par = (np.bitwise_count(self.idx & m) & 1).astype(bool)
            self.face_keep.append(par == False)

    def apply_H(self, v, lam):
        out = np.zeros_like(v)
        out -= 0.5 * len(self.vertices) * v
        for m in self.vertices:
            out[self.idx ^ m] -= 0.5 * v
        for keep in self.face_keep:
            out[keep] -= v[keep]
        # Z 场: -λΣZ_e = -λ(n - 2·popcount)
        out -= lam * (self.n - 2.0 * self.pop) * v
        return out

    def ground_state(self, lam, iters):
        rng = np.random.default_rng(42)
        v = rng.random(self.N); v /= np.linalg.norm(v)
        for _ in range(iters):
            w = self.apply_H(v, lam)
            nm = np.linalg.norm(w)
            if nm < 1e-300: break
            v = w / nm
        w = self.apply_H(v, lam)
        return float(np.dot(v, w)), v

    def flux_pair(self, v, lam, E0, L):
        """磁通对: X 串位翻转, 翻转第 0 行连续 L 条水平边 (端点面 B_p 违反)"""
        mask = 0
        for k in range(L):
            mask |= 1 << hidx(self.nx, self.ny, k, 0)
        psi = v[self.idx ^ mask].copy()
        w = self.apply_H(psi, lam)
        return float(np.dot(psi, w)) - E0

    def string_density(self, v):
        """弦密度: ⟨Σ_e g_e⟩/n = ⟨Σ(1-Z_e)/2⟩/n"""
        ze = 1.0 - 2.0 * ((self.idx >> 0) & 1).astype(np.float64)  # 每边同构, 用通用式
        sd = 0.0
        for e in range(self.n):
            ph = 1.0 - 2.0 * ((self.idx >> e) & 1).astype(np.float64)
            sd += float(np.dot(v*v, (1.0 - ph) / 2.0))
        return sd / self.n


# ============ 环面几何 (mod 索引) ============
class Torus:
    """环面 Lx x Ly 格点规范 (Z 场版), 完整对角化友好"""
    def __init__(self, nx, ny):
        self.nx, self.ny = nx, ny
        self.n = 2 * nx * ny           # 水平 nx*ny + 竖直 nx*ny
        self.N = 1 << self.n
        self.idx = np.arange(self.N, dtype=np.int64)
        # hidx(i,j) = i*ny + j (i,j mod); vidx(i,j) = nx*ny + i*ny + j
        self.vertices = []
        for i in range(nx):
            for j in range(ny):
                m = 0
                m |= 1 << ((i-1) % nx) * ny + j          # 上 hidx(i-1,j)
                m |= 1 << i * ny + j                      # 下 hidx(i,j)
                m |= 1 << nx*ny + i*ny + ((j-1) % ny)     # 左 vidx(i,j-1)
                m |= 1 << nx*ny + i*ny + j                # 右 vidx(i,j)
                self.vertices.append(m)
        self.faces = []
        for i in range(nx):
            for j in range(ny):
                m = 0
                m |= 1 << i*ny + j                        # 上 hidx(i,j)
                m |= 1 << i*ny + (j+1) % ny               # 下 hidx(i,j+1)
                m |= 1 << nx*ny + i*ny + j                # 左 vidx(i,j)
                m |= 1 << nx*ny + ((i+1)%nx)*ny + j       # 右 vidx(i+1,j)
                self.faces.append(m)
        self.face_keep = []
        for m in self.faces:
            par = (np.bitwise_count(self.idx & m) & 1).astype(bool)
            self.face_keep.append(par == False)
        self.pop = np.bitwise_count(self.idx).astype(np.float64)

    def apply_H(self, v, lam):
        out = np.zeros_like(v)
        out -= 0.5 * len(self.vertices) * v
        for m in self.vertices:
            out[self.idx ^ m] -= 0.5 * v
        for keep in self.face_keep:
            out[keep] -= v[keep]
        out -= lam * (self.n - 2.0 * self.pop) * v
        return out

    def dense_H(self, lam):
        H = np.zeros((self.N, self.N))
        H -= 0.5 * len(self.vertices) * np.eye(self.N)
        for m in self.vertices: H[self.idx, self.idx ^ m] -= 0.5
        for keep in self.face_keep: H[keep, keep] -= 1.0
        H[np.arange(self.N), np.arange(self.N)] -= lam * (self.n - 2.0 * self.pop)
        return H


def flux_sigma(lat, lam, iters):
    E0, v = lat.ground_state(lam, iters)
    Lmax = lat.nx - 1
    if Lmax < 2: return None
    pts = [lat.flux_pair(v, lam, E0, L) for L in range(1, Lmax+1)]
    Ls = np.arange(1, Lmax+1, dtype=float)
    coef = np.polyfit(Ls, pts, 1)
    return coef[0], coef[1], pts, E0


if __name__ == "__main__":
    print("=" * 74)
    print("P0-1 数值复核: Z 场版 H=-ΣA-ΣB-λΣZ_e (正确几何)")
    print("=" * 74)

    # ---- 1) 开边界 3x3 完整对角化验证 (λ=0 应 E0=-13, 能隙 1) ----
    lat = OpenLattice(3, 3)
    H = np.zeros((lat.N, lat.N))
    H -= 0.5 * len(lat.vertices) * np.eye(lat.N)
    for m in lat.vertices: H[lat.idx, lat.idx ^ m] -= 0.5
    for keep in lat.face_keep: H[keep, keep] -= 1.0
    ev = np.linalg.eigvalsh(H)
    print(f"\n[验证] 开边界 3x3 λ=0: E0={ev[0]:+.4f} (期望 -13), 能隙={ev[1]-ev[0]:+.4f} (期望 1)")

    # ---- 2) 磁通对线性势 σ_m (开边界 3x3 / 3x4) ----
    print("\n--- 磁通对 (X 串) 线性势 σ_m ---")
    for (nx, ny, it) in [(3, 3, 300), (3, 4, 400)]:
        lat = OpenLattice(nx, ny)
        print(f"格点 {nx}x{ny} ({lat.N:,} 态):")
        for lam in [0.0, 0.5, 1.0, 2.0]:
            t0 = time.time()
            r = flux_sigma(lat, lam, it)
            if r is None: continue
            sigma, off, pts, E0 = r
            print(f"  λ={lam:.1f}: σ_m={sigma:+.4f} (2λ={2*lam:.2f}, 偏差 {(sigma-2*lam)/(2*lam)*100:+.1f}% if λ>0 else 0) 截距={off:+.4f} dE={np.round(pts,4)} | {time.time()-t0:.0f}s")

    # ---- 3) 相变扫描: 环面 2x2 / 2x3 (简并 4→1 + 弦密度 + 能隙) ----
    print("\n--- 相变扫描: 环面 (拓扑序简并 4→1) ---")
    lams = [0.0, 0.05, 0.10, 0.12, 0.15, 0.20, 0.30, 0.50, 0.70, 1.0]
    for (nx, ny) in [(2, 2), (2, 3)]:
        tor = Torus(nx, ny)
        print(f"\n环面 {nx}x{ny} ({tor.N:,} 态, {tor.n} 边):")
        for lam in lams:
            H = tor.dense_H(lam)
            evs = np.linalg.eigvalsh(H)
            # 基态简并: 低能谱中 < E0+1e-4 的个数
            deg = int(np.sum(evs < evs[0] + 1e-4))
            gap = evs[1] - evs[0] if tor.N > 1 else float('nan')
            # 弦密度: 用基态
            gs = None
            print(f"  λ={lam:5.2f}: E0={evs[0]:+8.4f} 简并={deg} 能隙={gap:8.4f}")

    # ---- 4) 相变扫描: 开边界 3x3 (弦密度 + 能隙, 完整对角化) ----
    print("\n--- 相变扫描: 开边界 3x3 (弦密度 + 能隙) ---")
    lat = OpenLattice(3, 3)
    for lam in lams:
        H = np.zeros((lat.N, lat.N))
        H -= 0.5 * len(lat.vertices) * np.eye(lat.N)
        for m in lat.vertices: H[lat.idx, lat.idx ^ m] -= 0.5
        for keep in lat.face_keep: H[keep, keep] -= 1.0
        H[np.arange(lat.N), np.arange(lat.N)] -= lam * (lat.n - 2.0 * lat.pop)
        evs, evecs = np.linalg.eigh(H)
        gs = evecs[:, 0]
        sd = 0.0
        for e in range(lat.n):
            ph = 1.0 - 2.0 * ((lat.idx >> e) & 1).astype(np.float64)
            sd += float(np.dot(gs*gs, (1.0 - ph) / 2.0))
        sd /= lat.n
        print(f"  λ={lam:5.2f}: E0={evs[0]:+8.4f} 能隙={evs[1]-evs[0]:8.4f} 弦密度={sd:.4f}")
