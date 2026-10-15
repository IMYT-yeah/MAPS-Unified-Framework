# -*- coding: utf-8 -*-
"""第 96 轮：A1 Lean 资产恢复 —— 恢复产物核验。
LA-1 … LA-9。纯标准库。
"""
import io, os, re, zipfile

ok = 0; bad = 0
def chk(tag, cond, msg, strict=True):
    global ok, bad
    if cond: ok += 1; print("  [OK] {:<6} {}".format(tag, msg))
    elif strict: bad += 1; print("  [XX] {:<6} {}".format(tag, msg))
    else: print("  [--] {:<6} {}".format(tag, msg))

REPO = os.path.join("..", "MAPS-Unified-Framework")
LEAN = os.path.join(REPO, "verification", "lean")
R = lambda p: io.open(p, encoding="utf-8").read()

print("=" * 100)
print("LA-1  恢复文件齐全（5 件）")
FILES = {
    "StormPoC.lean": os.path.join(LEAN, "StormPoC.lean"),
    "lakefile.lean": os.path.join(LEAN, "lakefile.lean"),
    "lean-toolchain": os.path.join(LEAN, "lean-toolchain"),
    "README.md": os.path.join(LEAN, "README.md"),
    ".github/workflows/lean-poc.yml": os.path.join(REPO, ".github", "workflows", "lean-poc.yml"),
}
for name, p in FILES.items():
    ex = os.path.exists(p)
    n = os.path.getsize(p) if ex else 0
    # ⚠️ 第一版统一用 >100 字节 ⟹ lean-toolchain（单行 29 字节）假 FAIL。判据按文件类型分。
    minn = 10 if name == "lean-toolchain" else 100
    chk("LA-1", ex and n > minn, "{} 存在（{} 字节）".format(name.ljust(32), n))

print()
print("LA-2  StormPoC.lean 结构自检（无编译器下的轻量语法卫兵）")
S = R(FILES["StormPoC.lean"])
chk("LA-2a", S.startswith("/-") and "import Mathlib" in S, "文件头注释 + import Mathlib ✓")
ns_open = S.count("namespace StormPoC"); ns_close = S.count("end StormPoC")
sec_open = len(re.findall(r"noncomputable section", S)); sec_close = len(re.findall(r"^end$", S, re.M))
chk("LA-2b", ns_open == 1 and ns_close == 1, "namespace/end StormPoC 配对（{} / {}）".format(ns_open, ns_close))
chk("LA-2c", sec_open == 1 and sec_close == 1, "noncomputable section/end 配对（{} / {}）".format(sec_open, sec_close))
for a, b, nm in [("(", ")", "圆括号"), ("[", "]", "方括号"), ("{", "}", "花括号")]:
    chk("LA-2d-" + nm, S.count(a) == S.count(b), "{}平衡：{} vs {}".format(nm, S.count(a), S.count(b)))

print()
print("LA-3  定理计数与 sorry 计数")
n_thm = len(re.findall(r"^theorem ", S, re.M))
n_sorry = len(re.findall(r"\bsorry\b", S))
chk("LA-3a", n_thm == 23, "theorem 声明 = {}（重建版预期 23）".format(n_thm))
n_sorry2 = sum(1 for ln in S.split("\n") if ln.strip() == "sorry")
chk("LA-3b", n_sorry2 == 2, "sorry（行级独立）= {}；宽计数 {}（第一版含注释命中，判据过宽）".format(n_sorry2, n_sorry))

print()
print("LA-4  八族标记齐全")
for fam in ["GA/T", "A3 族", "A4 族", "BH 族", "AR 族", "LC 族", "LW 族", "BX 族"]:
    chk("LA-4", fam in S, "族标记「{}」在场".format(fam))

print()
print("LA-5  与历史日志的定理名对账（09-10 的 a3_/a4_ 名单）")
A3 = ["stationary_proper_time", "rate_from_clock", "time_frequency_metric", "clock_rate_ratio"]
A4 = ["a4_metric_reciprocal", "a4_exterior_roles", "a4_interior_roles",
      "a4_crossing_negative", "a4_crossing_positive",
      "a4_schwarzschild_exterior", "a4_schwarzschild_interior",
      "a4_a3_time_nonpositive", "a4_t_label_not_a3_time"]
miss_a3 = [n for n in A3 if n not in S]
miss_a4 = [n for n in A4 if n not in S]
chk("LA-5a", not miss_a3, "A3 四名全在（缺 {}）".format(miss_a3 or "无"))
chk("LA-5b", not miss_a4, "A4 九名全在（缺 {}）".format(miss_a4 or "无"))
for anchor in ["GA1", "GA2", "T1", "T2", "bh_horizon_iff_critical", "ar_net_charge_zero",
               "ar_net_energy_not_zero", "ar_k_from_lambda", "lc_beta_of_lambda_one", "lw_omega_k_formula"]:
    chk("LA-5c", anchor in S, "锚点 {} 在场".format(anchor))

print()
print("LA-6  README 恢复状态表与统计一致")
RM = R(FILES["README.md"])
chk("LA-6a", ("重建" in RM and "恢复状态表" in RM and "源文件已丢失" not in RM),
    "README 已更新（含「重建」与恢复状态表；旧「已丢失」表述已移除）")
chk("LA-6b", "含证明 21 条" in RM and "sorry 2 条" in RM and "待重写 23 条" in RM and "设计登记 5 条" in RM,
    "统计行（21 / 2 / 23 / 5）在场")
fam_rows = len(re.findall(r"^\| (GA/T|A3|A4|BH|AR|LC|LW|BX) \|", RM, re.M))
chk("LA-6c", fam_rows == 16, "两张族表各 8 行（实测合计 {}）".format(fam_rows))
chk("LA-6d", "ghfast" in RM and "MB/s" in RM and "850.7MB" in RM, "下载通道实测记录（ghfast / 850.7MB / MB/s 速度）")

print()
print("LA-7  RECOVERY.md 更新 + 四份报告补充登记")
RC = R(os.path.join(REPO, "RECOVERY.md"))
chk("LA-7a", RC.count("已重建") >= 2, "Lean 两条资产已标「已重建」（{} 处）".format(RC.count("已重建")))
for rep in ["黑洞宇宙条件_从巧合到必然", "路线A_50比50到平坦性_解剖报告", "攻λ_全息热力学与临界密度", "做功项修正_λ的命运"]:
    chk("LA-7b", rep in RC, "补充登记：{}".format(rep))

print()
print("LA-8  工具链安装验证（升级：已装 + 可运行 + smoke 编译）")
tool = os.path.join(os.path.expanduser("~"), ".elan", "toolchains", "leanprover--lean4---v4.34.0-rc2")
lean_exe = os.path.join(tool, "bin", "lean.exe")
lake_exe = os.path.join(tool, "bin", "lake.exe")
chk("LA-8a", os.path.exists(lean_exe) and os.path.exists(lake_exe),
    "lean.exe / lake.exe 存在（工具链目录已就位）")
import subprocess, tempfile
r1 = subprocess.run([lean_exe, "--version"], capture_output=True, text=True)
chk("LA-8b", "4.34.0-rc2" in (r1.stdout + r1.stderr), "lean --version → " + (r1.stdout.strip() or r1.stderr.strip())[:78])
r2 = subprocess.run([lake_exe, "--version"], capture_output=True, text=True)
chk("LA-8c", "5.0.0" in (r2.stdout + r2.stderr), "lake --version → " + (r2.stdout.strip() or r2.stderr.strip())[:78])
sm = os.path.join(tempfile.gettempdir(), "smoke_a1_96.lean")
io.open(sm, "w", encoding="utf-8").write(
    "theorem smoke_rfl : 1 + 1 = (2 : Nat) := rfl\n"
    "theorem smoke_omega (x : Nat) (h : x < 3) : Not (x = 5) := by omega\n")
r3 = subprocess.run([lean_exe, sm], capture_output=True, text=True)
chk("LA-8d", r3.returncode == 0,
    "smoke 编译通过（rfl / omega —— core 链健康）" if r3.returncode == 0 else "smoke 失败：" + (r3.stderr or r3.stdout)[:90])

print()
print("LA-9  CI workflow 自检")
W = R(FILES[".github/workflows/lean-poc.yml"])
chk("LA-9a", "verification/lean" in W and "lake build StormPoC" in W, "路径过滤器 + build 目标 ✓")
chk("LA-9b", "elan-init.sh" in W and "cache get" in W, "elan 安装 + mathlib cache 步骤 ✓")

print()
print("=" * 100)
print("通过 {} 项，失败 {} 项".format(ok, bad))
