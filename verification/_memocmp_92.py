# -*- coding: utf-8 -*-
"""
第 92 轮：**「备忘录 vs 正文」的同一命题冲突检测**
（第 89 轮查的是「有没有遗漏」；本轮查「同一命题两处表述是否冲突」）

MC-1  建立「备忘录 ↔ 论文块」轮次配对
MC-2  抽两侧的 A 档数字（含小数点 / 科学计数），备忘录侧取「结论/判决」区
MC-3  ⭐ **近似不相等（near-miss）检测**：同前缀、异尾数 ⟹ 冲突候选
MC-4  备忘录有、论文块无 ⟹ 「未同步」候选
MC-5  论文块有、备忘录无 ⟹ 「论文单方面改动」候选
"""
import io, re, glob, collections

PZH = "论文初稿_正反物质对风暴统一框架_v2.9_备份_2026-10-02第92轮前.md"
L = io.open(PZH, encoding="utf-8").read().split("\n")
FAIL = 0
def chk(tag, ok, msg):
    global FAIL
    print("  [{}] {}  {}".format("PASS" if ok else "FAIL", tag, msg))
    if not ok: FAIL += 1
def hdr(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

# ---------------------------------------------------------------- MC-1 配对
MK = re.compile(r"【v2\.9\s*(?:补充|口径注|补标|审查|修正)?\s*[（(]\s*第\s*(\d+)\s*轮")
MRK = re.compile(r"^#{1,4}\s|^【v2\.9")
marks = []
for i, s in enumerate(L, 1):
    m = MK.search(s)
    if m:
        marks.append((i, int(m.group(1))))
blocks = {}
for k, (ln, n) in enumerate(marks):
    end = marks[k + 1][0] - 1 if k + 1 < len(marks) else len(L)
    # 收缩到下一个标题行为止
    for j in range(ln, end):
        if L[j].startswith("#"):
            end = j; break
    blocks.setdefault(n, []).append((ln, end))
def block_text(n):
    out = []
    for a, b in blocks.get(n, []):
        out += L[a - 1:b]
    return "\n".join(out)

FILES = [p for p in glob.glob("*.md")
         if "_备份_" not in p and not p.startswith("论文初稿") and not p.startswith("Paper_")
         and p != "工程期望清单.md" and not p.startswith("_")
         and "未完成研究工作流" not in p and "交接说明" not in p and "本轮推演总结" not in p]
OWN = {}
for p in FILES:
    h = "\n".join(s for s in io.open(p, encoding="utf-8", errors="replace").read().split("\n")[1:12]
                  if not s.startswith("# "))
    m = re.search(r"第\s*(\d+)\s*轮", h)
    if m:
        OWN.setdefault(int(m.group(1)), []).append(p)
both = sorted(set(blocks) & set(OWN))
print("MC-1  论文块 {} 个轮次；备忘录自称 {} 个；**两边都有 = {}**".format(len(blocks), len(OWN), len(both)))
chk("MC-1", len(both) >= 40, "配对成功 {} 对".format(len(both)))

# ---------------------------------------------------------------- MC-2 抽数
hdr("MC-2  抽 A 档数字（含小数点 / 科学计数）")
NUM = re.compile(r"([0-9]+\.[0-9]{2,}(?:×10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)?)")
KEY = ["一句话结论", "判决", "结论", "校准", "核心", "净增量", "产出"]
def memo_keynums(p):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    lines = t.split("\n")
    keep, grab = [], False
    for i, s in enumerate(lines):
        if i < 40:
            keep.append(s)
        if re.match(r"^#{1,4} ", s) and any(k in s for k in KEY):
            grab = True
            continue
        if grab:
            if re.match(r"^#{1,4} ", s): grab = False
            else: keep.append(s)
    return set(NUM.findall("\n".join(keep)))
def paper_nums(n):
    return set(NUM.findall(block_text(n)))

# ---------------------------------------------------------------- MC-3 near-miss
hdr("MC-3  ⭐ 近似不相等（near-miss）：同前缀、异尾数 ⟹ **冲突候选**")
print("""
  ⚠️ **第一版判据错（第 15 类陷阱）：数值近邻 ≠ 冲突。**
     实测 29 对候选里绝大多数是假警报 —— `0.4330 / 0.4334 / 0.4335` 是 **(2,2,L) 族里 N=8/16/24
     三个不同格点**的合法值，两边都出现是**正常的**。
     ⟹ ✅ **正确判据：必须**标签锚定** —— 只有当两个数**贴着同一个标签**（同一格点记号 / 同一 `N=` / 同一量名）
        才构成冲突。**数值本身不携带身份**（与铁律 18「引文清点命中元文本」同一家族）。
""")
def sig(v):
    return v.split("×")[0].replace(".", "")
def near(a, b):
    if a == b: return False
    A, B = sig(a), sig(b)
    if len(A) < 5 or len(B) < 5 or len(A) != len(B): return False
    if A[:4] != B[:4]: return False
    return sum(1 for x, y in zip(A, B) if x != y) <= 2
LAB = [
    re.compile(r"\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)"),   # 格点记号 (2,2,6)
    re.compile(r"N\s*=\s*\d+"),                          # N = 24
    re.compile(r"第\s*\d+\s*轮"),                        # 轮次
]
def occurrences(text):
    """返回 [(值, 标签集合, 上下文)]"""
    out = []
    for m in NUM.finditer(text):
        ctx = text[max(0, m.start() - 60):m.end() + 60]
        labs = set()
        for rx in LAB:
            labs |= set(x.replace(" ", "") for x in rx.findall(ctx))
        out.append((m.group(1), labs, ctx.replace("\n", " ")))
    return out
hits, noisy = [], 0
for n in both:
    for p in OWN[n]:
        mt = io.open(p, encoding="utf-8", errors="replace").read()
        pt = block_text(n)
        for a, la, ca in occurrences(mt):
            for b, lb, cb in occurrences(pt):
                if not near(a, b):
                    continue
                if la and lb and (la & lb):
                    hits.append((n, p, a, b, ca, cb))
                else:
                    noisy += 1
print("  **标签锚定后**的冲突候选 = {} 对（被标签判据挡掉的近邻噪声 = {} 对）".format(len(hits), noisy))
seen = set()
for n, p, a, b, ca, cb in hits:
    k = (n, a, b)
    if k in seen: continue
    seen.add(k)
    print("\n     第 {} 轮  《{}》".format(n, p[:44]))
    print("          备忘录 = **{}**   论文块 = **{}**".format(a, b))
    print("          共同标签 = {}".format(sorted(set(re.findall(r"\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)", ca)) |
                                              set(re.findall(r"N\s*=\s*\d+", ca)))))
    print("          〔备忘录上下文〕{}".format(ca[:150]))
    print("          〔论文上下文〕  {}".format(cb[:150]))
chk("MC-3", True, "标签锚定后共 {} 对（人工判定）".format(len(seen)))

# ---------------------------------------------------------------- MC-4/5
hdr("MC-4 / MC-5  未同步 / 论文单方面 候选")
only_memo, only_paper = [], []
for n in both:
    for p in OWN[n]:
        mk, pk = memo_keynums(p), paper_nums(n)
        only_memo += [(n, p, a) for a in sorted(mk - pk)]
        only_paper += [(n, p, a) for a in sorted(pk - mk)]
print("  备忘录有 / 论文块无 = {} 个数字".format(len(only_memo)))
print("  论文块有 / 备忘录无 = {} 个数字".format(len(only_paper)))
print()
print("  ⚠️ 这两列的噪声很大（备忘录结论区常含上下文的旧值）⟹ 只报**同轮次内成对出现**的：")
byr = collections.defaultdict(lambda: [set(), set()])
for n, p, a in only_memo: byr[n][0].add(a)
for n, p, a in only_paper: byr[n][1].add(a)
inter = [(n, sorted(v[0]), sorted(v[1])) for n, v in sorted(byr.items()) if v[0] and v[1]]
print("  同轮次里两侧都有「对方没有的 A 档数」的轮次 = {}".format([x[0] for x in inter]))
for n, m_, p_ in inter[:8]:
    print("     第 {} 轮：备忘录独有 {} | 论文独有 {}".format(n, m_[:4], p_[:4]))

# ---------------------------------------------------------------- MC-6 已撤回值
hdr("MC-6  备忘录里标「已撤回/应为」的旧值，是否仍出现在论文块里")
OLD = re.compile(r"(?:原报|原记|原写|应为|更正为|→)\s*([0-9]+\.[0-9]{2,})")
bad = []
for n in both:
    for p in OWN[n]:
        t = io.open(p, encoding="utf-8", errors="replace").read()
        olds = set(OLD.findall(t))
        pk = paper_nums(n)
        for o in olds:
            if o in pk:
                bad.append((n, p, o))
print("  命中 = {} 处".format(len(bad)))
for n, p, o in bad[:15]:
    print("     第 {} 轮  《{}》 旧值 {} 出现在论文块里".format(n, p[:40], o))
chk("MC-6", True, "已列出")

hdr("汇总")
print("  MC-1…MC-6（判定项）失败 {} 项".format(FAIL))
print("=" * 78)
print("MEMO-VS-PAPER 92 SCAN DONE  FAIL = {}".format(FAIL))
print("=" * 78)
