# -*- coding: utf-8 -*-
"""GAP 调用助手（第 48 轮装成 GAP 4.16.1 后抽出，供后续轮次复用）。

用法：
    from _gap import gap_run, orbit_size_via_gap, gap_available
    out = gap_run('Print(Size(SymmetricGroup(5)), "\\n"); QUIT;')
    print(out)

⚠️ 三个坑（见 工作流说明「GAP」一节）：
  ① 必须把 runtime\\bin 与 gap 根目录都加进 PATH（cygwin1.dll / libgap.dll）；
  ② 不能用 `timeout` 包（Git Bash 的 execvp 与 Windows 加载器不兼容）；
  ③ `gap.bat` 走 cygstart+mintty，无法非交互，别用。
"""

import io
import os
import subprocess
import tempfile

GAPROOT = r"C:\Program Files\GAP-4.16.1\runtime\opt\gap-4.16.1"
GAPBIN_DIR = r"C:\Program Files\GAP-4.16.1\runtime\bin"


def _env():
    env = dict(os.environ)
    env["PATH"] = GAPBIN_DIR + os.pathsep + GAPROOT + os.pathsep + env.get("PATH", "")
    return env


def gap_available():
    """True/False —— 不抛异常。"""
    try:
        return "GAP" in gap_run('Print("GAP ", GAPInfo.Version, "\\n"); QUIT;', timeout=120)
    except Exception:
        return False


def gap_run(script_text, timeout=5400):
    """把 script_text 写进临时 .g，用 gap.exe -q -b 跑，返回合并后的输出。"""
    fd, path = tempfile.mkstemp(suffix=".g")
    os.close(fd)
    io.open(path, "w", encoding="ascii").write(script_text)
    try:
        r = subprocess.run([os.path.join(GAPROOT, "gap.exe"), "-q", "-b"],
                           stdin=open(path, "rb"), stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, env=_env(), timeout=timeout)
        return r.stdout.decode("utf-8", "replace")
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def permlist(p):
    """Python 0-indexed 置换（列表，p[i] = i 的像）→ GAP PermList。"""
    return "PermList([" + ",".join(str(x + 1) for x in p) + "])"


def config_set(cfg, N):
    """bitmask → GAP 集合 [i+1, ...]。"""
    return "[" + ",".join(str(i + 1) for i in range(N) if (cfg >> i) & 1) + "]"


def _parse_markers(out, n_cfgs):
    """解析 ORDER / STABn 标记。

    ⚠️ 坑（第 49 轮查出）：GAP 对**超长整数会折行**（(6,6,6) 的 |G| 有 223 位），
    于是输出是「ORDER\\n<数字片段1>\\n<片段2>…」。只按行解析会 IndexError。
    这里把「标记行之后、下一个标记之前」的**所有数字片段拼接**成一个整数。
    """
    order = None
    stabs = []
    buf = None                       # 当前正在累积的字段名（None = 还没遇到标记）
    acc = ""
    for raw in out.splitlines():
        ln = raw.strip()
        if not ln:
            continue
        if ln.startswith("ORDER"):
            buf, acc = "ORDER", ln[len("ORDER"):].strip()
        elif ln.startswith("STAB"):
            # 先把上一个字段收尾
            if buf == "ORDER":
                order = int(acc)
            elif buf is not None and buf.startswith("STAB"):
                stabs.append(int(acc))
            buf, acc = ln.split()[0] if ln.split() else "STAB", \
                (ln.split()[1] if len(ln.split()) > 1 else "")
        elif buf is not None:
            # 纯数字片段 ⟹ 拼到当前字段上（GAP 的折行续行）
            acc += ln
        else:
            continue                 # 标记之前的其它输出（如 GAP 报错）忽略
    if buf == "ORDER":
        order = int(acc)
    elif buf is not None and buf.startswith("STAB"):
        stabs.append(int(acc))
    if order is None or len(stabs) != n_cfgs:
        raise RuntimeError("GAP 输出不完整（order={}, stabs={}/{}）\n尾部：{}".format(
            order, len(stabs), n_cfgs, "\n".join(out.strip().splitlines()[-6:])))
    return order, stabs


def orbit_sizes_via_gap(gens, cfgs, N, timeout=5400):
    """返回 (|G|, [|O(c)| ...])；|O(c)| = |G| / |Stab_G(c)|。

    gens: 置换列表（每个是长度 N 的列表）；cfgs: bitmask 列表。
    """
    lines = ["SetPrintFormattingStatus(\"*stdout*\", false);;",   # 尽量不折行
             "gens := [", ",\n        ".join(permlist(g) for g in gens), "];;",
             "G := Group(gens);;", 'Print("ORDER ", Size(G), "\\n");']
    for k, cfg in enumerate(cfgs):
        lines.append("c{0} := {1};;".format(k, config_set(cfg, N)))
        lines.append('Print("STAB{0} ", Size(Stabilizer(G, c{0}, OnSets)), "\\n");'.format(k))
    lines.append("QUIT;")
    out = gap_run("\n".join(lines) + "\n", timeout=timeout)
    order, stabs = _parse_markers(out, len(cfgs))
    return order, [order // s for s in stabs]


if __name__ == "__main__":
    print("GAP 可用:", gap_available())
    print(gap_run('Print("sym5 stab ", Size(Stabilizer(SymmetricGroup(5),[1,2],OnSets)), "\\n"); QUIT;'))
