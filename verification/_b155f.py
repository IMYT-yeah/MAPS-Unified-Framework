#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""第 155 轮 F 组：多值符号清点的剩余项（承接第 152 轮，30 组中仅判定 8 组）"""
import io, sys, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

B = open('论文_正式稿_v3.0.md', encoding='utf-8').read()
L = B.split('\n')

# 抓 SYM =/≈ VAL，SYM 至少 2 字符（避免单字母噪声），VAL 需含小数点或 ×10
pat = re.compile(r'([A-Za-z\u0391-\u03c9][A-Za-z0-9_\u00b2\u00b3\u207b\u2080-\u2089/,()^]{1,18})'
                 r'\s*(?:=|≈)\s*([-\u2212]?\d+(?:\.\d+)?(?:\s*[\u00d7x]\s*10[-\u2212]?\d+)?)')

groups = collections.defaultdict(list)
for i, l in enumerate(L, 1):
    for m in pat.finditer(l):
        sym, val = m.group(1).strip(), m.group(2)
        if '.' not in val and '×10' not in val and 'x10' not in val:
            continue
        groups[sym].append((val, i))

def norm(v):
    v = v.replace('\u2212', '-').replace('\u00d7', 'e').replace('x1', 'e1').replace(' ', '')
    v = v.replace('e', 'e')
    try:
        if 'e' in v:
            a, b = v.split('e')
            return float(a) * 10 ** int(b)
        return float(v)
    except Exception:
        return None

print('=' * 96)
print('F 组 · 多值符号清点：同一符号出现 ≥2 个数值的组')
print('=' * 96)

cands = []
for sym, lst in groups.items():
    vals = {}
    for v, ln in lst:
        vals.setdefault(v, []).append(ln)
    if len(vals) < 2 or len(vals) > 8:
        continue
    nums = [norm(v) for v in vals]
    if any(n is None for n in nums):
        continue
    lo, hi = min(nums), max(nums)
    if lo <= 0:
        rel = float('inf')
    else:
        rel = (hi - lo) / abs(lo)
    cands.append((rel, sym, sorted(vals.items(), key=lambda x: norm(x[0]))))

cands.sort(reverse=True)
print('候选组 %d（值数 2–8，含小数/科学记数）' % len(cands))
print()
print('%-4s %-22s %-9s %s' % ('rel', '符号', '值数', '各值（出现行号）'))
print('-' * 96)
susp = []
for rel, sym, vals in cands:
    tag = ''
    if rel > 0.05:
        tag = '  <== 相对差 > 5%，需人工判定'
        susp.append((rel, sym, vals))
    vs = ' ｜ '.join('%s (L%s)' % (v, ','.join(map(str, lns[:3]))) for v, lns in vals)
    print('%-4s %-22s %-9d %s%s' % (
        ('%.3f' % rel if rel != float('inf') else 'inf'), sym[:22], len(vals), vs[:150], tag))

print()
print('=' * 96)
print('相对差 > 5%% 的组（需逐一判定「合法上下文」vs「未扫下游」）：%d 组' % len(susp))
print('=' * 96)
for rel, sym, vals in susp:
    print()
    print('【%s】 rel=%.3f' % (sym, rel))
    for v, lns in vals:
        for ln in lns[:2]:
            ctx = L[ln - 1]
            j = ctx.find(v)
            print('   %-14s L%-5d ...%s...' % (v, ln, ctx[max(0, j - 75):j + 75]))
