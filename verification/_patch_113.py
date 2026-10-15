# -*- coding: utf-8 -*-
"""第 113 轮补丁：I-24（部分结项）—— 中英同步 ＋ 清单 ＋ 交接说明"""
import io, os

BASE = r"C:\Users\Administrator\Desktop\2026-08-20-21-43-34"
OUT = os.path.join(BASE, "outputs")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
LIST = os.path.join(OUT, "工程期望清单.md")
HO = os.path.join(BASE, "环境交接说明.md")
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


# ---------------- 1) 论文 ZH：接在第 112 轮注之后 ----------------
ZH_N = "\n".join([
    "> **【v2.9 口径注（第 113 轮：I-24 —— `e→0` 的 `1/3` 已升为解析结论，并给出机制）】** 上一条注里的",
    "> `κ_rel(e→0) = 0.33332` 是**数值外推**；本轮用**圆轨道本轮频率比** `Γ ≡ ω_φ/ω_r`（进动 `= 2π(Γ−1)`）",
    "> 把它**解析**求出：以 `y = M/p_areal` 展开，`Γ_GR − 1 = 3y + 27/2·y² + 135/2·y³`（**与精确闭式",
    "> `(1−6y)^{−1/2}−1` 逐项相等** ⟹ 机器与 `ε↔y` 换式均已标定），`Γ_FW − 1 = 3y + 29/2·y² + 77y³`",
    "> ⟹ **`κ_rel(e→0) = Δc₂/c₁ = (29/2 − 27/2)/3 = 1/3`（精确有理数）**；圆轨道修正 `κ_rel = 1/3 + (5/3)y`。",
    "> ⭐ **机制**：只换一侧度规可把 `Δc₂` **严格分解**为 **`g_rr/g_θθ` 侧 `+1.25`** 与 **`g_tt` 侧 `−0.25`**",
    "> （`+1.25 − 0.25 = 1.00`，无交叉项）⟹ `κ = +5/12 − 1/12 = 1/3`。",
    "> ⚠️ **仍未得**：**一般偏心率**的 `κ_rel(e)` 解析式（两点积分 `2∫du/√F` 的全级数计算量过大，",
    "> 已登记 **I-25**；现有仅第 112 轮的数值表 `κ_rel(e): 1/3 → 0.4116`，`e: 0 → 0.961`）。",
    "> 📌 **N-42 复核**：本项的 `1/3` 现在**有机制**（= 度规自身的 2PN 系数差 ÷ 1PN 斜率），",
    "> 但 `Γ` 的 `s²` 系数 `1/3` 来自 Maxwell 角平均 ⟹ **两者机制不同，仍不得写作「同源」**。",
])
after_line(ZH, "【v2.9 口径注（第 112 轮：D4", ZH_N, "ZH-1 第113轮注")

EN_N = "\n".join([
    "> **【v2.9 caliber note (round 113: I-24 - the `1/3` at `e→0` is now an analytic result, with a mechanism)】** The `κ_rel(e→0) = 0.33332` in the note above was a **numerical extrapolation**; this round obtains it **analytically** from the **circular-orbit epicyclic ratio** `Γ ≡ ω_φ/ω_r` (advance `= 2π(Γ−1)`): expanded in `y = M/p_areal`, `Γ_GR − 1 = 3y + 27/2·y² + 135/2·y³` (**term-by-term equal to the exact closed form `(1−6y)^{−1/2}−1`** ⟹ both the machinery and the `ε↔y` conversion are calibrated), and `Γ_FW − 1 = 3y + 29/2·y² + 77y³` ⟹ **`κ_rel(e→0) = Δc₂/c₁ = (29/2 − 27/2)/3 = 1/3` (exact rational)**; the circular-orbit correction is `κ_rel = 1/3 + (5/3)y`.",
    "> ⭐ **Mechanism**: changing one side of the metric at a time decomposes `Δc₂` **exactly** into **`+1.25` from the `g_rr/g_θθ` side** and **`−0.25` from the `g_tt` side** (`+1.25 − 0.25 = 1.00`, no cross term) ⟹ `κ = +5/12 − 1/12 = 1/3`.",
    "> ⚠️ **Still open**: the analytic `κ_rel(e)` for **general eccentricity** (the full series of the two-turning-point integral `2∫du/√F` is computationally prohibitive; registered as **I-25**; only the round-112 numerical table `κ_rel(e): 1/3 → 0.4116`, `e: 0 → 0.961`, is available).",
    "> 📌 **N-42 re-check**: this `1/3` now **has a mechanism** (= the metric's own 2PN coefficient difference ÷ the 1PN slope), whereas the `s²` coefficient `1/3` of `Γ` comes from a Maxwellian angular average ⟹ **the mechanisms differ, so \"same origin\" remains forbidden**. ",
])
after_line(EN, "caliber note (round 112: D4", EN_N, "EN-1 round-113 note")

# ---------------- 2) 清单 ----------------
ROW = ("| **第 113 轮**（**I-24 执行**） | **I-24 部分结项：近圆极限的解析值 1/3 ＋ 机制分解** | "
       "第 112 轮登记的 **I-24**（`κ_rel(e)` 的解析式）。**结果**：① ⭐⭐⭐ **`κ_rel(e→0) = 1/3` 升为解析结论**"
       "（原为数值外推 0.33332，现差 1.3e-5）—— 方法 = 圆轨道**本轮频率比** `Γ ≡ ω_φ/ω_r`，进动 `= 2π(Γ−1)`；"
       "在 `y = M/p_areal` 下 `Γ_FW − 1 = 3y + 29/2·y² + 77y³`，`Γ_GR − 1 = 3y + 27/2·y² + 135/2·y³`；"
       "⟹ `κ_rel(0) = Δc₂/c₁ = 1/3`。② ⭐ **关键标定**：GR 侧**逐项复现精确闭式** `(1−6y)^{−1/2}−1` 到 `y³` ⟹ "
       "机器与 `ε↔y` 换式均正确（⚠️ 第一次换式**未生效**、`c₂` 错给 `10.5` 而非 `13.5` —— 靠闭式标定才发现）。"
       "③ ⭐ **机制**：只换一侧度规，`Δc₂` **严格可加分解**为 **`g_rr/g_θθ` 侧 `+1.25`** 与 **`g_tt` 侧 `−0.25`**"
       " ⟹ `κ = +5/12 − 1/12 = 1/3`（h 侧主导，f 侧抵消 20%）。④ **圆轨道修正** `κ_rel(y;e=0) = 1/3 + (5/3)y`"
       "（`y~0.01` 时 +1.7%）。⑤ ⚠️ **一般 e 的解析式仍未得**（两点积分全级数计算量过大，多次超时）⟹ 登记 **I-25**；"
       "现有仅第 112 轮数值表。⑥ **N-42 复核**：本项 `1/3` 现**有机制**（度规 2PN 系数差 / 1PN 斜率），"
       "与 `Γ` 的 `s²` 系数 `1/3`（Maxwell 角平均）**机制不同** ⟹ 「同源」仍禁止。⚠️ **论文中英各 1 处口径注**。 "
       "| 第 113 轮（`_i24_113.py` I24-1…I24-11，**13 项断言 0 失败**；计算 `_i24_a.py`／`_i24_fix.py`／`_i24_e.py`） | "
       "同 `I24结项_近圆极限的解析值与1_3的机制.md` |")
lines = rd(LIST).split("\n")
idx = [i for i, s in enumerate(lines) if s.startswith("| **第 107 轮**（**元任务 · 考古**）")]
if len(idx) == 1:
    lines[idx[0]:idx[0]] = ROW.split("\n")
    wr(LIST, "\n".join(lines))
    print("  [OK] L-1 零表第113轮行（行 " + str(idx[0] + 1) + "）")
else:
    BAD.append("L-1")
    print("  [XX] L-1 锚点 " + str(len(idx)) + " 次")

I24 = ("| **I-24** | ⭐⭐⭐ **`κ_rel(e→0) = 1/3` 的解析值与其机制（第 113 轮；部分结项）** | **难题（部分结项）** | "
       "**已解**：① 用**圆轨道本轮频率比** `Γ ≡ ω_φ/ω_r`（`ω_φ = L/ρ²`、`ω_r² = −V''_r/(2h)`、`V = E²/f − 1 − L²/ρ²`）"
       "解析展开，`y = M/p_areal` 下 `Γ_FW − 1 = 3y + 29/2·y² + 77y³`、`Γ_GR − 1 = 3y + 27/2·y² + 135/2·y³`"
       "（**GR 侧逐项等于精确闭式 `(1−6y)^{−1/2}−1`** ⟹ 机器与 `ε↔y` 换式标定通过）⟹ "
       "**`κ_rel(0) = Δc₂/c₁ = (29/2−27/2)/3 = 1/3`（精确有理数）**；② **机制**：`Δc₂` 严格可加分解 = "
       "**`g_rr/g_θθ` 侧 `+1.25`** ＋ **`g_tt` 侧 `−0.25`**（净 `1`）⟹ `κ = 5/12 − 1/12 = 1/3`；"
       "③ 圆轨道修正 `κ_rel = 1/3 + (5/3)y`。⚠️ **未解**：一般偏心率的解析式 ⟹ 见 **I-25**。 | "
       "第 113 轮（`_i24_a.py`／`_i24_fix.py`／`_i24_e.py`／`_i24_113.py`） | 同 `I24结项_…md` |")
I25 = ("| **I-25** | **`κ_rel(e)` 的一般解析式**（第 113 轮登记） | **难题（新登记）** | "
       "要算两点积分 `Δφ = 2∫_{u_a}^{u_p} du/√F`，`F = A·Hf(u) − B·h(u) − u²` 且 `(A,B)` 由端点 `F=0` 定"
       "（线性系统行列式 `~ 4ey` ⟹ 解含 `1/e` 但须在终式相消）。⚠️ 全级数化后 **sympy 计算量爆炸**（本轮多次超时）。"
       "**建议路线**：① 用 `(ū, a)` 的 **Lindstedt–Poincaré 平均法**只取共振项；② 或**数值 + 有理重构**"
       "（`κ_rel(e)` 拟合成有理函数再用高精度验证）。**验收标准**：`e→0` 必须回到 **1/3**，且与第 112 轮数值表"
       "逐点相符（≤1e-3）。 | 第 113 轮 | 同 `I24结项_…md`§六 |")
i42 = [i for i, s in enumerate(lines) if s.startswith("| **N-42** |")]
if len(i42) == 1:
    lines[i42[0] + 1:i42[0] + 1] = I24.split("\n") + I25.split("\n")
    wr(LIST, "\n".join(lines))
    print("  [OK] L-2 I-24 ＋ I-25（行 " + str(i42[0] + 2) + " 起）")
else:
    BAD.append("L-2")
    print("  [XX] L-2 锚点 " + str(len(i42)) + " 次")

# ---------------- 3) 交接说明 ----------------
PRI = ("0. 🎯 **当前建议（第 113 轮后）**：**I-24（第 112 轮登记）部分结项 —— 近圆极限 `κ_rel(e→0) = 1/3` 已解析**。"
       "⭐⭐⭐ 方法：圆轨道**本轮频率比** `Γ ≡ ω_φ/ω_r`（进动 `= 2π(Γ−1)`），`y = M/p_areal` 下 "
       "`Γ_FW − 1 = 3y + 29/2·y² + 77y³`、`Γ_GR − 1 = 3y + 27/2·y² + 135/2·y³` —— **GR 侧逐项等于精确闭式 "
       "`(1−6y)^{−1/2}−1`** ⟹ 机器与换式标定通过 ⟹ **`κ_rel(0) = Δc₂/c₁ = 1/3`（精确有理数）**；"
       "圆轨道修正 `1/3 + (5/3)y`。⭐ **机制**：`Δc₂` 严格可加 = **`g_rr/g_θθ` 侧 `+1.25`** ＋ **`g_tt` 侧 `−0.25`** "
       "⟹ `κ = 5/12 − 1/12 = 1/3`（h 侧主导、f 侧抵消 20%）。⚠️ **一般 e 的解析式仍未得**（两点积分全级数过大，多次超时）"
       "⟹ 登记 **I-25**（建议改用 L-P 平均法或数值+有理重构）。⚠️ **踩坑留痕**：`ε↔y` 换式第一次**未生效**"
       "（`h` 被当成与 `ε` 无关 ⟹ `c₂` 错给 `10.5` 而非 `13.5`）—— **只有靠精确闭式标定才发现** ⟹ "
       "**任何解析链都必须先用已知闭式标定**。📌 后续：I-25；EMRI 材料包数字重算（换 `κ_rel(e)`＋统一绝对/相对口径，"
       "需先清 **C-7/C-74**）；对外送私审／等 LISA。\n")
sub_once(HO, "0. 🎯 **当前建议（第 112 轮后）**", PRI + "\n0. 🎯 **（历史，第 112 轮后）**", "H-1 🎯 第113轮条目")

print("")
print("BAD = " + str(BAD))
