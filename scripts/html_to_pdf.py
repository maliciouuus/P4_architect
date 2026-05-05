#!/usr/bin/env python3
"""Convertit un fichier HTML en PDF via weasyprint."""

import sys
from pathlib import Path
from weasyprint import HTML, CSS

# Style d'impression minimal — la mise en page est déjà dans le HTML
PRINT_CSS = CSS(string="""
    @page {
        size: A4;
        margin: 18mm 14mm 20mm;
        @bottom-right {
            content: counter(page) " / " counter(pages);
            font-size: 9pt;
            color: #999;
        }
        @bottom-left {
            content: "DataShare MVP — Documentation Technique";
            font-size: 9pt;
            color: #bbb;
        }
    }
""")


def convert(html_path, pdf_path):
    base_url = str(Path(html_path).parent.resolve())
    HTML(filename=html_path, base_url=base_url).write_pdf(
        pdf_path,
        stylesheets=[PRINT_CSS],
    )
    print(f"✅ PDF généré : {pdf_path}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 html_to_pdf.py input.html output.pdf")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
