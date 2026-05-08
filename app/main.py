from colorama import Fore
from app.services.pdf.pdf_extraction import (
    extract_pdf,
    extract_company_name,
    extract_total_amount,
    extract_date,
)
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import pdfplumber

from app.ml.category.predict import predict_category
from app.ml.items.predict import is_item

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# todo cambiar el tema de los nombres de las empresas a reglas y no con ML


@app.get("/")
async def home():
    return {"message": "Hola desde FastAPI"}


@app.post("/upload")
async def upload(file: UploadFile):
    # Creamos una ruta para el archivo temporal
    file_path = f"app/temp/{file.filename}"

    os.makedirs("app/temp", exist_ok=True)

    # Creamos un archivo temporal para poder trabajar con el
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Comprobamos que pdfplumber pueda abrir el archivo
        # para comprobar que sea un .pdf
        with pdfplumber.open(file_path):
            pass
        # Extraemos los datos del pdf
        lines = extract_pdf(file_path)
        item_list = []
        for line in lines:
            if is_item(line):
                item_list.append(line)
        print("Lista de items:", item_list)
        texto = "".join(item_list)
        # Comprobamos que se haya leído
        # correctamente el pdf
        if lines == "":
            raise HTTPException(404, "No ha sido posible leer el PDF")

        # Una vez obtenido la información
        # eliminamos el archivo temporal
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(400, "El archivo debe ser un PDF")

    return {
        "company_name": f"{extract_company_name(lines)}",
        "date": f"{extract_date(lines)}",
        "total": f"{extract_total_amount(lines)}",
        "category": f"{predict_category(texto)}",
    }


# @app.get("/health")
# async def check_health():
#     return {"status": "OK"}


# lines = extract_pdf("files/factura_2.pdf")
# count = 0
# for line in lines:
#     print(f"{Fore.GREEN + str()}  {Fore.LIGHTBLUE_EX + line}")
#     count += 1

# company_name = extract_company_name(lines)
# total_amount = extract_total_amount(lines)
# date = extract_date(lines)
# print("Nombre: ", company_name)
# print("Total: ", total_amount)
# print("Fecha: ", date)
