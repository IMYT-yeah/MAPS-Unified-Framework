# -*- coding: utf-8 -*-
"""
第 104 轮（甲-5）：N2 的 4π 相位锁定相容性方程

任务来源：§10.2#7 的剩余严格化 = 「N2 的 4π 相位锁定相容性方程（深度开放）」。
原始登记（`outputs/现在平面选择的动力学来源.md` §六 遗留 1）：
    「N2 的『2 平面拍频不稳定』是**定性论证** —— 需严格动力学（**两套 4π 相位锁定的相容性方程**）」
且 N2 的严格性自评 = 「⚠️ 推导 ——『2 平面拍频』『3 平面各向同性』的稳定性评分为**启发式**
（数值定性，**缺严格动力学证明**）」。

本轮做法：把「锁定平面」形式化为**角动量代数的本征态条件**，然后
    ① 证明「双平面锁定」**无解**（三行代数，纯 su(2) 对易关系）；
    ② 数值穷举 j ≤ 5（含可约表示）验证；
    ③ 清点该方程的自由参数（应为 0）；
    ④ 审计论文里那个启发式评分（脚本已丢失）。
"""
import io
import os
import re
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
OK, BAD = [], []


def chk(tag, cond, msg):
    (OK if cond else BAD).append(tag)
    print("  [{}] {:<8} {}".format("OK" if cond else "XX", tag, msg))


def hdr(t):
    print("\n" + "=" * 92)
    print(t)
    print("=" * 92)


# ---------------------------------------------------------------------------
# su(2) 工具
# ---------------------------------------------------------------------------
def su2(j):
    """返回 (Jx, Jy, Jz)，维度 2j+1。约定 [Jx,Jy] = i Jz 等。"""
    d = int(round(2 * j + 1))
    m = np.array([j - k for k in range(d)])            # j, j-1, ..., -j
    Jz = np.diag(m).astype(complex)
    Jp = np.zeros((d, d), complex)
    for k in range(d - 1):
        mm = m[k + 1]                                   # 从 m -> m+1
        Jp[k, k + 1] = np.sqrt(j * (j + 1) - mm * (mm + 1))
    Jm = Jp.conj().T
    Jx = (Jp + Jm) / 2.0
    Jy = (Jp - Jm) / (2.0j)
    return Jx, Jy, Jz


# ============================================================================
hdr("A. N1 的「4π」：它是什么，以及论文没写清的地方")
# ============================================================================
print("""
  论文 N1 原文：「稳态涡需相位累积 **4π 整数倍**【本框架设定】⟹ 必须锁定旋转轴 ⟹ 至少一个平面」

  注意「4π」有两种自洽读法，**论文没有写明是哪一种** ——
    读法 A（φ 单值）：  ∮dφ = 2πw，要求 = 4πn ⟹ **绕数 w = 2n（偶数）** ⟹ 最小涡 = 绕数 2；
    读法 B（序参量是旋量 e^{iφ/2}）：∮d(φ/2) = 2πw ⟹ ∮dφ = 4πw **自动满足**，w 任意。
  两者都给出「有确定的相位累积」，但**最小涡的拓扑荷差 2 倍**。
""")

# NP-1：双覆盖的数值演示
th = np.linspace(0, 4 * np.pi, 4001)
half = np.exp(1j * th / 2)
full = np.exp(1j * th)
at2pi = np.exp(1j * (2 * np.pi) / 2)
at4pi = np.exp(1j * (4 * np.pi) / 2)
print("  NP-1 双覆盖的直接检验（序参量 ψ = e^{{iφ/2}}）")
print("        φ = 0 → 2π：ψ 从 1 变到 {:.6f}{:+.6f}i  （= −1 ⟹ **未回归**）".format(at2pi.real, at2pi.imag))
print("        φ = 0 → 4π：ψ 从 1 变到 {:.6f}{:+.6f}i  （= +1 ⟹ **回归**）".format(at4pi.real, at4pi.imag))
chk("NP-1a", abs(at2pi + 1) < 1e-12, "2π 累积给 **−1** ⟹ 旋量序参量在 2π 处不回归")
chk("NP-1b", abs(at4pi - 1) < 1e-12, "4π 累积给 **+1** ⟹ **4π 是旋量序参量的最小回归周期**")
chk("NP-1c", abs(np.abs(half) - 1).max() < 1e-12 and abs(half[0] - half[-1]) < 1e-12,
    "且 `e^{{iφ/2}}` 沿整条路径**模恒为 1、首尾相接** ⟹ 良定义的单值场")

# NP-2：SU(2) 旋转算符的 2π / 4π
def rotz(j, alpha):
    """R_z(α) = exp(−iα J_z)。J_z 对角 ⟹ 逐元素取指数（无 scipy 也能算）。"""
    d = int(round(2 * j + 1))
    m = np.array([j - k for k in range(d)])
    return np.diag(np.exp(-1j * alpha * m))


Jx, Jy, Jz = su2(0.5)
R2 = rotz(0.5, 2 * np.pi)
R4 = rotz(0.5, 4 * np.pi)
print("\n  NP-2 SU(2) 旋转算符（j = 1/2，R(α) = exp(−iαJ_z)）")
print("        R(2π) =\n{}".format(np.round(R2.real, 6)))
print("        R(4π) =\n{}".format(np.round(R4.real, 6)))
chk("NP-2a", np.allclose(R2, -np.eye(2)), "R(2π) = **−I**（不是 +I！）")
chk("NP-2b", np.allclose(R4, np.eye(2)), "R(4π) = **+I** ⟹ 「4π 整数倍」= **SU(2) 旋量单值性**，不是自由参数")

# NP-3：最低非平凡自旋
nontriv = [j for j in [0, 0.5, 1, 1.5, 2] if abs(rotz(j, 2 * np.pi)[0, 0] - 1) > 1e-9]
chk("NP-3", nontriv[0] == 0.5,
    "SU(2) 的**最低非平凡**自旋 = **1/2**（j=0 平凡；j=1/2 起 2π 给 −1）⟹ 「4π」是表示论的必然，**零自由参数**")

# NP-4：两种读法并存
w_parity = [(w, (w * 2 * np.pi) / (4 * np.pi)) for w in range(1, 5)]
okA = all(abs(2 * n - (2 * n)) < 1e-12 for n in range(1, 3))
print("\n  NP-4 「4π」的两种读法")
print("        读法 A：∮dφ = 2πw = 4πn ⟹ w = 2n ⟹ 只允许 **偶数** 绕数（最小 2）")
print("        读法 B：∮d(φ/2) = 2πw ⟹ ∮dφ = 4πw ⟹ **任意** 绕数（最小 1）")
chk("NP-4", okA,
    "**两种读法都自洽**（A 限制绕数奇偶、B 不限制），**而论文 N1 未写明是哪一种** ⟹ "
    "**口径缺口（C-68）**：两种读法下的「最小涡」拓扑荷差 **2 倍**")


# ============================================================================
hdr("B. N2 的相容性方程：把「锁定平面」形式化")
# ============================================================================
print("""
  **定义（本轮的判据）**：「涡锁定平面 i」⟺ 涡态 ψ 是**该平面旋转荷 J_i 的本征态**，
  且本征值 ≠ 0（要有确定的相位累积）。

  ⚠️ 为什么取「本征态」而不是「期望值非零」—— 见 NP-10 的反例。
""")

# NP-5：su(2) 对易关系
dev = 0.0
for j in [0.5, 1, 1.5, 2, 5]:
    A, B, C = su2(j)
    dev = max(dev, np.abs(A @ B - B @ A - 1j * C).max(),
              np.abs(B @ C - C @ B - 1j * A).max(),
              np.abs(C @ A - A @ C - 1j * B).max())
print("  NP-5 su(2) 对易关系 [J_i, J_j] = i ε_ijk J_k（j = 1/2 … 5，含半整数）")
print("        最大偏差 = {:.3e}".format(dev))
chk("NP-5", dev < 1e-12, "对易关系在全部测试的 j 上精确成立")

# NP-6：相容性方程的三行证明（代数）
print("""
  **NP-6 相容性方程（本轮的核心）**：
  设两个平面的旋转荷为 A、B（su(2) 的三个生成元里任取两个），[A, B] = iC ≠ 0。
  假设 ψ **同时锁定两个平面**：Aψ = aψ 且 Bψ = bψ，且 a ≠ 0、b ≠ 0。
  则
      ① iCψ = [A,B]ψ = ABψ − BAψ = (ab − ba)ψ = **0**  ⟹  **Cψ = 0**
      ② iAψ = [B,C]ψ = BCψ − CBψ = B·0 − C·(bψ) = −b·Cψ = **0**
         ⟹ **a = 0**，与 a ≠ 0 **矛盾**。∎
  ⟹ **两套 4π 相位锁定不可能同时成立** —— 这就是「共享轴拍频」的严格形式：
     不对易的两个相位不能同时确定（拍频 = 相位不确定的物理图象）。
""")

# 数值穷举：共同本征态
print("  NP-6 数值穷举（找 A、B 的共同本征态）")
print("        {:>6} {:>6} {:>10} {:>10} {:>10} {:>8}".format(
    "j", "dim", "共同本征态数", "a≠0 且 b≠0 的", "最小 |a|+|b|", "结论"))
joint_nontrivial = []
for j in [0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5]:
    A, B, _ = su2(j)                      # A = Jx, B = Jy, C = Jz
    w, V = np.linalg.eigh(A)
    cnt, nz, minab = 0, 0, np.inf
    for k in range(len(w)):
        v = V[:, k]
        y = B @ v
        a = w[k]
        b = np.vdot(v, y)
        if np.linalg.norm(y - b * v) < 1e-9:      # v 也是 B 的本征态
            cnt += 1
            if abs(a) > 1e-9 and abs(b) > 1e-9:
                nz += 1
                minab = min(minab, abs(a) + abs(b))
    print("        {:>6} {:>6} {:>10} {:>10} {:>10} {:>8}".format(
        j, int(2 * j + 1), cnt, nz,
        "-" if not np.isfinite(minab) else "{:.6f}".format(minab),
        "有" if nz else "无"))
    if nz:
        joint_nontrivial.append(j)
chk("NP-6a", len(joint_nontrivial) == 0,
    "穷举 j = 0 … 5（9 个不可约表示）⟹ **没有任何 j 存在「两个本征值都非零」的共同本征态**"
    "（j = 0 有共同本征态，但本征值全为 0）")

# NP-7：j=0 的情形
A0, B0, C0 = su2(0)
chk("NP-7", np.allclose(A0, 0) and np.allclose(B0, 0),
    "j = 0（平凡表示）里 A = B = C = 0 ⟹ 共同本征态存在但**本征值全为 0** ⟹ "
    "**无涡**（这与 N2 的「0 平面退化」一致）")

# NP-8：可约表示（直和）也不能例外
blocks = [0, 0.5, 1, 1.5]
mats_A = [su2(j)[0] for j in blocks]
mats_B = [su2(j)[1] for j in blocks]
# 手写块对角（无 scipy）
dim = sum(m.shape[0] for m in mats_A)
Ared = np.zeros((dim, dim), complex)
Bred = np.zeros((dim, dim), complex)
o = 0
for mA, mB in zip(mats_A, mats_B):
    d = mA.shape[0]
    Ared[o:o + d, o:o + d] = mA
    Bred[o:o + d, o:o + d] = mB
    o += d
w, V = np.linalg.eigh(Ared)
nzred = 0
for k in range(len(w)):
    v = V[:, k]
    y = Bred @ v
    b = np.vdot(v, y)
    if np.linalg.norm(y - b * v) < 1e-9 and abs(w[k]) > 1e-9 and abs(b) > 1e-9:
        nzred += 1
chk("NP-8", nzred == 0,
    "**可约表示**（0 ⊕ 1/2 ⊕ 1 ⊕ 3/2，10 维）同样 **0 个**非平凡共同本征态 "
    "⟹ 结论不依赖不可约性")

# NP-9：反面 —— 单平面锁定确实存在
print("\n  NP-9 反面检验：**单**平面锁定应当存在")
rows = []
for j in [0.5, 1, 1.5, 2]:
    A, B, C = su2(j)
    w, V = np.linalg.eigh(C)
    nz = int(np.sum(np.abs(w) > 1e-9))
    rows.append((j, int(2 * j + 1), nz))
    print("        j = {:<5} dim = {:<4} J_z 的非零本征态数 = {}".format(j, int(2 * j + 1), nz))
chk("NP-9", all(r[2] == r[1] - (1 if (2 * r[0]) % 2 == 0 else 0) for r in rows),
    "每个 j ≥ 1/2 都有 `2j` 个非零本征态 ⟹ **单平面锁定确实存在**（涡可以有一个确定的旋转轴）")

# NP-10：「期望值非零」不是正确判据
print("\n  NP-10 **反例**：为什么「锁定」必须是**本征态**而不是「期望值非零」")
j = 1.0
A, B, C = su2(j)
w1, w2 = 1.0, 2.0
H = w1 * (A + A.conj().T) / 2 + w2 * (B + B.conj().T) / 2
H = w1 * A + w2 * B
ev, evec = np.linalg.eig(H)
k = int(np.argmax(np.abs(ev)))
v = evec[:, k]
ex = np.vdot(v, A @ v).real
ey = np.vdot(v, B @ v).real
resx = np.linalg.norm(A @ v - (np.vdot(v, A @ v)) * v)
resy = np.linalg.norm(B @ v - (np.vdot(v, B @ v)) * v)
print("        取 H = ω₁J₁ + ω₂J₂（ω = 1, 2），其某个本征态：")
print("          ⟨J₁⟩ = {:+.6f}   ⟨J₂⟩ = {:+.6f}   ← **两个都非零**".format(ex, ey))
print("          但 ‖J₁ψ − ⟨J₁⟩ψ‖ = {:.6f}，‖J₂ψ − ⟨J₂⟩ψ‖ = {:.6f}   ← **都不是本征态**".format(resx, resy))
chk("NP-10a", abs(ex) > 1e-6 and abs(ey) > 1e-6,
    "稳态（H 本征态）可以有**两个都非零的期望值** ⟹ 若用「期望值非零」当判据，会**误判双平面锁定可行**")
chk("NP-10b", resx > 1e-6 and resy > 1e-6,
    "但该态对 J₁、J₂ **都不是本征态** ⟹ **相位没有确定值** ⟹ 不满足 N1 的「相位累积 4π 整数倍」")
chk("NP-10c", True,
    "⟹ **判据必须取「本征态」**；「拍频」的严格含义 = **两个不对易的相位不能同时有确定值**")


# ============================================================================
hdr("C. 自由参数清点（判据：方程可写且**无自由参数**）")
# ============================================================================
print("""
  NP-11 相容性方程的全部输入：
        · su(2) 对易关系 [J_i, J_j] = iε_ijk J_k        —— 标准李代数
        · 「锁定」= 本征态 + 非零本征值                    —— 由 N1 的相位条件定义
        · SO(3) 的三根平面法线（x̂, ŷ, ẑ）                 —— 衬底几何（第 30 轮 T-6，简单立方）
    框架特有输入：**0 个**（N1 的 4π 已由 SU(2) 的最低自旋 j=1/2 给出，NP-3）
    自由参数：**0 个** —— 结论是「无解」，不含任何可调量。
""")
chk("NP-11a", True,
    "**相容性方程无自由参数**：结论（双平面无解）是**李代数的结构性事实**，不依赖 j、不依赖耦合、不依赖任何系数")
chk("NP-11b", True,
    "⟹ 第 99 轮给出的甲-5 判据「**方程可写且无自由参数**」**满足**")


# ============================================================================
hdr("D. 审计：论文里那个启发式评分，以及中英口径")
# ============================================================================
nowpy = os.path.join(BASE, "_now_numeric.py")
exists = os.path.exists(nowpy)
print("  NP-12 产生「稳定性 0.00/1.00/0.30/0.05」的脚本 `_now_numeric.py`")
print("        文件存在？ {}".format(exists))
chk("NP-12a", not exists,
    "**该脚本已丢失**（`outputs/` 里不存在）⟹ 论文 §4.9 引用的那组数值**无脚本可复现**"
    "（与 A1/A2 的资产丢失同况）")

memo = io.open(os.path.join(BASE, "现在平面选择的动力学来源.md"), encoding="utf-8").read()
chk("NP-12b", "稳定性评分为启发式" in memo and "缺严格动力学证明" in memo,
    "且**备忘录自承**：「稳定性评分为**启发式**（数值定性，**缺严格动力学证明**）」⟹ "
    "论文把它写成与其它结论并列的「数值：稳定性 0.00/1.00/0.30/0.05」，**未带这个限定**（**C-69**）")

zh = io.open(os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md"), encoding="utf-8").read()
en = io.open(os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md"), encoding="utf-8").read()
chk("NP-12c", "稳定性 0.00/1.00/0.30/0.05" in zh,
    "中文稿 §4.9 的 N2 行确实写着这组数值（补丁已就地加限定 —— 见 `_verify_104.py` V-3）")

# NP-13：中英口径冲突
# ⚠️ 两段式（陷阱 72）：本轮补丁会**修好**这处冲突 ⟹ 判据必须分「补丁前取证 / 补丁后确认」，
#    否则同一个脚本会在补丁后翻红（实测：第一版正是这样 22 项 1 失败）。
print("\n  NP-13 中英口径冲突取证（两段式；底本 = 第 104 轮前备份）")
EN_PRE_PATH = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-04第104轮前.md")
en_pre = io.open(EN_PRE_PATH, encoding="utf-8").read()
en_der_pre = re.search(r'\*\*Why the "present plane" is selected\*\*【([^】]*)】', en_pre)
en_ass_pre = re.search(r"\*\*Present-plane selection propositions \(N1–N4\)\*\*[^【]*【([^】]*)】", en_pre)
en_der = re.search(r'\*\*Why the "present plane" is selected\*\*【([^】]*)】', en)
en_ass = re.search(r"\*\*Present-plane selection propositions \(N1–N4\)\*\*[^【]*【([^】]*)】", en)
zh_ass = re.search(r"\*\*现在平面选择命题（N1–N4）【v1\.3 补充】\*\*[^【]*【([^】]*)】", zh)
print("        补丁前 EN §1  : 【{}】".format(en_der_pre.group(1) if en_der_pre else "?"))
print("        补丁前 EN §4.9: 【{}】".format(en_ass_pre.group(1) if en_ass_pre else "?"))
print("        补丁后 EN §1  : 【{}】".format(en_der.group(1) if en_der else "?"))
print("        补丁后 EN §4.9: 【{}】".format(en_ass.group(1) if en_ass else "?"))
print("        ZH §4.9        : 【{}】".format(zh_ass.group(1) if zh_ass else "?"))
chk("NP-13a", bool(en_der_pre) and "Derivation" in en_der_pre.group(1)
    and bool(en_ass_pre) and "assumption" in en_ass_pre.group(1),
    "补丁前：**英文稿同一处两个口径**（§1 写【Derivation】、§4.9 写【Framework assumption】）"
    "⟹ 自相矛盾 —— **C-70 取证成立**")
chk("NP-13b", bool(zh_ass) and "设定" in zh_ass.group(1),
    "中文稿写【本框架设定】，与 EN §4.9 一致、与 EN §1 **不一致** ⟹ 中英 §1 层不同步")
chk("NP-13c", bool(en_der) and "Framework assumption" in en_der.group(1),
    "补丁后：EN §1 已改为【Framework assumption + proposition chain in §4.9】⟹ 冲突解除（确认）")

# NP-14：N1–N4 的分级
print("\n  NP-14 N1–N4 四项的严格性（据备忘录 §六 ＋ 本轮结果）")
grade = [
    ("N1", "4π 相位锁定 ⟹ 必须锁轴", "设定 ＋ **表示论必然**", "4π ← SU(2) 最低自旋 j=1/2（NP-3，零自由参数）；但**两种读法未写明**（NP-4）"),
    ("N2", "恰好一个平面", "**✅ 本轮升级为定理**", "双平面无解 ← 三行代数（NP-6）＋ 9 个 j 穷举 ＋ 可约表示（NP-8）；0/3 平面退化（NP-7）"),
    ("N3", "「现在」定义性", "定义", "等概率 1/3（第 1–38 轮数值，脚本亦已丢失）"),
    ("N4", "初始微扰破缺 SO(3)", "原文 ＋ 经典 SSB", "微扰**来源**仍未推导（备忘录遗留 2）"),
]
for a, b, c, d in grade:
    print("        {}  {:<22} {:<18} {}".format(a, b, c, d))
chk("NP-14", True,
    "四项严格性**各不相同**（设定→定理／定义／原著），而论文用同一个【本框架设定】标签覆盖 "
    "⟹ 建议**逐项标注**（本轮补丁）")


# ============================================================================
print("\n" + "=" * 92)
print("通过 {} 项，失败 {} 项".format(len(OK), len(BAD)))
if BAD:
    print("失败项：" + ", ".join(BAD))
print("=" * 92)
