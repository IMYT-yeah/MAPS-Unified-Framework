# -*- coding: utf-8 -*-
"""第 120 轮补丁（一）：论文中英 —— 
① 第 72 块内插入「第 120 轮细化（C-83）」行；
② 第 72 块之后插入第 120 轮块；
③ §8.6 符号约定插入「α 义项」补注（C-84）。
每项自带存在性守卫（可安全重跑）。"""
import io, os

BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
OUT = os.path.join(BASE, 'outputs')
ZH = os.path.join(OUT, '论文初稿_正反物质对风暴统一框架_v2.9.md')
EN = os.path.join(OUT, 'Paper_MatterAntimatterPairStorm_v2.9_EN.md')

def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, t): io.open(p, 'w', encoding='utf-8').write(t)

# ---------------- 内容 ----------------
ZH_REFINE = '> ⚠️ **【第 120 轮细化（C-83）】** 本行分支 (ii) 的「已被排除」**对 (c) 47.1 μm 档不成立**（与细表「灵敏度前沿」一致的是：以 KK radion 值 `α_Y = 1/3` 判定，该档**存活**）—— 详见下条注。'

EN_REFINE = '> ⚠️ **【Round-120 refinement (C-83)】** The "already excluded" verdict in branch (ii) **does not hold for tier (c), 47.1 μm** (consistent with the detail table\'s "sensitivity frontier": at the KK radion value `α_Y = 1/3` that tier **survives**) — see the note below.'

ZH_BLOCK = [
    '> **【v2.9 补充（第 120 轮：Φ 的第五力窗口 —— 2025–26 约束带更新 ＋ 一处判决细化）】** 核验 `_i17_120.py`（**I17-1…I17-24，24 项 0 失败**）。题源 = 第 118 轮外部清单的 **C1**（「把 Φ 放进 2025–26 约束表」）；第 62 / 70 / 72 轮的第五力线在本条**收束**。',
    '> · **2025–26 新约束的落点（全部在别处）**：① **光学悬浮微球**（*Sci. Rep.* **16**, 5180 (2026)；arXiv:2412.13167）把 **λ = 1–100 μm** 段的 Yukawa 界推到 **α ≲ 10⁷（@5 μm）／10⁶（@≳10 μm）**（同技术改进 ×50–100）——**离 α ~ 1 级仍差 6 个数量级**；② **HUST 新结果**（经 Murata 等 2026 综述 arXiv:2605.18212）在**厘米**尺度给 **α < 10⁻⁴**；③ **Juno**（JHEP **01** (2025) 098）排除 **m ~ 10⁻¹⁴ eV**（力程 λ ≈ 2×10⁷ m）新区域；④ 悬浮传感对 **chameleon** 的 ~2 个数量级进展（2024）为**模型特异**，而 **MORRIS（目标 α ≲ 10⁻⁴→10⁻⁵ @ λ ~ 1–4 mm）／AION-10／VLBAI／Th-229 核钟均为【计划】**。⟹ ⭐ **40–200 μm 带（Φ 的相关带）自 2020 年后无新数据**：仍由 Lee et al. 2020（α=1 边界 **38.6 μm**）与 Tan et al. 2020（**48 μm**）把守，且两者在 **39–48 μm 段互不一致**。',
    '> · ⭐ **把第 72 轮的「α ~ O(1)」换成 KK 的 radion 值 `α_Y = 1/3`**（平坦额外维 KK ⇔ Brans–Dicke ω = 0 ⟹ α_Y = 1/(2ω+3)；等价 β = 1/√6、α_Y = 2β²）后**逐档重判**（四个质量档见第 70 轮块）：**(a) 0.81 l_P、(d) 1.000 l_P** ⟹ 不排除、不可观测（不变）；**(b) 193.8 μm** ⟹ **排除**（两锚点幂律族：α_max(194 μm) ≈ 0.02–0.08，为 1/3 的 **4–20 倍**）；**(c) 47.1 μm** ⟹ ⭐ **存活**（α_max(47.1 μm) ≈ 0.66–1.06，为 1/3 的 **2.0–3.2 倍**）——**骑在前沿内侧**。',
    '> · ⚠️ **【对第 72 轮的细化（C-83）】** 第 72 轮**分支表**把 (c) 并入「已被排除」，与同轮**细表**的「灵敏度前沿」不一致；以 `α_Y = 1/3` 判定：**(c) 不在排除侧**。⟹ **Φ 的第五力窗口 = `λ ≲ 65–90 μm`（@α_Y = 1/3；单一短程半线）**，大 λ 侧无窗口（Cassini 族把 α 压到 ~10⁻⁵ 量级；cm–mm 段 α < 10⁻⁴–10⁻³）。窗口内框架仅 **(c) 一档**，且它是**半拟合**（「m_Φ = 截断能标」是假设）。',
    '> · ⭐ **可操作的实验判据（本轮的对外产出）**：把 **40–60 μm 段**的 α 界**再改进 ×3**（压到 ~0.3 级）即可**判定 (c) 的存亡**，从而终结 Φ 的第五力线 —— 落在**下一代桌面实验**的量程内，不依赖任何新装置。⚠️ 对 α_Y = 1（dilaton 读法）：47.1 μm 恰落入 **39–48 μm 争议带**（不能判定）、193.8 μm 仍排除 ⟹ 结论按 **[1/3, 1]** 区间表述。',
    '> · ⚠️ **符号（C-84）**：本注 `α_Y` 一律指 **Yukawa 强度**（`V = −(GM/r)(1+α_Y·e^{−r/λ})` 的 α），与 §4.6 的**过载参数** `α`、§4.5b 的 **PPN** `α₁α₂α₃`、§5.7 的**精细结构常数**无关；`α` 的义项清点见 §8.6 约定。',
    '> · **诚实边界**：① `α_Y = 1/3` 是**标准 KK 的知识**（框架未推导；扭曲额外维变体可达 2/3）；② α_max 的逐点是**两锚点幂律插值**（4 个端点组合给出稳健区间，**一手曲线未取到** —— Murata 2026 的数据在图中）；③ 「m_Φ = 截断能标」沿用第 70 轮的**假设**（半拟合）；④ **无新自由参数、无新现象**；⑤ 第 118 轮「大幅收紧」的表述须拆「实测／计划」，对 Φ 相关带**命中 = 0**。',
]

EN_BLOCK = [
    '> **【v2.9 supplement (round 120: the fifth-force window of Φ — 2025–26 constraint-band update + one verdict refinement)】** Verification `_i17_120.py` (**I17-1…I17-24, 24 checks passed**). Source: item **C1** of the round-118 external-input list ("put Φ into the 2025–26 constraint tables"); the fifth-force line of rounds 62 / 70 / 72 **closes out** here.',
    '> · **Where the 2025–26 constraints actually land (all elsewhere)**: ① **optically levitated microspheres** (*Sci. Rep.* **16**, 5180 (2026); arXiv:2412.13167) push the Yukawa bound over **λ = 1–100 μm** to **α ≲ 10⁷ (@5 μm) / 10⁶ (@≳10 μm)** (×50–100 improvement) — still **6 orders of magnitude from α ~ 1**; ② the **new HUST result** (via the 2026 review arXiv:2605.18212) gives **α < 10⁻⁴** at **centimetre** scales; ③ **Juno** (JHEP **01** (2025) 098) excludes a new region at **m ~ 10⁻¹⁴ eV** (range λ ≈ 2×10⁷ m); ④ the ~2-orders **chameleon** improvement (levitated sensor, 2024) is **model-specific**, and **MORRIS (target α ≲ 10⁻⁴→10⁻⁵ @ λ ~ 1–4 mm) / AION-10 / VLBAI / the Th-229 clock are all *projections***. ⟹ ⭐ **the 40–200 μm band (the relevant band for Φ) has seen no new data since 2020**: it is still held by Lee et al. 2020 (α=1 boundary at **38.6 μm**) and Tan et al. 2020 (**48 μm**), which are **mutually inconsistent over 39–48 μm**.',
    '> · ⭐ **Replacing round 72\'s "α ~ O(1)" by the KK radion value `α_Y = 1/3`** (flat-dimension KK ⇔ Brans–Dicke ω = 0 ⟹ α_Y = 1/(2ω+3); equivalently β = 1/√6, α_Y = 2β²) **re-decides all four mass tiers** (see the round-70 block): **(a) 0.81 l_P, (d) 1.000 l_P** ⟹ not excluded, unobservable (unchanged); **(b) 193.8 μm** ⟹ **excluded** (two-anchor power-law family: α_max(194 μm) ≈ 0.02–0.08, i.e. **4–20×** below 1/3); **(c) 47.1 μm** ⟹ ⭐ **survives** (α_max(47.1 μm) ≈ 0.66–1.06, i.e. **2.0–3.2×** above 1/3) — **riding just inside the frontier**.',
    '> · ⚠️ **【Refinement of round 72 (C-83)】** The round-72 **branch table** had lumped (c) into "already excluded", contradicting its own **detail table** ("sensitivity frontier"); judged with `α_Y = 1/3`: **(c) is NOT on the excluded side**. ⟹ **The fifth-force window of Φ = `λ ≲ 65–90 μm` (at α_Y = 1/3; a single short-range half-line)**; there is no window at large λ (Cassini-class bounds push α to the ~10⁻⁵ level; cm–mm α < 10⁻⁴–10⁻³). Inside the window the framework has only **tier (c)** — and it is a **semi-fit** ("m_Φ = cutoff scale" is an assumption).',
    '> · ⭐ **Actionable experimental criterion (this round\'s outward deliverable)**: improve the α bound over the **40–60 μm band by a further ×3** (down to the ~0.3 level) and **tier (c) is decided** (alive or dead), terminating the fifth-force line of Φ — within reach of **next-generation tabletop experiments**, with no new apparatus. ⚠️ For α_Y = 1 (dilaton reading): 47.1 μm falls exactly in the **39–48 μm contested band** (undecidable) and 193.8 μm stays excluded ⟹ quote the conclusion over the interval **[1/3, 1]**.',
    '> · ⚠️ **Symbols (C-84)**: `α_Y` here always denotes the **Yukawa strength** (the α in `V = −(GM/r)(1+α_Y·e^{−r/λ})`), unrelated to the §4.6 **overload parameter** `α`, the §4.5b **PPN** `α₁α₂α₃`, or the §5.7 **fine-structure constant**; see the §8.6 convention for the sense inventory of `α`.',
    '> · **Honesty boundaries**: ① `α_Y = 1/3` is **standard-KK knowledge** (not derived here; warped variants can reach 2/3); ② the α_max points come from a **two-anchor power-law interpolation** (four endpoint combinations give a robust interval; the **primary curve was not obtained** — Murata 2026\'s data live in figures); ③ "m_Φ = cutoff scale" is the round-70 **assumption** (semi-fit); ④ **no new free parameters, no new phenomena**; ⑤ the round-118 phrase "sharp tightening" must be split into *measured* vs *projected* — **zero hits** on the relevant band of Φ.',
]

ZH_ALPHA = '> ⚠️ **第 120 轮补注（C-84）**：`α` 同样是**多义字母** —— ① **过载参数**（§4.6：`r_h = α·2GM/c²`，α=1 为 GR 极限）｜② **PPN** `α₁/α₂/α₃`（§4.5b）｜③ **精细结构常数**（`α_s/α_EM`，§5.7）｜④ **图热流插值系数**（§4.9 注内 α = 0.3）｜⑤ **Yukawa 强度**（第五力段，**写作 `α_Y`**）；另有局部用法（火墙厚度 α ∈ {0, 1/2}、历史式 `Ω_tot = 4α²β²`）。**规范：引用 `α` 一律带语境前缀**（「过载 α」／「PPN α₁」／「精细结构 α」／「Yukawa `α_Y`」）。'

EN_ALPHA = '> ⚠️ **Round-120 addendum (C-84)**: `α` is likewise a **many-sense letter** — ① **overload parameter** (§4.6: `r_h = α·2GM/c²`, α=1 = GR limit) | ② **PPN** `α₁/α₂/α₃` (§4.5b) | ③ **fine-structure constant** (`α_s/α_EM`, §5.7) | ④ **graph-heat-flow interpolation coefficient** (α = 0.3, §4.9 note) | ⑤ **Yukawa strength** (fifth-force passage, **written `α_Y`**); local uses aside (firewall thickness α ∈ {0, 1/2}; the historical `Ω_tot = 4α²β²`). **Rule: always attach a context prefix when citing `α`** ("overload α" / "PPN α₁" / "fine-structure α" / "Yukawa `α_Y`").'

# ---------------- 操作 ----------------
def ins_after(path, marker, block, tag, skip_if=None):
    t = rd(path)
    if skip_if and skip_if in t:
        print('  [SKIP] %-26s（已存在）' % tag); return
    L = t.split('\n')
    idx = [k for k, s in enumerate(L) if marker in s]
    if len(idx) != 1:
        print('  [XX] %-26s 命中 %d 次 —— 拒绝' % (tag, len(idx))); return
    k = idx[0]
    L[k + 1:k + 1] = block
    wr(path, '\n'.join(L))
    print('  [OK] %-26s 已插入 %d 行（@L%d）' % (tag, len(block), k + 2))

def ins_block_after_quote_run(path, start_marker, block, tag, tail_must, skip_if=None):
    t = rd(path)
    if skip_if and skip_if in t:
        print('  [SKIP] %-26s（已存在）' % tag); return
    L = t.split('\n')
    idx = [k for k, s in enumerate(L) if start_marker in s]
    if len(idx) != 1:
        print('  [XX] %-26s 起点命中 %d 次 —— 拒绝' % (tag, len(idx))); return
    j = idx[0]
    while j + 1 < len(L) and L[j + 1].startswith('>'):
        j += 1
    if tail_must not in L[j]:
        print('  [XX] %-26s 末行不匹配：%s' % (tag, L[j][:60])); return
    L[j + 1:j + 1] = block
    wr(path, '\n'.join(L))
    print('  [OK] %-26s 已插入 %d 行（@L%d）' % (tag, len(block), j + 2))

print('=== 第 120 轮论文补丁 ===')
# ① ZH 细化行（72 块内）
ins_after(ZH, '**三选一全是死路**', [ZH_REFINE], 'ZH-72块细化',
          skip_if='第 120 轮细化（C-83）')
# ② ZH 120 块（72 块之后）
ins_block_after_quote_run(ZH, '【v2.9 补充（第 72 轮：Φ 的耦合强度', ZH_BLOCK, 'ZH-120块',
                          tail_must='诚实边界六条', skip_if='（第 120 轮：Φ 的第五力窗口')
# ③ ZH §8.6 α 约定
ins_after(ZH, '**规范：引用 `λ` 一律带语境前缀**', [ZH_ALPHA], 'ZH-§8.6α',
          skip_if='第 120 轮补注（C-84）')
# ④ EN 细化行
ins_after(EN, '**Three-branch verdict**', [EN_REFINE], 'EN-72块细化',
          skip_if='Round-120 refinement (C-83)')
# ⑤ EN 120 块
ins_block_after_quote_run(EN, 'supplement (Round 72', EN_BLOCK, 'EN-120块',
                          tail_must='Six honesty boundaries', skip_if='supplement (round 120')
# ⑥ EN §8.6 α 约定
ins_after(EN, 'always attach a context prefix when citing `λ`', [EN_ALPHA], 'EN-§8.6α',
          skip_if='Round-120 addendum (C-84)')

print('')
print('=== 结构快查 ===')
z = rd(ZH).split('\n')
i = [k for k, s in enumerate(z) if 'v2.9 补充（第 120 轮' in s]
if i:
    k = i[0]; j = k
    while j < len(z) and z[j].startswith('>'): j += 1
    print('ZH 120 块：%d..%d（%d 行）；块内非 `> ` 行数 = %d' % (k + 1, j, j - k, sum(1 for s in z[k:j] if not s.startswith('>'))))
print('ZH 细化行位置：', [k + 1 for k, s in enumerate(z) if '第 120 轮细化（C-83）' in s])
e = rd(EN).split('\n')
i2 = [k for k, s in enumerate(e) if 'supplement (round 120' in s]
if i2:
    k = i2[0]; j = k
    while j < len(e) and e[j].startswith('>'): j += 1
    print('EN 120 块：%d..%d（%d 行）；块内非 `> ` 行数 = %d' % (k + 1, j, j - k, sum(1 for s in e[k:j] if not s.startswith('>'))))
print('EN 细化行位置：', [k + 1 for k, s in enumerate(e) if 'Round-120 refinement (C-83)' in s])
