
import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.ingestion.loader import load_document
from app.ingestion.chunker import split_documents
from app.database.vector_store import save_documents

router = APIRouter()

UPLOAD_DIR = "uploaded_documents"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    allowed_extensions = [".pdf", ".docx", ".txt"]

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and TXT files are supported."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        documents = load_document(file_path)

        chunks = split_documents(documents)

        save_documents(chunks)

        return {
            "message": "Document uploaded and indexed successfully",
            "filename": file.filename,
            "total_chunks": len(chunks)
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:
        await file.close()
