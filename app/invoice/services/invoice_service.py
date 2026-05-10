import pdfplumber
import re
from app.ml.category.predict import predict_category
from app.ml.items.predict import is_item


def process_invoice(file_path):
    pdf_lines = extract_invoice_data(file_path)
    company_name = extract_company_name(pdf_lines)
    total_amount = extract_total_amount(pdf_lines)
    date = extract_date(pdf_lines)
    invoice_items = extract_invoice_items(pdf_lines)
    invoice_items_text = " ".join(invoice_items)
    category = predict_category(company_name, invoice_items_text)

    return {
        "company_name": f"{company_name}",
        "total": f"{total_amount}",
        "date": f"{date}",
        "category": f"{category}",
    }


def extract_invoice_data(file_path):

    pdf_lines = []

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            text = page.extract_text(
                x_tolerance=3,
                x_tolerance_ratio=None,
                y_tolerance=3,
                layout=False,
                x_density=7.25,
                y_density=13,
                line_dir_render=None,
                char_dir_render=None,
            )
            print(f"[PDF] Página {page.page_number} procesada")
            if text:
                pdf_lines.extend(text.split("\n"))

    return pdf_lines


def extract_company_name(pdf_lines):

    for line in pdf_lines:
        if not line:
            continue

        line = line.strip()

        if any(
            word in line.lower()
            for word in ["factura", "cliente", "cif", "fecha", "total", "neto"]
        ):
            continue

        if re.search(r"(SL\b|S\.L\.|SA\b|S\.A\.|SLU\b|S\.L\.U\.)", line, re.IGNORECASE):
            return line

    return "Sin resultado"


def extract_total_amount(pdf_lines):
    for i, line in enumerate(pdf_lines):

        if not line:
            continue

        line = line.strip()
        if any(word in line.lower() for word in ["subtotal", "iva", "descuento"]):
            continue
        if "total" in line.lower():

            # caso 1: total en la misma línea
            match = re.search(r"(\d+[.,]\d{2})", line)
            if match:
                return match.group(1)

            # caso 2: total en la siguiente línea
            if i + 1 < len(pdf_lines):
                next_line = pdf_lines[i + 1].strip()

                match = re.search(r"(\d+[.,]\d{2})", next_line)
                if match:
                    return match.group(1)

    return "Sin resultado"


def extract_date(pdf_lines):

    for line in pdf_lines:
        if not line:
            continue
        match = re.search(r"\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4}", line)
        if match:
            return match.group(0)

    return "Sin resultado"


def extract_invoice_items(pdf_lines):
    invoice_items = []
    for line in pdf_lines:
        if is_item(line.strip()):
            invoice_items.append(line)
    return invoice_items
