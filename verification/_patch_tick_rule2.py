# -*- coding: utf-8 -*-
"""第 26 轮补丁之二：把 UP-6b 的发现补进 §8.6.7(c) —— 相位必须「每线独立」。
中英同步。锚点必须恰好命中一次。"""
import io
import sys

BASE = "C:/Users/Administrator/Desktop/2026-08-20-21-43-34/outputs/"
ZH = BASE + "论文初稿_正反物质对风暴统一框架_v2.9.md"
EN = BASE + "Paper_MatterAntimatterPairStorm_v2.9_EN.md"
ACTIONS = []

def patch(path, old, new, tag):
    s = io.open(path, encoding="utf-8").read()
    n = s.count(old)
    if n != 1:
        print("  [XX] %-44s 锚点命中 %d 次 —— 拒绝改动" % (tag, n))
        ACTIONS.append((tag, False))
        return
    io.open(path, "w", encoding="utf-8").write(s.replace(old, new))
    print("  [OK] %-44s 已替换" % tag)
    ACTIONS.append((tag, True))

zh_old = ("- **相位随机**（每条线独立、每 tick 重抽）——相位固定时粒子在轴上的奇偶角色被锁定："
          "走一步即翻转奇偶，下一步便换回另一端，形成二周期振荡、位移有界"
          "（数值：⟨r²⟩ = 2，而扩散值为 600）。")
zh_new = ("- **相位随机**（**每条线独立**、每 tick 重抽）——两种偷懒都会失败："
          "(i) 相位固定时粒子在轴上的奇偶角色被锁定，走一步即翻转奇偶、下一步换回另一端，"
          "形成二周期振荡、位移有界（数值：⟨r²⟩ = 2，而扩散值为 600）；"
          "(ii) **即使每 tick 重抽，只要全局共用一个相位**（同一 tick 内所有线同侧），"
          "相位就与「轴」耦合成系统性取向模式，⟨r²⟩ 塌到 n 的 29.7% / 42.5%（两个种子），"
          "而每线独立时为 100.0%。**故「每线独立」是必需条件，不是实现偏好。**")
patch(ZH, zh_old, zh_new, "ZH 补 §8.6.7(c) 每线独立")

en_old = ("- **random phase** (independently redrawn per line each tick) — with a fixed phase, "
          "a particle's parity role on that axis is locked: one step flips its parity, so the next "
          "step sends it back, producing a two-cycle oscillation with bounded displacement "
          "(numerically ⟨r²⟩ = 2 against a diffusive value of 600).")
en_new = ("- **random phase** (**independently per line**, redrawn each tick) — two shortcuts both fail: "
          "(i) with a fixed phase, a particle's parity role on that axis is locked: one step flips its "
          "parity, so the next step sends it back, producing a two-cycle oscillation with bounded "
          "displacement (numerically ⟨r²⟩ = 2 against a diffusive value of 600); "
          "(ii) **even if the phase is redrawn every tick, a single global phase** (all lines on the same "
          "side within one tick) couples the phase to the axis into a systematic orientation pattern, "
          "collapsing ⟨r²⟩ to 29.7% / 42.5% of n (two seeds), versus 100.0% for independent per-line "
          "phases. **Per-line independence is therefore a requirement, not an implementation preference.**")
patch(EN, en_old, en_new, "EN patch 8.6.7(c) per-line")

print("\n" + "=" * 66)
ok = sum(1 for _, v in ACTIONS if v)
print("补丁动作 %d 项，成功 %d，失败 %d" % (len(ACTIONS), ok, len(ACTIONS) - ok))
sys.exit(0 if ok == len(ACTIONS) else 1)
