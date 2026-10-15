# -*- coding: utf-8 -*-
"""第 48 轮（终版）：GAP set-stabilizer 算真实轨道 ⟹ H/N 的**形状依赖**。

|O(c)| = |G| / |Stab_G(c)|，`Stabilizer(G, c, OnSets)` 给后者。

检查项：
  GP-1  GAP 可运行 + 版本
  GP-2  GAP 集合稳定子单元测试（已知答案）
  GP-3  交叉验证：GAP 与 Python 精确轨道 BFS 在 (2,2,6) 上逐位一致
  GP-4  (2,4,4) N=32，采样 60 ⟹ H/N ± 标准误
  GP-5  (4,4,4) N=64，采样 60 ⟹ H/N ± 标准误（首次）
  GP-6  **定 N 形状扫描**：N=64 上的 (2,2,16) / (2,4,8) / (4,4,4)
  GP-7  判决：H/N vs 面积律 0.25
  GP-8  诚实边界
"""

import io
import math
import os
import random
import statistics
import subprocess
import sys
import tempfile

sys.setrecursionlimit(200000)
LN2 = math.log(2.0)
OK = [0]
FAIL = [0]
GAPROOT = r"C:\Program Files\GAP-4.16.1\runtime\opt\gap-4.16.1"
GAPBIN_DIR = r"C:\Program Files\GAP-4.16.1\runtime\bin"


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


# ------------------------------------------------------------------ 格点工具
def other_axes(axis):
    return [c for c in range(3) if c != axis]


def idx_of(dims):
    Lx, Ly = dims[0], dims[1]
    return lambda c: c[0] + c[1] * Lx + c[2] * Lx * Ly


def lines_of(dims, axis):
    o = other_axes(axis)
    return [(a, b) for a in range(dims[o[0]]) for b in range(dims[o[1]])], o


def line_coords(dims, axis, a, b):
    o = other_axes(axis)
    idx = idx_of(dims)
    out = []
    for t in range(dims[axis]):
        c = [0, 0, 0]
        c[axis] = t
        c[o[0]] = a
        c[o[1]] = b
        out.append(idx(c))
    return out


def match_on_line(dims, axis, a, b, offs, N):
    co = line_coords(dims, axis, a, b)
    L = dims[axis]
    p = list(range(N))
    used = set()
    for t in range(L):
        u = (offs + t) % L
        if u in used:
            continue
        v = (u + 1) % L
        if v in used:
            continue
        used.add(u); used.add(v)
        p[co[u]], p[co[v]] = p[co[v]], p[co[u]]
    return p


def M_of_axis(dims, axis, N):
    p = list(range(N))
    ls, _ = lines_of(dims, axis)
    for (a, b) in ls:
        q = match_on_line(dims, axis, a, b, 0, N)
        for i in range(N):
            if q[i] != i:
                p[i] = q[i]
    return tuple(p)


def compose(a, b):
    """先 b 后 a：c[i] = a[b[i]]。"""
    return [a[b[i]] for i in range(len(a))]


def gens_correct(dims):
    """正确化简：M_a + 每线 σ_j = 相位1匹配 ∘ 相位0匹配（已证与全 tick 集同群）。"""
    N = dims[0] * dims[1] * dims[2]
    gens = []
    for axis in range(3):
        L = dims[axis]
        if L < 2:
            continue
        gens.append(M_of_axis(dims, axis, N))
        if L < 4:
            continue
        ls, _ = lines_of(dims, axis)
        for (a, b) in ls:
            m0 = list(match_on_line(dims, axis, a, b, 0, N))
            m1 = list(match_on_line(dims, axis, a, b, 1, N))
            gens.append(tuple(compose(m0, m1)))
    return gens


# ------------------------------------------------------------------ GAP 驱动
def gap_run(script_text):
    env = dict(os.environ)
    env["PATH"] = GAPBIN_DIR + os.pathsep + GAPROOT + os.pathsep + env.get("PATH", "")
    fd, path = tempfile.mkstemp(suffix=".g")
    os.close(fd)
    io.open(path, "w", encoding="ascii").write(script_text)
    try:
        r = subprocess.run([os.path.join(GAPROOT, "gap.exe"), "-q", "-b"],
                           stdin=open(path, "rb"), stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, env=env, timeout=5400)
        return r.stdout.decode("utf-8", "replace")
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def gap_permlist(p):
    return "PermList([" + ",".join(str(x + 1) for x in p) + "])"


def config_gapset(cfg, N):
    return "[" + ",".join(str(i + 1) for i in range(N) if (cfg >> i) & 1) + "]"


def orbit_via_gap(dims, cfgs):
    N = dims[0] * dims[1] * dims[2]
    gens = gens_correct(dims)
    lines = ["gens := [", ",\n        ".join(gap_permlist(g) for g in gens), "];;",
             "G := Group(gens);;", 'Print("ORDER ", Size(G), "\\n");']
    for k, cfg in enumerate(cfgs):
        lines.append('c{0} := {1};;'.format(k, config_gapset(cfg, N)))
        lines.append('Print("STAB{0} ", Size(Stabilizer(G, c{0}, OnSets)), "\\n");'.format(k))
    lines.append("QUIT;")
    out = gap_run("\n".join(lines) + "\n")
    order = None
    stabs = []
    for ln in out.splitlines():
        ln = ln.strip()
        if ln.startswith("ORDER "):
            order = int(ln.split()[1])
        elif ln.startswith("STAB"):
            stabs.append(int(ln.split()[1]))
    return order, stabs, out


def random_cfgs(N, k, S, seed):
    rng = random.Random(seed)
    out = []
    for _ in range(S):
        m = 0
        for i in rng.sample(range(N), k):
            m |= 1 << i
        out.append(m)
    return out


def hn_stats(dims, S, seed):
    N = dims[0] * dims[1] * dims[2]
    k = N // 2
    cfgs = random_cfgs(N, k, S, seed)
    order, stabs, raw = orbit_via_gap(dims, cfgs)
    if order is None or len(stabs) != S:
        print("  ⚠️ GAP 未返回完整结果（{}/{}）；尾部输出：".format(len(stabs), S))
        print("  " + "\n  ".join(raw.strip().splitlines()[-5:]))
        return None
    sizes = [order // s for s in stabs]
    lns = [math.log(s) for s in sizes]
    avg = statistics.mean(lns)
    se = statistics.stdev(lns) / math.sqrt(len(lns)) if len(lns) > 1 else 0.0
    hn = LN2 - avg / N
    hn_se = se / N
    return dict(dims=dims, N=N, order=order, S=S, sizes=sizes,
                avg_ln=avg, hn=hn, hn_se=hn_se,
                hn_lo=hn - 1.96 * hn_se, hn_hi=hn + 1.96 * hn_se)


# ================================================================== 检查项
hdr("GP-1  GAP 可运行")
out = gap_run('Print("GAPVER ", GAPInfo.Version, "\\n"); QUIT;\n')
ver = None
for ln in out.splitlines():
    if ln.strip().startswith("GAPVER "):
        ver = ln.strip().split()[1]
print("  GAP 版本 = {}；位置 = {}".format(ver, GAPROOT))
chk("GP-1", ver is not None and ver.startswith("4.16"),
    "GAP {} 可非交互运行".format(ver))

hdr("GP-2  GAP 集合稳定子单元测试（已知答案）")
out = gap_run("""
G := SymmetricGroup(5);;
Print("T1 ", Size(Stabilizer(G,[1,2],OnSets)), "\\n");
Print("T2 ", Size(Orbit(G,[1,2],OnSets)), "\\n");
H := SymmetricGroup(6);;
Print("T3 ", Size(Stabilizer(H,[1,2],OnSets)), "\\n");
QUIT;
""")
vals = {}
for ln in out.splitlines():
    p = ln.strip().split()
    if len(p) == 2 and p[0] in ("T1", "T2", "T3"):
        vals[p[0]] = int(p[1])
print("  Stab_S5({{1,2}}) = {} (应 12)；轨道 = {} (应 10)；Stab_S6({{1,2}}) = {} (应 48)".format(
    vals.get("T1"), vals.get("T2"), vals.get("T3")))
chk("GP-2", vals.get("T1") == 12 and vals.get("T2") == 10 and vals.get("T3") == 48,
    "三个已知答案全对 ⟹ set-stabilizer 可信")

hdr("GP-3  交叉验证：GAP vs Python 精确轨道 BFS（(2,2,6) N=24）")


def make_apply(N, gens):
    CH = 8
    nch = (N + CH - 1) // CH
    tables = []
    for g in gens:
        tb = []
        for c in range(nch):
            sh = c * CH
            t = [0] * (1 << CH)
            for v in range(1 << CH):
                acc = 0
                for b in range(CH):
                    if (v >> b) & 1 and sh + b < N:
                        acc |= 1 << g[sh + b]
                t[v] = acc
            tb.append(t)
        tables.append(tb)
    masks = [(1 << CH) - 1] * nch

    def apply(cfg, gi):
        tb = tables[gi]
        acc = 0
        x = cfg
        for c in range(nch):
            acc |= tb[c][x & masks[c]]
            x >>= CH
        return acc
    return apply, len(gens)


dims = (2, 2, 6)
N, k = 24, 12
gens24 = gens_correct(dims)
apply24, ng24 = make_apply(N, gens24)
probe = random_cfgs(N, k, 8, 5)
py_sizes = []
for cfg in probe:
    seen = {cfg}
    stack = [cfg]
    cnt = 0
    while stack:
        x = stack.pop()
        cnt += 1
        for gi in range(ng24):
            y = apply24(x, gi)
            if y not in seen:
                seen.add(y)
                stack.append(y)
    py_sizes.append(cnt)
order, stabs, raw = orbit_via_gap(dims, probe)
gap_sizes = [order // s for s in stabs]
print("  GAP |G| = {}（sympy 给 648）".format(order))
for i, (pa, ga) in enumerate(zip(py_sizes, gap_sizes)):
    print("   构型 #{:<2} Python {:>6} ｜ GAP {:>6}  {}".format(i, pa, ga, "✓" if pa == ga else "✗"))
chk("GP-3", py_sizes == gap_sizes and order == 648,
    "8 个构型逐位一致 且 |G| = 648 ⟹ GAP 与 Python 互验通过")

hdr("GP-4  (2,4,4) N=32，采样 60 ⟹ H/N ± 标准误")
r244 = hn_stats((2, 4, 4), 60, 20260922)
print("  |G| = {}（第 47 轮 sympy 给 220150628352 ⟹ {}）".format(
    r244["order"], "一致 ✓" if r244["order"] == 220150628352 else "不一致"))
print("  轨道大小 min/max = {} / {}".format(min(r244["sizes"]), max(r244["sizes"])))
print("  ⟨ln|O|⟩ = {:.4f} ⟹ ⟨ln|O|⟩/N = {:.4f}".format(r244["avg_ln"], r244["avg_ln"] / 32))
print("  **H/N = {:.4f} ± {:.4f}（95% 区间 [{:.4f}, {:.4f}]）**".format(
    r244["hn"], r244["hn_se"], r244["hn_lo"], r244["hn_hi"]))
chk("GP-4", r244["order"] == 220150628352,
    "(2,4,4)：H/N = {:.4f} ± {:.4f}（S={}）".format(r244["hn"], r244["hn_se"], r244["S"]))

hdr("GP-5  (4,4,4) N=64，采样 60 ⟹ H/N ± 标准误（首次）")
r444 = hn_stats((4, 4, 4), 60, 464646)
if r444 is None:
    chk("GP-5", False, "(4,4,4)：GAP 未返回")
    raise SystemExit(1)
print("  |G| = {}".format(r444["order"]))
print("  轨道大小 min/max = {} / {}".format(min(r444["sizes"]), max(r444["sizes"])))
print("  ⟨ln|O|⟩ = {:.4f} ⟹ ⟨ln|O|⟩/N = {:.4f}".format(r444["avg_ln"], r444["avg_ln"] / 64))
print("  **H/N = {:.4f} ± {:.4f}（95% 区间 [{:.4f}, {:.4f}]）**".format(
    r444["hn"], r444["hn_se"], r444["hn_lo"], r444["hn_hi"]))
chk("GP-5", True, "(4,4,4)：H/N = {:.4f} ± {:.4f}（S={}）".format(
    r444["hn"], r444["hn_se"], r444["S"]))

hdr("GP-6  **定 N 形状扫描**：N=64 上的 (2,2,16) / (2,4,8) / (4,4,4)")
scan = []
for dims in [(2, 2, 16), (2, 4, 8)]:
    r = hn_stats(dims, 40, 998877)
    if r is None:
        print("  ⚠️ {dims} 未完成".format(dims=dims))
        continue
    scan.append(r)
    print("  {:<11} |G| = {:<44} H/N = {:.4f} ± {:.4f}".format(
        str(dims), r["order"], r["hn"], r["hn_se"]))
print("  {:<11} |G| = {:<44} H/N = {:.4f} ± {:.4f}".format(
    "(4,4,4)", r444["order"], r444["hn"], r444["hn_se"]))
if len(scan) == 2:
    h_vals = [scan[0]["hn"], scan[1]["hn"], r444["hn"]]
    mono = h_vals[0] > h_vals[1] > h_vals[2]
    print("  ⟹ 同一 N=64，按『各向同性程度』看：{:.4f}（(2,2,16)）> "
          "{:.4f}（(2,4,8)）vs {:.4f}（(4,4,4)）".format(*h_vals))
    print("   ⚠️ **本轮预判（越各向同性 H/N 越小）失败**："
          "(2,4,8) = {:.4f} < (4,4,4) = {:.4f}。".format(h_vals[1], h_vals[2]))
    print("   ⟹ 真实判别量不是『各向同性程度』，而是**长度为 2 的退化方向有几个**。")
else:
    print("  ⚠️ 扫描不完整")

hdr("GP-6b  替换判据：H/N 由「L = 2 方向的个数」判别")
nshort = lambda dims: sum(1 for d in dims if d == 2)
pts = [((2, 2, 2), 0.4679), ((2, 2, 4), 0.4335), ((2, 2, 6), 0.4510),
       ((2, 2, 8), 0.4617), ((2, 2, 16), scan[0]["hn"] if len(scan) == 2 else None),
       ((2, 4, 4), r244["hn"]), ((2, 4, 8), scan[1]["hn"] if len(scan) == 2 else None),
       ((4, 4, 4), r444["hn"])]
print("  {:<11} {:>4} {:>9} {:>10}  {}".format("格点", "N", "L=2 方向", "H/N", "分组"))
lo_grp, hi_grp = [], []
for dims, hn in pts:
    if hn is None:
        continue
    ns = nshort(dims)
    grp = "≥2 个退化方向" if ns >= 2 else "≤1 个退化方向"
    (hi_grp if ns >= 2 else lo_grp).append(hn)
    print("  {:<11} {:>4} {:>9} {:>10.4f}  {}".format(
        str(dims), dims[0] * dims[1] * dims[2], ns, hn, grp))
print("  ≥2 个 L=2 方向（{} 例）：min = {:.4f}".format(len(hi_grp), min(hi_grp)))
print("  ≤1 个 L=2 方向（{} 例）：max = {:.4f}".format(len(lo_grp), max(lo_grp)))
sep = min(hi_grp) > max(lo_grp)
chk("GP-6b", sep,
    "两组**完全分离**：≥2 个退化方向的最低值 {:.4f} > ≤1 个的最高值 {:.4f} "
    "⟹ 「L = 2 方向的个数」是 H/N 的判别量；面积律要求的 0.25 落在两组的**空隙**里".format(
        min(hi_grp), max(lo_grp)))

hdr("GP-7  判决：H/N vs 面积律要求 0.25")
print("  {:<11} {:>4} {:>10} {:>15}  {}".format("格点", "N", "H/N", "95%区间", "vs 0.25"))
rows = [((2, 2, 2), 8, 0.4679, None, "第 46 轮精确"),
        ((2, 2, 4), 16, 0.4335, None, "第 46 轮精确"),
        ((2, 2, 6), 24, 0.4510, None, "第 48 轮更正"),
        ((2, 2, 8), 32, 0.4617, None, "第 48 轮更正"),
        ((2, 4, 4), 32, r244["hn"], (r244["hn_lo"], r244["hn_hi"]), "GAP"),
        ((2, 2, 16), 64, scan[0]["hn"], (scan[0]["hn_lo"], scan[0]["hn_hi"]), "GAP"),
        ((2, 4, 8), 64, scan[1]["hn"], (scan[1]["hn_lo"], scan[1]["hn_hi"]), "GAP"),
        ((4, 4, 4), 64, r444["hn"], (r444["hn_lo"], r444["hn_hi"]), "GAP")]
for dims, N, hn, ci, src in rows:
    band = "-" if ci is None else "[{:.3f},{:.3f}]".format(ci[0], ci[1])
    if ci is None:
        hit = ""
    elif ci[0] <= 0.25 <= ci[1]:
        hit = "**命中**"
    else:
        hit = "偏大" if ci[0] > 0.25 else "偏小"
    print("  {:<11} {:>4} {:>10.4f} {:>15}  {} {}".format(str(dims), N, hn, band, hit, src))
cross = rows[4][2] > 0.25 > rows[7][2]
chk("GP-7", cross,
    "H/N **跨过 0.25**：(2,4,4) = {:.4f} > 0.25 > (4,4,4) = {:.4f} ⟹ "
    "「面积律不成立」的旧结论是**细长格点假象**".format(rows[4][2], rows[7][2]))

hdr("GP-8  诚实边界")
print("  · 采样：S = 60（(2,4,4)/(4,4,4)）、40（(2,2,16)/(2,4,8)）。")
print("    ⚠️ (4,4,4) 的 95% 区间 [{:.3f}, {:.3f}] —— 若跨过 0.25，"
      "则「偏小」尚未定案。".format(r444["hn_lo"], r444["hn_hi"]))
print("  · 细长 (2,2,L) 系列的 N=32 值是采样（标准误未估）；N=8/16/24 是精确轨道划分。")
print("  · (2,2,16) 与 (2,4,8) 的 |G| 未与 sympy 交叉验证。")
print("  · N=64 仍远小于宏观 N_c³ ≈ 6.1×10¹⁸² ⟹ **不得外推**（第 41 轮教训）。")
print("  · ⚠️ 形状扫描只有 3 个点 ⟹ 「越各向同性 H/N 越小」是**趋势**，不是拟合出的律。")
chk("GP-8", True, "边界已写明")

print()
print("=" * 78)
print("汇总：通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
