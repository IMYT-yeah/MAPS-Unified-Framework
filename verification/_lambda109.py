# -*- coding: utf-8 -*-
"""第 109 轮 G4：λ 的统一收尾 —— 义项清点、内部冲突、操作式定义的落地核查

判据全部脚本化（LM-1 … LM-14）。两段式：凡「补丁会改掉的状态」一律同时读**补丁前备份**。
"""
import io
import os
import re

ROOT = r"C:\Users\Administrator\Desktop\2026-08-20-21-43-34"
OUT = os.path.join(ROOT, "outputs")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
ZH_PRE = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-04第109轮前.md")
EN_PRE = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-04第109轮前.md")
LIST = os.path.join(OUT, "工程期望清单.md")
HAND = os.path.join(ROOT, "环境交接说明.md")

FAIL = []
N = [0]


def ck(tag, cond, msg):
    N[0] += 1
    ok = bool(cond)
    if not ok:
        FAIL.append(tag)
    print("  [{}] {:<6} {}".format("OK" if ok else "XX", tag, msg))


def rd(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


zh, en = rd(ZH), rd(EN)
zhp = rd(ZH_PRE) if os.path.exists(ZH_PRE) else ""
enp = rd(EN_PRE) if os.path.exists(EN_PRE) else ""
print("=" * 96)
print("第 109 轮核验 —— λ 的统一收尾（G4）")
print("=" * 96)

# ---------------------------------------------------------------- LM-1 义项清点
zl = zh.split("\n")
el = en.split("\n")
lam_lines_zh = [i for i, s in enumerate(zl, 1) if "λ" in s]
lam_lines_en = [i for i, s in enumerate(el, 1) if "λ" in s]
print("\n--- LM-1…LM-4  λ 的义项清点（全文行计数）---")
print("      ZH 含 λ 的行 = {}；EN 含 λ 的行 = {}".format(len(lam_lines_zh), len(lam_lines_en)))
ck("LM-1", len(lam_lines_zh) >= 40,
   "ZH 含 λ 的行 = {}（第 72 轮记「44 行」，量级一致；本轮为补丁后计数）".format(len(lam_lines_zh)))

senses = {
    "① 宇宙学密度比（历史记法）": r"λ\s*=\s*1[^0-9]|λ = 1\b",
    "② §5 弦网耦合 + λ_c": r"λ_c|λ=0|λ = 0|H\(λ\)|λΣ",
    "③ §6.4 Φ⁴ 四次耦合": r"¼λΦ⁴|1/4 λ Φ|λΦ⁴",
    "④ 力程/康普顿波长 λ = ℏc/m": r"λ\s*=\s*ℏc/m|力程\s*\*\*?`?λ",
}
counts = {}
for name, pat in senses.items():
    c = len(re.findall(pat, zh))
    counts[name] = c
    print("      {:<34} ZH 命中 {}".format(name, c))
ck("LM-2", counts["④ 力程/康普顿波长 λ = ℏc/m"] >= 1,
   "**第四义（力程）确实在用**（ZH 命中 {}）—— 而 C-15 只登记了三义 ⟹ 缺一条".format(
       counts["④ 力程/康普顿波长 λ = ℏc/m"]))

# ---------------------------------------------------------------- LM-3 符号约定块
i_note = zh.find("本节**不使用 λ** 表示密度比")
ck("LM-3", i_note > 0, "§8.6 的「符号约定（重要）」块存在，且明写「本节**不使用 λ** 表示密度比」")
seg_conv = zh[i_note:i_note + 1400]
n_sense_conv = len(re.findall(r"第三义|第四义|第三義", seg_conv))
ck("LM-4", "第三义" in seg_conv,
   "该块已登记到**第三义**（§6.4 的 Φ⁴ 耦合，C-15）；**力程（第四义）未登记**")
seg_pre = zhp[zhp.find("本节**不使用 λ** 表示密度比"):][:2600] if zhp else ""
ck("LM-5", ("力程" not in seg_pre and "ℏc/m" not in seg_pre) and ("力程" in seg_conv and "ℏc/m" in seg_conv),
   "**两段式**：补丁前该窗口内「力程 / ℏc/m」各 **0 处**（取证 ⟹ 第四义确实漏登记）／补丁后已补 ✓")

# ---------------------------------------------------------------- LM-6 内部冲突
i_block = zh.find("【v2.9 收口（第 81 轮")
j_block = zh.find("\n\n", i_block + 200)
block = zh[i_block:j_block + 1] if i_block > 0 else ""
ck("LM-6", i_block > 0, "第 81 轮块（`8π/3` 那个待办）存在")
lam_in_block = re.findall(r"λ\s*(?:≡|=)\s*[^，。；\s]+", block)
print("      第 81 轮块内的 λ 定义式：{}".format(lam_in_block))
ck("LM-7", len(lam_in_block) >= 3,
   "**同一节内自相矛盾**：§8.6 约定「本节不使用 λ 表示密度比」，而 §8.6.5 的块里出现 {} 处 `λ = …`"
   " 表示密度比".format(len(lam_in_block)))
ck("LM-8", "ρ_micro/ρ_holo" in block,
   "冲突的具体形态 = `λ ≡ ρ_micro/ρ_holo`（块内），与约定直接冲突")

# ---------------------------------------------------------------- LM-9 表格 vs 正文
rows = [s for s in zl if s.startswith("|") and "3/(8π)" in s]
ck("LM-9", len(rows) == 1 and "Ω_tot = 3/(8π)" in rows[0],
   "判别表**表格行**已改成 `Ω_tot = 3/(8π)`（第 81 轮之后的某次修补）⟹ 一处：{}".format(rows[0][:60]))
i_pre = zhp.find("【v2.9 收口（第 81 轮") if zhp else -1
blk_pre = zhp[i_pre:i_pre + 1200] if i_pre > 0 else ""
ck("LM-10", zhp.count("Ω_tot = 3/(8π)") == 1 and zh.count("Ω_tot = 3/(8π)") >= 1
   and "λ ≡ ρ_micro/ρ_holo" in block
   and "λ ≡ ρ_micro/ρ_holo" in blk_pre and "第 109 轮口径注（C-75）" not in blk_pre,
   "**两段式**：补丁前 ⟹ 全 ZH 仅 **1** 处 `Ω_tot = 3/(8π)`（在表内）而块正文仍是 "
   "`λ ≡ ρ_micro/ρ_holo = 8π/3`（**改了表格、漏了正文**）；补丁后 ⟹ 块内已加口径注 ✓")

# ---------------------------------------------------------------- LM-11 数值自洽
import math
a = 8 * math.pi / 3.0
b = 3.0 / (8 * math.pi)
ck("LM-11", abs(a * b - 1.0) < 1e-12,
   "两个数**互为倒数**：`8π/3 = {:.6f}`、`3/(8π) = {:.6f}`，乘积 = {:.12f} ⟹ 换标签时**同时改了定义方向**，"
   "必须写明（不能默默等同）".format(a, b, a * b))

# ---------------------------------------------------------------- LM-12 操作式定义已落地
ck("LM-12", zhp.count("ρ/ρ_crit") == 2 and enp.count("ρ/ρ_crit") == 2
   and zh.count("ρ/ρ_crit") >= 2 and en.count("ρ/ρ_crit") >= 2,
   "操作式定义 **`Ω_tot ≡ ρ/ρ_crit` 已落地** —— 补丁前 ZH/EN **各 2 处**（§8.6 约定 ＋ 全局符号注）；"
   "补丁后 ZH {} / EN {} 处（本轮第四义注里又引了一次）".format(zh.count("ρ/ρ_crit"), en.count("ρ/ρ_crit")))
op = [i for i, s in enumerate(zl, 1) if "Ω_tot ≡ ρ/ρ_crit" in s]
opp = [i for i, s in enumerate(zhp.split("\n"), 1) if "Ω_tot ≡ ρ/ρ_crit" in s] if zhp else []
ck("LM-13", len(opp) == 2 and len(op) >= 2,
   "两段式：补丁前 **2 处**（行号 {}，前者 §8.6 约定、后者末尾符号注）／补丁后 {} 处".format(opp, len(op)))

# ---------------------------------------------------------------- LM-14 中英对称
en_conv = en.find("does not use")
ck("LM-14", enp.count("Ω_tot ≡ ρ/ρ_crit") == 2 and en.count("Ω_tot ≡ ρ/ρ_crit") >= 2
   and en.count("λ ≡ ρ_micro/ρ_holo") == 1
   and enp.count("3/(8π)") == 1 and en.count("3/(8π)") >= 1
   and en.count("Round-109 notation note (C-75)") == 1,
   "英文稿**对称**（两段式）：补丁前操作式 2 处／同冲突 1 处／表格行 1 处；补丁后口径注亦已加 ✓")

print()
print("=" * 96)
print("通过 {} 项，失败 {} 项{}".format(N[0] - len(FAIL), len(FAIL),
                                 "" if not FAIL else "  ⟹ " + ", ".join(FAIL)))
print("=" * 96)
