# -*- coding: utf-8 -*-
"""C1 湮灭损失率三通道统一报告 md → HTML（与 A2/A3 报告同款样式）"""
import re, markdown, pathlib

BASE = pathlib.Path(r"[OLD_WORKSPACE]/outputs")
MD = BASE / "C1_湮灭损失率三通道统一.md"
OUT = BASE / "C1_湮灭损失率三通道统一.html"

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
body{background:var(--bg);color:var(--ink);font:15px/1.75 -apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}
.page{max-width:980px;margin:0 auto;padding:36px 20px 80px}
h1{font-size:26px;line-height:1.45;padding:22px 26px;background:linear-gradient(135deg,#fff,#f2f7ff);
border:1px solid var(--line);border-left:5px solid var(--accent);border-radius:var(--radius);
box-shadow:var(--shadow);margin:0 0 14px}
h2{font-size:20px;margin:34px 0 12px;padding:10px 14px;background:var(--accent-soft);
border-radius:10px;border-left:4px solid var(--accent)}
h3{font-size:17px;margin:24px 0 8px;color:var(--accent)}
p{margin:10px 0}
blockquote{margin:12px 0;padding:10px 16px;background:#f8fafc;border-left:4px solid var(--gold);
border-radius:8px;color:var(--sub)}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:14px;background:#fff;
border-radius:10px;overflow:hidden;box-shadow:var(--shadow)}
th{background:#eef3fb;color:#33445c;padding:9px 12px;text-align:left;border-bottom:2px solid var(--line)}
td{padding:8px 12px;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:none}
tr:hover td{background:#fafcff}
code{background:#eef1f6;padding:1px 6px;border-radius:5px;font-size:13px;font-family:Consolas,monospace}
pre{background:#1e2936;color:#e2e8f0;padding:14px 16px;border-radius:10px;overflow-x:auto;margin:12px 0}
pre code{background:none;color:inherit;padding:0}
strong{color:#1a2b40}
hr{border:none;border-top:1px solid var(--line);margin:26px 0}
"""

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<div class="page">
<h1>{title}</h1>
{content}
</div>
</body>
</html>"""

OUT.write_text(html, encoding="utf-8")
print(f"OK -> {OUT} ({OUT.stat().st_size} bytes)")
