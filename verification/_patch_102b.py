# -*- coding: utf-8 -*-
"""第 102 轮补丁 b：修正两个未命中的锚点（EN-C64 / MEM-更正范围）"""
import io
import os

ROOT = r"C:/Users/Administrator/Desktop/2026-08-20-21-43-34"
EN = os.path.join(ROOT, "outputs/Paper_MatterAntimatterPairStorm_v2.9_EN.md")
MEM = os.path.join(ROOT, ".workbuddy/memory/MEMORY.md")
OK, BAD = [], []


def sub(path, old, new, tag):
    s = io.open(path, encoding="utf-8").read()
    n = s.count(old)
    if n != 1:
        BAD.append("{} :: 命中 {}\n     锚点: {}".format(tag, n, old[:130]))
        return
    io.open(path, "w", encoding="utf-8").write(s.replace(old, new))
    OK.append(tag)


sub(EN,
    "**Literature-comparison correction (v1.23, important)**: h_c=0.328474(3) is the critical value of the "
    "**σ^z field (Z field / flux-condensation version)** (dual 2+1D transverse-field Ising, Trebst 2007/Blöte–Deng 2002/"
    "Wu 2012); the framework's **X-field version (σ^x field / charge condensation) should be compared with h_xc≈0.32** "
    "(Trebst 2007/Vidal 2009, verified via arXiv:1304.0780) — the v1.22 citation \"h_c≈0.328 same order\" mixed the two "
    "versions, now corrected;",
    "**Literature comparison (the v1.23 text was itself wrong — corrected in round 102, C-64)**: v1.23 claimed that "
    "`h_c=0.328474(3)` is the **σ^z-field** value and that the framework's **X-field version should be compared with "
    "`h_xc≈0.32`**. **That correction was wrong.** Round-102 verification (arXiv 1309.7438 citing Trebst 2007 / "
    "Vidal 2009 / Tupitsyn 2010; arXiv 2603.14098): **`h_x^c ≈ 0.328` when `h_z = 0` (i.e. the X field)**, whereas "
    "**`h_x^c ≈ 0.34` belongs to the self-dual line `h_z = h_x`** — a different line. **X ↔ Z together with the dual "
    "lattice is an exact duality of the model (arXiv 2011.06611) ⟹ the two pure-field versions have the same value.** "
    "Moreover the model is exactly `H ≡ −Σ_v A_v − Σ_p B_p − h Σ_ℓ X_ℓ` (**on the torus**), matching this framework's "
    "model term-by-term. ⟹ **the X-field version is 0.328474, not 0.32**; ⚠️ the original script `_p03_torus.py` had it "
    "right (its docstring says \"X-field version … same convention as the literature h_c≈0.328\");",
    "EN-C64-修正")

sub(MEM, "（C-6…C-63）", "（C-6…C-66）", "MEM-更正范围")

print("== OK ==")
for x in OK:
    print("  ", x)
print("== BAD ==")
for x in BAD:
    print("  ", x)
