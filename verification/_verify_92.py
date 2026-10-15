# -*- coding: utf-8 -*-
"""第 92 轮 补丁后核验（铁律 18；两段式见陷阱 72）V-1…V-10"""
import io, os, re, glob

ZH  = "论文初稿_正反物质对风暴统一框架_v2.9.md"
PZH = "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第92轮前.md"
EN  = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
PEN = "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-02第92轮前.md"
LIST= "项目台账.md"
PLIST="项目台账_备份_2026-10-02第92轮前.md"
HS  = "../环境说明.md"
PHS = "../环境说明_备份_2026-10-02第92轮前.md"
MEM = "../.workbuddy/memory/MEMORY.md"
FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok: FAIL += 1
def hdr(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)
rd = lambda p: io.open(p, encoding="utf-8").read()
zt, et = rd(ZH), rd(EN)
pzt, pet = rd(PZH), rd(PEN)

# ---------------------------------------------------------------- V-1 两段式
hdr("V-1  ⭐ 两段式：第 55 轮归属注")
KZ, KE = "第 92 轮归属注（C-47）", "Round-92 attribution note (C-47)"
chk("V-1a", KZ not in pzt and zt.count(KZ) == 1, "ZH：{} → {}".format(pzt.count(KZ), zt.count(KZ)))
chk("V-1b", KE not in pet and et.count(KE) == 1, "EN：{} → {}".format(pet.count(KE), et.count(KE)))

# ---------------------------------------------------------------- V-2 缺口已消
hdr("V-2  ⭐⭐ 缺口的量化证据：块内关键词由「各 0 处」变「有」")
def block55(t):
    lines = t.split("\n")
    a = [i for i, s in enumerate(lines) if "第 55 轮" in s and "【v2.9" in s][0]
    b = next((i for i in range(a + 1, len(lines))
              if lines[i].startswith("#") or "【v2.9" in lines[i]), len(lines))
    return "\n".join(lines[a:b])
pre, now = block55(pzt), block55(zt)
for w in ["储能", "电池", "化学", "判否", "不覆盖", "零内容"]:
    print("     块内「{}」：补丁前 {} → 补丁后 {}".format(w, pre.count(w), now.count(w)))
chk("V-2", all(pre.count(w) == 0 for w in ["储能", "电池", "化学", "判否", "不覆盖", "零内容"])
           and all(now.count(w) >= 1 for w in ["储能", "电池", "化学", "判否", "不覆盖", "零内容"]),
    "六词全部「补丁前 0 → 补丁后 ≥1」⟹ **该轮的核心判否现在有了归属**")

# ---------------------------------------------------------------- V-3 块连续
hdr("V-3  ⭐ 插入块是连续引用块（陷阱 74 子坑）")
for path, mk, nm, tag in [(ZH, "第 92 轮归属注（C-47）", "主题应取自其中的主产物", "V-3a"),
                          (EN, "Round-92 attribution note (C-47)", "the topic should be taken from the main product", "V-3b")]:
    lines = rd(path).split("\n")
    a = [i for i, s in enumerate(lines) if mk in s]
    b = [i for i, s in enumerate(lines) if nm in s]
    ok = len(a) == 1 and len(b) == 1 and a[0] < b[0]
    span = lines[a[0]:b[0] + 1] if ok else []
    blanks = sum(1 for s in span if s.strip() == "")
    nonq = sum(1 for s in span if s.strip() and not s.startswith(">"))
    chk(tag, ok and blanks == 0 and nonq == 0,
        "{}：块 {} 行，空行 {}，非引用行 {} ⟹ {}".format(
            os.path.basename(path)[:12], len(span), blanks, nonq,
            "连续 ✓" if blanks == 0 and nonq == 0 else "被切断 ✗"))

# ---------------------------------------------------------------- V-4 中英同步
hdr("V-4  中英同步")
for kz, ke, tag in [("三条路径全部判否", "all three routes ruled out", "V-4a"),
                    ("各 0 处", "each occur **0 times**", "V-4b"),
                    ("S-13", "S-13", "V-4c")]:
    chk(tag, zt.count(kz) >= 1 and et.count(ke) >= 1,
        "ZH「{}」{} / EN「{}」{}".format(kz, zt.count(kz), ke, et.count(ke)))

# ---------------------------------------------------------------- V-5 清单
hdr("V-5  清单台账")
li, pli = rd(LIST), rd(PLIST)
chk("V-5a", "| **C-47** |" not in pli and li.count("| **C-47** |") == 1, "C-47 行：新增且唯一")
chk("V-5b", "**45 条**" in pli and "| **撤回 / 更正** | **46 条**" in li, "总账 45 → 46")
codes = sorted({int(m) for m in re.findall(r"(?<![A-Za-z])C-(\d+)", li)})
non = []
for c in codes:
    for s in li.split("\n"):
        if re.match(r"^\| \*\*C-{}\*\* \|".format(c), s):
            cols = [x.strip() for x in s.strip("|").split("|")]
            if len(cols) > 2 and "撤回" not in cols[2] and "更正" not in cols[2]:
                non.append(c)
            break
chk("V-5c", max(codes) - len(non) == 46,
    "编号 {} − 非撤回更正族 {} = {} == 声明的 46".format(max(codes), len(non), max(codes) - len(non)))

# ---------------------------------------------------------------- V-6 元文本
hdr("V-6  ⭐ 元文本自指自检（铁律 18/20）")
files = sorted(glob.glob("*_备份_2026-10-02第92轮前.md")) + sorted(glob.glob("../环境说明_备份_2026-10-02第92轮前.md"))
allz = True
for p in files:
    c = rd(p).count("C-47")
    if c: allz = False
    print("     {:<52} C-47 补丁前 = {} 处".format(os.path.basename(p)[:52], c))
chk("V-6", allz, "全部底本 C-47 = 0 ⟹ 两列法成立")

# ---------------------------------------------------------------- V-7 记忆
hdr("V-7  项目记忆")
mt = rd(MEM)
chk("V-7a", len(mt) <= 3000, "MEMORY.md = {} 字符（限额 3000）".format(len(mt)))
chk("V-7b", "换措辞就认不出" in mt, "铁律 38 已含第 15 类陷阱（换措辞认不出 ≠ 判据）")

# ---------------------------------------------------------------- V-8 原块未改
hdr("V-8  第 55 轮块原内容未被改（只加注）")
pl, nl = block55(pzt).split("\n"), block55(zt).split("\n")
ins = len(nl) - len(pl)
print("  补丁前 {} 行 → 补丁后 {} 行（插入 {} 行）".format(len(pl), len(nl), ins))
# ⚠️ 第一版把插入行数**写死成 6** ⟹ 假 FAIL（实际 8 行）。教训 = 陷阱 82⑦：**期望值不要写死**。
chk("V-8", pl[0] == nl[0] and pl[1:] == nl[1 + ins:] and ins >= 5,
    "首行一致 ＋ 插入 {} 行之后逐行一致 ⟹ **只加注、不动内容**".format(ins))

# ---------------------------------------------------------------- V-9 既有台账
hdr("V-9  既有台账仍在")
chk("V-9a", "v2.9 补标（第 90 轮" in zt and "v2.9 补标之二（第 91 轮" in zt, "第 90 / 91 轮两张台账都在")
chk("V-9b", "3.0887·N^{−0.6836}" in zt and "3.0887·N^{−0.6836}" in et, "第 87 轮组 B 拟合式仍在")

# ---------------------------------------------------------------- V-10 交接
hdr("V-10  交接说明")
hs, phs = rd(HS), rd(PHS)
chk("V-10a", "第 92 轮新增" not in phs and "第 92 轮新增" in hs, "§三 第 92 轮段：新增")
chk("V-10b", "每轮块的主题必须等于该轮备忘录的主题" in hs, "规范已写入")

hdr("汇总")
print("  V-1…V-10 失败 {} 项".format(FAIL))
print("=" * 78)
print("VERIFY 92 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
