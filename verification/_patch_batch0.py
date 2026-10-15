# -*- coding: utf-8 -*-
"""
第 0 批执行补丁（中英同步）：
    0.1 裁决 T-12 —— §7.4 的「底层确定」→「给定 tick 序列后确定」（方案 b）
    0.2② 补一处漏网 —— §8.6.5 判别表里的 `λ_micro = 8π/3` → `Ω_tot = 3/(8π)`

（0.2① 因果补丁 / 0.2③ ξ-稳健性 经核查**已完成**，本轮不打补丁，只在交接说明勾掉。）

锚点必须恰好命中一次，否则拒绝改动。
"""
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

OK = 0
BAD = 0
def sub_once(path, old, new, tag):
    global OK, BAD
    txt = io.open(path, encoding="utf-8").read()
    n = txt.count(old)
    if n != 1:
        print("  [XX] {:<34} 命中 {} 次 —— 拒绝".format(tag, n))
        BAD += 1
        return
    io.open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print("  [OK] {:<34} 已改".format(tag))
    OK += 1

print("第 0 批补丁（0.1 T-12 裁决 ＋ 0.2② 补漏）")

# ================================================================
# 0.1  ZH §7.4 正文
OLD = "定位是 **'t Hooft 元胞自动机式**：底层确定事件流，可观测代数非交换。"
NEW = ("定位是 **'t Hooft 元胞自动机式**：**给定 tick 序列后确定**"
       "（单 tick 为置换 ⟹ 双射、可逆、无熵产生，§8.6.7）的事件流，可观测代数非交换。"
       "⚠️ 此处**不**声称「整体决定论」—— tick 序列本身是外生输入，其随机性来源在框架内不可判定"
       "（裁决记录见下方第 57 轮块）。")
sub_once(ZH, OLD, NEW, "0.1 ZH §7.4 正文")

# 0.1  EN §7.4
OLDE = ("The positioning is **'t Hooft cellular-automaton-like**: "
        "underlying deterministic event flow, non-commutative observable algebra.")
NEWE = ("The positioning is **'t Hooft cellular-automaton-like**: an event flow that is "
        "**deterministic given the tick sequence** (each tick is a permutation ⟹ bijective, "
        "reversible, zero entropy production, §8.6.7), with a non-commutative observable algebra. "
        "⚠️ This does **not** claim global determinism — the tick sequence itself is an exogenous "
        "input, and the provenance of its randomness is undecidable within the framework "
        "(see the adjudication record in the round-57 block below).")
sub_once(EN, OLDE, NEWE, "0.1 EN §7.4 body")

# ================================================================
# 0.1  ZH §10 结论侧加限定
OLD2 = "- **量子侧**：非交换化闭环（CHSH=2√2、互补性）；'t Hooft 式定位；"
NEW2 = ("- **量子侧**：非交换化闭环（CHSH=2√2、互补性）；'t Hooft 式定位"
        "（底层**给定 tick 序列后确定**，**非**「决定论」—— 见 §7.4 的 2026-09-28 裁决）；")
sub_once(ZH, OLD2, NEW2, "0.1 ZH §10 结论")

OLDE2 = ("- **Quantum side**: non-commutativization closure (CHSH=2√2, complementarity); "
         "'t Hooft-like positioning;")
NEWE2 = ("- **Quantum side**: non-commutativization closure (CHSH=2√2, complementarity); "
         "'t Hooft-like positioning (deterministic **given the tick sequence**, **not** \"determinism\" "
         "— see the 2026-09-28 adjudication in §7.4);")
sub_once(EN, OLDE2, NEWE2, "0.1 EN §10 conclusion")

# ================================================================
# 0.1  第 57 轮块：标记 T-12 已裁决
OLD3 = ("⟹ 需一次**显式裁决**：或明确采用 H2 并在此加注，或把「底层确定」改为"
        "「**给定 tick 序列后确定**」（只声称可逆性，不声称决定论）。")
NEW3 = ("⟹ ~~需一次显式裁决~~ **✅ 已裁决（2026-09-28，第 0 批）**：采用**方案 (b)** —— "
        "§7.4 正文已改为「**给定 tick 序列后确定**」（只声称可逆性，不声称决定论）；"
        "**不采用 H2**（那需一并改写第 42 轮的 H1 工作表述，成本高且无必要）。")
sub_once(ZH, OLD3, NEW3, "0.1 ZH 第57轮块标记已裁决")

OLDE3 = ("⟹ An **explicit adjudication** is required: either adopt H2 and annotate here, "
         "or change \"underlying deterministic\" to \"**deterministic given the tick sequence**\" "
         "(claiming only reversibility, not determinism).")
NEWE3 = ("⟹ ~~An explicit adjudication is required~~ **✅ Adjudicated (2026-09-28, batch 0)**: "
         "**option (b)** adopted — the §7.4 body now reads \"**deterministic given the tick sequence**\" "
         "(claiming only reversibility, not determinism); **H2 is not adopted** (that would require "
         "rewriting round 42's H1 working statement — costly and unnecessary).")
sub_once(EN, OLDE3, NEWE3, "0.1 EN round-57 block adjudicated")

# ================================================================
# 0.2②  λ_micro 漏网（§8.6.5 判别表）
#       λ_micro = 8π/3 与 Ω_tot = 3/(8π) 互为倒数（8.3776 × 0.11937 = 1.0000）
#       ⟹ 统一为全文已用的 Ω_tot 记号
OLD4 = "| 表观视界（λ_micro = 8π/3） | 0.3455 | 0.1194 | +0.881 | ❌ 差 O(1) |"
NEW4 = "| 表观视界（Ω_tot = 3/(8π) 精确值） | 0.3455 | 0.1194 | +0.881 | ❌ 差 O(1) |"
sub_once(ZH, OLD4, NEW4, "0.2② ZH λ_micro → Ω_tot")

OLDE4 = "| Apparent horizon (λ_micro = 8π/3) | 0.3455 | 0.1194 | +0.881 | ❌ O(1) off |"
NEWE4 = "| Apparent horizon (Ω_tot = 3/(8π) exact) | 0.3455 | 0.1194 | +0.881 | ❌ O(1) off |"
sub_once(EN, OLDE4, NEWE4, "0.2② EN λ_micro → Ω_tot")

print("\n通过 {} 项，失败 {} 项".format(OK, BAD))
