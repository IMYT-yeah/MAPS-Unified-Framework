# -*- coding: utf-8 -*-
"""A23 侦查：盘点论文中 ℏ 的全部出现形态（按上下文片段聚类）"""
import io, re, collections, os

BASE = r"C:\Users\Administrator\Desktop\2026-08-20-21-43-34"
Z = io.open(os.path.join(BASE, "outputs", "论文初稿_正反物质对风暴统一框架_v2.9.md"),
            encoding="utf-8").read().split("\n")
E = io.open(os.path.join(BASE, "outputs", "Paper_MatterAntimatterPairStorm_v2.9_EN.md"),
            encoding="utf-8").read().split("\n")

for name, L, sym in (("ZH", Z, "\u210f"), ("EN", E, "hbar")):
    hits = [(i + 1, s) for i, s in enumerate(L) if sym in s]
    print("=== " + name + "：含 " + sym + " 的行数 = " + str(len(hits)) + " ===")
    if sym == "\u210f":
        ctx = collections.Counter()
        for i, s in hits:
            for m in re.finditer(r"[^ ，。；：（）|]{0,12}\u210f[^ ，。；：（）|]{0,12}", s):
                ctx[m.group(0)] += 1
        for k, v in ctx.most_common(80):
            print("   " + str(v) + "  " + k)
    else:
        ctx = collections.Counter()
        for i, s in hits:
            for m in re.finditer(r"[\w\\{}^/\-\.\{\} ]{0,16}hbar[\w\\{}^/\-\.\{\} ]{0,16}", s):
                ctx[m.group(0)] += 1
        for k, v in ctx.most_common(40):
            print("   " + str(v) + "  " + k)
    print("")
