# -*- coding: utf-8 -*-
"""
第 100 轮（甲-1 · Lean 侧补完）核验脚本：LF-1 … LF-16
末尾打印「通过 N 项，失败 M 项」。
"""
import io
import os
import re
import json

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
LEAN = os.path.join(ROOT, "MAPS-Unified-Framework", "verification", "lean")
SRC = os.path.join(LEAN, "StormPoC.lean")
HIST = os.path.join(LEAN, "_history")
LOG = r"C:\Users\Administrator\.lean-dl\lake_build_100.log"
PRE = os.path.join(HIST, "StormPoC_备份_2026-10-03第100轮前.lean")

PASS = FAIL = 0


def chk(t, c, m, strict=True):
    global PASS, FAIL
    if c:
        PASS += 1
        print("  [OK] {:<7} {}".format(t, m))
    else:
        if strict:
            FAIL += 1
            print("  [XX] {:<7} {}".format(t, m))
        else:
            print("  [INFO] {:<7} {}".format(t, m))


def hdr(s):
    print("\n" + "=" * 94)
    print(s)
    print("=" * 94)


def rd(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


print("第 100 轮核验（LF · Lean 侧补完：23→24 条待重写 ＋ 2 sorry ＋ 5→6 BX）")

cur = rd(SRC)
pre = rd(PRE)
log = rd(LOG) if os.path.exists(LOG) else ""

hdr("LF-1…4  构建终态（两段式：补丁前 / 补丁后）")
mj = re.search(r"Build completed successfully \((\d+)\s+jobs?\)", log)
chk("LF-1", bool(mj) and mj.group(1) == "8909", "构建日志 = {}".format(mj.group(0) if mj else "未解析到"))
n_err = len(re.findall(r"(?m)^error", log))
n_warn = len(re.findall(r"(?m)^warning", log))
chk("LF-2", n_err == 0 and n_warn == 0, "0 error ＋ 0 warning（实测 {} / {}）".format(n_err, n_warn))

n_sorry_pre = len(re.findall(r"(?m)^\s*sorry\s*$", pre))
n_sorry_cur = len(re.findall(r"(?m)^\s*sorry\s*$", cur))
chk("LF-3", n_sorry_pre == 2 and n_sorry_cur == 0,
    "sorry：补丁前 {} → 补丁后 {}（两段式）".format(n_sorry_pre, n_sorry_cur))

names_pre = set(re.findall(r"(?m)^theorem\s+(\w+)", pre))
names_cur = set(re.findall(r"(?m)^theorem\s+(\w+)", cur))
new = sorted(names_cur - names_pre)
chk("LF-4", len(names_pre) == 23 and len(new) == 32,
    "定理数：补丁前 {} → 补丁后 {}（新增 {}）".format(len(names_pre), len(names_cur), len(new)))

hdr("LF-5…9  分族内容（逐族点名）")
FAM = {
    "BH": ["bh_horizon_iff_critical", "bh_compactness_def", "bh_compactness_at_hubble",
           "bh_compactness_eq_Omega", "bh_compactness_scaling", "bh_frw_inside_uncaptured",
           "bh_frw_outside_anticaptured", "bh_radius_ratio_squared", "bh_discriminator_not_resolved"],
    "AR": ["ar_comoving_energy_identity", "ar_energy_zero_iff_flat", "ar_net_charge_zero",
           "ar_net_energy_not_zero", "ar_k_solved", "ar_curvature_negative_solvable",
           "ar_selfenergy_factor", "ar_k_from_lambda", "ar_flat_iff_lambda_one"],
    "LC": ["lc_gauge_identity", "lc_lambda_eq_2alphabeta", "lc_alpha_pi",
           "lc_lambda_eq_two_pi_beta", "lc_beta_one_iff_lambda_one", "lc_unruh_coefficient",
           "lc_beta_of_lambda_one"],
    "LW": ["lw_omega_k_formula", "lw_apparent_horizon_kappa", "lw_flat_iff_kappa_zero",
           "lw_GH_gives_flat", "lw_HK_omega_K", "lw_kodama_excluded"],
    "BX": ["bx_causal_horizon", "bx_kappa", "bx_lambda_one_from_energy_match",
           "bx_lambda_one_gives_RH", "bx_xi_cancels", "bx_alpha_beta_half"],
}
for i, (fam, items) in enumerate(FAM.items(), start=5):
    miss = [x for x in items if x not in names_cur]
    chk("LF-{}".format(i), not miss,
        "{} 族 {} 条齐备（缺：{}）".format(fam, len(items), miss if miss else "无"))

hdr("LF-10…13  分级标注与口径（不得混报）")
chk("LF-10", "**E. 【重设计·含证明】**" in cur and "**F. 【形式化·含证明】**" in cur,
    "文件头含 E（重设计）/ F（形式化）两档新标注")
chk("LF-11", "**E/F 两档（30 条）是【重设计/形式化】，不是「已恢复的原定理」**" in cur,
    "统计块写明「E/F ≠ 已恢复的原定理」")
chk("LF-12", "**8909 jobs」≠「54 个定理通过**" in cur or "8909 jobs」≠「54" in cur,
    "统计块保留 C-57 口径（jobs ≠ 定理数）")
chk("LF-13", "C-60" in cur and "BX-1…BX-5 ＋ BX-F 共 6 条" in cur,
    "统计块登记 C-60（「待重写 23 / 24」「BX 5 / 6」两处计数歧义）")

hdr("LF-14…16  备份、mirror 与规则检查")
chk("LF-14", os.path.exists(PRE), "补丁前底本存在（{}）".format(os.path.basename(PRE)))
man = os.path.join(LEAN, "lake-manifest.json")
chk("LF-15", os.path.exists(man), "manifest 仍在（环境未动）")
# ⚠️ 需**按状态机**跳过注释块（`/-- … -/` 与 `/- … -/`）—— 第一版只按行首判断，
#    把 doc 注释的**续行**当成代码行，误报 5 处（第 100 轮实测）。
code_bad, in_doc = [], False
for i, ln in enumerate(cur.split("\n"), 1):
    st = ln.strip()
    if in_doc:
        if "-/" in st:
            in_doc = False
        continue
    if st.startswith("/-"):
        if "-/" not in st:
            in_doc = True
        continue
    if st.startswith("--"):
        continue
    if "λ" in ln or "hλ" in ln:
        code_bad.append((i, st[:60]))
chk("LF-16", not code_bad,
    "代码行内无非法标识符 λ/hλ（实测 {}）—— 该坑第 3 次出现（97/98/100 轮）".format(code_bad or "0 处"))

print("\n" + "=" * 94)
print("LF 汇总：通过 {} 项，失败 {} 项".format(PASS, FAIL))
print("=" * 94)
