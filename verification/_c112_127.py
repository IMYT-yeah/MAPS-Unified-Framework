# -*- coding: utf-8 -*-
"""第 127 轮：候选①「−1/12 = 几何过滤残差」判定 —— 核验脚本
检查项：MIN-1 … MIN-18（含两段式；补丁后须 0 失败）
"""
import io, os, re
from mpmath import mp, mpf, zeta, exp

mp.dps = 30
B   = r'[WORKSPACE]'
DIR = os.path.join(B, '初始资料', '元宝对话_反物质与时间的哲学猜想', '检索批次')
P_ZH   = os.path.join(B, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md')
P_LP   = os.path.join(B, 'outputs', '项目台账.md')
P_LP_B = os.path.join(B, 'outputs', '项目台账_备份_2026-10-05第127轮前.md')
P_TZ   = os.path.join(B, 'outputs', '起点对话研究方向检索台账.md')
P_MEMO = os.path.join(B, 'outputs', '候选1判定_负十二分之一残差_对象消失与正规化依赖.md')
P_HO   = os.path.join(B, '环境说明.md')
P_LOG  = os.path.join(B, '.workbuddy', 'memory', '2026-10-05.md')

OK = 0; FAIL = 0
def chk(tag, cond, msg):
    global OK, FAIL
    if cond: OK += 1; print('[OK] %s %s' % (tag, msg))
    else:    FAIL += 1; print('[XX] %s %s' % (tag, msg))

def rd(p): return io.open(p, encoding='utf-8').read()

# ============ A 引文取证 ============
print('=== MIN-A 引文取证（对话原文 batch_10 / batch_30）===')
b10 = rd(os.path.join(DIR, 'batch_10.md'))
b30 = rd(os.path.join(DIR, 'batch_30.md'))
chk('MIN-1', '-1/12 在这个框架下有什么对应的地方吗' in b10, '第 97 轮用户原问句')
chk('MIN-2', ('完美湮灭' in b10) and ('正支几何' in b10) and ('有限残差' in b10),
    '第 97 轮主张句：总账→过滤→有限残差')
chk('MIN-3', '9/12-8/12' in b30.replace(' ', ''), '第 354 轮 3/4−2/3=1/12 算术句')

# ============ B 论文/清单现状 ============
print()
print('=== MIN-B 框架现状 ===')
Z = rd(P_ZH)
ctxs = []
for m in re.finditer(r'1/12', Z):
    ctxs.append(Z[max(0, m.start()-45):m.start()+45].replace('\n', '⏎'))
print('  论文「1/12」命中 %d 处：' % len(ctxs))
for c in ctxs: print('    …%s…' % c)
has_emri = any('5/12' in c for c in ctxs)
has_cnt  = any('失败' in c for c in ctxs)
has_sym4 = any('系数' in c for c in ctxs)
chk('MIN-4', (len(ctxs) == 3) and has_emri and has_cnt and has_sym4,
    '三处 = EMRI分解(%s)/计数(%s)/Sym4系数(%s)' % (has_emri, has_cnt, has_sym4))
chk('MIN-5', Z.count('正规化') == 0 and Z.count('卡西米尔') == 0 and Z.count('零点能') == 0 and Z.count('Lifshitz') == 0,
    '正规化/卡西米尔/零点能/Lifshitz 各 0 处')
chk('MIN-6', Z.count('Casimir') == 1, 'Casimir 1 处（仅作第五力尺度列举）')

# ============ C 数学核心 ============
print()
print('=== MIN-C 正规化家族数值演示 ===')
z1 = zeta(-1)
chk('MIN-7', abs(z1 + mpf(1)/12) < mpf('1e-25'), 'ζ(-1) = %s' % mp.nstr(z1, 12))

print('  指数阻尼：Σ n·e^(−εn) − 1/ε²')
last = None
for eps in [mpf('0.2'), mpf('0.1'), mpf('0.05'), mpf('0.02')]:
    s = exp(-eps)/(1-exp(-eps))**2
    r = s - 1/eps**2
    last = r
    print('    ε=%-5s 残差 = %s' % (mp.nstr(eps, 3), mp.nstr(r, 12)))
chk('MIN-8', abs(last + mpf(1)/12) < mpf('1e-5'), '指数正规化 → −1/12（ε=0.02 时偏差 %s）' % mp.nstr(last + mpf(1)/12, 4))

def gsum(eps):
    tot = mp.mpf(0); n = 0
    while True:
        n += 1
        t = eps*n
        if t > 12: break
        tot += n*exp(-t*t)
    return tot
print('  高斯阻尼：Σ n·e^(−(εn)²) − 1/(2ε²)')
gl = None
for eps in [mpf('0.2'), mpf('0.1'), mpf('0.05')]:
    s = gsum(eps)
    r = s - 1/(2*eps**2)
    gl = r
    print('    ε=%-5s 残差 = %s' % (mp.nstr(eps, 3), mp.nstr(r, 12)))
chk('MIN-9', abs(gl + mpf(1)/12) < mpf('1e-3'), '高斯正规化 → −1/12（ε=0.05 时偏差 %s）' % mp.nstr(gl + mpf(1)/12, 4))

print('  硬截断：Σ_{n≤N} n = N(N+1)/2 的「常数项」')
vals = []
for N in [10, 100, 1000, 10000]:
    v = mpf(N*(N+1))/2 - mpf(N)**2/2 - mpf(N)/2
    vals.append(v)
print('    N=10/100/1000/10000 → %s' % [str(v) for v in vals])
chk('MIN-10', all(v == 0 for v in vals), '硬截断无常数项（四个 N 精确 0）')
print('  ⟹ 对照：软化（ζ/指数/高斯）→ −1/12 ｜ 锐利（硬截断）→ 0')

# ============ D 登记一致性（两段式：补丁前预期失败） ============
print()
print('=== MIN-D 登记（补丁后项在预跑时预期失败）===')
L = rd(P_LP)
Lb = rd(P_LP_B)
cur_wo = '\n'.join(s for s in L.split('\n') if 'N-45' not in s)
chk('MIN-11', ('ζ(-1)' not in Lb) and ('正规化' not in Lb)
              and ('ζ(-1)' not in cur_wo) and ('正规化' not in cur_wo),
    '（两段式）补丁前清单无 −1/12 主题登记；补丁后新增字样仅限 N-45 行')

T = rd(P_TZ)
tz_ok = ('已判否' in T and 'N-45' in T)
chk('MIN-12', tz_ok, '台账候选①已更新为已判否/N-45（补丁后）')

n45 = [s for s in L.split('\n') if s.startswith('| **N-45** |')]
chk('MIN-13', len(n45) == 1 and ('1/12' in n45[0] or '−1/12' in n45[0]),
    '清单 N-45 行存在且唯一（补丁后）')
chk('MIN-14', '**45 条**' in L and 'N-45（第 127 轮' in L, '负面计数 44→45（补丁后）')

chk('MIN-15', os.path.exists(P_MEMO), '备忘录存在（补丁后）')
H = rd(P_HO)
chk('MIN-16', ('第 127 轮' in H) and ('第 126 轮' in H), '交接说明含第 126/127 轮（补丁后）')
G = rd(P_LOG)
chk('MIN-17', '第 127 轮' in G, '日志含第 127 轮（补丁后）')

# ============ E 格式 ============
print()
print('=== MIN-E 格式 ===')
def fmt_hits(t):
    L2 = t.split('\n')
    f1 = [i+1 for i, s in enumerate(L2) if s.strip().startswith(('，', ','))]
    f3 = [i+1 for i, s in enumerate(L2) if '\\|' in s and not s.lstrip().startswith('|')]
    return f1, f3
if os.path.exists(P_MEMO):
    f1, f3 = fmt_hits(rd(P_MEMO))
    chk('MIN-18', len(f1) == 0 and len(f3) == 0, '备忘录格式：残片 %s 表外竖线 %s' % (f1[:3], f3[:3]))
else:
    chk('MIN-18', False, '备忘录尚未生成（补丁后项）')

print()
print('=' * 56)
print('通过 %d 项，失败 %d 项' % (OK, FAIL))
