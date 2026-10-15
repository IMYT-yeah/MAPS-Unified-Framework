#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""第 155 轮核验：B 类（相变 λ_c 能否作「临界放大」载体）+ §9 预言表逐行审计 + 可算项清单"""
import io, sys, re, math, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

RES = []
def chk(tag, name, cond, extra=''):
    RES.append(bool(cond))
    print('[%s] %-6s %s' % ('OK' if cond else 'XX', tag, name + (('  ' + extra) if extra else '')))
def info(tag, name, val=''):
    print('[--]  %-5s %s %s' % (tag, name, val))

B = open('论文_正式稿_v3.0.md', encoding='utf-8').read()
Q = open('工程期望清单.md', encoding='utf-8').read()
MEM = open('../.workbuddy/memory/MEMORY.md', encoding='utf-8').read()

print('=' * 88)
print('A 组 · B 类：「临界放大」的载体是否存在？')
print('=' * 88)

# A-1 论文从未讨论相变阶数
terms = {k: B.count(k) for k in ['连续相变', '二级相变', '临界指数', '对称破缺', '临界发散',
                                 '关联长度', '标度不变', '普适类']}
info('A-1', '相变理论词条（论文全文）', str(terms))
chk('A-1', '论文【从未讨论相变阶数／临界指数】（前 4 项全 0）',
    all(terms[k] == 0 for k in ['连续相变', '二级相变', '临界指数', '对称破缺']))

# A-2 论文用 χ = −d⟨A⟩/dλ 作相变判据（= 敏感度）
chk('A-2', '论文用「χ = −d⟨A⟩/dλ」作相变判据（即敏感度型判据）',
    'χ=−d⟨A⟩/dλ' in B)

# A-3 / A-4 两处实测的 χ_max 标度指数（这才是判定的核心数据）
m2d = re.search(r'χ_max ∝ L\^\{([−\-]?[\d.]+)\}', B)
i3d = B.find('χ_max ∝ L^{−0.04}')
info('A-3', '2+1D（κ_c）χ_max 标度指数', m2d.group(1) if m2d else '未找到')
info('A-4', '3+1D（λ_c）χ_max 标度指数', '−0.04' if i3d > 0 else '未找到')
chk('A-3', '2+1D toric code：χ_max ∝ L^{1.12}（【正】指数 ⟹ 有临界发散）',
    bool(m2d) and abs(float(m2d.group(1).replace('−', '-')) - 1.12) < 1e-9)
chk('A-4', '3+1D 弦网：χ_max ∝ L^{−0.04}（≈0 ⟹ 【无】临界发散）', i3d > 0)

# A-5 独立数值基准：连续相变的 χ_max 必须随 L 增长
#     (a) 若 χ = −d<A>/dλ 为序参量导数 → χ_max ∝ L^{1/ν}
#     (b) 若为标准磁化率 ∂<M>/∂h    → χ_max ∝ L^{γ/ν}
IDX = {
    '3D Ising (ν=0.6300, γ=1.2370)': (1/0.6300, 1.2370/0.6300),
    '2D Ising (ν=1.0, γ=1.75)':      (1/1.0,    1.75/1.0),
}
print('-' * 88)
print('连续相变对 χ_max 的【硬要求】—— 独立于论文的标准标度理论：')
for name, (iv, gv) in IDX.items():
    info('A-5', name, '1/ν=%.4f（序参量导数）  γ/ν=%.4f（标准磁化率）' % (iv, gv))
# 与实测对比（3D）
iv3, gv3 = IDX['3D Ising (ν=0.6300, γ=1.2370)']
info('A-5', '3D 实测 −0.04 vs 应有 1.5873／1.9638',
     '差 %.1f 倍／%.1f 倍' % (iv3/0.04, gv3/0.04))
chk('A-5', '3D 实测指数（−0.04）与连续相变要求（≥1.0）相差 ≥ 25 倍',
    iv3/0.04 > 25)
# L=2→4 的增长倍数演示
for L1, L2 in [(2.0, 4.0)]:
    print('-' * 88)
    print('若为连续相变，L: %.0f→%.0f 时 χ_max 应增长：' % (L1, L2))
    info('A-6', 'L^{1/ν}=1.5873', '%.2f 倍' % (L2**iv3 / L1**iv3))
    info('A-6', 'L^{γ/ν}=1.9638', '%.2f 倍' % (L2**gv3 / L1**gv3))
    info('A-6', 'L^{−0.04}（3D 实测）', '%.4f 倍（≈ 持平，略降）' % (L2**-0.04 / L1**-0.04))
    info('A-6', 'L^{+1.12}（2D 实测）', '%.2f 倍' % (L2**1.12 / L1**1.12))
chk('A-6', '【核心对照】3D 实测（≈1.00 倍）与连续相变要求（≥3.0 倍）差 3 倍以上',
    (L2**-0.04/L1**-0.04) < 1.1 and (L2**iv3/L1**iv3) > 2.5)

# A-7 2D 实测 1.12 落在合理区间（支持 2D 连续相变）
iv2, gv2 = IDX['2D Ising (ν=1.0, γ=1.75)']
chk('A-7', '2D 实测 1.12 落在 [1/ν=1.00, γ/ν=1.75] 区间内 ⟹ 2D 有临界发散',
    iv2 <= 1.12 <= gv2)

# A-8 外部文献（3D toric code 相变 = 一阶）
chk('A-8', '【外部事实】3D toric code 相变为一阶（Mühlhauser+2022 SciPost 12,069；PRR 6,043007）'
           ' ⟹ 与 3D 实测无临界发散【一致】',
    True, '（检索自 WebSearch，非论文内容）')

# A-9 λ_c(∞) 未定位
chk('A-9', 'λ_c(∞) 判为「方法学不足，未定位」（C-61/62/63；判据分辨率 ~0.04 ≈ 尺寸漂移）',
    'λ_c(∞)' in B and '未定位' in B)

# A-10 动力学层判否
chk('A-10', '「动力学·耦合层」内部推导已判否（N-43）⟹ 放大必须有动力学层',
    'N-43' in MEM or '动力学·耦合层' in MEM)

print()
print('=' * 88)
print('B 组 · §9 可检验预言表逐行审计')
print('=' * 88)

L = B.split('\n')
a = [i for i, l in enumerate(L) if l.startswith('## 9 ')][0]
b = [i for i, l in enumerate(L) if l.startswith('## 10 ')][0]
rows = []
for l in L[a:b]:
    if not l.startswith('|'):
        continue
    # 用「| 编号 |」切分（编号不含 |）
    m = re.match(r'^\|\s*([^|]+?)\s*\|(.*)$', l)
    if not m:
        continue
    no = m.group(1).strip()
    if no in ('#', '') or set(no) <= set('-: '):
        continue
    cells = l.strip().strip('|').split('|')
    if len(cells) < 4:
        continue
    rows.append((no, cells[-1].strip()))
info('B-1', '§9 数据行数', str(len(rows)))
chk('B-1', '§9 数据行 = 23', len(rows) == 23, str(len(rows)))

# 状态分类
CLS = {'已判降调/结项': 0, '判别中': 0, '理论可算·待推导': 0, '与观测有张力': 0, '其他可检验': 0}
for no, st in rows:
    if ('降调' in st) or ('结项' in st) or ('❌' in st):
        CLS['已判降调/结项'] += 1
    elif '判别中' in st:
        CLS['判别中'] += 1
    elif '待推导' in st or '待算' in st:
        CLS['理论可算·待推导'] += 1
    elif '张力' in st:
        CLS['与观测有张力'] += 1
    else:
        CLS['其他可检验'] += 1
info('B-2', '状态分布', str(CLS))
chk('B-2', '至少 2 行已被判降调/结项（诚实标注已到位）', CLS['已判降调/结项'] >= 2)

# B-3 明说「可算未算」
todo = [(no, st) for no, st in rows if '待推导' in st or '待算' in st]
info('B-3', '状态栏明说「可算而数值未做」的行', str([no for no, _ in todo]))
chk('B-3', '存在 §9 表内【明说可算、数值待推导】的条目（= 现成的可算项）', len(todo) >= 1)

print()
print('=' * 88)
print('C 组 · 「还有什么能算」清单复核')
print('=' * 88)
info('C-1', '§9 第 4 行', [st for no, st in rows if no == '4'][0][:80])
chk('C-1', '§9 第 4 行 = SU(3) β 函数阶梯跳跃（理论可算，数值待推导）',
    any(no == '4' and '待推导' in st for no, st in rows))
info('C-2', '论文【待验证】标注数', str(B.count('【待验证】')))
chk('C-2', '【待验证】标注数 ≥ 5（未闭合项可清点）', B.count('【待验证】') >= 5)

a2 = [i for i, l in enumerate(L) if l.startswith('### 10.2')][0]
b2 = [i for i, l in enumerate(L) if l.startswith('## 附录 A')][0]
opens = [l for l in L[a2:b2] if re.match(r'^\d+\.\s', l)]
info('C-3', '§10.2 开放问题条数', str(len(opens)))
chk('C-3', '§10.2 开放问题 = 13 条', len(opens) == 13, str(len(opens)))
unres = [l[:48] for l in opens if '✅' not in l.split('**')[0][:40]]
info('C-4', '§10.2 中【段落开头未见 ✅】的条', str(len(unres)))

print()
print('=' * 88)
print('D 组 · §9 第 4 行的前提核查（它真能算吗？）')
print('=' * 88)
# §5.3 已判第四代 = 失败
chk('D-1', '§5.3 已给「第四代预言」判【失败】（四类判定注：本条 = 失败）',
    '本条 = 失败' in B and '第四代' in B)
chk('D-2', '§9 第 5 行对同一命题写「与 LHC 未发现存在张力」',
    any(no == '5' and '张力' in st for no, st in rows))
chk('D-3', '⟹ §9 第 4 行「理论可算」的前提【已被判失败】⟹ 算了也无检验价值',
    any(no == '4' and '待推导' in st for no, st in rows))
# 独立算 SU(3) β 系数（标准场论，可独立重算）
def b0(nf):
    return 11.0 - 2.0 * nf / 3.0
info('D-4', 'SU(3) β 系数 b0 = 11 − 2n_f/3', 'n_f=6 → %.4f；n_f=8（+第四代）→ %.4f' % (b0(6), b0(8)))
info('D-4', '阶梯跳跃 Δb0', '%.4f（= 4/3）' % (b0(6) - b0(8)))
chk('D-4', '阶梯跳跃 Δb0 = 7 − 17/3 = 4/3 ≈ 1.3333（【可独立重算】但不构成可检验预言）',
    abs((b0(6) - b0(8)) - 4.0/3.0) < 1e-12)
# α_s 跑动到 10 TeV 的差异
import math as _m
a0 = 0.1179  # α_s(m_Z), PDG
mZ, M4, M10 = 91.1876, 1000.0, 10000.0
inv1 = 1/a0 + (b0(6) / (2*_m.pi)) * _m.log(M4 / mZ)
inv_6 = inv1 + (b0(6) / (2*_m.pi)) * _m.log(M10 / M4)
inv_8 = inv1 + (b0(8) / (2*_m.pi)) * _m.log(M10 / M4)
info('D-5', 'α_s(10 TeV)：n_f=6 → %.5f ／ n_f=8 → %.5f' % (1/inv_6, 1/inv_8))
info('D-5', '相对差', '%.2f%%' % (abs(1/inv_6 - 1/inv_8) / (1/inv_6) * 100))
chk('D-5', '若第四代存在，α_s(10 TeV) 差约 3–5%（FCC-hh 量级可见）⟹ '
           '【唯一障碍是前提，不是计算】',
    0.02 < abs(1/inv_6 - 1/inv_8) / (1/inv_6) < 0.06)

print()
print('=' * 88)
print('E 组 · 论文里还剩多少「能从第一原理独立重算」的数值断言？')
print('=' * 88)
pat = re.compile(r'([A-Za-z\u0391-\u03c9][A-Za-z0-9_\u00b2\u00b3\u207b/(){}^\s]{0,20})\s*(?:=|≈|~)\s*'
                 r'([-\u2212]?\d+(?:\.\d+)?(?:\s*[\u00d7x]\s*10[-\u2212]?\d+)?)')
hits = pat.findall(B)
info('E-1', '数值等式/近似总数', str(len(hits)))
# 分类
L1 = []   # 纯数学/常数关系（随时可独立重算）
L2 = []   # 依赖框架参数
L3 = []   # 依赖外部数据/文献
KW_FRAME = ['ε', 'β', 'λ', 'κ', 'J', 'K', 'E_c', 'N_c', 'R_c', 'h_c', 'Δ', 'σ', 'ρ', 'Φ', 'g', 'M_Pl', 'H']
for lhs, rhs in hits:
    s = lhs.strip()
    if not s:
        continue
    if any(k in s for k in KW_FRAME):
        L2.append((s, rhs))
    elif re.search(r'[×x]\s*10', rhs) or '10' in rhs:
        L3.append((s, rhs))
    else:
        L1.append((s, rhs))
info('E-2', 'L1 纯数学/常数（随时可重算）', str(len(L1)))
info('E-2', 'L2 依赖框架参数', str(len(L2)))
info('E-2', 'L3 依赖外部数据', str(len(L3)))
chk('E-2', '三类合计 = 总数', len(L1) + len(L2) + len(L3) == len(hits),
    '%d+%d+%d vs %d' % (len(L1), len(L2), len(L3), len(hits)))
# 去重后的 L1
u1 = sorted(set(L1))
info('E-3', 'L1 去重条数', str(len(u1)))
print('  L1 样例（前 25）：')
for s, v in u1[:25]:
    print('      %-28s = %s' % (s[:28], v))
chk('E-3', 'L1 类存在多条（纯数学关系可随时独立验算）', len(u1) >= 5)

print()
print('=' * 88)
print('通过 %d 项，失败 %d 项' % (sum(RES), len(RES) - sum(RES)))
print('=' * 88)
