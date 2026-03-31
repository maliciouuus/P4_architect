#!/usr/bin/env python3
"""Convertit un fichier Markdown en PDF via weasyprint."""

import sys
import markdown
from weasyprint import HTML, CSS

CSS_STYLE = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=DM+Sans:wght@400;700&display=swap');

* { box-sizing: border-box; }
body {
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px 40px;
}
h1 {
    font-size: 22pt;
    font-weight: 700;
    color: #111;
    border-bottom: 2px solid #FF812D;
    padding-bottom: 8px;
    margin-top: 32px;
}
h2 {
    font-size: 15pt;
    font-weight: 700;
    color: #222;
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 4px;
    margin-top: 28px;
}
h3 { font-size: 12pt; font-weight: 700; color: #333; margin-top: 20px; }
h4 { font-size: 11pt; font-weight: 600; color: #555; margin-top: 16px; }
p { margin: 8px 0; }
ul, ol { margin: 8px 0; padding-left: 24px; }
li { margin: 4px 0; }
code {
    background: #f5f5f5;
    border: 1px solid #e0e0e0;
    border-radius: 3px;
    padding: 1px 5px;
    font-family: 'Courier New', monospace;
    font-size: 9.5pt;
    color: #c7254e;
}
pre {
    background: #f8f8f8;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 14px 16px;
    overflow-x: auto;
    margin: 12px 0;
}
pre code {
    background: none;
    border: none;
    padding: 0;
    color: #333;
    font-size: 9pt;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 10pt;
}
th {
    background: #FF812D;
    color: white;
    padding: 8px 12px;
    text-align: left;
    font-weight: 600;
}
td {
    padding: 7px 12px;
    border-bottom: 1px solid #e0e0e0;
}
tr:nth-child(even) { background: #fafafa; }
blockquote {
    border-left: 4px solid #FF812D;
    margin: 12px 0;
    padding: 8px 16px;
    background: #fff8f5;
    color: #555;
}
a { color: #FF812D; text-decoration: none; }
hr { border: none; border-top: 1px solid #e0e0e0; margin: 24px 0; }
@page {
    size: A4;
    margin: 20mm 15mm;
    @bottom-right {
        content: counter(page) ' / ' counter(pages);
        font-size: 9pt;
        color: #999;
    }
}
"""

def convert(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html_body = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc']
    )

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head>
<body>{html_body}</body>
</html>"""

    HTML(string=html).write_pdf(
        pdf_path,
        stylesheets=[CSS(string=CSS_STYLE)],
    )
    print(f"✅ PDF généré : {pdf_path}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 md_to_pdf.py input.md output.pdf")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
