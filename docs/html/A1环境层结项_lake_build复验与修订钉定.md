# A1 环境层结项：lake build 复验与修订钉定

> **第 97 轮** ｜ 2026-10-03（跨 10-02 夜）｜ 脚本 `_lean_build_97.py`（LB）＋ 补丁 `_patch_97.py`（15 项 0 失败）＋ 核验 `_verify_97.py`（V 系列）
> 任务来源：**外部待办 A1 环境层** —— 第 96 轮明确的「唯一剩余可判定入口」。

---

## 一、一句话结论

**A1 在环境层闭环**：mathlib 钉定到 **2026-09-09 原修订 `eda2e61d06…`** ＋ Lean **4.34.0-rc2** ⟹
`lake build StormPoC` = **`Build completed successfully (8909 jobs)`**（**0 error**，**2 处 `sorry` 警告** = 第 96 轮登记的「sorry 2」）。

⚠️ 但这个「8909」**不是**「8909 个定理通过」——见 §六（**C-57**）。

---

## 二、验收目标与达成情况

| 目标（第 96 轮列为待办） | 实测 | 判定 |
|---|---|---|
| ① `lake update` 成功，mathlib 落到 `eda2e61d06…` | ✅ manifest rev = 钉定值；clone pack **505,165,591 B**（505MB） | 达成 |
| ② `lake exe cache get` 取回 olean | ✅ 下载 **8892 个 .ltar / 451MB（100%）**；解压 olean **8905**／ilean 8902／trace 8947 | 达成 |
| ③ `lake build StormPoC` 全绿，对照 8909 | ✅ **8909 jobs**、0 error（但**首次失败 7 处**，修毕） | 达成 |

⚠️ ② 的 `cache get` 以 **exit=1** 收尾（报 `6694 decompression(s) failed`、`os error 5 拒绝访问`），
但磁盘上的 olean 已达 **8905**（≈ 全量）⟹ **判定为「产物到位、退出码不可信」**。原因见 §五-1。

---

## 三、关键决策：必须钉定 mathlib 修订（不能取 master）

| 事实 | 值 | 来源 |
|---|---|---|
| 原环境 mathlib 修订 | **`eda2e61d0616efeb868bc0523055b548e5bd761b`**（09-09 10:59 UTC 的 master HEAD） | 09-09 日志 |
| 该修订的 `lean-toolchain` | `leanprover/lean4:v4.34.0-rc2` | 实测（raw 通道解析短 SHA） |
| **今天的 mathlib master** | **`leanprover/lean4:v4.35.0-rc3`** ⚠️ | 实测 —— 与本机工具链**不兼容** |

⟹ 按原 lakefile 直接 `lake update` 会拉到 master（要求 v4.35.0-rc3）而失败。已改为：

```
require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "eda2e61d0616efeb868bc0523055b548e5bd761b"
```

📌 **可复用方法论**：依赖库的 master 会移动 ⟹ **凡「复现旧环境」必须钉修订**；
短 SHA → 完整 SHA 的解析手法 = **blobless ＋ depth 窗口 fetch ＋ `git rev-parse`**（本机代理不支持 api.github.com / HTML 提交页）。

---

## 四、环境再现流程（三件套，与 09-09 蓝图逐条对齐）

1. **git 全局面具**（lake 内部所有 fetch 走镜像）：
   ```
   git config --global url."https://ghfast.top/https://github.com/".insteadOf "https://github.com/"
   git config --global core.longpaths true     # Windows 长路径（mathlib 深层目录）
   ```
2. **cache 服务器（已迁移）**：`https://cache.mathlib.org/mathlib4`（旧 `olean-cache.lean-lang.org` = NXDOMAIN）；
   下载路径**内容寻址** `/f/{hash}.ltar`，落地 `~/.cache/mathlib/`。
3. **post_update 钩子**：根工程 update 后自动 `lake exe cache get`；⚠️ **必须在根工程跑**（子目录跑会触发嵌套克隆）。

**实测耗时**：`cache get` 单线程 23:44:13 → 04:42:08 = **4h58m**（下载 451MB ＋ 解压 8892 个 .ltar）。
`lake build` 首次 04:42:19 → 04:56:55（14.6 min，其中 **StormPoC 自身 674 s**）；后续增量重编 **100–124 s**。

---

## 五、过程记录：两处踩坑（可复用）

1. ⚠️ **不要在 lake 正在解压时用别的进程读同一批 `.ltar`**。
   本轮为统计「每包目标库名」用 16 线程并发读了 8892 个 `.ltar` 的头部 ⟹
   `cache get` 立刻开始报 `C:\…\62b897688f2651ba.ltar: 拒绝访问。（os error 5）`，
   最终 `exit=1`、`6694 decompression(s) failed`。**Windows 句柄共享冲突**所致。
   ✅ 幸而产物仍达到全量（olean 8905）⟹ 未影响 build。**下次要统计就等解压结束再扫。**
2. ⭐ **`leantar` 自带并行解压接口**，本轮白等了 5 小时：
   ```
   leantar -x -j - --jobs <N>        # '-j -' 表示 stdin 读 JSON
   # JSON: { file: "x.ltar", base?: "<解包根>", hash?: "..." }
   ```
   `--jobs N` **默认就是 num CPUs**，而 `lake exe cache get` 走的是**单线程**路径。
   ⟹ **下次换机重来：先 `cache get`（下载），再用 `leantar --jobs N` 自己并行解压**，可省约 4 小时。
   （本轮实测单线程解压速率 ≈ **0.5 个文件/秒**；而目标盘裸写小文件可达 **617 个/秒** ⟹ 瓶颈在 leantar 的每文件开销，不在磁盘。）

---

## 六、⚠️ C-57：两条口径更正（本轮真正的负面产出）

### ① **「8909 jobs 全绿」≠「8909 个定理通过」**

实测这 8909 个 job 里：

| 组成 | 数量 |
|---|---|
| mathlib 全量 ＋ batteries／aesop／Qq／Cli／proofwidgets／importGraph／plausible／LeanSearchClient | **8908** |
| **StormPoC 自身** | **1** |

⟹ 这个数**只证明「依赖建得起 ＋ 本文件能过」**。
论文/日志里把「8909 jobs 全绿」与「8 族 52 定理」**并列引用**是**口径混用**——它们量纲不同。
📌 **正确表述**：`lake build` 的 job 数衡量**构建规模**，定理数衡量**内容**，两者**不得互换**。

### ② **「日志记了修正」≠「重建时执行了修正」**

首次 build **7 处报错**，其中 **3 处**（`λ` 保留字）**09-09 日志早已记录** ——
但第 96 轮重建时**只把这条修正写进了源码注释，没有改代码**（注释写着「λ 是 Lean binder 保留字 ⟹ 参数改名 l」，
而三处签名里仍赫然是 `λ`）。

⟹ ⭐ **规范**：凡「历史已记录的修正」，重建时**必须在源码里落一行**，注释不算。

---

## 七、首次 build 的 9 处修正（逐条如实登记）

四次构建：**7 处报错 → 4 处 → 2 处 → 0**。

| # | 行 | 报错 | 性质 | 修正 |
|---|---|---|---|---|
| 1 | 50 | `unexpected token ':='; expected no space before` | 语法/记号 | `n !` → `n!`（阶乘记号**不许有空格**） |
| 2 | 58 | `unexpected token ')'` | 语法/记号 | `k !` → `k!` |
| 3 | 76 | `rw [mul_assoc]` 找不到 `?a * ?b * ?c` | 证明方向 | 已是右结合 ⟹ 改 `rw [← mul_assoc]` |
| 4 | 93 | `rw [div_neg, neg_div_neg_eq]` 失败 | 证明方向（多余重写） | 去掉 `div_neg`，只留 `neg_div_neg_eq` |
| 5 | 186 | `unexpected token 'λ'` | **保留字** | 参数 `λ` → `lam` |
| 6 | 199 | `unexpected token 'λ'` | **保留字** | 同上 |
| 7 | 215 | `unexpected token 'λ'` | **保留字** | 同上 |
| 8 | 52 | `↑n.factorial` vs `n!` 类型不匹配 | 类型口径 | 陈述改 `(n.factorial : ℝ)`／`(k.factorial : ℝ)` |
| 9 | 203 | `rw [← hα, ← hlam]` 找不到 `π` | 证明方向 | 改 `rw [hα] at hlam` → `rw [hlam] at h1` |

⚠️ 附带发现：**`hλ` 也不是合法标识符**（词法把 `λ` 单独切成 token）⟹ 一并改为 `hlam`（5 处）。

📌 **教训补充**：7 处里 **5 处是语法/记号**，与「API 名过时」无关；
第 96 轮 README 把它预估为「按报错微调若干 API 名」是**错的**（已更正）。

---

## 八、诚实边界（必须一起读）

1. **「编译通过」≠「原文件恢复」**：本文件仍是第 96 轮的**分级重建版**
   （含证 21／**sorry 2**／待重写 23／设计登记 5）。
   编译通过 = **已写的 21 条声明全部为真**；**不代表 23 条「待重写」已补**，
   也**不代表原 8 族 52 定理已全部还原**。
2. **2 处 sorry 仍在**（`StormPoC.lean:160` = `ar_k_from_lambda`、`:186` = BH 族锚点）——与登记值一致，**未消除**。
3. **钉定修订 ≈ 原环境，但不是原环境本身**：原 manifest 只留 10 位短 SHA，本轮解析为完整 SHA 后钉定；
   若原 clone 发生在 09-09 当日稍早/稍晚的提交上，可能有数个提交的偏差。
   ✅ 旁证：本次 job 数 **8909** 与原始记录 **8909** 一致 ⟹ 偏差（若有）未改变构建规模。
4. **本机为新机**（早期环境随丢失）；工具链 zip 大小等口径已在 C-56 / 第 96 轮登记。
5. **A1 结项 ≠ 项目有工程出口**：工程出口仍为 **0**（第 61 轮定案）；
   Lean PoC 属于**自洽性核验**，不是可造物。剩余待办只剩 **EMRI**（等 LISA，三前提在框架之外）。

---

## 九、本轮下游同步（下游同步三维：判定／正文／台账）

| 维度 | 改动 |
|---|---|
| 判定标签 | A1：~~进行中~~ → **✅ 全部结项**（文件层 96 ＋ 环境层 97） |
| 正文/资产 | `lean/README.md`（状态短语 ＋ 补全路线第 4 步 ＋ **首次 build 修正清单**）；`StormPoC.lean`（9 处修正） |
| 编号台账 | **C-57**（两条口径更正）；更正计数 55 → **56**；三处「剩余待办」行同步；交接说明 §七 96→97 ＋ 新增「第 97 轮」段 |

备份：`lean/_history/StormPoC_备份_2026-10-03第97轮build前.lean`；
清单/交接备份见根目录 `*_备份_2026-10-02第97轮前.md`；MEMORY 备份在 `~/.lean-dl/MEMORY_备份_2026-10-02第97轮前.md`。
