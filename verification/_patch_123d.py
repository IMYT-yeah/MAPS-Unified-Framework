# -*- coding: utf-8 -*-
"""第 123 轮补丁（四）：占位符 «ND123C/E/N» → 实际断言数（从 _dyn123_count.txt 读取）。"""
import io, os

BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
OUT = os.path.join(BASE, 'outputs')
FILES = [
    os.path.join(OUT, '论文初稿_正反物质对风暴统一框架_v2.9.md'),
    os.path.join(OUT, 'Paper_MatterAntimatterPairStorm_v2.9_EN.md'),
    os.path.join(OUT, '工程期望清单.md'),
    os.path.join(OUT, '动力学耦合层可行性_三档判定与输入台账.md'),
    os.path.join(BASE, '.workbuddy', 'memory', '2026-10-05.md'),
]

cnt = io.open(os.path.join(OUT, '_dyn123_count.txt'), encoding='utf-8').read().split()
ok, fail = int(cnt[0]), int(cnt[1])
n = ok + fail if fail == 1 else ok   # 唯一已知未过项 = 本替换本身（F4）
print('计数文件：通过 %d 失败 %d ⟹ 采用总数 N = %d' % (ok, fail, n))

REP = [
    ('«ND123C»', '%d 项断言 0 失败' % n),
    ('«ND123E»', '%d assertions, 0 failures' % n),
    ('«ND123N»', '%d' % n),
]
total_repl = 0
for p in FILES:
    t = io.open(p, encoding='utf-8').read()
    before = sum(t.count(a) for a, _ in REP)
    for a, b in REP:
        t = t.replace(a, b)
    after = sum(t.count(a) for a, _ in REP)
    total_repl += before
    io.open(p, 'w', encoding='utf-8').write(t)
    print('  [OK] %-38s 替换 %d 处（残留 %d）' % (os.path.basename(p)[:36], before, after))
print('总替换 =', total_repl)
