from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from database import get_db

router = APIRouter(prefix="/agent-interactions", tags=["agent-interactions"])


@router.post("/", response_model=schemas.AgentInteraction)
def create_agent_interaction(interaction: schemas.AgentInteractionCreate, db: Session = Depends(get_db)):
    """Log an agent interaction (Aurora will call this)"""
    return crud.create_agent_interaction(db=db, interaction=interaction)


@router.get("/user/{user_id}", response_model=list[schemas.AgentInteraction])
def get_user_interactions(user_id: int, agent_type: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all interactions for a user, optionally filtered by agent type"""
    return crud.get_agent_interactions(db=db, user_id=user_id, agent_type=agent_type, skip=skip, limit=limit)


@router.get("/{interaction_id}", response_model=schemas.AgentInteraction)
def get_agent_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Get a specific interaction"""
    db_interaction = crud.get_agent_interaction(db, interaction_id=interaction_id)
    if not db_interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return db_interaction


@router.delete("/{interaction_id}")
def delete_agent_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Delete an interaction"""
    db_interaction = crud.delete_agent_interaction(db=db, interaction_id=interaction_id)
    if not db_interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return {"message": "Interaction deleted successfully"}
