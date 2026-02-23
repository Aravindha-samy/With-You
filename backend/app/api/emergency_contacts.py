from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from database import get_db
from app.model import EmergencyContact

router = APIRouter(prefix="/emergency-contacts", tags=["emergency-contacts"])


@router.post("/", response_model=schemas.EmergencyContact)
def create_emergency_contact(contact: schemas.EmergencyContactCreate, db: Session = Depends(get_db)):
    return crud.create_emergency_contact(db=db, contact=contact)


@router.get("/", response_model=list[schemas.EmergencyContact])
def get_emergency_contacts(user_id: int = None, db: Session = Depends(get_db)):
    if user_id:
        return crud.get_emergency_contacts(db=db, user_id=user_id)
    # Return all if no user_id specified
    return db.query(EmergencyContact).all()


@router.get("/{contact_id}", response_model=schemas.EmergencyContact)
def get_emergency_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_emergency_contact(db, contact_id=contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Emergency contact not found")
    return db_contact


@router.put("/{contact_id}", response_model=schemas.EmergencyContact)
def update_emergency_contact(contact_id: int, contact: schemas.EmergencyContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.update_emergency_contact(db=db, contact_id=contact_id, contact=contact)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Emergency contact not found")
    return db_contact


@router.delete("/{contact_id}")
def delete_emergency_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.delete_emergency_contact(db=db, contact_id=contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Emergency contact not found")
    return {"message": "Emergency contact deleted successfully"}
