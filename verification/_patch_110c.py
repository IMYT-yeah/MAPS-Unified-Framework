# -*- coding: utf-8 -*-
"""第 110 轮补丁 c：重写英文注（上一版用了 ASCII 箭头 -> 与 ==>，与 EN 稿的 ⟹ 风格不一致）"""
import io, os

BASE = r"C:\Users\Administrator\Desktop\2026-08-20-21-43-34"
EN = os.path.join(BASE, "outputs", "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

NEW = [
    "> **【v2.9 caliber note (round 110: G9-2 closed — the \"invert for q\" table is a consistency construction, not a derivation)】** The series above",
    "> (q = 2 → 3.000, q = 3 → 3.585, q = 4 → 4.000, q = 5 → 4.322 bits) is **identically `2 + log2(q)`**",
    "> (to 3 decimals) ⟹ `bits(q) = log2(4q)` is merely a **rewriting** of \"`k·q = 16` with k = 4\".",
    "> ⟹ The \"**unique**\" in \"q = 4 → 4.000 (**unique**)\" comes **only from the strict monotonicity of the logarithm**",
    "> (the equation `2 + log2(q) = 4` has the unique real root q = 4) and **carries no selection information**;",
    "> it presupposes that **both k = 4 (§4.9 Lemma 1) and 16 (B5) are given inputs**.",
    "> ⚠️ **Moreover**: the constraint `k·q = 16` is **not unique by itself** — it has **five** integer solutions",
    "> `(k, q) = (1, 16) / (2, 8) / (4, 4) / (8, 2) / (16, 1)`; it only excludes **non-divisor** k (e.g. the",
    "> exterior coordination k = 6). The **only** genuine uniqueness in this chain comes from **reading B2**,",
    "> `2^k = 16 ⟹ k = 4` (`2^k` is injective in k), and that route **does not pass through q at all**.",
    "> ⟹ **Conclusion (G9-2 closed)**: the framework **has no** derivation of \"why exactly four states\",",
    "> and **no longer needs one** — under the current reading B2 the \"four states\" are no longer a framework",
    "> ingredient (raw configurations = 4 in-plane connections × ± branch ⟹ 2⁴ = 16), with \"vacuum /",
    "> annihilating\" **not entering the entropy count** (round-32 C-b / C-c) and \"vacuum\" fixed in round 20",
    "> as a **logical state** (no quantum ⟹ no site) ⟹ \"exactly four states\" is an **internal artifact of",
    "> reading A** and exits together with the round-32 verdict. The honest caveat in this section",
    "> (\"the dynamical uniqueness of 4\" lies at the **framework-assumption** level) is the **current**",
    "> statement and is **not modified**.",
]

lines = io.open(EN, encoding="utf-8").read().split("\n")
idx = [i for i, s in enumerate(lines) if "v2.9 caliber note (round 110" in s]
print("锚点命中 " + str(len(idx)) + " 次")
if len(idx) != 1:
    print("  [XX] 拒绝")
else:
    i = idx[0]
    ends = [k for k in range(i, i + 30) if "not modified" in lines[k]]
    assert len(ends) == 1, ends
    j = ends[0]
    old = lines[i:j + 1]
    print("  旧块行数 = " + str(len(old)) + "（应当 = 18）")
    assert len(old) == 18, len(old)
    lines[i:j + 1] = NEW
    io.open(EN, "w", encoding="utf-8").write("\n".join(lines))
    print("  [OK] 英文注已重写（行 " + str(i + 1) + " 起 " + str(len(NEW)) + " 行）")
