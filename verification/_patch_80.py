# -*- coding: utf-8 -*-
"""第 80 轮论文补丁（中英同步）：
  ① §4.8 —— 【第 80 轮】正式**登记**「格点离散结构 ↔ 面积律」为**框架不覆盖**（4.1）
  ② §4   —— 【第 80 轮】「遍历性」的**三层分层注**（4.2）

⚠️ 铁律：改前备份（已由本脚本复制到 paper/history/），改后列锚点，并复跑核验脚本。
"""
import io, os, shutil, sys

BASE = os.path.dirname(os.path.abspath(__file__))
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
TAG = "_备份_2026-10-02第80轮前.md"

OK = [0]
BAD = [0]


def chk(tag, cond, msg):
    if cond:
        OK[0] += 1
        print("  [OK] {:<6} {}".format(tag, msg))
    else:
        BAD[0] += 1
        print("  [XX] {:<6} {}  <-- 失败".format(tag, msg))


def backup(p):
    d = os.path.join(HIST, os.path.basename(p).replace(".md", TAG))
    shutil.copy2(p, d)
    print("  备份 → {}".format(os.path.basename(d)))


def sub_once(p, old, new, tag):
    t = io.open(p, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        print("  [XX] {:<26} 锚点命中 {} 次".format(tag, n))
        BAD[0] += 1
        return False
    io.open(p, "w", encoding="utf-8").write(t.replace(old, new, 1))
    print("  [OK] {:<26} 已插入".format(tag))
    OK[0] += 1
    return True


print("=" * 78)
print("第 80 轮论文补丁（中英同步）")
print("=" * 78)
backup(ZH)
backup(EN)

# ================================================================
print("\n[ZH-1] §4.8：正式登记「格点离散结构 ↔ 面积律」为**框架不覆盖**")
Z_ANCHOR = "> 🔧 **下一步（收口）**：这条（B5 ↔ 衬底）链路**到此收口**。"
Z_NEW = Z_ANCHOR + """

> **【v2.9 登记（第 80 轮：把「格点离散结构 ↔ 面积律」正式登记为「框架不覆盖」）】** 上一条块的末句提出「**是否该**正式登记」——本轮把它**落成声明**（脚本 `_shape_scaling_80.py`，**SH-1 … SH-7，7 项 0 失败**）。
>
> **✅ 正式登记**：**「格点离散结构 ↔ 面积律」这条链记为「框架不覆盖」。** 依据（第 46–52 轮**七轮** ＋ 第 78–80 轮复算，**全部负面**）：
> · ① **无等式** —— 链上唯一的定量关系是**不等式** `H/N ≤ 0.25`（**N-13**，第 51 轮）；
> · ② **无机制** —— `4` 是【本框架设定】（§4.9 引理 1）；B5 的 0.25 = 被 Hawking 温度钉住的**乘积** ＋ **不可观测的因式分解**（第 51 轮裁决，四类判定 = **半拟合 / 一致性**）；
> · ③ **不可证伪** —— 形式上 `N ≤ 39.6` 会违反，但一切真实黑洞 `N ≥ 10⁷⁷`、**余量 ≈ 10⁵⁰** ⟹ 不构成对衬底的有效约束（T-9）；
> · ④ **判据适用域受限（第 80 轮新增）** —— ⟨|O|⟩ 是**形状依赖量**：同一 N = 16 下 `(2,2,4)` = **50.87** ／ `(4,4,1)` = **514.80** ／ `(16,1,1)` = **15.23**（**相差 33.8 倍**；⚠️ 且 (2,2,4)/(2,4,2)/(4,2,2) **逐位相同 ✓** 的旋转等价检验通过）；同时「可迁性」的**必要条件** `|G| ≥ C(N,k)` 在 **N ≤ 24 上严格不成立**（⟹ 严格不可迁），却在 **N = 64 上已满足**（`|G|/C(N,k) = 1.5×10¹⁹`）⟹ **该判据在 N ≤ 24 上不能裁决宏观行为**。
> ⟹ 与 **N-13**（等式 → 不等式）、第 73 轮 **N-29**（判别点 → 包含关系）**同族**：**判据方向错了**，不是「还没算出来」。
> ⚠️ **登记的是「这条链不覆盖面积律」，不是「面积律错」** —— §4.8 的等分账（`ρ = 3H²/8πG`）**本身仍有内容**（不假设 Friedmann，见第 75 轮）；本条只否定**从衬底离散结构反推面积律**这条路。
> 📌 **⟨|O|⟩ 标度律（工作流 3.2 / I-15）的诚实边界**：三点 `5.00 / 50.87 / 426.93`（N = 8/16/24）**落在严格界 `1 ≤ ⟨|O|⟩ ≤ C(N,N/2)` 内**；对 `N^{2/3}` 的两段斜率 **0.9873 → 1.0795**（差 9.3%）⟹ **三点不足以判定幂指数**（⚠️ 与第 50 轮 `h_min·N^{−2/3}` 的 2.6% 残差**不是同一个量**：那是 **h_min**、这是 **⟨|O|⟩**）；⚠️ 且如上，**须标注「形状依赖、不外推」**。"""
sub_once(ZH, Z_ANCHOR, Z_NEW, "ZH §4.8 登记块")

print("\n[EN-1] §4.8: formally register \"lattice discretization ↔ area law\" as **NOT COVERED**")
E_ANCHOR = "> 🔧 **Next**: ① stop chasing `H/N = 0.25` (N-13);"
E_NEW = E_ANCHOR + """

> **【v2.9 registration (round 80: formally registering "lattice discretization ↔ area law" as NOT COVERED)】** The block above ended by asking "*should* this be formally registered?" — this round turns it into a **statement** (script `_shape_scaling_80.py`, **SH-1 … SH-7, 7 checks, 0 failures**).
>
> **✅ Formal registration**: **the chain "lattice discretization ↔ area law" is recorded as NOT COVERED by this framework.** Grounds (rounds 46–52, **seven rounds**, plus the rounds 78–80 recomputations — **all negative**):
> · ① **No equality** — the only quantitative relation on this chain is the **inequality** `H/N ≤ 0.25` (**N-13**, round 51);
> · ② **No mechanism** — the `4` is a 【framework assumption】 (§4.9 Lemma 1); B5's 0.25 = a **product** pinned by the Hawking temperature **plus** an **unobservable factorization** (round-51 verdict; four-way classification = **semi-fit / consistency construction**);
> · ③ **Not falsifiable** — formally `N ≤ 39.6` would violate it, but every real black hole has `N ≥ 10⁷⁷` with **margin ≈ 10⁵⁰** ⟹ it imposes no effective constraint on the substrate (T-9);
> · ④ **Restricted domain of validity (new in round 80)** — ⟨|O|⟩ is **shape-dependent**: at the same N = 16, `(2,2,4)` = **50.87** / `(4,4,1)` = **514.80** / `(16,1,1)` = **15.23** (**a factor of 33.8 across shapes**; ⚠️ while the rotation-equivalence test `(2,2,4)` / `(2,4,2)` / `(4,2,2)` passes with **bit-identical** results ✓). Moreover the **necessary condition** for transitivity, `|G| ≥ C(N,k)`, **fails strictly for all N ≤ 24** (⟹ strictly non-transitive) but is **already satisfied at N = 64** (`|G|/C(N,k) = 1.5×10¹⁹`) ⟹ **the criterion cannot adjudicate macroscopic behaviour from N ≤ 24 data**.
> ⟹ Same **family** as **N-13** (equality → inequality) and round 73's **N-29** (discriminating point → inclusion relation): **the criterion points the wrong way** — this is not "not computed yet".
> ⚠️ **What is registered is "this chain does not cover the area law", NOT "the area law is wrong"** — §4.8's equipartition balance (`ρ = 3H²/8πG`) **still has content** (it does not assume Friedmann; see round 75); this entry only rules out **deriving the area law from the substrate's discrete structure**.
> 📌 **Honest limits of the ⟨|O|⟩ scaling law (workflow 3.2 / I-15)**: the three points `5.00 / 50.87 / 426.93` (N = 8/16/24) **lie inside the rigorous bound `1 ≤ ⟨|O|⟩ ≤ C(N,N/2)`**; against `N^{2/3}` the two segment slopes are **0.9873 → 1.0795** (9.3% apart) ⟹ **three points cannot determine the exponent** (⚠️ not the same quantity as round 50's `h_min·N^{−2/3}` with its 2.6% residual: that is **h_min**, this is **⟨|O|⟩**); and as noted above it must carry the label "**shape-dependent, not to be extrapolated**"."""
sub_once(EN, E_ANCHOR, E_NEW, "EN §4.8 registration block")

# ================================================================
print("\n[ZH-2] §4：三个「遍历性」的分层注（4.2）")
Z2_ANCHOR = "- ⟹ **结论对、原证据错**：第 2 条的结论保留，证据替换为上述 Birkhoff 检验。"
Z2_NEW = Z2_ANCHOR + """

> **【v2.9 分层注（第 80 轮：「遍历性」在本框架里有三个互不相同的层次）】** 本轮词条清点发现：「遍历」一词全篇承载**相反结论**且**无区分说明**（脚本 `_shape_scaling_80.py` SH-5，7 项 0 失败）⟹ 补分层如下。**引用时必须写明层次**。
>
> | 层 | 空间 | 所问的问题 | 结论 | 出处 |
> |---|---|---|---|---|
> | **L1 速度空间** | 单粒子速度 **v** | 时间平均 = 系综平均？ | ✅ **遍历成立**（Birkhoff 检验：离散度 0.971 → 0.183 单调下降；冻结对照恒为 1.012） | 本命题链第 2 条 |
> | **L2 构型空间** | 衬底占据位型（2^N，或按 k 分层的 C(N,k)） | 一条轨迹能访问整个空间？ | ❌ **非遍历** —— tick 群把空间切成**不变轨道**，轨迹**永不离开**自己的轨道 | 第 40 / 57 轮 |
> | **L3 空间输运** | 标记（信息 / 物质）在格点上的位移 | 混合 / 输运走多远？ | **慢**：`R_mix = l_P√(t/t_P)`，一个哈勃时仅 **47 μm**（**并行归一化**） | §4.2 ② |
>
> ⟹ **三者不矛盾，因为问的不是同一件事**：**L1 是速度的局域平衡**（快，~4 t_P）；**L2 是构型的轨道封闭**（**不是**「没热化」—— 是「**到不了**」）；**L3 是位移**（慢）。
> ⟹ 第 40 轮「等分账**瞬时**成立 / **不需要**热化」用的正是 **L1 与 L3 的时标分离**（`τ_relax ≈ 4 t_P` 与 `t_H` 相差 **~10⁶⁰ 倍**，§4.2 两个时标）。
> ⚠️ **写作规范**：写「遍历性成立」必须写明 **L1（速度空间）**；写「非遍历」必须写明 **L2（构型空间）**；涉及「everything」的那一条（第 57 轮四读之 (c)）指的是 **L2**。
> ⚠️ **一处需要澄清的候选（本轮顺带查明）**：候选池 14 把第三项记作「**第 21 轮 47 μm 空间输运**」并称之为一种「遍历性」，但全文检索显示 **47 μm 处从未使用「遍历」一词**（`R_mix` 是**扩散标度**，不是遍历性判据）⟹ 本注**把它单列为 L3 并改名**，以免沿用「三种遍历性」这个**用词不实**的说法。"""
sub_once(ZH, Z2_ANCHOR, Z2_NEW, "ZH §4 遍历性分层注")

print("\n[EN-2] §4: layered note on the three distinct meanings of \"ergodicity\" (item 4.2)")
E2_ANCHOR = "- ⟹ **The conclusion is right, the original evidence was wrong**: item 2's conclusion is retained, with the Birkhoff test above as its evidence."
E2_NEW = E2_ANCHOR + """

> **【v2.9 layered note (round 80: "ergodicity" carries three distinct meanings in this framework)】** A term sweep this round found the word "ergodic" carrying **opposite conclusions** in the same paper with **no distinguishing note** (script `_shape_scaling_80.py` SH-5, 7 checks, 0 failures) ⟹ the layers are separated below. **Citations must state the layer.**
>
> | Layer | Space | Question asked | Verdict | Source |
> |---|---|---|---|---|
> | **L1 velocity space** | single-particle velocity **v** | time average = ensemble average? | ✅ **ergodic** (Birkhoff test: spread 0.971 → 0.183, monotone; frozen control flat at 1.012) | item 2 of this chain |
> | **L2 configuration space** | substrate occupancy patterns (2^N, or the k-layer C(N,k)) | can one trajectory visit the whole space? | ❌ **non-ergodic** — the tick group cuts the space into **invariant orbits**; a trajectory **never leaves** its own | rounds 40 / 57 |
> | **L3 spatial transport** | displacement of a marker (information / matter) | how far does mixing / transport reach? | **slow**: `R_mix = l_P√(t/t_P)`, only **47 μm** per Hubble time (**parallel normalization**) | §4.2 ② |
>
> ⟹ **The three do not conflict, because they do not ask the same question**: **L1 is local equilibration of velocities** (fast, ~4 t_P); **L2 is orbital closure of configurations** (not "not yet thermalized" but "**cannot get there**"); **L3 is displacement** (slow).
> ⟹ Round 40's "equipartition holds **instantaneously** / **no** thermalization needed" rests exactly on the **timescale separation between L1 and L3** (`τ_relax ≈ 4 t_P` versus `t_H`, a ratio of **~10⁶⁰**, §4.2's two timescales).
> ⚠️ **Writing rule**: "ergodicity holds" must say **L1 (velocity space)**; "non-ergodic" must say **L2 (configuration space)**; the "everything" reading (round 57, reading (c)) refers to **L2**.
> ⚠️ **One candidate needing clarification (found this round)**: candidate-pool item 14 records the third entry as "round 21's 47 μm spatial transport" and calls it a kind of "ergodicity", but a full-text search shows the **word "ergodic" is never used at the 47 μm passage** (`R_mix` is a **diffusion scaling**, not an ergodicity criterion) ⟹ this note lists it separately as **L3 and renames it**, so as not to perpetuate the **inaccurate** phrase "three kinds of ergodicity"."""
sub_once(EN, E2_ANCHOR, E2_NEW, "EN §4 ergodicity layered note")

# ================================================================
print("")
print("=" * 78)
print("  通过 {} 项，失败 {} 项".format(OK[0], BAD[0]))
print("=" * 78)
