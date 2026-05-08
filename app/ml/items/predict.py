import joblib
import re

MODEL_PATH = "app/ml/artifacts/model_items.pkl"

model = joblib.load(MODEL_PATH)


def is_item(line):
    line_lower = line.lower().strip()

    # ❌ EMAIL
    if re.search(r"\S+@\S+", line_lower):
        return False

    # ❌ TELÉFONO
    if re.search(r"(\+?\d[\d\s\-]{7,})", line_lower):
        return False

    # ❌ DNI / NIF
    if re.search(r"\b\d{7,8}[a-zA-Z]\b", line_lower):
        return False

    # ❌ PALABRAS CLAVE
    if any(
        word in line_lower
        for word in [
            "total",
            "iva",
            "irpf",
            "base",
            "factura",
            "fecha",
            "cif",
            "nif",
            "email",
            "teléfono",
            "precio",
            "unidad",
        ]
    ):
        return False

    # ❌ DEMASIADO CORTO (ruido típico)
    if len(line_lower.split()) <= 1:
        return False

    # 👉 SI PASA TODO → ML
    return model.predict([line])[0] == "item"
