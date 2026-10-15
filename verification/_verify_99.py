# -*- coding: utf-8 -*-
"""第 99 轮补丁后核验（V 系列，两段式）；末尾打印通过/失败计数"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
LIST = os.path.join(BASE, "工程期望清单.md")
PRE_LIST = os.path.join(BASE, "工程期望清单_备份_2026-10-03第99轮前.md")
HAND = os.path.join(ROOT, "环境交接说明.md")
PRE_HAND = os.path.join(ROOT, "环境交接说明_备份_2026-10-03第99轮前.md")
MEM = os.path.join(ROOT, ".workbuddy", "memory", "MEMORY.md")
PRE_MEM = os.path.join(ROOT, ".workbuddy", "memory", "MEMORY_备份_2026-10-03第99轮前.md")
MEMO = os.path.join(BASE, "可算与可推清单_第99轮四源交叉清点.md")

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


print("第 99 轮补丁后核验（V 系列）")

hdr("V-1  清单：三个维度（判定 / 正文 / 台账 ＋ 更正计数）")
pl, cl = rd(PRE_LIST), rd(LIST)
chk("V-1a", "**C-59**" not in pl and "**C-59**" in cl, "C-59 行已新增")
chk("V-1b", "| **撤回 / 更正** | **57 条**" in pl and "| **撤回 / 更正** | **58 条**" in cl,
    "更正计数 57 → 58")
chk("V-1c", "**第 99 轮**" in cl and "I-23" in cl, "§零 标识记录含「第 99 轮」；I-23 已登记")
chk("V-1d", "本行原缺 ✅ 共 13 处" in cl and cl.count("✅") > pl.count("✅") + 10,
    "台账行已补 ✅（≥ 11 处新增）＋ 第 99 轮注")
chk("V-1e", "清点不可只读本行" in cl, "表头警示已加")

hdr("V-2  交接说明（§七 99 ＋ 第 99 轮段）")
ph, ch = rd(PRE_HAND), rd(HAND)
chk("V-2a", "当前建议（第 98 轮后）" in ph and "当前建议（第 99 轮后）" in ch, "§七：98 → 99")
chk("V-2b", "**第 99 轮新增（四源交叉清点" in ch, "新增「第 99 轮」段")
chk("V-2c", "O1–O5" in ch and "C-59" in ch, "并轨 O1–O5 与 C-59 均已入交接")

hdr("V-3  MEMORY（进度 99 ＋ 限额 ＋ C-59 条）")
pm, cm = rd(PRE_MEM), rd(MEM)
chk("V-3a", "**进度：98**" in pm and "**进度：99**" in cm, "进度 98 → 99")
chk("V-3b", len(cm) <= 3000, "字符数 = {}（限额 3000）".format(len(cm)))
chk("V-3c", "45 ⭐⭐" in cm and "C-59" in cm, "新增第 45 条（清点须四源交叉）")
chk("V-3d", "C-6…C-59" in cm, "已判死编号范围更新 C-58 → C-59")

hdr("V-4  交付件与备份")
for t, p in [("V-4a", MEMO), ("V-4b", MEMO.replace(".md", ".html")),
             ("V-4c", os.path.join(BASE, "_open_99.py")), ("V-4d", PRE_LIST),
             ("V-4e", PRE_HAND), ("V-4f", PRE_MEM)]:
    chk(t, os.path.exists(p), "存在 {}".format(os.path.basename(p)))
chk("V-4g", os.path.exists(os.path.join(ROOT, "MAPS-Unified-Framework", "docs", "html",
                                        os.path.basename(MEMO.replace(".md", ".html")))),
    "已镜像到 docs/html/")

print("\n" + "=" * 92)
print("V 汇总：通过 {} 项，失败 {} 项".format(PASS, FAIL))
print("=" * 92)
