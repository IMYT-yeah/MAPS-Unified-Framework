# -*- coding: utf-8 -*-
"""
第 98 轮（A2 · python/maps 包恢复）核验脚本
核验项：A2-1 … A2-20（每项 [OK]/[XX]；末尾打印通过/失败计数）

五段：
  ① 五路取证（对象池 / git 史 / remote / 全盘 / 早期环境）—— 必须**全负**
  ② 重建文件与分级标注
  ③ 两个脚本实跑（抓「通过 N 项，失败 M 项」）
  ④ 五个锚点的数值判据（与项目既有记录逐条对）
  ⑤ C-58（F3 纳特/比特）与 README 状态的两段式取证
"""
import io
import os
import re
import glob
import zlib
import json
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))            # outputs/
ROOT = os.path.dirname(BASE)
REPO = os.path.join(ROOT, "MAPS-Unified-Framework")
PKG = os.path.join(REPO, "python", "maps")
GITDIR = os.path.join(REPO, ".git", "objects")
PY = r"[TOOLCHAIN]\binaries\python\envs\default\Scripts\python.exe"
OLD = "源文件 2026-09-16 丢失"          # 补丁前 python/README.md 的状态短语

PASS = FAIL = 0


def chk(tag, cond, msg, strict=True):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("  [OK] {:<7} {}".format(tag, msg))
    else:
        if strict:
            FAIL += 1
            print("  [XX] {:<7} {}".format(tag, msg))
        else:
            print("  [INFO] {:<7} {}".format(tag, msg))


def hdr(s):
    print("\n" + "=" * 92)
    print(s)
    print("=" * 92)


def rd(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


def run(args, cwd):
    r = subprocess.run([PY] + args, cwd=cwd, capture_output=True)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    return r.returncode, out


print("第 98 轮核验（A2 · python/maps 包恢复）")

# ======================================================= ① 五路取证
hdr("A2-1…5  五路取证（全部为负才允许说「只能重建」）")

# 路 1：.git 对象池 —— 找 maps 包源码的特征串
JUDGE = ["重聚焦在联合系统", "净荷", "泄漏方向性"]        # 原规格要求写进 formula.py 头注释
objs = glob.glob(os.path.join(GITDIR, "??", "*"))
pool_py, pool_judge, pool_meta = 0, 0, 0
for p in objs:
    try:
        txt = zlib.decompress(open(p, "rb").read()).decode("utf-8")
    except Exception:
        continue
    if not (re.search(r"(?m)^\s*(import|from)\s+\w", txt) and
            re.search(r"(?m)^\s*(def|class)\s+\w", txt)):
        continue
    pool_py += 1
    # ⚠️ 判据要紧：**「提到包」≠「是包」**（铁律 18：引文清点会命中元文本）。
    #    `_repo_assemble.py` 里含 `lam_c = 1.3e26` —— 那是它 **patch_maps() 的替换文本**，
    #    不是包源码。元文本对象（组装器）单独计数，不算命中。
    is_meta = ("patch_maps" in txt) or ("MAPS_SRC" in txt) or ("本地仓库组装器" in txt)
    if is_meta:
        pool_meta += 1
        continue
    if re.search(r"(?m)^def\s+(t1|t2|t3|t4|t5|T1|T2|T3|T4|T5)\b", txt):
        pool_judge += 1
print("  对象池文件数 = {}；其中 Python 类对象 = {}（元文本/组装器 {} 个已排除）".format(
    len(objs), pool_py, pool_meta))
chk("A2-1", pool_judge == 0,
    "第 1 路（对象池）：无任何对象**定义** T1–T5（maps 源码对象 = {}；含 `lam_c=1.3e26` 的只有组装器）".format(pool_judge))

# 路 2：git 历史
GITEXE = r"[TOOLCHAIN]\binaries\PortableGit\versions\1.2.0\cmd\git.exe"
r = subprocess.run([GITEXE, "log", "--all", "--oneline"], cwd=REPO, capture_output=True)
nlog = len([x for x in (r.stdout or b"").decode("utf-8", "replace").split("\n") if x.strip()])
chk("A2-2", nlog == 0, "第 2 路（git 史）：commit 数 = {}（仓库从未提交）".format(nlog))

# 路 3：remote
r = subprocess.run([GITEXE, "remote", "-v"], cwd=REPO, capture_output=True)
rem = (r.stdout or b"").decode("utf-8", "replace").strip()
chk("A2-3", rem == "", "第 3 路（remote）：无远端可拉（{}）".format(repr(rem)))

# 路 4：全盘（限定用户目录）文件名扫描
NAMES = {"formula.py", "maps_framework.py", "run.sh", "maps.py"}
SKIP = {".git", "node_modules", "__pycache__", ".venv", ".lake", "site-packages",
        "_workbuddy", "binaries", "_MAPS_explore"}
found = []
for rr in [r"[HOME]/Desktop", r"[HOME]/Documents",
           r"[HOME]/Downloads"]:
    if not os.path.isdir(rr):
        continue
    for dp, dns, fns in os.walk(rr):
        dns[:] = [d for d in dns if d not in SKIP]
        for fn in fns:
            if fn in NAMES:
                found.append(os.path.join(dp, fn))
# 唯一的命中应当是本轮自己重建的文件
rebuilt = [f for f in found if os.path.normcase(os.path.dirname(f)) == os.path.normcase(PKG)]
chk("A2-4", len(found) == len(rebuilt) and len(rebuilt) >= 3,
    "第 4 路（全盘）：命中 {} 处，全部是本轮重建的包（{} 个文件）".format(len(found), len(rebuilt)))

# 路 5：早期环境路径
chk("A2-5", not os.path.isdir("[OLD_DRIVE]/") and not os.path.isdir("[OLD_WORKSPACE]/_MAPS_explore"),
    "第 5 路（早期环境盘）：早期环境不存在（源目录 _MAPS_explore 不可达）")

# ======================================================= ② 文件与分级
hdr("A2-6…10  重建文件与分级标注")
FILES = ["formula.py", "maps_framework.py", "verify.py", "run.sh"]
for i, f in enumerate(FILES, start=6):
    p = os.path.join(PKG, f)
    chk("A2-{}".format(i), os.path.exists(p),
        "存在 {}（{} B）".format(f, os.path.getsize(p) if os.path.exists(p) else 0))

src_mf = rd(os.path.join(PKG, "maps_framework.py"))
src_v = rd(os.path.join(PKG, "verify.py"))
src_fm = rd(os.path.join(PKG, "formula.py"))
chk("A2-10", all(k in src_mf for k in ["lam_c = 1.3e26", "np.exp(-L_vals / lam_c)",
                                       "非概率（凝结强度/普朗克率）"]),
    "mapped A 级逐字片段已在 maps_framework.py 中（lam_c / 完整 F5 / 打印说明）")
chk("A2-11", "beta_ppn = -series.expand().coeff(x, 2) / 2" in src_v,
    "verify.py 的 PPN 行含**负号**（A 级逐字）")
chk("A2-12", "重聚焦在联合系统" in src_fm and "净荷" in src_fm,
    "formula.py 头注释含**并轨说明**（原规格明文要求）")

# ======================================================= ③ 实跑
hdr("A2-13…14  两个脚本实跑")
rc1, out1 = run(["maps_framework.py"], PKG)
m1 = re.search(r"汇总：通过 (\d+) 项，失败 (\d+) 项", out1)
chk("A2-13", rc1 == 0 and m1 and int(m1.group(2)) == 0,
    "maps_framework.py 退出码 {}，汇总 = {}".format(rc1, m1.group(0) if m1 else "未解析到"))
rc2, out2 = run(["verify.py"], PKG)
m2 = re.search(r"汇总：通过 (\d+) 项，失败 (\d+) 项", out2)
chk("A2-14", rc2 == 0 and m2 and int(m2.group(2)) == 0,
    "verify.py 退出码 {}，汇总 = {}".format(rc2, m2.group(0) if m2 else "未解析到"))

# ======================================================= ④ 锚点数值
hdr("A2-15…19  五个锚点的数值判据（与项目既有记录对）")
chk("A2-15", "beta_ppn = 1  (=1 通过)" in out1 and "gamma_ppn = 1" in out1,
    "T1：β = 1、γ = 1（PPN 与 GR 不可区分）")
dev = re.search(r"最大相对偏差 = ([\d.]+)%", out1)
sk = re.search(r"速率分布偏度 = ([+-][\d.]+)（Maxwell 解析值 ([+-][\d.]+)）", out1)
chk("A2-16", bool(dev) and float(dev.group(1)) < 15 and bool(sk) and abs(float(sk.group(1)) - float(sk.group(2))) < 0.12,
    "T2：Maxwell 偏差 {}% < 15%；偏度 {} vs 解析 {}（|Δ| < 0.12）".format(
        dev.group(1) if dev else "?", sk.group(1) if sk else "?", sk.group(2) if sk else "?"))
s3 = re.search(r"S = ([\d.eE+]+) 纳特", out1)
th = re.search(r"Hawking 温度 T = ([\d.eE+-]+) K", out1)
chk("A2-17", bool(s3) and abs(float(s3.group(1)) / 1.05e77 - 1) < 0.02 and
    bool(th) and abs(float(th.group(1)) - 6.16868e-8) / 6.16868e-8 < 1e-3,
    "T3：S = {} 纳特（记录 1.05e77）；T = {} K（标准值 6.16868e-8）".format(
        s3.group(1) if s3 else "?", th.group(1) if th else "?"))
chk("A2-18", "95.5290%" in out1.replace(" ", ""),
    "T4：v/c = 0.999 ⟹ Δm/m = 95.53%（记录 95.5%）")
chk("A2-19", "P(1e-35 m) = 1.6163" in out1 and "P(l_P) = 1" in out1,
    "T5：α = 1 反推成立（P(1e-35 m) = 1.6163 vs 记录 1.616）")

# ======================================================= ⑤ C-58 与两段式
hdr("A2-20   C-58（F3 纳特/比特）与 README 状态的两段式取证")
rm = rd(os.path.join(PKG, "README.md"))
chk("A2-20", ("·ln2" in rm and "1.05×10⁷⁷" in rm) and ("C-58" in rm) and ("纳特" in rm),
    "README 同时保留原规格（§0 留痕）、标出 C-58 并给出裁决（纳特）")
rp = rd(os.path.join(REPO, "python", "README.md"))
chk("A2-21", OLD not in rp and "已重建" in rp, "python/README.md：旧的「丢失」状态已替换为「已重建」")

print("\n" + "=" * 92)
print("A2 汇总：通过 {} 项，失败 {} 项".format(PASS, FAIL))
print("=" * 92)
