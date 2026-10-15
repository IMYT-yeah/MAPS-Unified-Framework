# -*- coding: utf-8 -*-
"""
甲-3 分析（第 102 轮）：Binder 交叉 + 保真度磁化率 + 能隙极小 —— 三判据定位 h_c

判据（甲-2 的教训：必须先量化判据自身的分辨率）：
  J1  **Binder 交叉**：U(h,L) = 1 − ⟨m⁴⟩/(3⟨m²⟩²)；相变处 U 与 L 无关 ⟹ 交叉点 = h_c
      （最可靠：**不需要任何数值微分**）
  J2  **保真度磁化率** χ_F = −2 lnF/δh²（F = |⟨ψ(h)|ψ(h+δh)⟩|）
  J3  **能隙** Δ = E1−E0 的极小点（有限尺寸下相变附近能隙最小）

⚠️ 本模型里 m = Σ_e ⟨X_e⟩/n 是**极化侧**的序参量（h→∞ 时 m→1），故 Binder 的
   有序/无序**方向与常规相反**：h 大 ⟹ U→2/3；h 小 ⟹ U→0。交叉仍发生在 h_c。
"""
import sys
import numpy as np

FILES = [("2×2", "_toric102_t22.npz"), ("2×3", "_toric102_t23.npz"),
         ("3×3", "_toric102_t33.npz"), ("3×4", "_toric102_t34.npz"),
         ("4×4", "_toric102_t44.npz")]


def load(fn):
    d = np.load(fn)
    r = d["rows"]
    return dict(h=r[:, 0], E0=r[:, 1], gap=r[:, 2], m=r[:, 3], m2=r[:, 4],
                m4=r[:, 5], U=r[:, 6], F=r[:, 7],
                dims=tuple(int(x) for x in d["dims"]), dim=int(d["dim"]))


def peak_quad(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    i = int(np.nanargmax(y))
    if i == 0 or i == len(y) - 1:
        return float(x[i]), float(y[i]), True
    xs = x[i - 1:i + 2]; ys = y[i - 1:i + 2]
    c = np.polyfit(xs, ys, 2)
    if c[0] >= 0:
        return float(x[i]), float(y[i]), True
    x0 = -c[1] / (2 * c[0])
    if not (xs[0] <= x0 <= xs[2]):
        return float(x[i]), float(y[i]), True
    return float(x0), float(np.polyval(c, x0)), False


def main():
    R = {}
    print("=" * 104)
    print("{:<8} {:>10} {:>9} {:>9} {:>11} {:>11} {:>11}".format(
        "系统", "扇区维", "h(Binder)", "h(χ_F)", "h(Δmin)", "U@0.30", "U@0.40"))
    print("=" * 104)
    for tag, fn in FILES:
        try:
            R[tag] = load(fn)
        except Exception as e:
            print("  {:<8} 缺: {}".format(tag, e)); continue
    for tag, r in R.items():
        h = r["h"]; U = r["U"]
        # J1 Binder：与"最粗"尺寸的交叉（两两交叉中点）
        # J2 保真度磁化率
        dh = np.diff(h)
        Fv = r["F"][1:]
        lamF = 0.5 * (h[1:] + h[:-1])
        ok = np.isfinite(Fv) & (Fv > 0.5)
        lF, vF, obF = (np.nan, np.nan, True)
        if ok.sum() >= 5:
            chiF = np.where(ok, -2.0 * np.log(np.clip(Fv, 1e-300, 1.0)) / dh ** 2, np.nan)
            m = np.isfinite(chiF)
            if m.sum() >= 5:
                lF, vF, obF = peak_quad(lamF[m], chiF[m])
        # J3 能隙极小
        lD, vD, obD = peak_quad(h, -r["gap"])
        name = "{}×{}".format(*r["dims"])
        print("{:<8} {:>10} {:>9} {:>9.4f} {:>11.4f} {:>11.4f} {:>11.4f}".format(
            name, r["dim"], "-", lF, lD, r["U"][np.argmin(abs(h - 0.30))],
            r["U"][np.argmin(abs(h - 0.40))]))

    # ---------------- J1 Binder 交叉（两两） ----------------
    print()
    print("=" * 104)
    print("J1 **Binder 交叉**（两两尺寸；交叉点 = h_c，**不需数值微分**）")
    print("=" * 104)
    keys = list(R.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            a, b = R[keys[i]], R[keys[j]]
            lo = max(a["h"][0], b["h"][0]); hi = min(a["h"][-1], b["h"][-1])
            g = np.linspace(lo, hi, 2000)
            ua = np.interp(g, a["h"], a["U"]); ub = np.interp(g, b["h"], b["U"])
            d = ua - ub
            s = np.where(np.diff(np.sign(d)))[0]
            nm = "{}×{}".format(*a["dims"]) + " vs " + "{}×{}".format(*b["dims"])
            if len(s) == 0:
                k = int(np.argmin(abs(d)))
                print("  {:<16} 无交叉；最小间距 {:.5f} @ h={:.4f}".format(nm, abs(d[k]), g[k]))
            else:
                xs = []
                for k in s:
                    x0, x1 = g[k], g[k + 1]; d0, d1 = d[k], d[k + 1]
                    xs.append(x0 - d0 * (x1 - x0) / (d1 - d0))
                print("  {:<16} 交叉于 h = {}".format(nm, ", ".join("{:.4f}".format(x) for x in xs)))

    print()
    print("=== 参照 ===")
    print("  文献 toric code + 横场：h_c ≈ 0.328474（论文 §10.1b 引 iPEPS）")
    print("  框架 A3：J/K = 3 ⟹ 「h_c = K/J = 1/3 = 0.3333」")
    print("  1/0.328474 = {:.6f}；与 3 的相对差 = {:.2f}%".format(
        1 / 0.328474, abs(1 / 0.328474 - 3) / 3 * 100))
    print("  ⟹ 「J/K = 3」与「1/h_c = 3.0444」的相对差 = {:.2f}%".format(
        abs(3 - 1 / 0.328474) / (1 / 0.328474) * 100))


if __name__ == "__main__":
    main()
