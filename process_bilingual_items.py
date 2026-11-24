import html
from pathlib import Path


def process_bilingual_items(items: list[dict[str, str]]) -> list[dict[str, str]]:
    """Clean whitespace and validate EN/PT text pairs."""
    cleaned = []
    for index, item in enumerate(items, start=1):
        en_text = " ".join(item.get("en", "").split())
        pt_text = " ".join(item.get("pt", "").split())
        if not en_text or not pt_text:
            raise ValueError(f"Item {index} is missing EN or PT content.")
        cleaned.append({"id": str(index), "en": en_text, "pt": pt_text})
    return cleaned


def build_html_report(items: list[dict[str, str]], output_path: str = "report.html") -> Path:
    """Render a clean HTML summary page from processed bilingual items."""
    rows = []
    for row in items:
        rows.append(
            f"<tr>"
            f"<td>{html.escape(row['id'])}</td>"
            f"<td>{html.escape(row['en'])}</td>"
            f"<td>{html.escape(row['pt'])}</td>"
            f"</tr>"
        )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>EN-PT Content Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; color: #1f2937; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
    th, td {{ border: 1px solid #d1d5db; padding: 0.75rem; text-align: left; }}
    th {{ background: #f3f4f6; }}
  </style>
</head>
<body>
  <h1>EN-PT Content Processing Summary</h1>
  <table>
    <thead>
      <tr><th>#</th><th>English</th><th>Portuguese (BR)</th></tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</body>
</html>"""

    target = Path(output_path)
    target.write_text(page, encoding="utf-8")
    return target


if __name__ == "__main__":
    sample_data = [
        {
            "en": "  Automate repetitive   tasks with clean Python scripts.  ",
            "pt": "  Automatize tarefas repetitivas   com scripts limpos em Python.  ",
        },
        {
            "en": "Fast, accurate English to Portuguese localization.",
            "pt": "Localização rápida e precisa de Inglês para Português.",
        },
        {
            "en": "Fast, accurate English to Portuguese localization.",
            "pt": "Localização rápida e precisa de Inglês para Português.",
        },
    ]
    processed = process_bilingual_items(sample_data)
    saved_file = build_html_report(processed)
    print(f"Report generated: {saved_file.resolve()}")
