# -*- coding: utf-8 -*-
"""将 论文初稿 md 转为完整版 HTML（复用旧 HTML 的 CSS 视觉框架）。"""
import re, markdown, pathlib

BASE = pathlib.Path(r"D:/Users/IMYT.YT/WorkBuddy/2026-08-20-21-43-34/outputs")
MD = BASE / "论文初稿_正反物质对风暴统一框架.md"
OLD_HTML = BASE / "论文初稿_正反物质对风暴统一框架.html"
OUT = BASE / "论文初稿_正反物质对风暴统一框架_v1.36.html"

text = MD.read_text(encoding="utf-8")

# 提取标题
m = re.search(r"^# (.+)$", text, re.M)
zh_title = m.group(1).strip() if m else "正反物质对风暴：统一四种基本力的涌现统计框架"
m = re.search(r"^## (.+)$", text, re.M)
en_title = m.group(1).strip() if m else ""

# 去掉 md 前两行标题（# 与 ##），正文从其后开始
lines = text.split("\n")
body = "\n".join(lines[3:]) if len(lines) > 3 else text

# 数学公式预处理：块级 $$...$$ -> <div class="formula">；行内 $...$ -> <span class="math">
body = re.sub(r"\$\$([\s\S]+?)\$\$",
              lambda mm: '<div class="formula">' + mm.group(1).strip() + '</div>', body)
body = re.sub(r"\$([^$\n]+?)\$",
              lambda mm: '<span class="math">' + mm.group(1).strip() + '</span>', body)

md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
content = md.convert(body)

# 从旧 HTML 提取 <style>
old_html = OLD_HTML.read_text(encoding="utf-8") if OLD_HTML.exists() else ""
style_m = re.search(r"<style>[\s\S]*?</style>", old_html)
css = style_m.group(0) if style_m else ""

tags = [
    "四条公理", "引力 = 通量场统计力学涌现（γ=β=1）",
    "规范 = 量子双代数涌现（v1.19）", "禁闭弦张力数值实现（v1.20）",
    "过载区均匀浆糊 + 光学透明（v1.25）",
    "指数度规 + 阴影 EHT 相容（v1.21）", "方向离散化 + Bekenstein 上界（v1.21）",
    "框架哈密顿量 H_F = −ΣA_v − ΣB_p", "弦网 3+1D 路线（四力=弦网序）", "S=A/4 packing 定理包",
    "P1 系列：弦网低能谱 + EMRI 修正 + λ_c + RG（v1.34–1.36）",
]
tags_html = "\n".join(f'    <span class="tag">{t}</span>' for t in tags)

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{zh_title}（v1.36）</title>
{css}
</head>
<body>
<div class="wrap">

<div class="hero">
  <div class="en">{en_title}</div>
  <h1>{zh_title}</h1>
  <p>论文初稿 v1.36（完整版）· 2026-08-24 · 启发式统一框架（参考架构，非已确立物理）</p>
  <div class="tags">
{tags_html}
  </div>
</div>

{content}

<div class="footer">论文初稿 v1.36 · P1 系列整合（弦网低能谱 + EMRI a-δ 修正 + λ_c 相变 + Wilson RG）· 2026-08-24</div>

</div>
</body>
</html>
"""

OUT.write_text(html, encoding="utf-8")
print(f"OK -> {OUT}  ({len(html)} bytes)")
