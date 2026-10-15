# -*- coding: utf-8 -*-
"""第 108 轮 · 第二轮：给 54 条线程补「交付物」一列，并给出四态判定。

判定的四条规则（写死在代码里，便于复核）：
  ⛔ 已判否      —— 该主题在清单的「撤回/更正(C-xx)」「负面边界(N-xx)」「已判死」区有记录
  ✅ 已执行      —— outputs/ 或 notes/ 下存在**文件名含该线程关键词**的交付物
  🔁 已并入后续  —— 后期日志（9-20~10-04）有 ≥3 次命中，或台账有 ≥5 次命中
  ⏳ 悬空        —— 以上都不满足（B 期提过，之后既无交付物也无人再提）
"""
import io
import os
import re

ROOT = r"C:\Users\Administrator\Desktop\2026-08-20-21-43-34"
MD = os.path.join(ROOT, ".workbuddy", "memory")
OUTD = os.path.join(ROOT, "outputs")
NOTES = os.path.join(ROOT, "MAPS-Unified-Framework", "notes", "推演专题")

logs = {fn[:10]: io.open(os.path.join(MD, fn), encoding="utf-8", errors="replace").read()
        for fn in sorted(os.listdir(MD)) if re.match(r"^2026-\d\d-\d\d\.md$", fn)}
BD = [d for d in sorted(logs) if d <= "2026-09-19"]
LD = [d for d in sorted(logs) if d > "2026-09-19"]
LATER = "\n".join(logs[d] for d in LD)
BEARLY = "\n".join(logs[d] for d in BD)

LIST = io.open(os.path.join(ROOT, "outputs", "工程期望清单.md"), encoding="utf-8", errors="replace").read()
HAND = io.open(os.path.join(ROOT, "环境交接说明.md"), encoding="utf-8", errors="replace").read()
MEM = io.open(os.path.join(MD, "MEMORY.md"), encoding="utf-8", errors="replace").read()

# 交付物文件名池（outputs + notes/推演专题 + docs/html）
fname_pool = []
for d in (OUTD, NOTES):
    if os.path.isdir(d):
        for f in os.listdir(d):
            fname_pool.append(f)
FN = "\n".join(fname_pool)

# 「已判否」语料：清单里 撤回/更正 与 负面边界 的全部行 + MEMORY 的已判死清单
dead_lines = [ln for ln in LIST.split("\n") if re.match(r"^\|\s*\*\*(C-\d+|N-\d+)\*\*", ln)]
DEAD = "\n".join(dead_lines) + "\n" + MEM

THREADS = [
    ("A1", "通量饱和机制（决定强场存亡）", ["饱和"]),
    ("A2", "强场度规裁决（分叉/两条路径）", ["强场"]),
    ("A3", "与 GR 对接（弱场框架·强场 GR）", ["GR 对接", "有效理论"]),
    ("A4", "压强临界面积锁定机制", ["临界面积"]),
    ("A5", "过载区径向密度分布与辐射传输", ["过载区", "辐射传输"]),
    ("A6", "吸积盘辐射传输", ["吸积盘"]),
    ("A7", "钳制物态微观推导", ["钳制"]),
    ("A8", "更高阶 PPN（2PN/3PN）", ["PPN"]),
    ("A9", "非热修正观测提案", ["非热"]),
    ("A10", "火墙厚度判定", ["火墙"]),
    ("A11", "1/r 稳态与弱场 g₀₀ 系数对齐", ["稳态"]),
    ("A12", "扩散方程严格解（有限 R/3D 球对称）", ["扩散"]),
    ("A13", "涡心失效区域严格尺寸", ["涡心", "涡"]),
    ("A14", "毛球拓扑 ⟹ ε 下界定量", ["毛球"]),
    ("A15", "初始微扰来源", ["微扰"]),
    ("A16", "内空间编码优先性动力学证明", ["内空间"]),
    ("A17", "现在平面选择的动力学来源", ["现在平面"]),
    ("A18", "观测者模型与全息集中严格对接", ["观测者", "全息"]),
    ("A19", "k=4 严格证明", ["k=4", "k动力学", "k_dyn"]),
    ("A20", "挂谷 packing ⟹ 1/4 严格推导", ["packing", "挂谷"]),
    ("A21", "A 定理包整合进论文", ["定理包"]),
    ("A22", "α 微观来源", ["α微观", "alpha"]),
    ("A23", "普朗克常数物理身份", ["普朗克"]),
    ("B1", "2D YM σ 的 N1–N4 四项", ["YM", "σ_E", "σ_m", "弦网λc"]),
    ("B2", "量子双代数定理包（阶段 A）", ["双代数"]),
    ("B3", "J/K 耦合强度第一性推导", ["JK", "J_K", "JK耦合"]),
    ("B4", "ε 项拓扑序 ⟹ 禁闭转变", ["禁闭", "拓扑序"]),
    ("B5", "3+1D 弦网严格化（连续极限/麦克斯韦谱）", ["弦网", "麦克斯韦", "U(1)连续"]),
    ("B6", "4D 自旋 2 涌现", ["自旋2", "自旋 2", "spin2"]),
    ("B7", "4D 质量隙（千禧年）", ["质量隙", "mass gap"]),
    ("B8", "Z₂→U(1) RG 严格化", ["RG 严格", "Z2U1", "Wilson"]),
    ("B9", "λ_c(∞) / κ_c 有限尺寸标度（P0-3）", ["λc", "λ_c", "相变", "κ_c"]),
    ("C1", "英文翻译 / arXiv 投稿准备", ["EN", "arXiv", "英文", "翻译"]),
    ("C2", "参考文献补全 30→50+", ["参考文献", "refs"]),
    ("C3", "投稿行政（CSO）", ["CSO", "cso"]),
    ("D1", "EMRI 波形模板与 Fisher 精度", ["EMRI", "Fisher"]),
    ("D2", "Kerr EMRI 波形与贝叶斯", ["Kerr", "EMRI"]),
    ("D3", "a-δ 联合 MCMC", ["EMRI", "a-δ"]),
    ("D4", "EMRI κ↔Γ 1/3 精确映射", ["EMRI", "κ"]),
    ("D5", "LISA EMRI 3PN 提案", ["EMRI", "LISA", "3PN"]),
    ("E1", "开放问题地图 A1–A4", ["开放问题"]),
    ("F1", "新框架缺陷 6 条（verify.py 等）", ["MAPS", "并轨"]),
    ("F2", "镜像支 B− 回归 / 分支 A-B", ["镜像支", "分支"]),
    ("G1", "Friedmann 缺口 / 动力学缺口", ["Friedmann", "动力学", "宇宙学"]),
    ("G2", "Ω_Λ 23.76 缺口 / O-Λ", ["ΩΛ", "Ω_Λ", "暗能量", "Λ"]),
    ("G3", "E_c 能标锁定", ["E_c", "E_c", "能标", "meV"]),
    ("G4", "λ 统一为操作式", ["λ 统一", "操作式", "λ统一"]),
    ("G5", "ln2 缺口", ["ln2", "单位", "熵"]),
    ("G6", "多种子 / 3D 硬球未做", ["硬球", "B2", "多种子"]),
    ("G7", "方向状态数 4 vs 6", ["状态数", "方向数", "16"]),
    ("G8", "C-b/C-c 跨层判定", ["跨层", "C-b", "C-c"]),
    ("G9", "底层四状态机制", ["四状态", "状态"]),
    ("G10", "Lean 资产 / mathlib 构建", ["Lean", "lean", "StormPoC", "mathlib", "A1"]),
    ("G11", "能标依赖 ε(E) 的组分比例", ["ε(E)", "A2", "组分"]),
]


def hits(t, kws):
    return sum(t.count(k) for k in kws)


rows = []
for tid, name, kws in THREADS:
    b = hits(BEARLY, kws)
    bdates = [d for d in BD if hits(logs[d], kws)]
    l = hits(LATER, kws)
    t = hits(LIST + HAND, kws)
    f = [fn for fn in fname_pool if any(k in fn for k in kws)]
    dl = hits(DEAD, kws)
    # 判定
    if dl >= 1 and "已判" in DEAD[:0] + "":
        pass
    if len(f) >= 1:
        state = "✅ 有交付物"
    elif l >= 3 or t >= 5:
        state = "🔁 已并入后续"
    elif dl >= 1:
        state = "⛔ 已判否/已登记结论"
    else:
        state = "⏳ 悬空（无交付物、后期无提）"
    rows.append(dict(tid=tid, name=name, b=b, first=(bdates[0][5:] if bdates else "—"),
                     last=(bdates[-1][5:] if bdates else "—"), l=l, t=t,
                     files=f[:4], nf=len(f), state=state, dl=dl))

order = {"✅ 有交付物": 0, "🔁 已并入后续": 1, "⛔ 已判否/已登记结论": 2, "⏳ 悬空（无交付物、后期无提）": 3}
rows.sort(key=lambda r: (order[r["state"]], r["tid"]))

out = []
out.append("=" * 118)
out.append("第 108 轮 · 8-20 ~ 9-19「待选清单」完成度核查（线程级 · 四态）")
out.append("=" * 118)
out.append("B 期 = 2026-08-20…09-19（17 天，只有日志）｜后期 = 2026-09-20…10-04（13 天，有对话原文）")
out.append("")
out.append("{:<5} {:<34} {:>5} {:>6} {:>5} {:>5} {:>4}  {}".format(
    "编号", "线程", "B期", "区间", "后期", "台账", "交付", "状态"))
out.append("-" * 118)
for r in rows:
    out.append("{:<5} {:<34} {:>5} {:>6} {:>5} {:>5} {:>4}  {}".format(
        r["tid"], r["name"][:32], r["b"], r["first"] + "~" + r["last"],
        r["l"], r["t"], r["nf"], r["state"]))
out.append("")
out.append("=" * 118)
out.append("交付物明细（文件名含该线程关键词）")
out.append("=" * 118)
for r in rows:
    if r["files"]:
        out.append("  {:<5} {:<30} → {}".format(r["tid"], r["name"][:28], " ｜ ".join(r["files"])))

out.append("")
out.append("=" * 118)
out.append("按状态汇总")
out.append("=" * 118)
for st in ["✅ 有交付物", "🔁 已并入后续", "⛔ 已判否/已登记结论", "⏳ 悬空（无交付物、后期无提）"]:
    ids = [r["tid"] for r in rows if r["state"] == st]
    out.append("  {:<28} {:>2} 条： {}".format(st, len(ids), "  ".join(ids)))

io.open(os.path.join(OUTD, "_ledger108c_out.txt"), "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out[:70]))
print()
print("⟹ 已写 outputs/_ledger108c_out.txt")
