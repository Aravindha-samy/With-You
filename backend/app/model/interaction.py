from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from datetime import datetime
from database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    # "aurora", "harbor", "roots", "solace", "legacy", "echo", "guardian"
    agent_type = Column(String(50), nullable=False)
    intent = Column(String(100), nullable=True)
    emotion_score = Column(Float, nullable=True)
    emotion_type = Column(String(50), nullable=True)
    repetition_count = Column(Integer, default=1)
    session_id = Column(String(100), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
