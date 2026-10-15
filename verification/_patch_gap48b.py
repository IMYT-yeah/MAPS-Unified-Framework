# -*- coding: utf-8 -*-
"""第 48 轮论文补丁 b 段：「偏大 1.75 倍」判决的四条限定（行号修正版）。"""

import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

N_OK = [0]
N_FAIL = [0]

ZH_SUF = (" ⚠️ **第 48 轮更正**：该「偏大 1.75 倍」只是 **(2,2,L) 细长格点**的结果；"
          "真三维格点上 (2,4,4) = **0.2834**（+13%）、(4,4,4) = **0.1839**（**−26%**）"
          "⟹ 面积律要求的 0.25 **被跨过**（见第 48 轮块）。")
EN_SUF = (" ⚠️ **Corrected in round 48**: this \"≈1.75× too large\" is only the result of the **(2,2,L)** "
          "elongated lattices; on genuinely 3D lattices (2,4,4) = **0.2834** (+13%) and (4,4,4) = **0.1839** "
          "(**−26%**) ⟹ the 0.25 required by the area law is **straddled** (see the round-48 block).")


def load(p):
    return io.open(p, encoding="utf-8").read().split("\n")


def save(p, L):
    io.open(p, "w", encoding="utf-8").write("\n".join(L))


def app(L, idx, need, suf, tag):
    if need not in L[idx]:
        print("  [XX] {:<30} 行 {} 不含「{}」；实际：{}".format(tag, idx + 1, need[:26], L[idx][:70]))
        N_FAIL[0] += 1
        return
    if "第 48 轮更正" in L[idx] or "Corrected in round 48" in L[idx]:
        print("  [--] {:<30} 行 {} 已有限定，跳过".format(tag, idx + 1))
        return
    L[idx] = L[idx] + suf
    print("  [OK] {:<30} 第 {} 行已加限定".format(tag, idx + 1))
    N_OK[0] += 1


L = load(ZH)
app(L, 412, "偏大约 1.75 倍", ZH_SUF, "ZH 结果2(413)")
app(L, 419, "不变读数偏大约 1.75 倍", ZH_SUF, "ZH 第41轮(420)")
save(ZH, L)

L = load(EN)
app(L, 438, "Result 2 (an invariant readout carries too much entropy)", EN_SUF, "EN Result2(439)")
app(L, 446, "invariant readout too large by", EN_SUF, "EN round41(447)")
save(EN, L)

print()
print("=" * 70)
print("b 段：成功 {} 项，失败 {} 项".format(N_OK[0], N_FAIL[0]))
print("=" * 70)
