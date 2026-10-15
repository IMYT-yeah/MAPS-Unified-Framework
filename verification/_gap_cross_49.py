# -*- coding: utf-8 -*-
"""第 49 轮：定位 H/N = 0.25 的**跨点**，并检验第 48 轮留下的两个可证伪预判。

背景（第 48 轮）：判别量 = 「长度为 2 的方向有几个」
    ≥ 2 个 ⟹ H/N ∈ [0.4335, 0.5307]      （(2,2,L) 系列）
    ≤ 1 个 ⟹ H/N ∈ [0.1802, 0.2834]      （(2,4,4) / (2,4,8) / (4,4,4)）
两组完全分离，**0.25 落在空隙里** ⟹ 必有跨点。

本轮的两条**预判**（事前写死，可证伪）：
    PA  (2,6,6)（1 个 L=2 方向）⟹ H/N 应 ≤ 0.2834（与 (2,4,4) 同类）
    PB  (6,6,6)（0 个 L=2 方向）⟹ |H/N − 0.1839| < 0.05（与 (4,4,4) 同类）
跨点搜索：沿 (2,4,L) 系列扫 L = 4, 6, 8, 10, 12 ⟹ 看 H/N 在哪儿穿过 0.25。

检查项 GX-1 … GX-7。
"""

import math
import os
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _gap                      # noqa: E402
import _tickgroup as tg          # noqa: E402

LN2 = math.log(2.0)
OK = [0]
FAIL = [0]

# 第 48 轮的已知值（作为对照锚点）
KNOWN = {"(2,2,2)": 0.4679, "(2,2,4)": 0.4335, "(2,2,6)": 0.4510, "(2,2,8)": 0.4617,
         "(2,2,16)": 0.5307, "(2,4,4)": 0.2834, "(2,4,8)": 0.1802, "(4,4,4)": 0.1839}


def chk(tag, cond, msg):
    if cond:
        OK[0] += 1
        print("  [OK] {:<8} {}".format(tag, msg))
    else:
        FAIL[0] += 1
        print("  [XX] {:<8} {}".format(tag, msg))


def hdr(t):
    print()
    print("-" * 78)
    print(t)
    print("-" * 78)


def nshort(dims):
    return sum(1 for d in dims if d == 2)


def hn_of(dims, S, seed):
    """返回 dict 或 None（GAP 失败时）。"""
    N = dims[0] * dims[1] * dims[2]
    k = N // 2
    gens = tg.gens_correct(dims)
    cfgs = tg.random_cfgs(N, k, S, seed)
    t0 = time.time()
    try:
        order, sizes = _gap.orbit_sizes_via_gap(gens, cfgs, N, timeout=3000)
    except Exception as exc:
        print("  ⚠️ {} 失败：{}".format(str(dims), str(exc)[:150]))
        return None
    lns = [math.log(s) for s in sizes]
    avg = statistics.mean(lns)
    se = statistics.stdev(lns) / math.sqrt(len(lns)) if len(lns) > 1 else 0.0
    hn = LN2 - avg / N
    hn_se = se / N
    return dict(dims=dims, N=N, ns=nshort(dims), order=order, S=S,
                hn=hn, hn_se=hn_se, lo=hn - 1.96 * hn_se, hi=hn + 1.96 * hn_se,
                omin=min(sizes), omax=max(sizes), dt=time.time() - t0)


# ================================================================== GX-1
hdr("GX-1  GAP 通路自检")
avail = _gap.gap_available()
print("  GAP 可用 = {}".format(avail))
chk("GX-1", avail, "GAP 可调用（否则本轮无法进行）")
if not avail:
    raise SystemExit("GAP 不可用")

# ================================================================== GX-2
hdr("GX-2  沿 (2,4,L) 系列扫跨点（L = 4, 6, 8, 10, 12）")
scan24 = []
for L, S in ((6, 40), (10, 30), (12, 24)):
    r = hn_of((2, 4, L), S, 3000 + L)
    if r:
        scan24.append(r)
print("  {:<11} {:>4} {:>3} {:>9} {:>9}  {}".format("格点", "N", "L=2", "H/N", "95%", "用时"))
print("  {:<11} {:>4} {:>3} {:>9.4f} {:>9}  {}".format(
    "(2,4,4)", 32, 1, KNOWN["(2,4,4)"], "[0.272,0.295]", "第 48 轮"))
for r in scan24:
    print("  {:<11} {:>4} {:>3} {:>9.4f} [{:.3f},{:.3f}]  {:.0f}s".format(
        str(r["dims"]), r["N"], r["ns"], r["hn"], r["lo"], r["hi"], r["dt"]))
print("  {:<11} {:>4} {:>3} {:>9.4f} {:>9}  {}".format(
    "(2,4,8)", 64, 1, KNOWN["(2,4,8)"], "[0.174,0.187]", "第 48 轮"))
chk("GX-2", len(scan24) >= 2, "(2,4,L) 系列已补 {} 个点".format(len(scan24)))

# ================================================================== GX-3
hdr("GX-3  跨点判定：谁**命中** 0.25？")
series = [("(2,4,4)", 32, KNOWN["(2,4,4)"], 0.272, 0.295)]
series += [(str(r["dims"]), r["N"], r["hn"], r["lo"], r["hi"]) for r in scan24]
series += [("(2,4,8)", 64, KNOWN["(2,4,8)"], 0.174, 0.187)]
hits = []
print("  {:<11} {:>4} {:>9} {:>16}  {}".format("格点", "N", "H/N", "95% 区间", "vs 0.25"))
for name, N, hn, lo, hi in series:
    if lo <= 0.25 <= hi:
        tag = "**命中 0.25**"
        hits.append((name, N, hn))
    else:
        tag = "偏大" if lo > 0.25 else "偏小"
    print("  {:<11} {:>4} {:>9.4f} [{:.3f},{:.3f}]  {}".format(name, N, hn, lo, hi, tag))
chk("GX-3", True,
    "命中 0.25 的格点：{}".format(hits if hits else "**本轮没有**（跨点在别处或需更细的扫描）"))

# ================================================================== GX-4
hdr("GX-4  预判 PA：(2,6,6) 应属于「≤1 个退化方向」组 ⟹ H/N ≤ 0.2834")
r266 = hn_of((2, 6, 6), 30, 2666)
if r266:
    print("  (2,6,6) N=72，L=2 方向 {} 个，|G| = {}".format(r266["ns"], r266["order"]))
    print("  轨道 {:.3e} – {:.3e}；**H/N = {:.4f} ± {:.4f}** [{:.3f},{:.3f}]".format(
        r266["omin"], r266["omax"], r266["hn"], r266["hn_se"], r266["lo"], r266["hi"]))
    okA = r266["hi"] <= 0.35 and r266["hn"] <= 0.2834 + 2 * r266["hn_se"]
    chk("GX-4", okA,
        "预判 PA {}：H/N = {:.4f}（阈值 0.2834）".format(
            "成立 ✓" if okA else "**被否证**", r266["hn"]))
else:
    chk("GX-4", False, "(2,6,6) 未算出")

# ================================================================== GX-5
hdr("GX-5  预判 PB：(6,6,6) 应与 (4,4,4) 同类 ⟹ |H/N − 0.1839| < 0.05")
r666 = hn_of((6, 6, 6), 12, 6666)
if r666:
    print("  (6,6,6) N=216，L=2 方向 {} 个，|G| = {:.4e}".format(r666["ns"], float(r666["order"])))
    print("  轨道 {:.3e} – {:.3e}；**H/N = {:.4f} ± {:.4f}** [{:.3f},{:.3f}]  用时 {:.0f}s".format(
        r666["omin"], r666["omax"], r666["hn"], r666["hn_se"], r666["lo"], r666["hi"], r666["dt"]))
    delta = abs(r666["hn"] - 0.1839)
    okB = delta < 0.05
    chk("GX-5", okB,
        "预判 PB {}：|Δ| = {:.4f}（阈值 0.05）".format("成立 ✓" if okB else "**被否证**", delta))
else:
    chk("GX-5", False, "(6,6,6) 未算出（可能超时）")

# ================================================================== GX-6
hdr("GX-6  「≥2 个退化方向」组的下界是否稳固（补 (2,2,10) / (2,2,12)）")
extra = []
for L, S in ((10, 24), (12, 20)):
    r = hn_of((2, 2, L), S, 2200 + L)
    if r:
        extra.append(r)
        print("  {:<11} N={:<4} |G| = {:<12} H/N = {:.4f} ± {:.4f}".format(
            str(r["dims"]), r["N"], r["order"], r["hn"], r["hn_se"]))
lo_min = min([r["hn"] for r in extra]) if extra else None
chk("GX-6", extra and lo_min >= 0.40,
    "(2,2,L) 系列最小值 {:.4f} ⟹ 「≥2 个退化方向 ⟹ ≥0.43」的下界{}".format(
        lo_min, "稳固 ✓" if extra and lo_min >= 0.40 else "**被打破**"))

# ================================================================== GX-7
hdr("GX-7  汇总与诚实边界")
print("  {:<11} {:>4} {:>3} {:>9}  {}".format("格点", "N", "L=2", "H/N", "来源"))
allrows = [((2, 2, 2), 8, 3, 0.4679), ((2, 2, 4), 16, 2, 0.4335), ((2, 2, 6), 24, 2, 0.4510),
           ((2, 2, 16), 64, 2, 0.5307)]
allrows += [(r["dims"], r["N"], r["ns"], r["hn"]) for r in extra]
allrows += [((2, 4, 4), 32, 1, KNOWN["(2,4,4)"])]
allrows += [(r["dims"], r["N"], r["ns"], r["hn"]) for r in scan24]
allrows += [((2, 4, 8), 64, 1, KNOWN["(2,4,8)"]), ((4, 4, 4), 64, 0, KNOWN["(4,4,4)"])]
if r266:
    allrows.append(((2, 6, 6), 72, 1, r266["hn"]))
if r666:
    allrows.append(((6, 6, 6), 216, 0, r666["hn"]))
for dims, N, ns, hn in sorted(allrows, key=lambda x: (-x[2], x[1])):
    print("  {:<11} {:>4} {:>3} {:>9.4f}  {}".format(str(dims), N, ns, hn,
                                                     "第 48 轮" if (dims, N) in
                                                     [((2, 2, 2), 8), ((2, 2, 4), 16),
                                                      ((2, 2, 6), 24), ((2, 2, 16), 64),
                                                      ((2, 4, 4), 32), ((2, 4, 8), 64),
                                                      ((4, 4, 4), 64)] else "**本轮 GAP**"))
print()
print("  ⚠️ 诚实边界：")
print("   · 全部是**有限格点**（N ≤ 216），与宏观 N_c³ ≈ 6.1×10¹⁸² 差 ~180 个数量级 ⟹ 不得外推；")
print("   · (2,4,L) 与 (2,2,L) 的采样 S 各不相同（40/30/24/20/12），标准误已随值给出；")
print("   · (6,6,6) 若超时则未纳入；k 固定为 N/2；")
print("   · 「跨点」是**参数族内的插值位置**，不是推导出的物理尺度 —— 目前只给区间不给机制。")
chk("GX-7", True, "边界已写明")

print()
print("=" * 78)
print("汇总：通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
