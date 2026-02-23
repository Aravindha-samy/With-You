from sqlalchemy.orm import Session
from datetime import datetime
from app.model import User, MoodCheckIn, MemoryCard, EmergencyContact, AgentInteraction, CognitiveInsight, CaregiverAlert
from app import schemas


# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(
        name=user.name,
        email=user.email,
        user_type=user.user_type
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# Mood Check-in CRUD operations
def create_mood_checkin(db: Session, checkin: schemas.MoodCheckInCreate):
    db_checkin = MoodCheckIn(
        user_id=checkin.user_id,
        mood=checkin.mood,
        notes=checkin.notes
    )
    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)
    return db_checkin


def get_mood_checkins(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(MoodCheckIn).filter(
        MoodCheckIn.user_id == user_id
    ).offset(skip).limit(limit).all()


def get_mood_checkin(db: Session, checkin_id: int):
    return db.query(MoodCheckIn).filter(
        MoodCheckIn.id == checkin_id
    ).first()


def delete_mood_checkin(db: Session, checkin_id: int):
    db_checkin = db.query(MoodCheckIn).filter(
        MoodCheckIn.id == checkin_id
    ).first()
    if db_checkin:
        db.delete(db_checkin)
        db.commit()
    return db_checkin


# Memory Card CRUD operations
def create_memory_card(db: Session, card: schemas.MemoryCardCreate):
    db_card = MemoryCard(
        user_id=card.user_id,
        title=card.title,
        description=card.description,
        image_url=card.image_url
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def get_memory_cards(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(MemoryCard).filter(
        MemoryCard.user_id == user_id
    ).offset(skip).limit(limit).all()


def get_memory_card(db: Session, card_id: int):
    return db.query(MemoryCard).filter(
        MemoryCard.id == card_id
    ).first()


def update_memory_card(db: Session, card_id: int, card: schemas.MemoryCardUpdate):
    db_card = db.query(MemoryCard).filter(
        MemoryCard.id == card_id
    ).first()
    if not db_card:
        return None
    for key, value in card.dict(exclude_unset=True).items():
        setattr(db_card, key, value)
    db_card.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_card)
    return db_card


def delete_memory_card(db: Session, card_id: int):
    db_card = db.query(MemoryCard).filter(
        MemoryCard.id == card_id
    ).first()
    if db_card:
        db.delete(db_card)
        db.commit()
    return db_card


# Emergency Contact CRUD operations
def create_emergency_contact(db: Session, contact: schemas.EmergencyContactCreate):
    db_contact = EmergencyContact(
        user_id=contact.user_id,
        name=contact.name,
        phone=contact.phone,
        email=contact.email,
        relationship=contact.relationship,
        is_primary=contact.is_primary
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_emergency_contacts(db: Session, user_id: int):
    return db.query(EmergencyContact).filter(
        EmergencyContact.user_id == user_id
    ).all()


def get_emergency_contact(db: Session, contact_id: int):
    return db.query(EmergencyContact).filter(
        EmergencyContact.id == contact_id
    ).first()


def update_emergency_contact(db: Session, contact_id: int, contact: schemas.EmergencyContactUpdate):
    db_contact = db.query(EmergencyContact).filter(
        EmergencyContact.id == contact_id
    ).first()
    if not db_contact:
        return None
    for key, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_emergency_contact(db: Session, contact_id: int):
    db_contact = db.query(EmergencyContact).filter(
        EmergencyContact.id == contact_id
    ).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


# Agent Interaction CRUD operations
def create_agent_interaction(db: Session, interaction: schemas.AgentInteractionCreate):
    db_interaction = AgentInteraction(
        user_id=interaction.user_id,
        agent_type=interaction.agent_type,
        user_input=interaction.user_input,
        agent_response=interaction.agent_response,
        intent=interaction.intent,
        emotion_score=interaction.emotion_score,
        emotion_type=interaction.emotion_type,
        is_routine=interaction.is_routine
    )
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction


def get_agent_interactions(db: Session, user_id: int, agent_type: str = None, skip: int = 0, limit: int = 100):
    query = db.query(AgentInteraction).filter(AgentInteraction.user_id == user_id)
    if agent_type:
        query = query.filter(AgentInteraction.agent_type == agent_type)
    return query.offset(skip).limit(limit).all()


def get_agent_interaction(db: Session, interaction_id: int):
    return db.query(AgentInteraction).filter(
        AgentInteraction.id == interaction_id
    ).first()


def delete_agent_interaction(db: Session, interaction_id: int):
    db_interaction = db.query(AgentInteraction).filter(
        AgentInteraction.id == interaction_id
    ).first()
    if db_interaction:
        db.delete(db_interaction)
        db.commit()
    return db_interaction


# Cognitive Insight CRUD operations
def create_cognitive_insight(db: Session, insight: schemas.CognitiveInsightCreate):
    db_insight = CognitiveInsight(
        user_id=insight.user_id,
        insight_type=insight.insight_type,
        metric_name=insight.metric_name,
        metric_value=insight.metric_value,
        period=insight.period,
        description=insight.description
    )
    db.add(db_insight)
    db.commit()
    db.refresh(db_insight)
    return db_insight


def get_cognitive_insights(db: Session, user_id: int, insight_type: str = None, period: str = None, skip: int = 0, limit: int = 100):
    query = db.query(CognitiveInsight).filter(CognitiveInsight.user_id == user_id)
    if insight_type:
        query = query.filter(CognitiveInsight.insight_type == insight_type)
    if period:
        query = query.filter(CognitiveInsight.period == period)
    return query.offset(skip).limit(limit).all()


def get_cognitive_insight(db: Session, insight_id: int):
    return db.query(CognitiveInsight).filter(
        CognitiveInsight.id == insight_id
    ).first()


def delete_cognitive_insight(db: Session, insight_id: int):
    db_insight = db.query(CognitiveInsight).filter(
        CognitiveInsight.id == insight_id
    ).first()
    if db_insight:
        db.delete(db_insight)
        db.commit()
    return db_insight


# Caregiver Alert CRUD operations
def create_caregiver_alert(db: Session, alert: schemas.CaregiverAlertCreate):
    db_alert = CaregiverAlert(
        user_id=alert.user_id,
        caregiver_id=alert.caregiver_id,
        alert_type=alert.alert_type,
        message=alert.message,
        trigger_agent=alert.trigger_agent
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def get_caregiver_alerts(db: Session, caregiver_id: int, acknowledged: bool = None, skip: int = 0, limit: int = 100):
    query = db.query(CaregiverAlert).filter(CaregiverAlert.caregiver_id == caregiver_id)
    if acknowledged is not None:
        query = query.filter(CaregiverAlert.is_acknowledged == acknowledged)
    return query.offset(skip).limit(limit).all()


def get_user_alerts(db: Session, user_id: int, acknowledged: bool = None, skip: int = 0, limit: int = 100):
    query = db.query(CaregiverAlert).filter(CaregiverAlert.user_id == user_id)
    if acknowledged is not None:
        query = query.filter(CaregiverAlert.is_acknowledged == acknowledged)
    return query.offset(skip).limit(limit).all()


def get_caregiver_alert(db: Session, alert_id: int):
    return db.query(CaregiverAlert).filter(
        CaregiverAlert.id == alert_id
    ).first()


def update_caregiver_alert(db: Session, alert_id: int, alert: schemas.CaregiverAlertUpdate):
    db_alert = db.query(CaregiverAlert).filter(
        CaregiverAlert.id == alert_id
    ).first()
    if not db_alert:
        return None
    for key, value in alert.dict(exclude_unset=True).items():
        if key == "acknowledged_at" and alert.is_acknowledged:
            setattr(db_alert, key, datetime.utcnow())
        else:
            setattr(db_alert, key, value)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def delete_caregiver_alert(db: Session, alert_id: int):
    db_alert = db.query(CaregiverAlert).filter(
        CaregiverAlert.id == alert_id
    ).first()
    if db_alert:
        db.delete(db_alert)
        db.commit()
    return db_alert
