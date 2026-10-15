# -*- coding: utf-8 -*-
"""第 121 轮 论文补丁（中英同步）：在第 120 轮块之后插入第 121 轮块（实验线 x3）。"""
import io, os

BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
OUT = os.path.join(BASE, 'outputs')
ZH = os.path.join(OUT, '论文初稿_正反物质对风暴统一框架_v2.9.md')
EN = os.path.join(OUT, 'Paper_MatterAntimatterPairStorm_v2.9_EN.md')

ZH_BLOCK = [
"> **【v2.9 补充（第 121 轮：实验线 ×3 —— 判据精确化与候选装置核对）】** 核验 `_exp121.py`（**E121-1…E121-16，41 项断言 0 失败**）。题源 = 第 120 轮 §八的「实验线：40–60 μm ×3」（升级为对外材料包）。",
"> · **判据精确化（C-85）**：以两条锚线（Lee 2020：`α = 1` @ **38.6 μm**；Tan 2020：`α = 1` @ **48 μm**）的四组幂律族重算，λ = 47.1 μm 处**判死 (c) 所需改进 = ×1.97（Lee 链）– ×3.17（Tan 链）**；**「×3」= 到达判定边缘**（新界 0.218–0.352 恰好跨过 `α_Y = 1/3`），**四链干净排除需 ×3.2**（把 `α = 1/3` 边界从 65–87 μm 推到 ≤ 47 μm）、**2× 裕度需 ×6.4**。",
"> · **现状核对（2026-10-04 公开检索）**：40–60 μm 带**自 2020 年后无新实验**（INSPIRE 题名扫描两条 ＋ 第 120 轮扫描共三条一致；仍由 Lee/Tan 2020 把守）；2020–22 的 HUST 系统学三篇（残余气体阻尼／非等温挤压膜阻尼／振动–静电耦合）是该带的工作前沿。",
"> · ⭐ **已发表的下一代设计（候选 ①）**：**Du et al. 2022（CQG 39, 105008）「32 重对称吸引子」**——摘要明言最强界覆盖 **40–800 μm**、**投影总误差 2.0×10⁻¹⁷ N·m**、**λ ≈ 300 μm 处改进约一个量级**；⚠️ 三处口径：它是**设计计算**（非实验）、**「×10」的 λ = 300 μm（不能搬去 47 μm）**、**40–60 μm 段投影未公布**（= 缺的那个数，登记 **I-27**）。",
"> · **候选 ②（在建）**：Cal Poly Humboldt（Hoyle/Decca/Sako）「**50 μm 以下**」成分偶极扭秤（APS 2025 摘要 ＋ 2025/26 海报；环境监测阶段；无公开灵敏度数字）。",
"> · **候选 ③（长线，不计入）**：悬浮/量子力传感器（*Sci. Rep.* 2026 微球；HFUT Meissner 悬浮提案 arXiv:2602.13829 目标 0.1–10 μm、投影 10⁻¹⁹ N/√Hz）——与 40–60 μm 段**不重叠**。",
"> · **产出**：对外《第五力实验线材料包》（**未送出**）——单一请求：「报 40–60 μm 段的 α_max，目标 ≤ 0.3（稳健 ≤ 1/6）」。",
"> · **诚实边界**：① 精确化 = 算术（无新物理）；② 全部改进因子/投影是**引文**（未复算实验数据）；③ **「×N 改进」必带自变量 λ**（Du 的 ×10 在 300 μm）；④ Humboldt 信息源 = 会议材料；⑤ 聚合器新闻一条（2026-05「0.1 mm 最大测试」）源头未追到，**未采用**。",
]

EN_BLOCK = [
"> **【v2.9 supplement (round 121: the experimental line ×3 — criterion sharpened, candidate apparatus checked)】** Verification `_exp121.py` (**E121-1…E121-16, 41 assertions, 0 failures**). Source = round 120 §8, item 2 (\"experimental line: 40–60 μm ×3\"), now upgraded into an outward-facing materials packet.",
"> · **Sharpened criterion (C-85)**: with the two anchor lines (Lee 2020: `α = 1` @ **38.6 μm**; Tan 2020: `α = 1` @ **48 μm**) and the four power-law chains recomputed, the improvement needed at λ = 47.1 μm to kill tier (c) is **×1.97 (Lee chain) – ×3.17 (Tan chain)**; **\"×3\" = reaching the decision edge** (new bound 0.218–0.352 straddles `α_Y = 1/3`), **clean exclusion on all four chains needs ×3.2** (moving the `α = 1/3` boundary from 65–87 μm down to ≤ 47 μm) and **a 2× margin needs ×6.4**.",
"> · **Status check (public search, 2026-10-04)**: the 40–60 μm band has **no new experiment since 2020** (two INSPIRE title sweeps + the round-120 sweep agree; still guarded by Lee/Tan 2020); the HUST systematics trilogy of 2020–22 (residual-gas damping / non-isothermal squeeze-film damping / vibration–electrostatic coupling) defines the frontier of that band.",
"> · ⭐ **Published next-generation design (candidate ①)**: **Du et al. 2022 (CQG 39, 105008), \"32-fold symmetric attractor\"** — the abstract states strongest bounds over **40–800 μm**, projected total error **2.0×10⁻¹⁷ N·m**, and **~one order of magnitude improvement at λ ≈ 300 μm**; ⚠️ three calibers: it is a **design calculation** (not a result), the **×10 is at 300 μm** (do not transplant to 47 μm), and the **40–60 μm projection is unpublished** (the missing number; registered as **I-27**).",
"> · **Candidate ② (under construction)**: Cal Poly Humboldt (Hoyle/Decca/Sako) \"**below 50 μm**\" composition-dipole torsion pendulum (APS 2025 abstract + 2025/26 posters; environmental-monitoring stage; no public sensitivity number).",
"> · **Candidate ③ (long term, not counted)**: levitated/quantum force sensors (*Sci. Rep.* 2026 microsphere; HFUT Meissner-levitation proposal arXiv:2602.13829 targeting 0.1–10 μm with 10⁻¹⁹ N/√Hz) — **no overlap** with the 40–60 μm band.",
"> · **Deliverable**: the outward-facing \"fifth-force experimental-line materials packet\" (**prepared, not sent**) — single request: \"report the α_max over 40–60 μm; target ≤ 0.3 (robust ≤ 1/6)\".",
"> · **Honesty boundaries**: ① the sharpening is arithmetic (no new physics); ② all improvement factors/projections are **citations** (experimental data not recomputed); ③ **any \"×N improvement\" must carry its λ** (Du's ×10 is at 300 μm); ④ the Humboldt entries rest on conference materials; ⑤ one aggregator news item (2026-05, \"biggest test at 0.1 mm\") could not be traced and was **not used**.",
]

def insert_after_quote_run(path, marker, skip_if, block, tag):
    t = io.open(path, encoding='utf-8').read()
    if skip_if in t:
        print('  [SKIP] %s 已存在（%s）' % (tag, skip_if))
        return
    L = t.split('\n')
    idx = [i for i, s in enumerate(L) if marker in s]
    if len(idx) != 1:
        print('  [XX] %s 起始行命中 %d 次 —— 拒绝' % (tag, len(idx)))
        return
    i = idx[0]
    j = i
    while j < len(L) and L[j].startswith('>'):
        j += 1
    if j >= len(L) or L[j].strip() != '':
        print('  [XX] %s 块结束处不是空行（L%d=%r）—— 拒绝' % (tag, j + 1, L[j][:60]))
        return
    L[j:j] = block
    io.open(path, 'w', encoding='utf-8').write('\n'.join(L))
    print('  [OK] %s 插入 %d 行（原块 %d..%d，新块起于 L%d）' % (tag, len(block), i + 1, j, j + 1))

print('=== 第 121 轮论文补丁（中英同步）===')
insert_after_quote_run(ZH, '【v2.9 补充（第 120 轮', '【v2.9 补充（第 121 轮', ZH_BLOCK, 'ZH-121块')
insert_after_quote_run(EN, '【v2.9 supplement (round 120', 'supplement (round 121', EN_BLOCK, 'EN-121块')

# 结构自查
for path, tag in ((ZH, 'ZH'), (EN, 'EN')):
    L = io.open(path, encoding='utf-8').read().split('\n')
    m = [i for i, s in enumerate(L) if ('第 121 轮：实验线' in s) or ('round 121: the experimental line' in s)]
    if len(m) != 1:
        print('  [XX] %s 结构：新块起始行命中 %d' % (tag, len(m)))
        continue
    i = m[0]
    j = i
    while j < len(L) and L[j].startswith('>'):
        j += 1
    print('  [OK] %s 结构：新块 %d..%d（%d 行），块前一行以「>」开头=%s，块后为空行=%s'
          % (tag, i + 1, j, j - i, L[i - 1].startswith('>'), L[j].strip() == ''))
