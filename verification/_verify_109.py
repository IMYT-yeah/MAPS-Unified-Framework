# -*- coding: utf-8 -*-
"""第 109 轮补丁核验（V-1 … V-16）—— 修复型检查项一律两段式（读补丁前备份）"""
import io
import os
import re

BASE = r"[WORKSPACE]"
OUT = os.path.join(BASE, "outputs")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
ZH_PRE = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-04第109轮前.md")
EN_PRE = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-04第109轮前.md")
LIST = os.path.join(OUT, "项目台账.md")
LIST_PRE = os.path.join(OUT, "项目台账_备份_2026-10-04第109轮前.md")
HAND = os.path.join(BASE, "环境说明.md")
HAND_PRE = os.path.join(BASE, "环境说明_备份_2026-10-04第109轮前.md")
MEMO = os.path.join(OUT, "λ统一收尾_四义清点与同轮块内表格正文分叉.md")
SCRIPT = os.path.join(OUT, "_lambda109.py")

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


z, e = rd(ZH), rd(EN)
zp, ep = rd(ZH_PRE), rd(EN_PRE)
l, lp = rd(LIST), rd(LIST_PRE)
h, hp = rd(HAND), rd(HAND_PRE)

print("=" * 96)
print("第 109 轮补丁核验（两段式）")
print("=" * 96)

print("\n--- V-1…V-3  台账结构 ---")
seq = [m.group(1) for m in re.finditer(r"^\|\s*\*\*(C-\d+)\*\*\s*\|", l, re.M)]
i = seq.index("C-67")
grp = seq[i:i + 9]
nums = [int(x.split("-")[1]) for x in grp]
ck("V-1", grp == ["C-%d" % k for k in range(67, 76)] and nums == sorted(nums),
   "**C-67…C-75 连续且严格升序**（本轮新条目插在**本轮上一条之后** —— 第 104 轮 C-71 立的规范）：{}".format(grp))
ck("V-2", "| **撤回 / 更正** | **74 条**" in l and "| **撤回 / 更正** | **73 条**" in lp,
   "计数 **73 → 74**（两段式：补丁前 73 ✓）")
ck("V-3", l.count("| **第 109 轮**") == 1 and lp.count("| **第 109 轮**") == 0,
   "清单**第 109 轮行**已加（补丁前 0 处）")

print("\n--- V-4…V-6  论文：两处插入（中英）---")
ck("V-4", z.count("第 109 轮补注（C-75）") == 1 and zp.count("第 109 轮补注（C-75）") == 0,
   "ZH §8.6 符号约定：**第四义补注**已加（补丁前 0 处）")
ck("V-5", e.count("Round-109 addendum (C-75)") == 1 and ep.count("Round-109 addendum (C-75)") == 0,
   "EN 对应补注已加（补丁前 0 处）")
ck("V-6", z.count("第 109 轮口径注（C-75）") == 1 and e.count("Round-109 notation note (C-75)") == 1
   and zp.count("第 109 轮口径注（C-75）") == 0,
   "第 81 轮块的**口径注**中英各 1 处（补丁前 0 处）")

print("\n--- V-7…V-9  口徑注的位置与历史留痕 ---")
lz = z.split("\n")
i_note = [k for k, s in enumerate(lz) if "第 109 轮口径注（C-75）" in s]
i_def = [k for k, s in enumerate(lz) if "λ ≡ ρ_micro/ρ_holo" in s]
ck("V-7", len(i_note) == 1 and len(i_def) == 1 and i_note[0] < i_def[0],
   "**口径注在复现行之前**（口径注 L{} < `λ ≡ ρ_micro/ρ_holo` L{}）⟹ 读者先看到限定".format(
       i_note[0] + 1, i_def[0] + 1))
ck("V-8", z.count("λ ≡ ρ_micro/ρ_holo") == 1 and zp.count("λ ≡ ρ_micro/ρ_holo") == 1,
   "**历史留痕**：块内原 `λ ≡ ρ_micro/ρ_holo` **未被删改**（补丁前后各 1 处）")
ck("V-9", "8π/3 × 3/(8π) = 1" in z and "8π/3 × 3/(8π) = 1" in e,
   "**倒数关系**已写入口径注（中英）—— 这是本轮新判据")

print("\n--- V-10…V-12  第四义与义项数 ---")
seg = z[z.find("本节**不使用 λ** 表示密度比"):][:2600]
ck("V-10", "力程" in seg and "ℏc/m" in seg,
   "符号约定块内**首次出现**「力程 / ℏc/m」（补丁前该窗口内各 0 处）")
segp = zp[zp.find("本节**不使用 λ** 表示密度比"):][:2600]
ck("V-11", "力程" not in segp and "ℏc/m" not in segp,
   "两段式取证：补丁前该窗口内「力程 / ℏc/m」**各 0 处** ✓")
ck("V-12", "第四义" in seg and "共四义" in seg and "fourth meaning" in e,
   "已明写「`λ` **共四义**」（中）／「four meanings」（英）＋ **语境前缀规范**")

print("\n--- V-13…V-16  下游与自洽 ---")
ck("V-13", "当前建议（第 109 轮后）" in h and "（历史，第 106 轮后）" in h
   and "当前建议（第 109 轮后）" not in hp,
   "交接说明 §七：**新建议在前、旧的标（历史）**（两段式 ✓）")
ck("V-14", "第 109 轮新增（G4：`λ` 的统一收尾）" in h and "第 109 轮新增" not in hp,
   "交接说明已加**第 109 轮段**")
ck("V-15", os.path.exists(MEMO) and all(k in rd(MEMO) for k in
                                        ["8.37758041", "0.11936621", "1.000000000000", "C-75"]),
   "备忘录存在，且含关键数（8π/3、3/(8π)、乘积 = 1、C-75）")
ck("V-16", os.path.exists(SCRIPT) and "LM-14" in rd(SCRIPT) and z.count("λ_micro") == 0,
   "核验脚本在 ＋ `λ_micro` 仍 **0 处**（G4 的前置事实未被本轮改动）")

print()
print("=" * 96)
print("通过 {} 项，失败 {} 项{}".format(N[0] - len(FAIL), len(FAIL),
                                 "" if not FAIL else "  ⟹ " + ", ".join(FAIL)))
print("=" * 96)
