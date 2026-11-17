import uuid
import hashlib
import os
import shutil
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import get_settings
from app.models.case import Case
from app.models.document import Document
from app.schemas.document import DocumentOut
from app.services.audit import log_action

router = APIRouter(prefix="/cases/{case_id}/documents", tags=["documents"])
settings = get_settings()

ALLOWED_TYPES = {"BANK_STMT", "ITR", "AIS", "26AS", "GST_RET", "MCA_ANN", "SALE_DEED", "EC", "PATTA", "MORTGAGE", "KYC", "UPI_STMT", "OTHER"}


@router.post("", response_model=DocumentOut)
def upload_document(
    case_id: uuid.UUID,
    doc_type: str = Form(..., description="BANK_STMT | ITR | AIS | 26AS | GST_RET | MCA_ANN | SALE_DEED | EC | PATTA | MORTGAGE | KYC | UPI_STMT | OTHER"),
    uploaded_by: str = Form(..., description="UUID of the uploader"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    if doc_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid doc_type. Must be one of: {ALLOWED_TYPES}")

    # Read file into memory (cap at MAX_UPLOAD_MB)
    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
    contents = file.file.read(max_bytes + 1)
    if len(contents) > max_bytes:
        raise HTTPException(status_code=413, detail=f"File exceeds {settings.MAX_UPLOAD_MB} MB limit")

    # SHA-256 hash for chain of custody
    file_hash = hashlib.sha256(contents).hexdigest()

    # Save to disk: uploads/{case_id}/{doc_id}_{filename}
    doc_id = uuid.uuid4()
    case_dir = os.path.join(settings.UPLOAD_DIR, str(case_id))
    os.makedirs(case_dir, exist_ok=True)
    safe_name = file.filename.replace("/", "_").replace("\\\\", "_")
    storage_path = os.path.join(case_dir, f"{doc_id}_{safe_name}")

    with open(storage_path, "wb") as f:
        f.write(contents)

    # Persist metadata
    doc = Document(
        id=doc_id,
        case_id=case_id,
        doc_type=doc_type,
        file_name=file.filename,
        file_hash=file_hash,
        file_size=len(contents),
        storage_path=storage_path,
        uploaded_by=uuid.UUID(uploaded_by),
        parse_status="PENDING",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    log_action(db, case_id, uuid.UUID(uploaded_by), "UPLOAD_DOCUMENT", "DOCUMENT", doc.id,
               {"file_name": doc.file_name, "doc_type": doc.doc_type, "hash": file_hash, "size": len(contents)})

    return doc


@router.get("", response_model=list[DocumentOut])
def list_documents(case_id: uuid.UUID, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return db.query(Document).filter(Document.case_id == case_id).order_by(Document.uploaded_at.desc()).all()