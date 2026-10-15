# -*- coding: utf-8 -*-
"""本地一键验证：stormetric 53 测试（+ maps 锚点，若已恢复）"""
import subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
PY = sys.executable


def run(cmd):
    print("\n$ " + " ".join(map(str, cmd)))
    return subprocess.run(cmd, cwd=ROOT).returncode


ok = True
maps = ROOT / "python/maps/maps_framework.py"
if maps.exists():
    ok &= run([PY, str(maps)]) == 0
else:
    print("\n[skip] python/maps 尚未恢复（见 python/maps/README.md）")
ok &= run([PY, "-m", "pytest", "python/stormetric", "-q"]) == 0
print("\n== 本地验证 %s ==" % ("全部通过" if ok else "存在失败"))
sys.exit(0 if ok else 1)
