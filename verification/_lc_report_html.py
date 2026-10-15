# -*- coding: utf-8 -*-
"""3+1D 弦网严格化报告 md → HTML"""
import re, markdown, pathlib

BASE = pathlib.Path(r"D:/Users/IMYT.YT/WorkBuddy/2026-08-20-21-43-34/outputs")
MD = BASE / "3+1D弦网λc相变.md"
OUT = BASE / "3+1D弦网λc相变.html"

text = MD.read_text(encoding="utf-8")
m = re.search(r"^# (.+)$", text, re.M)
title = m.group(1).strip()
body = "\n".join(text.split("\n")[3:]) if len(text.split("\n")) > 3 else text

body = re.sub(r"\$\$([\s\S]+?)\$\$",
              lambda mm: '<div class="formula">' + mm.group(1).strip() + '</div>', body)
body = re.sub(r"\$([^$\n]+?)\$",
              lambda mm: '<span class="math">' + mm.group(1).strip() + '</span>', body)

md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
content = md.convert(body)

tags = ["⟨A_c⟩ 光滑 S 形（1→0）", "E0=−N_c · 简并 2^(n−N_c) · Δ=2", "λ_c≈0.14 vs 2D toric code 0.25–0.32",
        "对偶 3D Ising β_c=0.2217 同量级", "Δ±2=Δ_vec > Δ_scalar（张量/矢量重 19%）", "原文 54-55 相变 = 通量冷凝点"]
tags_html = "\n".join(f'    <span class="tag">{t}</span>' for t in tags)

css = """
  :root{
    --bg:#f7f8fa; --card:#fff; --ink:#1f2329; --sub:#57606a; --line:#e4e6eb;
    --accent:#2f6fed; --accent-bg:#eaf1fe; --gold:#b8860b; --gold-bg:#fdf6e3;
    --green:#0a7d3c; --green-bg:#e8f7ee; --red:#c0392b; --red-bg:#fdecea;
    --purple:#6c3fb5; --purple-bg:#f1ebfa; --teal:#0e7c7c; --teal-bg:#e6f6f6;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--ink);font-family:"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.75;padding:32px 16px}
  .wrap{max-width:1080px;margin:0 auto}
  .hero{background:linear-gradient(135deg,#6c3fb5 0%,#0e7c7c 55%,#2f6fed 100%);border-radius:16px;padding:38px 42px;color:#fff;margin-bottom:26px}
  .hero h1{font-size:25px;font-weight:700;line-height:1.5;margin-bottom:12px}
  .hero p{opacity:.92;font-size:14px}
  .hero .tags{margin-top:14px}
  .hero .tag{display:inline-block;background:rgba(255,255,255,.16);border-radius:20px;padding:3px 14px;font-size:12.5px;margin:4px 8px 0 0}
  h2{font-size:21px;margin:38px 0 14px;padding-left:12px;border-left:5px solid var(--accent)}
  h3{font-size:16.5px;margin:18px 0 10px;color:#2f3b4d}
  p{margin:10px 0;font-size:14.5px}
  blockquote{background:var(--accent-bg);border-left:4px solid var(--accent);border-radius:0 8px 8px 0;padding:12px 18px;margin:12px 0;color:#33465f;font-size:14px}
  table{width:100%;border-collapse:collapse;margin:12px 0;font-size:13.5px;background:#fff;border-radius:8px;overflow:hidden}
  th{background:#eef2f8;font-weight:600;text-align:left;padding:9px 12px;border-bottom:2px solid var(--line)}
  td{padding:8px 12px;border-bottom:1px solid var(--line);vertical-align:top}
  tr:last-child td{border-bottom:none}
  .formula{background:#f8faff;border:1px dashed #b9cdf5;border-radius:10px;padding:14px 20px;margin:14px 0;text-align:center;font-size:16px;color:#1c3d7a;font-family:"Cambria Math","Times New Roman",serif}
  .math{font-family:"Cambria Math","Times New Roman",serif;color:#1c3d7a}
  .footer{text-align:center;color:var(--sub);font-size:13px;margin:42px 0 10px}
  @media(max-width:640px){.hero{padding:24px 18px}.hero h1{font-size:20px}.wrap{padding:0}}
"""

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<div class="wrap">

<div class="hero">
  <h1>{title}</h1>
  <p>P1-3 执行报告 · 2026-08-23 · C1 凝聚相稳定性边界</p>
  <div class="tags">
{tags_html}
  </div>
</div>

{content}

<div class="footer">3+1D弦网λc相变 · 2026-08-23 · χ 峰锁定 λ_χ=0.140（四尺寸）· 伪临界定位</div>

</div>
</body>
</html>
"""

OUT.write_text(html, encoding="utf-8")
print(f"OK -> {OUT} ({len(html)} bytes)")
