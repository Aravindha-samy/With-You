from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from database import get_db

router = APIRouter(prefix="/cognitive-insights", tags=["cognitive-insights"])


@router.post("/", response_model=schemas.CognitiveInsight)
def create_cognitive_insight(insight: schemas.CognitiveInsightCreate, db: Session = Depends(get_db)):
    """Create a cognitive insight (Guardian Agent will call this)"""
    return crud.create_cognitive_insight(db=db, insight=insight)


@router.get("/user/{user_id}", response_model=list[schemas.CognitiveInsight])
def get_user_insights(user_id: int, insight_type: str = None, period: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get cognitive insights for a user.
    
    Query params:
    - insight_type: anxiety_trend, orientation_trend, repetition, emotional_pattern
    - period: daily, weekly, monthly
    """
    return crud.get_cognitive_insights(db=db, user_id=user_id, insight_type=insight_type, period=period, skip=skip, limit=limit)


@router.get("/{insight_id}", response_model=schemas.CognitiveInsight)
def get_cognitive_insight(insight_id: int, db: Session = Depends(get_db)):
    """Get a specific insight"""
    db_insight = crud.get_cognitive_insight(db, insight_id=insight_id)
    if not db_insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    return db_insight


@router.delete("/{insight_id}")
def delete_cognitive_insight(insight_id: int, db: Session = Depends(get_db)):
    """Delete an insight"""
    db_insight = crud.delete_cognitive_insight(db=db, insight_id=insight_id)
    if not db_insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    return {"message": "Insight deleted successfully"}
