# -*- coding: utf-8 -*-
"""论文重量与可发表区间评估 md → HTML（复用论文 CSS 视觉框架）"""
import re, markdown, pathlib

BASE = pathlib.Path(r"[OLD_WORKSPACE]/outputs")
MD = BASE / "论文重量与可发表区间评估.md"
OUT = BASE / "论文重量与可发表区间评估.html"
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
  <p>评估报告 · 2026-08-24 · 基于论文 v1.36 全量盘点 · 诚实外部视角（不评判理论对错，只评估学术共同体重量与发表路径）</p>
  <div class="tags">
    <span class="tag">六维评分</span>
    <span class="tag">L0–L4 发表区间</span>
    <span class="tag">三条可执行路径</span>
    <span class="tag">诚实定位</span>
  </div>
</div>

{content}

<div class="footer">论文重量与可发表区间评估 · v1.36 基准 · 2026-08-24 · 建议：L0 预印本先行 + 3 篇单点拆分</div>

</div>
</body>
</html>
"""
OUT.write_text(html, encoding="utf-8")
print(f"OK -> {OUT} ({OUT.stat().st_size} bytes)")
