# -*- coding: utf-8 -*-
"""第 119 轮补丁（一）：论文中英 —— 指数度规文献锚定升级块"""
import io, os
BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
ZH = os.path.join(BASE, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md')
EN = os.path.join(BASE, 'outputs', 'Paper_MatterAntimatterPairStorm_v2.9_EN.md')
BAD = []

def sub_once(path, old, new, tag):
    t = io.open(path, encoding='utf-8').read()
    n = t.count(old)
    if n != 1:
        print('  [XX] %-16s 命中 %d 次 —— 拒绝' % (tag, n)); BAD.append(tag); return
    io.open(path, 'w', encoding='utf-8').write(t.replace(old, new, 1))
    print('  [OK] %-16s 已改' % tag)

def insert_after(path, pred, new_lines, tag):
    L = io.open(path, encoding='utf-8').read().split('\n')
    idx = [k for k, s in enumerate(L) if pred(s)]
    if len(idx) != 1:
        print('  [XX] %-16s 定位 %d 处 —— 拒绝' % (tag, len(idx))); BAD.append(tag); return
    L[idx[0] + 1:idx[0] + 1] = new_lines
    io.open(path, 'w', encoding='utf-8').write('\n'.join(L))
    print('  [OK] %-16s 已插入 %d 行（行 %d 后）' % (tag, len(new_lines), idx[0] + 1))

ZH_NEW = ("""**【v2.9 口径注（第 119 轮：指数度规文献锚定升级 ＋ 一处外部数字的复算裁定）】** ① **2025–26 该度规仍是活文献**：arXiv:2511.13471（2025-11：光子球/ISCO/Regge–Wheeler/阴影；定位＝无事件视界/各向异性流体源/可穿越虫洞）、EPJC 85, 531（2025-05：暗物质完美流体源变体）、EPJC（2026：磁偶极场）——与 v2.4 块 (iii)(iv)(v) 的定位一致。② **复算裁定（对 arXiv:2511.13471）**：该文的一般形（其 §2.6：`g_θθ = r²`）与本文 **v1.14/v1.21 排除的「标准坐标变体」**完全对应——其 l=0 强场量（光子球 `r_* = M`、阴影 `b_* = Me`、ISCO `2M`）与 v1.21 表「标准坐标」行**逐位一致**（`1.00 GM/c²`／`e`）；**它不是本文的各向同性指数度规**（后者光子球 `2GM/c²`、阴影 `2e·GM/c²`——v1.21 已与 EHT 相容；本轮回算复核：对 GR `2e/(3√3) = +4.63%`、对 EHT 5.2 为 `+4.55%`）。⟹ **该文不构成本框架度规的新约束**。③ ⚠️ 该文另有「被太阳系检验排除」主张（光偏折只一半、近日点进动只三分之一）：**本轮复算不支持**——两种 l=0 变体的光偏折积分均 → `4M/b`（= GR 的 1PN；γ=β=1，见 v2.4 块 (i)；数值见 `_lit119_verify.py` NU-1：`α·b/(4M) → 1.000`，不是 ½）；与 §4.5b 的 RK4 数值同向（b=10M：本轮积分 +3.4%、原 RK4 记 +5%——1.6pp 差登记待核）。**引用该文数字前须独立复核。** ④ 顺带回算（此前未算）：本文度规 **ISCO `r = (3+√5) GM/c² ≈ 5.236 GM/c²`**。⑤ EMRI 侧文献锚定（2026 自协力/1PA/标量荷波形三篇）见材料包 Q1 注。""")

EN_NEW = ("""**【v2.9 caliber note (round 119: literature-anchoring upgrade for the exponential metric ＋ adjudication of one external set of numbers)】** ① **The metric remains an active topic in 2025-26**: arXiv:2511.13471 (2025-11: photon sphere/ISCO/Regge-Wheeler/shadow; positioning: no event horizon / anisotropic-fluid source / traversable wormhole), EPJC 85, 531 (2025-05: dark-matter perfect-fluid sourced variant), EPJC (2026: magnetic dipole field) - consistent with items (iii)(iv)(v) of the v2.4 block. ② **Adjudication (arXiv:2511.13471)**: its general form (its §2.6: `g_thth = r²`) corresponds exactly to the **"standard-coordinate variant" excluded in v1.14/v1.21** - its l=0 strong-field numbers (photon sphere `r_* = M`, shadow `b_* = Me`, ISCO `2M`) match the v1.21 table's "standard-coordinate" row **digit for digit** (`1.00 GM/c²` / `e`); it is **not** this paper's isotropic exponential metric (photon sphere `2GM/c²`, shadow `2e·GM/c²` - EHT-compatible per v1.21; this round's recomputation: `2e/(3√3) = +4.63%` vs GR, `+4.55%` vs EHT 5.2). ⟹ **the paper imposes no new constraint on the framework metric**. ③ ⚠️ That paper also claims the metric is "ruled out by solar system tests" (only half the light bending, one-third the perihelion precession): **this round's recomputation does not support it** - for both l=0 variants the deflection integral trends to `4M/b` (= GR's 1PN; γ=β=1, see v2.4 item (i); numerics in `_lit119_verify.py` NU-1: `alpha*b/(4M) -> 1.000`, not 1/2); it agrees in direction with the §4.5b RK4 numbers (b=10M: this round's integral +3.4%, the original RK4 +5% - a 1.6pp gap flagged for later check). **Numbers from that paper must not be cited without independent verification.** ④ Side recomputation (previously not done): this metric has **ISCO `r = (3+sqrt5) GM/c² ≈ 5.236 GM/c²`**. ⑤ EMRI-side literature anchoring (three 2026 self-force / 1PA / scalar-charge waveform papers) is in the material-package Q1 note.""")

print('=== ZH ===')
insert_after(ZH, lambda s: s.startswith('**【v2.4 补充】与 exponential metric 文献的对照'), ['', ZH_NEW], 'ZH-119块')
print('=== EN ===')
insert_after(EN, lambda s: s.startswith('**【v2.4 supplement: comparison with the exponential-metric literature'), ['', EN_NEW], 'EN-119块')

print('')
print('BAD =', BAD)
