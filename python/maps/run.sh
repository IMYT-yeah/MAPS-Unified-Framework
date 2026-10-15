#!/usr/bin/env bash
# python/maps/run.sh —— 运行 MAPS 新思考包的 T1–T5 锚点验证
#
# ⚠️ 重建说明（第 98 轮 · 2026-10-03）：原 run.sh 未在任何日志/审计中留下内容
#    ⟹ 本文件属【C 级 · 重设计】。判据只有一条：把包跑完并给出可判定的退出码。
#
# 用法：  bash python/maps/run.sh
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 优先用项目隔离 venv（含 numpy/sympy），否则退回当前 python
PY="${MAPS_PY:-python}"
if [ -x "[HOME]/.workbuddy/binaries/python/envs/default/Scripts/python.exe" ]; then
  PY="${MAPS_PY:-[HOME]/.workbuddy/binaries/python/envs/default/Scripts/python.exe}"
fi

rc=0
echo "== [1/2] maps_framework.py（T1-T5 锚点） =="
( cd "$HERE" && "$PY" maps_framework.py ) || rc=1

echo
echo "== [2/2] verify.py（独立符号/数值自检） =="
( cd "$HERE" && "$PY" verify.py ) || rc=1

echo
if [ "$rc" -eq 0 ]; then
  echo "run.sh: 全部通过"
else
  echo "run.sh: 有失败项（退出码 $rc）"
fi
exit "$rc"
