# -*- coding: utf-8 -*-
"""
第 86 轮论文补丁（中英同步）
  C-39：第 78 轮块结论 ④ 的形状口径缺失 ＋ 结论方向有误
  C-40：第 48 轮「0.25 落在空隙里」—— 0.25 < 0.2834，不在空隙里
  另：§4.8 块链末加【第 86 轮】审计块
"""
import io, os, sys, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "outputs")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

BAD = []
def sub_once(path, old, new, tag, n=1):
    t = io.open(path, encoding="utf-8").read()
    c = t.count(old)
    if c != n:
        print("  [XX] {:<46} 命中 {}（期望 {}）".format(tag, c, n)); BAD.append(tag); return False
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, n))
    print("  [OK] {:<46} 已改".format(tag))

# ================================================================
# ① C-39：ZH 第 78 轮块结论 ④（整行做锚 —— 陷阱 74）
# ================================================================
print("[ZH-1] C-39：第 78 轮块结论 ④")
Z_OLD = ("> · **不变的四条结论**：① 不完备度**随 N 单调增长**（两套群下都成立）；② (Z₂)³ 不变量在 N ≥ 16 立即不完备；"
         "③ N = 8 的「14 = 14」是**偶然**（不变量退化，且**与生成元无关**）；④ **H/N 在 N=16 → 24 几乎饱和**"
         "（0.4335 → 0.4334）且 ≈ 0.433 ≫ 0.25 ⟹ **面积律在能算的格点上不成立**。")
Z_NEW = ("> · **不变的四条结论**：① 不完备度**随 N 单调增长**（两套群下都成立）；② (Z₂)³ 不变量在 N ≥ 16 立即不完备；"
         "③ N = 8 的「14 = 14」是**偶然**（不变量退化，且**与生成元无关**）；④ **H/N 在 N=16 → 24 几乎饱和**"
         "（0.4335 → 0.4334）~~且 ≈ 0.433 ≫ 0.25 ⟹ **面积律在能算的格点上不成立**~~。\n"
         "> ⚠️ ⭐ **【第 86 轮更正（C-39）：形状口径缺失 ＋ 结论方向有误】** 上一句有两个问题：\n"
         "> · **(a) 缺形状口径**：这两个数只来自 **(2,2,L) 系列**（含 **2 个长度为 2 的方向**）—— "
         "而长度 2 的环只有**一种**完美匹配 ⟹ 该方向 **σ_j = 恒等、不贡献相位自由度**（第 48 轮的机制），"
         "故 (2,2,L) 是**退化最重**的一族，`0.433` **不代表一般格点**；\n"
         "> · **(b) 结论方向反了**：**无退化**（0 个长度 2 方向）的算例 —— **(4,4,4) = 0.1839**、**(6,6,6) = 0.0779** "
         "—— **均 < 0.25 ⟹ 面积律在这两个算例上成立**（第 48 / 49 轮已算出，见上文两块）。\n"
         "> ⟹ **准确表述**：「**H/N 在退化 ≥ 2 个方向的细长格点上 ∈ [0.4334, 0.5307]（> 0.25）；"
         "在无退化方向的格点上 ∈ {0.0779, 0.1839}（< 0.25）**」；**物理宇宙对应「无退化」一组**（格点尺寸 ≫ 2）"
         "⟹ **本条不得读作「面积律不成立」**（与本块上文第 51 轮「(4,4,4) 的 0.1839 是**满足**」一致）。\n"
         "> 📌 **方法论**：**引用 H/N 数值必须同时给出「退化方向数」**（15 个算例按此二分、两组完全分离，"
         "空隙 (0.2834, 0.4334)）；仅报 `H/N` 而不报形状，会得出**方向相反**的结论。")
sub_once(ZH, Z_OLD, Z_NEW, "ZH C-39（第 78 轮块结论 ④）")

# ================================================================
# ② C-40：ZH 第 48 轮块「0.25 落在空隙里」
# ================================================================
print("\n[ZH-2] C-40：第 48 轮「0.25 落在空隙里」")
sub_once(ZH, "**两组完全分离、0.25 落在空隙里**（机理：长度 2 的环只有一种完美匹配",
         "**两组完全分离**；⚠️ ~~0.25 落在空隙里~~ —— **第 86 轮更正（C-40）**：两组间的空隙是 "
         "**(0.2834, 0.4334)**，而 **0.25 < 0.2834** ⟹ **0.25 不在空隙里，而在「≤ 1 个」这一组的内部**"
         "（真正的位置是「跨组内跨点」：(2,4,4) = 0.2834 **>** 0.25 **>** (2,4,6) = 0.2208，即 **N ∈ (32, 48)**，"
         "第 49 轮已给出）（机理：长度 2 的环只有一种完美匹配",
         "ZH C-40（第 48 轮「空隙」）")

# ================================================================
# ③ 块链末加【第 86 轮】审计块（插在第 79 轮块之后 —— 即 §4.8 块链末尾之前）
# ================================================================
print("\n[ZH-3] §4.8 加【第 86 轮】审计块")
# 锚：第 79 轮块的末行（C-30 那条）之后
t = io.open(ZH, encoding="utf-8").read()
L = t.split("\n")
i79 = next((k for k, s in enumerate(L) if "【v2.9 补充（第 79 轮" in s), None)
print("  第 79 轮块起始行：", (i79 + 1) if i79 is not None else "未找到")
# 找该块末行（下一个不以 '>' 开头的非空行之前）
j = i79
while j + 1 < len(L) and L[j + 1].lstrip().startswith(">"):
    j += 1
print("  第 79 轮块末行：", j + 1, "|", L[j].strip()[:120])
BLOCK = """> **【v2.9 审计（第 86 轮：**形状口径**的全链审计 —— 找出「后期把早期对的结论写错」的一处）】** 本轮是**审计轮**（脚本 `_shape_audit_86.py`，**SA-1 … SA-8，8 项 0 失败**），**不新增任何物理内容**。
>
> · **主发现（正是第 84/85 轮教训的镜像）**：**第 78 轮块**（本链下方）的结论 ④ 用 **(2,2,L) 细长格点**的数据，推翻了**第 48 / 51 轮用 GAP 算出的**「**(4,4,4) = 0.1839 满足 0.25**」⟹ **后期的一轮把早期正确的结论又写反了**。已就地更正为 **C-39**（带形状口径）。
> · ⭐ **机制（本轮补齐）**：「**退化方向**」= **线长为 2 的方向**（唯一使两种完美匹配重合 ⟹ **σ_j = 恒等** ⟹ 该方向无相位自由度）。**这是组合事实，不是归纳**（L = 2/4/6/8 逐项验证：只有 L = 2 重合）。
> · ⭐ **全表核对（15 个算例）**：按退化方向数二分，**两组完全分离** ——
>   **≥ 2 个**：`0.4679 / 0.4335 / 0.4334 / 0.4617 / 0.4802 / 0.5041 / 0.5307`（N = 8…64）；
>   **≤ 1 个**：`0.0779 / 0.1338 / 0.1571 / 0.1652 / 0.1802 / 0.1839 / 0.2208 / 0.2834`。
>   ⟹ **H/N 的主控变量是「退化方向数」（数值格点的伪影程度），不是 N**。
> · ⭐ **无退化算例只有两个**：(4,4,4) N=64 ⟹ **0.1839**、(6,6,6) N=216 ⟹ **0.0779**，**都 < 0.25** ⟹ **面积律在「物理上对应」的那一组里是被满足的**。
> · ⚠️ **C-40（顺带更正）**：第 48 轮块写「0.25 **落在空隙里**」—— 两组空隙是 **(0.2834, 0.4334)**，而 **0.25 < 0.2834** ⟹ 0.25 **不在空隙里**，而在「≤ 1 个」组的**内部**（跨点 N ∈ (32, 48)，第 49 轮已给出）。已就地更正。
> · ✅ **第 80 轮的「不覆盖」登记不需要撤回**：其四条依据（无等式 / 无机制 / 不可证伪 / 判据适用域）**没有一条**引用 `H/N ≈ 0.433` ⟹ 结论「框架不覆盖这条链」**仍然成立**。⚠️ 但登记块里「第 46–52 轮**七轮全部负面**」的措辞需精确化：第 48 / 49 轮给出的 **H/N < 0.25** 是**正面事实**（虽只是「不违反」，不等于「推出面积律」）。
> · 📌 **规范（已入技能陷阱 78）**：**报 `H/N` 必须同时报「退化方向数」**；且**审计「某结论是否被后期写错」时，要按「同一量的全部算例」列表核对，而不是只读最后一条结论句**。"""

L2 = L[:j + 1] + ["", BLOCK, ""] + L[j + 1:]
io.open(ZH, "w", encoding="utf-8").write("\n".join(L2))
print("  [OK] ZH §4.8 已插入【第 86 轮】审计块（{} 行）".format(len(BLOCK.split("\n"))))

# ================================================================
# ④ EN 侧
# ================================================================
print("\n[EN-1] C-39：EN 第 78 轮块 'Four unchanged conclusions'")
E_OLD = ("> · **Four unchanged conclusions**: ① the incompleteness ratio **grows monotonically with N** (under both groups); "
         "② the (Z₂)³ invariant fails immediately for N ≥ 16; ③ the \"14 = 14\" at N = 8 is **accidental** (invariant degenerates, "
         "and this is **generator-independent**); ④ **H/N nearly saturates between N=16 and 24** (0.4335 → 0.4334) and "
         "≈ 0.433 ≫ 0.25 ⟹ **the area law does not hold on any computable lattice**.")
E_NEW = ("> · **Four unchanged conclusions**: ① the incompleteness ratio **grows monotonically with N** (under both groups); "
         "② the (Z₂)³ invariant fails immediately for N ≥ 16; ③ the \"14 = 14\" at N = 8 is **accidental** (invariant degenerates, "
         "and this is **generator-independent**); ④ **H/N nearly saturates between N=16 and 24** (0.4335 → 0.4334) "
         "~~and ≈ 0.433 ≫ 0.25 ⟹ **the area law does not hold on any computable lattice**~~.\n"
         "> ⚠️ ⭐ **【Round-86 correction (C-39): missing shape caliber ＋ the conclusion points the wrong way】** The struck-out sentence has two defects:\n"
         "> · **(a) no shape caliber**: those two numbers come only from the **(2,2,L) family** (which has **2 directions of length 2**) — "
         "a cycle of length 2 has only **one** perfect matching, so such a direction has **σ_j = identity and carries no phase freedom** "
         "(round 48's mechanism). The (2,2,L) family is therefore the **most degenerate** one, and `0.433` **does not represent a generic lattice**;\n"
         "> · **(b) the conclusion is reversed**: the **non-degenerate** cases (0 directions of length 2) — **(4,4,4) = 0.1839** and "
         "**(6,6,6) = 0.0779** — are **both < 0.25 ⟹ the area law holds on those two lattices** (already computed in rounds 48 / 49, see the two blocks above).\n"
         "> ⟹ **Correct statement**: \"**H/N ∈ [0.4334, 0.5307] (> 0.25) on elongated lattices with ≥ 2 degenerate directions, and "
         "H/N ∈ {0.0779, 0.1839} (< 0.25) on lattices with no degenerate direction**\"; **the physical universe corresponds to the non-degenerate group** "
         "(lattice size ≫ 2) ⟹ **this item must not be read as \"the area law fails\"** (consistent with round 51's \"the 0.1839 of (4,4,4) is **satisfied**\" above).\n"
         "> 📌 **Methodology**: **quoting an H/N value requires quoting the \"number of degenerate directions\" alongside it** (the 15 cases split into two completely "
         "separated groups under this classification, with a gap of (0.2834, 0.4334)); reporting `H/N` without the shape can yield a conclusion of the **opposite sign**.")
sub_once(EN, E_OLD, E_NEW, "EN C-39")

print("\n[EN-2] C-40：EN 第 48 轮 '0.25 falls in the gap'")
sub_once(EN, "**the two groups are completely separated and 0.25 falls in the gap** (mechanism: a cycle of length 2 has only one perfect matching",
         "**the two groups are completely separated**; ⚠️ ~~0.25 falls in the gap~~ — **round-86 correction (C-40)**: the gap between the two groups is "
         "**(0.2834, 0.4334)** and **0.25 < 0.2834** ⟹ **0.25 is *not* in the gap but *inside* the \"≤ 1\" group** (its actual position is a "
         "**within-group crossing**: (2,4,4) = 0.2834 **>** 0.25 **>** (2,4,6) = 0.2208, i.e. **N ∈ (32, 48)**, given in round 49) "
         "(mechanism: a cycle of length 2 has only one perfect match",
         "EN C-40")

print("\n[EN-3] §4.8 加第 86 轮审计块")
tE = io.open(EN, encoding="utf-8").read()
LE = tE.split("\n")
i79e = next((k for k, s in enumerate(LE) if "(round 79:" in s), None)
print("  EN 第 79 轮块起始行：", (i79e + 1) if i79e is not None else "未找到")
if i79e is not None:
    j = i79e
    while j + 1 < len(LE) and LE[j + 1].lstrip().startswith(">"):
        j += 1
    print("  第 79 轮块末行：", j + 1, "|", LE[j].strip()[:120])
    EBLOCK = """> **【v2.9 audit (round 86: a full-chain audit of the **shape caliber** — locating the one place where a later round re-broke an earlier correct conclusion)】** This round is an **audit round** (script `_shape_audit_86.py`, **SA-1 … SA-8, 8 items, 0 failures**) and adds **no new physics**.
>
> · **Main finding (the mirror image of the round-84/85 lesson)**: the **round-78 block** below used data from the **(2,2,L) elongated lattices** to overturn the **GAP-computed result of rounds 48 / 51** — "**(4,4,4) = 0.1839 satisfies 0.25**" ⟹ **a later round wrote an earlier correct conclusion backwards**. Corrected in place as **C-39** (with the shape caliber restored).
> · ⭐ **Mechanism (supplied this round)**: a **"degenerate direction"** is a direction of **length 2** (the only length for which the two perfect matchings coincide ⟹ **σ_j = identity** ⟹ no phase freedom). **This is a combinatorial fact, not an induction** (verified item by item for L = 2/4/6/8: only L = 2 coincides).
> · ⭐ **Full-table check (15 cases)**: split by the number of degenerate directions, the **two groups are completely separated** —
>   **≥ 2**: `0.4679 / 0.4335 / 0.4334 / 0.4617 / 0.4802 / 0.5041 / 0.5307` (N = 8…64);
>   **≤ 1**: `0.0779 / 0.1338 / 0.1571 / 0.1652 / 0.1802 / 0.1839 / 0.2208 / 0.2834`.
>   ⟹ **the controlling variable of H/N is the "number of degenerate directions" (i.e. how much numerical artefact the lattice carries), not N**.
> · ⭐ **Only two non-degenerate cases exist**: (4,4,4) N=64 ⟹ **0.1839**, (6,6,6) N=216 ⟹ **0.0779**, **both < 0.25** ⟹ **the area law *is* satisfied in the group that physically corresponds to the universe**.
> · ⚠️ **C-40 (corrected in passing)**: the round-48 block says "0.25 **falls in the gap**" — the gap is **(0.2834, 0.4334)** and **0.25 < 0.2834** ⟹ 0.25 is **not** in the gap but **inside** the "≤ 1" group (crossing at N ∈ (32, 48), given in round 49). Corrected in place.
> · ✅ **The round-80 "NOT COVERED" registration needs no retraction**: none of its four grounds (no equation / no mechanism / unfalsifiable / limited domain) **quotes `H/N ≈ 0.433`** ⟹ the conclusion "the framework does not cover this chain" **still stands**. ⚠️ But the phrase "**all seven rounds (46–52) plus the recomputations of rounds 78–80 are negative**" needs qualification: the **H/N < 0.25 obtained in rounds 48 / 49** is a **positive fact** (though only "not violated", not a derivation of the area law).
> · 📌 **Norm (now skill trap 78)**: **reporting `H/N` requires reporting the "number of degenerate directions"**; and **auditing "was a conclusion re-broken later?" requires tabulating *all* cases of the same quantity, not just reading the last conclusion sentence**. """
    LE2 = LE[:j + 1] + ["", EBLOCK, ""] + LE[j + 1:]
    io.open(EN, "w", encoding="utf-8").write("\n".join(LE2))
    print("  [OK] EN §4.8 已插入第 86 轮审计块（{} 行）".format(len(EBLOCK.split("\n"))))

print("\n失败项：{}".format(BAD if BAD else "无 ✓"))
if BAD:
    sys.exit(1)
