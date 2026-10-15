# -*- coding: utf-8 -*-
"""§4.10/§4.11 的 B5 重述处：补齐单位与 k 的修正（中英同步）"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT, FAIL = [], []


def rep(path, tag, old, new):
    s = open(path, encoding="utf-8").read()
    n = s.count(old)
    if n != 1:
        FAIL.append("%s｜%s：命中 %d 次" % (os.path.basename(path), tag, n))
        print("  [XX] %-40s 命中 %d 次" % (tag, n))
        return
    open(path, "w", encoding="utf-8").write(s.replace(old, new, 1))
    OUT.append("%s｜%s" % (os.path.basename(path), tag))
    print("  [OK] %-40s 已改" % tag)


ZH = [
    ("§4.10｜Bekenstein 界（每 4 面元 1 比特）",
     "（k=4 ⟹ 每 4 面元 1 比特）⟹ **S ≤ A/(4l_P²)**——与 k=2^{1/4} 微态计数（\"=\"方向）**双闭合**",
     "（k=4 ⟹ 每 4 面元 **1 纳特**，v2.9 更正）⟹ **S ≤ A/(4l_P²)**（纳特）——与 k=e^{1/4} 微态计数（\"=\"方向）**双闭合**"),
    ("§4.11｜B5 重述（16 倍压缩 → 16 ln2）",
     "**16 倍压缩**：观测者原始可读 4 bits/面元 × 相干块（4面元×4方向=16 自由度→1 比特，k 模型）⟹ 熵密度 1/4 bit/面元 = 1/(4l_P²)【本框架推论：\"每 4 面元 1 bit\"】——观测者信息容量统一公式 S_max=(A/l_P²)×(4÷16)=A/(4l_P²)。",
     "**相干压缩 = 16 ln 2 = 11.0904**：观测者原始可读 **4 bits/面元**（= 4 方向 × 4 状态 = 16 原始态）× 相干块（4 面元）⟹ 原始熵 4·ln16 = 11.0904 纳特 → **每块 1 纳特**（v2.9 更正，原「1 比特」差一个 ln2）⟹ 熵密度 **1/4 纳特/面元 = 0.3607 bit/面元** = 1/(4l_P²)【本框架推论：每 4 面元 1 纳特】——观测者信息容量统一公式 S_max=(A/l_P²)×(4÷16)=A/(4l_P²)（纳特）。"),
]

EN = [
    ("§4.10｜Bekenstein bound (1 bit / 4 plaquettes)",
     "(k=4 ⟹ 1 bit per 4 plaquettes) ⟹ **S ≤ A/(4l_P²)** — doubly closed with the k=e^{1/4} microstate counting",
     "(k=4 ⟹ **1 nat** per 4 plaquettes, v2.9 correction) ⟹ **S ≤ A/(4l_P²)** (nats) — doubly closed with the k=e^{1/4} microstate counting"),
    ("§4.11｜B5 restatement (16-fold → 16 ln2)",
     "**16-fold compression**: observer's raw 4 bits/plaquette × coherent block (4 plaquettes × 4 directions = 16 degrees of freedom → 1 bit, k model) ⟹ entropy density 1/4 bit/plaquette = 1/(4l_P²)【Framework corollary: \"1 bit per 4 plaquettes\"】 — unified observer information-capacity formula S_max=(A/l_P²)×(4÷16)=A/(4l_P²).",
     "**coherent compression = 16 ln 2 = 11.0904**: the observer's raw **4 bits/plaquette** (= 4 directions × 4 states = 16 raw states) × coherent block (4 plaquettes) ⟹ raw entropy 4·ln16 = 11.0904 nats → **1 nat per block** (v2.9 correction; the former \"1 bit\" is off by ln2) ⟹ entropy density **1/4 nat/plaquette = 0.3607 bit/plaquette** = 1/(4l_P²)【Framework corollary: 1 nat per 4 plaquettes】 — unified observer information-capacity formula S_max=(A/l_P²)×(4÷16)=A/(4l_P²) (nats)."),
]

jobs = [(os.path.join(HERE, "论文初稿_正反物质对风暴统一框架_v2.9.md"), ZH),
        (os.path.join(HERE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md"), EN)]

for p, lst in jobs:
    print("\n" + "=" * 68 + "\n" + os.path.basename(p) + "\n" + "=" * 68)
    for tag, old, new in lst:
        rep(p, tag, old, new)

print("\n完成 %d 项；失败：%s" % (len(OUT), "；".join(FAIL) if FAIL else "无"))
