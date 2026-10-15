# -*- coding: utf-8 -*-
"""第 104 轮补丁 c：修正清单更正表的结构瑕疵（C-67 曾被插入第 102 轮块中间）。

⚠️ 溯源：第 103 轮把 C-67 插在 `| **C-66** |` 之前，而 C-66 属于第 102 轮的连续块
   （C-64, C-65, C-66）⟹ C-67 把该块**切开**了。本轮又把 C-68/69/70 插在 C-67 前，叠加。
修正：把 C-67/C-68/C-69/C-70 作为一个**连续组**移到 C-64 之前，恢复 C-64/C-65/C-66 连续。
"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
LIST = os.path.join(BASE, "工程期望清单.md")
OK, BAD = [], []


def sub(path, old, new, tag):
    t = io.open(path, encoding="utf-8").read()
    n = t.count(old)
    if n != 1:
        BAD.append("{}（命中 {}）".format(tag, n))
        print("  [XX] {:<24} 命中 {} 次 —— 拒绝".format(tag, n)); return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
    OK.append(tag); print("  [OK] {:<24}".format(tag))


T = io.open(LIST, encoding="utf-8").read()
lines = T.split("\n")

# ---------- ① 结构修正：移动 C-67..C-70 ----------
PATS = ["| **C-67** |", "| **C-68** |", "| **C-69** |", "| **C-70** |"]
found = {}
for pat in PATS:
    idx = [i for i, s in enumerate(lines) if s.startswith(pat)]
    if len(idx) != 1:
        BAD.append("定位 {}（{} 处）".format(pat, len(idx)))
        print("  [XX] 定位 {} —— {} 处".format(pat, len(idx)))
    else:
        found[pat] = idx[0]

if len(found) == 4:
    print("  移动前位置：" + "  ".join("{}@{}".format(p[6:9], i + 1) for p, i in
                                   sorted(found.items(), key=lambda kv: kv[1])))
    # 收集（含其后紧跟的一个空行）
    chunks = {}
    spans = []
    for pat, i in found.items():
        end = i + 1
        if end < len(lines) and lines[end].strip() == "":
            end += 1
        spans.append((i, end))
        chunks[pat] = lines[i:end]
    # 删除（从后往前）
    for a, b in sorted(spans, reverse=True):
        del lines[a:b]
    # 插到 C-64 之前
    i64 = [i for i, s in enumerate(lines) if s.startswith("| **C-64** |")]
    if len(i64) == 1:
        ins = []
        for pat in PATS:                      # C-67 → C-68 → C-69 → C-70
            ins += chunks[pat]
        lines[i64[0]:i64[0]] = ins
        io.open(LIST, "w", encoding="utf-8").write("\n".join(lines))
        OK.append("结构-移动C67..C70")
        print("  [OK] 结构-移动C67..C70      已移到 C-64 之前")
    else:
        BAD.append("定位 C-64（{} 处）".format(len(i64)))
        print("  [XX] 定位 C-64 —— {} 处".format(len(i64)))

# ---------- ② 补登记 C-71（表格块被切开） ----------
ROW_C71 = ("| **C-71** | ⭐ **更正表的块被后续轮次切开（第 103 轮引入；第 104 轮修）** | **结构 / 溯源** | "
           "第 103 轮把 **C-67** 插在 `\\| **C-66** \\|` **之前**，而 C-66 属于第 **102 轮**的连续块 "
           "（`C-64, C-65, C-66`）⟹ **C-67 把该块切开**；第 104 轮追加 C-68/69/70 时叠加了同一问题。 "
           "🔧 处置：把 `C-67, C-68, C-69, C-70` 作为一个**连续组**移到 **C-64 之前**，恢复 "
           "`C-64, C-65, C-66` 连续；并在此登记溯源（**改坏的是我自己上一轮的补丁**）。 "
           "📌 **规范**：新条目一律插在该轮**上一个条目之后**或该轮的**独立分组**里，"
           "**不得插进别轮的连续块中间**；收尾必做**编号连续性 / 分块完整性检查**。 "
           "📌 **同族**：**C-45**（第 90 轮的表格结构检查：裸竖线拆列 ＋ 残行）—— 那次是**排版破损**，"
           "本次是**分块完整性**。 "
           "| 第 104 轮 | 同 `甲5结项_…md` |")
t2 = io.open(LIST, encoding="utf-8").read()
if t2.count("| **C-71** |") == 0:
    sub(LIST, "| **C-70** |", ROW_C71 + "\n" + "| **C-70** |", "清单-C-71行")
else:
    print("  [SKIP] 清单-C-71行（已存在）")

sub(LIST, "| **撤回 / 更正** | **69 条**", "| **撤回 / 更正** | **70 条**", "清单-计数70")

# ---------- ③ 收尾自检 ----------
print("\n[自检：编号序列]")
import re
L2 = io.open(LIST, encoding="utf-8").read().split("\n")
seq = []
for i, s in enumerate(L2, 1):
    m = re.match(r"^\|\s*\*\*([CNI]-\d+)\*\*\s*\|", s)
    if m:
        seq.append((i, m.group(1)))
tail = [x for x in seq if x[0] > 95]
print("        " + " → ".join(x[1] for x in tail))
nums = [int(x[1].split("-")[1]) for x in tail if x[1].startswith("C-")]
print("        C 编号序列 = {}".format(nums))
print("        134 行附近的期望顺序：C-67, C-68, C-69, C-70, C-71, C-64, C-65, C-66, C-61, ...")

print("\n" + "=" * 90)
print("OK {} 项，BAD {} 项".format(len(OK), len(BAD)))
if BAD:
    print("失败：" + " ｜ ".join(BAD))
print("=" * 90)
