# -*- coding: utf-8 -*-
"""第 93 轮核验：候选池 #5 —— PPN 优越系（α₁ / ξ / α₂ / α₃）

任务来源登记（技能陷阱 87）：**外部待办** —— 项目台账 §三 候选池 #5
（非「上一轮诚实边界」式的内部循环）。

底本一律读 *_备份_2026-10-02第93轮前.md（铁律 18 / 20），
⟹ 本脚本**在补丁之后复跑仍然有效**；当前稿状态由 _verify_93.py 做两段式确认。
"""
import io
import re
import sympy as sp

N = 0
BAD = 0


def chk(tag, ok, msg):
    global N, BAD
    N += 1
    if not ok:
        BAD += 1
    print("  [{}] {:<10} {}".format("OK" if ok else "XX", tag, msg))


def hdr(s):
    print()
    print("=" * 100)
    print(s)
    print("=" * 100)


ZB = "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第93轮前.md"
EB = "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-02第93轮前.md"
LB = "项目台账_备份_2026-10-02第93轮前.md"
SB = "光速的意义_落差分解与超光速的结构性_备份_2026-10-02第93轮前.md"
B3B = "B3_高阶PPN与指数度规_备份_2026-10-02第93轮前.md"

ZT = io.open(ZB, encoding="utf-8").read()
ET = io.open(EB, encoding="utf-8").read()
LT = io.open(LB, encoding="utf-8").read()
ST = io.open(SB, encoding="utf-8").read()
BT = io.open(B3B, encoding="utf-8").read()
Z = ZT.split("\n")

# ---------------------------------------------------------------- PF-1
hdr("PF-1  存量清点：底本（备份）里「α₁」的全部出现点与语境分类")
hits = [(i, s) for i, s in enumerate(Z, 1) if "α₁" in s]
for i, s in hits:
    print("  L{:<5}| {}".format(i, s.strip()[:160]))
cats = {
    "§4.5b 参数表": any("ξ, α₁, α₂, α₃, ζ₁–ζ₄, ζ_W" in s for _, s in hits),
    "§8.6.7(e) C-2 句": any("C-2" in s and "泄漏" in s for _, s in hits),
}
print("  语境分类：{}".format({k: ("有" if v else "无") for k, v in cats.items()}))
chk("PF-1a", len(hits) == 2, "α₁ 底本出现 = {} 处（预期 2：参数表 ＋ C-2 句）".format(len(hits)))
chk("PF-1b", all(cats.values()), "两类语境（参数表 / C-2 句）齐备")
print("  ⚠️ 备忘：`α₁` 与 `PPN` 的检索是两码事 —— 含「PPN」的行有 ~20 处，含「α₁」的只有 2 处。")

# ---------------------------------------------------------------- PF-2
hdr("PF-2  依据等级：「其余全 0」的论证依据是什么")
z_just = [s for s in Z if "静态各向同性纯对角度规" in s]
b3_just = [s for s in BT.split("\n") if "度规静态、各向同性、纯对角" in s]
for s in z_just:
    print("  论文：{}".format(s.strip()[:150]))
for s in b3_just:
    print("  B3  ：{}".format(s.strip()[:190]))
chk("PF-2a", len(z_just) >= 1, "论文侧依据句在档（静态各向同性纯对角度规 ⟹）")
chk("PF-2b", len(b3_just) == 1 and "自动为 GR 值" in b3_just[0],
    "B3 侧依据句在档，且自带「（无 g₀ᵢ、无速度/自旋依赖）⟹ 自动为 GR 值」")
print("  ⟹ 判定：依据 = **静态 ansatz 的属性陈述**，不是动力学推导。")

# ---------------------------------------------------------------- PF-3
hdr("PF-3  定义域检验：引力侧有没有「运动 / 速度依赖」的 objet（盲区论证）")
TERMS = ["g₀ᵢ", "速度依赖", "矢量势", "含时", "动源", "运动源"]
counts = {t: ZT.count(t) for t in TERMS}
for t, c in counts.items():
    print("  底本中「{}」= {} 处".format(t, c))
chk("PF-3a", all(c == 0 for c in counts.values()),
    "六个「运动 / 速度依赖」类词在底本全文 0 处 ⟹ 框架引力侧只有**静态**对象")
lor = [(i, s) for i, s in enumerate(Z, 1) if "洛伦兹" in s]
print("  「洛伦兹」共 {} 处：".format(len(lor)))
for i, s in lor:
    print("    L{:<5}| {}".format(i, s.strip()[:130]))
chk("PF-3b", len(lor) >= 1 and all("α₁" not in s and "PPN" not in s for _, s in lor),
    "「洛伦兹」各处的语境均非引力侧优越系（都在因果集 / 涌撒段）")
sup = [(i, s) for i, s in enumerate(Z, 1) if "优越系" in s or "优先参照系" in s]
print("  「优越系 / 优先参照系」共 {} 处：".format(len(sup)))
for i, s in sup:
    print("    L{:<5}| {}".format(i, s.strip()[:150]))
chk("PF-3c", len(sup) == 1, "「优先参照系」全文 1 处（§8.6.7(e) L1622）；「优越系」一词论文里 0 处（只在清单/备忘录用）")

# ---------------------------------------------------------------- PF-4
hdr("PF-4  C-2 线程：三处登记 ＋「有没有演示」检查")
tk = io.open("tick更新规则_47μm属并行且串行被三条判据排除.md", encoding="utf-8").read()
chk("PF-4a", "C-2" in ST and "必须二选一" in ST, "光速 memo（第 18 轮）：承诺表 + 二选一在档")
chk("PF-4b", "从「可选」升为「必需」" in tk, "tick memo（第 47 轮）：升级为「必需」在档")
chk("PF-4c", "C-2（普朗克尺度的绝对性不得泄漏到 1PN" in ZT, "论文 §8.6.7(e)：C-2 句在档")
ab = []
for src, txt in [("光速memo", ST), ("论文", ZT), ("tickmemo", tk)]:
    for s in txt.split("\n"):
        if "绝对" in s and ("位置" in s or "性" in s):
            ab.append((src, s.strip()))
viol = [(src, s) for src, s in ab if ("演示" in s or "已证" in s or "已算" in s)]
asg = [(src, s) for src, s in ab if any(w in s for w in ["必须负责", "被派定", "派了个新活", "派定"])]
print("  含「绝对」的实质行 = {} 条；其中指派句 = {} 条，演示句 = {} 条".format(len(ab), len(asg), len(viol)))
for src, s in asg:
    print("    [指派] {}：{}".format(src, s[:135]))
chk("PF-4d", len(viol) == 0, "**没有任何「演示 / 已证」句** —— C-2 只有指派")
chk("PF-4e", len(asg) >= 2, "指派句 >= 2（「必须负责」/「被派定」/「派了个新活」式）")

# ---------------------------------------------------------------- PF-5
hdr("PF-5  观测限核对（本轮联网核查，Will 2006/2014 汇编 + Stairs 2003 Living Review）")
pool_row = [s for s in LT.split("\n") if s.startswith("5. **PPN / 优越系**")]
for s in pool_row:
    print("  池条目：{}".format(s.strip()[:150]))
chk("PF-5a", len(pool_row) == 1 and "α₁≲10⁻⁴" in pool_row[0],
    "池条目自带「α₁≲10⁻⁴」⟹ 与核查值（LLR ≤ 1×10⁻⁴）**一致** ✓")
old_a3 = [s for s in ST.split("\n") if s.startswith("| α₃ |")]
print("  memo 旧值：{}".format(old_a3[0].strip() if old_a3 else "（未命中）"))
chk("PF-5b", len(old_a3) == 1 and "10⁻⁸" in old_a3[0],
    "光速 memo 的 α₃ 记的是 10⁻⁸ ⟹ 与核查值 4×10⁻²⁰ **差 12 个数量级**（C-49 取证）")
print("  ── 本轮核对值（将写入光速 memo 更正注）：")
BOUNDS = [
    ("α₁", "≤ 1×10⁻⁴（LLR）／4×10⁻⁵（PSR J1738+0333）", "旧 10⁻⁴ ✓（另有更紧值）"),
    ("α₂", "≤ 2×10⁻⁹（毫秒脉冲星自旋进动）", "旧 10⁻⁷ 系早期表；更新"),
    ("α₃", "≤ 4×10⁻²⁰（脉冲星自旋减慢统计）", "旧 10⁻⁸ **错**（那是 ζ₃ 的量级）"),
    ("ξ", "≤ 4×10⁻⁹（毫秒脉冲星；旧 10⁻³ 为引力仪）", "更新"),
]
for k, v, note in BOUNDS:
    print("    {} : {}    [{}]".format(k, v, note))
chk("PF-5c", ST.count("4×10⁻²⁰") == 0, "旧底本中 4×10⁻²⁰ 未出现过（更正注将首次写入）")

# ---------------------------------------------------------------- PF-6
hdr("PF-6  判别力判定：与 GR 同值 ⟹ 判别力 0（N-22 同族）")
d1 = [s for s in Z if "1PN 与 GR 完全不可区分" in s]
d2 = [s for s in Z if "1PN 与 GR 不可区分" in s and "与 GR 同值" in s]
for s in d1:
    print("  §4.5b：{}".format(s.strip()[:130]))
for s in d2:
    print("  §9 台账：{}".format(s.strip()[:160]))
chk("PF-6a", len(d1) >= 1, "论文自认「1PN 与 GR 完全不可区分」在档")
chk("PF-6b", len(d2) >= 1, "§9 台账已标「与 GR 同值」（第 90 轮补标产物）")
print("  ⟹ α₁ = 0（若成立）与 GR 同值 ⟹ **观测无法区分框架与 GR** —— 判别力 0。")

# ---------------------------------------------------------------- PF-7
hdr("PF-7  数值复核：指数度规 1PN/2PN/3PN 展开（复核 §4.5b 表内数字）")
x = sp.symbols("x")
f00 = sp.series(-sp.exp(-2 * x), x, 0, 4).removeO()
g00gr = sp.series(-((1 - x / 2) / (1 + x / 2)) ** 2, x, 0, 4).removeO()
frr = sp.series(sp.exp(2 * x), x, 0, 4).removeO()
grrgr = sp.series((1 + x / 2) ** 4, x, 0, 4).removeO()


def cf(e, i):
    d = sp.Poly(sp.expand(e), x).as_dict()
    return sp.nsimplify(d.get((i,), 0))
print("  g₀₀ 框架 −exp(−2x)     系数 x¹..x³ = {}".format([cf(f00, i) for i in (1, 2, 3)]))
print("  g₀₀ GR  −[(1−x/2)/(1+x/2)]² = {}".format([cf(g00gr, i) for i in (1, 2, 3)]))
print("  g_rr 框架 exp(2x)      系数 x¹..x³ = {}".format([cf(frr, i) for i in (1, 2, 3)]))
print("  g_rr GR  (1+x/2)⁴     系数 x¹..x³ = {}".format([cf(grrgr, i) for i in (1, 2, 3)]))
chk("PF-7a", cf(f00, 1) == cf(g00gr, 1) == 2 and cf(frr, 1) == cf(grrgr, 1) == 2,
    "1PN 系数双方全同（g₀₀: 2 vs 2；g_rr: 2 vs 2）⟹「1PN 与 GR 不可区分」成立")
r2 = sp.nsimplify(cf(frr, 2) / cf(grrgr, 2))
chk("PF-7b", r2 == sp.Rational(4, 3),
    "2PN g_rr 比 = {} = 4/3 ⟹ **33.3% 分叉**（与论文表 x² 行一致）".format(r2))
r3 = sp.nsimplify(abs(cf(f00, 3)) / abs(cf(g00gr, 3)))
chk("PF-7c", r3 == sp.Rational(8, 9),
    "3PN g₀₀ 比 = {} = 8/9 ⟹ **11.1% 分叉**（与论文表 x³ 行一致；表内符号为括号约定）".format(r3))
print("  ⟹ §4.5b 表内数字复核通过；本轮**不动** γ/β 与 2PN/3PN 分叉的任何数值。")

# ---------------------------------------------------------------- PF-8
hdr("PF-8  英文稿同步检查")
en_ok = [
    ("参数表行", "ξ, α₁, α₂, α₃, ζ₁–ζ₄, ζ_W" in ET),
    ("框架值行", "0 (automatic GR values)" in ET),
    ("C-2 句", "must not leak into 1PN" in ET),
    ("C-2 升级句", "Parallel updating promotes C-2 from optional to required." in ET),
]
for k, v in en_ok:
    print("  {}：{}".format(k, "在档" if v else "缺失"))
chk("PF-8", all(v for _, v in en_ok), "英文稿四处全部在档 ⟹ 本轮补丁需中英同步四处")

# ---------------------------------------------------------------- PF-9
hdr("PF-9  [INFO] 记号存疑：「PPN α=β=γ=1」")
q = [s for s in Z if "α=β=γ" in s]
m4 = ["M4补强报告.md", "B3_高阶PPN与指数度规_备份_2026-10-02第93轮前.md"]
hits9 = [(f, s) for f in m4 for s in io.open(f, encoding="utf-8").read().split("\n") if "α=β=γ" in s]
print("  论文中 {} 处；M4/B3 memo 中 {} 处".format(len(q), len(hits9)))
for s in q + [s for _, s in hits9]:
    print("    | {}".format(s.strip()[:150]))
print("  [INFO] 标准 PPN（Will）无一阶「α」参数；此处疑似 Robertson–Schiff 记法或笔误。")
print("         **本轮不改**（可能引用特定文献记法），仅登记存疑。")
N += 0  # INFO 不计入

# ---------------------------------------------------------------- PF-10
hdr("PF-10  任务来源登记（陷阱 87）＋ 剩余外部待办")
rem = [s for s in LT.split("\n") if "剩余待办（全部）" in s]
for s in rem:
    print("  {}".format(s.strip()[:170]))
chk("PF-10a", len(pool_row) == 1, "任务来源 = 外部待办：候选池 #5（非内部循环）")
chk("PF-10b", len(rem) >= 1, "外部待办清单在档（本轮结项后须同步划线）")

# ---------------------------------------------------------------- 汇总
print()
print("=" * 100)
print("PPN93：通过 {} 项，失败 {} 项".format(N - BAD, BAD))
print("=" * 100)
print()
print("判决草案（候选池 #5，第 93 轮）：")
print("  ① 判别通道 —— **0**（论文自认 1PN 与 GR 不可区分；N-22 同族）")
print("  ② 约束通道 —— **C-2 = 未演示的必要条件**（N-38：各向同性 ≠ boost 不变；无泄漏量计算）")
print("  ③ 更正 —— C-48（§4.5b 范围限定）／C-49（观测限表 α₃ 记错）／C-50（「C」三套编号）")
print("  ④ 登记 —— I-22（tick 片层的 1PN 消隐）")
