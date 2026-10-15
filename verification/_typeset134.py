# -*- coding: utf-8 -*-
"""第 134 轮：论文初稿 → 正式稿 v3.0（正文精编 ＋ 轮次注剥离）
产出：
  1) outputs/论文_正式稿_v3.0.md        —— 正文（剥离 69 个历史块，原位留指针）
  2) outputs/论文_技术附录_轮次记录.md   —— 69 块原文（编号 A-01…A-69）
校验：块数守恒、字符守恒、Word 字数、悬空引用扫描
"""
import io, os, re

B = r'C:\Users\Administrator\Desktop\2026-08-20-21-43-34'
SRC = os.path.join(B, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md')
OUT_MAIN = os.path.join(B, 'outputs', '论文_正式稿_v3.0.md')
OUT_APX = os.path.join(B, 'outputs', '论文_技术附录_轮次记录.md')

t = io.open(SRC, encoding='utf-8').read()
L = t.split('\n')

# ---- 1) 重建块列表 ----
blocks = []
i = 0
while i < len(L):
    if L[i].startswith('>'):
        j = i
        while j + 1 < len(L) and L[j + 1].startswith('>'):
            j += 1
        blocks.append((i, j))
        i = j + 1
    else:
        i += 1
print('块总数:', len(blocks))

# ---- 2) 白名单（按起始行号，1-based 打印用；内部 0-based）----
WHITE_1B = {5, 139, 923, 1453, 1663, 2320}
starts = [b[0] + 1 for b in blocks]
for w in WHITE_1B:
    assert w in starts, '白名单行 %d 不是块起点！' % w
print('白名单命中:', len(WHITE_1B), '块')

# ---- 3) 生成正文与附录 ----
main, apx = [], []
apx.append('# 技术附录：轮次注记记录（原 v2.9 正文中的 69 个引用块）')
apx.append('')
apx.append('> 本文件是《论文_正式稿_v3.0》的**技术附录**：原工作底本 `论文初稿_正反物质对风暴统一框架_v2.9.md` 正文中嵌入的**全部历史轮次注记 / 口径注 / 更正记录 / 验证细节**（69 块）原样保留于此。')
apx.append('> 正文对应位置以 `📎 附 A-nn` 标记。**引用正文任何数字前，应先查本附录对应条目的口径注。**')
apx.append('')
apx.append('---')
apx.append('')

kept, moved = 0, 0
n_apx = 0
i = 0
while i < len(L):
    if L[i].startswith('>'):
        j = i
        while j + 1 < len(L) and L[j + 1].startswith('>'):
            j += 1
        first1b = i + 1
        if first1b in WHITE_1B:
            main.extend(L[i:j + 1])
            kept += 1
        else:
            n_apx += 1
            moved += 1
            # 正文指针
            main.append('> 📎 附 A-%02d' % n_apx)
            # 附录条目：找上方标题
            k = i - 1
            while k >= 0 and not L[k].startswith('#'):
                k -= 1
            hdr = L[k].strip('# ').strip() if k >= 0 else '(无)'
            head = L[i].lstrip('> ').strip()
            apx.append('## A-%02d ｜ %s' % (n_apx, head[:60] + ('…' if len(head) > 60 else '')))
            apx.append('')
            apx.append('*原位置：L%d–L%d ｜ 所属章节：%s*' % (first1b, j + 1, hdr[:60]))
            apx.append('')
            apx.extend(L[i:j + 1])
            apx.append('')
            apx.append('---')
            apx.append('')
        i = j + 1
    else:
        main.append(L[i])
        i += 1
print('保留 %d 块 ｜ 移出 %d 块' % (kept, moved))
assert kept + moved == len(blocks)
assert moved == n_apx

# ---- 4) 正文排版规整 ----
def tidy(lines):
    out = []
    blank = 0
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
# 头部：版本说明 + 目录
toc = ['## 目录', '']
for s in main:
    if re.match(r'^## ', s) and not s.startswith('## 目录'):
        toc.append('- ' + s[3:])
    elif re.match(r'^### ', s):
        toc.append('  - ' + s[4:])
toc.append('')
header = [
    '# 正反物质对风暴统一框架（正式稿 v3.0）',
    '',
    '> **版本**：正式稿 v3.0 ｜ 2026-10-06 ｜ 由工作底本 v2.9 精编（正文为科学内容主体；**69 条历史轮次注记／口径注／更正记录已剥离至《论文_技术附录_轮次记录.md》**，正文原位留 `📎 附 A-nn` 指针）。',
    '> ⚠️ **引用正文任何数字前，请先查附录 A 中的对应口径注**（本框架的诚实边界多集中于此）。',
    '> **定位**：启发式统一框架（参考架构，**非已确立物理**）。',
    '',
    '---',
    '',
]
# 去掉原文件前几行的旧头（# 标题 + v2.8 注 + 空行 + ---），保留其余
p = 0
while p < len(main) and (main[p].strip() == '' or main[p].startswith('# ') or main[p].startswith('>') or main[p].strip() == '---'):
    p += 1
main_final = header + toc + ['---', ''] + main[p:]
print('旧头部剔除 %d 行' % p)

io.open(OUT_MAIN, 'w', encoding='utf-8').write('\n'.join(main_final))
io.open(OUT_APX, 'w', encoding='utf-8').write('\n'.join(apx))
print('已写：', OUT_MAIN)
print('已写：', OUT_APX)

# ---- 5) 校验与统计 ----
def stats(s, tag):
    cjk = sum(1 for ch in s if '\u4e00' <= ch <= '\u9fff')
    w = len(re.findall(r"[A-Za-z][A-Za-z\-']*", s))
    print('  %-12s 全字符 %7d ｜ 汉字 %6d ｜ 词 %5d ｜ **Word 式 %6d**' % (tag, len(s), cjk, w, cjk + w))
    return len(s), cjk + w

print()
print('=== 字数统计 ===')
c0, w0 = stats(t, '原 v2.9')
m = io.open(OUT_MAIN, encoding='utf-8').read()
a = io.open(OUT_APX, encoding='utf-8').read()
c1, w1 = stats(m, '正式稿 v3.0')
c2, w2 = stats(a, '技术附录')
c3, w3 = stats(m + a, '两者合计')
print()
print('守恒检查：原 %d vs 合计 %d ⟹ 差 %+d（应 >0 且不大：指针行+头部+附录题头）' % (c0, c3, c3 - c0))

# 悬空引用扫描（正文里可能残留「上一条/见上/上注」）
print()
print('=== 悬空引用扫描（正文中「上一条/见上/上述注/前注」）===')
cnt = 0
for k, s in enumerate(m.split('\n'), 1):
    if re.search(r'(上一条|见上(一)?条|上述注|前注)', s):
        print('  L%d: %s' % (k, s[:110]))
        cnt += 1
print('  共 %d 处' % cnt)
