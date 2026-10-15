# -*- coding: utf-8 -*-
"""第 96 轮补丁后核验（V-1…V-8，两段式；底本 = 重演版第 96 轮前备份）。"""
import io, os, subprocess, sys

base = os.path.dirname(os.path.abspath(__file__))
B = lambda p: io.open(p, encoding="utf-8").read()

LI = os.path.join(base, "项目台账.md")
LI0 = os.path.join(base, "项目台账_备份_2026-10-02第96轮前.md")
HH = os.path.join(base, "..", "环境说明.md")
HH0 = os.path.join(base, "..", "环境说明_备份_2026-10-02第96轮前.md")
LI_c, LI_p = B(LI), B(LI0)
HH_c, HH_p = B(HH), B(HH0)

ok = 0; bad = 0
def chk(tag, cond, msg):
    global ok, bad
    if cond: ok += 1; print("  [OK] {:<6} {}".format(tag, msg))
    else: bad += 1; print("  [XX] {:<6} {}".format(tag, msg))

print("=" * 100)
print("V-1  清单总账计数（底本 54 → 当前 55；负面 39 → 40 复核）")
chk("V-1a", LI_p.count("| **撤回 / 更正** | **54 条**") == 1 and LI_c.count("| **撤回 / 更正** | **55 条**") == 1,
    "更正 54 → **55 条**（C-56 入账）")
chk("V-1b", LI_p.count("| **负面判定** | **40 条**") == 1 and LI_c.count("| **负面判定** | **40 条**") == 1,
    "负面保持 **40 条**（本轮无新负面）")

print()
print("V-2  清单本轮七处改动（底本无 / 当前有）")
for tag, key, name in [
    ("V-2a", "✅ 第 96 轮文件层结项", "剩余待办行①：A1 结项（含文件层）"),
    ("V-2b", "「需那台有 Lean 的机器」已改判", "行③：改判为本机重建"),
    ("V-2c", "| **A1 ✅** |", "台账 A1 ✅ 行"),
    ("V-2d", "| **C-56** |", "台账 C-56 行"),
    ("V-2e", "组 VI**：A1 ✅ **Lean 资产恢复（第 96 轮）**", "组 VI 行"),
]:
    chk(tag, LI_p.count(key) == 0 and LI_c.count(key) >= 1,
        "{}：「{}」底本 {} → 当前 {}".format(name, key[:26], LI_p.count(key), LI_c.count(key)))

print()
print("V-3  交接说明两处（底本无 / 当前有）")
chk("V-3a", HH_p.count("第 96 轮新增") == 0 and HH_c.count("第 96 轮新增") >= 1, "§三 第 96 轮段 ✓")
chk("V-3b", HH_p.count("当前建议（第 96 轮后）") == 0 and HH_c.count("当前建议（第 96 轮后）") >= 1, "§七 新建议 ✓")
chk("V-3c", HH_c.count("（历史，第 95 轮后，已被上式取代）") == 1, "旧建议已标历史 ✓")

print()
print("V-4  diff 规模卫兵（清单/交接：改动应集中在已知位置）")
import difflib
def diffstat(a, b, name):
    d = list(difflib.unified_diff(a.split("\n"), b.split("\n"), lineterm=""))
    add = sum(1 for s in d if s.startswith("+") and not s.startswith("+++"))
    rem = sum(1 for s in d if s.startswith("-") and not s.startswith("---"))
    return add, rem
a1, r1 = diffstat(LI_p, LI_c, "清单")
a2, r2 = diffstat(HH_p, HH_c, "交接")
chk("V-4a", r1 <= 14 and a1 <= 24, "清单：+{} / −{} 行（预期 ≤24/≤14：7 处替换 + 2 行插入）".format(a1, r1))
chk("V-4b", r2 <= 5 and a2 <= 16, "交接：+{} / −{} 行（预期 ≤16/≤5：两段插入 + 1 行替换）".format(a2, r2))

print()
print("V-5  lean 目录五文件 + 工具链（复跑 LA 核验）")
r = subprocess.run([sys.executable, os.path.join(base, "_lean_a1_96.py")],
                   capture_output=True, text=True, encoding="utf-8")
last = [s for s in r.stdout.split("\n") if "通过" in s and "失败" in s]
chk("V-5", bool(last) and "失败 0 项" in last[-1], "复跑 LA：{}".format(last[-1] if last else "（无汇总）"))

print()
print("V-6  MEMORY 限额")
mem = os.path.join(base, "..", ".workbuddy", "memory", "MEMORY.md")
t = B(mem)
chk("V-6", len(t) <= 3000 and "进度：96" in t and "资产恢复规范" in t,
    "MEMORY = {} 字符（≤3000 ✓；含进度 96 与铁律 42）".format(len(t)))

print()
print("V-7  第 96 轮前备份存在性（重演版）")
chk("V-7", os.path.exists(LI0) and os.path.exists(HH0),
    "两份备份在档（重演版：由第 95 轮前备份 + _patch_95.py 重演；本轮疏漏的正规备份的补救）")

print()
print("V-8  恢复产物关键行抽查")
S = B(os.path.join(base, "..", "MAPS-Unified-Framework", "verification", "lean", "StormPoC.lean"))
chk("V-8a", "重建版 v2" in S and "分级标注" in S, "StormPoC.lean 头部（重建版 v2 + 分级）✓")
chk("V-8b", "未经重新编译" in S, "诚实边界（未经编译）在档 ✓")

print()
print("=" * 100)
print("补丁后核验：通过 {} 项，失败 {} 项".format(ok, bad))
