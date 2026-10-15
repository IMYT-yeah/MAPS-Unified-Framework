# -*- coding: utf-8 -*-
"""第 123 轮核验：动力学·耦合层的可行性判定（D123-*）。

预跑（补丁前）：G0/A/B/C/D 组应全过；E/F 组的「补丁后」项失败 = 预期。
补丁后复跑：必须 0 失败。
"""
import io, os, re

BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
OUT  = os.path.join(BASE, 'outputs')
HIST = os.path.join(BASE, 'MAPS-Unified-Framework', 'paper', 'history')
MEMD = os.path.join(BASE, '.workbuddy', 'memory')
LP   = os.path.join(OUT, '工程期望清单.md')
ZH   = os.path.join(OUT, '论文初稿_正反物质对风暴统一框架_v2.9.md')
EN   = os.path.join(OUT, 'Paper_MatterAntimatterPairStorm_v2.9_EN.md')
HO   = os.path.join(BASE, '环境交接说明.md')
MT   = os.path.join(OUT, '动力学耦合层可行性_三档判定与输入台账.md')
LOG  = os.path.join(MEMD, '2026-10-05.md')
KM   = os.path.join(MEMD, 'MEMORY.md')
SK   = r'C:\Users\Administrator\.workbuddy\skills\maps-deduction-round\SKILL.md'
ZHb  = os.path.join(HIST, '论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-05第123轮前.md')
ENb  = os.path.join(HIST, 'Paper_v2.9_EN_备份_2026-10-05第123轮前.md')
LPb  = os.path.join(OUT, '工程期望清单_备份_2026-10-05第123轮前.md')
HOb  = os.path.join(BASE, '环境交接说明_备份_2026-10-05第123轮前.md')

def rd(p):
    return io.open(p, encoding='utf-8').read()

OK = FAIL = 0
def chk(tag, cond, msg=''):
    global OK, FAIL
    if cond:
        OK += 1; print('  [OK] %-10s %s' % (tag, msg))
    else:
        FAIL += 1; print('  [XX] %-10s %s' % (tag, msg))

print('=========== 第 123 轮核验：动力学·耦合层（可行性判定）===========')

# ---------------- G0 底本 ----------------
print('--- G0 补丁前备份 ---')
g0 = all(os.path.exists(p) for p in (ZHb, ENb, LPb, HOb))
chk('D123-00', g0, '五份补丁前备份存在（ZH/EN/清单/交接/…）')

# ---------------- A 三条结构性障碍 ----------------
print('--- A 三条结构性障碍（I-16 / I-20 / I-21）---')
LP_t = rd(LP); LPL = LP_t.split('\n')
def rows_of(tag):
    return [s for s in LPL if s.startswith('| **' + tag + '**')]
r16 = '\n'.join(rows_of('I-16'))
r20 = '\n'.join(rows_of('I-20'))
r21 = '\n'.join(rows_of('I-21'))
chk('D123-A1', ('位置算符缺口' in r16) and len(rows_of('I-16')) >= 1,
    'I-16 = 位置算子缺口（清单行 %d 条）' % len(rows_of('I-16')))
mt16 = os.path.join(OUT, '位置算符缺口_I-16的形式化与三层判定.md')
t16 = rd(mt16) if os.path.exists(mt16) else ''
chk('D123-A2', ('三层里没有一层同时满足' in t16) and ('c-数' in t16),
    '第 68 轮备忘录：三层判定表（无一层同时满足「位置＋能量＋q-数」）')
chk('D123-A3', ('不是方程，是对象' in r20) and ('I-20' in r20),
    'I-20：两个 ρ 不接 —— 缺的不是方程，是对象')
chk('D123-A4', ('外加' in r21) and ('非交换' in r21),
    'I-21：§7 非交换化是「外加」的')

# ---------------- B 终止态台账（15 例） ----------------
print('--- B 终止态台账（15 例，逐条证人）---')
LEDGER = [
    ('C-4',  '恒等式',      'E_c ≡ 1 meV（恒等式，非推导）'),
    ('N-32', '恒等式',      'D = ℏ/(3m)（恒等式；G 缩放检测）'),
    ('C-67', '恒等式',      '麦克斯韦谱「数值验证」= 恒等式'),
    ('C-76', '恒等式',      '反解 q 表 = 换写（log₂(4q)）'),
    ('C-77', '量纲',        'M²/A 不是普朗克常数（量纲＋恒等式）'),
    ('N-36', '定义式',      'h 的 L² = 定义式（定义 ≠ 发现）'),
    ('C-72', '量纲',        'R_net 量纲不成立（7.08e29 倍歧义）'),
    ('N-33', '没有对象',    'g 的精确值：没有对象'),
    ('N-35', '没有对象',    '8π/3：没有对象'),
    ('N-34', '4 个换算因子', 'n_G → α 无路径（4 个换算因子全缺）'),
    ('N-31', '条件命题',    '非交换 ⇒ 量子关联 = 条件命题、零框架元素'),
    ('N-30', '22.4σ',       '等分账 ρ + 守恒 ⟹ w = −1/3（22.4σ 排除）'),
    ('N-40', '一维简并族',  'η 能标不可导出（一维简并族）'),
    ('N-41', '不可辨识',    'ℏ 的独立身份不可辨识'),
    ('C-78', '唯象输入',    'κ = 0.30 是唯象输入（非标定/推导量）'),
]
b_ok = 0
for i, (tag, kw, desc) in enumerate(LEDGER):
    hit = any(s.startswith('| **' + tag + '**') and (kw in s) for s in LPL)
    if hit:
        b_ok += 1
    else:
        print('      [miss] %s（%s）—— 关键词未命中' % (tag, kw))
chk('D123-B', b_ok == len(LEDGER),
    '终止态台账 %d/%d 证人命中（恒等式 6／量纲 1／无对象 2／缺因子 1／外加 1／排除 1／自由 2／填的 1）'
    % (b_ok, len(LEDGER)))

# ---------------- C 三个样板（= 全部对外产出） ----------------
print('--- C 三个样板（度规 / Φ / A2）---')
b3 = rd(os.path.join(OUT, 'B3_高阶PPN与指数度规.md'))
chk('D123-C1', ('三条独立推导在此收敛' in b3) and ('指数度规' in rd(ZH)),
    '样板① 度规扇区：B3 三条收敛（论文含「指数度规」）')
cm = rd(os.path.join(OUT, '从A2推组分_暗能量能标已定.md'))
chk('D123-C2', ('1.0181 meV' in cm) and ('空白' in cm),
    '样板③ A2：E_c = 1.0181 meV（+ 暗物质空白）')
dy = rd(os.path.join(OUT, '动力学缺口_收缩到一条与tP复合过程.md'))
chk('D123-C3', ('Π·t_P = ρ_P/N' in dy) and ('61 个量级' in dy),
    '样板③ A2：自洽性过滤（Π·t_P = ρ_P/N；超出稀释率 61 量级）')
pkg = os.path.join(OUT, '第五力实验线材料包_给短程引力实验组.md')
c85 = any(s.startswith('| **C-85**') and ('×3.2' in s) for s in LPL)
chk('D123-C4', os.path.exists(pkg) and c85,
    '样板② Φ 扇区：实验线材料包存在 ＋ C-85（×3.2 = 干净排除）')
d4 = rd(os.path.join(OUT, 'D4结项_EMRI进动系数的偏心率依赖与1_3极限.md'))
chk('D123-C5', ('参数 −1' in d4) and ('κ_rel' in d4),
    '附带升级例：κ 0.30 → κ_rel(e)（参数 −1）')

# ---------------- D 输入台账侧证人 ----------------
print('--- D 输入台账侧证人 ---')
d1 = (rd(ZH).count('标准物理输入') >= 2)
d2 = any(s.startswith('| **N-13**') and ('0.25' in s) for s in LPL) and \
     any(s.startswith('| **I-17**') and ('第五力' in s) for s in LPL)
d3 = any(s.startswith('| **N-33**') and ('第 4 个纯输入' in s) for s in LPL)
d4b = any(s.startswith('| **I-26**') and ('screened' in s) for s in LPL) and \
      any(s.startswith('| **I-27**') and ('40–60' in s) for s in LPL)
chk('D123-D1', d1, '论文含「标准物理输入」≥2（1/4 与 β=1/(2π)）')
chk('D123-D2', d2, 'N-13（0.25 不等式）与 I-17（第五力）登记在册')
chk('D123-D3', d3, 'N-33 行含「第 4 个纯输入」（Φ 耦合成本）')
chk('D123-D4', d4b, 'I-26（screened）与 I-27（40–60 μm 投影）登记在册')

# ---------------- E 两段式（补丁前 / 补丁后） ----------------
print('--- E 两段式（底本 vs 当前稿）---')
ZHb_t = rd(ZHb); ENb_t = rd(ENb); LPb_t = rd(LPb); HOb_t = rd(HOb)
ZH_t = rd(ZH); EN_t = rd(EN); HO_t = rd(HO)

def block_of(text, startpred):
    L = text.split('\n')
    idx = [k for k, s in enumerate(L) if startpred(s)]
    if len(idx) != 1:
        return None, len(idx)
    i = idx[0]; j = i
    while j + 1 < len(L) and L[j + 1].startswith('>'):
        j += 1
    return L[i:j + 1], 1

# E1: ZH 新块（两段式 + 连续性）
zb, nzb = block_of(ZH_t, lambda s: s.startswith('> **【v2.9 判定（第 123 轮'))
zb_pre = ZHb_t.count('v2.9 判定（第 123 轮')
cont = bool(zb) and all(s.startswith('>') for s in zb) and not any(s.strip() == '>' for s in zb)
chk('D123-E1', (zb_pre == 0) and (nzb == 1) and cont and bool(zb) and len(zb) >= 4,
    'ZH 第 123 轮块：补丁前 0 处 ／ 补丁后 1 块 %s 行、连续无空行' % (len(zb) if zb else '?'))

# E2: EN 新块
eb, neb = block_of(EN_t, lambda s: s.startswith('> **【v2.9 determination (Round 123'))
eb_pre = ENb_t.count('determination (Round 123')
contE = bool(eb) and all(s.startswith('>') for s in eb) and not any(s.strip() == '>' for s in eb)
chk('D123-E2', (eb_pre == 0) and (neb == 1) and contE and bool(eb) and len(eb) >= 4,
    'EN 第 123 轮块：补丁前 0 处 ／ 补丁后 1 块 %s 行、连续无空行' % (len(eb) if eb else '?'))

# E1b/E2b: 块内关键内容
chk('D123-E1b', bool(zb) and all(k in '\n'.join(zb) for k in ('N-43', 'I-16', 'I-20', 'I-21', '15 例', '失效条件')),
    'ZH 块含 N-43/I-16/I-20/I-21/15 例/失效条件')
chk('D123-E2b', bool(eb) and all(k in '\n'.join(eb) for k in ('N-43', 'I-16', 'I-20', 'I-21', '15-instance', 'Failure condition')),
    'EN 块含 N-43/I-16/I-20/I-21/15-instance/Failure condition')

# E3: 清单 N-43 / C-86（两段式 + 顺序）
n43 = [k for k, s in enumerate(LPL) if s.startswith('| **N-43**')]
c86 = [k for k, s in enumerate(LPL) if s.startswith('| **C-86**')]
c85 = [k for k, s in enumerate(LPL) if s.startswith('| **C-85**')]
pre_n43 = LPb_t.count('| **N-43**'); pre_c86 = LPb_t.count('| **C-86**')
order = (len(c85) == 1 and len(c86) == 1 and len(n43) == 1 and c86[0] == c85[0] + 1 and n43[0] == c86[0] + 1)
chk('D123-E3', (pre_n43 == 0) and (pre_c86 == 0) and order,
    '清单：补丁前 0 ／ N-43 与 C-86 各 1 条；顺序 C-85 → C-86 → N-43（紧跟）')

# E4: 计数器
chk('D123-E4a', ('**42 条**' in LPb_t) and ('**43 条**' in LP_t),
    '负面计数器：补丁前 42 条 → 补丁后 43 条')
chk('D123-E4b', ('**84 条**' in LPb_t) and ('**85 条**' in LP_t),
    '撤回/更正计数器：补丁前 84 条 → 补丁后 85 条')

# E5: 零表新行
zr = [k for k, s in enumerate(LPL) if s.startswith('| **第 123 轮**（')]
r121 = [k for k, s in enumerate(LPL) if s.startswith('| **第 121 轮**（')]
zr_pre = LPb_t.count('| **第 123 轮**（')
chk('D123-E5', (zr_pre == 0) and (len(zr) == 1) and (len(r121) == 1) and (zr[0] == r121[0] + 1),
    '零表：新行紧跟第 121 轮行（补丁前 0 处）')

# E6: 交接说明
ho_pre_new = HOb_t.count('当前建议（第 123 轮后）')
ho_new = HO_t.count('当前建议（第 123 轮后）')
ho_dem = HO_t.count('**（历史，第 121 轮后）**')
chk('D123-E6', (ho_pre_new == 0) and (ho_new == 1) and (ho_dem == 1),
    '交接 §七：新条目（123）＋ 旧条目降为「历史，第 121 轮后」')

# E7: 金刚石补标（C-86）
jg_pre = ('（金刚石结构）' in HOb_t) and ('C-86' not in HOb_t)
jg_post = ('【第 123 轮补标（C-86）】' in HO_t) and ('简单立方' in HO_t)
chk('D123-E7', jg_pre and jg_post,
    '交接 L2764 行：「金刚石定案」补标为已撤回（C-86；几何 = 简单立方）')

# E8: 日志
log_ok = os.path.exists(LOG) and ('第 123 轮' in rd(LOG)) and ('动力学·耦合层' in rd(LOG))
chk('D123-E8', log_ok, '今日日志 2026-10-05.md 已创建并含第 123 轮条目')

# E9: MEMORY
km = rd(KM)
chk('D123-E9', ('进度 123' in km) and ('N-43' in km) and (len(km) <= 3000),
    'MEMORY：进度 123 ＋ N-43 边界 ＋ 长度 %d ≤ 3000' % len(km))

# E10: 清单 L265 剩余待办行
l265 = [s for s in LPL if s.startswith('**剩余待办（全部）**')]
chk('D123-E10', len(l265) == 1 and ('第 123 轮补（可行性判定）' in l265[0]),
    '清单「剩余待办」行补第 123 轮口径（判否 + 不是待办）')

# E11: 技能
sk = rd(SK)
chk('D123-E11', ('118.' in sk) and ('N-43' in sk) and ('动力学·耦合层' in sk),
    '技能：陷阱 118 ＋ §5.0 边界（N-43）')

# ---------------- F 结构 / 格式 ----------------
print('--- F 结构 / 格式 ---')
mt_ok = os.path.exists(MT) and all(k in rd(MT) for k in ('N-43', '15 例', '失效条件', '14 项', '三档'))
chk('D123-F1', mt_ok, '备忘录存在且含核心要素（N-43/15 例/失效条件/14 项/三档）')

def fmt_hits(p):
    L = rd(p).split('\n')
    frag = [i + 1 for i, s in enumerate(L) if s.strip().startswith(('，', ','))]
    bars = [i + 1 for i, s in enumerate(L) if '\\|' in s and not s.lstrip().startswith('|')]
    return frag, bars

zf, zbar = fmt_hits(ZH); zf0, zbar0 = fmt_hits(ZHb)
ef, ebar = fmt_hits(EN); ef0, ebar0 = fmt_hits(ENb)
chk('D123-F2', len(zf) == len(zf0) and len(zbar) == len(zbar0) and len(ef) == len(ef0) and len(ebar) == len(ebar0),
    '论文格式（两段式）：残片 ZH %d/%d、表外竖线 ZH %d/%d、EN %d/%d、%d/%d（无新增）'
    % (len(zf), len(zf0), len(zbar), len(zbar0), len(ef), len(ef0), len(ebar), len(ebar0)))

if os.path.exists(MT):
    mf, mbar = fmt_hits(MT)
    chk('D123-F3', len(mf) == 0 and len(mbar) == 0,
        '备忘录格式：残片 %d、表外竖线 %d（应为 0）' % (len(mf), len(mbar)))
else:
    chk('D123-F3', False, '备忘录尚未生成（预跑预期）')

# F4: 占位符已替换 + 最大编号
ph = sum(rd(p).count('«ND123') for p in (ZH, EN, LP, MT, LOG))
nmax = max(int(m.group(1)) for m in re.finditer(r'^\| \*\*N-(\d+)\*\*', LP_t, re.M))
cmax = max(int(m.group(1)) for m in re.finditer(r'^\| \*\*C-(\d+)\*\*', LP_t, re.M))
chk('D123-F4', (ph == 0) and (nmax == 43) and (cmax == 86),
    '占位符已替换（残留 %d）＋ 编号上限 N-%d / C-%d' % (ph, nmax, cmax))

print('')
print('通过 %d 项，失败 %d 项' % (OK, FAIL))
io.open(os.path.join(OUT, '_dyn123_count.txt'), 'w', encoding='utf-8').write('%d %d' % (OK, FAIL))
