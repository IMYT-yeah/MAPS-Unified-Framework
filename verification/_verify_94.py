# -*- coding: utf-8 -*-
"""第 94 轮补丁后核验（两段式：底本取证 ＋ 当前稿确认）。

只读，不改任何文件。伴跑 _voidcpt_94.py（读备份底本，补丁后复跑仍应全过）。
"""
import io
import os

N = 0
BAD = 0


def chk(tag, ok, msg):
    global N, BAD
    N += 1
    if not ok:
        BAD += 1
    print("  [{}] {:<8} {}".format("OK" if ok else "XX", tag, msg))


ZH = "论文初稿_正反物质对风暴统一框架_v2.9.md"
ZHB = "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第94轮前.md"
EN = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
ENB = "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-02第94轮前.md"
LI = "工程期望清单.md"
LIB = "工程期望清单_备份_2026-10-02第94轮前.md"
HH = "../环境交接说明.md"

r = lambda p: io.open(p, encoding="utf-8").read()
zh, zhb, en, enb, li, lib, hh = map(r, [ZH, ZHB, EN, ENB, LI, LIB, HH])

print("=== 第 94 轮 补丁后核验 ===")

# V-1 摘要 C-52
chk("V-1a", "第 94 轮注（C-52）" not in zhb and "第 94 轮注（C-52）" in zh,
    "ZH 摘要：底本无注 ⟹ 当前稿有 C-52 限定注")
chk("V-1b", "以 §8.2／§8.3 为准" in zh, "限定句（以 §8.2／§8.3 为准）在档")
chk("V-1c", "Round-94 note (C-52)" not in enb and "Round-94 note (C-52)" in en, "EN 摘要：同步")

# V-2 §8.4
chk("V-2a", "- 可检验预言：**void-CPT-κ 异常**" in zhb and "条件性 —— 第 94 轮注（C-51）" in zh,
    "ZH §8.4：底本无条件 ⟹ 当前稿加条件性")
chk("V-2b", "conditional — round-94 note (C-51)" in en, "EN §8.4：同步")

# V-3 §9 表
chk("V-3a", "机制已撤（§8.3 否证）：仅重建后成立（第 94 轮）" in zh, "ZH §9 表第 2 行：机制警告在档")
chk("V-3b", "mechanism withdrawn (§8.3 falsification): holds only if rebuilt (round 94)" in en, "EN §9 表：同步")

# V-4 90 台账行
chk("V-4a", "void-CPT-κ 异常 | **真预言** |" in zhb and "~~**真预言**~~ **悬空（机制未重建）**" in zh
    and "第 94 轮 C-51**：机制（镜像支投影）已硬否证" in zh, "ZH 90 台账行：降级 ＋ 依据在档")
chk("V-4b", "dangling (mechanism not rebuilt)" in en and "round-94 C-51" in en, "EN 90 台账行：同步")

# V-5 90 汇总/派生
chk("V-5a", "真预言 10 ＋ 悬空（机制未重建）1" in zh and "~~11~~ **10** 条「真预言」里" in zh,
    "ZH 90 汇总（10＋悬空 1）＋ 派生句（10 条）")
chk("V-5b", "true prediction 10 + dangling (mechanism not rebuilt) 1" in en and "among the ~~11~~ **10**" in en,
    "EN 90 汇总＋派生句：同步")

# V-6 90 块尾注
chk("V-6a", "【第 94 轮更正（C-51）】" in zh and "清单 **S-8**、第 84 轮审计" in zh, "ZH 90 块尾注在档")
chk("V-6b", "【Round-94 correction (C-51)】" in en, "EN 90 块尾注在档")

# V-7 91 台账
chk("V-7a", "§8.4 | void-CPT-κ 可检验预言 | ~~**真预言**~~ **悬空（机制未重建）**" in zh
    and "真预言 1 ＋ 悬空 1" in zh and "（C-51，同第 90 轮块）" in zh, "ZH 91 台账行＋汇总＋尾注")
chk("V-7b", "dangling (mechanism not rebuilt)" in en and "true prediction 1 + dangling 1" in en
    and "same as the round-90 block" in en, "EN 91 台账：同步")

# V-8 清单
chk("V-8a", "8. ✅ **已结项（第 94 轮）**" in li and "悬空（机制未重建）" in li, "池条目 8：结项＋降级标记")
chk("V-8b", "编号对账（第 94 轮 C-53）" in li and "引用候选池条目一律用名字" in li, "池表对账注在档")
chk("V-8c", "~~#7 void-CPT-κ~~（✅ 第 94 轮结项）" in li and "~~#5（PPN 优越系）~~（✅ 93 轮）" in li
    and "void-CPT-κ ✅ 94 轮" in li, "三行「剩余待办」划线齐")
chk("V-8d", "**C6 ✅ 宇宙学动力学（第 75 轮结项 ⟹ I-20" in li and "**C7 ~~void-CPT-κ~~（✅ 第 94 轮结项：悬空）**" in li,
    "台账行 C6/C7：补标")
chk("V-8e", "| **负面判定** | **39 条**" in li and "| **撤回 / 更正** | **52 条**" in li, "计数：39 / 52")
for tag, row in [("V-8f", "| **C-51** |"), ("V-8g", "| **C-52** |"), ("V-8h", "| **C-53** |"), ("V-8i", "| **N-39** |")]:
    chk(tag, row in li, "{} 新行在档".format(row.strip("| ")))

# V-9 交接
chk("V-9a", "当前建议（第 94 轮后）" in hh and "（历史，第 93 轮后，已被上式取代）" in hh, "§七：新建议 ＋ 旧降级")
chk("V-9b", "第 94 轮新增（候选池 void-CPT-κ 结项" in hh, "第 94 轮新增块在档")

# V-10 行数差（纯插入，无删改）
chk("V-10a", zh.count("\n") - zhb.count("\n") == 2 and en.count("\n") - enb.count("\n") == 2,
    "ZH/EN 各净增 2 行（块尾注 ×2；其余为行内替换）")

# V-11 「真预言 11」旧串不再裸留（已被划线版替换）
chk("V-11a", "**真预言 11** ｜" not in zh and "真预言 11" not in en, "旧汇总串不再裸留（ZH/EN）")
chk("V-11b", "void-CPT-κ 异常 | **真预言**" not in zh and "void-CPT-κ anomaly | **true prediction**" not in en,
    "旧「真预言」台账串不再裸留（ZH/EN）")

# V-12 备忘录
chk("V-12", os.path.exists("void-CPT-κ结项_机制已否证而判定未降级.md"), "本轮备忘录在档")

print()
print("=" * 100)
print("VERIFY94：通过 {} 项，失败 {} 项".format(N - BAD, BAD))
