# -*- coding: utf-8 -*-
"""第 128 轮：候选②「质子衰变的环境依赖」判定 —— 核验脚本
检查项：PD-1 … PD-16（含两段式；补丁后须 0 失败）
外部锚：Davoudiasl & Denton, PRD 111, 035026 (2025), arXiv:2410.19045
        —— 质子寿命可短 ~15 个数量级（天体允许窗口）；SK 下限 τ(p→e⁺π⁰) > 2.4×10³⁴ yr
"""
import io, os, re
from mpmath import mp, mpf, exp, log, log10

mp.dps = 30
B   = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
DIR = os.path.join(B, '初始资料', '元宝对话_反物质与时间的哲学猜想', '检索批次')
P_ZH   = os.path.join(B, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md')
P_LP   = os.path.join(B, 'outputs', '工程期望清单.md')
P_LP_B = os.path.join(B, 'outputs', '工程期望清单_备份_2026-10-05第128轮前.md')
P_TZ   = os.path.join(B, 'outputs', '起点对话研究方向检索台账.md')
P_MEMO = os.path.join(B, 'outputs', '候选2判定_质子衰变的环境依赖_不可算与量级关闭.md')
P_HO   = os.path.join(B, '环境交接说明.md')
P_LOG  = os.path.join(B, '.workbuddy', 'memory', '2026-10-05.md')

OK = 0; FAIL = 0
def chk(tag, cond, msg):
    global OK, FAIL
    if cond: OK += 1; print('[OK] %s %s' % (tag, msg))
    else:    FAIL += 1; print('[XX] %s %s' % (tag, msg))

def rd(p): return io.open(p, encoding='utf-8').read()

# ============ A 对话引文 ============
print('=== PD-A 对话原文取证 ===')
b1 = rd(os.path.join(DIR, 'batch_01.md'))
b2 = rd(os.path.join(DIR, 'batch_02.md'))
chk('PD-1', ('质子衰变率可能微升' in b1) and ('理论上可算' in b1),
    '第 14 轮原句：「质子衰变率可能微升……理论上可算」（元宝）')
chk('PD-2', ('微升' in b2) and ('强引力场' in b2),
    '第 17–18 轮：「unique prediction……强引力场下的微升」')

# ============ B 体系现状 ============
print()
print('=== PD-B 体系现状（未入体系 = 无需论文改动）===')
Z = rd(P_ZH); L = rd(P_LP)
Lb = rd(P_LP_B)
cur_wo = '\n'.join(s for s in L.split('\n') if 'N-46' not in s)
chk('PD-3', (Z.count('质子衰变') == 0) and (Z.count('衰变率') == 0) and (Lb.count('质子衰变') == 0)
            and ('质子衰变' not in cur_wo),
    '（两段式）改前论文/清单「质子衰变 / 衰变率」各 0 处；改后新增字样仅限 N-46 行')

# ============ C 量级关闭计算（本轮核心） ============
print()
print('=== PD-C 量级关闭（K_fw vs K_allow）===')
lab   = mpf('2.4e34')          # SK 下限（p→e⁺π⁰，90% CL；PRD 111 引）
earth = mpf('2.0e18')          # 地球铁核热量约束（Davoudiasl–Denton 2025）
ns    = mpf('1.5e18')          # 中子星 PSR J2144−3933 热量约束
cmb   = mpf('2.0e17')          # CMB 相关约束
k_allow = lab / min(earth, ns)
print('  SK 实验室下限            τ > %.1e yr' % lab)
print('  天体探针：地球铁核 %.1e / 中子星 %.1e / CMB %.1e' % (earth, ns, cmb))
print('  ⟹ K_allow = %.3e（约 %.1f 个数量级）' % (k_allow, log10(k_allow)))
k_fw_min = exp(mpf('0.1'))     # 中子星致密度 C=GM/Rc² 低端
k_fw_max = exp(mpf('0.5'))     # 高端
print('  框架最有利定标：K_fw = e^{C}，C∈[0.1,0.5] ⟹ [%.4f, %.4f]' % (k_fw_min, k_fw_max))
gap = k_allow / k_fw_max
print('  ⟹ 缺口 = K_allow / K_fw_max = %.3e（约 %.1f 个数量级）' % (gap, log10(gap)))
n_lo = log(k_allow)/mpf('0.5'); n_hi = log(k_allow)/mpf('0.1')
print('  ⟹ 若要跨过窗口需 Γ∝ρ^n：n ∈ [%.1f, %.1f]（无机制）' % (n_lo, n_hi))
chk('PD-4', gap > mpf('1e15'), '缺口 > 10¹⁵（约 %.1f 个数量级）' % log10(gap))
chk('PD-5', (mpf(1.6) < k_fw_max) and (k_fw_max < mpf(1.65)), 'K_fw 上界 = e^0.5 ≈ 1.6487')
chk('PD-6', (mpf(70) < n_lo) and (n_lo < mpf(80)) and (mpf(360) < n_hi) and (n_hi < mpf(380)),
    '幂指数需求 n ∈ [%.1f, %.1f]' % (n_lo, n_hi))

# ============ D 两段式登记（补丁后项，预跑预期失败） ============
print()
print('=== PD-D 登记（补丁后项在预跑时预期失败）===')
n46 = [s for s in L.split('\n') if s.startswith('| **N-46** |')]
chk('PD-7', len(n46) == 1 and ('质子衰变' in n46[0]),
    '清单 N-46 行存在且唯一（补丁后）')
chk('PD-8', ('**46 条**' in L) and ('N-46（第 128 轮' in L), '负面计数 45→46（补丁后）')
T = rd(P_TZ)
chk('PD-9', ('N-46' in T) and ('质子衰变' in T), '台账候选②已更新（含 N-46）（补丁后）')
chk('PD-10', os.path.exists(P_MEMO), '备忘录存在（补丁后）')
H = rd(P_HO)
chk('PD-11', '第 128 轮' in H, '交接说明含第 128 轮（补丁后）')
G = rd(P_LOG)
chk('PD-12', '第 128 轮' in G, '日志含第 128 轮（补丁后）')
M = rd(os.path.join(B, '.workbuddy', 'memory', 'MEMORY.md'))
chk('PD-13', ('进度 128' in M) and ('候选②' in M), 'MEMORY 进度 128＋候选②登记（补丁后）')

# ============ E 格式 ============
print()
print('=== PD-E 格式 ===')
def fmt_hits(t):
    L2 = t.split('\n')
    f1 = [i+1 for i, s in enumerate(L2) if s.strip().startswith(('，', ','))]
    f3 = [i+1 for i, s in enumerate(L2) if '\\|' in s and not s.lstrip().startswith('|')]
    return f1, f3
if os.path.exists(P_MEMO):
    f1, f3 = fmt_hits(rd(P_MEMO))
    chk('PD-14', len(f1) == 0 and len(f3) == 0, '备忘录格式：残片 %s 表外竖线 %s' % (f1[:3], f3[:3]))
else:
    chk('PD-14', False, '备忘录尚未生成（补丁后项）')

# 补充：台账候选②行现状（信息项）
tl = [s for s in T.split('\n') if '质子衰变环境依赖' in s]
print()
print('台账候选②相关行: %d 条' % len(tl))
for s in tl[:2]: print('  ', s[:150])

print()
print('=' * 56)
print('通过 %d 项，失败 %d 项' % (OK, FAIL))
