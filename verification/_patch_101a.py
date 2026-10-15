# -*- coding: utf-8 -*-
"""第 101 轮补丁（甲-2 结项 → 论文中英 + 台账 + 交接 + MEMORY）

⚠️ 铁律：所有替换用「整行/整段锚点 + count==1 断言」，禁止行号。
⚠️ 中英必须同步；本轮同时**补上英文稿缺失的两处**（C-63）。
"""
import io
import os
import re

ROOT = r"C:/Users/Administrator/Desktop/2026-08-20-21-43-34"
ZH = os.path.join(ROOT, "outputs/论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(ROOT, "outputs/Paper_MatterAntimatterPairStorm_v2.9_EN.md")
LIST = os.path.join(ROOT, "outputs/工程期望清单.md")
HAND = os.path.join(ROOT, "环境交接说明.md")
MEM = os.path.join(ROOT, ".workbuddy/memory/MEMORY.md")
A1R = os.path.join(ROOT, "outputs/A1_3D盒子λc数值定位.md")

OK, BAD = [], []


def sub(path, old, new, tag, must1=True):
    s = io.open(path, encoding="utf-8").read()
    n = s.count(old)
    if (must1 and n != 1) or (not must1 and n < 1):
        BAD.append("{} :: 命中 {} （期望 {}）\n     锚点前 80 字: {}".format(
            tag, n, 1 if must1 else ">=1", old[:80]))
        return
    io.open(path, "w", encoding="utf-8").write(s.replace(old, new))
    OK.append(tag)


# ============================================================ 中文稿
sub(ZH,
    "框架**有相变** `λ_c ∈ [0.21, 0.23]`、`κ_c ∈ [0.25, 0.32]`，",
    "框架**有相变**（弦网 `λ_c` 量级 ~0.2–0.3，**【第 101 轮：热力学极限值仍未定位】**；`κ_c ∈ [0.25, 0.32]`），",
    "ZH850-边界扩大")

sub(ZH,
    "【**v2.9 修正**：λ_c≈0.14 为棒/板伪临界；真 3D 盒子 λ_χ≈0.21–0.23，与 2D toric code（0.25–0.32）同量级、"
    "与 3D Ising β_c=0.2217 更接近（差 3–7%）——「递减谱系」实为伪临界假象，真谱系 2D↔3D 同量级（见 §10.1b）】",
    "【**v2.9 修正**：λ_c≈0.14 为棒/板伪临界（最薄方向=1）。**第 101 轮再修正**：真 3D 盒子扩到 **4 尺寸（含 L=3）**后，"
    "χ 峰位**并不收敛**（粗网格 0.2425→0.3075），且**网格差本身随尺寸增大（0.008→0.025）**、与尺寸漂移同量级 ⟹ "
    "**λ_c(∞) 判定为「方法学不足，未定位」**；⚠️ 与 3D Ising `β_c=0.2217` 的比较**不成立 —— 两者不在同一轴**"
    "（本模型 `K`=plaquette 耦合固定、沿 X 场 `λ` 扫描；对偶映射连接的是 `β`↔`K`，非 `β`↔`λ`）。见 §10.1b】",
    "ZH1126-v1.36修正")

sub(ZH,
    "**【v2.9 补充】真 3D 盒子 DMRG（A1）**：2×2×2（36 面，2^36=6.9×10¹⁰ 态）与 3×2×2（52 面）手写 1-site "
    "MPS/DMRG（χ=8，2×1×1 精确对角化验证至 1e-15）扫描——**χ 峰 λ_χ(2×2×2)=0.230、λ_χ(3×2×2)≈0.19–0.21（主峰）**；"
    "两尺寸最小线性尺寸均为 L=2 且峰位无漂移 ⟹ **λ_c(∞) 估计 [0.21, 0.23]**（与 3D Ising β_c=0.2217 差 3–7%，"
    "支持 v1.28 对偶自洽）；χ=8→16 峰区实测 ⟨A_c⟩ 偏移 2.3%、E 偏移 1.6%（截断稳健）；"
    "3×2×2 尾端（λ≥0.29）χ 回升为 χ=8 截断噪声。【诚实标注】λ_c(∞) 严格外推需 L=3 盒子与更高 χ"
    "（后续工作⑤，详见《A1 3D盒子λc数值定位》报告）。",
    "**【v2.9 补充】真 3D 盒子 DMRG（A1）**：2×2×2（36 面）与 3×2×2（52 面）手写 1-site MPS/DMRG（χ=8）扫描——"
    "χ 峰 λ_χ(2×2×2)=0.230、λ_χ(3×2×2)≈0.19–0.21。\n\n"
    "**【第 101 轮（甲-2）更正：`λ_c(∞)` 仍未定位，且 A1 的 [0.21, 0.23] 系过度解读】**"
    "（脚本 `_lc3d_box_fast.py`／`_lc3d_run_101.py`／`_lc3d_analyze.py`／`_lc3d_chitest.py`；"
    "求解器经 2×1×1 精确对角化验证至 1e-15、并**逐点复现** A1 的 2×2×2 数据 ⟨A_c⟩ 至 5e-5）"
    "——**四点更正**：\n"
    "① **尺寸扩到 4 个（2×2×2／3×2×2／3×3×2／3×3×3，含真 L=3）后峰位不收敛**：粗网格 0.2425→0.2459→0.2826→**0.3075**；"
    "A1 的「无漂移」是**两个最短边都为 2 的尺寸**所致（非独立标度点）；\n"
    "② **判据分辨率不足，且不计入误差棒就不能外推**：χ 峰的**网格差随尺寸增大**（0.008→0.018→**0.025**），"
    "与尺寸漂移（~0.03）**同量级**；细网格序列 0.2348→0.2281→0.2572 **不单调**；1/L̄ 外推给 **0.436**（**超出全部数据**，自证荒谬）；\n"
    "③ **`χ = −d⟨A_c⟩/dλ` 在本模型不是可靠的相变判据**（与本节已有的 2D 诊断「m(h_c) 外推 → 0.93 ≠ 0 ⟹ ⟨X⟩ 非序参量」**同族**）；"
    "且 **Binder 累积量恒等失效**（`A_c² = I` ⟹ ≡ 2/3）；本轮**唯一**较强判据是 ⟨A_c⟩ 的**跨尺寸交叉点**，集中在 **0.32–0.34**；\n"
    "④ **χ=8 截断已实测到 1–3%**（2×2×2 上 χ=8→16 使 ⟨A_c⟩ 偏 +0.0205，ΔE 1.7%）——"
    "⚠️ 而 1-site DMRG 的 discarded weight **恒为 0**（不增长 bond）⟹ **它不能当质量指标**，故 L=3 的误差**无法量化**。\n"
    "⟹ **判决：`λ_c(∞)` 在本方法下不可解（登记为「方法学不足，未定位」，不给数）**。要定位需**换序参量**"
    "（'t Hooft/Wilson 环的周长–面积律交叉）＋**换算法**（PEPS／3D DMRG／QMC——本模型无符号问题）＋**建立精确对偶映射**。"
    "详见《甲2结项_λc∞未定位_判据分辨率不足的量化》。",
    "ZH2033-A1段更正")

sub(ZH,
    "λ_c(∞) 已获 3D 盒子 DMRG 初值（v2.9，λ_χ≈0.21–0.23），L=3 严格外推待做（后续工作⑤）；",
    "λ_c(∞) **仍未定位**（第 101 轮：4 尺寸含 L=3 已做，但判据分辨率 ~0.04 与尺寸漂移同量级 ⟹ **方法学不足**，"
    "需换序参量与算法）；",
    "ZH2037-适用边界")

sub(ZH,
    "λ_c(∞) 精确定位（3D 盒子 DMRG 已给 λ_χ≈0.21–0.23 初值，L=3 盒子待做，v2.9）、麦克斯韦谱严格验证。",
    "λ_c(∞) 精确定位（**第 101 轮：4 尺寸含 L=3 已做，仍未定位**——χ 峰判据分辨率不足，需换序参量"
    "（'t Hooft/Wilson 环）与算法（PEPS/QMC），见 §10.1b）、麦克斯韦谱严格验证。",
    "ZH2053-10.2#13")

# ============================================================ 英文稿
sub(EN,
    "the framework **has transitions** at `lambda_c in [0.21, 0.23]` and `kappa_c in [0.25, 0.32]`",
    "the framework **has transitions** (string-net `lambda_c` of order ~0.2–0.3, **【round 101: thermodynamic-limit value still not localized】**; "
    "`kappa_c in [0.25, 0.32]`)",
    "EN850-边界扩大")

sub(EN,
    "**λ_c finite-size boundary**: 4-size χ_max ∝ L^{−0.04} (not growing) ⟹ the χ peak is a broadened pseudo-peak; "
    "λ_χ shows no drift (all 0.140) ⟹ **conservative interval λ_c(∞) ∈ [0.140, 0.140]; precise localization requires "
    "3D-box MPS/DMRG** (open numerical problem, honestly retained).",
    "**λ_c finite-size boundary**: 4-size χ_max ∝ L^{−0.04} (not growing) ⟹ the χ peak is a broadened pseudo-peak; "
    "λ_χ shows no drift (all 0.140) ⟹ v1.36's [0.140, 0.140] is a **rod/plate (thinnest direction = 1) pseudo-critical value**.\n\n"
    "**【v2.9 supplement】true 3D-box DMRG (A1)**: 2×2×2 (36 faces) and 3×2×2 (52 faces), hand-written 1-site MPS/DMRG (χ=8) — "
    "χ peaks λ_χ(2×2×2)=0.230, λ_χ(3×2×2)≈0.19–0.21.\n\n"
    "**【round 101 (item 甲-2) correction: `λ_c(∞)` is still NOT localized, and A1's [0.21, 0.23] was over-interpretation】** "
    "(scripts `_lc3d_box_fast.py` / `_lc3d_run_101.py` / `_lc3d_analyze.py` / `_lc3d_chitest.py`; the solver was validated "
    "against exact diagonalization on 2×1×1 to 1e-15 and **reproduces A1's 2×2×2 data point-by-point to 5e-5**) — **four corrections**:\n"
    "① **with 4 sizes (2×2×2 / 3×2×2 / 3×3×2 / 3×3×3, including a true L=3) the peak does not converge**: coarse grid "
    "0.2425→0.2459→0.2826→**0.3075**; A1's \"no drift\" came from **two sizes whose shortest edge is both 2** (not independent scaling points);\n"
    "② **the criterion's resolution is insufficient, and extrapolation without error bars is not possible**: the χ-peak **grid "
    "dependence grows with size** (0.008→0.018→**0.025**) and is **of the same order** as the size drift (~0.03); the fine-grid "
    "sequence 0.2348→0.2281→0.2572 is **non-monotonic**; 1/L̄ extrapolation gives **0.436** (**outside the entire data range** — self-evidently absurd);\n"
    "③ **`χ = −d⟨A_c⟩/dλ` is not a reliable transition criterion in this model** (same family as the 2D diagnosis already in this "
    "section: \"m(h_c) extrapolates to 0.93 ≠ 0 ⟹ ⟨X⟩ is not the order parameter\"); and the **Binder cumulant is identically "
    "useless** (`A_c² = I` ⟹ ≡ 2/3); the only relatively strong criterion this round is the **cross-size crossing point of ⟨A_c⟩**, "
    "clustered at **0.32–0.34**;\n"
    "④ **the χ=8 truncation error is measured at 1–3%** (on 2×2×2, χ=8→16 shifts ⟨A_c⟩ by +0.0205, ΔE by 1.7%) — ⚠️ and because "
    "1-site DMRG's discarded weight is **identically 0** (no bond growth) ⟹ **it cannot serve as a quality metric**, so the L=3 "
    "error **cannot be quantified**.\n"
    "⟹ **Verdict: `λ_c(∞)` is not solvable by this method** (registered as \"methodologically insufficient — not localized\", "
    "no number given). Localizing it requires a **different order parameter** ('t Hooft/Wilson-loop perimeter–area-law crossing) "
    "＋ a **different algorithm** (PEPS / 3D DMRG / QMC — this model has no sign problem) ＋ an **exact duality map**. "
    "See the memo 《甲2结项_λc∞未定位_判据分辨率不足的量化》.",
    "EN2000-A1段补齐+更正")

sub(EN,
    "**→ toy-model domain of validity clarified**: transition criteria (κ_c) depend on literature calibration and "
    "order-parameter upgrade; λ_c(∞) is an open numerical problem;",
    "**→ toy-model domain of validity clarified**: transition criteria (κ_c) depend on literature calibration and "
    "order-parameter upgrade; λ_c(∞) **remains unlocalized after round 101's 4-size (incl. L=3) scan — the criterion's "
    "resolution (~0.04) is the same order as the size drift**;",
    "EN2004-适用边界")

print("== OK ==")
for x in OK:
    print("  ", x)
print("== BAD ==")
for x in BAD:
    print("  ", x)
