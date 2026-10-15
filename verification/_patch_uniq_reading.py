# -*- coding: utf-8 -*-
"""
第 38 轮论文补丁：解除第 35 轮登记的「对应唯一性未论证」。
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


def replace_once(path, key, old, new, tag):
    lines = load(path)
    hits = [i for i, L in enumerate(lines) if key in L]
    if len(hits) != 1:
        print("  [XX] %-22s 命中 %d 行 —— 拒绝" % (tag, len(hits)))
        N_FAIL[0] += 1
        return
    i = hits[0]
    if old not in lines[i]:
        print("  [XX] %-22s 行内未找到待替换子串" % tag)
        N_FAIL[0] += 1
        return
    lines[i] = lines[i].replace(old, new)
    save(path, lines)
    print("  [OK] %-22s 已替换（第 %d 行）" % (tag, i + 1))
    N_OK[0] += 1


ZH_OLD = "该对应的唯一性未论证。"
ZH_NEW = ("该对应的唯一性未论证。**（第 38 轮已解除）** 另一种同样自然的读法是"
          "「面元 = 真方格面、连接 = 4 条有向边」。在方格格点上两种读法**逐项计数完全相同**"
          "（L=8：面元 64 / 槽位 256 / 不同对象 128 / 共享重数 2 / 独立自由度 2 每面元），"
          "因为**方格格点是自对偶的**（其对偶仍为方格）⟹ 二者是同一结构的两种画法，"
          "**无需在两者间选择，本条结论不受读法影响**。检验非空：在蜂巢（非自对偶）上，"
          "两种读法给 3 条 vs 6 条连接/面元，计数分歧 ⟹ 自对偶性是决定性因素，"
          "而这依赖 T-6 裁决的简单立方（其平面截面为方格）。")

EN_OLD = "the uniqueness of this correspondence has not been argued."
EN_NEW = ("the uniqueness of this correspondence has not been argued. **(Round 38 has removed this "
          "caveat.)** The equally natural alternative is \"plaquette = actual square face, connections = "
          "four oriented edges\". On the square lattice the two readings agree **item by item** "
          "(L = 8: 64 plaquettes / 256 slots / 128 distinct objects / multiplicity 2 / 2 independent "
          "degrees of freedom per plaquette), because **the square lattice is self-dual** (its dual is "
          "again a square lattice) ⟹ they are two drawings of one and the same structure; **no choice "
          "between them is needed and the conclusion is independent of the reading.** The test is not "
          "vacuous: on the honeycomb lattice (not self-dual) the two readings give 3 vs 6 connections "
          "per plaquette, i.e. the counts diverge ⟹ self-duality is the decisive factor, and it rests "
          "on the simple cubic lattice of the T-6 verdict (whose planar section is a square lattice).")

replace_once(ZH, "该对应的唯一性未论证。", ZH_OLD, ZH_NEW, "ZH §4.8 唯一性")
replace_once(EN, "the uniqueness of this correspondence has not been argued.", EN_OLD, EN_NEW,
             "EN §4.8 uniqueness")

print("\n补丁完成：成功 %d 项，失败 %d 项" % (N_OK[0], N_FAIL[0]))
