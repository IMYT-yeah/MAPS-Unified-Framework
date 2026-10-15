# 中国科技论文在线（paper.edu.cn）投稿包

**论文**：正反物质对风暴：一个统一四种基本力的涌现统计框架（v2.8 中文版）
**生成日期**：2026-08-24

---

## 包内容

| 文件 | 说明 |
|---|---|
| `main_cso.pdf` | **最终成品 PDF（43 页，可直接上传投稿）** |
| `main_cso.tex` | LaTeX 源码（csoarticle 格式） |
| `csoarticle.cls` | 官方模板类（已修复：GBK→UTF-8、去除 hyperref、字体改为 fontset=windows） |
| `cso-utf8.def` | 官方模板标头定义（UTF-8 版） |
| `csologo.pdf` | 页眉 logo（paper.edu.cn） |

---

## ⚠️ 编码版本选择（若平台提示"tex文件编码不正确，应为UTF8"）

本目录提供**两个 zip 包**，内容相同、仅编码格式不同：

| 包 | 编码 | 适用场景 |
|---|---|---|
| `CSO_submission_UTF8_BOM.zip` | **UTF-8 带 BOM**（推荐先试） | 平台按"有无 BOM"判断编码（记事本另存为 UTF-8 即此格式） |
| `CSO_submission_UTF8.zip` | UTF-8 无 BOM（标准） | 平台按严格 UTF-8 校验 |

- 若平台报编码错误，**优先上传 `CSO_submission_UTF8_BOM.zip`**。
- 包内 `main_cso.tex` 头部已含 `% !TEX encoding = UTF-8 Unicode` 声明，`\documentclass[UTF8,fontset=windows]` 已带 UTF8 选项。
- 若两个 zip 均被拒，请把平台报错原文/截图发回，以便进一步定位。

---

## 已按 CSO 格式整理的标头

- **中文标题**：正反物质对风暴：一个统一四种基本力的涌现统计框架
- **英文标题**：Matter–Antimatter Pair Storm: An Emergent Statistical Framework for the Unification of Fundamental Forces
- **作者**：`AUTHOR NAME`（占位，需替换为真实姓名）
- **单位**：占位（作者单位，城市　邮编）
- **中文摘要**：已从论文摘要提取（含公式转换）
- **英文摘要**：已从英文版 Abstract 提取
- **中文关键词**：正反物质对风暴；涌现统计框架；四种基本力统一；量子引力；引力涌现；弦网
- **英文关键词**：matter–antimatter pair storm; emergent statistical framework; unification of fundamental forces; quantum gravity; emergent gravity; string-net
- **中图分类号**：`O412`（相对论、引力理论，请按需核对）
- **作者简介**：占位
- **基金项目**：占位

正文已使用 csoarticle 的 `\section`/`\subsection` 自动编号（标题中手动数字已剥离），公式/表格/参考文献全部适配。

---

## 提交前必须替换的占位信息（编辑 main_cso.tex）

```latex
\authorCHN{真实姓名\affil{1}}
\authorENG{真实姓名拼音\affil{1}}
\affiliationCHN{ \affil{1} 单位名称，城市　邮编 }
\affiliationENG{ \affil{1} Affiliation, City 000000 }
\authorIntroduction{姓名（出生年-），性别，职称，主要研究方向：***。}
\fund{基金名称（编号）}
\cateidCHN{O412}   % 如需修改请查阅《中国图书馆分类法》
```

---

## 本地重新编译（验证用）

需要 `xelatex`（TeX Live 含 ctex）或 tectonic，且系统有中文字体（宋体/黑体，Windows 自带）。

```
xelatex main_cso.tex
```

注：随包的 `csoarticle.cls` 是**修复版**（原模板为 GBK 编码且依赖旧 hyperref/winfonts 接口，在现行 TeX 环境下无法编译；修复仅涉及编码与字体选项，版面不变）。若投稿平台要求使用其自带的官方模板，请以平台版本为准，并将 `main_cso.tex` 的正文移植过去。

---

## 投稿注意事项

- paper.edu.cn 接受 PDF 上传，`main_cso.pdf` 可直接提交。
- 摘要字数：CSO 建议 200–400 字，当前摘要为全文摘录（较长），如平台校验不通过可在投稿页精简。
- 参考文献格式：CSO 要求 GB/T 7714 风格（[J]/[M] 等标识）。当前 30 条为简略格式，投稿前建议按 CSO 要求规范化（作者姓大写、卷期页码、[J] 标注）。
- 文献数量：CSO 要求不少于 6 篇（当前 30 篇满足）；综述文章需 25+。
