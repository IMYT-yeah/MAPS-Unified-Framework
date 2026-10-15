# -*- coding: utf-8 -*-
"""
P0-1 复核 v2: 约束扇区方法测磁通对弦张力 (正确方法)
关键: A_v 项保持 B_p 扇区 (翻转4边 -> 每面0或2次) + Z场对角 -> B_p 违反扇区是 H 不变子空间
磁通对: 面 A, B 违反 (B_p=0), 其余面满足 (B_p=1); 距离 = 面格最短距离
E_pair(d) = E(扇区) - E(无违反扇区) = 2E_m + σ_m·d
"""
import numpy as np, time

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
    def __init__(self, nx, ny):
        self.nx, self.ny = nx, ny
        self.n, self.N, self.vertices, self.faces = build_open(nx, ny)
        self.idx = np.arange(self.N, dtype=np.int64)
        self.pop = np.bitwise_count(self.idx).astype(np.float64)
        # 每面的 parity (bool: True = 环积偶 = B_p=1)
        self.face_par = []
        for m in self.faces:
            self.face_par.append((np.bitwise_count(self.idx & m) & 1).astype(bool))

    def apply_H(self, v, lam):
        out = np.zeros_like(v)
        out -= 0.5 * len(self.vertices) * v
        for m in self.vertices:
            out[self.idx ^ m] -= 0.5 * v
        for par in self.face_par:
            keep = (par == False)
            out[keep] -= v[keep]
        out -= lam * (self.n - 2.0 * self.pop) * v
        return out

    def sector_mask(self, violate_faces):
        """B_p 违反扇区掩码: 指定面 B_p=0 (环积奇, par=True), 其余 B_p=1 (环积偶, par=False)"""
        keep = np.ones(self.N, dtype=bool)
        for fi, par in enumerate(self.face_par):
            if fi in violate_faces:
                keep &= (par == True)      # 违反面: 环积奇
            else:
                keep &= (par == False)     # 满足面: 环积偶
        return keep

    def sector_gs(self, lam, violate_faces, iters=300):
        """扇区基态 (幂迭代投影)"""
        keep = self.sector_mask(violate_faces)
        n_sub = int(keep.sum())
        rng = np.random.default_rng(7)
        v = rng.random(n_sub); v /= np.linalg.norm(v)
        for _ in range(iters):
            wf = np.zeros(self.N)
            wf[keep] = v
            wf = self.apply_H(wf, lam)
            v = wf[keep]
            nm = np.linalg.norm(v)
            if nm < 1e-300: break
            v = v / nm
        wf = np.zeros(self.N); wf[keep] = v
        wf = self.apply_H(wf, lam)
        return float(np.dot(v, wf[keep]))


def face_dist(nx, ny, fa, fb):
    """面格距离 (开边界面 (i,j) 的曼哈顿距离)"""
    ia, ja = fa // (ny-1), fa % (ny-1)
    ib, jb = fb // (ny-1), fb % (ny-1)
    return abs(ia-ib) + abs(ja-jb)


if __name__ == "__main__":
    print("=" * 78)
    print("P0-1 复核 v2: 约束扇区方法测磁通对弦张力 (正确方法)")
    print("=" * 78)

    for (nx, ny) in [(3, 3), (3, 4)]:
        lat = OpenLattice(nx, ny)
        nf = len(lat.faces)
        print(f"\n===== 开边界 {nx}x{ny}: {lat.N:,} 态, {lat.n} 边, {nf} 面 =====")
        # 磁通对配置: 面沿第 0 行 (0,0),(0,1),... 距离 d; 3x3 补对角 d=2
        pairs = []
        if nf >= 2:
            pairs.append((1, 0, 1))                      # 面0-面1 距离1
        if nf >= 3:
            pairs.append((2, 0, 2))                      # 面0-面2 距离2 (同排)
        if (nx, ny) == (3, 3) and nf >= 4:
            pairs.append((2, 0, 3))                      # 面0-面3 对角 距离2
        for lam in [0.0, 0.5, 1.0, 2.0]:
            t0 = time.time()
            E0 = lat.sector_gs(lam, [], iters=400 if lam == 0 else 300)
            pts = []
            for (d, fa, fb) in pairs:
                Ed = lat.sector_gs(lam, [fa, fb])
                pts.append((d, Ed - E0))
            # 线性拟合 σ_m (d vs E)
            if len(pts) >= 2:
                ds = np.array([p[0] for p in pts], float)
                Es = np.array([p[1] for p in pts], float)
                coef = np.polyfit(ds, Es, 1)
                sigma, off = coef[0], coef[1]
            else:
                sigma, off = pts[0][1], 0.0
            print(f"  λ={lam:.1f}: 磁通对 dE(d): {[(d, round(e,4)) for d,e in pts]} | "
                  f"σ_m={sigma:+.4f} (2λ={2*lam:.2f}) 截距={off:+.4f} | {time.time()-t0:.0f}s")
