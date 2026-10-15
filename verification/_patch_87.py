# -*- coding: utf-8 -*-
"""
第 87 轮论文补丁（中英同步）
  新增【第 87 轮】块：h_min 标度律的**分组重拟合** ＋ C-41（宏观外推口径）
  并在第 50 / 51 轮块的对应行加**指向标记**
"""
import io, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "outputs")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

BAD = []
def sub_once(path, old, new, tag, n=1):
    t = io.open(path, encoding="utf-8").read()
    c = t.count(old)
    if c != n:
        print("  [XX] {:<50} 命中 {}（期望 {}）".format(tag, c, n)); BAD.append(tag); return False
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, n))
    print("  [OK] {:<50} 已改".format(tag)); return True


def append_block(path, block_text, anchor_start, tag):
    """把 block 插到「以 anchor_start 开头的那个 `>` 块」的**末尾**（块链尾部）。"""
    L = io.open(path, encoding="utf-8").read().split("\n")
    cand = [k for k, s in enumerate(L) if anchor_start in s]
    if len(cand) != 1:
        print("  [XX] {:<50} 锚命中 {}（期望 1）".format(tag, len(cand))); BAD.append(tag); return False
    i = cand[0]
    j = i
    while j + 1 < len(L) and L[j + 1].lstrip().startswith(">"):
        j += 1
    print("  [锚] {} 块 L{}–L{}".format(tag, i + 1, j + 1))
    out = L[:j + 1] + ["", block_text] + L[j + 1:]
    io.open(path, "w", encoding="utf-8").write("\n".join(out))
    print("  [OK] {:<50} 已插入（{} 行）".format(tag, len(block_text.split("\n"))))
    return True


# ================================================================
ZH_BLOCK = """> **【v2.9 补充（第 87 轮：`h_min` 标度律的**分组重拟合** —— 上面那个「混合拟合」没有物理意义）】** 第 86 轮已证「**退化方向数**」是 H/N 的**主控变量**（= 数值格点的伪影程度）；而第 50 轮的 9 点标度律把**两族混在一起**了。本轮**同一 N ≥ 32 窗口**重拟合（脚本 `_scaling_split_87.py`，**SS-1 … SS-8，8 项 0 失败**）。
>
> | 组 | 判据 | 点数 | 拟合 | 最大残差 |
> |---|---|---|---|---|
> | **A** | 退化方向 **≥ 2**（伪影重） | 4 | `H/N = 0.2265·N^{+0.2051}` | **0.6%** |
> | **B** ⭐（物理对应） | 退化方向 **≤ 1** | 8 | `H/N = 3.0887·N^{−0.6836}` | **2.2%** |
>
> · ⭐⭐ **两组指数符号相反**：组 A **`p = +0.205 > 0`**（H/N 随 N **上升**，趋近 `ln2` —— 退化把轨道限死了）；组 B **`p = −0.684 < 0`**（H/N 随 N **下降**）。机制侧一致：`⟨ln|O|⟩/N` 组 A **下降**（斜率 −0.033）、组 B **上升**（+0.106）⟹ **把两族混拟合，等于把一条上升曲线与一条下降曲线拼起来**，得到的指数（≈ −0.93）**既不是 A 的也不是 B 的**。
> · ⭐⭐ **留一外推检验（决定性判据）**：只训练 N ≤ 96 的点，预测 (6,6,6) N = 216 —— **组 B 给 0.0793**（实测 0.0779，误差 **+1.7%**）；**混合给 0.0681**（误差 **−12.6%**）⟹ **组 B 好约 7 倍**，这是**可判定的改进**。
> · ⚠️ **组 A 的全窗口**（含 N ≤ 24）残差 **7.9%** —— 那一段有一个「浅谷」（`0.4679 → 0.4335 → 0.4334 → 0.4617`，**第 49 轮已记录**）⟹ **两族的幂律只应报在 N ≥ 32 窗口**。
> · ⚠️ **阈值精确化**（第 86 轮判据的收紧）：同 **N = 64** 下，**退化 0 个（0.1839）与 1 个（0.1802）只差 2.1%**，而 **1 个 → ≥ 2 个跳 ×2.95** ⟹ **真正有害的是「≥ 2 个退化方向」**，而不是「有退化方向」。
> · ⚠️ ⭐ **C-41（宏观外推的口径）**：第 51 轮用**混合**拟合 `3.01·N^{−0.6762}` 得 `H/N ≈ 5.4×10⁻⁵²`（余量 ≈ 4.7×10⁵⁰）。改用**组 B** 的干净拟合 `3.0887·N^{−0.6836}` 复算，得 **`H/N ≈ 2.7×10⁻⁵³`** ⟹ 与 5.4×10⁻⁵² **同量级（差约 4 倍）**，**余量结论不变**。⚠️ 但**必须声明口径**：混合拟合对「选哪些点」**极度敏感** —— 把全部 N ≥ 32 的 **12 点**混拟合给 **4.5×10⁻⁷²**，与组 B **相差 19 个数量级**。⟹ **宏观 H/N 的外推必须写形状口径**（与第 86 轮的规范同一条）。
> · 📌 **规范（第 87 轮）**：**标度律拟合前先按「退化方向数」分组**；**混合族的幂指数不得外推**。

"""

EN_BLOCK = """> **【v2.9 supplement (round 87: a **group-wise refit** of the `h_min` scaling law — the "mixed fit" above has no physical meaning)】** Round 86 established that the **number of degenerate directions** is the **controlling variable** of H/N (i.e. how much numerical artefact the lattice carries); yet round 50's nine-point scaling law **mixed the two families**. Refitting on the **same N ≥ 32 window** (script `_scaling_split_87.py`, **SS-1 … SS-8, 8 items, 0 failures**):
>
> | Group | Criterion | Points | Fit | Max residual |
> |---|---|---|---|---|
> | **A** | degenerate directions **≥ 2** (heavily polluted) | 4 | `H/N = 0.2265·N^{+0.2051}` | **0.6%** |
> | **B** ⭐ (physically relevant) | degenerate directions **≤ 1** | 8 | `H/N = 3.0887·N^{−0.6836}` | **2.2%** |
>
> · ⭐⭐ **The two exponents have opposite signs**: group A has **`p = +0.205 > 0`** (H/N **rises** with N, approaching `ln2` — degeneracy pins the orbits down); group B has **`p = −0.684 < 0`** (H/N **falls** with N). The mechanism agrees: `⟨ln|O|⟩/N` **falls** in group A (slope −0.033) and **rises** in group B (+0.106) ⟹ **mixing the two families is like splicing a rising curve onto a falling one**, and the resulting exponent (≈ −0.93) is **neither** A's **nor** B's.
> · ⭐⭐ **Leave-one-out extrapolation test (the decisive criterion)**: training only on the points with N ≤ 96 and predicting (6,6,6) at N = 216 — **group B gives 0.0793** (measured 0.0779, error **+1.7%**); **the mixed fit gives 0.0681** (error **−12.6%**) ⟹ **group B is about 7× better**; this is a **decidable improvement**.
> · ⚠️ **Group A's full window** (including N ≤ 24) has a residual of **7.9%** — that stretch contains a **shallow dip** (`0.4679 → 0.4335 → 0.4334 → 0.4617`, **already recorded in round 49**) ⟹ **both power laws should be quoted only on the N ≥ 32 window**.
> · ⚠️ **Sharpened threshold** (a tightening of round 86's criterion): at the **same N = 64**, **0 degenerate directions (0.1839) and 1 (0.1802) differ by only 2.1%**, whereas **1 → ≥ 2 jumps by ×2.95** ⟹ **what is genuinely harmful is "≥ 2 degenerate directions"**, not "having a degenerate direction".
> · ⚠️ ⭐ **C-41 (the caliber of the macroscopic extrapolation)**: round 51 used the **mixed** fit `3.01·N^{−0.6762}` to obtain `H/N ≈ 5.4×10⁻⁵²` (margin ≈ 4.7×10⁵⁰). Recomputing with **group B**'s clean fit `3.0887·N^{−0.6836}` gives **`H/N ≈ 2.7×10⁻⁵³`** ⟹ **the same order of magnitude as 5.4×10⁻⁵² (a factor ≈ 4 apart)**, so **the margin conclusion is unchanged**. ⚠️ But the **caliber must be stated**: the mixed fit is **extremely sensitive** to which points are chosen — mixing **all 12** points with N ≥ 32 gives **4.5×10⁻⁷²**, i.e. **19 orders of magnitude away** from group B. ⟹ **any macroscopic H/N extrapolation must carry the shape caliber** (the same norm as in round 86).
> · 📌 **Norm (round 87)**: **group by the number of degenerate directions before fitting a scaling law**; **the exponent of a mixed family must not be extrapolated**.

"""

# ① ZH：块链末尾加第 87 轮块（锚 = 第 86 轮块起点）
print("[ZH-1] 块链末尾插入【第 87 轮】块")
append_block(ZH, ZH_BLOCK, "【v2.9 审计（第 86 轮", "ZH 第87轮块")

# ② ZH：第 50 轮块的行加指向标记
print("\n[ZH-2] 指向标记")
sub_once(ZH, "（最大残差 **2.6%**）；留一外推（只用 N ≤ 96）预测 N = 216 为 0.0828，实测 0.0779（误差 **+6.3%**）",
         "（最大残差 **2.6%**）；留一外推（只用 N ≤ 96）预测 N = 216 为 0.0828，实测 0.0779（误差 **+6.3%**）"
         "〔⚠️ **第 87 轮：该混合拟合已被分组重拟合取代，见本节末【第 87 轮】块；且「9 点」是哪 9 个未记录**〕",
         "ZH 第50轮块 指向标记")

# ③ ZH：第 51 轮宏观外推加口径指针
sub_once(ZH, "太阳质量黑洞 N = A/l_P² ≈ **4.20×10⁷⁷** ⟹ H/N ≈ **5.4×10⁻⁵²** 纳特/格点 ⟹ **余量 ≈ 4.7×10⁵⁰ 倍**",
         "太阳质量黑洞 N = A/l_P² ≈ **4.20×10⁷⁷** ⟹ H/N ≈ **5.4×10⁻⁵²** 纳特/格点 ⟹ **余量 ≈ 4.7×10⁵⁰ 倍**"
         "〔⚠️ **第 87 轮口径注 C-41**：改用物理对应的**组 B** 干净拟合复算得 **2.7×10⁻⁵³**（同量级、差约 4 倍，余量结论不变）；"
         "但混合拟合对该用哪些点**极度敏感**（全 12 点给 4.5×10⁻⁷²，相差 19 个数量级）—— 见本节末【第 87 轮】块〕",
         "ZH 第51轮 口径指针")

# ④ EN
print("\n[EN-1] 块链末尾插入 round-87 块")
append_block(EN, EN_BLOCK, "(round 86:", "EN round-87 块")

print("\n[EN-2] 指向标记")
sub_once(EN, "Leave-one-out extrapolation (training on N ≤ 96 only) predicts 0.0828 at N = 216 against a measured 0.0779 (**+6.3%** error)",
         "Leave-one-out extrapolation (training on N ≤ 96 only) predicts 0.0828 at N = 216 against a measured 0.0779 (**+6.3%** error) "
         "[⚠️ **round 87: this mixed fit is superseded by the group-wise refit — see the round-87 block at the end of this section; "
         "and which nine points were used was never recorded**]",
         "EN round-50 block pointer")

sub_once(EN, "a solar-mass black hole has N = A/l_P² ≈ **4.20×10⁷⁷** ⟹ H/N ≈ **5.4×10⁻⁵²** nats/site ⟹ **margin ≈ 4.7×10⁵⁰**",
         "a solar-mass black hole has N = A/l_P² ≈ **4.20×10⁷⁷** ⟹ H/N ≈ **5.4×10⁻⁵²** nats/site ⟹ **margin ≈ 4.7×10⁵⁰** "
         "[⚠️ **round-87 caliber note C-41**: recomputing with the physically relevant **group B** clean fit gives **2.7×10⁻⁵³** "
         "(same order, a factor ≈ 4 apart; the margin conclusion is unchanged); but the mixed fit is **extremely sensitive** to the point "
         "selection (all 12 points give 4.5×10⁻⁷², 19 orders of magnitude away) — see the round-87 block at the end of this section]",
         "EN round-51 pointer")

print("\n失败项：{}".format(BAD if BAD else "无 ✓"))
if BAD:
    sys.exit(1)
