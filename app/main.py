from fastapi import FastAPI, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from app.file.services.file_service import (
    is_valid_pdf,
    save_temp_file,
    remove_temp_file,
)
from app.invoice.services.invoice_service import process_invoice

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


@app.post("/upload")
@limiter.limit("5/minute")
async def upload(request: Request, file: UploadFile):
    file_path = None
    try:
        file_path = save_temp_file(file)

        if not is_valid_pdf(file_path):
            raise HTTPException(400, "El archivo debe ser un PDF")

        result = process_invoice(file_path)
        return result

    except Exception as e:
        remove_temp_file(file_path)
        raise HTTPException(400, "El archivo debe ser un PDF")
    finally:
        remove_temp_file(file_path)


@app.get("/health")
@limiter.limit("5/minute")
async def check_health(request: Request):
    return {"status": "OK"}
