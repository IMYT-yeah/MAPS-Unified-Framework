# -*- coding: utf-8 -*-
"""
第 0 批（0.3 + 0.4）核查：

0.3  ε 的能标标注规范
     —— 核查「ε」在论文里**有多少个不同含义**、各自是否带能标
0.4  「轨道等权」残留对账
     —— 扫描 outputs/ 下全部脚本，找出算 H/N 的地方，判断口径
        **正确**：Σ|O|·ln|O| / Σ|O|（构型等权，第 50 轮 C-2 / R-2）
        **错误**：Σ ln|O| / #轨道（轨道等权）
     ⚠️ 免除项：GAP 的随机构型采样天然是构型等权（第 47/48/49 轮结果不受影响）
"""

import io, os, re, glob

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

OK = 0
BAD = 0
def chk(tag, cond, msg):
    global OK, BAD
    if cond:
        OK += 1
        print("  [OK] {:<6} {}".format(tag, msg))
    else:
        BAD += 1
        print("  [XX] {:<6} {}".format(tag, msg))

zh = io.open(ZH, encoding="utf-8").read()
zhL = zh.split("\n")

print("=" * 78)
print("第 0 批核查：0.3（ε 的能标标注）／ 0.4（轨道等权残留）")
print("=" * 78)

# ================================================================
print("\n[A3-1] ε 的**含义分类**（先分家，再谈标注）")
# 泄漏概率类：ε(E)、ε₀、ε_A、ε_B、泄漏
# Levi-Civita 类：ε_ijk、ε^ij、ε_ijkl、反对称
leak, lc, other = [], [], []
for i, s in enumerate(zhL, 1):
    if "ε" not in s:
        continue
    if re.search(r"ε_ijk|ε\^ij|ε_ijkl|ε_\{ijk\}|反对称.*ε|ε.*反对称|三阶", s):
        lc.append((i, s[:110]))
    elif re.search(r"ε\(|ε₀|ε_A|ε_B|泄漏|ε ≪|ε ~|ε~|ε ≈|β|能标", s):
        leak.append((i, s[:110]))
    else:
        other.append((i, s[:110]))
print("      ① **Levi-Civita / 表示论**类：{} 处（**与能标无关**，属记号撞车）".format(len(lc)))
for i, s in lc[:6]:
    print("         {}: {}".format(i, s[:95]))
print("      ② **泄漏概率**类：{} 处（**能标依赖**）".format(len(leak)))
for i, s in leak[:8]:
    print("         {}: {}".format(i, s[:95]))
print("      ③ 其他/待定：{} 处".format(len(other)))
for i, s in other[:6]:
    print("         {}: {}".format(i, s[:95]))
chk("A3-1", len(lc) >= 5 and len(leak) >= 20,
    "ε **至少两个含义**：泄漏概率（{} 处，能标依赖）+ Levi-Civita（{} 处，与能标无关）".format(
        len(leak), len(lc)))

# ================================================================
print("\n[A3-2] 泄漏概率 ε 的**能标标注**覆盖度")
# 判据：该行若含 ε 且是泄漏类，是否同时含能标标记（(@…)、E ~、M_Pl、meV、TeV、GeV）
SCALES = ["M_Pl", "meV", "TeV", "GeV", "eV", "E_P", "@", "能标", "β"]
bad_leak = []
for i, s in leak:
    if not any(k in s for k in SCALES):
        bad_leak.append((i, s))
print("      泄漏类共 {} 处；其中**未出现任何能标线索**的：{} 处".format(len(leak), len(bad_leak)))
for i, s in bad_leak:
    print("         ⚠️ {}: {}".format(i, s[:110]))
chk("A3-2", True,
    "泄漏类 {} 处中 {} 处缺能标线索 ⟹ 这是 @E 标注要补的地方".format(len(leak), len(bad_leak)))

# ================================================================
print("\n[A3-3] 「ε 有两个含义」这件事，论文自己**有没有声明**？")
# 判据收紧：只找「撞车声明」——即 ε 与（Levi-Civita / 反对称 / 表示论）同现且提「符号/记号/约定」
crash = [(i, s) for i, s in enumerate(zhL, 1)
         if "ε" in s and re.search(r"Levi|Levi-Civita|反对称|表示论", s)
         and re.search(r"符号|记号|约定|撞|区分", s)]
print("      「ε 撞车」的**显式声明**：{} 处".format(len(crash)))
for i, s in crash:
    print("        {}: {}".format(i, s[:130]))
# 对照组：λ 的撞车声明
lam = [(i, s) for i, s in enumerate(zhL, 1) if "符号约定（重要）" in s]
print("      对照组 —— λ 的撞车声明（`符号约定（重要）`）：{} 处".format(len(lam)))
for i, s in lam:
    print("        {}: {}".format(i, s[:120]))
print("      ⚠️ 判据（A3-3 失败的意义）：λ 撞车**有**声明，ε 撞车**没有**")
chk("A3-3", len(crash) == 0 and len(lam) >= 1,
    "ε 的双重含义**无任何声明**（而 λ 的撞车有「符号约定（重要）」）⟹ 应补一条")

# ================================================================
print("\n[A3-4] 英文本的 ε 交乘情况")
en = io.open(EN, encoding="utf-8").read()
en_leakish = len(re.findall(r"ε\(|ε₀|ε_A|ε_B|leakage", en))
en_lc = len(re.findall(r"ε_ijk|ε\^ij|ε_ijkl|antisymmetric", en))
print("      EN：泄漏类 {} 处 ／ Levi-Civita 类 {} 处".format(en_leakish, en_lc))
chk("A3-4", en_lc >= 3, "英文本同样两种含义并存 ⟹ 声明需**中英同步**")

# ================================================================
print("\n[A4-1] 0.4 扫描：含 H/N 计算的脚本")
pyfiles = sorted(glob.glob(os.path.join(BASE, "*.py")))
hits = []
for f in pyfiles:
    t = io.open(f, encoding="utf-8", errors="ignore").read()
    if not re.search(r"log\(len\(|log2\(len\(|np\.log\(len\(|math\.log\(len\(|ln\|O\||part_entropy|H/N|h_min", t):
        continue
    name = os.path.basename(f)
    if name.startswith("_patch_"):
        continue                      # 补丁脚本：引用数值而非重算，先排除
    hits.append((name, t))
print("      候选核验脚本（已排除 _patch_*）：{} 个".format(len(hits)))
for n, _ in hits:
    print("        · {}".format(n))

# ================================================================
print("\n[A4-2] ★ 逐脚本判口径：等权（错） vs 加权（对）")
# 错误模式：log 求和 再除以 len(...)（无权重）
EQ_PAT = re.compile(r"sum\(\s*(?:math\.|np\.)?log\S*\s+for\s+.*\)\s*/\s*len\(")
EQ_PAT2 = re.compile(r"sum\(\s*\[?\s*(?:math\.|np\.)?log\S*\(.*\)\s+for\s+.*\]?\s*\)\s*/\s*len\(")
# 正确模式：log 前有乘 |O| / size 权重，或分母是 sum(...)
W_PAT = re.compile(r"sum\([^)]*\*\s*(?:math\.|np\.)?log")
W_PAT2 = re.compile(r"\*\s*(?:math\.|np\.)?log\S*\([^)]*\)\s+for\s+")
summary = []
for name, t in hits:
    lines = t.split("\n")
    eq = [(i, s) for i, s in enumerate(lines, 1)
          if ("log" in s) and re.search(r"/\s*len\(", s)]
    w = [(i, s) for i, s in enumerate(lines, 1)
         if re.search(r"\*\s*(?:math\.|np\.)?log|log\S*\([^)]*\)\s*\*\s*", s)]
    summary.append((name, len(eq), len(w)))
    if eq or w:
        print("      {:<24} 可疑等权行 {} ／ 加权行 {}".format(name, len(eq), len(w)))
        for i, s in eq[:3]:
            print("           ⚠️ L{}: {}".format(i, s.strip()[:100]))
n_eq = sum(1 for _, e, _ in summary if e > 0)
print("      ⟹ 含「log 求和 / len(...)」模式的脚本：{} 个（**需人工确认**）".format(n_eq))
chk("A4-1", len(hits) >= 8,
    "候选核验脚本 {} 个（_patch_* 已排除）；其中 {} 个含可疑等权模式".format(len(hits), n_eq))

# ================================================================
print("\n[A4-3] 关键：**已经显式标注口径**的脚本")
marked = []
for name, t in hits:
    if re.search(r"构型等权|configuration-weighted|config_weighted|Σ\|O\|\s*·\s*ln", t):
        marked.append(name)
print("      显式提到「构型等权」的脚本：{} 个".format(len(marked)))
for m in marked:
    print("        · {}".format(m))
chk("A4-2", len(marked) >= 1,
    "{} 个脚本**显式标注了构型等权**（第 50 轮之后写的）；其余需逐个人工确认".format(len(marked)))

print("\n" + "=" * 78)
print("通过 {} 项，失败 {} 项".format(OK, BAD))
print("=" * 78)
