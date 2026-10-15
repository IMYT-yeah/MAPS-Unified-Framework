# -*- coding: utf-8 -*-
"""第 134 轮（v2）：论文初稿 → 正式稿 v3.0
剥离对象 = **含「第 N 轮 / Round N」标识的推演工作注**（两种形式：`>` 引用块 ＋ `**【vX.Y…（第 N 轮）】**` 独立段落）
保留对象 = 论文本体：正文、公理/命题/推导标注、**正式版本修订（v1.x/v2.x 补充/撤回/文献对照/诚实标注）**、附录 C（版本说明）、两处「符号约定」、packing 指针、第 133 轮最新外部状态注、标题区
"""
import io, os, re

B = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
SRC = os.path.join(B, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md')
OUT_MAIN = os.path.join(B, 'outputs', '论文_正式稿_v3.0.md')
OUT_APX = os.path.join(B, 'outputs', '论文_技术附录_轮次记录.md')

t = io.open(SRC, encoding='utf-8').read()
L = t.split('\n')

WHITE_1B = {5, 139, 923, 1453, 1663, 2320}   # 白名单块（保留）
APX_ZONE = 2315                                # 原行号 >= 此值 = 附录 C 区域（保留）

ROUND = re.compile(r'(（?第 \d+ 轮|Round \d+)')
def has_round(s):
    return bool(ROUND.search(s))

# ---- 扫描：两类"注"，统一成 (start, end, kind) ----
units = []   # kind: 'blk'（引用块）/'par'（段落式）
i = 0
while i < len(L):
    if L[i].startswith('>'):
        j = i
        while j + 1 < len(L) and L[j + 1].startswith('>'):
            j += 1
        units.append((i, j, 'blk'))
        i = j + 1
    elif L[i].startswith('**【') and has_round(L[i]):
        j = i
        while j + 1 < len(L) and L[j + 1].strip() != '':
            j += 1
        units.append((i, j, 'par'))
        i = j + 1
    else:
        i += 1

keep_set = set()
strip_set = set()
for (i, j, k) in units:
    f1 = i + 1
    if f1 in WHITE_1B or f1 >= APX_ZONE:
        keep_set.add((i, j, k))
    elif k == 'blk' or has_round(L[i]):      # 块：默认剥离；段落：仅含轮号者剥离
        strip_set.add((i, j, k))
    else:
        keep_set.add((i, j, k))
print('单元总数 %d ｜ 保留 %d ｜ 剥离 %d' % (len(units), len(keep_set), len(strip_set)))
n_blk = sum(1 for u in strip_set if u[2] == 'blk')
n_par = sum(1 for u in strip_set if u[2] == 'par')
print('  剥离明细：引用块 %d ＋ 段落式 %d' % (n_blk, n_par))

# ---- 生成 ----
main, apx = [], []
apx += ['# 技术附录：轮次推演注记（%d 条）' % len(strip_set), '',
        '> 本文件是《论文_正式稿_v3.0》的技术附录：原工作底本 `论文初稿_正反物质对风暴统一框架_v2.9.md` 中**含「第 N 轮」标识的推演工作注**（共 %d 条：引用块 %d ＋ 段落 %d）原样保留于此。' % (len(strip_set), n_blk, n_par),
        '> **论文本体内容不在本附录**（公理/命题/推导、正式版本修订 v1.x–v2.9、附录 C 版本说明等均保留在正文）。正文对应位置以 `📎 附 A-nn` 标记。',
        '> ⚠️ **引用正文任何数字前，应先查本附录对应条目的口径注**（本框架的口径限制与更正记录多集中于此）。', '', '---', '']

strip_map = {}
n = 0
i = 0
while i < len(L):
    hit = None
    for (a, b, k) in strip_set:
        if a == i:
            hit = (a, b, k)
            break
    if hit:
        a, b, k = hit
        n += 1
        strip_map[(a, b)] = n
        main.append('> 📎 附 A-%02d' % n)
        kk = a - 1
        while kk >= 0 and not L[kk].startswith('#'):
            kk -= 1
        hdr = L[kk].strip('# ').strip() if kk >= 0 else '(无)'
        head = L[a].lstrip('> ').strip()
        apx.append('## A-%02d ｜ %s' % (n, head[:60] + ('…' if len(head) > 60 else '')))
        apx += ['', '*原位置：L%d–L%d ｜ 所属章节：%s*' % (a + 1, b + 1, hdr[:60]), '']
        apx += L[a:b + 1]
        apx += ['', '---', '']
        i = b + 1
    else:
        main.append(L[i])
        i += 1
assert n == len(strip_set), (n, len(strip_set))
print('已剥离 %d 条' % n)

# ---- 排版规整 ----
def tidy(lines):
    out, blank = [], 0
    for s in lines:
        if s.strip() == '':
            blank += 1
            if blank <= 1:
                out.append('')
        else:
            blank = 0
            out.append(s)
    return out
main = tidy(main)
toc = ['## 目录', '']
for s in main:
    if re.match(r'^## ', s) and not s.startswith('## 目录'):
        toc.append('- ' + s[3:])
    elif re.match(r'^### ', s):
        toc.append('  - ' + s[4:])
toc.append('')
header = [
    '# 正反物质对风暴统一框架（正式稿 v3.0）', '',
    '> **版本**：正式稿 v3.0 ｜ 2026-10-06 ｜ 由工作底本 v2.9 精编：**%d 条含「第 N 轮」标识的推演工作注已剥离至《论文_技术附录_轮次记录.md》**，正文原位留 `📎 附 A-nn` 标记；**论文本体（公理／命题／推导／正式版本修订／附录 C）全部保留**。' % len(strip_set),
    '> ⚠️ **引用正文任何数字前，请先查附录 A 中的对应口径注**（本框架的口径限制与更正记录多集中于此）。',
    '> **定位**：启发式统一框架（参考架构，**非已确立物理**）。', '', '---', '']
p = 0
while p < len(main) and (main[p].strip() == '' or main[p].startswith('# ') or main[p].startswith('>') or main[p].strip() == '---'):
    p += 1
main_final = header + toc + ['---', ''] + main[p:]
io.open(OUT_MAIN, 'w', encoding='utf-8').write('\n'.join(main_final))
io.open(OUT_APX, 'w', encoding='utf-8').write('\n'.join(apx))

# ---- 统计 ----
def stats(s, tag):
    cjk = sum(1 for ch in s if '\u4e00' <= ch <= '\u9fff')
    w = len(re.findall(r"[A-Za-z][A-Za-z\-']*", s))
    print('  %-12s 全字符 %7d ｜ 汉字 %6d ｜ 英文词 %5d ｜ **Word 式 %6d**' % (tag, len(s), cjk, w, cjk + w))
print()
print('=== 字数 ===')
stats(t, '原 v2.9')
m = io.open(OUT_MAIN, encoding='utf-8').read(); a = io.open(OUT_APX, encoding='utf-8').read()
stats(m, '正式稿 v3.0'); stats(a, '技术附录'); stats(m + a, '合计')
# 标记字符占比（粗略：非汉字非空白非 ASCII 字母数字的字符）
mk = sum(1 for ch in m if not ('\u4e00' <= ch <= '\u9fff') and not ch.isalnum() and not ch.isspace())
print('  正式稿中「标记/标点/公式符」字符 ≈ %d（占 %.0f%%）' % (mk, 100 * mk / len(m)))
print()
print('  正文 📎 指针数: %d（应 %d）' % (m.count('📎 附 A-'), len(strip_set)))
print('  附录 ## A- 条目数: %d' % len(re.findall(r'(?m)^## A-\d+', a)))
print('  表格行：原 %d ｜ 正文 %d ｜ 附录 %d' % (
    len([l for l in t.split('\n') if l.startswith('|')]),
    len([l for l in m.split('\n') if l.startswith('|')]),
    len([l for l in a.split('\n') if l.startswith('|')])))
