# -*- coding: utf-8 -*-
"""
第 87 轮 GAP 补点探针：**无退化格点**上的 H/N
  (4,4,6) N=96、(4,4,8) N=128 —— 组 B 标度律的外推检验
工具链复用 `_gap_shape_48.py` 前 207 行（纯函数段，不含其检查项）。
"""
import io, os, sys, math, time, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.setrecursionlimit(200000)

# ---- 复用第 48 轮的工具链（只取函数定义段，不执行其检查项）----
src = io.open("_gap_shape_48.py", encoding="utf-8").read().split("\n")
FUNCS_ONLY = "\n".join(src[:207])      # 到 hn_stats 定义结束
exec(FUNCS_ONLY, globals())
print("[工具链] 已复用 _gap_shape_48.py 的前 207 行（gens_correct / orbit_via_gap / hn_stats）")

# ⚠️ **坑（第 49 轮查出、第 87 轮首次真触发、第 87 轮补跑时再次踩中）**：
#    `_gap_shape_48.py` 的 `orbit_via_gap` 用**逐行解析**（`int(ln.split()[1])`）；
#    而 GAP 对**超长整数会折行**（(4,4,8) 的 |G| 有 108 位）⟹ 大格点上 IndexError。
#    `_gap.py` 里有折行安全的 `_parse_markers`，且规范版 `orbit_sizes_via_gap` 会先关掉
#    GAP 的自动折行（`SetPrintFormattingStatus("*stdout*", false)`）⟹ 这里改用它。
import importlib.util
_spec = importlib.util.spec_from_file_location("gaphelper", "_gap.py")
gaph = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gaph)

# ⚠️⚠️ **本脚本第一次跑挂的真实原因（必须记下来）**：
#     折行修复**只打在了「被直接调用的那条路径」上**（探针用的 orbit_via_gap_safe），
#     而 `hn_stats` 是第 48 轮的函数，**内部自己去调** `orbit_via_gap` ——
#     于是采样阶段**原样踩回同一个坑**，报 IndexError。
#     判据：**改了函数 A，还要问「谁在内部调 A」**；只修调用点不修被调函数 = 假修复。
#     修法：把 globals() 里的 `orbit_via_gap` 重绑为安全版。
#     （Python 的函数体对全局名的查找是**运行时**的 ⟹ `hn_stats` 会拿到重绑后的版本。）
def orbit_via_gap_safe(dims, cfgs):
    """折行安全的版本（用 _gap.py 的 permlist / config_set / _parse_markers）。"""
    N = dims[0] * dims[1] * dims[2]
    gens = gens_correct(dims)
    lines = ['SetPrintFormattingStatus("*stdout*", false);;',   # ← 先关自动折行（双保险）
             "gens := [",
             ",\n        ".join(gaph.permlist(g) for g in gens), "];;",
             "G := Group(gens);;",
             'Print("ORDER ", Size(G), "\\n");']
    for k, cfg in enumerate(cfgs):
        lines.append("c{0} := {1};;".format(k, gaph.config_set(cfg, N)))
        lines.append('Print("STAB{0} ", Size(Stabilizer(G, c{0}, OnSets)), "\\n");'.format(k))
    lines.append("QUIT;")
    out = gap_run("\n".join(lines) + "\n")
    parsed = gaph._parse_markers(out, len(cfgs))
    order, stabs = (parsed[0], parsed[1]) if isinstance(parsed, tuple) else (None, [])
    return order, stabs, out

# ★ 关键：重绑（否则 hn_stats 内部仍旧版）
globals()["orbit_via_gap"] = orbit_via_gap_safe
print("[修复] hn_stats 内部的 orbit_via_gap 已重绑为折行安全版（并关闭 GAP 自动折行）")

print("[GAP] 版本探测：", gap_run('Print("GAPVER ", GAPInfo.Version, "\\n"); QUIT;\n').strip()[:60])
print()

CASES = [
    ("(4,4,8)", (4, 4, 8), 128),     # ⚠️ (4,4,6) 已算过：0.1333 ± 0.0027（不再重跑，省时）
]

for name, dims, N in CASES:
    print("=" * 78)
    print("### {}  N = {}   （退化方向数 = 0）".format(name, N))
    print("=" * 78)
    t0 = time.time()
    order, stabs, raw = orbit_via_gap_safe(dims, random_cfgs(N, N // 2, 1, 42))
    dt1 = time.time() - t0
    if order is None or not stabs:
        print("  ⚠️ GAP 未返回（可能超时/超内存）；尾部：")
        print("  " + "\n  ".join(raw.strip().splitlines()[-6:]))
        continue
    size = order // stabs[0]
    print("  |G| = {}  （{} 位十进制）".format(order, len(str(order))))
    print("  单构型：|Stab| = {} ⟹ |O| = {:.3g}".format(stabs[0], float(size)))
    print("  探针耗时 {:.1f} s".format(dt1))
    print()

    # 第二步：按时间预算决定采样数 S
    BUDGET = 1500.0        # 秒
    per = max(dt1, 1.0)
    S = int(max(3, min(30, BUDGET / per)))
    print("  ⟹ 时间预算 {:.0f} s ⟹ 采样 S = {}".format(BUDGET, S))
    t1 = time.time()
    r = hn_stats(dims, S, 42)
    dt2 = time.time() - t1
    if r is None:
        print("  ⚠️ 采样失败")
        continue
    print("  ⭐ **H/N = {:.4f} ± {:.4f}**（95% [{:.4f}, {:.4f}]），S = {}，用时 {:.0f} s".format(
        r["hn"], r["hn_se"], r["hn_lo"], r["hn_hi"], S, dt2))
    print("  ⟨ln|O|⟩/N = {:.4f}".format(r["avg_ln"] / N))
    print()

print("=" * 78)
print("探针结束")
print("=" * 78)
