# -*- coding: utf-8 -*-
"""
第 34 轮论文补丁：在 §4.8 的第 33 轮块之后，追加「w 与 f 的同一性」结论块（B2 闭环）。
中英同步；锚点要求恰好命中一次。正文引号一律用中文引号。
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
        print("  [XX] %-22s 命中 %d 行 —— 拒绝" % (tag, len(hits)))
        N_FAIL[0] += 1
        return
    i = hits[0]
    lines = lines[:i + 1] + block.split("\n") + lines[i + 1:]
    save(path, lines)
    print("  [OK] %-22s 已插入（第 %d 行后，%d 行）" % (tag, i + 1, len(block.split("\n"))))
    N_OK[0] += 1


ZH_BLOCK = (
    "> **【v2.9 补充（第 34 轮：w 与 f 的同一性 —— B2 闭环）】**\n"
    "> 第 33 轮留下的软肋是「空槽率 w 与衬底占位率 f 是否为同一个量」（当时默认 `w = 1 − f`）。本轮结论：\n"
    "> · **两者不是同一个量**：面元的「平面内连接」是格点间的**键**，一条键承载通量 ⟺ **两端格点都被占**；\n"
    ">   占位独立时 **`w = 1 − f²`**（Monte-Carlo 直接检验：f = 0.9 / 0.8 / 0.6 / 0.5 的实测键存活率\n"
    ">   与 f² 相符，偏差 ≤ 2.3%）。第 33 轮默认的 `w = 1 − f` **少了一个平方，是错的**；\n"
    ">   但因 `f = 1 ⟹ w = 0`（两式同给 0），**结论不变**。\n"
    "> · **同一性假设并不需要**：框架的置换动力学是**双射** ⟹ 每个格点**恒有且仅有 1 个诸元**\n"
    ">   ⟹ **f ≡ 1 逐 tick 恒等**（数值：1000 tick 内非置换 tick = 0，每格点占据数恒为 1）\n"
    ">   ⟹ **w ≡ 0 逐 tick 恒等**，也不是概率。⟹ B2 的「无空槽」既不来自跨层搬运，\n"
    ">   也不依赖格点间的独立性，**它是置换双射的直接后果**。\n"
    "> · **独立泊松衬底被第二次独立排除**：`f* = 1/2 ⟹ w = 0.75` ⟹ Hawking 温度偏差 **−5.77%**\n"
    ">   （第一条依据是第 20 轮的 Δc/c = 26%，两者互不相干，构成交叉验证）。\n"
    "> · 双约束反解 `H_S(1 − f²) = ln 16` ⟹ **f = 1** 或 **f = 0.4765**；后者意味着 52.3% 的格点是空的，\n"
    ">   与 C-1 冲突 ⟹ 排除。\n"
    "> ⟹ **B2 闭环**：满占位（置换双射）⟹ 每键承载通量 ⟹ 4 条平面内连接全活 ⟹ A1 的 50:50 分配正 / 负支\n"
    ">   ⟹ **2^4 = 16** ⟹ BH 定标成立 ⟹ Hawking 温度精确。\n"
    "> ⚠️ **仍开放**：「面元连接」与「格点键」是否严格对应，未独立论证。"
)

EN_BLOCK = (
    "> **【v2.9 addendum (round 34: the identity of w and f — closing the B2 loop)】**\n"
    "> Round 33 left one soft spot: whether the empty-slot rate w and the substrate occupancy f are\n"
    "> the same quantity (it was assumed that `w = 1 − f`). This round concludes:\n"
    "> · **They are not the same quantity**: a plaquette's \"in-plane connection\" is a **bond** between\n"
    ">   sites, and a bond carries flux ⟺ **both endpoints are occupied**; for independent occupancy,\n"
    ">   **`w = 1 − f²`** (direct Monte-Carlo check: measured bond-survival rates at f = 0.9 / 0.8 / 0.6 /\n"
    ">   0.5 agree with f² to within 2.3%). The round-33 default `w = 1 − f` **misses a square and is\n"
    ">   wrong**; but since `f = 1 ⟹ w = 0` under either form, **the conclusion is unchanged**.\n"
    "> · **No identity assumption is needed**: the framework's permutation dynamics is a **bijection** ⟹\n"
    ">   every site **always has exactly one 诸元** ⟹ **f ≡ 1 identically, tick by tick** (numerics:\n"
    ">   0 non-permutation ticks in 1000, per-site occupation count identically 1) ⟹ **w ≡ 0 identically**,\n"
    ">   not merely with probability zero. ⟹ B2's \"no empty slot\" comes neither from a cross-layer\n"
    ">   transfer nor from site independence; **it is a direct consequence of the permutation bijection**.\n"
    "> · **The independent-Poisson substrate is excluded a second time**: `f* = 1/2 ⟹ w = 0.75` ⟹\n"
    ">   Hawking-temperature deviation **−5.77%** (the first ground was round 20's Δc/c = 26%; the two\n"
    ">   are unrelated and cross-validate each other).\n"
    "> · Solving the two constraints jointly, `H_S(1 − f²) = ln 16` gives **f = 1** or **f = 0.4765**;\n"
    ">   the latter leaves 52.3% of sites empty and conflicts with C-1 ⟹ excluded.\n"
    "> ⟹ **B2 closes the loop**: full occupancy (permutation bijection) ⟹ every bond carries flux ⟹ all\n"
    ">   4 in-plane connections live ⟹ A1's 50:50 assigns +/− to each ⟹ **2^4 = 16** ⟹ BH normalisation\n"
    ">   holds ⟹ the Hawking temperature is exact.\n"
    "> ⚠️ **Still open**: whether the \"plaquette connection\" and the \"lattice bond\" correspond strictly\n"
    "> has not been argued independently."
)

insert_after(ZH, "若压缩因子被重新导出，该约束会随之改变。", ZH_BLOCK, "ZH §4.8 w-f 同一性")
insert_after(EN, "if the compression factor is ever re-derived this constraint moves.", EN_BLOCK,
             "EN §4.8 w-f identity")

print("\n补丁完成：成功 %d 项，失败 %d 项" % (N_OK[0], N_FAIL[0]))
