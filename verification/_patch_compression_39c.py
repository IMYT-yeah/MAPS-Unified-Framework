# -*- coding: utf-8 -*-
"""
第 39 轮论文补丁（c 段）：§4.10 命题 5（1/4 系数）里残留的最后一处「1 比特 / ln2」。

第 25 轮把同一处 ln2 错误在 12 个位置统一更正，本轮在收口核查中又发现**两处漏网**
（§4.9 的复述已由 39b 修掉，本条是 §4.10 命题 5）。这正是第 25 轮自己总结的教训：
「只改主段落，其余复述处会立刻自相矛盾」。锚点要求恰好命中一次。
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
        print("  [XX] {:<30} 命中 {} 次 —— 拒绝".format(tag, n))
        N_FAIL[0] += 1
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<30} 已改".format(tag))
    N_OK[0] += 1


sub_once(
    ZH,
    "→ 每单元 1 比特 ⟹ **S = (A/4l_P²)·ln2**，与 §4.8 微态计数**两条路径交叉验证**。",
    "→ 每单元 **1 纳特**（**第 39 轮单位更正**：原写「1 比特」并把换算残留在右侧括注里）"
    "⟹ **S/k_B = A/(4l_P²)（纳特）**，与 §4.8 微态计数**两条路径交叉验证**。",
    "ZH §4.10 命题 5 单位",
)

sub_once(
    EN,
    "→ 1 bit per unit ⟹ **S = (A/4l_P²)·ln2**, cross-validated with the §4.8 microstate counting "
    "as **two paths**.",
    "→ **1 nat** per unit (**round-39 unit correction**: it read \"1 bit\", with the conversion left "
    "dangling in the factor ln2 on the right) ⟹ **S/k_B = A/(4l_P²) (nats)**, cross-validated with the "
    "§4.8 microstate counting as **two paths**.",
    "EN §4.10 Theorem-5 unit",
)

print("")
print("通过 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
