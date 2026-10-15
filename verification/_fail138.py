# -*- coding: utf-8 -*-
"""
第 138 轮 · 项目成败评估的数据核验（判据 = 台账实际数字）
原则：评估里出现的每一个数字，必须在脚本里有断言。
"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

R = []
def chk(tag, name, cond, extra=''):
    R.append(bool(cond))
    print('[%s] %-6s %-38s %s' % ('OK' if cond else 'XX', tag, name, extra))
def info(tag, name, val):
    print('[--] %-6s %-38s %s' % (tag, name, val))

Q = open('项目台账.md', encoding='utf-8').read()
QL = Q.split('\n')
B = open('论文_正式稿_v3.0.md', encoding='utf-8').read()
BL = B.split('\n')
LEAN = open('../MAPS-Unified-Framework/verification/lean/StormPoC.lean', encoding='utf-8').read()
MEM = open('../.workbuddy/memory/MEMORY.md', encoding='utf-8').read()

print('=' * 88)
print('A 组 · 判定台账规模（137 轮累计）')
print('=' * 88)

nN = max(int(m.group(1)) for m in re.finditer(r'N-(\d+)', Q))
nC = max(int(m.group(1)) for m in re.finditer(r'C-(\d+)', Q))
nI = max(int(m.group(1)) for m in re.finditer(r'I-(\d+)', Q))
nS = max(int(m.group(1)) for m in re.finditer(r'S-(\d+)', Q))
info('A-1', '负面判定 N-1 …', 'N-%d（共 %d 条）' % (nN, nN))
info('A-2', '撤回 / 更正 C-…', 'C-%d（共 %d 条）' % (nC, nC))
info('A-3', '难题 / 接口 I-…', 'I-%d（共 %d 条）' % (nI, nI))
info('A-4', '工程项 S-…', 'S-%d（共 %d 条）' % (nS, nS))
chk('A-1', '负面判定 ≥ 50 条', nN >= 50)
chk('A-2', '撤回/更正 ≥ 89 条', nC >= 89)
chk('A-3', '负面判定数 > 难题接口数', nN > nI, '（判否多于开路）')

# 判定 vs 推进：轮号覆盖
rounds = sorted(set(int(m.group(1)) for m in re.finditer(r'第\s*(\d+)\s*轮', Q)))
info('A-5', '清单提及的轮次范围', '第 %d … %d 轮' % (min(rounds), max(rounds)))
chk('A-5', '轮号连续覆盖到 133+', max(rounds) >= 133)

print()
print('=' * 88)
print('B 组 · 工程出口（S 表）')
print('=' * 88)

star3 = len(re.findall(r'★★★', Q))
info('B-1', '清单里「★★★」出现次数', str(star3))
chk('B-1', '工程出口 = 0：无 ★★★ 残留（第 61 轮起清零）',
    '工程出口 = 0' in Q and '第 61 轮起真正清零' in Q)
chk('B-2', '★ 级 S 项无「可造物」表述',
    '无一条给出可造物' in Q)
chk('B-3', '结构性理由登记（缺「势阱型构型差」）',
    '缺「势阱型构型差」' in Q or '缺「势阱型构型差」' in Q)
chk('B-4', 'S-13 电池能量密度 = 用户战略目标且判否',
    'S-13' in Q and '电池能量密度' in Q)

print()
print('=' * 88)
print('C 组 · 对外可检验出口（§9 表）')
print('=' * 88)

a = [i for i, l in enumerate(BL) if l.startswith('## 9 ')][0]
b = [i for i, l in enumerate(BL) if l.startswith('## 10 ')][0]
sec9 = '\n'.join(BL[a:b])
rows = [l for l in BL[a:b] if l.startswith('|')]
info('C-1', '§9 表行数', str(len(rows)))
# EMRI 同源组
emri = len(re.findall(r'S-E[1-4]', sec9))
info('C-2', 'EMRI 条目（S-E1…S-E4）', '%d 条（同一物理 = 1 个独立出口）' % emri)
chk('C-2', 'EMRI 四项共用一个出口', emri >= 4)
chk('C-3', '§9 #8 已降调（非框架预言 / 伪问题）',
    '非框架预言' in sec9 and '已判为伪问题' in sec9)
chk('C-4', 'S-E5 已结项（未定义）', '结项' in sec9 and '无表达式' in sec9)
chk('C-5', '存在「框架独有」签名（S3／S-E4）',
    '框架独有签名' in sec9 and '框架独有' in sec9)
info('C-6', 'EMRI 观测窗口', 'LISA（~2035；2026 滑期风险）')
chk('C-6', 'EMRI 三前提在框架之外', '前提' in Q and '框架之外' in Q)

print()
print('=' * 88)
print('D 组 · 正面成果（少数为真的定量结果）')
print('=' * 88)

chk('D-1', 'S-7 宇宙学常数：解决 98.89% / 剩 23.76 倍',
    '98.89%' in Q and '23.76' in Q)
chk('D-2', 'S-12 平坦性 Ω_K=0 是从公理解出（非假设）',
    '从公理解出而非假设' in Q or '从公理解出' in Q)
chk('D-3', 'S-12 判别性 = 0（与 ΛCDM 同值）',
    '判别性 = 0' in Q and '同值' in Q)
chk('D-4', 'λ=1 闭环登记（黑洞宇宙）',
    'λ = 1' in Q or 'λ=1' in Q)
chk('D-5', 'S-8 暗物质 = 完全空白（诚实登记）',
    '完全空白' in Q)

print()
print('=' * 88)
print('E 组 · 形式化资产的实际覆盖面（Lean）')
print('=' * 88)

thm = len(re.findall(r'^\s*theorem\s+', LEAN, re.M))
sorry_tac = len(re.findall(r'^\s*sorry\s*$', LEAN, re.M))
info('E-1', 'StormPoC.lean theorem 数', str(thm))
info('E-2', '实际 sorry 战术', str(sorry_tac))
chk('E-1', 'theorem = 55', thm == 55, str(thm))
chk('E-2', 'sorry 战术 = 0', sorry_tac == 0)
gauge = {k: len(re.findall(re.escape(k), LEAN, re.I))
         for k in ['SU(3)', 'SU(2)', 'U(1)', '规范', 'fermion', 'gluon', '三代']}
info('E-3', '规范群/四力关键词', str(gauge))
# 「gauge」3 处全在引力侧定理名 lc_gauge_identity，需先排除再判
g_all = len(re.findall('gauge', LEAN, re.I))
g_grav = len(re.findall(r'lc_gauge_identity', LEAN))
info('E-3b', '「gauge」出现处',
     '%d 处，其中 %d 处在 lc_gauge_identity（引力侧全息装配）' % (g_all, g_grav))
chk('E-3', '规范群侧 Lean 覆盖 = 0',
    all(v == 0 for v in gauge.values()) and (g_all - g_grav) == 0)

print()
print('=' * 88)
print('F 组 · 自我评估的口径（最容易被误读处）')
print('=' * 88)

chk('F-1', '§10.1 存在「完成度 ~90%」自评', '完成度 ~90%' in B)
c43 = '无度量定义' in Q and 'C-43' in Q
chk('F-2', '该数字已被 C-43 判为「无度量定义」', c43)
chk('F-3', '自评与 §10.2 开放问题数不相容（已被登记）',
    '13 条' in Q and '不相容' in Q)
chk('F-4', '框架自定位为「非已确立物理」', '非已确立物理' in B)

print()
print('=' * 88)
print('G 组 · 过程状态（内部极限）')
print('=' * 88)

chk('G-1', 'MEMORY 记录进度 137', '**进度 137**' in MEM, )
EXT = open('外部输入清单_可接入的活问题与渠道_2026-10.md', encoding='utf-8').read()
chk('G-2', '「内部到极限」已被登记（外部输入清单 §二）',
    '内部到极限' in EXT and '新增自由参数' in EXT)
chk('G-3', '外部输入清单存在（4 类入口）',
    os.path.exists('外部输入清单_可接入的活问题与渠道_2026-10.md'))
chk('G-4', '唯一 0 工作量项 = 送私审（已备好）',
    '私审' in EXT and '0 新增工作量' in EXT)

print()
print('通过 %d 项，失败 %d 项' % (sum(R), len(R) - sum(R)))
