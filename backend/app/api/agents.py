from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from database import get_db
from typing import Optional

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/ask", response_model=schemas.AgentResponse)
def ask_agent(request: schemas.AgentRequest, db: Session = Depends(get_db)):
    """
    Main entry point for patient queries.
    
    Aurora (Orchestrator) will:
    1. Analyze user_input using Azure OpenAI
    2. Detect intent and emotion
    3. Route to appropriate agent (Harbor, Roots, Solace, Legacy, etc.)
    4. Get response from agent
    5. Apply Guardrail Engine checks
    6. Return response
    
    If agent_type is not specified, Aurora will automatically route.
    """
    
    # Verify user exists
    user = crud.get_user(db, user_id=request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # TODO: Implement Aurora Agent orchestration logic
    # For now, return a placeholder response
    response = schemas.AgentResponse(
        agent_type="aurora",
        response="Please implement Aurora agent orchestration",
        intent="unknown",
        emotion_score=0.5,
        emotion_type="neutral",
        alert_triggered=False
    )
    
    return response


@router.get("/harbor/location/{user_id}")
def get_location(user_id: int, db: Session = Depends(get_db)):
    """
    Harbor Agent: Get orientation information (Where am I?)
    
    Returns:
    - Location (home, hospital, etc.)
    - Move year
    - Safe reassurance message
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # TODO: Implement Harbor with location database
    return {
        "location": "Home",
        "move_year": 2018,
        "city": "Chennai",
        "message": "You're at home in Chennai. You moved here in 2018. You're safe."
    }


@router.get("/harbor/visits/{user_id}")
def get_scheduled_visits(user_id: int, db: Session = Depends(get_db)):
    """
    Harbor Agent: Get scheduled visits (Who is visiting today?)
    
    Returns list of scheduled family visits with times
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # TODO: Implement Harbor with visit scheduling
    return {
        "visits": [],
        "message": "No visits scheduled for today"
    }


@router.get("/roots/family/{user_id}")
def get_family_info(user_id: int, db: Session = Depends(get_db)):
    """
    Roots Agent: Get family member information (Who is this?)
    
    Returns list of family members with photos and descriptions
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get emergency contacts as family members
    family = crud.get_emergency_contacts(db, user_id=user_id)
    
    return {
        "family_members": family,
        "total": len(family)
    }


@router.post("/solace/calm-mode/{user_id}")
def activate_calm_mode(user_id: int, db: Session = Depends(get_db)):
    """
    Solace Agent: Activate calm mode
    
    Triggers calm music, photo slideshow, reassurance messages
    Used when patient is anxious or disoriented
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # TODO: Integrate with Calm Mode UI component
    return {
        "status": "calm_mode_activated",
        "message": "Calm mode activated. Playing soothing content...",
        "content": {
            "music": "gentle_piano.mp3",
            "photos": [],  # Should be from memory cards
            "reassurance": "You're safe. Take deep breaths. I'm here with you."
        }
    }


@router.get("/legacy/stories/{user_id}")
def get_personal_stories(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Legacy Agent: Get personal stories and memories
    
    Returns user's life narrative, work history, personal stories
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get memory cards as stories
    memories = crud.get_memory_cards(db=db, user_id=user_id, skip=skip, limit=limit)
    
    return {
        "stories": memories,
        "total": len(memories)
    }


@router.get("/guardian/dashboard/{user_id}")
def get_guardian_dashboard(user_id: int, db: Session = Depends(get_db)):
    """
    Guardian Agent: Get caregiver dashboard insights
    
    Returns:
    - Anxiety trends
    - Orientation trends
    - Repetition patterns
    - Emotional averages
    - Alerts for caregiver
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get recent interactions for analysis
    interactions = crud.get_agent_interactions(db=db, user_id=user_id, limit=100)
    insights = crud.get_cognitive_insights(db=db, user_id=user_id, limit=50)
    
    # Calculate some basic metrics
    anxiety_count = sum(1 for i in interactions if i.emotion_type == "anxious")
    routine_count = sum(1 for i in interactions if i.is_routine)
    
    return {
        "user_id": user_id,
        "total_interactions": len(interactions),
        "anxiety_instances": anxiety_count,
        "routine_questions": routine_count,
        "insights": insights,
        "recent_interactions": interactions[-10:] if interactions else []
    }


@router.get("/echo/patterns/{user_id}")
def get_memory_patterns(user_id: int, db: Session = Depends(get_db)):
    """
    Echo Agent: Get memory and behavior patterns
    
    Returns:
    - Repetition frequency
    - Anxiety patterns
    - Emotional trends
    - Question patterns
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    interactions = crud.get_agent_interactions(db=db, user_id=user_id, limit=100)
    
    # Calculate patterns
    intent_counts = {}
    emotion_counts = {}
    
    for interaction in interactions:
        intent_counts[interaction.intent] = intent_counts.get(interaction.intent, 0) + 1
        if interaction.emotion_type:
            emotion_counts[interaction.emotion_type] = emotion_counts.get(interaction.emotion_type, 0) + 1
    
    return {
        "user_id": user_id,
        "total_interactions": len(interactions),
        "intent_patterns": intent_counts,
        "emotion_patterns": emotion_counts,
        "repetition_index": sum(1 for i in interactions if i.is_routine) / len(interactions) if interactions else 0
    }
