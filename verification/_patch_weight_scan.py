# -*- coding: utf-8 -*-
"""
第 33 轮论文补丁：在 §4.8 的第 32 轮裁决块之后，追加「权重 w 扫描」的结论块。
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
    "> **【v2.9 补充（第 33 轮：权重 w 扫描 —— B2 软肋的定量检验）】**\n"
    "> 上面取 B2 时留有一个软肋：C-b / C-c（「真空 / 湮灭中不占权重」）是否属于把衬底占位\n"
    "> 动力学的结论**跨层搬运**到面元状态计数。本轮显式引入权重 w 做扫描，**结论是 B2 不需要这一搬运**：\n"
    "> · **槽模型**（4 个平面内连接，每槽 ∈ {正, 负, 空}，空槽权重 w）：\n"
    ">   `H_S(w) = 4[h₂(w) + (1−w)ln2]`；要求 `H_S = ln 16`（BH 定标）⟹ 解只有 **w = 0** 与\n"
    ">   **w = 0.7729**，后者意味着 **77.3% 的平面内连接是空的**，与 C-b（满占位 f = 1）冲突而被排除。\n"
    ">   ⟹ **w = 0 是由 BH 熵定标与满占位共同解出的结果，不是搬来的假设。**\n"
    "> · **对照**：模型 A（1-of-4 方向 × 四态）的 w 被 BH 锁在 **0.500**，而 C-b / C-c 要求 **0**——\n"
    ">   落差 0.5；即便只要求 Hawking 温度偏差 ≤ 1%，也需 **w ≥ 0.3833**（≤ 5% 需 w ≥ 0.2489）。\n"
    ">   ⟹ **模型 A 是被两头夹死，不是略差。**\n"
    "> ⟹ **副产品**：B2 的「每条平面内连接恒有通量」由此获得出处（BH 定标 + 满占位），\n"
    ">   不再是无依据的构造假设；物理链条为：满占位 ⟹ 每格点被占 ⟹ 每条键承载通量 ⟹ 4 条\n"
    ">   平面内连接全活，再由 A1 的 50:50 各取正支 / 负支 ⟹ **2^4 = 16**。\n"
    "> ⚠️ **仍开放**：槽模型的「空槽率」w 与衬底占位率 f 是否为同一个量，未独立论证（本轮默认同一）；\n"
    ">   w = 0 是 BH 的**精确**要求，若压缩因子被重新导出，该约束会随之改变。"
)

EN_BLOCK = (
    "> **【v2.9 addendum (round 33: the weight-w scan — a quantitative test of B2's soft spot)】**\n"
    "> Adopting B2 above left one soft spot: whether C-b / C-c (\"vacuum / annihilating carry no weight\")\n"
    "> amount to **carrying a conclusion of the substrate-occupancy dynamics across layers** into the\n"
    "> plaquette state count. This round introduces the weight w explicitly and scans it;\n"
    "> **the conclusion is that B2 needs no such transfer**:\n"
    "> · **Slot model** (4 in-plane connections, each slot ∈ {+, −, empty}, empty weight w):\n"
    ">   `H_S(w) = 4[h₂(w) + (1−w)ln 2]`; requiring `H_S = ln 16` (BH normalisation) leaves only\n"
    ">   **w = 0** and **w = 0.7729**, the latter meaning **77.3% of the in-plane connections are empty**,\n"
    ">   which conflicts with C-b (full occupancy f = 1) and is excluded.\n"
    ">   ⟹ **w = 0 is solved for by BH normalisation together with full occupancy; it is not an\n"
    ">   imported assumption.**\n"
    "> · **Contrast**: model A (1-of-4 direction × four states) has its w pinned by BH at **0.500**,\n"
    ">   while C-b / C-c require **0** — a gap of 0.5. Even demanding only a Hawking-temperature\n"
    ">   deviation ≤ 1% requires **w ≥ 0.3833** (≤ 5% requires w ≥ 0.2489).\n"
    ">   ⟹ **Model A is caught between two constraints, not merely slightly worse.**\n"
    "> ⟹ **By-product**: B2's \"every in-plane connection always carries flux\" now has a provenance\n"
    ">   (BH normalisation + full occupancy) instead of being an unsupported construct; the chain is:\n"
    ">   full occupancy ⟹ every site occupied ⟹ every bond carries flux ⟹ all 4 in-plane connections\n"
    ">   live, and then A1's 50:50 assigns + or − branch to each ⟹ **2^4 = 16**.\n"
    "> ⚠️ **Still open**: whether the slot model's empty-slot rate w and the substrate occupancy f are\n"
    "> the same quantity has not been argued independently (assumed identical here); w = 0 is an\n"
    "> **exact** BH requirement, so if the compression factor is ever re-derived this constraint moves."
)

insert_after(ZH, "**第 19 轮「内部四态 q = 4 是唯一解」撤回**。", ZH_BLOCK, "ZH §4.8 w 扫描")
insert_after(EN, "is the unique solution\" is withdrawn**.", EN_BLOCK, "EN §4.8 w-scan")

print("\n补丁完成：成功 %d 项，失败 %d 项" % (N_OK[0], N_FAIL[0]))
