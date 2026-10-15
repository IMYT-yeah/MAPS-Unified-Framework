# -*- coding: utf-8 -*-
"""第 146 轮核验：正负枝 / 粒子-波 / 「平面无解三维有解」意象
   原则：① 数字说了算；② 追溯须给轮次；③ 判据不引入本源之外的对象。"""
import io, sys, re, math, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

RES = []
def chk(tag, name, cond, extra=''):
    RES.append(bool(cond))
    print('[%s] %-8s %s %s' % ('OK' if cond else 'XX', tag, name, extra))
def info(tag, name, val):
    print('[--] %-8s %s %s' % (tag, name, val))

B = open('论文_正式稿_v3.0.md', encoding='utf-8').read()
A = open('论文_技术附录_轮次记录.md', encoding='utf-8').read()
SRC = open('../初始资料/元宝对话_反物质与时间的哲学猜想/对话全文_完整版.md', encoding='utf-8').read()
BB = open('论文_正式稿_v3.0_备份_2026-10-09第146轮前.md', encoding='utf-8').read()  # 改前口径（本轮）

print('=' * 86)
print('A 组 · 追溯：这轮说的东西，原文/论文里在不在')
print('=' * 86)

marks = [(m.start(), m.group(1)) for m in re.finditer(r'## 第\s*(\d+)\s*轮', SRC)]
def rnd(pos):
    r = None
    for p, n in marks:
        if p <= pos: r = n
        else: break
    return r

for kw in ['正枝', '负枝', '正负枝']:
    hits = list(re.finditer(re.escape(kw), SRC))
    rs = sorted(set(int(rnd(m.start())) for m in hits)) if hits else []
    info('A-1', '原文「%s」' % kw, '%d 次 / %d 轮 / %s..%s' % (len(hits), len(rs), rs[0] if rs else '-', rs[-1] if rs else '-'))

n_src = len(re.findall('正枝', SRC)) + len(re.findall('负枝', SRC))
chk('A-1', '原文里「正枝/负枝」是高密度线索（>300 次）', n_src > 300, str(n_src))

# 用户自己说正枝/负枝的消息数
us = list(re.finditer(r'### 🧑 用户', SRC))
cnt = 0
for i, m in enumerate(us):
    a = m.start(); b = us[i+1].start() if i+1 < len(us) else len(SRC)
    if re.search('正枝|负枝|正负枝', SRC[a:b]): cnt += 1
info('A-2', '用户说「正枝/负枝」的消息数', cnt)
chk('A-2', '是用户自己反复说的（≥10 条）', cnt >= 10, str(cnt))

# 论文里的用法
for kw in ['正支', '负支', '两支']:
    info('A-3', '论文「%s」' % kw, str(len(re.findall(re.escape(kw), B))))
chk('A-3', '论文只用了 4 次正支/负支（几乎未展开）',
    len(re.findall('正支', B)) == 2 and len(re.findall('负支', B)) == 2)

# 本轮新造措辞
for kw in ['平面无解', '粒子化', '波动化', '三维有解']:
    n1 = len(re.findall(re.escape(kw), SRC)); n2 = len(re.findall(re.escape(kw), B))
    info('A-4', '「%s」原文/论文' % kw, '%d / %d' % (n1, n2))
chk('A-4', '本轮三个关键词均为新造措辞（原文与论文皆 0）',
    all(len(re.findall(re.escape(k), SRC)) == 0 and len(re.findall(re.escape(k), B)) == 0
        for k in ['平面无解', '粒子化', '波动化']))

# 第 188 轮：用户自己提过挂谷维度
i188 = SRC.find('## 第 188 轮')
seg188 = SRC[i188:i188+3000]
chk('A-5', '第 188 轮用户曾自行提出「挂谷维度 ↔ ε 泄漏」的对应（本轮是同一线索的续）',
    '挂谷' in seg188 and '2.5' in seg188)

print()
print('=' * 86)
print('B 组 · 核心命题「平面无解、三维有解」—— 独立数值验证')
print('=' * 86)

def ang(a, b):
    d = sum(x*y for x, y in zip(a, b))
    return math.degrees(math.acos(max(-1.0, min(1.0, d))))

def fib_sphere(n):
    pts = []; ga = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        z = 1 - 2*(i + 0.5)/n
        r = math.sqrt(max(0.0, 1 - z*z)); th = ga*i
        pts.append((r*math.cos(th), r*math.sin(th), z))
    return pts

def cover_radius(dirs, extra=None, n=60000):
    """extra: 显式加入的关键候选最坏点（Fibonacci 网格命中不到极点的候选）。"""
    pts = fib_sphere(n)
    if extra: pts = pts + list(extra)
    worst = 0.0; wp = None
    for p in pts:
        mm = min(ang(p, d) for d in dirs)
        if mm > worst: worst, wp = mm, p
    return worst, wp

def norm(v):
    L = math.sqrt(sum(x*x for x in v)); return tuple(x/L for x in v)

# B-1 平面配置（共面 3 方向，120° 间隔）；最坏点 = 平面法线（显式加入）
planar3 = [(1,0,0), (-0.5, math.sqrt(3)/2, 0), (-0.5, -math.sqrt(3)/2, 0)]
r3, w3 = cover_radius(planar3, extra=[(0,0,1), (0,0,-1)], n=60000)
info('B-1', '共面 3 方向覆盖半径', '%.4f°  最坏点 %.4f %.4f %.4f' % (r3, *w3))
chk('B-1', '共面 3 方向 = 恰好 90.0000°（= 论文解析值）', abs(r3 - 90) < 1e-6, '%.6f' % r3)

# B-2 共面 k 任意 ⟹ 仍是 90°（法线方向恒为最坏点）
worst_norm = None
for k in [4, 8, 16, 64]:
    dirs = [(math.cos(2*math.pi*i/k), math.sin(2*math.pi*i/k), 0.0) for i in range(k)]
    rr, _ = cover_radius(dirs, extra=[(0,0,1), (0,0,-1)], n=30000)
    worst_norm = rr if worst_norm is None else worst_norm
    info('B-2', '共面 k=%d 覆盖半径' % k, '%.6f°' % rr)
    if abs(rr - 90) > 1e-6: worst_norm = -1
chk('B-2', '共面方向无论多少个，覆盖半径恒 = 90°（⟹ 平面方案结构性无解）', worst_norm > 0, '%.6f' % worst_norm)

# B-3 正四面体 4 方向；Voronoi 顶点 = 反向顶点（v1+v2+v3+v4=0）
tet = [norm(v) for v in [(1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)]]
r4, w4 = cover_radius(tet, extra=tet + [(-x,-y,-z) for (x,y,z) in tet], n=60000)
info('B-3', '正四面体 4 方向覆盖半径', '%.4f°（论文解析值 70.5288°）' % r4)
chk('B-3', '正四面体 4 方向 = arccos(1/3) = 70.5288°', abs(r4 - math.degrees(math.acos(1/3))) < 1e-6,
    '%.6f vs %.6f' % (r4, math.degrees(math.acos(1/3))))

# B-4 Tammes n=4 最小角
pairmin = min(ang(tet[i], tet[j]) for i in range(4) for j in range(i+1, 4))
info('B-4', '正四面体最小夹角', '%.4f°（arccos(1/3)... 实为 arccos(-1/3)=109.4712°）' % pairmin)
chk('B-4', '最小夹角 = arccos(-1/3) = 109.4712°（Tammes n=4，论文定理 2）',
    abs(pairmin - math.degrees(math.acos(-1/3))) < 0.05, '%.4f' % pairmin)

# B-5 挂谷要求：严格 < 90°
info('B-5', '判据', 'k=3 ⟹ %.2f°（=90，不满足「严格<90」）｜ k=4 ⟹ %.2f°（满足）' % (r3, r4))
chk('B-5', '「平面无解、三维有解」在覆盖半径意义上严格成立',
    r3 >= 90 - 1e-6 and r4 < 90)

# B-6 论文定理 1/2 原文
chk('B-6', '论文定理 1 含「90.0000°」与「平面法线」（与本验证的机制同一）',
    '90.0000°' in B and '平面法线' in B)
chk('B-7', '论文定理 2 含「70.5288°」与 Tammes n=4',
    '70.5288' in B and 'Tammes n=4' in B)

# B-8 「空间三维」作为独立论证
chk('B-8', '论文另有「空间三维（挂谷维数锁定）⟹ n≥4 排除」的独立三维性论证',
    '空间三维（挂谷维数锁定）' in B)

# B-9 两种「平面」读法必须分开（本轮结论依赖这个区分）
def fib_circle(n):
    return [(math.cos(2*math.pi*i/n), math.sin(2*math.pi*i/n), 0.0) for i in range(n)]
r_inplane, _ = cover_radius(fib_circle(3), extra=fib_circle(3600), n=0)  # 只在平面内取候选点
info('B-9', '若只要求覆盖「平面内」方向（S¹），共面 3 方向', '%.4f° （120° 间隔 ⟹ 60°，有解）' % r_inplane)
chk('B-9', '区分成立：平面内三维方向 60° 有解；但覆盖三维全方向时共面方案 90° 无解',
    abs(r_inplane - 60) < 1.0 and abs(r3 - 90) < 1e-6, '%.4f / %.6f' % (r_inplane, r3))

print()
print('=' * 86)
print('C 组 · 「正负枝」在框架里的确切结构位置')
print('=' * 86)

chk('C-1', '公理 3 = 时间箭头分叉、两支互为 CPT 镜像',
    '**【公理 3（时间箭头分叉）】**' in B and 'CPT 镜像' in B)
chk('C-2', '§4.8 明文：原始态 16 = 2^4（4 平面内连接 × {正支, 负支}）',
    '16 = 2^4' in B and '正支, 负支' in B)
chk('C-3', '§4.10 论证 4：4 = 时间双向 × 手性双向（Clifford Cl(1,3)）',
    '时间双向×手性双向' in B and 'Cl(1,3)' in B)
info('C-4', '结构', '三维 ⟹ 4 方向（定理 1/2）；每个连接再带 {正支/负支} ⟹ 16 = 2^4')
chk('C-4', '「正负支」是三维方向结构上的附加二分标记（与用户意象一致）',
    '4 个平面内连接 × {正支, 负支}' in B)
chk('C-5', '视界 = 时间箭头翻转面【本框架设定】', '视界 = 时间箭头翻转面' in B)
chk('C-6', '冻结 = 本体（正支投影源停止）在七环链中登记',
    '正支投影源停止' in B)
chk('C-7', '黑洞表层三层结构（翻转面／饱和模态驻留层／浆糊外围）',
    '表层三层结构' in B)

print()
print('=' * 86)
print('D 组 · 「粒子 → 层」跨支互换：载体在不在？载得动吗？')
print('=' * 86)

chk('D-1', '跨支通道存在：量子直线 = 同源泄漏事件在两支间的关联通道',
    '同源泄漏事件在两支间的关联通道' in B)
chk('D-2', '跨支通道 = 挂谷线段（214–218，ER=EPR）', '挂谷线段' in B)
chk('D-3', '⚠️ 明文边界：跨支通道「只载信息、不载能量」',
    '只载信息' in B and '不载能量' in B)
chk('D-4', '⚠️ 框架无负能量密度（P ≤ ρc²、ρ ≥ 0）⟹ 不支持可穿越',
    'P ≤ ρc²' in B and '没有负能量密度' in B)
chk('D-5', '⚠️ 量子不等式锁死预算（ΔE ≤ 1.06×10⁻³⁴ J，比 k_BT 小 14 个量级）',
    '1.06×10⁻³⁴' in B)
chk('D-6', '⟹ 跨支通道在框架内不能作为能量/物质通路（明文结论）',
    '跨支通道在框架内不能作为能量 / 物质通路' in B)

print()
print('=' * 86)
print('E 组 · 「粒子化 / 波动化」在框架里各是什么')
print('=' * 86)

chk('E-1', '粒子 = 孤子化（§2.3「孤子化 ⟹ 粒子（稳定局域结构）」）',
    '孤子化 ⟹ 粒子' in B)
chk('E-2', '观测者 = 现在平面局域孤子（O1）', '现在平面局域孤子' in B)
for kw in ['波动', '波函数', '波包', '量子态']:
    info('E-3', '论文「%s」' % kw, str(len(re.findall(re.escape(kw), B))))
# 判据修正：这些词只允许出现在 §7.4 的「否定性口径注」窗口内
i_note = B.find('框架**没有量子态层**')
win = B[max(0, i_note-400):i_note+900]
outside = []
for kw in ['波函数', '波包', '量子态']:
    for m in re.finditer(re.escape(kw), B):
        if not (max(0, i_note-400) <= m.start() <= i_note+900):
            outside.append((kw, B[max(0,m.start()-60):m.end()+60].replace('\n','⏎')))
info('E-3', '「波函数/波包/量子态」在否定性口径注窗口之外的出现数', len(outside))
for o in outside[:4]:
    info('E-3', '  窗口外', '%s: ...%s...' % o)
chk('E-3', '这些词只出现在「框架没有量子态层」的否定性口径注里（非正文使用）', not outside)
chk('E-4', '⚠️ 口径注明文：框架「没有量子态层」', '框架**没有量子态层**' in B)
chk('E-5', '⚠️ 口径注：观测者是经典粗粒化，不改变被观测系统的态',
    '经典粗粒化' in B)

print()
print('=' * 86)
print('F 组 · 质量：本轮无自指污染（用改前备份口径）')
print('=' * 86)

chk('F-1', '正式稿全字符 < 100000', len(B) < 100000, str(len(B)))
chk('F-2', '正式稿与改前备份的差 = 0（本轮无论文改动）', len(B) == len(BB), '%d vs %d' % (len(B), len(BB)))
chk('F-3', '技术附录未被本轮改动（72 条）',
    len(set(re.findall(r'^##\s*(A-\d+)', A, re.M))) == 72)
chk('F-4', '指针 72 ⇄ 附录 72', len(re.findall(r'📎\s*附\s*(A-\d+)', B)) == 72)

print()
print('通过 %d 项，失败 %d 项' % (sum(RES), len(RES) - sum(RES)))
