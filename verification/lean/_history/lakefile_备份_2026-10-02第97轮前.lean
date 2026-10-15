import Lake
open Lake DSL

-- ============================================================================
-- StormPoC —— MAPS 框架（正反物质对风暴）机器核验 PoC 的 Lake 工程文件
-- ============================================================================
-- 历史：原 lakefile.lean 于 2026-09-09 撰写（当日修复：缺 `package` 声明，
--       Lean 5.0 / Lake 强制），2026-09-16 随旧机 D 盘丢失。
-- 重建：2026-10-02（第 96 轮「A1 Lean 资产恢复」）——依据 09-09 日志与
--       `verification/lean/README.md` 恢复规格。
-- 备注：首次 `lake update` 时若格式报错，以本机 Lake 版本文档为准微调
--       （本工程于 Lean 4.34.0-rc2 / Lake 5.0.0-src 下核验过，见 lean-toolchain）。

package StormPoC where
  -- 无额外选项；工具链由 lean-toolchain 锁定

require mathlib from git
  "https://github.com/leanprover-community/mathlib4"

@[default_target]
lean_lib StormPoC where
  -- 默认根模块 = StormPoC.lean
