# -*- coding: utf-8 -*-
"""第 132 轮：候选⑤「1/3 债务谱系」判定 —— 同源误并 ＋ 生日式检验
TH-1 … TH-16（含两段式；补丁后须 0 失败）
"""
import io, os, re
from mpmath import mp, mpf

mp.dps = 30
B   = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
DIR = os.path.join(B, '初始资料', '元宝对话_反物质与时间的哲学猜想', '检索批次')
P_ZH   = os.path.join(B, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md')
P_LP   = os.path.join(B, 'outputs', '工程期望清单.md')
P_TZ   = os.path.join(B, 'outputs', '起点对话研究方向检索台账.md')
P_MEMO = os.path.join(B, 'outputs', '候选5判定_1-3债务谱系_同源误并与生日式检验.md')
P_HO   = os.path.join(B, '环境交接说明.md')
P_LOG  = os.path.join(B, '.workbuddy', 'memory', '2026-10-05.md')
P_MEM  = os.path.join(B, '.workbuddy', 'memory', 'MEMORY.md')

OK = 0; FAIL = 0
def chk(tag, cond, msg):
    global OK, FAIL
    if cond: OK += 1; print('[OK] %s %s' % (tag, msg))
    else:    FAIL += 1; print('[XX] %s %s' % (tag, msg))

def rd(p): return io.open(p, encoding='utf-8').read()

# ============ A 对话侧取证（batch_29–31） ============
print('=== TH-A 对话侧「1/3 债务」===')
tf = rd(os.path.join(DIR, '提取_batch_29-31.md'))
b30 = rd(os.path.join(DIR, 'batch_30.md'))
b31 = rd(os.path.join(DIR, 'batch_31.md'))
chk('TH-1', ('1/3=孤子债务' in tf) and ('收敛' in tf),
    'B30-01：级数收敛 2/3 ⟹ 「1 = 孤子、1/3 = 孤子债务」')
chk('TH-2', ('9/12 - 8/12' in b30.replace(' ', '')) or ('9/12' in b30),
    'B30-06：3/4 − 2/3 = 1/12（债务在平均因子中的份额）')
chk('TH-3', ('(1/3)' in tf) and ('120' in tf) and ('AI 外推' in tf),
    'B30-21：(1/3)^120〔AI 外推，第 363 轮已自更正为 (l_P/R)²〕')

# ============ B 框架侧（N-42 三处） ============
print()
print('=== TH-B 框架侧三处 1/3（N-42 现役）===')
LP = rd(P_LP); ZH = rd(P_ZH)
chk('TH-4', '两两不相交' in LP, 'N-42 现役：三条链输入两两不相交，不得写「同源」')
chk('TH-5', ('5/12 − 1/12' in ZH) or ('5/12 - 1/12' in ZH),
    '论文含第 113 轮机制分解 `κ = +5/12 − 1/12 = 1/3`')
chk('TH-6', 'Φ(s)/Φ(0)' in LP, 'N-42 登记含 ① `Φ(s)/Φ(0) = 1 + (1/3)s² − …`')

# ============ C 减法检查 ============
print()
print('=== TH-C 减法检查（C-76 族）：1/3 是否独立给出 ===')
# 对话：2/3 是收敛值（已算），1/3 = 1 − 2/3（减法）
chk('TH-7', ('1/3=孤子债务' in tf) and ('2/3' in tf),
    '「1/3」由「1 − 2/3」给出（2/3 是收敛值）⟹ 减法，不是独立计算')

# ============ D 生日式检验（核心新算） ============
print()
print('=== TH-D 生日式检验：4 个独立小分母分数「至少一对重复」的概率 ===')
def p_birthday(m):
    m = mpf(m)
    return 1 - m * (m - 1) * (m - 2) * (m - 3) / m ** 4
for m in [11, 20, 40]:
    print('  格子数 m = %2d ⟹ P(至少一对相同) = %.4f' % (m, p_birthday(m)))
p11, p20, p40 = p_birthday(11), p_birthday(20), p_birthday(40)
chk('TH-8', (mpf('0.45') < p11) and (p11 < mpf('0.47')), 'm=11（分母 ≤6）⟹ P = %.4f' % p11)
chk('TH-9', (mpf('0.26') < p20) and (p20 < mpf('0.29')), 'm=20 ⟹ P = %.4f' % p20)
chk('TH-10', (mpf('0.13') < p40) and (p40 < mpf('0.15')), 'm=40（分母 ≤12）⟹ P = %.4f' % p40)

# ============ E 两段式登记（补丁后项） ============
print()
print('=== TH-E 登记（补丁后项在预跑时预期失败）===')
n49 = [s for s in LP.split('\n') if s.startswith('| **N-49** |')]
chk('TH-11', len(n49) == 1 and ('1/3' in n49[0]), '清单 N-49 行存在且唯一（补丁后）')
chk('TH-12', ('**49 条**' in LP) and ('N-49（第 132 轮' in LP), '负面计数 48→49（补丁后）')
T = rd(P_TZ)
chk('TH-13', ('N-49' in T) and ('1/3 债务' in T or '债务谱系' in T), '台账候选⑤已更新（补丁后）')
chk('TH-14', os.path.exists(P_MEMO), '备忘录存在（补丁后）')
chk('TH-15', '第 132 轮' in rd(P_HO), '交接说明含第 132 轮（补丁后）')
chk('TH-16', '第 132 轮' in rd(P_LOG), '日志含第 132 轮（补丁后）')
chk('TH-17', '进度 132' in rd(P_MEM), 'MEMORY 进度 132（补丁后）')

# ============ F 格式 ============
print()
print('=== TH-F 格式 ===')
def fmt_hits(t):
    L2 = t.split('\n')
    f1 = [i+1 for i, s in enumerate(L2) if s.strip().startswith(('，', ','))]
    f3 = [i+1 for i, s in enumerate(L2) if '\\|' in s and not s.lstrip().startswith('|')]
    return f1, f3
if os.path.exists(P_MEMO):
    f1, f3 = fmt_hits(rd(P_MEMO))
    chk('TH-18', len(f1) == 0 and len(f3) == 0, '备忘录格式：残片 %s 表外竖线 %s' % (f1[:3], f3[:3]))
else:
    chk('TH-18', False, '备忘录尚未生成（补丁后项）')

print()
print('=' * 56)
print('通过 %d 项，失败 %d 项' % (OK, FAIL))
