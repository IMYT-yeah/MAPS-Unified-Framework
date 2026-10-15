# -*- coding: utf-8 -*-
"""第 85 轮补丁 · EN 侧（与 ZH 侧一一对应）"""
import io
import os

BASE = "C:/Users/Administrator/Desktop/2026-08-20-21-43-34"
EN = os.path.join(BASE, "outputs", "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
BAD = []


def sub_once(path, old, new, tag, n=1):
    t = io.open(path, encoding="utf-8").read()
    c = t.count(old)
    if c != n:
        print("  [XX] {:<42} 命中 {}（期望 {}）".format(tag, c, n))
        BAD.append(tag)
        return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, n))
    print("  [OK] {:<42} 已改".format(tag))


# ================================================================
print("[EN-1] §8.6.8: append the Round-85 correction note (C-37)")
E_A = 'The rank of "coordination number 6 ⟹ simple cubic" is 【**verdict (one of two readings)**】, not 【theorem】.'
E_A_NEW = E_A + """

> **【Round-85 correction note (C-37): two over-corrections of the round-84 note are withdrawn — the audit missed the memo family】** ⚠️ The round-84 note above was produced by reading **the paper only**, **without the memos** ⟹ two of its conclusions were **too harsh** and are now corrected:
>
> **① The charge against item (i) is withdrawn.** Round 84 wrote "③ the 'discriminator' language in (i) turns a **matching** into a **discrimination**" — **that charge does not hold**. Item (i) is an **exact enumeration** (round-31 RC-5; the memo reads: "exact enumeration — the extremum must occur in a plane spanned by some pair of directions, so it suffices to enumerate direction **pairs**, **no sampling needed**"): the **maximum number of coplanar directions** is **4** (normal = the out-of-plane axis) for simple cubic / octahedral **✅ passes**, and **2** for diamond / regular tetrahedron **❌ fails** (the 4 tetrahedral directions are **non-coplanar**, any plane holds at most 2). ⟹ This is a **mathematical argument** (necessary condition plus exhaustive enumeration) and **is formally valid**. The only correct qualification concerns its **premise**: it relies on Lemma 1's "4 + 2" requirement, and Lemma 1 is a 【framework assumption】 ⟹ **it is not a ground independent of Lemma 1** (as the honest-limits table already states).
>
> **② The "two equal readings" characterisation and the "restoration of the round-27 reading" are withdrawn.** Round 84 wrote "this is not 'round 27 got it wrong' but **a contest between two readings**" and on that basis **restored** the standing of reading I — **an over-correction**. What the memo family records is:
> · **Round 27 itself flagged the gap** (`格点几何_四邻居加二分…md`): the honest-limits table says the candidate screening "depends on the step **'surface plaquette 4 neighbours = bulk coordination number 4'** … **their being the same source requires an additional argument**"; and step 1 of "next steps" reads: "**bridge 'surface 4 neighbours ↔ bulk coordination number 4': this is the only external step on which this round's conclusion depends**";
> · **Round 28 FC-7(a) performed exactly this rank audit** (`四色定理辨析…md`): "last round I used 'surface plaquette 4 neighbours' as the support for 'bulk coordination number = 4'. **On tracing the source, that does not hold**" — because it is in fact **§4.9 Lemma 1's 2D in-plane count** (2 axes × 2 directions inside the observer's plane), **not the bulk coordination number**; the support was changed to §4.10 Theorems 1+2 (rigorous) ⟹ "**the conclusion still holds, but the support has been replaced by a stricter one (a theorem rather than an assumption)**". ⚠️ **But the replacement still contains an external step: "if every direction corresponds to one bond"**;
> · **Round 30 judged that external step still unbridged** (the direction cluster belongs to the **interior / information** layer and does not fix the geometric coordination number) ⟹ **the diamond was withdrawn**.
> ⟹ **Accurate statement**: **round 27 never claimed that step was proved**; round 30 is "**that external step was never bridged**", **not "a choice between two equal readings"**.
>
> **③ Round 38's UQ-5 is added back as a consistency check (not an independent ground)**: the non-self-dual **honeycomb** lattice gives a **counting discrepancy** (reading 1 = 3 connections/plaquette vs reading 2 = 6) ⟹ "the two plaquette readings coincide on the square lattice" is **not a coincidence**; ⚠️ but that item **depends on the T-6 verdict** (the memo reads: "self-duality is the deciding factor, and **it depends on the simple cubic of the T-6 verdict**") ⟹ it is a **self-consistency check**, **not an independent ground** (round 84 treating it as a "fourth ground" was likewise too broad).
>
> ⭐ **The precise rank of the conclusion**: "**coordination number 6 ⟹ simple cubic**" = 【**the unique self-consistent solution under Lemma 1 (an assumption) plus the geometric enumerations**】 — **not a 【theorem】** (because Lemma 1 is an assumption), **but also not "either of two equal readings"** (because the external step required by the other reading was never bridged).
> ⭐ **The hard reason why "the diamond fails" still stands** (retained from round 84): §4.8's 4 encoding connections are **coplanar** whereas the diamond's tetrahedral bonds are **non-coplanar** ⟹ **coplanarity is what fails**.
> ⚠️ **The round-84 lesson (now skill trap 77)**: **the audit surface must include the memo family** — the paper contains **no trace** of round 28's FC-7(a), of round 38's UQ-5, or of round 27's self-flagged gap (`external step` appears **0 times** in the paper)."""
sub_once(EN, E_A, E_A_NEW, "EN Round-85 note")

# ================================================================
print("\n[EN-2] honest-limits table: correct the two round-84 rows")
E_B = '| **"three independent grounds" (T-6)** | ⚠️ **Round-84 correction (C-36)**: none of the three is an independent mathematical theorem (Argument 4 = 【structural argument】 / Lemma 1 = 【framework assumption】); the genuinely hard grounds are the §4.8 counting constraints `k·q = 16` and `2^k = 16` ⟹ "coordination number 6 ⟹ simple cubic" should be labelled 【verdict (one of two readings)】, not 【theorem】 |'
E_B_NEW = '| **"three independent grounds" (T-6)** | ⚠️ Round 84 labelled it 【verdict (one of two readings)】; **round 85 corrects this again (C-37)** ⟹ precise rank = 【**the unique self-consistent solution under Lemma 1 (an assumption) + the geometric enumerations**】: Argument 4 = 【structural argument】 / Lemma 1 = 【framework assumption】 / **(i) is an exact enumeration (mathematics, formally valid, premise depends on Lemma 1)**; plus round 38\'s UQ-5 **consistency check** (depends on T-6, not an independent ground). **Not a 【theorem】, but also not "either of two equal readings"** |'
sub_once(EN, E_B, E_B_NEW, "EN honest-limits row 1")

E_C = '| **the round-27 reading (direction cluster = exterior bond directions ⟹ diamond)** | ⚠️ **Restored in round 84**: that inference is **self-consistent** under its reading and **was not a mistake**; the framework adopts the layered reading instead. **The hard reason "the diamond fails" is coplanarity** (§4.8\'s 4 encoding connections are **coplanar**, whereas diamond bonds are **non-coplanar** tetrahedral directions) |'
if E_C not in io.open(EN, encoding="utf-8").read():
    # 兼容：可能是不同的引号
    t = io.open(EN, encoding="utf-8").read()
    k = t.find("| **the round-27 reading")
    print("  实际行：", repr(t[k:k + 400]))
    BAD.append("EN honest-limits row 2（锚点不符）")
else:
    E_C_NEW = '| **the round-27 reading (direction cluster = exterior bond directions ⟹ diamond)** | ⚠️ **Round-85 correction (C-37): the round-84 "restoration" is withdrawn.** Round 27 **itself** flagged "this is the only **external step** on which this round\'s conclusion depends"; round 28 FC-7(a) **audited it and found that support does not hold** ("surface 4 neighbours" is in fact Lemma 1\'s 2D in-plane count); round 30 judged that external step **still unbridged** ⟹ withdrawn. **The hard reason why "the diamond fails" is coplanarity** (§4.8\'s 4 encoding connections are **coplanar**, whereas diamond bonds are **non-coplanar** tetrahedral directions) |'
    sub_once(EN, E_C, E_C_NEW, "EN honest-limits row 2")

# ================================================================
print("\n[EN-3] §8.6.8: add the round-27/28 gap record (0 occurrences in the paper before)")
E_D = "**(a) Hard constraints (retained)**: all nearest-neighbour transpositions within one tick form a **perfect matching** (every vertex covered exactly once)."
E_D_NEW = """**(a′) 【Added in round 85: the "external step" self-flagged by round 27, and round 28's audit】** When round 27 fixed the diamond it **flagged its own sole dependency**: the memo states that the candidate screening "depends on the step **'surface plaquette 4 neighbours = bulk coordination number 4'** … **their being the same source requires an additional argument**", and lists "**bridge 'surface 4 neighbours ↔ bulk coordination number 4'**" as step 1 of the next steps (wording: "**this is the only external step on which this round's conclusion depends**").
Round 28's **FC-7(a)** re-audited it and found that support **does not hold** — "surface 4 neighbours" is in fact §4.9 Lemma 1's **2D in-plane count** (2 axes × 2 directions inside the observer's plane), **not the bulk coordination number**; the support was changed to §4.10 Theorems 1+2 (rigorous), but the replacement chain still contains the external step "**if every direction corresponds to one bond**".
⟹ Round 30 judged that step unbridged and withdrew the diamond — **this is "the external step was never bridged", not "either reading may be chosen".**
⚠️ These two records previously existed **only in the memos** (0 occurrences in the paper); added here (**C-37**).

**(a) Hard constraints (retained)**: all nearest-neighbour transpositions within one tick form a **perfect matching** (every vertex covered exactly once)."""
sub_once(EN, E_D, E_D_NEW, "EN §8.6.8 gap record")

print("\n" + "=" * 70)
print("EN 侧完成，失败项：{}".format(BAD if BAD else "无 ✓"))
print("=" * 70)
