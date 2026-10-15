# -*- coding: utf-8 -*-
"""第 110 轮核验：G9-②（底层四状态）结项 —— 恒等式检验 ＋ 对象消失 ＋ 同步性
   检查项 G9B-1 … G9B-13。两段式项：取证读「补丁前备份」，确认读当前稿。
"""
import io, os, math, re

BASE = r"C:\Users\Administrator\Desktop\2026-08-20-21-43-34"
OUT = os.path.join(BASE, "outputs")
HIST = os.path.join(BASE, "MAPS-Unified-Framework", "paper", "history")

ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")
ZH_PRE = os.path.join(HIST, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-04第110轮前.md")
EN_PRE = os.path.join(HIST, "Paper_v2.9_EN_备份_2026-10-04第110轮前.md")
LIST = os.path.join(OUT, "工程期望清单.md")
HO = os.path.join(BASE, "环境交接说明.md")
HO_PRE = os.path.join(BASE, "环境交接说明_备份_2026-10-04第110轮前.md")

rd = lambda p: io.open(p, encoding="utf-8").read()
Z, E, LP, H, HP = rd(ZH), rd(EN), rd(LIST), rd(HO), rd(HO_PRE)
ZP, EP = rd(ZH_PRE), rd(EN_PRE)
ZL, EL = Z.split("\n"), E.split("\n")

OK = 0
FAIL = 0


def chk(tag, cond, msg):
    global OK, FAIL
    if cond:
        OK += 1
        print("  [OK] " + tag + " " + msg)
    else:
        FAIL += 1
        print("  [XX] " + tag + " " + msg)


print("=== G9B-1 「反解 q」表是恒等式 bits(q) = 2 + log2(q) ===")
tab = {2: "3.000", 3: "3.585", 4: "4.000", 5: "4.322"}
dev = []
for q, shown in tab.items():
    v = 2.0 + math.log2(q)
    dev.append(abs(v - float(shown)))
chk("G9B-1a", max(dev) <= 5.0e-4,
    "q = 2/3/4/5 的 `2 + log2(q)` = " + " / ".join("%.6f" % (2.0 + math.log2(q)) for q in (2, 3, 4, 5))
    + "，与论文打印值 3.000/3.585/4.000/4.322 最大偏差 = " + "%.2e" % max(dev))
seg = [s for s in ZL if "q=2 → 3.000 bits" in s]
chk("G9B-1b", len(seg) == 1 and "q=5 → 4.322" in seg[0],
    "该数列在 ZH 论文中命中 1 行（原始出处）")

print("=== G9B-2 「唯一」= log 单调性；`k·q = 16` 单独不唯一 ===")
mono = all(2.0 + math.log2(q) < 2.0 + math.log2(q + 1) for q in range(1, 64))
roots = [q for q in range(1, 100) if abs(2.0 + math.log2(q) - 4.0) < 1e-12]
pairs = [(k, 16 // k) for k in range(1, 17) if 16 % k == 0]
chk("G9B-2a", mono and roots == [4],
    "log 严格增 ⟹ 方程唯一解 q = " + str(roots) + "（单调性 ⟹ 唯一性自动，非选择准则）")
chk("G9B-2b", len(pairs) == 5 and pairs == [(1, 16), (2, 8), (4, 4), (8, 2), (16, 1)],
    "`k·q = 16` 的整数解 = " + str(pairs) + "（共 " + str(len(pairs)) + " 组 ⟹ 约束本身不唯一）")
chk("G9B-2c", 2 ** 4 == 16 and all(2 ** k != 16 for k in range(1, 17) if k != 4),
    "`2^k = 16` 的唯一解 k = 4（2^k 单射）⟹ 全链条唯一的真唯一性、且不经过 q")

print("=== G9B-3 论文的诚实边界（现行表述）===")
zh_cav = "「4 的动力学唯一性」（内空间为何 4 分量）在框架设定层"
en_cav = 'the "dynamical uniqueness of 4" (why the interior space has 4 components) lies at the framework-assumption level'
chk("G9B-3a", Z.count(zh_cav) == 1, "ZH 诚实边界 1 处")
chk("G9B-3b", E.count(en_cav) == 1, "EN 诚实边界 1 处")

print("=== G9B-4 「四态」的三个等级（文本取证）===")
chk("G9B-4a", Z.count("只有正 / 负进入熵的计数") >= 1 and E.count("algebraic** state space") >= 1,
    "正 / 负：只有这两态带权重（第 32 轮）—— 中英各 ≥1")
chk("G9B-4b", Z.count("零测度过渡态") >= 1 and E.count("zero measure within a tick") >= 1,
    "湮灭中：拍内零测度过渡态（第 32 轮 C-c）—— 中英各 ≥1")
chk("G9B-4c", Z.count("无空槽") >= 1 and E.count("no empty slot") >= 1,
    "真空：第 32 轮 C-b「无空槽」⟹ 不占权重 —— 中英各 ≥1")

print("=== G9B-5 第 32 轮撤回已入论文 ===")
chk("G9B-5", Z.count("已由第 32 轮撤回") == 1 and E.count("withdrawn in round 32") == 1,
    "中英各 1 处（「q = 4 唯一解」的撤回）")

print("=== G9B-6 两段式：第 110 轮新注（取证 → 确认）===")
mk_zh = "v2.9 口径注（第 110 轮"
mk_en = "v2.9 caliber note (round 110"
chk("G9B-6", ZP.count(mk_zh) == 0 and Z.count(mk_zh) == 1
    and EP.count(mk_en) == 0 and E.count(mk_en) == 1,
    "补丁前 ZH/EN 各 0 处 ⟹ 补丁后各 1 处")

print("=== G9B-7 / G9B-8 G9 的另两个子项各有归宿 ===")
chk("G9B-7", Z.count("判为伪问题") >= 2 and E.count("declared a pseudo-problem") >= 1,
    "G9-①（`11.0904` 的自然性）＝ 第 39 轮「判为伪问题」")
chk("G9B-8", Z.count("零测度过渡态") >= 1 and E.count("zero measure within a tick") >= 1,
    "G9-③（拍内零测度过渡态的机制）＝ 第 20 / 32 / 34 轮闭环")

print("=== G9B-9 交接说明的过期标记（两段式）===")
hp = [s for s in HP.split("\n") if "底层四状态为何恰是这四个" in s]
h = [s for s in H.split("\n") if "底层四状态为何恰是这四个" in s]
chk("G9B-9", len(hp) == 1 and ("仍未解决" in hp[0]) and len(h) == 1 and ("已全部结项" in h[0]),
    "补丁前：该行标「⚠️ 仍未解决」（取证）／补丁后：标「✅ 已全部结项」（确认）")

print("=== G9B-10 插入块的引用块连续性（陷阱 74 子坑）===")


def block_ok(lines, contains):
    idx = [i for i, s in enumerate(lines) if contains in s]
    if len(idx) != 1:
        return False, "锚点 " + str(len(idx)) + " 次"
    i = idx[0]
    a = i
    while a - 1 >= 0 and lines[a - 1].startswith(">"):
        a -= 1
    b = i
    while b + 1 < len(lines) and lines[b + 1].startswith(">"):
        b += 1
    blank = [k for k in range(a, b + 1) if lines[k].strip() == ""]
    return len(blank) == 0, "块 [" + str(a + 1) + ", " + str(b + 1) + "] 内空行 " + str(len(blank))


ok1, m1 = block_ok(ZL, mk_zh)
ok2, m2 = block_ok(EL, mk_en)
chk("G9B-10", ok1 and ok2, "ZH " + m1 + " ｜ EN " + m2)

print("=== G9B-11 清单：C-76 紧跟在 C-75 之后，且 67–76 段升序 ===")
rows = [(i + 1, int(re.match(r"^\| \*\*C-(\d+)\*\* \|", s).group(1)))
        for i, s in enumerate(LP.split("\n")) if re.match(r"^\| \*\*C-(\d+)\*\* \|", s)]
nums = [n for _, n in rows]
p75 = [i for i, (_, n) in enumerate(rows) if n == 75]
p67 = [i for i, (_, n) in enumerate(rows) if n == 67]
run = [n for _, n in rows[p67[0]:p75[0] + 2]] if (len(p75) == 1 and len(p67) == 1) else []
chk("G9B-11", len(rows) >= 40 and len(p75) == 1 and len(p67) == 1
    and rows[p75[0] + 1][1] == 76 and run == list(range(67, 77)),
    "C 行 " + str(len(rows)) + " 条；C-76 紧跟 C-75（行 " + str(rows[p75[0] + 1][0]) + "）；"
    "67–76 段 = " + str(run))
miss = [n for n in range(1, 77) if n not in nums]
print("  [INFO] 68/69 行数与编号上限不等属**文件既有**状态（非本轮引入）："
      "表中缺 " + str(len(miss)) + " 个编号 " + str(miss) + "；且 41–55 / 67–76 两段升序、其后为降序段")

print("=== G9B-12 中英同步 ===")
chk("G9B-12", Z.count("**结论（G9-② 结项）**") == 1 and E.count("**Conclusion (G9-2 closed)**") == 1
    and Z.count("(1, 16) / (2, 8) / (4, 4) / (8, 2) / (16, 1)") == 1
    and E.count("(1, 16) / (2, 8) / (4, 4) / (8, 2) / (16, 1)") == 1,
    "结论句 ＋ 5 组解列表在中英各 1 处")

print("=== G9B-13 新注不引入新符号 / 新编号 ===")
GRK = "".join(chr(c) for c in range(0x370, 0x400)) + "".join(chr(c) for c in range(0x3b1, 0x3ca))
zh_new = "\n".join(ZL[ZL.index([s for s in ZL if mk_zh in s][0]):][:15])
en_new = "\n".join(EL[EL.index([s for s in EL if mk_en in s][0]):][:18])
new_syms = set(ch for ch in (zh_new + en_new) if ch in GRK)
pre_syms = set(ch for ch in (ZP + EP) if ch in GRK)
nref = re.findall(r"(?<![A-Za-z])(?:C|N|I|S)-\d+", zh_new + en_new)
chk("G9B-13", new_syms <= pre_syms and len(nref) == 0,
    "新注希腊字母 " + str(sorted(new_syms)) + " ⊆ 补丁前集合 = " + str(new_syms <= pre_syms)
    + "；新编号引用 " + str(nref))

print("")
print("通过 " + str(OK) + " 项，失败 " + str(FAIL) + " 项")
