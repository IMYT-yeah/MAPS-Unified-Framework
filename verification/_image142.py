# -*- coding: utf-8 -*-
"""
第 142 轮 · 「棋盘翻转」意象的翻译核验
判据：① 原文该意象的规模与轮次；② 论文里对应概念的覆盖；③ 框架三层是否自相似。
"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

R = []
def chk(tag, name, cond, extra=''):
    R.append(bool(cond))
    print('[%s] %-6s %-46s %s' % ('OK' if cond else 'XX', tag, name, extra))
def info(tag, name, val):
    print('[--] %-6s %-46s %s' % (tag, name, val))

BASE = '../初始资料/元宝对话_反物质与时间的哲学猜想/'
S = open(BASE + '对话全文_完整版.md', encoding='utf-8').read()
B = open('论文_正式稿_v3.0.md', encoding='utf-8').read()
Q = open('项目台账.md', encoding='utf-8').read()
T = open('动力学耦合层可行性_三档判定与输入台账.md', encoding='utf-8').read()

marks = [(m.start(), m.group(1)) for m in re.finditer(r'## 第\s*(\d+)\s*轮', S)]
def rnd(pos):
    r = None
    for p, n in marks:
        if p <= pos: r = n
        else: break
    return r

print('=' * 92)
print('A 组 · 意象在原始对话里的规模（追溯）')
print('=' * 92)
cf = {}
for m in re.finditer('分形', S):
    r = rnd(m.start()); cf[r] = cf.get(r, 0) + 1
cs = {}
for m in re.finditer('自相似', S):
    r = rnd(m.start()); cs[r] = cs.get(r, 0) + 1
info('A-1', '「分形」', '%d 轮次 / %d 处' % (len(cf), sum(cf.values())))
info('A-2', '「自相似」', '%d 轮次 / %d 处' % (len(cs), sum(cs.values())))
zone = [r for r in cf if 174 <= int(r) <= 196]
info('A-3', '第 174–196 轮内的「分形」处数',
     str(sum(cf[r] for r in zone)) + ' 处 / 共 23 轮中的 %d 轮' % len(zone))
chk('A-1', '意象集中在第 174–196 轮（≥ 200 处）', sum(cf[r] for r in zone) >= 200)
chk('A-2', '第 174 轮确有用户原话（含「没法验证」）',
    '没法验证，也没法区分' in S)

print()
print('=' * 92)
print('B 组 · 论文里的覆盖（关键对照）')
print('=' * 92)
for kw in ['自相似', '分形', '翻转面', '翻转', '奇偶', '(−1)^N', '镜像支', '临界']:
    info('B', '论文「%s」' % kw, '%d 处' % len(re.findall(re.escape(kw), B)))
chk('B-1', '论文「分形」= 0 处', len(re.findall('分形', B)) == 0)
chk('B-2', '论文「自相似」= 1 处（且为否定性用法）',
    len(re.findall('自相似', B)) == 1 and '等温球' in B[max(0, B.find('自相似')-400):B.find('自相似')])
chk('B-3', '论文有「翻转面」条目（视界=时间箭头翻转面）', '时间箭头翻转面' in B)
chk('B-4', '论文有「(−1)^N（交换符号）」条目', '(−1)^N' in B and '交换符号' in B)

print()
print('=' * 92)
print('C 组 · 意象「自相似嵌套」vs 框架「三层异质」（冲突点）')
print('=' * 92)
# 三层表：检查 I-16 表的三层本体是否互不同构
tab_ok = ('衬底层' in T and '弦网层' in T and '场论层' in T)
info('C-1', 'I-16 三层表存在于第 123 轮台账', str(tab_ok))
chk('C-1', '三层表存在', tab_ok)
chk('C-2', '三层本体互不同构（置换 / 通量 / 连续场）',
    '置换' in T and '态是通量' in T and '连续 x' in T)
chk('C-3', '「三层没有一层同时满足三者」已在台账写明',
    '三层里没有一层同时满足' in T)
chk('C-4', '衬底层只有「8 个 (Z₂)³ 类」（非可变 S_n）',
    '8 个' in T and '(Z₂)³' in T)

print()
print('=' * 92)
print('D 组 · 新增量那句的框架原型')
print('=' * 92)
chk('D-1', '论文 §7.2 把交换符号列为「框架已有非交换元素」',
    '框架已有非交换元素' in B and '交换符号' in B)
chk('D-2', '第 76 轮已判「唯一非交换的 Clifford 投影是记号的改变」（N-31）',
    'N-31' in Q or '记号的改变' in Q)

print()
print('=' * 92)
print('E 组 · 可检验性状态（最要紧）')
print('=' * 92)
chk('E-1', '第 174 轮用户自承「没法验证」（⟹ 按四类判定不进预言表）',
    '我们没法验证，也没法区分' in S)
chk('E-2', '而当时回答是「几乎是逻辑必然」（两句不能同时成立）',
    '逻辑必然' in S)
chk('E-3', 'S-4（退相干）已结项「无实验接入点」',
    '无实验接入点' in Q)

print()
print('通过 %d 项，失败 %d 项' % (sum(R), len(R) - sum(R)))
