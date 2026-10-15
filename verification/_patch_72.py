# -*- coding: utf-8 -*-
"""第 72 轮论文补丁（中英同步）。锚点必须恰好命中一次，否则拒绝。"""
import io
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
HIST = os.path.join(ROOT, "MAPS-Unified-Framework", "paper", "history")
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

OK = []
BAD = []


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<30} 命中 {} 次 —— 拒绝".format(tag, n))
        BAD.append(tag)
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<30} 已改".format(tag))
    OK.append(tag)


# ── 0. 备份 ───────────────────────────────────────────────────────────
for p in (ZH, EN):
    dst = os.path.join(HIST, os.path.basename(p).replace(
        ".md", "_备份_2026-10-02第72轮前.md"))
    shutil.copy2(p, dst)
    print("备份 -> {}".format(os.path.basename(dst)))

# ══ 中文稿 ════════════════════════════════════════════════════════════
A_ZH_55 = ("力程 **`λ = 0.81 l_P`** ⟹ 与第五力搜索窗口（微米–星系）相差 "
           "**29–55 个数量级**（完全不可观测）。")

BLOCK_ZH = """
> **【v2.9 补充（第 72 轮：Φ 的耦合强度 —— I-17 耦合侧结项）】** 脚本 `_phi_coupling_72.py`（**PC-1 … PC-9，9 项 0 失败**）。第 70 轮做了 I-17 的**质量侧**，本轮做**耦合侧**（＝它未给的另一半）。
> · **耦合 `g` 是 Φ 的第 4 个纯输入**：Φ 一个场挂 **Λ**（§4.5b 谱作用截断）、**μ**（§6.4 势的质量参数）、**λ**（§6.4 四次耦合）、**g**（§6.1 钉扎项 `gΦψ̄ψ`），而**没有一行**把它们互相约束（含 `gΦ` 记号的等式 **0 处**、势内 μ–λ 关系 **0 处**）。⭐ **判定证据**：§6.2 的「退化检验」把 `g=0` 列为**特例** ⟹ **框架自己按自由参数在用 `g`**。
> · ⚠️ §4.5b 的「VEV 决定耦合常数与质量」有两种读法、且**两种都缺**：(a) 决定**规范耦合**（标准 KK 的 `g₄² = g₅²/(2πR)`）⟹ 与钉扎 `g` 无关；(b) 决定 **Φ–物质耦合**本身 ⟹ 那就存在一条关系，但**函数形式未写出**（0 处）。
> · ⭐ **桌面实验对照（外部锚点）**：引力强度（α = 1）Yukawa 修正的排除边界已由 Eöt-Wash 组推到 **39 μm**（197 → 56 → 42 → 39 μm @ 2001/2007/2013/2020）；Tan et al., PRL 124, 051301 (2020) 在 **40–350 μm** 区间给出 α 的最强上界，λ = 48 μm 处仍为 |α| ≤ 1。⟹ 对第 70 轮的四个质量档：**(b) 193.8 μm 与 (c) 47.1 μm 都落在已测区间**（后者在 39–48 μm 的边界缝隙），**(a)(d) 档 ~ l_P 既未排除也不可观测**。
> · ⭐ **§4.5b 的 `γ = β = 1` 对这个耦合失明**：λ = 0.194 mm 的标量在 1 AU 的 Yukawa 因子 = **10^(−3.35×10¹⁴)** ⟹ 太阳系 PPN 与 EMRI 强场检验**既不构成约束、也不构成冲突**；约束只能来自桌面实验。而框架**没有屏蔽机制**（chameleon / symmetron / Vainshtein / galileon / dilaton **各 0 处**）。
> · **三分支判决**：(i) **自由输入**（= 框架现状）⟹ 相互作用是 **4 参数族（Λ, μ, λ, g）**、**可识别性 = 0** ⟹ **零预言力**；(ii) 取 KK 读法 ＋ 毫米档 ⟹ 力程落在 **40–350 μm 已测区间** ⟹ **已被排除**；(iii) 同上 ＋ 普朗克档 ⟹ 力程 0.81 l_P ⟹ **不可观测**。⟹ **三选一全是死路**。与第 61 轮（工程出口 = 0）、第 62 轮（四力位无空位）合起来：**「第五力」这条线在框架内彻底关死** —— 不是「还没算」，是「**算出来也不能用**」。
> · **判决**：**I-17 结项**（质量侧第 70 轮 ＋ 耦合侧第 72 轮）—— 该位置的状态 = **「有场、有质量档位、无耦合」**；登记 **N-28**（负面）与 **C-15**（更正）。
> · ⚠️ **诚实边界六条**：① 39 / 48 / 40–350 μm 是**引文**，本轮未独立复算；② 「耦合 = 引力强度（α ~ 1/3–1）」是**标准 KK 的知识**，框架**从未**写出 α ⟹ (ii)/(iii) 是**条件结论**；③ 「`m_Φ` = 该截断能标」沿用第 70 轮的**假设**（半拟合）；④ **新查出**：第 70 轮弦网档的 `0.813 l_P` **隐含取 `g = 1`**（因 `J = n_G·E_P·g`）⟹ 该力程**本身是 `g` 的函数**；⑤ 屏蔽「0 处」是**引文清点**，不等于「框架证明了不存在屏蔽」；⑥ 本轮**未跑新数值**（除力程复算与 Yukawa 因子），结论性质 = **结构审查 ＋ 引文取证 ＋ 外部对照**。
"""

A_ZH_61 = ('- 钉扎项 gΦψ̄ψ：环境依赖有效质量 m_eff(x) = m + gΦ(x)——"粒子被风暴钉住"；')
N_ZH_61 = A_ZH_61 + """
- ⚠️【**第 72 轮口径注**】`g` 在本框架里是 **Φ 的第 4 个纯输入**（与 §4.5b 的 `Λ`、§6.4 的 `μ` 与 `λ` 并列），框架对它**零约束**（§6.2 的退化检验把 `g = 0` 当特例）；且 `g` 与 §5.7 的弦网几何因子 `J = n_G·E_P·g` **同字母两义** ⟹ 见 **C-15**。"""

A_ZH_26 = "全文 26 行；§8 此前为 0 行"
N_ZH_26 = "全文 **44 行**（第 72 轮实测；原记 26 行已过期）；§8 此前为 0 行"

A_ZH_867 = "> **`Ω_tot = 1`**，也就是平坦性本身。"
N_ZH_867 = A_ZH_867 + """
> ⚠️ **第 72 轮补注（C-15）**：`λ` 还有**第三义** —— §6.4 的 Φ⁴ 四次耦合 `V(Φ) = −½μ²Φ² + ¼λΦ⁴`（本约定此前**未提**）；另有 **`g` 同字母两义**（§6.1 的钉扎耦合 `gΦψ̄ψ` vs §5.7 的弦网几何因子 `J = n_G·E_P·g`），**此前无任何约定**。"""

print("\n[ZH]")
sub_once(ZH, A_ZH_55, A_ZH_55 + BLOCK_ZH, "§5.5 插第 72 轮块")
sub_once(ZH, A_ZH_61, N_ZH_61, "§6.1 g 的口径注")
sub_once(ZH, A_ZH_26, N_ZH_26, "§8.6 行数更正")
sub_once(ZH, A_ZH_867, N_ZH_867, "§8.6 C-15 补注")

# ══ 英文稿 ════════════════════════════════════════════════════════════
A_EN_55 = ("**`λ = 0.81 l_P`** ⟹ **29–55 orders of magnitude** away from the "
           "fifth-force search windows (micron to galactic) — utterly unobservable.")

BLOCK_EN = """
> **【v2.9 supplement (Round 72: the coupling of Φ — closing the coupling side of I-17)】** Script `_phi_coupling_72.py` (**PC-1 … PC-9, 9 checks, 0 failures**). Round 70 did the **mass side** of I-17; this round does the **coupling side** (the other half it left open).
> · **The coupling `g` is the 4th pure input of Φ**: a single field Φ carries **Λ** (§4.5b spectral-action cutoff), **μ** (§6.4 mass parameter), **λ** (§6.4 quartic coupling) and **g** (§6.1 pinning term `gΦψ̄ψ`), and **not one line** constrains them against each other (equalities containing the `gΦ` token: **0**; μ–λ relations inside the potential: **0**). ⭐ **Decisive evidence**: §6.2's "degeneracy check" lists `g = 0` as a **special case** ⟹ **the framework itself treats `g` as a free parameter**.
> · ⚠️ §4.5b's "the VEV determines the coupling constants and masses" admits two readings, and **both are missing**: (a) it determines the **gauge couplings** (standard KK: `g₄² = g₅²/(2πR)`) ⟹ unrelated to the pinning `g`; (b) it determines the **Φ–matter coupling** itself ⟹ a relation exists but its **functional form is never written** (0 occurrences).
> · ⭐ **Tabletop comparison (external anchors)**: the exclusion boundary for gravitational-strength (α = 1) Yukawa corrections has been pushed by the Eöt-Wash group to **39 μm** (197 → 56 → 42 → 39 μm in 2001/2007/2013/2020); Tan et al., PRL 124, 051301 (2020) give the strongest bound on α over **40–350 μm**, with |α| ≤ 1 still holding at λ = 48 μm. ⟹ For round 70's four mass tiers: **(b) 193.8 μm and (c) 47.1 μm both fall inside the probed range** (the latter in the 39–48 μm gap), while **(a)(d) at ~ l_P are neither excluded nor observable**.
> · ⭐ **§4.5b's `γ = β = 1` is blind to this coupling**: a scalar with λ = 0.194 mm has a Yukawa factor at 1 AU of **10^(−3.35×10¹⁴)** ⟹ solar-system PPN and the EMRI strong-field tests are **neither a constraint nor a conflict**; the only constraints come from tabletop experiments. And the framework has **no screening mechanism** (chameleon / symmetron / Vainshtein / galileon / dilaton: **0 each**).
> · **Three-branch verdict**: (i) **free input** (= the framework as it stands) ⟹ the interaction is a **4-parameter family (Λ, μ, λ, g)** with **identifiability = 0** ⟹ **zero predictive power**; (ii) take the KK reading with the millimetre tier ⟹ the range lands in the **already-probed 40–350 μm band** ⟹ **already excluded**; (iii) same with the Planck tier ⟹ range 0.81 l_P ⟹ **unobservable**. ⟹ **All three branches are dead ends.** Together with round 61 (engineering exits = 0) and round 62 (no free slot among the four forces): **the "fifth force" line is closed inside the framework** — not "not yet computed", but "**computable and still unusable**".
> · **Verdict**: **I-17 closed** (mass side in round 70 + coupling side in round 72) — the status of that slot = **"a field, with mass tiers, without a coupling"**; registered: **N-28** (negative) and **C-15** (correction).
> · ⚠️ **Six honesty boundaries**: ① the 39 / 48 / 40–350 μm numbers are **citations**, not independently recomputed here; ② "coupling = gravitational strength (α ~ 1/3–1)" is **standard-KK knowledge**, the framework **never** writes α ⟹ (ii)/(iii) are **conditional conclusions**; ③ "`m_Φ` = that cutoff scale" inherits round 70's **assumption**; ④ **newly found**: round 70's string-net tier `0.813 l_P` **implicitly took `g = 1`** (since `J = n_G·E_P·g`) ⟹ that range is **itself a function of `g`**; ⑤ the "0 screening mechanisms" is a **citation count**, not a proof that screening is impossible; ⑥ **no new numerics** this round (beyond recomputing the ranges and the Yukawa factor) — the conclusion is a **structural audit + citation evidence + external comparison**.
"""

A_EN_61 = ('- Pinning term gΦψ̄ψ: environment-dependent effective mass '
           'm_eff(x) = m + gΦ(x) — "the particle is pinned by the storm";')
N_EN_61 = A_EN_61 + """
- ⚠️【**Round-72 notation note**】`g` is **the 4th pure input of Φ** in this framework (alongside `Λ` of §4.5b and `μ`, `λ` of §6.4), with **zero constraints** (see §6.2's degeneracy check putting `g = 0` as a special case); and `g` **carries two meanings under one letter** (§5.7's string-net geometric factor `J = n_G·E_P·g`) ⟹ see **C-15**."""

A_EN_26 = "(11 lines in §5, 26 in the whole"
N_EN_26 = "(11 lines in §5, **44** in the whole (measured in round 72; the earlier 26 is stale)"

A_EN_867 = ("> A useful side effect: the earlier note \"λ = 1\" is revealed to be "
            "**`Ω_tot = 1`** — i.e. flatness itself.")
N_EN_867 = A_EN_867 + """
> ⚠️ **Round-72 addendum (C-15)**: `λ` carries a **third meaning** — the Φ⁴ quartic coupling of §6.4, `V(Φ) = −½μ²Φ² + ¼λΦ⁴` (**not mentioned** in this convention before); and **`g` carries two meanings under one letter** (§6.1's pinning coupling `gΦψ̄ψ` vs §5.7's string-net geometric factor `J = n_G·E_P·g`), previously **undeclared**. """

print("\n[EN]")
sub_once(EN, A_EN_55, A_EN_55 + BLOCK_EN, "§5.5 insert Round-72 block")
sub_once(EN, A_EN_61, N_EN_61, "§6.1 g notation note")
sub_once(EN, A_EN_26, N_EN_26, "§8.6 line-count correction")
sub_once(EN, A_EN_867, N_EN_867, "§8.6 C-15 addendum")

print("\n通过 {} 项，失败 {} 项".format(len(OK), len(BAD)))
if BAD:
    print("失败：{}".format(BAD))
