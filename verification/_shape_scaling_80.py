# -*- coding: utf-8 -*-
"""第 80 轮核验：工作流 3.2（I-15 ⟨|O|⟩ 标度律）＋ 4.1（登记不覆盖）＋ 4.2（三个遍历性）＋ H5（六处 4 复查）

用户指令：「下一步」。方向 = 第 79 轮交接说明定的四条一轮清。

本轮的四问：
  SH-1  ⟨|O|⟩ 的**形状依赖**：同一 N、不同形状给不同值吗？（旋转等价检验作内部一致性）
  SH-2  ⟨|O|⟩ 随 N 的**标度律**：三点扩到多点，给拟合 + 严格界
  SH-3  ⭐ 严格界：**可迁性的必要条件** `|G| ≥ C(N,k)` 在各 N 上成立吗？判据适用域在哪？
  SH-4  4.1：论文 §4.8 有没有**正式的**「框架不覆盖」登记（vs 第 51 轮块里的「是否该…」提问）
  SH-5  4.2：论文里「遍历性」有几处、几种含义？是否有分层说明？
  SH-6  H5：§4.10「六处 4」的逐处复查**是否已完成**（第 29 轮备忘录 + 第 39 轮标注修正）
  SH-7  C-31：清单里 H5 仍标 ☐ ⟹ 陈年待办已做（C-19 同族）

运行：<venv>/python.exe outputs/_shape_scaling_80.py
"""
import io, os, sys, math, itertools, time

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import _tickgroup as tg

ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
GL = os.path.join(BASE, "项目台账.md")
WF = os.path.join(BASE, "未完成研究工作流_按依赖排序.md")

OK = [0]
BAD = [0]


def chk(tag, cond, msg):
    if cond:
        OK[0] += 1
        print("  [OK] {:<6} {}".format(tag, msg))
    else:
        BAD[0] += 1
        print("  [XX] {:<6} {}  <-- 失败".format(tag, msg))


def hdr(t):
    print("")
    print("-" * 78)
    print(t)
    print("-" * 78)


def block_mask(lines):
    """排除已登记的轮次块（陷阱 47/65）：`> ` 引用块 + 以轮次标记开头的段落，直到下一个 # 标题；表格行永不标记。

    ⚠️ **第 80 轮修正（陷阱 65 第四次命中）**：块标记的**名字会变** ——
      此前只列了「补充 / 更正 / 加注 / 口径注 / 补注 / 【第 N 轮】」，
      而第 80 轮我写了「**v2.9 登记（第 80 轮…）**」与「**v2.9 分层注（第 80 轮…）**」——
      **不在白名单里** ⟹ 掩码漏 ⟹ SH-5 立刻从 0 处变成 2 处而翻红。
      ⟹ 判据改为**模式化**：`v2.9` ＋ 任意 ≤16 个非左括号字符 ＋ `（第 N 轮`。
      教训：**不要枚举块的名字，要匹配块的**模式**。
    """
    import re
    PAT = re.compile(r"(v2\.9\s*[^\n（|]{0,16}（第\s*\d+\s*轮|【第\s*\d+\s*轮|第\s*\d+\s*轮加注|第\s*\d+\s*轮口径注|第\s*\d+\s*轮补注)")
    m = [False] * len(lines)
    i = 0
    while i < len(lines):
        s = lines[i]
        if s.lstrip().startswith("|"):
            m[i] = False
            i += 1
            continue
        if s.lstrip().startswith(">") and ("v2.9 补充（第" in s or "【第" in s):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith(">"):
                m[j] = True
                j += 1
            i = j
            continue
        if PAT.search(s):
            j = i
            while j < len(lines) and not lines[j].startswith("#"):
                if not lines[j].lstrip().startswith("|"):
                    m[j] = True
                j += 1
            i = j
            continue
        i += 1
    return m


def apply_perm(c, g, N):
    out = 0
    i = 0
    x = c
    while x:
        if x & 1:
            out |= 1 << g[i]
        x >>= 1
        i += 1
    return out


def orbit_decompose(dims, k=None, gens=None):
    N = dims[0] * dims[1] * dims[2]
    if gens is None:
        gens = tg.gens_correct(dims)
    if k is None:
        cfgs = list(range(1 << N))
    else:
        cfgs = []
        for comb in itertools.combinations(range(N), k):
            mm = 0
            for i in comb:
                mm |= 1 << i
            cfgs.append(mm)
    unvis = set(cfgs)
    sizes = []
    while unvis:
        s = next(iter(unvis))
        comp = {s}
        stack = [s]
        while stack:
            c = stack.pop()
            for g in gens:
                nc = apply_perm(c, g, N)
                if nc not in comp:
                    comp.add(nc)
                    stack.append(nc)
        sizes.append(len(comp))
        unvis -= comp
    return N, len(cfgs), sizes


print("=" * 78)
print("第 80 轮：⟨|O|⟩ 的形状依赖与标度律 ＋ 三条登记/核查（3.2 / 4.1 / 4.2 / H5）")
print("=" * 78)

# ================================================================
hdr("[SH-1] ⟨|O|⟩ 的形状依赖（同一 N、不同形状）＋ 旋转等价检验")
# 旋转等价的形状必须给**逐位相同**的结果 —— 这是内部一致性检验
CASES16 = [((2, 2, 4), 8), ((2, 4, 2), 8), ((4, 2, 2), 8), ((4, 4, 1), 8), ((16, 1, 1), 8)]
CASES8 = [((2, 2, 2), 4), ((2, 4, 1), 4), ((8, 1, 1), 4)]

res = {}
print("  每个形状：k = N/2 层（占据数守恒 ⟹ 层内封闭）")
print("  {:<12} {:>4} {:>10} {:>9} {:>12} {:>11}".format("格点", "N", "M=C(N,k)", "轨道数", "⟨|O|⟩", "覆盖率"))
for dims, k in CASES8 + CASES16:
    N, M, sizes = orbit_decompose(dims, k)
    avg = M / float(len(sizes))
    res[dims] = (N, M, len(sizes), avg, avg / M, sizes)
    print("  {:<12} {:>4} {:>10} {:>9} {:>12.2f} {:>10.4%}".format(
        str(dims), N, M, len(sizes), avg, avg / M))
    sys.stdout.flush()

# 旋转等价检验
rot16 = [(2, 2, 4), (2, 4, 2), (4, 2, 2)]
same16 = all(res[d][3] == res[rot16[0]][3] and res[d][2] == res[rot16[0]][2] for d in rot16)
print()
print("  ⭐ **旋转等价检验**：(2,2,4) / (2,4,2) / (4,2,2)（同一格点，轴的写法不同）")
print("     轨道数 {}；⟨|O|⟩ {}；逐位相同 = **{}**".format(
    [res[d][2] for d in rot16], ["{:.6f}".format(res[d][3]) for d in rot16], same16))
shape8 = [(2, 2, 2), (2, 4, 1), (8, 1, 1)]
print("  ⭐ **形状依赖（N=8 三种形状）**：⟨|O|⟩ = {} ⟹ **不同形状给不同值**".format(
    ["{:.2f}".format(res[d][3]) for d in shape8]))
print("  ⭐ **形状依赖（N=16）**：(2,2,4) = {:.2f} vs (4,4,1) = {:.2f} vs (16,1,1) = {:.2f}".format(
    res[(2, 2, 4)][3], res[(4, 4, 1)][3], res[(16, 1, 1)][3]))
chk("SH-1", same16 and len({round(res[d][3], 6) for d in shape8}) >= 2,
    "**旋转等价 ⟹ 逐位相同 ✓**（(2,2,4)/(2,4,2)/(4,2,2)：轨道数 {}）；"
    "**换形状 ⟹ 结果改变**（N=8：{}；N=16：(2,2,4) {:.2f} vs (4,4,1) {:.2f} vs (16,1,1) {:.2f}）"
    "⟹ ⚠️ **⟨|O|⟩ 是形状依赖量，不得跨形状外推**（第 47/48 轮的独立变量的又一次确认）".format(
        res[(2, 2, 4)][2],
        " / ".join("{:.2f}".format(res[d][3]) for d in shape8),
        res[(2, 2, 4)][3], res[(4, 4, 1)][3], res[(16, 1, 1)][3]))

# ================================================================
hdr("[SH-2] ⟨|O|⟩ 随 N 的标度律（(2,2,L) 系列三点 + 拟合 + 不外推标注）")
TRI = [((2, 2, 2), 5.00, 8), ((2, 2, 4), res[(2, 2, 4)][3], 16), ((2, 2, 6), 426.93, 24)]
print("  ⚠️ (2,2,6) 的值引用第 46 轮（第 50 轮更正轨道数 6334 后 ⟨|O|⟩ = 2704156/6334 = {:.2f}）"
      .format(2704156 / 6334.0))
print("  {:<12} {:>4} {:>12} {:>12} {:>12}".format("格点", "N", "⟨|O|⟩", "ln⟨|O|⟩", "ln⟨|O|⟩/N"))
pts = []
for d, v, N in TRI:
    pts.append((N, v))
    print("  {:<12} {:>4} {:>12.2f} {:>12.4f} {:>12.4f}".format(str(d), N, v, math.log(v), math.log(v) / N))
print()
print("  ⭐ 三点不是幂律（ln⟨|O|⟩ vs lnN 的两段斜率 3.34 → 5.25），但**对 N^{2/3} 近线性**：")
for N, v in pts:
    print("     N = {:>3}  N^(2/3) = {:>7.4f}   ln⟨|O|⟩ = {:>7.4f}".format(N, N ** (2.0 / 3), math.log(v)))
sl = [(math.log(pts[i + 1][1]) - math.log(pts[i][1])) /
      (pts[i + 1][0] ** (2.0 / 3) - pts[i][0] ** (2.0 / 3)) for i in range(len(pts) - 1)]
print("     两段斜率（dlny/d(N^{{2/3}})）：{:.4f} → {:.4f}".format(sl[0], sl[1]))
print("     ⟹ 斜率差 {:.1f}% ⟹ 三点**不足以判定**幂指数，只可记「≈ exp(c·N^{{2/3}})，c ≈ 1.03」"
      .format(100 * abs(sl[1] / sl[0] - 1)))
print("  ⚠️ **严格界**（不需要拟合）：")
print("     · 上界：⟨|O|⟩ ≤ C(N,k)（整层一条轨道 ⟹ 完全可迁）")
print("     · 下界：⟨|O|⟩ ≥ 1")
for N, v in pts:
    c = math.comb(N, N // 2)
    print("     N = {:>3}：1 ≤ {:>10.2f} ≤ C(N,N/2) = {:>12}".format(N, v, c))
chk("SH-2", len(pts) == 3 and all(1 <= v <= math.comb(N, N // 2) for N, v in pts) and abs(sl[1] / sl[0] - 1) < 0.2,
    "⭐⭐ **3.2 的交付 = 严格界 + 形状依赖 + 不外推**：三点落在 `1 ≤ ⟨|O|⟩ ≤ C(N,N/2)` 内（严格）；"
    "对 `N^{{2/3}}` 的两段斜率 {:.4f} → {:.4f}（差 {:.1f}%）⟹ 三点**不足以判定幂指数**"
    "（⚠️ 与第 50 轮 `h_min·N^{{−2/3}}` 的 2.6% 残差**不是同一个量**：那是 **h_min**、这是 **⟨|O|⟩**）；"
    "⚠️ 且 ⟨|O|⟩ **形状依赖**（SH-1）⟹ **不得外推到 (2,2,L) 以外，也不得外推到 N > 24**".format(
        sl[0], sl[1], 100 * abs(sl[1] / sl[0] - 1)))

# ================================================================
hdr("[SH-3] ⭐ 严格界（续）：可迁性的必要条件 `|G| ≥ C(N,k)` 与**判据适用域**")
GEN = {8: 8, 16: 128, 24: 648, 32: None, 64: 2.79e37}
SRC = {8: "第 41 轮（(2,2,2)）", 16: "第 41 轮（(2,2,4)）", 24: "第 41 轮（(2,2,6)）",
       64: "第 41 轮（4×4×4，Schreier–Sims）"}
print("  判据：**若 G 在 k-层上可迁，则轨道数 = 1，故必须 |G| ≥ C(N,k)**。")
print("  {:<6} {:>16} {:>20} {:>16} {:>10}".format("N", "|G|", "C(N,N/2)", "|G|/C(N,k)", "可迁?"))
for N in (8, 16, 24, 64):
    c = math.comb(N, N // 2)
    g = GEN[N]
    ratio = g / float(c)
    print("  {:<6} {:>16.4g} {:>20.6g} {:>16.4g} {:>10}".format(
        N, g, c, ratio, "未排除" if ratio >= 1 else "**否**（严格）"))
print()
print("  ⭐ 结论：**N ≤ 24 全部严格不可迁**（|G| < C(N,k)）；**N = 64 的必要条件已满足**")
print("     ⟹ 判据在 N = 64 上**不能裁决**（可迁性既未被排除也未被证实），而 C(64,32) = {:.6e}"
      .format(math.comb(64, 32)))
print("     ⟹ **标度律判据的适用域 = N ≤ 24（细长格点）**；宏观行为**不能由它推出**")
# 交叉核对：实测轨道数 > 1 与必要条件一致
cons = all(res[d][2] > 1 for d, _ in CASES8 + CASES16)
chk("SH-3", cons and GEN[8] < math.comb(8, 4) and GEN[16] < math.comb(16, 8) and GEN[24] < math.comb(24, 12)
    and GEN[64] > math.comb(64, 32),
    "⭐ **必要条件给出判据的适用域**：N ≤ 24 时 `|G| < C(N,k)` ⟹ **严格不可迁**（与实测轨道数 > 1 一致 ✓）；"
    "N = 64 时 `|G|/C(N,k) = {:.4g}` ⟹ **可迁性未被排除** ⟹ 判据在此失效。"
    "⟹ 第 41 轮「结果 C」（若高度可迁则 H ≈ ½lnN ⟹ 面积律不成立）在 **N ≤ 24 上无法判定**".format(
        GEN[64] / float(math.comb(64, 32))))

# ================================================================
hdr("[SH-4] 4.1：论文 §4.8 有没有**正式的**「框架不覆盖」登记？")
# ⚠️ 陷阱 20/22 的执行细则：清点「某词 0 处」的论证，底本要**并列打印补丁前 / 补丁后**
PRE = os.path.join(BASE, "..", "MAPS-Unified-Framework", "paper", "history",
                   "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第80轮前.md")
PRE = os.path.abspath(PRE)
ZL = io.open(ZH, encoding="utf-8").read().split("\n")
MZ = block_mask(ZL)
BODY = [s for k, s in enumerate(ZL) if not MZ[k]]
PRE_L = io.open(PRE, encoding="utf-8").read().split("\n") if os.path.exists(PRE) else None
PM = block_mask(PRE_L) if PRE_L else None


def cnt_body(w):
    return sum(1 for k, s in enumerate(ZL) if w in s and not MZ[k])


def cnt_all(w):
    return sum(1 for s in ZL if w in s)


def cnt_pre_body(w):
    return sum(1 for k, s in enumerate(PRE_L) if w in s and not PM[k]) if PRE_L else -1


def cnt_pre_all(w):
    return sum(1 for s in PRE_L if w in s) if PRE_L else -1


print("  备份底本：{}".format("**存在**" if PRE_L else "缺失"))
print("  ⚠️ **并列打印「补丁前 / 补丁后」两列**（陷阱 20/22）：任一列非零者须人工判定，别只看当前稿")
print("  {:<12} {:>8} {:>8} {:>10} {:>10}".format("词", "前·全文", "后·全文", "前·正文", "后·正文"))
for w in ["框架不覆盖", "不覆盖", "松不等式", "登记为不覆盖", "登记（第 80 轮"]:
    print("  {:<12} {:>8} {:>8} {:>10} {:>10}".format(
        w, cnt_pre_all(w), cnt_all(w), cnt_pre_body(w), cnt_body(w)))
ask_pre = [k + 1 for k, s in enumerate(PRE_L) if "是否该" in s and "不覆盖" in s] if PRE_L else []
ask = [k + 1 for k, s in enumerate(ZL) if "是否该" in s and "不覆盖" in s]
print("  「是否该…登记为不覆盖」式的**提问**：补丁前 {} ｜ 当前 {}".format(ask_pre, ask))
reg = [k + 1 for k, s in enumerate(ZL) if "正式登记" in s and "不覆盖" in s and not MZ[k]]
print("  **正式登记声明**（正文，排除轮次块）：{}".format(reg if reg else "**0 处**"))
print()
print("  ⟹ 补丁前：第 51 轮块已经把**事实**写清，但停在「是否该正式登记？」这**一问**上；")
print("     补丁后：本轮补的【第 80 轮登记】块（**轮次块**，不计入正文）把它落成声明 ⟹ 4.1 完成")
chk("SH-4", len(ask_pre) >= 1 and cnt_pre_body("框架不覆盖") == 0 and len(ask) >= 1,
    "⭐ **4.1 的补丁前状态取证（陷阱 20 两列法）**：备份底本里「框架不覆盖」**正文 0 处**（全文 {} 处，均在 §4.10 储能条与轮次块内）、"
    "「是否该…登记为不覆盖」的**提问** 1 处（L{}）⟹ **事实齐备但停在提问**；"
    "本轮补的**登记声明**在轮次块内（正文仍 0 处 ⟹ 未与既有口径冲突）".format(
        cnt_pre_all("框架不覆盖"), ask_pre[0] if ask_pre else 0))

# ================================================================
hdr("[SH-5] 4.2：论文里「遍历性」有几处、几种含义？")
hits_pre = [(k + 1, s) for k, s in enumerate(PRE_L) if "遍历" in s] if PRE_L else []
hits = [(k + 1, s) for k, s in enumerate(ZL) if "遍历" in s]
print("  「遍历」命中：补丁前 **{} 行** ｜ 当前 **{} 行**（含轮次块）".format(len(hits_pre), len(hits)))
# ⭐ 显式判据：底本里「遍历」的行中，**没有一行**与 47 μm / R_mix 同行 ⟹ 候选池 14 的第三项用词不实
pre_47 = [k for k, s in hits_pre if ("47" in s and ("μm" in s or "微米" in s)) or "R_mix" in s]
pre_47_in_pre = [k + 1 for k, s in enumerate(PRE_L) if "遍历" in s and ("47 μm" in s or "R_mix" in s)] if PRE_L else []
print("  ⭐ **底本里「遍历」的行中，与「47 μm / R_mix」同行的：{}**".format(
    pre_47_in_pre if pre_47_in_pre else "**0 行**"))
KIND = {
    "速度空间（DSMC/B 分支）": ["Birkhoff", "Khinchin", "DSMC", "时间平均", "系综平均", "麦克斯韦"],
    "构型空间（tick 群）": ["不变轨道", "非遍历", "轨道", "tick 群"],
    "空间输运（47 μm）": ["47", "μm", "输运", "扩散"],
}
tagged = {kk: [] for kk in KIND}
for k, s in hits:
    for kk, ws in KIND.items():
        if any(w in s for w in ws):
            tagged[kk].append(k)
            break
for kk, v in tagged.items():
    print("     {:<22} {} 行".format(kk, v))
print()
decl = [k + 1 for k, s in enumerate(ZL) if "遍历" in s and ("分层" in s or "三种含义" in s or "不同含义" in s)]
decl_pre = [k + 1 for k, s in enumerate(PRE_L) if "遍历" in s and ("分层" in s or "三种含义" in s or "不同含义" in s)] if PRE_L else []
decl_body = [k + 1 for k, s in enumerate(ZL) if "遍历" in s and ("分层" in s or "三种含义" in s or "不同含义" in s) and not MZ[k]]
print("  「分层 / 三种含义」式的**区分说明**：补丁前 {} ｜ 当前（含轮次块）{} ｜ 当前·正文 {}".format(
    decl_pre if decl_pre else "**无**", decl if decl else "**无**", decl_body if decl_body else "**无**"))
print("  ⟹ 补丁前**无**区分说明（这是 4.2 未做的取证）；补丁后的说明在**轮次块**内，正文仍无 —— 与既有口径一致")
print()
print("  ⚠️ 四处**关键混用**（补丁前的行号）：")
for k in [17, 168, 177, 424]:
    if k <= len(PRE_L):
        print("     L{:<5} {}".format(k, PRE_L[k - 1][:150]))
chk("SH-5", len(decl_pre) == 0 and len(tagged["速度空间（DSMC/B 分支）"]) >= 1
    and len(tagged["构型空间（tick 群）"]) >= 1 and len(decl_body) == 0 and len(pre_47_in_pre) == 0,
    "⭐ **4.2 的补丁前状态取证（两列法）**：备份底本里「遍历」命中 **{} 行**，至少含**两种相反含义** —— "
    "① **速度空间**（§4 命题 2.1 / DSMC：Birkhoff 检验**成立**，{} 行）"
    "② **构型空间**（tick 群：**非遍历**，轨迹锁在不变轨道里，{} 行）；"
    "而「分层 / 三种含义」式区分说明 **0 处** ⟹ 同一篇论文里「遍历性成立」与「非遍历」并列无解释；"
    "⭐ 显式判据：底本里「遍历」的行中与「47 μm / R_mix」同行的 = **{} 行** ⟹ "
    "候选池 14 记的「三个**遍历性**」中第三项**用词不实**（47 μm 是**扩散标度**，底本从未称其为遍历性）"
    "⟹ 本轮补**三层分层注**并把 L3 **改名**为「空间输运」".format(
        len(hits_pre), len(tagged["速度空间（DSMC/B 分支）"]), len(tagged["构型空间（tick 群）"]),
        len(pre_47_in_pre)))

# ================================================================
hdr("[SH-6] H5：§4.10「六处 4」的逐处复查**是否已完成**？")
six = os.path.join(BASE, "六处4的分层判定_四会同源两处独立且等价于三维.md")
six_exists = os.path.exists(six)
print("  第 29 轮备忘录 `六处4的分层判定_四会同源两处独立且等价于三维.md`：{}".format(
    "**存在**" if six_exists else "缺失"))
if six_exists:
    st = io.open(six, encoding="utf-8").read()
    for w in ["SF-1", "SF-6", "四会同源", "LST/Borsuk", "(2, d) = (4, 3)"]:
        print("     含「{}」：{}".format(w, w in st))
lay = [k + 1 for k, s in enumerate(ZL) if "分级修正注" in s or "分层判定" in s]
print("  论文里的**分层注**所在行：{}".format(lay))
fixed39 = [k + 1 for k, s in enumerate(ZL) if "标注错位" in s and "第 39 轮" in s]
print("  「标注错位（第 39 轮已修正）」所在行：{}".format(fixed39))
# 核对论文里的「六处 4 同源」是否仍为旧措辞
old_w = [k + 1 for k, s in enumerate(ZL) if "六处「4」同源" in s]
print("  仍写「六处「4」同源」的行：{}（紧接下一行就是分级修正注）".format(old_w))
chk("SH-6", six_exists and len(lay) >= 1 and len(fixed39) >= 1 and len(old_w) >= 1,
    "✅ **H5 已于第 29 轮完成**：备忘录（**SF-1…SF-6，8 项 0 失败**）逐条追溯六处出处 ⟹ "
    "结论「**四会同源（锚在 LST/Borsuk）+ 两处独立**」；论文已加**分级修正注**（L{}）"
    "＋ 第 39 轮修正**两处标注错位**（L{}）⟹ **H5 无剩余工作**".format(
        lay[0] if lay else 0, fixed39[0] if fixed39 else 0))

# ================================================================
hdr("[SH-7] C-31：清单/工作流里 H5 仍标 ☐ ⟹ 陈年待办已做（C-19 同族）")
wft = io.open(WF, encoding="utf-8").read()
gt = io.open(GL, encoding="utf-8").read()
print("  工作流文档含「H5」：{}；清单含「H5」：{}".format("H5" in wft, "H5" in gt))
tb = os.path.join(BASE, "全量待办回溯_我的过度声明更正与真实待办总账.md")
tbt = io.open(tb, encoding="utf-8").read()
row = [s for s in tbt.split("\n") if "**H5**" in s]
PREMARK = os.path.join(BASE, "全量待办回溯_我的过度声明更正与真实待办总账_备份_2026-10-02第80轮前.md")
pre_row = []
if os.path.exists(PREMARK):
    pre_row = [s for s in io.open(PREMARK, encoding="utf-8").read().split("\n") if "**H5**" in s]
print("  ⚠️ **判据要跟着状态走**：本检查分**取证（补丁前）**与**确认（补丁后）**两步 —— ")
print("     补丁前 H5 行含 ✅？**{}**（应为 False ⟹ 标记过期）".format(
    ("✅" in pre_row[0]) if pre_row else "（底本缺失）"))
print("     补丁后 H5 行含 ✅？**{}**（应为 True ⟹ 已修复）".format(("✅" in row[0]) if row else False))
print("     台账 3.2 行含 ✅？**{}**".format(
    any("✅" in s for s in tbt.split("\n") if "**3.2**" in s)))
chk("SH-7", pre_row and ("✅" not in pre_row[0]) and row and ("✅" in row[0]),
    "**C-31（清单标记过期，第 11 条）**：台账 `全量待办总账` 的 **H5** 行在**补丁前**标的是「低（成本）」"
    "而**不是 ✅**，而 H5 **第 29 轮就做完了**（SH-6 取证）⟹ 与第 74 轮 **C-19** 同族（**已做却仍标待办**）；"
    "✅ 本轮**已改标 ✅**（补丁后含 ✅ = True ⟹ 修复确认）。"
    "⚠️ 教训：**判据本身也要跟着状态走** —— 第 80 轮首跑时我把台账改好之后，"
    "旧判据（「H5 行**没有** ✅」）反而**翻红**了 ⟹ 检查项必须写成「取证（补丁前）＋ 确认（补丁后）」两段")

# ================================================================
print("")
print("=" * 78)
print("  通过 {} 项，失败 {} 项".format(OK[0], BAD[0]))
print("=" * 78)
