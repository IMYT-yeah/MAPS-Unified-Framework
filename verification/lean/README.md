# verification/lean —— 机器核验（Lean 4 / mathlib）

> ✅ **本目录源文件已于 2026-10-02（第 96 轮「A1 资产恢复」）重建**。
> 历史：原文件 2026-09-09～09-12 撰写并核验（`lake build` = **8909 jobs 全绿**），
> 2026-09-16 随旧机丢失，09-16～10-02 期间本目录仅存恢复规格；现按恢复规格 + 日志重建。
> ✅ **第 97 轮（2026-10-03）已复验**：mathlib 钉定 `eda2e61d06…` ＋ Lean 4.34.0-rc2 ⟹
> `lake build StormPoC` = **`Build completed successfully (8909 jobs)`**
> （**0 error**；**2 处 `sorry` 警告** = 第 96 轮登记的「sorry 2」）。
> ⚠️ **首次 build 实测 7 处报错**（不是原 README 预估的「若干 API 名」），已逐条修，**其中 3 处**
> 是 09-09 日志**早有记录、但重建时只写了注释未执行**的 `λ` 保留字改名（详见文末修正清单）。
> 📌 **口径**：这 8909 个 job 里 **8908 个是依赖**（mathlib 全量 ＋ batteries/aesop/…），
> **StormPoC 自身只占 1 个 job** ⟹ 「8909 jobs 全绿」**不等于**「8909 个定理通过」。

## 恢复状态表（**v3 · 2026-10-03（第 100 轮）**）

| 族 | 原数量 | 重建层级 | 状态 |
|---|---|---|---|
| GA/T | 4 | ✅ **完整重建**（含证明） | 依据 09-09 日志（含三处 API 修正记录） |
| A3 | 4 | ✅ **完整重建**（含证明） | 依据 09-10 日志（两条定义性前提） |
| A4 | 9 | ✅ **重建·已编译确认**（含证明） | 第 97 轮 `lake build` 全绿确认 |
| BH | 9 | ✅ **含证明**（1 锚点补证 ＋ 8 **重设计·含证**） | **第 100 轮**；原定理名未入日志，逐条锚定 09-11 结论 |
| AR | 9 | ✅ **含证明**（2 有证 ＋ 1 锚点补证 ＋ 6 **重设计·含证**） | **第 100 轮**；依据 09-11（净荷 ≠ 净能量） |
| LC | 7 | ✅ **含证明**（1 锚点 ＋ 5 **重设计·含证** ＋ 1 工具拆分） | **第 100 轮**；依据 09-11（λ = 2αβ ⟹ β = 1/2π） |
| LW | 6 | ✅ **含证明**（1 锚点 ＋ 5 **重设计·含证**） | **第 100 轮**；依据 09-12（Ω_K = 1 − 4α²β²） |
| BX | 6 | ✅ **已形式化·含证明**（原「设计登记」） | **第 100 轮**；09-16 设计稿 BX-1…5 ＋ BX-F |

**重建统计（v3 · 第 100 轮后）**：
**含证明 55 条声明（54 条内容定理/引理 ＋ 1 条工具）｜ `sorry` = 0 ｜ 待重写 0 ｜ 设计登记 0**
⟹ `lake build StormPoC` = **8909 jobs、0 error、0 warning**。

⚠️ **必须与以下三条口径一起读**：
1. **E/F 两档（30 条）是【重设计/形式化】，不是「已恢复的原定理」** —— 原 BH/AR/LC/LW 的定理名与陈述
   **未入任何记录**；每条都锚定 09-11 / 09-12 日志的**已记录结论**（出处见 `StormPoC.lean` 各条 doc），
   但**逐条同一性不可核验**。
2. **「8909 jobs」≠「54 个定理通过」**（**C-57**）：8908 个 job 是依赖（mathlib 全量），本文件只占 1 个。
3. **计数口径有两处歧义（C-60）**：原写「待重写 **23**」而分族账为 `BH 8 + AR 6 + LC 5 + LW 5 = **24**`；
   原写「BX 族（**5**）」而设计稿列 `BX-1…BX-5 ＋ BX-F = **6** 条`。

## 第 100 轮补完（2026-10-03）—— 「甲-1：Lean 侧补完」

**做了什么**：把第 96 轮重建版里 **2 处 `sorry`** 补证、**23→24 条「待重写」**逐条重设计并给出证明、
**5（→6）条 BX「设计登记」**形式化。

**结果**：`sorry = 0`；**54 条内容定理/引理**（＋1 工具）；`lake build` = **8909 jobs、0 error、0 warning**。

**过程（8 次编译迭代）**：首次报错 **18 处** → 2 处 → 1 处 → **0 处**；
耗时基线：单次 `lake build StormPoC` **98–313 s**（冷缓存约 5–11 min）。

**⚠️ 新分档（E/F）**：
- **E【重设计·含证明】**：BH 8 ＋ AR 6 ＋ LC 5 ＋ LW 5 = **24 条**
- **F【形式化·含证明】**：BX **6 条**（含 `bx_alpha_beta_half` 相容性）

**本轮踩的 Lean 坑（可复用）**：
1. ⚠️⭐ **`λ` 与 `hλ` 都不是合法标识符**（词法把 `λ` 单独切成 token）—— 该坑**第 3 次**出现（97／98／100 轮）。
2. ⚠️⭐ **`field_simp; ring` 在 ≥8 个变量上会指数爆炸**：一条 10 变量的定理实测 **> 13 分钟未收敛**
   ⟹ **必须拆成 2–3 步小引理**（`lc_gauge_identity` 就是为此拆出来的）。
3. ⚠️ **`field_simp` 会顺带约掉两侧的公因子**（本轮把 `ℏ` 约掉了）—— 之后按原式继续推会找不到符号，
   应先打印/核对化简后的假设。
4. ⚠️ **`eq_div_iff` vs `div_eq_iff`**：`a = b/c` 用前者、`a/c = b` 用后者 —— 本轮**两次用错方向**。
5. ⚠️ **`field_simp` 常常已经把目标关掉** ⟹ 后面再 `ring` 会报 `No goals to be solved`。
   **稳妥写法：`field_simp; try ring`**。
6. ⚠️ **`linarith` 不处理含除法的原子**（`x/R = y`）—— 先 `field_simp at h` 清分母再 `linarith`。
7. ⚠️ **检查脚本本身也会误报**：LF-16 第一版只按行首判定注释，把 **doc 注释的续行**当代码 ⟹
   误报 5 处非法标识符。**须用状态机跳过 `/-- … -/` 块**。

## 文件（当前）

| 文件 | 状态 |
|---|---|
| `StormPoC.lean` | ✅ 重建版 v2（分级标注见文件头） |
| `lakefile.lean` | ✅ 重建（含 `package StormPoC` 声明 —— 09-09 当日修复项） |
| `lean-toolchain` | ✅ 重建（`leanprover/lean4:v4.34.0-rc2`） |
| `.github/workflows/lean-poc.yml` | ✅ 重建（仓库根 `.github/`；push 触发 elan + cache + build） |
| `README.md` | 本文件 |

## 工具链（版本必须对齐，否则 olean 缓存失效）

- Lean `leanprover/lean4:v4.34.0-rc2` + Lake 5.0.0-src（mathlib master 于 2026-09 锁此版本）
- **本机下载通道（2026-10-02 实测）**：`ghfast.top` GitHub 镜像 ——
  工具链 zip **850.7MB**（09 月记录「561.6MB」为旧口径）实测 **峰值 2.07 MB/s、全程 6m51s**
  （直连 github.com 仍不可用）。
- git 全局（装环境时）：`url.https://ghfast.top/https://github.com/.insteadof https://github.com/`
- olean 缓存服务器已迁移至 Azure `https://lakecache.blob.core.windows.net/mathlib4`
  （旧 `olean-cache.lean-lang.org` = NXDOMAIN）
- Windows 特有：构建期 "failed to read ...olean.private" = 瞬时文件锁，**重跑即愈**
- 解压工具链：**zstd**（python `zstandard` 包；`bsdtar` 不支持该包格式）

## 重建后的补全路线（供下一次有环境的会话执行）

1. `export PATH="$HOME/.elan/bin:$PATH"`（lean/lake 放入 PATH）；
2. 工程内 `lake update`（clone mathlib；git 走 ghfast 镜像）；
3. `lake exe cache get`（.ltar → leantar 解压；Windows IO 瓶颈，耐心/断点重试）；
4. `lake build StormPoC` —— ✅ **第 97 轮已达成**：实测 **`Build completed successfully (8909 jobs)`**；
5. 首次 build 的预期修正点（按报错逐个处理）：
   - T1/T2 的 exp 级数桥接名字（已在源码注释标记）；
   - A4 族 `field_simp` / 除法引理名（`_₀` 后缀族）；
   - C 层锚点的 sorry 补证明（BH-1、AR-8/9 优先 —— 均为可完成的代数组装）。
6. 全绿后：更新本表为「已复验」+ 在 `notes/` 回填日志。 ✅ **第 97 轮已完成**（见下节）。

## 首次 build 实测修正清单（第 97 轮 · 逐条如实登记）

> 四次构建、三次修正：`7 处报错` ⟶ `4 处` ⟶ `2 处` ⟶ **`Build completed successfully (8909 jobs)`**。
> 分类：首次 7 处 = **5 处语法/记号**（`n !`/`k !` 阶乘空格 2 ＋ `λ` 保留字 3）＋ **2 处证明方向**；
> 迭代中又暴露 2 处（`↑n.factorial` 类型口径 1 ＋ `rw` 顺序 1）⟹ **共修 9 处**。

| # | 行 | 报错 | 性质 | 修正 |
|---|---|---|---|---|
| 1 | 50 | `unexpected token ':='` | 语法 | `n !` → `n!`（阶乘记号**不许有空格**） |
| 2 | 58 | `unexpected token ')'` | 语法 | `k !` → `k!`（同上） |
| 3 | 76 | `rw [mul_assoc]` 找不到模式 | 证明方向 | 已是右结合 ⟹ 改 `rw [← mul_assoc]` |
| 4 | 93 | `rw [div_neg, neg_div_neg_eq]` 失败 | 多余的重写 | 去掉 `div_neg`，只留 `neg_div_neg_eq` |
| 5 | 186/199/215 | `unexpected token 'λ'` | **保留字** | 参数 `λ` → `lam`（09-09 日志**已记录**，重建时未执行） |
| 6 | 52 | `↑n.factorial` vs `n!` 类型不匹配 | 口径 | 陈述改 `(n.factorial : ℝ)`／`(k.factorial : ℝ)` |
| 7 | 203 | `rw [← hα, ← hlam]` 顺序错 | 证明方向 | 改 `rw [hα] at hlam` → `rw [hlam] at h1` |

⚠️ **教训（两条，可复用）**：
1. **「日志记了修正」≠「重建时执行了修正」** —— 第 96 轮在注释里**抄录**了 09-09 的 `λ` 保留字修正，
   却**没有**在代码里改名 ⟹ 凡「历史已记录的修正」必须**在源码里落一行**，不能只写注释。
2. **不要低估「陈述层」的报错** —— 7 处里 **4 处是语法/记号**，与「API 名过时」无关；
   原 README 把它预估为「若干 API 名」是**错的**。


## 定理族清单（原目标 · 恢复规格保留）

| 族 | 数量 | 代表定理 | 结论 |
|---|---|---|---|
| GA/T | 4 | `GA1 ∫e^{-x²}=√π`、`GA2 ∫e^{-2x²}=√(π/2)`、`T1 exp 级数`、`T2 泊松归一` | 数学基础设施 |
| A3 | 4 | `stationary_proper_time`、`rate_from_clock`、`time_frequency_metric`、`clock_rate_ratio` | 公理 3「时间 = 湮灭频率」降级为定理，`g₀₀ = −(f/f₀)²` |
| A4 | 9 | `a4_metric_reciprocal`、`a4_exterior_roles`、`a4_interior_roles`、`a4_crossing_*`、`a4_schwarzschild_*`、`a4_a3_time_nonpositive`、`a4_t_label_not_a3_time` | 公理 4「空间卷曲成时间」降级为定理，由 `g₀₀·g_rr = −1` 代数强迫 |
| BH | 9 | — | 「可观测宇宙 = 黑洞」的精确含义：`R_s = R_H ⟺ Ω = 1 ⟺ 哈勃球 = 表观视界` |
| AR | 9 | AR-1…AR-9 | 路线 A（50:50 ⟹ k = 0）解剖：中间一环断裂（净**荷**为零 ≠ 净**能量**为零）；球体自能版预言 `R_s/R = 10/3`，与观测 `C=1` 矛盾 |
| LC | 6 | LC-4…LC-7 | 攻 λ：全息热力学给出 **λ = 2αβ**；`S = A/(4l_P²)` ⟹ α = π；**λ = 1 ⟺ β = 1/(2π) ⟺ T = T_GH** |
| LW | 6 | LW-2、LW-3 | 做功项修正（**一般表观视界** `R²(H²+κ)=c²`，非循环）：**Ω_K = 1 − 4α²β²**；Kodama 动力学表面引力版被观测否证（217σ） |
| BX | 5 | BX-1…BX-5 | **攻 β（2026-09-16）**：因果视界 `R_c = c/H` ⟹ `κ = cH` ⟹ **β = 1/(2π)，与 λ 无关** ⟹ `E = N k_B T` 给出 **λ = 1**。另立 2π 来源（F3 + dE=TdS ⟹ T = ℏc³/(8πGMk_B)）。**仍未成定理**（缺环：熵的因果定义与 F3 统计定义需严格对接）。另立 **BX-F 稳健性**：`λ = 4α²β² = 1` 且 ξ 完全约掉 |

## Lean 踩坑（重建/复验时必读 —— 全部来自 09-09～09-12 实测）

1. `λ` 是 Lean binder 保留字，不可作变量名（T2 参数改名 `l`）。
2. `Real.exp_eq_tsum` 已删除 → 用 `rw [Real.exp_eq_exp_ℝ]` +
   `exact (congrFun (NormedSpace.exp_eq_tsum_div (𝔸 := ℝ)) x).symm`（该定理**无 𝕂 命名参数**）。
3. 实数除法的 `def` 必须放 `noncomputable section` 内。
4. `field_simp` 自动消公因子，勿再手动 `mul_left_cancel₀`。
5. linter 的 "Variable not explicitly referenced" 对 `field_simp [...]` 里的假设**会误报**，照它删参数反而编译失败。
6. `unfold` 目标中不存在的常量会直接失败；先 `rw [h]` 再 unfold。
7. `simpa` 需显式 `div_eq_mul_inv` 展开 `rs/r = rs*r⁻¹`（A4 族）。
8. cache get 必须在**根工程**跑；`lake` 进度计数含 no-op 目标，用 `grep -c "Built "` 统计真实编译量。
