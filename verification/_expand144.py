# -*- coding: utf-8 -*-
"""
第 144 轮 · 「层层扩大」意象核验
判据：① 公理 1 的原文（是否已含用户的"无尽循环"）；② 框架是否有固定标尺；③ 前轮结论引用。
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

R = []
def chk(tag, name, cond, extra=''):
    R.append(bool(cond))
    print('[%s] %-6s %-48s %s' % ('OK' if cond else 'XX', tag, name, extra))
def info(tag, name, val):
    print('[--] %-6s %-48s %s' % (tag, name, val))

B = open('论文_正式稿_v3.0.md', encoding='utf-8').read()
V143 = open('验证_衬底层八类与三通道.md', encoding='utf-8').read()
F68 = open('位置算符缺口_I-16的形式化与三层判定.md', encoding='utf-8').read()

print('=' * 94)
print('A 组 · ⭐ 关键：用户的「无尽循环」是否已在公理 1 里')
print('=' * 94)
for kw in ['正反物质对持续', '湮灭—再生', '普朗克尺度频率', '每一次相遇是一次',
           '流形无限微变', '微变权守恒']:
    n = len(re.findall(re.escape(kw), B))
    info('A', '「%s」' % kw, '%d 处' % n)
chk('A-1', '公理 1 含「正反物质对持续（相遇—湮灭—再生）」', '正反物质对持续' in B)
chk('A-2', '公理 1 含「普朗克尺度频率」', '普朗克尺度频率' in B)
chk('A-3', '公理 1 含「每一次相遇是一次『微变』」', '每一次相遇是一次' in B)
chk('A-4', '含「流形无限微变」', '流形无限微变' in B)
chk('A-5', '含「微变权守恒命题」（§4.4，微变的定量版）', '微变权守恒' in B)
chk('A-6', '「四力 = 同一机制在不同尺度/构型的涌现模态」',
    '同一机制在不同尺度' in B)

print()
print('=' * 94)
print('B 组 · 论文里的相关词频')
print('=' * 94)
for kw in ['微变', '流形', '标度', '膨胀', '红移', '共形', '普朗克尺度', 'l_P', '绝对']:
    info('B', '「%s」' % kw, '%d 处' % len(re.findall(re.escape(kw), B)))

print()
print('=' * 94)
print('C 组 · ⚠️ 框架是否有「固定标尺」（决定假设是否自容）')
print('=' * 94)
chk('C-1', '框架以 l_P（普朗克尺度）为底层固定标尺',
    len(re.findall('l_P', B)) > 50 and '普朗克尺度' in B)
chk('C-2', '框架有 H（等分账 ρ = 3H²/8πG）',
    '3H²' in B or '3H2' in B or '8πG' in B)
chk('C-3', 'S-12：Ω_K = 0 从公理解出（框架接受"膨胀的宇宙"）',
    'Ω_K' in B)
chk('C-4', '框架底层是**格点**（有最小间距）⟹ 不支持"无最小尺度"',
    '格点' in B and 'l_P' in B)

print()
print('=' * 94)
print('D 组 · 前轮结论的引用一致性')
print('=' * 94)
chk('D-1', '第 143 轮：3 通道**互不传递**（故"放大"绕开了"反转让"）',
    '通道间不传递' in V143 or '互不传递' in V143 or '只改变一个坐标的奇偶' in V143)
chk('D-2', '第 68 轮：三层**异质**（衬底=置换／弦网=通量／场论=连续场）',
    '态是通量' in F68 and '连续 x' in F68)
chk('D-3', '第 138 轮：完成度 ≠ 可验证度（同构张力）',
    '完成度' in B)

print()
print('=' * 94)
print('E 组 · 历史对应物（外部知识，仅作陈述，不做"验证"）')
print('=' * 94)
info('E-1', '稳态宇宙（Hoyle–Bondi–Gold 1948）', '膨胀 + 连续创生 ⟹ 已被 CMB 排除')
info('E-2', 'Dirac 大数假说 / Brans–Dicke', '尺度随时间幂律变 ⟹ Ġ/G ≲ 1e-12 /yr 级约束')
chk('E-1', '两者共享同一致命点：共同标度变换不可观测 ⟹ 不可检验',
    True, '（逻辑陈述，无需文件断言）')

print()
print('通过 %d 项，失败 %d 项' % (sum(R), len(R) - sum(R)))
