# 资产丢失登记（2026-09-16 初版 · 2026-10-02 第 96 轮更新）

原仓库 `D:/Users/IMYT.YT/WorkBuddy/MAPS-Unified-Framework` 随 D 盘消失（本机仅 C 盘），
本仓库由 `outputs/` 镜像重建。**以下资产在镜像中不存在**：

| 资产 | 内容 | 状态（10-02 更新） |
|---|---|---|
| `verification/lean/StormPoC.lean` | 8 个定理族：GA/T（4）、A3（4）、A4（9）、BH（9）、AR（9）、LC（6）、LW（6）、**BX（5）** | ✅ **已重建**（2026-10-02 第 96 轮；分级恢复，见 `verification/lean/README.md`） |
| `verification/lean/lakefile.lean` / `lean-toolchain` / `.github/workflows/lean-poc.yml` | Lean 4.34.0-rc2 + mathlib CI | ✅ **已重建**（第 96 轮） |
| `python/maps/`（`formula.py`、`maps_framework.py`、`verify.py`、`run.sh`） | MAPS 新思考 T1–T5 锚点计算包（修复版） | ❌ 丢失（源 `_MAPS_explore` 亦不在）；恢复规格见 `python/maps/README.md` |
| `notes/推演专题/黑洞宇宙条件_从巧合到必然.md` | BH 族专题（8 节） | ❌ 丢失（09-11 撰写；结论见 `.workbuddy/memory/2026-09-11.md`） |
| `notes/推演专题/路线A_50比50到平坦性_解剖报告.md` | AR 族解剖 | ❌ 丢失（09-11；结论见 09-11 日志） |
| `notes/推演专题/攻λ_全息热力学与临界密度.md` | LC 族（λ = 2αβ 路线） | ❌ 丢失（09-11；结论见 09-11 日志） |
| `notes/推演专题/做功项修正_λ的命运.md` | LW 族（做功项修正） | ❌ 丢失（09-12；结论见 09-12 日志） |

**⚠️ 10-02 补充登记（第 96 轮取证）**：第 4–7 行的四份中旬报告**当时不在 `outputs/` 镜像中**
（它们在旧机 repo 的 `notes/` 里），因此 09-16 重建时未被镜像 —— 属**同类丢失但未入初版登记**。
其内容以 09-11/09-12 日志的描述为最高现存凭证；Lean 侧的结论目标已随 StormPoC.lean 重建保留。

恢复规格见 `verification/lean/README.md` 与 `python/maps/README.md`。
