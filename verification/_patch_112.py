# -*- coding: utf-8 -*-
"""第 112 轮补丁：D4（EMRI κ↔Γ 映射）—— 中英同步 ＋ 材料包追加 ＋ 清单 ＋ 交接说明"""
import io, os

BASE = r"C:\Users\Administrator\Desktop\2026-08-20-21-43-34"
OUT = os.path.join(BASE, "outputs")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
LIST = os.path.join(OUT, "工程期望清单.md")
HO = os.path.join(BASE, "环境交接说明.md")
PACK = os.path.join(OUT, "EMRI材料包_给LISA组的S-E1-E4.md")
BAD = []

rd = lambda p: io.open(p, encoding="utf-8").read()
wr = lambda p, t: io.open(p, "w", encoding="utf-8").write(t)


def after_line(path, contains, block, tag):
    lines = rd(path).split("\n")
    idx = [i for i, s in enumerate(lines) if contains in s]
    if len(idx) != 1:
        print("  [XX] " + tag + " 行锚点 " + str(len(idx)) + " 次 —— 拒绝")
        BAD.append(tag)
        return
    lines[idx[0] + 1:idx[0] + 1] = block.split("\n")
    wr(path, "\n".join(lines))
    print("  [OK] " + tag + "（行 " + str(idx[0] + 2) + "）")


def before_line(path, contains, block, tag):
    lines = rd(path).split("\n")
    idx = [i for i, s in enumerate(lines) if contains in s]
    if len(idx) != 1:
        print("  [XX] " + tag + " 行锚点 " + str(len(idx)) + " 次 —— 拒绝")
        BAD.append(tag)
        return
    lines[idx[0]:idx[0]] = block.split("\n")
    wr(path, "\n".join(lines))
    print("  [OK] " + tag + "（行 " + str(idx[0] + 1) + "）")


def sub_once(path, old, new, tag):
    t = rd(path)
    n = t.count(old)
    if n != 1:
        print("  [XX] " + tag + " 命中 " + str(n) + " 次 —— 拒绝")
        BAD.append(tag)
        return
    wr(path, t.replace(old, new, 1))
    print("  [OK] " + tag)


# ---------------- 1) 论文 ZH ----------------
ZH_N = "\n".join([
    "> **【v2.9 口径注（第 112 轮：D4 —— `κ` 是唯象参数；度规自己的值是 `κ_rel(e)`）】** 上面这条链的",
    "> `δ = 0.30·x_p` **不是从度规或 `Γ(p)` 推出来的**：`stormetric` 的 `emri.py` 把 κ 写成 **`coupling`",
    "> （默认 `0.30`，docstring 自标 \"Phenomenological coupling\"）**，类文档并注明 `metric` 参数",
    "> **「kept for interface symmetry, the precession law itself is parametrised by κ」** ⟹ **进动律不经过度规**。",
    "> ⚠️ **口径**：代码把 `δ = κ x_p` 当**绝对**超额用（`Δφ_total = (6π+κ)x_p`、`n = 1/(κ x_p)`），",
    "> 但两度规 **1PN 相同** ⟹ **绝对**超额必为 `O(x_p²)`，**只有相对**超额才 ∝ `x_p` ⟹ 本条的数值须按",
    "> **相对**超额读（`0.57%/1.02%/1.55%` 即此）。",
    "> ⭐ **第 112 轮用本框架度规直接算**（测地线积分，mpmath 40 位；GR 复现闭式 `2π[(1−6M/p)^{−1/2}−1]`）：",
    "> **相对超额系数是偏心率依赖的** —— `κ_rel(e)` = **0.3333**（e→0）／0.3439（e=0.333）／0.3646（e=0.6）／",
    "> 0.3904（e=0.818）／**0.4116**（e=0.961）；**近圆极限 ⟹ `κ_rel → 1/3`**（外推 `0.33332`，误差 ≤10⁻⁴）。",
    "> ⟹ **唯象的单一 `κ = 0.30` 在全部偏心率下偏低 11%–37%**；「10% 缺口」不是矛盾，而是**掩盖了 κ 的",
    "> 偏心率依赖**。✅ **可升级**：`κ` 由**自由参数**升为**度规导出的函数 `κ_rel(e)`**（参数 **−1**）。",
    "> ⚠️ **诚实标注**：`κ_rel(e)` 本轮是**数值**（y→0 外推），**解析式未得**；且三处 `1/3`（`Γ` 的 `s²` 系数、",
    "> 2PN `g_rr` 分叉、`κ_rel(e→0)`）**代数无共同输入** ⟹ **不得写作「同源」**。",
])
after_line(ZH, "【v1.26 补充】LISA EMRI 检验提案", ZH_N, "ZH-1 D4 口径注")

EN_N = "\n".join([
    "> **【v2.9 caliber note (round 112: D4 - `κ` is a phenomenological parameter; the metric's own value is `κ_rel(e)`)】** The `δ = 0.30·x_p` above is **not derived from the metric or from `Γ(p)`**: in `stormetric`, `emri.py` declares κ as the **`coupling` field (default `0.30`, docstring \"Phenomenological coupling\")**, and the class docstring notes that the `metric` argument is **\"kept for interface symmetry, the precession law itself is parametrised by κ\"** ⟹ **the precession law does not pass through the metric at all**.",
    "> ⚠️ **Caliber**: the code uses `δ = κ x_p` as the **absolute** excess (`Δφ_total = (6π+κ)x_p`, `n = 1/(κ x_p)`); but the two metrics share the **same 1PN** ⟹ the **absolute** excess must be `O(x_p²)` and only the **relative** excess can scale as `x_p` ⟹ the numbers here must be read as the **relative** excess (the `0.57%/1.02%/1.55%` above).",
    "> ⭐ **Round 112 computed it directly from the framework's own metric** (geodesic quadrature, mpmath at 40 digits; GR reproduces the closed form `2π[(1−6M/p)^{−1/2}−1]`): **the relative-excess coefficient is eccentricity-dependent** — `κ_rel(e)` = **0.3333** (e→0) / 0.3439 (e=0.333) / 0.3646 (e=0.6) / 0.3904 (e=0.818) / **0.4116** (e=0.961); **the near-circular limit gives `κ_rel → 1/3`** (extrapolated `0.33332`, error ≤10⁻⁴).",
    "> ⟹ **The single phenomenological `κ = 0.30` is 11%–37% too low at every eccentricity**; the \"10% gap\" is not a contradiction but **conceals the eccentricity dependence of κ**. ✅ **Upgrade available**: κ moves from a **free parameter** to a **metric-derived function `κ_rel(e)`** (one parameter **removed**).",
    "> ⚠️ **Honest label**: `κ_rel(e)` here is **numerical** (y→0 extrapolation) with **no analytic form yet**; and the three occurrences of `1/3` (the `s²` coefficient of `Γ`, the 2PN `g_rr` bifurcation, and `κ_rel(e→0)`) have **no common algebraic input** ⟹ **they must not be called \"the same origin\"**.",
])
after_line(EN, "Numerical verification (geodesic RK4)", EN_N, "EN-1 round-112 caliber note")

# ---------------- 2) 材料包 ----------------
PK_N = "\n".join([
    "### 2.2b 【第 112 轮追加】`κ` 是唯象参数；框架度规自己的值是 `κ_rel(e)`",
    "",
    "⚠️ **这一条把 §2.2 的缺陷再往前推了一步**：查阅 `stormetric` 源码，`κ = 0.30` **不是标定出来的物理常数**，",
    "而是 `EMRIPrecession` 的**默认形参**（`coupling`），docstring 自标 **\"Phenomenological coupling\"**，",
    "且类文档注明度规参数是 **「kept for interface symmetry, the precession law itself is parametrised by κ」**",
    "⟹ **进动律不经过度规**。",
    "",
    "⭐ 而**用框架自己的度规**（`g_μν = diag(−e^{−2x}, e^{2x}, r²e^{2x}, r²sin²θ·e^{2x})`）做测地线积分",
    "（GR 侧复现闭式 `2π[(1−6M/p)^{−1/2}−1]` 作为标定），得到的**相对进动超额系数是偏心率依赖的**：",
    "",
    "| e | 0（圆轨道） | 0.333 | 0.6 | 0.818 | 0.961 |",
    "|---|---|---|---|---|---|",
    "| `κ_rel` | **0.3333** | 0.3439 | 0.3646 | 0.3904 | 0.4116 |",
    "",
    "**近圆极限 `κ_rel → 1/3`**（数值外推 `0.33332`，误差 ≤10⁻⁴）。",
    "",
    "⟹ ⚠️ **`κ = 0.30` 在全部偏心率下偏低 11%–37%**。**修正建议**：把 `κ` 换成 `κ_rel(e)`，",
    "并**用 `κ_rel(e)` 重算** S-E1–S-E4 的显著性数字；⚠️ 本轮给出的是**相对**超额，而代码的 `n = 1/(κ x_p)`",
    "按**绝对**相位用量 ⟹ **两侧口径需一并改**。",
    "",
    "⚠️ **诚实标注**：本轮的 `κ_rel(e)` 是**数值**（y→0 外推），**解析式未得**，精度约 10⁻³",
    "（e-依赖 13%–23% ≫ 求积残差 ~10⁻³）⟹ 本表是**「度规不同意单一 κ」**的证据，**不是**最终的预言数值。",
    "",
])
before_line(PACK, "### 2.3 三个前提", PK_N, "PK-1 材料包 2.2b")

# ---------------- 3) 清单 ----------------
ROW = ("| **第 112 轮**（**D4 执行**） | **C-78 更正 ＋ N-42 负面 ＋ D4 结项：EMRI 的 κ 是唯象参数，度规给 `κ_rel(e)`** | "
       "第 108 轮清点出的**最后一条**真缺口 D4（登记 08-29：「EMRI κ↔Γ 1/3 精确映射，10% 缺口，需轨道平均 s_p 分布积分」）。"
       "**结果**：① ⭐⭐ **C-78**：`κ = 0.30` 在 `stormetric/emri.py` 里是 **`coupling` 的默认形参**"
       "（docstring 自标 **\"Phenomenological coupling\"**；类文档注明度规参数 **「kept for interface symmetry, "
       "the precession law itself is parametrised by κ」**）⟹ **进动律不经过度规**；C1 报告亦自承「不是从 Γ(p) 第一性推导」。"
       "⚠️ **口径错位**：代码把 `δ = κ x_p` 当**绝对**超额（`Δφ_total=(6π+κ)x_p`、`n=1/(κ x_p)`），"
       "而 1PN 两度规相同 ⟹ **绝对**超额必为 `O(x_p²)`、**只有相对**超额 ∝ `x_p`（`0.57%/1.02%/1.55%` 是相对量）。"
       "② ⭐⭐⭐ **本轮定量产出（新）**：**用框架自己的度规**做测地线积分（mpmath 40 位；GR 侧复现闭式标定），"
       "得**相对超额系数 κ_rel(e)：0.3333(e→0)／0.3439(0.333)／0.3646(0.6)／0.3904(0.818)／0.4116(0.961)**，"
       "**近圆极限 → 1/3**（外推 0.33332，误差 ≤1e-4）⟹ **唯象的单一 κ = 0.30 在全部偏心率下偏低 11%–37%**；"
       "「10% 缺口」不是矛盾，而是**掩盖了 κ 的偏心率依赖**。✅ **可升级**：κ 由**自由参数**升为**度规导出的 `κ_rel(e)`**（**参数 −1**）。"
       "③ ⭐ **N-42**：三处 `1/3`（Γ 的 s² 系数／2PN g_rr 分叉／κ_rel(e→0)）**代数无共同输入** ⟹ 登记为"
       "**无机制的一致性**，**不得**写作「同源」（08-29 与 C1 报告原措辞已就地加注）。"
       "④ ⚠️ **数值稳健性**：Rp=1000 与 500 的最大相对差 **< 0.5%**；但 `κ_rel(e)` 仍是**数值**、**解析式未得**"
       "（登记 **I-24**），精度 ~1e-3（e-依赖 13%–23% ≫ 求积残差）。⚠️ **论文中英各 1 处口径注 ＋ 材料包新增 §2.2b**。 "
       "| 第 112 轮（`_d4_112.py` D4-1…D4-14，**17 项断言 0 失败**；计算 `_d4_kappa.py`／`_d4_recon6.py`） | "
       "同 `D4结项_EMRI进动系数的偏心率依赖与1_3极限.md` |")
lines = rd(LIST).split("\n")
idx = [i for i, s in enumerate(lines) if s.startswith("| **第 107 轮**（**元任务 · 考古**）")]
if len(idx) == 1:
    lines[idx[0]:idx[0]] = ROW.split("\n")
    wr(LIST, "\n".join(lines))
    print("  [OK] L-1 零表第112轮行（行 " + str(idx[0] + 1) + "）")
else:
    BAD.append("L-1")
    print("  [XX] L-1 锚点 " + str(len(idx)) + " 次")

C78 = ("| **C-78** | ⭐⭐ **EMRI 的 `κ` 是唯象输入（不是标定/推导量）＋ 绝对/相对口径错位（第 112 轮；D4）** | **更正 / 口径** | "
       "① `stormetric/src/stormetric/emri.py`：`kappa` 是 **`coupling: float = 0.30`** 的默认形参，docstring 自标 "
       "**\"Phenomenological coupling\"**，类文档注明 `metric` **「kept for interface symmetry, the precession law itself "
       "is parametrised by κ」** ⟹ **进动律不经过度规**；`cli.py` 两处 `--kappa` 默认 0.30（**可调**）。"
       "C1 报告亦自承「κ=0.30 不是从 Γ(p) 第一性推导的」。⟹ **「10% 缺口」是一个输入参数与一个解析系数的比较。** "
       "② **口径错位**：代码写 `δ = κ x_p` 并当**绝对**超额用（`Δφ_total=(6π+κ)x_p`、`n_orbits = 1/(κ x_p)`），"
       "但两度规 **1PN 相同**（β=γ=1）⟹ **绝对**超额必为 `O(x_p²)`，**只有相对**超额才 ∝ `x_p`"
       "（材料包 `0.57%/1.02%/1.55%` 是相对量）。⚠️ 另一处基线口径：代码 `6π x_p`（`x_p=GM/c²r_p`）"
       "与真值 `6πM/p = 6π x_p(1+q)/(2q)` 差 **25%（q=2）–45%（q=10）**——不影响相对量，但影响绝对去相位预算。 "
       "🔧 处置：中英各加 1 处口径注；材料包加 **§2.2b**。 | 第 112 轮（`_d4_112.py` D4-1／D4-3） | 同 `D4结项_…md` |")
N42 = ("| **N-42** | ⭐⭐ **把三处 `1/3` 当作「同源」（第 112 轮；D4）** | **负面** | "
       "**判否**。三处精确的 `1/3`：① `Γ(p)` 谱因子 `Φ(s)/Φ(0) = 1 + (1/3)s² − (1/30)s⁴ + …`"
       "（来自 `(s+1/2s)erf(s) + e^{−s²}/√π` 的展开）；② 2PN `g_rr` 分叉 `(2 − 3/2)/(3/2) = 1/3`"
       "（来自 `e^{2x}` vs `(1+x/2)⁴` 的二项系数）；③ **本轮新增**：框架度规的相对进动超额系数 "
       "`κ_rel(e→0) = 1/3`（数值外推 0.33332，误差 ≤1e-4）。**三条链的输入集合两两不相交** ⟹ "
       "只能登记为**无机制的一致性**（铁律 2），**不得**写作「同源」。⛔ 08-29 日志与 C1 报告的"
       "「与 2PN g_rr 分叉 1/3 **同源**」措辞应改。 | 第 112 轮（`_d4_112.py` D4-8） | 同 `D4结项_…md` |")
i77 = [i for i, s in enumerate(lines) if s.startswith("| **C-77** |")]
if len(i77) == 1:
    lines[i77[0] + 1:i77[0] + 1] = C78.split("\n") + N42.split("\n")
    wr(LIST, "\n".join(lines))
    print("  [OK] L-2 C-78 ＋ N-42（行 " + str(i77[0] + 2) + " 起）")
else:
    BAD.append("L-2")
    print("  [XX] L-2 锚点 " + str(len(i77)) + " 次")

sub_once(LIST, "| **撤回 / 更正** | **76 条**（**C-77（第 111 轮，A23）**",
         "| **撤回 / 更正** | **77 条**（**C-78（第 112 轮，D4）**：EMRI 的 `κ` 是**唯象输入**"
         "（`emri.py` 的 `coupling` 默认 0.30，自标 \"Phenomenological coupling\"）＋ 绝对/相对口径错位；"
         "**C-77（第 111 轮，A23）**", "L-3 撤回/更正 76→77")
sub_once(LIST, "| **负面判定** | **41 条**（**N-41",
         "| **负面判定** | **42 条**（**N-42（第 112 轮，D4）**：三处精确 `1/3`（Γ 的 s² 系数／2PN g_rr 分叉／"
         "`κ_rel(e→0)`）**代数无共同输入** ⟹ 不得写作「同源」；**N-41", "L-4 负面 41→42")
sub_once(LIST, "**A23 ✅ 第 111 轮结项**（`ℏ` 的身份 —— **不可辨识 ＋ `M²/A` 恒等式**；**C-77 ＋ N-41**）",
         "**A23 ✅ 第 111 轮结项**（`ℏ` 的身份 —— **不可辨识 ＋ `M²/A` 恒等式**；**C-77 ＋ N-41**）；"
         "**D4 ✅ 第 112 轮结项**（EMRI `κ` —— **唯象输入 ＋ 度规给 `κ_rel(e)`，近圆极限 = 1/3**；**C-78 ＋ N-42**）"
         "⟹ **清单上的 4 条真缺口全部结项（G4／G9／A23／D4）**",
         "L-5 剩余待办段")

# ---------------- 4) 交接说明 ----------------
PRI = ("0. 🎯 **当前建议（第 112 轮后）**：**D4（EMRI `κ↔Γ` 的 1/3 映射）已结项 —— 结论是「κ 是唯象参数」＋"
       "「度规给出的是偏心率依赖的函数」**。⭐⭐ **C-78**：`κ = 0.30` 在 `stormetric/emri.py` 里是 **`coupling` 的默认形参**"
       "（docstring 自标 **\"Phenomenological coupling\"**；类文档注明度规参数「kept for interface symmetry」）"
       "⟹ **进动律不经过度规**；且代码把 `δ = κ x_p` 当**绝对**超额用，而 1PN 相同 ⟹ 绝对超额必为 `O(x_p²)`"
       "（**口径错位**）。⭐⭐⭐ **本轮定量产出**：**用框架自己的度规**做测地线积分（GR 侧复现闭式 `2π[(1−6M/p)^{−1/2}−1]` 作标定），"
       "得**相对超额系数 `κ_rel(e)` = 0.3333(e→0)／0.3439(0.333)／0.3646(0.6)／0.3904(0.818)／0.4116(0.961)**，"
       "**近圆极限 → 1/3**（外推 0.33332）⟹ **唯一的出口上，单一 `κ = 0.30` 在全部偏心率下偏低 11%–37%**；"
       "✅ **可升级**：`κ` 由**自由参数**升为**度规导出的 `κ_rel(e)`**（**参数 −1**）。⚠️ 但 `κ_rel(e)` 仍是**数值**"
       "（解析式未得，精度 ~1e-3）⟹ 登记 **I-24**。⭐ **N-42**：三处 `1/3` **代数无共同输入** ⟹ 不得写作「同源」。"
       "📌 **清单上的 4 条真缺口已全部结项（G4／G9／A23／D4）** ⟹ 此后属「等外部」（LISA ~10–15 年）／「等人」（私下送审）；"
       "⚠️ **但 EMRI 的显著性数字（`ΔlnL = 357` 等）应先用 `κ_rel(e)` 重算**（材料包已加 §2.2b）。\n")
sub_once(HO, "0. 🎯 **当前建议（第 111 轮后）**", PRI + "\n0. 🎯 **（历史，第 111 轮后）**", "H-1 🎯 第112轮条目")

print("")
print("BAD = " + str(BAD))
