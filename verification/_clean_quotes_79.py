# -*- coding: utf-8 -*-
"""
第 79 轮 4.3：清理「中文行里的 ASCII 引号」→ 「」/『』

⚠️ 判据的演进（本轮踩到过，已写进技能）：
  ① 旧判据「引号**两侧均为 CJK**」太窄 —— 像 `"配对阶数" n=3` 的**闭引号右侧是空格**，
     不计入 ⟹ 该行只剩 1 个候选 ⟹ **配对错位**（只改了开引号）。实测行 23 就是这样坏的。
  ② 新判据：**按行处理** —— 若该行是**中文行**（CJK 字符 ≥ 10）且 ASCII `"` 个数为**偶数**，
     则把该行**全部** `"` 按出现顺序配对替换（奇数位 →「，偶数位 →」）。
     ⚠️ 实测全文 105 个含引号的行，**引号数全部为偶数**（72 行 2 个 / 23 行 4 个 / …），零奇数行。

用法：`python _clean_quotes_79.py`（dry run，只报数）｜`python _clean_quotes_79.py --apply`（实际改）
"""
import io, os, re, sys, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
HIST = os.path.join(os.path.dirname(BASE), "MAPS-Unified-Framework", "paper", "history")
APPLY = "--apply" in sys.argv

CJK = lambda c: "\u4e00" <= c <= "\u9fff"
SKIP_PAT = [(r"\$\$", "LaTeX $$"), (r"\]\(", "markdown 链接"), (r"!\[", "图片"), (r"`[^`]*[\"'][^`]*`", "行内代码含引号")]

txt = io.open(ZH, encoding="utf-8").read()
L = txt.split("\n")

PLAN, SKIPPED, NOQUOTE = [], [], 0
for k, s in enumerate(L, 1):
    nq = s.count('"')
    if nq == 0:
        NOQUOTE += 1
        continue
    cj = sum(1 for ch in s if CJK(ch))
    risk = [nm for pat, nm in SKIP_PAT if re.search(pat, s)]
    if s.strip().startswith("```"):
        SKIPPED.append((k, "代码围栏", nq)); continue
    if risk:
        SKIPPED.append((k, "+".join(risk), nq)); continue
    if cj < 10:
        SKIPPED.append((k, "非中文行（CJK<10）", nq)); continue
    if nq % 2 == 1:
        SKIPPED.append((k, "奇数个引号", nq)); continue
    out, n = s, 0
    for i, ch in enumerate(s):
        if ch == '"':
            out = out[:i] + ("「" if n % 2 == 0 else "」") + out[i + 1:]
            n += 1
    PLAN.append((k, s, out, nq))

n_all = sum(s.count('"') for s in L)
print("=" * 78)
print("4.3 引号清理 {}（第 79 轮）".format("【APPLY】" if APPLY else "【DRY RUN】"))
print("=" * 78)
print("  全文 ASCII 双引号总数 = {}".format(n_all))
print("  ⭐ **口径**：工作流说的「77 处」是**行计数**、格式指标里的「148」是**两侧 CJK 的字符计数**；")
print("     完整的本方案口径 = 「**中文行里的全部 ASCII 引号**」")
print()
print("  计划清理：**{} 行 / {} 个引号**".format(len(PLAN), sum(p[3] for p in PLAN)))
print("  跳过：{} 行".format(len(SKIPPED)))
for k, why, nq in SKIPPED[:20]:
    print("     行 {:<5} {:<28} （{} 个引号）".format(k, why, nq))
if len(SKIPPED) > 20:
    print("     … 共 {} 行".format(len(SKIPPED)))
print()
print("  抽样对照（前 10 行）：")
for k, a, b, nq in PLAN[:10]:
    ia = a.find('"')
    ib = b.find("「") if "「" in b else b.find("」")
    print("     行 {:<5} （{} 个引号）".format(k, nq))
    print("       − …{}…".format(a[max(0, ia - 45):ia + 55]))
    print("       + …{}…".format(b[max(0, ib - 45):ib + 55]))
print()

if APPLY:
    shutil.copy2(ZH, os.path.join(HIST, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第79轮前.md"))
    print("  [BK] 已备份")
    for k, a, b, nq in PLAN:
        L[k - 1] = b
    io.open(ZH, "w", encoding="utf-8").write("\n".join(L))
    print("  [OK] 已写入")
    # 自查
    L2 = io.open(ZH, encoding="utf-8").read().split("\n")
    rest = sum(s.count('"') for s in L2)
    rest_cjk = sum(1 for s in L2 for i, ch in enumerate(s)
                   if ch == '"' and 0 < i < len(s) - 1 and CJK(s[i - 1]) and CJK(s[i + 1]))
    print()
    print("  ── 自查 ──")
    print("     行数：{}（改前 {}）—— {}".format(len(L2), len(L), "✓" if len(L2) == len(L) else "✗"))
    print("     剩余 ASCII 双引号：**{} 个**（改前 {}）".format(rest, n_all))
    print("     其中「两侧 CJK」的：{} 个（改前 148）".format(rest_cjk))
    bad_pipe = sum(1 for s in L2 if "\\|" in s and not s.lstrip().startswith("|"))
    frag = [i + 1 for i, s in enumerate(L2) if s.strip().startswith(("，", ","))]
    print("     非表格反斜杠竖线：{} ｜ 残片行：{}".format(bad_pipe, frag))
    print("     剩余引号所在行：{}".format([i + 1 for i, s in enumerate(L2) if '"' in s]))
else:
    print("  （dry run —— 未改动文件。确认后用 `--apply`）")
print("=" * 78)
