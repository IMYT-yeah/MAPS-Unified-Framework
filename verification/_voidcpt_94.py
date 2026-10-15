# -*- coding: utf-8 -*-
"""第 94 轮核验：候选池 "void-CPT-κ" 结项 —— 机制已否证而「真预言」判定未降级

任务来源登记（技能陷阱 87）：**外部待办** —— 候选池「void-CPT-κ 异常」。

底本一律读 *_备份_2026-10-02第94轮前.md（铁律 18/20），
⟹ 本脚本**在补丁之后复跑仍然有效**；当前稿状态由 _verify_94.py 做两段式确认。
"""
import io

N = 0
BAD = 0


def chk(tag, ok, msg):
    global N, BAD
    N += 1
    if not ok:
        BAD += 1
    print("  [{}] {:<10} {}".format("OK" if ok else "XX", tag, msg))


def hdr(s):
    print()
    print("=" * 100)
    print(s)
    print("=" * 100)


ZB = "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第94轮前.md"
EB = "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-02第94轮前.md"
LB = "项目台账_备份_2026-10-02第94轮前.md"
M_DM = "暗物质_三大机制全过量级检验.md"
M_BK = "全量待办回溯_我的过度声明更正与真实待办总账.md"
M_AU = "全量冲突审计_撤回链依据等级与未同步检测.md"

ZT = io.open(ZB, encoding="utf-8").read()
ET = io.open(EB, encoding="utf-8").read()
LT = io.open(LB, encoding="utf-8").read()
DM = io.open(M_DM, encoding="utf-8").read()
BK = io.open(M_BK, encoding="utf-8").read()
AU = io.open(M_AU, encoding="utf-8").read()
Z = ZT.split("\n")

# ---------------------------------------------------------------- VC-1
hdr("VC-1  存量清点：底本（备份）里「void」的全部出现点与语境分类")
hits = [(i, s) for i, s in enumerate(Z, 1) if "void" in s]
for i, s in hits:
    print("  L{:<5}| {}".format(i, s.strip()[:170]))
cats = {
    "摘要预言列表": any("空洞-镜像支引力投影关联" in s for _, s in hits),
    "§8.3 条件句": any("仅在该机制被重建后才成立" in s for _, s in hits),
    "§8.4 可检验预言列表": any("可检验预言：**void-CPT-κ" in s for _, s in hits),
    "§9 表第 2 行": any("空洞弱透镜偏强、质量-光脱耦" in s for _, s in hits),
    "第 90 轮台账行": any("void-CPT-κ 异常 | **真预言**" in s for _, s in hits),
    "第 91 轮台账行": any("§8.4 | void-CPT-κ 可检验预言" in s for _, s in hits),
}
print("  语境分类：{}".format({k: ("有" if v else "无") for k, v in cats.items()}))
chk("VC-1a", len(hits) >= 6, "「void」底本出现 = {} 处（预期 ≥6）".format(len(hits)))
chk("VC-1b", all(cats.values()), "六类语境（摘要 / §8.3 / §8.4 / §9 表 / 两张台账）齐备")

# ---------------------------------------------------------------- VC-2
hdr("VC-2  机制否证链：证据是否在档")
chk("VC-2a", "已被否证" in ZT and "读法 A（只有引力跨支共享" in ZT,
    "§8.3【v2.9 修正】在档：镜像支投影已被否证（两读法方向相反）")
chk("VC-2b", "仅在该机制被重建后才成立" in ZT, "§8.3 条件句在档（「仅在该机制被重建后才成立」）")
chk("VC-2c", "硬否证" in DM and "5.31" in DM and "3.82" in DM,
    "否证源（{}）在档：硬否证 5.31 倍 / 3.82 倍".format(M_DM[:18]))
chk("VC-2d", "暗物质的定量解释在本框架中仍是空白" in ZT, "§8.2 自标「仍是空白」在档")

# ---------------------------------------------------------------- VC-3
hdr("VC-3  下游四处（补丁前状态取证 —— 两段式的前半段）")
L27 = [s for s in Z if s.startswith("5. **宇宙学**：")]
L29 = [s for s in Z if "空洞-镜像支引力投影关联" in s]
L1909 = [s for s in Z if "空洞弱透镜偏强、质量-光脱耦" in s]
L1938 = [s for s in Z if "void-CPT-κ 异常 | **真预言**" in s]
L1981 = [s for s in Z if "§8.4 | void-CPT-κ 可检验预言" in s]
chk("VC-3a", len(L27) == 1 and "空白" not in L27[0] and "否证" not in L27[0] and "第 94 轮" not in L27[0],
    "摘要 L27：**未带任何限定**（「给出暗物质密度」「叠加模型」裸留）")
chk("VC-3b", len(L29) == 1 and "第 91 轮注" in L29[0],
    "摘要 L29（预言列表）：已有第 91 轮台账指针 ✓")
chk("VC-3c", len(L1909) == 1 and "机制" not in L1909[0],
    "§9 表第 2 行：状态列未含机制警告（仅「可检验（分析方案已给出）」）")
chk("VC-3d", len(L1938) == 1 and "悬空" not in L1938[0],
    "第 90 轮台账：仍标「真预言」（未降级）")
chk("VC-3e", len(L1981) == 1 and "悬空" not in L1981[0],
    "第 91 轮台账：仍标「真预言」（未降级）")
print("  ⟹ 取证结论：机制侧（VC-2）已否证，而四处下游均未同步 —— 判定高估成立。")

# ---------------------------------------------------------------- VC-4
hdr("VC-4  三方交叉证据（其他文档早已按「悬空/未解决」处理）")
chk("VC-4a", "三大机制全被否证" in LT, "清单 S-8：「三大机制全被否证…框架目前未解决」在档")
chk("VC-4b", "镜像支机制被撤回" in BK, "第 74 轮回溯：“void-CPT-κ（镜像支机制被撤回 ⟹ 悬空）｜待重建”在档")
chk("VC-4c", "镜像支暗物质撤回" in AU, "第 84 轮审计：撤回链抽查含「镜像支暗物质撤回」条在档")

# ---------------------------------------------------------------- VC-5
hdr("VC-5  [INFO] 「真预言」机制轴抽查（±4 行窗口内与撤/否证类词共现）")
PROBE = [
    ("B1–B5 强场包", "B1–B5"),
    ("void-CPT-κ", "void-CPT-κ"),
    ("霍金辐射非热修正", "非热修正"),
    ("火墙厚度", "火墙厚度"),
    ("纠缠熵系数", "纠缠熵"),
    ("QNM", "QNM"),
    ("火墙弥散", "火墙弥散"),
    ("EMRI", "EMRI"),
]
TRIG = ["否证", "撤回", "降调", "结项", "重建", "不成立", "悬空", "空白"]
for name, key in PROBE:
    idx = [i for i, s in enumerate(Z) if key in s]
    found = []
    for i in idx:
        win = "\n".join(Z[max(0, i - 4):i + 5])
        for t in TRIG:
            if t in win:
                found.append((i + 1, t, Z[i].strip()[:80]))
                break
    if found:
        print("  ● {}：{} 处命中".format(name, len(found)))
        for ln, t, txt in found[:4]:
            print("      L{:<5}（{}）| {}".format(ln, t, txt))
    else:
        print("  ○ {}：无命中".format(name))
print("  [INFO] 抽查（非穷举）：除 void-CPT-κ 外未发现第二条「机制已撤而仍列」；")
print("         完整清单见备忘录 §诚实边界 ③。")

# ---------------------------------------------------------------- VC-6
hdr("VC-6  编号对账：候选池 #7/#8 两套互指 ＋ #5 漏改 ＋ C6 状态过期（补丁前取证）")
pool7 = [s for s in LT.split("\n") if s.startswith("7. **EMRI")]
pool8 = [s for s in LT.split("\n") if s.startswith("8. **void-CPT-κ")]
line192 = [s for s in LT.split("\n") if "#7 void-CPT-κ" in s]
line226 = [s for s in LT.split("\n") if "#5（PPN 优越系）" in s]
line308 = [s for s in LT.split("\n") if "C7 void-CPT-κ" in s]
chk("VC-6a", len(pool7) == 1 and len(pool8) == 1, "池表：#7 = EMRI、#8 = void-CPT-κ（本表口径）")
chk("VC-6b", len(line192) == 1 and "#7 void-CPT-κ" in line192[0],
    "「剩余待办」行①：#7 = void-CPT-κ —— **与池表互换**")
chk("VC-6c", len(line226) == 1 and "~~#5（PPN 优越系）~~" not in line226[0],
    "「剩余待办」行②：#5（PPN 优越系）**未划线** —— 第 93 轮漏改（括号写法）")
chk("VC-6d", len(line308) == 1 and "C6 宇宙学动力学" in line308[0] and "C6 ✅" not in line308[0],
    "台账行：C6（宇宙学动力学）**状态过期**（第 75 轮已结项未标）；C7 = void-CPT-κ")
print("  ⟹ 结论：编号不可作引用键（两套 #7/#8 互换）＋ 两处状态标记失真（C-19 族第 12 条）。")

# ---------------------------------------------------------------- VC-7
hdr("VC-7  英文稿同步检查（补丁前）")
en_ok = [
    ("EN §8.3 条件句", "holds only if the mechanism is rebuilt" in ET),
    ("EN §8.3 可检验预言行", "Testable prediction: **void-CPT-κ anomaly**" in ET),
    ("EN §9 表第 2 行", "testable (analysis scheme given) |" in ET and "void-CPT-κ anomaly** (void regions" in ET),
    ("EN 90 台账行", "void-CPT-κ anomaly | **true prediction** | analysis plan given" in ET),
    ("EN 91 台账行", "§8.4 | void-CPT-κ testable prediction | **true prediction**" in ET),
    ("EN 摘要句", "yields the dark-matter density; dark matter = superposition model" in ET),
]
for k, v in en_ok:
    print("  {}：{}".format(k, "在档" if v else "**缺失**"))
chk("VC-7", all(v for _, v in en_ok), "英文稿六处全部在档 ⟹ 本轮补丁需中英同步六处")

# ---------------------------------------------------------------- VC-8
hdr("VC-8  清单计数（补丁前；补丁后应变 15 / 39 / 52）")
chk("VC-8a", "| **未解科学难题** | **15 条**" in LT, "难题 15 条（本轮不变）")
chk("VC-8b", "| **负面判定** | **38 条**" in LT, "负面 38 条 → 补丁后 39（+N-39）")
chk("VC-8c", "| **撤回 / 更正** | **49 条**" in LT, "更正 49 条 → 补丁后 52（+C-51/52/53）")

# ---------------------------------------------------------------- VC-9
hdr("VC-9  任务来源登记（陷阱 87）＋ 判决草案")
print("  任务来源 = **外部待办**：候选池「void-CPT-κ 异常」（非内部循环）")
print("  判决草案（第 94 轮）：")
print("   ① 「真预言」判定**降级** → **悬空（机制未重建）**（C-51；§9 表 ↔ 90/91 台账 ↔ §8.4 ↔ 摘要 四处统一）")
print("   ② 摘要第 5 条暗物质表述加限定（C-52：以 §8.2「空白」/§8.3「已否证」为准）")
print("   ③ 候选池引用对账（C-53：#7/#8 两套互换、#6 异义、#5 漏改、C6 过期）")
print("   ④ 登记 **N-39**：不得把（机制已撤的）void-CPT-κ 计为可维持的可检验预言")
print("   ⑤ 计数影响：§9 表「真预言 11 → 10 ＋ 悬空 1」；正文级台账「真预言 2 → 1 ＋ 悬空 1」")

print()
print("=" * 100)
print("VOIDCPT94：通过 {} 项，失败 {} 项".format(N - BAD, BAD))
print("=" * 100)
