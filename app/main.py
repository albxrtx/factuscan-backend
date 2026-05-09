from app.services.pdf.pdf_extraction import (
    extract_pdf,
    extract_company_name,
    extract_total_amount,
    extract_date,
)
from fastapi import FastAPI, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import pdfplumber
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from app.ml.category.predict import predict_category
from app.ml.items.predict import is_item

from app.file.services.file_service import (
    is_valid_pdf,
    save_temp_file,
    remove_temp_file,
)

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# todo Cambiar el return del enpoint (/upload)


@app.post("/upload")
@limiter.limit("5/minute")
async def upload(request: Request, file: UploadFile):
    file_path = None
    try:
        file_path = save_temp_file(file)

        if not is_valid_pdf(file_path):
            raise HTTPException(400, "El archivo debe ser un PDF")

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

    except Exception as e:
        remove_temp_file(file_path)
        raise HTTPException(400, "El archivo debe ser un PDF")
    finally:
        remove_temp_file(file_path)
    return {
        "company_name": f"{extract_company_name(lines)}",
        "date": f"{extract_date(lines)}",
        "total": f"{extract_total_amount(lines)}",
        "category": f"{predict_category(texto)}",
    }


@app.get("/health")
@limiter.limit("5/minute")
async def check_health(request: Request):
    return {"status": "OK"}
