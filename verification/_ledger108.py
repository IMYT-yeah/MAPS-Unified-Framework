# -*- coding: utf-8 -*-
"""第 108 轮：8-20 ~ 9-19「待选清单」完成度核查

做三件事：
  ① 从 8-20 ~ 9-19 的日志里抽出「下一步候选 / 待办 / 遗留 / 未完成 / 开放问题」条目；
  ② 把这些条目归并为「线程」（thread），每个线程给一组判别关键词；
  ③ 对每条线程做三段取证：
       S1 源头（8-20~9-19 日志：首次/末次出现 + 命中数）
       S2 后续推进（9-20 ~ 10-04 日志：命中数 + 片段）
       S3 判决台账（工程期望清单 / MEMORY / 交接说明：命中数 + 片段）
     ⟹ 再由人（不是脚本）做状态判定。

⚠️ 本脚本**只做取证与归并**，不做自动判定 —— 判定写在备忘录里，理由逐条给出。
"""
import io
import os
import re

ROOT = r"C:\Users\Administrator\Desktop\2026-08-20-21-43-34"
MD = os.path.join(ROOT, ".workbuddy", "memory")
LIST = os.path.join(ROOT, "outputs", "工程期望清单.md")
HAND = os.path.join(ROOT, "环境交接说明.md")


def rd(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


# ---------------------------------------------------------------- 全部日志
logs = {}
for fn in sorted(os.listdir(MD)):
    if re.match(r"^2026-\d\d-\d\d\.md$", fn):
        logs[fn[:10]] = rd(os.path.join(MD, fn))
DATES = sorted(logs)
B_DATES = [d for d in DATES if d <= "2026-09-19"]          # B 期：只有日志
L_DATES = [d for d in DATES if d > "2026-09-19"]           # 有对话原文的时期
print("日志覆盖：B 期 {} 天（{}…{}）｜后期 {} 天（{}…{}）".format(
    len(B_DATES), B_DATES[0], B_DATES[-1], len(L_DATES), L_DATES[0], L_DATES[-1]))

# ---------------------------------------------------------------- 抽取条目
MARK = ["待办", "未完成", "尚未", "未做", "开放问题", "下一步", "剩余", "缺口",
        "TODO", "☐", "待定", "留给后续", "后续工作", "未解决", "待验证", "待严格"]
CAND = re.compile(r"(下一步候选|下一步|待办|遗留|剩余|未完成|开放问题|缺口|收尾待办)")

raw = []       # (date, lineno, text, [items])
for d in B_DATES:
    for i, ln in enumerate(logs[d].split("\n"), 1):
        if any(m in ln for m in MARK) and CAND.search(ln):
            body = re.sub(r"^[\-\*\s>*#]+", "", ln.strip())
            body = re.sub(r"^\*\*|\*\*$", "", body)
            parts = re.split(r"[①②③④⑤⑥⑦⑧⑨⑩]|；\s*(?=[A-Zα-ωa-z\u4e00-\u9fff])", body)
            items = [p.strip(" 　*：:。;；") for p in parts if len(p.strip()) > 5]
            raw.append((d, i, ln.strip(), items))
n_items = sum(len(r[3]) for r in raw)
print("抽出候选行 {} 条；切成条目 {} 条".format(len(raw), n_items))

# ---------------------------------------------------------------- 线程表
# (编号, 名称, 关键词组) —— 关键词组内任一命中即算；要求词足够特异
THREADS = [
    # ── A 引力侧（8-20 ~ 8-23）
    ("A1", "通量饱和机制（决定强场存亡）", ["通量饱和", "饱和机制", "通量过载", "过载区流体"]),
    ("A2", "强场度规裁决（分叉/两条路径）", ["强场分叉", "强场度规", "强场预言", "强场存亡", "强场机制"]),
    ("A3", "与 GR 对接（弱场框架·强场 GR）", ["与 GR 对接", "GR 对接", "强场由 Einstein", "有效理论接管"]),
    ("A4", "压强临界面积锁定机制", ["压强临界面积", "临界面积锁定"]),
    ("A5", "过载区径向密度分布与辐射传输", ["过载区径向", "径向密度分布", "辐射传输"]),
    ("A6", "吸积盘辐射传输", ["吸积盘"]),
    ("A7", "钳制物态微观推导（饱和模态=视界）", ["钳制物态", "饱和模态", "视界几何"]),
    ("A8", "更高阶 PPN（2PN/3PN）", ["更高阶 PPN", "2PN", "3PN", "β_ppn", "高阶PPN"]),
    ("A9", "非热修正观测提案", ["非热修正"]),
    ("A10", "火墙厚度判定", ["火墙"]),
    ("A11", "1/r 稳态与弱场 g₀₀ 系数对齐", ["1/r 稳态", "g₀₀ 系数对齐", "g00系数"]),
    ("A12", "扩散方程严格解（有限 R/3D 球对称）", ["扩散方程严格解", "有限 R 严格解", "3D 球对称扩散", "球对称扩散精确解"]),
    ("A13", "涡心失效区域严格尺寸", ["涡心失效"]),
    ("A14", "毛球拓扑 ⟹ ε 下界定量", ["毛球"]),
    ("A15", "初始微扰来源（与 ε 泄漏衔接）", ["初始微扰"]),
    ("A16", "内空间编码优先性动力学证明", ["内空间编码"]),
    ("A17", "现在平面选择的动力学来源", ["现在平面", "B4'", "B4′"]),
    ("A18", "观测者模型与全息集中严格对接", ["观测者模型", "全息集中"]),
    ("A19", "k=4 严格证明（最后一门）", ["k=4 严格", "k=4 动力学", "k=4"]),
    ("A20", "挂谷 packing ⟹ 1/4 严格推导", ["packing", "挂谷"]),
    ("A21", "A 定理包整合进论文 §4.3", ["定理包整合", "A 定理包"]),
    ("A22", "α 微观来源", ["α 微观", "α 来源"]),
    ("A23", "普朗克常数物理身份", ["普朗克常数物理身份", "普朗克常数"]),
    # ── B 规范侧 / 弦网（8-23 ~ 8-30）
    ("B1", "2D YM σ 的 N1–N4 四项", ["N1 2D YM", "N2 强耦合", "N3 σ(β)", "N4 弦断裂", "YM σ"]),
    ("B2", "量子双代数定理包（阶段 A）", ["双代数", "量子双代数"]),
    ("B3", "J/K 耦合强度第一性推导", ["J/K", "JK 耦合", "J/K 耦合"]),
    ("B4", "ε 项拓扑序 ⟹ 禁闭转变", ["禁闭转变", "拓扑序→禁闭", "ε 项拓扑序"]),
    ("B5", "3+1D 弦网严格化（连续极限/麦克斯韦谱）", ["弦网严格化", "连续极限", "麦克斯韦谱"]),
    ("B6", "4D 自旋 2 涌现", ["自旋 2", "自旋2"]),
    ("B7", "4D 质量隙（千禧年）", ["质量隙"]),
    ("B8", "Z₂→U(1) RG 严格化", ["RG 严格化", "Wilson RG", "Z₂→U(1)", "Z2→U(1)"]),
    ("B9", "λ_c(∞) 有限尺寸标度（P0-3）", ["λ_c", "λc", "κ_c", "κc"]),
    # ── C 论文 / 发表
    ("C1", "英文翻译 / arXiv 投稿准备", ["英文翻译", "arXiv", "英文版"]),
    ("C2", "参考文献补全 30→50+", ["参考文献"]),
    ("C3", "发表版重组 v2.1 / 投稿行政（CSO）", ["发表版重组", "CSO", "投稿"]),
    # ── D EMRI
    ("D1", "EMRI 波形模板与 Fisher 精度", ["Fisher"]),
    ("D2", "Kerr EMRI 波形与贝叶斯", ["Kerr EMRI", "Teukolsky"]),
    ("D3", "a-δ 联合 MCMC", ["a-δ", "联合 MCMC", "联合贝叶斯"]),
    ("D4", "EMRI κ↔Γ 1/3 精确映射（10% 缺口）", ["κ↔Γ", "κ=0.30", "轨道平均"]),
    ("D5", "LISA EMRI 3PN 提案", ["3PN 提案", "LISA"]),
    # ── E 开放问题地图（8-29 ~ 8-30）
    ("E1", "开放问题地图 A1–A4（4 项）", ["A1（λ_c", "A2（B2 Lanford", "A3（JK", "A4（v1.24", "开放问题地图"]),
    # ── F 9-07 新框架缺陷（6 条）
    ("F1", "新框架缺陷 6 条（verify.py 等）", ["verify.py", "F1 注释", "F4", "亚普朗克", "净对"]),
    ("F2", "镜像支 B− 回归 / 分支 A-B", ["镜像支", "分支 A", "分支 B"]),
    # ── G 9-09 ~ 9-19 缺口
    ("G1", "Friedmann 缺口（→ 动力学缺口）", ["Friedmann", "动力学缺口", "加速度方程", "连续性方程"]),
    ("G2", "Ω_Λ 23.76 缺口 / O-Λ", ["23.76", "Ω_Λ", "O-Λ", "ρ_Λ"]),
    ("G3", "E_c 能标锁定", ["E_c", "临界能标"]),
    ("G4", "λ 统一为操作式", ["操作式"]),
    ("G5", "ln2 缺口（15 轮定案）", ["ln2", "11.0904", "11.090355"]),
    ("G6", "多种子 / 3D 硬球未做", ["多种子", "硬球"]),
    ("G7", "方向状态数 4 vs 6", ["方向状态", "4 还是 6", "4还是6"]),
    ("G8", "C-b/C-c 跨层判定", ["跨层判定", "C-b", "C-c"]),
    ("G9", "底层四状态的机制", ["底层四状态", "恰是这四个"]),
    ("G10", "Lean 资产 / mathlib 构建", ["mathlib", "olean", "lake build", "Lean"]),
    ("G11", "能标依赖 ε(E) 的组分比例", ["组分比例", "ε(E)"]),
]


def count_hits(text, kws):
    c = 0
    for k in kws:
        c += text.count(k)
    return c


def first_snip(text, kws, width=110):
    best = None
    for k in kws:
        i = text.find(k)
        if i >= 0 and (best is None or i < best):
            best = i
    if best is None:
        return None
    s = text[max(0, best - 40):best + width].replace("\n", " ")
    return re.sub(r"\s+", " ", s)


later_all = "\n".join(logs[d] for d in L_DATES)
LIST_T = rd(LIST)
HAND_T = rd(HAND)

out = []
out.append("=" * 112)
out.append("第 108 轮 · 8-20 ~ 9-19「待选清单」完成度取证（线程级）")
out.append("=" * 112)
out.append("{:<5} {:<40} {:>4} {:>11} {:>11} | {:>4} {:>4}".format(
    "编号", "线程", "B命中", "首次", "末次", "后日", "台账"))
out.append("-" * 112)

table = []
for tid, name, kws in THREADS:
    # S1: B 期
    b_hit = 0
    b_dates = []
    for d in B_DATES:
        c = count_hits(logs[d], kws)
        if c:
            b_hit += c
            b_dates.append(d)
    # S2: 后期日志
    l_hit = count_hits(later_all, kws)
    # S3: 台账
    t_hit = count_hits(LIST_T, kws) + count_hits(HAND_T, kws)
    first = b_dates[0][5:] if b_dates else "—"
    last = b_dates[-1][5:] if b_dates else "—"
    table.append((tid, name, kws, b_hit, first, last, l_hit, t_hit))
    out.append("{:<5} {:<40} {:>4} {:>11} {:>11} | {:>4} {:>4}".format(
        tid, name[:38], b_hit, first, last, l_hit, t_hit))

out.append("")
out.append("=" * 112)
out.append("逐条证据（S2 后期日志片段 / S3 台账片段）")
out.append("=" * 112)
for tid, name, kws, b_hit, first, last, l_hit, t_hit in table:
    out.append("")
    out.append("【{}】{}   （B 期 {}~{}，命中 {}；后期 {}；台账 {}）".format(
        tid, name, first, last, b_hit, l_hit, t_hit))
    s2 = first_snip(later_all, kws)
    s3 = first_snip(LIST_T, kws)
    if s2:
        out.append("    S2 后期日志 : …{}…".format(s2))
    if s3:
        out.append("    S3 台账     : …{}…".format(s3))

io.open(os.path.join(ROOT, "outputs", "_ledger108_out.txt"), "w", encoding="utf-8").write("\n".join(out))
print("⟹ 已写 outputs/_ledger108_out.txt（{} 行）".format(len(out)))
print()
print("汇总：")
print("  B 期有出现且后期无命中（疑悬空）=",
      sum(1 for t in table if t[3] > 0 and t[6] == 0))
print("  B 期有出现且台账有记录       =",
      sum(1 for t in table if t[3] > 0 and t[7] > 0))
print("  线程总数 =", len(table))
