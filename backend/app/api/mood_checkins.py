from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from database import get_db
from app.model import MoodCheckIn

router = APIRouter(prefix="/mood-checkins", tags=["mood-checkins"])


@router.post("/", response_model=schemas.MoodCheckIn)
def create_mood_checkin(checkin: schemas.MoodCheckInCreate, db: Session = Depends(get_db)):
    return crud.create_mood_checkin(db=db, checkin=checkin)


@router.get("/", response_model=list[schemas.MoodCheckIn])
def get_mood_checkins(user_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if user_id:
        return crud.get_mood_checkins(db=db, user_id=user_id, skip=skip, limit=limit)
    # Return all if no user_id specified
    return db.query(MoodCheckIn).offset(skip).limit(limit).all()


@router.get("/{checkin_id}", response_model=schemas.MoodCheckIn)
def get_mood_checkin(checkin_id: int, db: Session = Depends(get_db)):
    db_checkin = crud.get_mood_checkin(db, checkin_id=checkin_id)
    if not db_checkin:
        raise HTTPException(status_code=404, detail="Mood check-in not found")
    return db_checkin


@router.delete("/{checkin_id}")
def delete_mood_checkin(checkin_id: int, db: Session = Depends(get_db)):
    db_checkin = crud.delete_mood_checkin(db=db, checkin_id=checkin_id)
    if not db_checkin:
        raise HTTPException(status_code=404, detail="Mood check-in not found")
    return {"message": "Mood check-in deleted successfully"}
