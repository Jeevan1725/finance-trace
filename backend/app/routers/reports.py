import uuid
import io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.report_gen import generate_report

router = APIRouter(prefix="/cases/{case_id}/report", tags=["reports"])


@router.get("")
def download_report(case_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        pdf_bytes = generate_report(db, case_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=forensic_report_{case_id}.pdf"},
    )