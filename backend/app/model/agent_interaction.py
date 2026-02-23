from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from datetime import datetime
from database import Base


class AgentInteraction(Base):
    __tablename__ = "agent_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    agent_type = Column(String(50), nullable=False)  # aurora, harbor, roots, solace, legacy, echo, guardian
    user_input = Column(Text, nullable=False)
    agent_response = Column(Text, nullable=False)
    intent = Column(String(100), nullable=True)  # event, location, identity, emotional, story
    emotion_score = Column(Float, nullable=True)  # 0-1 scale
    emotion_type = Column(String(50), nullable=True)  # sad, anxious, calm, happy, etc.
    is_routine = Column(Boolean, default=False)  # For tracking repetition patterns
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class CognitiveInsight(Base):
    __tablename__ = "cognitive_insights"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    insight_type = Column(String(50), nullable=False)  # anxiety_trend, orientation_trend, repetition, emotional_pattern
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    period = Column(String(20), nullable=False)  # daily, weekly, monthly
    description = Column(Text, nullable=True)
    calculated_at = Column(DateTime, default=datetime.utcnow)


class CaregiverAlert(Base):
    __tablename__ = "caregiver_alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    caregiver_id = Column(Integer, index=True, nullable=False)
    alert_type = Column(String(50), nullable=False)  # high_anxiety, disorientation, health_concern, needs_intervention
    trigger_agent = Column(String(50), nullable=True)  # Which agent triggered this
    message = Column(Text, nullable=False)
    is_acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
