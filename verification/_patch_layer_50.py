# -*- coding: utf-8 -*-
"""第 50 轮论文补丁（中英同步）。

三类改动：
  A. **更正第 48 轮的一处口径错误**：(2,2,6) k=12 的 H/N 0.4510 → 0.4334（共 6 处）
     并说明"第 48 轮那次更正同时换掉了平均口径"。
  B. 修掉第 49 轮留在论文里的**断行残片**（第 48 轮的"下一步"行被第 49 轮块劈成两半，
     后半截落在块尾且丢了 ">" 前缀）。
  C. 在第 49 轮块之后插入【第 50 轮】块。

锚点用「整行长锚点 + 命中次数必须为 1」的写法（本轮替换的都是很长的整行 ⟹ 唯一性有保障）。
"""

import io
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")

OK = [0]
FAIL = [0]


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        FAIL[0] += 1
        print("  [XX] {:<34} 命中 {} 次 —— 拒绝".format(tag, n))
        return False
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    OK[0] += 1
    print("  [OK] {:<34} 已改".format(tag))
    return True


# ------------------------------------------------------------------ 备份
os.makedirs(HIST, exist_ok=True)
for src, dst in ((ZH, "论文初稿_正反物质对风暴统一框架_v2.9.md_备份_2026-09-23第50轮前.md"),
                 (EN, "Paper_MatterAntimatterPairStorm_v2.9_EN.md_备份_2026-09-23第50轮前.md")):
    shutil.copy2(src, os.path.join(HIST, dst))
    print("  备份 → {}".format(dst))

print()
print("=== A. 更正第 48 轮的口径错误（中文 6 处）===")

# A1  第 46 轮块表格
sub_once(ZH,
         "| (2,2,6) | 24 | 2 704 156 | 648 | 6 334 | 1 050 | ❌ 不完备 | 0.2421 | **0.4510** |",
         "| (2,2,6) | 24 | 2 704 156 | 648 | 6 334 | 1 050 | ❌ 不完备 | 0.2421 | **0.4334**（第 50 轮更正，原报 0.4510） |",
         "ZH-A1 第46轮块表格行")

# A2  第 46 轮块判决 3
sub_once(ZH,
         "更正后：0.4679 ⟶ 0.4335 ⟶ **0.4510** ⟶ **0.4617** ⟶ **0.5307**（N=64））",
         "更正后：0.4679 ⟶ 0.4335 ⟶ **0.4334**（第 50 轮更正）⟶ **0.4617** ⟶ **0.5307**（N=64））",
         "ZH-A2 第46轮块判决3数列")

# A3  第 47 轮块表格
sub_once(ZH,
         "| (2,2,6) | 24 | 7 | 6.48×10² | 0.2697 | **0.4510**（精；第 48 轮更正，原 0.4330） |",
         "| (2,2,6) | 24 | 7 | 6.48×10² | 0.2697 | **0.4334**（精；**第 50 轮更正** —— 第 48 轮报的 0.4510 系**口径错误**） |",
         "ZH-A3 第47轮块表格行")

# A4  第 47 轮块判决 2
sub_once(ZH,
         "(2,2,L) 系列给 0.4679（N=8）⟶ 0.4335（N=16）⟶ **0.4510**（N=24）⟶ **0.4617**（N=32）。",
         "(2,2,L) 系列给 0.4679（N=8）⟶ 0.4335（N=16）⟶ **0.4334**（N=24；第 50 轮更正）⟶ **0.4617**（N=32）。",
         "ZH-A4 第47轮块判决2数列")

# A5  第 47 轮块方法自校验
sub_once(ZH,
         "⚠️ **第 48 轮更正**：0.4330 与 0.4343 都基于**错误的生成元集**；更正后该行精确值为 **0.4510**。",
         "⚠️ **第 48 轮更正**：0.4330 与 0.4343 都基于**错误的生成元集**；更正后该行精确值为 **0.4334**"
         "（⚠️ **第 50 轮查明**：第 48 轮那次更正**同时换掉了平均口径** —— 它用的是「轨道等权」`Σ_o ln|O_o| / #轨道`，"
         "而第 40 轮 `part_entropy` 的定义是**构型等权** `H = lnM − Σ_o (|O_o|/M)·ln|O_o|`；"
         "两者在 (2,2,6) 上差 **0.0176**，而生成元错误的真实影响只有 **0.0004** ⟹ 那次报的 0.0176 全部来自口径）。",
         "ZH-A5 第47轮块方法自校验")

# A6  第 48 轮块更正后的曲线
sub_once(ZH,
         "(2,2,6) N=24 由 **0.4330 → 0.4510**（精确划分；轨道数 6224 → 6334）",
         "(2,2,6) N=24 由 0.4330 → **0.4334**（精确划分；轨道数 6224 → 6334）"
         "〔⚠️ 第 50 轮更正：第 48 轮曾报 0.4510，系混入「轨道等权」口径〕",
         "ZH-A6 第48轮块更正曲线")

print()
print("=== A'. 英文版同 6 处 ===")
sub_once(EN,
         "| (2,2,6) | 24 | 2 704 156 | 648 | 6 334 | 1 050 | ❌ incomplete | 0.2421 | **0.4510** |",
         "| (2,2,6) | 24 | 2 704 156 | 648 | 6 334 | 1 050 | ❌ incomplete | 0.2421 | **0.4334** (corrected in round 50; 0.4510 as reported) |",
         "EN-A1 round-46 table")
sub_once(EN,
         "(corrected: 0.4679 ⟶ 0.4335 ⟶ **0.4510** ⟶ **0.4617** ⟶ **0.5307** at N=64)",
         "(corrected: 0.4679 ⟶ 0.4335 ⟶ **0.4334** (round 50) ⟶ **0.4617** ⟶ **0.5307** at N=64)",
         "EN-A2 round-46 verdict 3")
sub_once(EN,
         "| (2,2,6) | 24 | 7 | 6.48×10² | 0.2697 | **0.4510** (exact; corrected in round 48, was 0.4330) |",
         "| (2,2,6) | 24 | 7 | 6.48×10² | 0.2697 | **0.4334** (exact; **corrected in round 50** — the 0.4510 of round 48 was a **caliber error**) |",
         "EN-A3 round-47 table")
sub_once(EN,
         "the (2,2,L) family gives 0.4679 (N=8) ⟶ 0.4335 (N=16) ⟶ **0.4510** (N=24) ⟶ **0.4617** (N=32).",
         "the (2,2,L) family gives 0.4679 (N=8) ⟶ 0.4335 (N=16) ⟶ **0.4334** (N=24, round 50) ⟶ **0.4617** (N=32).",
         "EN-A4 round-47 verdict 2")
sub_once(EN,
         "the corrected exact value is **0.4510**.",
         "the corrected exact value is **0.4334** "
         "(⚠️ **established in round 50**: that round-48 correction **also swapped the averaging caliber** — it used "
         "the orbit-average `Σ_o ln|O_o| / #orbits`, whereas the round-40 `part_entropy` definition is the "
         "**configuration-weighted** `H = ln M − Σ_o (|O_o|/M)·ln|O_o|`; the two differ by **0.0176** at (2,2,6), "
         "while the generator error itself was worth only **0.0004** ⟹ the reported 0.0176 came entirely from the caliber).",
         "EN-A5 round-47 method self-check")
sub_once(EN,
         "for (2,2,6) at N=24 the H/N changes from **0.4330 → 0.4510** (exact partition; #orbits 6224 → 6334)",
         "for (2,2,6) at N=24 the H/N changes from 0.4330 → **0.4334** (exact partition; #orbits 6224 → 6334) "
         "[⚠️ corrected in round 50: round 48 had reported 0.4510, a caliber slip]",
         "EN-A6 round-48 corrected curve")

print()
print("=== B. 修断行残片 ===")
# 中文：466（第 48 轮的"下一步"开头）被第 49 轮块劈开，后半截是 478
# ⚠️ 顺序要紧：先**清除**残片，再**补全** 466 —— 否则补全后的文本会让残片锚点命中两次
sub_once(ZH,
         "（GAP 让这成为常规计算：全脚本约 76 s）；② **检验「退化方向数」判据** —— (2,6,6) 应与 (2,4,4) 同类、(6,6,6) 应与 (4,4,4) 同类。",
         "",
         "ZH-B1 清除孤立残片")
sub_once(ZH,
         "> 🔧 **下一步（两条都可证伪）**：① 在 N=32/64/128 上补形状，定位 **0.25 的跨点**",
         "> 🔧 **下一步（两条都可证伪）**：① 在 N=32/64/128 上补形状，定位 **0.25 的跨点**"
         "（GAP 让这成为常规计算：全脚本约 76 s）；② **检验「退化方向数」判据** —— "
         "(2,6,6) 应与 (2,4,4) 同类、(6,6,6) 应与 (4,4,4) 同类。",
         "ZH-B2 修复第48轮下一步断行")
# 英文
sub_once(EN,
         " (GAP makes this routine: the whole script takes ≈76 s); ② **test the \"number of degenerate directions\" criterion** — (2,6,6) should behave like (2,4,4) and (6,6,6) like (4,4,4).",
         "",
         "EN-B1 clear orphan fragment")
sub_once(EN,
         "> 🔧 **Next (both falsifiable)**: ① add shapes at N=32/64/128 to locate **the crossing point of 0.25**",
         "> 🔧 **Next (both falsifiable)**: ① add shapes at N=32/64/128 to locate **the crossing point of 0.25** "
         "(GAP makes this routine: the whole script takes ≈76 s); ② **test the \"number of degenerate directions\" "
         "criterion** — (2,6,6) should behave like (2,4,4) and (6,6,6) like (4,4,4).",
         "EN-B2 fix round-48 next-line split")

print()
print("=== C. 插入第 50 轮块 ===")

ZH_ANCHOR = ("> 🔧 **下一步**：① 在 N = 32–48 之间加密（(4,6,4) / (6,6,4) 等），把跨点区间收窄；"
             "② 在 N = 96 上补第三个形状，量化「形状修正」的量级；③ (6,6,6) 单次 200 s ⟹ 性价比低，暂缓。")
ZH_BLOCK = """> **【v2.9 补充（第 50 轮：改扫占据数层 k —— 对称性严格成立，并查出第 48 轮一处口径错误）】** 上一条要求「先想清楚口径再算」。本轮换参数化（固定 N、扫 k），三项结果中**第三项是对上一条自身表格的更正**。
>
> · **h(k) = h(N−k) 严格成立**（N=8 的 5 对、N=16 的 9 对，逐位相等，差 = 0）。机制：补集映射 c ↦ ~c 与每个置换群元素对易 ⟹ 轨道大小不变 ⟹ 只需扫 k ≤ N/2。
> · **h 不只依赖 k/N**（否证「占据分数决定一切」）：把三条曲线按 x = k/N 叠起来，同 x 上跨 N 的最大差 **0.0953**（x = 1/8 处）。原因：**k = 1 层群在单点上可迁**（|O| = N）⟹ 该层 H/N = ln2 − lnN/N，**显式含 N**（8/16/24 三层精确验证，差 < 1e−15）。
> · **小 N 上任何层都够不到 0.25**：min_k H/N = 0.4332 / 0.4292 / 0.4328（N = 8 / 16 / 24，**全层精确枚举**）⟹ 「扫 k 能收窄跨点」只在 N ≥ 48 一侧成立。N=48 的 k_c = 18.10（k_c/N = 0.377）、N=64 的 k_c = 18.48（k_c/N = 0.289）⟹ **k_c/N 随 N 下降** ⟹ k 不提供独立自由度。
> · ⚠️ **对第 48 轮一处数值的更正（本轮最重要）**：**(2,2,6) k=12 的 H/N 应为 0.4334，不是 0.4510**。原因：第 48 轮那次更正**同时换掉了平均口径** —— `_fix_run_48.py` 用「轨道等权」`Σ_o ln|O_o| / #轨道`，而第 40 轮 `part_entropy` 的定义是**构型等权** `H = lnM − Σ_o (|O_o|/M)·ln|O_o|`。本轮同时算两种口径：N=8 差 −0.0520、N=16 差 −0.0318、N=24 差 **−0.0176**，且 **0.4510 恰是 h_orb 那一列**（逐位相同）。**生成元错误的真实影响只有 0.0004**（0.4330 → 0.4334）。GAP 独立复核（随机构型采样，S=40）给 0.4314 ± 0.0032 ⟹ 与 0.4334 一致、远离 0.4510。
> · **未受影响**：第 47/48/49 轮的**全部 GAP 结果**（(2,4,L)、(4,4,L)、(6,6,6)）—— 随机构型采样本身就是构型等权；第 46 轮的 Python 结果也是构型等权。**只有第 48 轮那一个脚本错了口径。**
> · **由此「≥2 个 L=2 方向」族曲线要更正**：0.4679（N=8）⟶ 0.4335（16）⟶ **0.4334**（24，原报 0.4510）⟶ 0.4617（32）⟶ 0.4802（40）⟶ … ⟹ 该族**不是**从 N=16 起单调上升，而是先在 N=16/24 处**平台/浅谷**，自 N ≥ 24 起才上升。「升 / 降」的**方向结论不变**；「≤1 个」族全部来自 GAP ⟹ 不受影响。
> · **h_min(N)（k = N/2）的标度律**（9 个 GAP 数据点，N ∈ [32, 216]，跨 6.75 倍）：拟合 `h_min = C·N^p` 给 **C = 3.01、p = −0.6762**（最大残差 **2.6%**）；留一外推（只用 N ≤ 96）预测 N = 216 为 0.0828，实测 0.0779（误差 **+6.3%**）。⚠️ 这是**拟合，不是推导**；C ≈ 2.9 **无机制**，按本项目铁律**不得作证据、不得写进正文**（仅登记候选池）。
> · **大 N 上 H/N(k) 无真振荡**：N=48 用 S=30 重扫 k = 12…24，相邻层跳变**全部落在 2σ 内**（0 处超过）⟹ 第 48 轮 S=8 时看到的起伏是采样噪声。**小 N（精确）确实有微小非单调**（N=24：k=11 的 0.4328 < k=12 的 0.4334，差 0.0006）。
> ⚠️ **诚实边界**：k 的物理相关值应是 **k = N/2**（等分账 ⟹ 均匀分布 ⟹ 典型构型是半满）⟹ **k 不是可调参数**，本轮只提供结构信息，**没有**为 0.25 提供新自由度；k_c 只有两个 N（48、64）且依赖 GAP 采样（S = 30 / 10）；标度律**无机制**；N ≥ 128 未做。
> 🔧 **下一步**：三个「扫参数」方向（N、k、形状）都已扫过，0.25 的命中都只是**曲线穿过**，无一处给出机制 ⟹ **该转向机制一侧**：检查 B5 的「每 4l_P² 取 1 纳特」是否隐含一个特定的 N 或 k；若无，则 0.25 与本框架的衬底之间**根本不存在定量联系**（这是一个可以写清的负面结论）。"""

sub_once(ZH, ZH_ANCHOR, ZH_ANCHOR + "\n" + ZH_BLOCK, "ZH-C 插入第50轮块")

EN_ANCHOR = ("> 🔧 **Next**: ① densify between N = 32 and 48 ((4,6,4), (6,6,4), …) to narrow the bracket; "
             "② add a third shape at N = 96 to quantify the size of the \"shape correction\"; "
             "③ (6,6,6) costs ≈200 s per sample ⟹ poor value for money, deferred.")
EN_BLOCK = """> **【v2.9 supplement (round 50: scanning the occupation layer k — the symmetry holds exactly, and a caliber error in round 48 is uncovered)】** The previous block asked for the caliber to be settled first. This round re-parameterises (fix N, scan k). Of the three results, **the third corrects the previous block's own tables**.
>
> · **h(k) = h(N−k) holds exactly** (all 5 pairs at N=8 and all 9 pairs at N=16 agree digit for digit). Mechanism: the complement map c ↦ ~c commutes with every group element ⟹ orbit sizes are preserved ⟹ only k ≤ N/2 needs scanning.
> · **h is not a function of k/N alone** (refuting "the occupation fraction decides everything"): overlaying the three curves on x = k/N, the largest cross-N spread is **0.0953** (at x = 1/8). Reason: the **k = 1 layer is transitive on single sites** (|O| = N) ⟹ its H/N = ln2 − lnN/N, which **depends on N explicitly** (verified exactly at N = 8/16/24, discrepancy < 1e−15).
> · **At small N no layer reaches 0.25**: min_k H/N = 0.4332 / 0.4292 / 0.4328 (N = 8 / 16 / 24, **every layer enumerated exactly**) ⟹ "scanning k narrows the crossing point" holds only for N ≥ 48. For N=48, k_c = 18.10 (k_c/N = 0.377); for N=64, k_c = 18.48 (k_c/N = 0.289) ⟹ **k_c/N falls with N** ⟹ k supplies no independent degree of freedom.
> · ⚠️ **A numerical correction to round 48 (the most important item here)**: **(2,2,6) at k=12 gives H/N = 0.4334, not 0.4510**. Cause: that round-48 correction **also swapped the averaging caliber** — `_fix_run_48.py` used the orbit average `Σ_o ln|O_o| / #orbits`, whereas the round-40 `part_entropy` definition is the **configuration-weighted** `H = ln M − Σ_o (|O_o|/M)·ln|O_o|`. Computing both here: N=8 differs by −0.0520, N=16 by −0.0318, N=24 by **−0.0176**, and **0.4510 is exactly the h_orb column** (digit for digit). **The generator error itself was worth only 0.0004** (0.4330 → 0.4334). An independent GAP check (random configuration sampling, S=40) gives 0.4314 ± 0.0032 ⟹ consistent with 0.4334 and far from 0.4510.
> · **Unaffected**: **all GAP results of rounds 47/48/49** ((2,4,L), (4,4,L), (6,6,6)) — sampling random configurations is itself configuration-weighted; the round-46 Python results are configuration-weighted too. **Only that single round-48 script had the wrong caliber.**
> · **Hence the "≥ 2 length-2 directions" curve must be corrected**: 0.4679 (N=8) ⟶ 0.4335 (16) ⟶ **0.4334** (24, reported 0.4510) ⟶ 0.4617 (32) ⟶ 0.4802 (40) ⟶ … ⟹ that family does **not** rise monotonically from N=16; it has a **plateau/shallow dip** at N = 16/24 and rises only from N ≥ 24. The **direction** of the "rising / falling" claim is unchanged; the "≤ 1 direction" family comes entirely from GAP ⟹ unaffected.
> · **Scaling law of h_min(N) (at k = N/2)** (9 GAP points, N ∈ [32, 216], spanning 6.75×): fitting `h_min = C·N^p` gives **C = 3.01, p = −0.6762** (max residual **2.6%**); leave-one-out (fitting only N ≤ 96) predicts 0.0828 at N = 216 against the measured 0.0779 (error **+6.3%**). ⚠️ This is a **fit, not a derivation**; C ≈ 2.9 has **no mechanism** and, per this project's rules, **must not be used as evidence or written into the body text** (registered in the candidate pool only).
> · **No genuine oscillation in H/N(k) at large N**: rescanning N=48 over k = 12…24 with S=30, every adjacent-layer jump lies **within 2σ** (0 exceedances) ⟹ the wiggles seen at S=8 in round 48 were sampling noise. **Small N (exact) does show a tiny genuine non-monotonicity** (N=24: 0.4328 at k=11 vs 0.4334 at k=12, a 0.0006 difference).
> ⚠️ **Honest limits**: the physically relevant value of k should be **k = N/2** (equipartition ⟹ uniform distribution ⟹ typical configurations are half-filled) ⟹ **k is not a tunable parameter**; this round supplies structural information only and **adds no new degree of freedom** for 0.25; k_c exists for only two values of N (48, 64) and depends on GAP sampling (S = 30 / 10); the scaling law has **no mechanism**; N ≥ 128 was not attempted.
> 🔧 **Next**: all three "scan-a-parameter" directions (N, k, shape) have now been scanned; every hit on 0.25 is merely a curve crossing, none supplies a mechanism ⟹ **the work should move to the mechanism side**: check whether B5's "1 nat per 4 l_P²" implies a particular N or k; if it does not, then **no quantitative link exists between 0.25 and this framework's substrate** — a negative conclusion that can be stated cleanly."""

sub_once(EN, EN_ANCHOR, EN_ANCHOR + "\n" + EN_BLOCK, "EN-C insert round-50 block")

print()
print("=" * 78)
print("补丁汇总：成功 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
