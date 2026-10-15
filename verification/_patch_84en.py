# -*- coding: utf-8 -*-
"""第 84 轮补丁 · EN 侧（与 ZH 侧三项一一对应）"""
import io
import os

BASE = "C:/Users/Administrator/Desktop/2026-08-20-21-43-34"
EN = os.path.join(BASE, "outputs", "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
BAD = []


def sub_once(path, old, new, tag, n=1):
    t = io.open(path, encoding="utf-8").read()
    c = t.count(old)
    if c != n:
        print("  [XX] {:<40} 命中 {}（期望 {}）".format(tag, c, n))
        BAD.append(tag)
        return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, n))
    print("  [OK] {:<40} 已改".format(tag))


# ================================================================
print("[EN-1] §8.6.8: audit note on the 'three independent grounds' (C-36)")
E_A = '> §4.9 Lemma 1 ("4 in-plane directions + 2 out-of-plane directions curled up") is exactly the statement "4 of the 6 neighbours are available for information transfer" — the two are consistent.'
E_A_NEW = E_A + """

> **【Round-84 audit note (C-36): rank of the grounds for the T-6 verdict】** The claim of **"three independent grounds"** in item (i) above is **overstated** — none of the three is an independent mathematical theorem: ① §4.10 **Argument 4** is labelled 【**structural argument**】 (end of §4.10: "Theorems 1 and 3 rigorous; Theorem 2 established; **Argument 4 a structural argument**"); ② §4.9 **Lemma 1** is labelled 【**framework assumption**】 (round 29 corrected it from "a derivation of this framework" ⟹ **no mechanism**); ③ the "discriminator" language in (i) turns a **matching** into a **discrimination** — Lemma 1 is a statement about **information channels** (see C-34), and using it to fix the geometry requires the extra reading "4 of the 6 neighbours are usable", itself labelled 【framework assumption】 (honest-limits table).
>
> ⭐ **The genuinely hard grounds live in §4.8**: the number of encoding directions is forced to 4 by two **counting constraints** — **`k·q = 16` (no integer solution at k = 6: 16/6 = 2.667)** and **`2^k = 16 ⟹ k = 4` (k = 6 gives 64 states)** — and both derive from **B5's "raw readable 4 bits/plaquette" plus the BH temperature calibration** (§4.8, round 33: `w = 0` is *solved for* jointly by the BH entropy calibration and full occupancy, not imported as an assumption).
>
> ⟹ **The correct — and harder — reason why "the diamond fails"**: the 4 encoding connections of §4.8 are **the bonds from a site to its 4 in-plane neighbours (±x, ±y)** (§4.9, round 35), and those 4 directions are **coplanar**; whereas the 4 bonds of diamond point along the **regular-tetrahedron directions (non-coplanar)** ⟹ **no plane in diamond can contain all 4 of its bonds** ⟹ **coplanarity is what fails**.
>
> ⚠️ **This also restores the standing of the round-27 reading**: round 27 fixed the lattice bond directions from "direction cluster k = 4 (Tammes regular tetrahedron)", and that inference **is self-consistent under the reading "direction cluster = exterior-space bond directions"**; round 30 instead adopts the **layered reading** (the direction cluster belongs to the **information / interior** layer and does not fix the geometric coordination number). ⟹ This is **not "round 27 got it wrong" but a contest between two readings**, and the framework adopts the latter. **The conclusion (simple cubic) is unchanged, but the wording should be read as "the attribution on which that step rested is not adopted" rather than "that step fails".** The rank of "coordination number 6 ⟹ simple cubic" is 【**verdict (one of two readings)**】, not 【theorem】."""
sub_once(EN, E_A, E_A_NEW, "EN §8.6.8 audit note")

# ================================================================
print("\n[EN-2] §4.9 Lemma 1: notation note on 'curled' (C-34)")
E_B = "- Lemma 1: accessible information = in-plane 4-direction connections (2 out-of-plane directions curled)【Framework assumption】;"
E_B_NEW = E_B + """
> **【Round-84 notation note (C-34): "curled" has three senses in this framework; Lemma 1 uses the third】**
> ① §2.1: **time dimensions** curled into the normal direction of the spatial plane ("the other two time dimensions are curled into the normal direction of the space plane");
> ② **Axiom 4**: **space** can be curled into time (the space–time interchange inside a black hole);
> ③ **this lemma**: "the 2 out-of-plane directions are curled" = the **information channel** along those 2 directions is inaccessible, while **geometrically they still exist** (see §8.6.8(b): simple-cubic coordination number 6; the L = 8 three-axis diffusion numerics give ⟨z²⟩ = 506.70 ✓).
> ⟹ ⚠️ Reading ③ as ② (space curled into time ⟹ ±z is not a spatial neighbour) would **directly contradict** the "coordination number 6" of §8.6.8(b). **When citing "curled", always state which sense is meant.**
> ⚠️ Same family as **C-15** (`λ`, three senses) / **C-16** (`ε`, three senses) / **C-21** (`ρ`, five senses) / **C-32** (`N`, two senses) — the **5th term clash**, and the one **most likely to flip a conclusion** (the earlier four only mis-stated a convention; this one can turn the lattice-geometry layer inside out)."""
sub_once(EN, E_B, E_B_NEW, "EN §4.9 Lemma 1 notation note")

# ================================================================
print("\n[EN-3] §4.8: synchronisation note on '(unique)' (C-35)")
t = io.open(EN, encoding="utf-8").read()
L = t.split("\n")
k = next(i for i, s in enumerate(L) if s.startswith("- **Origin of the substrate state count"))
line = L[k]
print("      行 L{}：{}…".format(k + 1, line[:110]))
NEW = line + """
> **【Round-84 synchronisation note (C-35)】** The "q = 4 → 4.000 (**unique**)" above refers to uniqueness **under inversion of B5's target "raw readable 4 bits/plaquette"**; the separate claim "**q = 4 is the unique solution**" was **withdrawn in round 32** (the reading verdict adopts **B2**: four in-plane connections each carrying a positive/negative branch ⟹ `2^4 = 16`) — see the round-32 block below. ⚠️ This chain is moreover a **consistency construction** (inverted from 16 states and 1 nat/block) and therefore has **no predictive power for `S = A/4`** (established in round 39)."""
sub_once(EN, line, NEW, "EN §4.8 synchronisation note")

# ================================================================
print("\n[EN-4] §8.6.8 honest-limits table: two added rows")
E_D = '| the precise meaning of "2 out-of-plane directions curled up" | 【framework assumption】, read here as "4 of the 6 neighbours available for information transfer" |'
E_D_NEW = E_D + """
| **"three independent grounds" (T-6)** | ⚠️ **Round-84 correction (C-36)**: none of the three is an independent mathematical theorem (Argument 4 = 【structural argument】 / Lemma 1 = 【framework assumption】); the genuinely hard grounds are the §4.8 counting constraints `k·q = 16` and `2^k = 16` ⟹ "coordination number 6 ⟹ simple cubic" should be labelled 【verdict (one of two readings)】, not 【theorem】 |
| **the round-27 reading (direction cluster = exterior bond directions ⟹ diamond)** | ⚠️ **Restored in round 84**: that inference is **self-consistent** under its reading and **was not a mistake**; the framework adopts the layered reading instead. **The hard reason "the diamond fails" is coplanarity** (§4.8's 4 encoding connections are **coplanar**, whereas diamond bonds are **non-coplanar** tetrahedral directions) |"""
sub_once(EN, E_D, E_D_NEW, "EN honest-limits two rows")

print("\n" + "=" * 70)
print("EN 侧完成，失败项：{}".format(BAD if BAD else "无 ✓"))
print("=" * 70)
