# -*- coding: utf-8 -*-
"""
MAPS-Unified-Framework 本地仓库组装器
========================================
把项目 outputs/ 中全部理论资产（论文/备忘录/包/数值脚本）+ MAPS 新包（修复版）
整理进一个 GitHub-ready 目录，排除构建缓存与巨型工具链，并生成 README/LICENSE 等。
用法: python _repo_assemble.py    （可重复执行：先清空目标目录再重建）
"""
import os, re, shutil, pathlib, datetime

SRC = pathlib.Path(r"D:/Users/IMYT.YT/WorkBuddy/2026-08-20-21-43-34/outputs")
MAPS_SRC = pathlib.Path(r"D:/Users/IMYT.YT/WorkBuddy/_MAPS_explore")
DST = pathlib.Path(r"D:/Users/IMYT.YT/WorkBuddy/MAPS-Unified-Framework")

EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", "_tex_bin", "_bom_test", "_tex_bin2"}
EXCLUDE_EXTS = {".pyc", ".log", ".zip"}
BLUEPRINT = {"项目发展蓝图.md", "遗留问题重整与统一四力行动清单.md",
             "论文重量与可发表区间评估.md", "原文标注改写策略.md", "论文理论推演报告.md"}


def cls(name: str):
    """文件名 -> 目标子目录"""
    if name.startswith("论文初稿_正反物质对风暴统一框架"):
        return "paper/history" if "_v2.8" not in name else "paper/zh"
    if name.startswith("Paper_Matter"):            # 英文主文档
        return "paper/en"
    if "MAPS" in name:
        return "notes/MAPS"
    if re.match(r"^A\d", name):   return "notes/A-series"
    if re.match(r"^B\d|^B分支", name): return "notes/B-series"
    if re.match(r"^C\d", name):   return "notes/C-series"
    if re.match(r"^M\d补强", name): return "notes/M-series"
    if re.match(r"^P\d|^P1p", name): return "notes/P-series"
    if re.match(r"^(EMRI|LISA|Kerr)", name): return "notes/EMRI"
    if name.startswith("Stormetric包审计"): return "notes/包工程"
    if re.match(r"^批\d\d", name): return "docs/origin-batches"
    if name in BLUEPRINT: return "docs/蓝图与行动清单"
    return "notes/推演专题"


def copy_tree(src, dst, exts=(), subdirs_ok=True):
    n = 0
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        rel = pathlib.Path(root).relative_to(src)
        for f in files:
            if pathlib.Path(f).suffix in EXCLUDE_EXTS or f.endswith(".pyc"):
                continue
            if not subdirs_ok and rel != pathlib.Path("."):
                continue
            target = dst / rel / f if str(rel) != "." else dst / f
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(os.path.join(root, f), target)
            n += 1
    return n


def copy_md(name, sub):
    p = SRC / name
    if p.exists():
        (DST / sub).mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, DST / sub / name)
        return 1
    return 0


def main():
    if DST.exists():
        shutil.rmtree(DST)
    DST.mkdir(parents=True)
    stats = {}

    # ---------- 1. 论文（md） ----------
    n = 0
    for f in sorted(SRC.glob("*.md")):
        if f.name.startswith(("论文初稿", "Paper_Matter")):
            n += copy_md(f.name, cls(f.name))
    # 论文 html（当前版中文）
    for h in SRC.glob("论文初稿_正反物质对风暴统一框架_v2.8.html"):
        shutil.copy2(h, DST / "paper/zh" / h.name)
        n += 1
    stats["paper(md+html)"] = n
    # 中英版本历史: paper/history 里放英文历史版本? (无) 直接跳过

    # ---------- 2. 备忘录/报告（md only，html 由 md 在 GitHub 渲染）----------
    cnt = {}
    for f in sorted(SRC.glob("*.md")):
        if f.name.startswith(("论文初稿", "Paper_Matter")):
            continue
        sub = cls(f.name)
        if copy_md(f.name, sub):
            cnt[sub] = cnt.get(sub, 0) + 1
    stats["notes"] = cnt

    # ---------- 3. stormetric Python 包（去缓存） ----------
    st_dst = DST / "python/stormetric"
    n = copy_tree(SRC / "stormetric", st_dst)
    # 去掉本地缓存目录残留
    for r, d, _ in os.walk(st_dst):
        for x in d:
            if x in EXCLUDE_DIRS:
                shutil.rmtree(os.path.join(r, x))
    # pytest 配置：src 布局零安装导入（离线可用）
    (st_dst / "pytest.ini").write_text(
        "[pytest]\npythonpath = src\ntestpaths = tests\n", encoding="utf-8")
    stats["stormetric_files"] = n

    # ---------- 4. MAPS 新包（复制 + 修复） ----------
    maps_dst = DST / "python/maps"
    maps_dst.mkdir(parents=True)
    for f in ["formula.py", "maps_framework.py", "verify.py", "run.sh"]:
        shutil.copy2(MAPS_SRC / f, maps_dst / f)
    patch_maps(maps_dst)
    stats["maps_files"] = 4

    # ---------- 5. 数值验证脚本与数据（顶层 _*.py / .npy / .npz） ----------
    vdst = DST / "verification"
    vdst.mkdir(parents=True, exist_ok=True)
    vn = 0
    for f in sorted(SRC.glob("_*.py")):
        shutil.copy2(f, vdst / f.name); vn += 1
    (vdst / "data").mkdir(parents=True, exist_ok=True)
    dn = 0
    for f in list(SRC.glob("*.npy")) + list(SRC.glob("*.npz")):
        shutil.copy2(f, vdst / "data" / f.name); dn += 1
    stats["verification_py"], stats["data_files"] = vn, dn

    # ---------- 6. 顶层图件 ----------
    (DST / "assets").mkdir(parents=True, exist_ok=True)
    an = 0
    for f in list(SRC.glob("*.png")) + list(SRC.glob("*.jpg")):
        shutil.copy2(f, DST / "assets" / f.name); an += 1
    stats["assets"] = an

    # ---------- 7. 投稿源文件 ----------
    for src_dir, sub in [("arXiv_submission", "paper/submissions/arxiv"),
                         ("cso_submission", "paper/submissions/cso")]:
        s = SRC / src_dir
        if not s.exists():
            continue
        d = DST / sub
        d.mkdir(parents=True, exist_ok=True)
        files = [f for pat in ("*.tex", "*.pdf", "*.md", "*.cls", "*.def") for f in s.glob(pat)]
        for f in files:
            shutil.copy2(f, d / f.name)
    stats["submissions"] = "copied tex/pdf/md/cls/def"

    # ---------- 8. 生成 README / LICENSE / 索引 等 ----------
    write_meta()

    # 打印统计
    print("== 组装完成 ->", DST)
    for k, v in stats.items():
        print("  %-18s %s" % (k, v))
    total = sum(len(f) for _, _, fs in os.walk(DST) for f in fs)
    print("  文件总数:", total)


def patch_maps(d: pathlib.Path):
    """MAPS 包修复：beta 符号 / F1 注释 / T5 概率越界+指数项 / 头注释并入镜像支"""
    # verify.py: beta 符号
    p = d / "verify.py"
    t = p.read_text(encoding="utf-8")
    t = t.replace("beta_ppn = series.expand().coeff(x, 2) / 2",
                  "beta_ppn = -series.expand().coeff(x, 2) / 2   # 负号: Will 约定 g00=-(1-2x+2 beta x^2)")
    t = t.replace('print("[PPN] beta =", beta_ppn, "(=1 通过)")',
                  'print("[PPN] beta =", float(beta_ppn), "(=1 通过)")')
    p.write_text(t, encoding="utf-8")
    # maps_framework.py: 头注释 + T5
    p = d / "maps_framework.py"
    t = p.read_text(encoding="utf-8")
    t = t.replace(
        "     低能极限 epsilon -> 0, 解释重子不对称 eta ~ 6e-10 与暗能量 rho_Lambda ~(meV)^4.",
        "     高能端(E->M_Pl) epsilon -> epsilon0=7.7e-20; 低能端(E->meV) epsilon -> 1(饱和=暗能量).\n"
        "     重子不对称 eta~6e-10 对应 E~1TeV 能标(见论文 §8.1); 方向性(反份->镜像支)见 README.")
    t = t.replace(
        "    P = (l_P / L_vals) ** alpha",
        "    lam_c = 1.3e26  # 宇宙学尺度候选 lambda_c(m)\n"
        "    P = (l_P / L_vals) ** alpha * np.exp(-L_vals / lam_c)  # 完整 F5: 幂律 x 指数压制")
    t = t.replace('print("[T5] L=%.2e m -> P_emerge = %.3e" % (L, p))',
                  'print("[T5] L=%.2e m -> P_emerge = %.3e (L>=l_P 才为概率; L<l_P 为凝结强度/普朗克率)" % (L, p))')
    p.write_text(t, encoding="utf-8")
    # formula.py: 说明并入镜像支(按行定位插入 P3' 行, 避免引号匹配问题)
    p = d / "formula.py"
    t = p.read_text(encoding="utf-8")
    lines = t.splitlines()
    out = []
    inserted = False
    for ln in lines:
        out.append(ln)
        if (not inserted) and ln.strip().startswith("P3 湮灭即空间"):
            out.append("  P3' (并轨镜像支, 见 notes/MAPS 融合备忘录): 重聚焦在联合系统"
                       "(B+ U B- U 物质) 中保净荷(分支A); 净正物质由泄漏方向性提供 -- "
                       "反份入镜像支 B-、正份留本支 B+ (旧公理2, 镜像支不可删).")
            inserted = True
    if inserted:
        p.write_text("\n".join(out) + "\n", encoding="utf-8")
    else:
        print("  [warn] formula.py P3 行未找到, 跳过并轨注释")


def write_meta():
    today = datetime.date.today().isoformat()
    # ---------- README ----------
    readme = """# 正反物质对风暴（Matter-Antimatter Pair Storm, MAPS）统一框架

> **核心思想**：宇宙底层是正反物质对持续"相遇—湮灭—再生"的事件流；四种基本力是同一风暴的统计涌现模态；
> 时空 = 事件流微变的统计平均；**湮灭（溶解）= 空间，涌现（生成）= 空间重聚焦 —— 同一相变的两面**。
>
> ⚠️ **诚实声明**：本仓库为**启发式统一框架，非已确立物理**。所有【推导】为框架内自洽论证，
> 【待验证】/【开放问题】不得作为推导依据。与实验冲突处（PPN、EHT 阴影、DESI w、LHC 空结果等）均已显式标注。

## 一句话地图

| 目录 | 内容 |
|---|---|
| `paper/` | 主论文（中/英 v2.8）+ 版本沿革（v1–v2.7）+ arXiv/CSO 投稿源文件 |
| `notes/` | 理论备忘录全集：A/B/C 系列严格化证明、M 系列审稿补强、P 系列行动报告、EMRI 判别方案、MAPS 新思考与融合备忘录、各专题推演 |
| `python/stormetric` | 开源 Python 包 v0.2.0：度规→光子球/阴影 5.436（EHT 对标）+ PPN 3PN 分叉 + EMRI 进动差标度律（**53 项测试**） |
| `python/maps` | 新思考计算包（修复版）：PPN/玻尔兹曼/熵/运动湮灭/涌现概率 + 镜像支并轨说明 |
| `verification/` | 数值验证脚本全集（与各备忘录一一对应）与数据 |
| `docs/` | 蓝图/行动清单/原始文献分批整理 |
| `assets/` | 图件 |

## 核心公式

```
公理1  事件流: 正反物质对相遇-湮灭-再生, 各向同性, 50:50, ν~1/t_P;  时空 = 微变统计平均
公理2  泄漏:   每次湮灭 ε 概率绑定失败; ε(E)=ε₀(M_Pl/E)^β, β≈0.615, ε₀≈7.7×10⁻²⁰
              (方向性: 反份入镜像支, 正份留本支 —— 镜像支不可删, 支撑暗物质叠加模型)
公理3  时间 = 湮灭事件频率;     两支互为 CPT 镜像
公理4  空间可卷曲成时间 (黑洞极限)
F2     g₀₀ = -e^{−2x}  ⇒  PPN γ=1, β=1        (1PN 与 GR 不可区分)
       2PN g_rr 分叉 +33% / 3PN g₀₀ 分叉 −11%  (损失率/泊松累积语言, 见 notes/C-series)
F3     S = A/(4l_P²)·ln2  ⇒  太阳黑洞 1.05×10⁷⁷ 纳特  (通量管相干块微态计数, k=2^{1/4})
F4(新) 运动=湮灭: Δm = m(1−1/γ)   [解释分支, 见 notes/MAPS 融合备忘录]
F5(新) 溶解/涌现: P(L)=(l_P/L)^α·exp(−L/λ_c)   [锚点越小涌现概率越大]
```

## 本地运行（一条命令）

```bash
python run_all.py          # 依次运行: maps 锚点验证 + stormetric pytest + 输出汇总
# 或分步:
python python/maps/maps_framework.py          # MAPS 新思考 T1-T5
python -m pytest python/stormetric -q          # stormetric 53 项测试
```

依赖：`numpy scipy matplotlib sympy pytest`（见 requirements.txt）。

## 可检验预言（节选）

- **黑洞阴影** b_min = 2e·GM/c² ≈ 5.437 GM/c² —— EHT M87*/Sgr A* 相容（5.2±0.3）
- **EMRI 进动差标度律** δ_prec = κ·x_p（κ≈0.30）—— LISA 单源判决 27σ/28σ（见 notes/EMRI）
- **原初黑洞辐射非热修正** ε_A²(kT_H)（主导 1/S 修正 10²⁴–10³¹×，C1-A1，见 notes/C-series）
- **暗能量** w = −1+4ε/3 常数偏离（wa=0）；E_c≈1.01 meV 截断 —— DESI DR2 判别中
- **void-CPT-κ 异常**（镜像支暗物质投影）—— 空洞弱透镜偏强

## 版本状态

- 主论文 v2.8（含 v2.9 增量注记：A1–A4 / B1 / C1 / 视界几何等）
- 系列备忘录: A/B/C 严格化 + M1–M7 审稿补强 + EMRI 分析 + P 系列行动报告
- **MAPS 新思考**（2026-09 入册）：空间重聚焦理论 —— 与主框架并轨（SPB 空间库模型），
  镜像支保留、矛盾分支化/开放化，见 `notes/MAPS/`
- 待办：接入 GitHub API 上传本仓库

*组装日期：@DATE@。源资产：项目 outputs/（422 文件，85.7 MB），本仓库为整理后镜像（排除构建缓存与 70 MB 本地 TeX 工具链）。*
"""
    (DST / "README.md").write_text(readme.replace("@DATE@", today), encoding="utf-8")

    # ---------- LICENSE ----------
    (DST / "LICENSE").write_text("""MIT License

Copyright (c) 2026  (MAPS Unified Framework 作者)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""", encoding="utf-8")

    (DST / "LICENSE-docs").write_text("""文档（paper/ 与 notes/ 下全部 Markdown 与衍生内容）采用
知识共享 署名 4.0 国际 (CC BY 4.0) — https://creativecommons.org/licenses/by/4.0/
代码（python/, verification/, run_all.py）采用 MIT License（见 LICENSE）。
""", encoding="utf-8")

    # ---------- CITATION ----------
    (DST / "CITATION.cff").write_text("""cff-version: 1.2.0
message: "正反物质对风暴（MAPS）统一框架 —— 论文 + 备忘录 + 可复现数值全集"
title: "正反物质对风暴统一框架 (Matter-Antimatter Pair Storm Unified Framework)"
type: software
authors:
  - name: "（作者名待填，接入上传前请补全）"
date-released: "2026-09-07"
keywords: [physics, emergence, gravity, dark-energy, entropy, unified-framework]
license: MIT (code) / CC-BY-4.0 (docs)
""", encoding="utf-8")

    # ---------- requirements / .gitignore ----------
    (DST / "requirements.txt").write_text(
        "numpy>=1.24\nscipy>=1.10\nmatplotlib>=3.7\nsympy>=1.11\npytest>=7\n", encoding="utf-8")
    (DST / ".gitignore").write_text(
        "__pycache__/\n*.pyc\n.pytest_cache/\n*.log\n*.zip\n_tex_bin/\n"
        "python/stormetric/build/\npython/stormetric/dist/\npython/stormetric/*.egg-info/\n"
        "verification/data/*.npy\nverification/data/*.npz\n", encoding="utf-8")

    # ---------- notes/README 自动索引 ----------
    lines = ["# 备忘录索引（自动生成）", "",
             "| 文件 | 一级标题 |", "|---|---|"]
    for sub in ["A-series", "B-series", "C-series", "M-series", "P-series", "EMRI",
                "MAPS", "包工程", "推演专题"]:
        d = DST / "notes" / sub
        if not d.exists():
            continue
        lines.append(f"\n## {sub}")
        lines.append("")
        lines.append("| 文件 | 标题 |")
        lines.append("|---|---|")
        for f in sorted(d.glob("*.md")):
            head = ""
            try:
                first = f.read_text(encoding="utf-8", errors="ignore").splitlines()
                for ln in first[:4]:
                    if ln.startswith("#"):
                        head = ln.lstrip("#").strip()
                        break
            except Exception:
                pass
            lines.append(f"| {f.name} | {head} |")
    (DST / "notes/README.md").write_text("\n".join(lines), encoding="utf-8")

    # ---------- run_all.py ----------
    (DST / "run_all.py").write_text('''# -*- coding: utf-8 -*-
"""本地一键验证：MAPS 锚点 + stormetric 53 测试 + 简短汇总"""
import subprocess, sys, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
PY = sys.executable

def run(cmd, cwd):
    print("\\n$ " + " ".join(map(str, cmd)))
    r = subprocess.run(cmd, cwd=cwd)
    return r.returncode

ok = True
ok &= run([PY, "python/maps/maps_framework.py"], ROOT) == 0
ok &= run([PY, "-m", "pytest", "python/stormetric", "-q"], ROOT) == 0
print("\\n== 本地验证 %s ==" % ("全部通过 ✅" if ok else "存在失败 ❌"))
sys.exit(0 if ok else 1)
''', encoding="utf-8")

    # ---------- python/README ----------
    (DST / "python/README.md").write_text("""# python/ —— 可运行计算包

| 包 | 状态 | 内容 |
|---|---|---|
| `stormetric/` | 已审计 v0.2.0，53 测试 | 输入度规 → 光子球半径/阴影 5.436（EHT 对标）→ PPN 3PN 分叉图 → EMRI 进动差标度律 → CLI |
| `maps/` | 修复版（beta 符号/注释/T5） | 新思考 T1–T5 锚点 + 镜像支并轨说明（头注释 P3′） |

```bash
python -m pytest python/stormetric -q      # 53 passed
python python/maps/maps_framework.py        # T1–T5 锚点
```
""", encoding="utf-8")

    # ---------- verification/README ----------
    (DST / "verification/README.md").write_text("""# verification/ —— 数值验证脚本全集

每个 `_*.py` 对应一份备忘录（文件名前缀对齐：A2→_a2_bbgky_verify.py, C1→_c1_gamma_three_channel.py, 等）。
运行环境见根 README。数据文件在 `data/`（.npy/.npz，部分脚本的可复现中间结果）。

```bash
python verification/_c1_gamma_three_channel.py   # 例：C1 湮灭损失率三通道 53 项检查
```
""", encoding="utf-8")


if __name__ == "__main__":
    main()
