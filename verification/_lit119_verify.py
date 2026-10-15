# -*- coding: utf-8 -*-
"""第 119 轮核验：指数度规 2025-26 文献锚定 + 对 arXiv:2511.13471 数字的复算裁定。
数值部分（NU）：光子球/阴影/ISCO/光偏折 —— 两种 l=0 变体 + GR 标定。
文档部分（LIT）：论文/材料/清单/交接 的补丁落地（两段式）。
"""
import io, os, math
import mpmath as mp
mp.mp.dps = 40
M = mp.mpf(1)

# ---------- 两种变体（l=0） ----------
# ISO = 本框架各向同性指数度规: -e^{-2M/r}dt^2 + e^{2M/r}(dr^2 + r^2 dOmega^2)
#   null: (du/dphi)^2 = e^{4Mu}/b^2 - u^2
# STD = 标准坐标变体（Ernazarov §2.6，g_thth=r^2）: -e^{-2M/r}dt^2 + e^{2M/r}dr^2 + r^2 dOmega^2
#   null: (du/dphi)^2 = 1/b^2 - u^2 e^{-2Mu}

def _bisect(f, lo, hi, it=200):
    """返回根内侧（f>0 一侧）的点 —— 保证被积函数非负"""
    flo = f(lo)
    for _ in range(it):
        mid = (lo + hi)/2
        if (f(mid) > 0) == (flo > 0):
            lo = mid
        else:
            hi = mid
    return lo

def u_max_iso(b):
    # 物理根 = 最小正根；围栏 [1e-15, 2/b]（端点符号相反）
    f = lambda u: mp.e**(4*M*u)/b**2 - u**2
    return _bisect(f, mp.mpf('1e-15'), 2/b)

def u_max_std(b):
    f = lambda u: 1/b**2 - u**2*mp.e**(-2*M*u)
    return _bisect(f, mp.mpf('1e-15'), 2/b)

def deflection(b, kind):
    """alpha = 2*int_0^{u_max} du/sqrt(f) - pi ; u = u_max - s^2 正则化"""
    um = u_max_iso(b) if kind == 'ISO' else u_max_std(b)
    if kind == 'ISO':
        g = lambda s: mp.e**(4*M*(um - s**2))/b**2 - (um - s**2)**2
    else:
        g = lambda s: 1/b**2 - (um - s**2)**2*mp.e**(-2*M*(um - s**2))
    val = mp.quad(lambda s: 2*s/mp.sqrt(g(s)), [0, mp.sqrt(um)])
    return 2*val - mp.pi

def deflection_gr(b):
    """GR 标定：Schwarzschild 面积坐标 (du/dphi)^2 = 1/b^2 - u^2 + 2M u^3"""
    f = lambda u: 1/b**2 - u**2 + 2*M*u**3
    um = _bisect(f, mp.mpf('1e-15'), 2/b)
    g = lambda s: 1/b**2 - (um - s**2)**2 + 2*M*(um - s**2)**3
    val = mp.quad(lambda s: 2*s/mp.sqrt(g(s)), [0, mp.sqrt(um)])
    return 2*val - mp.pi

print('=' * 88)
print('NU-1 光偏折：两种变体 vs GR（b 以 M 为单位）')
print('=' * 88)
print('  b/M      α(ISO)·b/(4M)    α(STD)·b/(4M)    α(GR)·b/(4M)   α(ISO)/α(GR)')
for b in (mp.mpf(10), mp.mpf(100), mp.mpf(1000)):
    aI = deflection(b, 'ISO'); aS = deflection(b, 'STD'); aG = deflection_gr(b)
    print('  %-8s %.6f          %.6f          %.6f        %.4f'
          % (b, aI*b/(4*M), aS*b/(4*M), aG*b/(4*M), aI/aG))
print('  ⟹ 两种变体的 1PN 系数都 → 4M/b（= GR 值；不是「一半」2M/b）')

print('')
print('=' * 88)
print('NU-2 光子球 / 阴影（b_c = min_r r·e^{kM/r}）')
print('=' * 88)
# ISO: b_c^2 = min_r [r^2 e^{4M/r}] = min (r e^{2M/r})^2 ; STD: min (r e^{M/r})^2
r_iso = mp.findroot(lambda r: mp.diff(lambda x: x*mp.e**(2*M/x), r), mp.mpf('2.0'))
r_std = mp.findroot(lambda r: mp.diff(lambda x: x*mp.e**(M/x), r), mp.mpf('1.0'))
b_iso = r_iso*mp.e**(2*M/r_iso)
b_std = r_std*mp.e**(M/r_std)
chk_ph = mp.findroot(lambda r: 2*M/r**2 - (2/r - 2*M/r**2), mp.mpf('2.0'))  # A'/A=C'/C
print('  ISO: 光子球 r = %.6f (应 2)   b_c = %.6f (应 2e=%.6f)' % (r_iso, b_iso, 2*mp.e))
print('  STD: 光子球 r = %.6f (应 1)   b_c = %.6f (应 e=%.6f)' % (r_std, b_std, mp.e))
print('  A\'/A=C\'/C 复核（ISO 光子球条件）：r = %.6f' % chk_ph)
print('  ⟹ 本文度规(ISO)阴影/GR 阴影 = %.6f（+%.2f%%）'
      % (b_iso/(3*mp.sqrt(3)), 100*(b_iso/(3*mp.sqrt(3)) - 1)))
print('  ⟹ arXiv:2511.13471 的数字（r_*=M, b_*=Me）与 STD 行**完全一致**')

print('')
print('=' * 88)
print('NU-3 ISCO：l~2 极小点 min Mr^2e^{2M/r}/(r-2M)（ISO）与 Mr^2/(r-M)（STD）')
print('=' * 88)
r_isco_iso = mp.findroot(lambda r: mp.diff(lambda x: x**2*mp.e**(2*M/x)/(x-2*M), r), mp.mpf('5.0'))
r_isco_std = mp.findroot(lambda r: mp.diff(lambda x: x**2/(x-M), r), mp.mpf('2.0'))
print('  ISO: r_ISCO = %.6f   （解析 (3+√5)M = %.6f）' % (r_isco_iso, 3+mp.sqrt(5)))
print('  STD: r_ISCO = %.6f   （= 2M，与 arXiv:2511.13471 一致）' % r_isco_std)

print('')
print('=' * 88)
print('NU-4 关键比值（可复算）')
print('=' * 88)
print('  2e/(3√3) = %.6f  ⟹ +%.3f%%（论文 v1.21 表记 +4.55%% 系对 EHT 的 5.2）' % (2*mp.e/(3*mp.sqrt(3)), 100*(2*mp.e/(3*mp.sqrt(3))-1)))
print('  EHT 参考 5.2±0.3：+%.3f%%；2e = %.6f；3√3 = %.6f' % (100*(2*mp.e/5.2-1), 2*mp.e, 3*mp.sqrt(3)))
print('  「一半偏折」假设检验：α_ISO·b/(2M) @ b=1000 = %.4f（若「一半」应=1.0000，实测应≈2）'
      % (deflection(mp.mpf(1000), 'ISO')*1000/(2*M)))

# ---------- 文档部分 ----------
print('')
print('=' * 88)
print('LIT：补丁落地（两段式）')
print('=' * 88)
BASE = r'[WORKSPACE]'
P = dict(
    ZH=os.path.join(BASE, 'outputs', '论文初稿_正反物质对风暴统一框架_v2.9.md'),
    EN=os.path.join(BASE, 'outputs', 'Paper_MatterAntimatterPairStorm_v2.9_EN.md'),
    MAT=os.path.join(BASE, 'outputs', 'EMRI材料包_给LISA组的S-E1-E4.md'),
    LIST=os.path.join(BASE, 'outputs', '项目台账.md'),
    HO=os.path.join(BASE, '环境说明.md'),
    MEMO=os.path.join(BASE, 'outputs', '文献锚定升级_指数度规2025-26与EMRI波形2026.md'),
)
B = dict(
    ZH=os.path.join(BASE, 'MAPS-Unified-Framework', 'paper', 'history',
                    '论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-04第119轮前.md'),
    EN=os.path.join(BASE, 'MAPS-Unified-Framework', 'paper', 'history',
                    'Paper_v2.9_EN_备份_2026-10-04第119轮前.md'),
    MAT=os.path.join(BASE, 'outputs', 'EMRI材料包_给LISA组的S-E1-E4_备份_2026-10-04第119轮前.md'),
    LIST=os.path.join(BASE, 'outputs', '项目台账_备份_2026-10-04第119轮前.md'),
    HO=os.path.join(BASE, '环境说明_备份_2026-10-04第119轮前.md'),
)
rd = lambda p: io.open(p, encoding='utf-8').read() if os.path.exists(p) else ''
cur = {k: rd(v) for k, v in P.items()}
bak = {k: rd(v) for k, v in B.items()}
OK, FAIL = 0, 0
def chk(tag, cond, msg):
    global OK, FAIL
    if cond: OK += 1; print('  [OK] %-9s %s' % (tag, msg))
    else: FAIL += 1; print('  [XX] %-9s %s' % (tag, msg))

chk('LIT-1', 'v2.9 口径注（第 119 轮' in cur['ZH'] and 'v2.9 口径注（第 119 轮' not in bak['ZH'],
    '论文 ZH 119 块（两段式）')
chk('LIT-2', 'round 119' in cur['EN'] and 'round 119' not in bak['EN'], '论文 EN 119 块（两段式）')
chk('LIT-3', '2511.13471' in cur['ZH'] and '2511.13471' in cur['EN'], '中英均含外部文献号')
chk('LIT-4', '标准坐标变体' in cur['ZH'] and 'standard-coordinate variant' in cur['EN'], '中英均含「标准坐标变体」裁定')
chk('LIT-5', '第 119 轮' in cur['MAT'] and '第 119 轮' not in bak['MAT'], '材料包 119 注（两段式）')
chk('LIT-6', '2607.09310' in cur['MAT'] and '2607.09310' not in bak['MAT'], '材料包 Q1 锚定（两段式）')
chk('LIT-7', '第 119 轮' in cur['LIST'] and '第 119 轮' not in bak['LIST'], '清单 119 行（两段式）')
chk('LIT-8', '第 119 轮' in cur['HO'] and '第 119 轮' not in bak['HO'], '交接 119 条目（两段式）')
chk('LIT-9', len(cur['MEMO']) > 2500, '备忘录存在（%d 字符）' % len(cur['MEMO']))
# 块结构
L = cur['ZH'].split('\n')
idx = [k for k, s in enumerate(L) if 'v2.9 口径注（第 119 轮' in s]
if idx:
    k0 = idx[0]; k1 = k0
    while k1 < len(L) and L[k1].strip() != '': k1 += 1
    chk('LIT-10', k1 - k0 >= 1 and len(L[k0]) > 600, 'ZH 119 段：单段长 %d 字符' % len(L[k0]))
else:
    chk('LIT-10', False, 'ZH 119 块未找到')

print('')
print('=' * 60)
print('通过 %d 项，失败 %d 项' % (OK, FAIL))
