# -*- coding: utf-8 -*-
"""
第 83 轮清单补丁（v2 · 修正顺延范围）

v1 的两个错：
  ① 顺延把 1.1 也 +1 了 ⟹ 与新建的 1.2 撞车、1.1 消失（连续=False、重复=[2]）
     ✅ 正解：**只顺延 N ≥ 2**（1.1 是「最新一轮」的永久位置，不动）
  ② 总账计数用的是「**N 条**」而我的正则找「**N 项**」⟹ 静默未改（陷阱 73 家族：改前先断言）
     ✅ 正解：定位到行、逐字匹配 `| **撤回 / 更正** | **32 条**`
"""
import io
import os
import re
import shutil

BASE = "C:/Users/Administrator/Desktop/2026-08-20-21-43-34"
GL = os.path.join(BASE, "outputs", "工程期望清单.md")
BAK = os.path.join(BASE, "outputs", "工程期望清单_备份_2026-10-02第83轮前.md")
BAD = []


def sub_once(path, old, new, tag, n_expected=1):
    t = io.open(path, encoding="utf-8").read()
    n = t.count(old)
    if n != n_expected:
        print("  [XX] {:<42} 命中 {}（期望 {}）".format(tag, n, n_expected))
        BAD.append(tag)
        return
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, n_expected))
    print("  [OK] {:<42} 已改".format(tag))


def check_num(tag, strict=True):
    """⚠️ strict=False 用于**中间态**（如「已顺延、尚未插入新节」）——
    此时「缺 1.2」是**预期的**，不是失败（第 83 轮踩过：把中间态当失败报了 [XX]）。"""
    L = io.open(GL, encoding="utf-8").read().split("\n")
    nums = [int(m.group(1)) for m in (re.match(r"^### 1\.(\d+) ", s) for s in L) if m]
    ok = nums == list(range(1, len(nums) + 1))
    lvl = "OK" if ok else ("XX" if strict else "INFO")
    print("  [{}] {:<26} 1.{}–1.{}  连续={}  重复={}".format(
        lvl, tag, nums[0], nums[-1], ok,
        [x for x in set(nums) if nums.count(x) > 1] or "无"))
    if not ok and strict:
        BAD.append("编号" + tag)
    return ok


# 恢复
shutil.copy2(BAK, GL)
print("[恢复] 已从第 83 轮前备份恢复清单\n")
check_num("恢复后")

# ================================================================
print("\n[L1] 顺延（**只对 N ≥ 2**）")


def bump(m):
    n = int(m.group(1))
    return "### 1.{} ".format(n + 1 if n >= 2 else n)


t = io.open(GL, encoding="utf-8").read()
io.open(GL, "w", encoding="utf-8").write(re.sub(r"^### 1\.(\d+) ", bump, t, flags=re.M))
check_num("顺延后（中间态）", strict=False)

# ================================================================
print("\n[L2] 插入新的 1.2 节")
L = io.open(GL, encoding="utf-8").read().split("\n")
ANCHOR = next(s for s in L if s.startswith("### 1.3 "))
print("     锚点：{}".format(ANCHOR[:80]))

NEW_SEC = """### 1.2 第 83 轮（**更正 / 撤回**：第 82 轮的「(g′) 4-正则补证」**前提有误，已撤回**）

> **触发**：用户指出「某一个步骤不是证明金刚石不对吗，怎么还金刚石」——**用户是对的**。
> 核验：`_diamond_83.py`（**DM-1 … DM-8b，9 项 0 失败**）。

| 标识 | 条目 | 类型 | 诚判 | 出处 |
|---|---|---|---|---|
| **C-33** ⭐ | **把「已撤回的初稿几何」当作现行几何，并据此做「补证」** | **撤回 / 更正** | **撤回第 82 轮的 §8.6.8 (g′)**。事实链：**第 27 轮初稿**据「配位数 = 方向簇 `k = 4`」定为**金刚石**；**第 30 轮 T-6 裁决**追溯后发现该步不成立（§4.10 论证 4：正四面体 4 方向 = **内空间**；八面体 6 方向 = **外空间轴**）⟹ **撤回金刚石，定案简单立方**（配位数 **6**、二分）。**§8.6.8 的标题就写着**「外空间 6 方向 ⟹ 简单立方（**T-6 裁决，第 30 轮**）」，同一小节 (i) 段写「**金刚石结构与 §4.9 引理 1 不相容**，简单立方通过」，开头的撤回块是**该小节第一段**。⚠️ 第 82 轮却写「**第 27 轮定案的格点几何是金刚石**」——把「初稿」当「定案」，且**跳过了紧贴标题的撤回块**。⭐ **更硬的一层**：**(g) 算的 6-正则 = 简单立方 = 衬底的现行几何** ⟹ **(g) 已覆盖它**；「4-正则（配位数 4）」在**底本里 0 处**（`4-正则` / `配位数 4` 全 0）⟹ **该档没有对象** —— 不是「论文漏算」，是「**不该算**」。不等式本身无误（`m = 2n` vs 上界 `2n−4`，对一切 n 矛盾），但**框架用不上**。⚠️ **同族第 4 次**：75「缺的不是方程，是对象」／77「`g` 的精确值没有对象」／81「`8π/3` 没有对象」／**83「4-正则档没有对象」**。 | 论文 §8.6.8 (g′)（**已撤回**）｜§10.2 第 82 轮块（依据已改为 **(g)**）｜备忘录 §六更正 |
| —— | **第 82 轮「唯一正面产出」归零** | 更正 | 第 82 轮记的「唯一正面产出 = (g′) 补证」**不成立** ⟹ 第 82 轮的产出 = **只有负面（N-37）＋不覆盖登记**，**正面产出 0 条**。⚠️ **N-37（Ricci 流不覆盖）本身不撤回**（四条理由与 (g′) 无关）。 | 同上 |
| —— | **§10.2「衬底非平面」的依据** | 更正 | 由 (g′)（4-正则/金刚石）改为 **(g)**（**6-正则 = 简单立方**）⟹ 结论**不变**、理由换成对的那一个。 | 论文 §10.2（中英同步） |

**⚠️ 教训（已立为技能陷阱 75）**：**检索到某个词 ≠ 那个词描述的是「现行」状态** ——
本处在底本里「金刚石」命中 **5 处**，其中 **4 处带撤回/不相容标记**（唯一例外是 (f) 段的
「在简单立方与金刚石两种几何上独立重现」，那是**并列提及两种几何做数值对照**，不是「衬底是金刚石」）。
⟹ **规范**：凡要断言「框架的现状是 X」，先**反向检索 X 的撤回标记**（`撤回` / `作废` / `withdrawn` /
`incompatible` / `不成立`），并**读该词所在小节的标题**（本处标题直接写着「简单立方（T-6 裁决，第 30 轮）」）。

**总账**：**更正 32 → 33**（＋C-33）；负面 **37 条不变**（N-37 不撤回）；难题条数不变。

"""
sub_once(GL, ANCHOR, NEW_SEC + ANCHOR, "插入 1.2 节")
check_num("插入 1.2 后")

# ================================================================
print("\n[L3] 更正现 1.3 节（原 1.2，第 82 轮）")
sub_once(GL,
         "### 1.3 第 82 轮新增（**庞加莱猜想 ＋ Ricci 流 的接入审查：四处对不上；顺带补证 4-正则（金刚石）非平面**）",
         "### 1.3 第 82 轮新增（**庞加莱猜想 ＋ Ricci 流 的接入审查：四处对不上**）⚠️ **第 83 轮更正：其中『顺带补证 4-正则（金刚石）非平面』前提有误，已撤回（C-33）**",
         "1.3 节标题更正")

t = io.open(GL, encoding="utf-8").read()
L = t.split("\n")
k = next(i for i, s in enumerate(L) if s.startswith("| **§8.6.8 (g′) ✅**"))
REPL = ("| ~~**§8.6.8 (g′) ✅ 4-正则二分图（金刚石）非平面**~~ | ~~本轮补证（论文缺的那一档）~~ | "
        "**❌ 第 83 轮撤回（C-33）** | **前提有误**：第 27 轮的「金刚石」是**初稿**，**第 30 轮 T-6 裁决已撤回**，定案为**简单立方（配位数 6）**；"
        "而 **(g) 算的 6-正则 = 简单立方 = 现行几何** ⟹ **(g) 已覆盖**；「4-正则（配位数 4）」在底本里 **0 处** ⟹ **该档没有对象**。"
        "不等式本身无误，但**框架用不上**。 | 论文 §8.6.8 (g′) 撤回块 |")
t = t.replace(L[k], REPL, 1)
io.open(GL, "w", encoding="utf-8").write(t)
print("  [OK] 1.3 节的 (g′) 条目已改为撤回记录（原 L{}）".format(k + 1))

# ================================================================
print("\n[L4] 总账：插入 C-33 ＋ 计数 32 → 33")
t = io.open(GL, encoding="utf-8").read()
L = t.split("\n")
row = next(i for i, s in enumerate(L) if s.startswith("| **撤回 / 更正**"))
print("     行 L{}，前 90 字符：{}".format(row + 1, L[row][:90]))
INS = ("**C-33 ⭐ 把「已撤回的初稿几何」当现行几何并据此补证**（第 83 轮：第 27 轮金刚石**第 30 轮 T-6 已撤回**"
       "⟹定案简单立方；**4-正则档没有对象**）｜")
j = L[row].rstrip().rfind("|")
L[row] = L[row][:j] + INS + " " + L[row][j:]
# 计数：逐字匹配
t2 = "\n".join(L)
old_cnt = "| **撤回 / 更正** | **32 条**"
new_cnt = "| **撤回 / 更正** | **33 条**"
assert t2.count(old_cnt) == 1, t2.count(old_cnt)
t2 = t2.replace(old_cnt, new_cnt, 1)
io.open(GL, "w", encoding="utf-8").write(t2)
print("  [OK] 总账行已插入 C-33，计数 **32 条 → 33 条**")
print("     行尾核对：{}".format(t2.split("\n")[row][-150:]))

# ================================================================
print("\n[L5] 结构自检")
check_num("最终")
L = io.open(GL, encoding="utf-8").read().split("\n")
bad = [i + 1 for i, x in enumerate(L) if x.lstrip().startswith("|") and not x.rstrip().endswith("|")]
print("  表格首尾不成对：{}".format(bad if bad else "无 ✓"))
print("  C-33 出现 {} 处；总账行含「**33 条**」= {}".format(
    sum(1 for s in L if "C-33" in s), any("**33 条**" in s and s.startswith("| **撤回 / 更正**") for s in L)))
print("\n失败项：{}".format(BAD if BAD else "无 ✓"))
