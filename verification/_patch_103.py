# -*- coding: utf-8 -*-
"""第 103 轮（甲-4）补丁：论文中英同步 ＋ 清单 ＋ 交接说明。

铁律 74：锚点取**整行**（或足够长的唯一子串），任一命中数 != 1 即拒绝并报错。
"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
LIST = os.path.join(BASE, "工程期望清单.md")
HAND = os.path.join(os.path.dirname(BASE), "环境交接说明.md")

OK, BAD = [], []


def sub(path, old, new, tag):
    t = io.open(path, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        BAD.append("{}（命中 {}）".format(tag, n))
        print("  [XX] {:<28} 命中 {} 次 —— 拒绝".format(tag, n))
        return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    OK.append(tag)
    print("  [OK] {:<28}".format(tag))


def insert_before_line(path, prefix, block, tag, keep=True):
    """在「以 prefix 开头」的整行**之前**插入 block（整行锚点，防插进行中间）"""
    t = io.open(path, encoding="utf-8").read()
    L = t.split("\n")
    cand = [i for i, s in enumerate(L) if s.startswith(prefix)]
    if len(cand) != 1:
        BAD.append("{}（行首命中 {}）".format(tag, len(cand)))
        print("  [XX] {:<28} 行首命中 {} 次 —— 拒绝".format(tag, len(cand)))
        return
    i = cand[0]
    L = L[:i] + [block, ""] + L[i:]
    io.open(path, "w", encoding="utf-8").write("\n".join(L))
    OK.append(tag)
    print("  [OK] {:<28}".format(tag))


print("=" * 88)
print("第 103 轮补丁")
print("=" * 88)

# ============ ① 中文稿：§5.8 两处就地更正 ============
print("\n[① 中文稿 §5.8 就地更正]")
sub(ZH,
    "光子色散 **ω=|k|**（ω/k=1.0000 验证）、横极化 2 个自由度",
    "光子色散 **ω=|k|（长波极限）**、横极化 2 个自由度"
    "（⚠️ **第 103 轮更正**：原写「ω/k=1.0000 验证」—— 该数出自脚本里 `omega = k` 的**直接赋值**，"
    "是恒等式；严格的、方向无关的界见 **§10.1b 第 103 轮块**）",
    "ZH-1 ω=1.0000 更正")

sub(ZH,
    "- **数值验证 C**：库仑相光子格点色散 ω(k)=2√(Σsin²(k/2))，长波 **ω/|k|=0.9999**（光速 c=1 ✓）；",
    "- **数值验证 C**：库仑相光子格点色散 ω(k)=2√(Σsin²(k/2))，长波 **ω/|k|=0.9999**（光速 c=1 ✓）"
    "（⚠️ **第 103 轮**：该 0.9999 = k=0.05 处 `2 sin(k/2)/k` 的**泰勒值** `1 − k²/24 = 0.9998958` 的四舍五入，"
    "**不构成对框架的验证**（推导链里框架元素 **0 个**）；已改为**方向无关的显式界**，见 **§10.1b 第 103 轮块**）；",
    "ZH-2 数值验证 C 加注")

# ============ ② 英文稿：对应两处 ============
print("\n[② 英文稿 §5.8 就地更正]")
sub(EN,
    "photon dispersion **ω=|k|** (ω/k=1.0000 verified), 2 transverse polarizations",
    "photon dispersion **ω=|k| (long-wavelength limit)**, 2 transverse polarizations"
    " (⚠️ **corrected in round 103**: the earlier `ω/k=1.0000 verified` came from a direct `omega = k` "
    "assignment in the script — an identity; the rigorous, direction-independent bound is given in the "
    "round-103 block of §10.1b)",
    "EN-1 ω=1.0000 更正")

sub(EN,
    "- **Numerical verification C**: Coulomb-phase photon lattice dispersion ω(k)=2√(Σsin²(k/2)), "
    "long-wavelength **ω/|k|=0.9999** (speed of light c=1 ✓);",
    "- **Numerical verification C**: Coulomb-phase photon lattice dispersion ω(k)=2√(Σsin²(k/2)), "
    "long-wavelength **ω/|k|=0.9999** (speed of light c=1 ✓)"
    " (⚠️ **round 103**: this 0.9999 is the rounded value of the Taylor expansion "
    "`2 sin(k/2)/k = 1 − k²/24 = 0.9998958` at k = 0.05; it does **not** verify the framework "
    "(zero framework-specific elements enter the derivation); replaced by a **direction-independent "
    "explicit bound**, see the round-103 block in §10.1b);",
    "EN-2 数值验证 C 加注")

# ============ ③ 中文稿：§10.1b 第 103 轮块 ============
BLOCK_ZH = "\n".join([
    "**【第 103 轮（甲-4）麦克斯韦谱：「数值验证 C」降级为恒等式，长波极限已严格化】**"
    "（脚本 `_maxwell_103.py`，**MW-1 … MW-10，25 项 0 失败**；底本 = 第 103 轮前备份）",
    "① ⚠️ **C-67：「数值验证 C」是两处独立的空转** —— `ω/k = 1.0000` 出自 `_u1_spin2.py` 的 `omega = k`"
    "（**变量直接赋值** ⟹ 即 `x/x = 1`，零内容）；`ω/|k| = 0.9999` 是 `_z2u1_spin2_4d.py` 中 k=0.05 行的"
    "**四舍五入**，其解析值 `2 sin(k/2)/k = 1 − k²/24 = 0.9998958` 是**长波泰勒展开**。"
    "⚠️ 该脚本还把「分量约定」与「沿方向约定」混用（严格应为 `sinc(k/(2√3)) = 1 − k²/72`）。"
    "**框架特有元素在推导链里出现 0 次**（只用离散 Laplace 算子的定义与 `sin x ≈ x`）。",
    "② ✅ **严格化（本轮的正面增量）**：三维立方格点（a=1）上 `0 ≤ 1 − ω(k)/|k| ≤ 1 − √(1 − k²/12) ≤ k²/12`"
    "（`0 < |k| ≤ √12`），**最坏方向为 [100] 型**（单一非零分量），该处界**紧**；"
    "证明用 `|sin y| ≤ |y|`、`sin y ≥ y − y³/6`（0 ≤ y ≤ π/2）、`Σk_i⁴ ≤ k⁴`（交叉项非负）与 `1 − √(1−ε) ≤ ε`；"
    "**2800 个随机点扫描验证，紧度 99.59%**。",
    "③ ⭐ **各向同性是「分层」的（立方群 `O_h`（48 元）表示论判定）**：**`Sym²(T₁)` 的不变子空间维数 = 1** "
    "⟹ 任何 `O_h` 不变的二次作用量必为 `M_ij = c·δ_ij` ⟹ **光速 c 自动各向同性 —— 这是定理，只需立方对称，"
    "不需要连续旋转**；而 **`Sym⁴(T₁)` 的不变子空间维数 = 2**（不变量 `(k²)²` 与 `Σk_i⁴`）"
    "⟹ **四阶修正必然各向异性**（实测 [100] 系数 **1/12** vs [111] 的 **1/36**，**差 3 倍**）"
    "⟹ **全谱各向同性只能靠连续极限**（世界级，本报告不声称）。",
    "④ ⚠️ **两处措辞更正**：(a) 「**ω=|k|**」在格点上**全谱不成立** —— `ω(π,π,π)/|k| = 2/π = 0.6366`"
    "（与 1 差 **36%**），且 `ω` 是 BZ **周期函数** ⟹ 只能是**长波极限**；"
    "(b) 格点上实际有 **3 支**（2 横 ＋ 1 纵），纵向模的消失同样依赖连续极限 —— "
    "**不得**写成「框架推出 2 个横向极化」。",
    "⟹ **判决**：§10.2#13 的「麦克斯韦谱严格验证」**结项** —— **可严格化的部分已严格化**"
    "（二阶各向同性定理 ＋ 方向无关误差界），**不可严格化的部分**（全谱／连续极限）**明确划界**；"
    "**框架对麦克斯韦谱的独有贡献 = 0**（唯一非平凡的一环是连续极限）。"
    "详见《甲4结项_麦克斯韦谱_恒等式验证与二阶各向同性定理》。",
])
print("\n[③ 中文稿 §10.1b 新块]")
insert_before_line(ZH, "**EMRI 系统误差上界**", BLOCK_ZH, "ZH-3 第103轮块")

# ============ ④ 英文稿：§10.1b 第 103 轮块 ============
BLOCK_EN = "\n".join([
    "**【Round 103 (item 甲-4) Maxwell spectrum: \"numerical verification C\" demoted to an identity, "
    "long-wavelength limit made rigorous】** (script `_maxwell_103.py`, **MW-1 … MW-10, 25 items 0 failures**; "
    "pre-patch baseline = the round-103 backup)",
    "① ⚠️ **C-67: \"numerical verification C\" consists of two independent idle loops** — `ω/k = 1.0000` comes "
    "from `omega = k` in `_u1_spin2.py` (**a direct variable assignment** ⟹ i.e. `x/x = 1`, zero content); "
    "`ω/|k| = 0.9999` is the **rounded** value of the k = 0.05 row of `_z2u1_spin2_4d.py`, whose analytic value "
    "`2 sin(k/2)/k = 1 − k²/24 = 0.9998958` is a **long-wavelength Taylor expansion**. "
    "⚠️ That script also mixes the \"component\" and \"along-direction\" conventions (strictly it should be "
    "`sinc(k/(2√3)) = 1 − k²/72`). **Zero framework-specific elements enter the derivation** "
    "(only the definition of the discrete Laplacian and `sin x ≈ x`).",
    "② ✅ **Rigorization (this round's positive increment)**: on a 3D cubic lattice (a = 1), "
    "`0 ≤ 1 − ω(k)/|k| ≤ 1 − √(1 − k²/12) ≤ k²/12` for `0 < |k| ≤ √12`, with the **worst direction being [100]-type** "
    "(a single non-zero component), where the bound is **tight**; the proof uses `|sin y| ≤ |y|`, "
    "`sin y ≥ y − y³/6` (0 ≤ y ≤ π/2), `Σk_i⁴ ≤ k⁴` (non-negative cross terms) and `1 − √(1−ε) ≤ ε`; "
    "**2800 random points scanned, tightness 99.59%**.",
    "③ ⭐ **Isotropy is layered (representation theory of the cubic group `O_h`, 48 elements)**: "
    "**the invariant subspace of `Sym²(T₁)` has dimension 1** ⟹ any `O_h`-invariant quadratic action must be "
    "`M_ij = c·δ_ij` ⟹ **the speed of light c is automatically isotropic — a theorem requiring only cubic "
    "symmetry, not continuous rotations**; whereas **the invariant subspace of `Sym⁴(T₁)` has dimension 2** "
    "(invariants `(k²)²` and `Σk_i⁴`) ⟹ **the fourth-order correction is necessarily anisotropic** "
    "(measured: coefficient **1/12** along [100] vs **1/36** along [111], a **factor of 3**) "
    "⟹ **full-spectrum isotropy can only come from the continuum limit** (world-class, not claimed here).",
    "④ ⚠️ **Two wording corrections**: (a) \"**ω=|k|**\" **fails on the full spectrum** on a lattice — "
    "`ω(π,π,π)/|k| = 2/π = 0.6366` (**36%** off), and `ω` is a BZ-**periodic** function ⟹ only the "
    "**long-wavelength limit** is meaningful; (b) the lattice actually has **3 branches** (2 transverse + 1 "
    "longitudinal), and the disappearance of the longitudinal mode likewise depends on the continuum limit — "
    "one **must not** write \"the framework predicts 2 transverse polarizations\".",
    "⟹ **Verdict**: the \"rigorous Maxwell-spectrum verification\" of §10.2#13 is **closed** — "
    "**what can be rigorized is rigorized** (second-order isotropy theorem + a direction-independent error "
    "bound), **what cannot is explicitly demarcated** (full spectrum / continuum limit); "
    "**the framework's own contribution to the Maxwell spectrum = 0** (the only non-trivial link is the "
    "continuum limit). See 《甲4结项_麦克斯韦谱_恒等式验证与二阶各向同性定理》.",
])
print("\n[④ 英文稿 §10.1b 新块]")
insert_before_line(EN, "**EMRI systematic-error upper bound**", BLOCK_EN, "EN-3 第103轮块")

# ============ ⑤ §10.2#13 的开放项收口 ============
print("\n[⑤ §10.2#13 开放项收口]")
sub(ZH,
    "见 §10.1b）、麦克斯韦谱严格验证。",
    "见 §10.1b）、**~~麦克斯韦谱严格验证~~ ✅ 第 103 轮结项**"
    "（「数值验证 C」降级为**恒等式**〔**C-67**〕：`omega = k` 的赋值 ＋ 长波泰勒展开；"
    "长波极限已**严格化**〔方向无关的显式界 ＋ **二阶各向同性定理**（仅需立方对称）〕，"
    "而四阶**必**各向异性〔`Sym⁴` 不变量维数 2〕、全谱各向同性须连续极限〔世界级〕；"
    "**框架独有贡献 = 0**）——见 §10.1b 第 103 轮块。",
    "ZH-4 §10.2#13 收口")

sub(EN,
    "see §10.1b), rigorous Maxwell-spectrum verification.",
    "see §10.1b), **~~rigorous Maxwell-spectrum verification~~ ✅ closed in round 103** "
    "(the \"numerical verification C\" is demoted to an **identity** 〔**C-67**〕: a `omega = k` assignment "
    "plus a long-wavelength Taylor expansion; the long-wavelength limit is made **rigorous** "
    "〔a direction-independent explicit bound + a **second-order isotropy theorem** (requiring only cubic "
    "symmetry)〕, while the fourth order is **necessarily** anisotropic 〔`Sym⁴` invariant dimension 2〕 and "
    "full-spectrum isotropy needs the continuum limit 〔world-class〕; **the framework's own contribution = 0**) "
    "— see the round-103 block in §10.1b.",
    "EN-4 §10.2#13 收口")

# ============ ⑥ 清单：第 103 轮行 ＋ C-67 ＋ 计数 ＋ 剩余待办 ============
print("\n[⑥ 工程期望清单]")
ROW103 = ("| **第 103 轮**（**甲-4 执行**） | **C-67 更正** ＋ **甲-4 结项：麦克斯韦谱严格化** | "
          "第 99 轮清点点选的「甲-4」= §10.2#13 的最后一项「**麦克斯韦谱严格验证**」。"
          "**结果**：① ⚠️ **C-67**：「数值验证 C」是**两处独立的空转** —— `ω/k=1.0000` 出自 "
          "`_u1_spin2.py` 的 `omega = k`（**直接赋值** ⟹ `x/x=1`）；`ω/|k|=0.9999` = k=0.05 行 "
          "`2 sin(k/2)/k = 1 − k²/24` 的四舍五入（**泰勒**）；**框架特有元素 0 个**。"
          "② ✅ **严格化**：`0 ≤ 1 − ω/|k| ≤ 1 − √(1 − k²/12) ≤ k²/12`（最坏方向 [100]，"
          "**2800 点验证、紧度 99.59%**）。③ ⭐ **各向同性分层**：立方群 `O_h` 的 `Sym²` 不变子空间维数 "
          "**= 1** ⟹ **光速各向同性是定理（只需立方对称）**；`Sym⁴` 维数 **= 2** ⟹ **四阶必各向异性** "
          "（[100] 1/12 vs [111] 1/36，**差 3 倍**）。④ 措辞更正：「ω=|k|」**全谱不成立**"
          "（`ω(π,π,π)/|k| = 2/π`，差 36%）。⟹ **§10.2#13「麦克斯韦谱严格验证」结项**；"
          "**框架独有贡献 = 0**。 |")
insert_before_line(LIST, "| **第 102 轮**（**甲-3 执行**） |", ROW103, "清单-第103轮行")

ROW_C67 = ("| **C-67** | ⭐⭐ **「数值验证」是恒等式（第 103 轮；甲-4）** | **更正 / 判定降级** | "
           "论文 §5.8 的「**数值验证 C**」有两处独立空转：① `ω/k = 1.0000`（v1.29 段，L1100）出自 "
           "`_u1_spin2.py` L70 的 `omega = k` —— **变量被直接赋值**，验证 `omega/k == 1` 即 `x/x = 1`；"
           "② `ω/|k| = 0.9999`（v1.30 段，L1121）是 `_z2u1_spin2_4d.py` 中 k=0.05 行的四舍五入，"
           "解析值 `2 sin(k/2)/k = 1 − k²/24 = 0.9998958` 是**长波泰勒展开**（且该脚本混用「分量/沿方向」"
           "两个约定）。**框架特有元素在推导链里出现 0 次** ⟹ 它**不验证框架的任何命题**。"
           "🔧 处置：中英就地加注 ＋ §10.2#13 收口（**降级为恒等式**），同时补上**真正严格**的部分"
           "（方向无关误差界 ＋ **二阶各向同性定理**，见 §10.1b 第 103 轮块）。 "
           "📌 **同族**：**C-4**（`E_c ≡ 1 meV` 恒等式）、**N-36**（`L²` 是 `h` 的定义式）、"
           "**N-32**（`D = ℏ/(3m)` 恒等式）—— 本项是第 **4** 次同族命中，且是**在「数值验证」的名义下**。 "
           "| 第 103 轮（`_maxwell_103.py` MW-1／MW-2／MW-10） | 同 `甲4结项_…md` |")
insert_before_line(LIST, "| **C-66** |", ROW_C67, "清单-C-67行")

sub(LIST, "| **撤回 / 更正** | **65 条**", "| **撤回 / 更正** | **66 条**", "清单-计数66")

sub(LIST,
    "**~~甲-3 相变点精确值~~ ✅ 第 102 轮结项（结论 = 数值不能判别；且「h_c = K/J」缺机制；C-64/65/66）**；",
    "**~~甲-3 相变点精确值~~ ✅ 第 102 轮结项（结论 = 数值不能判别；且「h_c = K/J」缺机制；C-64/65/66）**；"
    "**~~甲-4 麦克斯韦谱严格化~~ ✅ 第 103 轮结项**（结论 = 「数值验证」是**恒等式**〔C-67〕；"
    "长波已严格化 ＋ **二阶各向同性定理**；框架独有贡献 = 0）；",
    "清单-剩余待办")

sub(LIST,
    "⚠️ **有明确可判定入口的待办已清空**（只剩 EMRI，其三个前提在框架之外）。",
    "⚠️ **甲类只剩 甲-5**（N2 的 4π 相位锁定相容性方程，§10.2#7）；"
    "此外只剩 EMRI（等 LISA，三个前提在框架之外）与两类交付物（EMRI 材料包／私审准备包）。",
    "清单-甲类剩余")

print("\n" + "=" * 88)
print("OK {} 项，BAD {} 项".format(len(OK), len(BAD)))
if BAD:
    print("失败：" + " ｜ ".join(BAD))
print("=" * 88)
