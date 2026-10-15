# -*- coding: utf-8 -*-
"""
第 153 轮核验：A 类五项（承接第 152 轮的分级清单）

  A 组  λ_c 的下游同步扫描（13 处，逐处判"是否带失效修正"）
  B 组  κ_c / h_c 的 C-64 覆盖范围
  C 组  引理 1 vs 定理 1：能否推出？（独立数值几何验证）
  D 组  依据链的循环识别（引理 1 ↔ 简单立方）
  E 组  外部常数声明检查
  Z 组  论文零改动
"""
import io, os, re, math

BASE = os.path.dirname(os.path.abspath(__file__))
ZH   = os.path.join(BASE, "论文_正式稿_v3.0.md")
ZH_B = os.path.join(BASE, "论文_正式稿_v3.0_备份_2026-10-09第151轮前.md")
Q    = os.path.join(BASE, "项目台账.md")

B  = io.open(ZH,   encoding="utf-8").read()
BB = io.open(ZH_B, encoding="utf-8").read()
QY = io.open(Q,    encoding="utf-8").read()
L  = B.split("\n")

RES = []
def chk(tag, name, cond, extra=""):
    RES.append(bool(cond))
    print("[{}] {:<6} {} {}".format("OK" if cond else "XX", tag, name, extra))
def info(tag, name, val=""):
    print("[--] {:<6} {} {}".format(tag, name, val))

def line_of(sub):
    for i, l in enumerate(L, 1):
        if sub in l:
            return i, l
    return None, None

print("=" * 82)
print("A 组 · λ_c 下游同步扫描（13 处出现，逐处判「是否带失效修正」）")
print("=" * 82)

FIX = ["未定位", "方法学不足", "伪临界", "再修正", "已撤销", "口径注"]
lam = [(i, l) for i, l in enumerate(L, 1) if "λ_c" in l]
info("A-1", "含 λ_c 的行数", str(len(lam)))
nofix = []
for i, l in lam:
    if not any(k in l for k in FIX):
        nofix.append((i, l))
info("A-2", "未含任何失效词的行数", str(len(nofix)))
for i, l in nofix:
    info("A-2", "  L{}".format(i), l[:120])

# 关键判定：摘要层与附录 C
i107, _ = line_of("**3+1D λ_c≈0.14**（四尺寸锁定")
i1467, _ = line_of("**v1.36 变更**：3+1D λ_c 相变")
i1393, _ = line_of("λ_c(∞) **仍未定位**")
chk("A-3", "§1 摘要（L{}）写「λ_c≈0.14（四尺寸锁定）」且【不带】伪临界修正".format(i107),
    i107 is not None and not any(k in L[i107-1] for k in FIX))
chk("A-4", "附录 C（L{}）的 v1.36 变更同样【不带】伪临界修正".format(i1467),
    i1467 is not None and not any(k in L[i1467-1] for k in FIX))
chk("A-5", "而 §10.2（L{}）已明确「λ_c(∞) 仍未定位／方法学不足」".format(i1393),
    i1393 is not None and "仍未定位" in L[i1393-1] and "方法学不足" in L[i1393-1])
i1508, _ = line_of("v1.36 的 0.140 为棒/板（最薄方向=1）伪临界")
chk("A-6", "§附录/§5.8（L{}）已判 0.140 为「棒/板伪临界」".format(i1508), i1508 is not None)
info("A-7", "⟹ 结论", "摘要＋附录 C 共 2 处未同步（C-96）")

print()
print("=" * 82)
print("B 组 · κ_c / h_c 的 C-64 覆盖范围")
print("=" * 82)

# B-1 κ_c 的「两个值」是否冲突
i775, _ = line_of("1/L 外推 κ_c=0.2255")
chk("B-1", "κ_c=0.2255（L{}）是【开边界 FSS 的 1/L 外推中间值】，非冲突值".format(i775),
    i775 is not None and "开边界 FSS" in L[i775-1])
chk("B-1b", "该行紧接着标注「主要是边界效应（v1.23 环面证实）」⟹ 已交代",
    i775 is not None and "边界效应" in L[i775-1])
info("B-1", "⟹ κ_c 的两值判定", "合法（不同方法/阶段），不构成不一致")

# B-2 C-64 的正确内容
i787, l787 = line_of("该更正本身是错的")
chk("B-2", "§5.7（L{}）已写明 C-64：v1.23 那句「h_c=0.328474 是 σ^z 场值」【本身是错的】".format(i787),
    i787 is not None)
info("B-2", "C-64 的正确结论", "X 场版本的文献值【就是】0.328474 ⟹ 唯一合法比较 = 1/3 vs 0.328474（差 1.6%）")

# B-3 摘要层未同步
i112, l112 = line_of("h_c=0.328 为 σ^z 场版本值")
chk("B-3", "⚠️ §1 摘要（L{}）仍写「h_c=0.328 为 σ^z 场版本值」—— 正是 C-64 判为错误的那句".format(i112),
    i112 is not None and "σ^z 场版本值" in L[i112-1])

# B-4 附录 C 未同步
i1510, l1510 = line_of("与 h_xc≈0.32/0.328 交叉验证 1.6–4%")
chk("B-4", "⚠️ 附录 C（L{}）仍写「与 h_xc≈0.32/0.328 交叉验证 1.6–4%」—— 4% 那半来自 C-64 已判错的口径".format(i1510),
    i1510 is not None and "1.6–4%" in L[i1510-1])

# B-5 正确值：C-64 的「1.6%」自己算错了
r_ok  = abs(1/3 - 0.328474) / 0.328474   # 合法比较
r_bad = abs(1/3 - 0.328)    / 0.328      # C-64 判为错的口径
info("B-5", "1/3 vs 0.328474（C-64 声明的合法比较）", "差 {:.3%}".format(r_ok))
info("B-5", "1/3 vs 0.328（C-64 判为错的口径）", "差 {:.3%}".format(r_bad))
chk("B-5", "⚠️ C-64 写「唯一合法比较 = 1/3 vs 0.328474，差 1.6%」—— 但 1.6% 实际来自 0.328（应 1.48%）⟹ 更正本身没算对",
    abs(r_bad - 0.016) < abs(r_ok - 0.016) and abs(r_bad - 0.016) < 0.002)

print()
print("=" * 82)
print("C 组 · 引理 1 能否从定理 1 推出？（独立数值几何）")
print("=" * 82)

norm = lambda v: tuple(x / math.sqrt(sum(y*y for y in v)) for x in v)
def ang(u, v):
    d = sum(a*b for a, b in zip(u, v)) / (math.sqrt(sum(a*a for a in u))*math.sqrt(sum(b*b for b in v)))
    return math.degrees(math.acos(max(-1.0, min(1.0, d))))

# C-1 S¹（平面内）最优 k 方向覆盖
def cover_s1(k, n=3600):
    dirs = [(math.cos(2*math.pi*i/k), math.sin(2*math.pi*i/k), 0.0) for i in range(k)]
    return max(min(ang((math.cos(2*math.pi*j/n), math.sin(2*math.pi*j/n), 0.0), d) for d in dirs)
               for j in range(n))
info("C-1", "S¹（平面内）等分 k 方向的覆盖半径：")
for k in (2, 3, 4, 6):
    info("C-1", "  k={}".format(k), "{:.4f}°".format(cover_s1(k)))
chk("C-1", "S¹ 上 k=3 覆盖半径 = 60.0° < 90° ⟹ 引理 1 的「平面内 4」【不是】平面覆盖下界逼出的（3 就够）",
    abs(cover_s1(3) - 60.0) < 0.2)

# C-2 S² 覆盖
info("C-2", "S² 覆盖半径（数值，含解析最坏点）：")
planar3 = [(1,0,0), (-0.5, math.sqrt(3)/2, 0), (-0.5, -math.sqrt(3)/2, 0)]
tet = [norm(v) for v in [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]]
def cover_s2(dirs, n=30000):
    pts = []
    ga = math.pi*(3-math.sqrt(5))
    for i in range(n):
        y = 1 - 2*(i+0.5)/n
        r = math.sqrt(max(0.0, 1-y*y))
        th = ga*i
        pts.append((r*math.cos(th), r*math.sin(th), y))
    pts += [(0,0,1),(0,0,-1),(1,0,0),(-1,0,0),(0,1,0),(0,-1,0)]
    pts += [(-a, -b, -c) for (a, b, c) in dirs]      # 反向点 = 正四面体的 Voronoi 顶点（最坏点）
    return max(min(ang(p, d) for d in dirs) for p in pts)
r3 = cover_s2(planar3); r4 = cover_s2(tet)
info("C-2", "  3 个共面方向（120°）", "{:.4f}°（解析 90.0000°）".format(r3))
info("C-2", "  4 个正四面体方向", "{:.4f}°（解析 arccos(1/3) = {:.4f}°）".format(r4, math.degrees(math.acos(1/3))))
chk("C-2", "S² 上 k=3 → 90.0000°、k=4 → 70.5288°（定理 1 的两端点）",
    abs(r3 - 90) < 0.05 and abs(r4 - math.degrees(math.acos(1/3))) < 0.05)

# C-3 简单立方 6 轴的最大共面数
axes = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
best = 0; bestn = None
cands = set()
for a in axes:
    for b in axes:
        cx = (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
        n2 = sum(x*x for x in cx)
        if n2 > 1e-9:
            cands.add(norm(cx))
for nn in list(cands) + [(1,0,0),(0,1,0),(0,0,1),(1,1,1)]:
    c = sum(1 for a in axes if abs(sum(x*y for x, y in zip(nn, a))) < 1e-9)
    if c > best: best, bestn = c, nn
info("C-3", "简单立方 6 轴在任一平面内的最大方向数", "{}（法线 = {}）".format(best, tuple(round(x,4) for x in bestn)))
chk("C-3", "简单立方 6 轴最大共面数 = 4 ⟹ 引理 1 的「4」来自【格点几何】",
    best == 4)

print()
print("=" * 82)
print("D 组 · 依据链的循环识别（引理 1 ↔ 简单立方）")
print("=" * 82)

i_simple, l_simple = line_of("「外空间 6 方向 ⟹ 简单立方」")
info("D-1", "§8.6.8 诚实边界（L{}）原文".format(i_simple), (l_simple or "")[:150])
chk("D-1", "该行把「6 方向 ⟹ 简单立方」的等级标为【判定】，依据含「§4.9 引理 1 的原文」",
    i_simple is not None and "引理 1" in L[i_simple-1] and "判定" in L[i_simple-1])
i_i, l_i = line_of("简单立方 6 方向的**最大平面内方向数 = 4**")
chk("D-2", "(i) 段（L{}）用「简单立方 6 方向最大平面内数 = 4」来【支持】引理 1".format(i_i),
    i_i is not None)
chk("D-3", "⚠️ ⟹ 引理 1（设定）→ 简单立方（判定，依据含引理 1）→ 用它支持引理 1 ⟹ **循环**",
    i_simple is not None and i_i is not None)
i_le1, _ = line_of("引理 1：可访问信息 = 平面内 4 方向连接")
chk("D-4", "§4.9 引理 1（L{}）自身等级确为【本框架设定】".format(i_le1),
    i_le1 is not None and "本框架设定" in L[i_le1-1])

print()
print("=" * 82)
print("E 组 · 外部常数声明检查")
print("=" * 82)

EXT = {
    "H₀（哈勃常数取值）": ["67.4", "67.66"],
    "M_Pl（普朗克质量）": ["1.2209", "1.221", "1.22e19"],
    "t_P（普朗克时间）":   ["5.391247", "5.39"],
    "η（重子-光子比来源）": ["Planck 2018", "6.12", "BBN"],
    "G、c、ℏ 的取值":     ["6.674", "6.67e-11", "2.998e8"],
}
for name, keys in EXT.items():
    hits = {k: B.count(k) for k in keys}
    info("E-1", name, str(hits))
chk("E-1", "论文未声明 H₀ 取值（45 轮已查，此处复核）", B.count("67.4") == 0 and B.count("67.66") == 0)
chk("E-2", "论文未声明 M_Pl 数值（C-95 的根因）", B.count("1.2209") == 0 and B.count("1.221") == 0)
chk("E-3", "论文未声明 Planck 文献来源（'Planck 2018' 出现 {} 次）".format(B.count("Planck 2018")),
    B.count("Planck 2018") == 0)

print()
print("=" * 82)
print("Z 组 · 底本状态")
print("=" * 82)
chk("Z-1", "本轮未改动论文（当前稿 = 备份）", B == BB, "len {} vs {}".format(len(B), len(BB)))

print()
n_ok = sum(RES)
print("通过 {} 项，失败 {} 项".format(n_ok, len(RES) - n_ok))
