# -*- coding: utf-8 -*-
"""
第 88 轮：**横向一致性审计** —— 同一命题在不同章节的表述是否一致

方法：给每条关键命题建一个「出现点台账」——
  每行 = (行号, **正文 or 轮次块**, 该行里出现的该量的值, 上下文片段)
判据三类：
  (a) **数值冲突**：同一命题在正文里出现两个不同值（且无更正标记）
  (b) **未同步**：轮次块里已更正，但**正文仍是旧值**
  (c) **中英不同步**：同一命题 ZH 有 / EN 无（或反之）

⚠️ 轮次块掩码用**模式化判据**（陷阱 65），不用枚举白名单。
⚠️ 输出只做**取证与标注**，不做自动判定 —— 判定在人工读完表之后。
"""
import io, re, os

ZH = "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
ZH_MARK = "【v2.9"

FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok:
        FAIL += 1

def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

zh_lines = io.open(ZH, encoding="utf-8").read().split("\n")
en_text = io.open(EN, encoding="utf-8").read()

# ---------------------------------------------------------------- 轮次块掩码（模式化，陷阱 65）
PAT = re.compile(r"(v2\.9\s*[^\n（|]{0,16}（第\s*\d+\s*轮|【第\s*\d+\s*轮"
                 r"|第\s*\d+\s*轮加注|第\s*\d+\s*轮口径注|第\s*\d+\s*轮补注"
                 r"|第\s*\d+\s*轮(补充|更正|登记|分层注|裁决))")
def mask(lines):
    m, in_note = [], False
    for s in lines:
        if s.lstrip().startswith("|"):
            m.append(False); continue          # 表格行永不标记（保守）
        if s[:1] == "#":
            in_note = False
        if PAT.search(s):
            in_note = True
        m.append(in_note)
    return m
M = mask(zh_lines)
n_block = sum(M)
print("轮次块掩码：{} 行属于轮次块 / 共 {} 行（正文 {} 行）".format(n_block, len(zh_lines), len(zh_lines) - n_block))

PUB = "@"

# ---------------------------------------------------------------- 出现点台账
def ledger(name, locators, value_re, limit=40):
    """locators: 行必须包含其中任一；value_re: 提取该量的值。"""
    print("\n" + "-" * 78)
    print("### {}    定位词 = {}".format(name, locators))
    print("-" * 78)
    rows = []
    for i, s in enumerate(zh_lines, 1):
        if not any(l in s for l in locators):
            continue
        vals = sorted(set(value_re.findall(s)))
        if not vals:
            continue
        rows.append((i, "块" if M[i - 1] else "正文", vals, s.strip()[:96]))
    for i, kind, vals, snip in rows[:limit]:
        print("  L{:<5} [{}] {:<22} {}".format(i, kind, ",".join(vals), snip))
    if len(rows) > limit:
        print("  …（还有 {} 行）".format(len(rows) - limit))
    # 冲突判定：正文里出现的值集合
    body_vals = set()
    for i, kind, vals, _ in rows:
        if kind == "正文":
            body_vals |= set(vals)
    print("  ⟹ 正文里出现的值 = {}".format(sorted(body_vals) if body_vals else "（无）"))
    return rows, body_vals

NUM = lambda *pats: re.compile("|".join(pats))

hdr("CO-1  (4,4,4) 的 H/N")
r, bv = ledger("P1 (4,4,4) 的 H/N", ["(4,4,4)"], NUM(r"0\.18\d\d"))
chk("CO-1", bv <= {"0.1839"}, "正文里只有 0.1839（实际 {}）".format(sorted(bv)))

hdr("CO-2  (6,6,6) 的 H/N")
r, bv = ledger("P2 (6,6,6) 的 H/N", ["(6,6,6)"], NUM(r"0\.07\d\d"))
chk("CO-2", bv <= {"0.0779"}, "正文里只有 0.0779（实际 {}）".format(sorted(bv)))

hdr("CO-3  (2,2,6) 的 H/N 与派生量")
r, bv = ledger("P3 (2,2,6)", ["(2,2,6)"], NUM(r"0\.4\d\d\d", r"5\.9\d", r"6[23]\d\d"))
chk("CO-3", bv <= {"0.4334", "6334"}, "正文里只有 0.4334 / 6334（实际 {}）".format(sorted(bv)))

hdr("CO-4  ⭐ 临界格点数 N_c（C-28：41.8 是旧值、39.6 是新值）")
r, bv = ledger("P4 N_c", ["N_c"], NUM(r"4[19]\.\d"), limit=50)
chk("CO-4", bv <= {"39.6"}, "正文里只有新值 39.6（实际 {}；若含 41.8 ⟹ **正文未同步**）".format(sorted(bv)))

hdr("CO-5  轨道数 / 不完备度（C-26 的派生量）")
r, bv = ledger("P5 轨道数派生量", ["6224", "6334", "5.93", "1050"], NUM(r"6[23]\d\d", r"5\.9\d", r"10\d\d"), limit=50)
chk("CO-5", "6224" not in bv, "正文里不再出现旧值 6224（实际 {}）".format(sorted(bv)))

hdr("CO-6  E_c（C-4：1.0181 是数值残差，恒等值 ≡ 1.000000 meV）")
r, bv = ledger("P6 E_c", ["E_c", "E_c "], NUM(r"1\.0\d+", r"1\.000000"), limit=50)

hdr("CO-7  ⭐ 宏观 H/N（C-41：5.4×10⁻⁵² 是混合拟合、2.7×10⁻⁵³ 是组 B）")
r, bv = ledger("P7 宏观 H/N", ["5.4×10⁻⁵²", "2.7×10⁻⁵³", "10⁻⁵²", "10⁻⁵³"],
               NUM(r"5\.4×10⁻⁵²", r"2\.7×10⁻⁵³", r"4\.5×10⁻⁷²"), limit=50)
chk("CO-7", True, "5.4×10⁻⁵² 在正文出现 ⟹ 应带「混合拟合」口径标记（见下表）")

hdr("CO-8  弦网能隙（C-11：Δ=1 应为 Δ=4J）")
r, bv = ledger("P8 能隙", ["能隙"], NUM(r"Δ\s*=\s*\d+[J]?"), limit=50)
chk("CO-8", "Δ = 1" not in bv and "Δ=1" not in bv, "正文里不再出现旧的 Δ = 1（实际 {}）".format(sorted(bv)))

hdr("CO-9  压缩因子 / 相干熵（5.545、11.0904、16）")
r, bv = ledger("P9 压缩因子", ["11.0904", "5.545", "压缩因子"], NUM(r"11\.0904", r"5\.545", r"2\.7726"), limit=50)

hdr("CO-10  χ = 2（拓扑荷）")
r, bv = ledger("P10 χ", ["χ = 2", "χ=2"], NUM(r"χ\s*=\s*2"), limit=50)
chk("CO-10", len(bv) <= 1, "正文里 χ 的表述唯一")

hdr("CO-11  w = −1/3（C：曲率标度）")
r, bv = ledger("P11 w", ["w = −1/3", "w=−1/3"], NUM(r"w\s*=\s*−?1/3"), limit=50)

hdr("CO-12  Ω_K（N-22：与平 ΛCDM 同值）")
r, bv = ledger("P12 Ω_K", ["Ω_K"], NUM(r"Ω_K\s*=\s*0"), limit=50)
co = [i for i, s in enumerate(zh_lines, 1) if "Ω_K" in s and "ΛCDM" in s]
chk("CO-12", True, "「Ω_K」与「ΛCDM」同行共现 = {} 行（第 61 轮的判据）".format(len(co)))

hdr("CO-13  EMRI 三个数（C-7：两组数不能并列引用）")
r, bv = ledger("P13 EMRI", ["1.6×10⁻⁶", "7.49×10⁻⁴", "ΔlnL"], NUM(r"1\.6×10⁻⁶", r"7\.49×10⁻⁴", r"\d+\s*σ", r"357"), limit=50)

hdr("CO-14  0.25 纳特/l_P²（B5）")
r, bv = ledger("P14 B5", ["0.25 纳特", "0.25 纳特/l"], NUM(r"0\.25"), limit=50)
co = [i for i, s in enumerate(zh_lines, 1) if "0.25 纳特" in s and "4π" in s]
chk("CO-14", True, "「0.25 纳特」与「4π」同行共现 = {} 行（C-20 的面积口径）".format(len(co)))

# ---------------------------------------------------------------- 中英同步（同一命题两边都有）
hdr("CO-15  中英同步：关键数两边都在")
KEYS = ["0.1839", "0.0779", "0.4334", "39.6", "1.0181", "2.7×10⁻⁵³", "0.1103", "0.1120",
        "3.0887", "0.6884", "0.0779", "8π/3", "1.0494×10⁷⁷", "5.545", "11.0904"]
for k in KEYS:
    a, b = sum(1 for s in zh_lines if k in s), en_text.count(k)
    flag = "✓" if (a >= 1 and b >= 1) else "⚠️"
    print("  {} {:<16} ZH {:>3} 处 / EN {:>3} 处".format(flag, k, a, b))
    if a >= 1 and b < 1:
        FAIL += 1
        print("       [FAIL] CO-15-{}  ZH 有 / EN 无 ⟹ 中英不同步".format(k))

hdr("汇总")
print("  CO-1…CO-15 失败 {} 项（含中英同步项）".format(FAIL))
print("  ⚠️ 本轮的判定以**出现点台账**为准，[FAIL] 只是提示，需人工读表确认")
print("=" * 78)
print("CONSISTENCY 88 SCAN DONE  FAIL = {}".format(FAIL))
print("=" * 78)
