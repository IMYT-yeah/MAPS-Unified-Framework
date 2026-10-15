# -*- coding: utf-8 -*-
"""第 130 轮：候选③「纠缠保真度 ∝ 物质分布」判定 —— 核验脚本
EB-1 … EB-15（含两段式；补丁后须 0 失败）
"""
import io, os, re
from mpmath import mp, mpf, pi, log10, exp

mp.dps = 30
B   = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
DIR = os.path.join(B, '初始资料', '元宝对话_反物质与时间的哲学猜想', '检索批次')
P_ZH   = os.path.join(B, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md')
P_LP   = os.path.join(B, 'outputs', '工程期望清单.md')
P_TZ   = os.path.join(B, 'outputs', '起点对话研究方向检索台账.md')
P_MEMO = os.path.join(B, 'outputs', '候选3判定_纠缠保真度与物质分布_对话自撤与双向失控.md')
P_HO   = os.path.join(B, '环境交接说明.md')
P_LOG  = os.path.join(B, '.workbuddy', 'memory', '2026-10-05.md')
P_MEM  = os.path.join(B, '.workbuddy', 'memory', 'MEMORY.md')

OK = 0; FAIL = 0
def chk(tag, cond, msg):
    global OK, FAIL
    if cond: OK += 1; print('[OK] %s %s' % (tag, msg))
    else:    FAIL += 1; print('[XX] %s %s' % (tag, msg))

def rd(p): return io.open(p, encoding='utf-8').read()

# ============ A 对话弧线取证 ============
print('=== EB-A 对话弧线（第 20 → 22 轮）===')
b2 = rd(os.path.join(DIR, 'batch_02.md'))
chk('EB-1', '必然会帮助另外一方遮挡来自另外一边的底层风暴' in b2, '第 20 轮用户提出「遮挡」原句')
chk('EB-2', ('保真度应该与两个粒子之间的' in b2) and ('可控密度气体' in b2),
    '第 20 轮元宝「可检验推论」（保真度 ∝ 物质分布 ＋ 气体实验提案）')
chk('EB-3', ('有遮挡物也没事' in b2) and ('和现实物质无关' in b2), '第 22 轮用户自撤原句')
chk('EB-4', ('你现在的反驳是' in b2) and ('并没有特别破坏纠缠的关联性' in b2),
    '第 22 轮元宝承认撤销（并引墨子号/光纤实验支持）')
chk('EB-5', '10⁻³⁰ 球面度' in b2, '第 20 轮元宝自算的几何立体角（10⁻³⁰ 球面度）')

# ============ B 体系现状 ============
print()
print('=== EB-B 体系现状 ===')
ZH = rd(P_ZH); LP = rd(P_LP)
chk('EB-6', (ZH.count('保真度磁化率') == 2) and (ZH.count('信道') == 0)
            and (ZH.count('可见度') == 0) and (ZH.count('密度矩阵') == 0),
    '论文「保真度」2 处均为 toric 判据（保真度磁化率）；信道/可见度/密度矩阵 各 0')
chk('EB-7', ('退相干' in ZH) and ('各 0 处' in ZH),
    '论文含第 57 轮「无量子态层」清点（退相干/纯态/混合态 = 0 ⟹ 保真度无定义）')
chk('EB-8', ('量子退相干' in LP) and ('无任何实验接入点' in LP),
    '清单 S-4（量子退相干：底层无熵产生、来自粗粒化、无实验接入点）现役')

# ============ C 定量：立体角复算 ＋ 双向失控 ============
print()
print('=== EB-C 定量 ===')
# C1 复算元宝的立体角：Ω = π r_p² / R²
r_p = mpf('1e-15'); R_dis = mpf(1)
omega = pi * r_p**2 / R_dis**2
print('  几何立体角 Ω = π(1e-15)²/1² = %.4e sr（元宝给 ~10⁻³⁰）' % omega)
chk('EB-9', (mpf('3.0e-30') < omega) and (omega < mpf('3.3e-30')), '立体角复算 = %.4e sr' % omega)

# C2 两读法的机制强度
n_air = mpf('2.5e25')      # m^-3
sigma_atom = mpf('1e-20')  # m²（几何原子截面量级）
L = mpf(1)
tau_opt = n_air * sigma_atom * L
mod_grav = mpf('6.674e-11') * mpf('1.2') / (mpf('8.98755e16') * mpf(1))   # Φ/c²（1 m³ 空气）
print('  读法①（引力耦合）：1 m³ 空气的 Φ/c² = %.3e ⟹ 相对调制 ~10⁻²⁷' % mod_grav)
print('  读法②（原子截面）：光学深度 τ = nσL = %.3e ⟹ 完全遮挡' % tau_opt)
span = -log10(mod_grav)
print('  ⟹ 两读法跨度 = %.2f 个数量级（10⁻²⁷ ↔ ~1）' % span)
chk('EB-10', (mpf('2.4e5') < tau_opt) and (tau_opt < mpf('2.6e5')), '光学深度 = %.2e（完全遮挡）' % tau_opt)
chk('EB-11', (mpf('8.8e-28') < mod_grav) and (mod_grav < mpf('9.0e-28')), '引力耦合调制 = %.3e' % mod_grav)
chk('EB-12', (mpf('26.9') < span) and (span < mpf('27.2')), '两读法跨度 = %.2f dex' % span)

# ============ D 两段式登记（补丁后项） ============
print()
print('=== EB-D 登记（补丁后项在预跑时预期失败）===')
n47 = [s for s in LP.split('\n') if s.startswith('| **N-47** |')]
chk('EB-13', len(n47) == 1 and ('纠缠' in n47[0]), '清单 N-47 行存在且唯一（补丁后）')
chk('EB-14', ('**47 条**' in LP) and ('N-47（第 130 轮' in LP), '负面计数 46→47（补丁后）')
T = rd(P_TZ)
chk('EB-15', ('N-47' in T) and ('纠缠保真度' in T), '台账候选③已更新（补丁后）')
chk('EB-16', os.path.exists(P_MEMO), '备忘录存在（补丁后）')
H = rd(P_HO)
chk('EB-17', '第 130 轮' in H, '交接说明含第 130 轮（补丁后）')
chk('EB-18', '第 130 轮' in rd(P_LOG), '日志含第 130 轮（补丁后）')
chk('EB-19', '进度 130' in rd(P_MEM), 'MEMORY 进度 130（补丁后）')

# ============ E 格式 ============
print()
print('=== EB-E 格式 ===')
def fmt_hits(t):
    L2 = t.split('\n')
    f1 = [i+1 for i, s in enumerate(L2) if s.strip().startswith(('，', ','))]
    f3 = [i+1 for i, s in enumerate(L2) if '\\|' in s and not s.lstrip().startswith('|')]
    return f1, f3
if os.path.exists(P_MEMO):
    f1, f3 = fmt_hits(rd(P_MEMO))
    chk('EB-20', len(f1) == 0 and len(f3) == 0, '备忘录格式：残片 %s 表外竖线 %s' % (f1[:3], f3[:3]))
else:
    chk('EB-20', False, '备忘录尚未生成（补丁后项）')

print()
print('=' * 56)
print('通过 %d 项，失败 %d 项' % (OK, FAIL))
