from fpdf import FPDF
import os

def generate_pdf_log(success_file, fail_file, output_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="YouTube Download Summary", ln=True, align='C')

    def add_section(title, filepath):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt=title, ln=True)
        pdf.set_font("Arial", size=10)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    pdf.multi_cell(0, 8, txt=line.strip())
        else:
            pdf.multi_cell(0, 8, txt="No data.")

    add_section("✅ Successful Downloads", success_file)
    add_section("❌ Failed Downloads", fail_file)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
