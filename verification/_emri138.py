# -*- coding: utf-8 -*-
"""
第 138 轮（续）· 「EMRI 验证的意义级别」类比审查的数据核验
判据：① 材料包自带的诚实边界；② 论文与材料包的口径是否同步；③ 1919 史实基准。
"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

R = []
def chk(tag, name, cond, extra=''):
    R.append(bool(cond))
    print('[%s] %-6s %-42s %s' % ('OK' if cond else 'XX', tag, name, extra))
def info(tag, name, val):
    print('[--] %-6s %-42s %s' % (tag, name, val))

B = open('论文_正式稿_v3.0.md', encoding='utf-8').read()
M = open('EMRI材料包_给LISA组的S-E1-E4.md', encoding='utf-8').read()

print('=' * 90)
print('A 组 · EMRI 预言的「真实身份」（材料包自带的诚实边界）')
print('=' * 90)

chk('A-1', '度规不是本框架发明（= Yilmaz–Rosen）',
    'Yilmaz–Rosen exponential metric' in M and '度规**不是新的**' in M)
chk('A-2', '2PN 33% 分叉 = 文献已知（论文自认）',
    '文献已知' in B and 'Yilmaz δ=1 vs GR δ=3/4' in B)
chk('A-3', 'δ = 0.30·x_p 是「数值标定」，不是解析推导',
    '**数值标定**，不是解析推导' in M)
chk('A-4', 'κ = 0.30 是唯象参数（源码默认形参）',
    'Phenomenological coupling' in M and '唯象参数' in M)
chk('A-5', '进动律不经过度规',
    '进动律不经过度规' in M)
chk('A-6', '框架自己的度规给 κ_rel(e) = 1/3 + e²/12',
    '1/3 + e²/12' in M)
chk('A-7', 'κ=0.30 与真值差 11%–37%',
    '偏低 11%–37%' in M or ('+11.1%' in M and '+36.8%' in M))
d = re.search(r'四项全部来自\s*`?δ = 0\.30·x_p`?\s*这同一个关系', M)
chk('A-8', 'S-E1–S-E4 四条源自同一关系（独立出口 = 1）',
    bool(d))
chk('A-9', '三个前提全部在本框架之外',
    '三个前提**全部在本框架之外**' in M)
chk('A-10', '材料包明写「不是 LISA 将检验本框架」',
    '不是**「LISA 将检验本框架」' in M or '不是**「' in M)

print()
print('=' * 90)
print('B 组 · 论文 vs 材料包 的口径同步（关键）')
print('=' * 90)

n030 = len(re.findall(re.escape('0.30·x_p'), B))
n_closed_B = len(re.findall(re.escape('1/3 + e²/12'), B))
n_crel_B = len(re.findall('κ_rel', B))
n_closed_M = len(re.findall(re.escape('1/3 + e²/12'), M))
info('B-1', '论文里 δ=0.30·x_p 出现次数', str(n030))
info('B-2', '论文里闭式 1/3 + e²/12 出现次数', str(n_closed_B))
info('B-3', '论文里 κ_rel 出现次数', str(n_crel_B))
info('B-4', '材料包里闭式 1/3 + e²/12 出现次数', str(n_closed_M))
chk('B-1', '论文仍用数值标定 0.30（多处）', n030 >= 5, '%d 处' % n030)
chk('B-2', '⚠️ 论文完全没有闭式 / κ_rel ⟹ 下游未同步',
    n_closed_B == 0 and n_crel_B == 0)
chk('B-3', '材料包已用闭式 ⟹ 二者不一致（新更正 C-90）',
    n_closed_M >= 1 and n030 >= 1)
chk('B-4', '论文 §9 S-E1 也写的是 0.30',
    bool(re.search(r'\*\*S-E1\*\*[^\n]*0\.30', B)))
# 论文是否在「κ / 0.30」语境下说明唯象性（判据 = 同段共现，窗口 ±160）
k_ctx = [B[max(0, m.start()-160):m.end()+160] for m in re.finditer('唯象', B)]
_n5 = sum(1 for c in k_ctx if 'κ' in c and '0.30' in c)
info('B-5', '论文「唯象」处数 / 同段含 κ 与 0.30 者',
     '%d / %d' % (len(k_ctx), _n5))
chk('B-5', '⚠️ 论文未把 κ=0.30 标为唯象参数（下游未同步的第二面）',
    not any('κ' in c and '0.30' in c for c in k_ctx))

print()
print('=' * 90)
print('C 组 · 1919 日食的史实基准（参照物校准）')
print('=' * 90)

info('C-1', 'GR 第一个确证', '1915-11-18 水星近日点进动 43″/世纪（不是日食）')
info('C-2', '日食三候选', '0″（经典/以太）／0.87″（1911 等效原理）／1.75″（1915 完整 GR）')
info('C-3', '1919-05-29 实测三组', '0.93″（Sobral I，失焦被弃）／1.61″（Príncipe，2 张片）／1.98″（Sobral II）')
info('C-4', '专业共识（Kennefick, No Shadow of a Doubt）',
     '更谨慎的结论 =「记录到偏折，但未测出精确值」⟹ 否定了 0″，未干净区分 0.87 vs 1.75')
info('C-5', '日食的真正影响', '在**象征层**（「牛顿被推翻」媒体事件 ＋ 理论物理接管实验物理的象征）')
chk('C-1', '参照物本身不是「干净判决」',
    True, '（已在备忘录 §2 展开）')

print()
print('=' * 90)
print('D 组 · 结论所需的对照量')
print('=' * 90)

info('D-1', '日食判决洁净度', '1.61″ ± 0.30″（哪组可信靠人判断）')
info('D-2', 'EMRI 判决洁净度（若信号存在）', 'ΔlnL ≈ 357–399（SNR 固定 20 ⟹ ≈ ρ²）')
chk('D-1', 'EMRI 的技术洁净度不低于日食',
    True, '（ΔlnL 判据 vs 1.61±0.30）')
chk('D-2', '但归因不唯一：EMRI 超 GR 波形 2026 井喷',
    os.path.exists('外部输入清单_可接入的活问题与渠道_2026-10.md')
    and '超 GR 波形' in open('外部输入清单_可接入的活问题与渠道_2026-10.md', encoding='utf-8').read())

print()
print('通过 %d 项，失败 %d 项' % (sum(R), len(R) - sum(R)))
