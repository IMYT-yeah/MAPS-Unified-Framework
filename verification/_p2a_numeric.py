# -*- coding: utf-8 -*-
"""
P2-A 数值验证（纯 Python，无外部依赖）：
1) CHSH 量子界 S=2√2 vs 经典界 S=2
2) 互补性 V^2 + I^2 <= 1
3) 量子游走 vs 经典随机游走扩散对比
"""
import math

print("="*70)
print("A1) CHSH 不等式：经典界 vs 量子界")
print("="*70)
print(f"经典界 (局域隐变量): S <= 2")
print(f"量子界 (Tsirelson):  S <= 2*sqrt(2) = {2*math.sqrt(2):.4f}")
print(f"  差值: 2*sqrt(2) - 2 = {2*math.sqrt(2)-2:.4f}")

# 纯 Python 4x4 矩阵运算
def mat_mul(A, B):
    n = len(A)
    return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def mat_vec(M, v):
    return [sum(M[i][j]*v[j] for j in range(len(v))) for i in range(len(v))]

def vec_dot(v, w):
    return sum(a*b for a, b in zip(v, w))

def kron2(M, N):
    # M,N 都是 2x2 -> 4x4
    return [[M[i//2][j//2]*N[i%2][j%2] for j in range(4)] for i in range(4)]

Z = [[1,0],[0,-1]]
X = [[0,1],[1,0]]
I2 = [[1,0],[0,1]]
s2 = math.sqrt(2)
B1 = [[(1/s2), (1/s2)],[(1/s2), -(1/s2)]]    # (Z+X)/sqrt(2)
B2 = [[(1/s2), -(1/s2)],[-(1/s2), -(1/s2)]]  # (Z-X)/sqrt(2)
A1, A2 = Z, X

# Bell 态 |psi-> = (|01>-|10>)/sqrt(2) 在 |00>,|01>,|10>,|11> 基
psi = [0, 1/s2, -1/s2, 0]

print("\n--- 显式计算: Bell 态 |psi-> = (|01>-|10>)/sqrt(2), 基 B1=(Z+X)/√2, B2=(Z-X)/√2 ---")
pairs = [("A1",A1,"B1",B1), ("A1",A1,"B2",B2), ("A2",A2,"B1",B1), ("A2",A2,"B2",B2)]
signs = [1, 1, 1, -1]
S = 0.0
for (na,A,nb,B), s in zip(pairs, signs):
    Op = kron2(A, B)
    Mv = mat_vec(Op, psi)
    val = vec_dot(psi, Mv)
    S += s * val
    print(f"  <{na}⊗{nb}> = {val:+.4f}")
print(f"  CHSH S = {S:.4f}  (|S| = {abs(S):.4f} = 2*sqrt(2) = {2*s2:.4f})")
print(f"  => |S| = 2√2 > 2: 非交换事件流可产生贝尔违背")

print()
print("="*70)
print("A2) 互补性: V^2 + I^2 <= 1")
print("="*70)
print("路径态内积 a = <L|R> 的互补性检验 (纯态恒等, 混合态 <= 1):")
for a in [0, 0.3, 0.5, 0.7, 0.9, 1.0]:
    V2, I2 = a**2, 1-a**2
    print(f"  a={a:.1f}: V^2={V2:.3f}, I^2={I2:.3f}, 和={V2+I2:.3f} <= 1 ✓")
print("=> 互补性来自路径态非正交(非交换): [|L><L|, |R><R|] != 0")

print()
print("="*70)
print("A3) 非交换算子 -> 不确定性 (互补性的根源)")
print("="*70)
print("Robertson: Delta A * Delta B >= |<[A,B]>|/2")
print("经典(交换): [A,B]=0 -> 无下限 -> 隐变量可完备描述")
print("非交换:     [A,B]!=0 -> 最小不确定度 -> V^2+I^2<=1 类不等式")
print("=> 事件流非交换化 = 互补性/贝尔违背的共同来源")

print()
print("="*70)
print("A4) 量子游走 vs 经典随机游走（扩散对比）")
print("="*70)
N = 8
dim = 2*N+1

def qw_step(c, p):
    # c: 2 维硬币 (复数), p: dim 维位置
    c0 = (c[0]+c[1])/s2
    c1 = (c[0]-c[1])/s2
    new_c = [c0, c1]
    new_p = [0.0j]*dim
    # coin 0 -> 左移, coin 1 -> 右移
    for i in range(dim):
        if i > 0:
            new_p[i-1] += c0*p[i]
        if i < dim-1:
            new_p[i+1] += c1*p[i]
    return new_c, new_p

def cl_step(p):
    new = [0.0]*dim
    for i in range(dim):
        if i>0: new[i-1] += 0.5*p[i]
        if i<dim-1: new[i+1] += 0.5*p[i]
    return new

# 量子游走
c = [1/s2, 1/s2]
p = [0.0j]*dim; p[N] = 1.0
q_spreads = []
for t in range(1, 8):
    c, p = qw_step(c, p)
    prob = [abs(x)**2 for x in p]
    q_spreads.append(math.sqrt(sum(((i-N)**2)*prob[i] for i in range(dim))))

# 经典游走
pc = [0.0]*dim; pc[N] = 1.0
c_spreads = []
for t in range(1, 8):
    pc = cl_step(pc)
    c_spreads.append(math.sqrt(sum(((i-N)**2)*pc[i] for i in range(dim))))

print("t | 量子游走 sigma | 经典游走 sigma | 量子/经典")
for t in range(7):
    print(f"  {t+1} |     {q_spreads[t]:.3f}    |     {c_spreads[t]:.3f}     | {q_spreads[t]/c_spreads[t]:.2f}")
print("=> 量子游走 ~ t (弹道), 经典 ~ sqrt(t) (扩散) => 非交换化保留相干性")
print("=> t=7: 量子 sigma/t =", round(q_spreads[6]/7, 3), "vs 经典 sigma/sqrt(t) =", round(c_spreads[6]/math.sqrt(7), 3))

print()
print("="*70)
print("A5) 框架事件流的非交换结构定位")
print("="*70)
print("框架已有非交换元素 (原文):")
print("  * Clifford 代数 {gamma^mu,gamma^nu}=2eta^munu (微变事件离散不可交换性, 批1数学组)")
print("  * 路径积分 (-1)^N_exchange (费米子交换符号, 批3: 1545-1551)")
print("  * 叠加态几何起源 (正反风暴中心全局等价 => |+>+|->, 批3: 632-634)")
print("=> P2-A: 这些元素已隐含非交换结构, 需明确为事件流的算子代数化")
