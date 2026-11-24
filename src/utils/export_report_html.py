"""Script konversi laporan Markdown menjadi dokumen HTML dan potongan JSON untuk Google Docs."""

import base64
import html
import json
import re
from pathlib import Path


def _extract_brace_arg(s: str, pos: int) -> tuple[str, int]:
    """Ambil argumen dalam kurung kurawal {...} mulai dari pos (skip spasi)."""
    n = len(s)
    while pos < n and s[pos].isspace():
        pos += 1
    if pos >= n:
        return "", pos
    if s[pos] != "{":
        if s[pos] == "\\":
            m = re.match(r"\\[a-zA-Z]+", s[pos:])
            if m:
                return m.group(0), pos + len(m.group(0))
        return s[pos], pos + 1
    depth = 0
    start = pos + 1
    i = pos
    while i < n:
        ch = s[i]
        if ch == "\\" and i + 1 < n:
            i += 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return s[start:i], i + 1
        i += 1
    return s[start:], n


def _latex_to_html_inner(tex: str, is_display: bool = False) -> str:
    """Konversi rekursif ekspresi LaTeX menjadi HTML/Unicode bersih untuk Word & Google Docs."""
    s = tex.strip()

    # 1. Handle \begin{cases} ... \end{cases}
    def repl_cases(m):
        body = m.group(1).strip()
        rows = [r.strip() for r in re.split(r"\\\\", body) if r.strip()]
        formatted_rows = []
        for row in rows:
            parts = [p.strip() for p in row.split("&")]
            if len(parts) >= 2:
                left = _latex_to_html_inner(parts[0])
                right = _latex_to_html_inner(" ".join(parts[1:]))
                formatted_rows.append(f"{left}&nbsp;&nbsp;&nbsp;&nbsp;{right}")
            else:
                formatted_rows.append(_latex_to_html_inner(parts[0]))
        if is_display:
            inner = "<br/>".join(f"&nbsp;&nbsp;&nbsp;&nbsp;{r}" for r in formatted_rows)
            return f"{{<br/>{inner}"
        return "{ " + "; ".join(formatted_rows) + " }"

    s = re.sub(r"\\begin\{cases\}(.*?)\\end\{cases\}", repl_cases, s, flags=re.DOTALL)

    # 2. Remove \displaystyle, \left, \right, spacing commands
    s = s.replace("\\displaystyle", "")
    s = re.sub(r"\\left\s*([(\[|{.|])", r"\1", s)
    s = re.sub(r"\\right\s*([)\]}|.|])", r"\1", s)
    s = s.replace("\\left\\{", "{").replace("\\right\\}", "}")
    s = s.replace("\\{", "&#123;").replace("\\}", "&#125;")
    s = s.replace("\\qquad", "    ").replace("\\quad", "  ")
    s = re.sub(r"\\[,;:!]", " ", s)

    # 3. Replace \underbrace{expr}_{label}
    while "\\underbrace" in s:
        idx = s.find("\\underbrace")
        arg1, p1 = _extract_brace_arg(s, idx + len("\\underbrace"))
        sub_label = ""
        p_end = p1
        if p1 < len(s) and s[p1] == "_":
            sub_label, p_end = _extract_brace_arg(s, p1 + 1)
        rendered_arg = _latex_to_html_inner(arg1)
        if sub_label:
            rendered_sub = _latex_to_html_inner(sub_label)
            rep = f"{rendered_arg} [{rendered_sub}]"
        else:
            rep = rendered_arg
        s = s[:idx] + rep + s[p_end:]

    # 4. Replace \dfrac{a}{b} and \frac{a}{b}
    for cmd in ("\\dfrac", "\\frac"):
        while cmd in s:
            idx = s.find(cmd)
            num, p1 = _extract_brace_arg(s, idx + len(cmd))
            den, p2 = _extract_brace_arg(s, p1)
            r_num = _latex_to_html_inner(num)
            r_den = _latex_to_html_inner(den)

            def _needs_paren(x: str) -> bool:
                plain = re.sub(r"<[^>]+>", "", x).strip()
                return any(op in plain for op in [" + ", " - ", " − ", " +", "+ "]) and not (
                    plain.startswith("(") and plain.endswith(")")
                )

            n_str = f"({r_num})" if _needs_paren(r_num) else r_num
            d_str = f"({r_den})" if _needs_paren(r_den) else r_den
            s = s[:idx] + f"{n_str} / {d_str}" + s[p2:]

    # 5. Replace \sqrt{x}
    while "\\sqrt" in s:
        idx = s.find("\\sqrt")
        arg, p1 = _extract_brace_arg(s, idx + len("\\sqrt"))
        r_arg = _latex_to_html_inner(arg)
        s = s[:idx] + f"√({r_arg})" + s[p1:]

    # 6. Replace \hat{x}
    while "\\hat" in s:
        idx = s.find("\\hat")
        arg, p1 = _extract_brace_arg(s, idx + len("\\hat"))
        r_arg = _latex_to_html_inner(arg).strip()
        rep = "ŷ" if r_arg == "y" else f"{r_arg}\u0302"
        s = s[:idx] + rep + s[p1:]

    # 7. Replace \mathbb, \mathcal, \textbf, \mathbf, \texttt, \text (NEVER emit <code>!)
    bb_map = {"R": "ℝ", "N": "ℕ", "Z": "ℤ"}
    cal_map = {"N": "𝒩", "D": "𝒟"}
    for cmd, mode in [
        ("\\mathbb", "bb"),
        ("\\mathcal", "cal"),
        ("\\textbf", "b"),
        ("\\mathbf", "b"),
        ("\\texttt", "plain"),
        ("\\text", "plain"),
    ]:
        while cmd in s:
            idx = s.find(cmd)
            arg, p1 = _extract_brace_arg(s, idx + len(cmd))
            if mode == "bb":
                rep = bb_map.get(arg.strip(), arg.strip())
            elif mode == "cal":
                rep = cal_map.get(arg.strip(), arg.strip())
            elif mode == "b":
                rep = f"<b>{html.escape(arg)}</b>"
            else:
                rep = f"<span style=\"font-style:normal;\">{html.escape(arg)}</span>"
            s = s[:idx] + rep + s[p1:]

    # 8. Replace standard math symbols & functions
    symbol_map = [
        ("\\arg\\max", "arg max"),
        ("\\argmax", "arg max"),
        ("\\implies", " ⇒ "),
        ("\\approx", " ≈ "),
        ("\\times", " × "),
        ("\\cdot", " · "),
        ("\\Delta", "Δ"),
        ("\\alpha", "α"),
        ("\\forall", "∀"),
        ("\\dots", "…"),
        ("\\quad", "  "),
        ("\\max", "max"),
        ("\\min", "min"),
        ("\\arg", "arg"),
        ("\\sum", "∑"),
        ("\\int", "∫"),
        ("\\mid", " | "),
        ("\\mu", "μ"),
        ("\\le", " ≤ "),
        ("\\ge", " ≥ "),
        ("\\in", " ∈ "),
        ("\\to", " → "),
    ]
    for k, v in symbol_map:
        s = re.sub(re.escape(k) + r"(?![a-zA-Z])", v, s)

    # 9. Replace subscripts _{...} / _x and superscripts ^{...} / ^x
    out = []
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if ch in ("_", "^") and i + 1 < n:
            tag = "sub" if ch == "_" else "sup"
            arg, p_next = _extract_brace_arg(s, i + 1)
            rendered = _latex_to_html_inner(arg)
            out.append(f"<{tag}>{rendered}</{tag}>")
            i = p_next
        elif ch in ("{", "}"):
            i += 1
        else:
            out.append(ch)
            i += 1
    res = "".join(out)
    res = re.sub(r" {2,}", " ", res)
    res = res.replace(" ,", ",").replace("( ", "(").replace(" )", ")")
    return res


def render_math_html(tex: str, is_display: bool = False) -> str:
    """Konversi ekspresi LaTeX menjadi HTML akademik bersih (Google Docs & Word ready)."""
    rendered = _latex_to_html_inner(tex, is_display=is_display)
    if is_display:
        return (
            "<p style=\"font-family:'Times New Roman',serif; font-size:12pt; font-weight:normal; "
            "color:#000000; line-height:1.5; text-align:center; text-indent:0; margin:6pt 18pt;\">"
            f"<i>{rendered}</i></p>"
        )
    return f"<i>{rendered}</i>"


def protect_math_and_code(md_text: str):
    """Melindungi blok kode (tanpa tag <code> hijau) dan mengonversi LaTeX ($...$ / $$...$$)."""
    placeholders = {}
    counter = [0]

    def store(val: str) -> str:
        key = f"@@PLACEHOLDER_{counter[0]}@@"
        counter[0] += 1
        placeholders[key] = val
        return key

    # 1. Fenced code blocks ```lang ... ``` — gunakan <p> monospaced hitam polos TANPA <code> agar tidak hijau di Google Docs
    def repl_code_block(match):
        code_lines = match.group(2).rstrip("\n").splitlines()
        escaped_lines = [html.escape(ln).replace(" ", "&nbsp;") for ln in code_lines]
        body = "<br/>".join(escaped_lines)
        return store(
            "<p style=\"font-family:'Courier New',monospace; font-size:9pt; font-weight:normal; "
            "color:#000000; line-height:1.35; background-color:#f8f9fa; border:1px solid #cccccc; "
            "padding:6pt 8pt; margin:6pt 0 8pt 0; text-align:left; text-indent:0;\">"
            f"{body}</p>"
        )

    md_text = re.sub(r"```([^\n]*)\n(.*?)```", repl_code_block, md_text, flags=re.DOTALL)

    # 2. Display math $$...$$
    def repl_display_math(match):
        return store(render_math_html(match.group(1), is_display=True))

    md_text = re.sub(r"\$\$(.*?)\$\$", repl_display_math, md_text, flags=re.DOTALL)

    # 3. Inline code `...` — konversi ke teks Times New Roman bersih (TANPA <code> hijau!)
    def repl_inline_code(match):
        code = html.escape(match.group(1))
        return store(code)

    md_text = re.sub(r"`([^`\n]+)`", repl_inline_code, md_text)

    # 4. Inline math $...$
    def repl_inline_math(match):
        return store(render_math_html(match.group(1), is_display=False))

    md_text = re.sub(r"(?<!\$)\$(?!\$)([^\$\n]+?)(?<!\$)\$(?!\$)", repl_inline_math, md_text)

    return md_text, placeholders


def format_inline(text: str) -> str:
    """Memformat bold, italic, dan link pada teks sebaris."""
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" style="color:#000000;">\1</a>', text)
    return text


def build_cover_html(docs_dir: Path, for_gdocs: bool = False) -> str:
    """
    Membangun Halaman Sampul (Cover) resmi berstandar Universitas Udayana
    yang 100% selaras dengan format tab TLF_Pertemuan12_Kelompok_Kelas_NIM
    dan dirancang muat rapi dalam tepat 1 halaman (Page 1).
    """
    logo_path = docs_dir / "figures" / "logo_unud.png"
    if not for_gdocs and logo_path.exists():
        b64 = base64.b64encode(logo_path.read_bytes()).decode("ascii")
        logo_block = (
            "<p style=\"text-align:center; text-indent:0; margin:14pt 0 14pt 0;\">"
            f"<img src=\"data:image/png;base64,{b64}\" alt=\"Logo Universitas Udayana\" "
            "style=\"width:165px; height:165px;\" /></p>"
        )
    else:
        logo_block = (
            "<p style=\"font-family:'Times New Roman',serif; font-size:10.5pt; font-weight:normal; "
            "font-style:italic; color:#555555; text-align:center; text-indent:0; line-height:1.5; "
            "margin:42pt 0 42pt 0;\">"
            "[Sisipkan Logo Universitas Udayana (salin dari tab TLF_Pertemuan12 "
            "atau sisipkan file docs/figures/logo_unud.png)]</p>"
        )

    members = [
        ("Nathanael Adrian Wattimena", "2408561013"),
        ("I Wayan Arya Adi Guna", "2408561019"),
        ("Komang Dhika Artika Nurdi", "2408561055"),
        ("Kadek Phatra Adisuta Timonuli", "2408561076"),
        ("I Putu Maichail Ganio Wijaya", "2408561123"),
    ]
    names_col = "<br/>".join(m[0] for m in members)
    nims_col = "<br/>".join(m[1] for m in members)
    members_table = (
        "<table align=\"center\" style=\"width:72%; margin:2pt auto 12pt auto; border-collapse:collapse; "
        "border:0px solid #ffffff; font-family:'Times New Roman',serif;\">"
        "<tbody><tr>"
        "<td style=\"border:0px solid #ffffff; padding:2pt 6pt; font-family:'Times New Roman',serif; "
        "font-size:12pt; font-weight:normal; color:#000000; text-align:left; line-height:1.55;\">"
        f"{names_col}</td>"
        "<td style=\"border:0px solid #ffffff; padding:2pt 6pt; font-family:'Times New Roman',serif; "
        "font-size:12pt; font-weight:normal; color:#000000; text-align:right; width:105pt; line-height:1.55;\">"
        f"{nims_col}</td>"
        "</tr></tbody></table>"
    )

    return "\n".join([
        "<p style=\"font-family:'Times New Roman',serif; font-size:13pt; font-weight:bold; "
        "color:#000000; text-align:center; text-indent:0; line-height:1.4; margin:0 0 4pt 0;\">"
        "FINAL PROJECT<br/>"
        "SISTEM PENDUKUNG KEPUTUSAN PENENTUAN KUALITAS DAN KELAYAKAN AIR MINUM "
        "MENGGUNAKAN KOMBINASI METODE FUZZY MAMDANI DAN K-NEAREST NEIGHBOR (KNN)<br/>"
        "MATA KULIAH TEKNOLOGI LOGIKA FUZZY</p>",
        logo_block,
        "<p style=\"font-family:'Times New Roman',serif; font-size:12pt; font-weight:normal; "
        "color:#000000; text-align:center; text-indent:0; line-height:1.45; margin:4pt 0 10pt 0;\">"
        "<strong>Dosen Pengampu:</strong><br/>"
        "Dr. Made Agung Raharja, S.Si., M.Cs.</p>",
        "<p style=\"font-family:'Times New Roman',serif; font-size:12pt; font-weight:normal; "
        "color:#000000; text-align:center; text-indent:0; line-height:1.4; margin:2pt 0 4pt 0;\">"
        "Oleh Kelompok 1</p>",
        members_table,
        "<p style=\"font-family:'Times New Roman',serif; font-size:13pt; font-weight:bold; "
        "color:#000000; text-align:center; text-indent:0; line-height:1.4; margin:10pt 0 0 0;\">"
        "PROGRAM STUDI INFORMATIKA<br/>"
        "FAKULTAS MATEMATIKA DAN ILMU PENGETAHUAN ALAM<br/>"
        "UNIVERSITAS UDAYANA<br/>"
        "TAHUN 2026</p>",
    ])


def is_table_start(lines: list[str], idx: int) -> bool:
    if idx + 1 >= len(lines):
        return False
    first = lines[idx].strip()
    second = lines[idx + 1].strip()
    if "|" not in first or "|" not in second:
        return False
    second_clean = second.strip("|").strip()
    if not second_clean:
        return False
    cells = [c.strip() for c in second_clean.split("|")]
    return all(bool(re.match(r"^:?-{2,}:?$", c)) for c in cells)


def parse_table(lines: list[str]) -> str:
    """Tabel HTML akademik berstandar TLF_Pertemuan12 (header putih bold, garis hitam 1px)."""
    rows = []
    alignments = []
    for idx, line in enumerate(lines):
        raw = line.strip()
        if raw.startswith("|"):
            raw = raw[1:]
        if raw.endswith("|"):
            raw = raw[:-1]
        cells = [c.strip() for c in raw.split("|")]
        if idx == 1 and all(re.match(r"^:?-{2,}:?$", c.replace(" ", "")) for c in cells):
            for c in cells:
                c_clean = c.replace(" ", "")
                if c_clean.startswith(":") and c_clean.endswith(":"):
                    alignments.append("center")
                elif c_clean.endswith(":"):
                    alignments.append("right")
                else:
                    alignments.append("left")
            continue
        rows.append(cells)

    if not rows:
        return ""

    out = [
        "<table style=\"width:100%; border-collapse:collapse; border:1px solid #000000; "
        "font-family:'Times New Roman',serif; font-size:10.5pt; color:#000000; margin:6pt 0 10pt 0;\">"
    ]
    header = rows[0]
    out.append("<thead><tr>")
    for i, cell in enumerate(header):
        align = alignments[i] if i < len(alignments) else "center"
        out.append(
            f"<th style=\"border:1px solid #000000; background-color:#ffffff; color:#000000; "
            f"padding:5pt 6pt; font-weight:bold; text-align:{align}; line-height:1.35;\">"
            f"{format_inline(cell)}</th>"
        )
    out.append("</tr></thead>")

    if len(rows) > 1:
        out.append("<tbody>")
        for r in rows[1:]:
            out.append("<tr>")
            for i, cell in enumerate(r):
                align = alignments[i] if i < len(alignments) else "left"
                out.append(
                    f"<td style=\"border:1px solid #000000; background-color:#ffffff; color:#000000; "
                    f"padding:4pt 6pt; font-weight:normal; text-align:{align}; line-height:1.35;\">"
                    f"{format_inline(cell)}</td>"
                )
            out.append("</tr>")
        out.append("</tbody>")

    out.append("</table>")
    return "\n".join(out)


def parse_markdown_blocks(md_text: str, docs_dir: Path) -> list[dict]:
    """
    Parse Markdown menjadi daftar blok terstruktur dengan format standar TLF_Pertemuan12:
      - Halaman Sampul (Cover) resmi Universitas Udayana di blok pertama
      - Page break sebelum DAFTAR ISI, DAFTAR TABEL, DAFTAR GAMBAR, BAB I..V, DAFTAR PUSTAKA, LAMPIRAN
      - Nol garis horizontal (<hr/>), nol tag <code> hijau, nol kebocoran bold
    """
    # Potong bagian cover lama Markdown (sebelum ## DAFTAR ISI) karena diganti Cover resmi Universitas Udayana
    m_start = re.search(r"^## DAFTAR ISI\s*$", md_text, flags=re.MULTILINE)
    if m_start:
        md_body = md_text[m_start.start():]
    else:
        md_body = md_text

    # Gabungkan "# BAB X\n# JUDUL" menjadi satu H1 "BAB X JUDUL" (tanpa titik dua, sesuai TLF_Pertemuan12)
    md_body = re.sub(
        r"^# (BAB [IVX]+)\s*\n+# ([A-Z][^\n]+)$",
        r"# \1 \2",
        md_body,
        flags=re.MULTILINE,
    )

    protected_text, placeholders = protect_math_and_code(md_body)
    lines = protected_text.splitlines()
    blocks: list[dict] = [
        {
            "type": "cover",
            "html_standalone": build_cover_html(docs_dir, for_gdocs=False),
            "html_gdocs": build_cover_html(docs_dir, for_gdocs=True),
            "page_break_before": False,
        }
    ]

    i = 0
    n = len(lines)
    current_front_section = None  # "DAFTAR ISI" | "DAFTAR TABEL" | "DAFTAR GAMBAR" | None

    def restore(s: str) -> str:
        for key, val in placeholders.items():
            if key in s:
                s = s.replace(key, val)
        return s

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Hapus semua garis horizontal (---) — format laporan universitas tidak memakai garis pemisah
        if re.match(r"^-{3,}$", stripped):
            i += 1
            continue

        # Image line ![alt](rel_path)
        m_img = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", stripped)
        if m_img:
            alt = m_img.group(1).strip()
            rel_path = m_img.group(2).strip()
            img_path = (docs_dir / rel_path).resolve()
            b64_html = ""
            if img_path.exists():
                b64 = base64.b64encode(img_path.read_bytes()).decode("ascii")
                b64_html = (
                    "<p style=\"text-align:center; text-indent:0; margin:10pt 0 4pt 0;\">"
                    f"<img src=\"data:image/png;base64,{b64}\" alt=\"{html.escape(alt)}\" "
                    "style=\"max-width:100%; height:auto; border:1px solid #dddddd;\" /></p>"
                )
            gdocs_placeholder = (
                "<p style=\"font-family:'Times New Roman',serif; font-size:10.5pt; font-weight:normal; "
                "font-style:italic; color:#444444; text-align:center; text-indent:0; "
                "border:1px dashed #999999; padding:8pt 12pt; margin:8pt 24pt 4pt 24pt;\">"
                f"[Sisipkan {html.escape(alt)} (file lokal: docs/{html.escape(rel_path)})]</p>"
            )
            blocks.append({
                "type": "image",
                "alt": alt,
                "path": str(img_path),
                "html_standalone": b64_html,
                "html_gdocs": gdocs_placeholder,
                "page_break_before": False,
            })
            i += 1
            continue

        # Block placeholder (code block or display math)
        if stripped.startswith("@@PLACEHOLDER_") and stripped.endswith("@@") and len(stripped.split()) == 1:
            blocks.append({
                "type": "html",
                "html": restore(stripped),
                "page_break_before": False,
            })
            i += 1
            continue

        # Headings
        m_h = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m_h:
            level = len(m_h.group(1))
            raw_title = m_h.group(2).strip()
            content = restore(format_inline(raw_title))
            plain_title = re.sub(r"<[^>]+>", "", content).strip().upper()

            # Front matter sections: DAFTAR ISI, DAFTAR TABEL, DAFTAR GAMBAR -> H1 centered + blank space + page break
            if plain_title in ("DAFTAR ISI", "DAFTAR TABEL", "DAFTAR GAMBAR"):
                current_front_section = plain_title
                style = (
                    "font-family:'Times New Roman',serif; font-size:13pt; font-weight:bold; "
                    "color:#000000; text-align:center; text-indent:0; line-height:1.5; "
                    "margin:4pt 0 12pt 0;"
                )
                blank_p = (
                    "<p style=\"font-family:'Times New Roman',serif; font-size:12pt; "
                    "font-weight:normal; color:#000000; text-align:left; text-indent:0; "
                    "line-height:1.5; margin:6pt 0;\">&nbsp;</p>"
                )
                blocks.append({
                    "type": "html",
                    "html": f"<h1 style=\"{style}\">{content}</h1>\n{blank_p}",
                    "page_break_before": True,
                })
                i += 1
                continue

            current_front_section = None
            page_break = False

            if level == 1:
                # BAB I PENDAHULUAN, ..., DAFTAR PUSTAKA, LAMPIRAN — rata kiri 13pt Bold (seperti TLF_Pertemuan12)
                page_break = True
                align = "center" if plain_title in ("DAFTAR PUSTAKA", "LAMPIRAN") else "left"
                style = (
                    f"font-family:'Times New Roman',serif; font-size:13pt; font-weight:bold; "
                    f"color:#000000; text-align:{align}; text-indent:0; line-height:1.5; "
                    "margin:4pt 0 10pt 0;"
                )
            elif level == 2:
                style = (
                    "font-family:'Times New Roman',serif; font-size:12pt; font-weight:bold; "
                    "color:#000000; text-align:left; text-indent:0; line-height:1.5; "
                    "margin:12pt 0 4pt 0;"
                )
            elif level == 3:
                style = (
                    "font-family:'Times New Roman',serif; font-size:12pt; font-weight:bold; "
                    "color:#000000; text-align:left; text-indent:0; line-height:1.5; "
                    "margin:10pt 0 4pt 0;"
                )
            else:
                style = (
                    "font-family:'Times New Roman',serif; font-size:12pt; font-weight:bold; "
                    "font-style:italic; color:#000000; text-align:left; text-indent:0; "
                    "line-height:1.5; margin:8pt 0 4pt 0;"
                )

            blocks.append({
                "type": "html",
                "html": f"<h{level} style=\"{style}\">{content}</h{level}>",
                "page_break_before": page_break,
            })
            i += 1
            continue

        # Table
        if is_table_start(lines, i):
            table_lines = []
            while i < n and "|" in lines[i].strip():
                table_lines.append(lines[i])
                i += 1
            blocks.append({
                "type": "html",
                "html": restore(parse_table(table_lines)),
                "page_break_before": False,
            })
            continue

        # Lists
        if re.match(r"^(\s*)([-*]|\d+\.)\s+", line):
            # Untuk DAFTAR ISI / DAFTAR TABEL / DAFTAR GAMBAR -> render sebagai baris <p> rapi TANPA bullet!
            if current_front_section is not None:
                front_paras = []
                while i < n and re.match(r"^(\s*)([-*]|\d+\.)\s+", lines[i]):
                    m_item = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
                    indent_spaces = len(m_item.group(1))
                    item_text = restore(format_inline(m_item.group(3).strip()))
                    ml = "24pt" if indent_spaces >= 2 else "0"
                    front_paras.append(
                        f"<p style=\"font-family:'Times New Roman',serif; font-size:12pt; "
                        f"font-weight:normal; color:#000000; line-height:1.5; text-align:left; "
                        f"text-indent:0; margin:2pt 0 2pt {ml};\">{item_text}</p>"
                    )
                    i += 1
                blocks.append({
                    "type": "html",
                    "html": "\n".join(front_paras),
                    "page_break_before": False,
                })
                continue

            list_items = []
            is_ordered = bool(re.match(r"^\s*\d+\.\s+", line))
            tag = "ol" if is_ordered else "ul"
            while i < n and (
                re.match(r"^(\s*)([-*]|\d+\.)\s+", lines[i])
                or (lines[i].startswith("   ") and lines[i].strip() and not is_table_start(lines, i))
            ):
                curr = lines[i]
                m_item = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", curr)
                if m_item:
                    indent = len(m_item.group(1))
                    item_text = restore(format_inline(m_item.group(3).strip()))
                    ml = " margin-left:18pt;" if indent >= 2 else ""
                    list_items.append(
                        f"<li style=\"font-family:'Times New Roman',serif; font-size:12pt; "
                        f"font-weight:normal; color:#000000; line-height:1.5; text-align:justify;{ml}\">"
                        f"{item_text}</li>"
                    )
                else:
                    if list_items:
                        list_items[-1] = (
                            list_items[-1][:-5] + " " + restore(format_inline(curr.strip())) + "</li>"
                        )
                i += 1
            blocks.append({
                "type": "html",
                "html": (
                    f"<{tag} style=\"margin:4pt 0 8pt 18pt; padding-left:14pt; "
                    f"font-family:'Times New Roman',serif; font-size:12pt; font-weight:normal; color:#000000;\">\n"
                    + "\n".join(list_items)
                    + f"\n</{tag}>"
                ),
                "page_break_before": False,
            })
            continue

        # Paragraph
        para_lines = []
        while i < n:
            s = lines[i].strip()
            if (
                not s
                or re.match(r"^-{3,}$", s)
                or re.match(r"^(#{1,6})\s+", s)
                or re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", s)
                or re.match(r"^(\s*)([-*]|\d+\.)\s+", lines[i])
                or is_table_start(lines, i)
                or (s.startswith("@@PLACEHOLDER_") and s.endswith("@@") and len(s.split()) == 1)
            ):
                break
            if lines[i].endswith("  "):
                para_lines.append(format_inline(s) + "<br/>")
            else:
                para_lines.append(format_inline(s))
            i += 1

        if para_lines:
            para_html = restore(" ".join(para_lines))
            if re.match(r"^<strong>(Tabel|Gambar)\s+", para_html):
                align = "center" if para_html.startswith("<strong>Gambar") else "left"
                p_style = (
                    f"font-family:'Times New Roman',serif; font-size:11pt; font-weight:normal; "
                    f"color:#000000; line-height:1.4; text-align:{align}; text-indent:0; "
                    "margin:6pt 0 6pt 0;"
                )
            elif re.match(r"^<strong>(Keterangan|Catatan|Interpretasi|Kesimpulan|Hasil|Ringkasan)", para_html):
                p_style = (
                    "font-family:'Times New Roman',serif; font-size:12pt; font-weight:normal; "
                    "color:#000000; line-height:1.5; text-align:justify; text-indent:0; "
                    "margin:4pt 0 6pt 0;"
                )
            else:
                # Paragraf narasi standar: Times New Roman 12pt normal, rata kanan-kiri, indentasi 1.25cm (36pt)
                p_style = (
                    "font-family:'Times New Roman',serif; font-size:12pt; font-weight:normal; "
                    "color:#000000; line-height:1.5; text-align:justify; text-indent:36pt; "
                    "margin:0 0 6pt 0;"
                )
            blocks.append({
                "type": "html",
                "html": f"<p style=\"{p_style}\">{para_html}</p>",
                "page_break_before": False,
            })
        else:
            blocks.append({
                "type": "html",
                "html": (
                    "<p style=\"font-family:'Times New Roman',serif; font-size:12pt; "
                    "font-weight:normal; color:#000000; line-height:1.5; text-align:justify; "
                    f"text-indent:36pt; margin:0 0 6pt 0;\">{restore(format_inline(stripped))}</p>"
                ),
                "page_break_before": False,
            })
            i += 1

    return blocks


def convert_report_to_html(md_path: Path, html_path: Path, chunks_json_path: Path | None = None):
    md_content = md_path.read_text(encoding="utf-8")
    blocks = parse_markdown_blocks(md_content, md_path.parent)

    # 1. Build standalone self-contained HTML (dengan Cover berlogo Unud + seluruh gambar PNG tertanam)
    body_parts = []
    for b in blocks:
        if b.get("page_break_before"):
            body_parts.append("<div class=\"page-break\" style=\"page-break-before:always;\"></div>")
        if b["type"] in ("cover", "image"):
            if b["html_standalone"]:
                body_parts.append(b["html_standalone"])
        else:
            body_parts.append(b["html"])
    body_html = "\n\n".join(body_parts)

    full_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Laporan Resmi Final Project TLF - Kelompok 1 Informatika Universitas Udayana</title>
  <style>
    @page {{
      size: A4;
      margin: 2.54cm 2.54cm 2.54cm 3.0cm;
    }}
    body {{
      font-family: "Times New Roman", Times, Georgia, serif;
      font-size: 12pt;
      font-weight: normal;
      line-height: 1.5;
      color: #000000;
      background-color: #f4f4f4;
      margin: 0;
      padding: 24px 12px;
    }}
    .document-container {{
      max-width: 21cm;
      margin: 0 auto;
      background-color: #ffffff;
      padding: 2.54cm 2.54cm 2.54cm 3.0cm;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.12);
      box-sizing: border-box;
    }}
    .page-break {{
      border-top: 1px dashed #dddddd;
      margin: 28pt 0;
    }}
    @media print {{
      body {{ background-color: #ffffff; padding: 0; }}
      .document-container {{ box-shadow: none; padding: 0; max-width: 100%; }}
      .page-break {{ border: 0; margin: 0; page-break-before: always; }}
      table, img {{ page-break-inside: avoid; }}
    }}
  </style>
</head>
<body>
  <div class="document-container">
{body_html}
  </div>
</body>
</html>
"""
    html_path.write_text(full_html, encoding="utf-8")
    print(f"[SUCCESS] Laporan HTML mandiri selesai: {html_path} ({html_path.stat().st_size:,} bytes)")

    # 2. Build Google Docs sequential chunks (pecah setiap page_break_before & max 16KB per chunk)
    if chunks_json_path is not None:
        chunks = []
        buf = []
        buf_len = 0
        buf_page_break = False
        MAX_CHUNK = 16000

        def flush():
            nonlocal buf, buf_len, buf_page_break
            if buf:
                chunks.append({
                    "type": "html",
                    "page_break_before": buf_page_break,
                    "html": "\n\n".join(buf),
                })
                buf = []
                buf_len = 0
                buf_page_break = False

        for b in blocks:
            frag = b["html_gdocs"] if b["type"] in ("cover", "image") else b["html"]
            if not frag:
                continue
            if b.get("page_break_before"):
                flush()
                buf_page_break = True
            elif buf and (buf_len + len(frag) > MAX_CHUNK):
                flush()
            buf.append(frag)
            buf_len += len(frag)
        flush()

        chunks_json_path.parent.mkdir(parents=True, exist_ok=True)
        chunks_json_path.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")
        pb_count = sum(1 for c in chunks if c["page_break_before"])
        print(
            f"[SUCCESS] Paket Google Docs ({len(chunks)} segmen, {pb_count} page break) tersimpan di: "
            f"{chunks_json_path}"
        )

    # 3. Audit ketat: 0 LaTeX mentah, 0 <hr>, 0 <code> hijau
    audit_text = re.sub(r"data:image/png;base64,[A-Za-z0-9+/=]+", "", body_html)
    audit_text = audit_text.replace("\\Scripts\\activate", "")
    raw_cmds = re.findall(r"\\[a-zA-Z]+", audit_text)
    raw_dollars = re.findall(r"\$", audit_text)
    raw_sub_sup = re.findall(r"[_^]\{", audit_text)
    hr_count = len(re.findall(r"<hr\b", audit_text, flags=re.IGNORECASE))
    code_count = len(re.findall(r"<code\b", audit_text, flags=re.IGNORECASE))
    print(f"[AUDIT] Raw LaTeX commands: {len(raw_cmds)} {raw_cmds[:10]}")
    print(f"[AUDIT] Raw '$' tokens: {len(raw_dollars)}")
    print(f"[AUDIT] Raw '_{{/^}}' tokens: {len(raw_sub_sup)}")
    print(f"[AUDIT] <hr> tags: {hr_count} | <code> tags: {code_count}")


if __name__ == "__main__":
    base_dir = Path("/Users/dhikaartika/Documents/Final-Project-Fuzzy/docs")
    md_file = base_dir / "Laporan_Final_Project_TLF_Kelompok_1.md"
    html_file = base_dir / "Laporan_Final_Project_TLF_Kelompok_1.html"
    chunks_file = Path(
        "/Users/dhikaartika/.t3/userdata/providers/antigravity/"
        "ac0a3dfd6dddb20962cecff6ee5fe65e19d3923be20e52c5ab52ff877f7e4c32/"
        "antigravity-acp/brain/bee19c33-1962-4a18-a81f-e9db52ed9aee/scratch/gdocs_clean_chunks.json"
    )
    convert_report_to_html(md_file, html_file, chunks_file)
