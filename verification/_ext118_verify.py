# -*- coding: utf-8 -*-
"""第 118 轮（元任务·对外扫描）核验：E118-1…（两段式取证）"""
import io, os

BASE = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
P = dict(
    MEMO=os.path.join(BASE, 'outputs', '外部输入清单_可接入的活问题与渠道_2026-10.md'),
    MEMO_H=os.path.join(BASE, 'outputs', '外部输入清单_可接入的活问题与渠道_2026-10.html'),
    LIST=os.path.join(BASE, 'outputs', '工程期望清单.md'),
    HO=os.path.join(BASE, '环境交接说明.md'),
    MEM=os.path.join(BASE, '.workbuddy', 'memory', 'MEMORY.md'),
    LOG=os.path.join(BASE, '.workbuddy', 'memory', '2026-10-04.md'),
    ZH=os.path.join(BASE, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md'),
)
B = dict(
    LIST=os.path.join(BASE, 'outputs', '工程期望清单_备份_2026-10-04第118轮前.md'),
    HO=os.path.join(BASE, '环境交接说明_备份_2026-10-04第118轮前.md'),
)
rd = lambda p: io.open(p, encoding='utf-8').read()
OK, FAIL = 0, 0
def chk(tag, cond, msg):
    global OK, FAIL
    if cond: OK += 1; print('  [OK] %-9s %s' % (tag, msg))
    else: FAIL += 1; print('  [XX] %-9s %s' % (tag, msg))

cur = {k: rd(v) if os.path.exists(v) else '' for k, v in P.items()}
bak = {k: rd(v) if os.path.exists(v) else '' for k, v in B.items()}

print('=== E118-1 备忘录 ===')
chk('E118-1a', len(cur['MEMO']) > 3000, '备忘录存在（%d 字符）' % len(cur['MEMO']))
FACTS = ['2511.13471', '2605.27221', '2511.10631', '2607.09310', '2606.27429', '2608.28037',
         '2608.21222', '天琴二号', '2035', 'I-17', '第 73 轮判据', '推荐顺序', '不计入总账']
for s in FACTS:
    chk('E118-1b', s in cur['MEMO'], '备忘录含 %s' % s)
chk('E118-1c', 'Yilmaz–Rosen' in cur['MEMO'] and 'Papapetrou 1954' in cur['MEMO'],
    '已把「度规 = Yilmaz–Rosen/Papapetrou」登记在案（防重复发现）')

print('=== E118-2 清单（两段式）===')
chk('E118-2a', '| **第 118 轮**（**元任务 · 对外扫描**）' in cur['LIST'] and '（不计入总账）' in cur['LIST'],
    '第 118 轮行存在 + 不计入总账')
chk('E118-2b', '第 118 轮' not in bak['LIST'], '补丁前无第 118 轮行（取证）')
chk('E118-2c', '**81 条**' in cur['LIST'] and '**81 条**' in bak['LIST'],
    '撤回计数未被本轮改动（仍 81 条，元任务不计账）')

print('=== E118-3 交接说明（两段式）===')
chk('E118-3a', '**当前建议（第 118 轮后 · 对外扫描）**' in cur['HO'], '§七 新条目')
chk('E118-3b', '**（历史，第 117 轮后）**' in cur['HO'] and '**（历史，第 117 轮后）**' not in bak['HO'],
    '117 条目改历史（补丁前仍为当前）')
chk('E118-3c', '外部输入清单' in cur['HO'] and '外部输入清单' not in bak['HO'],
    '§七 指向清单文件（两段式）')

print('=== E118-4 MEMORY / 日志 ===')
chk('E118-4a', '118 外部输入扫描' in cur['MEM'] and len(cur['MEM']) <= 3000,
    'MEMORY 含 118 记录且 ≤3000（%d 字符）' % len(cur['MEM']))
chk('E118-4b', '第 118 轮' in cur['LOG'] and '外部输入清单' in cur['LOG'], '日志含第 118 轮段')
chk('E118-4c', '无新物理' in cur['LOG'], '日志写明无新物理')

print('=== E118-5 论文未被本轮改动 ===')
chk('E118-5a', '外部输入清单' not in cur['ZH'], '论文 ZH 不含本轮内容（元任务不入论文）')

print('=== E118-6 HTML 快照 ===')
chk('E118-6a', os.path.exists(P['MEMO_H']) and os.path.getsize(P['MEMO_H']) > 5000,
    '备忘录 HTML 快照存在（%d 字节）' % (os.path.getsize(P['MEMO_H']) if os.path.exists(P['MEMO_H']) else 0))

print('')
print('=' * 60)
print('通过 %d 项，失败 %d 项' % (OK, FAIL))
