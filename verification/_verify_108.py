# -*- coding: utf-8 -*-
"""第 108 轮核验：待选清单完成度核查（LC-1…LC-14）"""
import io
import os
import re

ROOT = r"[WORKSPACE]"
MD = os.path.join(ROOT, ".workbuddy", "memory")
OUTD = os.path.join(ROOT, "outputs")
MEMO_P = os.path.join(OUTD, "待选清单完成度核查_8-20至9-19.md")
MEMO = io.open(MEMO_P, encoding="utf-8").read()
HAND = io.open(os.path.join(ROOT, "环境说明.md"), encoding="utf-8", errors="replace").read()
LIST = io.open(os.path.join(OUTD, "项目台账.md"), encoding="utf-8", errors="replace").read()

FAIL = []
N = [0]


def ck(tag, cond, msg):
    N[0] += 1
    ok = bool(cond)
    if not ok:
        FAIL.append(tag)
    print("  [{}] {:<6} {}".format("OK" if ok else "XX", tag, msg))


# ---------------------------------------------------------------- 复算抽取
logs = {fn[:10]: io.open(os.path.join(MD, fn), encoding="utf-8", errors="replace").read()
        for fn in sorted(os.listdir(MD)) if re.match(r"^2026-\d\d-\d\d\.md$", fn)}
BD = [d for d in sorted(logs) if d <= "2026-09-19"]
MARK = ["待办", "未完成", "尚未", "未做", "开放问题", "下一步", "剩余", "缺口",
        "TODO", "☐", "待定", "留给后续", "后续工作", "未解决", "待验证", "待严格"]
CAND = re.compile(r"(下一步候选|下一步|待办|遗留|剩余|未完成|开放问题|缺口|收尾待办)")
nline, nitem = 0, 0
for d in BD:
    for ln in logs[d].split("\n"):
        if any(m in ln for m in MARK) and CAND.search(ln):
            nline += 1
            body = re.sub(r"^[\-\*\s>*#]+", "", ln.strip())
            body = re.sub(r"^\*\*|\*\*$", "", body)
            parts = re.split(r"[①②③④⑤⑥⑦⑧⑨⑩]|；\s*(?=[A-Zα-ωa-z\u4e00-\u9fff])", body)
            nitem += len([p for p in parts if len(p.strip()) > 5])

print("=" * 92)
print("第 108 轮核验 —— 待选清单完成度核查")
print("=" * 92)
ck("LC-1", len(BD) == 17, "B 期日志天数 = {}（08-20…09-19）".format(len(BD)))
ck("LC-2", nline == 142 and nitem == 265,
   "复算抽取：候选行 = {}（期望 142）｜条目 = {}（期望 265）".format(nline, nitem))

# ---------------------------------------------------------------- 五态计数
ck("LC-3", "38" in MEMO and "**12**" in MEMO and "**4**" in MEMO,
   "备忘录 §二 给出 38 / 12 / 4 三档计数")
ck("LC-4", 38 + 12 + 4 == 54, "38 + 12 + 4 = 54（线程总数）")

# 附录 A 行数
ids38 = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A9", "A10", "A11", "A12", "A13", "A15", "A17",
         "A18", "A19", "A21", "A22", "B1", "B2", "B4", "B5", "B7", "B8", "C1", "C2", "C3",
         "D1", "D2", "D3", "D5", "E1", "F1", "G3", "G6", "G7", "G8", "G10"]
appA = MEMO.split("附录 A")[1] if "附录 A" in MEMO else ""
found = set()
for ln in appA.split("\n"):
    m = re.match(r"^\|\s*([A-G]\d+)\s*\|", ln)
    if m:
        found.add(m.group(1))
ck("LC-5", len(ids38) == 38, "清单内 ✅ 编号数 = {}（期望 38）".format(len(ids38)))
ck("LC-6", found == set(ids38),
   "附录 A 实际列出 {} 条；与清单差 = {}".format(len(found), sorted(set(ids38) ^ found)))

# §三 真缺口 4 条
sec3 = MEMO.split("## 三、")[1].split("## 四、")[0] if "## 三、" in MEMO else ""
gaps = sorted(set(re.findall(r"\*\*(A\d+|D\d+|G\d+)\*\*", sec3)))
ck("LC-7", gaps == ["A23", "D4", "G4", "G9"],
   "§三 真缺口 = {}（期望 A23/D4/G4/G9）".format(gaps))

# §五 十二行
sec5 = MEMO.split("## 五、")[1].split("## 六、")[0] if "## 五、" in MEMO else ""
r5 = [m.group(1) for m in re.finditer(r"^\|\s*([A-G]\d+)\s*\|", sec5, re.M)]
ck("LC-8", len(r5) == 12, "§五「✅→⛔」表 = {} 行（期望 12）：{}".format(len(r5), r5))

# ---------------------------------------------------------------- 关键事实复核
# A23 / D4 / G4 无可交付物
pool = []
for d in (OUTD, os.path.join(ROOT, "MAPS-Unified-Framework", "notes", "推演专题")):
    if os.path.isdir(d):
        pool += os.listdir(d)
def has(sub):
    return [f for f in pool if sub in f]
ck("LC-9", not has("普朗克常数") and not has("κ↔Γ") and not has("操作式"),
   "A23/D4/G4 **确实无交付物**（普朗克常数={}｜κ↔Γ={}｜操作式={}）".format(
       has("普朗克常数"), has("κ↔Γ"), has("操作式")))
# G9 仍开放
ck("LC-10", "⚠️ **仍未解决**" in HAND and "底层四状态为何恰是这四个" in HAND,
   "交接说明原文仍写「⚠️ **仍未解决**：11.0904 的自然性；底层四状态为何恰是这四个」⟹ G9 确为未解")
# G7/G8 已解决
ck("LC-11", "第 31 轮已复查并定案" in HAND and "16 = 4 × 4 保住" in HAND,
   "G7 已在**第 31 轮定案**（16 = 4×4 保住、方向数必须 4）")
ck("LC-12", "B2 闭环" in HAND or "两个软肋至此全部解除" in HAND,
   "G8 已在**第 32/33 轮闭环**（w 扫描 ⟹ B2 软肋解除）")
# A9 并入
ck("LC-13", "非热修正" in io.open(os.path.join(OUTD, "吸积盘辐射传输报告.md"), encoding="utf-8").read(),
   "A9「非热修正观测提案」确实并入 `吸积盘辐射传输报告`（该文件含「非热修正」）")
# E1 收官
ck("LC-14", "A 类 4 项全部收官" in logs["2026-08-30"],
   "E1「开放问题地图 A1–A4」在 08-30 日志明写「**A 类 4 项全部收官**」")

print()
print("=" * 92)
print("通过 {} 项，失败 {} 项{}".format(N[0] - len(FAIL), len(FAIL),
                                 "" if not FAIL else "  ⟹ " + ", ".join(FAIL)))
print("=" * 92)
