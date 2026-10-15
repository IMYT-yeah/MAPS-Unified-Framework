# -*- coding: utf-8 -*-
"""第 50 轮（GAP 验证）：用**独立方法**（GAP 随机构型采样）复核半满层 H/N。

目的：本轮查出第 48 轮的 Python 全层脚本用了「轨道等权」（偏离第 40 轮定义）。
本脚本用 GAP（随机构型采样 = 构型等权）独立复核三个半满层值：

    (2,2,2) k=4   : 本轮精确值 0.4679（与第 46 轮一致）
    (2,2,6) k=12  : 本轮精确值 0.4334（第 48 轮报 0.4510 —— 疑为口径错）
    (2,2,8) k=16  : 第 49 轮报 0.4617（GAP，构型等权）

若 GAP 采样与精确值一致 ⟹ 口径判定成立（构型等权是正确口径）。
"""

import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _gap
import _tickgroup as tg

LN2 = math.log(2.0)
OK = [0]
FAIL = [0]


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


print("GAP 可用:", _gap.gap_available())

hdr("LV  GAP 采样复核半满层（S = 40，构型等权）")
JOBS = [((2, 2, 2), 4, 0.4679, "本轮精确值（与第 46 轮一致）"),
        ((2, 2, 6), 12, 0.4334, "本轮精确值（第 48 轮报 0.4510）"),
        ((2, 2, 8), 16, 0.4617, "第 47/49 轮 GAP 值")]
print("  {:>10} {:>5} {:>10} {:>12} {:>10}  {}".format(
    "格点", "k", "参考值", "GAP 采样值", "差", "参考来源"))
for dims, k, ref, src in JOBS:
    N = dims[0] * dims[1] * dims[2]
    gens = tg.gens_correct(dims)
    cfgs = tg.random_cfgs(N, k, 40, 777)
    t0 = time.time()
    order, sizes = _gap.orbit_sizes_via_gap(gens, cfgs, N)
    dt = time.time() - t0
    lns = [math.log(s) for s in sizes]
    m = sum(lns) / len(lns)
    sd = math.sqrt(sum((x - m) ** 2 for x in lns) / (len(lns) - 1))
    se = sd / math.sqrt(len(lns))
    h = LN2 - m / N
    h_se = se / N
    print("  {:>10} {:>5} {:>10.4f} {:>12.4f} {:>+10.4f}  {}".format(
        str(dims), k, ref, h, h - ref, src))
    print("             |G| = {}（{} 位）；⟨ln|O|⟩ = {:.4f} ± {:.4f}；"
          "H/N 的 1σ = ±{:.4f}；用时 {:.0f} s".format(
              order, len(str(order)), m, se, h_se, dt))
    tol = max(4 * h_se, 0.01)
    chk("LV-{}".format(N), abs(h - ref) < tol,
        "{}：GAP 采样 {:.4f} vs 参考 {:.4f}（容差 {:.4f} = 4σ）⟹ {}".format(
            str(dims), h, ref, tol, "一致" if abs(h - ref) < tol else "**不一致**"))

print()
print("  结论：若 (2,2,6) 的 GAP 采样值 ≈ 0.4334（而非 0.4510）,")
print("        则确认第 48 轮那个 0.4510 是**口径错误**（轨道等权），而非生成元问题。")

print()
print("=" * 78)
print("汇总：通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
