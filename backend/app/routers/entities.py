import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.case import Case
from app.models.entity import Person, Company
from app.schemas.entity import PersonCreate, PersonOut, CompanyCreate, CompanyOut
from app.services.audit import log_action

router = APIRouter(prefix="/cases/{case_id}", tags=["entities"])


def _get_case_or_404(db: Session, case_id: uuid.UUID) -> Case:
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.post("/persons", response_model=PersonOut)
def add_person(case_id: uuid.UUID, payload: PersonCreate, db: Session = Depends(get_db)):
    case = _get_case_or_404(db, case_id)

    if payload.pan:
        existing = db.query(Person).filter(Person.case_id == case_id, Person.pan == payload.pan).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Person with PAN {payload.pan} already exists in this case")

    person = Person(case_id=case_id, **payload.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)

    log_action(db, case_id, case.created_by, "CREATE_PERSON", "PERSON", person.id,
               {"full_name": person.full_name, "role": person.role, "pan": person.pan})
    return person


@router.post("/companies", response_model=CompanyOut)
def add_company(case_id: uuid.UUID, payload: CompanyCreate, db: Session = Depends(get_db)):
    case = _get_case_or_404(db, case_id)

    if payload.pan:
        existing = db.query(Company).filter(Company.case_id == case_id, Company.pan == payload.pan).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Company with PAN {payload.pan} already exists")

    company = Company(case_id=case_id, **payload.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)

    log_action(db, case_id, case.created_by, "CREATE_COMPANY", "COMPANY", company.id,
               {"name": company.name, "pan": company.pan, "cin": company.cin})
    return company


@router.get("/entities")
def list_entities(case_id: uuid.UUID, db: Session = Depends(get_db)):
    _get_case_or_404(db, case_id)
    persons = db.query(Person).filter(Person.case_id == case_id).all()
    companies = db.query(Company).filter(Company.case_id == case_id).all()
    return {
        "persons": [PersonOut.model_validate(p) for p in persons],
        "companies": [CompanyOut.model_validate(c) for c in companies],
    }