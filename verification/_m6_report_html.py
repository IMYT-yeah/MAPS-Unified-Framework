# -*- coding: utf-8 -*-
"""第三方审稿意见 md → HTML（清爽样式）"""
import re, markdown, pathlib

BASE = pathlib.Path(r"[OLD_WORKSPACE]/outputs")
MD = BASE / "M6补强报告.md"
OUT = BASE / "M6补强报告.html"

text = MD.read_text(encoding="utf-8")
m = re.search(r"^# (.+)$", text, re.M)
title = m.group(1).strip()
body = "\n".join(text.split("\n")[1:])
md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
content = md.convert(body)

CSS = """
:root{--bg:#f4f6fa;--card:#fff;--ink:#22303f;--sub:#60708a;--line:#e4e9f2;
--accent:#2f6fed;--accent-soft:#edf3ff;--gold:#b8860b;--gold-soft:#fdf7e6;
--radius:14px;--shadow:0 1px 3px rgba(30,50,90,.06),0 4px 16px rgba(30,50,90,.05)}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:-apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.9;font-size:16px;padding:28px 16px}
.wrap{max-width:1000px;margin:0 auto}
.hero{background:linear-gradient(135deg,#0e7c7c 0%,#2f6fed 55%,#6c3fb5 100%);border-radius:18px;padding:38px 42px;color:#fff;margin-bottom:28px;box-shadow:0 8px 30px rgba(47,111,237,.25)}
.hero h1{font-size:26px;line-height:1.4;margin-bottom:12px}
.hero p{opacity:.92;font-size:13.5px;line-height:1.8}
h2{font-size:21px;margin:44px 0 16px;padding:13px 18px;background:var(--card);border:1px solid var(--line);border-left:6px solid var(--accent);border-radius:12px;box-shadow:var(--shadow);color:#17304f}
h3{font-size:17px;margin:26px 0 10px;color:#1d3a5f;padding-left:13px;border-left:4px solid var(--gold)}
p{margin:11px 0}
strong{color:#0f2a47}
ul,ol{margin:11px 0;padding-left:26px}
li{margin:6px 0}
table{width:100%;border-collapse:separate;border-spacing:0;margin:18px 0;border:1px solid var(--line);border-radius:12px;overflow:hidden;box-shadow:var(--shadow);font-size:14px}
th{background:linear-gradient(135deg,#2f6fed,#5a8df0);color:#fff;padding:10px 14px;text-align:left}
td{padding:9px 14px;border-top:1px solid var(--line);vertical-align:top}
tbody tr:nth-child(even) td{background:#f8fafd}
blockquote{background:var(--accent-soft);border-left:5px solid var(--accent);border-radius:0 10px 10px 0;padding:12px 18px;margin:14px 0;color:#3a4f6e}
hr{border:none;border-top:1.5px dashed var(--line);margin:32px 0}
.footer{text-align:center;color:var(--sub);font-size:13px;margin:40px 0;padding-top:18px;border-top:1px solid var(--line)}
@media(max-width:800px){.hero{padding:26px 22px}.hero h1{font-size:20px}}
"""

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<div class="hero">
  <h1>{title}</h1>
  <p>M6 补强执行报告 · 2026-08-24 · 配对阶数→规范群的结构筛选论证（10 候选 → 唯一幸存）</p>
</div>
{content}
<div class="footer">M6 补强 · 结构筛选 · 2026-08-24</div>
</div>
</body>
</html>
"""
OUT.write_text(html, encoding="utf-8")
print(f"OK -> {OUT} ({OUT.stat().st_size} bytes)")
