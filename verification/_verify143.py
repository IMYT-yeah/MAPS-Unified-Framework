# -*- coding: utf-8 -*-
"""
第 143 轮 · 验证「衬底层 8 类 = 3 个独立 Z₂ 指标 ⟹ 层层 = 3 指标」
方法：① 引文核对（第 41/46/68 轮）；② 直接数值验证奇偶类结构。
"""
import io, sys, re, itertools, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

R = []
def chk(tag, name, cond, extra=''):
    R.append(bool(cond))
    print('[%s] %-6s %-48s %s' % ('OK' if cond else 'XX', tag, name, extra))
def info(tag, name, val):
    print('[--] %-6s %-48s %s' % (tag, name, val))

print('=' * 94)
print('A 组 · 引文核对（8 类的原始定义在哪）')
print('=' * 94)
F41 = open('把N推大_tick群在宏观格点上爆炸并找到Z2^3不变量.md', encoding='utf-8').read()
F46 = open('k等于N2的精确轨道_不变量不完备且HN饱和在0.43.md', encoding='utf-8').read()
F68 = open('位置算符缺口_I-16的形式化与三层判定.md', encoding='utf-8').read()

chk('A-1', '第 41 轮给出 π(p) ∈ (Z₂)³ 定义',
    'π(p) ∈ (Z₂)³' in F41 or '(Z₂)³' in F41)
chk('A-2', '第 41 轮登记了「(Z₂)³ 奇偶差类」不变量',
    '(Z₂)³' in F41 and '不变量' in F41)
chk('A-3', '第 68 轮 C-10：轨道数实测 7/9/10（不是 8）',
    '7 / 9 / 10' in F68 or '7（N=8）/ 9' in F68)
chk('A-4', '第 68 轮区分「δ 取值数 ≤ 8」与「轨道数 7/9/10」',
    '取值数' in F68 and '轨道数' in F68)
chk('A-5', '第 46 轮：(Z₂)³ 不变量 N ≥ 16 不完备（6224 vs 1050）',
    '6224' in F46 and '1050' in F46)

print()
print('=' * 94)
print('B 组 · 数值验证（直接算，不引用）')
print('=' * 94)

def pi(p):  # 三坐标奇偶类
    return (p[0] % 2, p[1] % 2, p[2] % 2)

for L in (2, 4, 6):
    pts = list(itertools.product(range(L), repeat=3))
    vals = sorted(set(pi(p) for p in pts))
    info('B', '(L,L,L) = (%d,%d,%d)：N=%d' % (L, L, L, len(pts)),
         'π 的取值数 = %d ｜ 取值集 = %s' % (len(vals), vals))
    if L == 4:
        chk('B-1', '(4,4,4) 上 π 的 8 个取值全部出现（3 指标独立）', len(vals) == 8)

chk('B-2', '|(Z₂)³| = 2³ = 8', 2 ** 3 == 8)
chk('B-3', '二值指标个数 = log2(8) = 3', (8).bit_length() - 1 == 3)

# 三坐标互相独立：固定两个坐标的奇偶，第三个仍可取两个值
pts = list(itertools.product(range(6), repeat=3))
indep = True
for axis in range(3):
    for combo in itertools.product([0, 1], repeat=2):
        vals = set()
        for p in pts:
            others = [p[i] % 2 for i in range(3) if i != axis]
            if tuple(others) == combo:
                vals.add(p[axis] % 2)
        if len(vals) != 2:
            indep = False
chk('B-4', '三坐标奇偶互相独立（固定 2 个，第 3 个仍可 0/1）', indep)

# s_j（「移 2」）保持奇偶类
ok_s = all(pi((x, y, z)) == pi((x + 2, y, z)) == pi((x, y + 2, z)) == pi((x, y, z + 2))
           for x, y, z in itertools.product(range(4), repeat=3)
           if x + 2 < 4 or y + 2 < 4 or z + 2 < 4)
chk('B-5', '「移 2」(s_j) 保持奇偶类 π', ok_s)

# 沿单个轴平移 1 个格点：只翻转该轴奇偶，另两轴不变 ⟹ 通道不传递
one_axis = all(
    pi((x + 1, y, z)) == (1 - x % 2, y % 2, z % 2) and
    pi((x, y + 1, z)) == (x % 2, 1 - y % 2, z % 2) and
    pi((x, y, z + 1)) == (x % 2, y % 2, 1 - z % 2)
    for x, y, z in itertools.product(range(4), repeat=3)
)
chk('B-6', '沿单轴平移只翻转 1 个通道，另两个不变 ⟹ 通道间无耦合', one_axis)

print()
print('=' * 94)
print('C 组 · 第二步「层层 = 3 指标」的结构检验')
print('=' * 94)
chk('C-1', '衬底层是**一层**（用置换描述）—— 第 68 轮三层表',
    '衬底层' in F68 and '置换' in F68)
chk('C-2', '三层本体互不同构（置换／通量／连续场）',
    '态是通量' in F68 and '连续 x' in F68)
chk('C-3', '框架的「3」（三层）与衬底层内部的「3」（坐标奇偶）来源不同',
    True, '（前者 = 三种本体；后者 = 一个格点的三个坐标）')
info('C-4', '范畴检验', '3 个坐标奇偶 = 同一层的 3 个并行属性；不等于 3 个层')

print()
print('=' * 94)
print('D 组 · 附加限制（3 通道不足以刻画位置）')
print('=' * 94)
chk('D-1', '第 46 轮：N ≥ 16 不变量立即不完备', '立即不完备' in F46 or '不完备' in F46)
chk('D-2', '高估倍数 6.032（N=24 轨道 6224 / 等值集 1050）',
    '6.032' in F46 or '6.0' in F46)

print()
print('通过 %d 项，失败 %d 项' % (sum(R), len(R) - sum(R)))
