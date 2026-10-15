# -*- coding: utf-8 -*-
"""第 95 轮：候选池清尾（#1 η 能标 / #2 暗能量能标 / #4 η/s / #6 规范群结构）—— 形式结项审计。
CP-1 … CP-10，纯标准库 + math。

⚠️ 底本 = 补丁前备份（铁律 18/20）：本轮审计的是补丁前状态（论文里 §8.4 的【推导】句、
   池条目的「未结项」状态），补丁后状态由 `_verify_95.py` 两段式确认。
"""
import io, math, os

BAD = 0; OK = 0
def chk(tag, ok, msg, strict=True):
    global BAD, OK
    if ok:
        OK += 1; print("  [OK] {:<8} {}".format(tag, msg))
    elif strict:
        BAD += 1; print("  [XX] {:<8} {}".format(tag, msg))
    else:
        print("  [--] {:<8} {}".format(tag, msg))

def hdr(s): print("\n" + "=" * 100 + "\n" + s)

ZH_BASE = "论文初稿_正反物质对风暴统一框架_v2.9"
ZH_P = ZH_BASE + "_备份_2026-10-02第95轮前.md"   # 底本
EN_P = "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-02第95轮前.md"
LI_P = "工程期望清单_备份_2026-10-02第95轮前.md"
print("[底本] 一律读 *_备份_2026-10-02第95轮前.md（当前稿状态见 _verify_95.py）")

Z = io.open(ZH_P, encoding="utf-8").read()
E = io.open(EN_P, encoding="utf-8").read()
L = io.open(LI_P, encoding="utf-8").read()

# ---------------------------------------------------------------- CP-1
hdr("CP-1  三份源头文档存在 + 判决句取证（candidate-pool 三条的判定来源）")
SRC = {
    "从A2推组分_暗能量能标已定.md": ["复算不是预言", "独立解释", "23.76 倍", "CM-1", "CM-5"],
    "ΩΛ缺口判决_二选一与放弃.md": ["二选一", "该放弃", "465", "23.7622", "OM-1"],
    "工程路径评估_超导是不是前置的前置.md": ["KSS"],
}
for f, keys in SRC.items():
    if not os.path.exists(f):
        chk("CP-1", False, "源头文档缺失：" + f); continue
    t = io.open(f, encoding="utf-8").read()
    miss = [k for k in keys if k not in t]
    chk("CP-1", not miss, "《{}》{} 字符；判决句 {}（缺 {}）".format(f[:26], len(t), "全在" if not miss else "有缺", miss or "无"))

# ---------------------------------------------------------------- CP-2
hdr("CP-2  ⭐ #2 缺口量化：判决核心内容在论文（底本）里 = 0 处")
for k in ["23.76", "23.8 倍", "二选一", "放弃"]:
    n = Z.count(k)
    print("    论文「{}」= {} 处".format(k, n))
chk("CP-2a", Z.count("23.76") == 0 and Z.count("二选一") == 0,
    "「23.76」（0 处）＋「二选一」（0 处）⟹ **判决核心 25 天未进论文**（2026-09-17 → 本轮）")
n0 = Z.count("0.0290")
# ⚠️ 第一版把期望值写死成 1 ⟹ 假 FAIL（实际 2 处：§8.6.5 块内正文 + 诚实边界引用）。
#    教训 = 陷阱 82⑦：**期望值不要写死**；判据应是「数值在、报告词不在」这个不对称。
chk("CP-2b", n0 >= 1 and Z.count("23.76") == 0,
    "数值 `0.0290` 在论文里（{} 处，均在第 73 轮宇宙学审计块内），但**判决核心词（23.76/二选一）0 处** ⟹ 与判决**不连接**".format(n0))
key84 = "【推导】暗能量 = ε_A 饱和区贡献 ρ_Λ ~ (E_c)⁴"
chk("CP-2c", key84 in Z, "§8.4 的【推导】句在场（判决**未同步**的落点）")
key812 = "（(E_c)⁴ 差 27 倍，O(1) 系数待定）"
chk("CP-2d", key812 in Z, "§8.1 截断能标句里「O(1) 系数待定」在场（判决**未同步**的第二落点）")

# ---------------------------------------------------------------- CP-3
hdr("CP-3  #2 复算：Ω_Λ 缺口 = 23.76 倍（两条路互验）")
c = 2.99792458e8
G = 6.67430e-11
hbar_c_eVm = 1.97327e-7          # eV·m
eV_J = 1.602176634e-19
rho_crit = 7.7282e-10            # J/m³（OM 输入；见 CP-3c 自洽检查）
Ec_meV = 1.0181
# 路线 1：ρ_Λ = E_c⁴/(ℏc)³
rhoL = (Ec_meV * 1e-3) ** 4 / hbar_c_eVm ** 3 * eV_J
Om_L = rhoL / rho_crit
print("  路线1  ρ_Λ = E_c⁴/(ℏc)³ = {:.4e} J/m³  ⟹ Ω_Λ = {:.5f}".format(rhoL, Om_L))
chk("CP-3a", abs(Om_L - 0.028991) / 0.028991 < 0.02,
    "复算 Ω_Λ = {:.5f}，OM 记录 0.028991（相对差 {:.1%}）".format(Om_L, abs(Om_L - 0.028991) / 0.028991))
gap = 0.6889 / Om_L
chk("CP-3b", abs(gap - 23.76) / 23.76 < 0.02,
    "缺口 = 0.6889 / {:.5f} = **{:.2f} 倍**（OM 记录 23.76）".format(Om_L, gap))
# CP-3c：ρ_crit 反推 H0 自洽
rhop = rho_crit / c ** 2
H0 = math.sqrt(8 * math.pi * G * rhop / 3)
H0_kms = H0 * 3.0856775814913673e22 / 1000
chk("CP-3c", 65 < H0_kms < 70,
    "ρ_crit = 7.7282e-10 J/m³ ⟺ H₀ = **{:.2f} km/s/Mpc**（Planck 域，自洽 ✓）".format(H0_kms))
# CP-3d：闭式
lP = math.sqrt(1.054571817e-34 * G / c ** 3)
RH = c / H0
eps0, beta = 7.7e-20, 0.615
Om_closed = (8 * math.pi / 3) * (RH / lP) ** 2 * eps0 ** (4 / beta)
chk("CP-3d", abs(Om_closed - 0.028991) / 0.028991 < 0.05,
    "闭式 8π/3·(R_H/l_P)²·ε₀^{{4/β}} = {:.5f}（与路线 1 同量级 ✓，两条路互验）".format(Om_closed))
# CP-3e：数值占卜拒绝表
print("  拒绝数值占卜（目标因子 = {:.4f}）：".format(gap))
cands = [("4! = 24", 24.0), ("e^π", math.e ** math.pi), ("π⁴/4", math.pi ** 4 / 4), ("8π", 8 * math.pi)]
worst = []
for name, v in cands:
    dev = (v / gap - 1) * 100
    worst.append(abs(dev))
    print("    {:<8} = {:.4f}  偏差 {:+.2f}%".format(name, v, dev))
chk("CP-3e", min(worst) > 0.9,
    "最接近的天然因子偏差 {:.2f}% ⟹ 凑得上的不少、**有机制的没有**（拒绝数值占卜）".format(min(worst)))

# ---------------------------------------------------------------- CP-4
hdr("CP-4  #2 二选一复算：保住能标 ⟹ 放弃 ρ_Λ；配住 Ω_Λ ⟹ 破坏能标与 η")
MPl_eV = 1.22089e28
def Ec_of(eps, b): return MPl_eV * eps ** (1 / b) * 1e3    # → meV
def Om_of(eps, b):
    ec = MPl_eV * eps ** (1 / b)                            # eV
    return ec ** 4 / hbar_c_eVm ** 3 * eV_J / rho_crit
A = (7.7e-20, 0.615)
B = (4.696e-20, 0.62887)
for tag, (eps, b), want_ec, want_om in [("选项 A（当前）", A, 1.018, 0.0290), ("选项 B（联立）", B, 2.248, 0.6889)]:
    ec, om = Ec_of(eps, b), Om_of(eps, b)
    print("  {}  β={:.5f} ε₀={:.3e}  ⟹ E_c={:.3f} meV（记 {:.3f}）  Ω_Λ={:.4f}（记 {:.4f}）".format(
        tag, b, eps, ec, want_ec, om, want_om))
chk("CP-4a", abs(Ec_of(*A) - 1.018) < 0.02 and abs(Om_of(*A) - 0.0290) < 0.0015,
    "选项 A 复算复现 OM 表（E_c 卡在 1.018 meV ✓、Ω_Λ 仍差 23.8× ✗）")
chk("CP-4b", abs(Ec_of(*B) - 2.248) < 0.05 and abs(Om_of(*B) - 0.6889) < 0.01,
    "选项 B 复算复现 OM 表（Ω_Λ 配住 ✓、E_c 变成 2.25 meV ✗ = 2.2×E_c）")
chk("CP-4c", abs(Om_of(*A) - 0.0290) < 0.0015 and abs(Om_of(*B) - 0.6889) < 0.01,
    "**二选一成立**：能标对 ⟺ 密度错 23.8×；密度对 ⟺ 能标错 2.2×（不可兼得）")

# ---------------------------------------------------------------- CP-5
hdr("CP-5  ⭐⭐ #1 单参数族：任意能标 E* 都能配住两个锚点 ⟹ 能标不被框架约束")
eta_obs = 6.14e-10
meV_eV = 1e-3
print("  给定任意 E*，解 β*(E*) = ln(1/η)/ln(E*/1meV)、ε₀* = (1meV/M_Pl)^{β*} ⟹ 两锚点逐一验证：")
allok = True
for Estr, Estar_TeV in [("0.246 TeV（电弱）", 0.246), ("0.969 TeV（反解值）", 0.969), ("5 TeV", 5.0), ("100 TeV", 100.0)]:
    Estar_eV = Estar_TeV * 1e12
    b = math.log(1 / eta_obs) / math.log(Estar_eV / meV_eV)
    eps = (meV_eV / MPl_eV) ** b
    e1 = eps * (MPl_eV / meV_eV) ** b        # ε(1 meV)
    e2 = eps * (MPl_eV / Estar_eV) ** b      # ε(E*)
    d1, d2 = abs(e1 - 1), abs(e2 / eta_obs - 1)
    ok = d1 < 1e-10 and d2 < 1e-10
    allok &= ok
    print("    E* = {:<16} β* = {:.4f}  ε(1meV) = {:.12f}   ε(E*) = {:.4e}（η 相对差 {:.1e}）".format(
        Estr, b, e1, e2, d2))
chk("CP-5a", allok, "**任意** E*（0.246 → 100 TeV）都精确配住两个锚点（相对差 < 1e-10）⟹ **一维简并族**")
b969 = math.log(1 / eta_obs) / math.log(0.969e12 / meV_eV)
chk("CP-5b", abs(b969 - 0.615) < 0.005,
    "反解值 E* = 0.969 TeV 给 β* = {:.4f} ≈ 论文 0.615 ✓（0.969 TeV 就是「让 ε = η 的那个能标」——反解，非预言）".format(b969))

# ---------------------------------------------------------------- CP-6
hdr("CP-6  #1 机制判否：框架没有「重子能标」机制")
n_ew = Z.count("电弱")
lines_ew = [i for i, s in enumerate(Z.split("\n"), 1) if "电弱" in s]
print("  论文「电弱」= {} 处（行 {}）".format(n_ew, lines_ew))
for i in lines_ew:
    print("    L{}| {}".format(i, Z.split("\n")[i - 1][:110]))
chk("CP-6a", n_ew <= 3, "「电弱」仅 {} 处，且均非「重子能标机制」（逐行核对见上）".format(n_ew))
k2 = "重子能标"
chk("CP-6b", Z.count(k2) == 0, "论文「{}」= {} 处 ⟹ **框架没有任何重子能标机制**".format(k2, Z.count(k2)))
cm = io.open("从A2推组分_暗能量能标已定.md", encoding="utf-8").read()
chk("CP-6c", "框架没给出它" in cm and "选来配 η 的" in cm,
    "CM-2 判据句在档：「E = 1 TeV 是选来配 η 的」「**框架没给出它**」")

# ---------------------------------------------------------------- CP-7
hdr("CP-7  #4 η/s：判定已存在（H2 ✅），池条目与台账双轨核对")
h2 = [s for s in L.split("\n") if s.startswith("| **H2")]
chk("CP-7a", len(h2) == 1 and "✅" in h2[0], "清单 H2 行在场且已标 ✅（S-3 收口：两条判别预言**都不独有**）")
ks = [i for i, s in enumerate(L.split("\n"), 1) if "KSS 界，2001" in s]
chk("CP-7b", len(ks) >= 1, "清单里「KSS 界，2001」在场（行 {}）⟹ 「η/s → 1/4π」= **postdiction / 一致性**".format(ks))
pool4 = [i for i, s in enumerate(L.split("\n"), 1) if s.startswith("4. **湍流 / 输运**")]
chk("CP-7c", len(pool4) == 1 and "✅" not in L.split("\n")[pool4[0] - 1],
    "⚠️ 池条目 #4 仍是**未结项**形态（双轨不一致：" + "H2 已收口 vs 池条目挂起" + "）")

# ---------------------------------------------------------------- CP-8
hdr("CP-8  池表四条现状（结项前取证）")
LN = L.split("\n")
for tag, pat in [("#1", "1. **重子不对称 η**"), ("#2", "2. **暗能量能标**"),
                 ("#4", "4. **湍流 / 输运**"), ("#6", "6. **规范群结构（§5）**")]:
    idx = [i for i, s in enumerate(LN, 1) if s.startswith(pat)]
    if idx:
        s = LN[idx[0] - 1]
        has = "✅" in s
        print("  {} 行{}：{} {}".format(tag, idx[0], "已标 ✅" if has else "**未结项**", s[:96]))
        chk("CP-8" + tag[1:], not has, "{} = 结项前状态（未标 ✅）".format(tag))
print("  ⚠️ **四条未结项**（#1/#2/#4/#6）—— 第 93/94 轮回顾只说「#1/#2/#4」，**漏了 #6**（C-18 族：回顾过度声明）")

# ---------------------------------------------------------------- CP-9
hdr("CP-9  英文稿（EN）对应落点")
EN_L = E.split("\n")
en838 = [i for i, s in enumerate(EN_L, 1) if "0.969 TeV" in s and "fitted" in s]
chk("CP-9a", len(en838) == 1, "EN「0.969 TeV, **fitted**」在场（L{}，储能块语境）".format(en838))
en84 = [i for i, s in enumerate(EN_L, 1) if "Dark energy = contribution of the ε_A saturation region ρ_Λ ~ (E_c)⁴" in s]
chk("CP-9b", len(en84) == 1, "EN §8.4【Derivation】句在场（L{}，判决未同步的落点）".format(en84))
en812 = [i for i, s in enumerate(EN_L, 1) if "O(1) coefficient undetermined" in s or "O(1) coefficient undet" in s]
chk("CP-9c", len(en812) >= 1, "EN §8.1「O(1) coefficient undet…」（L{}）在场".format(en812[:2]))
enp4 = [i for i, s in enumerate(EN_L, 1) if "three sources, one origin" in s]
chk("CP-9d", len(enp4) >= 1, "EN P4「three sources, one origin」在场（L{}）⟹ 4 处 EN 落点齐备".format(enp4[:3]))

# ---------------------------------------------------------------- CP-10
hdr("CP-10  编号可用性 + 综合判决")
for code in ["N-40", "C-54", "C-55"]:
    chk("CP-10-" + code, L.count(code) == 0, "{} 未被占用（可登记）".format(code))
print()
print("  综合判决（形式结项）：")
print("    #1 η 能标：**半拟合**（一维简并 ⟹ 能标不被约束）；「独立解释为何 ~1 TeV」= **判否** ⟹ N-40")
print("    #2 暗能量能标：判决（2026-09-17）**保住 meV 量级 / 放弃 ρ_Λ = E_c⁴ 定量识别**；")
print("       论文从未同步（CP-2）⟹ 补录 = **C-54**")
print("    #4 η/s：postdiction / 一致性（KSS 2001）；池条目与 H2 双轨不一致 ⟹ 并入 **C-55**")
print("    #6 规范群结构：结构对应 = 解释性（判别力 0）；数值映射 = 判否（**N-34**）⟹ 结项")
print("    ⟹ 候选池清尾后剩余 = **EMRI**（等 LISA）＋ **A1**（换机资产）")

print()
print("=" * 100)
print("通过 {} 项，失败 {} 项".format(OK, BAD))
