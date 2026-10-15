# -*- coding: utf-8 -*-
"""第 91 轮 补丁后核验（铁律 18；两段式见陷阱 72）V-1…V-10"""
import io, os, re, glob

ZH  = "论文初稿_正反物质对风暴统一框架_v2.9.md"
PZH = "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第91轮前.md"
EN  = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
PEN = "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-02第91轮前.md"
LIST= "工程期望清单.md"
PLIST="工程期望清单_备份_2026-10-02第91轮前.md"
HS  = "../环境交接说明.md"
PHS = "../环境交接说明_备份_2026-10-02第91轮前.md"
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

# ---------------------------------------------------------------- V-1 冲突已修
hdr("V-1  ⭐ 两段式：§5.3「第四代预言」的四类判定注")
KEY_Z = "第 91 轮四类判定注"
KEY_E = "Round-91 four-way-verdict note"
chk("V-1a", pzt.count(KEY_Z) == 0 and zt.count(KEY_Z) == 1,
    "ZH：补丁前 {} → 补丁后 {}（新增且唯一）".format(pzt.count(KEY_Z), zt.count(KEY_Z)))
chk("V-1b", pet.count(KEY_E) == 0 and et.count(KEY_E) == 1,
    "EN：补丁前 {} → 补丁后 {}（新增且唯一）".format(pet.count(KEY_E), et.count(KEY_E)))
# 冲突判据：邻域现在含限定词
def near(t, key, win=400):
    i = t.find(key)
    return t[max(0, i - win):i + win] if i >= 0 else ""
nz, ne = near(zt, "第四代预言"), near(et, "Fourth-generation prediction")
chk("V-1c", "与 LHC 未发现存在张力" in nz, "ZH 邻域现在含 §9 第 5 行的状态原文")
chk("V-1d", "tension with LHC non-detection" in ne, "EN 邻域现在含 §9 row 5 的状态原文")

# ---------------------------------------------------------------- V-2 摘要指针
hdr("V-2  摘要：四类判定指针")
KEY_AZ = "第 91 轮注**：以上各项的**四类判定"
KEY_AE = "Round-91 note**: the **four-way verdicts"
chk("V-2a", KEY_AZ not in pzt and KEY_AZ in zt, "ZH 摘要指针：新增")
chk("V-2b", KEY_AE not in pet and KEY_AE in et, "EN 摘要指针：新增")
chk("V-2c", "只有 S-E5 一项带判定" in zt and "only S-E5 previously carried a verdict" in et,
    "两稿都点明了「摘要约 12 项里此前只有 1 项带判定」")

# ---------------------------------------------------------------- V-3 正文级台账
hdr("V-3  正文级承诺句台账：底本 0 → 现稿 1（中英）")
for path, pre, key, tag in [(ZH, PZH, "v2.9 补标之二（第 91 轮", "V-3a"),
                            (EN, PEN, "v2.9 labelling II (round 91", "V-3b")]:
    x, y = rd(pre).count(key), rd(path).count(key)
    chk(tag, x == 0 and y == 1, "{}：{} → {}".format(os.path.basename(path)[:12], x, y))

# ---------------------------------------------------------------- V-4 块连续
hdr("V-4  ⭐ 插入块是连续引用块（陷阱 74 子坑）")
for path, mk, nm, tag in [(ZH, "v2.9 补标之二（第 91 轮", "必须能指到四类判定台账", "V-4a"),
                          (EN, "v2.9 labelling II (round 91", "must resolve to a four-way verdict ledger", "V-4b")]:
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

# ---------------------------------------------------------------- V-5 中英同步
hdr("V-5  中英同步")
for kz, ke, tag in [("真预言 2", "true prediction 2", "V-5a"),
                    ("正文级实质承诺句 21 行", "21 substantive body claims", "V-5b"),
                    ("失败 3", "failed 3", "V-5c")]:
    chk(tag, zt.count(kz) >= 1 and et.count(ke) >= 1,
        "ZH「{}」{} 处 / EN「{}」{} 处".format(kz, zt.count(kz), ke, et.count(ke)))

# ---------------------------------------------------------------- V-6 清单
hdr("V-6  清单台账")
li, pli = rd(LIST), rd(PLIST)
chk("V-6a", "| **C-46** |" not in pli and li.count("| **C-46** |") == 1, "C-46 行：新增且唯一")
chk("V-6b", "**44 条**" in pli and "| **撤回 / 更正** | **45 条**" in li, "总账 44 → 45")
codes = sorted({int(m) for m in re.findall(r"(?<![A-Za-z])C-(\d+)", li)})
non = []
for c in codes:
    for s in li.split("\n"):
        if re.match(r"^\| \*\*C-{}\*\* \|".format(c), s):
            cols = [x.strip() for x in s.strip("|").split("|")]
            if len(cols) > 2 and "撤回" not in cols[2] and "更正" not in cols[2]:
                non.append(c)
            break
chk("V-6c", max(codes) - len(non) == 45,
    "编号 {} − 非撤回更正族 {} = {} == 声明的 45".format(max(codes), len(non), max(codes) - len(non)))

# ---------------------------------------------------------------- V-7 元文本
hdr("V-7  ⭐ 元文本自指自检（铁律 18/20）")
files = sorted(glob.glob("*_备份_2026-10-02第91轮前.md")) + sorted(glob.glob("../环境交接说明_备份_2026-10-02第91轮前.md"))
allz = True
for p in files:
    c = rd(p).count("C-46")
    if c: allz = False
    print("     {:<52} C-46 补丁前 = {} 处".format(os.path.basename(p)[:52], c))
chk("V-7", allz, "全部底本 C-46 = 0 ⟹ 两列法成立")

# ---------------------------------------------------------------- V-8 记忆
hdr("V-8  项目记忆")
mt = rd(MEM)
chk("V-8a", len(mt) <= 3000, "MEMORY.md = {} 字符（限额 3000）".format(len(mt)))
chk("V-8b", "41 ⭐⭐" in mt, "铁律 41 已写入")

# ---------------------------------------------------------------- V-9 两段台账共存
hdr("V-9  两段台账共存（第 90 轮 ＋ 第 91 轮）")
old = [s for s in zt.split("\n") if s.startswith("> | ")]
n90 = sum(1 for s in old if re.match(r"^> \| (\d+|6′|\*\*S)", s))
print("  §9 后台账表格行 = {}".format(len(old)))
chk("V-9a", "v2.9 补标（第 90 轮" in zt and "v2.9 补标之二（第 91 轮" in zt, "两段台账都在")
chk("V-9b", len(old) >= 30, "台账表格行合计 {}（第 90 轮 21 ＋ 第 91 轮 21）".format(len(old)))

# ---------------------------------------------------------------- V-10 既有
hdr("V-10  既有内容未被破坏")
chk("V-10a", "3.0887·N^{−0.6836}" in zt and "3.0887·N^{−0.6836}" in et, "第 87 轮组 B 拟合式仍在")
chk("V-10b", "S-C1" in zt and "1895" in zt, "第 88 / 90 轮的注仍在")
chk("V-10c", "第 89 轮" in rd(HS), "交接说明第 89 轮段仍在")

hdr("汇总")
print("  V-1…V-10 失败 {} 项".format(FAIL))
print("=" * 78)
print("VERIFY 91 DONE  FAIL = {}".format(FAIL))
print("=" * 78)
