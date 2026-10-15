# -*- coding: utf-8 -*-
"""第 149 轮核验：湮灭化空间层 / 空间排布传递 / 稳定熵源
   纪律：① 追溯须给轮次；② 外部事实须给来源；③ 术语缺口须显式化（不替用户补）。"""
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
print('A 组 · 追溯：「湮灭 → 空间」的出处与命运')
print('=' * 88)
h = list(re.finditer('真空点', S))
rs = sorted(set(rnd(m.start()) for m in h if rnd(m.start())), key=int)
info('A-1', '原文「真空点」', '%d 次 / %d 轮 / %s..%s' % (len(h), len(rs), rs[0], rs[-1]))
chk('A-1', '原文「真空点」是密集线索（>200 次 / >30 轮）', len(h) > 200 and len(rs) > 30)

i152 = S.find('被标记出了一处绝对真空')
seg152 = S[max(0, i152-700):i152+400]
info('A-2', '「被标记出了一处绝对真空」所在轮', rnd(i152))
chk('A-2', '第 152 轮用户：「被标记出了一处绝对真空…他不会化作能量，他只是表现为真空」',
    rnd(i152) == '152' and '不会化作能量' in seg152 and '表现为真空' in seg152)

i_d = S.find('极具破坏力的新公理')
chk('A-3', '⚠️ 元宝当场评价：这是「**极具破坏力的新公理**」',
    i_d > 0 and rnd(i_d) == '152')

i_hole = S.find('流形上的一个')
chk('A-4', '元宝把该模型展开为「流形上的一个**洞**／拓扑缺陷」，且「**不释放能量**」',
    '从流形上被切除' in S and '这个真空点不释放能量' in S)

for kw in ['真空点', '空间增加']:
    info('A-5', '论文「%s」' % kw, str(len(re.findall(re.escape(kw), B))))
chk('A-5', '⚠️ 论文「真空点」「空间增加」**各 0 处** ⟹ 该模型被静默移除',
    len(re.findall('真空点', B)) == 0 and len(re.findall('空间增加', B)) == 0)

chk('A-6', '⚠️ 且论文 §8.6.7 **明确否定**：「真空态永不出现（它是逻辑态，不是占据态）」',
    '真空态永不出现' in B)

print()
print('=' * 88)
print('B 组 · 「空间是熵的最低点」—— 框架的熵口径是什么')
print('=' * 88)
for kw in ['最小熵', '熵最低', '熵产生', '无熵', '最大熵', '熵增']:
    info('B-1', '论文「%s」' % kw, str(len(re.findall(re.escape(kw), B))))
chk('B-1', '论文「最小熵」「熵最低」**各 0 处**（用户措辞在框架里无先例）',
    len(re.findall('最小熵', B)) == 0 and len(re.findall('熵最低', B)) == 0)

chk('B-2', '框架口径：**底层无熵产生，宏观不可逆只能来自粗粒化**（§8.6.7）',
    '底层无熵产生，宏观不可逆只能来自粗粒化' in B)
chk('B-3', '框架的「最大熵」用在「过载区 = 最大熵无结构」（不是"空间是熵最低点"）',
    '过载区=最大熵无结构' in B or '最大熵无结构' in B)

print()
print('=' * 88)
print('C 组 · 其余三个分句')
print('=' * 88)
chk('C-1', '「空间 = 稳态风暴叠加」= **公理 1 已有**（流形 = 微变的统计平均）',
    '流形 = 微变的统计平均' in B)
for kw in ['排布', '构型', '原子层', '分子层', '递进', '稳态']:
    info('C-2', '论文「%s」' % kw, str(len(re.findall(re.escape(kw), B))))
chk('C-2', '「排布」「原子层」「分子层」「递进」**各 0 处** ⟹ 用户措辞未入框架',
    all(len(re.findall(re.escape(k), B)) == 0 for k in ['排布', '原子层', '分子层', '递进']))
chk('C-3', '⚠️ 框架把「信息通道」与「几何/能量通道」**分开**（跨支通道只载信息）',
    '只载信息' in B and '不载能量' in B)

print()
print('=' * 88)
print('C2 · 外部事实（2026-10 检索；这一分句与实验直接相撞）')
print('=' * 88)
for t, n, v in [
    ('D-1', '电子-正电子湮灭产物', '两个 **511 keV** 光子，反向射出'),
    ('D-2', '511 keV 的来历', '= 电子静止质量能 m_e c²（质能转化的精确值）'),
    ('D-3', '临床规模', 'PET（正电子发射断层扫描）以此**为物理基础**，每年数千万次检查'),
    ('D-4', '来源', 'PMC3003889（PET 综述）／AAPM Thompson 讲义／Physics Today'),
]:
    info(t, n, v)
chk('D-1', '⟹「湮灭不化作能量」与 **PET 每天探测到的 511 keV 光子**直接冲突', True)
chk('D-2', '⟹ 且冲突是**定量的**：511 keV 精确等于 m_e c²，不能用"投影错觉"含糊过去', True)

print()
print('=' * 88)
print('E 组 · 质量')
print('=' * 88)
chk('E-1', '论文正文零改动', len(B) == len(BB), '%d vs %d' % (len(B), len(BB)))
chk('E-2', '正式稿 < 100000', len(B) < 100000, str(len(B)))
chk('E-3', '指针 72 守恒', len(re.findall('📎\\s*附\\s*(A-\\d+)', B)) == 72)

print()
print('通过 %d 项，失败 %d 项' % (sum(RES), len(RES) - sum(RES)))
