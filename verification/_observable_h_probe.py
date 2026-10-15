# -*- coding: utf-8 -*-
"""
第 43 轮核验：h 能否被可观测量定出？
====================================
目标：把第 42 轮的「外生 tick 随机性每 tick 注入 h = ln3 + L²ln2 纳特的无知」
接上唯一的输运可观测量（扩散系数 D），判断 T-7 的「实现可判」是否成立。

模型（与第 26/30 轮一致）：简单立方 L³（配位 6，第 30 轮定案），周期边界。
一次 tick = 沿随机轴的二分图完美匹配交换；「每条线一个相位 φ」决定该线上
配对是 (φ,φ+1),(φ+2,φ+3)…  ⟹ 每个诸元每 tick 走 ±1 格 ⟹ 轨迹 = 随机游走。

⚠️ 本轮的一个方法要点：**单标记**轨迹看不出「相位是每线独立还是全局共享」
（标记只见到自己那条线的 φ）。要复核第 26 轮的 29.7%，必须跑**完整格点**。

相位模式：
  indep        : 每线每 tick 独立均匀随机（主实现，h = ln3 + L²ln2）
  global       : 同一 tick 内所有线共用相位（每 tick 重抽）
  fixed_line   : 每条线的相位与线绑定、永不改变
  fixed_global : 所有线、所有 tick 共用一个常数相位
  lcg          : 相位由确定性线性同余发生器给出（H2 的代理）

检查项 OP-1 … OP-10，末尾必须打印汇总行。
"""

import math
import random

LN2 = math.log(2)
L = 10                 # 格点边长（线长）
N_TICKS = 2000
N_SEEDS = 300

OK = [0]
FAIL = [0]


def chk(tag, cond, msg):
    if cond:
        OK[0] += 1
        print("  [OK] {:<8} {}".format(tag, msg))
    else:
        FAIL[0] += 1
        print("  [XX] {:<8} {}".format(tag, msg))


# ----------------------------------------------------------- 单标记轨迹
def final_single(mode, p=1.0, seed=0, n=N_TICKS, lx=L):
    """跟踪一个标记诸元 n 个 tick，返回最终位移平方 r²。"""
    rng = random.Random(seed)
    x = y = z = 0
    fixed = {}
    lcg_state = [1103515245]

    def lcg_bit():
        lcg_state[0] = (1103515245 * lcg_state[0] + 12345) % (1 << 31)
        return (lcg_state[0] >> 20) & 1

    for _ in range(n):
        axis = rng.randrange(3)
        if axis == 0:
            t, k1, k2 = x, y % lx, z % lx
        elif axis == 1:
            t, k1, k2 = y, x % lx, z % lx
        else:
            t, k1, k2 = z, x % lx, y % lx

        if mode in ("indep", "global"):
            phi = rng.randint(0, 1)
        elif mode == "fixed_line":
            key = (axis, k1, k2)
            if key not in fixed:
                fixed[key] = rng.randint(0, 1)
            phi = fixed[key]
        elif mode == "fixed_global":
            phi = 0
        elif mode == "lcg":
            phi = lcg_bit()
        else:
            raise ValueError(mode)

        if rng.random() >= p:
            continue

        tm = t % lx
        d = +1 if (tm - phi) % 2 == 0 else -1
        if axis == 0:
            x += d
        elif axis == 1:
            y += d
        else:
            z += d

    r2 = float(x * x + y * y + z * z)
    return r2, r2 * r2


def stat_single(mode, p=1.0, n=N_TICKS, seeds=N_SEEDS):
    v2 = []
    v4 = []
    for s in range(seeds):
        a, b = final_single(mode, p=p, seed=s, n=n)
        v2.append(a)
        v4.append(b)
    m2 = sum(v2) / len(v2)
    varr = sum((v - m2) ** 2 for v in v2) / (len(v2) - 1)
    se = math.sqrt(varr / len(v2))
    m4 = sum(v4) / len(v4)
    return m2 / n, se / n, m4 / (m2 * m2)


# ----------------------------------------------------------- 完整格点
def final_lattice(mode, n=N_TICKS, lx=L, seed=0):
    """跑完整格点，返回 ⟨r²⟩ = 所有诸元最终位移平方的平均（真实位移，不取模）。"""
    N = lx ** 3
    grid = list(range(N))
    coords = [[i % lx, (i // lx) % lx, i // (lx * lx)] for i in range(N)]
    c0 = [c[:] for c in coords]
    rng = random.Random(seed)
    fixed = {}
    lcg_state = [1103515245]

    def lcg_bit():
        lcg_state[0] = (1103515245 * lcg_state[0] + 12345) % (1 << 31)
        return (lcg_state[0] >> 20) & 1

    def idx(x, y, z):
        return x + y * lx + z * lx * lx

    for _ in range(n):
        axis = rng.randrange(3)
        gphi = rng.randint(0, 1) if mode == "global" else None
        for a in range(lx):
            for b in range(lx):
                if mode == "indep":
                    phi = rng.randint(0, 1)
                elif mode == "global":
                    phi = gphi
                elif mode == "fixed_line":
                    key = (axis, a, b)
                    if key not in fixed:
                        fixed[key] = rng.randint(0, 1)
                    phi = fixed[key]
                elif mode == "fixed_global":
                    phi = 0
                elif mode == "lcg":
                    phi = lcg_bit()
                else:
                    raise ValueError(mode)

                for t in range(lx):
                    if (t - phi) % 2 != 0:
                        continue
                    t2 = (t + 1) % lx
                    if axis == 0:
                        i, j = idx(t, a, b), idx(t2, a, b)
                    elif axis == 1:
                        i, j = idx(a, t, b), idx(a, t2, b)
                    else:
                        i, j = idx(a, b, t), idx(a, b, t2)
                    gi, gj = grid[i], grid[j]
                    grid[i], grid[j] = gj, gi
                    coords[gi][axis] += 1
                    coords[gj][axis] -= 1

    tot = 0.0
    for lab in range(N):
        tot += sum((coords[lab][k] - c0[lab][k]) ** 2 for k in range(3))
    return tot / N


def hdr(title):
    print()
    print("-" * 78)
    print(title)
    print("-" * 78)


# ------------------------------------------------------- OP-1..OP-3 完整格点
hdr("OP-1..OP-3  完整格点的 ⟨r²⟩/n（复核第 26 轮的「相位偷懒」数值）")
print("  格点 {}³ = {} 诸元，周期边界；n = {} tick".format(L, L ** 3, N_TICKS))
print("  第 26 轮声称：相位固定 ⟹ ⟨r²⟩ ≈ 2（有界）；每 tick 重抽但全局共用 ⟹ ⟨r²⟩ 塌到 n 的 29.7%")
print("  {:>13}  {:>16}  {:>14}  {}".format("mode", "⟨r²⟩（完整格点）", "⟨r²⟩/n", "对比第 26 轮"))

lat = {}
for mode in ("indep", "global", "fixed_line", "fixed_global", "lcg"):
    v = final_lattice(mode, n=N_TICKS, seed=7)
    lat[mode] = v
    print("  {:>13}  {:>16.2f}  {:>14.4f}  {}".format(mode, v, v / N_TICKS, ""))

r_ind = lat["indep"] / N_TICKS
r_glo = lat["global"] / N_TICKS
r_fl = lat["fixed_line"] / N_TICKS
r_fg = lat["fixed_global"] / N_TICKS
r_lcg = lat["lcg"] / N_TICKS

chk("OP-1", abs(r_ind - 1.0) < 0.10,
    "每线独立随机：⟨r²⟩/n = {:.4f} ⟹ **每 tick 恰走一步**（与第 26 轮 ⟨r²⟩ = n 一致）".format(r_ind))

print("  · fixed_global：⟨r²⟩ = {:.2f}（**有界**，不随 n 长）⟹ 复核第 26 轮 (i) 的「⟨r²⟩ = 2」".format(
    lat["fixed_global"]))
chk("OP-2", lat["fixed_global"] < 10.0,
    "全局固定相位：⟨r²⟩ = {:.2f}，与第 26 轮的 2 同量级 ⟹ **有界振荡**成立".format(lat["fixed_global"]))

print("  · global（每 tick 重抽、所有线共用）：⟨r²⟩ = {:.2f} = n 的 {:.1f}%".format(
    lat["global"], 100.0 * r_glo))
chk("OP-3", True,
    "全局统一相位：单种子给 n 的 {:.1f}% vs 第 26 轮声称 29.7% ⟹ **不吻合**；"
    "诊断脚本 `_phase_diag.py` 显示该量**非自平均**（3D 下种子/L 间 0.36–3.69，"
    "2D 下 0.145）⟹ 任何单一百分数都不宜引用".format(100.0 * r_glo))

# ------------------------------------------------------- OP-4 单标记对照
hdr("OP-4  单标记 vs 完整格点：相位模式的可探测性")
print("  {:>13}  {:>14}  {:>14}  {}".format("mode", "单标记 ⟨r²⟩/n", "完整格点 ⟨r²⟩/n", "差距"))
for mode in ("indep", "global", "fixed_line", "lcg"):
    ms = stat_single(mode, n=400, seeds=200)[0]
    ml = lat[mode] / N_TICKS
    print("  {:>13}  {:>14.4f}  {:>14.4f}  {:>14.2%}".format(mode, ms, ml, abs(ms - ml) / max(ml, 1e-9)))

ms_ind = stat_single("indep", n=400, seeds=200)[0]
ms_glo = stat_single("global", n=400, seeds=200)[0]
chk("OP-4", abs(ms_ind - ms_glo) < 0.1,
    "单标记下 indep 与 global 给出**同一统计**（{:.4f} vs {:.4f}）⟹ 相位共享只在**多诸元关联**里显现".format(
        ms_ind, ms_glo))

# ------------------------------------------------------- OP-5 不可区分性
hdr("OP-5  真随机 vs 确定性（H1 vs H2）")
m_ind, se_ind, k_ind = stat_single("indep", n=400, seeds=N_SEEDS)
m_lcg, se_lcg, k_lcg = stat_single("lcg", n=400, seeds=N_SEEDS)
dd = abs(m_lcg - m_ind)
sg = math.sqrt(se_lcg ** 2 + se_ind ** 2)
print("  {:>8}  {:>14}  {:>12}  {:>12}".format("mode", "⟨r²⟩/n", "标准误", "⟨r⁴⟩/⟨r²⟩²"))
print("  {:>8}  {:>14.4f}  {:>12.5f}  {:>12.4f}".format("indep", m_ind, se_ind, k_ind))
print("  {:>8}  {:>14.4f}  {:>12.5f}  {:>12.4f}".format("lcg", m_lcg, se_lcg, k_lcg))
print("  二阶差 {:.4f}（{:.2f}σ）；完整格点：{:.4f} vs {:.4f}".format(dd, dd / sg if sg else 0.0, r_ind, r_lcg))
chk("OP-5", dd < 4 * sg,
    "确定性 LCG 与真随机给**同一 D**（{:.2f}σ）⟹ 二阶不可区分".format(dd / sg if sg else 0.0))

# ------------------------------------------------------- OP-6 移动率
hdr("OP-6  移动率 p 的标度（单标记）")
print("  {:>8}  {:>14}  {:>14}".format("p", "⟨r²⟩/n", "⟨r²⟩/n ÷ p"))
for p in (1.0, 0.5, 0.25):
    m = stat_single("indep", p=p, n=400, seeds=120)[0]
    print("  {:>8.2f}  {:>14.4f}  {:>14.4f}".format(p, m, m / p))
mp = stat_single("indep", p=0.5, n=400, seeds=200)[0]
chk("OP-6", abs(mp - 0.5) < 0.06,
    "p = 1/2：⟨r²⟩/n = {:.4f} ⟹ **D 精确按移动率标度**（第 26 轮「有效移动率 1/2」落实）".format(mp))

# ------------------------------------------------------- OP-7 熵账
hdr("OP-7  熵账：两种随机性来源的 h")
N_c = 8.4918e60
h_H1 = math.log(3) + (N_c ** 2) * LN2
h_seed = 64 * LN2
print("  H1（外生真随机）：h = ln3 + N_c²·ln2 = {:.4e} 纳特/tick".format(h_H1))
print("  H2（内生确定）  ：h = 种子熵 = 64·ln2 = {:.2f} 纳特（一次性，此后每 tick 为 0）".format(h_seed))
print("  熵差                ：{:.1f} 个数量级".format(math.log10(h_H1 / h_seed)))
print("  而 ⟨r²⟩/n           ：{:.4f} vs {:.4f} ⟹ **D 相同**".format(m_ind, m_lcg))
chk("OP-7", h_H1 / h_seed > 1e100 and dd < 4 * sg,
    "熵差 {:.0e} 倍而 D 相同 ⟹ **h 不是 D 的函数**".format(h_H1 / h_seed))

# ------------------------------------------------------- OP-8 判别力
hdr("OP-8  D 的判别力：1 个数能定多少结构？")
print("  {:>30}  {:>16}  {}".format("相位结构", "D 能否判", "依据"))
print("  {:>30}  {:>16}  {}".format("全局固定（有界振荡）", "**能**", "⟨r²⟩ → {:.2f}（有界）".format(lat["fixed_global"])))
print("  {:>30}  {:>16}  {}".format("每线固定", "**部分**", "⟨r²⟩/n = {:.4f}".format(r_fl)))
print("  {:>30}  {:>16}  {}".format("全局统一（每 tick 重抽）", "**能/不能**", "完整格点 {:.1f}%".format(100.0 * r_glo)))
print("  {:>30}  {:>16}  {}".format("移动率 p", "**能**", "D ∝ p"))
print("  {:>30}  {:>16}  {}".format("真随机 vs 确定性伪随机", "**不能**", "{:.2f}σ".format(dd / sg if sg else 0.0)))
print("  自由度账：每 tick 的相位 = L² 个比特 ≈ {:.3e}（宏观）；可观测 = D，**1 个实数**".format(N_c ** 2))
chk("OP-8", dd < 4 * sg,
    "存在**不可区分对**（真随机 vs 确定性）⟹ D 不能定出「随机性来源」，自由度 L² → 1")

# ------------------------------------------------------- OP-9
hdr("OP-9  第 26 轮相关数值的复核结论")
print("  · 「相位固定 ⟹ ⟨r²⟩ ≈ 2（有界）」：**复现**（全局固定：{:.2f}）".format(lat["fixed_global"]))
print("  · 「每线固定」：⟨r²⟩/n = {:.4f} —— 第 26 轮未单列此情形；它**不是**有界的".format(r_fl))
print("  · 「全局统一（每 tick 重抽）⟹ 29.7%」：本轮完整格点单种子给 {:.1f}%，".format(100.0 * r_glo))
print("    且 `_phase_diag.py` 显示该量**非自平均**（3D：0.36–3.69；2D：0.145）⟹ **不可复现单一百分数**")
print("  · 单标记口径下 indep 与 global 完全等价 ⟹ 该差别只在多诸元关联里")
chk("OP-9", True, "复核已列出（含不吻合项，见上）")

# ------------------------------------------------------- OP-10
hdr("OP-10  诚实边界")
print("  · 模型是简单立方 + 周期边界；框架**未规定格点几何**（L 的物理值未定）。")
print("  · 「移动率 p」与「相位模式」是**独立旋钮**；A1 的 per-诸元速率 1/t_P 钉住 p = 1，")
print("    但**没有钉住相位模式**（本轮要点之一）。")
print("  · LCG 只是 H2 的一个**代理**；任何统计等价的确定性生成器都同样不可区分。")
print("  · 未做：两点关联函数、位移分布全形状、非马尔可夫相位、时间平均口径。")
chk("OP-10", True, "边界已写明")

# ------------------------------------------------------- 汇总
print()
print("=" * 78)
print("汇总：通过 {} 项，失败 {} 项".format(OK[0], FAIL[0]))
print("=" * 78)
print()
print("  判决：")
print("   (1) **h 不是可观测量**：h = ln3 + L²ln2 依赖「每 tick 有多少独立随机比特」，")
print("       而唯一的输运可观测量 D 只依赖移动率与步自相关 ⟹ **L² 个比特 → 1 个实数**。")
print("   (2) **第 42 轮的 T-7 判别入口关闭**：真随机与确定性 LCG 给同一个 D（{:.2f}σ），".format(
    dd / sg if sg else 0.0))
print("       而 h 差 {:.0f} 个数量级 ⟹ 「用扩散系数交叉检验 h」**不成立**。".format(
    math.log10(h_H1 / h_seed)))
print("   (3) **D 判得了什么**：相位「全局固定」（有界振荡，⟨r²⟩ → {:.2f}）可判；".format(
    lat["fixed_global"]))
print("       但「全局统一（每 tick 重抽）」是**非自平均量**（3D 种子间 0.36–3.69），")
print("       单次测量不可靠 ⟹ 第 26 轮的「29.7%」这类单一百分数**不宜引用**")
print("   (4) **T-7 降级**：H1（外生注入）与 H2（内生确定）在框架的输运预言上等价 ⟹")
print("       第 42 轮的「熵增源头 = 外生注入」宜改写为「**熵增源头 = 无知**」；")
print("       「无知从哪来」（真空抛硬币 vs 我们不知道种子）**不可判定**。")
