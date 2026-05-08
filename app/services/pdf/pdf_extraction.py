import pdfplumber
import re


def extract_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        p0 = pdf.pages[0]

        lines = p0.extract_text(
            x_tolerance=3,
            x_tolerance_ratio=None,
            y_tolerance=3,
            layout=False,
            x_density=7.25,
            y_density=13,
            line_dir_render=None,
            char_dir_render=None,
        ).split("\n")

    return lines


def extract_company_name(lines):

    for line in lines:
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


def extract_total_amount(lines):
    for i, line in enumerate(lines):

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
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()

                match = re.search(r"(\d+[.,]\d{2})", next_line)
                if match:
                    return match.group(1)

    return "Sin resultado"


def extract_date(lines):

    for line in lines:
        if not line:
            continue
        match = re.search(r"\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4}", line)
        if match:
            return match.group(0)

    return "Sin resultado"
