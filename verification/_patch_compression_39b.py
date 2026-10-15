# -*- coding: utf-8 -*-
"""
第 39 轮论文补丁（b 段）：把 §4.9 里对「每 4 面元 1 比特」的**复述处**一并对齐。

理由（第 25 轮教训）：同一处单位/标注错误散落在多处复述里，只改主段落必留自相矛盾。
本段只处理 §4.9 的复述与「标注错位」条目（它们不在 §4.8 的 v2.8 更正声明覆盖范围内）。
锚点要求恰好命中一次。
"""

import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

N_OK = [0]
N_FAIL = [0]


def sub_once(path, old, new, tag):
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<34} 命中 {} 次 —— 拒绝".format(tag, n))
        N_FAIL[0] += 1
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<34} 已改".format(tag))
    N_OK[0] += 1


# ------------------------------------------------------------------ ZH
sub_once(ZH, "每 4 面元 1 比特、Clifford 4 分量", "每 4 面元 1 纳特、Clifford 4 分量", "ZH 分级注·复述")

sub_once(ZH, "每 4 面元 1 比特、挂谷 packing 1/4",
         "每 4 面元 1 纳特（**第 39 轮单位更正**）、挂谷 packing 1/4", "ZH 分层判定·复述")

sub_once(
    ZH,
    "> ⚠️ 标注错位（建议修正）：① 表面 4 邻居标的「本框架推论」其实直接依据 §4.9 引理 1【本框架设定】；"
    "④「每 4 面元 1 比特」标【本框架设定】但可由 ③ 直接推出。",
    "> ⚠️ 标注错位（**第 39 轮已修正**）：① 表面 4 邻居原标「本框架推论」，其实直接依据 "
    "§4.9 引理 1【本框架设定】；④「每 4 面元 1 比特」原标【本框架设定】**且单位有误** —— "
    "应为 **1 纳特**（§4.8 的 Hawking 温度裁决），并可由 ③ 的 packing 命题直接推出。"
    "本行之上「六处\"4\"同源」清单中的两处标注已同步更正。",
    "ZH 标注错位条目",
)

# ------------------------------------------------------------------ EN
sub_once(EN, "4l_P² coherent cross-section, 1 bit per 4 plaquettes, Clifford 4 components, Kakeya 1/4)",
         "4l_P² coherent cross-section, 1 nat per 4 plaquettes, Clifford 4 components, Kakeya 1/4)",
         "EN graded note·restatement")

sub_once(EN, "4l_P² coherent cross-section, 1 bit per 4 plaquettes, Kakeya packing 1/4",
         "4l_P² coherent cross-section, 1 nat per 4 plaquettes (**round-39 unit correction**), "
         "Kakeya packing 1/4",
         "EN layered verdict·restatement")

sub_once(
    EN,
    "> ⚠️ Label mismatch (worth fixing): ① \"4 neighbours of a surface element\" is labelled "
    "\"framework corollary\" but rests directly on §4.9 Lemma 1【framework assumption】; "
    "④ \"1 bit per 4 plaquettes\" is labelled 【framework assumption】 but follows directly from ③.",
    "> ⚠️ Label mismatch (**fixed in round 39**): ① \"4 neighbours of a surface element\" was labelled "
    "\"framework corollary\" but rests directly on §4.9 Lemma 1【framework assumption】; "
    "④ \"1 bit per 4 plaquettes\" was labelled 【framework assumption】 **and carried a unit error** — "
    "it is **1 nat** (Hawking-temperature verdict of §4.8) and follows directly from ③'s packing "
    "proposition. Both labels in the \"six occurrences\" list above have been corrected accordingly.",
    "EN label-mismatch item",
)

print("")
print("通过 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
