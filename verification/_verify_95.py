# -*- coding: utf-8 -*-
"""第 95 轮补丁后核验（两段式：补丁前取证 / 补丁后确认），V-1…V-12。"""
import io, subprocess, sys, os

ZH = "论文初稿_正反物质对风暴统一框架_v2.9.md"
PZH = "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第95轮前.md"
EN = "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
PEN = "Paper_MatterAntimatterPairStorm_v2.9_EN_备份_2026-10-02第95轮前.md"
LI = "工程期望清单.md"
PLI = "工程期望清单_备份_2026-10-02第95轮前.md"
HH = "../环境交接说明.md"
PHH = "../环境交接说明_备份_2026-10-02第95轮前.md"

ok = 0; bad = 0
def chk(tag, cond, msg):
    global ok, bad
    if cond: ok += 1; print("  [OK] {:<7} {}".format(tag, msg))
    else: bad += 1; print("  [XX] {:<7} {}".format(tag, msg))

R = lambda p: io.open(p, encoding="utf-8").read()
z, pz = R(ZH), R(PZH)
e, pe = R(EN), R(PEN)
li, pli = R(LI), R(PLI)
hh, phh = R(HH), R(PHH)

print("=" * 100)
print("V-1..V-4  ZH 论文四处（补丁前 0 处 / 补丁后 ≥1 处）")
CASES_ZH = [
    ("V-1", "第 95 轮注（N-40：能标是输入、且不可独立解释）", "§8.1 N-40 注"),
    ("V-2", "「O(1) 系数」的期待已判否", "§8.1 C-54 短注"),
    ("V-3", "ρ_Λ = E_c⁴` 的定量识别已放弃", "§8.4 主判决块"),
    ("V-4", "不含对能标的预言", "P4 尾注"),
]
for tag, key, name in CASES_ZH:
    chk(tag, pz.count(key) == 0 and z.count(key) >= 1,
        "{}：「{}」底本 {} 处 → 当前 {} 处".format(name, key[:24], pz.count(key), z.count(key)))
chk("V-3b", pz.count("23.76") == 0 and z.count("23.76") >= 1,
    "⭐ 判决核心词「23.76」首次进入论文（0 → {} 处）".format(z.count("23.76")))

print()
print("V-5  EN 论文四处")
CASES_EN = [
    ("V-5a", "N-40: the scales are inputs", "EN §8.1 N-40"),
    ("V-5b", "Round-95 addendum (C-54)", "EN §8.1 C-54 短注"),
    ("V-5c", "the quantitative identification", "EN §8.4 主判决块"),
    ("V-5d", "carries no prediction of the scale", "EN P4 尾注"),
]
for tag, key, name in CASES_EN:
    chk(tag, pe.count(key) == 0 and e.count(key) >= 1,
        "{}：「{}」底本 {} → 当前 {}".format(name, key[:30], pe.count(key), e.count(key)))
chk("V-5e", e.count("23.76") >= 1, "EN「23.76× gap」在场（{} 处）".format(e.count("23.76")))

print()
print("V-6..V-8  清单")
n_closed = li.count("✅ **已结项（第 95 轮）**")
chk("V-6", n_closed == 4 and pli.count("✅ **已结项（第 95 轮）**") == 0,
    "池条目结项标注 = {} 条（应为 4：#1/#2/#4/#6）".format(n_closed))
chk("V-7a", "| **负面判定** | **40 条**" in li, "总账：负面 39 → **40 条** ✓")
chk("V-7b", "| **撤回 / 更正** | **54 条**" in li, "总账：更正 52 → **54 条** ✓")
import re
rows = {c: len(re.findall(r"^\| \*\*" + c + r"\*\* \|", li, re.M)) for c in ["N-40", "C-54", "C-55"]}
chk("V-8", all(v == 1 for v in rows.values()), "台账条目行各 1：{}".format(rows))

print()
print("V-9  交接说明")
chk("V-9a", phh.count("第 95 轮新增") == 0 and hh.count("第 95 轮新增") >= 1, "§三 第 95 轮段 ✓")
chk("V-9b", phh.count("当前建议（第 95 轮后）") == 0 and hh.count("当前建议（第 95 轮后）") >= 1, "§七 新当前建议 ✓")
chk("V-9c", "（历史，第 94 轮后，已被上式取代）" in hh, "旧建议已标历史 ✓")

print()
print("V-10  插入块连续性（陷阱 74 子坑：块内不得有空行）")
def blockspan(text, start_key, end_key):
    L = text.split("\n")
    i = next(k for k, s in enumerate(L) if start_key in s)
    j = next(k for k in range(i, len(L)) if end_key in L[k])
    return L[i:j + 1]
for tag, sk, ek, name in [
    ("V-10a", "【v2.9 判决注（第 95 轮 C-54）", "引用「meV 量级」时须同时写本判决", "ZH §8.4 判决块"),
    ("V-10b", "v2.9 verdict note (round 95, C-54)", 'citing the "meV order of magnitude" must include this verdict', "EN §8.4 判决块"),
]:
    txt = z if tag.endswith("a") else e
    span = blockspan(txt, sk, ek)
    bad_rows = [s for s in span if s.strip() != "" and not s.startswith("> ")]
    empty = [s for s in span if s.strip() == ""]
    chk(tag, len(bad_rows) == 0 and len(empty) == 0,
        "{}：{} 行，全部以「> 」开头、无空行（非引用行 {}、空行 {}）".format(name, len(span), len(bad_rows), len(empty)))

print()
print("V-11  ZH / EN 改动分类（纯插入 ×3 ＋ 行内追加 ×1；无删除、无其他改动）")
import difflib
def classify(a_text, b_text):
    a, b = a_text.split("\n"), b_text.split("\n")
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ins, rep, dele, other = 0, [], 0, 0
    for t, i1, i2, j1, j2 in sm.get_opcodes():
        if t == "equal": continue
        if t == "insert": ins += 1
        elif t == "delete": dele += 1
        elif t == "replace":
            # 行内追加：新行必须以旧行开头（允许 1:1 或多:1）
            ok_pref = all(b[j].startswith(a[i1]) for j in range(j1, j2) if a[i1])
            rep.append((i2 - i1, j2 - j1, ok_pref))
        else: other += 1
    return ins, rep, dele, len(a), len(b)
for tag, name, at, bt in [("V-11a", "ZH", pz, z), ("V-11b", "EN", pe, e)]:
    ins, rep, dele, la, lb = classify(at, bt)
    okrep = len(rep) == 1 and rep[0][0] == 1 and rep[0][1] == 1 and rep[0][2]
    chk(tag, ins == 3 and okrep and dele == 0,
        "{}：{} → {} 行；纯插入块 {} 个（应 3）／行内追加 {} 块（应 1，前缀保持 {}）／删除 {} 块".format(
            name, la, lb, ins, len(rep), rep[0][2] if rep else "-", dele))

print()
print("V-12  复跑正式核验（底本版，应仍 0 失败）")
r = subprocess.run([sys.executable, "_candpool_95.py"], capture_output=True, text=True, encoding="utf-8")
last = [s for s in r.stdout.split("\n") if "通过" in s and "失败" in s]
chk("V-12", bool(last) and "失败 0 项" in last[-1], "复跑：{}".format(last[-1] if last else "（无汇总行）"))

print()
print("=" * 100)
print("补丁后核验：通过 {} 项，失败 {} 项".format(ok, bad))
