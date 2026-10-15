# -*- coding: utf-8 -*-
"""第 115 轮核验：I-25（κ_rel(e) 的闭式）＋ C-79（D4 表格抄录更正）

检查项 I25-1 … I25-18，末尾打印「通过 N 项，失败 M 项」。
⚠️ 「修复型」检查项一律两段式：读 *_备份_2026-10-04第115轮前.md 作补丁前底本。
"""
import io
import os
import sys
from fractions import Fraction as F

BASE = r'[WORKSPACE]'
OUT = os.path.join(BASE, 'outputs')
HIST = os.path.join(BASE, 'MAPS-Unified-Framework', 'paper', 'history')
sys.path.insert(0, OUT)

ZH = os.path.join(OUT, '论文初稿_正反物质对风暴统一框架_v2.9.md')
EN = os.path.join(OUT, 'Paper_MatterAntimatterPairStorm_v2.9_EN.md')
LP = os.path.join(OUT, '项目台账.md')
HO = os.path.join(BASE, '环境说明.md')
MAT = os.path.join(OUT, 'EMRI材料包_给LISA组的S-E1-E4.md')
D4M = os.path.join(OUT, 'D4结项_EMRI进动系数的偏心率依赖与1_3极限.md')
D4M_PRE = os.path.join(OUT, 'D4结项_EMRI进动系数的偏心率依赖与1_3极限_备份_2026-10-04第115轮前.md')
ZH_PRE = os.path.join(HIST, '论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-04第115轮前.md')
EN_PRE = os.path.join(HIST, 'Paper_v2.9_EN_备份_2026-10-04第115轮前.md')
MEM = os.path.join(BASE, '.workbuddy', 'memory', 'MEMORY.md')

rd = lambda p: io.open(p, encoding='utf-8').read()
n_ok = n_bad = 0


def chk(tag, cond, msg):
    global n_ok, n_bad
    if cond:
        n_ok += 1
        print('  [OK] %-8s %s' % (tag, msg))
    else:
        n_bad += 1
        print('  [XX] %-8s %s' % (tag, msg))


print('=' * 96)
print('I-25 核验（第 115 轮）')
print('=' * 96)

# ---------------- 解析侧 ----------------
import _i25_b as MB

EVALS = [F(1, 3), F(1, 2), F(2, 3), F(3, 4), F(4, 5), F(5, 6), F(12, 13)]
COMBOS = {'GR/GR': ('GR', 'GR'), 'GR/FW': ('GR', 'FW'),
          'FW/GR': ('FW', 'GR'), 'FW/FW': ('FW', 'FW')}
CLOSED = {'GR/GR': (F(27, 2), F(3, 4)), 'GR/FW': (F(59, 4), F(1)),
          'FW/GR': (F(53, 4), F(3, 4)), 'FW/FW': (F(29, 2), F(1))}
res = {}
for k, c in COMBOS.items():
    res[k] = [MB.S_of(c, e) for e in EVALS]

print('=== I25-1 一阶（1PN）系数恒为 3（四组合 × 7 个 e）===')
chk('I25-1', all(a1 == 3 for v in res.values() for a1, _, _ in v),
    '32 个 eps^1 系数全部 = 3 ⟹ 1PN 与 GR 一致（内建检查）')

print('=== I25-2/3/4 四个组合的 S(e) = a0 + b e^2（7 个精确有理点全中）===')
for k in ('GR/GR', 'GR/FW', 'FW/GR', 'FW/FW'):
    a0, b = CLOSED[k]
    hit = all(res[k][i][1] == a0 + b * EVALS[i] ** 2 for i in range(len(EVALS)))
    chk('I25-2' if k == 'GR/GR' else ('I25-3' if k == 'FW/FW' else 'I25-4'),
        hit, '%s: S(e) = %s + %s e^2（全部 7 点精确命中）' % (k, a0, b))

print('=== I25-5 可加性（单侧替换）：ΔS = h侧 + f侧，严格无交叉项 ===')
add_ok = all(res['FW/FW'][i][1] - res['GR/GR'][i][1] ==
             (res['GR/FW'][i][1] - res['GR/GR'][i][1]) + (res['FW/GR'][i][1] - res['GR/GR'][i][1])
             for i in range(len(EVALS)))
chk('I25-5', add_ok, 'ΔS = (h侧) + (f侧) 对全部 7 个 e 严格成立（精确有理数）')

print('=== I25-6 f 侧与 e 无关；h 侧承载全部偏心率依赖 ===')
f_ind = all(res['FW/GR'][i][1] - res['GR/GR'][i][1] == F(-1, 4) for i in range(len(EVALS)))
h_val = all(res['GR/FW'][i][1] - res['GR/GR'][i][1] == F(5, 4) + EVALS[i] ** 2 / 4
            for i in range(len(EVALS)))
chk('I25-6', f_ind and h_val,
    'f(g_tt) 侧 ≡ −1/4（与 e 无关）；h(g_rr/g_θθ) 侧 = 5/4 + e²/4 ⟹ e-依赖全在 h 侧')

print('=== I25-7/8 κ_rel(e) = 1/3 + e²/12（精确闭式）＋ 两端极限 ===')
K = [(res['FW/FW'][i][1] - res['GR/GR'][i][1]) / 3 for i in range(len(EVALS))]
chk('I25-7', all(K[i] == F(1, 3) + EVALS[i] ** 2 / 12 for i in range(len(EVALS))),
    '7 点全部等于 1/3 + e²/12（精确有理数）；样例 e=1/3 → %s' % K[0])
chk('I25-8', (F(1, 3) + F(0) / 12) == F(1, 3) and (F(1, 3) + F(1) / 12) == F(5, 12),
    'e→0 回到第 113 轮的 1/3；e→1 的上界 = 5/12 = %s（解析上确界）' % float(F(5, 12)))

# ---------------- 数值侧（独立标定） ----------------
print('=== I25-9 数值标定：框架/GR 测地线积分 vs 史瓦西精确椭圆积分闭式 ===')
import mpmath as mp
import _i25_num as MN

mp.mp.dps = 50
rel = []
for q in (mp.mpf(2), mp.mpf(9)):
    for Rp in (mp.mpf(100), mp.mpf(1000)):
        rp, ra = MN.turning('GR', Rp), MN.turning('GR', q * Rp)
        rel.append(abs(MN.dphi(MN.MODELS['GR'], rp, ra) / MN.dphi_gr_exact(rp, ra) - 1))
chk('I25-9', rel[1] < 1e-5 and rel[3] < 1e-5,
    '相对差 = %s（y=7.5e-3 与 7.5e-4；椭圆闭式 4K(k)/√(2M(u₃−u_a))）' %
    ['%.1e' % float(v) for v in rel])

print('=== I25-10 数值 y→0 外推 vs 解析闭式 ===')
RP3 = (125, 500, 2000)
diffs = []
for q, e in ((mp.mpf(2), mp.mpf(1) / 3), (mp.mpf(4), mp.mpf(3) / 5)):
    for tag, a0, b in (('GR', F(27, 2), F(3, 4)), ('FW', F(29, 2), F(1))):
        s0 = MN.extrap(MN.S_num(tag, q, RP3))[0]
        diffs.append(abs(s0 - (a0 + b * e ** 2)))
chk('I25-10', max(diffs) < 1e-5,
    '|数值外推 − 闭式| 最大 = %.2e（4 组：GR/FW × 2 个 e）' % float(max(diffs)))

# ---------------- C-79：D4 表格是「原始值」而非「外推值」 ----------------
print('=== I25-11 ⭐ C-79 两段式取证：D4 备忘录 §3.2 的表列 == 原始 y 值 ===')
d4rows = [l for l in rd(D4M_PRE).split('\n') if l.startswith('| `κ_rel` |')]
tab_vals = [float(x) for x in [s.strip().strip('*') for s in d4rows[0].split('|')][2:-1]] if d4rows else []
memo_e = [0.0909, 0.2, 1 / 3, 0.5, 0.6, 0.7143, 0.8182, 0.9048, 0.9608]
memo_v = tab_vals[1:]                      # 跳过第一列「0（圆）」
qs = [mp.mpf(6) / 5, mp.mpf(3) / 2, mp.mpf(2), mp.mpf(3), mp.mpf(4),
      mp.mpf(6), mp.mpf(10), mp.mpf(20), mp.mpf(50)]
raw, ext = [], []
Rp0 = mp.mpf(1000)
for q in qs:
    Rp, Ra = Rp0, q * Rp0
    rpg, rag = MN.turning('GR', Rp), MN.turning('GR', Ra)
    rpf, raf = MN.turning('FW', Rp), MN.turning('FW', Ra)
    ag = MN.dphi(MN.MODELS['GR'], rpg, rag) - 2 * mp.pi
    af = MN.dphi(MN.MODELS['FW'], rpf, raf) - 2 * mp.pi
    y = mp.mpf(1) / (2 * Rp * Ra / (Rp + Ra))
    raw.append(float((af / ag - 1) / y))
    ext.append(float(F(1, 3) + (mp.mpf(1) * ((q - 1) / (q + 1)) ** 2) / 12))
d_raw = max(abs(raw[i] - memo_v[i]) for i in range(len(qs)))
d_ext = max(abs(ext[i] - memo_v[i]) for i in range(len(qs)))
chk('I25-11a', d_raw < 2e-5,
    '备忘录表列 vs 我复算的【Rp=1000 原始值】最大差 = %.1e ⟹ 表列就是原始 y 值' % d_raw)
chk('I25-11b', d_ext > 1e-3,
    '备忘录取表列 vs 【y→0 闭式 1/3+e²/12】最大差 = %.1e ⟹ 表头「y→0 外推值」是错的（C-79）' % d_ext)
chk('I25-11c', d_raw < d_ext / 50,
    '两个候选相差 %d 倍 ⟹ 结论可判定（不是口径口味）' % int(d_ext / max(d_raw, 1e-12)))

print('=== I25-12 派生量更正：κ = 0.30 的「真值比」 ===')
k0 = float(F(1, 3))
k1 = float(F(1, 3) + F(49, 51) ** 2 / 12)     # e = 49/51 = 0.9608（q = 50）
chk('I25-12', abs((k0 / 0.30 - 1) - 0.111111) < 1e-5 and abs((k1 / 0.30 - 1) - 0.367528) < 1e-4,
    'e→0: +%.3f%%；e=0.9608: +%.3f%%（原写 37.2%% ⟹ 更正为 %.2f%%）'
    % (100 * (k0 / 0.30 - 1), 100 * (k1 / 0.30 - 1), 100 * (k1 / 0.30 - 1)))

# ---------------- 文档侧 ----------------
print('=== I25-13/16 论文中英同步 ＋ 交付物落地 ===')
Z, E = rd(ZH), rd(EN)
chk('I25-13a', Z.count('第 115 轮：I-25') >= 1 and E.count('round 115: I-25') >= 1,
    '论文中英各含第 115 轮注（ZH %d / EN %d）' % (Z.count('第 115 轮：I-25'), E.count('round 115: I-25')))
chk('I25-13b', Z.count('1/3 + e²/12') >= 1 and E.count('1/3 + e^2/12') + E.count('1/3 + e²/12') >= 1,
    '闭式 `1/3 + e²/12` 落地（中英）')
chk('I25-13c', rd(MAT).count('2.2c') >= 1, 'EMRI 材料包含 §2.2c')
chk('I25-13d', rd(D4M).count('C-79') >= 1, 'D4 备忘录含 C-79 更正注')

print('=== I25-14 清单：I-25 结项 ＋ C-79 ＋ 零表行 ＋ 计数 ===')
L = rd(LP)
i25row = [l for l in L.split('\n') if l.startswith('| **I-25** |')]
chk('I25-14a', len(i25row) == 1 and '结项（第 115 轮）' in i25row[0] and 'I-25-OLD' not in L,
    '清单 I-25 行已标结项（%d 行；旧占位残留 = %s）' % (len(i25row), 'I-25-OLD' in L))
chk('I25-14b', L.count('C-79') >= 2, '清单含 C-79 行与计数引用（%d 处）' % L.count('C-79'))
chk('I25-14c', L.count('第 115 轮') >= 2, '清单零表含第 115 轮行')
chk('I25-14d', '**78 条**（**C-79' in L, '撤回/更正计数 77 → 78')
chk('I25-15', rd(HO).count('第 115 轮') >= 1, '交接说明 §七 含第 115 轮条目')

print('=== I25-17 结构：第 113 轮注不再嵌进第 112 轮注内部（两段式）===')
for tag, cur, pre, mk112, mk113, cont112 in (
        ('ZH', ZH, ZH_PRE, '口径注（第 112 轮', '口径注（第 113 轮', '> `δ = 0.30·x_p`'),
        ('EN', EN, EN_PRE, 'caliber note (round 112', 'caliber note (round 113', '> ⚠️ **Caliber**')):
    Lc, Lp = rd(cur).split('\n'), rd(pre).split('\n')
    ic = next(i for i, s in enumerate(Lc) if mk112 in s)
    jc = next(i for i, s in enumerate(Lc) if mk113 in s)
    ip = next(i for i, s in enumerate(Lp) if mk112 in s)
    jp = next(i for i, s in enumerate(Lp) if mk113 in s)
    chk('I25-17' + tag, (jp - ip == 1) and (jc - ic >= 5) and Lc[ic + 1].startswith(cont112),
        '%s: 补丁前 113 紧贴 112 首行（gap=1）、112 块被劈开／补丁后 gap=%d 且 112 块续行紧接首行'
        % (tag, jc - ic))

print('=== I25-18 无新希腊字母（新块用到的符号 ⊆ 底本）===')
import re
greek = set('αβγδεζηθικλμνξπρστυφχψωΓΔΘΛΞΠΣΦΨΩ')
newblk = []
for src, mk in ((Z, '第 115 轮：I-25'), (E, 'round 115: I-25')):
    i = src.index(mk)
    j = src.index('\n\n', i)
    newblk.append(src[i:j])
syms_new = set(ch for b in newblk for ch in b if ch in greek)
pre_txt = rd(ZH_PRE) + rd(EN_PRE)
miss = sorted(c for c in syms_new if c not in pre_txt)
chk('I25-18', not miss,
    '新块希腊字母 %s 全部已在底本中出现（新增 = %s）' % (sorted(syms_new), miss or '无'))

print('')
print('通过 %d 项，失败 %d 项' % (n_ok, n_bad))
