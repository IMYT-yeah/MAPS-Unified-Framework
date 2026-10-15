# -*- coding: utf-8 -*-
"""第 100 轮补丁后核验（V 系列，两段式）；末尾打印通过/失败计数"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
REPO = os.path.join(ROOT, "MAPS-Unified-Framework")
LEAN = os.path.join(REPO, "verification", "lean")

LIST = os.path.join(BASE, "工程期望清单.md")
PRE_LIST = os.path.join(BASE, "工程期望清单_备份_2026-10-03第100轮前.md")
HAND = os.path.join(ROOT, "环境交接说明.md")
PRE_HAND = os.path.join(ROOT, "环境交接说明_备份_2026-10-03第100轮前.md")
MEM = os.path.join(ROOT, ".workbuddy", "memory", "MEMORY.md")
PRE_MEM = os.path.join(ROOT, ".workbuddy", "memory", "MEMORY_备份_2026-10-03第100轮前.md")
MEMO = os.path.join(BASE, "A1补完_Lean侧23条与2sorry与5BX_从重建到全绿.md")
SRC = os.path.join(LEAN, "StormPoC.lean")
README = os.path.join(LEAN, "README.md")

PASS = FAIL = 0


def chk(t, c, m, strict=True):
    global PASS, FAIL
    if c:
        PASS += 1
        print("  [OK] {:<7} {}".format(t, m))
    else:
        if strict:
            FAIL += 1
            print("  [XX] {:<7} {}".format(t, m))
        else:
            print("  [INFO] {:<7} {}".format(t, m))


def hdr(s):
    print("\n" + "=" * 92)
    print(s)
    print("=" * 92)


def rd(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


print("第 100 轮补丁后核验（V 系列）")

hdr("V-1  清单（三维：判定 / 正文 / 台账 ＋ 计数）")
pl, cl = rd(PRE_LIST), rd(LIST)
chk("V-1a", "**C-60**" not in pl and "**C-60**" in cl, "C-60 行已新增")
chk("V-1b", "| **撤回 / 更正** | **58 条**" in pl and "| **撤回 / 更正** | **59 条**" in cl, "更正计数 58 → 59")
chk("V-1c", "**第 100 轮**" in cl and "甲-1" in cl, "§零 含「第 100 轮」＋「甲-1」")
chk("V-1d", "**结项（第 96 ／ 97 ／ **100** 轮）**" in cl and "**`sorry = 0`**" in cl,
    "A1 行更新为「96／97／100 轮」＋ `sorry = 0`")

hdr("V-2  交接说明（§七 100 ＋ 第 100 轮段）")
ph, ch = rd(PRE_HAND), rd(HAND)
chk("V-2a", "当前建议（第 99 轮后）" in ph and "当前建议（第 100 轮后）" in ch, "§七：99 → 100")
chk("V-2b", "**第 100 轮新增（甲-1" in ch and "LW-2" in ch, "新增第 100 轮段 ＋ 明记未完成项 LW-2")

hdr("V-3  MEMORY（进度 100 ＋ 限额 ＋ 铁律 46）")
pm, cm = rd(PRE_MEM), rd(MEM)
chk("V-3a", "**进度：99**" in pm and "**进度：100**" in cm, "进度 99 → 100")
chk("V-3b", len(cm) <= 3000, "字符数 = {}（限额 3000）".format(len(cm)))
chk("V-3c", "46 ⭐⭐" in cm and "C-60" in cm, "新增第 46 条（Lean 侧三铁律）")
chk("V-3d", "A1 Lean ✅97＋100" in cm, "A1 行已更新（97＋100）")
chk("V-3e", cm.count("## 三、铁律") == 1, "MEMORY **未被截断/清空**（恢复后结构完整）")

hdr("V-4  Lean 侧终态（与 LF 呼应）")
src = rd(SRC)
chk("V-4a", "【重建版 v3 · 2026-10-03" in src, "StormPoC.lean 文件头已升 v3")
chk("V-4b", len([l for l in src.split("\n") if l.strip() == "sorry"]) == 0, "`sorry` = 0")
chk("V-4c", "重建统计（v4" in src, "统计块已升 v4（按实际定理数）")
rm = rd(README)
chk("V-4d", "恢复状态表（**v3 · 2026-10-03（第 100 轮）**）" in rm, "README 状态表已升 v3")
chk("V-4e", "第 100 轮补完（2026-10-03）" in rm and "本轮踩的 Lean 坑" in rm,
    "README 含第 100 轮补完段与 Lean 坑清单")

hdr("V-5  备份与派生产物")
for t, p in [("V-5a", PRE_LIST), ("V-5b", PRE_HAND), ("V-5c", PRE_MEM),
             ("V-5d", os.path.join(LEAN, "_history", "StormPoC_备份_2026-10-03第100轮前.lean")),
             ("V-5e", MEMO), ("V-5f", MEMO.replace(".md", ".html")),
             ("V-5g", os.path.join(BASE, "_lean_fill_100.py")),
             ("V-5h", os.path.join(BASE, "_lean_fill_verify_100.py"))]:
    chk(t, os.path.exists(p), "存在 {}".format(os.path.basename(p)))
chk("V-5i", os.path.exists(os.path.join(REPO, "docs", "html",
                                        os.path.basename(MEMO.replace(".md", ".html")))),
    "已镜像到 docs/html/")

print("\n" + "=" * 92)
print("V 汇总：通过 {} 项，失败 {} 项".format(PASS, FAIL))
print("=" * 92)
