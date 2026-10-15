# -*- coding: utf-8 -*-
"""第 101 轮补丁 b：英文稿的 v1.36 修正段 + §10.2#13 条目（中英同步，C-63 收尾）"""
import io
import os

ROOT = r"C:/Users/Administrator/Desktop/2026-08-20-21-43-34"
EN = os.path.join(ROOT, "outputs/Paper_MatterAntimatterPairStorm_v2.9_EN.md")
OK, BAD = [], []


def sub(path, old, new, tag):
    s = io.open(path, encoding="utf-8").read()
    n = s.count(old)
    if n != 1:
        BAD.append("{} :: 命中 {}\n     锚点前 90 字: {}".format(tag, n, old[:90]))
        return
    io.open(path, "w", encoding="utf-8").write(s.replace(old, new))
    OK.append(tag)


sub(EN,
    "λ_c≈0.14 is of the same order as the dual 3D Ising β_c=0.2217 (v1.28 duality self-consistent);",
    "λ_c≈0.14 is of the same order as the dual 3D Ising β_c=0.2217 (v1.28 duality self-consistent);"
    "【**v2.9 correction**: λ_c≈0.14 is a rod/plate pseudo-critical value (thinnest direction = 1). "
    "**Round-101 re-correction**: with 4 true 3D boxes (incl. L=3) the χ peak does **not** converge "
    "(coarse grid 0.2425→0.2459→0.2826→0.3075), and the **grid dependence itself grows with size** "
    "(0.008→0.018→0.025) — the same order as the size drift ⟹ **λ_c(∞) judged \"methodologically "
    "insufficient — not localized\"**; ⚠️ comparison with 3D Ising `β_c=0.2217` is **not valid — different "
    "axes** (here the plaquette coupling `K` is fixed while the X-field `λ` is swept; the duality maps "
    "`β`↔`K`, not `β`↔`λ`). See §10.1b.】",
    "EN-v1.36修正")

sub(EN,
    "λ_c(∞) exact value (requires 3D-box MPS/DMRG), rigorous Maxwell-spectrum verification.",
    "λ_c(∞) exact value (**round 101: 4 sizes incl. L=3 already done, still not localized** — the χ-peak "
    "criterion's resolution is insufficient; requires a different order parameter ('t Hooft/Wilson-loop "
    "perimeter–area-law crossing) and a different algorithm (PEPS/QMC), see §10.1b), rigorous "
    "Maxwell-spectrum verification.",
    "EN-10.2#13")

print("== OK ==")
for x in OK:
    print("  ", x)
print("== BAD ==")
for x in BAD:
    print("  ", x)
