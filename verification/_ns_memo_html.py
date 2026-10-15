# -*- coding: utf-8 -*-
import re, markdown, pathlib
BASE = pathlib.Path(r"D:/Users/IMYT.YT/WorkBuddy/2026-08-20-21-43-34/outputs")
MD = BASE / "NS奇点启发与框架对照.md"
OUT = BASE / "NS奇点启发与框架对照.html"
text = MD.read_text(encoding="utf-8")
m = re.search(r"^# (.+)$", text, re.M)
title = m.group(1).strip()
md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
content = md.convert("\n".join(text.split("\n")[1:]))
css = re.search(r'CSS = """(.*?)"""', open("_c1_report_html.py", encoding="utf-8").read(), re.S).group(1)
html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><style>{css}</style></head>
<body><div class="page"><h1>{title}</h1>{content}</div></body></html>"""
OUT.write_text(html, encoding="utf-8")
print(f"OK -> {OUT.name} ({OUT.stat().st_size} bytes)")
