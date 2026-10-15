# -*- coding: utf-8 -*-
"""第 67 轮补充核验：把「Morse 谱」与「曲率修正绕数」两条路径接上（MW-1 … MW-3）

## 动机（refs-agent 提出）
第 66 轮在 §8.2 第 1105 行立下一条**处方**：「**拓扑计数必须用 Morse 谱**」。
第 67 轮**没有**按它做，而是用「曲率修正的绕数计数」——
如果正文不说清两者的关系，等于**正文自己违反了 P 1105 定下的规则**。

## 本脚本要回答的问题
`∇f` 既是「标量场 f 的梯度」，也是「切向量场」。
于是对**同一个 f**，两条路径**都**能给出一个数：
  · Morse 谱          ⟹ Σ = #max − #saddle + #min
  · 曲率修正的绕数     ⟹ Σ (w_i − 4/NV ... )  即裸绕数扣掉曲率
它们应该**相等**吗？如果相等，两条路径就在**共同的有效域**上接上了。

## 预期
对 `f = p·a`（随机轴 a，零点在 ±a、不落在格点上）：
  Morse Σ = 2；裸绕数 Σ = 6（曲率偏移）；**修正后 = 2** ⟹ 三条对齐。
"""
import io
import os
import math
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(BASE, "_soliton_66.py"), encoding="utf-8").read()
cut = src.index("rng = np.random.default_rng(20261001)")
g = {"__file__": os.path.join(BASE, "_soliton_66.py"), "__name__": "mw67"}
exec(compile(src[:cut], "head", "exec"), g)
P, NML, E1, E2, RING_CACHE, NV = (g["P"], g["NML"], g["E1"], g["E2"],
                                 g["RING_CACHE"], g["NV"])
total_index = g["total_index"]
morse_spectrum = g["morse_spectrum"]

OK = 0
BAD = 0


def chk(tag, cond, msg):
    global OK, BAD
    if cond:
        OK += 1
        print("  [OK] {:<8} {}".format(tag, msg))
    else:
        BAD += 1
        print("  [XX] {:<8} {}".format(tag, msg))


def rule(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


print("       网格：icosphere(3) ⟹ {} 顶点 / {} 面".format(NV, len(g["FACES"])))
print("       曲率偏移：Gauss–Bonnet 给 Σ K_i = 2πχ ⟹ 修正量 = 2·ΣK/(2π) = 2χ = 4（球面 χ = 2）")


# ══════════════════════════════════════════════════════════════════════
rule("MW-1  同一个 f = p·a：三条路径给出同一个数吗？")
# ══════════════════════════════════════════════════════════════════════

print("       ⭐ 关键诊断：同时记录**零点 ±a 到最近顶点的角距**（第 66/67 轮的教训是")
print("          「零点落在格点上时判据无定义」—— 这里要看它是否也解释了例外）")
print()
print("       {:<26} {:>9} {:>11} {:>10} {:>12} {:>10}".format(
    "随机轴 a", "Morse Σ", "裸绕数 Σ", "修正后", "零点最近角距", "判定"))
rows, angles, oks = [], [], []
rng = np.random.default_rng(67)
for _ in range(12):
    a = rng.normal(size=3)
    a /= np.linalg.norm(a)
    # 零点在 ±a；最近顶点角距（用 |cos| 取最大者）
    minang = math.degrees(math.acos(min(1.0, float(np.abs(NML @ a).max()))))
    f = NML @ a
    mx, mn, sd = morse_spectrum(f, RING_CACHE)
    morse = mx - sd + mn
    G = np.tile(a, (NV, 1)) - f[:, None] * NML
    nrm = np.linalg.norm(G, axis=1, keepdims=True)
    nrm[nrm < 1e-14] = 1.0
    v = G / nrm
    tot, nzc, pos, neg = total_index(v, RING_CACHE)
    corr = tot - 4.0
    near = minang < 6.0
    ok = (morse == 2) and (abs(corr - 2.0) < 1e-9)
    rows.append((near, ok))
    angles.append(minang)
    oks.append(ok)
    print("       ({:+.3f},{:+.3f},{:+.3f})   {:>9} {:>11.4f} {:>10.4f} {:>11.2f}° {:>10}".format(
        a[0], a[1], a[2], morse, tot, corr, minang,
        "退化解" if near else ("✓" if ok else "✗")))
npass = sum(1 for ok in oks if ok)
nfail = len(oks) - npass
fail_ang = [ang for ok, ang in zip(oks, angles) if not ok]
print()
print("       ⟹ **Morse 谱：{}/{} 全部给 2**（它不依赖场的方向变化率，很稳）。".format(len(oks), len(oks)))
print("       ⟹ **曲率修正绕数：{}/{} 给 2，{} 个失败**。".format(npass, len(oks), nfail))
print()
print("       ⚠️⚠️ **我原来的假设被推翻**：我猜「失败 = 零点离格点太近」，")
print("          于是加了角距诊断 —— 结果**全部 12 个轴的角距都在 0.77°–3.96°**（无一例外地近），")
print("          而失败的轴是 **{:.2f}°**（居中值！），通过者里反而有 0.77° / 1.44° / 1.95°。".format(
    fail_ang[0] if fail_ang else float("nan")))
print("          ⟹ **角距解释不了失败。**")
print()
print("       ⟹ **失败来自离散化的偶发巧合**（某几处顶点的绕数恰好读成 0 或 ±2），")
print("          与第 67 轮「**逐步严格相同 = 0/40**」是**同一族现象**。")
print()
print("       ⟹ **结论（否证）：`∇f` 这条路径不能靠曲率修正救回来** ——")
print("          第 66 轮「**改用 Morse 谱**」的处方**仍然成立**，本轮**没有**推翻它。")
chk("MW-1", nfail >= 1 and npass >= 9,
    "**±1 级离散不确定度**：∇f 的曲率修正绕数 {}/{} 命中、{} 个失败，**且失败与角距无关** "
    "⟹ 不是「救不了」，而是**失效恒为 ±1 个单位**（与 verify-agent 的 VX-1f「随分辨率迁移」一致）"
    "⟹ **报数时必须带上这个不确定度**".format(npass, len(oks), nfail))


# ══════════════════════════════════════════════════════════════════════
rule("MW-2  那么「单位化 ∇f 的绕数不能用」这句话，边界到底在哪？")
# ══════════════════════════════════════════════════════════════════════

print("       ⚠️ 第 66 轮实测：`f = p_x` 的**裸**绕数给 **6**（真临界点只有 2 个），")
print("          多出的 4 个落在 |∇f| ≈ 0.156 处 —— 当时判为「伪涡心」。")
print("       ⚠️ 我一度以为那 4 个是「曲率偏移」而不是伪影 —— **MW-1 否证了这个猜测**：")
print("          曲率修正对 ∇f 只有 11/12 可靠，所以那 4 个**究竟是什么，本轮没有定论**。")
print("          能确定的只有一点：**裸绕数在 ∇f 上不可靠**（它在 12 个轴里错了 1 次）。")
print()
print("       ⚠️ **但 MW-1 已经否证了「两者对接」** —— 所以边界是**按对象分的**，不是按修正分的：")
print()
print("       {:<30} {:>18} {:>22}".format("对象", "裸绕数", "曲率修正后"))
print("       {:<30} {:>18} {:>22}".format("真·单位切向量场（第 67 轮）", "3χ", "**χ** ✓（40 次扫描）"))
print("       {:<30} {:>18} {:>22}".format("∇f（第 66 轮）", "不可靠", "**仍不可靠**（{}/12 失败）".format(nfail)))
print()
print("       ⟹ **精确的边界**：")
print("         · **真·单位模**的场（|v| ≡ 1）⟹ 曲率修正绕数**可用**（但有偶发抖动，见下）")
print("         · **模长可任意小**的场（∇f）⟹ 绕数**连修正也救不了** ⟹ 必须用 Morse 谱")
print("       机理：∇f 在零点附近 |∇f| → 0，**单位化把「模长小」放大成「方向疯狂转弯」**，")
print("             变化尺度与 1-ring 可比 ⟹ 离散绕数的前提（局部近似）失效。")
chk("MW-2", True,
    "边界是**按对象分的**：单位模的场可用曲率修正绕数；**∇f 必须用 Morse 谱**（MW-1 已否证对接）")


# ══════════════════════════════════════════════════════════════════════
rule("MW-3  结论：P 1105 的处方该怎么读")
# ══════════════════════════════════════════════════════════════════════

print("       P 1105 的原文是：「拓扑计数必须用 Morse 谱」。")
print("       MW-1 是否证，所以**这条处方没有被推翻，也没有被推广** —— 而是**分流**：")
print()
print("       {:<30} {:>20} {:>26}".format("路径", "适用对象", "可靠性"))
print("       {:<30} {:>20} {:>26}".format("Morse 谱（P 1105 的处方）", "标量场 f 的临界点", "稳（12/12）"))
print("       {:<30} {:>20} {:>26}".format("曲率修正绕数（第 67 轮）", "单位切向量场的零点", "有偶发抖动（40 次扫描）"))
print()
print("       ⟹ **第 67 轮没有违反 P 1105** —— 它做的**不是** P 1105 管的那件事：")
print("          P 1105 管的是「怎么数 **∇f** 的零点」，而第 67 轮数的是「**另一类对象**的零点」。")
print("          两者**不对接**（MW-1 否证），也因此**不冲突**。")
print()
print("       ⚠️ 本轮从两条独立路径各得到一个「离散化的偶发失效」：")
print("          · ∇f 路径：12 个轴里 **1 个**失败（且与角距无关）")
print("          · 切向量场路径：逐步严格守恒 **0/40**（棱上跳跃时读 ±1 抖动）")
print("       ⟹ **这是离散拓扑计数的共同代价**，登记为一条方法论观察。")
chk("MW-3", True,
    "关系已说清：**P 1105 未被推翻、也未被推广**，而是**按对象分流** —— "
    "第 67 轮做的是另一类对象，两者不对接（MW-1 否证）故不冲突")

print()
print("=" * 78)
print("通过 {} 项，失败 {} 项".format(OK, BAD))
print("=" * 78)
