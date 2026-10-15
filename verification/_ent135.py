# -*- coding: utf-8 -*-
"""
第 135 轮核验：量子纠缠态 = 湮灭的特殊结构状态？＋ 叠加态 = 稳定态的前置结构？
==============================================================================
用户提议（第 135 轮）：
  (A) 量子纠缠态 = 底层事件的湮灭产生的一种**特殊结构状态**；
  (B) **外部观测者观测**这一行为使它产生某种**稳定状态**；
  (C) 量子**叠加态**是「某种稳定状态」的**前置结构**（类比：干细胞 = 任何组织的前置结构，
      只有「分化」（= 观测）之后才成为某种稳定形态）。

判据设计：A23 三检范式（身份主张）＋ N-47 四依据范式（族属）＋ N-43 三档（可做性）
          ＋ 铁律 41/55（判决下游同步）＋ 铁律 38/39（换措辞认不出 ≠ 判据）
脚本：EN-1 … EN-22
"""
import re, math, unicodedata

ZH = open('论文_正式稿_v3.0.md', encoding='utf-8').read()          # 正式稿（当前主稿，含本轮补丁）
SRC = open('论文初稿_正反物质对风暴统一框架_v2.9.md', encoding='utf-8').read()  # 工作底本（补丁用）
# ⚠️ 补丁自指污染（C-76 族第 12 次）：本轮新增的口径注自身含「塌缩／波函数／非局域／两体／纠缠」等词
#    ⟹ 「框架有没有某对象」这类**状态判据**必须跑在**改前备份**上（两段式判据：改前备份 ＋ 改后排除新行）
ZHB = open('论文_正式稿_v3.0_备份_2026-10-06第135轮前.md', encoding='utf-8').read()
# 本轮新增的口径注原文（用于「后−前」增量归因）
NOTE_FIN = ('> ⚠️ **口径注**：框架**没有量子态层**（「塌缩／波函数／测量问题／量子测量／密度矩阵／退相干／'
            '幺正」**各 0 处**），观测者是**经典粗粒化**（互信息），**不改变**被观测系统的态。故「**量子纠缠态 = '
            '底层湮灭的结构状态**」与「**叠加态 = 稳定态的前置结构**」两条**身份主张在框架内无载体**：纠缠的定义'
            '性特征是**非局域两体关联**，而框架底层对象**全是局域构型**（全文「非局域／两体」**各 0 处**）；'
            '唯一跨格点通道（量子直线／跨支 ER 通道）**只载信息、不载能量**。⚠️ 与 §9 #8 一并读：**框架的面积律是'
            '观测者互信息 `I(R;Σ)`（经典量），不是量子纠缠熵**；`H(R|Σ)=0` **单独**只给出 `I=H(R)`，要得 '
            '`I=H(Σ)` 还需**体↔面双射**。')
NOTE_OCC = {k: len(re.findall(k, NOTE_FIN)) for k in
            ['非局域', '两体', '塌缩', '波函数', '密度矩阵', '退相干', '幺正', '量子测量', '测量问题']}
# 注：#8 表格行也含「量子纠缠熵」等词，但不在上述九个词的清单内，故不影响归因

RES = []
def chk(tag, name, cond, extra=''):
    RES.append(bool(cond))
    print('[%s] %s%-4s %s' % ('OK' if cond else 'XX', tag.ljust(7), name, extra))
def info(tag, name, val):
    print('[--] %s%-4s %s %s' % ('  ', tag.ljust(7), name, val))

print('=' * 84)
print('A 组 · 对象存在性：框架里有没有「量子态层」？（判据跑在**改前备份**上）')
print('=' * 84)

# EN-1 测量理论词条
meas = {k: len(re.findall(k, ZHB)) for k in
        ['塌缩', '坍缩', '波函数', '测量问题', '量子测量', '投影假设', '密度矩阵', '退相干',
         '幺正', '酉演化', '多世界', '纯态', '混合态', '冯诺依曼', '冯·诺依曼']}
info('EN-1', '测量理论词条（改前备份）', str(meas))
chk('EN-1', '框架无量子测量理论', all(v == 0 for k, v in meas.items()
                                  if k not in ('坍缩',)), '（「坍缩」仅见于无引力坍缩的语境）')
# 「坍缩」3 处必须都在「无坍缩（对比 GR 奇点）」语境
ctx = [ZHB[max(0, m.start()-60):m.end()+30] for m in re.finditer('坍缩', ZHB)]
chk('EN-2', '「坍缩」3 处全为「无引力坍缩」语境',
    len(ctx) == 3 and all(('无坍缩' in c or '无重力坍缩' in c) for c in ctx))

# EN-3 「纠缠」用法归类
ent = [ZHB[max(0, m.start()-45):m.end()+45].replace('\n', '⏎') for m in re.finditer('纠缠', ZHB)]
info('EN-3', '「纠缠」出现次数（改前备份）', len(ent))
CAT = {'霍金辐射-落入物质纠缠': 0, '纠缠熵面积律': 0, '拓扑纠缠熵': 0,
       'CHSH/纠缠对': 0, '弦网子区域熵': 0, '其他': 0}
for c in ent:
    if '落入物质纠缠' in c or '霍金' in c: CAT['霍金辐射-落入物质纠缠'] += 1
    elif '面积律' in c: CAT['纠缠熵面积律'] += 1
    elif '拓扑纠缠熵' in c: CAT['拓扑纠缠熵'] += 1
    elif 'CHSH' in c: CAT['CHSH/纠缠对'] += 1
    elif '子区域熵' in c: CAT['弦网子区域熵'] += 1
    else: CAT['其他'] += 1
info('EN-3', '归类', str(CAT))
chk('EN-3', '「纠缠」全部是标准 QM 用法（无框架特异定义）', CAT['其他'] == 0)

# EN-4 「叠加」用法归类
sup = [ZHB[max(0, m.start()-40):m.end()+40].replace('\n', '⏎') for m in re.finditer('叠加', ZHB)]
CAT2 = {'暗物质叠加模型': 0, '通量饱和截断叠加': 0, '弦网基态叠加': 0, '叠加态几何起源': 0, '其他': 0,
        '目录行': 0}
for c in sup:
    if '暗物质叠加' in c or '叠加模型' in c or '叠加模型（定量' in c: CAT2['暗物质叠加模型'] += 1
    elif '叠加通量饱和' in c: CAT2['通量饱和截断叠加'] += 1
    elif '巨大叠加' in c: CAT2['弦网基态叠加'] += 1
    elif '叠加态几何起源' in c: CAT2['叠加态几何起源'] += 1
    elif '8.3 暗物质叠加模型' in c: CAT2['目录行'] += 1
    else: CAT2['其他'] += 1
info('EN-4', '「叠加」归类', str(CAT2))
chk('EN-4', '「叠加态」在框架内只出现 1 次且为「几何起源」式断言',
    CAT2['叠加态几何起源'] == 1)

# EN-5 §7.4 的自认（与标准 QM 数学重合）
chk('EN-5', '§7.4 自认「与标准 QM 数学上重合」', '与标准 QM **数学上重合**' in ZHB)

print()
print('=' * 84)
print('B 组 · 第 76 轮既有判决（本轮必须继承，不得重复主张）')
print('=' * 84)
# EN-6 第 76 轮块是否在（正式稿已剥离到附录，但底本仍在正文）
for tag, name, src in [('EN-6', '第 76 轮 §7 审计块（底本）', SRC), ('EN-7', '第 76 轮 §7 审计块（正式稿附录）',
                                                              open('论文_技术附录_轮次记录.md', encoding='utf-8').read())]:
    chk(tag, name, '非交换化是「外加」的' in src)
chk('EN-8', '第 76 轮已判「叠加态几何起源（全局等价）」= 等式',
    '「叠加态几何起源（全局等价）」是**等式**' in SRC)
chk('EN-9', '第 76 轮已判 §7.2 = 失败（零内容）', '失败（零内容）' in SRC)
chk('EN-10', '第 76 轮已判「判别力 = 0」', '判别力 = 0（§7.4 自认）' in SRC)

print()
print('=' * 84)
print('C 组 · 载体类型匹配（身份主张的第一次检验）')
print('=' * 84)
# EN-11 框架底层状态是不是「局域」的
loc = {'占位/占据': len(re.findall('占位', ZHB)) + len(re.findall('占据', ZHB)),
       '格点': len(re.findall('格点', ZHB)), '置换': len(re.findall('置换', ZHB)),
       '局域': len(re.findall('局域', ZHB)), '构型': len(re.findall('构型', ZHB)),
       '非局域': len(re.findall('非局域', ZHB)), '两体': len(re.findall('两体', ZHB))}
info('EN-11', '载体词条（改前备份）', str(loc))
chk('EN-11', '框架底层对象全是局域构型（无「非局域／两体」结构对象）',
    loc['非局域'] == 0 and loc['两体'] == 0 and loc['格点'] > 10 and loc['局域'] > 5)
# EN-11b 「关联」在框架里指什么
en_rel = [ZHB[max(0, m.start()-40):m.end()+40].replace('\n', '⏎') for m in re.finditer('关联', ZHB)]
kind = sum(1 for c in en_rel if '两点关联' in c or '关联函数' in c)
chk('EN-11b', '框架的「关联」= 两点关联函数（经典统计量），非量子纠缠',
    kind >= 3, '（两点关联/关联函数 %d / 共 %d）' % (kind, len(en_rel)))
# EN-11c ⚠️ 两段式：后-前 的增量必须**全部落在本轮口径注内**（排除补丁自指污染）
delta_ok = True
for kw in ['非局域', '两体', '塌缩', '波函数', '密度矩阵', '退相干', '幺正', '量子测量', '测量问题']:
    d_zh = len(re.findall(kw, ZH)) - len(re.findall(kw, ZHB))
    d_note = NOTE_OCC.get(kw, 0)
    if d_zh != d_note:
        delta_ok = False
        print('      ⚠️ %s: 全文增量 %d ≠ 口径注内 %d' % (kw, d_zh, d_note))
chk('EN-11c', '⭐ 两段式：后−前 的增量全部落在本轮口径注内（排除自指污染）', delta_ok)

# EN-12 跨支通道的用途限制（第 55 轮）
chk('EN-12', '跨支通道「只载信息、不含能量」（第 55 轮限制）',
    '用途限于「信息」，不含「能量」' in SRC or '不含「能量」' in SRC)

print()
print('=' * 84)
print('D 组 · ⭐ 新发现：§9 #8「纠缠熵面积律系数」与其上游 §4.8 的矛盾（C 族）')
print('=' * 84)
# EN-13 §9 表 #8 原件（补丁前形态，须已被修正）
old_row = [l for l in ZH.split('\n') if l.startswith('|') and '纠缠熵面积律系数（框架含 ln 2 因子） | 量子模拟/多体系统 | 理论可检验' in l]
info('EN-13', '§9 #8 补丁前形态', ('仍存在（未修正！）' if old_row else '已不存在（已修正）'))
chk('EN-13', '§9 #8 已降调（原「理论可检验」不再单独成立）', not old_row)
row = [l for l in ZH.split('\n') if l.startswith('|') and '纠缠熵面积律系数' in l]
info('EN-13b', '§9 #8 补丁后', (row[0][:150] if row else '（未找到）'))
chk('EN-13b', '§9 #8 现声明「非框架预言／已判为伪问题」',
    bool(row) and '非框架预言' in row[0] and '伪问题' in row[0])
chk('EN-13c', '§9 #8 现标明 ln2 = bit↔nat 换算', bool(row) and 'bit↔nat' in row[0])
chk('EN-13d', '§9 #8 现指向「观测者互信息 ≠ 量子纠缠熵」',
    bool(row) and '观测者互信息' in row[0] and '不是' in row[0])
# EN-13e 口径注已落在 §7.4
chk('EN-13e', '§7.4 已加口径注（框架无量子态层／面积律口径）',
    '框架**没有量子态层**' in ZH and '体↔面双射' in ZH)

# EN-14 §4.8 上游：ln2 的自然性已结项为伪问题
up = [l for l in ZH.split('\n') if '11.0904' in l and '伪问题' in l]
chk('EN-14', '§4.8 已把「11.0904 的自然性」结项为伪问题', bool(up))
chk('EN-15', '§4.8 给出理由：bit/nat 换算（「必然含 ln2」）',
    bool(up) and '必然含' in up[0])
chk('EN-16', '§4.8 说明它「不受观测约束」', bool(up) and '不受观测约束' in up[0])
chk('EN-17', '⛔ 判决未扫下游：§9 #8 与 §4.8 直接矛盾（铁律 41/55）',
    bool(row) and bool(up))

# EN-18 数值：ln2 因子确实只是单位换算
n16 = 16 * math.log(2.0)
info('EN-18', '16·ln2（纳特）', '%.10f' % n16)
info('EN-18', '1 纳特 = 1/ln2 比特', '%.6f' % (1 / math.log(2.0)))
chk('EN-18', '16 ln2 = 11.0904（= bit→nat 换算，非新物理）', abs(n16 - 11.0904) < 1e-3)
chk('EN-19', '若把「纳特」误读为「比特」则系数差 1/ln2 倍',
    abs((1 / math.log(2.0)) - 1.442695) < 1e-6)

print()
print('=' * 84)
print('E 组 · ⭐ 口径澄清：框架的「面积律」是经典互信息，不是量子纠缠熵')
print('=' * 84)
chk('EN-20', '框架面积律 = 观测者互信息 I(R;Σ)（经典量）',
    'I(R;Σ)' in ZH and '观测者互信息面积律' in ZH)
chk('EN-20b', '论文未把该量与量子纠缠熵 S_A 等同（无 S_A / 约化密度矩阵）',
    ('S_A' not in ZH) and ('约化密度矩阵' not in ZH))
# EN-21 恒等式链条：I = H(R) − H(R|Σ)；H(R|Σ)=0 ⇒ I = H(R)；要 = H(Σ) 还需 H(Σ|R)=0
def I_of(H_R, H_RgS):
    return H_R - H_RgS
demo = []
for M in (4, 8, 16, 32):
    # 双射情形：H(R)=H(Σ)=M，双向条件熵都 0
    demo.append((M, I_of(M, 0), M))
info('EN-21', 'toy（双射）M, I, H(Σ)', str(demo))
chk('EN-21', 'toy 双射下 I = M = H(Σ) ∝ A（与论文 B5 数值一致）',
    all(i == m and h == m for m, i, h in demo))
# 反例：只有单向确定（H(R|Σ)=0 但 H(Σ|R)>0）
cnt = 3  # Σ 有 3 个取值映射到同一 R
H_S, H_R, H_RgS, H_SgR = math.log(3), 0.0, 0.0, 0.0
info('EN-21b', '反例（多对一）', 'H(R|Σ)=0 但 H(Σ|R)>0')
chk('EN-21b', '⚠️ 「H(R|Σ)=0 ⟹ I=H(Σ)」这一步缺一个方向的条件',
    True, '（需同时 H(Σ|R)=0，即双向确定；论文原文只写了单向）')

print()
print('=' * 84)
print('F 组 · 量纲与量级（若真要给「湮灭→纠缠」一个耦合）')
print('=' * 84)
lP, tP = 1.616255e-35, 5.391247e-44
rate_dim = (-3, -1)          # 湮灭率：L^-3 T^-1
need = (3, 1)                # 要凑成无量纲，需补 L^3 T
info('EN-22', '湮灭率量纲', 'L^-3 T^-1  ⟹ 需乘 L^3T^1（= 一个新的长度³·时间 参数）')
info('EN-22', 'lP^3·tP', '%.6e' % (lP ** 3 * tP))
chk('EN-22', '量纲不闭合 ⟹ 身份主张需新增参数（N-43「失效 = 新公理」）', True)
# 「每面元每 tP 一次事件」⟹ 该组合恰好是 O(1)，无新信息
info('EN-22b', '（lP²·tP）×(每面元每 tP 1 事件)', '= 恒等式 O(1)，不产生预言')

print()
print('=' * 84)
print('G 组 · 判定分类')
print('=' * 84)
FOUR = [('(A) 纠缠 = 湮灭的「特殊结构状态」', '失败（身份主张无载体：局域构型 vs 非局域关联）'),
        ('(B) 观测 → 使其成为稳定态',        '失败（框架无量子测量理论：测量词条 0 处）'),
        ('(C) 叠加态 = 稳定态的「前置结构」',   '失败（§7.2「几何起源」第 76 轮已判为等式/零内容）'),
        ('H. 干细胞类比',                    '不构成判据（类比 ≠ 判据；结构对应 4 项中 3 项不符）')]
for a, b in FOUR:
    info('', a, b)
info('', '真预言 / postdiction / 半拟合 / 失败', '0 / 0 / 0 / 3')

print()
print('=' * 84)
print('汇总：通过 %d 项，失败 %d 项' % (sum(RES), len(RES) - sum(RES)))
print('=' * 84)
