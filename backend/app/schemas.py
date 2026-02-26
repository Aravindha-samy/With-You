from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr
    user_type: str  # "patient" or "caregiver"


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class MoodCheckInBase(BaseModel):
    mood: str
    notes: Optional[str] = None


class MoodCheckInCreate(MoodCheckInBase):
    user_id: int


class MoodCheckIn(MoodCheckInBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class MemoryCardBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None


class MemoryCardCreate(MemoryCardBase):
    user_id: int


class MemoryCardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class MemoryCard(MemoryCardBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmergencyContactBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    relationship: Optional[str] = None
    is_primary: bool = False


class EmergencyContactCreate(EmergencyContactBase):
    user_id: int


class EmergencyContactUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    relationship: Optional[str] = None
    is_primary: Optional[bool] = None


class EmergencyContact(EmergencyContactBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Agent Interaction Schemas
class AgentInteractionBase(BaseModel):
    agent_type: str
    user_input: str
    agent_response: str
    intent: Optional[str] = None
    emotion_score: Optional[float] = None
    emotion_type: Optional[str] = None
    is_routine: bool = False


class AgentInteractionCreate(AgentInteractionBase):
    user_id: int


class AgentInteraction(AgentInteractionBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# Cognitive Insight Schemas
class CognitiveInsightBase(BaseModel):
    insight_type: str
    metric_name: str
    metric_value: float
    period: str
    description: Optional[str] = None


class CognitiveInsightCreate(CognitiveInsightBase):
    user_id: int


class CognitiveInsight(CognitiveInsightBase):
    id: int
    user_id: int
    calculated_at: datetime

    class Config:
        from_attributes = True


# Caregiver Alert Schemas
class CaregiverAlertBase(BaseModel):
    alert_type: str
    message: str
    trigger_agent: Optional[str] = None


class CaregiverAlertCreate(CaregiverAlertBase):
    user_id: int
    caregiver_id: int


class CaregiverAlertUpdate(BaseModel):
    is_acknowledged: Optional[bool] = None
    acknowledged_at: Optional[datetime] = None


class CaregiverAlert(CaregiverAlertBase):
    id: int
    user_id: int
    caregiver_id: int
    is_acknowledged: bool
    acknowledged_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Agent Request Schemas (for calling agents)
class AgentRequest(BaseModel):
    user_id: int
    user_input: str
    agent_type: Optional[str] = None  # If None, Aurora will route
    voice_enabled: Optional[bool] = False
    session_id: Optional[str] = None


class AgentResponse(BaseModel):
    agent_type: str
    response: str
    intent: Optional[str] = None
    emotion_score: Optional[float] = None
    emotion_type: Optional[str] = None
    alert_triggered: Optional[bool] = False
    alert_message: Optional[str] = None
