# -*- coding: utf-8 -*-
"""
λ_c(∞) 三判据分析 + 有限尺寸外推（第 101 轮 · 甲-2）

判据：
  J1  χ 峰        χ(λ) = −d⟨A_c⟩/dλ        （原 A1 报告的判据；微分型，对网格/噪声敏感）
  J2  保真度磁化率 χ_F(λ) = −2 ln F / δλ²   （F = |⟨ψ(λ)|ψ(λ+δλ)⟩|；不需微分，峰更锐）
  J3  E0 二阶导    d²E/dλ²                  （对应 ⟨ΣX_f⟩ 的"磁化率"）

⚠️ Binder 累积量在本模型**恒等失效**：A_c² = I ⟹ ⟨A²⟩≡1、⟨A⁴⟩≡1 ⟹ Binder ≡ 2/3。
   （这是本模型的特殊性质，不是实现问题 —— 报告中必须写明，否则会被当成"漏做了一个判据"。）

外推：λ_c(L̄) = λ_c(∞) + a·L̄^{−1}，L̄ = V^{1/3}。
  ⚠️ 只外推 λ_c、**不**同时拟合 ν —— 3 个尺寸定不了 (λ_c, ν, a) 三个参数（铁律 5：可识别性）。
"""
import sys
import numpy as np


def peak_quad(lam, y):
    """峰区三点二次拟合给亚网格峰位。返回 (λ0, y0, 是否越界)

    ⚠️ 局部数组 `x` 只有 3 个点 ⟹ 边界判断必须用 `x[0]`/`x[2]`，
       不能用全局下标 `i`（第一版写成 `x[i-1]`/`x[i+1]`，i=4 时越界 —— 本轮已修）。
    """
    lam = np.asarray(lam, float); y = np.asarray(y, float)
    i = int(np.argmax(y))
    if i == 0 or i == len(y) - 1:
        return float(lam[i]), float(y[i]), True
    x = lam[i - 1:i + 2]; f = y[i - 1:i + 2]
    c = np.polyfit(x, f, 2)
    if c[0] >= 0:                      # 非凹 ⟹ 退回网格点
        return float(lam[i]), float(y[i]), True
    x0 = -c[1] / (2 * c[0])
    if not (x[0] <= x0 <= x[2]):
        return float(lam[i]), float(y[i]), True
    return float(x0), float(np.polyval(c, x0)), False


def crit_from_file(fn):
    d = np.load(fn, allow_pickle=True)
    lam = d['lams']; ac = d['ac']; E = d['E']; fid = d['fid']
    dims = tuple(int(x) for x in d['dims'])
    V = int(np.prod(dims)); Lbar = V ** (1.0 / 3.0)

    # J1 χ 峰（原始 np.gradient + 峰区二次拟合）
    chi = -np.gradient(ac, lam)
    l1, c1, ob1 = peak_quad(lam, chi)

    # J1s χ 峰（Savitzky–Golay 平滑后求导；窗口自适应，至少 5 点）
    l1s, c1s, ob1s = (np.nan, np.nan, True)
    if len(lam) >= 7:
        from scipy.signal import savgol_filter
        w = min(len(lam) if len(lam) % 2 == 1 else len(lam) - 1, 11)
        w = max(w, 5)
        acs = savgol_filter(ac, w, 3)
        chis = -np.gradient(acs, lam)
        l1s, c1s, ob1s = peak_quad(lam, chis)

    out = {'dims': dims, 'V': V, 'Lbar': Lbar, 'n': int(d['n']), 'Nc': int(d['Nc']),
           'chi_bond': int(d['chi']), 'lams': lam, 'ac': ac, 'E': E, 'X': chi,
           'J1': (l1, c1, ob1), 'J1s': (l1s, c1s, ob1s)}

    # J2 保真度磁化率（⚠️ 必须排除 |F|≪1 的点：简并基态跳跃或正交分支）
    dl = np.diff(lam)
    ok = np.isfinite(fid[1:]) & (np.abs(fid[1:]) > 0.5)
    out['J2'] = (np.nan, np.nan, True)
    if ok.sum() >= 5:
        chiF = np.where(ok, -2.0 * np.log(np.clip(np.abs(fid[1:]), 1e-300, 1.0)) / dl ** 2, np.nan)
        lamF = 0.5 * (lam[1:] + lam[:-1])
        m = np.isfinite(chiF)
        if m.sum() >= 5:
            out['J2'] = peak_quad(lamF[m], chiF[m])
            out['J2n'] = int(ok.sum())

    # J3 E0 二阶导（⚠️ 排除两端 15%：边界处梯度不可靠）
    d1 = np.gradient(E, lam); d2 = np.gradient(d1, lam)
    k = max(2, int(round(0.15 * len(lam))))
    if len(lam) - 2 * k >= 5:
        out['J3'] = peak_quad(lam[k:len(lam) - k], d2[k:len(lam) - k])
    else:
        out['J3'] = (np.nan, np.nan, True)

    out['E0_lam0'] = float(E[0]); out['expect_lam0'] = float(-out['Nc'])
    out['fid_ok'] = int(ok.sum()); out['npts'] = len(lam)
    return out


def main(tags):
    R = {}
    print("=" * 112)
    print("{:<18} {:>5} {:>7} {:>5} {:>5} | {:>9} {:>9} {:>9} {:>9}".format(
        "系统", "V", "L̄", "n", "点数", "J1 χ峰", "J1s 平滑", "J2 保真度", "J3 E''峰"))
    print("=" * 112)
    for t, fn in tags:
        try:
            r = crit_from_file(fn)
        except Exception as e:
            print("  {:<18} 读取失败: {}".format(t, e)); continue
        R[t] = r
        print("{:<18} {:>5} {:>7.3f} {:>5} {:>5} | {:>9.4f} {:>9.4f} {:>9.4f} {:>9.4f}".format(
            t, r['V'], r['Lbar'], r['n'], r['npts'],
            r['J1'][0], r['J1s'][0], r['J2'][0], r['J3'][0]))
        print("{:<18} {:>5} {:>7} {:>5} {:>5} | {:>9} {:>9} {:>9} {:>9}   (越界 {}/{}/{}/{})".format(
            "", "χ={}".format(r['chi_bond']), "", "", "",
            "χmax=%.3f" % r['J1'][1],
            "-" if not np.isfinite(r['J1s'][1]) else "χsmax=%.3f" % r['J1s'][1],
            "-" if not np.isfinite(r['J2'][1]) else "%.1e" % r['J2'][1],
            "d2max=%.2f" % r['J3'][1],
            r['J1'][2], r['J1s'][2], r['J2'][2], r['J3'][2]))

    # ---------------- 1/L̄ 外推 ----------------
    print()
    print("=" * 112)
    print("1/L̄ 外推（λ_c(L̄) = λ_c(∞) + a/L̄；只拟 2 参数 ⟹ 可识别）")
    print("=" * 112)
    keys = sorted(R.keys(), key=lambda k: R[k]['V'])
    for J in ('J1', 'J1s', 'J2', 'J3'):
        xs, ys, ns = [], [], []
        for k in keys:
            r = R[k]; v = r[J][0]
            if np.isfinite(v) and not r[J][2]:
                xs.append(1.0 / r['Lbar']); ys.append(v); ns.append(k)
        if len(xs) < 2:
            print("  {}: 有效点不足（需 ≥2，且不越界）".format(J)); continue
        xs = np.array(xs); ys = np.array(ys)
        c = np.polyfit(xs, ys, 1)
        res = ys - np.polyval(c, xs)
        print("  {}: λ_c(∞) = {:.4f}（斜率 a = {:+.4f}）｜残差 RMS = {:.4f}｜{} 点".format(
            J, c[1], c[0], float(np.sqrt(np.mean(res ** 2))), len(xs)))
        print("       " + "  ".join("{}: {:.4f}".format(n, y) for n, y in zip(ns, ys)))

    # ---------------- 跨尺寸 ⟨A_c⟩ 交叉 ----------------
    print()
    print("=" * 112)
    print("跨尺寸 ⟨A_c⟩ 比较（交叉点 ≈ λ_c；若两曲线不相交，给出最小间距点）")
    print("=" * 112)
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            ki, kj = keys[i], keys[j]
            ri, rj = R[ki], R[kj]
            if ri['Nc'] == rj['Nc'] and ri['chi_bond'] == rj['chi_bond']:
                pass
            lo = max(ri['lams'][0], rj['lams'][0]); hi = min(ri['lams'][-1], rj['lams'][-1])
            g = np.linspace(lo, hi, 500)
            ai = np.interp(g, ri['lams'], ri['ac']); aj = np.interp(g, rj['lams'], rj['ac'])
            diff = ai - aj
            s = np.where(np.diff(np.sign(diff)))[0]
            if len(s) == 0:
                k0 = int(np.argmin(np.abs(diff)))
                print("  {} vs {}: 无交叉；最小间距 {:.5f} 在 λ = {:.4f}".format(
                    ki, kj, abs(diff[k0]), g[k0]))
            else:
                xs = []
                for k in s:
                    x0, x1 = g[k], g[k + 1]; d0, d1 = diff[k], diff[k + 1]
                    xs.append(x0 - d0 * (x1 - x0) / (d1 - d0))
                print("  {} vs {}: 交叉于 λ = {}".format(
                    ki, kj, ", ".join("{:.4f}".format(x) for x in xs)))

    print()
    print("=== 3D Ising 参照 ===")
    print("  3D Ising β_c = 0.2216544(3)（精确已知）；若「3+1D 弦网 ↔ 3D Z₂ 格点规范 ↔ 3D Ising」")
    print("  对偶精确成立，则 λ_c(∞) 应 = 0.22165。偏差方向和大小即对偶映射的定量检验。")
    print()
    for k in keys:
        r = R[k]
        print("  {:<18} {}×{}×{}: E(λ=0)={:.6f}（应={}）｜χ_bond={}｜fid 可用点 {}/{}".format(
            k, *r['dims'], r['E0_lam0'], r['expect_lam0'], r['chi_bond'],
            r.get('fid_ok', -1), r['npts']))
    return R


if __name__ == "__main__":
    tags = [("2×2×2 c8 粗", "_lc3d_101_t222chi8.npz"),
            ("2×2×2 c8 细", "_lc3d_101_f222chi8.npz"),
            ("3×2×2 c8 粗", "_lc3d_101_t322chi8.npz"),
            ("3×2×2 c8 细", "_lc3d_101_f322chi8.npz"),
            ("3×3×2 c8 粗", "_lc3d_101_t332chi8.npz"),
            ("3×3×2 c8 细", "_lc3d_101_f332chi8.npz"),
            ("3×3×3 c8 粗", "_lc3d_101_t333chi8.npz"),
            ("3×3×3 c8 细", "_lc3d_101_f333chi8.npz")]
    if len(sys.argv) > 1:
        want = set(sys.argv[1:])
        tags = [t for t in tags if t[0] in want]
    main(tags)
