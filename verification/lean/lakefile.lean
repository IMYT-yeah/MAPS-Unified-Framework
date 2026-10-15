import Lake
open Lake DSL

-- ============================================================================
-- StormPoC —— MAPS 框架（正反物质对风暴）机器核验 PoC 的 Lake 工程文件
-- ============================================================================
-- 历史：原 lakefile.lean 于 2026-09-09 撰写（当日修复：缺 `package` 声明，
--       Lean 5.0 / Lake 强制），2026-09-16 随旧机 D 盘丢失。
-- 重建：2026-10-02（第 96 轮「A1 Lean 资产恢复」）——依据 09-09 日志与
--       `verification/lean/README.md` 恢复规格。
-- 修订钉定：2026-10-02（第 97 轮「环境层：lake update → cache get → build 复验」）——
--       ⚠️ mathlib master 现已移到 leanprover/lean4:v4.35.0-rc3，与本工程工具链
--       （v4.34.0-rc2）不兼容 ⟹ 必须钉修订（不能取 master）。
--       钉定值 = 2026-09-09 原环境 clone 时的 master HEAD
--       （09-09 日志：「manifest 生成（HEAD eda2e61d06 = master）」，其 lean-toolchain = v4.34.0-rc2）。

package StormPoC where
  -- 无额外选项；工具链由 lean-toolchain 锁定

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "eda2e61d0616efeb868bc0523055b548e5bd761b"

@[default_target]
lean_lib StormPoC where
  -- 默认根模块 = StormPoC.lean
