# -*- coding: utf-8 -*-
"""(6,6,6) N=216 —— 用**修复后的解析器**重算（第 49 轮）。

原失败原因已查明（不是 GAP 失败）：GAP 对超长整数**折行**，|G| 有 223 位 ⟹
「ORDER」行没有第二个 token ⟹ 旧解析器 IndexError。见 `_gap._parse_markers`。
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
dims = (6, 6, 6)
N = 216
k = 108
S = 6
gens = tg.gens_correct(dims)
cfgs = tg.random_cfgs(N, k, S, 6666)
t0 = time.time()
order, sizes = _gap.orbit_sizes_via_gap(gens, cfgs, N, timeout=5400)
dt = time.time() - t0
lns = [math.log(s) for s in sizes]
avg = statistics.mean(lns)
se = statistics.stdev(lns) / math.sqrt(len(lns))
hn = LN2 - avg / N
hn_se = se / N
print("(6,6,6) N=216，L=2 方向 0 个")
print("|G| = {}".format(order))
print("轨道 {:.3e} – {:.3e}".format(min(sizes), max(sizes)))
print("⟨ln|O|⟩ = {:.4f}；⟨ln|O|⟩/N = {:.4f}".format(avg, avg / N))
print("**H/N = {:.4f} ± {:.4f}（95% [{:.4f}, {:.4f}]）**  用时 {:.0f}s".format(
    hn, hn_se, hn - 1.96 * hn_se, hn + 1.96 * hn_se, dt))
print()
print("预判 PB（应与 (4,4,4) 的 0.1839 相差 < 0.05）：|Δ| = {:.4f} ⟹ {}".format(
    abs(hn - 0.1839), "成立" if abs(hn - 0.1839) < 0.05 else "**被否证**"))
print("（第 49 轮的新认知：H/N 随 N 强烈下降 ⟹ N=216 理应远小于 N=64 的 0.1839）")
