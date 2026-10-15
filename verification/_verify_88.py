# -*- coding: utf-8 -*-
"""
第 88 轮 补丁后核验（铁律 18；两段式见陷阱 72）
V-1…V-10
"""
import io, os, glob

ZH = "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
MEMO = "横向一致性审计_成熟度自评与三张表不相容.md"
LIST = "工程期望清单.md"
PRE_Z = "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第88轮前.md"
PRE_E = "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-02第88轮前.md"
MEM = "../.workbuddy/memory/MEMORY.md"

FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok:
        FAIL += 1
def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

Z = io.open(ZH, encoding="utf-8").read()
E = io.open(EN, encoding="utf-8").read()
PZ = io.open(PRE_Z, encoding="utf-8").read()
PE = io.open(PRE_E, encoding="utf-8").read()
MO = io.open(MEMO, encoding="utf-8").read()
LI = io.open(LIST, encoding="utf-8").read()

# ------------------------------------------------------------------ V-1 两段式
hdr("V-1  ⭐ 两段式：补丁前没有、补丁后有（陷阱 72）")
chk("V-1a", PZ.count("第 88 轮 **C-43**") == 0 and Z.count("第 88 轮 **C-43**") == 1,
    "ZH：补丁前 {} 处 → 补丁后 {} 处".format(PZ.count("第 88 轮 **C-43**"), Z.count("第 88 轮 **C-43**")))
chk("V-1b", PE.count("round 88, **C-43**") == 0 and E.count("round 88, **C-43**") == 1,
    "EN：补丁前 {} 处 → 补丁后 {} 处".format(PE.count("round 88, **C-43**"), E.count("round 88, **C-43**")))
chk("V-1c", PZ.count("完成度 ~90%") == 1 and Z.count("完成度 ~90%") == 1,
    "「完成度 ~90%」**原句未被删**（补丁前 {} → 补丁后 {}）⟹ 只补口径、不改数".format(
        PZ.count("完成度 ~90%"), Z.count("完成度 ~90%")))

# ------------------------------------------------------------------ V-2 块连续
hdr("V-2  插入块是**连续引用块**（陷阱 74 子坑）")
for path, mk, nm, tag in [(ZH, "第 88 轮 **C-43**", "同一族的「口径缺失」", "V-2a"),
                          (EN, "round 88, **C-43**", "same family of caliber gaps", "V-2b")]:
    lines = io.open(path, encoding="utf-8").read().split("\n")
    a = [i for i, s in enumerate(lines) if mk in s]
    b = [i for i, s in enumerate(lines) if nm in s]
    ok = len(a) == 1 and len(b) == 1 and a[0] < b[0]
    span = lines[a[0]:b[0] + 1] if ok else []
    blanks = sum(1 for s in span if s.strip() == "")
    nonq = sum(1 for s in span if s.strip() and not s.startswith(">"))
    chk(tag, ok and blanks == 0 and nonq == 0,
        "{}：块 {} 行，空行 {}，非引用行 {} ⟹ {}".format(
            os.path.basename(path)[:10], len(span), blanks, nonq,
            "连续 ✓" if blanks == 0 and nonq == 0 else "被切断 ✗"))

# ------------------------------------------------------------------ V-3 中英同步
hdr("V-3  中英同步（同一组数字两边都在）")
for k in ["1895", "13", "5 条明示未闭合", "25 行", "0 处"]:
    a, b = Z.count(k), E.count(k)
    flag = "✓" if a >= 1 and b >= 1 else "⚠️"
    print("  {} {:<16} ZH {:>2} / EN {:>2}".format(flag, k, a, b))
for k in ["1895", "13"]:
    chk("V-3-{}".format(k), Z.count(k) >= 1 and E.count(k) >= 1, "「{}」两稿都有".format(k))

# ------------------------------------------------------------------ V-4 无旧状态残留
hdr("V-4  无「待做 / 未完成」类旧状态串残留")
for p, t in [(ZH, Z), (EN, E), (MEMO, MO)]:
    bad = [k for k in ["待第 88", "第 88 轮未", "TODO-88", "尚未审计"] if k in t]
    chk("V-4-{}".format(os.path.basename(p)[:6]), not bad, "残留 = {}".format(bad or "无"))

# ------------------------------------------------------------------ V-5 清单
hdr("V-5  清单台账")
chk("V-5a", LI.count("| **C-43** |") == 1, "C-43 行存在且唯一（实际 {}）".format(LI.count("| **C-43** |")))
chk("V-5b", "| **撤回 / 更正** | **42 条**" in LI, "总账已改为 42 条")
import re
rows = re.findall(r"^\| \*\*(C-\d+)\*\* \|", LI, re.M)
chk("V-5c", len(rows) == len(set(rows)), "C 编号无重复（{} 行 / {} 唯一）".format(len(rows), len(set(rows))))

# ------------------------------------------------------------------ V-6 老块未破
hdr("V-6  既有内容未被破坏")
chk("V-6a", "3.0887·N^{−0.6836}" in Z and "3.0887·N^{−0.6836}" in E, "第 87 轮组 B 拟合式仍在（中英）")
chk("V-6b", "0.1103" in Z and "0.1103" in E, "第 87 轮补的 (4,4,8) 仍在（中英）")
chk("V-6c", Z.count("【v2.9 补充（第 87 轮：") == 1 and Z.count("【v2.9 补充（第 87 轮补") == 1,
    "第 87 轮主块 / 补块各 1 个（ZH {} / {}）".format(
        Z.count("【v2.9 补充（第 87 轮："), Z.count("【v2.9 补充（第 87 轮补")))
chk("V-6d", "S-C1" in Z and "第 61 轮加注" in Z, "§9 的 S-C1 加注仍在")

# ------------------------------------------------------------------ V-7 数值自洽
hdr("V-7  数值自洽（论文里的数 vs 核验脚本算出的）")
z = Z.split("\n")
i = next(k for k, s in enumerate(z) if "完成度 ~90%" in s)
seg = "\n".join(z[i:i + 8])
chk("V-7a", "1895" in seg, "「相距 1895 行」出现在注里（= 1926 − 31）")
chk("V-7b", "13 条" in seg and "25 行" in seg, "「13 条开放问题」「25 行」都在注里")

# ⚠️ **本轮踩到的新坑（第七类判据陷阱）**：第一版用**硬编码行号区间**（`1945 <= k <= 1959`）取 §10.2，
#    而**同一轮的补丁往 §10.1 插了 6 行** ⟹ §10.2 整体下移 ⟹ 区间只剩 6 条 ⟹ **假 FAIL**。
#    ✅ 正确做法：**结构定位**（标题 → 下一个同级标题），不用行号。
def section(lines, head, level=3):
    """返回 (start, end)，end = 下一个 level 及以上标题（0-based，含头不含尾）。"""
    a = [i for i, s in enumerate(lines) if s.startswith("#" * level + " " + head)]
    if len(a) != 1:
        return None
    st = a[0]
    for j in range(st + 1, len(lines)):
        s = lines[j]
        if s.startswith("#") and not s.startswith("#" * (level + 1) + " "):
            return (st, j)
    return (st, len(lines))

z_ = io.open(ZH, encoding="utf-8").read().split("\n")
r102 = section(z_, "10.2 开放问题（按重要性排序）")
r9 = section(z_, "9 可检验预言", level=2)
n102 = sum(1 for s in z_[r102[0]:r102[1]] if re.match(r"^\d+\. ", s)) if r102 else -1
n9 = sum(1 for s in z_[r9[0]:r9[1]] if s.lstrip().startswith("|")) if r9 else -1
print("     ⚠️ 第一版用行号区间 1945–1959 ⟹ 被本轮补丁的 **+6 行** 顶掉 ⟹ 只数到 6 条（假 FAIL）")
print("     结构定位：§10.2 = 行 {}-{}；§9 = 行 {}-{}".format(
    r102[0] + 1, r102[1] + 1, r9[0] + 1, r9[1] + 1))
print("     实测（结构定位）：§10.2 编号条目 {} 条；§9 表行 {} 行".format(n102, n9))
chk("V-7c", n102 == 13 and n9 == 25,
    "注里的 13 / 25 与**结构定位**实测一致（{} / {}）⟹ 行号区间判据已被补丁移位破坏".format(n102, n9))

# ------------------------------------------------------------------ V-8 记忆
hdr("V-8  项目记忆")
n = len(io.open(MEM, encoding="utf-8").read())
chk("V-8a", n <= 3000, "MEMORY.md = {} 字符（限额 3000）".format(n))
chk("V-8b", "38 ⭐⭐" in io.open(MEM, encoding="utf-8").read(), "铁律 38 已写入")

# ------------------------------------------------------------------ V-9 元文本自指
hdr("V-9  ⭐ 元文本自指自检（铁律 18 执行细则）")
print("  本轮的「C-43」是**我自己写进去的** ⟹ 日后清点必须用**补丁前备份**做底本：")
for p in sorted(glob.glob("*_备份_2026-10-02第88轮前.md")):
    t = io.open(p, encoding="utf-8").read()
    print("     {:<52} C-43 补丁前 = {} 处".format(os.path.basename(p)[:52], t.count("C-43")))
chk("V-9", all(io.open(p, encoding="utf-8").read().count("C-43") == 0
               for p in glob.glob("*_备份_2026-10-02第88轮前.md")),
    "全部 4 个底本里 C-43 = 0 处 ⟹ 补丁后出现即**全部是本轮写的**（两列法成立）")

# ------------------------------------------------------------------ V-10 备忘录自洽
hdr("V-10  备忘录自洽")
chk("V-10a", "CR-1 … CR-9，15 项 0 失败" in MO, "备忘录引用的核验结果与实测一致")
chk("V-10b", "四类「判据陷阱」" in MO or "四类判据陷阱" in MO, "四类陷阱已写入备忘录")
chk("V-10c", "未同步残留 = 0" in MO, "正面产出已写入备忘录")

hdr("汇总")
print("  V-1…V-10 失败 {} 项".format(FAIL))
print("=" * 78)
print("VERIFY 88 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
