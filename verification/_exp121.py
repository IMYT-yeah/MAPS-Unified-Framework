# -*- coding: utf-8 -*-
"""第 121 轮核验脚本：实验线 x3 —— 判据精确化（C-85）＋ 候选装置核对。

E121-1…E121-8  数学：两锚点幂律族、判死 (c) 所需改进、三档（边缘/干净/裕度）
E121-9…E121-16 文档：论文中英新块、清单、交接、MEMORY、日志、技能、备忘录/材料包、格式
两段式：凡「本轮修好」的检查，均读 2026-10-04第121轮前 备份做取证。
"""
import io, os, math

BASE = r'[WORKSPACE]'
H = os.path.join(BASE, 'MAPS-Unified-Framework', 'paper', 'history')
OUT = os.path.join(BASE, 'outputs')
MEM = os.path.join(BASE, '.workbuddy', 'memory')
工作流说明 = r'[WORKFLOW]\工作流说明'

def rd(p):
    return io.open(p, encoding='utf-8').read()

OK = 0
FAIL = 0
def chk(tag, cond, msg):
    global OK, FAIL
    if cond:
        OK += 1
        print('  [OK] %s  %s' % (tag, msg))
    else:
        FAIL += 1
        print('  [XX] %s  %s' % (tag, msg))

# ============ 数学部分 ============
print('=== E121-1…E121-8：两锚点幂律族与判据精确化 ===')
TAN, LEE, LAMC = 48.0, 38.6, 47.1
TH = 1.0 / 3.0
def p_of(lam1, a1, lam2, a2):
    return math.log(a1 / a2) / math.log(lam2 / lam1)

chains = {
    'A': (TAN, 1.0, 70.0, TH),
    'B': (TAN, 1.0, 1000.0, 1e-3),
    'C': (TAN, 1.0, 2000.0, 1e-3),
    'D': (LEE, 1.0, 1000.0, 1e-3),
}
P = {k: p_of(a, b, c, d) for k, (a, b, c, d) in chains.items()}
exp_p = {'A': 2.91, 'B': 2.27, 'C': 1.85, 'D': 2.12}
for k in 'ABCD':
    chk('E121-1' + k, abs(P[k] - exp_p[k]) < 0.01,
        '%s 链 p = %.4f（第 120 轮记 %.2f）' % (k, P[k], exp_p[k]))

def amax(k, lam):
    a0 = chains[k][0]
    return (lam / a0) ** (-P[k])

AM = {k: amax(k, LAMC) for k in 'ABCD'}
vmin, vmax = min(AM.values()), max(AM.values())
chk('E121-2', abs(vmax - 1.0566) < 0.003 and abs(vmin - 0.655) < 0.003,
    'α_max(47.1 μm) = [%.3f, %.3f]（第 120 轮 [0.655, 1.057]）' % (vmin, vmax))

F_clean = {k: AM[k] / TH for k in 'ABCD'}
fc_min, fc_max = min(F_clean.values()), max(F_clean.values())
chk('E121-3', abs(fc_min - 1.97) < 0.01 and abs(fc_max - 3.17) < 0.01,
    '判死 (c) 所需改进 = ×%.2f（D）– ×%.2f（A）⟹ 区间 [1.97, 3.17]' % (fc_min, fc_max))

F_marg = {k: AM[k] / (TH / 2.0) for k in 'ABCD'}
fm_min, fm_max = min(F_marg.values()), max(F_marg.values())
chk('E121-4', abs(fm_min - 3.93) < 0.02 and abs(fm_max - 6.34) < 0.02,
    '2× 裕度所需改进 = ×%.2f（D）– ×%.2f（A）' % (fm_min, fm_max))
chk('E121-4b', 6.3 < fm_max < 6.4,
    '×6.3 不足（< %.4f）⟹ 稳健档取 ×6.4（= %.2f 的四链最严值上取整）' % (fm_max, 6.4))

E3 = {k: AM[k] / 3.0 for k in 'ABCD'}
e3_min, e3_max = min(E3.values()), max(E3.values())
chk('E121-5', e3_min < TH < e3_max,
    '×3 后新界 = [%.3f, %.3f] 跨过 1/3 ⟹「×3 = 到达判定边缘」（不是干净判定）' % (e3_min, e3_max))

CL = {k: AM[k] / 3.2 for k in 'ABCD'}
chk('E121-6', all(v < TH for v in CL.values()),
    '×3.2 后新界 = [%.3f, %.3f] 全部 < 1/3 ⟹ 四链干净排除' % (min(CL.values()), max(CL.values())))

def lam_star(k, F):
    # 解 amax(λ)/F = 1/3 ⟹ λ = a0·(F/3)^(−1/p)
    a0 = chains[k][0]
    return a0 * (F / 3.0) ** (-1.0 / P[k])

LS32 = {k: lam_star(k, 3.2) for k in 'ABCD'}
chk('E121-7', all(v < LAMC for v in LS32.values()),
    '×3.2 把 α=1/3 边界推到 λ* = %.1f–%.1f μm（全部 ≤ 47.1）' % (min(LS32.values()), max(LS32.values())))
LS3 = {k: lam_star(k, 3.0) for k in 'ABCD'}
chk('E121-7b', all(abs(LS3[k] - chains[k][0]) < 1e-9 for k in 'ABCD'),
    '×3 把 α=1/3 边界恰好推到旧的 α=1 锚点（48/48/48/38.6）⟹ 边界与锚点重合（边缘的量级来源）')

MG = {k: AM[k] / 6.4 for k in 'ABCD'}
chk('E121-8', all(v < TH / 2.0 for v in MG.values()),
    '×6.4 后新界 = [%.4f, %.4f] 全部 < 1/6 ⟹ 2× 裕度达成' % (min(MG.values()), max(MG.values())))

# ============ 文档部分 ============
print('')
print('=== E121-9…E121-16：文档与登记 ===')
ZH = rd(os.path.join(OUT, '论文初稿_正反物质对风暴统一框架_v2.9.md'))
EN = rd(os.path.join(OUT, 'Paper_MatterAntimatterPairStorm_v2.9_EN.md'))
ZHp = rd(os.path.join(H, '论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-04第121轮前.md'))
ENp = rd(os.path.join(H, 'Paper_v2.9_EN_备份_2026-10-04第121轮前.md'))

chk('E121-9zh', ('第 121 轮' not in ZHp) and ('第 121 轮' in ZH),
    'ZH 论文：补丁前无 / 补丁后有「第 121 轮」块（两段式）')
chk('E121-9en', ('round 121' not in ENp.lower()) and ('round 121' in EN.lower()),
    'EN 论文：补丁前无 / 补丁后有 round 121 块（两段式）')

for tag, txt in (('zh', ZH), ('en', EN)):
    need = ['×3.2', '×6.4', '40–800', '2.0×10⁻¹⁷', 'I-27']
    if tag == 'zh':
        need += ['38.6', '48', 'C-85', '实验线']
    ok = all(s in txt for s in need)
    miss = [s for s in need if s not in txt]
    chk('E121-10' + tag, ok, '%s 块关键串齐全（缺：%s）' % ('ZH' if tag == 'zh' else 'EN', miss))

LP = rd(os.path.join(OUT, '项目台账.md'))
LPp = rd(os.path.join(OUT, '项目台账_备份_2026-10-04第121轮前.md'))
chk('E121-11a', ('| **第 121 轮**' not in LPp) and ('| **第 121 轮**' in LP),
    '清单：补丁前无 / 补丁后有「第 121 轮」零表行（两段式）')
chk('E121-11b', ('| **C-85** |' not in LPp) and ('| **C-85** |' in LP),
    '清单：C-85 行已插入')
chk('E121-11c', ('| **I-27** |' not in LPp) and ('| **I-27** |' in LP),
    '清单：I-27 行已插入')

LL = LP.split('\n')
i84 = [i for i, s in enumerate(LL) if s.startswith('| **C-84** |')]
i85 = [i for i, s in enumerate(LL) if s.startswith('| **C-85** |')]
chk('E121-11d', len(i84) == 1 and len(i85) == 1 and i85[0] == i84[0] + 1,
    'C-85 紧跟 C-84 之后（%s -> %s）' % (i84, i85))
i26 = [i for i, s in enumerate(LL) if s.startswith('| **I-26** |')]
i27 = [i for i, s in enumerate(LL) if s.startswith('| **I-27** |')]
chk('E121-11e', len(i26) == 1 and len(i27) == 1 and i27[0] == i26[0] + 1,
    'I-27 紧跟 I-26 之后（%s -> %s）' % (i26, i27))

chk('E121-12a', ('**撤回 / 更正** | **83 条**' in LPp) and ('**撤回 / 更正** | **84 条**' in LP),
    '计数：撤回/更正 83 → 84（两段式）')
chk('E121-12b', 'I-27' in LP and '第 99 轮后新登记的 I-23…I-27' in LP,
    'I 计数行已提及 I-27')

HO = rd(os.path.join(BASE, '环境说明.md'))
chk('E121-13a', ('当前建议（第 121 轮后）' in HO) and ('（历史，第 120 轮后）' in HO),
    '交接说明 §七：新条目在顶 ＋ 第 120 轮条目降为历史')

MEMTXT = rd(os.path.join(MEM, 'MEMORY.md'))
chk('E121-13b', ('121' in MEMTXT) and ('C-85' in MEMTXT) and len(MEMTXT) <= 3000,
    'MEMORY：进度/条目更新且长度 %d ≤ 3000' % len(MEMTXT))

LOG = rd(os.path.join(MEM, '2026-10-04.md'))
chk('E121-13c', '第 121 轮' in LOG and '实验线' in LOG,
    '日志：含「第 121 轮 · 实验线」段')

SK = rd(工作流说明)
chk('E121-14a', '117.' in SK and '第 121 轮' in SK,
    '技能：陷阱 117 ＋ §5.0 第 121 轮修定已入')

MEMO = os.path.join(OUT, '第五力实验线_x3判据精确化与候选装置核对.md')
PKG = os.path.join(OUT, '第五力实验线材料包_给短程引力实验组.md')
chk('E121-15a', os.path.exists(MEMO) and os.path.exists(PKG), '备忘录与材料包文件存在')
MT = rd(MEMO) if os.path.exists(MEMO) else ''
PT = rd(PKG) if os.path.exists(PKG) else ''
chk('E121-15b', all(s in MT for s in ['×3.2', '×6.4', '40–800', '2.0×10⁻¹⁷', 'I-27', '38.6']),
    '备忘录关键串齐全')
chk('E121-15c', all(s in PT for s in ['×3.2', '×6.4', '0.3', '未送出', '退出']),
    '材料包关键串齐全（含「未送出」与退出机制）')

# 格式自查（两段式：与备份比，无新增残片/表外竖线）
def fmt_hits(lines):
    b1 = [i + 1 for i, s in enumerate(lines) if s.strip().startswith(('，', ','))]
    b3 = [i + 1 for i, s in enumerate(lines) if '\\|' in s and not s.lstrip().startswith('|')]
    return b1, b3
zb1, zb3 = fmt_hits(ZH.split('\n'))
zp1, zp3 = fmt_hits(ZHp.split('\n'))
eb1, eb3 = fmt_hits(EN.split('\n'))
ep1, ep3 = fmt_hits(ENp.split('\n'))
chk('E121-16a', len(zb1) == len(zp1) and len(zb3) == len(zp3) and len(eb1) == len(ep1) and len(eb3) == len(ep3),
    '格式（两段式）：残片/表外竖线 ZH %d/%d（前 %d/%d）、EN %d/%d（前 %d/%d）' %
    (len(zb1), len(zb3), len(zp1), len(zp3), len(eb1), len(eb3), len(ep1), len(ep3)))
# 新块内不得有空行：扫描 121 块
def block_check(text, marker):
    L = text.split('\n')
    i0 = [i for i, s in enumerate(L) if marker in s]
    if len(i0) != 1:
        return None
    i = i0[0]
    j = i
    while j < len(L) and L[j].startswith('>'):
        j += 1
    return L[i:j]
blk = block_check(ZH, '【v2.9 补充（第 121 轮')
chk('E121-16b', blk is not None and all(s.startswith('>') for s in blk) and len(blk) >= 6,
    'ZH 121 块 %s 行全为「> 」且无空行' % (len(blk) if blk else 'None'))
blk2 = block_check(EN, 'supplement (round 121')
chk('E121-16c', blk2 is not None and all(s.startswith('>') for s in blk2) and len(blk2) >= 6,
    'EN 121 块 %s 行全为「> 」且无空行' % (len(blk2) if blk2 else 'None'))

print('')
print('=' * 60)
print('通过 %d 项，失败 %d 项' % (OK, FAIL))
