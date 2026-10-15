# -*- coding: utf-8 -*-
"""第 103 轮补丁核验（V-1 … V-20）。

⚠️ 两段式（陷阱 72）：凡「本轮把某个 Bad 状态改好」的检查，一律用
   「补丁前备份取证 ＋ 补丁后确认」两段，避免「改好了反而翻红」。
"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
ZH_PRE = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-04第103轮前.md")
EN_PRE = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-04第103轮前.md")
LIST = os.path.join(BASE, "工程期望清单.md")
HAND = os.path.join(os.path.dirname(BASE), "环境交接说明.md")
MEMO = os.path.join(BASE, "甲4结项_麦克斯韦谱_恒等式验证与二阶各向同性定理.md")
OUT = os.path.join(BASE, "_maxwell_103_out.txt")


def rd(p):
    return io.open(p, encoding="utf-8").read()


OK, BAD = [], []


def ck(tag, cond, msg):
    (OK if cond else BAD).append(tag)
    print("  [{}] {:<7} {}".format("OK" if cond else "XX", tag, msg))


zh, en = rd(ZH), rd(EN)
zhp, enp = rd(ZH_PRE), rd(EN_PRE)
L, H = rd(LIST), rd(HAND)
memo = rd(MEMO)
out = rd(OUT)

print("=" * 92)
print("第 103 轮补丁核验")
print("=" * 92)

# ---------- 论文 ZH ----------
print("\n[论文 · 中文稿]")
ck("V-1", "**ω=|k|（长波极限）**" in zh and "第 103 轮更正" in zh,
   "ZH §5.8 L1100：`ω=|k|` 已加「（长波极限）」限定 ＋ 「第 103 轮更正」标注")
ck("V-2", "该 0.9999 = k=0.05 处" in zh and "1 − k²/24 = 0.9998958" in zh,
   "ZH §5.8 L1121：「数值验证 C」已加注（泰勒值 ＋ 不构成验证）")
ck("V-3", "**【第 103 轮（甲-4）麦克斯韦谱" in zh and "MW-1 … MW-10，25 项 0 失败" in zh,
   "ZH §10.1b：第 103 轮块已插入（含脚本与核验项数）")
ck("V-4", "`Sym²(T₁)` 的不变子空间维数 = 1" in zh and "`Sym⁴(T₁)` 的不变子空间维数 = 2" in zh,
   "ZH 块含表示论分层结论（Sym² = 1 ⟹ 各向同性定理；Sym⁴ = 2 ⟹ 四阶必各向异性）")
ck("V-5", "**~~麦克斯韦谱严格验证~~ ✅ 第 103 轮结项**" in zh,
   "ZH §10.2#13：「麦克斯韦谱严格验证」已划掉并标结项")

# ---------- 论文 EN ----------
print("\n[论文 · 英文稿]")
ck("V-6", "**ω=|k| (long-wavelength limit)**" in en and "corrected in round 103" in en,
   "EN §5.8 L1116：对应更正已同步")
ck("V-7", "1 − k²/24 = 0.9998958" in en and "round 103" in en,
   "EN §5.8 L1139：`Numerical verification C` 已加注")
ck("V-8", "**【Round 103 (item 甲-4) Maxwell spectrum" in en,
   "EN §10.1b：第 103 轮块已插入")
ck("V-9", "the invariant subspace of `Sym²(T₁)` has dimension 1" in en
   and "has dimension 2" in en,
   "EN 块含表示论分层结论（中英对称）")
ck("V-10", "**~~rigorous Maxwell-spectrum verification~~ ✅ closed in round 103**" in en,
   "EN §10.2#13：对应收口已同步")
ck("V-11", zh.count("第 103 轮") >= 5 and en.count("round 103") + en.count("Round 103") >= 4,
   "中英两稿都含第 103 轮的 ≥4 处登记（ZH {} 处 / EN {} 处）".format(
       zh.count("第 103 轮"), en.count("round 103") + en.count("Round 103")))

# ---------- 两段式（陷阱 72）----------
print("\n[两段式取证（补丁前 / 补丁后）]")
ck("V-12", ("ω/k=1.0000" in zhp) and ("第 103 轮更正" not in zhp),
   "补丁前：`ω/k=1.0000 验证` **无任何标注**（= 以恒等式冒充验证）—— 取证成立")
ck("V-13", ("ω/k=1.0000" in zh) and ("第 103 轮更正" in zh),
   "补丁后：该串**保留在「更正注」里**（历史留痕）＋ 已带标记 —— 确认已修")

# ---------- 块结构（陷阱 74 的子坑：块内不得有空行）----------
print("\n[块结构]")
i0 = zh.find("**【第 103 轮（甲-4）麦克斯韦谱")
i1 = zh.find("详见《甲4结项_麦克斯韦谱", i0)
seg = zh[i0:i1 + 30]
lines = [s for s in seg.split("\n")]
n_blank = sum(1 for s in lines if s.strip() == "")
ck("V-14", i0 > 0 and i1 > i0 and n_blank == 0,
   "ZH 第 103 轮块：区间长度 {} 行，**内部空行 = {}**（轮次块判据要求块内无空行，"
   "否则会被切段 ⟹ 自指污染）".format(len(lines), n_blank))
j0 = en.find("**【Round 103 (item 甲-4) Maxwell spectrum")
j1 = en.find("See 《甲4结项_麦克斯韦谱", j0)
seg_en = en[j0:j1 + 30] if j1 > j0 else en[j0:j0 + 3000]
n_blank_en = sum(1 for s in seg_en.split("\n") if s.strip() == "")
ck("V-15", j0 > 0 and n_blank_en == 0,
   "EN 第 103 轮块：内部空行 = {}".format(n_blank_en))

# ---------- 清单 ----------
print("\n[工程期望清单]")
ck("V-16", "| **第 103 轮**（**甲-4 执行**） |" in L,
   "§零 表格已加第 103 轮行")
ck("V-17", "| **C-67** | ⭐⭐ **「数值验证」是恒等式（第 103 轮；甲-4）**" in L,
   "更正表已加 C-67 行（类型 = 更正 / 判定降级）")
ck("V-18", "| **撤回 / 更正** | **66 条**" in L,
   "计数已更新 65 → **66**")
ck("V-19", "**~~甲-4 麦克斯韦谱严格化~~ ✅ 第 103 轮结项**" in L,
   "「剩余待办」行已更新甲-4 结项")
ck("V-20", "**甲类只剩 甲-5**" in L and "有明确可判定入口的待办已清空" not in L,
   "⚠️ 原句「有明确可判定入口的待办已清空」在甲-4/甲-5 未完时**是错的** ⟹ 已改为"
   "「甲类只剩 甲-5」（同轮修正一处**过度声明**）")

# ---------- 交接说明 ----------
print("\n[环境交接说明]")
ck("V-21", "**当前建议（第 103 轮后）**" in H and "**（历史，第 102 轮后）**" in H,
   "§七：新建议在前、旧建议标「（历史，第 102 轮后）」")
ck("V-22", "**第 103 轮新增（甲-4：麦克斯韦谱严格化" in H,
   "已加第 103 轮新增段（6 条：C-67／严格化／表示论／措辞更正／结项／诚判）")

# ---------- 脚本与备忘录 ----------
print("\n[脚本与交付件]")
ck("V-23", os.path.exists(MEMO) and "MW-1 … MW-10，25 项 0 失败" in memo,
   "备忘录存在且含核验项数")
ck("V-24", "通过 25 项，失败 0 项" in out,
   "`_maxwell_103.py` 的**补丁后复跑**仍 **25 项 0 失败**（存档 `_maxwell_103_out.txt`）")
ck("V-25", "MW-3" in memo and "99.59%" in memo and "1/12" in memo and "1/36" in memo,
   "备忘录含三个关键数：界的紧度 99.59%、四阶系数 1/12（[100]）与 1/36（[111]）")

print("\n" + "=" * 92)
print("通过 {} 项，失败 {} 项".format(len(OK), len(BAD)))
if BAD:
    print("失败项：" + ", ".join(BAD))
print("=" * 92)
