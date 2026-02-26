from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base


class MoodCheckIn(Base):
    __tablename__ = "mood_checkins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    mood = Column(String(50), nullable=False)  # happy, sad, anxious, calm, etc.
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
