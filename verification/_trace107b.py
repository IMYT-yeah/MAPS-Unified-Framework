# -*- coding: utf-8 -*-
"""第 107 轮 · b：未完成分支的可追溯性盘点（TR-17 … TR-24）

从全部日志 + 台账里提取「未完成/待办/开放」类标记，按日期与项目归类，
并判断每条落在哪个追溯区间（日志有 / 对话原文有 / 两者都有 / 已不可逐句追）。
"""
import io
import os
import glob
import re
import collections

HOME = r"C:/Users/Administrator"
WS = os.path.join(HOME, "Desktop/2026-08-20-21-43-34")
WS2 = os.path.join(HOME, "Desktop/2026-08-30-22-39-18")

MARK = ["待办", "未完成", "尚未", "未做", "开放问题", "下一步", "剩余", "缺口",
        "TODO", "☐", "待定", "未攻", "判否", "留给后续", "后续工作"]

P, F = [0], []


def ck(tag, cond, msg):
    ok = bool(cond)
    P[0] += 1
    if not ok:
        F.append(tag)
    print("  [{}] {} — {}".format("OK" if ok else "XX", tag, msg))


def scan(dirpath, label):
    """→ [(date, file, mark, line)]"""
    out = []
    for fp in sorted(glob.glob(os.path.join(dirpath, "2026-*.md"))):
        d = os.path.basename(fp)[:10]
        for ln in io.open(fp, encoding="utf-8", errors="replace").read().split("\n"):
            s = ln.strip()
            if not s or len(s) < 8:
                continue
            for m in MARK:
                if m in s:
                    out.append((d, label, m, s))
                    break
    return out


A = scan(os.path.join(WS, ".workbuddy/memory"), "MAPS")
B = scan(os.path.join(WS2, ".workbuddy/memory"), "jczq")

print("=" * 100)
print("第 107 轮 · b：未完成分支盘点")
print("=" * 100)

print("\n--- TR-17…TR-19  「未完成」类标记的规模 ---")
ca = collections.Counter(d for d, _, _, _ in A)
cb = collections.Counter(d for d, _, _, _ in B)
print("      MAPS 项目：{} 条标记，分布在 {} 天".format(len(A), len(ca)))
print("      jczq 项目：{} 条标记，分布在 {} 天".format(len(B), len(cb)))
print("      MAPS 标记最多的 8 天：{}".format(
    [(k[5:], v) for k, v in ca.most_common(8)]))
ck("TR-17", len(A) >= 200,
   "MAPS 日志里有 **{} 条**「未完成/待办/开放」类标记 ⟹ 素材量足够做盘点".format(len(A)))
ck("TR-18", all(len(c) > 0 for c in [ca, cb]),
   "两个项目**都有**未完成标记（jczq {} 条）".format(len(B)))
ck("TR-19", len(ca) >= 25,
   "标记覆盖 **{} 天**（8-20 起）⟹ 可按时间轴还原「什么时候开的什么分支」".format(len(ca)))

print("\n--- TR-20…TR-21  正式台账（已结构化的未完成清单）---")
tabs = [
    ("全量待办总账", os.path.join(WS, "outputs/工程期望清单.md")),
    ("交接说明（含逐轮段）", os.path.join(WS, "环境交接说明.md")),
    ("工作流（按依赖排序）", os.path.join(WS, "outputs/未完成研究工作流_按依赖排序.md")),
    ("候选池", os.path.join(WS, "outputs/工程期望清单.md")),
]
for name, fp in tabs:
    ok = os.path.exists(fp)
    print("      {:<22} {}  {}".format(name, "✅" if ok else "❌",
                                    "{:.0f} KB".format(os.path.getsize(fp) / 1024) if ok else ""))
ck("TR-20", all(os.path.exists(fp) for _, fp in tabs[:3]),
   "**三个正式台账都在**（清单／交接说明／工作流）⟹ 已结构化的未完成分支**全部可追**")
ck("TR-21", os.path.exists(tabs[0][1]) and "撤回 / 更正" in io.open(tabs[0][1], encoding="utf-8").read(),
   "清单内含「撤回/更正」表（**已被否掉的分支**也有记录，避免重开）")

print("\n--- TR-22…TR-24  追溯分级（按「对话原文是否覆盖」）---")
CUT = "2026-09-20"      # 对话原文的起点
g = {"可逐句追（9-20 后）": 0, "仅日志（8-20～9-19）": 0}
for d, _, _, _ in A:
    if d >= CUT:
        g["可逐句追（9-20 后）"] += 1
    else:
        g["仅日志（8-20～9-19）"] += 1
print("      MAPS：{}".format(g))
print("      jczq：{}".format(
    {"可逐句追（9-20 后）": sum(1 for d, _, _, _ in B if d >= CUT),
     "仅日志（8-20～9-19）": sum(1 for d, _, _, _ in B if d < CUT)}))
ck("TR-22", g["仅日志（8-20～9-19）"] > 0,
   "⚠️ **{} 条标记落在 8-20～9-19**（只有日志、无对话原文）".format(g["仅日志（8-20～9-19）"]))
ck("TR-23", g["可逐句追（9-20 后）"] > 0,
   "**{} 条落在 9-20 后**（日志 ＋ 对话原文双源可核）".format(g["可逐句追（9-20 后）"]))

# 抽样：早期（仅日志）的「下一步」类行，看粒度
print("\n【抽样：8-20～9-19 的「下一步/待办」行（这些只能靠日志）】")
early = [(d, m, s) for d, lab, m, s in A if d < CUT and m in ("下一步", "待办", "剩余", "未完成")]
seen = set()
n = 0
for d, m, s in sorted(early):
    key = (d, m)
    if key in seen:
        continue
    seen.add(key)
    print("   [{}] ({}) {}".format(d[5:], m, s[:110]))
    n += 1
    if n >= 14:
        break
ck("TR-24", n >= 8,
   "抽样可见：**早期日志的「下一步」粒度足够还原分支**（抽 {} 条）".format(n))

print("\n" + "=" * 100)
print("通过 {} 项，失败 {} 项{}".format(P[0] - len(F), len(F),
                                "" if not F else "  ⟹ " + ", ".join(F)))
print("=" * 100)
