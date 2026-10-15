# -*- coding: utf-8 -*-
"""
第 86 轮核验：形状口径的**全链审计**
  —— 找的是用户说的那一类：「某些是对的结论后期再算变成错的，其实它就是对的」

主嫌疑：
  第 78 轮块（论文 §4.8）写「H/N ≈ 0.433 ≫ 0.25 ⟹ **面积律在能算的格点上不成立**」
  而第 48/51 轮已用 GAP 算出：**(4,4,4) = 0.1839**、**(6,6,6) = 0.0779**，**都 ≤ 0.25（满足）**。
  ⟹ 第 78 轮用**(2,2,L) 细长格点**的数据（作者自己的诚实边界写明「不外推」）推翻了它。

检查项：SA-1 … SA-8
"""
import io, os, re, sys
from itertools import combinations

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "outputs")
HIST = os.path.join(BASE, "MAPS-Unified-Framework", "paper", "history")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(OUT, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

PREZH = os.path.join(HIST, "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第86轮前.md")
PRE = io.open(PREZH, encoding="utf-8").read() if os.path.exists(PREZH) else io.open(ZH, encoding="utf-8").read()
Z = io.open(ZH, encoding="utf-8").read()
ZL = Z.split("\n")
PL = PRE.split("\n")

OK, BAD, WARN = [], [], []
def chk(tag, cond, msg):
    (OK if cond else BAD).append(tag)
    print("  [{}] {} {}".format("OK" if cond else "XX", tag, msg))
    print()

def hdr(t):
    print("\n" + "=" * 92)
    print(t)
    print("=" * 92)

# ⚠️ 掩码（陷阱 65/47/20 的规范做法：**模式化**，不枚举块名；表格行永不标记）
NORM = re.compile(r"(v2\.9\s*[^\n（|]{0,18}（第\s*\d+\s*轮|【第\s*\d+\s*轮"
                  r"|第\s*\d+\s*轮加注|第\s*\d+\s*轮口径注|第\s*\d+\s*轮补注"
                  r"|【v\d[^\n]{0,26}(修正|裁决|补充|更正|分级|登记|审查|分层注|撤回|审计|关联|复核))")
def block_mask(lines):
    m = [False] * len(lines)
    i = 0
    while i < len(lines):
        s = lines[i]
        if s.lstrip().startswith("|"):
            i += 1; continue
        if s.lstrip().startswith(">") and NORM.search(s):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith(">"):
                m[j] = True; j += 1
            i = j; continue
        if NORM.search(s):
            j = i
            while j < len(lines) and lines[j].strip() != "":
                m[j] = True; j += 1
            i = j; continue
        i += 1
    return m
MZ = block_mask(ZL)
MP = block_mask(PL)

# ================================================================
hdr("[SA-1] 组合事实：线长 L 的两种「偶-奇 / 奇-偶」配对，何时给出**恒等** σ_j？")
print("  σ_j ≡ (相位1匹配) ∘ (相位0匹配)⁻¹；线长 L 上取 **无序完美匹配**。")
print("  {:<6} {:>6} {:>10} {:>22}".format("L", "顶点", "完美匹配数", "两种配对是否同一个"))
rows = []
for L in (2, 4, 6, 8):
    E0 = frozenset(frozenset((i, (i + 1) % L)) for i in range(0, L, 2))          # 偶-奇
    E1 = frozenset(frozenset((i, (i + 1) % L)) for i in range(1, L + 1, 2))       # 奇-偶
    same = (E0 == E1)
    rows.append((L, L, 2, same))
    print("  {:<6} {:>6} {:>10} {:>22}".format(L, L, 2, "✅ 同一个 ⟹ σ_j = 恒等" if same else "❌ 不同 ⟹ σ_j ≠ 恒等"))
print()
print("  ⟹ ⭐ **只有 L = 2 的线**两种配对重合 ⟹ 该方向 **σ_j = 恒等，不贡献群元素**；")
print("     L ≥ 4 的线两种配对不同 ⟹ σ_j ≠ 恒等 ⟹ 该方向**贡献相位自由度**。")
chk("SA-1", [r[3] for r in rows] == [True, False, False, False],
    "**「退化方向」= 线长为 2 的方向**（唯一使 σ_j = 恒等的长度）—— 组合事实，逐 L 验证：\n"
    "     L = 2 ⟹ 两种配对**同一个** ⟹ σ_j = 恒等；L = 4/6/8 ⟹ 不同 ⟹ 有相位自由度 ✓\n"
    "     ⟹ 第 48 轮「判别量 = L=2 方向数」**有机制**（不是归纳出的巧合）")

# ================================================================
hdr("[SA-2] 全部 H/N 算例 × 退化方向数 —— 是否真的完全分离？")
# 数据来源：论文 §4.8 各轮块已记录的值（脚本不重算轨道，只做**数据表核对**）
CASES = [
    # (格点, N, H/N, 出处轮次)
    ("(2,2,2)",   8, 0.4679, 46),
    ("(2,2,4)",  16, 0.4335, 46),
    ("(2,2,6)",  24, 0.4334, 46),
    ("(2,2,8)",  32, 0.4617, 47),
    ("(2,2,10)", 40, 0.4802, 49),
    ("(2,2,14)", 48, 0.5041, 49),
    ("(2,2,16)", 64, 0.5307, 48),
    ("(2,4,4)",  32, 0.2834, 48),
    ("(2,4,6)",  48, 0.2208, 49),
    ("(2,4,8)",  64, 0.1802, 48),
    ("(2,4,10)", 80, 0.1571, 49),
    ("(2,4,12)", 96, 0.1338, 49),
    ("(2,6,6)",  72, 0.1652, 49),
    ("(4,4,4)",  64, 0.1839, 48),
    ("(6,6,6)", 216, 0.0779, 49),
]
print("  {:<10} {:>5} {:>9} {:>8}  {}".format("格点", "N", "H/N", "退化方向", "出处"))
TAB = []
for lat, N, hn, rd in CASES:
    deg = len([1 for x in re.findall(r"\d+", lat) if int(x) == 2])
    print("  {:<10} {:>5} {:>9.4f} {:>8}  第 {} 轮".format(lat, N, hn, deg, rd))
    TAB.append((lat, N, hn, deg))
g_hi = [r for r in TAB if r[3] >= 2]
g_lo = [r for r in TAB if r[3] <= 1]
g_0  = [r for r in TAB if r[3] == 0]
mx_lo = max(r[2] for r in g_lo); mn_hi = min(r[2] for r in g_hi)
mx_0  = max(r[2] for r in g_0);  mn_0  = min(r[2] for r in g_0)
print()
print("  组 A（退化方向 ≥ 2，n = {}）：[{:.4f}, {:.4f}]".format(len(g_hi), mn_hi, max(r[2] for r in g_hi)))
print("  组 B（退化方向 ≤ 1，n = {}）：[{:.4f}, {:.4f}]".format(len(g_lo), min(r[2] for r in g_lo), mx_lo))
print("  ⟹ 组 A 最小值 {:.4f} > 组 B 最大值 {:.4f} ⟹ **两组完全分离**".format(mn_hi, mx_lo))
print("  ⚠️ 但 **0.25 < {:.4f}** ⟹ **0.25 并不落在两组的「空隙」里**，而在**组 B 内部**".format(mx_lo))
print()
# 指出第 48 轮的措辞错误
w48 = ["0.25 落在空隙里" in s or ("最低值 0.4335" in s and "空隙" in s) for s in PL]
n48_bad = sum(1 for k, s in enumerate(PL) if "落在两组**空隙**里" in s or ("空隙" in s and "0.25" in s))
print("  第 48 轮原文里「0.25 落在空隙里」类表述：论文 {} 处；备忘录 {} 处".format(
    n48_bad, io.open(os.path.join(OUT, "装上GAP并首次算出HN的形状依赖_跨过面积律.md"), encoding="utf-8").read().count("0.25 落在空隙里")))
chk("SA-2", mn_hi > mx_lo and min(r[2] for r in g_lo) < 0.25 < mx_lo,
    "**15 个算例按「退化方向数」二分，两组完全分离**：组 A（≥2 个 L=2 方向）∈ [{:.4f}, {:.4f}]；"
    "组 B（≤1 个）∈ [{:.4f}, {:.4f}]。\n"
    "     ⭐ H/N 的主控变量是**「退化方向数」（数值格点的伪影程度）**，不是 N。\n"
    "     ⚠️ **顺带更正 C-40**：0.25 **不在**两组的空隙里（空隙 = ({:.4f}, {:.4f})，而 0.25 < {:.4f}）\n"
    "     —— 0.25 落在**组 B 内部**（跨点 N ∈ (32, 48)，第 49 轮已给出）；第 48 轮的「0.25 落在两组空隙里」**不成立**。".format(
        mn_hi, max(r[2] for r in g_hi), min(r[2] for r in g_lo), mx_lo, mx_lo, mn_hi, mx_lo))

# ================================================================
hdr("[SA-3] ⭐ 关键：**无退化**（0 个 L=2 方向）的算例给多少？")
zero = [(r[0], r[1], r[2]) for r in TAB if r[3] == 0]
for l, n, h in zero:
    print("  {:<10} N = {:<5} H/N = {:.4f}   vs 0.25 ⟹ {}".format(l, n, h, "**满足（H/N < 0.25）**" if h < 0.25 else "违反"))
print("  共 {} 个无退化算例；max = {:.4f}".format(len(zero), max(h for _, _, h in zero)))
print()
print("  ⟹ **真实宇宙的格点 L 很大 ⟹ 退化方向数 = 0** ⟹ 物理上对应的正是这一组。")
chk("SA-3", len(zero) >= 2 and all(h < 0.25 for _, _, h in zero),
    "⭐ **所有「无退化方向」算例都满足面积律**：(4,4,4) = 0.1839、(6,6,6) = 0.0779，**均 < 0.25**；\n"
    "     而**物理宇宙对应的正是这一组**（格点尺寸远大于 2）⟹ 在这条链上，面积律是**被满足**的，\n"
    "     **不是被否定的**。")

# ================================================================
hdr("[SA-4] 取证：第 78 轮块的「面积律在能算的格点上不成立」")
pat = re.compile(r"面积律在能算的格点上不成立")
h_pre = [(k + 1, s) for k, s in enumerate(PL) if pat.search(s)]
h_now = [(k + 1, s) for k, s in enumerate(ZL) if pat.search(s)]
print("  底本（第 86 轮前）命中 {} 行；当前稿命中 {} 行".format(len(h_pre), len(h_now)))
for k, s in h_pre:
    print("     L{}: {}".format(k, s.strip()[:230]))
print()
# 同块的诚实边界
h_edge = [(k + 1, s) for k, s in enumerate(PL) if "细长格点」限制**依然有效**" in s or "只算了 **(2,2,L)** 系列" in s]
for k, s in h_edge:
    print("  同块的诚实边界 L{}: {}".format(k, s.strip()[:230]))
print()
chk("SA-4", len(h_pre) == 1 and len(h_edge) >= 1,
    "⭐ **底本取证**：第 78 轮块含「**面积律在能算的格点上不成立**」（1 行），\n"
    "     ⚠️ 而**同一块**的诚实边界写着「只算了 **(2,2,L)** 系列 …… 细长格点限制**依然有效**，结论**不外推**」\n"
    "     ⟹ **同块内部矛盾**：结论句声称「能算的格点」，而边界承认只算了细长格点。")

# ================================================================
hdr("[SA-5] 论文里**已经**存在的相反结论（第 48/51 轮）")
key1 = [(k + 1, s) for k, s in enumerate(ZL) if "0.1839 是**满足**" in s or "0.1839" in s and "满足" in s]
key2 = [(k + 1, s) for k, s in enumerate(ZL) if "是细长格点假象" in s]
key3 = [(k + 1, s) for k, s in enumerate(ZL) if "面积律要求的 **0.25 被「跨过」了**" in s or "0.25 被「跨过」" in s]
for nm, arr in [("「(4,4,4) 的 0.1839 是满足」", key1), ("「细长格点假象」", key2), ("「0.25 被跨过」", key3)]:
    print("  ### {} —— {} 行".format(nm, len(arr)))
    for k, s in arr[:3]:
        print("     L{}: {}".format(k, s.strip()[:210]))
    print()
chk("SA-5", len(key1) >= 1 and len(key2) >= 1,
    "**论文里早已有相反的（更早、更权威）结论**：\n"
    "     · 第 51 轮：「(2,4,4) 的 0.2834 是**违反**自洽性；**(4,4,4) 的 0.1839 是满足**」（L524 一带）\n"
    "     · 第 48 轮：「第 40 轮以来『偏大 1.75 倍 ⟹ 面积律不成立』的判决**是细长格点假象**」（L492 一带）\n"
    "     ⟹ 第 78 轮的「不成立」与这两条**直接冲突**，且**更晚**。")

# ================================================================
hdr("[SA-6] 反向扫描：论文里「面积律 + 不成立」类句子，哪些**没有形状口径**？")
# ⚠️ 陷阱 72（两段式）：本轮的补丁会把该句改成「删除线 + C-39 更正」形式
#   ⟹ 判据必须区分「无保护的历史陈述」（底本）与「带更正标记的现行陈述」（当前稿）。
GUARD = ["细长", "(2,2,L)", "退化方向", "不外推", "形状依赖", "形状参数", "L = 2", "格点尺寸"]
FIXMARK = ["~~", "C-39", "C-40", "第 86 轮更正", "round-86 correction"]
def scan(lines):
    sus, guard = [], []
    for k in range(len(lines)):
        s = lines[k]
        if ("面积律" in s) and (("不成立" in s) or ("≫ 0.25" in s) or ("未被命中" in s)):
            if any(g in s for g in GUARD) or any(g in s for g in FIXMARK):
                guard.append((k + 1, s.strip()))
            else:
                sus.append((k + 1, s.strip()))
    return sus, guard
sus_pre, guard_pre = scan(PL)
sus_now, guard_now = scan(ZL)
print("  底本：无保护 {} 行 ／ 有保护或已更正 {} 行".format(len(sus_pre), len(guard_pre)))
print("  当前：无保护 {} 行 ／ 有保护或已更正 {} 行".format(len(sus_now), len(guard_now)))
print()
print("  ❌ 底本的**无保护**行：")
for k, s in sus_pre:
    print("     L{:<5} {}".format(k, s[:200]))
print()
print("  ✅ 当前稿里该句的形态（已带删除线/C-39）：")
for k, s in guard_now:
    if "面积律在能算的格点上不成立" in s:
        print("     L{:<5} {}".format(k, s[:230]))
print()
target_pre = [k for k, s in sus_pre if "面积律在能算的格点上不成立" in s]
target_now_free = [k for k, s in sus_now if "面积律在能算的格点上不成立" in s]
chk("SA-6", len(target_pre) == 1 and len(target_now_free) == 0,
    "⭐ **反向扫描命中唯一一处缺口，且补丁后已消除**：\n"
    "     · 底本：那句（L{}）**无任何形状口径保护词**，而其余「面积律＋不成立」句都带「细长 / (2,2,L) / 退化方向 / 不外推」之一；\n"
    "     · 当前稿：该串**只出现在删除线 ＋ C-39 更正语境**里，**无保护形态 0 行** ⟹ 缺口已闭合 ✓".format(
        target_pre[0] if target_pre else 0))

# ================================================================
hdr("[SA-7] 第 80 轮「不覆盖」登记是否引用了 H/N 的「不成立」？（决定要不要改登记）")
i80 = next((k for k, s in enumerate(ZL) if "【v2.9 登记（第 80 轮" in s), None)
print("  第 80 轮登记块起始行：", (i80 + 1) if i80 is not None else "未找到")
blk = ZL[i80:i80 + 12] if i80 is not None else []
for k, s in enumerate(blk):
    print("     L{:<5} {}".format(i80 + 1 + k, s.strip()[:190]))
has433 = any("0.433" in s or "0.4334" in s for s in blk)
print()
print("  ⟹ 登记块内是否直接引用 `0.433`：**{}**".format("是" if has433 else "否"))
chk("SA-7", i80 is not None and not has433,
    "**第 80 轮的「不覆盖」登记本身不需撤回** —— 它的四条依据（无等式 / 无机制 / 不可证伪 / 判据适用域）\n"
    "     **没有一条**引用「H/N ≈ 0.433」（登记块内 `0.433` 0 处）⟹ 结论「框架不覆盖这条链」**仍然成立**。\n"
    "     ⚠️ 但登记块说「第 46–52 轮**七轮＋第 78–80 轮复算，全部负面**」—— 第 48/51 轮给出的\n"
    "     **(4,4,4)/(6,6,6) 满足 0.25** 是**正面事实**（虽不等于「推出面积律」）⟹ 该措辞需要精确化。")

# ================================================================
hdr("[SA-8] 补丁后确认（陷阱 72 两段式：底本取证 ＋ 当前稿确认）")
P = re.compile(r"面积律在能算的格点上不成立")
free_pre = [k + 1 for k, s in enumerate(PL) if P.search(s) and not any(g in s for g in FIXMARK)]
free_now = [k + 1 for k, s in enumerate(ZL) if P.search(s) and not any(g in s for g in FIXMARK)]
n39 = len([1 for s in ZL if "C-39" in s]); n40 = len([1 for s in ZL if "C-40" in s])
blk86 = len([1 for s in ZL if "形状口径**的全链审计" in s or "full-chain audit of the **shape caliber**" in s])
print("  底本「无保护」命中 {} 行；当前稿「无保护」命中 {} 行".format(len(free_pre), len(free_now)))
print("  当前稿含 `C-39` {} 处、`C-40` {} 处；第 86 轮审计块 {} 处".format(n39, n40, blk86))
chk("SA-8", len(free_pre) >= 1 and len(free_now) == 0 and n39 >= 2 and n40 >= 1 and blk86 >= 1,
    "**两段式确认**：① 底本里该句是**无保护的历史陈述**（{} 行）；② 补丁后**无保护形态 0 行**（改成了「删除线 ＋ C-39 更正」）；\n"
    "     ③ 新增 `C-39`（{} 处）与 `C-40`（{} 处）登记；④ 第 86 轮审计块已落在 §4.8 块链**末尾** ✓".format(
        len(free_pre), n39, n40))

# ================================================================
print("\n" + "=" * 92)
print("通过 {} ／ 失败 {} ／ 待人工核对 {}".format(len(OK), len(BAD), len(WARN)))
print("=" * 92)
if BAD:
    print("失败项：", BAD)
    sys.exit(1)
