# -*- coding: utf-8 -*-
"""第 96 轮：Lean 工具链解压安装（zip → ~/.elan/toolchains/leanprover--lean4---v4.34.0-rc2）。"""
import zipfile, os, shutil, time

zpath = r'C:/Users/Administrator/.lean-dl/lean-4.34.0-rc2-windows.zip'
dest = r'C:/Users/Administrator/.elan/toolchains/leanprover--lean4---v4.34.0-rc2'
prefix = 'lean-4.34.0-rc2-windows/'
os.makedirs(dest, exist_ok=True)
z = zipfile.ZipFile(zpath)
t0 = time.time(); n = 0
for info in z.infolist():
    nm = info.filename
    if not nm.startswith(prefix):
        continue
    rel = nm[len(prefix):]
    if rel == '' or rel.endswith('/'):
        if rel:
            os.makedirs(os.path.join(dest, rel.rstrip('/')), exist_ok=True)
        continue
    target = os.path.join(dest, rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with z.open(info) as src, open(target, 'wb') as out:
        shutil.copyfileobj(src, out, 1024 * 256)
    n += 1
    if n % 3000 == 0:
        print('  {}/18377  {:.0f}s'.format(n, time.time() - t0), flush=True)
print('INSTALL DONE: {} files, {:.0f}s'.format(n, time.time() - t0))
