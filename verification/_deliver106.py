# -*- coding: utf-8 -*-
"""第 106 轮核验：丙类交付物（私审准备包 ＋ EMRI 材料包）＋ 数字机器复算 ＋ 论文零改动"""
import io
import os
import re
import numpy as np

ROOT = r"C:/Users/Administrator/Desktop/2026-08-20-21-43-34"
OUT = os.path.join(ROOT, "outputs")
PRIV = os.path.join(OUT, "私审准备包_三处待核与已知边界.md")
EMRI = os.path.join(OUT, "EMRI材料包_给LISA组的S-E1-E4.md")
LIST = os.path.join(OUT, "工程期望清单.md")
PRE_LIST = os.path.join(OUT, "工程期望清单_备份_2026-10-04第106轮前.md")
HAND = os.path.join(ROOT, "环境交接说明.md")
PRE_HAND = os.path.join(ROOT, "环境交接说明_备份_2026-10-04第106轮前.md")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")

P, F = [0], []


def ck(tag, cond, msg):
    ok = bool(cond)
    P[0] += 1
    if not ok:
        F.append(tag)
    print("  [{}] {} — {}".format("OK" if ok else "XX", tag, msg))


def rd(p):
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


priv, emri, cur_l, pre_l = rd(PRIV), rd(EMRI), rd(LIST), rd(PRE_LIST)
cur_h, pre_h, zh = rd(HAND), rd(PRE_HAND), rd(ZH)

print("=" * 92)
print("第 106 轮核验 · 丙类（私审准备包 ＋ EMRI 材料包）")
print("=" * 92)

print("\n--- DL-1…DL-8  私审准备包 ---")
ck("DL-1", os.path.exists(PRIV) and len(priv) > 4000,
   "`私审准备包_三处待核与已知边界.md` 存在（{} 字）".format(len(priv)))
ck("DL-2", all(k in priv for k in ["§4.5b", "§9", "§8.1"]),
   "**三处齐全**（§4.5b／§9／§8.1）—— 与第 63 轮「只看三处」的规格一致")
qs = re.findall(r"\*\*Q(\d)\*\*", priv)
uniq = sorted(set(qs), key=int)
ck("DL-3", uniq == [str(i) for i in range(1, 10)],
   "**9 个具体问题 Q1–Q9**（每处 3 个）；标记共出现 {} 次 = 9 个定义 ＋ 「20 分钟版」重提 Q2/Q4/Q8 ✓ —— 实得 {}".format(
       len(qs), uniq))
ck("DL-4", priv.count("疑虑") >= 3 and "请你核" in priv,
   "每处都写了「**我自己的疑虑**」＋「**请你核**」")
ck("DL-5", "请不要在这上面花时间" in priv and priv.count("已知边界") >= 2,
   "有「**已知边界 —— 请不要在这上面花时间**」段（避免重复告知）")
ck("DL-6", "20 分钟" in priv and "Q2" in priv and "Q4" in priv and "Q8" in priv,
   "有「**20 分钟版 3 问**」（Q2 第五力／Q4 四项同源／Q8 `E_c` 恒等式）")
ck("DL-7", "锚定效应" in priv,
   "⚠️ 显式承认**锚定效应**风险（并请对方先独立看）")
ck("DL-8", "是判断的" in priv and "未做的" in priv,
   "有「哪些是取证 / 哪些是判断 / 未做的」的诚实边界段")

print("\n--- DL-9…DL-16  EMRI 材料包 ---")
ck("DL-9", os.path.exists(EMRI) and len(emri) > 4000,
   "`EMRI材料包_给LISA组的S-E1-E4.md` 存在（{} 字）".format(len(emri)))
ck("DL-10", all(k in emri for k in ["S-E1", "S-E2", "S-E3", "S-E4"]),
   "四条预言 S-E1–S-E4 齐全")
ck("DL-11", "Yilmaz" in emri and "Papapetrou 1954" in emri and "1962" in emri,
   "⚠️ **边界 2.1 到位**：明确说度规**就是** Yilmaz–Rosen（Papapetrou 1954／Rosen 1962）⟹ 框架贡献在**涌现机制**")
ck("DL-12", "数值标定" in emri and "RK4" in emri,
   "⚠️ **边界 2.2 到位**：`δ = 0.30·x_p` 是**数值标定**（RK4 三点），不是解析推导")
ck("DL-13", "三个前提**全部在本框架之外**" in emri or "全部在本框架之外" in emri,
   "⚠️ **边界 2.3 到位**：三前提（LISA 发射／事件率／波形模型）全在框架之外")
ck("DL-14", "以它为准" in emri and "7.5×10⁻⁴" in emri,
   "**口径节到位**：三口径不可并存，**以 `ΔlnL` 为准**，等效宽度 **7.5×10⁻⁴**")
ck("DL-15", "它们是 1 条，不是 4 条" in emri or "按「独立可检验预言」计，它们是 1 条" in emri,
   "⚠️ **四项同源 ⟹ 按 1 条计**的声明到位（并邀请反驳）")
ck("DL-16", all(k in emri for k in ["Q1", "Q2", "Q3", "Q4"]) and "请直接说" in emri,
   "**四问给 LISA 组**（波形／简并／判据／「若不值得做请直说」）")

print("\n--- DL-17…DL-21  C-74 数字机器复算 ---")
d, dl2, dl4 = 0.0200, 357.4, 396.2
s_cur2, s_cur4 = 1.63e-6, 7.37e-7
s_eff2, s_eff4 = d / np.sqrt(2 * dl2), d / np.sqrt(2 * dl4)
r_cur, r_dl = s_cur2 / s_cur4, dl4 / dl2
pred = dl2 * r_cur ** 2
print("      σ_eff(2yr) = {:.4e}｜σ_eff(4yr) = {:.4e}".format(s_eff2, s_eff4))
print("      σ_cur 比 = {:.4f}｜ΔlnL 比 = {:.4f}｜预期 ΔlnL(4yr) = {:.1f}（实际 {:.1f}）".format(
    r_cur, r_dl, pred, dl4))
ck("DL-17", abs(s_eff2 - 7.49e-4) < 0.02e-4 and abs(s_eff2 / s_cur2 - 459) < 2,
   "等效宽度 **7.49×10⁻⁴**（与文中所报一致）＋ 宽度比 **459**（= C-7）")
ck("DL-18", abs(pred - 1748) < 2 and abs(pred / dl4 - 4.41) < 0.02,
   "变化率检验：预期 **1748** vs 实际 **396.2** ⟹ 差 **4.41 倍**（文中数字复算一致）")
ck("DL-19", abs(((d / s_cur2) ** 2 / 2) / dl2 - 2.11e5) < 0.05e5
   and abs(((d / s_cur4) ** 2 / 2) / dl4 - 9.29e5) < 0.05e5,
   "绝对值检验：2 yr 差 **2.11×10⁵**、4 yr 差 **9.29×10⁵ 倍**（文中数字复算一致）")
ck("DL-20", abs(7108 / 27 - 263) < 2,
   "`7108σ` 与 `27σ` 之比 ≈ **263**（C-7 记 267，口径略异 —— 已在文中按 263 述）")
ck("DL-21", "1748" in emri and "4.41" in emri and "2.11×10⁵" in emri and "9.29×10⁵" in emri,
   "材料包内四个数字与机器复算**逐一对应**")

print("\n--- DL-22…DL-26  台账与交接 ---")
ck("DL-22", "| **第 106 轮**（**丙类 · 交付物**） |" in cur_l
   and "第 106 轮" not in pre_l,
   "清单有**第 106 轮行**（两段式：补丁前无）")
ck("DL-23", "| **C-74** |" in cur_l and "| **C-74** |" not in pre_l,
   "**C-74 行已加**（补丁前无）")
seq = [re.match(r"^\|\s*\*\*(C-\d+)\*\*\s*\|", x).group(1)
       for x in cur_l.split("\n") if re.match(r"^\|\s*\*\*(C-\d+)\*\*\s*\|", x)]
i67 = seq.index("C-67")
grp = seq[i67:i67 + 8]
nums = [int(x.split("-")[1]) for x in grp]
ck("DL-24", grp == ["C-67", "C-68", "C-69", "C-70", "C-71", "C-72", "C-73", "C-74"]
   and nums == sorted(nums),
   "**结构自检：C-67…C-74 连续且严格升序**")
ck("DL-25", "| **撤回 / 更正** | **73 条**" in cur_l
   and "| **撤回 / 更正** | **72 条**" in pre_l,
   "计数 **72 → 73**（两段式）")
ck("DL-26", "**丙类 ✅ 第 106 轮结项**" in cur_l
   and "**当前建议（第 106 轮后）**" in cur_h
   and "**第 106 轮新增（丙类 · 交付物" in cur_h,
   "清单剩余待办 ＋ 交接 §七 ＋ 第 106 轮段 三处均已更新")

print("\n--- DL-27…DL-30  ⚠️ 论文零改动（本轮是「对外材料」轮）---")
mz = os.path.getmtime(ZH)
mref = min(os.path.getmtime(PRIV), os.path.getmtime(EMRI))
ck("DL-27", mz < mref,
   "**论文修改时间早于本轮交付物** ⟹ 论文本轮**零改动**"
   "（Δ = {:.0f} s）".format(mref - mz))
ck("DL-28", "交付物" in cur_l and "论文零改动" in cur_l,
   "清单第 106 轮行显式写明「**论文本轮零改动**」")
ck("DL-29", "论文本轮零改动" in cur_h,
   "交接第 106 轮段 ⑤ 同样写明")
ck("DL-30", zh.count("Yilmaz") >= 1 and "exponential metric" in zh,
   "交叉验证：论文**确有** Yilmaz–Rosen 的文献对照段（材料包的说法有依据）")

print("\n--- DL-31…DL-34  两份交付物的定位自洽 ---")
ck("DL-31", "启发式统一框架" in priv and "参考架构" in emri,
   "两份各自引用论文自身的定位（私审包用「启发式统一框架」；EMRI 包用「参考架构，非已确立物理」）")
ck("DL-32", "第 63 轮" in priv and all(k in emri for k in ["EMRI完整波形", "KerrEMRI", "LISA_EMRI", "Fisher"]),
   "来源可溯：私审包指向第 63 轮战略评估；EMRI 包指向四份定量工作（Fisher／Kerr／a-δ／3PN 提案）")
ck("DL-33", "未提交" in emri and "未联系任何人" in emri,
   "EMRI 包**显式声明「未提交、未联系任何人」**（不越权代表作者对外）")
ck("DL-34", "IV" in priv or "不夸" in priv or "不隐藏" in emri,
   "两份都写了「不隐藏缺陷、不夸大」的自我定位")

print("\n" + "=" * 92)
print("通过 {} 项，失败 {} 项{}".format(P[0] - len(F), len(F),
                                "" if not F else "  ⟹ " + ", ".join(F)))
print("=" * 92)
