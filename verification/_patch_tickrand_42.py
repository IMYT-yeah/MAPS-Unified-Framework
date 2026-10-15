# -*- coding: utf-8 -*-
"""
第 42 轮论文补丁（中英同步）。

一处：在 §8.6.7「诚实边界」表之前插入【v2.9 补充（第 42 轮：外生 tick 随机性 = 熵增的源头）】：
  · 每 tick 注入 ln3 + L²ln2 纳特的无知；
  · 达到视界 BH 熵只需 **π/ln2 = 4.532 tick ≈ 2.44×10⁻⁴³ s**（解析值）；
  · ⟹ 统计混合瞬时、空间输运很慢（47 μm/哈勃时），两者相差 ~10⁶⁰，**是两件事、不矛盾**
    （第 40 轮「等分账瞬时成立」由此获得动力学理由）；
  · 熵增上界 = ln|O|（容量不是瓶颈）；
  · ⚠️ T-7 判否：H1/H2 经验等价 ⟹ 「未来能否被预测」在框架内不可判定；现行表述下 = 不可预测。

锚点要求恰好命中一次。正文引号一律用「」。
"""

import io
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
STAMP = "2026-09-21第42轮前"

N_OK = [0]
N_FAIL = [0]


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<28} 命中 {} 次 —— 拒绝".format(tag, n))
        N_FAIL[0] += 1
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<28} 已改".format(tag))
    N_OK[0] += 1


print("备份：")
for src, dst in [
    (ZH, os.path.join(HIST, "论文初稿_v2.9_备份_%s.md" % STAMP)),
    (EN, os.path.join(HIST, "Paper_v2.9_EN_备份_%s.md" % STAMP)),
]:
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
        print("  [OK] {}".format(os.path.basename(dst)))
    else:
        print("  [--] {}（跳过）".format(os.path.basename(dst)))

ZH_A = "**【诚实边界（8.6.7）】**"
ZH_B42 = "\n".join([
    "**【v2.9 补充（第 42 轮：外生 tick 随机性 = 熵增的源头）】** "
    "本小节把 tick 的轴 / 相位取为随机。本轮把这件事的**定量后果**算出来：",
    "",
    "| 量 | 值 |",
    "|---|---|",
    "| 一次 tick 的选择数 | 3 轴 × 2^(L²)（L = 格点边长，线数 = L²） |",
    "| 每 tick 注入的无知 | `h = ln3 + L² ln2` 纳特/ tick |",
    "| 宏观值（L ≈ N_c = 8.4918×10⁶⁰） | `h = 4.998×10¹²¹` 纳特/ tick，`ḣ = h/t_P = 9.27×10¹⁶⁴` 纳特/秒 |",
    "| 视界 BH 熵 | `S_BH/k_B = πN_c² = 2.265×10¹²²` 纳特 |",
    "| **达到 S_BH 所需** | **`S_BH/h = π/ln2 = 4.532 tick ≈ 2.44×10⁻⁴³ s`（解析值）** |",
    "",
    "⟹ **统计混合是瞬时的**：系综熵在约 4.5 个普朗克时间内就达到视界的 BH 熵。"
    "这与 §4.2 ② 的空间输运（`R_mix(t_H) = 47 μm`，一个哈勃时才走这么远）**相差约 10⁶⁰ 倍** —— "
    "两者是**两件事**：一个是**信息的混合**，一个是**物质的输运**，并不矛盾。"
    "⟹ 这也给第 40 轮的「等分账瞬时成立 / 不需要热化」提供了**动力学理由**："
    "外生 tick 随机性在 ~4.5 tick 内就把系综带到等分。",
    "",
    "⚠️ **熵增的上界**：系综熵饱和于 `ln|O|`（轨道大小），而 "
    "`ln|O| ≤ ln C(N, N/2) ≈ 4.24×10¹⁸²` 纳特 ≫ `S_BH`（约 1.9×10⁶⁰ 倍）⟹ "
    "**容量不是瓶颈，速率才是**；饱和之后不再增长。",
    "",
    "⚠️ **T-7 的第一次判别（结论是否定的）**：tick 的随机性是「外生真随机」（H1）还是"
    "「更底层的确定性被粗粒化」（H2）？本轮给出：H2 需要把 tick 选择编码进衬底自身，"
    "其开销 =（tick 选择的比特数 ≈ L²）/（格点数 L³） = **1/L → 0**"
    "（宏观时 = 1.18×10⁻⁶¹ 比特/格点）⟹ **不与「0.25 纳特/l_P² 次二元」冲突** ⟹ "
    "**H1 与 H2 在可见衬底层面经验等价，不可判别**。"
    "⟹ 「未来是否原则上可预测」在本框架内**不可判定**；但在**现行表述（H1）**下答案明确："
    "**不可预测**（未来不是当前状态的函数）。",
    "",
    "⚠️ **与第 21 轮并存**：单个 tick 仍是双射 ⟹ **状态的信息严格守恒**；"
    "本轮算的是**系综（无知）熵**的增长。二者不矛盾——"
    "「无信息丢失」说的是状态，「熵增」说的是我们对状态的无知。",
    "",
])
sub_once(ZH, ZH_A, ZH_B42 + "\n" + ZH_A, "ZH §8.6.7 第 42 轮块")

EN_A = "**【Honest boundary (8.6.7)】**"
EN_B42 = "\n".join([
    "**【v2.9 supplement (round 42: the exogenous tick randomness is the source of entropy growth)】** "
    "This subsection takes the tick axis/phase to be random; this round computes the **quantitative "
    "consequence**:",
    "",
    "| Quantity | Value |",
    "|---|---|",
    "| Choices per tick | 3 axes × 2^(L²) (L = lattice side, #lines = L²) |",
    "| Ignorance injected per tick | `h = ln3 + L² ln2` nats/tick |",
    "| Macroscopic (L ≈ N_c = 8.4918×10⁶⁰) | `h = 4.998×10¹²¹` nats/tick, `ḣ = h/t_P = 9.27×10¹⁶⁴` nats/s |",
    "| Horizon BH entropy | `S_BH/k_B = πN_c² = 2.265×10¹²²` nats |",
    "| **Time to reach S_BH** | **`S_BH/h = π/ln2 = 4.532 ticks ≈ 2.44×10⁻⁴³ s` (analytic)** |",
    "",
    "⟹ **Statistical mixing is instantaneous**: the ensemble entropy reaches the horizon's BH entropy "
    "in about 4.5 Planck times. This differs from the **spatial transport** of §4.2 ② "
    "(`R_mix(t_H) = 47 μm` per Hubble time) by about **10⁶⁰** — they are **two different things**: "
    "the mixing of *information* versus the transport of *matter*, and they do not conflict. "
    "⟹ This also supplies the **dynamical reason** for round 40's \"equipartition holds "
    "instantaneously / needs no thermalisation\": the exogenous tick randomness drives the ensemble "
    "to equipartition within ~4.5 ticks.",
    "",
    "⚠️ **Upper bound on entropy growth**: the ensemble entropy saturates at `ln|O|` (the orbit size), "
    "and `ln|O| ≤ ln C(N, N/2) ≈ 4.24×10¹⁸²` nats ≫ `S_BH` (about 1.9×10⁶⁰ times) ⟹ "
    "**capacity is not the bottleneck; the rate is**. After saturation there is no further growth.",
    "",
    "⚠️ **First adjudication of T-7 (negative)**: is the tick randomness \"exogenous true randomness\" "
    "(H1) or \"an underlying determinism, merely coarse-grained\" (H2)? This round shows that H2 must "
    "encode the tick choice in the substrate itself, at a cost of (#bits of the tick choice ≈ L²) / "
    "(#sites L³) = **1/L → 0** (= 1.18×10⁻⁶¹ bits per site macroscopically) ⟹ it does **not** conflict "
    "with the sub-binary density \"0.25 nat per l_P²\" ⟹ **H1 and H2 are empirically equivalent at the "
    "level of the visible substrate and cannot be distinguished**. ⟹ Whether the future is predictable "
    "*in principle* is **undecidable within this framework**; under the **current formulation (H1)** "
    "the answer is definite: **not predictable** (the future is not a function of the present state).",
    "",
    "⚠️ **Coexists with round 21**: a single tick is still a bijection ⟹ the information of the "
    "*state* is strictly conserved; what this round computes is the growth of the *ensemble* "
    "(ignorance) entropy. The two do not conflict — \"no information is lost\" is about the state, "
    "\"entropy grows\" is about our ignorance of it.",
    "",
])
sub_once(EN, EN_A, EN_B42 + "\n" + EN_A, "EN §8.6.7 round-42 block")

print("")
print("通过 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
