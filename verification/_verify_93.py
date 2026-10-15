# -*- coding: utf-8 -*-
"""第 93 轮补丁后核验（两段式：底本取证 ＋ 当前稿确认）。

只读，不改任何文件。伴跑 _ppn_93.py（读备份底本，补丁后复跑仍应全过）。
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
ZHB = "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第93轮前.md"
EN = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
ENB = "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-02第93轮前.md"
LI = "项目台账.md"
LD = "光速的意义_落差分解与超光速的结构性.md"
LSB = "光速的意义_落差分解与超光速的结构性_备份_2026-10-02第93轮前.md"
B3 = "B3_高阶PPN与指数度规.md"
HH = "../环境说明.md"

r = lambda p: io.open(p, encoding="utf-8").read()
zh, zhb, en, enb, li, lsd, lsb, b3, hh = map(r, [ZH, ZHB, EN, ENB, LI, LD, LSB, B3, HH])

print("=== 第 93 轮 补丁后核验 ===")

# V-1 §4.5b
chk("V-1a", "第 93 轮口径注" not in zhb and "第 93 轮口径注" in zh, "ZH §4.5b：底本无注 ⟹ 当前稿有 C-48 注")
chk("V-1b", "Round-93 scope note" not in enb and "Round-93 scope note" in en, "EN §4.5b：同上")
chk("V-1c", "| 框架值 | **1** | **1** | **0（自动 GR 值）** |" in zh, "表行原文保留（只加注、不删改）")

# V-2 §8.6.7(e)
chk("V-2a", "第 93 轮注（N-38）" not in zhb and "第 93 轮注（N-38）" in zh, "ZH §8.6.7(e)：N-38 注已加")
chk("V-2b", "Round-93 note (N-38)" not in enb and "Round-93 note (N-38)" in en, "EN §8.6.7(e)：同上")
chk("V-2c", "引用「C-n」必须写明序列" in zh and "must state its series" in en, "C-50 消歧句（中英）在档")

# V-3 清单 #5
chk("V-3a", "5. ✅ **已结项（第 93 轮）**" in li, "池条目 #5 已结项标记")
chk("V-3b", "~~原条目~~" in li, "原条目保留（不删档）")
chk("V-3c", "~~#5 PPN 优越系~~（✅ 第 93 轮结项）" in li and "C5 ✅ PPN 优越系（第 93 轮结项）" in li,
    "两处剩余待办同步划线")

# V-4 清单计数
chk("V-4a", "| **未解科学难题** | **15 条**" in li and "| **未解科学难题** | **14 条**" not in li, "难题 14 → 15")
chk("V-4b", "| **负面判定** | **38 条**" in li and "| **负面判定** | **37 条**" not in li, "负面 37 → 38")
chk("V-4c", "| **撤回 / 更正** | **49 条**" in li and "| **撤回 / 更正** | **46 条**" not in li, "更正 46 → 49")

# V-5 新行
for tag, row in [("V-5a", "| **C-48** |"), ("V-5b", "| **C-49** |"), ("V-5c", "| **C-50** |"),
                 ("V-5d", "| **N-38** |"), ("V-5e", "| **I-22** |")]:
    chk(tag, row in li, "{} 行在档".format(row.strip("| ")))

# V-6 光速 memo
chk("V-6a", "| α₃ | 10⁻⁸ | 0 | 同上 |" not in lsd and "~~10⁻⁸~~ **4×10⁻²⁰**" in lsd, "α₃ 行已就地更正")
chk("V-6b", lsd.count("4×10⁻²⁰") >= 2, "4×10⁻²⁰ 出现 ≥2 次（行内 ＋ 注）")
chk("V-6c", "~~待核~~ **已核（第 93 轮" in lsd and "第 93 轮核对注" in lsd, "待核 → 已核 ＋ 核对注在档")
chk("V-6d", "α₂ | ~~10⁻⁷~~ **2×10⁻⁹**" in lsd and "ξ | ~~10⁻³~~ **4×10⁻⁹**" in lsd, "α₂ / ξ 行已更新")

# V-7 B3
chk("V-7", "第 93 轮注（C-48）" in b3 and "名不符实" in b3, "B3 memo 已加注")

# V-8 交接说明
chk("V-8a", "当前建议（第 93 轮后）" in hh, "§七 新建议在档")
chk("V-8b", "（历史，第 90 轮后，已被上式取代）" in hh, "旧建议已降级")
chk("V-8c", "第 93 轮新增（候选池 #5 结项" in hh, "第 93 轮新增块在档")

# V-9 论文行数差 ＋ 旧文本保留
chk("V-9a", zh.count("\n") - zhb.count("\n") == 6 and en.count("\n") - enb.count("\n") == 6,
    "ZH/EN 各净增 6 行（纯插入，无删改）")
chk("V-9b", "γ=β=1" in zh and "33%" in zh and "11%" in zh, "分叉数值段未动（本注不涉数字）")

# V-10 关键短语
chk("V-10a", "尚未演示" in zh and "未演示的必要条件" in zh, "ZH 关键短语（尚未演示 / 未演示的必要条件）")
chk("V-10b", "has not been demonstrated" in en and "undemonstrated necessary condition" in en, "EN 关键短语")

# V-11 备忘录
chk("V-11", os.path.exists("PPN优越系结项_静态扇区盲区与未演示的C-2.md"), "本轮备忘录在档")

print()
print("=" * 100)
print("VERIFY93：通过 {} 项，失败 {} 项".format(N - BAD, BAD))
