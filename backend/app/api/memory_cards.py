from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from database import get_db
from app.model import MemoryCard

router = APIRouter(prefix="/memory-cards", tags=["memory-cards"])


@router.post("/", response_model=schemas.MemoryCard)
def create_memory_card(card: schemas.MemoryCardCreate, db: Session = Depends(get_db)):
    return crud.create_memory_card(db=db, card=card)


@router.get("/", response_model=list[schemas.MemoryCard])
def get_memory_cards(user_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if user_id:
        return crud.get_memory_cards(db=db, user_id=user_id, skip=skip, limit=limit)
    # Return all if no user_id specified
    return db.query(MemoryCard).offset(skip).limit(limit).all()


@router.get("/{card_id}", response_model=schemas.MemoryCard)
def get_memory_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud.get_memory_card(db, card_id=card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Memory card not found")
    return db_card


@router.put("/{card_id}", response_model=schemas.MemoryCard)
def update_memory_card(card_id: int, card: schemas.MemoryCardUpdate, db: Session = Depends(get_db)):
    db_card = crud.update_memory_card(db=db, card_id=card_id, card=card)
    if not db_card:
        raise HTTPException(status_code=404, detail="Memory card not found")
    return db_card


@router.delete("/{card_id}")
def delete_memory_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud.delete_memory_card(db=db, card_id=card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Memory card not found")
    return {"message": "Memory card deleted successfully"}
