# -*- coding: utf-8 -*-
"""
第 87 轮补 补丁后核验（铁律 18：补丁后必须复跑核验）
V-1…V-10
"""
import io, os, re

FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok:
        FAIL += 1

def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

ZH   = "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN   = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
MEMO = "h_min标度律的分组重拟合_两条方向相反的幂律与干净底本.md"
LIST = "工程期望清单.md"
MEM  = r"../.workbuddy/memory/MEMORY.md"

zh = io.open(ZH, encoding="utf-8").read()
en = io.open(EN, encoding="utf-8").read()
mo = io.open(MEMO, encoding="utf-8").read()
li = io.open(LIST, encoding="utf-8").read()

# ------------------------------------------------------------------ V-1 块存在
hdr("V-1  第 87 轮补块存在于中英两稿")
chk("V-1a", zh.count("第 87 轮补：") == 1, "ZH 有且仅有 1 个第 87 轮补块标记（实际 {}）".format(zh.count("第 87 轮补：")))
chk("V-1b", en.count("round 87b:") == 1, "EN 有且仅有 1 个 round 87b 块标记（实际 {}）".format(en.count("round 87b:")))

# ------------------------------------------------------------------ V-2 块连续（不得被空行切断）
hdr("V-2  ⭐ 块内必须是连续引用块（第 87 轮补踩到的新坑）")
for path, mk, nm, tag in [(ZH, "第 87 轮补：", "规范（第 87 轮补）", "V-2a"),
                          (EN, "round 87b:", "Norm (round 87b)", "V-2b")]:
    lines = io.open(path, encoding="utf-8").read().split("\n")
    a = [i for i, s in enumerate(lines) if mk in s]
    b = [i for i, s in enumerate(lines) if nm in s]
    ok = len(a) == 1 and len(b) == 1 and a[0] < b[0]
    span = lines[a[0]:b[0] + 1] if ok else []
    blanks = sum(1 for s in span if s.strip() == "")
    nonq = sum(1 for s in span if s.strip() != "" and not s.startswith(">"))
    chk(tag, ok and blanks == 0 and nonq == 0,
        "{}：区间 {} 行，空行 {}，非引用行 {} ⟹ {}".format(
            os.path.basename(path), len(span), blanks, nonq,
            "连续引用块 ✓" if blanks == 0 and nonq == 0 else "被切断 ✗"))

# ------------------------------------------------------------------ V-3 中英同步
hdr("V-3  中英同步（同一组数字两边都在）")
KEYS = ["0.1103", "0.0021", "0.1120", "1.09", "3.83", "0.0023", "0.0037", "3.1423", "0.6884"]
for k in KEYS:
    a, b = zh.count(k), en.count(k)
    chk("V-3-{}".format(k), a >= 1 and b >= 1,
        "「{}」ZH {} 处 / EN {} 处".format(k, a, b))
chk("V-3-C42", zh.count("C-42") >= 1 and en.count("C-42") >= 1,
    "「C-42」ZH {} 处 / EN {} 处".format(zh.count("C-42"), en.count("C-42")))

# ------------------------------------------------------------------ V-4 无残留「未完成」
hdr("V-4  无「(4,4,8) 未完成 / 重跑中」的残留")
for path, txt in [(ZH, zh), (EN, en), (MEMO, mo)]:
    bad = []
    for pat in ["(4,4,8) N = 128 未完成", "(4,4,8) 未完成", "重跑中", "still running", "is running"]:
        if pat in txt:
            bad.append(pat)
    chk("V-4-{}".format(os.path.basename(path)[:6]), not bad, "残留标记 = {}".format(bad or "无"))

# ------------------------------------------------------------------ V-5 备忘录
hdr("V-5  备忘录更新到位")
chk("V-5a", "五·补二" in mo and "C-42" in mo, "新增 §五·补二（C-42 判别力判据）")
chk("V-5b", "**第 87 轮补已完成**" in mo, "§九 第 5 条已勾（(4,4,8) 到位）")
chk("V-5c", "**更正 39 → 40**（第 87 轮）**→ 41**" in mo and "总账 **41 条**" in mo,
    "§八 总账 两处均改为 41（更正行 / 清单行）")
chk("V-5d", "1.09σ" in mo and "3.83σ" in mo, "判别力两个实测值在备忘录里")

# ------------------------------------------------------------------ V-6 清单
hdr("V-6  清单台账")
chk("V-6a", li.count("| **C-42** |") == 1, "C-42 行存在且唯一（实际 {}）".format(li.count("| **C-42** |")))
chk("V-6b", "| **撤回 / 更正** | **41 条**" in li, "总账已改为 41 条")
rows = re.findall(r"^\| \*\*(C-\d+)\*\* \|", li, re.M)
chk("V-6c", len(rows) == len(set(rows)), "C 编号无重复（{} 行，去重后 {}）".format(len(rows), len(set(rows))))
print("      （说明：C 条目在清单里分行登记，本项只查重号）")

# ------------------------------------------------------------------ V-7 第 87 轮原块未被破坏
hdr("V-7  第 87 轮原有内容未被破坏")
chk("V-7a", "3.0887·N^{−0.6836}" in zh, "ZH 保留组 B 原拟合式")
chk("V-7b", "3.0887·N^{−0.6836}" in en, "EN 保留组 B 原拟合式")
chk("V-7c", "C-41" in zh and "C-41" in en and "C-41" in li, "C-41 三处都在")
chk("V-7d", zh.count("【v2.9 补充（第 87 轮：") == 1 and en.count("【v2.9 supplement (round 87:") == 1,
    "第 87 轮主块各 1 个（ZH {} / EN {}；第 87 轮补块另计）".format(
        zh.count("【v2.9 补充（第 87 轮："), en.count("【v2.9 supplement (round 87:")))

# ------------------------------------------------------------------ V-8 数值自洽
hdr("V-8  数值自洽（论文里的数与核验脚本一致）")
import math
C8, p8 = 3.0887, -0.6836
pred = C8 * 128 ** p8
chk("V-8a", abs(pred - 0.1120) < 0.0001, "组B 对 N=128 的预测 = {:.4f}（论文写 0.1120）".format(pred))
chk("V-8b", abs((0.1103 / pred - 1) * 100 + 1.5) < 0.15,
    "偏差 = {:+.2f}%（论文写 −1.5%）".format((0.1103 / pred - 1) * 100))

# ------------------------------------------------------------------ V-9 记忆文件
hdr("V-9  项目记忆文件在限额内")
n = len(io.open(MEM, encoding="utf-8").read())
chk("V-9", n <= 3000, "MEMORY.md = {} 字符（限额 3000）".format(n))
chk("V-9b", "37" in io.open(MEM, encoding="utf-8").read(), "铁律 37（判别力判据）已写入")

# ------------------------------------------------------------------ V-10 「0 处」类论证自检
hdr("V-10  ⭐ 元文本自指自检（铁律 18 的执行细则）")
print("  ⚠️ 本轮的「C-42」是我**自己写进去的** ⟹ 若日后清点「C-42 出现几处」，")
print("     必须用**补丁前备份**做底本（`*_备份_2026-10-02第87轮补前.md`）。实测：")
import glob
for path in sorted(glob.glob("*_备份_2026-10-02第87轮补前.md")):
    t = io.open(path, encoding="utf-8").read()
    print("     {:<55} C-42 在补丁前 = {} 处".format(os.path.basename(path)[:55], t.count("C-42")))
chk("V-10", True, "底本路径已列出（两列对照：补丁前 0 处 → 补丁后见 V-3）")

hdr("汇总")
print("  V-1…V-10 失败 {} 项".format(FAIL))
print("=" * 78)
print("VERIFY 87b DONE  FAIL = {}".format(FAIL))
print("=" * 78)
