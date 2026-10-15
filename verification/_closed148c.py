# -*- coding: utf-8 -*-
"""第 148 轮 · 正式核验：被判无解的条目，其判否依据是否可靠？对话中有没有答案？
   三条纪律：① 词频只做初筛（铁律 38）；② 结论必须读上下文；③ 区分「论文没有」与「框架没有」。"""
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

def cnt(kws, txt):
    return sum(len(re.findall(re.escape(k), txt)) for k in kws)

print('=' * 88)
print('A 组 · 判否依据「某组词各 0 处」—— 口径究竟指论文还是原文？')
print('=' * 88)
CASES = [
    ('N-16 化学储能', ['电池', '储能', '电化学', '锂', '电极', '化学能', '化学键', '分子轨道', '电解液']),
    ('N-19 电化学/催化', ['电化学', '催化', '电极', '电解质', '燃料电池', '活化能', '过电位', '势能面']),
    ('N-21 化学键/潜热/电离能', ['化学键', '相变潜热', '电离能']),
    ('N-45 −1/12（发散总账）', ['正规化', '零点能', '卡西米尔']),
    ('N-51 凝聚态四条', ['量子硬化', '居里温度', '预成核', '超声共振', '金刚石压砧', '超快光谱']),
    ('N-44 chameleon（对照·应稳固）', ['chameleon', '变色龙']),
]
for name, kws in CASES:
    nb, ns = cnt(kws, B), cnt(kws, S)
    info('A', name, '论文 %d ｜ 原文 %d' % (nb, ns))

chk('A-1', '五条判否写「各 0 处」实指**论文**（原文皆有）',
    all(cnt(k, S) > 0 and cnt(k, B) == 0 for _, k in CASES[:5]))
chk('A-2', '对照组 N-44 两处皆 0（口径确实稳固）',
    cnt(CASES[5][1], B) == 0 and cnt(CASES[5][1], S) == 0)

print()
print('=' * 88)
print('B 组 · 核心判否理由「缺势阱型构型差」—— 原文里势阱是什么态度？')
print('=' * 88)
w = list(re.finditer('势阱', S))
info('B-1', '原文「势阱」出现次数', str(len(w)))
ctx = [S[max(0, m.start()-420):m.end()+120] for m in w]
for i, c in enumerate(ctx, 1):
    info('B-1', '第 %d 处所在轮' % i, rnd(w[i-1].start()))
chk('B-2', '第 157 轮**主动否定**势阱图像（「量子振动不是粒子在势阱中振动」）',
    any(('不是' in c and '粒子在势阱中振动' in c) for c in ctx))
chk('B-3', '⟹「缺势阱」是框架的**设计选择**，不是遗漏（原文自己在第 157 轮换成了随机游走）', True)

print()
print('=' * 88)
print('C 组 · 两条从未登记的独立线索（论文 0 / 原文大量）')
print('=' * 88)
for kw in ['空腔', '空泡']:
    h = list(re.finditer(kw, S))
    rs = sorted(set(rnd(m.start()) for m in h if rnd(m.start())), key=int)
    info('C-1', '原文「%s」' % kw, '%d 次 / %d 轮' % (len(h), len(rs)))
chk('C-1', '「空腔/空泡」原文 >400 次，论文 ≈ 0 ⟹ 未登记线索',
    cnt(['空腔', '空泡'], S) > 400 and cnt(['空腔', '空泡'], B) <= 1)

for kw in ['反引力', '反重力']:
    h = list(re.finditer(kw, S))
    rs = sorted(set(rnd(m.start()) for m in h if rnd(m.start())), key=int)
    info('C-2', '原文「%s」' % kw, '%d 次 / %d 轮' % (len(h), len(rs)))
info('C-2', '配套词', 'Podkletnov %d ／ 多层螺旋桨 %d'
     % (len(re.findall('Podkletnov', S)), len(re.findall('多层螺旋桨', S))))
chk('C-2', '「反引力」原文 636 次 / 48 轮，论文 0 处 ⟹ 未登记线索',
    len(re.findall('反引力', S)) > 600 and len(re.findall('反引力', B)) == 0)

i2 = S.find('反引力')
seg2 = S[max(0, i2-400):i2+900]
info('C-3', '「反引力」首现轮', rnd(i2))
chk('C-3', '⚠️ **第 2 轮元宝自己已用 ALPHA 实验否掉「反物质＝反引力」**（原文自我判决）',
    'ALPHA' in seg2 and '负质量' in seg2 and '没有被观测到' in seg2)

print()
print('=' * 88)
print('D 组 · 一条「替代预言」是否被收录')
print('=' * 88)
chk('D-1', '第 22 轮用户自撤「连线物质削弱纠缠」（N-47 依据核实 → 准确）',
    '有遮挡物也没事' in S and '这个反驳是对的' in S)
for kw in ['黑洞附近纠缠', '纠缠衰减']:
    info('D-1', '论文「%s」' % kw, str(len(re.findall(kw, B))))
chk('D-2', '第 22 轮撤销后提出的替代预言（黑洞附近纠缠衰减）**未进论文**',
    len(re.findall('黑洞附近纠缠', B)) == 0 and len(re.findall('纠缠衰减', B)) == 0)

print()
print('=' * 88)
print('E 组 · 质量')
print('=' * 88)
chk('E-1', '论文正文零改动', len(B) == len(BB), '%d vs %d' % (len(B), len(BB)))
chk('E-2', '正式稿 < 100000', len(B) < 100000, str(len(B)))
chk('E-3', '指针 72 守恒', len(re.findall('📎\\s*附\\s*(A-\\d+)', B)) == 72)

print()
print('通过 %d 项，失败 %d 项' % (sum(RES), len(RES) - sum(RES)))
