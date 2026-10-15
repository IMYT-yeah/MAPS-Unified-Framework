# -*- coding: utf-8 -*-
"""第 135 轮论文补丁：C-89（§9 #8 ↔ §4.8 矛盾）＋ 面积律口径（互信息 ≠ 纠缠熵）＋ N-50 口径注。
中英同步；正式稿 v3.0 同步（按其「注记规范」不带轮号）。
锚点必须恰好命中一次，否则整份文件拒绝改动。
"""
import pathlib, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

NOTE_ZH = """> ⚠️ **【v2.9 口径注（第 135 轮：量子纠缠态／叠加态的「身份主张」判否 **N-50**）】** 承第 57／76 轮：框架**没有量子态层**（「塌缩／波函数／测量问题／量子测量／密度矩阵／退相干／幺正」**各 0 处**），观测者是**经典粗粒化**（互信息），**不改变**被观测系统的态。故两条身份主张 —— 「**量子纠缠态 = 底层湮灭产生的某种结构状态**」与「**叠加态 = 某个稳定状态的前置结构**」—— **在框架内无载体**：纠缠的定义性特征是**非局域两体关联**，而框架底层对象**全是局域构型**（全文「非局域／两体」**各 0 处**）；唯一的跨格点通道 = 量子直线／跨支 ER 通道，第 55 轮已判**只载信息、不载能量**。⚠️ 另须与 §9 #8 一并读：**框架的面积律是观测者互信息 `I(R;Σ)`（经典量），不是量子纠缠熵 `S_A`**（全文无 `S_A`／约化密度矩阵）；且 `H(R|Σ)=0` **单独**只给出 `I=H(R)`，要得 `I=H(Σ)` 还需**反向**条件熵为零（**体↔面双射**）。⚠️ 四类判定：三条子主张**全部 = 失败**，**真预言 0 条**。"""

NOTE_EN = """> ⚠️ **【v2.9 note (round 135: the "identity" claims for quantum entanglement / superposition — rejected, **N-50**)**】 Continuing rounds 57/76: the framework has **no quantum-state layer** ("collapse / wave function / measurement problem / quantum measurement / density matrix / decoherence / unitary" — **0 occurrences each**), and the observer is a **classical coarse-graining** (mutual information) that **does not change** the observed state. Hence the two identity claims — "**quantum entanglement = some structural state produced by substrate annihilation**" and "**superposition = the precursor of a stable state**" — **have no carrier in the framework**: the defining feature of entanglement is a **non-local two-body correlation**, whereas every substrate object is a **local configuration** ("non-local / two-body" occur **0 times**); the only inter-site channel (quantum straight line / cross-branch ER channel) was already ruled in round 55 to **carry information only, not energy**. ⚠️ Read together with §9 #8: **the framework's area law is the observer mutual information `I(R;Σ)` (a classical quantity), not the quantum entanglement entropy `S_A`** (no `S_A` / reduced density matrix anywhere); and `H(R|Σ)=0` **alone** yields only `I=H(R)`; to obtain `I=H(Σ)` the **reverse** conditional entropy must also vanish (**bulk↔boundary bijection**). ⚠️ Four-way verdict: all three sub-claims = **failed**; **true predictions: 0**. """

NOTE_FIN = """> ⚠️ **口径注**：框架**没有量子态层**（「塌缩／波函数／测量问题／量子测量／密度矩阵／退相干／幺正」**各 0 处**），观测者是**经典粗粒化**（互信息），**不改变**被观测系统的态。故「**量子纠缠态 = 底层湮灭的结构状态**」与「**叠加态 = 稳定态的前置结构**」两条**身份主张在框架内无载体**：纠缠的定义性特征是**非局域两体关联**，而框架底层对象**全是局域构型**（全文「非局域／两体」**各 0 处**）；唯一跨格点通道（量子直线／跨支 ER 通道）**只载信息、不载能量**。⚠️ 与 §9 #8 一并读：**框架的面积律是观测者互信息 `I(R;Σ)`（经典量），不是量子纠缠熵**；`H(R|Σ)=0` **单独**只给出 `I=H(R)`，要得 `I=H(Σ)` 还需**体↔面双射**。"""

ROW_ZH = "| 8 | ~~纠缠熵面积律系数（框架含 ln 2 因子）~~ ⚠️ **非框架预言**：该 ln 2 因子是 **bit↔nat 单位换算**（`16 ln 2 = 11.0904`）；框架的面积律是**观测者互信息** `I(R;Σ)`（**经典量**），**不是**量子纠缠熵 | 量子模拟/多体系统 | ⚠️ **降调：已判为伪问题（见 §4.8）** |"
ROW_EN = "| 8 | ~~entanglement-entropy area-law coefficient (framework contains ln 2 factor)~~ ⚠️ **not a framework prediction**: the ln 2 factor is a **bit↔nat unit conversion** (`16 ln 2 = 11.0904`); the framework's area law is the **observer mutual information** `I(R;Σ)` (**classical**), **not** the quantum entanglement entropy | quantum simulation / many-body systems | ⚠️ **downgraded: judged a pseudo-problem (see §4.8)** |"

A_ROW_ZH = "| 8 | 纠缠熵面积律系数（框架含 ln 2 因子） | 量子模拟/多体系统 | 理论可检验 |"
A_ROW_EN = "| 8 | entanglement-entropy area-law coefficient (framework contains ln 2 factor) | quantum simulation / many-body systems | theoretically testable |"
A_74_ZH = "⑤ 本轮**不改 §7.1–§7.4 的正文措辞**，只追加本块与 §7.2 的一条判别力标注。"
A_74_EN = "⑤ this round **does not alter the wording of §7.1–§7.4**, adding only this block plus one discriminating-power annotation in §7.2."
A_74_FIN = "其随机性来源在框架内不可判定（裁决记录见下方口径注）。"

JOBS = [
    # (path, [(anchor, replacement, 期望命中)])
    ("论文初稿_正反物质对风暴统一框架_v2.9.md", [
        (A_ROW_ZH, ROW_ZH, 1),
        (A_74_ZH,  A_74_ZH + "\n>\n" + NOTE_ZH, 1),
    ]),
    ("Paper_MatterAntimatterPairStorm_v2.9_EN.md", [
        (A_ROW_EN, ROW_EN, 1),
        (A_74_EN,  A_74_EN + "\n>\n" + NOTE_EN, 1),
    ]),
    ("论文_正式稿_v3.0.md", [
        (A_ROW_ZH, ROW_ZH, 1),
        (A_74_FIN, A_74_FIN + "\n\n" + NOTE_FIN, 1),
    ]),
]

fail = 0
for path, ops in JOBS:
    p = pathlib.Path(path)
    S = p.read_text(encoding='utf-8')
    n0 = len(S)
    newS = S
    for anc, rep, want in ops:
        c = newS.count(anc)
        ok = (c == want)
        print('[%s] %-46s 命中 %d（期望 %d）' % ('OK' if ok else 'XX', path[:44], c, want))
        if not ok:
            fail += 1
        else:
            newS = newS.replace(anc, rep, 1)
    if fail:
        print('   ⟹ 有锚点未命中，本文件**拒绝写入**')
        continue
    p.write_text(newS, encoding='utf-8')
    print('   ⟹ 已写入  %d -> %d（%+d 字符）' % (n0, len(newS), len(newS) - n0))

print()
print('锚点失败 %d 处' % fail)
