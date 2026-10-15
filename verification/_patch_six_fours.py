# -*- coding: utf-8 -*-
"""第 29 轮补丁：§4.10「六处 4」的分层判定（追加在上一轮的分级修正注之后）
中英同步；锚点必须恰好命中一次。"""
import io
import sys

BASE = "C:/Users/Administrator/Desktop/2026-08-20-21-43-34/outputs/"
ZH = BASE + "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN = BASE + "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
ACTIONS = []

def patch(path, old, new, tag):
    s = io.open(path, encoding="utf-8").read()
    n = s.count(old)
    if n != 1:
        print("  [XX] %-36s 锚点命中 %d 次 —— 拒绝改动" % (tag, n))
        ACTIONS.append((tag, False))
        return
    io.open(path, "w", encoding="utf-8").write(s.replace(old, new))
    print("  [OK] %-36s 已替换" % tag)
    ACTIONS.append((tag, True))

# ---------------------------------------------------------------- ZH
zh_anchor = "建议本表述降调为「六处数值均为 4，其中若干同源、若干独立」。"
zh_new = zh_anchor + """

> **【v2.9 分层判定（第 29 轮，逐条追溯）】** 结论：
> · **同源组（4 处）**：4l_P² 相干截面、每 4 面元 1 比特、挂谷 packing 1/4、正四面体 4 方向簇 —— 全部锚在 **k = 4**（= 本节定理 1 = **LST/Borsuk**）；
> · **独立组（2 处）**：表面 4 邻居（= (d−1) 维表面网格配位 **2(d−1)**）、Clifford 4 分量（= Cl(1,d) 表示维数 **2^⌊(d+1)/2⌋**，已独立核对 D = 3/4/5/6 = 2/4/4/8）。
> 三组取值同时相等 **⟺ d = 3（空间三维）**，且 **(n, d) = (4, 3) 是唯一解**（枚举 2 ≤ d < 200 确认唯一）。
> ⟹ 这几处「4」的相等**底层等价于「空间三维」**。⚠️ 这只是**自洽性条件，不能反推三维**（d = 3 为【本框架设定】）。
> ⚠️ 另登记张力 **T-6**：§4.9 引理 1「平面内 4 + 平面外 2」给出 **6 个格点方向**（= 简单立方 6 邻居，其中 2 个被卷曲），而本节定理给 **k = 4** —— 两者对**体配位数**口径不同（4 vs 6）；§8.6.8 的「金刚石结构」依赖「每个 S² 方向 = 一条格点键」这一步，**该步尚未独立论证**，待裁决。
> ⚠️ 标注错位（建议修正）：① 表面 4 邻居标的「本框架推论」其实直接依据 §4.9 引理 1【本框架设定】；④「每 4 面元 1 比特」标【本框架设定】但可由 ③ 直接推出。"""
patch(ZH, zh_anchor, zh_new, "ZH 六处4 分层判定")

# ---------------------------------------------------------------- EN
en_anchor = 'Recommend downgrading this statement to "**all six numbers are 4; some share a source, some are independent**".'
en_new = en_anchor + """

> **【v2.9 layered verdict (round 29, item-by-item tracing)】** Findings:
> · **Co-sourced group (4 items)**: 4l_P² coherent cross-section, 1 bit per 4 plaquettes, Kakeya packing 1/4, regular-tetrahedron 4-direction cluster — all anchored on **k = 4** (= Theorem 1 of this section = **LST/Borsuk**);
> · **Independent group (2 items)**: surface 4 neighbours (= (d−1)-dimensional surface-lattice coordination **2(d−1)**), Clifford 4 components (= representation dimension of Cl(1,d), **2^⌊(d+1)/2⌋**; independently checked for D = 3/4/5/6 giving 2/4/4/8).
> The three groups take equal values **⟺ d = 3 (three spatial dimensions)**, and **(n, d) = (4, 3) is the unique solution** (enumeration over 2 ≤ d < 200 confirms uniqueness).
> ⟹ The equality of these "4"s is **ultimately equivalent to "space is three-dimensional"**. ⚠️ This is only a **self-consistency condition and cannot be used to derive three-dimensionality** (d = 3 is a 【framework assumption】).
> ⚠️ Also registered: tension **T-6**: §4.9 Lemma 1 ("4 in-plane + 2 out-of-plane") yields **6 lattice directions** (= simple-cubic 6 neighbours, 2 of them curled up), whereas the theorem here gives **k = 4** — the two differ on the **bulk coordination number** (4 vs 6); the "diamond structure" conclusion of §8.6.8 relies on the step "each S² direction = one lattice bond", which **has not been independently argued**. Pending adjudication.
> ⚠️ Label mismatch (worth fixing): ① "4 neighbours of a surface element" is labelled "framework corollary" but rests directly on §4.9 Lemma 1【framework assumption】; ④ "1 bit per 4 plaquettes" is labelled 【framework assumption】 but follows directly from ③."""
patch(EN, en_anchor, en_new, "EN six 4s layered verdict")

print("\n" + "=" * 58)
ok = sum(1 for _, v in ACTIONS if v)
print("补丁动作 %d 项，成功 %d，失败 %d" % (len(ACTIONS), ok, len(ACTIONS) - ok))
sys.exit(0 if ok == len(ACTIONS) else 1)
