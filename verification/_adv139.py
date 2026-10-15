# -*- coding: utf-8 -*-
"""
第 139 轮 · 「是不是理论超前、工具不够」——用**判否理由的分布**回答
方法：把全部负面判定（N 系列）的理由按类型分类并计数。
判据：若判否理由以「对象不存在/错位」为主 ⟹ 不是工具问题；
      若以「算不出/方法学不足」为主 ⟹ 才是工具问题。
"""
import io, sys, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

Q = open('项目台账.md', encoding='utf-8').read()
row = [l for l in Q.split('\n') if l.startswith('| **负面判定**')][0]

# 逐条切分 N-xx
parts = re.split(r'(N-\d+)', row)
items = []
i = 1
while i < len(parts) - 1:
    items.append((parts[i], parts[i+1]))
    i += 2
print('负面判定条目数（本行内）: %d' % len(items))

# 理由分类（关键词 → 类别）
CATS = {
    '① 对象不存在/消失': ['对象消失', '无对象', '没有对象', '对象不是', '无「', '没有「',
                        '不存在', '未定义', '无定义', '不可定义', '不可能被定义'],
    '② 对象错位/载体不符': ['错位', '载体', '无量子态层', '分层居住', '没有量子态',
                          '无 Fock', '无手性', '无势阱', '缺「势'],
    '③ 量级差太远（算得出）': ['数量级', 'dex', '缺口', '稀释', '超上界',
                            '倍 ≈', '差 4', '偏大', '偏低', 'σ'],
    '④ 恒等式/除法/同源（对象是假的）': ['恒等式', '除法', '同源', '减法', '伪问题', '零内容'],
    '⑤ 不独有/外部已有': ['独有性', '文献已知', '已有', '同值', '包含关系', '读数'],
    '⑥ 工具不足/算不出': ['不可算', '算不出', '方法学不足', '无法计算', '未收敛'],
    '⑦ 前提/依据不成立': ['前提', '依据不成立', '未演示', '自撤', '支撑不成立'],
}

hit = collections.Counter()
per = collections.defaultdict(list)
for tag, body in items:
    matched = []
    for cat, kws in CATS.items():
        if any(k in body for k in kws):
            matched.append(cat)
            hit[cat] += 1
    per[tag] = matched

print()
print('=' * 88)
print('判否理由分类统计（同一条可命中多类）')
print('=' * 88)
for cat, n in hit.most_common():
    print('  %-28s %2d 条  (%.0f%%)' % (cat, n, 100.0 * n / len(items)))

print()
print('=' * 88)
print('关键对比：① ② ④（对象类） vs ⑥（工具类）')
print('=' * 88)
obj = hit['① 对象不存在/消失'] + hit['② 对象错位/载体不符'] + hit['④ 恒等式/除法/同源（对象是假的）']
tool = hit['⑥ 工具不足/算不出']
info_ok = obj > tool * 5
print('  对象类合计 %d 条 ｜ 工具类 %d 条' % (obj, tool))
print('  ⟹ 对象类 / 工具类 = %.1f 倍' % (obj / max(tool, 1)))
print()

# 举出「工具类」的那几条（这是需要公平承认的部分）
print('=== 明确以「工具不足/算不出」为由的条目（应公平承认）===')
for tag, cats in per.items():
    if '⑥ 工具不足/算不出' in cats:
        body = dict(items)[tag]
        print('  %s : %s' % (tag, body[:170].replace('\n', ' ')))
print()

# 另外：全清单范围内「方法学不足」的出现
print('=== 全清单「方法学不足」出现次数 ===')
print('  ', Q.count('方法学不足'))
for m in re.finditer('方法学不足', Q):
    print('   ...%s...' % Q[max(0, m.start()-120):m.end()+80].replace('\n', '⏎')[:230])
