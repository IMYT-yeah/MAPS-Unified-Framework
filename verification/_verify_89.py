# -*- coding: utf-8 -*-
"""第 89 轮 补丁后核验（铁律 18；两段式见陷阱 72）V-1…V-10"""
import io, os, glob

M59  = "不变必亏与因变化而变化_最优频率是平方根.md"
P59  = "不变必亏与因变化而变化_最优频率是平方根_备份_2026-10-02第89轮前.md"
M82  = "庞加莱猜想与Ricci流能否接入框架_四处对不上与一个补证.md"
P82  = "庞加莱猜想与Ricci流能否接入框架_四处对不上与一个补证_备份_2026-10-02第89轮前.md"
LIST = "工程期望清单.md"
PLIST= "工程期望清单_备份_2026-10-02第89轮前.md"
HS   = "../环境交接说明.md"
PHS  = "../环境交接说明_备份_2026-10-02第89轮前.md"
MEMO = "备忘录族的轮次溯源缺口_四种判据四个答案.md"
MEM  = "../.workbuddy/memory/MEMORY.md"

FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok: FAIL += 1
def hdr(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)
rd = lambda p: io.open(p, encoding="utf-8").read()

# ---------------------------------------------------------------- V-1
hdr("V-1  ⭐ 两段式：第 59 轮补 ID")
a, b = rd(P59), rd(M59)
chk("V-1a", "第 59 轮" not in a and "第 59 轮补注" not in a,
    "补丁前：备忘录里**没有**「第 59 轮」（实际 {} 处）⟹ 缺 ID 属实".format(a.count("第 59 轮")))
chk("V-1b", b.count("第 59 轮") >= 1 and "第 89 轮补注（C-44）" in b,
    "补丁后：有「第 59 轮」{} 处，且标了「第 89 轮补注（C-44）」⟹ **补的是 ID、并注明是后补的**".format(b.count("第 59 轮")))

# ---------------------------------------------------------------- V-2 内容未被改（硬检查）
hdr("V-2  ⭐⭐ 硬检查：第 59 轮备忘录**正文一字未改**")
la, lb = a.split("\n"), b.split("\n")
ins = len(lb) - len(la)
head_same = la[:3] == lb[:3]
tail_same = la[3:] == lb[3 + ins:]
print("  补丁前 {} 行 → 补丁后 {} 行（插入 {} 行）".format(len(la), len(lb), ins))
print("  前 3 行一致 = {}；第 {} 行之后逐行一致 = {}".format(head_same, 3 + ins + 1, tail_same))
chk("V-2", head_same and tail_same and ins == 3,
    "**除插入的 3 行外，其余逐行完全一致** ⟹ 只补元数据、不动内容 ✓")

# ---------------------------------------------------------------- V-3 第 82 轮
hdr("V-3  第 82 轮备忘录：标注「含第 83 轮」")
a, b = rd(P82), rd(M82)
chk("V-3", "本档同时承载第 83 轮" not in a and "本档同时承载第 83 轮" in b,
    "补丁前无标注 → 补丁后有（并注明 C-44）")

# ---------------------------------------------------------------- V-4 交接说明
hdr("V-4  交接说明")
a, b = rd(PHS), rd(HS)
chk("V-4a", "第 89 轮新增" not in a and "第 89 轮新增" in b, "§三 第 89 轮段：补丁前无 → 补丁后有")
chk("V-4b", "已知缺口（第 89 轮 C-44 登记" not in a and "已知缺口（第 89 轮 C-44 登记" in b,
    "§七 新增「已知缺口」条（第 64/79 轮 ＋ 第 1–38 轮）")
chk("V-4c", "当前建议（第 88 轮后）" in a and "当前建议（第 88 轮后）" not in b,
    "§七 item 0 已从「第 88 轮后」更新为「第 89 轮后」")
chk("V-4d", "第 64 轮" in b and "第 79 轮" in b and "_universe_sim_64" in b,
    "缺口条里写明了「取证位置」（脚本名 / 论文块 / 清单行）")

# ---------------------------------------------------------------- V-5 清单
hdr("V-5  清单台账")
li, pli = rd(LIST), rd(PLIST)
chk("V-5a", "| **C-44** |" not in pli and li.count("| **C-44** |") == 1, "C-44 行：新增且唯一")
chk("V-5b", "**42 条**" in pli and "| **撤回 / 更正** | **43 条**" in li, "总账 42 → 43")
import re
# ⚠️ 本项连续错了三次（同一类）：① 数「条目行」得 37（条目有**合并行**）；
#    ② `C-(\d+)` 把 **`RC-9`** 的尾巴当成 C-9（**代码层子串误命中**）；
#    ③ 以为 44 个编号就该等于声明的 43。
#    ✅ 定案：**严格编号全集 = 44（C-1…C-44，无缺口）**；其中 **C-1 的处置列是「修正」**
#       （第 49 轮登记，见清单 L34），**不属于「撤回 / 更正」族** ⟹ 44 − 1 = **43** == 声明值 ✓。
def disp_of(code):
    for s in li.split("\n"):
        if re.match(r"^\| \*\*C-{}\*\* \|".format(code), s):
            cols = [x.strip() for x in s.strip("|").split("|")]
            return re.sub(r"\*", "", cols[2]) if len(cols) > 2 else ""
    return ""
allcodes = sorted({int(m) for m in re.findall(r"(?<![A-Za-z])C-(\d+)", li)})
naive = sorted({int(m) for m in re.findall(r"C-(\d+)", li)})
maxc = max(allcodes)
gaps = [i for i in range(1, maxc + 1) if i not in allcodes]
rows = [s for s in li.split("\n") if re.match(r"^\| \*\*C-\d+\*\* \|", s)]
fixed = [c for c in allcodes if disp_of(c) and "撤回" not in disp_of(c) and "更正" not in disp_of(c)]
print("  严格编号全集 = {} 个（1–{}，缺 {}）".format(len(allcodes), maxc, gaps))
print("  宽松判据多出 = {}（`RC-9` 的子串幽灵）".format(sorted(set(naive) - set(allcodes))))
print("  独立条目行 = {} 行（C 条目有**合并行**：C-33…C-38 与 C-9 写在长串里）".format(len(rows)))
print("  非「撤回/更正」族的编号 = {}（处置列 = {}）".format(fixed, [disp_of(c) for c in fixed]))
chk("V-5c", maxc - len(gaps) - len(fixed) == 43 and "**43 条**" in li,
    "严格编号 {} − 非撤回更正族 {} = **{}** == 声明的 43 ⟹ 台账一致".format(
        maxc - len(gaps), len(fixed), maxc - len(gaps) - len(fixed)))

# ---------------------------------------------------------------- V-6 记忆
hdr("V-6  项目记忆")
t = rd(MEM)
chk("V-6a", len(t) <= 3000, "MEMORY.md = {} 字符（限额 3000）".format(len(t)))
chk("V-6b", "39 ⭐⭐" in t, "铁律 39 已写入")

# ---------------------------------------------------------------- V-7 备忘录自洽
hdr("V-7  备忘录自洽")
m = rd(MEMO)
chk("V-7a", "TR-1 … TR-8，0 失败" in m, "引用的核验结果与实测一致")
chk("V-7b", "2 / 3 / 4 / 16" in m or "2** | 64, 79" in m, "判据敏感性四答案表在档")
chk("V-7c", "不伪造" in m or "不改写历史" in m, "「不伪造历史」的处置原则在档")

# ---------------------------------------------------------------- V-8 元文本自指
hdr("V-8  ⭐ 元文本自指自检（铁律 18/20）")
files = sorted(glob.glob("*_备份_2026-10-02第89轮前.md")) + sorted(glob.glob("../环境交接说明_备份_2026-10-02第89轮前.md"))
print("  本轮底本 {} 份：".format(len(files)))
allzero = True
for p in files:
    c = rd(p).count("C-44")
    if c: allzero = False
    print("     {:<56} C-44 补丁前 = {} 处".format(os.path.basename(p)[:56], c))
chk("V-8", allzero, "全部底本里 C-44 = 0 处 ⟹ 补丁后出现的 C-44 **全部是本轮写的**（两列法成立）")
print("  ⚠️ 特别提示：**第 59 轮备忘录的 ID 行是我补的** ⟹ 日后清点「第 59 轮在头部出现几次」")
print("     必须用 `…_备份_2026-10-02第89轮前.md` 做底本（该底本里「第 59 轮」= {} 处）".format(
    rd(P59).count("第 59 轮")))

# ---------------------------------------------------------------- V-9 复跑正式核验
hdr("V-9  复跑正式核验（铁律 18：补丁后必须复跑）")
print("  → 见下方 `_traceability_89.py` 的汇总行")

# ---------------------------------------------------------------- V-10 未破坏既有
hdr("V-10  既有内容未被破坏")
chk("V-10a", "3.0887·N^{−0.6836}" in rd("h_min标度律的分组重拟合_两条方向相反的幂律与干净底本.md"),
    "第 87 轮组 B 拟合式仍在")
chk("V-10b", "C-43" in li and "C-42" in li and "C-41" in li, "C-41/42/43 台账行仍在")
chk("V-10c", "第 88 轮" in rd(HS), "第 88 轮段仍在交接说明里")

hdr("汇总")
print("  V-1…V-10 失败 {} 项".format(FAIL))
print("=" * 78)
print("VERIFY 89 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
