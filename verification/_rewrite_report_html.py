# -*- coding: utf-8 -*-
"""论文重量与可发表区间评估 md → HTML（复用论文 CSS 视觉框架）"""
import re, markdown, pathlib

BASE = pathlib.Path(r"[OLD_WORKSPACE]/outputs")
MD = BASE / "原文标注改写策略.md"
OUT = BASE / "原文标注改写策略.html"
OLD_HTML = BASE / "论文初稿_正反物质对风暴统一框架.html"

text = MD.read_text(encoding="utf-8")
m = re.search(r"^# (.+)$", text, re.M)
title = m.group(1).strip() if m else "论文重量与可发表区间评估"
lines = text.split("\n")
body = "\n".join(lines[1:]) if len(lines) > 1 else text
body = re.sub(r"\$\$([\s\S]+?)\$\$",
              lambda mm: '<div class="formula">' + mm.group(1).strip() + '</div>', body)
body = re.sub(r"\$([^$\n]+?)\$",
              lambda mm: '<span class="math">' + mm.group(1).strip() + '</span>', body)
md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
content = md.convert(body)

old_html = OLD_HTML.read_text(encoding="utf-8") if OLD_HTML.exists() else ""
style_m = re.search(r"<style>[\s\S]*?</style>", old_html)
css = style_m.group(0) if style_m else "<style>body{font-family:sans-serif;max-width:900px;margin:auto;padding:2em}</style>"

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
{css}
</head>
<body>
<div class="wrap">

<div class="hero">
  <div class="en">Assessment: Weight &amp; Publishable Range — Matter–Antimatter Pair Storm Framework (v1.36)</div>
  <h1>{title}</h1>
  <p>策略报告 · 2026-08-24 · 论文 v1.36 全量 59 处【原文】引用盘点 · 发表前置条件第一项</p>
  <div class="tags">
    <span class="tag">分类映射表</span>
    <span class="tag">三原则改写</span>
    <span class="tag">披露声明模板</span>
    <span class="tag">三阶段执行计划</span>
  </div>
</div>

{content}

<div class="footer">【原文】标注改写策略 · v1.36 基准 · 2026-08-24 · 致命障碍解除 → 可进入英文翻译与 arXiv 投稿</div>

</div>
</body>
</html>
"""
OUT.write_text(html, encoding="utf-8")
print(f"OK -> {OUT} ({OUT.stat().st_size} bytes)")
