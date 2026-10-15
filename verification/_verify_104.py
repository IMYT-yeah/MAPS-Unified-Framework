# -*- coding: utf-8 -*-
"""第 104 轮补丁核验（V-1 … V-21）。两段式（陷阱 72）：修复型检查一律「补丁前取证 ＋ 补丁后确认」。"""
import io
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
ZH_PRE = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-04第104轮前.md")
EN_PRE = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-04第104轮前.md")
LIST = os.path.join(BASE, "工程期望清单.md")
HAND = os.path.join(os.path.dirname(BASE), "环境交接说明.md")
MEMO = os.path.join(BASE, "甲5结项_N2的4π相位锁定相容性方程.md")
OUT = os.path.join(BASE, "_n2phase_104_out.txt")


def rd(p):
    return io.open(p, encoding="utf-8").read()


OK, BAD = [], []


def ck(tag, cond, msg):
    (OK if cond else BAD).append(tag)
    print("  [{}] {:<7} {}".format("OK" if cond else "XX", tag, msg))


zh, en = rd(ZH), rd(EN)
zhp, enp = rd(ZH_PRE), rd(EN_PRE)
L, H = rd(LIST), rd(HAND)
memo, out = rd(MEMO), rd(OUT)

print("=" * 94)
print("第 104 轮补丁核验")
print("=" * 94)

# ---------- 论文 ZH ----------
print("\n[论文 · 中文稿 §4.9]")
ck("V-1", "**4π 不是自由参数**" in zh and "SU(2) 旋量单值性" in zh,
   "ZH N1 行已加 4π 严格化注（不是自由参数 ⟸ 最低自旋 1/2）")
ck("V-2", "第 104 轮升级为定理" in zh and "双平面锁定在 su(2) 代数下无解" in zh,
   "ZH N2 行已加 su(2) 定理（双平面无解）")
ck("V-3", "**C-69**" in zh and "`_now_numeric.py` **已丢失**" in zh,
   "ZH N2 行已带 C-69 限定（启发式 ＋ 脚本已丢失 ⟹ 不得作独立证据）")
ck("V-4", "**【v2.9 补充（第 104 轮：N2 的 4π 相位锁定相容性方程" in zh,
   "ZH §4.9 已插入第 104 轮块（7 条）")
ck("V-5", "\\boxed{a = 0}" in zh or "a = 0}$" in zh,
   "ZH 块含三行代数的结论式 $a = 0$")
ck("V-6", "**~~N2 的 4π 相位锁定相容性方程~~ ✅ 第 104 轮结项**" in zh,
   "ZH §10.2#7 已收口（划掉 ＋ 结项）")
ck("V-7", "四项严格性**各不相同**" in zh,
   "ZH N1–N4 标题行已加「四项严格性各不相同」注")

print("\n[论文 · 英文稿]")
ck("V-8", "**4π is not a free parameter**" in en and "SU(2) spinor single-valuedness" in en,
   "EN N1 行已同步")
ck("V-9", "**upgraded to a theorem in round 104**" in en and "two-plane locking is impossible in su(2)" in en,
   "EN N2 行已同步")
ck("V-10", "`_now_numeric.py`) is lost" in en,
   "EN N2 行已带 C-69 限定")
ck("V-11", "**【v2.9 supplement (round 104: N2's 4π phase-locking compatibility equation" in en,
   "EN §4.9 已插入第 104 轮块")
ck("V-12", "~~N2's 4π phase-locking compatibility equation~~ ✅ closed in round 104" in en,
   "EN §10.2#7 已收口")
ck("V-13", "the four items have **different** levels of rigor" in en,
   "EN N1–N4 标题行已加注")

# ---------- 两段式（陷阱 72）----------
print("\n[两段式取证（C-70 的修复）]")
ck("V-14", "【Derivation, proposition chain in §4.9】" in enp,
   "补丁前：EN §1 标【Derivation, proposition chain in §4.9】—— 与 §4.9 的【Framework assumption】冲突 ⟹ 取证成立")
ck("V-15", "【Framework assumption + proposition chain in §4.9" in en and "【Derivation, proposition chain in §4.9】" not in en,
   "补丁后：EN §1 已改为【Framework assumption + proposition chain…】⟹ 冲突解除")

# ---------- 块结构（块内不得有空行）----------
print("\n[块结构]")
# ⚠️ 区间右端必须**卡在该行行尾**（第一版写 i1 + 40 ⟹ 把**块后的空行**算成"内部空行"）
#    ⟹ 假 FAIL（同第 100 轮 LF-16：检查器自己误报）。
i0 = zh.find("**【v2.9 补充（第 104 轮：")
i1 = zh.find("详见《甲5结项_N2的4π相位锁定相容性方程》", i0)
seg = zh[i0:zh.index("\n", i1)]
blank = sum(1 for s in seg.split("\n") if s.strip() == "")
ck("V-16", i0 > 0 and i1 > i0 and blank == 0,
   "ZH 第 104 轮块：{} 行、**内部空行 = {}**（轮次块判据要求块内无空行）".format(
       len(seg.split("\n")), blank))
j0 = en.find("**【v2.9 supplement (round 104:")
j1 = en.find("See 《甲5结项_N2的4π相位锁定相容性方程》", j0)
seg_en = en[j0:en.index("\n", j1)] if j1 > j0 else en[j0:j0 + 4000]
blank_en = sum(1 for s in seg_en.split("\n") if s.strip() == "")
ck("V-17", j0 > 0 and blank_en == 0, "EN 第 104 轮块：内部空行 = {}".format(blank_en))

# ---------- 清单 ----------
print("\n[工程期望清单]")
ck("V-18", "| **第 104 轮**（**甲-5 执行**） |" in L, "§零 表格已加第 104 轮行")
ck("V-19", all("| **{}** |".format(c) in L for c in ["C-68", "C-69", "C-70", "C-71"]),
   "更正表已加 C-68 / C-69 / C-70 / C-71 四行")
ck("V-20", "| **撤回 / 更正** | **70 条**" in L, "计数已更新 69 → **70**")
ck("V-21", "**~~甲-5 N2 的 4π 相位锁定相容性方程~~ ✅ 第 104 轮结项**" in L
   and "**甲类（甲-1…甲-5）已全部结项（✅ 第 100–104 轮）**" in L,
   "「剩余待办」行已更新甲-5 结项 ＋ 甲类全部结项")

seq = [re.match(r"^\|\s*\*\*([CNI]-\d+)\*\*\s*\|", s).group(1)
       for s in L.split("\n") if re.match(r"^\|\s*\*\*([CNI]-\d+)\*\*\s*\|", s)]
i = seq.index("C-67")
ck("V-22", seq[i:i + 8] == ["C-67", "C-68", "C-69", "C-70", "C-71", "C-64", "C-65", "C-66"],
   "**表格块完整性**：C-67…C-71 连续，且 **C-64/C-65/C-66（第 102 轮块）恢复连续**（修 103 轮引入的切开）")

# ---------- 交接 ----------
print("\n[环境交接说明]")
ck("V-23", "**当前建议（第 104 轮后）**" in H and "**（历史，第 103 轮后）**" in H,
   "§七：新建议在前、旧建议标「（历史，第 103 轮后）」")
ck("V-24", "**第 104 轮新增（甲-5：N2 的 4π 相位锁定相容性方程" in H,
   "已加第 104 轮新增段（8 条）")

# ---------- 脚本与交付件 ----------
print("\n[脚本与交付件]")
ck("V-25", os.path.exists(MEMO) and "NP-1 … NP-14，24 项 0 失败" in memo,
   "备忘录存在且含核验项数")
ck("V-26", "通过 24 项，失败 0 项" in out,
   "`_n2phase_104.py` **24 项 0 失败**（存档 `_n2phase_104_out.txt`）")
ck("V-27", "j = 0 … 5" in out and "0.447214" in out,
   "存档含关键数据（9 个 j 穷举 ＋ 反例的 ⟨J₁⟩=0.447214）")

print("\n" + "=" * 94)
print("通过 {} 项，失败 {} 项".format(len(OK), len(BAD)))
if BAD:
    print("失败项：" + ", ".join(BAD))
print("=" * 94)
