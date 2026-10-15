# -*- coding: utf-8 -*-
"""第 102 轮核验（V-1…V-xx）"""
import io
import os
import numpy as np

ROOT = r"[WORKSPACE]"
ZH = os.path.join(ROOT, "outputs/论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(ROOT, "outputs/Paper_MatterAntimatterPairStorm_v2.9_EN.md")
LIST = os.path.join(ROOT, "outputs/项目台账.md")
HAND = os.path.join(ROOT, "环境说明.md")
MEM = os.path.join(ROOT, ".workbuddy/memory/MEMORY.md")
MEMO = os.path.join(ROOT, "outputs/甲3结项_toric_code相变点_判据不能判别与h_c=K-J缺机制.md")
OUT = os.path.join(ROOT, "outputs")
N, BAD = 0, []


def ck(tag, cond, msg):
    global N
    N += 1
    if not cond:
        BAD.append("{}: {}".format(tag, msg))


rd = lambda p: io.open(p, encoding="utf-8").read()
zh, en, li, hd, me, mo = rd(ZH), rd(EN), rd(LIST), rd(HAND), rd(MEM), rd(MEMO)

# ---------------- 中文稿 ----------------
ck("V-1", "该更正本身是错的" in zh, "ZH §5.7 的 C-64 更正缺失")
ck("V-2", "X 场版本 = 0.328474，不是 0.32" in zh, "ZH C-64 结论句缺失")
ck("V-3", "**相变不依赖 J**" in zh, "ZH C-65 缺")
ck("V-4", "【第 102 轮（甲-3）toric code 相变点" in zh, "ZH 第 102 轮块缺失")
ck("V-5", "0.31 ± 0.02" in zh and "0.3683" in zh, "ZH 数值结果缺")
ck("V-6", "**跨约定不可混比**（**C-66**）" in zh, "ZH C-66 缺")
ck("V-7", "**X 场版本应对标 h_xc≈0.32**" not in zh.replace("v1.23 曾写", ""), "ZH 旧错误表述未清")

# ---------------- 英文稿 ----------------
ck("V-8", "That correction was wrong" in en, "EN C-64 缺")
ck("V-9", "the X-field version is 0.328474, not 0.32" in en, "EN C-64 结论句缺")
ck("V-10", "the transition **does not depend on J**" in en, "EN C-65 缺")
ck("V-11", "Round 102 (item 甲-3) toric-code transition" in en, "EN 第 102 轮块缺")
ck("V-12", "0.31 ± 0.02" in en and "0.3683" in en, "EN 数值结果缺")
ck("V-13", "cross-convention comparison is invalid (C-66)" in en, "EN C-66 缺")
ck("V-14", "should be compared with h_xc≈0.32**" not in en.replace("v1.23 claimed", ""), "EN 旧错误表述未清")

# ---------------- 台账 / 交接 ----------------
ck("V-15", "| **第 102 轮**（**甲-3 执行**） |" in li, "清单 §零 第 102 轮行缺")
for c in ("C-64", "C-65", "C-66"):
    ck("V-16-" + c, "| **{}** |".format(c) in li, "清单缺 {}".format(c))
ck("V-17", "| **撤回 / 更正** | **65 条**" in li, "清单计数未改 65")
ck("V-18", "甲-3 相变点精确值~~ ✅ 第 102 轮结项" in li, "清单剩余待办未更新")
ck("V-19", "当前建议（第 102 轮后）" in hd, "交接 §七 未更新")
ck("V-20", "第 102 轮新增（甲-3：toric code 相变点" in hd, "交接第 102 轮段缺")

# ---------------- MEMORY / 技能 ----------------
ck("V-21", len(me) <= 3000, "MEMORY 超限：{}".format(len(me)))
ck("V-22", "**进度：102**" in me, "MEMORY 进度未更新")
ck("V-23", "48 ⭐⭐⭐ **选判据前先查「极限处是否退化」**" in me, "MEMORY 缺铁律 48")
ck("V-24", "C-6…C-66" in me, "MEMORY 更正范围未更新")

# ---------------- 数据与脚本 ----------------
need = ["_toric102.py", "_toric102_run.py", "_toric102_analyze.py", "_patch_102.py", "_patch_102b.py",
        "_toric102_t22.npz", "_toric102_t23.npz", "_toric102_t33.npz", "_toric102_t34.npz",
        "_toric102_t44.npz", "_toric102_datadump.txt",
        "甲3结项_toric_code相变点_判据不能判别与h_c=K-J缺机制.md"]
miss = [f for f in need if not os.path.exists(os.path.join(OUT, f))]
ck("V-25", not miss, "缺文件: {}".format(miss))

# ---------------- 数据自洽（硬数字） ----------------
d = np.load(os.path.join(OUT, "_toric102_t44.npz"))
ck("V-26", int(d["dim"]) == 131072, "4×4 扇区维 ≠ 131072")
ck("V-27", abs(d["rows"][0, 1] - (-32.339755307)) < 1e-6, "4×4 的 E0(h=0.20) 不符")
d33 = np.load(os.path.join(OUT, "_toric102_t33.npz"))
i35 = int(np.argmin(np.abs(d33["rows"][:, 0] - 0.35)))
ck("V-28", abs(d33["rows"][i35, 3] - 0.376308) < 1e-5, "3×3 的 m(h=0.35) 与当年记录不一致")
ck("V-29", abs(d33["rows"][0, 1] - (-18.210495638)) < 1e-6, "3×3 的 E0(h=0.20) 不符")
# 3×3 vs 4×4 的 Binder 交叉应在 0.30–0.33 之间
g = np.linspace(0.20, 0.50, 3000)
u3 = np.interp(g, d33["rows"][:, 0], d33["rows"][:, 6])
u4 = np.interp(g, d["rows"][:, 0], d["rows"][:, 6])
s = np.where(np.diff(np.sign(u3 - u4)))[0]
if len(s) >= 1:
    ck("V-30", 0.29 <= g[s[0]] <= 0.34,
       "3×3 vs 4×4 的 Binder 交叉不在 0.29–0.34（实得 {:.4f}）".format(g[s[0]]))
else:
    k0 = int(np.argmin(np.abs(u3 - u4)))
    ck("V-30", 0.29 <= g[k0] <= 0.34,
       "3×3 vs 4×4 无交叉且最小间距点不在 0.29–0.34（实得 {:.4f}）".format(g[k0]))
    ck("V-30b", abs(g[k0] - 0.3100) < 0.005, "最小间距点与备忘录记的 0.3100 不符")
# 关键数字在备忘录里
for tag, txt in [("V-31", mo), ("V-32", zh), ("V-33", en)]:
    ck(tag, "0.328474" in txt, "关键数字 0.328474 未出现")
ck("V-34", "3.3e4" in mo or "3.3×10⁴" in mo or "131072" in mo, "备忘录缺扇区压缩比")
ck("V-35", "1e-12" in mo, "备忘录缺 J 无关性的精度")

print("=" * 78)
print("第 102 轮核验：{} 项，失败 {} 项".format(N, len(BAD)))
print("=" * 78)
for b in BAD:
    print("  ✗", b)
if not BAD:
    print("  全部通过 ✓")
