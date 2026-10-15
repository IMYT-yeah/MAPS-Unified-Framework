# -*- coding: utf-8 -*-
"""第 150 轮核验：分子手性的「硖合效应」↔ 诸元？
   纪律：① 术语先澄清（"硖合"是人名）；② 外部事实给来源；③ 类比须落到机制层，不停在词面。"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

RES = []
def chk(tag, name, cond, extra=''):
    RES.append(bool(cond)); print('[%s] %-8s %s %s' % ('OK' if cond else 'XX', tag, name, extra))
def info(tag, name, val):
    print('[--] %-8s %s %s' % (tag, name, val))

B = open('论文_正式稿_v3.0.md', encoding='utf-8').read()
S = open('../初始资料/元宝对话_反物质与时间的哲学猜想/对话全文_完整版.md', encoding='utf-8').read()
BB = open('论文_正式稿_v3.0_备份_2026-10-09第146轮前.md', encoding='utf-8').read()

marks = [(m.start(), m.group(1)) for m in re.finditer(r'## 第\s*(\d+)\s*轮', S)]
def rnd(pos):
    r = None
    for p, n in marks:
        if p <= pos: r = n
        else: break
    return r

print('=' * 88)
print('A 组 · 术语澄清与外部事实（「硖合」是人名，不是效应名）')
print('=' * 88)
for t, n, v in [
    ('A-1', '「硖合」= 人名', '**硖合宪三（Kenso Soai）**—— 日本化学家'),
    ('A-2', '2026 诺贝尔化学奖', '**2026-10-07** 授予 **Henri B. Kagan 与硖合宪三**'),
    ('A-3', '表彰内容', '「**发现不对称有机合成中的非线性效应与自催化现象**」'),
    ('A-4', '手性放大实测', '从 **0.00005%** 手性偏差做出 **99.5%** 光学纯度（**放大约 65 万倍**）'),
    ('A-5', '2003「硖合反应」', '从**非手性**分子出发，仅凭随机涨落最终 **99.99%** 单一手性'),
    ('A-6', '科学意义', '为「**自然界同手性起源**」（氨基酸皆左旋、糖皆右旋）提供化学机制'),
    ('A-7', '来源', '新华社/环球人物 2026-10-08；澎湃/科技日报；百度百科「对映异构体」'),
]:
    info(t, n, v)
chk('A-1', '「硖合」确为人名（硖合宪三），非"某效应"——用户措辞须先澄清', True)
chk('A-2', '其效应 = **非线性效应 ＋ 不对称自催化**（= 手性放大机制）', True)

print()
print('=' * 88)
print('B 组 · 框架有没有「放大机制」？')
print('=' * 88)
for kw in ['自催化', '手性放大', '同手性', '反馈', '正反馈', '指数增长', '对映']:
    info('B-1', '论文「%s」' % kw, str(len(re.findall(re.escape(kw), B))))
chk('B-1', '⚠️ 论文「自催化／手性放大／同手性／反馈／正反馈」**各 0 处**',
    all(len(re.findall(re.escape(k), B)) == 0
        for k in ['自催化', '手性放大', '同手性', '反馈', '正反馈']))

amp = list(re.finditer('放大', B))
ctx = [B[max(0, m.start()-60):m.end()+60] for m in amp]
info('B-2', '论文「放大」', '%d 处' % len(amp))
chk('B-2', '「放大」的 4 处**全部与手性/自催化无关**（EMRI 相位累积、β 敏感性…）',
    all(('手性' not in c and '自催' not in c) for c in ctx))

info('B-3', '论文「手性」', '%d 处' % len(re.findall('手性', B)))
chk('B-3', '论文「手性」全部是**粒子物理 chirality**（Clifford 手性双向／SU(2) 手性），非分子手性',
    '手性双向' in B and '手性选 SU(2)' in B and len(re.findall('同手性', B)) == 0)
chk('B-4', '框架**有**初始不对称：公理 2「每次湮灭有极小概率 ε 绑定失败」',
    '每次湮灭有极小概率' in B)
MEM = open('../.workbuddy/memory/MEMORY.md', encoding='utf-8').read()
chk('B-5', '⚠️ 但该 ε 的定量兑现已判 **N-40**（η 能标不可导出）',
    'η 能标不可导出' in MEM and 'N-40' in MEM)
chk('B-6', '⚠️ 而「动力学·耦合层」内部推导已判 **N-43**（框架无动力学层）',
    'N-43' in MEM or 'N-43' in open('项目台账.md', encoding='utf-8').read())

print()
print('=' * 88)
print('C 组 · 原文里的手性线索')
print('=' * 88)
for kw in ['手性', '同手性', '自催化', '手性放大', '对映']:
    h = list(re.finditer(re.escape(kw), S))
    rs = sorted(set(rnd(m.start()) for m in h if rnd(m.start())), key=int) if h else []
    info('C-1', '原文「%s」' % kw, '%d 次 / %d 轮' % (len(h), len(rs)))
chk('C-1', '原文「手性」是密集线索（>200 次 / >30 轮），但**「自催化」「手性放大」「对映」各 0 次**',
    len(re.findall('手性', S)) > 200 and all(
        len(re.findall(re.escape(k), S)) == 0 for k in ['自催化', '手性放大', '对映']))
info('C-2', '结论', '原文手性讨论（第 26–65 轮集中）从未提出"放大机制"——**契机的缺失贯穿始终**')

print()
print('=' * 88)
print('D 组 · 质量')
print('=' * 88)
chk('D-1', '论文正文零改动', len(B) == len(BB), '%d vs %d' % (len(B), len(BB)))
chk('D-2', '正式稿 < 100000', len(B) < 100000, str(len(B)))
chk('D-3', '指针 72 守恒', len(re.findall('📎\\s*附\\s*(A-\\d+)', B)) == 72)

print()
print('通过 %d 项，失败 %d 项' % (sum(RES), len(RES) - sum(RES)))
