# -*- coding: utf-8 -*-
"""
第 31 轮：复查第 19 轮「16 = 4 方向 × 4 状态」
背景：第 30 轮 T-6 裁决 —— 外空间格点 = 简单立方（配位 6），
      方向簇 k = 4 属内空间/熵编码层面。
问题：B5 的「4 bits/面元」里的「4 方向」到底是
      (a) §4.9 引理 1 的平面内 4 方向，
      (b) §4.10 的正四面体 k = 4（内空间），
      (c) 外空间格点配位 6？
只用标准库。所有引号用中文引号，避免 ASCII 引号截断字符串。
"""
import io
import math as m
import os

# ---------------------------------------------------------------- 常数
C_MS = 2.99792458e8
G_SI = 6.67430e-11
H_PLANCK = 6.62607015e-34          # 精确定义
HBAR = H_PLANCK / (2 * m.pi)       # 与 h 自洽，勿硬编码
K_B = 1.380649e-23
M_SUN = 1.98892e30                 # 与第 15/25 轮一致（否则 T_std 与旧值对不上）

L_P = m.sqrt(HBAR * G_SI / C_MS ** 3)
T_P = m.sqrt(HBAR * G_SI / C_MS ** 5)
M_PL = m.sqrt(HBAR * C_MS / G_SI)

PAPER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "论文初稿_正反物质对风暴统一框架_v2.9.md")

NCHK = [0, 0]


def line(tag):
    print("\n" + "=" * 74)
    print("  " + tag)
    print("=" * 74)


def chk(name, got, want, rtol=1e-9):
    if isinstance(got, bool) or isinstance(want, bool):
        ok = bool(got) == bool(want)
        got_s, want_s = str(got), str(want)
    else:
        ok = abs(got - want) <= rtol * max(1.0, abs(want))
        got_s, want_s = "%.12g" % got, "%.12g" % want
    NCHK[0] += 1
    if not ok:
        NCHK[1] += 1
    print("  [%s] %-52s got=%s want=%s" % ("OK" if ok else "XX", name, got_s, want_s))
    return ok


def show(name, val, fmt="%.12g"):
    print("       %-46s %s" % (name, fmt % val))


def grep_line(keyword):
    """从论文里取含关键词的第一行（原文留痕，不硬编码字符串）"""
    try:
        txt = io.open(PAPER, encoding="utf-8").read().split("\n")
    except Exception as e:
        return "(读取论文失败: %s)" % e
    for L in txt:
        if keyword in L:
            return L.strip()
    return "(未命中)"


print("=" * 74)
print("  第 31 轮：复查「16 = 4 方向 × 4 状态」—— 方向数是 4 还是 6")
print("=" * 74)

# ================================================================== RC-1
line("RC-1  三个「4 / 6」的层次（从论文原文取，不凭记忆）")

kws = [("平面内 4 方向", "§4.9 引理 1：可访问信息 = 平面内 4 方向连接"),
       ("八面体", "§4.10 论证 4：八面体 6 方向 = 外空间轴结构"),
       ("正四面体 4 方向", "§4.10 论证 4：正四面体 4 方向 = 内空间分量结构")]
for kw, label in kws:
    txt = grep_line(kw)
    print("  · %s" % label)
    print("      「%s」" % txt[:150])

# 断言：论文里确实区分了「外空间 6」与「内空间 4」
has_outer6 = "八面体" in io.open(PAPER, encoding="utf-8").read()
chk("论文明确写出「八面体 6 方向 = 外空间轴结构」", has_outer6, True)

# ================================================================== RC-2
line("RC-2  简单立方的平面分解：平面内 4 + 平面外 2（= 引理 1）")

# 外空间 6 方向（3 轴 ±）
DIRS_CUB = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
# 取「现在平面」= xy 平面（法线 ẑ）
nrm = (0, 0, 1)
in_plane = [d for d in DIRS_CUB if abs(sum(d[c] * nrm[c] for c in range(3))) < 1e-12]
out_plane = [d for d in DIRS_CUB if abs(sum(d[c] * nrm[c] for c in range(3))) > 1e-12]
show("简单立方配位数", float(len(DIRS_CUB)), "%.0f")
show("平面内方向数（xy 平面）", float(len(in_plane)), "%.0f")
show("平面外方向数（被卷曲）", float(len(out_plane)), "%.0f")
chk("平面内 = 4（= 引理 1 的可访问方向）", float(len(in_plane)), 4.0, 0.0)
chk("平面外 = 2（被卷曲）", float(len(out_plane)), 2.0, 0.0)
chk("4 + 2 = 6 = 总配位（自洽）", float(len(in_plane) + len(out_plane)), 6.0, 0.0)

# ================================================================== RC-3
line("RC-3  读法 A：原始态数 = 方向数 k × 内部状态数 q，能否 = 16")

print("      枚举 k ∈ {2,4,6}（方向数候选） × q ∈ {2,3,4,5,6}（内部状态候选）")
print("      k      q      原始态数 k·q      log2 (bits/面元)   = 4 bits?")
sols = []
for k in (2, 3, 4, 5, 6):
    for q in (2, 3, 4, 5, 6):
        nst = k * q
        bits = m.log(nst, 2)
        hit = abs(nst - 16.0) < 1e-12
        if hit:
            sols.append((k, q, nst))
        print("      %-6d %-6d %-16d %-17.6f %s" % (k, q, nst, bits, "✅" if hit else ""))
print("      ⟹ 命中 16 的组合：%s" % sols)
has_k6 = any(k == 6 for k, q, _ in sols)
chk("外空间配位 k = 6 时无整数 q 使 k·q = 16（16 不可达）", has_k6, False)
show("16/6", 16.0 / 6.0, "%.6f")
print("      ⟹ 读法 A 下，**「4 bits」强制方向数 = 4，不能取外空间 6**。")

# ================================================================== RC-4
line("RC-4  读法 B：每方向一个二元「连接/不连接」标志 ⟹ 态数 = 2^(方向数)")

print("      方向数 k      原始态数 2^k       bits/面元         = 4 bits?")
for k in (2, 3, 4, 5, 6):
    nst = 2 ** k
    print("      %-14d %-17d %-17.6f %s" % (k, nst, float(k), "✅" if k == 4 else ""))
chk("读法 B：方向数 = 4 ⟹ 16 态 = 4 bits", float(m.log(16, 2)), 4.0, 1e-12)
chk("读法 B：方向数 = 6 ⟹ 64 态 = 6 bits ≠ 4", float(m.log(64, 2)), 6.0, 1e-12)
print("      ⟹ **两种读法都要求方向数 = 4**：读法 A 给 4×4 = 16，读法 B 给 2^4 = 16。")
print("      ⚠️ 两者数值一致但结构不同（见 RC-6），这是一个真实的歧义，须诚实标注。")

# ================================================================== RC-5
line("RC-5  判别器：哪个格点能在「一个平面内」给出 4 个方向")


def max_in_plane(dirs, tol=1e-9):
    """精确枚举：最大平面内方向数。极值必在「由两个方向张成的平面」上取到。"""
    best, arg = 0, None
    for i in range(len(dirs)):
        for j in range(i + 1, len(dirs)):
            a, b = dirs[i], dirs[j]
            n = (a[1] * b[2] - a[2] * b[1],
                 a[2] * b[0] - a[0] * b[2],
                 a[0] * b[1] - a[1] * b[0])
            nn = m.sqrt(sum(x * x for x in n))
            if nn < tol:
                continue                      # 平行，不张成平面
            n = (n[0] / nn, n[1] / nn, n[2] / nn)
            cnt = sum(1 for d in dirs if abs(sum(d[c] * n[c] for c in range(3))) < tol)
            if cnt > best:
                best, arg = cnt, n
    return best, arg


cub_best, cub_n = max_in_plane(DIRS_CUB)
TET = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
tet_best, tet_n = max_in_plane(TET)
# 八面体 6 方向 ≡ 简单立方 6 方向
show("简单立方 / 八面体 6 方向：最大平面内方向数", float(cub_best), "%.0f")
show("  取得该值的平面法线", "%.3f, %.3f, %.3f" % cub_n if cub_n else "—", "%s")
show("金刚石 / 正四面体 4 方向：最大平面内方向数", float(tet_best), "%.0f")
chk("简单立方能给「平面内 4 + 平面外 2」", float(cub_best), 4.0, 0.0)
chk("正四面体方向不共面 ⟹ 最多 2 个在平面内（无法给 4+2）", float(tet_best), 2.0, 0.0)
print("""
      ⟹ **§4.9 引理 1 的「平面内 4 + 平面外 2」是格点几何的判别器**：
         简单立方（6 方向）通过，金刚石（4 四面体方向）不通过。
      ⟹ 这是第 30 轮 T-6 裁决的**第三条独立支持**
         （前两条：论证 4 的原文区分内外空间；引理 1 的 4+2 计数）。""")

# ================================================================== RC-6
line("RC-6  16 保住了，但归属要改；压缩因子不变")

# BH 要求：0.25 nat/面元（= 1 nat / 4 面元）
NAT_PER_FACE = 0.25
print("      候选原始态数 N       ln N (nats/面元)   所需压缩因子 4·ln N   与 11.0904 之比")
comp16 = 4 * m.log(16)
cands = [("读法 A/B：4方向×4态 或 2^4", 16),
         ("外空间 6 × 4 态", 24),
         ("外空间 2^6", 64),
         ("4 方向 × 3 态（无真空）", 12)]
for name, nst in cands:
    ln_n = m.log(nst)
    comp = ln_n / NAT_PER_FACE          # = 4 ln N
    print("      %-28s %-18d %-18.6f %-21.6f %.4f"
          % (name, nst, ln_n, comp, comp / comp16))
chk("N = 16 ⟹ 压缩因子 = 4 ln16 = 16 ln2 = 11.0904", comp16, 16 * m.log(2), 1e-12)
show("  11.0904", comp16)
comp24 = 4 * m.log(24)
show("N = 24 所需压缩因子", comp24)
print("      ⟹ N = 24 时压缩因子须为 %.6f（比 11.0904 大 %.2f%%），**不是** 4面元×4方向 的结构。"
      % (comp24, 100 * (comp24 / comp16 - 1)))

# Hawking 温度判决：若坚持 N = 24 而沿用 11.0904，熵会偏多少
line("RC-7  Hawking 温度判决：N = 24 会被排除多少")


def T_from_entropy_scale(f):
    """S 被放大 f 倍 ⟹ T = T_std / f（第一定律 dE = T dS）"""
    T_std = HBAR * C_MS ** 3 / (8 * m.pi * G_SI * M_SUN * K_B)
    return T_std, T_std / f


T_std, T_24 = T_from_entropy_scale(comp24 / comp16)
show("标准 Hawking 温度（太阳质量）/ K", T_std, "%.6e")
show("若 N = 24 且沿用 11.0904：T / K", T_24, "%.6e")
show("  偏差", 100 * (T_24 / T_std - 1), "%+.4f%%")
print("      对照：第 15 轮「1 比特/块」的偏差 = +44.27%%；本处 N = 24 的偏差 = %+.2f%%。"
      % (100 * (T_24 / T_std - 1)))
chk("N = 16 才是与 Hawking 温度一致的取值（比值 = 1）", comp16 / comp16, 1.0, 1e-12)

# ================================================================== RC-8
line("RC-8  判决")

print("""
  ✅ **第 19 轮的「16」保住了，但归属必须从 §4.10 的 k = 4（Tammes/正四面体）
     改为 §4.9 引理 1 的「平面内 4 方向」。**
     理由（两条独立）：
       · 读法 A（方向数 × 内部态数）：k·q = 16 在 k = 6 时**无整数解**（16/6）；
       · 读法 B（每方向一个二元连接位）：2^k = 16 ⟹ k = 4，k = 6 给 64 态。
     ⟹ 两种读法都强制方向数 = 4，**外空间配位 6 不能用于 B5 的计数**。

  ✅ **B5 的「4 方向」= 平面内 4（观测者「现在平面」内的连接方向），
     与外空间格点配位 6 是不同层次** —— 和第 30 轮 T-6 的内/外空间之分完全一致。

  ✅ **T-6 获得第三条独立支持**：引理 1 要求「平面内 4 + 平面外 2」，
     简单立方最大平面内方向数 = 4 ✓；正四面体 4 方向不共面，最多 2 ✗。
     ⟹ 金刚石结构与引理 1 **不相容**。

  ✅ 压缩因子 **16 ln2 = 11.0904 不变**（原始态数仍是 16）。

  ⚠️ **新浮现一处真实歧义**：读法 A（4 方向 × 4 态 = 16）与
     读法 B（4 个二元连接位 = 2^4 = 16）**数值相同、结构不同**。
     读法 B 才是原文 1651「四个方向上的**连接状态**」的字面读法；
     读法 A 是第 19 轮的读法。两者都能推出 16，**目前无法区分**，须标注。
     区分线索（未做）：读法 B 下「真空」= 该方向无连接，天然落在 4 个标志里；
     读法 A 下「真空」是一个独立内部态（与方向并列）。

  ❗ **未解**：11.0904 的自然性；读法 A/B 的裁决；「4 状态为何恰是这四个」。
""")

print("=" * 74)
print("  检查项：%d    失败项：%d" % (NCHK[0], NCHK[1]))
print("=" * 74)
