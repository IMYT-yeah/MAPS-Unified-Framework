# -*- coding: utf-8 -*-
"""第 109 轮补丁（G4：λ 的统一收尾）

四处改动（中英同步）：
  ① §8.6 符号约定块 —— 补**第四义（力程 λ = ℏc/m）** ＋ 语境前缀规范；
  ② §8.6.5 第 81 轮块 —— 加**口径注**（历史记法 λ 与当代记号的对应 ＋ 倒数关系），**不删历史**；
  ③ 清单 —— 第 109 轮行 ＋ C-75 ＋ 计数 73→74 ＋ 剩余待办；
  ④ 交接说明 —— §七 建议 ＋ 第 109 轮段。
锚点一律取**整行**（陷阱 74），`sub_once` 命中数 ≠ 1 即拒绝并计 BAD。
"""
import io
import os

BASE = r"C:\Users\Administrator\Desktop\2026-08-20-21-43-34"
OUT = os.path.join(BASE, "outputs")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
LIST = os.path.join(OUT, "工程期望清单.md")
HAND = os.path.join(BASE, "环境交接说明.md")

OK, BAD = [], []


def sub_once(path, old, new, tag):
    t = io.open(path, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        BAD.append((tag, n))
        print("  [XX] {:<30} 命中 {} 次 —— 拒绝".format(tag, n))
        return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    OK.append(tag)
    print("  [OK] {:<30} 已改".format(tag))


# ================================================================ ① 符号约定：第四义
Z_CONV = ("> ⚠️ **第 72 轮补注（C-15）**：`λ` 还有**第三义** —— §6.4 的 Φ⁴ 四次耦合 "
          "`V(Φ) = −½μ²Φ² + ¼λΦ⁴`（本约定此前**未提**）；另有 **`g` 同字母两义**"
          "（§6.1 的钉扎耦合 `gΦψ̄ψ` vs §5.7 的弦网几何因子 `J = n_G·E_P·g`），**此前无任何约定**。")
Z_CONV_NEW = Z_CONV + "\n" + (
    "> ⚠️ **第 109 轮补注（C-75）**：`λ` 还有**第四义** —— **力程 / 康普顿波长** `λ = ℏc/m`\n"
    "> （§6 第五力段：`m = 0.41 J ⟹ λ = 0.81 l_P`；同族处另有外部锚点 `λ = 0.194 mm` / `48 μm`）。\n"
    "> 该义与 §5 的弦网耦合**同字母、无任何关系**，此前**未登记**。\n"
    "> ⟹ **本文 `λ` 共四义**：① 宇宙学密度比（**历史记法**，现统一用 `Ω_tot ≡ ρ/ρ_crit`）｜"
    "② §5 弦网耦合常数（含 `λ_c`）｜③ §6.4 的 Φ⁴ 四次耦合｜④ **力程**（§6 第五力段）。\n"
    "> **规范：引用 `λ` 一律带语境前缀**（「密度比 λ」／「弦网 λ」／「Φ⁴ λ」／「力程 λ」）。")

E_CONV = ("> ⚠️ **Round-72 addendum (C-15)**: `λ` carries a **third meaning** — the Φ⁴ quartic coupling "
          "of §6.4, `V(Φ) = −½μ²Φ² + ¼λΦ⁴` (**not mentioned** in this convention before); and "
          "**`g` carries two meanings under one letter** (§6.1's pinning coupling `gΦψ̄ψ` vs "
          "§5.7's string-net geometric factor `J = n_G·E_P·g`), previously **undeclared**. ")
E_CONV_NEW = E_CONV + "\n" + (
    "> ⚠️ **Round-109 addendum (C-75)**: `λ` carries a **fourth meaning** — the **force range / Compton wavelength** "
    "`λ = ℏc/m`\n"
    "> (§6 fifth-force passage: `m = 0.41 J ⟹ λ = 0.81 l_P`; sibling external anchors `λ = 0.194 mm` / `48 μm`).\n"
    "> It shares the letter with §5's string-net coupling and is **unrelated** to it; **previously unregistered**.\n"
    "> ⟹ **`λ` has four meanings in this paper**: ① cosmological density ratio (**historical notation**; now standardised "
    "as `Ω_tot ≡ ρ/ρ_crit`) | ② §5 string-net coupling (including `λ_c`) | ③ §6.4's Φ⁴ quartic coupling | "
    "④ **force range** (§6 fifth-force passage).\n"
    "> **Rule: always attach a context prefix when citing `λ`** (\"density-ratio λ\" / \"string-net λ\" / \"Φ⁴ λ\" / \"range λ\").")

# ================================================================ ② 第 81 轮块：口径注
Z_OPEN = ("> **【v2.9 收口（第 81 轮：`8π/3` 这个待办**没有对象**）】** 交接清单的老编号里有「**消掉 `8π/3`**」"
          "（第 17 轮登记）。本轮把它算清（脚本 `_h1h4_81.py`，**H1-1 … H4-3，9 项 0 失败**）。")
Z_NOTE = (
    "> ⚠️ **【第 109 轮口径注（C-75）】**：本块（第 81 轮）的 `λ` 是**历史记法** —— 它指 `ρ_micro/ρ_holo`，\n"
    "> **与本节开头约定的 `λ`（= §5 弦网耦合）不是一回事**（该约定已明写「本节**不使用 λ** 表示密度比」）。\n"
    "> 对应的**当代记号**见 §8.6.5 判别表末列 **`Ω_tot = 3/(8π) = 0.119366`**。\n"
    "> ⚠️ 二者**互为倒数**（`8π/3 × 3/(8π) = 1`；数值 `8.37758041 × 0.11936621 = 1.00000000`）⟹ "
    "**换标签时定义方向也变了**：\n"
    "> 引用必须写清是 `ρ_micro/ρ_holo`（= `8π/3`）还是 `ρ_holo/ρ_micro`（= `3/(8π)`）。\n"
    "> 本块内的「`λ = 1`」（② 全息路）与「`λ = 8/3`」（① 投影面积路）同理，均按此读。")

E_OPEN = ("> **【v2.9 close-out (round 81: the `8π/3` task has **no object**)】** The handover list kept an old item "
          "\"**eliminate `8π/3`**\" (registered in round 17). This round settles it (script `_h1h4_81.py`, "
          "**H1-1 … H4-3, 9 checks, 0 failures**).")
E_NOTE = (
    "> ⚠️ **【Round-109 notation note (C-75)】** This block (round 81) uses `λ` as **historical notation** — it means "
    "`ρ_micro/ρ_holo`,\n"
    "> and is **not** the `λ` declared at the head of this section (= §5's string-net coupling; that convention "
    "already states \"this section **does not use λ** for a density ratio\").\n"
    "> The **current notation** is the last column of the §8.6.5 discrimination table: "
    "**`Ω_tot = 3/(8π) = 0.119366`**.\n"
    "> ⚠️ The two are **reciprocals** (`8π/3 × 3/(8π) = 1`; numerically `8.37758041 × 0.11936621 = 1.00000000`) ⟹ "
    "**relabelling also flips the direction of the definition**:\n"
    "> a citation must say whether it is `ρ_micro/ρ_holo` (= `8π/3`) or `ρ_holo/ρ_micro` (= `3/(8π)`).\n"
    "> The block's \"`λ = 1`\" (route ②, holographic) and \"`λ = 8/3`\" (route ①, projected area) read the same way.")

print("=== ① 符号约定块：补第四义 ===")
sub_once(ZH, Z_CONV, Z_CONV_NEW, "ZH-符号约定-第四义")
sub_once(EN, E_CONV, E_CONV_NEW, "EN-符号约定-第四义")

print("=== ② 第 81 轮块：加口径注 ===")
sub_once(ZH, Z_OPEN + "\n>\n", Z_OPEN + "\n>\n" + Z_NOTE + "\n>\n", "ZH-第81轮块-口径注")
sub_once(EN, E_OPEN + "\n>\n", E_OPEN + "\n>\n" + E_NOTE + "\n>\n", "EN-第81轮块-口径注")

# ================================================================ ③ 清单
ROW_109 = ("| **第 109 轮**（**G4 执行**） | **C-75 更正 ＋ G4 结项：`λ` 的统一收尾** | "
           "第 108 轮清点点出的「真缺口 G4」= 交接说明挂了很久的「**λ 统一用操作式 `λ ≡ ρ/ρ_crit`（面敏感）**」。"
           "⭐ **取证结论**：该待办**已基本落地**（`λ_micro` 全文 **0 处**；操作式 **`Ω_tot ≡ ρ/ρ_crit` ZH/EN 各 2 处**），"
           "但留下两处缺口 —— ① **§8.6 内部自相矛盾**：约定明写「本节**不使用 λ** 表示密度比」，"
           "而 §8.6.5 的**第 81 轮块正文**仍写 `λ ≡ ρ_micro/ρ_holo = 8π/3`（同轮修补只改了**判别表表格行**"
           "→ `Ω_tot = 3/(8π)`，**漏了正文**）⟹ **陷阱 70（改表格漏正文）的新形态**；"
           "② **`λ` 的第四义（力程 `λ = ℏc/m`）从未登记**（C-15 只记三义）。"
           "🔧 处置：中英各加 **1 处符号约定（第四义 ＋ 语境前缀规范）** ＋ **1 处块内口径注**（含**倒数关系**："
           "`8π/3 × 3/(8π) = 1`，换标签时定义方向也变）。⚠️ **历史留痕**：块内原 `λ` 写法**不删**，只加注。 "
           "| 第 109 轮（`_lambda109.py` LM-1…LM-14，**14 项 0 失败**） | 同 `λ统一收尾_四义清点与同轮块内表格正文分叉.md` |\n")

ROW_C75 = ("| **C-75** | ⭐⭐ **`λ` 的两处口径缺口（第 109 轮；G4）** | **更正 / 口径** | "
           "① **同轮块内「表格改了、正文没改」**：第 81 轮的修补把 §8.6.5 **判别表的表格行**改成 "
           "`Ω_tot = 3/(8π)`，而**同一轮块的正文**仍写 `λ ≡ ρ_micro/ρ_holo = 8π/3` ⟹ 与本节开头的符号约定"
           "（「本节不使用 λ 表示密度比」）**直接冲突**（两者相距约 100 行，**同一 §8.6 内**）。"
           "② **`λ` 的第四义未登记**：**力程 / 康普顿波长** `λ = ℏc/m`（§6 第五力段 `λ = 0.81 l_P`；"
           "外部锚点 `0.194 mm` / `48 μm`）—— **C-15 只记三义**（密度比／弦网耦合／Φ⁴），且符号约定块内 "
           "「力程 / ℏc/m」**各 0 处**。⚠️ 附带：两值**互为倒数**（`8π/3 = 8.37758041`、`3/(8π) = 0.11936621`，"
           "乘积 = 1.000000000000）⟹ **换标签时定义方向也翻转**，引用须写清分子分母。 "
           "📌 **同族**：**C-26**（漏改派生量）／**C-27**（改了工具没改产物）／**C-35**（未同步）—— 这是「**更正作用域没扫全**」的**第 4 次**。 "
           "| 第 109 轮（`_lambda109.py` LM-7…LM-11） | 同 `λ统一收尾_…md` |\n")


def insert_before(path, anchor_prefix, block, tag):
    t = io.open(path, encoding="utf-8").read()
    lines = t.split("\n")
    idx = [i for i, s in enumerate(lines) if s.startswith(anchor_prefix)]
    if len(idx) != 1:
        BAD.append((tag, len(idx)))
        print("  [XX] {:<30} 锚点命中 {} 次 —— 拒绝".format(tag, len(idx)))
        return
    lines.insert(idx[0], block.rstrip("\n"))
    io.open(path, "w", encoding="utf-8").write("\n".join(lines))
    OK.append(tag)
    print("  [OK] {:<30} 已插入".format(tag))


print("=== ③ 清单 ===")
insert_before(LIST, "| **第 104 轮**（**甲-5 执行**） |", ROW_109, "清单-第109轮行")
insert_before(LIST, "| **C-74** | ⭐⭐ **EMRI 的 `σ_δ` 与 `ΔlnL`", ROW_C75, "清单-C-75行")

sub_once(LIST,
         "| **撤回 / 更正** | **73 条**（**C-74（第 106 轮，丙类）**：EMRI 的 σ_δ 与 ΔlnL **变化率**也不自洽（差 4.41 倍）",
         "| **撤回 / 更正** | **74 条**（**C-75（第 109 轮，G4）**：`λ` 的两处口径缺口 —— 同轮块内「表格改了、正文没改」"
         "（`λ ≡ ρ_micro/ρ_holo = 8π/3` 与「本节不使用 λ 表示密度比」冲突）＋ `λ` 的**第四义（力程 `λ = ℏc/m`）未登记**；"
         "两值互为倒数 ⟹ 换标签定义方向也翻转｜**C-74（第 106 轮，丙类）**：EMRI 的 σ_δ 与 ΔlnL **变化率**也不自洽（差 4.41 倍）",
         "清单-计数 73→74")

sub_once(LIST, "；**丙类 ✅ 第 106 轮结项**", "；**丙类 ✅ 第 106 轮结项**；**G4 ✅ 第 109 轮结项**（`λ` 统一收尾 —— 四义清点 ＋ 块内口径注；**C-75**）",
         "清单-剩余待办")

# ================================================================ ④ 交接说明
H_ADV = "0. 🎯 **当前建议（第 106 轮后）**："
H_ADV_NEW = ("0. 🎯 **当前建议（第 109 轮后）**：**G4（`λ` 的统一收尾）已结项** —— 该待办**已基本落地**"
             "（`λ_micro` 全文 **0 处**；操作式 **`Ω_tot ≡ ρ/ρ_crit` ZH/EN 各 2 处**），本轮收尾两处缺口："
             "① ⚠️ **§8.6 内部自相矛盾**（约定「本节不使用 λ 表示密度比」vs 第 81 轮块正文 `λ ≡ ρ_micro/ρ_holo = 8π/3`）"
             "—— 同轮修补**只改了判别表表格行**、**漏了正文**；② ⚠️ **`λ` 的第四义（力程 `λ = ℏc/m`）从未登记**。"
             "🔧 已中英各加 1 处符号约定（第四义 ＋ **语境前缀规范**）＋ 1 处块内口径注（含**倒数关系**）。"
             "📌 **剩余 = 第 108 轮清点出的另三条真缺口**：**A23**（普朗克常数的物理身份，从未推进）／"
             "**D4**（EMRI `κ↔Γ` 的 1/3 映射，10% 缺口）／**G9**（底层四状态机制＋`11.0904` 自然性，交接说明标「⚠️ 仍未解决」）。"
             "📌 其余对外两条通道不变：**送私审**（等人）／**等 LISA**（~10–15 年）。\n"
             "\n"
             "0. 🎯 **（历史，第 106 轮后）**：")

H_SEC_NEW = ("**第 109 轮新增（G4：`λ` 的统一收尾）**：脚本 `_lambda109.py`（**LM-1 … LM-14，14 项 0 失败**）。\n"
             "① ⭐ **待办已基本落地**：`λ_micro` **0 处**（第 81 轮后的某次修补）；**`Ω_tot ≡ ρ/ρ_crit` 中英各 2 处**"
             "（§8.6 约定 ＋ 末尾符号注）⟹ 「λ 统一为操作式」**实质完成**。\n"
             "② ⚠️ **缺口 A（同轮块内表格/正文分叉）**：§8.6.5 的**判别表行**已改 `Ω_tot = 3/(8π)`（全文仅 1 处），"
             "而**同轮块正文**仍 `λ ≡ ρ_micro/ρ_holo = 8π/3` ⟹ 与本节约定（「不使用 λ 表示密度比」）冲突。"
             "**陷阱 70 的新形态**（改表格漏正文）；与 **C-26**（漏改派生量）／**C-27**（改工具没改产物）／**C-35**（未同步）同族 ⟹ **第 4 次**。\n"
             "③ ⚠️ **缺口 B（`λ` 第四义未登记）**：**力程 / 康普顿波长** `λ = ℏc/m`（§6 第五力段 `λ = 0.81 l_P`；"
             "外部锚点 `0.194 mm` / `48 μm`）—— 而 **C-15 只记三义**，符号约定块内「力程 / ℏc/m」**各 0 处**。\n"
             "④ ✅ **数值自洽**：`8π/3 = 8.37758041` 与 `3/(8π) = 0.11936621` **互为倒数**（乘积 = 1.000000000000）"
             "⟹ **换标签时定义方向也翻转**，引用须写清分子分母（这条是本轮新登记的判据）。\n"
             "⑤ 🔧 **处置**：中英各加 1 处符号约定（第四义 ＋ **语境前缀规范**：「密度比 λ」／「弦网 λ」／「Φ⁴ λ」／「力程 λ」）"
             "＋ 1 处块内口径注；⚠️ **历史留痕** —— 块内原 `λ` 写法**不删**，只加注（承 C-73 范式）。\n"
             "⑥ 📌 **`λ` 义项计数（脚本实测）**：ZH 含 λ 的行 **58 行**（第 72 轮记 44 行、更早记 26 行，均过期）；"
             "四义命中：密度比 3｜弦网耦合 74｜Φ⁴ 1｜力程 3。\n"
             "\n"
             "**第 107 轮新增（元任务 · 考古：数据可追溯性盘点）**：")

print("=== ④ 交接说明 ===")
sub_once(HAND, H_ADV, H_ADV_NEW, "交接-§七建议")
sub_once(HAND, "**第 107 轮新增（元任务 · 考古：数据可追溯性盘点）**：", H_SEC_NEW, "交接-第109轮段")

print()
print("=" * 92)
print("OK = {} 项；BAD = {}".format(len(OK), BAD if BAD else "无"))
print("=" * 92)
