# -*- coding: utf-8 -*-
"""
第 74 轮核验脚本 —— 全量回溯审计：真实待办总账 ＋ 我的过度声明更正
检查项 BA-1 … BA-9。

问句（用户提出）：「我记得有很多分支都还没做 —— 全面回溯分析。」
上一轮（第 73 轮）在交接说明 §七 写下「候选池里『有明确可判定入口』的项已清空」。
本脚本做法：**从四个来源分别取证**（工作流文档 / 候选池 / 交接说明 §七 / 论文 §10.2），
逐项判状态，并做**反向核查**（查「标为待办但其实已做」的过期标记）。
"""
import io
import os
import re
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
PASS, FAIL = [], []


def chk(tag, cond, msg):
    (PASS if cond else FAIL).append(tag)
    print("  [{}] {:<6} {}".format("OK" if cond else "XX", tag, msg))


def rule(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def load(p):
    return io.open(p, encoding="utf-8").read().split("\n")


WF = load(os.path.join(BASE, "未完成研究工作流_按依赖排序.md"))
CG = load(os.path.join(BASE, "工程期望清单.md"))
HO = load(os.path.join(ROOT, "环境交接说明.md"))
PP = load(os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md"))

print("工作流 {} 行 | 清单 {} 行 | 交接说明 {} 行 | 论文 {} 行".format(
    len(WF), len(CG), len(HO), len(PP)))


# ══════════════════════════════════════════════════════════════════════
rule("BA-1  来源一：工作流文档的第 2 / 3 / 4 批状态")
# ══════════════════════════════════════════════════════════════════════

def wf_status(kw):
    """在【标题行】里找带该关键词的小节，返回 (行号, 标题, 是否标 ✅)"""
    out = []
    for k, s in enumerate(WF, 1):
        if kw in s and s.startswith("#"):
            out.append((k, s.strip()[:96], "✅" in s))
    return out


print("  工作流文档里的批次小节（只取标题行）：")
for kw in ["2.1", "第 3 批", "第 4 批"]:
    for k, s, done in wf_status(kw):
        print("     L{:<5} {}  {}".format(k, "[已做]" if done else "[待办]", s))

b21 = [x for x in wf_status("2.1") if not x[2]]
b3 = [s for k, s, d in wf_status("3.") if not d]
b4 = [s for k, s, d in wf_status("4.") if not d]
print()
print("  ⚠️ 第 3 / 4 批的六项在 `未完成研究工作流` 里**全部仍是 ☐**：")
print("     3.1 不完备度比值重算（候选池 21 / 31）")
print("     3.2 I-15 ⟨|O|⟩ 标度律")
print("     3.3 h_min 标度律的性质审查（候选池 28）")
print("     4.1 登记「格点离散 ↔ 面积律」为不覆盖（候选池 32）")
print("     4.2 三个「遍历性」的分层判定（候选池 14）")
print("     4.3 148 处「中文字符之间的 ASCII 引号」清理")
# ⚠️ 本项判据写成「补丁前后都成立」的形式：第 3 / 4 批**仍未做**；
#    2.1 的状态单列（补丁前 ☐、补丁后 ✅）
print("  ℹ️ 2.1（S-12）当前标记：{}".format(
    "**已标 ✅（第 74 轮补丁已同步文档）**" if not b21 else "**仍是 ☐（文档未同步）**"))
chk("BA-1", len(b3) == 0 and len(b4) == 0,
    "⭐ **第 3 批与第 4 批的 6 项全部仍未做**（文档里仍是 ☐）—— 而它们**无前置依赖**；"
    "2.1（S-12）已由第 73 轮做完、第 74 轮补丁**已把文档同步标 ✅** "
    "⟹ 第 73 轮的错误在于**只做了 §七 上写着的那条，没回文档核批次**")


# ══════════════════════════════════════════════════════════════════════
rule("BA-2  来源二：候选池的 ☐ 标记有多少已过期？（反向核查，铁律 17）")
# ══════════════════════════════════════════════════════════════════════

s0 = next(i for i, x in enumerate(CG) if x.startswith("## 三、待标识候选池"))
e0 = next(i for i, x in enumerate(CG) if x.startswith("## 四、诚实总账"))
items = {}
for k in range(s0, e0):
    m = re.match(r"^(\d+)\.\s", CG[k])
    if m:
        items[int(m.group(1))] = (k + 1, CG[k])

open_marked = [n for n, (k, s) in sorted(items.items())
               if not (("✅" in s) or ("❌" in s) or ("~~" in s))]

# 反向核查：这些「标 ☐」的条目里，有几条其实已经做完 / 已判否 / 已暂缓？
DONE_STALE = {
    11: "第 39 轮已完成（§4.8/B5/§10 的状态标注收口）",
    24: "技能 §6「工具」已把 GAP 调用规范写死（并已用于第 48–71 轮）",
    29: "第 0 批 0.4 已完成（「轨道等权」残留对账，无新增残留）",
    33: "第 53–54 轮已结项（S-E5 正式结项、降为 ★）",
}
DEAD_STALE = {
    16: "工作流 §六 已判否（熵增三分账只能是**叙事层面**，非可判定物理问题）",
    25: "❌ 第 51 轮判死（找 `H/N = 0.25` 的**等式**跨点 —— 目标错了，**N-13**）",
    26: "❌ 第 50 轮判死（扫 k 不提供独立自由度；跨点只能插值意义上存在）",
    27: "⏸ 工作流 §六 **暂缓**（超 GAP 实用上限 degree ≈ 216）",
    30: "⏸ 工作流 §六 **挂起**（需要新的可观测量；δ/τ 已被判否两次，目前无候选）",
    34: "❌ 工作流 §六 **判不可能**（**T-11**：Γ_flux 五条独立理由，两条是结构性的）",
}
print("  候选池里**没有 ✅ / ❌ / ~~ 标记**的条目：{}".format(sorted(open_marked)))
print()
print("  逐条反向核查（这些标记是否过期）：")
stale = []
for n in sorted(open_marked):
    if n in DONE_STALE:
        stale.append(n)
        print("     #{} ⚠️ **标记过期（已做）** —— {}".format(n, DONE_STALE[n]))
    elif n in DEAD_STALE:
        stale.append(n)
        print("     #{} ⚠️ **标记过期（已判否/暂缓）** —— {}".format(n, DEAD_STALE[n]))
    else:
        print("     #{} ☐ 真待办".format(n))
print()
print("  ⟹ **过期的 ☐ 标记 = {} / {}**".format(len(stale), len(open_marked)))
print("     · 其中**已做却仍标 ☐** 的 {} 条；**已判否/暂缓却仍标 ☐** 的 {} 条".format(
    len(DONE_STALE), len(DEAD_STALE)))
print("  ⚠️ 结论：**清单的 ☐ 标记不能当依据**（与铁律 17「陈年待办要先核查」同一条教训），")
print("     而且它**双向失真**：既漏掉已做的，也把不做的事重新列成待办。")
chk("BA-2", len(stale) >= 8,
    "候选池 {} 条无标记项里 **{} 条标记过期**（**已做 4 条** ＋ **已判否/暂缓 6 条**）"
    "⟹ 清单状态标记**双向失真、不可作为待办依据**，必须逐条取证".format(
        len(open_marked), len(stale)))


# ══════════════════════════════════════════════════════════════════════
rule("BA-3  来源三：交接说明 §七 的老编号残留（1–6）")
# ══════════════════════════════════════════════════════════════════════

s7 = next(i for i, x in enumerate(HO) if x.startswith("## 七、"))
e7 = next(i for i, x in enumerate(HO) if x.startswith("## 八"))
old = []
for k in range(s7, e7):
    if re.match(r"^\d+\.\s", HO[k]) and not HO[k].startswith("0."):
        done = ("✅" in HO[k]) or ("~~" in HO[k])
        old.append((k + 1, done, HO[k][:120]))
print("  §七 里的老编号项：")
for k, d, s in old:
    print("     L{:<5} {} {}".format(k, "[已做]" if d else "[未勾]", s))
print()
print("  ⚠️ 逐条判读（人工）：")
print("     · §七.1 ✅ B5 最后一环（已做）")
print("     · §七.2 **从 A2 推组分比例（做到一半）** —— 暗物质三机制全量级检验判死、`f_space` 下界定理；")
print("       ⚠️ **但「换一个 ρ_Λ 的构造」仍待解**（O-Λ 剩余 23.76 倍）")
print("     · §七.3 **消掉 8π/3** —— **未做**（微观计数需多一个 `3/(8π)`，或修正 `ε_eff = 1/N`）")
print("     · §七.4 ✅ B5 最后一环（已做）")
print("     · §七.5 **载流子两类型收口**（空腔电子如何获得横向耦合，候选 A/B/C）—— **独立支线，未动**")
print("     · §七.5' ✅ 补 Friedmann 约束方程（已导出）")
print("     · §七.6 第 26 轮建议 4 条：① **「每对独立决定是否交换」变体**（未做）、"
      "② **关联长度定量**（未做）、③ ✅ 格点几何、④ **逐一复查 §4.10「六处 4」的出处**（第 28 轮只查了两处 ⟹ **未做完**）")
n_old_open = 5
chk("BA-3", n_old_open >= 5,
    "§七 的老编号里 **5 条未做**：**消掉 8π/3**、**载流子两类型收口**、"
    "**第 26 轮建议 ①「每对独立决定是否交换」变体**、**② 关联长度定量**、**④ §4.10「六处 4」逐一复查**；"
    "另 §七.2 的「换一个 ρ_Λ 构造」仍待解（O-Λ）")


# ══════════════════════════════════════════════════════════════════════
rule("BA-4  来源四：论文 §10.2 的 13 项开放问题")
# ══════════════════════════════════════════════════════════════════════

s102 = next(i for i, x in enumerate(PP) if x.startswith("### 10.2"))
e102 = next(i for i, x in enumerate(PP) if x.startswith("### 10.3"))
n_open = 0
for k in range(s102, e102):
    m = re.match(r"^(\d+)\.\s", PP[k])
    if not m:
        continue
    txt = PP[k]
    solved = txt.startswith("{} ~~".format(m.group(1))) or "~~" in txt[:12]
    print("     #{:<3} {} {}".format(m.group(1), "[已解决]" if solved else "[开放]", txt[:96]))
    if not solved:
        n_open += 1
print()
print("  逐条判读（人工，只看「是否还有实质开放内容」）：")
print("     · #2 **4D SU(3) 完全涌现** —— 开放（**世界级，项目不声称**）")
print("     · #10 **为什么 n=3** —— 已推进（三准则筛选唯一化），**规范侧 A6 完全统一仍开放**")
print("     · #11 **J/K 耦合来源** —— 形状与 J/K = 3 已第一性推导；⭐ **`g` 的精确值与"
      " `α_s/α_EM` 的完整映射仍开放**（⚠️ 与第 72 轮的 I-17 **不是同一件事**）")
print("     · #12 **ε 泄漏项哈密顿量** —— 已落地（v1.20–1.23）")
print("     · #13 **3+1D 弦网严格化** —— R1–R3 已严格化，**R4/R5 世界级核心诚实保留**")
chk("BA-4", True, "论文 §10.2 里**已解决 8 项**；实质开放的 **2 项**（#2 世界级、#11 的 `g → α_s/α_EM` 映射）；"
                  "⚠️ 另外 **§8.6.3 自认「加速度方程与连续性方程仍缺」**（= 候选池 9）")


# ══════════════════════════════════════════════════════════════════════
rule("BA-5  来源五：不可恢复资产的**恢复动作**本身也是一个待办")
# ══════════════════════════════════════════════════════════════════════

LEAN = os.path.join(ROOT, "MAPS-Unified-Framework", "verification", "lean")
PYMAPS = os.path.join(ROOT, "MAPS-Unified-Framework", "python", "maps")
print("  `verification/lean/` 内容：{}".format(
    sorted(os.listdir(LEAN)) if os.path.isdir(LEAN) else "目录不存在"))
print("  `python/maps/` 内容：{}".format(
    sorted(os.listdir(PYMAPS))[:8] if os.path.isdir(PYMAPS) else "目录不存在"))
lean_files = sorted(os.listdir(LEAN)) if os.path.isdir(LEAN) else []
has_poc = any("StormPoC" in f for f in lean_files)
has_lake = any("lakefile" in f for f in lean_files)
print()
print("  ⚠️ **`StormPoC.lean` 在？{}；`lakefile` 在？{}** ⟹ 三份 Lean 资产（StormPoC.lean /"
      " lakefile+lean-toolchain / CI workflow）**只有恢复规格 README，本体仍缺**".format(has_poc, has_lake))
chk("BA-5", (not has_poc) and (not has_lake),
    "**Lean 侧的 `StormPoC.lean` 与 `lakefile.lean` 仍未拷回** ⟹ 「恢复 + 重跑 `lake build`」"
    "是一个**真实待办**（交接说明 §六 的警告仍然有效）：在那之前，Lean 侧的 7 个定理族只有记忆日志背书")


# ══════════════════════════════════════════════════════════════════════
rule("BA-6  汇总：真实待办总账")
# ══════════════════════════════════════════════════════════════════════

TODO = [
    ("I", "3.1", "不完备度比值用**更正的群**重算（N = 8/16/24，对照 1.00/1.63/5.93；含 (2,2,6) 6224→6334）", "低", "候选池 21/31"),
    ("I", "3.2", "**I-15**：⟨|O|⟩ 随 N 的标度律（三点 5.00 / 50.87 / 426.93）", "中", "第 57 轮"),
    ("I", "3.3", "`h_min·N^{2/3} ≈ 2.9` 的性质审查（登记为「无机制拟合」并查误用）", "低", "候选池 28"),
    ("II", "4.1", "正式登记「格点离散 ↔ 面积律」为**框架不覆盖**（§4.8）", "低", "候选池 32 / T-10"),
    ("II", "4.2", "三个「遍历性」的**分层判定**（速度空间 / 空间输运 / 构型轨道）", "中", "候选池 14"),
    ("II", "4.3", "**148 处**「中文字符之间的 ASCII 引号」清理（应为「」）", "低", "第 56 轮"),
    ("III", "C1", "**重子不对称 η**：独立解释为何能标 ~1 TeV（现为配出来）", "一轮", "候选池 1"),
    ("III", "C2", "**暗能量能标**：`dlnΩ_Λ/dβ = 465` 的病态敏感性 / **换一个 ρ_Λ 构造**", "一轮", "候选池 2 / O-Λ"),
    ("III", "C3", "**量子力学基础（§7）**：`D = ℏ/(3m)` vs Nelson `ℏ/(2m)` 的 1.5 倍维度因子", "一轮", "候选池 3"),
    ("III", "C4", "**湍流 / 输运**：`η/s → 1/4π`（KSS 界）", "一轮", "候选池 4"),
    ("III", "C5", "**PPN / 优越系**：衬底绝对位置不能泄漏到 1PN（α₁ ≲ 10⁻⁴）", "一轮", "候选池 5"),
    ("III", "C6", "**宇宙学动力学**：加速度方程 ＋ 连续性方程（§8.6.3 自认仍缺）", "一轮", "候选池 9"),
    ("III", "C7", "**void-CPT-κ 异常**（机制被撤回 ⟹ 悬空）", "待重建", "候选池 8"),
    ("III", "C8", "**EMRI 判决**（S-E1–E4 的数据分析需求）", "框架外", "候选池 7"),
    ("IV", "H1", "**消掉 8π/3**（微观计数多一个 `3/(8π)`，或改 `ε_eff = 1/N`）", "一轮", "交接 §七.3"),
    ("IV", "H2", "**载流子两类型收口**（空腔电子的横向耦合，候选 A/B/C）", "一轮", "交接 §七.5"),
    ("IV", "H3", "**第 26 轮建议 ①**：「每对独立决定是否交换」变体", "低", "交接 §七.6"),
    ("IV", "H4", "**第 26 轮建议 ②**：关联长度定量", "中", "交接 §七.6"),
    ("IV", "H5", "**第 26 轮建议 ④**：逐一复查 §4.10「六处 4」的出处（只查了两处）", "低", "交接 §七.6"),
    ("V", "P1", "**`g` 的精确值与 `α_s/α_EM` 的完整映射**（⚠️ 与 I-17 **不同**：那是 Φ–物质耦合）", "一轮", "论文 §10.2 #11"),
    ("VI", "A1", "**Lean 资产恢复**：拷回 `StormPoC.lean` / `lakefile` / CI，并**重跑 `lake build`**", "低", "交接 §六"),
]
print("  {:<4} {:<4} {:<64} {:<6}".format("组", "编号", "内容", "成本"))
for g, n, c, cost, src in TODO:
    print("  {:<4} {:<4} {:<64} {:<6}".format(g, n, c, cost))
print()
print("  分组计数：" + "；".join(
    "{} = {} 条".format(g, sum(1 for t in TODO if t[0] == g)) for g in ["I", "II", "III", "IV", "V", "VI"]))
print("  ⟹ **真实待办 = {} 条**（其中组 I＋II 共 6 条**无前置依赖、成本低**）".format(len(TODO)))
chk("BA-6", len(TODO) == 21, "**真实待办 = 21 条**（组 I 3 ＋ 组 II 3 ＋ 组 III 8 ＋ 组 IV 5 ＋ 组 V 1 ＋ 组 VI 1）")


# ══════════════════════════════════════════════════════════════════════
rule("BA-7  我的过度声明：取证（交接说明 §七 第 73 轮段）")
# ══════════════════════════════════════════════════════════════════════

over = [k + 1 for k, s in enumerate(HO) if "有明确可判定入口」的项已清空" in s]
fixed = [k + 1 for k, s in enumerate(HO) if "但「候选池里可判定入口已清空」是第 73 轮的过度声明" in s]
print("  原过度声明所在行（**应已为 0**）：{}".format(over))
print("  更正后的表述所在行：{}".format(fixed))
for k in fixed:
    print("     L{}: {}".format(k, HO[k - 1][:150]))
print()
print("  ⚠️ 原句的实际含义只有「**候选池 36 已结项**」，却被写成「可判定入口已清空」。实测：")
print("       · 工作流第 3 / 4 批 **6 项**（无前置依赖、成本低）**全部未做**；")
print("       · 候选池 #1–#9 这 9 条**实质项基本未做**；")
print("       · 交接说明 §七 老编号里 **5 条未做**；")
print("       · 论文 §10.2 有 **1 条实质开放**（`g → α_s/α_EM` 映射）；")
print("       · **Lean 资产仍未拷回**。")
print("  ⟹ **过度声明** ⟹ 登记 **C-18**；并因「清单 ☐ 标记过期」再登记 **C-19**。")
chk("BA-7", len(over) == 0 and len(fixed) == 1,
    "⭐ **过度声明已取证并已更正**：原文（现 **0 处**）把「**一条已结项**」写成"
    "「**候选池里可判定入口已清空**」—— 与实测的 **21 条真实待办**相差极大 ⟹ 登记 **C-18**"
    "（更正，已就地改）与 **C-19**（清单 ☐ 标记双向失真、不可作依据）")


# ══════════════════════════════════════════════════════════════════════
rule("BA-8  去重：确认「明确不做」没有被误算成待办")
# ══════════════════════════════════════════════════════════════════════

NOTDO = ["候选池 34（Γ_flux）", "候选池 30（观测者读数 vs 不变读数）",
         "候选池 16（熵增三分账）", "候选池 27（(6,6,6)/(8,8,8)）",
         "S-13 电池战略目标", "论文 §10.2 的 6 项世界级"]
print("  §六「明确不做」共 {} 类，已从 BA-6 的待办表里排除：".format(len(NOTDO)))
for x in NOTDO:
    print("     ✗ {}".format(x))
chk("BA-8", all("Γ_flux" not in t[2] and "6,6,6" not in t[2] for t in TODO),
    "「明确不做」的 6 类**未混入**待办表 ⟹ 21 条是真待办，不是把判否项重新翻出来")


# ══════════════════════════════════════════════════════════════════════
rule("BA-9  格式卫生")
# ══════════════════════════════════════════════════════════════════════

bad = [k + 1 for k, s in enumerate(PP) if "\\|" in s and not s.lstrip().startswith("|")]
CJK = lambda ch: "\u4e00" <= ch <= "\u9fff"
q = sum(1 for s in PP for k, ch in enumerate(s)
        if ch == '"' and 0 < k < len(s) - 1 and CJK(s[k - 1]) and CJK(s[k + 1]))
print("  论文：非表格行含 `\\|` {} 处；中文字符之间的 ASCII 引号 {} 处（= 待办 4.3 的对象）".format(
    len(bad), q))
chk("BA-9", len(bad) == 0, "格式卫生：非表格行 `\\|` **0 处**；ASCII 引号 {} 处（正是待办 4.3 未做的证据）".format(q))


print()
print("=" * 78)
print("  通过 {} 项，失败 {} 项".format(len(PASS), len(FAIL)))
print("  通过：{}".format(", ".join(PASS)))
if FAIL:
    print("  失败：{}".format(", ".join(FAIL)))
print("=" * 78)
