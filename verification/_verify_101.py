# -*- coding: utf-8 -*-
"""第 101 轮补丁核验（V-1…V-2x）"""
import io
import os
import numpy as np

ROOT = r"C:/Users/Administrator/Desktop/2026-08-20-21-43-34"
ZH = os.path.join(ROOT, "outputs/论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(ROOT, "outputs/Paper_MatterAntimatterPairStorm_v2.9_EN.md")
LIST = os.path.join(ROOT, "outputs/工程期望清单.md")
HAND = os.path.join(ROOT, "环境交接说明.md")
MEM = os.path.join(ROOT, ".workbuddy/memory/MEMORY.md")
A1R = os.path.join(ROOT, "outputs/A1_3D盒子λc数值定位.md")
MEMO = os.path.join(ROOT, "outputs/甲2结项_λc∞未定位_判据分辨率不足的量化.md")
SKILL = r"C:/Users/Administrator/.workbuddy/skills/maps-deduction-round/SKILL.md"
OUT = os.path.join(ROOT, "outputs")

N, BAD = 0, []


def ck(tag, cond, msg):
    global N
    N += 1
    if not cond:
        BAD.append("{}: {}".format(tag, msg))


def rd(p):
    return io.open(p, encoding="utf-8").read()


zh, en, li, hd, me, a1, mo = rd(ZH), rd(EN), rd(LIST), rd(HAND), rd(MEM), rd(A1R), rd(MEMO)
sk = rd(SKILL)

# ---------------- 论文：中文 ----------------
ck("V-1", "【第 101 轮：热力学极限值仍未定位】" in zh, "ZH850 未更新")
ck("V-2", "第 101 轮再修正" in zh and "两者不在同一轴" in zh, "ZH1126 v1.36 修正未同步")
ck("V-3", "【第 101 轮（甲-2）更正：`λ_c(∞)` 仍未定位" in zh, "ZH2033 更正段缺失")
ck("V-4", "「方法学不足，未定位」" in zh, "ZH2033 判决句缺失")
ck("V-5", "λ_c(∞) **仍未定位**（第 101 轮" in zh, "ZH2037 未更新")
ck("V-6", "第 101 轮：4 尺寸含 L=3 已做，仍未定位" in zh, "ZH §10.2#13 未更新")
ck("V-7", "λ_c ∈ [0.21, 0.23]" not in zh and "[0.21, 0.23]**（与 3D Ising" not in zh,
   "ZH 仍残留旧结论（λ_c ∈ [0.21,0.23] 或 λ_c(∞) 估计 [0.21,0.23]）")
ck("V-7b", zh.count("0.21, 0.23") <= 2, "ZH 中 0.21, 0.23 出现次数异常")

# ---------------- 论文：英文（中英同步） ----------------
ck("V-8", "round 101: thermodynamic-limit value still not localized" in en, "EN850 未更新")
ck("V-9", "Round-101 re-correction" in en and "not valid — different axes" in en, "EN v1.36 修正未同步")
ck("V-10", "the peak does not converge" in en and "0.3075" in en, "EN §10.1b 第 101 轮段缺失")
ck("V-11", "still not localized" in en, "EN §10.1b 判决句缺失")
ck("V-12", "remains unlocalized after round 101" in en, "EN §10.1b 末句未更新")
ck("V-13", "round 101: 4 sizes incl. L=3 already done" in en, "EN §10.2#13 未补")
ck("V-14", "λ_c(∞) ∈ [0.140, 0.140]" not in en, "EN 仍残留旧的 [0.140,0.140] 结论")

# ---------------- 台账 ----------------
ck("V-15", "| **第 101 轮**（**甲-2 执行**） |" in li, "清单 §零 第 101 轮行缺失")
for c in ("C-61", "C-62", "C-63"):
    ck("V-16-" + c, "| **{}** |".format(c) in li, "清单缺 {}".format(c))
ck("V-17", "| **撤回 / 更正** | **62 条**" in li, "清单计数未改为 62")
ck("V-18", "甲-2 `λ_c(∞)` 精确定位~~ ✅ 第 101 轮结项" in li, "清单剩余待办未更新")

# ---------------- 交接 ----------------
ck("V-19", "当前建议（第 101 轮后）" in hd, "交接 §七 未更新")
ck("V-20", "第 101 轮新增（甲-2：`λ_c(∞)` 精确定位" in hd, "交接第 101 轮段缺失")

# ---------------- A1 报告更正注 ----------------
ck("V-21", "【第 101 轮（甲-2）更正 —— 本报告的核心结论已被推翻" in a1, "A1 报告缺更正注")

# ---------------- MEMORY ----------------
ck("V-22", len(me) <= 3000, "MEMORY 超限：{} 字符".format(len(me)))
ck("V-23", "**进度：101**" in me, "MEMORY 进度未更新")
ck("V-24", "47 ⭐⭐⭐ **「判据分辨率」必须先量化" in me, "MEMORY 缺铁律 47")
ck("V-25", "**C-6…C-63**" in me or "C-6…C-63" in me, "MEMORY 缺 C-63 范围")

# ---------------- 技能 ----------------
ck("V-26", "98. **⭐⭐⭐ 「判据分辨率」必须先量化" in sk, "技能缺陷阱 98")
ck("V-27", "陷阱 1–98" in me, "MEMORY 未更新陷阱范围")

# ---------------- 数据与脚本 ----------------
need = ["_lc3d_box_fast.py", "_lc3d_run_101.py", "_lc3d_analyze.py", "_lc3d_chitest.py",
        "_lc3d_pushbench.py", "_lc3d_101_t222chi8.npz", "_lc3d_101_t322chi8.npz",
        "_lc3d_101_t332chi8.npz", "_lc3d_101_t333chi8.npz",
        "_lc3d_101_f222chi8.npz", "_lc3d_101_f322chi8.npz", "_lc3d_101_f332chi8.npz",
        "甲2结项_λc∞未定位_判据分辨率不足的量化.md", "_patch_101a.py", "_patch_101b.py",
        "_patch_101c.py", "_lc3d_101_datadump.txt"]
miss = [f for f in need if not os.path.exists(os.path.join(OUT, f))]
ck("V-28", not miss, "缺文件：{}".format(miss))

# ---------------- 数据自洽（硬数字核验） ----------------
d = np.load(os.path.join(OUT, "_lc3d_101_t333chi8.npz"))
ck("V-29", abs(d['E'][0] - (-27.0)) < 1e-12, "3×3×3 的 E(λ=0) ≠ −N_c")
ck("V-30", int(d['Nc']) == 27 and int(d['n']) == 108, "3×3×3 的 N_c/n 不符")
phi = -np.gradient(d['ac'], d['lams'])
i = int(np.argmax(phi))
ck("V-31", abs(d['lams'][i] - 0.30) < 1e-9, "3×3×3 粗扫 χ 峰不在 0.30")
# 备忘录与论文里的关键数字必须与数据一致
for tag, txt in [("V-32", mo), ("V-33", zh), ("V-34", en)]:
    ck(tag, "0.3075" in txt, "关键数字 0.3075 未出现")
ck("V-35", "0.436" in mo and "0.436" in zh, "外推荒谬值 0.436 未登记")
ck("V-36", "6.93" in mo, "χ 截断 6.93% 未登记")

print("=" * 78)
print("第 101 轮核验：{} 项，失败 {} 项".format(N, len(BAD)))
print("=" * 78)
for b in BAD:
    print("  ✗", b)
if not BAD:
    print("  全部通过 ✓")
