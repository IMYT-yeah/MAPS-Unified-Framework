# -*- coding: utf-8 -*-
"""
§4.2 第三处修正：把「遍历性」的证据换成真正的 Birkhoff 检验，并补记未通过项
依据：outputs/_m1_ergodicity_proper.py（EG-1…EG-3，失败项：无）
      + 重跑 outputs/_m1_boltzmann.py 的实测（A/B/C 三段）
锚点必须恰好命中一次，否则报错退出。
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
        print("  [XX] %-40s 命中 %d 次" % (tag, n))
        return
    open(path, "w", encoding="utf-8").write(s.replace(old, new, 1))
    OUT.append("%s｜%s" % (os.path.basename(path), tag))
    print("  [OK] %-40s 已改" % tag)


ZH_NEW = """**数值模拟验证**【推导】：细致平衡马尔可夫链收敛到玻尔兹曼分布（偏差 2.12%）。

**【v2.9 复核修正：遍历性证据的替换与未通过项补记】**【数值】：重跑 `_m1_boltzmann.py` 与新建 `_m1_ergodicity_proper.py`（EG-1…EG-3）：
- **① 原证据不是遍历性检验**：原「遍历性（前后两半时间平均偏差 <0.2%）」实测为 0.00%，但**对照实验**（采样阶段关闭碰撞，系统明确非遍历）**同样给 0.00%** ⟹ 该指标对非遍历**完全不敏感**；它实际测的是**温度的平稳性/无漂移**，而 T 由能量守恒固定，故几乎恒为零。**它应改标为第 1 条（平稳性）的证据。**
- **② 改用真正的 Birkhoff 检验**（可观测 O = v²，比较 per-particle 时间平均 ⟨O_i⟩_t 的离散度随样本数 n_t 的标度；2D 麦克斯韦下单次采样相对离散度为 1）：原设置下离散度 **0.971 → 0.848 → 0.553 → 0.284 → 0.183**（n_t = 25/100/400/1600/4000）**单调下降**；冻结对照**恒为 1.012、不随 n_t 下降**。⟹ **遍历性成立**（离散度 ∝ 1/√n_t 的趋势明确，降幅小于理论值是采样相关所致）。
- ⟹ **结论对、原证据错**：第 2 条的结论保留，证据替换为上述 Birkhoff 检验。
- **③ 诚实补记未通过项**（原稿未列）：**确定性硬球（A 段）**速度分布加权偏差 **22.74%**（原稿记 ~18%），**总体判定为「未完全收敛」**（判据 <10% 未过）；**参数扫描（C 段）**中 v0=2.0/N=1000 与 v0=1.0/N=500 两项偏差 **13.6% / 20.7%**，**未通过**判据。**事件流 DSMC（B 段）**全部通过（温度 0.00%、分布 7.02%、ΔH = −2.266、Birkhoff 检验通过）——本命题链的核心支撑来自 B 段。
"""

EN_NEW = """**Numerical simulation verification**【Derivation】: detailed-balance Markov chain converges to the Boltzmann distribution (deviation 2.12%).

**【v2.9 audit correction: replacing the ergodicity evidence and recording the failed cases】**【Numerical】: re-running `_m1_boltzmann.py` and the new `_m1_ergodicity_proper.py` (EG-1…EG-3):
- **① The original evidence is not an ergodicity test**: the reported "ergodicity (first/second-half time averages differ <0.2%)" measures 0.00%, but a **control experiment** (collisions switched off during sampling, i.e. manifestly non-ergodic) **also gives 0.00%** ⟹ the indicator is **completely insensitive to non-ergodicity**. It actually tests **stationarity/absence of drift of the temperature**, and since T is fixed by energy conservation it is nearly identically zero. **It should be relabelled as evidence for item 1 (stationarity).**
- **② A genuine Birkhoff test** is used instead (observable O = v²; compare the spread of the per-particle time averages ⟨O_i⟩_t as a function of sample number n_t; for the 2D Maxwellian the single-sample relative spread is 1): in the original setting the spread **decreases monotonically, 0.971 → 0.848 → 0.553 → 0.284 → 0.183** (n_t = 25/100/400/1600/4000), whereas the frozen control **stays at 1.012 and does not decrease with n_t**. ⟹ **Ergodicity holds** (the ∝1/√n_t trend is clear; the decrease is slower than the ideal value because of sampling correlations).
- ⟹ **The conclusion is right, the original evidence was wrong**: item 2's conclusion is retained, with the Birkhoff test above as its evidence.
- **③ Honest record of failed cases (not listed before)**: **deterministic hard disks (run A)** give a weighted distribution deviation of **22.74%** (the draft noted ~18%) and an **overall verdict of "not fully converged"** (the <10% criterion is not met); in the **parameter scan (run C)**, v0=2.0/N=1000 and v0=1.0/N=500 give **13.6% / 20.7%**, **failing** the criterion. The **event-flow DSMC (run B)** passes everything (temperature 0.00%, distribution 7.02%, ΔH = −2.266, Birkhoff test passed) — the core support for this proposition chain comes from run B.
"""

jobs = [
    (os.path.join(HERE, "论文初稿_正反物质对风暴统一框架_v2.9.md"),
     "**数值模拟验证**【推导】：细致平衡马尔可夫链收敛到玻尔兹曼分布（偏差 2.12%）；遍历性（前后两半时间平均偏差 <0.2%）。",
     ZH_NEW),
    (os.path.join(HERE, "Paper_MatterAntimatterPairStorm_v2.9_EN.md"),
     "**Numerical simulation verification**【Derivation】: detailed-balance Markov chain converges to the Boltzmann distribution (deviation 2.12%); ergodicity (first/second-half time averages differ <0.2%).",
     EN_NEW),
]

HIST = os.path.join(ROOT, "MAPS-Unified-Framework", "paper", "history")
os.makedirs(HIST, exist_ok=True)
for p, _, _ in jobs:
    b = os.path.join(HIST, os.path.basename(p).replace(".md", "_备份_2026-09-18ergod前.md"))
    open(b, "w", encoding="utf-8").write(open(p, encoding="utf-8").read())
    print("  备份 →", os.path.basename(b))

for p, old, new in jobs:
    print("\n" + "=" * 70 + "\n" + os.path.basename(p) + "\n" + "=" * 70)
    rep(p, "遍历性证据替换 + 未通过项补记", old, new)

print("\n完成 %d 项" % len(OUT))
for o in OUT:
    print("  ·", o)
print("失败：%s" % ("；".join(FAIL) if FAIL else "无"))
