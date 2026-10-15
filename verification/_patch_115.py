# -*- coding: utf-8 -*-
"""第 115 轮补丁（一）：论文中英（块复位 ＋ 第 115 轮注）／EMRI 材料包 §2.2c／D4 备忘录 C-79 注"""
import io
import os

BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
OUT = os.path.join(BASE, 'outputs')
ZH = os.path.join(OUT, '论文初稿_正反物质对风暴统一框架_v2.9.md')
EN = os.path.join(OUT, 'Paper_MatterAntimatterPairStorm_v2.9_EN.md')
MAT = os.path.join(OUT, 'EMRI材料包_给LISA组的S-E1-E4.md')
D4M = os.path.join(OUT, 'D4结项_EMRI进动系数的偏心率依赖与1_3极限.md')

rd = lambda p: io.open(p, encoding='utf-8').read()
wr = lambda p, t: io.open(p, 'w', encoding='utf-8').write(t)
BAD = []


def ok(tag, cond, msg):
    print(('  [OK] ' if cond else '  [XX] ') + '%-14s %s' % (tag, msg))
    if not cond:
        BAD.append(tag)


def sub_once(path, old, new, tag):
    t = rd(path)
    n = t.count(old)
    ok(tag, n == 1, '命中 %d 次（要求 1）' % n)
    if n == 1:
        wr(path, t.replace(old, new, 1))


def insert_after(path, anchor, block, tag, before=False):
    t = rd(path)
    n = t.count(anchor)
    ok(tag, n == 1, '锚点命中 %d 次（要求 1）' % n)
    if n == 1:
        if before:
            wr(path, t.replace(anchor, block + anchor, 1))
        else:
            wr(path, t.replace(anchor, anchor + block, 1))


# ============================================================
# 1) 论文中文：把第 113 轮块从第 112 轮块内部移出，再追加第 115 轮注
# ============================================================
BLOCK_ZH = """
> **【v2.9 口径注（第 115 轮：I-25 —— `κ_rel(e)` 的闭式，以及上两注那串数的口径更正）】** 上两注里的
> `κ_rel(e)` 数值（`0.3439 / 0.3646 / 0.3904 / 0.4116`）是 **`y ≈ 7.5×10⁻⁴` 处的原始值**，而不是它
> 表头写的「`y → 0` 外推值」（**C-79**：第 112 轮备忘录 §3.2 的那一列表列**抄错了** —— **同一脚本**
> 打印的 `y→0` 外推值是 `0.3426 / 0.3633 / 0.3891 / 0.4103`，与下面的闭式一致到 **10⁻⁵**）。
> 本轮把**一般偏心率**解析求出：两点积分 `Δφ = 2∫_{u_a}^{u_p} du/√G`（`G = hW`、`u = 1/r`）以
> `s = SB + AA·cos θ` 正则化（`SB = (s_p+s_a)/2`、`AA = (s_p−s_a)/2`）后作 `s` / `y` 双级数展开，
> 在**面积半径**半通径 `p` 与 `e = (R_a−R_p)/(R_a+R_p)` 下：
> **`Δφ/(2π) = 1 + 3y + S(e)·y² + O(y³)`**（`y = M/p`），其中
> **`S_GR(e) = 27/2 + (3/4)e²`**（7 个精确有理 `e ≤ 12/13` 全中）、**`S_FW(e) = 29/2 + e²`**
> ⟹ **`κ_rel(e) = (S_FW − S_GR)/3 = 1/3 + e²/12`**（**精确闭式**；`e→0` 回到第 113 轮的 `1/3`，
> `e→1` 的上确界 `5/12 = 0.4167`）。
> ⭐ **机制分解**（单侧替换，严格可加、无交叉项）：**全部偏心率依赖来自 `g_rr/g_θθ` 侧** ——
> `h` 侧 `ΔS = 5/4 + e²/4`、`f`（`g_tt`）侧 `ΔS ≡ −1/4`（**与 `e` 无关**）⟹ `1/3 + e²/12`。
> ✅ **双重标定**：GR 侧测地线积分与**精确椭圆积分闭式** `4K(k)/√(2M(u₃−u_a))` 相对差 ≤ 2×10⁻⁶
> （`y = 7.5×10⁻⁴`）；解析 `S(e)` 与数值 `y→0` 外推差 ≤ 2.2×10⁻⁶。
> ⚠️ **更正后的引用值**：`κ = 0.30` 的真值比 = **+11.1%（`e→0`）→ +36.8%（`e = 0.96`）**（原写 37.2%）；
> `e = 0.333 / 0.6 / 0.818 / 0.961` 处 `κ_rel = 0.3426 / 0.3633 / 0.3891 / 0.4103`。
> ⚠️ **两个极限方向不同**：`e = 0` 时 `κ_rel` 随 `y` 走 `1/3 + (5/3)y`（第 113 轮），
> 而 `y→0` 时随 `e` 走 `1/3 + e²/12`（本轮）—— 两者不冲突。
> 📌 **本轮无新物理、新增自由参数 0**（闭式只是把第 112 轮的数值换成有理式）；并顺带把第 113 轮的注
> **从第 112 轮注的内部移到其后面**（原锚点取成了行首前缀，把上一轮的块**劈成两半**）。
"""

L = rd(ZH).split('\n')
i112 = [i for i, s in enumerate(L) if '口径注（第 112 轮' in s]
i113 = [i for i, s in enumerate(L) if '口径注（第 113 轮' in s]
ok('ZH-1', len(i112) == 1 and len(i113) == 1, '两个锚点各命中 1 次')
i112, i113 = i112[0], i113[0]
ok('ZH-2', i113 == i112 + 1, '补丁前：第 113 轮注紧贴第 112 轮注首行（gap=%d）' % (i113 - i112))
ok('ZH-3', L[i112].rstrip().endswith('上面这条链的'), '补丁前：第 112 轮注首行在句中被截断')
cont = [i for i, s in enumerate(L) if s.startswith('> `δ = 0.30·x_p`')]
ok('ZH-4', len(cont) == 1, '第 112 轮块续行唯一（命中 %d）' % len(cont))
k = cont[0]
end = k
while end < len(L) and L[end].startswith('>'):
    end += 1
ok('ZH-5', all(L[j].startswith('>') for j in range(i113, end)),
   '第 113 轮块与第 112 轮块剩余部分都是连续引用块（%d 行）' % (end - i113))
new = L[:i112] + [L[i112]] + L[k:end] + L[i113:k] + BLOCK_ZH.split('\n')[1:] + L[end:]
wr(ZH, '\n'.join(new))
L2 = rd(ZH).split('\n')
i112b = next(i for i, s in enumerate(L2) if '口径注（第 112 轮' in s)
i113b = next(i for i, s in enumerate(L2) if '口径注（第 113 轮' in s)
i115b = next(i for i, s in enumerate(L2) if '口径注（第 115 轮' in s)
ok('ZH-6', L2[i112b + 1].startswith('> `δ = 0.30·x_p`'), '补丁后：第 112 轮注首行与其续行相邻')
ok('ZH-7', L2[i115b - 1].startswith('> 但 `Γ` 的 `s²`'),
   '补丁后：第 115 轮注紧接第 113 轮块末行（相距 %d 行）' % (i115b - i113b))
e115 = i115b
while e115 < len(L2) and L2[e115].startswith('>'):
    e115 += 1
blk = L2[i115b:e115]
ok('ZH-8', len(blk) == 21 and not any(s.strip() == '>' for s in blk),
   '第 115 轮块 %d 行全部为 `> ` 且无块内空行（期望 21）' % len(blk))

# ============================================================
# 2) 论文英文：同一复位 ＋ 同位置加注
# ============================================================
BLOCK_EN = """
> **【v2.9 caliber note (round 115: I-25 - closed form of `κ_rel(e)`, plus a caliber correction to the numbers in the two notes above)】** The `κ_rel(e)` numbers above (`0.3439 / 0.3646 / 0.3904 / 0.4116`) are the **raw values at `y ≈ 7.5×10⁻⁴`**, not the "`y → 0` extrapolation" their caption claims (**C-79**: that table column in the round-112 memo §3.2 was mis-transcribed - the `y→0` extrapolated values printed by the **same script** are `0.3426 / 0.3633 / 0.3891 / 0.4103`, agreeing with the closed form below to **10⁻⁵**).
> This round solves the **general eccentricity** analytically: the two-turning-point integral `Δφ = 2∫_{u_a}^{u_p} du/√G` (`G = hW`, `u = 1/r`), regularised by `s = SB + AA·cos θ` and expanded as a double series in `s` and `y`, gives, with the **areal** semi-latus rectum `p` and `e = (R_a−R_p)/(R_a+R_p)`:
> **`Δφ/(2π) = 1 + 3y + S(e)·y² + O(y³)`** (`y = M/p`), with **`S_GR(e) = 27/2 + (3/4)e²`** (exact on all seven rational `e ≤ 12/13` tested) and **`S_FW(e) = 29/2 + e²`**
> ⟹ **`κ_rel(e) = (S_FW − S_GR)/3 = 1/3 + e²/12`** (an **exact closed form**; `e→0` recovers round 113's `1/3`, and `e→1` gives the upper bound `5/12 = 0.4167`).
> ⭐ **Mechanism** (single-side replacement, strictly additive, no cross term): the **entire eccentricity dependence comes from the `g_rr/g_θθ` side** - the `h` side contributes `ΔS = 5/4 + e²/4`, the `f` (`g_tt`) side `ΔS ≡ −1/4` (**independent of `e`**) ⟹ `1/3 + e²/12`.
> ✅ **Two independent calibrations**: the GR geodesic quadrature agrees with the **exact elliptic-integral closed form** `4K(k)/√(2M(u₃−u_a))` to ≤ 2×10⁻⁶ (at `y = 7.5×10⁻⁴`); the analytic `S(e)` agrees with the numerical `y→0` extrapolation to ≤ 2.2×10⁻⁶.
> ⚠️ **Corrected reference values**: the true value of `κ` **divided by `0.30`** is **+11.1% (`e→0`) → +36.8% (`e = 0.96`)** (previously written 37.2%); at `e = 0.333 / 0.6 / 0.818 / 0.961`, `κ_rel = 0.3426 / 0.3633 / 0.3891 / 0.4103`.
> ⚠️ **The two limits act along different directions**: at `e = 0`, `κ_rel` runs as `1/3 + (5/3)y` in `y` (round 113), whereas at `y → 0` it runs as `1/3 + e²/12` in `e` (this round) - they do not conflict.
> 📌 **No new physics and zero new free parameters this round** (the closed form merely replaces round 112's numerics by a rational expression). The round-113 note has also been **moved out of the interior of the round-112 note** (its anchor was a line prefix, which had split the previous round's block in two).
"""
L = rd(EN).split('\n')
i112 = [i for i, s in enumerate(L) if 'caliber note (round 112' in s]
i113 = [i for i, s in enumerate(L) if 'caliber note (round 113' in s]
ok('EN-1', len(i112) == 1 and len(i113) == 1, '两个锚点各命中 1 次')
i112, i113 = i112[0], i113[0]
ok('EN-2', i113 == i112 + 1, '补丁前：113 紧贴 112（gap=%d）' % (i113 - i112))
cont = [i for i, s in enumerate(L) if s.startswith('> ⚠️ **Caliber**')]
ok('EN-3', len(cont) == 1, '第 112 轮块续行唯一（命中 %d）' % len(cont))
k = cont[0]
end = k
while end < len(L) and L[end].startswith('>'):
    end += 1
ok('EN-4', all(L[j].startswith('>') for j in range(i113, end)), '块连续性 ✓')
new = L[:i112] + [L[i112]] + L[k:end] + L[i113:k] + BLOCK_EN.split('\n')[1:] + L[end:]
wr(EN, '\n'.join(new))
L2 = rd(EN).split('\n')
i112b = next(i for i, s in enumerate(L2) if 'caliber note (round 112' in s)
i113b = next(i for i, s in enumerate(L2) if 'caliber note (round 113' in s)
i115b = next(i for i, s in enumerate(L2) if 'caliber note (round 115' in s)
ok('EN-5', L2[i112b + 1].startswith('> ⚠️ **Caliber**'), '补丁后：第 112 轮注首行与续行相邻')
ok('EN-6', L2[i115b - 1].startswith('> 📌 **N-42 re-check**'),
   '补丁后：115 紧接 113 块末行（相距 %d 行）' % (i115b - i113b))
e115 = i115b
while e115 < len(L2) and L2[e115].startswith('>'):
    e115 += 1
blk = L2[i115b:e115]
ok('EN-7', len(blk) == 9 and not any(s.strip() == '>' for s in blk),
   'EN 第 115 轮块 %d 行全为 `> ` 且无块内空行' % len(blk))

# ============================================================
# 3) EMRI 材料包：新增 §2.2c
# ============================================================
SEC = """### 2.2c 【第 115 轮追加】`κ_rel(e)` 的**闭式**（取代 §2.2b 的数值表）

⭐ ✂️ 上一小节的 `κ_rel(e)` 数值表已被**解析式取代**（同一台机器、同一面积半径口径）：

**Δφ/(2π) = 1 + 3y + S(e)·y² + O(y³)** ，`y = M/p_areal`，`e = (R_a−R_p)/(R_a+R_p)`
**S_GR(e) = 27/2 + (3/4)·e²**（史瓦西；面积半径口径下的**精确**值）
**S_FW(e) = 29/2 + e²**（本框架度规）
⟹ **`κ_rel(e) = (S_FW − S_GR)/3 = 1/3 + e²/12`**

| e | 0 | 0.333 | 0.6 | 0.818 | 0.961 | →1 |
|---|---|---|---|---|---|---|
| `κ_rel` | **0.33333** | 0.34259 | 0.36333 | 0.38912 | 0.41026 | 0.41667 |

⚠️ **两条必须与上表同时读的说明**：

① **§2.2b 表列的口径更正（C-79）**：那张表的数字（0.3439 / 0.3646 / 0.3904 / 0.4116）是
**`y ≈ 7.5×10⁻⁴` 处的原始值**，不是它表头写的「`y → 0` 外推值」；`y → 0` 的极限是**上表**的
`0.34259 / 0.36333 / 0.38912 / 0.41026`（与闭式一致到 `10⁻⁵`）。
② **两个极限方向不同**：`e = 0` 时 `κ_rel` 随 `y` 走 `1/3 + (5/3)y`；`y → 0` 时随 `e` 走 `1/3 + e²/12`。

✅ **对 S-E1–S-E4 的意义（改良的、但仍是「相对」超额）**：`κ = 0.30` 与真值的比 =
**+11.1%（`e → 0`）→ +36.8%（`e = 0.96`）**。**修正建议不变**：把 `κ` 换成 `1/3 + e²/12` 重算；
⚠️ 代码的 `n = 1/(κ x_p)` 按**绝对**相位用量，与 `κ_rel`（**相对**量）口径不同，**两侧须一并改**。

⚠️ **诚实边界（不变 ＋ 新增一条）**：闭式是 **`y²` 阶的相对**超额，`O(y³)` 项**未算**；
且 `σ_δ ↔ ΔlnL` 的自洽性（**C-7 / C-74**）**仍未清** ⟹ 本节的三个显著性数字**仍以 2 yr 的
`ΔlnL = 357` 为准**，4 yr 不给倍数。

"""
insert_after(MAT, '### 2.3 三个前提**全部在本框架之外**\n', SEC, 'MAT-A', before=True)

# ============================================================
# 4) D4 备忘录：C-79 更正注（非破坏性）
# ============================================================
NOTE = ("""> ⚠️ **【第 115 轮更正 C-79】** §3.2 的 `κ_rel` 表列是 **`y ≈ 7.5×10⁻⁴` 处的原始值**
> （同轮脚本 `_d4_kappa.py` 打印的 **`y → 0` 外推值**是 `0.3426 / 0.3633 / 0.3891 / 0.4103`），
> 而表头的说明写的是「下表为 `y → 0` 外推值」⟹ **表列抄错**（本轮的解析闭式与**外推值**一致到 `10⁻⁵`）。
> ✅ **本轮的定性结论不受影响**（`κ_rel` 随 `e` 单调升、近圆极限 = `1/3`）。
> 📌 **闭式（第 115 轮 I-25）**：`κ_rel(e) = 1/3 + e²/12`。
""")
insert_after(D4M, '> 「EMRI κ↔Γ 1/3 精确映射（10% 缺口）—— 需轨道平均 `s_p` 分布积分」）\n',
             NOTE, 'D4M-A')

print('')
print('BAD =', BAD)
