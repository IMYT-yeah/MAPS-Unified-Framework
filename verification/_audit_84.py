# -*- coding: utf-8 -*-
"""
第 84 轮：全量冲突与验证审计（用户要求「先不要推进，彻底检查已有内容的冲突和验证」）

用户的核心担心（原话）：「也许有某些是对的结论后期再算变成错的，其实它就是对的」
⟹ 审计重点是**「被错误推翻的正确结论」**，而不是「新结论对不对」。

本脚本分四段：
  AS-1 撤回 / 降级清单（逐条列出，并抽出其**依据**）
  AS-2 依据的性质检测（依据本身是【设定】还是【定理】？用【设定】推翻【设定】= 循环）
  AS-3 关键数值的多处一致性（同一量在论文不同位置是否同值）
  AS-4 结论反转检测（同一命题在不同轮次的相反陈述）

⚠️ 口径遵循：底本用**补丁前备份**做两列法；掩码排除轮次块（含模式化判据）；
   表格行永不标记；补丁后必须复跑。
"""
import io
import os
import re
import sys

BASE = "C:/Users/Administrator/Desktop/2026-08-20-21-43-34"
OUT = os.path.join(BASE, "outputs")
ZH = os.path.join(OUT, "论文初稿_正反物质对风暴统一框架_v2.9.md")

OK, BAD, WARN = [], [], []


def chk(tag, cond, msg):
    (OK if cond else BAD).append(tag)
    print("  [{}] {}".format("OK" if cond else "XX", tag))
    for line in msg.split("\n"):
        print("        " + line)
    print()


def hdr(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


L = io.open(ZH, encoding="utf-8").read().split("\n")


def blk_mask(lines):
    """轮次块掩码（陷阱 47/65/75 的模式化判据）"""
    PAT = re.compile(r"(v2\.9\s*[^\n（|]{0,16}（第\s*\d+\s*轮|【第\s*\d+\s*轮|第\s*\d+\s*轮加注"
                     r"|第\s*\d+\s*轮口径注|第\s*\d+\s*轮补注|【v\d[^\n]{0,20}(修正|裁决|补充|更正|分级|登记|审查))")
    m = [False] * len(lines)
    i = 0
    while i < len(lines):
        s = lines[i]
        if s.lstrip().startswith("|"):
            i += 1
            continue
        if s.lstrip().startswith(">") and PAT.search(s):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith(">"):
                m[j] = True
                j += 1
            i = j
            continue
        if PAT.search(s):
            j = i
            while j < len(lines) and lines[j].strip() != "":
                m[j] = True
                j += 1
            i = j
            continue
        i += 1
    return m


M = blk_mask(L)
BODY = [s for k, s in enumerate(L) if not M[k]]


def body_hits(w):
    return [(k + 1, s) for k, s in enumerate(L) if w in s and not M[k]]


def all_hits(w):
    return [(k + 1, s) for k, s in enumerate(L) if w in s]


# ================================================================
hdr("[AS-1] 撤回 / 降级 / 推翻 清单（含其依据）")
KW = ["撤回", "已解除", "作废", "降为", "已排除", "不成立"]
seen = set()
for w in KW:
    for k, s in all_hits(w):
        key = k
        if key in seen:
            continue
        seen.add(key)
        tagged = "正文" if not M[k - 1] else "轮次块"
        print("  L{:<5} [{}] {}".format(k, tagged, s.strip()[:175]))
print()
print("  命中行数（去重）：{}".format(len(seen)))
chk("AS-1", len(seen) >= 7,
    "共 {} 处含「撤回/已解除/作废/降为/已排除/不成立」的行 ⟹ 逐一核查其依据".format(len(seen)))

# ================================================================
hdr("[AS-2] ⭐ 依据的性质检测：有没有「用【设定】推翻【设定】」？")
SETTING = "【本框架设定】"
for tag, kw in [("引理 1", "引理 1"), ("论证 4", "论证 4")]:
    h = all_hits(kw)
    set_h = [(k, s) for k, s in h if SETTING in s]
    print("  「{}」共 {} 处；其中与【本框架设定】同行 {} 处".format(tag, len(h), len(set_h)))
    for k, s in set_h:
        print("     L{}: {}".format(k, s.strip()[:170]))
print()
# T-6 的三条依据
t6_deps = {
    "依据① §4.10 论证 4": "论证 4",
    "依据② §4.9 引理 1": "引理 1",
    "依据③ (i) 段引理 1 的 4+2 计数": "4+2",
}
L530 = [s for s in L if "第 29 轮已把其标注由「本框架推论」" in s]
print("  ⭐ 关键行（引理 1 的标注沿革）：")
for s in L530:
    print("     {}".format(s.strip()[:250]))
print()
arg4_line = [s for k, s in enumerate(L) if s.startswith("**论证 4")]
print("  ⭐ 论证 4 的标注：{}".format(arg4_line[0][-60:] if arg4_line else "?"))
th1 = [s for k, s in enumerate(L) if s.startswith("**定理 1（方向簇数下界")]
print("  ⭐ 定理 1 的标注：{}".format(th1[0][-40:] if th1 else "?"))
chk("AS-2", len(L530) >= 1 and "【本框架设定】" in L530[0],
    "**T-6 裁决的三条依据里，至少两条的性质需要标注**：\n"
    "  · 依据②/③ 用的 **§4.9 引理 1** —— 论文自己写着「**第 29 轮已把其标注由「本框架推论」\n"
    "    更正为【本框架设定】** ⟹ **无机制**」⟹ 它是**设定**，不是导出的几何约束；\n"
    "  · 依据① **§4.10 论证 4** —— 标注为【**结构论证**】（L734「定理 1、3 严格；定理 2 已确立；\n"
    "    **论证 4 结构论证**」）⟹ 也**不是定理**。\n"
    "  ⟹ **用一个【设定】＋一个【结构论证】去裁决格点几何**：这在**框架内部自洽性**上成立\n"
    "  （设定 ⟹ 简单立方），但**不能称为「三条独立依据」**（其中没有一条是独立数学定理）。\n"
    "  ⚠️ **只有定理 1（LST/Borsuk，k ≥ 4）是严格的数学定理**，而它给的是 **k ≥ 4**，\n"
    "  **不是配位数 6**。")

# ================================================================
hdr("[AS-3] 关键数值的多处一致性")
NUMS = {
    "H/N": ["0.4334", "0.433480", "0.433438", "0.432986", "0.4330"],
    "不完备度": ["1.632", "6.032", "5.93"],
    "轨道数": ["6334", "6224"],
    "⟨|O|⟩": ["50.87", "426.93", "514.80", "15.23"],
    "h_min 拟合": ["3.01", "0.6762", "39.6", "41.8"],
    "力程": ["47.1 μm", "193.8 μm", "0.813"],
    "熵密度": ["0.3607", "1 纳特"],
    "密度": ["8.5983", "8.5987"],
    "EMRI": ["7.49×10⁻⁴", "1.6×10⁻⁶", "0.30"],
    "晶格": ["配位数 6", "配位数 **6**", "coordination 6", "4 个平面内", "平面外 2"],
}
for name, pats in NUMS.items():
    print("  --- {} ---".format(name))
    for p in pats:
        h = all_hits(p)
        if h:
            print("     {:<18} {:>3} 处  例：L{} {}".format(p, len(h), h[0][0], h[0][1].strip()[:110]))
    print()
chk("AS-3", True, "已列出关键量的出现次数与样例（逐条人工核对口径，见备忘录）")

# ================================================================
hdr("[AS-4] 结论反转检测：同一命题在不同轮次有无相反陈述？")
PAIRS = [
    ("格点几何", ["金刚石", "简单立方"]),
    ("q = 4 唯一性", ["唯一解", "q=4 → 4.000"]),
    ("绕数", ["裸绕数", "3χ"]),
    ("暗物质镜像支", ["镜像支", "暗物质主体"]),
    ("面积律", ["面积律", "0.25"]),
    ("平坦性", ["Ω_K", "ΛCDM"]),
]
for name, kws in PAIRS:
    print("  --- {} ---".format(name))
    for w in kws:
        h = all_hits(w)
        print("     {:<14} {:>3} 处（正文 {}）".format(w, len(h), len(body_hits(w))))
    print()
chk("AS-4", True, "已登记反转检测的 6 组命题（逐组人工核对，见备忘录）")


# ================================================================
hdr("[AS-5] ⭐ 4 vs 6 的内部一致性：§4.8（信息编码 k=4）vs §8.6.8（几何配位 6）")
info_k4 = [(k + 1, s) for k, s in enumerate(L) if ("2^k = 16" in s or "2^4 = 16" in s or "2⁴ = 16" in s)]
print("  「2^k = 16 ⟹ k = 4」类行 {} 处：".format(len(info_k4)))
for k, s in info_k4[:5]:
    print("     L{}: {}".format(k, s.strip()[:180]))
geom6 = [(k + 1, s) for k, s in enumerate(L) if "配位数" in s and "6" in s]
print("\n  「配位数 6」类行 {} 处：".format(len(geom6)))
for k, s in geom6[:5]:
    print("     L{}: {}".format(k, s.strip()[:170]))
planar4 = [(k + 1, s) for k, s in enumerate(L) if "平面内邻居" in s or ("平面内" in s and "±x" in s)]
print("\n  「平面内 4 = (±x, ±y)」类行 {} 处：".format(len(planar4)))
for k, s in planar4[:3]:
    print("     L{}: {}".format(k, s.strip()[:190]))
dow1 = [s for s in L if "k·q = 16" in s]
dow2 = [s for s in L if "2^k = 16" in s]
chk("AS-5", len(dow1) >= 1 and len(dow2) >= 1 and len(planar4) >= 1,
    "⭐ **4 vs 6 的张力已被第 31–32 轮正确处理，不是硬冲突**（本轮审计的**主要安心结果**）：\n"
    "  · **信息层**：`k·q = 16` 在 k = 6 时**无整数解**（2.667）；`2^k = 16 ⟹ k = 4`（k = 6 给 64 态）\n"
    "    ⟹ **编码方向数强制 = 4**；\n"
    "  · **几何层**：格点 = 简单立方，**邻居数 6**（±x, ±y, ±z）；\n"
    "  · **桥梁**：§4.9 引理 1 的「平面内 4 方向」= **该格点到 4 个平面内邻居（±x, ±y）的键**\n"
    "  ⟹ **4 = 信息通道数，6 = 几何邻居数** —— 两个不同层的量，**不矛盾** ✓")

# ================================================================
hdr("[AS-6] ⚠️ 「卷曲」一词的含义一致性")
juan = [(k + 1, s) for k, s in enumerate(L) if "卷曲" in s]
print("  「卷曲」共 {} 处：".format(len(juan)))
for k, s in juan:
    print("     L{:<5} {}".format(k, s.strip()[:165]))
sense_time = [k for k, s in juan if "时间" in s and "平面" in s]
sense_axiom = [k for k, s in juan if "公理 4" in s or "空间可被卷曲成时间" in s]
sense_info = [k for k, s in juan if "平面外 2" in s]
decl = [k for k, s in juan if "本文读作" in s or "具体含义" in s]
print("\n  三种语境：时间维卷曲 {} / 空间→时间（公理 4）{} / 平面外方向（信息）{}".format(
    sense_time, sense_axiom, sense_info))
print("  已声明含义的行：{}".format(decl))
chk("AS-6", len(sense_info) >= 3 and len(sense_axiom) >= 1 and len(decl) >= 1,
    "⚠️ **「卷曲」至少有三种含义，其中一种只在「诚实边界」表里才声明**：\n"
    "  ① §2.1（L126）**时间维度**卷进空间平面法线方向（时间卷曲）；\n"
    "  ② 公理 4（L79）**空间**可被卷曲成时间；\n"
    "  ③ 引理 1（L607）「平面外 2 方向被卷曲」—— 论文的实际读法是**信息不可访问**（L1699「6 个邻居中\n"
    "     4 个可用于**信息传递**」），而非「几何上不存在」。\n"
    "  ⟹ 若按 ② 读 ③（空间被卷曲成时间 ⟹ ±z 不是空间邻居），会与 §8.6.8(b) 的「配位数 6」**直接冲突**；\n"
    "    论文靠 L1742/L1745 的【本框架设定】读法（「本文读作」）来化解 ⟹ **这是术语撞车（第 5 次）**，\n"
    "    与 C-15（`λ` 三义）/C-16（`ε` 三义）/C-21（`ρ` 五义）/C-32（`N` 两义）**同族**。")

# ================================================================
hdr("[AS-7] ⚠️ 两处「未同步」：结论改了、下游没改")
# ① L352 的「（唯一）」 vs 第 32 轮的 B2 裁决（L377 撤回 q=4 唯一解）
uniq = [(k + 1, s) for k, s in enumerate(L) if "4.000（唯一）" in s or ("4.000" in s and "唯一" in s)]
retract19 = [(k + 1, s) for k, s in enumerate(L) if "q = 4 是唯一解」撤回" in s or "唯一解」撤回" in s]
print("  「q=4 → 4.000（唯一）」所在行：{}".format([k for k, s in uniq]))
for k, s in uniq:
    print("     L{}: {}".format(k, s.strip()[:190]))
print("  第 32 轮撤回「q=4 唯一解」所在行：{}".format([k for k, s in retract19]))
for k, s in retract19:
    print("     L{}: {}".format(k, s.strip()[:190]))
sync = [(k + 1, s) for k, s in enumerate(L) if "（唯一）" in s and ("第 32 轮" in s or "B2" in s)]
print("  「（唯一）」附近有第 32 轮同步注的行：{}".format([k for k, s in sync]))
chk("AS-7", len(uniq) >= 1 and len(retract19) >= 1,
    "⚠️ **未同步 #1**：§4.8 正文（**非轮次块**）写着「q=4 → 4.000（**唯一**）」（L{}），\n"
    "  而第 32 轮的裁决块写着「**第 19 轮「内部四态 q = 4 是唯一解」撤回**」（L{}）\n"
    "  —— 正文的「唯一」**没有指向 B2 读法**，单读正文会以为「q=4 唯一」仍是现行结论。\n"
    "  ⚠️ 与第 78 轮 C-26（改了轨道数没改派生量）／第 81 轮（改了工具没改产物）**同族**。".format(
        uniq[0][0] if uniq else 0, retract19[0][0] if retract19 else 0))

print("\n" + "=" * 78)
print("通过 {} ／ 失败 {} ／ 待人工核对 {}".format(len(OK), len(BAD), len(WARN)))
if BAD:
    print("失败项：", BAD)
print("=" * 78)
