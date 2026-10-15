# -*- coding: utf-8 -*-
"""第 108 轮 · 第三轮（收紧规则）：8-20 ~ 9-19「待选清单」完成度核查

⚠️ 修正记录：上一版用**整组关键词**匹配交付物文件名 ⟹ 泛词污染
   （`EMRI` 让 D1–D5 全变"有交付物"；`饱和` 让 A1 匹配到不相干文件）。
   本版改为每个线程给一组**专用文件名关键词**（`file_keys`），且**必须命中**才算交付物。

四态（优先级从上到下）：
   ⛔ 判否       —— 清单 C-/N- 行或 MEMORY 已判死对**该线程专用词**有命中
   ✅ 已执行     —— ① 交付物文件名命中 file_keys；或 ② B 期日志里该线程行含「完成/闭环/关闭/✅」
   🔁 后续推进   —— 后期日志 ≥3 次命中，或台账 ≥5 次
   ⏳ 悬空       —— 都不满足
   ※ 「✅ + ⛔」同时成立者单列 `✅→⛔`（执行过但结论被后续修正/撤回）
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

LIST = io.open(os.path.join(ROOT, "outputs", "工程期望清单.md"), encoding="utf-8", errors="replace").read()
HAND = io.open(os.path.join(ROOT, "环境交接说明.md"), encoding="utf-8", errors="replace").read()
MEM = io.open(os.path.join(MD, "MEMORY.md"), encoding="utf-8", errors="replace").read()
TAI = LIST + HAND

fname_pool = []
for d in (OUTD, NOTES):
    if os.path.isdir(d):
        fname_pool += [f for f in os.listdir(d)]

dead_lines = [ln for ln in LIST.split("\n") if re.match(r"^\|\s*\*\*(C-\d+|N-\d+)\*\*", ln)]
DEAD = "\n".join(dead_lines) + "\n" + MEM

DONE_MARK = ["完成", "闭环", "关闭", "收官", "✅", "已解决", "定案", "结项"]

# (编号, 名称, 全期关键词, 交付物文件名关键词)
T = [
 ("A1", "通量饱和机制", ["通量饱和", "饱和机制", "饱和强场"], ["饱和"]),
 ("A2", "强场度规裁决", ["强场分叉", "强场度规", "强场预言", "强场机制", "强场"], ["强场"]),
 ("A3", "与 GR 对接", ["与 GR 对接", "GR 对接", "强场由 Einstein"], []),
 ("A4", "压强临界面积锁定", ["压强临界面积", "临界面积"], ["临界面积"]),
 ("A5", "过载区径向分布与辐射传输", ["过载区径向", "辐射传输", "过载区密度"], ["过载", "辐射传输"]),
 ("A6", "吸积盘辐射传输", ["吸积盘"], ["吸积"]),
 ("A7", "钳制物态微观推导", ["钳制物态", "钳制"], ["钳制"]),
 ("A8", "更高阶 PPN（2PN/3PN）", ["更高阶 PPN", "2PN", "3PN", "高阶PPN", "PPN"], ["PPN", "ppn"]),
 ("A9", "非热修正观测提案", ["非热修正"], ["非热"]),
 ("A10", "火墙厚度判定", ["火墙"], ["火墙"]),
 ("A11", "1/r 稳态与弱场 g₀₀ 对齐", ["1/r 稳态", "g₀₀ 系数", "g00系数"], ["稳态"]),
 ("A12", "扩散方程严格解", ["扩散方程严格解", "有限 R 严格解", "3D 球对称扩散", "球对称扩散"], ["扩散"]),
 ("A13", "涡心失效区域尺寸", ["涡心失效", "涡心", "孤子"], ["涡心", "孤子"]),
 ("A14", "毛球拓扑 ⟹ ε 下界", ["毛球"], ["毛球"]),
 ("A15", "初始微扰来源", ["初始微扰", "微扰来源"], ["微扰"]),
 ("A16", "内空间编码动力学证明", ["内空间编码", "内空间"], ["内空间"]),
 ("A17", "现在平面选择的动力学来源", ["现在平面"], ["现在平面"]),
 ("A18", "观测者模型与全息集中对接", ["观测者模型", "全息集中"], ["观测者", "全息"]),
 ("A19", "k=4 严格证明", ["k=4 严格", "k=4 动力学"], ["k的动力学", "k动力学", "k_dyn", "k等于"]),
 ("A20", "挂谷 packing ⟹ 1/4", ["packing", "挂谷"], ["packing", "挂谷", "1_4", "1/4"]),
 ("A21", "A 定理包整合进论文", ["定理包整合", "A 定理包"], ["定理包"]),
 ("A22", "α 微观来源", ["α 微观", "α的微观"], ["α微观", "alpha"]),
 ("A23", "普朗克常数物理身份", ["普朗克常数物理身份"], []),
 ("B1", "2D YM σ 的 N1–N4", ["N1 2D YM", "N2 强耦合", "N3 σ", "N4 弦断裂"], ["弦网", "YM", "σ"]),
 ("B2", "量子双代数定理包", ["双代数"], ["双代数"]),
 ("B3", "J/K 耦合强度推导", ["J/K", "JK 耦合", "JK耦合"], ["JK", "JK耦合"]),
 ("B4", "ε 项拓扑序 ⟹ 禁闭", ["禁闭转变", "ε 项拓扑序", "拓扑序→禁闭"], ["禁闭", "拓扑序"]),
 ("B5", "3+1D 弦网严格化", ["弦网严格化", "弦网 λc", "弦网λc"], ["弦网"]),
 ("B6", "4D 自旋 2 涌现", ["自旋 2", "自旋2", "spin-2"], ["自旋2", "自旋 2", "spin2"]),
 ("B7", "4D 质量隙", ["质量隙"], ["质量隙"]),
 ("B8", "Z₂→U(1) RG 严格化", ["RG 严格化", "Wilson RG"], ["Z2U1", "RG"]),
 ("B9", "λ_c(∞) / κ_c 标度", ["λ_c", "λc", "κ_c", "κc", "P0-3"], ["λc", "κ", "相变"]),
 ("C1", "英文翻译 / arXiv 投稿", ["英文翻译", "arXiv 投稿"], ["英文", "EN", "Paper_"]),
 ("C2", "参考文献补全", ["参考文献"], ["参考文献", "refs"]),
 ("C3", "投稿行政（CSO）", ["CSO", "投稿行政"], ["CSO", "cso"]),
 ("D1", "EMRI 波形模板与 Fisher", ["Fisher"], ["Fisher"]),
 ("D2", "Kerr EMRI 波形与贝叶斯", ["Kerr EMRI", "Teukolsky"], ["Kerr"]),
 ("D3", "a-δ 联合 MCMC", ["a-δ 联合", "联合贝叶斯", "联合 MCMC"], ["a-δ", "a_δ"]),
 ("D4", "EMRI κ↔Γ 1/3 映射", ["κ↔Γ", "轨道平均 s_p"], []),
 ("D5", "LISA EMRI 3PN 提案", ["3PN 提案", "LISA EMRI"], ["EMRI", "3PN", "LISA"]),
 ("E1", "开放问题地图 A1–A4", ["开放问题地图"], []),
 ("F1", "新框架缺陷 6 条", ["verify.py", "亚普朗克", "洛伦兹标量"], ["并轨", "MAPS"]),
 ("F2", "镜像支 B− / 分支 A-B", ["镜像支", "分支 A", "分支 B"], ["镜像支", "并轨"]),
 ("G1", "Friedmann / 动力学缺口", ["Friedmann", "动力学缺口", "加速度方程"], ["Friedmann", "动力学", "宇宙学", "状态方程"]),
 ("G2", "Ω_Λ 23.76 / O-Λ", ["23.76", "Ω_Λ", "O-Λ"], ["Ω", "暗能量", "Lambda", "Λ"]),
 ("G3", "E_c 能标锁定", ["E_c", "E_c 锁定"], []),
 ("G4", "λ 统一为操作式", ["操作式"], []),
 ("G5", "ln2 缺口", ["ln2", "11.0904"], ["单位", "熵", "ln2"]),
 ("G6", "多种子 / 3D 硬球", ["多种子", "硬球"], ["硬球", "BBGKY", "a2_"]),
 ("G7", "方向状态数 4 vs 6", ["4 还是 6", "方向状态数", "状态数复查"], []),
 ("G8", "C-b/C-c 跨层判定", ["跨层判定", "跨层"], []),
 ("G9", "底层四状态机制", ["底层四状态", "四状态"], []),
 ("G10", "Lean 资产 / mathlib", ["lake build", "olean", "StormPoC", "mathlib"], ["lean", "Lean", "StormPoC"]),
 ("G11", "ε(E) 的组分比例", ["组分比例", "ε(E)"], ["组分", "A2"]),
]


def hit(t, kws):
    return sum(t.count(k) for k in kws)


rows = []
for tid, name, kws, fk in T:
    b = hit("\n".join(logs[d] for d in BD), kws)
    bd = [d for d in BD if hit(logs[d], kws)]
    l = hit(LATER, kws)
    ta = hit(TAI, kws)
    d = hit(DEAD, kws)
    files = sorted({f for f in fname_pool if any(k in f for k in fk)})
    # B 期「完成句」
    done_ln = []
    for dt in BD:
        for ln in logs[dt].split("\n"):
            if hit(ln, kws) and any(m in ln for m in DONE_MARK):
                done_ln.append((dt, re.sub(r"\s+", " ", ln.strip())[:120]))
    has_deliv = len(files) > 0
    has_done = len(done_ln) > 0
    executed = has_deliv or has_done
    neg = d >= 1
    if executed and neg:
        st = "✅→⛔"
    elif executed:
        st = "✅ 已执行"
    elif l >= 3 or ta >= 5:
        st = "🔁 后续推进"
    elif neg:
        st = "⛔ 已判否"
    else:
        st = "⏳ 悬空"
    rows.append(dict(tid=tid, name=name, b=b, first=(bd[0][5:] if bd else "—"), last=(bd[-1][5:] if bd else "—"),
                     l=l, ta=ta, d=d, files=files, st=st, done=done_ln))

order = {"✅ 已执行": 0, "✅→⛔": 1, "🔁 后续推进": 2, "⛔ 已判否": 3, "⏳ 悬空": 4}
rows.sort(key=lambda r: (order[r["st"]], r["tid"]))

out = []
A = out.append
A("=" * 120)
A("第 108 轮 · 8-20 ~ 9-19「待选清单」完成度核查（收紧规则 · 五态）")
A("=" * 120)
A("B 期 = 08-20…09-19（17 天，只有日志）｜后期 = 09-20…10-04（13 天）")
A("判据：交付物文件名必须命中**专用词**；或 B 期日志里该线程行含「完成/闭环/关闭/✅」")
A("")
A("{:<5} {:<30} {:>4} {:>11} {:>4} {:>4} {:>3} {:>3}  {}".format(
    "编号", "线程", "B期", "区间", "后期", "台账", "判否", "交付", "状态"))
A("-" * 120)
for r in rows:
    A("{:<5} {:<30} {:>4} {:>11} {:>4} {:>4} {:>3} {:>3}  {}".format(
        r["tid"], r["name"][:28], r["b"], r["first"] + "~" + r["last"], r["l"], r["ta"],
        r["d"], len(r["files"]), r["st"]))
A("")
A("=" * 120)
A("证据明细")
A("=" * 120)
for r in rows:
    A("")
    A("【{}】{}   {}".format(r["tid"], r["name"], r["st"]))
    if r["files"]:
        A("    交付物：{}".format(" ｜ ".join(r["files"][:5])))
    if r["done"]:
        for dt, ln in r["done"][:2]:
            A("    B期完成句 [{}]：{}".format(dt[5:], ln))
    A("    命中：B期 {}｜后期 {}｜台账 {}｜判否语料 {}".format(r["b"], r["l"], r["ta"], r["d"]))
A("")
A("=" * 120)
A("汇总")
A("=" * 120)
for st in ["✅ 已执行", "✅→⛔", "🔁 后续推进", "⛔ 已判否", "⏳ 悬空"]:
    ids = [r["tid"] for r in rows if r["st"] == st]
    A("  {:<12} {:>2} 条   {}".format(st, len(ids), "  ".join(ids)))

io.open(os.path.join(OUTD, "_ledger108d_out.txt"), "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out[:1] + out[3:72]))
print()
print("⟹ 已写 outputs/_ledger108d_out.txt（{} 行）".format(len(out)))
