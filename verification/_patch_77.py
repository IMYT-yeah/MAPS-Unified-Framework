# -*- coding: utf-8 -*-
"""第 77 轮论文补丁（中英同步 6 项）：§5.7 口径注＋块 ＋ §10.2 #11 标注 ＋ EN 补 A3（C-25 修复）"""
import io, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(ROOT, "MAPS-Unified-Framework", "paper", "history")
TAG = "2026-10-02第77轮前"

for p in (ZH, EN):
    b = os.path.join(HIST, os.path.basename(p).replace(".md", "_备份_{}.md".format(TAG)))
    shutil.copy2(p, b)
    print("  [BK] {}".format(os.path.basename(b)))


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<34} 命中 {} 次 —— 拒绝".format(tag, n))
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<34} 已改".format(tag))


# ── 1. ZH §10.2 #11 行内标注（C-24） ─────────────────────
ZH_11 = "耦合强度谱系预言强:弱:电磁 = 3:2:1（配对阶数）；g 精确值与 α_s/α_EM 完整映射仍开放；"
ZH_11_NEW = ("**配对阶数之比** n_G = 3 : 2 : 1（**群论整数，不是耦合常数之比** —— "
             "⚠️ 第 77 轮 C-24：若按字面读作耦合常数比，强/电磁 = 3 vs 观测（同能标 M_Z）**15.10**，"
             "**差 5.03 倍 ≈ 100σ**）；**g 精确值与 α_s/α_EM 完整映射仍开放**，"
             "而第 77 轮（P1 结项）证明：**这一半也判否** —— ⓐ 弦网 `g` **处处相消**（扫 g 跨 18 个数量级 `J/K` 恒 3）"
             "⟹「精确值」**没有对象**；ⓑ 从 `n_G` 到 `α` 需要的 **4 个换算因子（群论→耦合／弦网标度→M_Z／格点→长度／绝对归一化）一个都没有**，"
             "且 `α` 是 @E 量而 `n_G` 是整数；ⓒ §5.8 自认**连续极限仍开放** ⟹ 连续规范场尚未涌现 ⟹ `α` **连定义域都没有**；"
             "详见 §5.7 末【第 77 轮】块；")
sub_once(ZH, ZH_11, ZH_11_NEW, "ZH §10.2 #11 标注")

# ── 2. EN §10.2 #11 补 A3（C-25 修复）＋ 标注（C-24） ────
EN_11 = "no first-principles values (still open);"
EN_11_NEW = ("**v2.9 A3 first-principles derivation**: `J = n_G·E_P·g` (pairing = condensation of `n_G` events, "
             "strong n=3), `K = m_G·E_P·g` (closure = `m_G` winding flux loops, EM m=1); the same-origin "
             "geometric factor cancels ⟹ **J/K = n_SU(3)/m_U(1) = 3** (dynamical derivation, not heuristic); "
             "transition point h_c = K/J = 1/3 ≈ 0.333 (vs h_xc≈0.32, 4% apart; σ^z field 0.328, 1.6% apart; "
             "P0-3b κ_c∈[0.25,0.32], cross-validated ✓); the absolute scale is Planckian (J~3E_P·g, K~E_P·g); "
             "**the ratio of pairing orders** n_G = 3 : 2 : 1 (**group-theoretic integers, NOT a ratio of "
             "coupling constants** — ⚠️ round-77 C-24: read literally as a coupling-constant ratio, "
             "strong/EM = 3 versus the observed (same scale M_Z) **15.10**, i.e. **off by 5.03× ≈ 100σ**); "
             "**the exact value of `g` and the full `α_s/α_EM` map remain open**, and round 77 (P1 closed) shows "
             "that **this half is also negative**: ⓐ the string-net `g` **cancels identically** (scanning `g` over "
             "18 orders of magnitude leaves J/K exactly 3) ⟹ an \"exact value\" **has no object**; ⓑ the **four "
             "conversion factors** needed from `n_G` to `α` (group theory→coupling / string-net scale→M_Z / "
             "lattice→length / absolute normalization) **are all absent**, and `α` is a @E quantity while `n_G` "
             "is an integer; ⓒ §5.8 itself declares the **continuum limit still open** ⟹ no continuum gauge field "
             "has emerged ⟹ `α` **lacks even a domain of definition**; see the round-77 block at the end of §5.7;")
sub_once(EN, EN_11, EN_11_NEW, "EN §10.2 #11 补 A3 + 标注")

# ── 3. ZH §5.7：口径注 ＋【第 77 轮】块（插在「命题链 B1–B5」之前） ──
ZH_ANCHOR57 = "**命题链 B1–B5**："
ZH_BLOCK = """> **【第 77 轮 P1 口径注（C-24）】** 上式「耦合强度谱系预言强:弱:电磁 = 3:2:1」中的 `3:2:1` 是 **`n_G = d_min(G)` 之比（群论整数）**；「耦合强度谱系」在标准用法里指**耦合常数谱系** ⟹ 两者必须显式分开：**若按字面读作耦合常数比，强/电磁 = 3 与观测（同能标 `M_Z`）15.10 差 5.03 倍（约 100σ）**。⚠️ 另：`J/K = 3` 与 `g` **无关**（同源几何因子相消）⟹ 本节的 `g` **不可识别**。

---

> **【v2.9 补充（第 77 轮：P1 结项 —— `g` 的精确值与 `α_s/α_EM` 的映射「两半都判否」）】** 本轮是**引文取证 ＋ 外部锚点对照 ＋ 数值**（脚本 `_alpha_map_77.py`，**QG-1 … QG-12，12 项 0 失败**）。
>
> · ⭐ **第一半「`g` 的精确值」= 一个没有对象的待办**：§5.7 与 §10.2 #11 两处都只说「同源几何因子 `g` **相消**」。**扫 `g` 从 1e−6 到 137.036（跨 18 个数量级），`J/K` 恒为 3.000000**（极差 4.4×10⁻¹⁶）⟹ **框架能给出的只有比值，而它与 `g` 无关** ⟹ `g` **从未被赋值、也从未需要赋值**。⚠️ 且 `J` 的**绝对尺度是普朗克标度**（`3 E_P` = 3.663×10²⁸ eV，比 `M_Z` 高 **17.6 个数量级**）。（与第 75 轮「缺的不是方程，是对象」**同构**。）
>
> · ⭐ **第二半「`α_s/α_EM` 的映射」被四条独立理由封死**：
>   ① **数字**：若把「3:2:1」按字面读作耦合常数比 —— 强/电磁 = **3** vs 观测（同能标 `M_Z`）**15.0981**（PDG 2024：`α_s(M_Z) = 0.1180 ± 0.0009`、`α_EM⁻¹(M_Z) = 127.95`、`sin²θ_W(M_Z) = 0.23129`）⟹ **差 5.03 倍，约 100σ**；弱/电磁 = 2 vs 4.3236 ⟹ 差 2.16 倍。
>   ② **数性**：`n_G = 3,2,1` 是 **`d_min(G)`（群论整数，与能标无关）**，而 `α` 是**能标依赖量**（`α_s` 自己从 ~2.5 GeV 的 0.32 跑到 `M_Z` 的 0.1180，**差 2.7 倍**）；论文「**跑动**」正文 **0 处**、「**无量纲耦合**」**0 处**、「RG」与「α」的实质同行共现 **0 处** ⟹ **铁律 6：整数比与 `(@E)` 的 `α` 不可比**。
>   ③ **定义域**：§5.8 **自己写着**「连续极限 Z₂→U(1)（**开放**）→ 麦克斯韦 `L_eff = −(1/4)F²` 验证（**开放**）」；§3.4 的标题就是「连续极限的开放问题」⟹ **连续规范场尚未涌现 ⟹ `α` 连定义域都没有**。（这比第 72 轮**更根本**：那边「有场、有质量、无耦合」，这边「**连场都还没有**」。）
>   ④ **换算因子**：按第 54 轮三步法第 3 步清点，从 `n_G` 到 `α` 需要 **4 个**（群论→耦合／弦网标度→`M_Z`／格点→长度／绝对归一化）—— **具备的 = 0**。⚠️ 其中「格点间距 `a`」在第 55 / 60 轮已被指出过（那时是给**化学键**量纲），本轮是**第二次**撞到同一个缺失。
>
> · **判别力 = 0**：即便将来补上四个因子，`g` 仍是自由参数（可调 1 个、测 2 个）⟹ 是**拟合**而非预言；且唯一可检验的影子「3 : 2 : 1」在 `α` 上**已被 5.03 倍排除**。
>
> · ⚠️ **C-24（措辞）**：「耦合强度谱系预言强:弱:电磁 = 3:2:1」应改为「**配对阶数之比 `n_G = 3 : 2 : 1`（群论整数，不是耦合常数之比）**」。
>
> · ⚠️ **C-25（本轮顺带查出：中英不同步）**：**英文稿完全没有 v2.9 A3 的内容** —— EN §5.7 正文无 `J = n_G·E_P·g`、EN §10.2 #11 仍写「no first-principles values (still open)」，且 EN 全文 `3:2:1` **0 处**。本轮**已补齐**（EN §5.7 加对应句、EN §10.2 #11 同步更新）。
>
> ⚠️ **五条诚实边界**：① 「5.03 倍」是**按字面读**的后果，而 §10.2 #11 的括号里写了「（配对阶数）」⟹ 严格说不是「算错」而是**措辞风险**（故记 C-24 而非 N）；② 外部锚点是 **PDG 2024 / CODATA 的引文**，本轮未独立复算其误差；`α_W` 用 `α_EM/sin²θ_W` 这一常用口径（弱耦合定义在文献里不唯一）；③ 「`g` 处处相消」只针对 §5.7 的 `J`、`K` 两个定义式，**未证明**框架在别处也不能给 `g` 一个值；④ QG-7 的四个换算因子是**必要性清点**，补上它们**不保证**映射存在（还需 `α = f(n_G)` 的形式）；⑤ 本轮**不改 §10.2 #11 的实质内容**，只加口径注与本节末的【第 77 轮】块。

"""
txt = io.open(ZH, encoding="utf-8").read()
n = txt.count(ZH_ANCHOR57)
if n != 1:
    print("  [XX] ZH §5.7 锚点命中 {} 次".format(n))
else:
    txt = txt.replace(ZH_ANCHOR57, ZH_BLOCK + ZH_ANCHOR57, 1)
    io.open(ZH, "w", encoding="utf-8").write(txt)
    print("  [OK] {:<34} 已加注 + 插块".format("ZH §5.7"))

# ── 4. EN §5.7：补 A3 句（C-25 修复）＋ 块 ───────────────
EN_ANCHOR57 = "**Proposition chain B1–B5**:"
EN_A3 = """**First-principles origin of J/K (v2.9 A3)**: `J = n_G·E_P·g` (pairing = condensation of `n_G` events, strong n=3), `K = m_G·E_P·g` (closure = `m_G` winding flux loops, EM m=1); the same-origin geometric factor cancels ⟹ **J/K = n_SU(3)/m_U(1) = 3**, transition point h_c = K/J = 1/3 (cross-validated against h_xc≈0.32; see §10.2 #11).

> **【Round-77 P1 caliber note (C-24)】** In "the coupling-strength spectrum predicts strong:weak:EM = 3:2:1" above, `3:2:1` is a ratio of **`n_G = d_min(G)` (group-theoretic integers)**; "coupling-strength spectrum" normally means a **coupling-constant** spectrum ⟹ the two must be kept explicitly apart: **read literally as a coupling-constant ratio, strong/EM = 3 differs from the observed (same scale `M_Z`) 15.10 by a factor 5.03 (≈ 100σ)**. ⚠️ Also, `J/K = 3` is **independent of `g`** (the same-origin geometric factor cancels) ⟹ the `g` of this subsection is **not identifiable**.

---

> **【v2.9 supplement (round 77: P1 closed — "the exact value of `g`" and "the `α_s/α_EM` map" are *both* negative)】** This round is a **citation check + external-anchor comparison + numerics** (script `_alpha_map_77.py`, **QG-1 … QG-12, 12 items, 0 failures**).
>
> · ⭐ **First half, "the exact value of `g`" = a task with no object**: both §5.7 and §10.2 #11 say only that the same-origin geometric factor `g` **cancels**. **Scanning `g` from 1e−6 to 137.036 (18 orders of magnitude) leaves `J/K` exactly 3.000000** (spread 4.4×10⁻¹⁶) ⟹ **the framework can produce only the ratio, and it is independent of `g`** ⟹ `g` is **never assigned a value and never needs one**. ⚠️ Moreover the **absolute scale of `J` is Planckian** (`3 E_P` = 3.663×10²⁸ eV, **17.6 orders of magnitude** above `M_Z`). (Isomorphic to round 75's "what is missing is not the equation but the object".)
>
> · ⭐ **Second half, "the `α_s/α_EM` map", is sealed off by four independent reasons**:
>   ① **Numbers**: reading "3:2:1" literally as a coupling-constant ratio gives strong/EM = **3** versus the observed (same scale `M_Z`) **15.0981** (PDG 2024: `α_s(M_Z) = 0.1180 ± 0.0009`, `α_EM⁻¹(M_Z) = 127.95`, `sin²θ_W(M_Z) = 0.23129`) ⟹ **off by 5.03×, ≈ 100σ**; weak/EM = 2 versus 4.3236 ⟹ off by 2.16×.
>   ② **Kind of number**: `n_G = 3,2,1` is **`d_min(G)` (group-theoretic integers, scale-independent)**, whereas `α` is **scale-dependent** (`α_s` itself runs from 0.32 at ~2.5 GeV to 0.1180 at `M_Z`, a factor **2.7**); in the paper "**running**" occurs **0 times** in the body, "**dimensionless coupling**" **0 times**, and "RG" co-occurs substantively with "α" **0 times** ⟹ **iron rule 6: an integer ratio cannot be compared with a `(@E)` quantity like `α`**.
>   ③ **Domain of definition**: §5.8 **itself states** "continuum limit Z₂→U(1) (**open**) → Maxwell `L_eff = −(1/4)F²` verification (**open**)"; the title of §3.4 is literally "open problems of the continuum limit" ⟹ **no continuum gauge field has emerged ⟹ `α` lacks even a domain of definition**. (This is **more fundamental** than round 72: there "field and mass exist but the coupling does not"; here "**even the field is not there yet**".)
>   ④ **Conversion factors**: by step 3 of round 54's three-step test, going from `n_G` to `α` requires **4** (group theory→coupling / string-net scale→`M_Z` / lattice→length / absolute normalization) — **present: 0**. ⚠️ The lattice spacing `a` had already been flagged in rounds 55 / 60 (then for **chemical bonds**); this round hits the same gap a **second** time.
>
> · **Discriminating power = 0**: even if the four factors were later supplied, `g` would remain free (1 adjustable, 2 measured) ⟹ a **fit**, not a prediction; and the only testable shadow, the ratio "3 : 2 : 1", is **already excluded by the factor 5.03** on `α`.
>
> · ⚠️ **C-24 (wording)**: "the coupling-strength spectrum predicts strong:weak:EM = 3:2:1" should read "**the ratio of pairing orders `n_G = 3 : 2 : 1` (group-theoretic integers, not a ratio of coupling constants)**".
>
> · ⚠️ **C-25 (found in passing this round: ZH/EN desync)**: **the English manuscript lacks the entire v2.9 A3 content** — EN §5.7's body has no `J = n_G·E_P·g`, EN §10.2 #11 still reads "no first-principles values (still open)", and `3:2:1` occurs **0 times** in EN. This round **supplies the missing content** (an A3 sentence in EN §5.7; §10.2 #11 updated).
>
> ⚠️ **Five honesty boundaries**: ① the "5.03×" is a consequence of **reading literally**, whereas §10.2 #11's parenthesis says "(pairing order)" ⟹ strictly this is a **wording risk**, not an arithmetic error (hence C-24, not N); ② the external anchors are **citations of PDG 2024 / CODATA**, not independently recomputed here; `α_W` uses the common convention `α_EM/sin²θ_W` (the weak coupling is defined variously in the literature); ③ "`g` cancels identically" refers only to the two definitions of `J` and `K` in §5.7 — it is **not proved** that the framework cannot assign `g` a value elsewhere; ④ round 77's four conversion factors are a **necessity count**; supplying them does **not guarantee** the map exists (an `α = f(n_G)` form is also needed); ⑤ this round **does not alter the substance of §10.2 #11**, adding only a caliber note and the round-77 block at the end of this subsection.

"""
txt = io.open(EN, encoding="utf-8").read()
n = txt.count(EN_ANCHOR57)
if n != 1:
    print("  [XX] EN §5.7 锚点命中 {} 次".format(n))
else:
    txt = txt.replace(EN_ANCHOR57, EN_A3 + EN_ANCHOR57, 1)
    io.open(EN, "w", encoding="utf-8").write(txt)
    print("  [OK] {:<34} 已补 A3 + 插块".format("EN §5.7"))

# ── 自查 ─────────────────────────────────────────────────
print()
for p, nm in ((ZH, "ZH"), (EN, "EN")):
    L = io.open(p, encoding="utf-8").read().split("\n")
    bad_pipe = sum(1 for s in L if "\\|" in s and not s.lstrip().startswith("|"))
    frag = [i + 1 for i, s in enumerate(L) if s.strip().startswith(("，", ","))]
    print("  {} 行数 {}；非表格反斜杠竖线 {}；残片行 {}".format(nm, len(L), bad_pipe, frag))
print("  ZH「第 77 轮」=", io.open(ZH, encoding="utf-8").read().count("第 77 轮"))
print("  EN「round 77」=", io.open(EN, encoding="utf-8").read().count("round 77"))
print("  EN「3:2:1」=", io.open(EN, encoding="utf-8").read().count("3:2:1"))
print("  EN「n_G·E_P·g」=", io.open(EN, encoding="utf-8").read().count("n_G·E_P·g"))
