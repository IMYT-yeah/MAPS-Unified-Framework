# arXiv Submission Package

**Paper**: Matter–Antimatter Pair Storm: An Emergent Statistical Framework for the Unification of Fundamental Forces (v2.8 EN)

**Generated**: 2026-08-24

---

## Package contents

| File | Description |
|---|---|
| `main.tex` | LaTeX source (arXiv-submission ready, compiled with pdfLaTeX/XeLaTeX) |
| `main.pdf` | Compiled PDF (after running tectonic/pdflatex) |
| `main.tex.log` | Compilation log (if produced) |

No external image/graphic files are required — all content is text/math/tables.

---

## Before submitting: fill in the metadata

Edit `main.tex` and replace the placeholder author line:

```latex
\author{AUTHOR NAME\thanks{Author affiliation.} \\ \small Author affiliation}
```

with the real author name(s) and affiliation(s), e.g.

```latex
\author{Your Name\\ \small Department of Physics, Your University}
```

---

## Suggested arXiv metadata

| Field | Value |
|---|---|
| Title | Matter–Antimatter Pair Storm: An Emergent Statistical Framework for the Unification of Fundamental Forces |
| Authors | (fill in) |
| Primary category | `gr-qc` (General Relativity and Quantum Cosmology) — gravity/black-hole/cosmology core |
| Secondary categories | `hep-th`, `quant-ph`, `astro-ph.CO` |
| Comments | "Heuristic unification framework. 30 references; PPN/EMRI/string-net numerics included." |

The primary category is a suggestion: if you prefer a high-energy-theory framing, use `hep-th` as primary and `gr-qc` as secondary. Note that the framework also touches quantum foundations (Bell/CHSH, §7) and condensed-matter analogues (string-net, §5.8), so `quant-ph` and `cond-mat.str-el` are defensible secondary choices.

---

## Compile locally (verify)

With any TeX distribution (TeX Live / MiKTeX / Overleaf), run:

```
pdflatex main.tex     (run twice for stable cross-references)
```

Required packages (all standard, included in TeX Live / MiKTeX / Overleaf / arXiv's TeX Live):
`geometry, amsmath, amssymb, amsthm, ulem, booktabs, tabularx, array, enumitem, lmodern, microtype, hyperref`

> Note: the file was compiled and verified with the Tectonic engine (XeTeX-based, TeX Live-compatible). It uses only standard packages — no `pifont`/custom fonts — so arXiv's pdflatex pipeline should accept it without modification. If arXiv reports anything unusual, first recompile locally with `pdflatex main.tex` and compare warnings.

---

## Submit to arXiv

1. Go to <https://arxiv.org/submit> (requires an arXiv account; author endorsement may be needed for first submission to hep-th/gr-qc).
2. Upload `main.tex` (and `main.pdf` if you want to double-check the rendered version).
3. Fill in the metadata form (title, authors, abstract, categories — see above).
4. Use the arXiv "Preview" button to inspect the compiled output before final submission.
5. If arXiv's TeX Live reports errors you do not see locally, check the arXiv TeX Live version (currently TeX Live 2024) and avoid bleeding-edge packages.

---

## Known remaining work before a polished version

- **References**: currently 30 entries. The paper header states "to be completed to 50+ in the published version" — consider expanding (string-net/topological-order literature, EMRI/LISA literature, DESI DR2 cosmology, exponential-metric tradition, emergent-gravity reviews) before or after submission.
- **Abstract length**: arXiv limits abstracts to ~1920 characters (1,920) for the metadata form — the current abstract is long; arXiv truncates display but accepts full text if it fits within the limit. Verify on the submission form.
- **Figures**: none included. If desired, figures for the seven-loop mechanism chain (§4.6), the string-net condensation numerics (§5.7/5.8), and the EMRI verdict (§9 S-E1) could be added in a follow-up version.

---

## Files in the parent directory (for reference, not part of the submission)

- `Paper_MatterAntimatterPairStorm_v2.8_EN.md` — the English source (Markdown)
- `论文初稿_正反物质对风暴统一框架_v2.8.md` — the Chinese source
- `_arxiv_convert.py` — the Markdown→LaTeX converter used to generate `main.tex`
