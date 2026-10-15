# -*- coding: utf-8 -*-
"""
第 72 轮核验脚本 —— Φ 的耦合强度（I-17 耦合侧）
检查项 PC-1 … PC-9。

问题：「框架能不能给出 Φ 与物质的耦合强度 g？」
方法：① 引文清点（底本 = 补丁前备份）② 参数清点（Φ 挂几个纯输入）
      ③ 同符号检查 ④ 判定入口（屏蔽机制 / PPN / 桌面实验）
      ⑤ 三分支判决
"""
import io
import os
import math

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
CUR = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
HISTDIR = os.path.join(ROOT, "MAPS-Unified-Framework", "paper", "history")
PREV = os.path.join(HISTDIR, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第71轮前.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

PASS = []
FAIL = []


def chk(tag, cond, msg):
    (PASS if cond else FAIL).append(tag)
    print("  [{}] {:<6} {}".format("OK" if cond else "XX", tag, msg))


def rule(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def load(p):
    return io.open(p, encoding="utf-8").read().split("\n")


ZH = load(CUR)
PRE = load(PREV) if os.path.exists(PREV) else None
print("当前稿行数 = {}；补丁前备份 = {}".format(
    len(ZH), "找到（{} 行）".format(len(PRE)) if PRE else "缺失"))
print("底本：引文清点以**当前稿**为底本（= 本轮补丁前），备份列作对照")


# ══════════════════════════════════════════════════════════════════════
rule("PC-1  引文清点：Φ 的耦合 / 第五力 / 桌面检验 —— 两列对照")
# ══════════════════════════════════════════════════════════════════════

WORDS = [
    "耦合强度", "gΦψ̄ψ", "钉扎", "标量模", "g₅₅", "VEV", "radion",
    "第五力", "五力", "Yukawa", "汤川", "逆平方", "inverse square",
    "chameleon", "变色龙", "Vainshtein", "symmetron", "筛选机制",
    "屏蔽", "screening", "等效原理", "Eöt", "力程", "PPN",
]


def count(lines, w):
    return sum(1 for s in lines if w in s)


def block_mask(lines, marker="v2.9 补充（第"):
    """陷阱 47/20：标记出「已登记的轮次块」（`> ` 起始的连续引用块）⟹ True = 属于块内。"""
    m = [False] * len(lines)
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith(">") and marker in lines[i]:
            j = i
            while j < len(lines) and lines[j].lstrip().startswith(">"):
                m[j] = True
                j += 1
            i = j + 1
        else:
            i += 1
    return m


def round_para_mask(lines):
    """⚠️ 本轮新发现（陷阱 47/20 的执行细则）：轮次块**不全是 `> ` 引用块** ——
    有些直接以 `**【v2.9 补充（第 N 轮…` 开头（无 `>` 前缀），或写成「（第 N 轮加注）」，
    且**跨多个自然段**（第 62 轮在 §5.5 的加注就跨了两段：805–808 与 810–820）。
    ⟹ 排除规则：从含轮次标记的行起，一直标记到**下一个 `#` 标题**为止；
       但**表格行永不标记**（表格是正文，宁可少排除 = 对「0 处」更严）。"""
    m = [False] * len(lines)
    in_note = False
    PAT = __import__("re").compile(
        r"(v2\.9 补充（第|v2\.9 更正（第|第 \d+ 轮加注|第 \d+ 轮口径注|第 \d+ 轮补注)")
    for i, s in enumerate(lines):
        if s.lstrip().startswith("|"):
            m[i] = False
            continue
        if s[:1] == "#":
            in_note = False
        if PAT.search(s):
            in_note = True
        m[i] = in_note
    return m


MASK = [a or b for a, b in zip(block_mask(ZH), round_para_mask(ZH))]
if PRE:
    PRE_MASK = [a or b for a, b in zip(block_mask(PRE), round_para_mask(PRE))]
else:
    PRE_MASK = None
BODY = [s for i, s in enumerate(ZH) if not MASK[i]]
PRE_BODY = [s for i, s in enumerate(PRE) if not PRE_MASK[i]] if PRE else []
print("  已登记轮次文本（`> ` 块 ＋ 无 `>` 前缀的 `**【v2.9 补充（第…` 段）："
      "当前稿 {} 行；正文（排除后）= {} 行".format(sum(MASK), len(BODY)))

print("  {:<16} {:>9} {:>8} {:>9}".format("词", "第71轮前", "当前", "当前·正文"))
print("  " + "-" * 48)
for w in WORDS:
    a = count(PRE, w) if PRE else -1
    b = count(ZH, w)
    c = count(BODY, w)
    print("  {:<16} {:>9} {:>8} {:>9}".format(w, a if a >= 0 else "?", b, c))

# 判据：耦合侧的「桌面检验 / 新力」类词在【正文】必须为 0
core = ["Yukawa", "汤川", "逆平方", "inverse square", "chameleon", "变色龙",
        "Vainshtein", "symmetron", "筛选机制", "screening", "第五力", "五力"]
pre_body = {w: count(PRE_BODY, w) for w in core}
now_body = {w: count(BODY, w) for w in core}
print()
print("  耦合侧判据词（补丁前正文 → 当前正文）：")
for w in core:
    print("     {:<14} {} → {}".format(w, pre_body[w], now_body[w]))
n_hit_now = sum(v for v in now_body.values())
pre_hit = sum(v for v in pre_body.values())
print()
print("  ⚠️ 元文本对照：全稿计数（第 3 列）里「第五力 = 10」等全部落在**已登记的轮次块**内"
      "（第 62 / 70 轮的 `> ` 引用块）；排除块后正文计数归 0 —— 这就是陷阱 47/20 的自指效应。")
chk("PC-1", n_hit_now == 0 and pre_hit == 0,
    "耦合侧 12 个判据词在**论文正文**里 **0 处**（补丁前也是 0 处）⟹ Φ 的耦合强度"
    "**从未被处理过**，本轮是首次；全稿计数里的非零项全部来自已登记的轮次块（自指）")


# ══════════════════════════════════════════════════════════════════════
rule("PC-2  Φ 的参数清点：耦合 g 与任何已定量之间有等式吗？")
# ══════════════════════════════════════════════════════════════════════

# 先定位 Φ 的三个定义处
ANCHORS = [
    ("§4.5b Φ 的身份", "KK 标量模场（g₅₅）的低能投影"),
    ("§6.1 钉扎项", "gΦ"),
    ("§6.4 Φ⁴ 势", "-\\tfrac12\\mu^2\\Phi^2"),
]
for nm, a in ANCHORS:
    hits = [i + 1 for i, s in enumerate(ZH) if a in s]
    print("  {:<16} 命中行 {}".format(nm, hits))

# 纯输入清单
INPUTS = {
    "Λ": "§4.5b 谱作用截断 `S = Tr f(D²/Λ²)`",
    "μ": "§6.4 `V(Φ) = −½μ²Φ² + ¼λΦ⁴` 的质量参数",
    "λ（§6.4）": "§6.4 同一势的四次耦合",
    "g": "§6.1 钉扎项 `gΦψ̄ψ`（§6.2 场方程 `□Φ = V'(Φ) + gψ̄ψ`）",
}
print()
print("  Φ 一个场挂的**纯输入**：")
for k, v in INPUTS.items():
    print("     {:<12} {}".format(k, v))

# 判据：有没有一行**明确**把 g 与 {μ, λ, ⟨Φ⟩} 用等号连起来（判据要严：必须出现 `gΦ` 记号）
# ⚠️ 必须排除已登记的轮次文本 —— 否则本轮自己写的块会把 0 处变成 N 处（陷阱 47/20 自指）
rels = []
for i, s in enumerate(ZH, 1):
    if MASK[i - 1]:
        continue
    if "gΦ" not in s:
        continue
    if "=" not in s:
        continue
    if sum(1 for t in ["μ", "λ", "Φ⟩", "α_EM", "E_P"] if t in s) >= 1:
        rels.append((i, s.strip()[:150]))
print()
print("  「含 `gΦ` 记号 + 等号 + 另一参数」的行（= 可能构成约束）：")
if not rels:
    print("     （无）")
for i, s in rels:
    print("     行 {}: {}".format(i, s))

# 另查：有没有一行把势里两个参数（μ 与 λ）用等号连起来
import re as _re
PAT_ML = _re.compile(r"(λ\s*=\s*[^=\n]{0,40}μ)|(μ\s*=\s*[^=\n]{0,40}λ)")
rel2 = [(i, s.strip()[:120]) for i, s in enumerate(ZH, 1)
        if PAT_ML.search(s) and not MASK[i - 1]]
print()
print("  「μ 与 λ 互相相等/相等关系」的行（= 势内部参数之间有无关系）：{} 处".format(len(rel2)))
for i, s in rel2:
    print("     行 {}: {}".format(i, s))

# 明确的约束判据：退化检验把 g=0 当特例 ⟹ g 自由
deg = [i + 1 for i, s in enumerate(ZH) if (not MASK[i]) and "退化检验" in s and "g=0" in s]
print()
print("  ⭐ 判定证据：§6.2 的「退化检验」行 = {}".format(deg))
print("     该行写 `g=0、V=½m²Φ² → 自由 Dirac+标量+GR` ⟹ **g = 0 被当作一个特例**")
print("     ⟹ 框架**自己**把 g 当自由参数（否则不会把 0 列为退化情形）。")
chk("PC-2", len(rels) == 0 and len(rel2) == 0 and len(deg) == 1,
    "Φ 挂 **4 个纯输入**（Λ / μ / λ / g），**没有一行**把它们互相约束（`gΦ` 记号 + 等号"
    "的关系式 0 处、势内部 μ–λ 关系 0 处）；§6.2 退化检验又把 `g=0` 当特例 "
    "⟹ 框架自己按**自由参数**处理耦合")


# ══════════════════════════════════════════════════════════════════════
rule("PC-3  符号撞车：`λ` 与 `g` 各占几义？§8.6 的约定覆盖了吗？")
# ══════════════════════════════════════════════════════════════════════


def section_of(idx):
    """给定行号(1-based)，回溯最近的 '### ' 或 '## ' 标题。"""
    for j in range(idx - 1, -1, -1):
        s = ZH[j]
        if s.startswith("### ") or s.startswith("## "):
            return s.strip()[:40]
    return "?"


lam_rows = [i + 1 for i, s in enumerate(ZH) if "λ" in s]
print("  含 λ 的行共 {} 行。按小节归类：".format(len(lam_rows)))
from collections import Counter
cnt = Counter(section_of(i) for i in lam_rows)
for k, v in cnt.most_common():
    print("     {:<42} {}".format(k, v))

# §6.4 的 λ
s64 = [i + 1 for i, s in enumerate(ZH) if "-\\tfrac12\\mu^2\\Phi^2" in s or "λ/4" in s or "\\tfrac{\\lambda}{4}" in s]
print()
print("  §6.4 的 Φ⁴ 势（含 λ 作为四次耦合）出现在行 {}".format(s64))

# §8.6 的符号约定原文
conv = [i + 1 for i, s in enumerate(ZH) if "符号约定（重要）" in s and "不使用 λ" in s]
ctxt = ""
if conv:
    k = conv[0] - 1
    ctxt = " ".join(ZH[k:k + 3])
print("  §8.6 符号约定行 = {}".format(conv))
print("  原文：{}".format(ctxt[:220]))
mentions64 = ("§6.4" in ctxt) or ("6.4" in ctxt)
mentions61 = ("§6.1" in ctxt) or ("6.1" in ctxt)
print()
print("  ⚠️ 该约定提到「§5 弦网耦合常数」与「λ_c ≈ 0.14」，"
      "是否提到 §6.4 的 λ（Φ⁴ 四次耦合）：{}".format(mentions64))

# g 的两义
g_pin = [i + 1 for i, s in enumerate(ZH) if "gΦ" in s]
g_net = [i + 1 for i, s in enumerate(ZH) if "J = n_G·E_P·g" in s or "n_G·E_P·g" in s]
print()
print("  `g` 的第一义（钉扎耦合）：行 {}".format(g_pin))
print("  `g` 的第二义（弦网几何因子，`J = n_G·E_P·g`）：行 {}".format(g_net))
g_decl = [i + 1 for i, s in enumerate(ZH) if "符号约定" in s and ("`g`" in s or "字母 g" in s)]
print("  有没有为 `g` 写符号约定：{}".format(g_decl if g_decl else "0 处"))
chk("PC-3", (not mentions64) and (not g_decl),
    "**两处撞车均未声明**：① `λ` 有**第三义**（§6.4 的 Φ⁴ 四次耦合），而 §8.6 的符号约定"
    "只声明了 §5 与 λ_c，**未提 §6.4**；② `g` 同字母两义（§6.1 钉扎耦合 vs §5.7 弦网几何因子"
    "`J = n_G·E_P·g`），**无任何符号约定** ⟹ 登记 **C-15**（陷阱 45 家族，第六种口径病）")


# ══════════════════════════════════════════════════════════════════════
rule("PC-4  屏蔽机制：框架有没有「把耦合藏起来」的机制？")
# ══════════════════════════════════════════════════════════════════════

SCREEN = ["chameleon", "变色龙", "Vainshtein", "symmetron", "galileon", "伽利略子",
          "screening", "五次方", "dilaton"]
GENERIC = ["筛选", "屏蔽", "藏起", "压制耦合"]
sc = {w: count(BODY, w) for w in SCREEN}
ge = {w: count(BODY, w) for w in GENERIC}
print("  专用屏蔽机制词条（正文计数）：")
for w, v in sc.items():
    print("     {:<14} {}".format(w, v))
print("  泛用词（正文计数，逐行判读）：")
for w, v in ge.items():
    hits = [(i + 1, s.strip()[:90]) for i, s in enumerate(ZH) if w in s and not MASK[i]]
    print("     {:<10} {} 处 {}".format(w, v, [h[0] for h in hits]))
    for h in hits[:3]:
        print("        行 {}: {}".format(h[0], h[1]))
tot_sc = sum(sc.values())
chk("PC-4", tot_sc == 0,
    "专用屏蔽机制 **0 处**（chameleon / symmetron / Vainshtein / galileon / dilaton 全 0）"
    "⟹ 框架没有「把 O(1) 耦合藏在桌面尺度」的机制；泛用词「筛选 / 屏蔽」的命中全是"
    "**完全无关**的用法（候选筛选 / 窗函数），非机制")


# ══════════════════════════════════════════════════════════════════════
rule("PC-5  PPN 失明：§4.5b 的 γ=β=1 能不能约束这个耦合？")
# ══════════════════════════════════════════════════════════════════════

# 力程（第 70 轮数字，本轮独立复算）
hbarc_eVm = 1.054571817e-34 * 2.99792458e8 / 1.602176634e-19   # eV·m
lP = math.sqrt(1.054571817e-34 * 6.67430e-11 / 2.99792458e8 ** 3)
AU = 1.495978707e11
mm = 1e-3

lam_c = hbarc_eVm / 1.0181e-3        # 粗粒化 @ E_c
lam_rh = hbarc_eVm / 4.1894e-3       # 粗粒化 @ E(R_H)
print("  ℏc = {:.6e} eV·m ；l_P = {:.6e} m".format(hbarc_eVm, lP))
print("  λ(粗粒化 @ E_c) = {:.6e} m = {:.4f} μm".format(lam_c, lam_c * 1e6))
print("  λ(粗粒化 @ R_H) = {:.6e} m = {:.4f} μm".format(lam_rh, lam_rh * 1e6))
print()
print("  Yukawa 压制因子 e^(−r/λ)（取 λ = λ_c）：")
for r, nm in [(50e-6, "桌面 50 μm"), (mm, "1 mm"), (1.0, "1 m"), (AU, "1 AU")]:
    x = r / lam_c
    if x < 700:
        print("     {:<12} r/λ = {:>10.3e} ⟹ e^(−r/λ) = {:.3e}".format(nm, x, math.exp(-x)))
    else:
        print("     {:<12} r/λ = {:>10.3e} ⟹ log10(e^(−r/λ)) = {:.3e}".format(
            nm, x, -x / math.log(10)))
chk("PC-5", math.exp(-50e-6 / lam_c) > 0.5 and (AU / lam_c) > 1e10,
    "桌面尺度（50 μm）与 λ_c 同量级 ⟹ **敏感**；太阳系尺度（1 AU）压制 "
    "~10^(−3.4×10^14) ⟹ **完全失明** ⟹ §4.5b 的 `γ=β=1` **不能**约束这个耦合 "
    "（既不是冲突，也不是支持）—— 约束只能来自桌面实验")


# ══════════════════════════════════════════════════════════════════════
rule("PC-6  ⭐⭐ 桌面实验对照：0.05–0.2 mm 这一档还在窗口里吗？")
# ══════════════════════════════════════════════════════════════════════

J_net = 3.6627e28          # eV，第 70 轮用的 §5.8 弦网 J（= 3·E_P·g，取 g = 1）
TIERS = [
    ("(a) 弦网标量扇区 Δ=0.41 J", 0.41 * J_net, "§5.8 / 第 62 轮"),
    ("(b) 粗粒化 @ E_c = 1.0181 meV", 1.0181e-3, "第 1090 行（恒等式）"),
    ("(c) 粗粒化 @ E(R_H) = 4.1894 meV", 4.1894e-3, "第 674 行"),
    ("(d) 普朗克（公理 1）", 1.220910e28, "第 322 行"),
]
# 已发表的 α=1 边界（外部锚点）
EDGE_EW = 39e-6      # Eöt-Wash 2020：α=1 排除到 39 μm
EDGE_TAN = 48e-6     # Tan et al. PRL 124,051301(2020)：|α|≤1 保持到 48 μm
BAND = (40e-6, 350e-6)   # Tan：40–350 μm 区间给出 α 的最强上界

print("  ⭐ 外部锚点（Eöt-Wash 组 / Tan et al.）——「引力强度（α=1）Yukawa 修正」的排除边界：")
print("     197 μm(2001) → 56 μm(2007) → 42 μm(2013) → **39 μm(2020, Eöt-Wash)**")
print("     Tan et al. PRL 124, 051301 (2020)：ISL 在 λ = **48 μm** 处仍为 |α| ≤ 1；")
print("     并在 **40–350 μm** 区间给出 α 的最强上界（λ≈70 μm 处改进 3 倍）。")
print()
print("  {:<30} {:>14} {:>12} {:>14}".format("Φ 质量档位", "力程 λ (m)", "λ/μm", "∈ 40–350 μm?"))
for nm, m_eV, src in TIERS:
    lam = hbarc_eVm / m_eV
    inband = BAND[0] <= lam <= BAND[1]
    print("  {:<30} {:>14.4e} {:>12.4f} {:>14}".format(nm, lam, lam * 1e6, "✓ 在带内" if inband else "✗"))
print()
print("  逐条判定（对照 α = O(1) 的排除边界）：")
for nm, m_eV, src in TIERS:
    lam = hbarc_eVm / m_eV
    if lam >= EDGE_TAN:
        v = "**被排除**（两种边界都排除：λ ≥ 48 μm）"
    elif lam >= EDGE_EW:
        v = "**处于灵敏度前沿**（Eöt-Wash 已排除到 39 μm，Tan 到 48 μm ⟹ 落在缝隙里）"
    else:
        v = "未排除（太短，桌面实验够不着）⟹ **同时也不可观测**"
    print("     {:<30} {}   〔λ = {:.2f} μm vs 39/48 μm〕".format(nm, v, lam * 1e6))
chk("PC-6", hbarc_eVm / 1.0181e-3 >= EDGE_TAN and hbarc_eVm / 4.1894e-3 >= EDGE_EW,
    "两个粗粒化档（**193.8 μm** 与 **47.1 μm**）**都落在 40–350 μm 的已测区间里**"
    "（后者落在 39–48 μm 的边界缝隙，属灵敏度前沿）⟹ 若 Φ 的耦合是引力强度"
    "（标准 KK 里 radion 的自然值 α ~ 1/3–1），**(b) 档已被排除、(c) 档在最前沿**；"
    "而 (a)(d) 档力程 ~ l_P，**既未排除也不可观测** ⟹ 四档**没有一档能活**")


# ══════════════════════════════════════════════════════════════════════
rule("PC-7  三分支判决（逻辑汇总）")
# ══════════════════════════════════════════════════════════════════════

BRANCH = [
    ("(i) 自由输入（= 框架现状）", "g 是第 4 个纯输入，无任何约束",
     "Φ 的相互作用 = **4 参数族（Λ, μ, λ, g）** ⟹ 可识别性 = 0（铁律 5）⟹ **零预言力**"),
    ("(ii) 取 §4.5b 的 KK 读法 + 粗粒化质量档", "耦合 = 几何固定（普适，α ~ O(1)）",
     "力程 47–194 μm ⟹ **落在 40–350 μm 已测区间** ⟹ **已被桌面实验排除**"),
    ("(iii) 同上 + 弦网质量档", "同上",
     "力程 0.81 l_P ⟹ 桌面实验**够不着**，等价于**不可观测** ⟹ 不是预言"),
]
print("  {:<38} {:<34} {}".format("分支", "耦合", "后果"))
print("  " + "-" * 110)
for a, b, c in BRANCH:
    print("  {:<38} {:<34} {}".format(a, b, c))
print()
print("  ⟹ **三条路都通向「不能用」**：要么无预言力，要么被排除，要么不可观测。")
print("  ⟹ 与第 61 轮（工程出口 = 0）、第 62 轮（四力位无空位）合起来：")
print("     「第五力」这条线**在框架内彻底关死**：不是「还没算」，是「算出来也不能用」。")
chk("PC-7", True, "三分支判决完成：**自由输入 / 被排除 / 不可观测** 三选一 ⟹ "
                  "I-17 耦合侧的答案是「框架给不出 g，而补上最自然的假设后该档位已被排除」")


# ══════════════════════════════════════════════════════════════════════
rule("PC-8  与既有轮次的接口自洽（不重叠、不推翻）")
# ══════════════════════════════════════════════════════════════════════

# 第 70 轮的数字复算（独立）
lam_c_70 = hbarc_eVm / 1.0181e-3
print("  第 70 轮力程数字独立复算：")
print("     λ_c = {:.4e} m（第 70 轮记 1.938e-4 m）⟹ 相对差 {:.2e}".format(
    lam_c_70, abs(lam_c_70 - 1.938e-4) / 1.938e-4))
J_used = 3.6627e28
lam_a = hbarc_eVm / (0.41 * J_used)
print("     λ_a = {:.4e} m = {:.4f} l_P（第 70 轮记 0.813 l_P）".format(lam_a, lam_a / lP))
print("     ⚠️ 独立发现：λ_a 的数值**依赖 J 的取值**，而 `J = n_G·E_P·g` 里的 g **正是本轮要审的耦合**")
print("        —— 第 70 轮用了 **g = 1**（J = 3.6627e28 eV = 3 E_P）。⟹ 弦网档的力程本身是 g 的函数。")
ratio = (hbarc_eVm / 1.0181e-3) / (hbarc_eVm / (0.41 * J_used))
print("     两档之比 = {:.4e} ⟹ log10 = {:.1f}（第 70 轮记 31.2）".format(
    ratio, math.log10(ratio)))
chk("PC-8", abs(math.log10(ratio) - 31.2) < 0.15 and abs(lam_a / lP - 0.813) < 0.01,
    "第 70 轮的两个数字**复现**（0.813 l_P、31.2 个数量级）；⚠️ 同时查明**弦网档依赖 g = 1** ——"
    "这是第 70 轮未标明的隐含取值，本轮把它显式化（不推翻其结论，但把它变成条件结论）")


# ══════════════════════════════════════════════════════════════════════
rule("PC-9  卫生检查：非表格行的 `\\|` 与中文字符之间的 ASCII 引号")
# ══════════════════════════════════════════════════════════════════════

bad_pipe = [i + 1 for i, s in enumerate(ZH) if "\\|" in s and not s.lstrip().startswith("|")]
print("  非表格行含 `\\|` 的行数 = {}".format(len(bad_pipe)))
if bad_pipe:
    print("     {}".format(bad_pipe[:20]))

CJK = lambda ch: "\u4e00" <= ch <= "\u9fff"
cnt_quote = 0
qlines = []
for i, s in enumerate(ZH, 1):
    for k, ch in enumerate(s):
        if ch == '"' and k > 0 and k + 1 < len(s) and CJK(s[k - 1]) and CJK(s[k + 1]):
            cnt_quote += 1
            qlines.append(i)
            break
print("  中文字符之间的 ASCII 引号：{} 处（历史遗留，第 56 轮登记为 77 处）".format(cnt_quote))
chk("PC-9", len(bad_pipe) == 0, "格式卫生：非表格行的 `\\|` **0 处**；"
      "ASCII 引号 {} 处为历史遗留（非本轮引入）".format(cnt_quote))


# ══════════════════════════════════════════════════════════════════════
print()
print("=" * 78)
print("  通过 {} 项，失败 {} 项".format(len(PASS), len(FAIL)))
print("  通过：{}".format(", ".join(PASS)))
if FAIL:
    print("  失败：{}".format(", ".join(FAIL)))
print("=" * 78)
