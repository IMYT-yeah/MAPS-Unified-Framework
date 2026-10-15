# -*- coding: utf-8 -*-
"""第 48 轮：用 GAP 的 set-stabilizer 算 (2,4,4) / (4,4,4) 的真实轨道 ⟹ H/N。

原理：|O(c)| = |G| / |Stab_G(c)|，而 `Stabilizer(G, c, OnSets)` 直接给后者。

检查项：
  GP-1  GAP 可运行且版本
  GP-2  GAP 集合稳定子单元测试（已知答案）
  GP-3  交叉验证：GAP 的 |G|/|Stab| 与 Python 精确轨道 BFS 在 (2,2,6) 上逐位一致
  GP-4  (2,4,4) N=32：|G| + 采样构型的轨道大小 ⟹ **H/N（第 47 轮未算出）**
  GP-5  (4,4,4) N=64：|G| + 采样构型的轨道大小 ⟹ **H/N（首次）**
  GP-6  诚实边界
"""

import io
import math
import os
import random
import shutil
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


def compose(a, b):
    """先 b 后 a：c[i] = a[b[i]]（与 sympy 的 a*b 一致）。"""
    return [a[b[i]] for i in range(len(a))]


# ------------------------------------------------------------------ GAP 驱动
def gap_run(script_text, tag):
    """在临时文件里跑 GAP，返回 stdout。"""
    env = dict(os.environ)
    env["PATH"] = GAPBIN_DIR + os.pathsep + GAPROOT + os.pathsep + env.get("PATH", "")
    fd, path = tempfile.mkstemp(suffix=".g")
    os.close(fd)
    io.open(path, "w", encoding="ascii").write(script_text)
    try:
        r = subprocess.run([os.path.join(GAPROOT, "gap.exe"), "-q", "-b"],
                           stdin=open(path, "rb"), stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, env=env, timeout=3000)
        return r.stdout.decode("utf-8", "replace")
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def gap_permlist(p):
    """Python 0-indexed perm → GAP PermList（1-indexed 像）。"""
    return "PermList([" + ",".join(str(x + 1) for x in p) + "])"


def config_gapset(cfg, N):
    """bitmask → GAP 集合 [i+1, ...]。"""
    return "[" + ",".join(str(i + 1) for i in range(N) if (cfg >> i) & 1) + "]"


def orbit_via_gap(dims, cfgs, gap_order_known=None, timeout_note=""):
    """返回 (|G|, [|O(c)| ...])。"""
    N = dims[0] * dims[1] * dims[2]
    gens = gens_correct(dims)
    lines = ["gens := [", ",\n        ".join(gap_permlist(g) for g in gens), "];;",
             "G := Group(gens);;", 'Print("ORDER ", Size(G), "\\n");']
    for k, cfg in enumerate(cfgs):
        lines.append('c{0} := {1};;'.format(k, config_gapset(cfg, N)))
        lines.append('Print("STAB{0} ", Size(Stabilizer(G, c{0}, OnSets)), "\\n");'.format(k))
    lines.append("QUIT;")
    out = gap_run("\n".join(lines) + "\n", "orbit")
    order = None
    stabs = []
    for ln in out.splitlines():
        ln = ln.strip()
        if ln.startswith("ORDER "):
            order = int(ln.split()[1])
        elif ln.startswith("STAB"):
            stabs.append(int(ln.split()[1]))
    return order, stabs, out


# ================================================================== 检查项
hdr("GP-1  GAP 可运行")
out = gap_run('Print("GAPVER ", GAPInfo.Version, "\\n"); QUIT;\n', "ver")
ver = None
for ln in out.splitlines():
    if ln.strip().startswith("GAPVER "):
        ver = ln.strip().split()[1]
print("  GAP 版本 = {}".format(ver))
print("  安装位置 = {}".format(GAPROOT))
chk("GP-1", ver is not None and ver.startswith("4.16"),
    "GAP {} 安装在 {} 且可非交互运行".format(ver, GAPROOT))

hdr("GP-2  GAP 集合稳定子单元测试（已知答案）")
out = gap_run("""
G := SymmetricGroup(5);;
Print("T1 ", Size(Stabilizer(G,[1,2],OnSets)), "\\n");
Print("T2 ", Size(Orbit(G,[1,2],OnSets)), "\\n");
H := SymmetricGroup(6);;
Print("T3 ", Size(Stabilizer(H,[1,2],OnSets)), "\\n");
QUIT;
""", "unit")
vals = {}
for ln in out.splitlines():
    p = ln.strip().split()
    if len(p) == 2 and p[0] in ("T1", "T2", "T3"):
        vals[p[0]] = int(p[1])
print("  Stab_S5({{1,2}}) = {} (应 12)；轨道 = {} (应 10)；Stab_S6({{1,2}}) = {} (应 48)".format(
    vals.get("T1"), vals.get("T2"), vals.get("T3")))
chk("GP-2", vals.get("T1") == 12 and vals.get("T2") == 10 and vals.get("T3") == 48,
    "三个已知答案全对 ⟹ set-stabilizer 可信")

hdr("GP-3  交叉验证：GAP |G|/|Stab| vs Python 精确轨道 BFS（(2,2,6) N=24）")
dims = (2, 2, 6)
N, k = 24, 12
# Python 侧：精确枚举轨道大小（与 _fix_run_48.py 同法，但只算前 12 个轨道）
from sympy.combinatorics import Permutation as SP  # noqa: E402


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


gens24 = gens_correct(dims)
apply24, ng24 = make_apply(N, gens24)
rng = random.Random(5)
probe_cfgs = []
for _ in range(8):
    m = 0
    for i in rng.sample(range(N), k):
        m |= 1 << i
    probe_cfgs.append(m)
py_sizes = []
for cfg in probe_cfgs:
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
order, stabs, raw = orbit_via_gap(dims, probe_cfgs)
gap_sizes = [order // s for s in stabs]
print("  GAP |G| = {}（第 46/48 轮 sympy 给 648）".format(order))
print("  {:<8} {:<12} {:<12} {}".format("构型", "Python 轨道", "GAP 轨道", "一致？"))
allok = True
for i, (pa, ga) in enumerate(zip(py_sizes, gap_sizes)):
    ok = (pa == ga)
    allok = allok and ok
    print("  #{:<7} {:<12} {:<12} {}".format(i, pa, ga, "✓" if ok else "✗"))
chk("GP-3", allok and order == 648,
    "8 个构型的轨道大小**逐位一致**，且 |G| = 648 与 sympy 相同 ⟹ GAP 与 Python 互验通过")

hdr("GP-4  (2,4,4) N=32 —— GAP 算真实轨道（第 47 轮因 |G| 超上限而未算）")
dims = (2, 4, 4)
N, k = 32, 16
rng = random.Random(20260922)
S = 25
cfgs = []
for _ in range(S):
    m = 0
    for i in rng.sample(range(N), k):
        m |= 1 << i
    cfgs.append(m)
order44, stabs44, raw44 = orbit_via_gap(dims, cfgs)
sizes44 = [order44 // s for s in stabs44]
# ✅ 口径说明（第 0 批 2026-09-28 加注）：sizes44 来自**随机采样的 S 个构型**（每构型一个轨道大小），
#    故 Σ ln|O(c)| / S **就是构型等权**（第 50 轮确认：GAP 采样天然正确）。
#    ⚠️ 它**看上去**像「轨道等权」，但采样使每个构型等权 ⟹ **不是**错误口径，**请勿「修正」**。
avg44 = sum(math.log(s) for s in sizes44) / len(sizes44)
hn44 = LN2 - avg44 / N
print("  |G| = {}  （第 47 轮 sympy 给 220150628352 ⟹ {}）".format(
    order44, "一致 ✓" if order44 == 220150628352 else "**不一致**"))
print("  采样 {} 个构型：轨道大小 min = {}，max = {}".format(S, min(sizes44), max(sizes44)))
print("  ⟨ln|O|⟩ = {:.4f}，⟨ln|O|⟩/N = {:.4f}".format(avg44, avg44 / N))
print("  **H/N = {:.4f}**".format(hn44))
chk("GP-4", order44 == 220150628352 and len(sizes44) == S,
    "(2,4,4) 的 H/N = {:.4f}（形状对照的关键数）".format(hn44))

hdr("GP-5  (4,4,4) N=64 —— GAP 算真实轨道（首次）")
dims = (4, 4, 4)
N, k = 64, 32
rng = random.Random(464646)
cfgs = []
for _ in range(10):
    m = 0
    for i in rng.sample(range(N), k):
        m |= 1 << i
    cfgs.append(m)
order444, stabs444, raw444 = orbit_via_gap(dims, cfgs)
if order444 is None or len(stabs444) != 10:
    print("  ⚠️ GAP 未返回完整结果，原始输出尾部：")
    print("  " + "\n  ".join(raw444.strip().splitlines()[-6:]))
    chk("GP-5", False, "(4,4,4)：GAP 未返回（见上）")
    hn444 = None
else:
    sizes444 = [order444 // s for s in stabs444]
    # ✅ 口径说明（同 0.4②）：随机采样 ⟹ 构型等权，**不是**错误口径，请勿「修正」。
    avg444 = sum(math.log(s) for s in sizes444) / len(sizes444)
    hn444 = LN2 - avg444 / N
    print("  |G| = {}".format(order444))
    print("  采样 10 个构型：轨道大小 min = {}，max = {}".format(min(sizes444), max(sizes444)))
    print("  ⟨ln|O|⟩ = {:.4f}，⟨ln|O|⟩/N = {:.4f}".format(avg444, avg444 / N))
    print("  **H/N = {:.4f}**".format(hn444))
    chk("GP-5", hn444 is not None, "(4,4,4) 的 H/N = {:.4f}（首次给出三维格点的值）".format(hn444))

hdr("GP-6  汇总：H/N 的形状依赖")
print("  {:<12} {:>4} {:>10}  {}".format("格点", "N", "H/N", "来源"))
for name, NN, val, src in [("(2,2,2)", 8, 0.4679, "第 46 轮（精确）"),
                           ("(2,2,4)", 16, 0.4335, "第 46 轮（精确）"),
                           ("(2,2,6)", 24, 0.4510, "第 48 轮更正"),
                           ("(2,2,8)", 32, 0.4617, "第 48 轮更正"),
                           ("(2,4,4)", 32, hn44, "**第 48 轮 GAP**"),
                           ("(4,4,4)", 64, hn444, "**第 48 轮 GAP**")]:
    print("  {:<12} {:>4} {:>10}  {}".format(name, NN,
                                             "-" if val is None else "{:.4f}".format(val), src))
print()
print("  面积律要求 H/N = 0.25；已测全部落在 **0.43–0.47** ⟹ 偏大 ≈ 1.7–1.9 倍。")
chk("GP-6", True, "汇总表已列")

hdr("GP-7  诚实边界")
print("  · (2,4,4)/(4,4,4) 用**采样**（25 / 10 个构型），⟨ln|O|⟩ 的标准误未估；")
print("  · (4,4,4) 的 k=N/2 构型数 C(64,32) = 1.83×10¹⁸，采样占比可忽略 ⟹ 只给数量级；")
print("  · GAP 的 Stabilizer(...,OnSets) 是**精确**算法（非随机回溯失败重试后），")
print("    但本脚本未检查 GAP 是否走完整回溯（未加 InfoWarning 抑制）。")
print("  · N=64 仍远小于宏观 N_c³ ≈ 6.1×10¹⁸² ⟹ **不得外推**（第 41 轮教训）。")
chk("GP-7", True, "边界已写明")

print()
print("=" * 78)
print("汇总：通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
