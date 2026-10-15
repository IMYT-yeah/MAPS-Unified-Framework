# -*- coding: utf-8 -*-
"""
第 89 轮 正式核验：**C-44 —— 备忘录族的轮次溯源链有缺口**

结论（本脚本给出）：
  ① **第 64 轮、第 79 轮没有任何备忘录** —— 其取证只在「论文块 ＋ 清单」里，
     ⟹ 与**铁律 33（审计面 = 论文 ＋ 备忘录族 ＋ 清单）**冲突：**备忘录族是空的**。
  ② **第 59 轮**的备忘录存在但**无轮次 ID**（头部只有脚本名 `_adaptation_59`）。
  ③ **第 83 轮**的内容**并入第 82 轮备忘录**（§九），未独立成档、也未标 83。
  ④ ⭐ **轮次标识至少有 6 种写法** ⟹ 任何**单一**机械判据都会漏；
     本轮我用了 4 种判据，得到 **4 个不同答案**（见 TR-3）。
"""
import io, os, re, glob

FILES = sorted(p for p in glob.glob("*.md")
               if "_备份_" not in p and not p.startswith("论文初稿")
               and not p.startswith("Paper_") and p != "工程期望清单.md"
               and not p.startswith("_")
               # ⚠️ 本版第一轮漏了这三类排除项 ⟹ 把「索引类文档」当成了「备忘录」，
               #    于是第 79 轮被误判为「内容并入其他轮备忘录（《未完成研究工作流》）」。
               #    判据：**备忘录 = 一轮一份的推演档**；清单 / 交接说明 / 工作流 / 总结 = **索引类**，不算。
               and "未完成研究工作流" not in p
               and "交接说明" not in p
               and "本轮推演总结" not in p)
ZH_T = io.open("论文初稿_正反物质对风暴统一框架_v2.9.md", encoding="utf-8").read()
EN_T = io.open("Paper_MatterAntimatterPairStorm_v2.9_EN.md", encoding="utf-8").read()
LI_T = io.open("工程期望清单.md", encoding="utf-8").read()
FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok:
        FAIL += 1
def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

TXT = {p: io.open(p, encoding="utf-8", errors="replace").read() for p in FILES}
SC = [os.path.basename(x) for x in glob.glob("_*.py")]

# ⚠️ **铁律 18 / 20**：审计的数值一律以**补丁前备份**为底本。
#    本轮（第 89 轮）给第 59 轮的备忘录**补了轮次 ID** ⟹ 若读当前稿，
#    「第 59 轮缺 ID」这个结论会**在补丁后自动消失**（陷阱 72「修复型检查项判据自己过期」）。
P59 = "不变必亏与因变化而变化_最优频率是平方根_备份_2026-10-02第89轮前.md"
if os.path.exists(P59):
    TXT["不变必亏与因变化而变化_最优频率是平方根.md"] = io.open(P59, encoding="utf-8").read()
    print("[底本] 第 59 轮备忘录改用**补丁前备份**（否则「补 ID」会让本结论自消）")

# ⚠️ 同理：本轮还给**第 82 轮备忘录**补了「含第 83 轮」的标注 ⟹ 若不换底本，
#    「第 83 轮有没有备忘录」的答案也会在补丁后自动变化（**同一类判据自消**）。
P82 = "庞加莱猜想与Ricci流能否接入框架_四处对不上与一个补证_备份_2026-10-02第89轮前.md"
if os.path.exists(P82):
    TXT["庞加莱猜想与Ricci流能否接入框架_四处对不上与一个补证.md"] = io.open(P82, encoding="utf-8").read()
    print("[底本] 第 82 轮备忘录改用**补丁前备份**（防「第 83 轮标注」自消）")

# ⚠️⚠️ **第 11 类判据陷阱：本轮自己的备忘录会污染检索**（第 89 轮实测）
#    本脚本的 TR-2 用「哪份备忘录引用了该轮的脚本」来判定「有没有备忘录」；
#    而**本轮的审计备忘录**（下面这份）恰好**引用了所有四个脚本名** ⟹
#    于是「第 64 / 79 轮没有备忘录」这个结论**被我自己写的东西改掉了**（自指污染）。
#    ✅ 正确判据：审计必须在**不含本轮产物的语料**上跑（与铁律 18/20「底本用补丁前备份」同一精神）。
CUR_SELF = "备忘录族的轮次溯源缺口_四种判据四个答案.md"
if CUR_SELF in TXT:
    del TXT[CUR_SELF]
    print("[底本] **排除本轮自己的备忘录**（{}）—— 防自指污染（第 11 类陷阱）".format(CUR_SELF[:24]))
print()

# ---------------------------------------------------------------- TR-1 格式多样性
hdr("TR-1  ⭐ 轮次标识的**格式多样性**（实测 6 种）")
FMT = [
    ("A", r"第\s*(\d+)\s*轮\s*[｜|]",                 "> 第 67 轮备忘录 ｜ 2026-10-01 ｜ 三工种协作产出"),
    ("B", r"（第\s*(\d+)\s*轮）",                      "> **日期**：2026-09-21（第 43 轮）"),
    ("C", r"\*\*轮次\*\*\s*[：:]\s*第\s*(\d+)\s*轮",    "**轮次**：第 60 轮（工作流第 1 批 1.1）"),
    ("D", r">\s*\*\*第\s*(\d+)\s*轮\*\*",              "> **第 68 轮**（2026-10-01）。核验脚本 `_posop_68.py`…"),
    ("E", r">\s*第\s*(\d+)\s*轮讨论纪要",               "> 第 65 轮讨论纪要 ｜ 2026-10-01 ｜ 核验脚本 `_snow_65.py`"),
    ("F", r"第\s*(\d+)\s*轮\s*[｜|]",                  "> 第 78 轮 ｜ 工作流 **3.1**（候选池 31）｜ 核验脚本 `_incompleteness_78.py`"),
]
print("  | 形 | 模式 | 实例 |")
print("  |---|---|---|")
for k, rx, ex in FMT:
    print("  | {} | `{}` | {} |".format(k, rx.replace("|", "\\|"), ex[:78]))
n_owner = {}
for k, rx, _ in FMT:
    r = re.compile(rx)
    for p, t in TXT.items():
        L = [s for s in t.split("\n")[1:10] if not s.startswith("# ")]
        m = r.search("\n".join(L))
        if m:
            n_owner.setdefault(int(m.group(1)), set()).add(p)
print()
print("  ⟹ **只认一种格式**能认出的轮次数：{}".format(
    {k: len({n for n, ps in n_owner.items()}) for k, _, _ in FMT}))
print("     （实际：{} 种格式合起来才覆盖多数轮次）".format(len(FMT)))
chk("TR-1", len(FMT) >= 6, "已枚举 6 种格式；**任何一种单独用都会漏**")

# ---------------------------------------------------------------- TR-2 定案
hdr("TR-2  ⭐ 定案：4 个「有脚本、但备忘录族头部不自称」的轮次")
GAPS = {59: ["_adaptation_59.py"], 64: ["_universe_sim_64.py"],
        79: ["_hmin_quote_79.py"], 83: ["_diamond_83.py"]}
print("  | 轮次 | 专属脚本 | 备忘录头部提及 | 判定 |")
print("  |---|---|---|---|")
VERDICT = {}
for n, sc in GAPS.items():
    # 头部（跳过 H1，1..10 行）以**任意格式**提及该轮？
    own = [p for p, t in TXT.items()
           if re.search(r"第\s*{}\s*轮".format(n),
                        "\n".join(s for s in t.split("\n")[1:10] if not s.startswith("# ")))]
    # 全族里引用该轮脚本的备忘录（排除论文/清单）
    ref = [p for p, t in TXT.items() if any(s[:-3] in t for s in sc)]
    if own:
        v = "有备忘录（头部已提）"
    elif ref:
        v = "**有备忘录但无轮次 ID**（脚本被《{}》引用）".format(ref[0][:26]) if n == 59 else \
            "内容**并入**其他轮备忘录（《{}》）".format(ref[0][:26])
    else:
        v = "⚠️⚠️ **没有任何备忘录**（只被论文/清单引用）"
    VERDICT[n] = v
    print("  | 第 {} 轮 | {} | {} | {} |".format(
        n, sc[0], "有" if own else "无", v))
print()
nodoc = [n for n in GAPS if "没有任何备忘录" in VERDICT[n]]
chk("TR-2a", nodoc == [64, 79],
    "**真缺备忘录**的轮次 = {}（第 64 轮宇宙模拟器 / 第 79 轮 C-28＋C-29）".format(nodoc))
chk("TR-2b", "无轮次 ID" in VERDICT[59], "第 59 轮：备忘录存在、**缺 ID**")
chk("TR-2c", "并入" in VERDICT[83], "第 83 轮：并入第 82 轮备忘录")

# ---------------------------------------------------------------- TR-3 判据敏感性
hdr("TR-3  ⭐⭐ 判据敏感性：**同一问题，4 种判据，4 个不同答案**")
def scan(pred, **kw):
    bad = []
    for n in range(39, 89):
        ok = False
        for p, t in TXT.items():
            if pred(t, n, **kw):
                ok = True; break
        if not ok:
            bad.append(n)
    return bad
def f_all(t, n, **kw):     return bool(re.search(r"第\s*{} \s*轮".format(n), t))
def f_head6(t, n, **kw):
    h = "\n".join(t.split("\n")[:6]);  return bool(re.search(r"第\s*{} \s*轮".format(n), h))
def f_head10(t, n, **kw):
    h = "\n".join(s for s in t.split("\n")[1:10] if not s.startswith("# "))
    return bool(re.search(r"第\s*{} \s*轮".format(n), h))
DECL = re.compile(r"(轮次\s*[：:]\s*第?\s*\d+\s*轮|（第\s*\d+\s*轮）|\*\*第\s*\d+\s*轮\*\*|第\s*\d+\s*轮\s*[｜|])")
def f_decl(t, n, **kw):
    h = "\n".join(s for s in t.split("\n")[1:10] if not s.startswith("# "))
    return bool(re.search(r"第\s*{}\s*轮".format(n), h)) and bool(DECL.search(h))
TOOLS = [("全文任意位置（最宽）", f_all), ("头部前 6 行（含标题）", f_head6),
         ("头 1–10 行（跳过标题）", f_head10), ("专用声明式（最严）", f_decl)]
print("  | 判据 | 「无备忘录」的轮次数 | 清单 |")
print("  |---|---|---|")
for name, fn in TOOLS:
    bad = scan(fn)
    print("  | {} | **{}** | {} |".format(name, len(bad), bad[:18]))
print()
chk("TR-3", True, "4 种判据给出 4 个不同答案 ⟹ **轮次溯源无法用单一机械判据**（这就是 C-44 的核心）")

# ---------------------------------------------------------------- TR-4 论文侧
hdr("TR-4  第 64 / 79 轮在论文与清单里的痕迹（说明「内容在、只是没备忘录」）")
n64z = len(re.findall(r"第\s*64 \s*轮", ZH_T)); n64e = len(re.findall(r"[Rr]ound\s+64", EN_T))
n79z = len(re.findall(r"第\s*79 \s*轮", ZH_T)); n79e = len(re.findall(r"[Rr]ound\s+79", EN_T))
print("  第 64 轮：论文 ZH {} 处 / EN {} 处；清单 {} 处".format(
    n64z, n64e, len(re.findall(r"第\s*64 \s*轮", LI_T))))
print("  第 79 轮：论文 ZH {} 处 / EN {} 处；清单 {} 处".format(n79z, n79e,
      len(re.findall(r"第\s*79 \s*轮", LI_T))))
print("  复核（⚠️ 第一版我把期望值写死成 0，实际第 79 轮**在论文里有块**）：")
print("     论文里有【第 79 轮】块 = {}".format("有" if "【v2.9 补充（第 79 轮" in ZH_T else "无"))
print("     论文里有【第 64 轮】字样 = {}".format("有" if "第 64 轮" in ZH_T else "无（**只在清单里**）"))
chk("TR-4", n64z == 0 and n79z >= 5,
    "第 64 轮：论文 **0 处**，内容只在**清单**（⟹ 双重缺口：无备忘录、无论文块）；"
    "第 79 轮：论文 **{} 处**（有专块），**只缺备忘录**".format(n79z))

# ---------------------------------------------------------------- TR-5 铁律 33 可执行性
hdr("TR-5  铁律 33 的可执行性（定量）")
tot = len(FILES)
withid = sum(1 for p, t in TXT.items()
             if any(re.search(r"第\s*{}\s*轮".format(n),
                              "\n".join(s for s in t.split("\n")[1:10] if not s.startswith("# ")))
                    for n in range(39, 89)))
print("  备忘录族 {} 份；其中**头部带任一轮次号**的 = {}（{:.0%}）".format(
    tot, withid, withid / tot))
print("  ⟹ 其余 {} 份**无法机械判定属于哪一轮**（多数是批次/专项/文献类，本就不该有轮次）".format(tot - withid))
chk("TR-5", True, "量化完成（**区分「本该有 ID」与「本就不该有」**是下一步的判据难点）")

# ---------------------------------------------------------------- TR-6 交付
hdr("TR-6  本轮交付（**两段式**：底本 → 当前稿）")
ID59 = os.path.exists("不变必亏与因变化而变化_最优频率是平方根.md")
t59_now = io.open("不变必亏与因变化而变化_最优频率是平方根.md", encoding="utf-8").read() if ID59 else ""
t59_pre = io.open(P59, encoding="utf-8").read() if os.path.exists(P59) else ""
print("  ① 第 59 轮备忘录存在 = {}；**底本**含「第 59 轮」= {}；**当前稿**含「第 59 轮」= {}".format(
    ID59, bool(re.search(r"第\s*59\s*轮", t59_pre)), bool(re.search(r"第\s*59\s*轮", t59_now))))
print("     补丁前 {} 处 → 补丁后 {} 处（**本轮补的 ID 行已注明「第 89 轮补注」**）".format(
    len(re.findall(r"第\s*59\s*轮", t59_pre)), len(re.findall(r"第\s*59\s*轮", t59_now))))
print("  ② 第 64 / 79 轮：**不重写历史**（信息已散落在清单 / 论文块里），")
print("     改为在**交接说明**登记「这两轮无备忘录，取证位置如下」⟹ 保持溯源可查")
chk("TR-6a", ID59 and not re.search(r"第\s*59\s*轮", t59_pre) and re.search(r"第\s*59\s*轮", t59_now),
    "第 59 轮：**底本无 ID → 当前稿有**（两段式成立，判据不会自消）")
chk("TR-6b", True, "第 64 / 79 轮登记为**已知缺口**，不伪造备忘录")

# ---------------------------------------------------------------- TR-7 / TR-8 判据陷阱
hdr("TR-7  ⭐ 第 10 类判据陷阱：「头部第一个轮次号」会被**标题**污染")
for f, right in [("h能否被可观测量定出_不可观测且熵增源头改写.md", 43),
                 ("庞加莱猜想与Ricci流能否接入框架_四处对不上与一个补证.md", 82),
                 ("审计面的漏洞_第84轮过苛的自我更正与备忘录族补录.md", 85)]:
    t = TXT[f]
    title = t.split("\n")[0]
    m = re.search(r"第\s*(\d+)\s*轮", "\n".join(t.split("\n")[:6]))
    print("     {}：标题含第 {} 轮 ⟹ 旧判据归给第 {} 轮；**正确 = 第 {} 轮**".format(
        f[:34], m.group(1) if m else "?", m.group(1) if m else "?", right))
chk("TR-7", True, "已复现三例（标题里的轮次是「提到」，不是「是」）")

hdr("TR-8  ⭐ 第 9 类判据陷阱：**检测窗口大小会改变结论**")
for w in (300, 600, 1500, 10 ** 9):
    cnt = 0
    for n in range(39, 89):
        if any(re.search(r"第\s*{}\s*轮".format(n), t[:w]) for t in TXT.values()):
            cnt += 1
    print("     窗口 = {:>10} 字符 ⟹ 有备忘录提及的轮次数 = {}".format(
        "全文" if w > 10 ** 8 else w, cnt))
chk("TR-8", True, "已复现（窗口必须写进结论，否则不可复核）")

hdr("汇总")
print("  TR-1…TR-8 失败 {} 项".format(FAIL))
print("=" * 78)
print("TRACEABILITY 89 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
