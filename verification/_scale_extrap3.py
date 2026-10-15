# -*- coding: utf-8 -*-
"""
热力学极限标度外推 v3 (正确弦态构造)
- 电荷对 (e-e): Z 串 = 相位翻转 psi = v * Π_{e∈path}(-1)^{g_e}  (端点 A_v 违反)
- 磁通对 (m-m): X 串 = 位翻转 psi = v[idx^mask]                (端点 B_p 违反)
- Wilson Z 环: ⟨W⟩ = Σ|v_i|² Π_{e∈ring}(-1)^{g_i,e}  (对角相位加权)
先 3x3 完整对角化全 κ 验证物理, 再 3x4/4x4 幂迭代
"""
import numpy as np, time

def hidx(nx, ny, i, j): return i*ny + j
def vidx(nx, ny, i, j): return (nx-1)*ny + j*nx + i

def build(nx, ny):
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

class Lattice:
    def __init__(self, nx, ny):
        self.nx, self.ny = nx, ny
        self.n, self.N, self.vertices, self.faces = build(nx, ny)
        self.idx = np.arange(self.N, dtype=np.int64)
        # 预计算每条边的 Z 相位因子: phase_e[i] = (-1)^{bit_e of i} = 1-2*bit
        self.zph = []
        for e in range(self.n):
            self.zph.append(1.0 - 2.0 * ((self.idx >> e) & 1).astype(np.float64))
        self.face_keep = []
        for m in self.faces:
            par = (np.bitwise_count(self.idx & m) & 1).astype(bool)
            self.face_keep.append(par == False)

    def apply_H(self, v, kappa):
        out = np.zeros_like(v)
        out -= 0.5 * len(self.vertices) * v
        for m in self.vertices:
            out[self.idx ^ m] -= 0.5 * v
        for keep in self.face_keep:
            out[keep] -= v[keep]
        for e in range(self.n):
            out[self.idx ^ (1 << e)] -= kappa * v
        return out

    def ground_state(self, kappa, iters):
        rng = np.random.default_rng(42)
        v = rng.random(self.N); v /= np.linalg.norm(v)
        for _ in range(iters):
            w = self.apply_H(v, kappa)
            nm = np.linalg.norm(w)
            if nm < 1e-300: break
            v = w / nm
        w = self.apply_H(v, kappa)
        E0 = float(np.dot(v, w))
        return E0, v

    def path_edges_row0(self, L):
        """第 0 行连续路径: 边 hidx(k,0), k=0..L-1 (顶点 (0,0)->(L,0))"""
        return [hidx(self.nx, self.ny, k, 0) for k in range(L)]

    def charge_pair(self, v, kappa, E0, L):
        """电荷对: Z 串相位翻转, 路径长度 L (边数)"""
        mask = 0
        for e in self.path_edges_row0(L):
            mask |= 1 << e
        phase = np.ones(self.N)
        for e in self.path_edges_row0(L):
            phase *= self.zph[e]
        psi = v * phase
        w = self.apply_H(psi, kappa)
        E = float(np.dot(psi, w))
        return E - E0

    def flux_pair(self, v, kappa, E0, L):
        """磁通对: X 串位翻转, 翻转 L 条连续水平边"""
        mask = 0
        for e in self.path_edges_row0(L):
            mask |= 1 << e
        psi = v[self.idx ^ mask].copy()
        w = self.apply_H(psi, kappa)
        E = float(np.dot(psi, w))
        return E - E0

    def wilson_z(self, v, ring_mask):
        """Wilson Z 环: ⟨W⟩ = Σ|v_i|² Π(-1)^{g_e} = Σ_i v_i² phase_i"""
        phase = np.ones(self.N)
        for e in range(self.n):
            if ring_mask >> e & 1:
                phase *= self.zph[e]
        return float(np.dot(v*v, phase))

    def wilson_ring1(self, v):
        return self.wilson_z(v, self.faces[0])

    def wilson_ring2(self, v):
        """2x1 Z 环: 面(0,0)+面(0,1) 外边界 = h(0,0)|h(0,2)|v(0,0)|v(2,0)"""
        ring = 0
        ring |= 1 << hidx(self.nx, self.ny, 0, 0)
        ring |= 1 << hidx(self.nx, self.ny, 0, 2)
        ring |= 1 << vidx(self.nx, self.ny, 0, 0)
        ring |= 1 << vidx(self.nx, self.ny, 2, 0)
        return self.wilson_z(v, ring)


def run(nx, ny, kappas, iters):
    lat = Lattice(nx, ny)
    print(f"\n===== 格点 {nx}x{ny}: {lat.n} 边, 2^{lat.n}={lat.N:,} 态 =====")
    Lmax = nx - 1
    for k in kappas:
        t0 = time.time()
        E0, v = lat.ground_state(k, iters)
        # 电荷对 Z 串
        Ec = [lat.charge_pair(v, k, E0, L) for L in range(1, Lmax+1)]
        # 磁通对 X 串
        Em = [lat.flux_pair(v, k, E0, L) for L in range(1, Lmax+1)]
        Ls = np.arange(1, Lmax+1, dtype=float)
        ce = np.polyfit(Ls, Ec, 1) if Lmax >= 2 else (float(Ec[0]), 0.0)
        cm = np.polyfit(Ls, Em, 1) if Lmax >= 2 else (float(Em[0]), 0.0)
        w1 = lat.wilson_ring1(v); w2 = lat.wilson_ring2(v)
        sW = -np.log(abs(w2)/abs(w1)) if (abs(w1) > 1e-12 and abs(w2) > 1e-12) else float('nan')
        print(f"  κ={k:.1f}: E0={E0:+.4f} | 电荷σ_E={ce[0]:+.4f} 截距={ce[1]:+.4f} (dE: {np.round(Ec,4)}) | "
              f"磁通σ_m={cm[0]:+.4f} (dE: {np.round(Em,4)}) | ⟨W_Z1⟩={w1:+.4f} ⟨W_Z2⟩={w2:+.4f} σ_W={sW:+.4f} | {time.time()-t0:.0f}s")


if __name__ == "__main__":
    kappas = [0.0, 0.5, 1.0, 2.0]
    print("热力学极限 v3 (正确弦态): H=-ΣA-ΣB-κΣX")
    run(3, 3, kappas, 300)
    run(3, 4, kappas, 400)
    run(4, 4, kappas, 90)
    print("\n5x4 (31边, 21.5亿态): numpy 全态不可行 (需 ~17GB/向量) -> 3点外推")
