import os, shutil, pdfplumber


def is_valid_pdf(file_path):
    try:
        with pdfplumber.open(file_path):
            pass

        print("[PDF] Archivo válido")
        return True
    except Exception as e:
        print(f"[PDF ERROR] {e}")
        return False


def save_temp_file(file):
    file_path = f"app/temp/{file.filename}"

    os.makedirs("app/temp", exist_ok=True)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"[FILE] Archivo guardado: {file.filename}")

    return file_path


def remove_temp_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print("[FILE] Archivo eliminado")
