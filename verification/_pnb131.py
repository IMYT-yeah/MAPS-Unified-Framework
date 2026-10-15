# -*- coding: utf-8 -*-
"""第 131 轮：候选④「三态 P/N/B」评估 —— 框架已含（无新增）＋「e 进制」自相矛盾
PNB-1 … PNB-17（含两段式；补丁后须 0 失败）
"""
import io, os, re
from mpmath import mp, mpf, log, log10, findroot

mp.dps = 30
B   = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
DIR = os.path.join(B, '初始资料', '元宝对话_反物质与时间的哲学猜想', '检索批次')
P_ZH   = os.path.join(B, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md')
P_LP   = os.path.join(B, 'outputs', '工程期望清单.md')
P_LP_B = os.path.join(B, 'outputs', '工程期望清单_备份_2026-10-05第131轮前.md')
P_TZ   = os.path.join(B, 'outputs', '起点对话研究方向检索台账.md')
P_MEMO = os.path.join(B, 'outputs', '候选4评估_三态PNB_框架已含无新增与e进制自相矛盾.md')
P_HO   = os.path.join(B, '环境交接说明.md')
P_LOG  = os.path.join(B, '.workbuddy', 'memory', '2026-10-05.md')
P_MEM  = os.path.join(B, '.workbuddy', 'memory', 'MEMORY.md')

OK = 0; FAIL = 0
def chk(tag, cond, msg):
    global OK, FAIL
    if cond: OK += 1; print('[OK] %s %s' % (tag, msg))
    else:    FAIL += 1; print('[XX] %s %s' % (tag, msg))

def rd(p): return io.open(p, encoding='utf-8').read()

# ============ A 对话原文（batch_15） ============
print('=== PNB-A 对话原文 ===')
tf = rd(os.path.join(DIR, '提取_batch_14-16.md'))
raw = rd(os.path.join(DIR, 'batch_15.md'))
chk('PNB-1', ('P(P) = P(N) = (1 - P(B))/2' in tf) and ('三进制符号' in tf),
    'B15-02：三态定义 ＋ P(B)=ε≈10⁻⁹ ＋ 三进制编码（提取件）')
chk('PNB-2', '无变化是一种被排除的性质' in raw, 'B15-05 原句：「无变化是一种被排除的性质」')
chk('PNB-3', 'e^{-λt}' in raw or 'e^' in raw, 'B15-04 原文含泊松/指数式')

# ============ B 框架现状 ============
print()
print('=== PNB-B 框架现状（已含/未含）===')
ZH = rd(P_ZH); LP = rd(P_LP)
chk('PNB-4', '每 tick 每个格点恰好一次对换' in ZH,
    '★框架已含（且更强）：第 40 轮口径「每 tick 每个格点恰好一次对换」')
chk('PNB-5', '2.7×10⁻⁹⁶' in ZH, '串行归一化已被排除（2.7×10⁻⁹⁶ m 荒谬值，口径确立）')
LP_b = rd(P_LP_B)
cur_wo = '\n'.join(s for s in LP.split('\n') if 'N-48' not in s)
chk('PNB-6', all((ZH.count(k) == 0) and (LP_b.count(k) == 0) and (k not in cur_wo)
                 for k in ['三态', '字母表', 'P/N/B']),
    '（两段式）改前论文/清单「三态/字母表/P/N/B」各 0 处；改后新增字样仅限 N-48 行')
chk('PNB-7', 'C-16' in LP, 'ε 多义已有登记（C-16：§8.4 漂移指数为第三义）')
chk('PNB-8', ZH.count('泊松涌撒') >= 1, '框架已有「泊松涌撒」（§3.1 因果集公理化，%d 处）' % ZH.count('泊松涌撒'))
chk('PNB-9', '1.855' in LP, 'tick 频率 1.855×10⁴³ s⁻¹ 已在清单（S-4；对应 B15-08 的「B 事件间隔 = t_P」）')

# ============ C 信息熵复核（本轮唯一新算） ============
print()
print('=== PNB-C 信息熵复核：三态模型给多少 bit/事件 ===')
def H(eps):
    eps = mpf(eps)
    return -(1 - eps) * (log((1 - eps) / 2) / log(2)) - eps * (log(eps) / log(2))
h_eps = H(mpf('1e-9'))
log2e = log(mp.e) / log(2)
print('  H(ε=1e-9) = %.6f bit/事件（三态模型自设参数）' % h_eps)
print('  log₂e = %.6f（「e 进制」的上限参照）' % log2e)
print('  log₂3 = %.6f（三态均匀上限）' % (log(3) / log(2)))
eps_sol = findroot(lambda e: H(e) - log2e, mpf('0.14'))
print('  ⟹ 要 H = log₂e 需 ε ≈ %.4f（与自设 10⁻⁹ 差 8 个数量级）' % eps_sol)
chk('PNB-10', (mpf('0.999') < h_eps) and (h_eps < mpf('1.001')),
    'H(ε=1e-9) = %.6f bit ≈ 1.0（不是 log₂e = %.4f）' % (h_eps, log2e))
chk('PNB-11', (mpf('0.12') < eps_sol) and (eps_sol < mpf('0.16')),
    '解 H(ε) = log₂e ⟹ ε ≈ %.4f（与 10⁻⁹ 相差 ~10⁸ 倍）' % eps_sol)

# ============ D 伴生条目（信息项） ============
print()
print('=== PNB-D 伴生条目分布（信息）===')
for kw in ['隧穿', '瞬时', '无穷远', '射影']:
    print('  %-4s ZH %d | LP %d' % (kw, ZH.count(kw), LP.count(kw)))

# ============ E 两段式登记（补丁后项） ============
print()
print('=== PNB-E 登记（补丁后项在预跑时预期失败）===')
n48 = [s for s in LP.split('\n') if s.startswith('| **N-48** |')]
chk('PNB-12', len(n48) == 1 and ('三态' in n48[0]), '清单 N-48 行存在且唯一（补丁后）')
chk('PNB-13', ('**48 条**' in LP) and ('N-48（第 131 轮' in LP), '负面计数 47→48（补丁后）')
T = rd(P_TZ)
chk('PNB-14', ('N-48' in T) and ('三态' in T), '台账候选④已更新（补丁后）')
chk('PNB-15', os.path.exists(P_MEMO), '备忘录存在（补丁后）')
chk('PNB-16', '第 131 轮' in rd(P_HO), '交接说明含第 131 轮（补丁后）')
chk('PNB-17', '第 131 轮' in rd(P_LOG), '日志含第 131 轮（补丁后）')
chk('PNB-18', '进度 131' in rd(P_MEM), 'MEMORY 进度 131（补丁后）')

# ============ F 格式 ============
print()
print('=== PNB-F 格式 ===')
def fmt_hits(t):
    L2 = t.split('\n')
    f1 = [i+1 for i, s in enumerate(L2) if s.strip().startswith(('，', ','))]
    f3 = [i+1 for i, s in enumerate(L2) if '\\|' in s and not s.lstrip().startswith('|')]
    return f1, f3
if os.path.exists(P_MEMO):
    f1, f3 = fmt_hits(rd(P_MEMO))
    chk('PNB-19', len(f1) == 0 and len(f3) == 0, '备忘录格式：残片 %s 表外竖线 %s' % (f1[:3], f3[:3]))
else:
    chk('PNB-19', False, '备忘录尚未生成（补丁后项）')

print()
print('=' * 56)
print('通过 %d 项，失败 %d 项' % (OK, FAIL))
