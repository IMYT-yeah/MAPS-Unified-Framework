# -*- coding: utf-8 -*-
"""第 133 轮：候选⑥ 希尔伯特第六问题补强 —— 文献级对账 ＋ 模型嵌入缺口（I-29）
H6-1 … H6-14（含两段式）
"""
import io, os, re
from mpmath import mp, mpf

mp.dps = 30
B   = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
P_ZH   = os.path.join(B, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md')
P_EN   = os.path.join(B, 'outputs', 'Paper_MatterAntimatterPairStorm_v2.9_EN.md')
P_LP   = os.path.join(B, 'outputs', '工程期望清单.md')
P_TZ   = os.path.join(B, 'outputs', '起点对话研究方向检索台账.md')
P_MEMO = os.path.join(B, 'outputs', '候选6结项_希尔伯特第六问题补强_文献对账与模型嵌入缺口.md')
P_HO   = os.path.join(B, '环境交接说明.md')
P_LOG  = os.path.join(B, '.workbuddy', 'memory', '2026-10-06.md')
P_MEM  = os.path.join(B, '.workbuddy', 'memory', 'MEMORY.md')

OK = 0; FAIL = 0
def chk(tag, cond, msg):
    global OK, FAIL
    if cond: OK += 1; print('[OK] %s %s' % (tag, msg))
    else:    FAIL += 1; print('[XX] %s %s' % (tag, msg))

def rd(p): return io.open(p, encoding='utf-8').read()

ZH = rd(P_ZH); EN = rd(P_EN); LP = rd(P_LP)
ZH_b = rd(os.path.join(B, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-06第133轮前.md'))
EN_b = rd(os.path.join(B, 'outputs', 'Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-06第133轮前.md'))
zh_wo = '\n'.join(s for s in ZH.split('\n') if '第 133 轮' not in s)
en_wo = '\n'.join(s for s in EN.split('\n') if 'round 133' not in s)

# ============ A 框架现状 ============
print('=== H6-A 框架现状 ===')
chk('H6-1', ('| **I-12** |' in LP) and ('Chapman–Enskog' in LP), 'I-12（★ 待补强条目）现役')
chk('H6-2', ('① 从湮灭动力学证明' in ZH) and ('连续极限收敛性' in ZH), 'ZH §3.4 三条【待验证】原文')
chk('H6-3', '邓煜-Hani-马骁硬球链条' in ZH, 'ZH §4 链条第 4 环已引 DHM 硬球链条')
chk('H6-4', all(k not in ZH_b for k in ['欧拉方程', 'Navier', 'Enskog'])
            and all(k not in zh_wo for k in ['欧拉方程', 'Navier', 'Enskog']),
    '（两段式）改前/改后（排除本轮注）论文均缺「玻尔兹曼 → 流体」的 2025 外部进展')
chk('H6-5', all(EN_b.count(k) == 0 for k in ['Lanford', 'hard sphere', 'molecular chaos', 'Chapman', 'Navier'])
            and all(k not in en_wo for k in ['Lanford', 'hard sphere', 'molecular chaos', 'Chapman', 'Navier']),
    '（两段式）★EN 稿缺链条内容（改前／改后排除本轮注均成立）')

# ============ B 尺度分离与稀薄性前提 ============
print()
print('=== H6-B 尺度分离 vs 稀薄性前提 ===')
tP = mpf('5.391247e-44'); lP = mpf('1.616255e-35')
tau_relax = 4 * tP
ratio_t = mpf(1) / tau_relax
print('  τ_relax = 4 t_P = %.4e s ；1 s / τ_relax = %.3e' % (tau_relax, ratio_t))
Kn = lP / mpf(1)
print('  Kn（实验室 L = 1 m）= l_P/L = %.3e ⟹ ≪ 1（连续极限的尺度分离 ✅）' % Kn)
thin = lP / lP
print('  ⚠️ 稀薄性前提：衬底 λ_mfp / 格距 = l_P / l_P = %.1f ⟹ DHM 的「λ_mfp ≫ 间距」**不满足**' % thin)
chk('H6-6', (mpf('4.5e42') < ratio_t) and (ratio_t < mpf('4.8e42')), '宏观/微观时间分离 = %.3e' % ratio_t)
chk('H6-7', (mpf('1.5e-35') < Kn) and (Kn < mpf('1.7e-35')), 'Kn = %.3e（尺度分离满足）' % Kn)
chk('H6-8', thin == 1, '衬底 λ_mfp/格距 = 1（稀薄前提不满足，结构性缺口）')

# ============ C 两段式登记 ============
print()
print('=== H6-C 登记（补丁后项在预跑时预期失败）===')
i29 = [s for s in LP.split('\n') if s.startswith('| **I-29** |')]
chk('H6-9', len(i29) == 1 and ('模型嵌入' in i29[0]), '清单 I-29 行存在且唯一（补丁后）')
i12 = [s for s in LP.split('\n') if s.startswith('| **I-12** |')]
chk('H6-10', len(i12) == 1 and ('第 133 轮' in i12[0]), 'I-12 行含第 133 轮更新（补丁后）')
chk('H6-11', '| **C-88** |' in LP, 'C-88（EN 不同步登记）存在（补丁后）')
chk('H6-12', ('第 133 轮' in ZH) and ('round 133' in EN), '论文中英各含第 133 轮注（补丁后）')
chk('H6-13', os.path.exists(P_MEMO), '备忘录存在（补丁后）')
chk('H6-14', '第 133 轮' in rd(P_HO), '交接说明含第 133 轮（补丁后）')
chk('H6-15', '第 133 轮' in rd(P_LOG), '日志含第 133 轮（补丁后）')
chk('H6-16', '进度 133' in rd(P_MEM), 'MEMORY 进度 133（补丁后）')

# ============ D 格式 ============
print()
print('=== H6-D 格式 ===')
def fmt_hits(t):
    L2 = t.split('\n')
    f1 = [i+1 for i, s in enumerate(L2) if s.strip().startswith(('，', ','))]
    f3 = [i+1 for i, s in enumerate(L2) if '\\|' in s and not s.lstrip().startswith('|')]
    return f1, f3
if os.path.exists(P_MEMO):
    f1, f3 = fmt_hits(rd(P_MEMO))
    chk('H6-17', len(f1) == 0 and len(f3) == 0, '备忘录格式：残片 %s 表外竖线 %s' % (f1[:3], f3[:3]))
else:
    chk('H6-17', False, '备忘录尚未生成（补丁后项）')

print()
print('=' * 56)
print('通过 %d 项，失败 %d 项' % (OK, FAIL))
