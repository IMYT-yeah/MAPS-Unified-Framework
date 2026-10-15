# -*- coding: utf-8 -*-
"""第 117 轮核验（K117-1…）：Kerr 重算 + C-81/C-82 落地的两段式取证。"""
import io, os, re

BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
P = dict(
    ZH=os.path.join(BASE, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md'),
    EN=os.path.join(BASE, 'outputs', 'Paper_MatterAntimatterPairStorm_v2.9_EN.md'),
    MAT=os.path.join(BASE, 'outputs', 'EMRI材料包_给LISA组的S-E1-E4.md'),
    LIST=os.path.join(BASE, 'outputs', '工程期望清单.md'),
    HO=os.path.join(BASE, '环境交接说明.md'),
    MEMO=os.path.join(BASE, 'outputs', 'Kerr版EMRI重算_delta与lnL与sigma口径_C-81与C-82.md'),
    SKILL=r'C:\Users\Administrator\.workbuddy\skills\maps-deduction-round\SKILL.md',
    MEM=os.path.join(BASE, '.workbuddy', 'memory', 'MEMORY.md'),
    LOG=os.path.join(BASE, '.workbuddy', 'memory', '2026-10-04.md'),
)
B = dict(
    ZH=os.path.join(BASE, 'MAPS-Unified-Framework', 'paper', 'history',
                    '论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-04第117轮前.md'),
    EN=os.path.join(BASE, 'MAPS-Unified-Framework', 'paper', 'history',
                    'Paper_v2.9_EN_备份_2026-10-04第117轮前.md'),
    MAT=os.path.join(BASE, 'outputs', 'EMRI材料包_给LISA组的S-E1-E4_备份_2026-10-04第117轮前.md'),
    LIST=os.path.join(BASE, 'outputs', '工程期望清单_备份_2026-10-04第117轮前.md'),
    HO=os.path.join(BASE, '环境交接说明_备份_2026-10-04第117轮前.md'),
)
rd = lambda p: io.open(p, encoding='utf-8').read()
OK, FAIL = 0, 0

def chk(tag, cond, msg, strict=True):
    global OK, FAIL
    if cond:
        OK += 1; print('  [OK] %-9s %s' % (tag, msg))
    elif strict:
        FAIL += 1; print('  [XX] %-9s %s' % (tag, msg))
    else:
        print('  [INFO] %-9s %s' % (tag, msg))

cur = {k: rd(v) for k, v in P.items() if os.path.exists(v)}
bak = {k: rd(v) for k, v in B.items()}

print('=== K117-1 材料 §五 第三行（Kerr 行）===')
row = [s for s in cur['MAT'].split('\n') if s.startswith('| `KerrEMRI波形与贝叶斯分析`')]
chk('K117-1a', len(row) == 1, 'Kerr 行 %d 条' % len(row))
chk('K117-1b', '**`ΔlnL = 399`**' in row[0] and '**`δ = 2.222%`**' in row[0] and '7.9×10⁻⁴' in row[0],
    '新版含 δ=2.222% / ΔlnL=399 / 有效宽 7.9×10⁻⁴')
chk('K117-1c', '待按第 116 轮重算' not in cur['MAT'] and '待按第 116 轮重算' in bak['MAT'],
    '「待按第 116 轮重算」：补丁前在（取证）、补丁后 0 处（确认）')

print('=== K117-2 材料 §2.2e ===')
i = cur['MAT'].find('### 2.2e 【第 117 轮】')
chk('K117-2a', i >= 0, '§2.2e 存在')
sec = cur['MAT'][i:i + 4000]
for s in ['2.222%', '399.2', '385.9', '7.90×10⁻⁷', '1.588×10⁻⁶', '7.87×10⁻⁴', '9.65×10⁻⁴', '28.3σ', '针状']:
    chk('K117-2b', s in sec, '§2.2e 含 %s' % s)
chk('K117-2c', i < cur['MAT'].find('### 2.3 三个前提'), '§2.2e 位于 §2.3 之前')

print('=== K117-3 材料 §2.2d 更正段（两段式）===')
chk('K117-3', '2.5416×10⁻⁶' in cur['MAT'] and '2.5396×10⁻⁶' in cur['MAT']
    and '2.5416×10⁻⁶' not in bak['MAT'],
    '更正段（2.5416/2.5396）补丁后 1 处、补丁前 0 处')
chk('K117-3b', '（比值 ≈ 853，与本文测的 459 同量级）' not in cur['MAT']
    and '（比值 ≈ 853，与本文测的 459 同量级）' in bak['MAT'],
    '§三注旧句已替换（补丁前在）')

print('=== K117-4 论文中英 117 块 ===')
for tag, key, mark in (('ZH', 'ZH', 'v2.9 口径注（第 117 轮'), ('EN', 'EN', 'caliber note (round 117')):
    L = cur[key].split('\n')
    idx = [k for k, s in enumerate(L) if mark in s]
    chk('K117-4a', len(idx) == 1, '%s 117 块起始 1 处' % tag)
    k0 = idx[0]; k1 = k0
    while k1 < len(L) and L[k1].startswith('>'): k1 += 1
    chk('K117-4b', k1 - k0 == 23, '%s 块长 = %d（应 23）' % (tag, k1 - k0))
    chk('K117-4c', all(s.startswith('>') and s.strip() != '>' for s in L[k0:k1]),
        '%s 块全为 `> ` 且无空行' % tag)
    # 紧接上一块（相邻行也是 >）
    chk('K117-4e', L[k0 - 1].startswith('>'), '%s 117 块紧接 116 块（上行亦为 `>`）' % tag)

print('=== K117-5 116 块内更正指针 ===')
chk('K117-5a', '【第 117 轮更正（C-81）】' in cur['ZH'] and '【第 117 轮更正（C-81）】' not in bak['ZH'],
    'ZH C-81 指针（两段式）')
chk('K117-5b', '【第 117 轮更正】' in cur['ZH'] and '**C-7 的 459**' in cur['ZH'].split('【第 117 轮更正】')[1][:400],
    'ZH 459/比值指针')
chk('K117-5c', 'Round-117 correction (C-81)' in cur['EN'] and 'Round-117 correction (C-81)' not in bak['EN'],
    'EN C-81 指针（两段式）')

print('=== K117-6 「仍未做」标完成 ===')
chk('K117-6a', '~~**Kerr 版**未重算' in cur['ZH'] and '**✅ 第 117 轮已完成**' in cur['ZH'],
    'ZH：strikethrough + ✅')
chk('K117-6b', 'done in round 117' in cur['EN'] and '**Still not done** ~~' in cur['EN'],
    'EN：strikethrough + done in round 117')

print('=== K117-7 §4.5b 正文指针 ===')
chk('K117-7', 'Kerr 版已重算 —— `ΔlnL = 399`' in cur['ZH'] and 'the Kerr version has been recomputed' in cur['EN'],
    'ZH/EN §4.5b 各加更正指针')

print('=== K117-8 清单 ===')
chk('K117-8a', '| **第 117 轮**（**Kerr 版重算**）' in cur['LIST'], '第 117 轮行')
c81 = [s for s in cur['LIST'].split('\n') if s.startswith('| **C-81** |')]
c82 = [s for s in cur['LIST'].split('\n') if s.startswith('| **C-82** |')]
chk('K117-8b', len(c81) == 1 and len(c82) == 1, 'C-81/C-82 行各 1 条')
seq = [m.group(1) for s in cur['LIST'].split('\n') for m in [re.match(r'^\| \*\*C-(\d+)\*\* ', s)] if m]
k80 = seq.index('80'); 
chk('K117-8c', seq[k80:k80 + 3] == ['80', '81', '82'],
    'C 序号：C-80 后紧跟 C-81、C-82（实际序列片段 %s）' % seq[k80:k80 + 4])
chk('K117-8d', '**81 条**' in cur['LIST'] and '**79 条**' in bak['LIST'] and '**79 条**' not in cur['LIST'],
    '撤回计数 79 → 81（两段式）')

print('=== K117-9 交接说明 ===')
chk('K117-9a', '**当前建议（第 117 轮后）**' in cur['HO'] and '**（历史，第 116 轮后）**' in cur['HO'],
    '§七 新条目 + 116 条目改历史')
chk('K117-9b', '**（历史，第 116 轮后）**' not in bak['HO'], '116 条目在补丁前仍为「当前」（取证）')

print('=== K117-10 数字一致性（可复算）===')
chk('K117-10a', abs((1 / 3) / 0.30 - 1.1111111) < 1e-6, '(1/3)/0.30 = 1.1111')
import math
chk('K117-10b', abs(math.sqrt(2 * 399.18) - 28.26) < 0.02, '√(2×399.2) = %.2f ≈ 28.3σ' % math.sqrt(2 * 399.18))
chk('K117-10c', abs(7.481e-4 / 1.629e-6 - 459.2) < 0.5 and abs(9.7e-4 / 1.63e-6 - 595.1) < 1.0,
    '459.2（C-7 复现）与 595（~600×）可复算')
chk('K117-10d', abs(2.5416 / 1.2307 - 2.065) < 0.005, '剖面/条件 = 2.065（C1 案例）')

print('=== K117-11 符号与引用自查（新块含新希腊字母？）===')
GREEK = lambda t: set(c for c in t if '\u0370' <= c <= '\u03ff' or '\u1f00' <= c <= '\u1fff')
cur_all = ''.join([cur['ZH'], cur['EN']])
new_zh = [s for s in cur['ZH'].split('\n') if s.startswith('> ') and '第 117 轮' in s]
i = cur['ZH'].find('【v2.9 口径注（第 117 轮')
j = cur['ZH'].find('\n\n', i)
newblk = cur['ZH'][i:j if j > 0 else len(cur['ZH'])]
newg = GREEK(newblk); oldg = GREEK(bak['ZH'])
chk('K117-11a', newg <= oldg, '新块希腊字母 %s ⊆ 补丁前集合' % sorted(newg - oldg) if newg - oldg else '新块希腊字母 ⊆ 补丁前集合 ✓')
refs = set(re.findall(r'(?<![A-Za-z])(C-\d+|N-\d+|I-\d+)', newblk))
known = set(re.findall(r'(?<![A-Za-z])(C-\d+|N-\d+|I-\d+)', cur['LIST']))
chk('K117-11b', refs <= known, '新块引用的编号 %s' % sorted(refs))

print('=== K117-12 MEMO / MEMORY / 日志 / 技能 ===')
chk('K117-12a', os.path.exists(P['MEMO']), '备忘录存在')
mem_txt = rd(P['MEM']) if os.path.exists(P['MEM']) else ''
chk('K117-12b', '117' in mem_txt, 'MEMORY 含 117 记录（%d 字符）' % len(mem_txt))
chk('K117-12c', len(mem_txt) <= 3000, 'MEMORY ≤ 3000 字符（实际 %d）' % len(mem_txt))
log_txt = rd(P['LOG']) if os.path.exists(P['LOG']) else ''
chk('K117-12d', '第 117 轮' in log_txt, '当日日志含第 117 轮')
sk = rd(P['SKILL'])
chk('K117-12e', '114.' in sk and '115.' in sk, '技能含陷阱 114 / 115')

print('=== K117-13 旧报告横幅与生成器修复 ===')
rpt = rd(os.path.join(BASE, 'outputs', 'KerrEMRI波形与贝叶斯分析.md'))
rptb = rd(os.path.join(BASE, 'outputs', 'KerrEMRI波形与贝叶斯分析_备份_2026-10-04第117轮前.md'))
chk('K117-13a', '第 117 轮更正' in rpt and '第 117 轮更正' not in rptb, '报告横幅（两段式）')
gen = rd(os.path.join(BASE, 'outputs', '_kerr_report_html.py'))
chk('K117-13b', 'IMYT.YT' not in gen and '__file__' in gen, '生成器旧机路径已修')
chk('K117-13c', '第 117 轮更正' in rd(os.path.join(BASE, 'MAPS-Unified-Framework', 'docs', 'html', 'KerrEMRI波形与贝叶斯分析.html')),
    'docs/html 副本含横幅')

print('')
print('=' * 60)
print('通过 %d 项，失败 %d 项' % (OK, FAIL))
