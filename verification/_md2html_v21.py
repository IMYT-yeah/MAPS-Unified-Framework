# -*- coding: utf-8 -*-
"""v2.1 发表版 HTML 生成器 — 清爽界面 + 静态数学公式渲染（无 JS/CDN 依赖）
LaTeX 公式在生成阶段静态转换为 HTML 数学排版（分式/根号/上下标/希腊字母），
任何浏览器离线均可显示为人类语言公式。"""
import re, markdown, pathlib

BASE = pathlib.Path(r"[OLD_WORKSPACE]/outputs")
MD = BASE / "论文初稿_正反物质对风暴统一框架_v2.8.md"
OUT = BASE / "论文初稿_正反物质对风暴统一框架_v2.8.html"

# ================= 静态 LaTeX → HTML 数学转换器 =================

_GREEK = {
    'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε',
    'varepsilon': 'ε', 'theta': 'θ', 'vartheta': 'ϑ', 'lambda': 'λ', 'mu': 'μ',
    'nu': 'ν', 'rho': 'ρ', 'sigma': 'σ', 'tau': 'τ', 'phi': 'φ', 'varphi': 'ϕ',
    'Phi': 'Φ', 'chi': 'χ', 'psi': 'ψ', 'omega': 'ω', 'Omega': 'Ω', 'Gamma': 'Γ',
    'pi': 'π', 'xi': 'ξ', 'zeta': 'ζ', 'eta': 'η', 'kappa': 'κ', 'ell': 'ℓ',
    'Delta': 'Δ', 'Lambda': 'Λ', 'Sigma': 'Σ', 'Pi': 'Π', 'Theta': 'Θ', 'Xi': 'Ξ',
    'hbar': 'ℏ', 'partial': '∂', 'nabla': '∇', 'infty': '∞',
}

_SYM = {
    'cdot': '·', 'times': '×', 'approx': '≈', 'leq': '≤', 'geq': '≥',
    'to': '→', 'rightarrow': '→', 'longrightarrow': '→', 'Longrightarrow': '⟹',
    'Rightarrow': '⇒', 'leftarrow': '←', 'longleftarrow': '←',
    'Longleftarrow': '⟸', 'Leftarrow': '⇐', 'leftrightarrow': '↔',
    'leftrightarrow': '↔', 'Leftrightarrow': '⇔', 'mapsto': '↦', 'longmapsto': '⟼',
    'cdots': '⋯', 'ldots': '…', 'pm': '±', 'mp': '∓', 'neq': '≠',
    'equiv': '≡', 'sim': '∼', 'simeq': '≃', 'propto': '∝', 'in': '∈',
    'ni': '∋', 'subset': '⊂', 'supset': '⊃', 'cup': '∪', 'cap': '∩',
    'forall': '∀', 'exists': '∃', 'neg': '¬', 'wedge': '∧', 'vee': '∨',
    'oplus': '⊕', 'otimes': '⊗', 'prime': '′', 'circ': '∘', 'bullet': '•',
    'int': '∫', 'oint': '∮', 'sum': '∑', 'prod': '∏', 'quad': ' ', 'qquad': '  ',
    'quad ': ' ', ';': ' ', ':': ' ', '!': '',
}

_FN = {'sin', 'cos', 'tan', 'csc', 'sec', 'cot', 'arcsin', 'arccos', 'arctan',
       'ln', 'log', 'exp', 'det', 'dim', 'max', 'min', 'sup', 'inf'}


def _find_group(s, i):
    """s[i]=='{' → (内部内容, 结束索引+1)；支持嵌套花括号"""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == '{':
            depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
    return s[i + 1:], len(s)


def _conv_short(s):
    """单 token 转换（用于 ^x / _x 的单字符参数，支持 \\command 形式）"""
    if s.startswith('\\'):
        m = re.match(r'\\[a-zA-Z]+', s)
        if m:
            return _conv(m.group(0))
        return _conv(s[:2]) if len(s) >= 2 else ''
    return _conv(s[0])


def _conv(s):
    """递归转换 LaTeX 片段 → HTML（上标/下标/分式/根号/符号映射）"""
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == '\\':
            m = re.match(r'\\[a-zA-Z]+', s[i:])
            if m:
                cmd, j = m.group(0)[1:], i + len(m.group(0))
                # ---- \frac / \tfrac / \dfrac ----
                if cmd in ('frac', 'dfrac', 'tfrac'):
                    # TeX 简写 \frac12 = \frac{1}{2}、\tfrac12
                    if j < n and s[j].isdigit():
                        num = s[j]
                        if j + 1 < n and s[j + 1].isdigit():
                            den, i = s[j + 1], j + 2
                        else:
                            den, i = '2', j + 1
                        out.append(f'<span class="frac"><span class="num">{num}</span>'
                                   f'<span class="den">{den}</span></span>')
                        continue
                    if j < n and s[j] == '{':
                        a, j2 = _find_group(s, j)
                        if j2 < n and s[j2] == '{':
                            b, j3 = _find_group(s, j2)
                            out.append(f'<span class="frac"><span class="num">{_conv(a)}</span>'
                                       f'<span class="den">{_conv(b)}</span></span>')
                            i = j3
                            continue
                # ---- \sqrt ----
                if cmd == 'sqrt' and j < n and s[j] == '{':
                    a, j2 = _find_group(s, j)
                    out.append(f'<span class="sqrt">√<span class="radicand">{_conv(a)}</span></span>')
                    i = j2
                    continue
                # ---- \text / \mathrm / \operatorname / \mathcal / \mathbf ----
                if cmd in ('text', 'mathrm', 'operatorname', 'mbox', 'textrm'):
                    if j < n and s[j] == '{':
                        a, j2 = _find_group(s, j)
                        out.append(f'<span class="{ "txt" if cmd == "text" else "rm" }">{a}</span>')
                        i = j2
                        continue
                if cmd in ('mathcal', 'mathbf', 'mathbb', 'mathscr', 'mathfrak'):
                    if j < n and s[j] == '{':
                        a, j2 = _find_group(s, j)
                        cls = {'mathcal': 'cal', 'mathbf': 'bf', 'mathbb': 'bb',
                               'mathscr': 'cal', 'mathfrak': 'frak'}[cmd]
                        out.append(f'<span class="{cls}">{a}</span>')
                        i = j2
                        continue
                # ---- \bar / \hat / \tilde / \vec ----
                if cmd in ('bar', 'hat', 'tilde', 'vec', 'dot', 'ddot'):
                    acc = {'bar': '̄', 'hat': '̂', 'tilde': '̃', 'vec': '⃗',
                           'dot': '̇', 'ddot': '̈'}[cmd]
                    if j < n and s[j] == '{':
                        a, j2 = _find_group(s, j)
                        out.append(f'<span class="acc">{_conv(a)}{acc}</span>')
                        i = j2
                        continue
                    elif j < n:
                        # \bar\psi 形式：取单个 token（含 \command）
                        if s[j] == '\\':
                            m2 = re.match(r'\\[a-zA-Z]+', s[j:])
                            if m2:
                                out.append(f'<span class="acc">{_conv(m2.group(0))}{acc}</span>')
                                i = j + len(m2.group(0))
                                continue
                        out.append(f'<span class="acc">{s[j]}{acc}</span>')
                        i = j + 1
                        continue
                # ---- 括号修饰 \left( \right) \big( 等 ----
                if cmd in ('left', 'right', 'big', 'Big', 'bigg', 'Bigg',
                           'bigl', 'bigr', 'Bigl', 'Bigr'):
                    if j < n and s[j] in '()[]|.':
                        ch = {'(': '(', ')': ')', '[': '[', ']': ']', '|': '|', '.': ''}[s[j]]
                        out.append(ch)
                        i = j + 1
                        continue
                # ---- 符号 ----
                if cmd in _SYM:
                    out.append(_SYM[cmd])
                    i = j
                    continue
                # ---- 希腊字母 ----
                if cmd in _GREEK:
                    out.append(_GREEK[cmd])
                    i = j
                    continue
                # ---- 函数名 ----
                if cmd in _FN:
                    out.append(f'<span class="fn">{cmd}</span>')
                    i = j
                    continue
                # ---- 未知命令：仅输出命令文本 ----
                out.append(cmd)
                i = j
                continue
            else:
                # 非字母转义：\\{ \\} \\_ \\% \\, \\; \\! 等
                nxt = s[i + 1] if i + 1 < n else ''
                if nxt == '!':            # \! 负细空格 → 空
                    pass
                elif nxt in ',;:':        # \, \; \: 窄空格
                    out.append(' ')
                elif nxt == '\\':         # \\ 换行符 → 空格
                    out.append(' ')
                else:
                    out.append(nxt)
                i += 2
                continue
        elif c == '^':
            if i + 1 < n and s[i + 1] == '{':
                a, j2 = _find_group(s, i + 1)
                out.append(f'<sup>{_conv(a)}</sup>')
                i = j2
            elif i + 1 < n:
                if s[i + 1] == '\\':
                    m2 = re.match(r'\\[a-zA-Z]+', s[i + 1:])
                    if m2:
                        out.append(f'<sup>{_conv(m2.group(0))}</sup>')
                        i += 1 + len(m2.group(0))
                        continue
                out.append(f'<sup>{_conv_short(s[i + 1])}</sup>')
                i += 2
            else:
                i += 1
        elif c == '_':
            if i + 1 < n and s[i + 1] == '{':
                a, j2 = _find_group(s, i + 1)
                out.append(f'<sub>{_conv(a)}</sub>')
                i = j2
            elif i + 1 < n:
                if s[i + 1] == '\\':
                    m2 = re.match(r'\\[a-zA-Z]+', s[i + 1:])
                    if m2:
                        out.append(f'<sub>{_conv(m2.group(0))}</sub>')
                        i += 1 + len(m2.group(0))
                        continue
                out.append(f'<sub>{_conv_short(s[i + 1])}</sub>')
                i += 2
            else:
                i += 1
        elif c == '{':
            a, j2 = _find_group(s, i)
            out.append(_conv(a))
            i = j2
        elif c == '}':
            i += 1
        elif c == '~':
            out.append(' ')
            i += 1
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def latex2html(tex):
    """LaTeX → HTML 数学排版（静态，无 JS 依赖）"""
    return _conv(tex.strip())


# ================= 读取与预处理 =================

text = MD.read_text(encoding="utf-8")
m = re.search(r"^# (.+)$", text, re.M)
zh_title = m.group(1).strip()
m = re.search(r"^## (.+)$", text, re.M)
en_title = m.group(1).strip()

lines = text.split("\n")
body = "\n".join(lines[3:]) if len(lines) > 3 else text

# 数学公式：$$...$$ → 静态 HTML 数学块；$...$ → 行内数学
body = re.sub(r"\$\$([\s\S]+?)\$\$",
              lambda mm: '<div class="formula">' + latex2html(mm.group(1)) + '</div>', body)
body = re.sub(r"\$([^$\n]+?)\$",
              lambda mm: '<span class="math">' + latex2html(mm.group(1)) + '</span>', body)

# 加粗预处理：先把非嵌套 **...** 转 <strong>（Python-markdown 对中英混排 ** 偶发解析失败）
n_strong = len(re.findall(r"\*\*(?=\S)([^*\n]+?)(?<=\S)\*\*", body))
body = re.sub(r"\*\*(?=\S)([^*\n]+?)(?<=\S)\*\*", r"<strong>\1</strong>", body)

md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
content = md.convert(body)

# ================= 清爽 CSS（含数学排版样式） =================

CSS = """
:root{
  --bg:#f4f6fa; --card:#ffffff; --ink:#22303f; --sub:#60708a; --line:#e4e9f2;
  --accent:#2f6fed; --accent-soft:#edf3ff; --gold:#b8860b; --gold-soft:#fdf7e6;
  --green:#0a7d3c; --green-soft:#e9f8ef; --red:#c0392b; --red-soft:#fdecea;
  --radius:14px; --shadow:0 1px 3px rgba(30,50,90,.06),0 4px 16px rgba(30,50,90,.05);
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);
  font-family:-apple-system,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  line-height:1.9;font-size:16px;padding:28px 18px}
.wrap{max-width:1160px;margin:0 auto}

/* ---------- 侧栏 TOC ---------- */
.toc{position:sticky;top:26px;width:236px;flex-shrink:0;max-height:calc(100vh - 52px);
  overflow:auto;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:16px 14px;box-shadow:var(--shadow);font-size:13px;line-height:1.7}
.toc-title{font-weight:700;font-size:13px;color:var(--sub);letter-spacing:1px;margin-bottom:10px;
  padding-bottom:8px;border-bottom:1px dashed var(--line)}
.toc a{color:var(--sub);text-decoration:none;display:block;padding:3px 8px;border-radius:7px;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.toc a:hover{color:var(--accent);background:var(--accent-soft)}
.toc .toc-h2 a{font-weight:600;color:var(--ink);margin-top:6px}
.toc .toc-h3 a{padding-left:20px;font-size:12.5px}

/* ---------- 主内容 ---------- */
.main{flex:1;min-width:0}
.hero{background:linear-gradient(135deg,#0e7c7c 0%,#2f6fed 55%,#6c3fb5 100%);
  border-radius:18px;padding:42px 46px;color:#fff;margin-bottom:30px;box-shadow:0 8px 30px rgba(47,111,237,.25)}
.hero .en{font-size:13.5px;opacity:.88;letter-spacing:.6px;margin-bottom:10px}
.hero h1{font-size:30px;font-weight:700;line-height:1.45;margin-bottom:14px}
.hero p{opacity:.94;font-size:14px;max-width:900px;line-height:1.8}
.hero .tags{margin-top:18px}
.hero .tag{display:inline-block;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.25);
  border-radius:20px;padding:4px 15px;font-size:12.5px;margin:4px 8px 0 0;backdrop-filter:blur(4px)}

h2{font-size:23px;margin:52px 0 18px;padding:14px 20px;background:var(--card);
  border:1px solid var(--line);border-left:6px solid var(--accent);border-radius:12px;
  box-shadow:var(--shadow);color:#17304f}
h3{font-size:18px;margin:30px 0 12px;color:#1d3a5f;padding-left:14px;border-left:4px solid var(--gold)}
h4{font-size:15.5px;margin:20px 0 8px;color:#33465f}

p{margin:12px 0}
strong{color:#0f2a47}
ul,ol{margin:12px 0;padding-left:28px}
li{margin:7px 0}

/* 表格 */
table{width:100%;border-collapse:separate;border-spacing:0;margin:20px 0;
  border:1px solid var(--line);border-radius:12px;overflow:hidden;box-shadow:var(--shadow);font-size:14.5px}
th{background:linear-gradient(135deg,#2f6fed,#5a8df0);color:#fff;padding:11px 15px;font-weight:600;
  text-align:left;letter-spacing:.3px}
td{padding:10px 15px;border-top:1px solid var(--line);vertical-align:top}
tbody tr:nth-child(even) td{background:#f8fafd}
tbody tr:hover td{background:var(--accent-soft)}

/* 引用 / 标注块 */
blockquote{background:var(--accent-soft);border-left:5px solid var(--accent);
  border-radius:0 10px 10px 0;padding:13px 20px;margin:16px 0;color:#3a4f6e;font-size:15px}
blockquote strong{color:var(--accent)}

/* ---------- 数学公式（静态 HTML 排版） ---------- */
.formula{background:#f8fafd;border:1px solid var(--line);border-radius:10px;
  padding:20px 24px;margin:20px 0;text-align:center;overflow-x:auto;
  font-family:Georgia,"Times New Roman","STIX Two Math","Cambria Math",serif;
  font-size:18.5px;letter-spacing:.4px;color:#14263f;line-height:2.1}
.math{font-family:Georgia,"Times New Roman","STIX Two Math","Cambria Math",serif;
  color:#17304f;white-space:nowrap;font-size:.95em}
/* 分式 */
.frac{display:inline-flex;flex-direction:column;vertical-align:middle;
  text-align:center;margin:0 3px;line-height:1.3}
.frac .num{padding:0 5px;border-bottom:1.2px solid currentColor;font-size:.86em}
.frac .den{padding:0 5px;font-size:.86em}
/* 根号 */
.sqrt{white-space:nowrap}
.radicand{border-top:1.2px solid currentColor;padding:0 3px;font-size:.94em}
/* 上下标 */
sup,sub{line-height:0;font-size:.72em;color:#1d3a5f}
/* 函数/正体/花体 */
.fn{font-style:normal;font-variant:small-caps}
.rm{font-style:normal}
.txt{font-style:normal}
.cal{font-family:"Segoe Script","Lucida Calligraphy","STXingkai","Comic Sans MS",cursive;font-size:1.08em}
.bf{font-weight:700}
.bb{font-family:"Cambria Math","STIX Two Math",serif;font-weight:700}
.frak{font-family:"Old English Text MT","UnifrakturMaguntia",serif}
.acc{white-space:nowrap}

/* 代码 */
code{background:#eef1f7;border-radius:5px;padding:1.5px 7px;font-size:.9em;
  font-family:"SF Mono","JetBrains Mono",Consolas,monospace}
pre{background:#1f2937;color:#e5e7eb;border-radius:12px;padding:18px 22px;overflow:auto;
  margin:18px 0;font-size:13.5px;line-height:1.7}
pre code{background:none;color:inherit;padding:0;font-size:inherit}

hr{border:none;border-top:1.5px dashed var(--line);margin:38px 0}

.footer{text-align:center;color:var(--sub);font-size:13px;margin:44px 0 10px;padding-top:20px;
  border-top:1px solid var(--line)}

@media(max-width:960px){
  .toc{display:none}
  .wrap{display:block}
  .hero{padding:30px 26px}
  .hero h1{font-size:23px}
}
"""

TOC_JS = """
<script>
document.addEventListener('DOMContentLoaded', function(){
  var toc = document.getElementById('toc-list');
  if(!toc) return;
  var hs = document.querySelectorAll('.main h2, .main h3');
  hs.forEach(function(h){
    if(!h.id){ h.id = 'sec-' + Math.random().toString(36).slice(2,8); }
    var a = document.createElement('a');
    a.href = '#' + h.id;
    a.textContent = h.textContent.replace(/^\\s*\\d+[.．]?\\s*/, '').trim();
    var box = document.createElement('div');
    box.className = h.tagName === 'H2' ? 'toc-h2' : 'toc-h3';
    box.appendChild(a);
    toc.appendChild(box);
  });
  var links = toc.querySelectorAll('a');
  window.addEventListener('scroll', function(){
    var pos = window.scrollY + 120;
    var cur = null;
    hs.forEach(function(h){ if(h.offsetTop <= pos) cur = h.id; });
    links.forEach(function(l){
      l.style.color = (l.getAttribute('href') === '#'+cur) ? 'var(--accent)' : '';
      l.style.background = (l.getAttribute('href') === '#'+cur) ? 'var(--accent-soft)' : '';
    });
  });
});
</script>
"""

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{zh_title}（v2.8）</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">

<nav class="toc">
  <div class="toc-title">📑 目录</div>
  <div id="toc-list"></div>
</nav>

<div class="main">

<div class="hero">
  <div class="en">{en_title}</div>
  <h1>{zh_title}</h1>
  <p>论文初稿 v2.8（M7 因子推导补强）· 2026-08-24 · 启发式统一框架（参考架构，非已确立物理）</p>
  <div class="tags">
    <span class="tag">四条公理</span>
    <span class="tag">引力 = 通量场统计力学涌现</span>
    <span class="tag">规范 = 量子双代数涌现</span>
    <span class="tag">弦网 3+1D 路线</span>
    <span class="tag">30+ 可检验预言</span>
  </div>
</div>

{content}

<div class="footer">论文初稿 v2.8（M7 因子推导补强）· 2026-08-24 · 公式为静态数学排版（无脚本依赖）· 数值可靠性评估（M3 补强）· 术语五级规范· 开发版本沿革见附录 C · 来源与 AI 协助声明见附录 B</div>

</div>
</div>
{TOC_JS}
</body>
</html>
"""
OUT.write_text(html, encoding="utf-8")
print(f"OK -> {OUT} ({OUT.stat().st_size} bytes) | strong: {n_strong} 对")
