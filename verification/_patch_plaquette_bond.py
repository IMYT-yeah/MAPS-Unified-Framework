# -*- coding: utf-8 -*-
"""
第 35 轮论文补丁：在 §4.8 的第 34 轮块之后，追加「面元 ↔ 键」显式构造的结论块。
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
    "> **【v2.9 补充（第 35 轮：「面元 ↔ 键」的显式构造）】** 上一条的开放项**已处理**：\n"
    "> · **构造**：面元 = 格点在「现在平面」内的**对偶面元**（面积 l_P² ⟹ 面元数 = A/l_P²\n"
    ">   ⟹ 面积律自洽）；面元的 4 条「平面内连接」= 该格点到 4 个平面内邻居（±x, ±y）的**键**。\n"
    "> · **计数**（L=8 平面）：面元数 64、槽位 256、**不同键 128 = 2×64**、每条键的共享重数**恰为 2** ✓。\n"
    "> · **「相邻面元强相关」第一次有了机制**：不是统计相关，而是**恒等约束**——\n"
    ">   相邻面元共享同一条键，两个槽位必须取同一个值（同一条键所承载的正 / 负支不能分身）。\n"
    ">   绑定对数 = 键数 = 128 ⟹ 独立自由度 = `4N_p − N_b = 2N_p`（每面元 2 条独立键）。\n"
    "> · **压缩因子第一次有了部分机制**：\n"
    ">   **`16 ln2 = 2`（键共享，已有机制）`× 8 ln2 = 5.545`（仍无机制）**。\n"
    ">   ⚠️ 只解释了因子 2；剩余 **5.545 仍未解释**，不得包装成完整推导。\n"
    "> · **措辞纠正**：B5 的「4 面元 × 4 方向 = 16 自由度」中，16 是**槽位数**而非独立自由度数\n"
    ">   （2×2 块实测：16 槽位 ⟶ **12** 条不同键 = 4 条块内键 + 8 条跨界键）。\n"
    "> ⚠️ **仍开放**：剩余压缩 5.545 无机制；「面元 = 格点对偶面元」仍是本轮的**定义**\n"
    ">   （§4.9 引理 1 只说「平面内 4 方向连接」，未明说是格点的对偶面元），该对应的唯一性未论证。"
)

EN_BLOCK = (
    "> **【v2.9 addendum (round 35: explicit construction of the plaquette ↔ bond correspondence)】**\n"
    "> The open item above is **resolved**:\n"
    "> · **Construction**: a plaquette is the **dual cell** of a site inside the present plane\n"
    ">   (area l_P² ⟹ number of plaquettes = A/l_P² ⟹ the area law is consistent); its four\n"
    ">   \"in-plane connections\" are the **bonds** from that site to its four in-plane neighbours (±x, ±y).\n"
    "> · **Counting** (L = 8 plane): 64 plaquettes, 256 slots, **128 distinct bonds = 2 × 64**, and every\n"
    ">   bond has multiplicity **exactly 2** ✓.\n"
    "> · **The \"strong correlation of adjacent plaquettes\" finally has a mechanism**: it is not a\n"
    ">   statistical correlation but an **identity constraint** — adjacent plaquettes share one and the\n"
    ">   same bond, so the two slots must take the same value (one bond cannot carry two branches).\n"
    ">   Number of bound slot pairs = number of bonds = 128 ⟹ independent degrees of freedom\n"
    ">   `4N_p − N_b = 2N_p` (2 independent bonds per plaquette).\n"
    "> · **The compression factor has a partial mechanism for the first time**:\n"
    ">   **`16 ln 2 = 2` (bond sharing, mechanism found) `× 8 ln 2 = 5.545` (no mechanism yet)**.\n"
    ">   ⚠️ Only the factor 2 is explained; the remaining **5.545 stays unexplained** and must not be\n"
    ">   dressed up as a complete derivation.\n"
    "> · **Wording corrected**: in B5's \"4 plaquettes × 4 directions = 16 degrees of freedom\", 16 is the\n"
    ">   number of **slots**, not of independent degrees of freedom (measured on a 2×2 block: 16 slots ⟶\n"
    ">   **12** distinct bonds = 4 internal + 8 crossing).\n"
    "> ⚠️ **Still open**: the residual factor 5.545 has no mechanism; \"plaquette = dual cell of a site\"\n"
    ">   remains a **definition** adopted here (§4.9 Lemma 1 speaks only of \"four in-plane connections\"),\n"
    ">   and the uniqueness of this correspondence has not been argued."
)

insert_after(ZH, "「面元连接」与「格点键」是否严格对应，未独立论证。", ZH_BLOCK, "ZH §4.8 面元-键")
insert_after(EN, "has not been argued independently.", EN_BLOCK, "EN §4.8 plaquette-bond")

print("\n补丁完成：成功 %d 项，失败 %d 项" % (N_OK[0], N_FAIL[0]))
