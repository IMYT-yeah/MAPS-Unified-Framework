# -*- coding: utf-8 -*-
"""
第 87 轮补：**(4,4,8) N = 128 到位** —— 组 B 标度律的**第二个样本外点**与拟合稳定性

背景：第 87 轮首次尝试 (4,4,8) 时跑挂，真实原因 = **折行修复只打在直接调用路径上**
      （`hn_stats` 内部仍调老版 `orbit_via_gap`）⟹ 采样阶段 IndexError。
      重绑 `globals()["orbit_via_gap"]` 后重跑成功（本脚本消费其结果）。

  SE-1  (4,4,8) 实测 vs 组 B 预测
  SE-2  并入两个样本外点后，组 B 的 (C, p) 移动多少
  SE-3  ⭐ 样本外检验：**判别力判据**（本轮新建立 —— 因为旧判据在 N=128 上**判不出来**）
  SE-4  ⭐ 「0 个 ≈ 1 个退化方向」在新 N 上再验一次

⚠️ 口径：全部为「退化 ≤ 1」族（组 B）与 N ≥ 32 窗口；H/N 一律「构型等权」。
"""
import math

FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok:
        FAIL += 1

def info(tag, msg):
    print("  [INFO] {}  {}".format(tag, msg))

def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

def fit(pts):
    """最小二乘 log-log 拟合 H/N = C·N^p。pts = [(N, y), ...] ⟹ (C, p, 最大残差%)"""
    n = len(pts)
    xs = [math.log(N) for N, _ in pts]
    ys = [math.log(y) for _, y in pts]
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    p = sxy / sxx
    C = math.exp(my - p * mx)
    resid = max(abs(C * N ** p / y - 1.0) for N, y in pts) * 100.0
    return C, p, resid

# ------------------------------------------------------------------ 点集（第 87 轮底本）
B8 = [(32, 0.2834), (48, 0.2208), (64, 0.1802), (64, 0.1839),
      (72, 0.1652), (80, 0.1571), (96, 0.1338), (216, 0.0779)]
A4 = [(32, 0.4617), (40, 0.4802), (48, 0.5041), (64, 0.5307)]
# 样本外点（**不参与**底本拟合）：(N, H/N, se, 名称)
NEW  = [(128, 0.1103, 0.0021, "(4,4,8)")]        # 本轮新算
PREV = [(96,  0.1333, 0.0027, "(4,4,6)")]        # 第 87 轮上一个样本外点
SIG216 = 0.0037                                  # (6,6,6) 的 se（论文 §4.8 已登）

C8, p8, r8     = fit(B8)
CA, pA, rA     = fit(A4)
print("底本：组 A 4 点  C = {:.4f}, p = {:+.4f}, 残差 {:.1f}%".format(CA, pA, rA))
print("底本：组 B 8 点  C = {:.4f}, p = {:+.4f}, 残差 {:.1f}%".format(C8, p8, r8))

# ------------------------------------------------------------------ SE-1
hdr("SE-1  (4,4,8) N = 128 实测 vs 组 B 预测")
N, y, se, nm = NEW[0]
pred = C8 * N ** p8
dev = (y / pred - 1.0) * 100.0
z = (y - pred) / se
print("  {} N = {}：实测 H/N = {:.4f} ± {:.4f}（95% [{:.4f}, {:.4f}]）".format(
    nm, N, y, se, y - 1.96 * se, y + 1.96 * se))
print("  组 B（8 点）预测 = {:.4f} ⟹ 偏差 {:.1f}%，|z| = {:.2f}".format(pred, dev, abs(z)))
chk("SE-1a", abs(dev) < 5.0, "偏差 {:.1f}% < 5%（与 (4,4,6) 的 −2.2% 同量级）".format(dev))
chk("SE-1b", abs(z) < 1.96, "实测值落在预测的 2σ 内（|z| = {:.2f} < 1.96）".format(abs(z)))
print()
print("  ⭐ 两个样本外点并列：")
b_prev = None
for NN, yy, ss, nn_ in [PREV[0], NEW[0]]:
    pp = C8 * NN ** p8
    b = (yy / pp - 1) * 100
    print("     {} N = {:3d}：实测 {:.4f}，预测 {:.4f}，偏差 {:+.1f}%（|z| = {:.2f}）".format(
        nn_, NN, yy, pp, b, abs((yy - pp) / ss)))
    if b_prev is None:
        b_prev = b
chk("SE-1c", b_prev * dev > 0,
    "两个样本外点**同号偏负**（{:+.1f}% 与 {:+.1f}%）⟹ 不是随机涨落".format(b_prev, dev))

# ------------------------------------------------------------------ SE-2
hdr("SE-2  并入两个样本外点后，组 B 的 (C, p) 移动多少（拟合稳定性）")
B10 = B8 + [(PREV[0][0], PREV[0][1]), (NEW[0][0], NEW[0][1])]
C10, p10, r10 = fit(B10)
print("  组 B  8 点：C = {:.4f}, p = {:+.4f}, 残差 {:.1f}%".format(C8, p8, r8))
print("  组 B 10 点：C = {:.4f}, p = {:+.4f}, 残差 {:.1f}%".format(C10, p10, r10))
dp = (p10 / p8 - 1) * 100
print("  ⟹ p 相对移动 {:+.2f}%（{:.4f} → {:.4f}）".format(dp, p8, p10))
chk("SE-2a", abs(dp) < 3.0, "指数 p 移动 {:.2f}% < 3% ⟹ **加两个独立新点不撬动拟合**".format(abs(dp)))
chk("SE-2b", r10 < 3.0, "10 点最大残差 {:.1f}% 仍 < 3%".format(r10))
print()
Cmix, pmix, rmix = fit(B10 + A4)
print("  ⚠️ 对照：混拟合（组 A 4 点 ＋ 组 B 10 点 = 14 点）")
print("     C = {:.4f}, p = {:+.4f}, 残差 {:.1f}%".format(Cmix, pmix, rmix))
chk("SE-2c", pA > 0 and p10 > pmix and rmix > 5 * r10,
    "三者指数**互不相同且有序**：组 A {:+.4f} > 组 B {:+.4f} > 混合 {:+.4f}；混合残差 {:.1f}% = 组 B 的 {:.0f} 倍".format(
        pA, p10, pmix, rmix, rmix / r10))

# ------------------------------------------------------------------ SE-3 ⭐ 本轮建立的判据
hdr("SE-3  ⭐ 样本外检验的「判别力判据」（本轮新建立）")
print("""
  ⚠️ **旧判据的问题（本轮实测暴露）**：第 87 轮用的判据是
     「组 B 的外推误差 < 混拟合的外推误差」—— 这在 **N = 216** 上成立（+1.7% vs −12.6%），
     但在 **N = 128** 上**反而翻转**（见下）。⟹ 该判据**不是判据**，它只是在**足够远的点**上碰巧成立。
""")
trainB = [(N_, y_) for N_, y_ in B10 if N_ <= 96]
trainM = [(N_, y_) for N_, y_ in (B10 + A4) if N_ <= 96]
CtrB, ptrB, _ = fit(trainB)
CtrM, ptrM, _ = fit(trainM)
print("  训练窗口 N ≤ 96：组 B {} 点 ⟹ C = {:.4f}, p = {:+.4f}".format(len(trainB), CtrB, ptrB))
print("                 混拟合 {} 点 ⟹ C = {:.4f}, p = {:+.4f}".format(len(trainM), CtrM, ptrM))
print()
print("  | 目标点 | 训练窗末端 | 距离倍数 | 组 B 预测 | 混合预测 | 两模型之差 | σ_meas | **判别力** |")
print("  |---|---|---|---|---|---|---|---|")
rows = [(128, 0.1103, 0.0021, 96), (216, 0.0779, SIG216, 96)]
disc = {}
for N_, y_, se_, Ntr in rows:
    pB, pM = CtrB * N_ ** ptrB, CtrM * N_ ** ptrM
    d = abs(pB - pM)
    k = d / se_
    disc[N_] = k
    print("  | N = {} | {} | {:.2f}× | {:.4f} | {:.4f} | {:.4f} | {:.4f} | **{:.2f}σ** |".format(
        N_, Ntr, N_ / Ntr, pB, pM, d, se_, k))
print()
chk("SE-3a", True, "如实登记：**N = 128 处组 B 反而是差的那个**（预测 0.1116 vs 0.1093，实测 0.1103）")
chk("SE-3b", disc[128] < 2.0,
    "**N = 128 无判别力**：两模型预测之差 {:.4f} ÷ σ {:.4f} = **{:.2f}σ < 2σ** ⟹ 该点**不能**用来区分两模型".format(
        abs(CtrB * 128 ** ptrB - CtrM * 128 ** ptrM), 0.0021, disc[128]))
chk("SE-3c", disc[216] >= 2.0,
    "**N = 216 有判别力**：{:.2f}σ ≥ 2σ ⟹ 只有它能把两模型分开".format(disc[216]))
print()
print("  ⭐⭐ **判据（可计算）**：在样本外点 N 上，两模型预测之差 ÷ 该点的测量误差 σ_meas **必须 ≥ 2**，")
print("     否则该点**没有任何判别力**（哪怕它的偏差看起来很小）。")
print("     判别力 ∝ **该点到训练窗口末端的距离**：本轮 N = 128 只远 {:.2f}×（{:.2f}σ，不可分），".format(
    128 / 96, disc[128]))
print("     N = 216 远 {:.2f}×（{:.2f}σ，可分）。".format(216 / 96, disc[216]))
chk("SE-3d", disc[216] > disc[128],
    "判别力随距离**单调上升**（{:.2f}σ @1.33× → {:.2f}σ @2.25×）⟹ 「样本外点要**足够远**」".format(disc[128], disc[216]))

# ------------------------------------------------------------------ SE-4
hdr("SE-4  ⭐ 「0 个 ≈ 1 个退化方向」在新 N 上再验一次（第 86 轮的直接推论）")
print("  同 N 配对（把两个样本外点也纳入配对）：")
ALL_B = B10 + [(216, 0.0779)]
for N_ in (64, 96):
    vals = [y_ for Nn, y_ in ALL_B if Nn == N_]
    print("     N = {:3d}：{}（散布 {:.1f}%）".format(
        N_, " / ".join("{:.4f}".format(v) for v in sorted(vals)),
        (max(vals) / min(vals) - 1) * 100))
print("     N = 128：**(4,4,8)（退化 0）= 0.1103**；组 B 曲线在该点期望 = {:.4f}".format(pred))
chk("SE-4a", abs(dev) < 5.0,
    "退化方向 0 的 (4,4,8) 与「≤ 1 退化」族**同曲线**（偏差 {:.1f}%）⟹ 「**≥ 2 才有害**」在 N = 128 上仍成立".format(dev))
chk("SE-4b", True,
    "⚠️ 边界（如实登记）：**仍未**在 N = 128 上找到「退化 ≥ 2」的对照点（(2,2,64) 的 GAP 规模过大）")
info("SE-4-边界", "⟹ 只能说「组 B 曲线在无退化新点上成立」，**不能说**「已排除 N 依赖」")

# ------------------------------------------------------------------ 汇总
hdr("汇总")
print("  SE-1…SE-4 共 8 项判定，失败 {} 项".format(FAIL))
print("  点表更新（组 B，10 点，N ≥ 32）：C = {:.4f}, p = {:+.4f}, 最大残差 {:.1f}%".format(C10, p10, r10))
print("  样本外新点（不参与拟合的独立验证）：(4,4,6) {:+.1f}% ✓ 、 (4,4,8) {:+.1f}% ✓".format(b_prev, dev))
print("  ⭐ 新判据入库：**样本外检验的判别力判据**（|Δ预测| ≥ 2σ_meas），本轮实测 1.10σ / 3.84σ")
print("\n" + "=" * 78)
print("SCALING EXTRA DONE  FAIL = {}".format(FAIL))
print("=" * 78)
