#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown -> LaTeX converter for arXiv submission.
Converts Paper_MatterAntimatterPairStorm_v2.8_EN.md into a compilable main.tex
with the framework's annotation system, Unicode math symbols, tables, lists,
formulas and references all adapted to LaTeX.

Usage: python _arxiv_convert.py
Output: arXiv_submission/main.tex
"""
import re
import os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   'Paper_MatterAntimatterPairStorm_v2.8_EN.md')
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'arXiv_submission')
OUT = os.path.join(OUT_DIR, 'main.tex')

# ---------------------------------------------------------------------------
# Unicode -> LaTeX math command maps
# ---------------------------------------------------------------------------
GREEK_MATH = {
    'α': r'\alpha', 'β': r'\beta', 'γ': r'\gamma', 'δ': r'\delta',
    'ε': r'\varepsilon', 'ζ': r'\zeta', 'η': r'\eta', 'θ': r'\theta',
    'κ': r'\kappa', 'λ': r'\lambda', 'μ': r'\mu', 'ν': r'\nu', 'ξ': r'\xi',
    'π': r'\pi', 'ρ': r'\rho', 'σ': r'\sigma', 'τ': r'\tau', 'φ': r'\varphi',
    'χ': r'\chi', 'ψ': r'\psi', 'ω': r'\omega',
    'Γ': r'\Gamma', 'Δ': r'\Delta', 'Λ': r'\Lambda', 'Π': r'\Pi',
    'Σ': r'\Sigma', 'Φ': r'\Phi', 'Ω': r'\Omega',
}
OP_MATH = {
    '−': '-', '∝': r'\propto', '≥': r'\geq', '≤': r'\leq', '⊂': r'\subset',
    '≈': r'\approx', '∫': r'\int', '∇': r'\nabla', '≪': r'\ll', '≺': r'\prec',
    '∈': r'\in', '≅': r'\cong', '∞': r'\infty', '≫': r'\gg',
    '∎': r'\blacksquare', '⋯': r'\cdots', '≠': r'\neq', '∂': r'\partial',
    '∀': r'\forall', '⊗': r'\otimes', '≇': r'\ncong', '≡': r'\equiv',
    '⊕': r'\oplus', '⋉': r'\ltimes', '±': r'\pm', '×': r'\times',
    '÷': r'\div', '°': r'^{\circ}', '½': r'\tfrac12', 'ℏ': r'\hbar',
    '·': r'\cdot', '‖': r'\|', '†': r'^\dagger', '⟨': r'\langle',
    '⟩': r'\rangle', '□': r'\square', '☉': r'\odot',
}
ARROW_MATH = {
    '→': r'\to', '⟹': r'\implies', '⟺': r'\iff',
    '↔': r'\leftrightarrow', '⇒': r'\Rightarrow',
}
MATH_SINGLE = dict(GREEK_MATH)
MATH_SINGLE.update(OP_MATH)
MATH_SINGLE.update(ARROW_MATH)

# Text-mode single-char map (wrapped in \ensuremath)
SINGLE_MAP = {}
for _k, _v in MATH_SINGLE.items():
    SINGLE_MAP[_k] = r'\ensuremath{' + _v + '}'
SINGLE_MAP['Ṁ'] = r'\ensuremath{\dot{M}}'

SUP_MAP = {'⁻': '-', '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4',
           '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9',
           'ⁿ': 'n', '⁺': '+', 'ᵀ': 'T'}
SUB_MAP = {'₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5',
           '₆': '6', '₇': '7', '₈': '8', '₉': '9', 'ₙ': 'n', 'ᵢ': 'i'}

SUP_CHARS = ''.join(SUP_MAP.keys())
SUB_CHARS = ''.join(SUB_MAP.keys())
GREEK_ASCII = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
               'αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ')


def convert_math(text):
    """Convert Unicode math symbols inside math mode (pure commands)."""
    text = re.sub(r'(.)\u0304',
                  lambda m: '\\bar{' + GREEK_MATH.get(m.group(1), m.group(1)) + '}', text)
    text = re.sub(r'(.)\u20D7',
                  lambda m: '\\vec{' + m.group(1) + '}', text)
    for ch, cmd in MATH_SINGLE.items():
        # Append {} to bare control sequences so a following letter cannot
        # merge into the command name (e.g. \cdotl would be an undefined cs).
        if re.fullmatch(r'\\[a-zA-Z]+', cmd):
            cmd = cmd + '{}'
        text = text.replace(ch, cmd)
    text = re.sub('[' + SUP_CHARS + ']+',
                  lambda m: '^{' + ''.join(SUP_MAP.get(c, c) for c in m.group(0)) + '}', text)
    text = re.sub('[' + SUB_CHARS + ']+',
                  lambda m: '_{' + ''.join(SUB_MAP.get(c, c) for c in m.group(0)) + '}', text)
    # sqrt forms (content converted recursively)
    text = re.sub(r'√\(((?:[^()]|\([^()]*\))*)\)',
                  lambda m: '\\sqrt{' + convert_math(m.group(1)) + '}', text)
    text = re.sub(r'√([A-Za-z0-9]+|[' + GREEK_ASCII + ']+)',
                  lambda m: '\\sqrt{' + convert_math(m.group(1)) + '}', text)
    # Separate a control sequence from a following letter (e.g. \cdotl -> \cdot{}l).
    # Greedy full command-name match, then insert {} only when a letter follows.
    def _protect(text):
        out, last = [], 0
        for m in re.finditer(r'\\[a-zA-Z]+', text):
            end = m.end()
            out.append(text[last:end])
            if end < len(text) and text[end].isalpha():
                out.append('{}')
            last = end
        out.append(text[last:])
        return ''.join(out)
    text = _protect(text)
    return text


# ---------------------------------------------------------------------------
# Inline conversion
# ---------------------------------------------------------------------------
def convert_inline(text):
    """Convert a line of mixed text/math Markdown into LaTeX."""
    # 1. combining macron / vector arrow
    text = re.sub(r'(.)\u0304',
                  lambda m: '\\ensuremath{\\bar{' + GREEK_MATH.get(m.group(1), m.group(1)) + '}}', text)
    text = re.sub(r'(.)\u20D7',
                  lambda m: '\\ensuremath{\\vec{' + m.group(1) + '}}', text)
    # 2. bare ^{...} -> \up{...}  (MUST precede Unicode-superscript runs)
    text = re.sub(r'\^\{([^{}]*)\}',
                  lambda m: '\\up{' + convert_math(m.group(1)) + '}', text)
    # 2b. bare ^(...) -> \up{...}
    text = re.sub(r'\^\(([^()]*)\)',
                  lambda m: '\\up{' + convert_math(m.group(1)) + '}', text)
    # 2c. bare ^X -> \up{X} (single/short token: letters, digits, greek)
    # Exclude '*' so markdown bold markers are never swallowed into \up.
    text = re.sub(r'\^(?!\{)([^\s{}\\()*]+)',
                  lambda m: '\\up{' + convert_math(m.group(1)) + '}', text)
    # 3. bare _{...} -> \down{...}
    text = re.sub(r'\_\{([^{}]*)\}',
                  lambda m: '\\down{' + convert_math(m.group(1)) + '}', text)
    # 4. bare _word -> \down{word}
    text = re.sub('_([A-Za-z0-9]+|[' + GREEK_ASCII + ']+|[\u4e00-\u9fff]+)',
                  lambda m: '\\down{' + convert_math(m.group(1)) + '}', text)
    # 5. Unicode superscript runs -> \up{}
    text = re.sub('[' + SUP_CHARS + ']+',
                  lambda m: '\\up{' + ''.join(SUP_MAP.get(c, c) for c in m.group(0)) + '}', text)
    # 6. Unicode subscript runs -> \down{}
    text = re.sub('[' + SUB_CHARS + ']+',
                  lambda m: '\\down{' + ''.join(SUB_MAP.get(c, c) for c in m.group(0)) + '}', text)
    # 7. sqrt forms
    text = re.sub(r'√\(((?:[^()]|\([^()]*\))*)\)',
                  lambda m: '\\ensuremath{\\sqrt{' + convert_math(m.group(1)) + '}}', text)
    text = re.sub(r'√([A-Za-z0-9]+|[' + GREEK_ASCII + ']+)',
                  lambda m: '\\ensuremath{\\sqrt{' + convert_math(m.group(1)) + '}}', text)
    text = re.sub(r'√([^\s，。；：、（）()]+)',
                  lambda m: '\\ensuremath{\\sqrt{' + convert_math(m.group(1)) + '}}', text)
    # 8. single char map
    for ch, cmd in SINGLE_MAP.items():
        text = text.replace(ch, cmd)
    # 9. punctuation & accents
    text = text.replace('§', r'\S{}')
    text = text.replace('–', '--')
    text = text.replace('—', '---')
    text = text.replace('…', r'\ldots{}')
    text = text.replace('′', r'\ensuremath{^\prime}')
    text = text.replace('″', r'\ensuremath{^{\prime\prime}}')
    text = text.replace('‴', r'\ensuremath{^{\prime\prime\prime}}')
    text = text.replace('é', r"\'{e}")
    text = text.replace('ö', r'\"{o}')
    text = text.replace('&', r'\&')
    text = text.replace('%', r'\%')
    text = text.replace('#', r'\#')
    # escaped pipe in body text -> math double-bar (in tables handled by cell())
    text = text.replace(r'\|', r'\ensuremath{\|}')
    # 10. circled numbers -> plain parenthesized numbers (pifont unavailable)
    cir = {'①': '(1)', '②': '(2)', '③': '(3)', '④': '(4)', '⑤': '(5)',
           '⑥': '(6)', '⑦': '(7)', '⑧': '(8)', '⑨': '(9)', '⑩': '(10)'}
    for k, v in cir.items():
        text = text.replace(k, v)
    # 11. status symbols (pifont-free); drop emoji variation selectors
    text = text.replace('\uFE0F', '')
    text = text.replace('✅', r'\checkmark')
    text = text.replace('✓', r'\checkmark')
    text = text.replace('✗', r'\ensuremath{\times}')
    text = text.replace('⚠', r'\textbf{!}')
    # 12. annotation brackets 【X】 -> \mtag{X} (nested-aware, BEFORE bold)
    while re.search(r'【', text):
        new = re.sub(r'【([^】【]*)】', lambda m: '\\mtag{' + m.group(1) + '}', text)
        if new == text:
            break
        text = new
    # 13. **bold**
    text = re.sub(r'\*\*(.+?)\*\*', lambda m: '\\textbf{' + m.group(1) + '}', text)
    # 14. ~~strike~~
    text = re.sub(r'~~(.+?)~~', lambda m: '\\sout{' + m.group(1) + '}', text)
    # 15. *word* italic (single words only, avoids k* etc.)
    text = re.sub(r'(?<!\*)\*([A-Za-z]+)\*(?!\*)',
                  lambda m: '\\textit{' + m.group(1) + '}', text)
    # 16. ~ (approx) after strike/bold have consumed "~~"
    text = text.replace('~', r'\ensuremath{\sim}')
    return text


# ---------------------------------------------------------------------------
# Code blocks
# ---------------------------------------------------------------------------
def convert_code(block):
    ascii_map = {'├──': '|--', '└──': '`--', '─': '-', '⟹': '=>', '→': '->',
                 'ε': 'eps', '≈': '~', '↔': '<->', '–': '--'}
    out = []
    for line in block:
        for k, v in ascii_map.items():
            line = line.replace(k, v)
        out.append(line)
    return '\\begin{verbatim}\n' + '\n'.join(out) + '\n\\end{verbatim}'


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------
def is_sep(line):
    return bool(re.match(r'^\s*\|[\s\-:|]+\|\s*$', line)) and '-' in line


def convert_table(block):
    rows = []
    for line in block:
        s = line.strip()
        if s.startswith('|'):
            s = s[1:]
        if s.endswith('|'):
            s = s[:-1]
        cells = [c.strip() for c in s.split('|')]
        rows.append(cells)
    sep_idx = None
    for idx, cells in enumerate(rows):
        if all(set(c.replace('-', '').replace(':', '').strip()) == set() for c in cells):
            sep_idx = idx
            break
    if sep_idx is None:
        return ''
    header = rows[0]
    data = rows[sep_idx + 1:]
    ncol = len(header)
    if ncol < 2:
        return ''
    colspec = 'l' + 'X' * (ncol - 1)

    def cell(c, first=False):
        # Escaped pipes in tables mean single vertical bars (|G|² etc.) —
        # handle before convert_inline so they stay single bars.
        c = c.replace(r'\|', '$|$')
        c = convert_inline(c)
        # Protect a leading '[' in the first column: LaTeX would otherwise
        # treat it as the optional argument (row spacing) of the previous \\.
        if first and c.startswith('['):
            c = '{' + c + '}'
        return c

    L = [r'\begin{table}[htbp]', r'\centering']
    L.append(r'\footnotesize' if ncol >= 5 else r'\small')
    L.append('\\begin{tabularx}{\\textwidth}{@{}' + colspec + '@{}}')
    L.append(r'\toprule')
    L.append(' & '.join(cell(c, first=(i == 0)) for i, c in enumerate(header)) + r' \\')
    L.append(r'\midrule')
    for r in data:
        r = (r + [''] * ncol)[:ncol]
        L.append(' & '.join(cell(c, first=(i == 0)) for i, c in enumerate(r)) + r' \\')
    L.append(r'\bottomrule')
    L.append(r'\end{tabularx}')
    L.append(r'\end{table}')
    return '\n'.join(L)


# ---------------------------------------------------------------------------
# Lists
# ---------------------------------------------------------------------------
def convert_list(lines, i):
    out = []
    stack = []  # (env, indent)
    while i < len(lines):
        line = lines[i]
        m_item = re.match(r'^(\s*)[-*]\s+(.*)$', line)
        m_num = re.match(r'^(\s*)(\d+)[.)]\s+(.*)$', line)
        if not (m_item or m_num):
            break
        if m_item:
            indent, kind, content = len(m_item.group(1)), 'itemize', m_item.group(2)
        else:
            indent, kind, content = len(m_num.group(1)), 'enumerate', m_num.group(3)
        while stack and stack[-1][1] > indent:
            out.append('\\end{' + stack.pop()[0] + '}')
        if not stack or stack[-1][1] < indent or stack[-1][0] != kind:
            if stack and stack[-1][1] == indent:
                out.append('\\end{' + stack.pop()[0] + '}')
            out.append('\\begin{' + kind + '}')
            stack.append((kind, indent))
        out.append('\\item ' + convert_inline(content))
        i += 1
    while stack:
        out.append('\\end{' + stack.pop()[0] + '}')
    return '\n'.join(out), i


# ---------------------------------------------------------------------------
# References
# ---------------------------------------------------------------------------
def convert_ref_line(line):
    m = re.match(r'^\*\*(.+?)\*\*[:：]\s*(.*)$', line)
    if m:
        rest = m.group(2)
        parts = re.split(r'(?=\[\d+\])', rest)
        out = []
        for e in parts:
            m2 = re.match(r'\[(\d+)\]\s*(.*)$', e)
            if m2:
                out.append('\\bibitem{ref' + m2.group(1) + '} ' + convert_inline(m2.group(2)))
        return '\n'.join(out)
    return convert_inline(line)


# ---------------------------------------------------------------------------
# Main Markdown -> LaTeX body
# ---------------------------------------------------------------------------
def md_to_tex(md_text, skip_idx=(), cso_mode=False):
    lines = md_text.split('\n')
    out = []
    i = 0
    in_code = False
    code_buf = []
    abstract_open = False
    refs_open = False
    appendix_open = False

    while i < len(lines):
        line = lines[i]
        # skip the document title line (already used for \title{}) and extras
        if i in skip_idx or i == 0:
            i += 1
            continue
        if line.strip().startswith('```'):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                in_code = False
                out.append(convert_code(code_buf))
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue
        if not line.strip():
            out.append('')
            i += 1
            continue
        if re.match(r'^\s*-{3,}\s*$', line):
            out.append('')
            i += 1
            continue
        # table block
        if line.startswith('|') and i + 1 < len(lines) and is_sep(lines[i + 1]):
            block = []
            while i < len(lines) and lines[i].startswith('|'):
                block.append(lines[i])
                i += 1
            out.append(convert_table(block))
            continue
        # display equation
        m = re.match(r'^\s*\$\$(.*)\$\$\s*$', line)
        if m:
            out.append('\\[' + convert_math(m.group(1)) + '\\]')
            i += 1
            continue
        # headings
        m = re.match(r'^(#{1,4})\s+(.*?)\s*$', line)
        if m:
            level = len(m.group(1))
            title_txt = convert_inline(m.group(2))
            if title_txt.strip() in ('Abstract', '摘要'):
                if refs_open:
                    out.append('\\end{thebibliography}')
                    refs_open = False
                out.append('\\begin{abstract}')
                abstract_open = True
            elif title_txt.startswith('References') or title_txt.startswith('参考文献'):
                if abstract_open:
                    out.append('\\end{abstract}')
                    abstract_open = False
                out.append('\\section*{' + title_txt + '}')
                out.append('\\begin{thebibliography}{30}')
                refs_open = True
            elif title_txt.startswith('Appendix') or title_txt.startswith('附录'):
                if abstract_open:
                    out.append('\\end{abstract}')
                    abstract_open = False
                if refs_open:
                    out.append('\\end{thebibliography}')
                    refs_open = False
                out.append('\\section*{' + title_txt + '}')
                appendix_open = True
            else:
                if abstract_open:
                    out.append('\\end{abstract}')
                    abstract_open = False
                if refs_open:
                    out.append('\\end{thebibliography}')
                    refs_open = False
                cmd = {1: 'section', 2: 'section', 3: 'subsection',
                       4: 'subsubsection'}[min(level, 4)]
                star = '*' if appendix_open else ''
                htxt = title_txt
                # CSO classes auto-number sections: strip the manual prefix
                # numbers (e.g. "1 引言" -> "引言") to avoid double numbering.
                if cso_mode and not star:
                    m2 = re.match(r'^(\d+(?:\.\d+)*[a-z]?)\s+(.*)$', htxt)
                    if m2:
                        htxt = m2.group(2)
                out.append('\\' + cmd + star + '{' + htxt + '}')
            i += 1
            continue
        # blockquote
        if line.startswith('> '):
            q = []
            while i < len(lines) and lines[i].startswith('> '):
                q.append(convert_inline(lines[i][2:]))
                i += 1
            out.append('\\begin{quote}\n' + '\n'.join(q) + '\n\\end{quote}')
            continue
        # reference entries (category line like **Topic**: [1] ... or bare [n] ...)
        m_refcat = re.match(r'^\*\*.+?\*\*[:：]\s*\[\d+\]', line)
        m_ref = re.match(r'^\[(\d+)\]\s*(.*)$', line)
        if refs_open and m_refcat:
            out.append(convert_ref_line(line))
            i += 1
            continue
        if refs_open and m_ref:
            out.append('\\bibitem{ref' + m_ref.group(1) + '} ' + convert_inline(m_ref.group(2)))
            i += 1
            continue
        # lists
        m_item = re.match(r'^(\s*)[-*]\s+(.*)$', line)
        m_num = re.match(r'^(\s*)(\d+)[.)]\s+(.*)$', line)
        if m_item or m_num:
            block, i = convert_list(lines, i)
            out.append(block)
            continue
        # plain paragraph
        out.append(convert_inline(line))
        i += 1

    if abstract_open:
        out.append('\\end{abstract}')
    if refs_open:
        out.append('\\end{thebibliography}')
    return '\n'.join(out)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def extract_section(md_text, marker):
    """Return the text block under '## marker' up to the next '## '."""
    ls = md_text.split('\n')
    start = None
    for i, l in enumerate(ls):
        if l.strip().startswith(marker):
            start = i + 1
            break
    if start is None:
        return ''
    body = []
    for l in ls[start:]:
        if l.startswith('## '):
            break
        body.append(l)
    return '\n'.join(body).strip()


def flatten_list(text):
    """Turn markdown list lines into inline text for abstract/header fields."""
    out = []
    for l in text.split('\n'):
        s = l.strip()
        if not s:
            out.append('')
            continue
        s = re.sub(r'^\d+[.)]\s*', '', s)
        s = re.sub(r'^[-*]\s*', '', s)
        out.append(s)
    return ' '.join(out)


def strip_section(md_text, marker):
    """Remove a whole '## marker ... (next ##)' block from the text."""
    ls = md_text.split('\n')
    start = None
    for i, l in enumerate(ls):
        if l.strip().startswith(marker):
            start = i
            break
    if start is None:
        return md_text
    end = start + 1
    for j in range(start + 1, len(ls)):
        if ls[j].startswith('## ') and ls[j].strip() != marker:
            end = j
            break
    else:
        end = len(ls)
    return '\n'.join(ls[:start] + ls[end:])


def main():
    import sys
    zh_mode = '--zh' in sys.argv
    cso_mode = '--cso' in sys.argv
    base = os.path.dirname(os.path.abspath(__file__))
    if cso_mode:
        src = os.path.join(base, '论文初稿_正反物质对风暴统一框架_v2.8.md')
        out = os.path.join(OUT_DIR, 'main_cso.tex')
    elif zh_mode:
        src = os.path.join(base, '论文初稿_正反物质对风暴统一框架_v2.8.md')
        out = os.path.join(OUT_DIR, 'main_zh.tex')
    else:
        src, out = SRC, OUT

    md = open(src, encoding='utf-8').read()
    lines = md.split('\n')

    title_zh = lines[0].lstrip('#').strip()
    subtitle = ''
    skip = ()
    if zh_mode or cso_mode:
        for k, l in enumerate(lines[1:6], 1):
            if l.startswith('## ') and l[3:].strip().startswith('Matter'):
                subtitle = l.lstrip('#').strip()
                skip = (k,)
                break

    if cso_mode:
        en_md = open(os.path.join(base, 'Paper_MatterAntimatterPairStorm_v2.8_EN.md'),
                     encoding='utf-8').read()
        zh_abs = extract_section(md, '## 摘要')
        en_abs = extract_section(en_md, '## Abstract')
        body_md = strip_section(md, '## 摘要')
        title_tex = convert_inline(title_zh)
        body = md_to_tex(body_md, skip_idx=skip, cso_mode=True)
        zh_abs_tex = convert_inline(flatten_list(zh_abs))
        en_abs_tex = convert_inline(flatten_list(en_abs))
        kw_zh = '正反物质对风暴；涌现统计框架；四种基本力统一；量子引力；引力涌现；弦网'
        kw_en = ('matter--antimatter pair storm; emergent statistical framework; '
                 'unification of fundamental forces; quantum gravity; '
                 'emergent gravity; string-net')
        preamble = r'''\documentclass[UTF8,fontset=windows]{csoarticle}

% --- theorem environments (Chinese) ---
\newtheorem{theorem}{定理}
\newtheorem{lemma}{引理}
\renewcommand{\proofname}{证明}

% --- extra packages needed by the paper body ---
\usepackage{tabularx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{ulem}
\usepackage{enumitem}

% --- framework annotation system ---
\newcommand{\mtag}[1]{\textbf{[#1]}}
\newcommand{\up}[1]{\ensuremath{^{#1}}}
\newcommand{\down}[1]{\ensuremath{_{#1}}}

% --- article header (China Science & Technology Online / paper.edu.cn) ---
\titleCHN{''' + title_tex + r'''}
\titleENG{''' + convert_inline(subtitle) + r'''}
\authorCHN{AUTHOR NAME\affil{1}}
\authorENG{AUTHOR NAME\affil{1}}
\affiliationCHN{
    \affil{1} 作者单位，城市　邮编
}
\affiliationENG{
    \affil{1} Author Affiliation, City 000000
}
\abstractCHN{''' + zh_abs_tex + r'''}
\abstractENG{''' + en_abs_tex + r'''}
\keywordCHN{''' + kw_zh + r'''}
\keywordENG{''' + kw_en + r'''}
\cateidCHN{O412}
\authorIntroduction{作者姓名（出生年-），性别，职称，主要研究方向：***。}
\fund{基金项目（编号）}

\begin{document}
\maketitle

''' + body + r'''

\end{document}
'''
    else:
        body = md_to_tex(md, skip_idx=skip)
        if zh_mode:
            title_tex = convert_inline(title_zh) + (' \\\\ ' + convert_inline(subtitle) if subtitle else '')
            author_block = (r'\author{AUTHOR NAME\thanks{作者单位。} \\ \small 作者单位}' + '\n' +
                            r'\date{\today}')
            docclass = r'''\documentclass[12pt]{article}

\usepackage[margin=1in]{geometry}
\usepackage[fontset=windows]{ctex}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{ulem}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{enumitem}
\usepackage{lmodern}
\usepackage[T1]{fontenc}
\usepackage{microtype}
\usepackage[hidelinks]{hyperref}

% --- framework annotation system ---
\newcommand{\mtag}[1]{\textbf{[#1]}}
\newcommand{\up}[1]{\ensuremath{^{#1}}}
\newcommand{\down}[1]{\ensuremath{_{#1}}}

\title{''' + title_tex + r'''}
'''
        else:
            title_tex = convert_inline(title_zh)
            author_block = (r'\author{AUTHOR NAME\thanks{Author affiliation.} \\ \small Author affiliation}' + '\n' +
                            r'\date{\today}')
            docclass = r'''\documentclass[12pt]{article}

\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{ulem}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{enumitem}
\usepackage{lmodern}
\usepackage[T1]{fontenc}
\usepackage{microtype}
\usepackage[hidelinks]{hyperref}

% --- framework annotation system ---
\newcommand{\mtag}[1]{\textbf{[#1]}}
\newcommand{\up}[1]{\ensuremath{^{#1}}}
\newcommand{\down}[1]{\ensuremath{_{#1}}}

\title{''' + title_tex + r'''}
'''
        preamble = docclass + author_block + r'''

\begin{document}
\maketitle

''' + body + r'''

\end{document}
'''
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(preamble)
    print('Wrote', out)


if __name__ == '__main__':
    main()
