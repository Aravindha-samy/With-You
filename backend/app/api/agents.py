from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from database import get_db
from typing import Optional
from app.agents import aurora, harbor, roots, solace, legacy, echo, guardian
import uuid

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/ask", response_model=schemas.AgentResponse)
def ask_agent(request: schemas.AgentRequest, db: Session = Depends(get_db)):
    """
    Main entry point for patient queries - Aurora Orchestrator

    Aurora (Orchestrator) will:
    1. Analyze user_input
    2. Detect intent and emotion
    3. Route to appropriate agent (Harbor, Roots, Solace, Legacy, etc.)
    4. Get response from agent
    5. Log interaction via Echo
    6. Return response
    """

    # Verify user exists
    user = crud.get_user(db, user_id=request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())

    # Track repetition
    repetition_count = echo.track_repetition(
        db, request.user_id, request.user_input)

    # Aurora analyzes the input
    analysis = aurora.analyze_input(
        user_input=request.user_input,
        user_id=request.user_id,
        session_history=[],
        repetition_counter=repetition_count,
        csi=1.0
    )

    # Route to appropriate agent
    target_agent = analysis["target_agent"]
    response_text = ""
    alert_triggered = False

    if target_agent == "harbor":
        # Get user data
        user_data = {"location": "home"}  # TODO: Get from user profile
        harbor_response = harbor.respond(
            query=request.user_input,
            user_data=user_data,
            repetition_counter=repetition_count,
            anxiety_score=analysis["emotional_score"]
        )
        response_text = harbor_response["message"]
        alert_triggered = harbor_response["followup_suggestion"] == "call_family"

    elif target_agent == "roots":
        # Get relationship data if asking about someone
        # TODO: Parse person name from query and fetch from DB
        roots_response = roots.respond(
            query=request.user_input,
            person_node=None,
            anxiety_high=analysis["emotional_score"] > 0.8
        )
        response_text = roots_response["message"]
        alert_triggered = roots_response["suggest_call"]

    elif target_agent == "solace":
        solace_response = solace.respond(
            query=request.user_input,
            anxiety_score=analysis["emotional_score"],
            repetition_count=repetition_count
        )
        response_text = solace_response["message"]
        alert_triggered = solace_response["caregiver_alert"]

    elif target_agent == "legacy":
        # TODO: Get life stories from memory cards
        legacy_response = legacy.respond(
            query=request.user_input,
            life_stories=[]
        )
        response_text = legacy_response["message"]

    else:
        # Default to Solace for safety
        response_text = "I'm here with you. How can I help?"

    # Log interaction via Echo
    echo.log_interaction(
        db=db,
        user_id=request.user_id,
        question=request.user_input,
        response=response_text,
        agent_type=target_agent,
        intent=analysis["intent"],
        emotion_score=analysis["emotional_score"],
        session_id=session_id
    )

    # Check if caregiver intervention needed
    if guardian.check_intervention_needed(db, request.user_id):
        alert_triggered = True

    response = schemas.AgentResponse(
        agent_type=target_agent,
        response=response_text,
        intent=analysis["intent"],
        emotion_score=analysis["emotional_score"],
        emotion_type="anxious" if analysis["emotional_score"] > 0.7 else "calm",
        alert_triggered=alert_triggered
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
    memories = crud.get_memory_cards(
        db=db, user_id=user_id, skip=skip, limit=limit)

    return {
        "stories": memories,
        "total": len(memories)
    }


@router.get("/guardian/dashboard/{user_id}")
def get_guardian_dashboard(user_id: int, db: Session = Depends(get_db)):
    """
    Guardian Agent: Get caregiver dashboard insights

    Returns:
    - Daily summary
    - Emotional trends
    - Orientation trends
    - Alerts for caregiver
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate daily summary using Guardian agent
    daily_summary = guardian.generate_daily_summary(db, user_id)

    # Generate weekly report
    weekly_report = guardian.generate_weekly_report(db, user_id)

    # Check intervention needed
    intervention_needed = guardian.check_intervention_needed(db, user_id)

    return {
        "user_id": user_id,
        "daily_summary": daily_summary,
        "weekly_report": weekly_report,
        "intervention_needed": intervention_needed
    }


@router.get("/echo/patterns/{user_id}")
def get_memory_patterns(user_id: int, db: Session = Depends(get_db)):
    """
    Echo Agent: Get memory and behavior patterns

    Returns:
    - Repetition frequency
    - Anxiety patterns
    - Emotional trends
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get emotional variance
    emotional_variance = echo.compute_emotional_variance(db, user_id, days=7)

    return {
        "user_id": user_id,
        "emotional_variance": emotional_variance,
        "status": "analysis_complete"
    }
