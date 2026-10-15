# -*- coding: utf-8 -*-
"""
第 32 轮论文补丁：读法 A/B 裁决 —— 取 B2（4 平面内连接 × 正/负支 ⟹ 2^4 = 16）
  ① 摘要：改写「16 是怎么数出来的」
  ② §4.8：在第 31 轮的 A/B 歧义块之后追加裁决块（读法 A 撤回）
  ③ §4.8 中间量可证伪：改「16 = 4 方向 × 4 状态」
中英同步；锚点要求恰好命中一次。正文引号一律用中文引号。
"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, "论文初稿_正反物质对风暴统一框架_v2.9.md")
EN = os.path.join(BASE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md")

N_OK = [0]
N_FAIL = [0]


def load(p):
    return io.open(p, encoding="utf-8").read().split("\n")


def save(p, lines):
    io.open(p, "w", encoding="utf-8").write("\n".join(lines))


def insert_after(path, key, block, tag):
    lines = load(path)
    hits = [i for i, L in enumerate(lines) if key in L]
    if len(hits) != 1:
        print("  [XX] %-24s 命中 %d 行 —— 拒绝" % (tag, len(hits)))
        N_FAIL[0] += 1
        return
    i = hits[0]
    lines = lines[:i + 1] + block.split("\n") + lines[i + 1:]
    save(path, lines)
    print("  [OK] %-24s 已插入（第 %d 行后，%d 行）" % (tag, i + 1, len(block.split("\n"))))
    N_OK[0] += 1


def replace_once(path, key, old, new, tag):
    lines = load(path)
    hits = [i for i, L in enumerate(lines) if key in L]
    if len(hits) != 1:
        print("  [XX] %-24s 命中 %d 行 —— 拒绝" % (tag, len(hits)))
        N_FAIL[0] += 1
        return
    i = hits[0]
    if old not in lines[i]:
        print("  [XX] %-24s 行内未找到待替换子串" % tag)
        N_FAIL[0] += 1
        return
    lines[i] = lines[i].replace(old, new)
    save(path, lines)
    print("  [OK] %-24s 已替换（第 %d 行）" % (tag, i + 1))
    N_OK[0] += 1


# ------------------------------------------------------------- ① 摘要
replace_once(ZH, "原始态 = 4 方向（**平面内**",
             "原始态 = 4 方向（**平面内**，§4.9 引理 1）× 4 状态 = 16",
             "原始态 = **2^4 = 16**（4 个平面内连接 × {正支, 负支}，读法 B2，见 §4.8）",
             "ZH 摘要")
replace_once(EN, "raw states = 4 **in-plane** directions",
             "raw states = 4 **in-plane** directions (§4.9 Lemma 1) × 4 states = 16",
             "raw states = **2^4 = 16** (4 in-plane connections × {+ branch, − branch}, reading B2, see §4.8)",
             "EN abstract")

# --------------------------------------------------- ② §4.8 裁决块
ZH_BLOCK = (
    "> **【v2.9 修正（第 32 轮：读法 A / B 的裁决）】** 上一条登记的 A/B 歧义**已裁决**：\n"
    "> 取 **读法 B2** —— **4 个平面内连接，每个承载正支或负支 ⟹ 2^4 = 16 = 4 bits/面元**，\n"
    "> 而非「1-of-4 方向 × 4 内部态」。依据：五条约束的打分矩阵中 **B2 是唯一全过者**——\n"
    "> C-a 原始可读 4 bits ✓；C-b 满占位 f = 1（**无空槽**，故「真空」不占权重）✓；\n"
    "> C-c「湮灭中」为拍内零测度过渡态（不占权重）✓；\n"
    "> C-d 方向数 = 4（§4.9 引理 1 的平面内 4）✓；C-e **A1 的 50:50 直接落在每槽上** ✓。\n"
    "> **读法 A 落选**：它让「真空」「湮灭中」与「正 / 负」等权，与 C-b / C-c 冲突；\n"
    "> 剔除二者后只剩 4 × 2 = 8 态 = 3 bits，与 4 bits/面元不符——\n"
    "> 若硬沿用压缩因子 11.0904，Hawking 温度偏差 **+33.33%**（对照：N = 24 时 −12.76%）。\n"
    "> ⟹ **16 态、4 bits、0.25 nat/面元、压缩因子 16 ln2 = 11.0904 全部不变**；\n"
    "> 变的只是「16 是怎么数出来的」，且 B2 **把 A1 的 50:50 直接用上了**（读法 A 未用）。\n"
    "> ⚠️ **代价**：{正, 负, 湮灭中, 真空} 中**只有正 / 负进入熵的计数**；四态降为\n"
    "> **代数**状态空间（仅两态携带权重）⟹ **第 19 轮「内部四态 q = 4 是唯一解」撤回**。"
)

EN_BLOCK = (
    "> **【v2.9 correction (round 32: adjudicating readings A / B)】** The A/B ambiguity registered\n"
    "> above is **resolved in favour of reading B2**: **4 in-plane connections, each carrying the\n"
    "> + or − branch ⟹ 2^4 = 16 = 4 bits/plaquette**, rather than \"1-of-4 direction × 4 internal\n"
    "> states\". Grounds: in the scoring matrix over five constraints, **B2 is the only model that\n"
    "> passes all of them** — C-a raw readable 4 bits ✓; C-b full occupancy f = 1 (**no empty slot**,\n"
    "> so \"vacuum\" carries no weight) ✓; C-c \"annihilating\" is a zero-measure in-tick transient ✓;\n"
    "> C-d direction count = 4 (the four in-plane directions of §4.9 Lemma 1) ✓; C-e **A1's 50:50\n"
    "> sits directly on each slot** ✓. **Reading A fails**: it gives \"vacuum\" and \"annihilating\"\n"
    "> the same weight as \"+/−\", contradicting C-b / C-c; removing the two leaves 4 × 2 = 8 states\n"
    "> = 3 bits, inconsistent with 4 bits/plaquette — and if the compression factor 11.0904 is kept\n"
    "> regardless, the Hawking temperature is off by **+33.33%** (compare −12.76% for N = 24).\n"
    "> ⟹ **16 states, 4 bits, 0.25 nat/plaquette and the compression factor 16 ln 2 = 11.0904 are\n"
    "> all unchanged**; only the way 16 is counted changes, and B2 **makes direct use of A1's 50:50**\n"
    "> (which reading A did not). ⚠️ **Cost**: of {+, −, annihilating, vacuum} only **+ and − enter\n"
    "> the entropy count**; the four states demote to an **algebraic** state space with two weighted\n"
    "> states ⟹ **the round-19 claim \"q = 4 internal states is the unique solution\" is withdrawn**."
)

insert_after(ZH, "读法 A 下「真空」是与方向并列的独立内部态。", ZH_BLOCK, "ZH §4.8 裁决块")
insert_after(EN, "on a par with the directions.", EN_BLOCK, "EN §4.8 adjudication")

# ------------------------------------------- ③ 中间量可证伪
replace_once(ZH, "中间量可证伪", "底层状态数 **16 = 4 方向 × 4 状态**",
             "底层状态数 **16 = 2^4（4 平面内连接 × 正 / 负支）**", "ZH 中间量")
replace_once(EN, "intermediate quantities falsifiable",
             "substrate state count **16 = 4 directions × 4 states**",
             "substrate state count **16 = 2^4 (4 in-plane connections × +/− branch)**", "EN intermediate")

print("\n补丁完成：成功 %d 项，失败 %d 项" % (N_OK[0], N_FAIL[0]))
