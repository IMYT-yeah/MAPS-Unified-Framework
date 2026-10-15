# -*- coding: utf-8 -*-
"""
第 87 轮补 补丁：把「(4,4,8) 到位 ＋ C-42（假判据被废）」写进
  论文 ZH / 论文 EN / 备忘录 / 清单
规则：① 锚点一律取**整行**；② 未命中即报错（不许静默失败）；③ 中文正文引号用「」『』。
"""
import io, sys

ZH = "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
MEMO = "h_min标度律的分组重拟合_两条方向相反的幂律与干净底本.md"
LIST = "工程期望清单.md"

FAIL = 0

def sub_once(path, old, new, tag):
    """整串替换，必须恰好命中 1 次。"""
    global FAIL
    t = io.open(path, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        print("  [FAIL] {}  命中 {} 次（应为 1）".format(tag, n))
        FAIL += 1
        return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new))
    print("  [PASS] {}  已替换".format(tag))

def ins_after_line(path, line_head, block, tag, lines_after=0):
    """在「以 line_head 开头的行」之后插入 block（block 自带前导换行）。"""
    global FAIL
    lines = io.open(path, encoding="utf-8").read().split("\n")
    idx = [i for i, s in enumerate(lines) if s.startswith(line_head)]
    if len(idx) != 1:
        print("  [FAIL] {}  锚行命中 {} 次（应为 1）".format(tag, len(idx)))
        FAIL += 1
        return
    i = idx[0] + 1 + lines_after
    lines[i:i] = block.split("\n")
    io.open(path, "w", encoding="utf-8").write("\n".join(lines))
    print("  [PASS] {}  已插入（行 {}）".format(tag, idx[0] + 1))

# ==================================================================== 1. 论文 ZH
print("=== 1. 论文 ZH ===")
ZH_BLOCK = """
>
> **【v2.9 补充（第 87 轮补：`h_min` 的**第二个样本外点**到位，并**废掉一个假判据**）】** 第 87 轮遗留的 **(4,4,8) N = 128 已算完**（脚本 `_gap_nondegen_87.py`）。⚠️ **首次跑挂的原因不是 GAP**，而是**折行修复只打在了直接调用路径上** —— `hn_stats` 复用第 48 轮的函数、**内部自己调**旧版逐行解析 ⟹ 采样阶段 `IndexError`；重绑 `globals()["orbit_via_gap"]` 后通过。核验脚本 `_scaling_extra_87.py`，**SE-1 … SE-4，8 项 0 失败**。
> · ✅ **(4,4,8) N = 128（退化方向 0）= 0.1103 ± 0.0021**（95% [0.1062, 0.1144]；S = 30，608 s；|G| = 1.47×10¹⁰⁷，单构型 |O| = 2.03×10³²）—— **组 B 拟合 `3.0887·N^{−0.6836}` 预测 0.1120 ⟹ 误差 −1.5%（|z| = 0.82）** ✓。
> · ⭐ **两个样本外点同号偏负**：(4,4,6) **−2.2%**（|z| = 1.13）、(4,4,8) **−1.5%**（|z| = 0.82）⟹ 组 B 的曲线在这两点上**都略高于实测**（系统性的 1–2%），不是随机涨落。
> · ⭐⭐ **拟合稳定性**：把两个样本外点并入后，组 B 由 **8 点**（`C = 3.0887、p = −0.6836`，残差 **2.2%**）变为 **10 点**（`C = 3.1423、p = −0.6884`，残差 **2.4%**）⟹ **指数只移动 0.70%** ⟹ **加两个独立新点不撬动拟合**。对照：混拟合 14 点 `p = −0.9642`、残差 **57.4%** —— 是组 B 的 **24 倍**。
> · ⚠️ ⭐⭐ **更正（C-42：第 87 轮用过的一个「判据」根本不是判据）**：第 87 轮的留一外推判据写作「**组 B 的外推误差 < 混合的外推误差**」。**把同一判据挪到 N = 128 上，结论翻转** —— 训练 N ≤ 96 时，**组 B**（`C = 3.1113、p = −0.6859`）预测 **0.1116**（误差 −1.2%），**混合**（`C = 16.1516、p = −1.0296`）预测 **0.1093**（误差 **+0.9%**，**反而更准**）⟹ **「谁的外推误差小」没有判别力**，它只是在**距离足够远**的点上碰巧成立。
> · ⭐⭐ **正确判据（本轮建立，可计算）**：设两模型在样本外点 N 上的预测之差为 `Δ`、该点的测量误差为 `σ_meas`，则**只有当 `Δ/σ_meas ≥ 2` 时该点才有判别力**：

>   | 目标点 | 距训练窗末端 | `Δ` | `σ_meas` | **判别力** |
>   |---|---|---|---|---|
>   | N = 128 | 1.33× | 0.0023 | 0.0021 | **1.09σ ⟹ 不可分** |
>   | N = 216 | 2.25× | 0.0142 | 0.0037 | **3.83σ ⟹ 可分** |

>   ⟹ **判别力 ∝ 样本外点到训练窗口末端的距离**。第 87 轮那条「好约 7 倍」的**有效结论只来自 N = 216**；(4,4,6) 与 (4,4,8) 两点**只证明「组 B 曲线在自身预测上成立」，不证明「组 B 优于混合」**。
> · ⚠️ **边界（如实登记）**：仍未在 N = 128 上找到「退化 ≥ 2」的对照点（(2,2,64) 的 GAP 规模过大）⟹ 只能说「组 B 曲线在无退化新点上成立」，**不能说「已排除 N 依赖」**。
> · 📌 **规范（第 87 轮补）**：**报样本外检验时，必须同时报「该点到训练窗的距离」与「两模型预测之差 ÷ σ_meas」** —— 只报「误差几个百分点」会掩盖「这个点其实什么都判不了」。"""

ins_after_line(ZH, "> · 📌 **规范（第 87 轮）**：**标度律拟合前先按「退化方向数」分组**",
               ZH_BLOCK, "ZH-1 第 87 轮补块")

# ==================================================================== 2. 论文 EN
print("=== 2. 论文 EN ===")
EN_BLOCK = """
>
> **【v2.9 supplement (round 87b: the **second out-of-sample point** for `h_min` has landed, and a **bogus criterion is retired**)】** The **(4,4,8) at N = 128** left over from round 87 has now been computed (script `_gap_nondegen_87.py`). ⚠️ **The first attempt did not fail because of GAP** — the line-folding fix had been applied **only to the directly-called path**, while `hn_stats` reuses a round-48 function that **calls the old line-by-line parser internally** ⟹ `IndexError` in the sampling stage; it passed after rebinding `globals()["orbit_via_gap"]`. Verification script `_scaling_extra_87.py`, **SE-1 … SE-4, 8 items, 0 failures**.
> · ✅ **(4,4,8) at N = 128 (0 degenerate directions) = 0.1103 ± 0.0021** (95% [0.1062, 0.1144]; S = 30, 608 s; |G| = 1.47×10¹⁰⁷, single configuration |O| = 2.03×10³²) — **group B's fit `3.0887·N^{−0.6836}` predicts 0.1120 ⟹ error −1.5% (|z| = 0.82)** ✓.
> · ⭐ **Both out-of-sample points are low by the same sign**: (4,4,6) **−2.2%** (|z| = 1.13), (4,4,8) **−1.5%** (|z| = 0.82) ⟹ group B's curve sits **slightly above** the measurements at both points (a systematic 1–2%), not a random fluctuation.
> · ⭐⭐ **Fit stability**: after absorbing both out-of-sample points, group B goes from **8 points** (`C = 3.0887, p = −0.6836`, residual **2.2%**) to **10 points** (`C = 3.1423, p = −0.6884`, residual **2.4%**) ⟹ **the exponent moves by only 0.70%** ⟹ **two independent new points do not move the fit**. For contrast, the mixed 14-point fit gives `p = −0.9642` with a residual of **57.4%** — **24×** group B's.
> · ⚠️ ⭐⭐ **Correction (C-42: a "criterion" used in round 87 was never a criterion)**: round 87's leave-one-out criterion read "**group B's extrapolation error < the mixed fit's extrapolation error**". **Moving the same criterion to N = 128 flips the conclusion** — training on N ≤ 96, **group B** (`C = 3.1113, p = −0.6859`) predicts **0.1116** (error −1.2%) while **the mixed fit** (`C = 16.1516, p = −1.0296`) predicts **0.1093** (error **+0.9%**, i.e. **more accurate**) ⟹ **"whose extrapolation error is smaller" has no discriminative power**; it merely happens to hold at points that are far enough away.
> · ⭐⭐ **The correct criterion (established this round, computable)**: let `Δ` be the difference between the two models' predictions at the out-of-sample point N and `σ_meas` the measurement error there; then **the point has discriminative power only if `Δ/σ_meas ≥ 2`**:

>   | Target point | Distance beyond training window | `Δ` | `σ_meas` | **Discriminative power** |
>   |---|---|---|---|---|
>   | N = 128 | 1.33× | 0.0023 | 0.0021 | **1.09σ ⟹ not separable** |
>   | N = 216 | 2.25× | 0.0142 | 0.0037 | **3.83σ ⟹ separable** |

>   ⟹ **Discriminative power ∝ the distance of the out-of-sample point beyond the training window.** Round 87's "about 7× better" **is valid only for N = 216**; the (4,4,6) and (4,4,8) points **show only that "group B's curve holds at its own prediction", not that "group B beats the mixed fit"**.
> · ⚠️ **Boundary (recorded honestly)**: no "≥ 2 degenerate directions" control point at N = 128 has been found ((2,2,64) is too large for GAP) ⟹ one may only say "group B's curve holds on a new non-degenerate point", **not "N-dependence has been ruled out"**.
> · 📌 **Norm (round 87b)**: **when reporting an out-of-sample test, always report both "the distance of the point beyond the training window" and "the difference of the two models' predictions divided by σ_meas"** — reporting only "an error of a few percent" hides the fact that **the point can decide nothing at all**."""

ins_after_line(EN, "> · 📌 **Norm (round 87)**: **group by the number of degenerate directions before fitting a scaling law**",
               EN_BLOCK, "EN-1 第 87 轮补块")

# ==================================================================== 3. 备忘录
print("=== 3. 备忘录 ===")
sub_once(MEMO,
"""⟹ 两条判据同时通过：**组 B 的标度律在新点上成立**，且**「0 个 ≈ 1 个」再次被支持**。

⚠️ **(4,4,8) N = 128 未完成**：首次尝试命中「**GAP 对超长整数折行**」这个已知坑
（`_gap_shape_48.py` 的 `orbit_via_gap` 用逐行解析 ⟹ `IndexError`）；
已在 `_gap_nondegen_87.py` 改用 `_gap.py` 的折行安全解析 `_parse_markers`，重跑中。""",
"""⟹ **两条判据同时通过**：**组 B 的标度律在新点上成立**，且**「0 个 ≈ 1 个」再次被支持**。
⚠️ **但「同时通过」不等于「这个点有判别力」** —— 见下方 §五·补（第 87 轮补：C-42）。

### 五·补 ✅ **(4,4,8) N = 128 已算完**（第 87 轮补，脚本 `_gap_nondegen_87.py`）

> **(4,4,8) N = 128（退化方向 0）⟹ H/N = 0.1103 ± 0.0021**（95% [0.1062, 0.1144]）
> ｜`|G| = 1.47×10¹⁰⁷`（108 位十进制）｜单构型 `|O| = 2.03×10³²`｜S = 30，608 s

- 组 B（8 点）预测 `3.0887·128^{−0.6836}` = **0.1120** ⟹ 实测 0.1103，**误差 −1.5%（|z| = 0.82）** ✓
- ⭐ **两个样本外点同号偏负**：(4,4,6) **−2.2%**、(4,4,8) **−1.5%** ⟹ 曲线在两点上都**略高于**实测（系统性 1–2%）

⚠️ **第 87 轮首次跑挂的真实原因（不是 GAP，是我自己）**：折行修复**只打在了直接调用路径**上 ——
`hn_stats` 复用第 48 轮的函数、**内部自己调**旧版逐行解析 ⟹ 采样阶段原样 `IndexError`。
修法：`globals()["orbit_via_gap"] = orbit_via_gap_safe`（函数体对全局名的查找是**运行时**的）。
⟹ **教训：改了函数 A，还要问「谁在内部调 A」；只修调用点 = 假修复。**（已登记技能陷阱 80）

---

## 五·补二 ⚠️⭐⭐ **C-42：第 87 轮用过的一个「判据」根本不是判据**

**第 87 轮的写法**：留一外推判据 = 「**组 B 的外推误差 < 混合的外推误差**」（在 N = 216 上是 +1.7% vs −12.6% ⟹ 好约 7 倍）。

**本轮把它挪到 N = 128**（同一训练窗口 N ≤ 96），**结论翻转**：

| 训练 N ≤ 96 | C | p | 预测 N = 128 | 实测 | 误差 |
|---|---|---|---|---|---|
| **组 B** | 3.1113 | −0.6859 | **0.1116** | 0.1103 | **−1.2%** |
| **混合** | 16.1516 | −1.0296 | **0.1093** | 0.1103 | **+0.9%** ← **混合反而更准** |

⟹ **「谁的外推误差小」没有判别力** —— 它只是在**距离足够远**的点上碰巧成立。

### ✅ **正确的判据（可计算）**

> 设两模型在样本外点 N 上的预测之差为 `Δ`、该点的测量误差为 `σ_meas`，
> 则**只有当 `Δ / σ_meas ≥ 2` 时，该点才有判别力**。

| 目标点 | 距训练窗末端 | `Δ` | `σ_meas` | **判别力** |
|---|---|---|---|---|
| **N = 128** | 1.33× | 0.0023 | 0.0021 | **1.09σ ⟹ 不可分** |
| **N = 216** | 2.25× | 0.0142 | 0.0037 | **3.83σ ⟹ 可分** |

⟹ ⭐⭐ **判别力 ∝ 样本外点到训练窗口末端的距离**。
⟹ 第 87 轮那条「好约 7 倍」的**有效结论只来自 N = 216**；
   **(4,4,6) 与 (4,4,8) 两点只证明「组 B 曲线在自身预测上成立」，不证明「组 B 优于混合」**。
⟹ ⚠️ **这一条不是把第 87 轮的结论推翻**（组 A / 组 B 分组本身仍成立，判据仍是**残差 ＋ 机制 ＋ 留一外推三合一**），
   而是**收回其中「新点也支持了组 B 优于混合」这个读法**。

### ⭐ 拟合稳定性（并入两个样本外点）

| 点集 | 点数 | C | p | 最大残差 |
|---|---|---|---|---|
| 组 B（底本） | 8 | 3.0887 | −0.6836 | 2.2% |
| **组 B ＋ 两个样本外点** | **10** | **3.1423** | **−0.6884** | **2.4%** |
| 混合（组 A 4 ＋ 组 B 10） | 14 | 12.4537 | −0.9642 | **57.4%** |

⟹ **指数只移动 0.70%** ⟹ 加两个独立新点**不撬动拟合**；混合拟合残差是组 B 的 **24 倍**。

### 📌 规范（第 87 轮补）

**报样本外检验时，必须同时报「该点到训练窗的距离」与「两模型预测之差 ÷ σ_meas」** ——
只报「误差几个百分点」会掩盖「**这个点其实什么也判不了**」。""",
"MEMO-1 §五 更新 ＋ 新增 §五·补 / §五·补二")

sub_once(MEMO,
"""  - ⭐⭐ **样本外新点 (4,4,6) = 0.1333**（对组 B 的独立验证）""",
"""  - ⭐⭐ **样本外新点 (4,4,6) = 0.1333**（对组 B 的独立验证）
  - ⭐⭐ **样本外新点 (4,4,8) = 0.1103**（**第二个**样本外点，−1.5% ✓；第 87 轮补）
  - ⚠️⭐⭐ **C-42：撤回「新点也证明组 B 优于混合」这个读法**（判别力判据 `Δ/σ_meas ≥ 2`；N=128 处只 1.09σ）""",
"MEMO-2 §八 净增量")

sub_once(MEMO,
"""- 总账：**更正 39 → 40**；**负面条数不变**（本轮**没有新的负面判定**，也**未推翻任何已有结论**）""",
"""- 总账：**更正 39 → 40**（第 87 轮）**→ 41**（第 87 轮补：C-42）；**负面条数不变**（两轮**均无新的负面判定**，也**未推翻任何已有结论**）""",
"MEMO-3 §八 总账")

sub_once(MEMO,
"""5. **(4,4,8) 未完成**（折行坑已修，重跑中）⟹ 若它给出与组 B 预测显著不同的值，本条的拟合需重审。""",
"""5. ~~**(4,4,8) 未完成**（折行坑已修，重跑中）⟹ 若它给出与组 B 预测显著不同的值，本条的拟合需重审。~~
   ✅ **第 87 轮补已完成**：**(4,4,8) N = 128 = 0.1103 ± 0.0021**，对组 B 预测 0.1120 的误差 **−1.5%** ⟹ **拟合无需重审**（并入后 p 只移动 0.70%）。
6. ⚠️ **两个样本外点都只有「低 1–2%」的量级，且都落在 2σ 内** ⟹ 它们**足以**验证「组 B 曲线自身成立」，
   **不足以**判定「组 B 优于混合」（判别力判据：N = 128 处仅 **1.09σ**）⟹ 见 **C-42**。
7. ⚠️ **仍未在 N = 128 上找到「退化 ≥ 2」的对照点**（(2,2,64) 的 GAP 规模过大）
   ⟹ 只能说「组 B 曲线在**无退化**新点上成立」，**不能说「已排除 N 依赖」**。""",
"MEMO-4 §九 诚实边界")

# ==================================================================== 4. 清单
print("=== 4. 清单 ===")
C42 = "| **C-42** | **「外推误差更小」不是判别性检验（第 87 轮的留一外推判据）** | **更正 / 收紧** | 第 87 轮把「**组 B 的外推误差 < 混合的外推误差**」当判据（在 N = 216 上 +1.7% vs −12.6%）。**本轮把它挪到 N = 128，结论翻转** —— 训练 N ≤ 96 时：**组 B** 预测 0.1116（误差 −1.2%）、**混合** 预测 0.1093（误差 **+0.9%**，**反而更准**）⟹ **该判据没有判别力**，只在距离足够远的点上碰巧成立。⭐ **正确判据（可计算）**：两模型预测之差 `Δ` ÷ 该点测量误差 `σ_meas` **必须 ≥ 2** —— 实测 **N = 128 处 1.09σ（不可分）**、**N = 216 处 3.83σ（可分）** ⟹ **判别力 ∝ 样本外点到训练窗末端的距离**。⟹ 第 87 轮「好约 7 倍」**只对 N = 216 有效**；(4,4,6) / (4,4,8) **只证明「组 B 曲线在自身预测上成立」**（−2.2% / −1.5%，均落 2σ 内）。⚠️ **第 87 轮的分组本身不撤回**。 | 第 87 轮补（`_scaling_extra_87.py` SE-1…SE-4） | 技能陷阱 81 |"
ins_after_line(LIST, "| **C-41** |", C42, "LIST-1 新增 C-42 行")
sub_once(LIST,
"""| **撤回 / 更正** | **40 条**（**C-41 ⭐""",
"""| **撤回 / 更正** | **41 条**（**C-42 ⭐ 样本外检验的判别力判据**（第 87 轮补：「外推误差更小」**不是**判别性检验 —— 在 N = 128 上混合拟合反而更准（+0.9% vs −1.2%）；正确判据 `Δ/σ_meas ≥ 2`，实测 **1.09σ**（N=128，不可分）vs **3.83σ**（N=216，可分）⟹ **判别力 ∝ 距离训练窗的远近**）｜**C-41 ⭐""",
"LIST-2 总账 40 → 41")

print()
print("=" * 70)
print("PATCH 87b DONE  FAIL = {}".format(FAIL))
print("=" * 70)
