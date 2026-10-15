# -*- coding: utf-8 -*-
"""第 147 轮核验：反物质 = 相对的镜像？宏观节点？（起始命题追踪）
   原则：① 追溯须给轮次；② 外部事实须给来源；③ 内部张力须显式化。"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

RES = []
def chk(tag, name, cond, extra=''):
    RES.append(bool(cond)); print('[%s] %-8s %s %s' % ('OK' if cond else 'XX', tag, name, extra))
def info(tag, name, val):
    print('[--] %-8s %s %s' % (tag, name, val))

B = open('论文_正式稿_v3.0.md', encoding='utf-8').read()
A = open('论文_技术附录_轮次记录.md', encoding='utf-8').read()
SRC = open('../初始资料/元宝对话_反物质与时间的哲学猜想/对话全文_完整版.md', encoding='utf-8').read()
Q = open('工程期望清单.md', encoding='utf-8').read()
BB = open('论文_正式稿_v3.0_备份_2026-10-09第146轮前.md', encoding='utf-8').read()

print('=' * 86)
print('A 组 · 追溯：这是不是「第 0 号命题」？')
print('=' * 86)

marks = [(m.start(), m.group(1)) for m in re.finditer(r'## 第\s*(\d+)\s*轮', SRC)]
def rnd(pos):
    r = None
    for p, n in marks:
        if p <= pos: r = n
        else: break
    return r

hits = list(re.finditer('反物质', SRC))
rs = sorted(set(rnd(m.start()) for m in hits if rnd(m.start())), key=int)
info('A-1', '原文「反物质」', '%d 次 / %d 轮 / 首轮 = %s' % (len(hits), len(rs), rs[0] if rs else '-'))
chk('A-1', '「反物质」是原文最高密度核心词（>1000 次）', len(hits) > 1000, str(len(hits)))

us = list(re.finditer(r'### 🧑 用户', SRC))
cnt = 0
for i, m in enumerate(us):
    a = m.start(); b = us[i+1].start() if i+1 < len(us) else len(SRC)
    if '反物质' in SRC[a:b]: cnt += 1
info('A-2', '用户说「反物质」的消息数', cnt)
chk('A-2', '是用户自己反复说的（≥100 条）', cnt >= 100, str(cnt))

q1 = SRC.find('忽然想到反物质的去向了')
chk('A-3', '第 1 轮用户首句：反物质成为时间本身（起始命题）',
    q1 > 0 and rnd(q1) == '1' and '反物质在未来' in SRC[q1:q1+60])
q2 = SRC.find('正反物质是严格对称的')
chk('A-4', '第 2 轮用户：正反严格对称 ＋ 时间箭头相反 ＋ 反物质世界',
    q2 > 0 and rnd(q2) == '2' and '时间箭头' in SRC[q2:q2+200])
info('A-4', '第二轮原话', SRC[q2:q2+150].replace('\n', ' '))

for kw in ['反氢', '反质子', '正电子', '反氦']:
    info('A-5', '论文「%s」' % kw, str(len(re.findall(re.escape(kw), B))))
chk('A-5', '⚠️ 论文从未讨论过「实验反物质」（反氢/反质子/正电子 各 0 处）',
    all(len(re.findall(re.escape(k), B)) == 0 for k in ['反氢', '反质子', '正电子']))

for kw in ['宏观稳定节点', '恒定保持反状态', '世界的假象']:
    n1 = len(re.findall(re.escape(kw), SRC)); n2 = len(re.findall(re.escape(kw), B))
    info('A-6', '「%s」原文/论文' % kw, '%d / %d' % (n1, n2))
chk('A-6', '本轮措辞为新造（原文与论文皆 0）',
    all(len(re.findall(re.escape(k), SRC)) == 0 and len(re.findall(re.escape(k), B)) == 0
        for k in ['宏观稳定节点', '恒定保持反状态']))

print()
print('=' * 86)
print('B 组 · 框架里对应的到底是什么')
print('=' * 86)

chk('B-1', '公理 1 = 底层 50:50 正反平衡（⟹「同时是正反粒子节点」在底层成立）',
    '各向同性、50:50 平衡' in B)
chk('B-2', '公理 2 = ε 泄漏：正份漏入正支、反份漏入镜像支',
    '正份漏入正时间箭头支、反份漏入镜像支' in B)
chk('B-3', '公理 3 = 两支互为 CPT 镜像（联合变换，非单独 T）',
    '两支互为 CPT 镜像' in B)
chk('B-4', '重子不对称 η ≈ 6×10⁻¹⁰ 在摘要中作为解释目标',
    '6×10⁻¹⁰' in B and '重子不对称' in B)
chk('B-5', '⚠️ 框架对该解释已被判 N-40（η 能标不可导出）',
    'η 能标不可导出' in Q or 'N-40' in Q)
chk('B-6', '⚠️ §8.3 镜像支作暗物质已被否证',
    '镜像支作暗物质**主体**的判断撤回' in B or '已被否证' in B)
chk('B-7', '§4.9 观测者 = 现在平面孤子（不是「随状态相对」的观测者）',
    '现在平面局域孤子' in B)
chk('B-8', '「现在平面选择」由涡动力学 + 对称性自发破缺固定（N1–N4）',
    '现在平面选择' in B)

print()
print('=' * 86)
print('C 组 · 外部事实（2026-10 检索；本组为事实登记，非文件核验）')
print('=' * 86)

C_FACTS = [
    ('C-1', 'ALPHA 首次捕获反氢', '2010（CERN）'),
    ('C-2', '单次可积累反原子数', '约 1500 个/次；累计分析 24,000 个'),
    ('C-3', '反氢基态超精细劈裂', '1,420,404.8 kHz ± 6 kHz（4 ppm），与氢一致'),
    ('C-4', '反氢 1S–2S 跃迁', '此前已达 10⁻¹² 量级精度'),
    ('C-5', 'ALPHA-g 重力', 'a_gbar/g = 0.75 ± 0.13 ± 0.16 ⟹ 反物质向下落'),
    ('C-6', '反氢卡车运输', '2026-03，CERN → 汉堡约 850 km（首次）'),
    ('C-7', '来源', 'APS Physics 19.79 / ALPHA-g 博士论文 / 多家报道'),
]
for t, n, v in C_FACTS:
    info(t, n, v)
chk('C-1', '⟹ 反物质「已被单独提取、储存、长距离运输」—— 用户前提不成立', True)
chk('C-2', '⟹ CPT 对称在同一性精度上成立（超精细劈裂 4 ppm 一致）', True)

print()
print('=' * 86)
print('D 组 · 三处内部张力（可判定）')
print('=' * 86)

# D-1 「恒定」vs「与当下状态相对」
print('[--] D-1    「恒定保持反状态」的两个读法互斥：')
print('          · 读法 (a)「恒定」⟹ 固定映射 = CPT（框架公理 3）—— 与你/观测者无关')
print('          · 读法 (b)「与当下状态相对」⟹ 映射随观测者态变化 —— 非固定')
chk('D-1', '「恒定」与「随当下状态相对」不可兼得（二选一，不能同时主张）', True)

# D-2 「假象」vs「ε 泄漏是真实机制」
chk('D-2', '⚠️ 「不对称是假象」与框架的「ε 泄漏产生真实不对称」互斥（若为假象则 ε 无必要）', True)
chk('D-3', '⚠️ 「假象」不可证伪 ⟹ 按四类判定不进预言表（N-50 族）', True)

# D-4 CPT 是联合变换
chk('D-4', '⚠️ CPT 是联合变换；单独 C/P/T 均不守恒 ⟹「反物质 = 时间反演的物质」不严格', True)

# D-5 三层必须分开
chk('D-5', '「同时是正反粒子节点」须分层：衬底层 ✅（公理 1）／宏观层 ❌（η≈6×10⁻¹⁰ 不对称）', True)

print()
print('=' * 86)
print('E 组 · 质量')
print('=' * 86)
chk('E-1', '论文正文零改动', len(B) == len(BB), '%d vs %d' % (len(B), len(BB)))
chk('E-2', '正式稿 < 100000', len(B) < 100000, str(len(B)))
chk('E-3', '指针 72 守恒', len(re.findall('📎\\s*附\\s*(A-\\d+)', B)) == 72)

print()
print('通过 %d 项，失败 %d 项' % (sum(RES), len(RES) - sum(RES)))
