# -*- coding: utf-8 -*-
"""第 129 轮：候选②·补强 —— 词形完整性 ＋ 双载子封闭（引力／Φ）＋ 外部清单登记
检查项：PE-1 … PE-14（含两段式；补丁后须 0 失败）
"""
import io, os, re, glob
from mpmath import mp, mpf, exp, log10

mp.dps = 30
B   = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
DIR = os.path.join(B, '初始资料', '元宝对话_反物质与时间的哲学猜想', '检索批次')
P_ZH   = os.path.join(B, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md')
P_LP   = os.path.join(B, 'outputs', '工程期望清单.md')
P_TZ   = os.path.join(B, 'outputs', '起点对话研究方向检索台账.md')
P_MEMO = os.path.join(B, 'outputs', '候选2判定_质子衰变的环境依赖_不可算与量级关闭.md')
P_EI   = os.path.join(B, 'outputs', '外部输入清单_可接入的活问题与渠道_2026-10.md')
P_LOG  = os.path.join(B, '.workbuddy', 'memory', '2026-10-05.md')
P_MEM  = os.path.join(B, '.workbuddy', 'memory', 'MEMORY.md')

OK = 0; FAIL = 0
def chk(tag, cond, msg):
    global OK, FAIL
    if cond: OK += 1; print('[OK] %s %s' % (tag, msg))
    else:    FAIL += 1; print('[XX] %s %s' % (tag, msg))

def rd(p): return io.open(p, encoding='utf-8').read()

# ============ A 词形完整性 ============
print('=== PE-A 词形完整性核查（全 36 批）===')
bb = {}
for f in glob.glob(os.path.join(DIR, 'batch_*.md')):
    key = os.path.basename(f).replace('batch_', '').replace('.md', '')
    bb[key] = io.open(f, encoding='utf-8').read()
c_pd = {k: v.count('质子衰变') for k, v in bb.items() if v.count('质子衰变')}
print('  质子衰变分布: %s' % c_pd)
chk('PE-1', set(c_pd.keys()) == {'01', '02', '03'}
            and all(v.count('核子衰变') == 0 and v.count('重子衰变') == 0 for v in bb.values()),
    '「质子衰变」仅 01–03（%s）；核子/重子衰变 全 0' % c_pd)

c_b = {k: v.count('β 衰变') for k, v in bb.items() if v.count('β 衰变')}
print('  β 衰变分布: %s' % c_b)
b7 = bb['07']
chk('PE-2', set(c_b.keys()) == {'07'} and ('核废料加速衰变' in b7 or '宏观超表面做不到' in b7),
    '「β 衰变」仅 07（%s）；原句含「核废料加速衰变／宏观超表面做不到」' % c_b)

# ============ B 载子封闭（核心） ============
print()
print('=== PE-B 双载子封闭 ===')
# 载子 A：引力/通量密度
k_fw    = exp(mpf('0.5'))
k_allow = mpf('2.4e34') / mpf('1.5e18')
gap_A   = k_allow / k_fw
print('  载子 A（引力）: K_fw = %.4f ; K_allow = %.3e ; 缺口 = %.3e（%.1f dex）'
      % (k_fw, k_allow, gap_A, log10(gap_A)))
chk('PE-3', abs(log10(gap_A) - mpf('16.0')) < mpf('0.2'),
    '载子 A 缺口 = %.2f 个数量级（复算自 128 轮）' % log10(gap_A))

# 载子 B：Φ 标量（力程口径）
R_earth = mpf('6.371e6')       # m（地球半径）
lam_c   = mpf('47.1e-6')       # m（存活的 (c) 档力程）
ratio   = R_earth / lam_c
print('  载子 B（Φ·力程）: R⊕/λ_c = %.4e（%.2f dex）; 指数压制 e^{−R⊕/λ} = e^{−%.2e}'
      % (ratio, log10(ratio), ratio))
chk('PE-4', (mpf('1.3e11') < ratio) and (ratio < mpf('1.4e11'))
            and (mpf('11.0') < log10(ratio)) and (log10(ratio) < mpf('11.2')),
    'R⊕/λ_c = %.3e（%.2f dex）' % (ratio, log10(ratio)))

# 载子 B：质量口径（一致性）
hbarc = mpf('1.9732698e-7')    # eV·m
m_req = hbarc / R_earth
m_fw  = mpf('4.1894e-3')       # eV（= 4.1894 meV，(c) 档）
ratio2 = m_fw / m_req
print('  载子 B（Φ·质量）: m_req = %.3e eV ; m_fw = %.3e eV ; 比值 = %.3e（%.2f dex）'
      % (m_req, m_fw, ratio2, log10(ratio2)))
chk('PE-5', abs(ratio2 / ratio - 1) < mpf('1e-4'),
    '质量口径与力程口径一致（比值 %.3e；相对差 %.1e = 四位有效数字互推的舍入）' % (ratio2, abs(ratio2 / ratio - 1)))

# 二难：框架自己的第五力窗口要求短程
LP = rd(P_LP)
chk('PE-6', '65–90 μm' in LP,
    '框架第五力窗口「λ ≲ 65–90 μm」在清单（短程需求 ⟹ 与长程二难）')
chk('PE-7', ('四力' in LP) and ('给不出' in LP),
    '「四力位无空位／框架给不出 g」的既有登记在清单（无第三载子的依据）')

# ============ C 两段式登记（补丁后项） ============
print()
print('=== PE-C 登记（补丁后项在预跑时预期失败）===')
MEMO = rd(P_MEMO)
chk('PE-8', ('载子封闭' in MEMO) or ('双载子' in MEMO), '备忘录 §补强存在（补丁后）')
n46 = [s for s in LP.split('\n') if s.startswith('| **N-46** |')]
chk('PE-9', len(n46) == 1 and ('第 129 轮' in n46[0]), '清单 N-46 行含补强句（补丁后）')
EI = rd(P_EI)
chk('PE-10', ('Davoudiasl' in EI) or ('2410.19045' in EI), '外部清单含 B4 新条目（补丁后）')
chk('PE-11', '第 129 轮' in rd(P_LOG), '日志含第 129 轮（补丁后）')
chk('PE-12', '进度 129' in rd(P_MEM), 'MEMORY 进度 129（补丁后）')
chk('PE-13', ('载子封闭' in rd(P_TZ)) or ('第 129 轮' in rd(P_TZ)), '台账含补强登记（补丁后）')

# ============ D 格式 ============
print()
print('=== PE-D 格式 ===')
def fmt_hits(t):
    L2 = t.split('\n')
    f1 = [i+1 for i, s in enumerate(L2) if s.strip().startswith(('，', ','))]
    f3 = [i+1 for i, s in enumerate(L2) if '\\|' in s and not s.lstrip().startswith('|')]
    return f1, f3
f1, f3 = fmt_hits(MEMO)
chk('PE-14', len(f1) == 0 and len(f3) == 0, '备忘录格式：残片 %s 表外竖线 %s' % (f1[:3], f3[:3]))

print()
print('=' * 56)
print('通过 %d 项，失败 %d 项' % (OK, FAIL))
