# -*- coding: utf-8 -*-
"""第 123 轮补丁（一）：论文中英各加 1 处判定注（§8.6.3，第 75 轮块后）。
锚点：run 起 = '> **【v2.9 补充（第 75 轮' （ZH） / '> **【v2.9 supplement (Round 75:'（EN）；
插入点 = run 末行之后的空行之后、'#### 8.6.4' 之前。
"""
import io, os

BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
ZH = os.path.join(BASE, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md')
EN = os.path.join(BASE, 'outputs', 'Paper_MatterAntimatterPairStorm_v2.9_EN.md')

def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, t): io.open(p, 'w', encoding='utf-8').write(t)

ZH_NOTE = [
"> **【v2.9 判定（第 123 轮：动力学·耦合层的可行性）】** 题源 = 第 122 轮瓶颈分析（「衬底 ↔ 对称骨架之间缺动力学·耦合层」）→ 用户问「能不能做？」。判定分三档：",
"> · ⛔ **作为从现有公理出发的内部推导 —— 判否**（登记 **N-43**）。依据 = 三条**结构性障碍**（非工作量问题）：① §4.9 的**位置量子化缺口**（**I-16**：三层中没有一层同时具备「位置 ＋ 能量 ＋ 位置是 q-数」）；② 本节的**两个 `ρ` 不接**（**I-20**：缺的不是方程，是对象）；③ §7 的**非交换化缺口**（**I-21**：唯一非交换的 Clifford 投影是记号）。加**终止态台账**（第 53–112 轮间 **15 例**耦合/动力学推导尝试，**无一落在「推导成功」**：恒等式/换写 6 ｜ 量纲不成立 1 ｜ 无对象 2 ｜ 缺换算因子 1 ｜ 外加 1 ｜ 排除 1 ｜ 自由输入 2 ｜ 填的 1）。",
"> · ✅ **作为「条件构造」（显式声明输入 ＋ 自洽性过滤）—— 可做，且已在做**：三个样板 = 度规扇区（B3：三条框架内线索收敛 ⟹ 指数度规 ⟹ EMRI）／Φ 扇区（§6.4 ＋ 第 61–72 轮 ⟹ 第五力窗口）／A2 动能扇区（§8.1 ⟹ `E_c` 能标与 `τ = t_P`）。**框架目前全部对外产出都出自这一档。**",
"> · ⚖️ 「它该不该存在」：宇宙学侧已判定为**「不该有」**（本节 I-20）；耦合侧「无对象」（N-33／N-35）。",
"> ⚠️ **失效条件**（本判否的边界）：**任何新增公理级输入**（例如把 §6.1 的 Φ 背景量子化 —— 第 68 轮边界句「引力量子化之日，就是这条边界消失之时」）会使第一档**自动重开**。",
"> 详见 `outputs/动力学耦合层可行性_三档判定与输入台账.md`（核验 `_dyn123_verify.py`，«ND123C»）。",
]

EN_NOTE = [
"> **【v2.9 determination (Round 123: feasibility of the \"dynamics·coupling layer\")】** Origin = round 122's bottleneck analysis (\"a dynamics·coupling layer is missing between the substrate and the symmetry skeleton\"); the question: \"can it be built?\". Three-way verdict:",
"> · ⛔ **As an internal derivation from the existing axioms - ruled out** (registered as **N-43**), on three **structural obstacles** (not a matter of effort): ① the position-quantisation gap of §4.9 (**I-16**: no layer has \"position + energy + position as a q-number\" simultaneously); ② the two unconnected `ρ`'s of this section (**I-20**: what is missing is not an equation but an object); ③ the non-commutativity gap of §7 (**I-21**: the only non-commutative Clifford projection is notation). Plus a 15-instance ledger of terminal states (rounds 53-112: identity/rewriting 6; dimensional failure 1; no object 2; missing conversion factors 1; externally added 1; excluded 1; free inputs 2; fitted 1 - **none reached \"derivation succeeded\"**).",
"> · ✅ **As a \"conditional construction\" (explicit inputs + self-consistency filter) - feasible, and already in use**: three exemplars = the metric sector (B3: three in-framework threads converge ⟹ exponential metric ⟹ EMRI); the Φ sector (§6.4 + rounds 61-72 ⟹ fifth-force window); the A2 kinetic sector (§8.1 ⟹ `E_c` scale and `τ = t_P`). **All current external outputs of the framework come from this track.**",
"> · ⚖️ \"Should it exist\": the cosmological side was already judged **\"should not\"** (I-20 above); the coupling side \"no object\" (N-33/N-35).",
"> ⚠️ **Failure condition**: any **new axiom-level input** (e.g. quantising the §6.1 Φ background - round 68's boundary sentence \"the day gravity is quantised, this boundary disappears\") reopens the first track automatically.",
"> See `outputs/动力学耦合层可行性_三档判定与输入台账.md` (`_dyn123_verify.py`, «ND123E»).",
]

def insert_note(path, startpred, nextpred, note, tag):
    t = rd(path)
    L = t.split('\n')
    idx = [k for k, s in enumerate(L) if startpred(s)]
    assert len(idx) == 1, (tag, 'run-start 命中 %d' % len(idx))
    i = idx[0]; j = i
    while j + 1 < len(L) and L[j + 1].startswith('>'):
        j += 1
    assert L[j + 1].strip() == '', (tag, 'run 后非空行', repr(L[j + 1][:60]))
    assert nextpred(L[j + 2]), (tag, '下一行非预期', repr(L[j + 2][:60]))
    L[j + 2:j + 2] = note + ['']
    t2 = '\n'.join(L)
    wr(path, t2)
    print('  [OK] %-10s 已在 L%d…%d（run 末）后插入 %d 行' % (tag, j + 3, j + 2 + len(note), len(note)))

print('=== 第 123 轮补丁（一）：论文中英 ===')
assert rd(ZH).count('v2.9 判定（第 123 轮') == 0, 'ZH 已含该注？'
assert rd(EN).count('determination (Round 123') == 0, 'EN 已含该注？'
insert_note(ZH, lambda s: s.startswith('> **【v2.9 补充（第 75 轮'),
            lambda s: s.startswith('#### 8.6.4'), ZH_NOTE, 'ZH-123')
insert_note(EN, lambda s: s.startswith('> **【v2.9 supplement (Round 75:'),
            lambda s: s.startswith('#### 8.6.4 Why the two ends'), EN_NOTE, 'EN-123')
# 复核
zt = rd(ZH); et = rd(EN)
print('  ZH 注计数 =', zt.count('v2.9 判定（第 123 轮'), '| EN 注计数 =', et.count('determination (Round 123'))
print('  ZH 占位符 =', zt.count('«ND123C»'), '| EN 占位符 =', et.count('«ND123E»'))
print('done')
