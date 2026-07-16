"""
pdf.py - PDF generation with source code layout.
"""

from pathlib import Path

from fpdf import FPDF

STUDENT = "Xavier Merida / 1166726"


class SourcePDF(FPDF):
    """PDF document with header/footer and lab-assignment sections."""

    def header(self):
        self.set_font("Helvetica", size=9)
        self.cell(0, 6, STUDENT, align="R", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=9)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def title_page(self, title: str, subtitle: str = ""):
        """Add a centered title page."""
        self.add_page()
        self.ln(60)
        self.set_font("Helvetica", "B", 28)
        self.cell(0, 15, title, align="C", new_x="LMARGIN", new_y="NEXT")
        if subtitle:
            self.ln(5)
            self.set_font("Helvetica", "", 18)
            self.cell(0, 12, subtitle, align="C", new_x="LMARGIN", new_y="NEXT")

    def add_activity(self, name: str, files: list[str], project_root: Path):
        """Add a section for one activity with its source files."""
        self.add_page()
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 12, name, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

        for path in files:
            full = project_root / path
            if not full.exists():
                print(f"  [!] Not found: {path}")
                continue

            content = full.read_text()
            self.set_font("Helvetica", "B", 12)
            self.cell(0, 10, path, new_x="LMARGIN", new_y="NEXT")
            self.ln(2)
            self.set_font("Courier", size=10)
            self.multi_cell(0, 5, content)
            self.ln(6)

    def add_screenshot(self, path: str):
        """Add a full-page screenshot section."""
        self.add_page()
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 12, "Execution", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        self.image(str(path), w=170)


def generate_pdf(
    project_root: Path,
    title: str,
    activities: list[dict],
    output_path: Path,
    subtitle: str = "",
    image_path: Path | None = None,
) -> Path:
    """Generate the source code PDF. Returns the output path."""
    pdf = SourcePDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.title_page(title, subtitle)

    for act in activities:
        pdf.add_activity(act["name"], act["files"], project_root)

    if image_path and image_path.exists():
        pdf.add_screenshot(image_path)

    pdf.output(output_path)
    return output_path
