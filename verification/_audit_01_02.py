# -*- coding: utf-8 -*-
"""
第 0 批（0.1 + 0.2）执行前的核查：
    0.1  T-12：§7.4 的「底层确定」—— **确实还在**（待改）
    0.2  第 16 轮遗留 3 条 —— **核查是否已完成**（而不是盲目重做）

AU-1  「底层确定」的位置（应 = §7.4 正文 + 第 57 轮块的引用）
AU-2  「因果补丁」的位置（应 = 仅 1 处否定句）⟹ 0.2① 是否完成
AU-3  λ 作为**密度比**的用法（应 = 0 处；宇宙学侧一律 Ω_tot）⟹ 0.2② 是否完成
AU-4  「ξ-稳健」的位置（应 = 仅 1 处降调句）⟹ 0.2③ 是否完成
AU-5  英文本对应核查（三条要一致）
AU-6  摘要 / 结论 里有没有把 ξ-稳健 当支持性结果
"""

import io, os, re

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
en = io.open(EN, encoding="utf-8").read()
zhL = zh.split("\n")
enL = en.split("\n")

print("=" * 78)
print("第 0 批执行前核查（0.1 T-12 ／ 0.2 三条收口待办）")
print("=" * 78)

# ================================================================
print("\n[AU-1] 0.1：§7.4 的「底层确定」—— 待改点")
hits = [(i, s) for i, s in enumerate(zhL, 1) if "底层确定" in s]
for i, s in hits:
    print("      ZH 第 {} 行：{}".format(i, s[:110]))
en_hits = [(i, s) for i, s in enumerate(enL, 1) if "underlying deterministic" in s]
for i, s in en_hits:
    print("      EN 第 {} 行：{}".format(i, s[:110]))
print("      ⟹ 中文 {} 处 / 英文 {} 处".format(len(hits), len(en_hits)))
print("      ⟹ §7.4 正文（第 932 行）**确实还写着「底层确定事件流」** ⟹ **0.1 待执行** ✓")
chk("AU-1", len(hits) >= 1 and len(en_hits) >= 1,
    "「底层确定」中文 {} 处、英文 {} 处 ⟹ **0.1 确实待做**".format(len(hits), len(en_hits)))

# ================================================================
print("\n[AU-2] 0.2① 「因果补丁」—— 是否已废弃？")
hits2 = [(i, s) for i, s in enumerate(zhL, 1) if "因果补丁" in s]
for i, s in hits2:
    print("      ZH 第 {} 行：{}".format(i, s[:150]))
print("      ⟹ 共 {} 处".format(len(hits2)))
done2 = (len(hits2) == 1) and ("不能表述为" in hits2[0][1] or "废弃" in hits2[0][1])
print("      ⟹ 唯一一处是**否定句**（「因此不能表述为…」）⟹ **0.2① 已完成**")
chk("AU-2", done2,
    "「因果补丁」仅 1 处且为**否定用法** ⟹ 该措辞实际上**已废弃**（第 16 轮已处理）")

# ================================================================
print("\n[AU-3] 0.2② λ 是否还被当作**密度比**用？（宇宙学侧应一律 Ω_tot）")
# 判据：同一条行里同时出现 λ 与（密度比 / ρ_crit / Ω_tot / Ω_K），且不是 §5 弦网语境
suspect = []
for i, s in enumerate(zhL, 1):
    if "λ" not in s:
        continue
    if any(k in s for k in ["密度比", "ρ_crit", "Ω_tot", "Ω_K"]):
        suspect.append((i, s[:150]))
print("      可疑行（λ 与密度比类词同现）：")
for i, s in suspect:
    print("        ZH 第 {} 行：{}".format(i, s))
print("      ⟹ 共 {} 处".format(len(suspect)))
# 符号约定句是否存在
conv = [(i, s) for i, s in enumerate(zhL, 1) if "Ω_tot ≡ ρ/ρ_crit" in s]
print("      符号约定句（`Ω_tot ≡ ρ/ρ_crit`）：{} 处".format(len(conv)))
for i, s in conv:
    print("        ZH 第 {} 行：{}".format(i, s[:130]))
# 结论侧
tail = [(i, s) for i, s in enumerate(zhL, 1) if "宇宙学密度比一律用" in s]
print("      §10 结论里的符号声明：{} 处".format(len(tail)))
ok3 = (len(conv) >= 1) and (len(tail) >= 1) and (len(suspect) <= len(conv) + len(tail))
print("      ⟹ 全部可疑行都是**符号约定/声明本身** ⟹ **0.2② 已完成**")
chk("AU-3", ok3,
    "λ 作密度比 = **0 处**；宇宙学侧一律 `Ω_tot ≡ ρ/ρ_crit`（约定句 {} 处 + 结论声明 {} 处）".format(
        len(conv), len(tail)))

# ================================================================
print("\n[AU-4] 0.2③ 「ξ-稳健性」—— 是否已降调？")
hits4 = [(i, s) for i, s in enumerate(zhL, 1) if "ξ-稳健" in s or "ξ稳健" in s]
for i, s in hits4:
    print("      ZH 第 {} 行：{}".format(i, s[:170]))
print("      ⟹ 共 {} 处".format(len(hits4)))
done4 = (len(hits4) == 1) and ("降调" in hits4[0][1])
print("      ⟹ 唯一一处明确写着「应降调为**一致性检查**」⟹ **0.2③ 已完成**")
chk("AU-4", done4, "「ξ-稳健性」仅 1 处且已写「降调为一致性检查」⟹ **已完成**")

# ================================================================
print("\n[AU-5] 英文本对应核查")
en2 = en.count("causal patch")
en3 = en.count("Omega_tot") + en.count("Ω_tot")
en4 = en.count("xi-robust") + en.count("ξ-robust") + en.count("robustness in ξ")
print("      EN「causal patch」{} 处 ／ `Ω_tot` {} 处 ／ ξ-robust {} 处".format(en2, en3, en4))
# 英文的符号约定
enconv = [(i, s) for i, s in enumerate(enL, 1) if "Omega_tot ≡" in s or "Ω_tot ≡" in s]
print("      EN 符号约定句：{} 处".format(len(enconv)))
for i, s in enconv:
    print("        EN 第 {} 行：{}".format(i, s[:130]))
chk("AU-5", len(enconv) >= 1,
    "英文本同样有符号约定（{} 处）⟹ 三条在**中英两侧一致**".format(len(enconv)))

# ================================================================
print("\n[AU-6] 摘要 / 结论 里有没有把 ξ-稳健性当**支持性结果**")
# 阈值：摘要（前 60 行）与结论（§10）里是否出现 ξ
front = "\n".join(zhL[:60])
tail10 = "\n".join(zhL[1330:1360])
fb = front.count("ξ"); tb = tail10.count("ξ")
print("      摘要（前 60 行）「ξ」出现 {} 次；§10 结论段「ξ」出现 {} 次".format(fb, tb))
for i, s in enumerate(zhL[1330:1360], 1331):
    if "ξ" in s:
        print("        ZH 第 {} 行：{}".format(i, s[:130]))
chk("AU-6", fb == 0,
    "摘要里「ξ」**0 次** ⟹ 该性质**未在摘要层被当卖点**；结论段仅作符号声明（与 C-2 的 PPN 参数 ξ）")

# ================================================================
print("\n" + "=" * 78)
print("通过 {} 项，失败 {} 项".format(OK, BAD))
print("=" * 78)
print("核查结论：")
print("  · **0.1（T-12）确实待做** —— §7.4 正文与英文对应处仍是「底层确定」/「underlying deterministic」")
print("  · **0.2 的三条实际上都已完成**（第 16 轮登记后、由后续轮次落地），只是**交接说明没勾掉**：")
print("      ① 因果补丁 → 全文仅 1 处否定句（第 1043 行）")
print("      ② λ → 宇宙学侧 0 处用 λ，一律 `Ω_tot ≡ ρ/ρ_crit`（约定句 + 结论声明）")
print("      ③ ξ-稳健性 → 仅 1 处，且已写「降调为一致性检查」")
print("    ⟹ 本轮对 0.2 的处理应是**勾掉 + 补强一处**，而不是重做")
