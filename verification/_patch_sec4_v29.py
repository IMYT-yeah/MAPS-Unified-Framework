# -*- coding: utf-8 -*-
"""
§4.2 两处修正（中英同步，就地改 v2.9）
依据：outputs/_sec4_ergodicity_audit.py（EA-0…EA-5，失败项：无）
  ① 正文第 2 条：B–K 定理以度量传递性为前提 ⟹ 遍历性是**假设**，不是定理结论
  ② 新增「两个时标的分离」：速度空间弛豫 ~4 t_P  vs  衬底构型混合 47 μm/t_H（差 ~10^30）
     + 把「配对湮灭-再生 ≡ 弹性散射」从断言升级为机制（相邻对换 = 全同粒子交换身份）
锚点必须恰好命中一次，否则报错退出。
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT, FAIL = [], []


def rep(path, tag, old, new):
    s = open(path, encoding="utf-8").read()
    n = s.count(old)
    if n != 1:
        FAIL.append("%s｜%s：锚点命中 %d 次" % (os.path.basename(path), tag, n))
        print("  [XX] %-40s 命中 %d 次" % (tag, n))
        return
    open(path, "w", encoding="utf-8").write(s.replace(old, new, 1))
    OUT.append("%s｜%s" % (os.path.basename(path), tag))
    print("  [OK] %-40s 已改" % tag)


ZH_NOTE = """**【v2.9 补充：两个时标的分离 —— 局域热平衡与全局非平衡共存】**【推导 + 数值】：置换模型（§8.6，第 21 轮）给出两个相差约 10³⁰ 倍的时标：
- **① 速度空间弛豫（快）**：满占位衬底的数密度 n = 1/l_P³、截面 σ = l_P²、速率 c ⟹ 碰撞率 nσv = **1/t_P = 1.85×10⁴³ s⁻¹**、平均自由程 = **l_P**，局域平衡在 ~4 次对换内达成（τ_relax ≈ 4 t_P ≈ 2.2×10⁻⁴³ s、弛豫长度 ≈ 4 l_P ≈ 6.5×10⁻³⁵ m）；
- **② 衬底构型混合（慢）**：R_mix = l_P·√(t/t_P)，一个哈勃时仅 ≈ 4.7×10⁻⁵ m（**47 μm**，≈ 3.4×10⁻³¹ R_c）。

⟹ **本命题链所需的是①（速度空间的局域平衡），与②的「全局远未热化」并不矛盾**——这正是动理论的标准情形（局域平衡 + 全局梯度），也与上文「引力系统无全局热平衡」的限制一致。
⟹ 附带：**相邻对换 = 全同粒子交换身份**，与等质量弹性散射在多体层面不可区分 ⟹ 本小节开头那句「配对的湮灭-再生在完美平衡（50:50）下**与弹性散射动力学等价**」由此**获得机制**（此前为断言）。

"""

EN_NOTE = """**【v2.9 supplement: separation of two timescales — local equilibrium and global non-equilibrium coexist】**【Derivation + Numerical】: the permutation model (§8.6, round 21) yields two timescales differing by about 10³⁰:
- **① velocity-space relaxation (fast)**: with a fully occupied substrate, n = 1/l_P³, σ = l_P², v = c ⟹ collision rate nσv = **1/t_P = 1.85×10⁴³ s⁻¹**, mean free path = **l_P**; local equilibrium is reached within ~4 transpositions (τ_relax ≈ 4 t_P ≈ 2.2×10⁻⁴³ s, relaxation length ≈ 4 l_P ≈ 6.5×10⁻³⁵ m);
- **② substrate configurational mixing (slow)**: R_mix = l_P·√(t/t_P), only ≈ 4.7×10⁻⁵ m (**47 μm**, ≈ 3.4×10⁻³¹ R_c) per Hubble time.

⟹ **What this proposition chain needs is ① (local equilibrium in velocity space); it does not conflict with ② ("globally far from thermalized").** This is the standard situation in kinetic theory (local equilibrium + global gradients), and it is consistent with the "no global thermal equilibrium for gravitational systems" limitation above.
⟹ Incidentally: **an adjacent transposition = exchange of identities of identical particles**, indistinguishable from equal-mass elastic scattering at the many-body level ⟹ the claim at the head of this subsection that "paired annihilation–regeneration at perfect 50:50 is **dynamically equivalent to elastic scattering**" thereby **acquires a mechanism** (it was an assertion before).

"""

jobs = [
    (os.path.join(HERE, "论文初稿_正反物质对风暴统一框架_v2.9.md"), [
        ("① 遍历性标注为假设",
         "2. 遍历性（Birkhoff–Khinchin 定理）：时间平均 = 系综平均；",
         "2. 遍历性（Birkhoff–Khinchin 定理）：时间平均 = 系综平均 —— **B–K 定理以度量传递性（遍历性）为前提，故此处是动力学假设，不是定理结论**；数值验证见下文 v2.6 补充（实测 0.00%）；"),
        ("② 新增两个时标的分离",
         "**【v2.6 补充：玻尔兹曼涌现的数值证明 + 循环风险回应（响应审稿 M1）】**：",
         ZH_NOTE + "**【v2.6 补充：玻尔兹曼涌现的数值证明 + 循环风险回应（响应审稿 M1）】**："),
    ]),
    (os.path.join(HERE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md"), [
        ("① ergodicity flagged as assumption",
         "2. Ergodicity (Birkhoff–Khinchin theorem): time average = ensemble average;",
         "2. Ergodicity (Birkhoff–Khinchin theorem): time average = ensemble average — **the B–K theorem presupposes metric transitivity, so this is a dynamical assumption, not a theorem output**; numerically verified in the v2.6 supplement below (measured 0.00%);"),
        ("② two-timescale separation added",
         "**【v2.6 supplement: numerical proof of Boltzmann emergence + response to the circularity objection (referee M1)】**:",
         EN_NOTE + "**【v2.6 supplement: numerical proof of Boltzmann emergence + response to the circularity objection (referee M1)】**:"),
    ]),
]

# 先备份（git 尚未首次提交，这是可回滚点）
HIST = os.path.join(ROOT, "MAPS-Unified-Framework", "paper", "history")
os.makedirs(HIST, exist_ok=True)
for p, _ in jobs:
    b = os.path.join(HIST, os.path.basename(p).replace(".md", "_备份_2026-09-18sec4前.md"))
    open(b, "w", encoding="utf-8").write(open(p, encoding="utf-8").read())
    print("  备份 →", os.path.basename(b))

for p, edits in jobs:
    print("\n" + "=" * 70 + "\n" + os.path.basename(p) + "\n" + "=" * 70)
    for tag, old, new in edits:
        rep(p, tag, old, new)

print("\n完成 %d 项" % len(OUT))
for o in OUT:
    print("  ·", o)
print("失败：%s" % ("；".join(FAIL) if FAIL else "无"))
