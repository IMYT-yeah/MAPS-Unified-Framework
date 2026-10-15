# -*- coding: utf-8 -*-
"""
第 140 轮 · 「原始对话里的凝聚态预言」检索核验
判据：① 原文关键词密度与轮次定位；② 项目内是否评估过；③ 第 126 轮台账的漏检。
"""
import io, sys, re, glob, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

R = []
def chk(tag, name, cond, extra=''):
    R.append(bool(cond))
    print('[%s] %-6s %-44s %s' % ('OK' if cond else 'XX', tag, name, extra))
def info(tag, name, val):
    print('[--] %-6s %-44s %s' % (tag, name, val))

BASE = '../初始资料/元宝对话_反物质与时间的哲学猜想/'
S = open(BASE + '对话全文_完整版.md', encoding='utf-8').read()
LEDGER = open('起点对话研究方向检索台账.md', encoding='utf-8').read()
PAPER = open('论文_正式稿_v3.0.md', encoding='utf-8').read()

print('=' * 92)
print('A 组 · 原文规模与轮次')
print('=' * 92)
marks = [(m.start(), m.group(1)) for m in re.finditer(r'## 第\s*(\d+)\s*轮', S)]
info('A-1', '原文全字符', '{:,}'.format(len(S)))
info('A-2', '轮次标记数 / 范围', '%d 个，第 %s – %s 轮' % (len(marks), marks[0][1], marks[-1][1]))
chk('A-1', '原文 ≥ 140 万字符', len(S) > 1_400_000)
chk('A-2', '轮次标记 = 433', len(marks) == 433, str(len(marks)))

def rnd(pos):
    r = None
    for p, n in marks:
        if p <= pos: r = n
        else: break
    return r

print()
print('=' * 92)
print('B 组 · 关键词密度（实测）')
print('=' * 92)
for kw in ['凝聚态', '超导', '分形', '晶格', '量子霍尔', '分数量子霍尔', '狄拉克', '玻色',
           '双半子', '负质量', '激子-极化激元', '港湾几何', '量子硬化', '居里温度', '预成核']:
    info('B', kw, str(len(re.findall(kw, S))))
chk('B-1', '「凝聚态」实测 47 处（台账说 2 处）', len(re.findall('凝聚态', S)) == 47)
chk('B-2', '「双半子」实测 84 处（台账说 0）', len(re.findall('双半子', S)) == 84)
chk('B-3', '「量子硬化」1 处 / 「居里温度」6 处 / 「预成核」2 处',
    len(re.findall('量子硬化', S)) == 1 and len(re.findall('居里温度', S)) == 6
    and len(re.findall('预成核', S)) == 2)

print()
print('=' * 92)
print('C 组 · 轮次定位（A 类四条预言）')
print('=' * 92)
loc = {}
for kw in ['量子硬化', '居里温度', '预成核', '激子-极化激元']:
    rs = sorted(set(rnd(m.start()) for m in re.finditer(kw, S)), key=int)
    loc[kw] = rs
    info('C', kw, '第 %s 轮' % '/'.join(rs))
chk('C-1', '量子硬化 → 第 80 轮', loc['量子硬化'] == ['80'])
chk('C-2', '居里温度 → 第 85 轮', loc['居里温度'] == ['85'])
chk('C-3', '预成核 → 第 87 轮', loc['预成核'] == ['87'])
chk('C-4', '激子-极化激元 → 含第 63/65/66/98 轮',
    set(['63', '65', '66', '98']).issubset(set(loc['激子-极化激元'])))

print()
print('=' * 92)
print('D 组 · 项目内是否评估过（关键）')
print('=' * 92)
allmd = {f: open(f, encoding='utf-8').read() for f in glob.glob('*.md')}
# ⚠️ 两段式判据（C-76 族第 13 次）：排除本轮新产出的文件，否则自指污染
allmd = {k: v for k, v in allmd.items()
         if '备份' not in k and '原始对话凝聚态预言' not in k}
print('  （已排除本轮产出；扫描 %d 个历史文件）' % len(allmd))
tot = {}
for kw in ['量子硬化', '居里温度', '预成核', '超声共振谱', '金刚石压砧', '超快光谱',
           '刚性模量', '极化激元']:
    tot[kw] = sum(len(re.findall(kw, v)) for v in allmd.values())
    info('D', '项目内「%s」' % kw, '%d 处' % tot[kw])
chk('D-1', 'A1/A2/A3 的关键词在项目内全 0（从未评估）',
    all(tot[k] == 0 for k in ['量子硬化', '居里温度', '预成核', '超声共振谱',
                              '金刚石压砧', '超快光谱', '刚性模量', '极化激元']))
chk('D-2', '引力子模那一支**已评估**（S-E5 在论文里）',
    'S-E5' in PAPER and 'FQH' in PAPER)

print()
print('=' * 92)
print('E 组 · 台账的漏检（C-91）')
print('=' * 92)
chk('E-1', '台账写「凝聚态」仅 2 处（与实测 47 矛盾）',
    '「凝聚态」仅 2 处' in LEDGER)
chk('E-2', '台账写「半子」0 命中（与实测 84 矛盾）',
    '「半子」0' in LEDGER or '「半子」0——未入' in LEDGER)
chk('E-3', '台账把「铁磁 = 共振腔」标为 ⏸️ 未核到',
    '铁磁 = 共振腔' in LEDGER)
chk('E-4', '台账把「双半子论文」标为 ⏸️ 未入', '双半子论文' in LEDGER)

print()
print('=' * 92)
print('F 组 · 判定所需的框架依据')
print('=' * 92)
chk('F-1', '第 60 轮的「缺势阱型构型差」在清单里',
    '势阱型构型差' in open('工程期望清单.md', encoding='utf-8').read())
chk('F-2', '框架的「自旋」是自旋 2（引力模态），非磁自旋',
    '自旋 2' in PAPER)
chk('F-3', 'N-21（化学键/相变潜热/电离能）已登记为同源障碍',
    'N-21' in open('工程期望清单.md', encoding='utf-8').read())

print()
print('通过 %d 项，失败 %d 项' % (sum(R), len(R) - sum(R)))
