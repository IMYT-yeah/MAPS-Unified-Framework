# -*- coding: utf-8 -*-
"""诊断：(6,6,6) 到底失败在哪一步。逐步跑 GAP，打印每一步的原始输出。"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _gap                 # noqa: E402
import _tickgroup as tg     # noqa: E402

dims = (6, 6, 6)
N = 216
k = 108
gens = tg.gens_correct(dims)
print("生成元 {} 个，N = {}".format(len(gens), N))

for S in (1, 2):
    cfgs = tg.random_cfgs(N, k, S, 6789)
    lines = ["gens := [", ",\n        ".join(_gap.permlist(g) for g in gens), "];;",
             "G := Group(gens);;"]
    lines.append('Print("ORDER ", Size(G), "\\n");')
    for j, cfg in enumerate(cfgs):
        lines.append("c{} := {};;".format(j, _gap.config_set(cfg, N)))
        lines.append('Print("STAB{} ", Size(Stabilizer(G, c{}, OnSets)), "\\n");'.format(j, j))
    lines.append("QUIT;")
    script = "\n".join(lines) + "\n"
    t0 = time.time()
    out = _gap.gap_run(script, timeout=1200)
    dt = time.time() - t0
    print("\n=== S = {}  用时 {:.0f} s ===".format(S, dt))
    ls = [x.strip() for x in out.splitlines() if x.strip()]
    print("非空输出行数 = {}".format(len(ls)))
    for ln in ls:
        toks = ln.split()
        head = toks[0] if toks else "<空>"
        ntok = len(toks)
        tail = toks[1][:40] if ntok > 1 else "<无第二个 token>"
        print("   头={:<16} token 数={:<3} 第二项={}".format(head[:16], ntok, tail))
    if not ls:
        print("   （GAP 无任何输出 —— 可能超时/崩溃）")
        print("   原始输出片段:", repr(out[:300]))
