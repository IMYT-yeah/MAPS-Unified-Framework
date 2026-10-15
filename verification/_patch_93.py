# -*- coding: utf-8 -*-
"""第 93 轮 补丁：候选池 #5 结项 —— C-48 / C-49 / C-50 ＋ N-38 ＋ I-22

改动面：论文 ZH/EN（§4.5b ＋ §8.6.7(e)）、工程期望清单、（光速 memo / B3 memo）、环境交接说明。
所有锚点均为整行 / 单次命中（预检已过）。
"""
import io

ZH = "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
LIST = "工程期望清单.md"
LS = "光速的意义_落差分解与超光速的结构性.md"
B3 = "B3_高阶PPN与指数度规.md"
HH = "../环境交接说明.md"

FAIL = 0


def sub_once(path, old, new, tag):
    global FAIL
    t = io.open(path, encoding="utf-8").read()
    if t.count(old) != 1:
        print("  [FAIL] {}  命中 {} 次".format(tag, t.count(old)))
        FAIL += 1
        return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    print("  [PASS] {}  已替换".format(tag))


def ins_after_line(path, sub, block, tag):
    global FAIL
    lines = io.open(path, encoding="utf-8").read().split("\n")
    idx = [i for i, s in enumerate(lines) if sub in s]
    if len(idx) != 1:
        print("  [FAIL] {}  锚命中 {} 次".format(tag, len(idx)))
        FAIL += 1
        return
    lines[idx[0] + 1:idx[0] + 1] = block.split("\n")
    io.open(path, "w", encoding="utf-8").write("\n".join(lines))
    print("  [PASS] {}  已插入（锚行 {}）".format(tag, idx[0] + 1))


def ins_before_line(path, sub, block, tag):
    global FAIL
    lines = io.open(path, encoding="utf-8").read().split("\n")
    idx = [i for i, s in enumerate(lines) if sub in s]
    if len(idx) != 1:
        print("  [FAIL] {}  锚命中 {} 次".format(tag, len(idx)))
        FAIL += 1
        return
    lines[idx[0]:idx[0]] = block.split("\n")
    io.open(path, "w", encoding="utf-8").write("\n".join(lines))
    print("  [PASS] {}  已插入（锚行 {}）".format(tag, idx[0] + 1))


# ---------------------------------------------------------------- 1. 论文 ZH §4.5b（C-48 口径注）
print("=== 1. 论文 §4.5b：加口径注（C-48，中英同步）===")
ZH_NOTE_A = """> ⚠️ **【第 93 轮口径注（C-48）：本表适用域 = 静态扇区】** `ξ, α₁, α₂, α₃, ζ₁–ζ₄` 属**优越系 / 运动型参数**（其效应以「相对优越系的运动」或「特殊位置」为因子出现），而**静态各向同性 ansatz 对它们是盲区** —— 既不能给出 0、也不能给出非 0。表中「0」的身份是**框架的要求值**：由 **C-2**（普朗克尺度的绝对性不得泄漏到 1PN，§8.6.7(e)）承担，**截至第 93 轮尚未演示**。
> ⟹ **引用本表必须同时引 C-2**；不得单引「其余全 0」作已得结果。（消歧：本处「C-2」= 第 18 轮**承诺序列**，非清单台账的「更正 C-2」；详见 §8.6.7(e) 第 93 轮注 C-50。）"""
ins_after_line(ZH, "| 框架值 | **1** | **1** | **0（自动 GR 值）** |", "\n" + ZH_NOTE_A, "ZH-1")

EN_NOTE_A = """> ⚠️ **【Round-93 scope note (C-48): this table covers the static sector only】** `ξ, α₁, α₂, α₃, ζ₁–ζ₄` are **preferred-frame / motion-type parameters** (their effects enter with a factor of the motion relative to the preferred frame, or of special location), and a **static isotropic ansatz is blind to them** — it can neither give 0 nor a non-zero value. The "0" in the table is a **required value of the framework**, carried by **C-2** (Planck-scale absoluteness must not leak into 1PN; §8.6.7(e)); **as of round 93 it has not been demonstrated**.
> ⟹ **Any citation of this table must also cite C-2**; do not quote "all others 0" as an established result. (Disambiguation: "C-2" here = the round-18 **commitment series**, not the checklist's correction "C-2"; see the round-93 note in §8.6.7(e), C-50.)"""
ins_after_line(EN, "| Framework value | **1** | **1** | **0 (automatic GR values)** |", "\n" + EN_NOTE_A, "EN-1")

# ---------------------------------------------------------------- 2. 论文 ZH §8.6.7(e)（N-38 + C-50 消歧）
print("=== 2. 论文 §8.6.7(e)：加注（N-38 机制未演示 ＋ C-50 消歧，中英同步）===")
ZH_NOTE_B = """

> ⚠️ **【第 93 轮注（N-38）：该「必须负责」尚未演示】** 「A1 的 50:50 ＋ 各向同性」是**关于涨落统计的对称性**；而 α / ξ 参数描述的是**对优越系运动的敏感性** —— **各向同性 ≠ boost 不变**（完全各向同性的介质仍定义优越系：声学介质即反例；tick 的等时面法矢 `n^μ` 在结构上与 aether 的 `u^μ` 同类，isotropic aether 照样可以给 `α₁ ≠ 0`）。全项目检索：**无任何「泄漏量」的计算**（「演示 / 已证」与「绝对性」同行 **0 处**；登记处只有「必须负责」「被派定」「派了个新活」式**指派**）。⟹ **C-2 升级为「未演示的必要条件」**；登记 **I-22（tick 片层的 1PN 消隐）**。⚠️ C-2 也是 **EMRI 判决干净解读的前置条件之一**。
> 📌 **消歧（C-50）**：本处「C-2」= **第 18 轮承诺序列**（C-1 满占位 f=1／C-2 绝对性不泄漏／C-3 质量=反转概率）；**不是**清单台账的「更正 C-2」（第 50 轮 H/N 口径更正），也**不是**第 74 轮待办分组的 `C5 = PPN 优越系`。**引用「C-n」必须写明序列。**"""
sub_once(ZH, "并行使 C-2 从「可选」升为「必需」。", "并行使 C-2 从「可选」升为「必需」。" + ZH_NOTE_B, "ZH-2")

EN_NOTE_B = """

> ⚠️ **【Round-93 note (N-38): the "must be responsible" has not been demonstrated】** "A1's 50:50 + isotropy" is a symmetry of the **fluctuation statistics**, whereas the α/ξ parameters describe **sensitivity to motion relative to a preferred frame** — **isotropy ≠ boost invariance** (a fully isotropic medium still defines a preferred frame: acoustic media are the counterexample; the tick's constant-time-surface normal `n^μ` is structurally the same kind of object as the aether `u^μ`, and an isotropic aether can still give `α₁ ≠ 0`). Project-wide search: **no calculation of any "leakage" exists** (the words "demonstrated / proved" never co-occur with "absoluteness"; the registrations are only **assignments**). ⟹ **C-2 is upgraded to an undemonstrated necessary condition**; **I-22** registered. ⚠️ C-2 is also **one of the preconditions for a clean EMRI verdict**.
> 📌 **Disambiguation (C-50)**: "C-2" here = the **round-18 commitment series** (C-1 occupancy f=1 / C-2 no leakage / C-3 mass = reversal probability); **not** the checklist's correction "C-2" (round-50 H/N convention), and **not** the round-74 backlog group's `C5 = PPN preferred frame`. **Any citation of "C-n" must state its series.**"""
sub_once(EN, "Parallel updating promotes C-2 from optional to required.", "Parallel updating promotes C-2 from optional to required." + EN_NOTE_B, "EN-2")

# ---------------------------------------------------------------- 3. 清单
print("=== 3. 清单：候选池 #5 结项 ＋ 五条新行 ＋ 三处计数 ===")
lines = io.open(LIST, encoding="utf-8").read().split("\n")
idx = [i for i, s in enumerate(lines) if s.startswith("5. **PPN / 优越系**")]
if len(idx) != 1:
    print("  [FAIL] LIST-0  池条目锚命中 {} 次".format(len(idx)))
    FAIL += 1
else:
    orig = lines[idx[0]]
    orig2 = orig[3:] if orig.startswith("5. ") else orig
    new_pool = ("5. ✅ **已结项（第 93 轮）** —— ① **判别通道 = 0**（论文自认「1PN 与 GR 完全不可区分」，与 **N-22** 同族）；"
                "② **约束通道 = C-2 未演示**（「A1 会抹掉绝对性」不成立为已有论证，**N-38**；登记 **I-22**）。"
                "顺带 **C-48 / C-49 / C-50**。观测限已核（联网）：α₁ ≤ 10⁻⁴（LLR）／4×10⁻⁵（PSR J1738+0333）、α₂ ≤ 2×10⁻⁹、α₃ ≤ 4×10⁻²⁰、ξ ≤ 4×10⁻⁹。\n"
                "   ❌ ~~原条目~~：" + orig2)
    lines[idx[0]:idx[0] + 1] = new_pool.split("\n")
    io.open(LIST, "w", encoding="utf-8").write("\n".join(lines))
    print("  [PASS] LIST-0  候选池 #5 已结项（行 {}）".format(idx[0] + 1))

sub_once(LIST, "／#5 PPN 优越系／", "／~~#5 PPN 优越系~~（✅ 第 93 轮结项）／", "LIST-2 剩余待办（line 187）")
sub_once(LIST, "C5 PPN 优越系／", "C5 ✅ PPN 优越系（第 93 轮结项）／", "LIST-3 待办台账（line 303）")
sub_once(LIST, "第 47/48/49 轮的全部 GAP 结果。",
         "第 47/48/49 轮的全部 GAP 结果。⚠️（第 93 轮 **C-50**：本行与**第 18 轮承诺序列**的「C-2」**非同一编号**；引用须写明序列。）",
         "LIST-4 C-2 行加消歧注")

ROWS = """| **C-48** | **§4.5b「完整 PPN 参数集……其余全 0」缺范围限定（第 93 轮；候选池 #5）** | **更正 / 口径** | 「0（自动 GR 值）」的依据是**静态 ansatz**（B3：度规静态、各向同性、纯对角、无 g₀ᵢ／无速度依赖），而 `ξ, α₁, α₂, α₃, ζ` 系是**运动 / 优越系型参数** ⟹ **静态 ansatz 对它们是盲区**（既不能给 0、也不能给非 0）。「0」的正确身份 = **框架要求值**，由 **C-2** 承担（**未演示**，见 N-38）。⟹ 已在 §4.5b 表后加口径注（中英同步）；引用须同时引 C-2。 | 第 93 轮（`_ppn_93.py` PF-1…PF-10） | —— |
| **C-49** | **第 18 轮「待核」观测限表：α₃ 记错 ＋ 两项须更新（第 93 轮）** | **更正 / 外文核** | 光速 memo §B 表：`α₃ = 10⁻⁸` **系误记**（10⁻⁸ 是 `ζ₃` 的量级；实为 **≤ 4×10⁻²⁰**，差 12 个数量级）；`α₂` 10⁻⁷ → **≤ 2×10⁻⁹**、`ξ` 10⁻³ → **≤ 4×10⁻⁹**（均毫秒脉冲星）。`α₁ ≤ 10⁻⁴`（LLR）与池条目一致 ✓，另有更紧的 **4×10⁻⁵**（PSR J1738+0333）。来源：Will 2006/2014 汇编（转引核）。 | 第 93 轮（联网核对） | —— |
| **C-50** | **「C」编号三套并行（撞车第 7 次）** | **更正 / 符号** | ① **第 18 轮承诺序列** `C-1/C-2/C-3`（满占位 / 绝对性不泄漏 / 质量=反转概率；光速 memo、tick memo、论文 §8.6.7(e)）；② **清单台账「更正」序列** `C-1…C-50`（本表；其中 **C-2 = 第 50 轮 H/N 口径更正**）；③ **第 74 轮待办分组** `C1–C8`（C5 = PPN 优越系）。⟹ §8.6.7(e) 已加消歧注（中英）；**规范：引用「C-n」必须写明序列**。 | 第 93 轮 | —— |
| **N-38** | **把「A1（50:50 ＋ 各向同性）会抹掉衬底绝对性 ⟹ PPN 优越系参数 = 0」当作已成立的机制 / 保证** | **负面** | **排除**。① 各向同性是**方向型**对称，α 参数是**对优越系运动的敏感性** —— **各向同性介质仍定义优越系**（声学反例；tick 等时面法矢 `n^μ` ~ aether `u^μ`）⟹ 方向对称**不蕴含**无优越系动力学；② 全项目检索：**无任何「泄漏量」计算**（「演示/已证」与「绝对性」同行 **0 处**；只有「必须负责」「被派定」「派了个新活」式**指派**）。⟹ **C-2 升级为「未演示的必要条件」**；登记 **I-22**。 | 第 93 轮（`_ppn_93.py` PF-4） | 同 C-48 备忘录 |
| **I-22** | **tick 片层的 1PN 消隐（「优越系消隐」机制）** | **难题（第 93 轮登记）** | 要把 **C-2** 从「要求」变「结论」，需给出：**全局同时 tick 的片层（等时面法矢 `n^μ` = 单位类时矢量场）与物质 / 引力自由度在 1PN 阶的耦合系数** —— 证明其为零（消隐机制），或算出量级与 `α₁ ≤ 10⁻⁴ / α₂ ≤ 2×10⁻⁹ / ξ ≤ 4×10⁻⁹` 对照。框架现状：**该系数连对象都没有**（引力侧无含时 / 速度依赖量）。⚠️ 属「引力侧低能洛伦兹恢复」的具体切片。 | 第 93 轮 | `_ppn_93.py`（PF-1…PF-10） |"""
ins_after_line(LIST, "| **C-47** | **第 55 轮块主题错位", ROWS, "LIST-5 C-48/C-49/C-50/N-38/I-22 五条新行")

sub_once(LIST, "| **未解科学难题** | **14 条**（⚠️ **I-21",
         "| **未解科学难题** | **15 条**（**I-22 tick 片层的 1PN 消隐**（第 93 轮登记）｜⚠️ **I-21",
         "LIST-6 难题 14 → 15")
sub_once(LIST, "| **负面判定** | **37 条**（**N-33",
         "| **负面判定** | **38 条**（**N-38 把「A1（50:50＋各向同性）会抹掉衬底绝对性」当作已成立机制**（第 93 轮：**各向同性 ≠ boost 不变** —— 各向同性介质仍定义优越系；全项目**无「泄漏量」计算** ⟹ **C-2 升级为「未演示的必要条件」**；登记 **I-22**）｜**N-33",
         "LIST-7 负面 37 → 38")
sub_once(LIST, "| **撤回 / 更正** | **46 条**（**C-47 ⭐",
         "| **撤回 / 更正** | **49 条**（**C-48 / C-49 / C-50 ⭐（第 93 轮，候选池 #5 结项）**：**C-48** §4.5b「其余全 0」缺范围限定（静态 ansatz 对优越系参数是**盲区**；「0」依赖 **C-2**，未演示）｜**C-49** 光速 memo 观测限表 **α₃ 记错**（10⁻⁸ → **4×10⁻²⁰**；10⁻⁸ 是 ζ₃ 的量级）＋ α₂/ξ 更新｜**C-50** 「**C**」编号**三套并行**（撞车第 **7** 次）｜**C-47 ⭐",
         "LIST-8 更正 46 → 49")

# ---------------------------------------------------------------- 4. 光速 memo
print("=== 4. 光速 memo：观测限核对注（C-49）＋ 三行就地更新 ===")
sub_once(LS, "文献量级（Will 综述，**待核**）：",
         "文献量级（Will 综述，~~待核~~ **已核（第 93 轮，见下方核对注）**）：", "LS-1 待核 → 已核")
sub_once(LS, "| α₂ | 10⁻⁷ | 0 | 同上 |", "| α₂ | ~~10⁻⁷~~ **2×10⁻⁹** | 0 | 同上 |", "LS-2 α₂ 行")
sub_once(LS, "| α₃ | 10⁻⁸ | 0 | 同上 |", "| α₃ | ~~10⁻⁸~~ **4×10⁻²⁰** | 0 | 同上 |", "LS-3 α₃ 行")
sub_once(LS, "| ξ | 10⁻³ | 0 | 同上 |", "| ξ | ~~10⁻³~~ **4×10⁻⁹** | 0 | 同上 |", "LS-4 ξ 行")

LS_NOTE = """
**⭐【第 93 轮核对注（C-49 ＋ N-38）：本表已核；α₃ 系误记】** 第 93 轮以 Will 2006/2014 汇编（＋ Stairs 2003 Living Review 表 1）核对：

| 参数 | 第 18 轮记 | **第 93 轮核对值** |
|---|---|---|
| α₁ | 10⁻⁴ | **≤ 10⁻⁴（LLR）／4×10⁻⁵（PSR J1738+0333）** ✓ |
| α₂ | 10⁻⁷ | **≤ 2×10⁻⁹**（毫秒脉冲星；早期表 4×10⁻⁷） |
| α₃ | ~~10⁻⁸~~ | **≤ 4×10⁻²⁰**（脉冲星自旋减慢统计）⚠️ **10⁻⁸ 是 `ζ₃` 的量级，原表张冠李戴** |
| ξ | 10⁻³ | **≤ 4×10⁻⁹**（毫秒脉冲星；10⁻³ 系早期引力仪数据） |

⚠️ **逻辑更正（N-38）**：上文选项 (i) 的「宏观上被 A1 的 50:50 + 各向同性抹平 ⟹ = 0 ✓」**不成立** —— 各向同性是**方向型**对称，α 参数是**对优越系运动的敏感性**；**各向同性介质仍定义优越系**（声学反例；`n^μ` ~ aether `u^μ`）。**C-2 是未演示的必要条件**（无对象、无计算）。详见《PPN优越系结项_静态扇区盲区与未演示的C-2.md》。"""
ins_after_line(LS, "普朗克尺度的绝对性是衬底属性，A1 的 50:50 + 各向同性保证其在 1PN 上无残留。", LS_NOTE, "LS-5 核对注")

# ---------------------------------------------------------------- 5. B3 memo
print("=== 5. B3 memo：加注（C-48）===")
B3_NOTE = """
> ⚠️ **【第 93 轮注（C-48）】** 上句「补全其余参数全部 = 0 的**论证**」名不符实：依据是**静态 ansatz 本身**（「无 g₀ᵢ、无速度/自旋依赖」），而 `ξ, α₁, α₂, α₃, ζ` 系的定义域是**运动 / 优越系** —— **静态 ansatz 对它们是盲区**，既不能给 0、也不能给非 0。「= 0」是**框架的要求**（由 **C-2** 承担，§8.6.7(e)），**不是本批所得**；引用时须同时引 C-2。详见第 93 轮备忘录《PPN优越系结项》。"""
ins_after_line(B3, "本批补全其余参数全部 = 0 的论证（静态各向同性纯对角结构", B3_NOTE, "B3-1")

# ---------------------------------------------------------------- 6. 交接说明
print("=== 6. 交接说明：§七 新建议 ＋ 第 93 轮新增块 ===")
sub_once(HH, "0. 🎯 **当前建议（第 90 轮后）**：", "0. 🎯 **（历史，第 90 轮后，已被上式取代）**：", "HH-1 降级旧建议")

HH_ITEM = """0. 🎯 **当前建议（第 93 轮后）**：**候选池 #5（PPN 优越系）已结项** —— 两条出口都给了答案：
   **判别通道 = 0**（1PN 与 GR 同值，**N-22** 同族）；**约束通道 = C-2 未演示**（「A1 会抹掉绝对性」不成立为已有论证，**N-38**；登记 **I-22**）。
   ⭐ **净增量**：**C-48 / C-49 / C-50** ＋ **N-38** ＋ **I-22** ＋ 观测限**联网核对**（α₃ 由 10⁻⁸ 更正为 **4×10⁻²⁰**）。
   📌 **剩余待办**：候选池 **#1 η 能标／#2 暗能量能标／#4 η/s（已判不独有）／#7 void-CPT-κ／#8 EMRI**；**A1（Lean 资产恢复）**。
   ⚠️ **#1/#2 是「配出来的数」（低优先）；#7 / #8 / A1 见各自条目**。
"""
ins_before_line(HH, "0. 🎯 **（历史，第 90 轮后，已被上式取代）**", HH_ITEM, "HH-2 新建议")

HH_BLOCK93 = """**第 93 轮新增（候选池 #5 结项：PPN 优越系 —— 静态扇区盲区 ＋ C-2 未演示）**：脚本 `_ppn_93.py`（**PF-1…PF-10，23 项 0 失败**）。
① ✅ **两条出口都给了答案**：**判别通道 = 0**（论文自认「1PN 与 GR 完全不可区分」，与 **N-22** 同族）；**约束通道 = C-2 未演示**。
② ⚠️ **C-48**：§4.5b「完整 PPN 参数集……其余全 0」缺范围限定 —— `ξ, α₁, α₂, α₃, ζ` 系是**运动 / 优越系型参数**，**静态 ansatz 对它们是盲区**（「自动 GR 值」把「不出现」误报为「= 0」）；「0」= 依赖 **C-2** 的**要求值** ⟹ 已在 §4.5b 加口径注（中英）。
③ ⚠️ **C-49**：光速 memo「待核」表**已核** —— **α₃ 系误记**（10⁻⁸ → **4×10⁻²⁰**；10⁻⁸ 是 `ζ₃` 的量级）；α₂ → **2×10⁻⁹**、ξ → **4×10⁻⁹**；α₁ ≤ 10⁻⁴（LLR）／更紧 4×10⁻⁵（PSR J1738+0333）。
④ ⚠️ **C-50**：「**C**」编号**三套并行**（第 18 轮承诺 `C-1/2/3` ｜ 本台账更正 `C-xx` ｜ 第 74 轮分组 `C1–C8`）——**撞车第 7 次**；§8.6.7(e) 已加消歧注；规范：**引用「C-n」必须写明序列**。
⑤ ⚠️ **N-38**：「A1（50:50＋各向同性）会抹掉衬底绝对性」**不成立为已有机制** —— **各向同性 ≠ boost 不变**（各向同性介质仍定义优越系；`n^μ` ~ aether `u^μ`）；全项目**无「泄漏量」计算** ⟹ **C-2 升级为「未演示的必要条件」**；登记 **I-22**。
⑥ 📌 **规范（第 93 轮起）**：**凡「已由对称性关闭」式断言，必须区分「方向型对称」与「运动型不变」**；**引用「C-n」必须写明序列**。
"""
ins_before_line(HH, "0. 🎯 **（历史，第 86 轮，已被上式取代）**：**审计轮三连", HH_BLOCK93, "HH-3 第 93 轮新增块")

print()
print("=" * 60)
print("PATCH 93 DONE  FAIL = {}".format(FAIL))
print("=" * 60)
