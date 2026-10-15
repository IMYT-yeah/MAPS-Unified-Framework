# -*- coding: utf-8 -*-
"""第 91 轮 补丁：C-46（正文级「预言」承诺句未带四类判定；1 处与 §9 冲突）"""
import io
ZH, EN = "论文初稿_正反物质对风暴统一框架_v2.9.md", "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
LIST = "工程期望清单.md"
FAIL = 0
def sub_once(path, old, new, tag):
    global FAIL
    t = io.open(path, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        print("  [FAIL] {}  命中 {} 次（应为 1）".format(tag, n)); FAIL += 1; return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    print("  [PASS] {}  已替换".format(tag))
def append_before(path, anchor, block, tag):
    global FAIL
    t = io.open(path, encoding="utf-8").read()
    if t.count(anchor) != 1:
        print("  [FAIL] {}  锚命中 {} 次".format(tag, t.count(anchor))); FAIL += 1; return
    io.open(path, "w", encoding="utf-8").write(t.replace(anchor, block + "\n\n" + anchor, 1))
    print("  [PASS] {}  已插入".format(tag))

# ---------------------------------------------------------------- 1. 修冲突（§5.3 第四代）
print("=== 1. 修 L920 / EN L938 的冲突 ===")
sub_once(ZH,
"第三代 n=3。**第四代预言**：n=4 涡在 z>1000 不稳定衰变，>1 TeV 极重极短命。",
"第三代 n=3。**第四代预言**：n=4 涡在 z>1000 不稳定衰变，>1 TeV 极重极短命。〔⚠️ **第 91 轮四类判定注**：**本条 = 失败** —— §9 表第 5 行对**同一命题**写的是「**与 LHC 未发现存在张力**」；本句原称「预言」而**无一字限定**。**引用本条时必须同时引 §9 第 5 行的状态**，否则等于把已被观测排除域的东西仍当预言卖。〕",
"ZH-1 第四代判定注")
sub_once(EN,
"third generation n=3. **Fourth-generation prediction**: n=4 vortices decay unstably at z>1000, extremely heavy and short-lived above 1 TeV.",
"third generation n=3. **Fourth-generation prediction**: n=4 vortices decay unstably at z>1000, extremely heavy and short-lived above 1 TeV. [⚠️ **Round-91 four-way-verdict note**: **this item = FAILED** — the §9 table's row 5 states, for **the same proposition**, \"**tension with LHC non-detection**\"; this sentence called it a \"prediction\" with **no qualifier at all**. **Any citation of this sentence must carry §9 row 5's status.**]",
"EN-1 fourth-generation note")

# ---------------------------------------------------------------- 2. 摘要指针
print("=== 2. 摘要 L29：加四类判定指针 ===")
sub_once(ZH,
"、SU(3) β 函数阶梯跳跃、纠缠熵面积律的 ln 2 因子。",
"、SU(3) β 函数阶梯跳跃、纠缠熵面积律的 ln 2 因子。〔⚠️ **第 91 轮注**：以上各项的**四类判定**（真预言 / postdiction / 半拟合 / 失败）见 §9 之后的两张台账；**本段约 12 项里此前只有 S-E5 一项带判定**。〕",
"ZH-2 摘要指针")
sub_once(EN,
"the SU(3) β-function staircase jump, and the ln 2 factor in the entanglement-entropy area law.",
"the SU(3) β-function staircase jump, and the ln 2 factor in the entanglement-entropy area law. [⚠️ **Round-91 note**: the **four-way verdicts** (true prediction / postdiction / half-fit / failed) for all items above are tabulated in the two ledgers after §9; **of the roughly 12 items in this paragraph, only S-E5 previously carried a verdict**.]",
"EN-2 abstract pointer")

# ---------------------------------------------------------------- 3. 正文级台账
print("=== 3. 追加正文级承诺句台账 ===")
ZH_B = """> **【v2.9 补标之二（第 91 轮：**正文级**「预言」承诺句的四类判定 —— 第 90 轮只做了 §9 表 23 行）】** 脚本 `_bodyclaim_91.py`（**BC-1…BC-5，0 失败**）。把全文含「预言」的 73 行按**正文 / 轮次块**二分（正文 30 / 块 43），再剔掉表行、索引行、变更记录行，得**正文级实质承诺句 21 行**，判定如下：
> | 位置 | 承诺句（简） | **四类判定** | 依据 |
> |---|---|---|---|
> | §4 概览 | 指数度规（PPN `γ=β=1` 其余全 0） | **postdiction** | **1PN 与 GR 不可区分** ⟹ 与 GR 同值 |
> | 摘要 | 「框架给出多项可检验预言」（约 12 项） | **混合（本轮前仅 1 项带判定）** | 见本表其余各行 |
> | 诚实声明 | v1.0 强场外推预言 | **失败（已撤回）** | 原文已标 |
> | §4.5b | β=1 通过 ／ β=1/2 被 **1600σ** 排除 | **postdiction ／ 失败（备选路径）** | 原文已标 |
> | §4.5b | 测地线 RK4 进动/偏折数值 | **推导 / 数值** | —— |
> | §4.6 | v1.1 修订：撤回「光子球 1GM vs 3GM」EHT 冲突预言 | **失败（已撤回）** | 原文已标 |
> | §4.6 | v1.15 单参数族 `α`（阴影 `b=5.196α·GM/c²` 等） | **半拟合** | `α` 是参数（框架称 `α=1` 由自洽性强制 ⟹ 未独立检验） |
> | §4.6 | 新预言：声速剖面 `c_s² = c²·sech²(ρ/ρ_P)` | **推导 / 数值** | 碎片-风暴碰撞动力学涌现 |
> | §4.6 | 过载区数值（`ρ_avg`、`P`、`c_s`） | **推导 / 数值** | —— |
> | §4.6 | 吸积盘辐射传输【引用 + 数值】 | **推导 / 数值** | —— |
> | §4.5b | 「有与观测相容的**几何预言**」 | **postdiction** | EHT **已观测** ⟹ 事后相容 |
> | §4.10 | 强场预言「见 §9 表」 | **索引**（非承诺） | —— |
> | §4.10 | **F4 发射层预言** `~√(l_P/R)` | **真预言** | 原初黑洞**未观测** |
> | **§5.3** | **「第四代预言」** | ⚠️ **失败（第 91 轮补标）** | **§9 第 5 行同命题 =「与 LHC 未发现存在张力」**；本句原**无一字限定** |
> | §8.2 | 诚实标注：`⟨f_space⟩` 式 | **半拟合（已标）** | 原文已标「拟合式而非预言」 |
> | §8.4 | void-CPT-κ 可检验预言 | **真预言** | 未观测（DES/Y3） |
> | §10.2 | 强场度规形式（开放问题 3） | **未定量 / 开放** | 原文标「✅ 已推进」 |
> | §10.2 | 统计→几何严格化（开放问题 4） | **推导 / 数值** | —— |
> | 版本沿革 | 各 `v1.xx 变更` 行 | **索引**（非承诺） | —— |
> | §8.2 末尾 | §8.2 修正（`f_space`） | **解释性（零预言力，已标）** | 原文已标 |
> · ⭐ **汇总（21 行，剔索引 3 行后 18 行）**：**真预言 2 ｜ postdiction 3 ｜ 半拟合 2 ｜ 失败 3 ｜ 推导 / 数值 5 ｜ 未定量 / 开放 1 ｜ 解释性 1 ｜ 混合 1（摘要）**。
> · ⚠️ **本轮修掉的冲突（C-46）**：**§5.3 的「第四代预言」与 §9 第 5 行的「与 LHC 未发现存在张力」是同一命题的两种表述** —— 正文称「预言」、表格称「失败」，**且中英对称地如此**（EN 亦写 `Fourth-generation prediction`）。已在本句加四类判定注。
> · ⚠️ **摘要级缺口**：摘要列出**约 12 项**预言，**此前只有 S-E5 一项带判定** —— 摘要是最先被读的部分，本轮加了指向前两张台账的指针。
> · 📌 **规范（第 91 轮）**：**正文里凡出现「预言 / 可检验 / 独有」字样的承诺句，必须能指到四类判定台账**；⚠️ **同一命题在「表」与「正文」两处表述必须一致**（本条与第 88 轮 C-43 同族）。"""

EN_B = """> **【v2.9 labelling II (round 91: **four-way verdicts for body-text** "prediction" claims — round 90 covered only the 23 rows of the §9 table)】** Script `_bodyclaim_91.py` (**BC-1 … BC-5, 0 failures**). The 73 lines containing "prediction" were split into **body (30) / round-blocks (43)**; after removing table rows, index lines and changelog lines, **21 substantive body claims** remain:
> | Location | Claim (abridged) | **Four-way verdict** | Rationale |
> |---|---|---|---|
> | §4 overview | exponential metric (PPN `γ=β=1`, rest 0) | **postdiction** | **1PN indistinguishable from GR** ⟹ same value as GR |
> | abstract | "the framework gives several testable predictions" (~12 items) | **mixed (only 1 carried a verdict before this round)** | see the remaining rows |
> | honesty declaration | v1.0 strong-field extrapolation prediction | **failed (withdrawn)** | already marked |
> | §4.5b | β=1 passes / β=1/2 excluded at **1600σ** | **postdiction / failed (the alternative)** | already marked |
> | §4.5b | geodesic RK4 precession/deflection numerics | **derivation / numerics** | — |
> | §4.6 | v1.1 revision: withdrawn "photon sphere 1GM vs 3GM" EHT-conflict prediction | **failed (withdrawn)** | already marked |
> | §4.6 | v1.15 one-parameter family `α` (shadow `b=5.196α·GM/c²`, …) | **half-fit** | `α` is a parameter (the framework claims `α=1` is forced by self-consistency ⟹ never tested independently) |
> | §4.6 | new prediction: sound-speed profile `c_s² = c²·sech²(ρ/ρ_P)` | **derivation / numerics** | emergent from debris-storm collision dynamics |
> | §4.6 | overload-region numerics (`ρ_avg`, `P`, `c_s`) | **derivation / numerics** | — |
> | §4.6 | accretion-disc radiative transfer [citation + numerics] | **derivation / numerics** | — |
> | §4.5b | "a **geometric prediction** compatible with observation" | **postdiction** | EHT **already observed** ⟹ a posteriori compatibility |
> | §4.10 | strong-field predictions "see the §9 table" | **index** (not a claim) | — |
> | §4.10 | **F4 emission-layer prediction** `~√(l_P/R)` | **true prediction** | primordial black holes **unobserved** |
> | **§5.3** | **"fourth-generation prediction"** | ⚠️ **failed (labelled this round)** | the §9 table's row 5 states, for **the same proposition**, "**tension with LHC non-detection**"; this sentence had **no qualifier** |
> | §8.2 | honesty note on the `⟨f_space⟩` formula | **half-fit (already marked)** | already marked "a fit, not a prediction" |
> | §8.4 | void-CPT-κ testable prediction | **true prediction** | unobserved (DES/Y3) |
> | §10.2 | strong-field metric form (open problem 3) | **not quantified / open** | marked "✅ advanced" |
> | §10.2 | statistics → geometry rigour (open problem 4) | **derivation / numerics** | — |
> | changelog | the various `v1.xx change` lines | **index** (not a claim) | — |
> | end of §8.2 | the §8.2 correction (`f_space`) | **interpretive (zero predictive power, already marked)** | already marked |
> · ⭐ **Tally (21 rows; 18 after removing 3 index rows)**: **true prediction 2 | postdiction 3 | half-fit 2 | failed 3 | derivation/numerics 5 | not quantified/open 1 | interpretive 1 | mixed 1 (abstract)**.
> · ⚠️ **The conflict fixed this round (C-46)**: **§5.3's "fourth-generation prediction" and §9 row 5's "tension with LHC non-detection" are two statements of the same proposition** — the body called it a "prediction", the table called it "failed", **and symmetrically in both languages** (EN also reads `Fourth-generation prediction`). A four-way-verdict note was added to that sentence.
> · ⚠️ **Abstract-level gap**: the abstract lists **roughly 12** predictions and **only S-E5 previously carried a verdict** — the abstract is the first thing a reader sees. A pointer to the two ledgers was added this round.
> · 📌 **Norm (round 91)**: **every body-text claim containing the words "prediction / testable / unique" must resolve to a four-way verdict ledger**; ⚠️ **the same proposition must not be described differently in the table and in the body** (same family as round 88's C-43)."""
append_before(ZH, "## 10 结论与开放问题", ZH_B, "ZH-3 正文级台账")
append_before(EN, "## 10 Conclusions and Open Problems", EN_B, "EN-3 正文级台账")

# ---------------------------------------------------------------- 4. 清单
print("=== 4. 清单 ===")
C46 = ("| **C-46** | **正文级「预言」承诺句未带四类判定；且 1 处与 §9 表冲突（第 91 轮）** | **更正 / 补标** | "
       "① ⚠️ **冲突（C-46 主体）**：**§5.3 的「第四代预言」与 §9 第 5 行的「与 LHC 未发现存在张力」是同一命题的两种表述** —— "
       "正文称「预言」、表格称「失败」，**且中英对称地如此**（EN 亦写 `Fourth-generation prediction`）⟹ 已加四类判定注。"
       "② 全文含「预言」的 **73 行**按正文/轮次块二分（**正文 30 / 块 43**），剔除表行/索引/变更记录后得 "
       "**正文级实质承诺句 21 行**，判定：**真预言 2｜postdiction 3｜半拟合 2｜失败 3｜推导/数值 5｜未定量·开放 1｜解释性 1｜混合 1（摘要）**。"
       "③ ⚠️ **摘要级缺口**：摘要列出**约 12 项**预言，**此前只有 S-E5 一项带判定** ⟹ 已加指向两张台账的指针。"
       "④ 📌 新规范：**正文里凡出现「预言/可检验/独有」的承诺句，必须能指到四类判定台账**。"
       " | 第 91 轮（`_bodyclaim_91.py` BC-1…BC-5） | 技能陷阱 85 |")
lines = io.open(LIST, encoding="utf-8").read().split("\n")
idx = [i for i, s in enumerate(lines) if s.startswith("| **C-45** |")]
if len(idx) != 1:
    print("  [FAIL] LIST-1  C-45 锚行命中 {} 次".format(len(idx))); FAIL += 1
else:
    lines[idx[0] + 1:idx[0] + 1] = [C46]
    io.open(LIST, "w", encoding="utf-8").write("\n".join(lines))
    print("  [PASS] LIST-1  C-46 行已插入（行 {}）".format(idx[0] + 2))
sub_once(LIST, "| **撤回 / 更正** | **44 条**（**C-45 ⭐",
         "| **撤回 / 更正** | **45 条**（**C-46 ⭐ 正文级「预言」承诺句未带四类判定 ＋ 1 处与 §9 表冲突**"
         "（第 91 轮：**§5.3「第四代预言」与 §9 第 5 行「与 LHC 未发现存在张力」是同一命题**，中英对称冲突；"
         "正文级承诺句 **21 行**补标；摘要 **约 12 项只有 1 项带判定**）｜**C-45 ⭐", "LIST-2 总账 44 → 45")

print()
print("=" * 60)
print("PATCH 91 DONE  FAIL = {}".format(FAIL))
print("=" * 60)
