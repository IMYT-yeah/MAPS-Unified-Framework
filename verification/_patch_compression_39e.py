# -*- coding: utf-8 -*-
"""
第 39 轮论文补丁（e 段）：**结论处的状态同步**（把"推出 S = A/4"降为"与 S = A/4 一致"）。

理由：第 39 轮判定「压缩因子 11.0904 系由 BH 反解 ⟹ 该链条对 S = A/4 无预言力」。
§4.8 的块内与开放项已注明，但 §10 结论仍把「S=A/4 微态计数」列为成就而不带条件
⟹ 与 §4.8 冲突。本段补一句限定，不改任何数值。锚点要求恰好命中一次。
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
    "Jacobson 涌现路径；S=A/4 微态计数（k=e^{1/4}）；",
    "Jacobson 涌现路径；S=A/4 微态计数（k=e^{1/4}；**第 39 轮状态更正**：其压缩因子 "
    "11.0904 系由 BH 反解，**属与 S=A/4 一致的一致性构造，不是对 S=A/4 的独立推导** —— "
    "详见 §4.8 第 39 轮块）；",
    "ZH 结论·S=A/4 状态",
)

sub_once(
    EN,
    "Jacobson emergence path; S=A/4 microstate counting (k=e^{1/4});",
    "Jacobson emergence path; S=A/4 microstate counting (k=e^{1/4}; **round-39 status "
    "correction**: its compression factor 11.0904 was reverse-engineered from BH, so it is a "
    "**consistency construction with S=A/4, not an independent derivation of S=A/4** — see the "
    "round-39 block in §4.8);",
    "EN conclusion·S=A/4 status",
)

print("")
print("通过 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
