# -*- coding: utf-8 -*-
"""补算 (4,4,6) N=96（0 个 L=2 方向），检验「组内 H/N 是否只由 N 决定」。

(2,4,12) 也是 N=96（1 个 L=2 方向），H/N = 0.1338。
若 (4,4,6) 与之接近 ⟹ 组内**形状无关**、H/N 由 N 主导（比第 48 轮的「退化方向数」更细的判据）。
另补 (2,2,14) N=56，看「≥2 个退化方向」组是否继续上升。
"""

import math
import os
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _gap                 # noqa: E402
import _tickgroup as tg     # noqa: E402

LN2 = math.log(2.0)


def hn_of(dims, S, seed):
    N = dims[0] * dims[1] * dims[2]
    k = N // 2
    gens = tg.gens_correct(dims)
    cfgs = tg.random_cfgs(N, k, S, seed)
    t0 = time.time()
    order, sizes = _gap.orbit_sizes_via_gap(gens, cfgs, N, timeout=2400)
    lns = [math.log(s) for s in sizes]
    avg = statistics.mean(lns)
    se = statistics.stdev(lns) / math.sqrt(len(lns)) if len(lns) > 1 else 0.0
    return dict(dims=dims, N=N, ns=sum(1 for d in dims if d == 2), order=order, S=S,
                hn=LN2 - avg / N, hn_se=se / N,
                lo=LN2 - avg / N - 1.96 * se / N, hi=LN2 - avg / N + 1.96 * se / N,
                dt=time.time() - t0)


print("=" * 78)
print("补算：固定 N 换形状")
print("=" * 78)
res = []
for dims, S, seed in (((4, 4, 6), 24, 4460), ((2, 2, 14), 20, 2214)):
    try:
        r = hn_of(dims, S, seed)
    except Exception as exc:
        print("  ⚠️ {} 失败：{}".format(str(dims), str(exc)[:120]))
        continue
    res.append(r)
    print("  {:<11} N={:<4} L=2 方向 {} 个 |G| = {:<40} H/N = {:.4f} ± {:.4f} [{:.3f},{:.3f}]  {:.0f}s".format(
        str(r["dims"]), r["N"], r["ns"], str(r["order"])[:38], r["hn"], r["hn_se"], r["lo"], r["hi"], r["dt"]))

print()
print("--- 与同 N 的对照 ---")
print("  N=96： (2,4,12) = 0.1338（1 个退化方向） vs (4,4,6) = {}（0 个）".format(
    "{:.4f}".format(res[0]["hn"]) if res and res[0]["N"] == 96 else "—"))
if res and res[0]["N"] == 96:
    d = abs(res[0]["hn"] - 0.1338)
    tol = 1.96 * math.sqrt((0.0034 ** 2) + (res[0]["hn_se"] ** 2))
    print("      |Δ| = {:.4f}；两者标准误合成的 95% 容差 ≈ {:.4f} ⟹ {}".format(
        d, tol, "**相容（支持「H/N 由 N 主导」）**" if d <= tol else "不相容 ⟹ 形状仍有独立作用"))
print("  N=56： (2,2,14) = {}（2 个退化方向）".format(
    "{:.4f}".format(res[1]["hn"]) if len(res) > 1 else "—"))
