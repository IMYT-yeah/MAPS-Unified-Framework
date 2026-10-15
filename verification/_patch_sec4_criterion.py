# -*- coding: utf-8 -*-
"""
§4.2 第四处修正：判据校准 —— 把上一轮写的「A 段未通过」改对
依据：outputs/_m1_runA_convergence.py（HA-1…HA-3，失败项：无）
  噪声基线（从精确麦克斯韦抽样、同口径）：N=256→24.3%±4.9%、500→16.6%、512→16.5%、
  1000→11.4%、1024→11.4%、2000→8.0%、8000→3.9%
  A 段实测 22.74% = 基线 0.94 倍（1σ 内）；加长 4× 后 28.25%（1.16 倍，未下降）
锚点必须恰好命中一次。
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT, FAIL = [], []


def rep(path, tag, old, new):
    s = open(path, encoding="utf-8").read()
    n = s.count(old)
    if n != 1:
        FAIL.append("%s｜%s：锚点命中 %d 次" % (os.path.basename(path), tag, n))
        print("  [XX] %-42s 命中 %d 次" % (tag, n))
        return
    open(path, "w", encoding="utf-8").write(s.replace(old, new, 1))
    OUT.append("%s｜%s" % (os.path.basename(path), tag))
    print("  [OK] %-42s 已改" % tag)


ZH_OLD = "- **③ 诚实补记未通过项**（原稿未列）：**确定性硬球（A 段）**速度分布加权偏差 **22.74%**（原稿记 ~18%），**总体判定为「未完全收敛」**（判据 <10% 未过）；**参数扫描（C 段）**中 v0=2.0/N=1000 与 v0=1.0/N=500 两项偏差 **13.6% / 20.7%**，**未通过**判据。**事件流 DSMC（B 段）**全部通过（温度 0.00%、分布 7.02%、ΔH = −2.266、Birkhoff 检验通过）——本命题链的核心支撑来自 B 段。"

ZH_NEW = """- **③ 判据校准（重要修正：上一版记的「A 段未通过」实为判据不可用）**：该加权偏差指标存在**随 N 变化的统计噪声基线**（从**精确麦克斯韦**分布抽样、同一 bins/权重口径测得，400 次平均）：N=256 → **24.3%±4.9%**、N=500 → 16.6%、N=512 → 16.5%、N=1000 → 11.4%、N=1024 → 11.4%、N=2000 → **8.0%**、N=8000 → 3.9%。⟹ **绝对判据「<10%」在 N ≲ 1600 时不可用**（基线本身已 ≥10%）。据此复核三段：
  · **A 段（确定性硬球，N=256）**实测 **22.74% = 基线的 0.94 倍**（落在 1σ 内）⟹ **与完全正确的麦克斯韦分布不可区分，不存在「未完全收敛」**；且**步数加长 4 倍（20000 步）后偏差 28.25%（1.16 倍基线）并未下降** ⟹ 进一步排除「弛豫不足」，残余可归因于 2D 长时尾（原稿已诚实标注）；
  · **C 段**：v0=2.0/N=1000 的 13.6% = 基线 11.4% 的 1.19 倍（1.1σ）；v0=1.0/N=500 的 20.7% = 基线 16.6% 的 1.25 倍（1.4σ）⟹ **均为噪声量级，非物理失败**；
  · **B 段（事件流 DSMC，N=2000）**：分布 7.02% = 基线 8.0% 的 **0.88 倍**，连同温度 0.00%、ΔH = −2.266、Birkhoff 检验通过 ⟹ **全部通过**。
  ⟹ **判据应改为相对式「实测偏差 / 噪声基线 ≲ 1.5」**；原绝对判据在 N=2000 时也仅比基线高约 1.4σ，辨别力有限。**本命题链的核心支撑来自 B 段。**"""

EN_OLD = "- **③ Honest record of failed cases (not listed before)**: **deterministic hard disks (run A)** give a weighted distribution deviation of **22.74%** (the draft noted ~18%) and an **overall verdict of \"not fully converged\"** (the <10% criterion is not met); in the **parameter scan (run C)**, v0=2.0/N=1000 and v0=1.0/N=500 give **13.6% / 20.7%**, **failing** the criterion. The **event-flow DSMC (run B)** passes everything (temperature 0.00%, distribution 7.02%, ΔH = −2.266, Birkhoff test passed) — the core support for this proposition chain comes from run B."

EN_NEW = """- **③ Criterion calibration (important correction: the "run A fails" note in the previous version was a criterion artifact)**: this weighted-deviation metric has a **sample-size-dependent statistical noise floor** (obtained by sampling from the **exact Maxwellian** with identical bins/weights, averaged over 400 trials): N=256 → **24.3%±4.9%**, N=500 → 16.6%, N=512 → 16.5%, N=1000 → 11.4%, N=1024 → 11.4%, N=2000 → **8.0%**, N=8000 → 3.9%. ⟹ the absolute criterion "<10%" is **unusable for N ≲ 1600** (the floor itself is ≥10%). Re-auditing the three runs against the floor:
  · **run A (deterministic hard disks, N=256)** measures **22.74% = 0.94× the floor** (within 1σ) ⟹ **indistinguishable from a perfectly correct Maxwellian — there is no "not fully converged"**; moreover **quadrupling the number of steps (20000) leaves the deviation at 28.25% (1.16× floor), i.e. it does not decrease** ⟹ "insufficient relaxation" is further excluded, and the residual can be attributed to the 2D long-time tail (already honestly noted in the draft);
  · **run C**: v0=2.0/N=1000 gives 13.6% = 1.19× the N=1000 floor 11.4% (1.1σ); v0=1.0/N=500 gives 20.7% = 1.25× the N=500 floor 16.6% (1.4σ) ⟹ **both at the noise level, not physical failures**;
  · **run B (event-flow DSMC, N=2000)**: distribution 7.02% = **0.88×** the 8.0% floor, together with temperature 0.00%, ΔH = −2.266 and the Birkhoff test ⟹ **fully passing**.
  ⟹ **The criterion should be changed to the relative form "measured / noise floor ≲ 1.5"**; the original absolute criterion is only ~1.4σ above the floor even at N=2000, so its discriminating power is limited. **The core support for this proposition chain comes from run B.**"""

jobs = [
    (os.path.join(HERE, "论文初稿_正反物质对风暴统一框架_v2.9.md"), ZH_OLD, ZH_NEW),
    (os.path.join(HERE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md"), EN_OLD, EN_NEW),
]

HIST = os.path.join(ROOT, "MAPS-Unified-Framework", "paper", "history")
os.makedirs(HIST, exist_ok=True)
for p, _, _ in jobs:
    b = os.path.join(HIST, os.path.basename(p).replace(".md", "_备份_2026-09-18判据前.md"))
    open(b, "w", encoding="utf-8").write(open(p, encoding="utf-8").read())
    print("  备份 →", os.path.basename(b))

for p, old, new in jobs:
    print("\n" + "=" * 70 + "\n" + os.path.basename(p) + "\n" + "=" * 70)
    rep(p, "判据校准：A/C 段失败项改正", old, new)

print("\n完成 %d 项" % len(OUT))
for o in OUT:
    print("  ·", o)
print("失败：%s" % ("；".join(FAIL) if FAIL else "无"))
