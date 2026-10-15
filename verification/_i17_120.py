# -*- coding: utf-8 -*-
"""第 120 轮核验：I-17 修定（第五力窗口 —— 2025-26 约束带更新 ＋ 一处判决细化）
I17-1 … I17-24。用法：补丁前跑（物理部分）、补丁后复跑（全部）。
"""
import io, os, math, re

BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
OUT = os.path.join(BASE, 'outputs')
HIS = os.path.join(BASE, 'MAPS-Unified-Framework', 'paper', 'history')
MEM = os.path.join(BASE, '.workbuddy', 'memory')

def rd(p): return io.open(p, encoding='utf-8').read()
ZH = os.path.join(OUT, '论文初稿_正反物质对风暴统一框架_v2.9.md')
EN = os.path.join(OUT, 'Paper_MatterAntimatterPairStorm_v2.9_EN.md')
LP = os.path.join(OUT, '工程期望清单.md')
HO = os.path.join(BASE, '环境交接说明.md')
M72 = os.path.join(OUT, 'Φ的耦合强度_框架给不出第五力的另一半.md')
M118 = os.path.join(OUT, '外部输入清单_可接入的活问题与渠道_2026-10.md')
MEMO = os.path.join(OUT, 'I17第五力窗口_2025-26约束带与47微米档的存活.md')
SKILL = r'C:\Users\Administrator\.workbuddy\skills\maps-deduction-round\SKILL.md'
D = '第120轮前'
PRE = {
    'ZH': os.path.join(HIS, '论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-04%s.md' % D),
    'EN': os.path.join(HIS, 'Paper_v2.9_EN_备份_2026-10-04%s.md' % D),
    'LP': os.path.join(OUT, '工程期望清单_备份_2026-10-04%s.md' % D),
    'HO': os.path.join(BASE, '环境交接说明_备份_2026-10-04%s.md' % D),
    'M72': os.path.join(OUT, 'Φ的耦合强度_框架给不出第五力的另一半_备份_2026-10-04%s.md' % D),
    'M118': os.path.join(OUT, '外部输入清单_可接入的活问题与渠道_2026-10_备份_2026-10-04%s.md' % D),
}

OK = 0
FAIL = 0
def chk(tag, cond, msg):
    global OK, FAIL
    if cond:
        OK += 1
        print('[OK] %-8s %s' % (tag, msg))
    else:
        FAIL += 1
        print('[XX] %-8s %s' % (tag, msg))

print('=' * 78)
print('第 120 轮核验 · I-17 修定（第五力窗口）')
print('=' * 78)

# ---------- 物理部分 ----------
HBARC = 1.97327e-7      # eV·m
LPm = 1.616255e-35      # m
EP = 1.220890e28        # eV
print('')
print('--- 物理：常数与四档力程 ---')

# I17-1 常数自洽
lp_self = 1.616255e-35
chk('I17-1', abs(HBARC / 1e-3 * 1e6 - 197.327) < 0.01,
    'hbar*c = %.5e eV·m；1 meV 对应 lambda = %.3f μm（应 ~197.33）' % (HBARC, HBARC / 1e-3 * 1e6))

# I17-2 三档力程（(b)(c)）与 l_P 档
lb = HBARC / 1.0181e-3
lc = HBARC / 4.1894e-3
chk('I17-2', abs(lb / 1.938e-4 - 1.0) < 5e-3 and abs(lc / 4.710e-5 - 1.0) < 5e-3,
    '(b) 1.0181 meV -> %.4e m = %.2f μm；(c) 4.1894 meV -> %.4e m = %.2f μm' % (lb, lb * 1e6, lc, lc * 1e6))

# I17-3 (a)(d) 普朗克档
J = 3.0 * EP
ma = 0.41 * J
la = HBARC / ma
ld = HBARC / EP
chk('I17-3', abs(la / LPm - 0.8131) < 5e-3 and abs(ld / LPm - 1.0) < 5e-3,
    '(a) 0.41*3*E_P -> %.4f l_P；(d) E_P -> %.6f l_P' % (la / LPm, ld / LPm))

# I17-4 Juno 换算
lj = HBARC / 1e-14
chk('I17-4', abs(lj / 1.9733e7 - 1.0) < 5e-3,
    'Juno m = 1e-14 eV -> lambda = %.4e m = %.2e AU' % (lj, lj / 1.495978707e11))

print('')
print('--- 物理：两锚点幂律插值族（alpha_max(lambda)）---')
# (lambda0, alpha0) -> (lambda1, alpha1)：alpha = alpha0 * (l/l0)^(-p)，p = ln(a0/a1)/ln(l1/l0)
MODELS = {
    'A: Tan 48um/1 + 70um/1/3': (48e-6, 1.0, 70e-6, 1.0 / 3.0),
    'B: Tan 48um/1 + 1mm/1e-3': (48e-6, 1.0, 1000e-6, 1e-3),
    'C: Tan 48um/1 + 2mm/1e-3': (48e-6, 1.0, 2000e-6, 1e-3),
    'D: Lee 38.6um/1 + 1mm/1e-3': (38.6e-6, 1.0, 1000e-6, 1e-3),
}

def alpha_of(l, l0, a0, l1, a1):
    p = math.log(a0 / a1) / math.log(l1 / l0)
    return a0 * (l / l0) ** (-p), p

lam_star, ac47, ac194 = [], [], []
for nm, (l0, a0, l1, a1) in MODELS.items():
    p = math.log(a0 / a1) / math.log(l1 / l0)
    ls = l0 * (3.0) ** (1.0 / p)          # alpha = 1/3 的交叉
    a47, _ = alpha_of(47.1e-6, l0, a0, l1, a1)
    a194, _ = alpha_of(193.8e-6, l0, a0, l1, a1)
    lam_star.append(ls); ac47.append(a47); ac194.append(a194)
    print('   %-28s p=%.3f  lambda_(1/3)=%.1f μm  a_max(47.1)=%.4f  a_max(193.8)=%.4f'
          % (nm, p, ls * 1e6, a47, a194))

# I17-5 λ_{1/3} 区间
chk('I17-5', 60e-6 < min(lam_star) and max(lam_star) < 95e-6,
    'lambda_(1/3) ∈ [%.1f, %.1f] μm（4 模型）' % (min(lam_star) * 1e6, max(lam_star) * 1e6))

# I17-6 (c) 47.1 μm：四模型都 > 1/3，余量区间
m47 = [a / (1.0 / 3.0) for a in ac47]
chk('I17-6', all(a > 1.0 / 3.0 for a in ac47) and 1.9 < min(m47) and max(m47) < 3.3,
    '(c) 存活：a_max(47.1) ∈ [%.3f, %.3f]；余量 ∈ [%.2f, %.2f]' % (min(ac47), max(ac47), min(m47), max(m47)))

# I17-7 (b) 193.8 μm：四模型都 < 1/3，余量区间
m194 = [(1.0 / 3.0) / a for a in ac194]
chk('I17-7', all(a < 1.0 / 3.0 for a in ac194) and 4.0 < min(m194) and max(m194) < 20.0,
    '(b) 排除：a_max(193.8) ∈ [%.4f, %.4f]；余量 ∈ [%.1f, %.1f]' % (min(ac194), max(ac194), min(m194), max(m194)))

# I17-8 ×3 判据：判定 (c) 所需改进
chk('I17-8', 1.9 < min(m47) and max(m47) < 3.3,
    '判定 (c)（压到 a_max<1/3）所需改进 = a_max(47.1)/(1/3) ∈ [%.2f, %.2f] ⟹ 「×3 量级」' % (min(m47), max(m47)))

# I17-9 α_Y = 1/3 与 Cassini 的量级链
al_rad = 1.0 / (2 * 0 + 3)
al_beta = 2 * (1.0 / 6.0)
al_cass = 1.0 / (2 * 4e4 + 3)
chk('I17-9', abs(al_rad - 1.0 / 3.0) < 1e-12 and abs(al_beta - 1.0 / 3.0) < 1e-12 and 1e-5 < al_cass < 2e-5,
    'radion: 1/(2w+3)|w=0 = %.6f = 2β²|β=1/√6 = %.6f；Cassini(w>4e4) α < %.3e' % (al_rad, al_beta, al_cass))

# I17-10 微球锚点（120 备忘中）
M = rd(MEMO) if os.path.exists(MEMO) else ''
chk('I17-10', ('10⁷' in M or '10^7' in M or '107' in M) and ('10⁶' in M or '106' in M or '10^6' in M) and '2412.13167' in M,
    '备忘含微球锚点（10^7 @5 μm / 10^6 @>=10 μm）+ arXiv 号')

# I17-11 HUST 与 2026 综述
chk('I17-11', '2605.18212' in M and ('10⁻⁴' in M or '1e-4' in M or '10^-4' in M),
    '备忘含综述 arXiv:2605.18212 与 HUST 厘米 α < 10^-4')

# I17-12 Lee / Tan 边界与争议带
chk('I17-12', ('38.6' in M and '48' in M and '39–48' in M) and ('38.6' in rd(ZH)) and ('38.6' in rd(EN)),
    'Lee 38.6 μm / Tan 48 μm / 39–48 争议带（备忘 + 论文中英）')

# I17-13 MORRIS/Juno 的「计划 vs 实测」标注
chk('I17-13', ('计划' in M) and ('10⁻¹⁴' in M) and ('MORRIS' in M),
    '备忘区分【计划】（MORRIS 等）与实测（Juno 10^-14 eV 等）')

# ---------- 文档部分 ----------
print('')
print('--- 文档：论文中英 ---')
zh_t = rd(ZH); en_t = rd(EN); zh_p = rd(PRE['ZH']); en_p = rd(PRE['EN'])

# I17-14 ZH 120 块
z120 = zh_t.count('v2.9 补充（第 120 轮')
z120p = zh_p.count('v2.9 补充（第 120 轮')
chk('I17-14', z120 == 1 and z120p == 0,
    'ZH 120 块 = %d 处（补丁前 %d）' % (z120, z120p))

# I17-15 ZH 块结构（连续 >、无空行、≥6 行）
zlines = zh_t.split('\n')
zi = [k for k, s in enumerate(zlines) if 'v2.9 补充（第 120 轮' in s][0] if z120 else -1
zblk = []
if zi >= 0:
    j = zi
    while j < len(zlines) and zlines[j].startswith('>'):
        zblk.append(zlines[j]); j += 1
chk('I17-15', len(zblk) >= 6 and all(s.startswith('>') for s in zblk) and not any(s.strip() == '>' for s in zblk),
    'ZH 块 %d 行、全 `> `、无块内空行' % len(zblk))

# I17-16 ZH 细化行（补丁前无 / 补丁后有）
chk('I17-16', ('第 120 轮细化（C-83）' in zh_t) and ('第 120 轮细化' not in zh_p),
    'ZH 第 72 块细化行（两段式：前 %d / 后 %d）' % (zh_p.count('第 120 轮细化'), zh_t.count('第 120 轮细化')))

# I17-17 EN 120 块 + 细化行
e120 = en_t.count('supplement (round 120')
e120p = en_p.count('supplement (round 120')
chk('I17-17', e120 == 1 and e120p == 0 and ('Round-120 refinement (C-83)' in en_t),
    'EN 120 块 = %d 处（前 %d）；细化行 = %d' % (e120, e120p, en_t.count('Round-120 refinement (C-83)')))

# I17-18 §8.6 α 约定（中英）
chk('I17-18', zh_t.count('第 120 轮补注（C-84）') == 1 and zh_p.count('C-84') == 0
    and en_t.count('Round-120 addendum (C-84)') == 1,
    '§8.6 α 约定：ZH 1 处（前 0）／EN 1 处')

# I17-19 中英关键串同步
key_pairs = [('α_Y', 'α_Y'), ('47.1', '47.1'), ('193.8', '193.8'), ('65–90', '65–90'), ('×3', '×3')]
allok = all((a in zh_t) and (b in en_t) for a, b in key_pairs)
chk('I17-19', allok, '关键串中英同步：' + ' / '.join(a for a, b in key_pairs))

print('')
print('--- 文档：清单 / 交接 / 备忘 / 记忆 / 技能 ---')
lp_t = rd(LP); lp_p = rd(PRE['LP'])
ho_t = rd(HO); ho_p = rd(PRE['HO'])
m72 = rd(M72); m72p = rd(PRE['M72'])
m118 = rd(M118); m118p = rd(PRE['M118'])
mem_t = rd(os.path.join(MEM, 'MEMORY.md'))
log_t = rd(os.path.join(MEM, '2026-10-04.md'))
sk_t = rd(SKILL)

# I17-20 清单四件
c83 = lp_t.count('| **C-83** |'); c84 = lp_t.count('| **C-84** |'); i26 = lp_t.count('| **I-26** |')
row120 = lp_t.count('第 120 轮**（**I-17 修定')
cnt83 = lp_t.count('**撤回 / 更正** | **83 条**')
chk('I17-20', c83 == 1 and c84 == 1 and i26 == 1 and row120 == 1 and cnt83 == 1 and lp_p.count('**C-83**') == 0,
    '清单：C-83×%d / C-84×%d / I-26×%d / 第120轮行×%d / 计数83×%d' % (c83, c84, i26, row120, cnt83))

# I17-21 交接说明
chk('I17-21', ho_t.count('第 120 轮后') == 1 and ho_t.count('（历史，第 119 轮后）') == 1
    and ho_p.count('当前建议（第 119 轮后）') == 1,
    '交接：新条目 1 处、119 降历史 1 处（补丁前 119 为当前建议）')

# I17-22 两份备忘注（两段式）
chk('I17-22', m72.count('第 120 轮') >= 1 and m72p.count('第 120 轮') == 0
    and m118.count('第 120 轮注') == 1 and m118p.count('第 120 轮注') == 0,
    '第 72 轮备忘 §十二（前 %d → 后 %d）＋ 第 118 轮备忘注（前 %d → 后 %d）'
    % (m72p.count('第 120 轮'), m72.count('第 120 轮'), m118p.count('第 120 轮注'), m118.count('第 120 轮注')))

# I17-23 记忆 / 日志 / 技能
chk('I17-23', ('进度 120' in mem_t) and ('I-26' in mem_t) and len(mem_t) <= 3000
    and log_t.count('第 120 轮') >= 1 and ('116. **⭐⭐⭐' in sk_t),
    'MEMORY 进度 120 / I-26 / %d 字符；日志含第 120 轮；技能含陷阱 116' % len(mem_t))

# I17-24 格式自查（新增块：非表格行 `\|`、块内残片）
def fmt_hits(t):
    L = t.split('\n')
    b1 = [i + 1 for i, s in enumerate(L) if s.strip().startswith(('，', ','))]
    b3 = [i + 1 for i, s in enumerate(L) if '\\|' in s and not s.lstrip().startswith('|')]
    return b1, b3
zb1, zb3 = fmt_hits(zh_t); eb1, eb3 = fmt_hits(en_t)
mb1, mb3 = fmt_hits(M)
zhp1, zhp3 = fmt_hits(zh_p)
enp1, enp3 = fmt_hits(en_p)
newb1 = [i for i in zb1 if i not in zhp1]
chk('I17-24', len(zb3) == len(zhp3) and len(eb3) == len(enp3) and len(mb3) == 0 and len(newb1) == 0,
    '格式（两段式）：表外 `\\|` ZH %d(前 %d)/EN %d(前 %d)/备忘 %d；ZH 新增残片 = %d'
    % (len(zb3), len(zhp3), len(eb3), len(enp3), len(mb3), len(newb1)))

print('')
print('=' * 78)
print('通过 %d 项，失败 %d 项' % (OK, FAIL))
print('=' * 78)
