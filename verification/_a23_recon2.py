# -*- coding: utf-8 -*-
"""A23 侦查 2：定位 08-23 那个「普朗克常数」在现稿里是否还有对象；并核 ℏ 与 G 的辨识性线索"""
import io, os

BASE = r"C:\Users\Administrator\Desktop\2026-08-20-21-43-34"
FILES = {
    "ZH论文": os.path.join(BASE, "outputs", "论文初稿_正反物质对风暴统一框架_v2.9.md"),
    "EN论文": os.path.join(BASE, "outputs", "Paper_MatterAntimatterPairStorm_v2.9_EN.md"),
    "交接说明": os.path.join(BASE, "环境交接说明.md"),
    "清单": os.path.join(BASE, "outputs", "工程期望清单.md"),
    "技能SKILL": os.path.join(r"C:\Users\Administrator\.workbuddy\skills\maps-deduction-round", "SKILL.md"),
}
KEYS = ["16\u03c0G\u00b2", "M\u00b2/A", "3.6\u00d710\u2075\u00b2", "3.6\u00d7 10\u2075\u00b2",
        "\u666e\u6717\u514b\u5e38\u6570", "Planck constant", "l_P\u00b2 = G\u210f/c\u00b3",
        "G\u210f/c\u00b3", "l_P^2 = G\\hbar", "\u4e8b\u4ef6\u6d41\u6700\u5c0f\u5c3a\u5ea6",
        "\u975e\u57fa\u672c\u5e38\u6570", "not fundamental",
        "\u5012\u63a8", "\u03b2 = 1/(2\u03c0)", "\u03b1 = 1"]

for name, p in FILES.items():
    if not os.path.exists(p):
        print(name + "  <缺失>")
        continue
    t = io.open(p, encoding="utf-8").read()
    print("=== " + name + " ===")
    for k in KEYS:
        n = t.count(k)
        if n:
            print("   " + str(n) + "  " + k)
    print("")
