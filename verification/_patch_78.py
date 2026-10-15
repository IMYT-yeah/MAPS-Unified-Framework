# -*- coding: utf-8 -*-
"""第 78 轮论文补丁（中英同步 6 项）：5.93 → 6.03 ＋ 标注 3.1 已做 ＋ §4.8 块链末插【第 78 轮】块"""
import io, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(ROOT, "MAPS-Unified-Framework", "paper", "history")
TAG = "2026-10-02第78轮前"

for p in (ZH, EN):
    b = os.path.join(HIST, os.path.basename(p).replace(".md", "_备份_{}.md".format(TAG)))
    shutil.copy2(p, b)
    print("  [BK] {}".format(os.path.basename(b)))


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<36} 命中 {} 次 —— 拒绝".format(tag, n))
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<36} 已改".format(tag))


# ── 1. ZH 第 46 轮块：5.93 → 6.03 ────────────────────────
ZH_A = "> · **副产品**：不完备度（轨道数/等值集数）= 1.00 ⟶ 1.63 ⟶ **5.93**，随 N 增长 ⟹ 该比值本身可能是有结构的量，已列入候选池。"
ZH_A_NEW = ("> · **副产品**：不完备度（轨道数/等值集数）= 1.00 ⟶ 1.63 ⟶ ~~5.93~~ **6.03**"
            "（⚠️ **第 78 轮更正 C-26**：原 5.93 是用**未更正的生成元**（纯平移）算的；用 `_tickgroup.gens_correct` 重算，"
            "N=24 的轨道数 6224 → **6334** ⟹ 不完备度 5.928 → **6.032**。趋势不变：随 N 单调增长），"
            "随 N 增长 ⟹ 该比值本身可能是有结构的量，已列入候选池。")
sub_once(ZH, ZH_A, ZH_A_NEW, "ZH 第 46 轮块 5.93→6.03")

# ── 2. ZH 第 51 轮块：标 ✅ 3.1 已做 ──────────────────────
ZH_B = "③ 便宜项：不完备度比值（1.00→1.63→5.93）用更正后的群重算。"
ZH_B_NEW = "③ ~~便宜项：不完备度比值（1.00→1.63→5.93）用更正后的群重算。~~ **✅ 已完成（第 78 轮，工作流 3.1）**：只有 N=24 改变（5.93 → **6.03**，轨道 6224 → 6334），趋势与结论不变。"
sub_once(ZH, ZH_B, ZH_B_NEW, "ZH 第 51 轮块 标 ✅")

# ── 3. ZH §4.8 块链末插【第 78 轮】块 ────────────────────
ZH_ANCHOR = "> 🔧 **下一步（收口）**：这条（B5 ↔ 衬底）链路**到此收口**。"
ZH_BLOCK = """
---

> **【v2.9 补充（第 78 轮：工作流 3.1 —— 不完备度比值用更正后的群重算）】** 本轮是**复算 ＋ 正对照 ＋ 更正**（脚本 `_incompleteness_78.py`，**UB-1 … UB-12，11 项 0 失败**）。
>
> · ⭐ **结论：只有 N = 24 改变，趋势与结论完全不变**。第 46 轮的 `_orbit_k_half.py` 里「移 2」写的是 `coords[(i+2)%L]` —— 那是**纯平移**，正是本框架早已记下的陷阱（σ_j = 「**偶位 +2、奇位 −2**」，**不是**全体 +2；两者在 **L ≤ 4 时逐元素相同**、**L ≥ 6 才分叉**）。实测：(2,2,2) 与 (2,2,4) 的两套生成元**逐元素完全相同**（(2,2,4) 上两群作为集合完全相等，128 个元素逐一比对）；(2,2,6) 有 **4 个生成元不同**，且**两群同为 648 阶** —— 再次印证「**阶相同 ≠ 群相同**」。
>
> · **重算表**（k = N/2 单层，构型等权；**先用旧群复现第 46 轮的值作正对照**）：
>
> | 格点 | N | 轨道数（旧 → 新） | 等值集数 | **不完备度** | H/N |
> |---|---|---|---|---|---|
> | (2,2,2) | 8 | 14 → **14** | 14 | 1.000 → 1.000 | 0.467874 → 0.467874 |
> | (2,2,4) | 16 | 253 → **253** | 155 | 1.632 → 1.632 | 0.433480 → 0.433480 |
> | **(2,2,6)** | 24 | **6224 → 6334** | 1050 | **5.928 → 6.032** | 0.432986 → **0.433438** |
>
> · **等值集数完全不变**（14 / 155 / 1050）—— 符合预期：等值集只由**不变量**（(Z₂)³ 奇偶类计数向量 + 平移规范形式）决定，**与生成元无关** ⟹ 这是一条**内部一致性检验**：若它变了，说明轨道实现有问题。
> · ⭐ **H/N 新值 0.433438 = 0.4334** —— 与本节第 50 轮已更正的 **0.4334 完全一致** ⟹ 这是对第 50 轮的一次**独立复算验证**。
> · **不变的四条结论**：① 不完备度**随 N 单调增长**（两套群下都成立）；② (Z₂)³ 不变量在 N ≥ 16 立即不完备；③ N = 8 的「14 = 14」是**偶然**（不变量退化，且**与生成元无关**）；④ **H/N 在 N=16 → 24 几乎饱和**（0.4335 → 0.4334）且 ≈ 0.433 ≫ 0.25 ⟹ **面积律在能算的格点上不成立**。
>
> · ⚠️ ⭐ **C-26（本轮顺带查出：论文内部不一致 —— 一次「半改」）**：第 50 轮的更正把**轨道数 6224 → 6334** 与 **H/N 0.4330 → 0.4334** 都改了（本节上文），**却漏改了同一份记录里的「5.93」** —— 而 5.93 正是用**未更正的 6224** 算的 ⟹ **同一段文字里两个数来自不同的群**。本轮已就地更正（5.93 → 6.03，保留删除线留痕）。⟹ **教训**：一次更正若只改它直接面对的那几个数，**必须扫同一处的派生量**（这里是「轨道数 / 等值集数」的比值）。
> · ⚠️ **C-27（实现层）**：第 46 轮脚本 `_orbit_k_half.py::reduced_generators` 的「移 2」是**纯平移**（本框架技能陷阱 27 的命中）。第 48 轮已查明并写了 `gens_buggy` / `gens_correct` 对照，但**第 46 轮的产物（含 5.93）当时未被回溯更正**。
>
> ⚠️ **四条诚实边界**：① 只算了 **(2,2,L)** 系列（L = 2 / 4 / 6）—— 第 46 轮的「细长格点」限制**依然有效**，结论**不外推**到各向同性三维格点；② 层口径 = **k = N/2 单层**（与第 46 轮同口径，与第 40 轮的全空间 2^N 不同）；③ H/N 用**构型等权**；④ N = 24 是 **C(24,12) = 2,704,156 个构型的全枚举**（非采样）⟹ 精确值。
"""
txt = io.open(ZH, encoding="utf-8").read()
i = txt.find(ZH_ANCHOR)
if i < 0:
    print("  [XX] ZH §4.8 锚点未找到")
else:
    j = txt.find("\n", i)
    txt = txt[:j + 1] + ZH_BLOCK + txt[j + 1:]
    io.open(ZH, "w", encoding="utf-8").write(txt)
    print("  [OK] {:<36} 已插块".format("ZH §4.8 【第 78 轮】块"))

# ── 4. EN 第 46 轮块：5.93 → 6.03 ────────────────────────
EN_A = "> · **By-product**: the incompleteness ratio (#orbits / #level sets) = 1.00 ⟶ 1.63 ⟶ **5.93** grows with N ⟹ this ratio may itself be a structured quantity; it has been added to the candidate pool."
EN_A_NEW = ("> · **By-product**: the incompleteness ratio (#orbits / #level sets) = 1.00 ⟶ 1.63 ⟶ ~~5.93~~ **6.03**"
            " (⚠️ **round-78 correction C-26**: the old 5.93 was computed with the **uncorrected generators** (pure translation); recomputing with "
            "`_tickgroup.gens_correct` gives 6224 → **6334** orbits at N=24 ⟹ 5.928 → **6.032**. The trend is unchanged: it grows with N), "
            "grows with N ⟹ this ratio may itself be a structured quantity; it has been added to the candidate pool.")
sub_once(EN, EN_A, EN_A_NEW, "EN round-46 block 5.93→6.03")

# ── 5. EN 第 51 轮块：标 ✅ ──────────────────────────────
EN_B = "③ cheap item: recompute the incompleteness ratio (1.00→1.63→5.93) with the corrected group."
EN_B_NEW = "③ ~~cheap item: recompute the incompleteness ratio (1.00→1.63→5.93) with the corrected group.~~ **✅ done (round 78, workflow item 3.1)**: only N=24 changes (5.93 → **6.03**; 6224 → 6334 orbits), trend and conclusions unchanged."
sub_once(EN, EN_B, EN_B_NEW, "EN round-51 block ✅")

# ── 6. EN §4.8 块链末插块 ────────────────────────────────
EN_ANCHOR = "> 🔧 **Next (closure)**: the (B5 ↔ substrate) chain **closes here**."
EN_BLOCK = """
---

> **【v2.9 supplement (round 78: workflow item 3.1 — recomputing the incompleteness ratio with the corrected group)】** This round is a **recomputation + positive control + correction** (script `_incompleteness_78.py`, **UB-1 … UB-12, 11 items, 0 failures**).
>
> · ⭐ **Verdict: only N = 24 changes; trend and conclusions are completely unchanged.** The "shift by 2" in round 46's `_orbit_k_half.py` was written as `coords[(i+2)%L]` — a **pure translation**, which is precisely the trap this project had already recorded (σ_j = "**even sites +2, odd sites −2**", **not** a uniform +2; the two coincide **element-wise for L ≤ 4** and only **diverge at L ≥ 6**). Measured: (2,2,2) and (2,2,4) have **element-wise identical** generator sets (at (2,2,4) the two groups are equal **as sets**, all 128 elements compared); (2,2,6) has **4 differing generators**, and the two groups **share the same order 648** — again confirming "**same order ≠ same group**".
>
> · **Recomputation table** (k = N/2 layer, configuration-equal-weight; **the old group is run first to reproduce round 46 as a positive control**):
>
> | Lattice | N | #orbits (old → new) | #level sets | **incompleteness ratio** | H/N |
> |---|---|---|---|---|---|
> | (2,2,2) | 8 | 14 → **14** | 14 | 1.000 → 1.000 | 0.467874 → 0.467874 |
> | (2,2,4) | 16 | 253 → **253** | 155 | 1.632 → 1.632 | 0.433480 → 0.433480 |
> | **(2,2,6)** | 24 | **6224 → 6334** | 1050 | **5.928 → 6.032** | 0.432986 → **0.433438** |
>
> · **The number of level sets is completely unchanged** (14 / 155 / 1050) — as expected: level sets depend only on the **invariant** ((Z₂)³ parity-class counting vector + translation-normal form), **not on the generators** ⟹ this is an **internal consistency check**: had it changed, the orbit implementation would be at fault.
> · ⭐ **The new H/N = 0.433438 = 0.4334** — **exactly matching** the 0.4334 already corrected above in round 50 ⟹ this is an independent recomputation verifying round 50.
> · **Four unchanged conclusions**: ① the incompleteness ratio **grows monotonically with N** (under both groups); ② the (Z₂)³ invariant fails immediately for N ≥ 16; ③ the "14 = 14" at N = 8 is **accidental** (invariant degenerates, and this is **generator-independent**); ④ **H/N nearly saturates between N=16 and 24** (0.4335 → 0.4334) and ≈ 0.433 ≫ 0.25 ⟹ **the area law does not hold on any computable lattice**.
>
> · ⚠️ ⭐ **C-26 (found in passing: an internal inconsistency — a "half-edit")**: round 50's correction updated **#orbits 6224 → 6334** and **H/N 0.4330 → 0.4334** above, **but missed the "5.93" in the same record** — and 5.93 was computed from the **uncorrected 6224** ⟹ **two numbers in the same passage come from different groups**. Corrected in place here (5.93 → 6.03, with strike-through retained). ⟹ **Lesson**: a correction that touches only the numbers it directly faces **must sweep the derived quantities of the same passage** (here: the ratio of #orbits to #level sets).
> · ⚠️ **C-27 (implementation)**: the "shift by 2" in round 46's `_orbit_k_half.py::reduced_generators` is a **pure translation** (a hit on this project's trap 27). Round 48 identified it and introduced the `gens_buggy` / `gens_correct` comparison, but round 46's outputs (including 5.93) were **never retro-corrected**.
>
> ⚠️ **Four honesty boundaries**: ① only the **(2,2,L)** series was computed (L = 2 / 4 / 6) — round 46's "slender lattice" restriction **still applies** and the conclusions are **not extrapolated** to isotropic 3D lattices; ② the layer caliber is **k = N/2** (same as round 46; different from round 40's full-space 2^N); ③ H/N uses **configuration-equal weight**; ④ N = 24 is a **full enumeration of C(24,12) = 2,704,156 configurations** (not sampled) ⟹ exact.
"""
txt = io.open(EN, encoding="utf-8").read()
i = txt.find(EN_ANCHOR)
if i < 0:
    print("  [XX] EN §4.8 锚点未找到")
else:
    j = txt.find("\n", i)
    txt = txt[:j + 1] + EN_BLOCK + txt[j + 1:]
    io.open(EN, "w", encoding="utf-8").write(txt)
    print("  [OK] {:<36} 已插块".format("EN §4.8 round-78 block"))

# ── 自查 ─────────────────────────────────────────────────
print()
for p, nm in ((ZH, "ZH"), (EN, "EN")):
    L = io.open(p, encoding="utf-8").read().split("\n")
    bad_pipe = sum(1 for s in L if "\\|" in s and not s.lstrip().startswith("|"))
    frag = [i + 1 for i, s in enumerate(L) if s.strip().startswith(("，", ","))]
    print("  {} 行数 {}；非表格反斜杠竖线 {}；残片行 {}".format(nm, len(L), bad_pipe, frag))
print("  ZH「第 78 轮」=", io.open(ZH, encoding="utf-8").read().count("第 78 轮"))
print("  EN「round 78」=", io.open(EN, encoding="utf-8").read().count("round 78"))
print("  ZH「6.03」=", io.open(ZH, encoding="utf-8").read().count("6.03"))
print("  EN「6.03」=", io.open(EN, encoding="utf-8").read().count("6.03"))
