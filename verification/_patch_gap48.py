# -*- coding: utf-8 -*-
r"""第 48 轮论文补丁（中英同步，行定位 + 断言）。

A 段：**修 §4.8 的两处拼接/断行缺陷**（第 41 轮补丁留下的）
      — 中文版把第 41 轮块粘在第 40 轮块尾同一行；中英都有一句被拆成
      「…（第 450/423 行，句子断掉）」+「，…（第 484/457 行，残片）」。
B 段：更正第 46 / 47 轮的过期数值（(2,2,6) 0.4330 → 0.4510 等）。
C 段：给「偏大 1.75 倍」的判决加第 48 轮限定。
D 段：把残片那一行**替换**为【第 48 轮】块（接在 v2.9 补充链末尾）。

做法：按**行号**改，每步先断言该行内容符合预期（含指定子串），不符则整份拒绝。
"""

import io
import os
import shutil
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
STAMP = "2026-09-22第48轮前"

N_OK = [0]
N_FAIL = [0]


def load(p):
    return io.open(p, encoding="utf-8").read().split("\n")


def save(p, L):
    io.open(p, "w", encoding="utf-8").write("\n".join(L))


def edit(L, idx, need, new, tag):
    """把 L[idx]（0-indexed）换成 new，要求原行含 need。"""
    if idx >= len(L):
        print("  [XX] {:<30} 行号越界".format(tag))
        N_FAIL[0] += 1
        return False
    if need not in L[idx]:
        print("  [XX] {:<30} 行 {} 不含「{}」；实际：{}".format(
            tag, idx + 1, need[:26], L[idx][:70]))
        N_FAIL[0] += 1
        return False
    L[idx] = new
    print("  [OK] {:<30} 第 {} 行已改".format(tag, idx + 1))
    N_OK[0] += 1
    return True


# ============================================================ 备份
os.makedirs(HIST, exist_ok=True)
for src, stem in ((ZH, "论文初稿_v2.9"), (EN, "Paper_v2.9_EN")):
    dst = os.path.join(HIST, "{}_备份_{}.md".format(stem, STAMP))
    shutil.copy2(src, dst)
    print("  备份 ->", os.path.basename(dst))
print()

# ============================================================ 第 48 轮块（中文）
ZH_BLOCK = [
    "> **【v2.9 补充（第 48 轮：装上 GAP —— H/N 的形状依赖，**跨过** 0.25）】** 上一条把形状对照停在「(2,4,4) 算不出来（|G| = 2.2×10¹¹ 超上限）」。本轮 ① 装上 **GAP 4.16.1**，用 `Stabilizer(G, c, OnSets)` 直接给 `|O(c)| = |G|/|Stab_G(c)|`；② **顺带查出第 41/46/47 轮的一处真错误**（见下）。",
    "",
    "> · **发现 A（生成元集错误 —— 本轮最重要的负面发现）**：第 41/46/47 轮的化简生成元集把每线的 σ_j 写成 **`coords[i] → coords[(i+2) % L]`（全体 +2 的「纯平移」）**，而正确的 σ_j（= 相位 1 匹配 ∘ 相位 0 匹配）是 **偶位 +2、奇位 −2**。两者在 **L ≤ 4 时逐元素相同** —— 第 41 轮的「化简验证」只在 2×2×2 / 2×2×4 上做过，是**退化情形**；**L ≥ 6 时群不同**：单线长 6 上两群只共有 2 个元素（|并| = 10），8 个随机真 tick 里**只有 3 个**落在旧群里 ⟹ 旧群**漏掉 5/8 的真 tick**。",
    "> · **受影响范围（比预想窄，但正落在关键算例上）**：只有「**恰好一个长轴（L ≥ 6）**」的细长格点，即 **(2,2,6)、(2,2,8)**；(2,2,2)、(2,2,4)、(2,4,4)、(4,4,4)、(6,6,6) **不受影响**（旧生成元全部落在正确群里 ⟹ 同一群）。",
    "> · **更正后的 (2,2,L) 曲线**：(2,2,6) N=24 由 **0.4330 → 0.4510**（精确划分；轨道数 6224 → 6334）；(2,2,8) N=32 由 0.4614 → **0.4617**。",
    "> · **发现 B（H/N 的形状依赖 —— 本轮正面结果）**：用 GAP 首次算出 —— **(2,4,4) N=32：H/N = 0.2834 ± 0.0061**（轨道 10³·⁴–10⁶·⁸，S=60）；**(4,4,4) N=64：H/N = 0.1839 ± 0.0031**（轨道 10¹²·²–10¹⁵·³，S=60）；**(2,4,8) N=64：0.1802 ± 0.0034**；**(2,2,16) N=64：0.5307**（40 个采样轨道大小全等于 |G| ⟹ 稳定子平凡）。",
    "> · **判决（本轮实质结论）**：面积律要求的 **0.25 被「跨过」了** —— (2,4,4) = 0.2834 **> 0.25** > (4,4,4) = 0.1839。⟹ **第 40 轮以来「不变读数偏大约 1.75 倍 ⟹ 面积律不成立」的判决是细长格点假象。** 判别量**不是**「各向同性程度」（本轮预判「越各向同性 H/N 越小」**被自己否证**：(2,4,8) = 0.1802 **<** (4,4,4) = 0.1839），而是「**长度为 2 的方向有几个**」：**≥ 2 个**时 H/N ∈ [0.4335, 0.5307]，**≤ 1 个**时 H/N ∈ [0.1802, 0.2834]，**两组完全分离、0.25 落在空隙里**（机理：长度 2 的环只有一种完美匹配 ⟹ 该方向**没有相位自由度**，σ_j = 恒等）。",
    "> · **GAP 的调用条件（工程记录）**：安装包 `gap-4.16.1-x86_64.exe`（782.5 MB，sha256 与官方一致）静默装到 `C:\\Program Files\\GAP-4.16.1\\`；它是 **Cygwin/MSYS 版** ⟹ 调用时须把 `runtime\\bin` 与 gap 根目录**都**加进 PATH（否则报 `No such file or directory`），且**不能用 `timeout` 包**（Git Bash 的 execvp 与 Windows 加载器不兼容）。验证：`Stabilizer(Sym(5),[1,2],OnSets) = 12`、`Stabilizer(Sym(6),[1,2],OnSets) = 48`，并与 Python 精确轨道 BFS 在 (2,2,6) 上 **8/8 逐位一致**。",
    "> ⚠️ **诚实边界**：(2,4,4)/(4,4,4) 用采样 S=60、(2,2,16)/(2,4,8) 用 S=40 ⟹ (4,4,4) 与 (2,4,8) 的 95% 区间**都在 0.25 下方**（[0.178,0.190] / [0.174,0.187]），而 (2,4,4) 在上方 [0.272,0.295] ⟹ **「跨过」确定、跨点未定**。形状扫描只有 3 个 N=64 点 ⟹ 上述判据是**在 8 个算例上归纳出来的，不是推导的**。k 固定为 N/2；N = 64 仍远小于宏观 N_c³ ≈ 6.1×10¹⁸² ⟹ **不得外推**（第 41 轮教训）。",
    "> 🔧 **下一步（两条都可证伪）**：① 在 N=32/64/128 上补形状，定位 **0.25 的跨点**（GAP 让这成为常规计算：全脚本约 76 s）；② **检验「退化方向数」判据** —— (2,6,6) 应与 (2,4,4) 同类、(6,6,6) 应与 (4,4,4) 同类。",
]

EN_BLOCK = [
    "> **【v2.9 supplement (round 48: GAP installed — the shape dependence of H/N, which **straddles** 0.25)】** The previous block stopped the shape comparison at \"(2,4,4) cannot be computed (|G| = 2.2×10¹¹ exceeds the cap)\". This round ① installs **GAP 4.16.1** and uses `Stabilizer(G, c, OnSets)` to obtain `|O(c)| = |G|/|Stab_G(c)|` directly; ② and **uncovers a genuine error of rounds 41/46/47** along the way.",
    "",
    "> · **Finding A (the generator set was wrong — this round's most important negative finding)**: the reduced generator set of rounds 41/46/47 wrote the per-line σ_j as **`coords[i] → coords[(i+2) % L]` (a \"pure translation\" by +2)**, whereas the correct σ_j (= phase-1 matching ∘ phase-0 matching) is **+2 on even positions and −2 on odd ones**. The two coincide **element-by-element for L ≤ 4** — the \"reduction check\" of round 41 only ever ran on 2×2×2 / 2×2×4, which is a **degenerate case**; for **L ≥ 6 the groups differ**: on a single line of length 6 they share only 2 elements (|union| = 10), and of 8 random true ticks **only 3** lie in the old group ⟹ the old group **misses 5/8 of the true ticks**.",
    "> · **Scope of impact (narrower than feared, but exactly where it matters)**: only elongated lattices with **exactly one long axis (L ≥ 6)**, i.e. **(2,2,6) and (2,2,8)**; (2,2,2), (2,2,4), (2,4,4), (4,4,4) and (6,6,6) are **unaffected** (every old generator lies in the correct group ⟹ same group).",
    "> · **The corrected (2,2,L) curve**: for (2,2,6) at N=24 the H/N changes from **0.4330 → 0.4510** (exact partition; #orbits 6224 → 6334); for (2,2,8) at N=32 it goes from 0.4614 → **0.4617**.",
    "> · **Finding B (the shape dependence of H/N — this round's positive result)**: computed for the first time with GAP — **(2,4,4) N=32: H/N = 0.2834 ± 0.0061** (orbits 10³·⁴–10⁶·⁸, S=60); **(4,4,4) N=64: H/N = 0.1839 ± 0.0031** (orbits 10¹²·²–10¹⁵·³, S=60); **(2,4,8) N=64: 0.1802 ± 0.0034**; **(2,2,16) N=64: 0.5307** (all 40 sampled orbits equal |G| ⟹ trivial stabiliser).",
    "> · **Verdict (the substantive conclusion of this round)**: the value required by the area law, **0.25, is \"straddled\"** — (2,4,4) = 0.2834 **> 0.25** > (4,4,4) = 0.1839. ⟹ **The verdict held since round 40 — \"the invariant readout is too large by ≈1.75× ⟹ the area law fails\" — is an artefact of elongated lattices.** The discriminator is **not** the degree of isotropy (this round's prediction \"the more isotropic, the smaller H/N\" was **refuted by itself**: (2,4,8) = 0.1802 **<** (4,4,4) = 0.1839) but \"**how many directions have length 2**\": with **≥ 2** of them H/N ∈ [0.4335, 0.5307], with **≤ 1** of them H/N ∈ [0.1802, 0.2834] — **the two groups are completely separated and 0.25 falls in the gap** (mechanism: a cycle of length 2 has only one perfect matching ⟹ such directions carry **no phase freedom**, σ_j = identity).",
    "> · **GAP invocation requirements (engineering record)**: the installer `gap-4.16.1-x86_64.exe` (782.5 MB, sha256 identical to the official one) was silently installed to `C:\\Program Files\\GAP-4.16.1\\`; it is a **Cygwin/MSYS build** ⟹ when invoking, **both** `runtime\\bin` and the gap root must be on PATH (otherwise `No such file or directory`), and it **must not be wrapped in `timeout`** (Git Bash's execvp is incompatible with the Windows loader). Verification: `Stabilizer(Sym(5),[1,2],OnSets) = 12`, `Stabilizer(Sym(6),[1,2],OnSets) = 48`, and **8/8 agreement** with the exact Python orbit BFS on (2,2,6).",
    "> ⚠️ **Honest limits**: (2,4,4)/(4,4,4) use S=60 samples, (2,2,16)/(2,4,8) use S=40 ⟹ the 95% intervals of (4,4,4) and (2,4,8) lie **entirely below 0.25** ([0.178,0.190] / [0.174,0.187]) while (2,4,4)'s lies above [0.272,0.295] ⟹ **the straddle is certain, the crossing point is not**. The shape scan has only 3 points at N=64 ⟹ the criterion above is **induced from 8 cases, not derived**. k is fixed at N/2; N = 64 is still far below the macroscopic N_c³ ≈ 6.1×10¹⁸² ⟹ **do not extrapolate** (lesson of round 41).",
    "> 🔧 **Next (both falsifiable)**: ① add shapes at N=32/64/128 to locate **the crossing point of 0.25** (GAP makes this routine: the whole script takes ≈76 s); ② **test the \"number of degenerate directions\" criterion** — (2,6,6) should behave like (2,4,4) and (6,6,6) like (4,4,4).",
]

# ============================================================ 中文版
print("=== 中文版 ===")
L = load(ZH)

# D 段 + A 段：残片行 → 第 48 轮块（必须在改其它行之前按**降序**处理）
if edit(L, 456, "，**跨过 0.25**", "\n".join(ZH_BLOCK), "ZH 残片→第48轮块"):
    # 残片前的三个空行保留一个
    pass

# B 段
edit(L, 451, "方法自校验",
     "> · **方法自校验**：(2,2,6) 采样给 0.4343，上一条精确值 0.4330 ⟹ 差 **0.0013** ⟹ 采样法可信。"
     "⚠️ **第 48 轮更正**：0.4330 与 0.4343 都基于**错误的生成元集**；更正后该行精确值为 **0.4510**。",
     "ZH 自校验更正")
edit(L, 449, "判决 2（修正上一条）",
     "> · **判决 2（修正上一条）**：**H/N 非单调** —— (2,2,L) 系列给 0.4679（N=8）⟶ 0.4335（N=16）⟶ "
     "**0.4510**（N=24）⟶ **0.4617**（N=32）。⚠️ **第 48 轮更正**：原值 0.4330 / 0.4614 基于**错误的生成元集**"
     "（长度 ≥ 6 的线用了「纯平移」而非正确的 σ_j），只有「非单调」这个定性结论存活；"
     "原文的机制解释（「ln|G|/N 下降 ⟹ 轨道相对受限 ⟹ 回升」）**未经更正后数据检验，暂不可信**。",
     "ZH 判决2更正")
edit(L, 445, "| (2,2,8) | 32 | 7 |",
     "| (2,2,8) | 32 | 7 | **2.048×10³** | 0.2383 | **0.4617**（采；第 48 轮更正，原 0.4614） |",
     "ZH 47表 (2,2,8)")
edit(L, 444, "| (2,2,6) | 24 | 7 |",
     "| (2,2,6) | 24 | 7 | 6.48×10² | 0.2697 | **0.4510**（精；第 48 轮更正，原 0.4330） |",
     "ZH 47表 (2,2,6)")
edit(L, 435, "判决 3（正面",
     "> · **判决 3（正面，本轮最有用；⚠️ 第 47 轮改「非单调」、第 48 轮**更正数值**）**：**H/N 落在 0.43–0.53**"
     "（(2,2,L) 系列，更正后：0.4679 ⟶ 0.4335 ⟶ **0.4510** ⟶ **0.4617** ⟶ **0.5307**（N=64））。"
     "⟹ **面积律要求的 0.25 在细长格点上未被命中**（偏大 ≈ 1.7–2.1 倍）。"
     "⚠️ **但第 48 轮证明这是细长格点假象**：(2,4,4) = 0.2834、(4,4,4) = 0.1839 ⟹ **0.25 被跨过**；"
     "**不得**再把「偏大 1.75 倍」当作宏观结论。",
     "ZH 判决3更正")
edit(L, 431, "| (2,2,6) | 24 | 2 704 156 |",
     "| (2,2,6) | 24 | 2 704 156 | 648 | 6 334 | 1 050 | ❌ 不完备 | 0.2421 | **0.4510** |",
     "ZH 46表 (2,2,6)")
edit(L, 423, "k = N/2 的精确轨道",
     "> **【v2.9 补充（第 46 轮：k = N/2 的精确轨道 —— 不变量不完备，H/N 落在 0.43–0.53）】** "
     "⚠️ **第 47 轮修正**：原文的「H/N 饱和在 ≈0.433」**不成立** —— 把 (2,2,L) 系列推进到 N=32 得 H/N 回升 ⟹ **非单调**。"
     "⚠️ **第 48 轮更正**：本块的 (2,2,6) 一行（0.4330）**基于错误的生成元集**，更正为 **0.4510**；"
     "定性结论（不变量不完备、H/N 远离 0.25）不变。 上一条把问题归结为「需要 k = N/2 的真实轨道」，"
     "并用 (Z₂)³ 奇偶差类不变量给出上界。本轮用**精确轨道划分**检验该不变量是否**完备**。",
     "ZH 46标头更正")
edit(L, 422, "仍未定",
     "> ⚠️ **仍未定**：H/N 的界为 **0.162 – 0.693**，**跨过 0.25** ⟹ 宏观精确值待 k = N/2 的**真实轨道**"
     "（需要 set-stabilizer；sympy 目前不提供）。⟹ 上一条的「三难」应改写为「**两难 + 一个结构**」："
     "不变的读数既非「太多」（第 ① 条不可外推）、也非「太少」（群非高度可迁），而是**受 (Z₂)³ 不变量约束**。"
     "✅ **第 48 轮已用 GAP 落实**：(2,4,4) = 0.2834、(4,4,4) = 0.1839 ⟹ **确实跨过 0.25**。",
     "ZH 仍未定补全")
edit(L, 416, "但上述判据与 N 无关",
     "> ⚠️ **诚实边界**：|G| 与轨道结构只在 **N ≤ 16** 上穷举；格子越大、每线相位自由度越多"
     "（4×4×4 有 513 个生成元）⟹ 群可能大得多 ⟹ **H/N 的 N → ∞ 极限未定**。但上述判据与 N 无关、可直接检验。",
     "ZH 拆开拼接")
edit(L, 410, "上一条的第 ① 条（不变读数偏大约 1.75 倍）",
     L[410] + " ⚠️ **第 48 轮再更正**：**连「偏大 1.75 倍」本身也是细长格点假象** —— "
     "(2,4,4) = 0.2834（+13%）、(4,4,4) = 0.1839（**−26%**）⟹ 面积律**跨过** 0.25。",
     "ZH 1.75倍 限定(420)")
edit(L, 408, "偏大约 1.75 倍",
     L[408] + " ⚠️ **第 48 轮更正**：该「偏大 1.75 倍」只是 **(2,2,L) 细长格点**的结果；"
     "真三维格点上 (2,4,4) = 0.2834、(4,4,4) = 0.1839 ⟹ **跨过 0.25**（见第 48 轮块）。",
     "ZH 1.75倍 限定(413)")
save(ZH, L)

# ============================================================ 英文版
print()
print("=== 英文版 ===")
L = load(EN)
edit(L, 483, ", which **straddles 0.25**", "\n".join(EN_BLOCK), "EN 残片→第48轮块")
edit(L, 478, "Self-check of the method",
     "> · **Self-check of the method**: (2,2,6) sampled gives 0.4343 against the previous exact 0.4330 "
     "⟹ a difference of **0.0013** ⟹ the sampling method is trustworthy. ⚠️ **Corrected in round 48**: both "
     "0.4330 and 0.4343 rest on the **wrong generator set**; the corrected exact value is **0.4510**.",
     "EN self-check fix")
edit(L, 476, "Verdict 2 (corrects the previous block)",
     "> · **Verdict 2 (corrects the previous block)**: **H/N is non-monotonic** — the (2,2,L) family gives "
     "0.4679 (N=8) ⟶ 0.4335 (N=16) ⟶ **0.4510** (N=24) ⟶ **0.4617** (N=32). ⚠️ **Corrected in round 48**: the "
     "earlier values 0.4330 / 0.4614 rested on the **wrong generator set** (lines of length ≥ 6 used the "
     "\"pure translation\" instead of the correct σ_j); only the qualitative claim (non-monotonic) survives, "
     "and the original mechanism (\"ln|G|/N drops ⟹ orbits more constrained ⟹ recovery\") is **not yet "
     "re-verified against corrected data**.",
     "EN Verdict2 fix")
edit(L, 472, "| (2,2,8) | 32 | 7 |",
     "| (2,2,8) | 32 | 7 | **2.048×10³** | 0.2383 | **0.4617** (sampled; corrected in round 48, was 0.4614) |",
     "EN 47 table (2,2,8)")
edit(L, 471, "| (2,2,6) | 24 | 7 |",
     "| (2,2,6) | 24 | 7 | 6.48×10² | 0.2697 | **0.4510** (exact; corrected in round 48, was 0.4330) |",
     "EN 47 table (2,2,6)")
edit(L, 462, "Verdict 3 (positive",
     "> · **Verdict 3 (positive; ⚠️ re-qualified in round 47 as \"non-monotonic\" and **corrected numerically in "
     "round 48**)**: **H/N lies in 0.43–0.53** for the (2,2,L) family (corrected: 0.4679 ⟶ 0.4335 ⟶ **0.4510** "
     "⟶ **0.4617** ⟶ **0.5307** at N=64). ⟹ **the 0.25 required by the area law is not hit on elongated "
     "lattices** (too large by ≈1.7–2.1×). ⚠️ **But round 48 shows this is an artefact of elongated lattices**: "
     "(2,4,4) = 0.2834 and (4,4,4) = 0.1839 ⟹ **0.25 is straddled**; \"too large by 1.75×\" must **not** be "
     "quoted as a macroscopic conclusion.",
     "EN Verdict3 fix")
edit(L, 458, "| (2,2,6) | 24 | 2 704 156 |",
     "| (2,2,6) | 24 | 2 704 156 | 648 | 6 334 | 1 050 | ❌ incomplete | 0.2421 | **0.4510** |",
     "EN 46 table (2,2,6)")
edit(L, 450, "the exact orbit at k = N/2",
     "> **【v2.9 supplement (round 46: the exact orbit at k = N/2 — the invariant is incomplete, and H/N lies in "
     "0.43–0.53)】** ⚠️ **Corrected in round 47**: the original claim that \"H/N saturates at ≈0.433\" **fails** — "
     "extending the (2,2,L) family to N=32 makes H/N rise again ⟹ **non-monotonic**. ⚠️ **Corrected in round 48**: "
     "this block's (2,2,6) entry (0.4330) rests on the **wrong generator set** and becomes **0.4510**; the "
     "qualitative conclusions (the invariant is incomplete, H/N is far from 0.25) are unaffected.",
     "EN 46 header fix")
edit(L, 449, "Still open",
     "> ⚠️ **Still open**: the bracket for H/N is **0.162 – 0.693**, which **straddles 0.25** ⟹ the macroscopic "
     "value awaits the **true orbit at k = N/2** (a set-stabilizer is needed; sympy does not provide one). "
     "⟹ The \"trilemma\" of the previous block should be rewritten as \"**a dilemma plus one structure**\": an "
     "invariant readout is neither \"too large\" (item ① does not extrapolate) nor \"too small\" (the group is not "
     "highly transitive), but is **constrained by the (Z₂)³ invariant**. ✅ **Delivered in round 48 with GAP**: "
     "(2,4,4) = 0.2834, (4,4,4) = 0.1839 ⟹ **0.25 is indeed straddled**.",
     "EN still-open fix")
edit(L, 438, "invariant readout too large by",
     L[438] + " ⚠️ **Corrected in round 48**: \"too large by 1.75×\" is itself an artefact of the **(2,2,L) "
     "elongated lattices**; on genuinely 3D lattices (2,4,4) = 0.2834 and (4,4,4) = 0.1839 ⟹ **0.25 is "
     "straddled** (see the round-48 block).",
     "EN 1.75x limit (439)")
edit(L, 436, "Result 2 (an invariant readout carries too much entropy)",
     L[436] + " ⚠️ **Corrected in round 48**: this \"≈1.75× too large\" is only the **(2,2,L)** result; on truly "
     "3D lattices (2,4,4) = 0.2834 and (4,4,4) = 0.1839 ⟹ **0.25 is straddled**.",
     "EN 1.75x limit (439b)")
save(EN, L)

print()
print("=" * 70)
print("论文补丁：成功 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
print("=" * 70)
sys.exit(0 if N_FAIL[0] == 0 else 1)
