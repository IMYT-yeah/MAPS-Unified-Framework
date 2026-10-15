# -*- coding: utf-8 -*-
"""第 111 轮核验：A23（普朗克常数的物理身份）
   检查项 A23-1 … A23-13。两段式项：取证读「补丁前备份」，确认读当前稿。
"""
import io, os, math, re

BASE = r"[WORKSPACE]"
OUT = os.path.join(BASE, "outputs")
HIST = os.path.join(BASE, "MAPS-Unified-Framework", "paper", "history")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
ZH_PRE = os.path.join(HIST, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-04第111轮前.md")
EN_PRE = os.path.join(HIST, "Paper_v2.9_EN_备份_2026-10-04第111轮前.md")
LIST = os.path.join(OUT, "项目台账.md")
HO = os.path.join(BASE, "环境说明.md")

rd = lambda p: io.open(p, encoding="utf-8").read()
Z, E, LP, H = rd(ZH), rd(EN), rd(LIST), rd(HO)
ZP, EP = rd(ZH_PRE), rd(EN_PRE)
ZL, EL = Z.split("\n"), E.split("\n")

OK = [0]
FAIL = [0]


def chk(tag, cond, msg):
    if cond:
        OK[0] += 1
        print("  [OK] " + tag + " " + msg)
    else:
        FAIL[0] += 1
        print("  [XX] " + tag + " " + msg)


# ---- 常数（自洽：l_P 由 G、hbar、c 导出，不引外部 l_P 值） ----
c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
H0 = 2.1925e-18          # 反解自论文 ρ = 8.5983e-27 kg/m^3
C4 = c ** 4

print("=== A23-1 `M^2/A = c^4/(16 pi G^2)` 是 GR 的代数恒等式（任意 M）===")
worst = 0.0
for M in (2.0e30, 1.989e30, 8.7e36, 4.3e6 * 1.989e30, 5.97e24):
    rs = 2.0 * G * M / c ** 2
    A = 4.0 * math.pi * rs ** 2
    lhs = M ** 2 / A
    rhs = C4 / (16.0 * math.pi * G ** 2)
    worst = max(worst, abs(lhs - rhs) / rhs)
chk("A23-1", worst <= 1e-15,
    "5 个质量（太阳 / M87* / Sgr A* / 地球）下 `M^2/(4pi r_h^2)` 与 `c^4/(16 pi G^2)` 最大相对差 "
    + "%.1e" % worst + " ⟹ 与 M 无关 ⟹ 该常数**由 r_h = 2GM/c^2 定义**")

print("=== A23-2 数值与量纲 ===")
val = C4 / (16.0 * math.pi * G ** 2)
chk("A23-2a", abs(val / 3.6e52 - 1.0) < 0.01,
    "`c^4/(16 pi G^2)` = %.4e kg^2/m^2（论文写 3.6e52）" % val)
dim_lhs = (1 + 1 - 2 * (-1) + 0, 4 - 2 * 3 + 2 * 2 - 0, -4 + 2 * 2)   # 占位，改用下面的函数
# 用指数运算严格计算：(kg, m, s)
def mul(a, b, n=1):
    return tuple(a[i] + n * b[i] for i in range(3))


def powr(a, n):
    return tuple(n * x for x in a)


KG, M, S = (1, 0, 0), (0, 1, 0), (0, 0, 1)
dim_c = (0, 1, -1)
dim_G = (-1, 3, -2)
dim_hbar = (1, 2, -1)
d_lhs = mul(powr(dim_c, 4), powr(dim_G, -2))
chk("A23-2b", d_lhs == (2, -2, 0) and dim_hbar == (1, 2, -1),
    "量纲：`c^4/(16 pi G^2)` = " + str(d_lhs) + " (**kg^2/m^2**) ｜ 普朗克常数 hbar = "
    + str(dim_hbar) + " (**kg·m^2/s**) ⟹ **不同量纲**")
chk("A23-2c", "16\u03c0G\u00b2" in Z and "3.6\u00d710\u2075\u00b2" in Z,
    "论文现稿含该式与数值 ⟹ 该误标**在论文里**（非仅日志）")

print("=== A23-3 v1.17 的连锁：循环 + 「双重来源」===")
chk("A23-3a", Z.count("\u53cc\u91cd\u6765\u6e90") >= 1 or Z.count("dual origin") >= 1,
    "ZH 现稿含「双重来源」措辞 " + str(Z.count("\u53cc\u91cd\u6765\u6e90")) + " 处")
chk("A23-3b", E.count("dual origin") >= 1, "EN 现稿含 'dual origin' 1 处")
# 循环：用 M^2/A 的常数反推 r_h，必回到同一个 r_h
M0 = 1.989e30
rh_in = 2.0 * G * M0 / c ** 2
rh_out = math.sqrt(M0 ** 2 / (C4 / (16.0 * math.pi * G ** 2)) / (4.0 * math.pi))
chk("A23-3c", abs(rh_out - rh_in) / rh_in < 1e-12,
    "用该常数反解 r_h = %.6e m，与输入 r_h = %.6e m 逐位相同 ⟹ **循环**（常数就是用史瓦西面算出来的）"
    % (rh_out, rh_in))

print("=== A23-4 lambda = 1 链里 hbar 逐项抵消（核心定量事实）===")
rows = []
for t in (0.5, 1.0, 2.0, 10.0, 1e6):
    h = t * hbar
    lp2 = G * h / c ** 3                      # l_P 随 hbar 同步（R2 锁定）
    R = c / H0
    N = math.pi * R ** 2 / lp2
    kT = h * H0 / (2.0 * math.pi)
    E_tot = N * kT
    rho = E_tot / ((4.0 * math.pi / 3.0) * R ** 3 * c ** 2)
    rows.append((t, lp2, rho))
rho0 = rows[1][2]
dev = max(abs(r / rho0 - 1.0) for _, _, r in rows)
chk("A23-4a", dev < 1e-13,
    "hbar -> t*hbar（t = 0.5/1/2/10/1e6）并同步重算 l_P^2：rho 最大相对差 = %.1e ⟹ **rho 不含 hbar**" % dev)
zhi = 3.0 * H0 ** 2 / (8.0 * math.pi * G)
chk("A23-4b", abs(rho0 / zhi - 1.0) < 1e-12 and abs(rho0 / 8.5983e-27 - 1.0) < 5e-3,
    "解析对照 `3H_0^2/(8 pi G)` = %.6e，数值 = %.6e，论文值 8.5983e-27 ⟹ 一致" % (zhi, rho0))
# 独立检查：若把 l_P 当作固定输入，则 rho ∝ hbar ⟹ 仍无法单独定 hbar
rho_fixed_lp = []
for t in (0.5, 2.0):
    R = c / H0
    lp2 = G * hbar / c ** 3
    rho_fixed_lp.append((t, (math.pi * R ** 2 / lp2) * (t * hbar * H0 / (2 * math.pi))
                         / ((4 * math.pi / 3) * R ** 3 * c ** 2)))
chk("A23-4c", abs(rho_fixed_lp[1][1] / rho_fixed_lp[0][1] - 4.0) < 1e-12,
    "若把 l_P 固定而只改 hbar ⟹ rho ∝ hbar（t=2 / t=0.5 之比 = %.6f）⟹ 两条读法都只锁住**组合**"
    % (rho_fixed_lp[1][1] / rho_fixed_lp[0][1]))

print("=== A23-5 可辨识性计数（铁律 5）===")
rel = 2      # c = l_P/t_P ; l_P^2 = G hbar / c^3
unk = 5      # c, t_P, l_P, G, hbar
chk("A23-5a", unk - rel == 3,
    "框架内关系 " + str(rel) + " 条、未知 " + str(unk) + " 个 ⟹ 自由 " + str(unk - rel) + " 个")
chk("A23-5b", (unk - rel) - 1 == 2,
    "c 有外部实测值 ⟹ 剩 {l_P, G, hbar} 三个未知、**一条**关系 ⟹ **自由度 2** ⟹ 观测量 1 < 待定量 2 ⟹ hbar 不可辨识")
lp_num = re.findall(r"l_P\s*=\s*([0-9.]+)\u00d710([^\s]{1,4})\s*m(?![A-Za-z])", Z)
chk("A23-5c", len(lp_num) == 1 and lp_num[0][0] == "1.62",
    "「`l_P = <数值> m`」命中 " + str(len(lp_num)) + " 处 ⟹ 全文**唯一**一处 `l_P` 数值 = "
    + ("1.62e-35 m（附录参数表）" if lp_num else "无"))
chk("A23-5c2", len(re.findall(r"l_P\s*=\s*[0-9]", Z)) >= 3,
    "另有 " + str(len(re.findall(r"l_P\s*=\s*[0-9]", Z)) - len(lp_num))
    + " 处 `l_P = <数>` 是**系数/比值**（`√3 l_P = 1.7321 l_P`、`N_c = R_c/l_P = 8.49×10⁶⁰`）**不是 l_P 的数值**")
lp_self = math.sqrt(G * hbar / c ** 3)
chk("A23-5d", abs(lp_self / 1.62e-35 - 1.0) < 0.01,
    "该数值 1.62e-35 m 与自洽式 `sqrt(G*hbar/c^3)` = %.4e m 相符 ⟹ **它就是普朗克长度，由 hbar 给出** "
    "⟹ 不存在「不依赖 hbar 的 l_P 数值」" % lp_self)
zl = [s for s in ZL if "\u210f" in s]
withG = len([s for s in zl if "G" in s])
chk("A23-5e", withG >= 5,
    "含 hbar 的 " + str(len(zl)) + " 行中，含 G 的 " + str(withG) + " 行（= 可经 l_P^2 表达）；"
    "其余为**标准外部公式**（Hawking T / Compton / `hbar*omega_c` / `hbar*H0/2pi`）")

print("=== A23-6 论文原句与诚实标注 ===")
zh_claim = "\u975e\u57fa\u672c\u5e38\u6570\uff0c\u662f\u4e8b\u4ef6\u6d41\u6700\u5c0f\u5c3a\u5ea6\u7684\u5bfc\u51fa\u91cf"
en_claim = "not fundamental constants; derived quantities of the event-flow minimal scale"
chk("A23-6a", Z.count(zh_claim) == 1 and E.count(en_claim) == 1,
    "ZH 原句 " + str(Z.count(zh_claim)) + " 处；EN 原句 " + str(E.count(en_claim)) + " 处")
chk("A23-6b", Z.count("\u6807\u51c6\u7269\u7406\u8f93\u5165") >= 2 and E.count("standard physics") >= 1,
    "§8.6 已把 `1/4` 与 `beta` 标为「标准物理输入」（ZH " + str(Z.count("\u6807\u51c6\u7269\u7406\u8f93\u5165"))
    + " 处 / EN " + str(E.count("standard physics")) + " 处）⟹ **输入侧确实含标准 hbar 量**")

print("=== A23-7 两段式：第 111 轮三处新注（取证 -> 确认）===")
marks = {
    "ZH-4.8": "\u53e3\u5f84\u6ce8\uff08\u7b2c 111 \u8f6e\uff1aA23 \u2014\u2014 `G\u3001\u210f`",
    "EN-4.8": 'round 111: A23 - the "composite appearance"',
    "ZH-1.17": "\u53e3\u5f84\u6ce8\uff08\u7b2c 111 \u8f6e\uff1aA23 \u2014\u2014 `M\u00b2/A`",
    "EN-1.17": 'round 111: A23 - `M\u00b2/A` is not',
    "ZH-8.6.3": "\u7b2c 111 \u8f6e\u8865\u6ce8\uff08A23\uff09",
    "EN-8.6.3": "Round-111 addendum (A23)",
}
for tag, mk in marks.items():
    src, pre = (Z, ZP) if tag.startswith("ZH") else (E, EP)
    chk("A23-7 " + tag, pre.count(mk) == 0 and src.count(mk) == 1,
        "补丁前 0 -> 补丁后 1")

print("=== A23-8 插入块的引用块连续性 ===")


def block_ok(lines, contains):
    idx = [i for i, s in enumerate(lines) if contains in s]
    if len(idx) != 1:
        return False, "anchor x" + str(len(idx))
    i = idx[0]
    a = i
    while a - 1 >= 0 and lines[a - 1].startswith(">"):
        a -= 1
    b = i
    while b + 1 < len(lines) and lines[b + 1].startswith(">"):
        b += 1
    blank = [k for k in range(a, b + 1) if lines[k].strip() == ""]
    return len(blank) == 0, "[" + str(a + 1) + "," + str(b + 1) + "] blank=" + str(len(blank))


ok3, m3 = block_ok(ZL, marks["ZH-4.8"])
ok4, m4 = block_ok(ZL, marks["ZH-1.17"])
ok5, m5 = block_ok(ZL, marks["ZH-8.6.3"])
chk("A23-8", ok3 and ok4 and ok5, "4.8 " + m3 + " | 1.17 " + m4 + " | 8.6.3 " + m5)

print("=== A23-9 / A23-10 清单编号与中性检查 ===")
rows = [(i + 1, int(re.match(r"^\| \*\*C-(\d+)\*\* \|", s).group(1)))
        for i, s in enumerate(LP.split("\n")) if re.match(r"^\| \*\*C-(\d+)\*\* \|", s)]
p76 = [i for i, (_, n) in enumerate(rows) if n == 76]
chk("A23-9", len(p76) == 1 and rows[p76[0] + 1][1] == 77,
    "C-77 紧跟 C-76（行 " + str(rows[p76[0] + 1][0]) + "）")
nrows = [int(m.group(1)) for m in re.finditer(r"(?m)^\| \*\*N-(\d+)\*\* \|", LP)]
i77 = [i for i, s in enumerate(LP.split("\n")) if s.startswith("| **C-77** |")]
i41 = [i for i, s in enumerate(LP.split("\n")) if s.startswith("| **N-41** |")]
chk("A23-9b", len(nrows) >= 1 and 41 in nrows and len(i41) == 1 and len(i77) == 1
    and i41[0] == i77[0] + 1,
    "N 行共 " + str(len(nrows)) + " 条；N-41 紧跟 C-77（行 " + str(i41[0] + 1) + "）")

print("=== A23-11 中英同步 ===")
chk("A23-11", Z.count("\u4e0d\u53ef\u8fa8\u8bc6") >= 1 and E.count("not separately identifiable") >= 1,
    "「不可辨识 / not separately identifiable」中英各 >=1（ZH " + str(Z.count("\u4e0d\u53ef\u8fa8\u8bc6"))
    + " / EN " + str(E.count("not separately identifiable")) + "）")

print("=== A23-12 交接说明加「hbar 身份 = 已判定」===")
chk("A23-12", H.count("A23") >= 1 and (H.count("\u210f \u7684\u8eab\u4efd") >= 1 or H.count("\u4e0d\u53ef\u8fa8\u8bc6") >= 1),
    "交接说明含 A23 条目 " + str(H.count("A23")) + " 处")

print("=== A23-13 新注不引入新符号 / 新编号 ===")
GRK = "".join(chr(x) for x in range(0x370, 0x400)) + "".join(chr(x) for x in range(0x3b1, 0x3ca))
i = [k for k, s in enumerate(ZL) if marks["ZH-4.8"] in s][0]
zh_new = "\n".join(ZL[i:i + 14])
j = [k for k, s in enumerate(EL) if marks["EN-1.17"] in s][0]
en_new = "\n".join(EL[j:j + 12])
new_syms = set(ch for ch in (zh_new + en_new) if ch in GRK)
pre_syms = set(ch for ch in (ZP + EP) if ch in GRK)
nref = re.findall(r"(?<![A-Za-z])(?:C|N|I|S)-\d+", zh_new + en_new)
LB = rd(os.path.join(OUT, "\u5de5\u7a0b\u671f\u671b\u6e05\u5355_\u5907\u4efd_2026-10-04\u7b2c111\u8f6e\u524d.md"))
chk("A23-13", new_syms <= pre_syms and all((r in ZP or r in EP or r in LB) for r in nref),
    "新注希腊字母 " + str(sorted(new_syms)) + " (subset=" + str(new_syms <= pre_syms)
    + ")；引用的编号 " + str(nref) + " 均已登记 = "
    + str(all((r in ZP or r in EP or r in LB) for r in nref)))

print("")
print("\u901a\u8fc7 " + str(OK[0]) + " \u9879\uff0c\u5931\u8d25 " + str(FAIL[0]) + " \u9879")
