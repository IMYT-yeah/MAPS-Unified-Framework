# -*- coding: utf-8 -*-
"""
第 39 轮论文补丁（d 段）：把 §4.8 里那条**过期开放项**指向第 39 轮的结项结论。

不改数值，只改"状态"：读者不应在第 39 轮块之后仍读到「11.0904 的自然性仍未解释」。
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
        print("  [XX] {:<30} 命中 {} 次 —— 拒绝".format(tag, n))
        N_FAIL[0] += 1
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<30} 已改".format(tag))
    N_OK[0] += 1


sub_once(
    ZH,
    "① 11.0904 非整数，其「自然性」仍未解释（它由 16 态与 1 纳特/块两个已知数逼出）；",
    "① ~~11.0904 非整数，其「自然性」仍未解释（它由 16 态与 1 纳特/块两个已知数逼出）~~ —— "
    "**第 39 轮已结项：判为伪问题**（它是「以比特计的槽位数 ÷ 以纳特计的熵」，必然含 ln2；"
    "既无枚举机制、也无几何机制、且不受观测约束，见上方第 39 轮块）；",
    "ZH §4.8 开放项状态",
)

sub_once(
    EN,
    "① 11.0904 is not an integer; its \"naturalness\" remains unexplained (it is forced by the two "
    "known numbers, 16 states and 1 nat/block);",
    "① ~~11.0904 is not an integer; its \"naturalness\" remains unexplained (it is forced by the two "
    "known numbers, 16 states and 1 nat/block)~~ — **closed in round 39 and declared a "
    "pseudo-problem** (it is \"slots counted in bits divided by an entropy in nats\", so it "
    "necessarily carries ln2; it has no enumerative mechanism, no geometric mechanism, and is "
    "constrained by no observation — see the round-39 block above);",
    "EN §4.8 open-item status",
)

print("")
print("通过 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
