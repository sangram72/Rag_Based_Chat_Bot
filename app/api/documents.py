
import os
import re
import shutil

from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.ingestion.loader import load_document
from app.ingestion.chunker import split_documents
from app.database.vector_store import save_documents


router = APIRouter()

UPLOAD_DIR = "uploaded_documents"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def create_document_id(filename):
    """
    Create a stable document ID from the filename.
    """

    name = Path(filename).stem.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def identify_document_type(filename, person_name=None):

    filename = filename.lower()

    if person_name:
        return "cv"

    if any(word in filename for word in ["cv", "resume", "curriculum"]):
        return "cv"

    if any(word in filename for word in ["policy", "leave", "employee", "hr"]):
        return "policy"

    return "general"


def infer_person_name(filename):

    name = Path(filename).stem

    name = re.sub(
        r"(?i)\b(cv|resume|curriculum|vitae)\b",
        "",
        name
    )

    name = re.sub(r"[_\-.]+", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    person_name: str = Form(default="")
):

    allowed_extensions = [".pdf", ".docx", ".txt"]

    filename = (file.filename or "").replace("\\", "/").split("/")[-1]

    extension = Path(filename).suffix.lower()

    if not filename or extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and TXT files are supported."
        )

    person_name = person_name.strip()

    if not person_name and extension == ".pdf":
        person_name = infer_person_name(filename)

    document_type = identify_document_type(
        filename,
        person_name
    )

    document_id = create_document_id(filename)

    file_path = os.path.join(UPLOAD_DIR, filename)

    try:

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        documents = load_document(file_path)

        chunks = split_documents(documents)

        save_documents(
            chunks=chunks,
            filename=filename,
            document_id=document_id,
            document_type=document_type,
            person=person_name if document_type == "cv" else None
        )

        return {
            "message": "Document uploaded and indexed successfully",
            "filename": filename,
            "document_id": document_id,
            "document_type": document_type,
            "person": person_name if document_type == "cv" else None,
            "total_chunks": len(chunks)
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:
        await file.close()
