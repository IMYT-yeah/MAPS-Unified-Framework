# -*- coding: utf-8 -*-
"""
第 31 轮论文补丁：
  ① §4.8 修正块：把「4 方向」的归属从 §4.10 的 k=4（Tammes/正四面体）
     改为 §4.9 引理 1 的「平面内 4 方向」，并登记读法 A/B 歧义；
  ② 摘要：微态计数条加「平面内」限定；
  ③ §8.6.8：新增 (i) —— 引理 1 的「平面内 4 + 平面外 2」是格点几何判别器
     （T-6 的第三条独立支持）。
中英同步；每个锚点要求恰好命中一次，否则拒绝改动。
正文引号一律用中文引号。
"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

N_OK = [0]
N_FAIL = [0]


def load(p):
    return io.open(p, encoding="utf-8").read().split("\n")


def save(p, lines):
    io.open(p, "w", encoding="utf-8").write("\n".join(lines))


def insert_after(path, key, block, tag):
    lines = load(path)
    hits = [i for i, L in enumerate(lines) if key in L]
    if len(hits) != 1:
        print("  [XX] %-26s 命中 %d 行 —— 拒绝" % (tag, len(hits)))
        N_FAIL[0] += 1
        return
    i = hits[0]
    lines = lines[:i + 1] + block.split("\n") + lines[i + 1:]
    save(path, lines)
    print("  [OK] %-26s 已插入（第 %d 行后，%d 行）" % (tag, i + 1, len(block.split("\n"))))
    N_OK[0] += 1


def replace_once(path, key, old, new, tag):
    lines = load(path)
    hits = [i for i, L in enumerate(lines) if key in L]
    if len(hits) != 1:
        print("  [XX] %-26s 命中 %d 行 —— 拒绝" % (tag, len(hits)))
        N_FAIL[0] += 1
        return
    i = hits[0]
    if old not in lines[i]:
        print("  [XX] %-26s 行内未找到待替换子串" % tag)
        N_FAIL[0] += 1
        return
    lines[i] = lines[i].replace(old, new)
    save(path, lines)
    print("  [OK] %-26s 已替换（第 %d 行）" % (tag, i + 1))
    N_OK[0] += 1


# ------------------------------------------------------------ ① §4.8 修正块
ZH_BLOCK = (
    "> **【v2.9 修正（第 31 轮：T-6 裁决的下游复查）】** 上一句把「4 方向」归给 §4.10 的\n"
    "> **方向簇 k = 4**（Tammes / 正四面体，**内空间**层面）。经第 30–31 轮核对，\n"
    "> 归属应为 **§4.9 引理 1 的「平面内 4 方向」**——即观测者「现在平面」内的连接方向；\n"
    "> 外空间格点配位是 **6**（简单立方，3 轴 ±），其中 4 个落在平面内、2 个被卷曲。\n"
    "> 两条独立理由：① 读法 A（方向数 k × 内部态数 q）下 `k·q = 16` 在 k = 6 时**无整数解**\n"
    "> （16/6 = 2.667）；② 读法 B（每方向一个二元「连接 / 不连接」标志）下 `2^k = 16 ⟹ k = 4`，\n"
    "> k = 6 给 64 态。⟹ **两种读法都强制方向数 = 4，不能用外空间配位 6**。\n"
    "> 数值结论「16 = 4 × 4」与压缩因子 **16 ln2 = 11.0904 均不变**。\n"
    "> ⚠️ **新登记歧义 A/B**：读法 A（4 方向 × 4 态 = 16，本条原读法）与读法 B\n"
    "> （4 个二元连接位 = 2⁴ = 16，原文 1651「四个方向上的**连接状态**」的字面读法）\n"
    "> **数值相同、结构不同，目前无法区分**，两者并列为候选。区分线索（未做）：\n"
    "> 读法 B 下「真空」= 该方向无连接（落在 4 个标志内）；读法 A 下「真空」是与方向并列的独立内部态。"
)

EN_BLOCK = (
    "> **【v2.9 correction (round 31: downstream re-check of the T-6 verdict)】** The line above\n"
    "> assigns the \"4 directions\" to the **direction cluster k = 4** of §4.10 (Tammes / regular\n"
    "> tetrahedron, the **interior-space** layer). Rounds 30–31 show the correct attribution is\n"
    "> the **\"four in-plane directions\" of §4.9 Lemma 1** — the connection directions inside the\n"
    "> observer's present plane. The exterior-space lattice coordination is **6** (simple cubic,\n"
    "> three axes ±), of which 4 lie in the plane and 2 are curled away. Two independent reasons:\n"
    "> (i) under reading A (direction count k times internal-state count q), `k·q = 16` has **no\n"
    "> integer solution at k = 6** (16/6 = 2.667); (ii) under reading B (one binary\n"
    "> connected/not-connected flag per direction), `2^k = 16 ⟹ k = 4`, while k = 6 gives 64 states.\n"
    "> ⟹ **Both readings force the direction count to be 4; the exterior-space coordination 6\n"
    "> cannot be used here.** The numerical conclusion \"16 = 4 × 4\" and the compression factor\n"
    "> **16 ln 2 = 11.0904 are unchanged.**\n"
    "> ⚠️ **Newly registered ambiguity A/B**: reading A (4 directions × 4 states = 16, the original\n"
    "> reading of this item) and reading B (4 binary connection flags = 2⁴ = 16, the literal reading\n"
    "> of the source text 1651 \"connection status in the four directions\") agree numerically but differ\n"
    "> structurally; they cannot be distinguished at present and are both kept as candidates.\n"
    "> Discriminating clue (not pursued): under reading B, \"vacuum\" = no connection in that direction\n"
    "> (inside the flags); under reading A, \"vacuum\" is an internal state on a par with the directions."
)

insert_after(ZH, "底层状态数的来源", ZH_BLOCK, "ZH §4.8 归属修正")
insert_after(EN, "Origin of the substrate state count", EN_BLOCK, "EN §4.8 attribution fix")

# ------------------------------------------------------------------ ② 摘要
replace_once(ZH, "微态计数", "原始态 = 4 方向 × 4 状态 = 16",
             "原始态 = 4 方向（**平面内**，§4.9 引理 1）× 4 状态 = 16", "ZH 摘要")
replace_once(EN, "Microstate counting", "raw states = 4 directions × 4 states = 16",
             "raw states = 4 **in-plane** directions (§4.9 Lemma 1) × 4 states = 16", "EN abstract")

# ---------------------------------------------------- ③ §8.6.8 新增 (i)
ZH_I = (
    "- **(i) 第三条独立支持（第 31 轮）：引理 1 的「平面内 4 + 平面外 2」是格点几何的判别器。**\n"
    "  精确枚举（极值必在「由任意两个方向张成的平面」上取到，故只需枚举方向对）：\n"
    "  简单立方 6 方向的**最大平面内方向数 = 4**（法线即平面外轴）✓；\n"
    "  正四面体 4 方向**不共面**，最大平面内方向数 = **2** ✗。\n"
    "  ⟹ **金刚石结构与 §4.9 引理 1 不相容**，简单立方通过。\n"
    "  这与「论证 4 显式区分内空间 4 / 外空间 6」及「引理 1 的 4+2 计数」一起，\n"
    "  构成 T-6 裁决的**三条独立依据**。"
)

EN_I = (
    "- **(i) Third independent support (round 31): Lemma 1's \"4 in-plane + 2 out-of-plane\" is a\n"
    "  discriminator for the lattice geometry.** Exact enumeration (the extremum is attained on a\n"
    "  plane spanned by two of the directions, so enumerating direction pairs suffices): the\n"
    "  **maximum in-plane count is 4** for the six simple-cubic directions (normal = the\n"
    "  out-of-plane axis) ✓, while the four tetrahedral directions are **not coplanar** and give a\n"
    "  maximum in-plane count of **2** ✗. ⟹ **The diamond structure is incompatible with §4.9\n"
    "  Lemma 1**; simple cubic passes. Together with \"Argument 4 explicitly separates interior-4 /\n"
    "  exterior-6\" and \"Lemma 1's 4+2 count\", this gives **three independent grounds** for T-6."
)

def insert_before(path, key, block, tag):
    lines = load(path)
    hits = [i for i, L in enumerate(lines) if key in L]
    if len(hits) != 1:
        print("  [XX] %-26s 命中 %d 行 —— 拒绝" % (tag, len(hits)))
        N_FAIL[0] += 1
        return
    i = hits[0]
    lines = lines[:i] + block.split("\n") + lines[i:]
    save(path, lines)
    print("  [OK] %-26s 已插入（第 %d 行前，%d 行）" % (tag, i + 1, len(block.split("\n"))))
    N_OK[0] += 1


insert_before(ZH, "**【诚实边界（8.6.8）】**", ZH_I, "ZH §8.6.8 (i)")
insert_before(EN, "**【Honest boundary (8.6.8)】**", EN_I, "EN §8.6.8 (i)")

print("\n补丁完成：成功 %d 项，失败 %d 项" % (N_OK[0], N_FAIL[0]))
