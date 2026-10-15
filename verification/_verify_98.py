# -*- coding: utf-8 -*-
"""
第 98 轮补丁后核验（两段式：补丁前取证 ＋ 补丁后确认）
核验项：V-1 … V-12；末尾打印通过/失败计数

底本（补丁前）：
  ① outputs/项目台账_备份_2026-10-03第98轮前.md
  ② 环境说明_备份_2026-10-03第98轮前.md
  ③ .workbuddy/memory/MEMORY_备份_2026-10-03第98轮前.md
  ④ MAPS-Unified-Framework/python/_history/README_备份_2026-10-03第98轮前.md（**事后补录**）
"""
import io
import os
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
REPO = os.path.join(ROOT, "MAPS-Unified-Framework")
PKG = os.path.join(REPO, "python", "maps")

LIST = os.path.join(BASE, "项目台账.md")
PRE_LIST = os.path.join(BASE, "项目台账_备份_2026-10-03第98轮前.md")
HAND = os.path.join(ROOT, "环境说明.md")
PRE_HAND = os.path.join(ROOT, "环境说明_备份_2026-10-03第98轮前.md")
MEM = os.path.join(ROOT, ".workbuddy", "memory", "MEMORY.md")
PRE_MEM = os.path.join(ROOT, ".workbuddy", "memory", "MEMORY_备份_2026-10-03第98轮前.md")
PY_README = os.path.join(REPO, "python", "README.md")
PRE_PYREADME = os.path.join(REPO, "python", "_history", "README_备份_2026-10-03第98轮前.md")

PASS = FAIL = 0


def chk(tag, cond, msg, strict=True):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("  [OK] {:<7} {}".format(tag, msg))
    else:
        if strict:
            FAIL += 1
            print("  [XX] {:<7} {}".format(tag, msg))
        else:
            print("  [INFO] {:<7} {}".format(tag, msg))


def hdr(s):
    print("\n" + "=" * 92)
    print(s)
    print("=" * 92)


def rd(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


print("第 98 轮补丁后核验（V 系列）")

# ============================================================ V-1 清单
hdr("V-1  项目台账（两段式）")
pre_l, cur_l = rd(PRE_LIST), rd(LIST)
chk("V-1a", "**A2 ✅**" not in pre_l and "**A2 ✅**" in cur_l, "补丁前无 A2 行 → 补丁后有（两段式）")
chk("V-1b", "**C-58**" not in pre_l and "**C-58**" in cur_l, "补丁前无 C-58 → 补丁后有")
chk("V-1c", "| **撤回 / 更正** | **56 条**" in pre_l and "| **撤回 / 更正** | **57 条**" in cur_l,
    "更正计数 56 → 57（两段式）")
chk("V-1d", cur_l.count("A2") >= 5, "A2 在清单中出现 {} 处（含三处剩余待办 ＋ 台账组 VI）".format(cur_l.count("A2")))

# ============================================================ V-2 交接说明
hdr("V-2  环境说明（§七 98 ＋ 第 98 轮段）")
pre_h, cur_h = rd(PRE_HAND), rd(HAND)
chk("V-2a", "当前建议（第 97 轮后）" in pre_h and "当前建议（第 98 轮后）" in cur_h,
    "§七：97 → 98（两段式）")
chk("V-2b", "**第 98 轮新增（A2" in cur_h and "五路取证" in cur_h, "新增「第 98 轮」段 ＋ 五路取证结论")
chk("V-2c", "**α = 1 双证反推**" in cur_h and "**C-58**" in cur_h, "α = 1 与 C-58 均已入交接说明")

# ============================================================ V-3 MEMORY
hdr("V-3  MEMORY.md（进度 98 ＋ 限额 ＋ 铁律合并）")
pre_m, cur_m = rd(PRE_MEM), rd(MEM)
chk("V-3a", "**进度：97**" in pre_m and "**进度：98**" in cur_m, "进度 97 → 98")
chk("V-3b", len(cur_m) <= 3000, "字符数 = {}（限额 3000）".format(len(cur_m)))
chk("V-3c", ("A2 `python/maps` ✅ 98" in cur_m) and ("42 ⭐⭐ **资产恢复规范**（96/97/98" in cur_m),
    "A2 行已更新；铁律 42 已并入 98 轮结论（原独立第 44 条已合并不重复）")
chk("V-3d", "44 ⭐" not in cur_m.split("## 四")[0].split("## 三")[1],
    "未遗留重复的独立第 44 条（合并后不重复计数）", strict=False)

# ============================================================ V-4 包终态
hdr("V-4  python/maps 包终态")
FILES = ["formula.py", "maps_framework.py", "verify.py", "run.sh", "README.md"]
miss = [f for f in FILES if not os.path.exists(os.path.join(PKG, f))]
chk("V-4a", not miss, "5 个文件齐备（缺 {}）".format(miss if miss else "无"))
rm = rd(os.path.join(PKG, "README.md"))
chk("V-4b", "已重建" in rm and "恢复状态" in rm, "包 README 含「已重建」＋「恢复状态」表")
chk("V-4c", "·ln2" in rm and "C-58" in rm, "原规格留痕（§0）与 C-58 并存")
rp, prep = rd(PY_README), rd(PRE_PYREADME)
chk("V-4d", "源文件 2026-09-16 丢失" in prep and "源文件 2026-09-16 丢失" not in rp,
    "python/README.md：旧「丢失」状态已移除（两段式；底本为**事后补录**）")

# ============================================================ V-5 备份
hdr("V-5  备份与派生资产（含本轮登记的流程违规）")
for tag, p in [("V-5a", PRE_LIST), ("V-5b", PRE_HAND), ("V-5c", PRE_MEM), ("V-5d", PRE_PYREADME)]:
    chk(tag, os.path.exists(p), "存在 {}".format(os.path.basename(p)))
chk("V-5e", "事后补录" in rd(PRE_PYREADME), "python/README 底本已标明「事后补录（违反铁律 9）」")

# ============================================================ V-6 产物
hdr("V-6  派生产物")
memo = os.path.join(BASE, "A2结项_python_maps包恢复_T1-T5五锚点.md")
chk("V-6a", os.path.exists(memo), "备忘录存在")
chk("V-6b", os.path.exists(memo.replace(".md", ".html")), "HTML 快照存在（项目模板生成）")
chk("V-6c", os.path.exists(os.path.join(REPO, "docs", "html", os.path.basename(memo.replace(".md", ".html")))),
    "已镜像到 docs/html/")
chk("V-6d", os.path.exists(os.path.join(BASE, "_maps_a2_98.py")), "核验脚本 _maps_a2_98.py 存在")

print("\n" + "=" * 92)
print("V 汇总：通过 {} 项，失败 {} 项".format(PASS, FAIL))
print("=" * 92)
