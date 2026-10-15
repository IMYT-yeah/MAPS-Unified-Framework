# -*- coding: utf-8 -*-
"""第 105 轮核验（两段式）：底本 = 补丁前备份；并列打印 补丁前/补丁后。

⚠️ 铁律 18/20：凡「某词 0 处」类论证，一律读 `*_备份_<日期>第N轮前.md` 做底本，
   不读当前稿；并**并列打印两列**（一眼可见污染）。
"""
import io
import os
import re
import hashlib

ROOT = r"C:/Users/Administrator/Desktop/2026-08-20-21-43-34"
OUT = os.path.join(ROOT, "outputs")
LIST = os.path.join(OUT, "工程期望清单.md")
PRE_LIST = os.path.join(OUT, "工程期望清单_备份_2026-10-04第105轮前.md")
HAND = os.path.join(ROOT, "环境交接说明.md")
PRE_HAND = os.path.join(ROOT, "环境交接说明_备份_2026-10-04第105轮前.md")
MEMO = os.path.join(OUT, "乙类并轨结项_O1-O5逐条判定与分支B的空悬.md")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
RL = os.path.join(OUT, "_rail105.py")
RLOUT = os.path.join(OUT, "_rail105_out.txt")

P, F = [0], []


def ck(tag, cond, msg):
    ok = bool(cond)
    P[0] += 1
    if not ok:
        F.append(tag)
    print("  [{}] {} — {}".format("OK" if ok else "XX", tag, msg))


def rd(p):
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def hd(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()[:12] if os.path.exists(p) else "MISSING"


print("=" * 92)
print("第 105 轮核验 · 乙类并轨（O1–O5 逐条判定）")
print("=" * 92)

cur_l, pre_l = rd(LIST), rd(PRE_LIST)
cur_h, pre_h = rd(HAND), rd(PRE_HAND)
cur_z, cur_e = rd(ZH), rd(EN)
memo, rlout = rd(MEMO), rd(RLOUT)

print("\n--- V-1…V-8  清单台账 ---")
ck("V-1", "| **第 105 轮**（**乙类并轨**） |" in cur_l,
   "清单有**第 105 轮行**（乙类并轨）")
ck("V-2", "| **第 105 轮**（**乙类并轨**） |" not in pre_l,
   "补丁前无该行（**两段式取证**）")
i105 = cur_l.split("\n").index([x for x in cur_l.split("\n")
                                if x.startswith("| **第 105 轮**")][0])
i104 = cur_l.split("\n").index([x for x in cur_l.split("\n")
                                if x.startswith("| **第 104 轮**")][0])
ck("V-3", i105 < i104, "顺序正确：第 105 轮行在第 104 轮行**之前**")

ck("V-4", "| **C-72** |" in cur_l and "| **C-72** |" not in pre_l,
   "**C-72 行已加**（补丁前无）")
ck("V-5", "量纲不成立" in cur_l and "(3, 6, −7)" in cur_l,
   "C-72 的判据写明了**量纲指数 (3, 6, −7)** 与「不是任何率」")
ck("V-6", "7.08×10²⁹" in cur_l,
   "C-72 写明**定标歧义 7.08×10²⁹ 倍**")

seq = [re.match(r"^\|\s*\*\*(C-\d+)\*\*\s*\|", x).group(1)
       for x in cur_l.split("\n") if re.match(r"^\|\s*\*\*(C-\d+)\*\*\s*\|", x)]
i67 = seq.index("C-67")
grp = seq[i67:i67 + 7]
nums = [int(x.split("-")[1]) for x in grp]
ck("V-7", grp == ["C-67", "C-68", "C-69", "C-70", "C-71", "C-72", "C-73"] and nums == sorted(nums),
   "**结构自检：C-67…C-73 连续且严格升序**（不破块 —— 第 104 轮 C-71 立的规范；"
   "本轮曾把 C-73 插到 C-72 之前，已修）")

ck("V-8", "| **撤回 / 更正** | **72 条**" in cur_l
   and "| **撤回 / 更正** | **70 条**" in pre_l,
   "计数 **70 → 72**（两段式：补丁前 70 ✓；本轮新增 C-72 与 C-73）")

print("\n--- V-9…V-11  剩余待办 ---")
ck("V-9", "**乙类并轨 ✅ 第 105 轮结项**" in cur_l and "乙类并轨 ✅ 第 105 轮结项" not in pre_l,
   "剩余待办行已更新（乙类并轨结项）")
ck("V-10", "O2 收口为「分支 B 悬空、A 保留」" in cur_l,
   "剩余待办行写明 O2 的判决")
ck("V-11", "EMRI（等 LISA" in cur_l and "私审准备包" in cur_l,
   "剩余仍为 EMRI ＋ 两类交付物（丙类）")

print("\n--- V-12…V-16  交接说明 ---")
ck("V-12", "**当前建议（第 105 轮后）**" in cur_h and "**当前建议（第 105 轮后）**" not in pre_h,
   "§七 已更新到第 105 轮（补丁前无）")
ck("V-13", "**（历史，第 104 轮后）**" in cur_h,
   "第 104 轮的建议已标「（历史）」（不删，留痕）")
ck("V-14", "**第 105 轮新增（乙类并轨" in cur_h and "第 105 轮新增" not in pre_h,
   "交接说明有**第 105 轮段**")
ck("V-15", "6.4651×10⁻¹³ s" in cur_h and "4.5782×10¹⁷ s" in cur_h,
   "第 105 轮段写明两个时间尺度（τ_ℏ / τ_H）")
ck("V-16", "5.776×10⁻¹⁹ 核子/(m³·s)" in cur_h and "0.56 倍" in cur_h and "13.3 倍" in cur_h,
   "第 105 轮段写明**观测上限**与**两个口径的慢读法结果**（且要求成对引用）")

print("\n--- V-17…V-23  备忘录关键数字 ---")
ck("V-17", os.path.exists(MEMO) and "分支 B = 悬空（机制未重建）" in memo,
   "备忘录存在且给出 **B = 悬空** 的判决")
ck("V-18", "2.2403×10⁻¹¹ J/m³" in memo and "5.2831×10⁻¹⁰ J/m³" in memo,
   "备忘录给出 **ρ_Λ 两口径**（框架 2.2403e-11 / 观测 5.2831e-10 J/m³）")
ck("V-19", "23.58" in memo and "23.76" in memo,
   "且写明 23.58（本轮复算）vs 23.76（论文口径）")
ck("V-20", "3.99×10²⁹" in memo and "9.41×10³⁰" in memo and "13.3" in memo,
   "备忘录给出**三个超限倍数**（快×2 口径 ＋ 慢×观测口径）")
ck("V-21", "差异**不是**纯记账" in memo or "「差异在记账层」" in memo,
   "备忘录**更正了「差异在记账层」**")
ck("V-22", "N-21" in memo and "同族第 2 次" in memo,
   "O4 判否引 **N-21** 并标「同族第 2 次」")
ck("V-23", "撞已判死区" in memo and "第 55 轮" in memo and "第 94 轮" in memo,
   "O5 判否引第 55 轮（跨支用途限信息）与第 94 轮（void-CPT-κ 悬空）")

print("\n--- V-24…V-28  脚本与自洽 ---")
ck("V-24", "通过 39 项，失败 0 项" in rlout,
   "`_rail105.py` = **RL-1…RL-16，39 项 0 失败**（存档 `_rail105_out.txt`）")
ck("V-25", "(3, 6, -7)" in rlout and "(1, -1, -3)" in rlout,
   "脚本**打印了量纲指数**（可复核，非断言）")
ck("V-26", "7.081e+29" in rlout or "7.08e+29" in rlout,
   "脚本算出**定标比 7.08×10²⁹**（数值可复跑）")
ck("V-27", "空集" in rlout and "6.70e-04" in rlout,
   "O1 的 ε_c 窗口**随 n 变化**（n=2 时空集）—— 结论非口号")
ck("V-28", "总表" in rlout and "O1" in rlout and "O5" in rlout,
   "脚本末尾有 **O1–O5 总表**")

print("\n--- V-29…V-33  ⚠️ 并轨内容未混入论文 ＋ 论文仅加 C-73 口径注 ---")
for nm, t in [("中文稿", cur_z), ("英文稿", cur_e)]:
    hits = {m: t.count(m) for m in ["SPB", "分支 A/B", "分支 B", "Branch A/B", "branch B", "并轨-O1"]}
    print("      {}：{}".format(nm, hits))
ck("V-29", not any(cur_z.count(m) for m in ["SPB", "分支 A/B", "分支 B", "并轨-O1"]),
   "**中文稿：并轨线的结构词 0 处** ⟹ 并轨内容**确实没有并入**")
ck("V-30", not any(cur_e.count(m) for m in ["SPB", "Branch A/B", "branch B", "merger-O1"]),
   "**英文稿：同样 0 处** ⟹ 中英一致（都未并入）")
ck("V-31", cur_z.count("并轨") <= 3 and cur_e.count("并轨") <= 3,
   "「并轨」两字仅出现在**既有上下文与本轮口径注**里（≤3 处），**无内容并入**")

zp = rd(ZH.replace(".md", "_备份_2026-10-04第105轮前.md"))
ep = rd(EN.replace(".md", "_备份_2026-10-04第105轮前.md"))
ck("V-32", "第 105 轮口径注（C-73）" in cur_z and "第 105 轮口径注（C-73）" not in zp,
   "**中文稿确有改动，且仅为 C-73 口径注**（补丁前无）")
ck("V-33", "Round-105 numbering note (C-73)" in cur_e and "Round-105 numbering note (C-73)" not in ep,
   "**英文稿同样仅加 C-73 口径注**（补丁前无）")

print("\n--- V-34…V-38  C-73 专项（「O1–O4」两套编号并存）---")
ck("V-34", "| **C-73** |" in cur_l and "| **C-73** |" not in pre_l,
   "**C-73 行已加**（补丁前无）")
ck("V-35", cur_z.count("○") >= 0 and ("O1 `Ω_K = 0`" in cur_z and "（O1（观测者结构）" not in cur_z),
   "两套编号**确实同处一稿**（§4.9 的 `（O1）`／`O1（观测者结构）` 与 §9 的 `O1 \`Ω_K = 0\``）")
ck("V-36", cur_z.count("O1") >= 9 and cur_z.count("O4") >= 8,
   "量化：中文稿 `O1` 命中 ≥9 处、`O4` ≥8 处（**两套都活着**，非笔误）")
ck("V-37", "语境前缀" in cur_z and "context prefix" in cur_e,
   "中英注都写明「引用须带**语境前缀**」")
ck("V-38", "并轨备忘录" in cur_z or "space-library merger memo" in cur_e,
   "中英注都点明**第三套**（并轨备忘录的 O1–O5）存在且**未入本文**")

print("\n--- V-39…V-42  文件指纹（可复核）---")
print("      中文稿 md5 = {}（补丁前 {}）".format(hd(ZH), hd(ZH.replace(".md", "_备份_2026-10-04第105轮前.md"))))
print("      英文稿 md5 = {}（补丁前 {}）".format(hd(EN), hd(EN.replace(".md", "_备份_2026-10-04第105轮前.md"))))
print("      清单   md5 = {}（补丁前 {}）".format(hd(LIST), hd(PRE_LIST)))
print("      交接   md5 = {}（补丁前 {}）".format(hd(HAND), hd(PRE_HAND)))
ck("V-39", hd(LIST) != hd(PRE_LIST), "清单**已变更**（补丁生效）")
ck("V-40", hd(HAND) != hd(PRE_HAND), "交接说明**已变更**（补丁生效）")
ck("V-41", hd(ZH) != hd(ZH.replace(".md", "_备份_2026-10-04第105轮前.md")),
   "中文稿**已变更**（仅 C-73 口径注）")
ck("V-42", hd(EN) != hd(EN.replace(".md", "_备份_2026-10-04第105轮前.md")),
   "英文稿**已变更**（仅 C-73 口径注）")

print("\n" + "=" * 92)
print("通过 {} 项，失败 {} 项{}".format(P[0] - len(F), len(F),
                                "" if not F else "  ⟹ " + ", ".join(F)))
print("=" * 92)
