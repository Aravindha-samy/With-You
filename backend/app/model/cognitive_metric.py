from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey, Text
from datetime import datetime
from database import Base


class CognitiveMetric(Base):
    __tablename__ = "cognitive_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Cognitive Stability Index
    csi_score = Column(Float, nullable=True)  # 0.0 to 1.0

    # Orientation metrics
    orientation_frequency = Column(Integer, default=0)
    orientation_repetition = Column(Integer, default=0)

    # Anxiety metrics
    anxiety_average = Column(Float, default=0.0)
    anxiety_peak = Column(Float, default=0.0)

    # Repetition patterns
    repetition_pattern = Column(Text, nullable=True)  # JSON string

    # Escalation flags
    # "none", "monitor", "intervene"
    escalation_flag = Column(String(50), default="none")

    # Trend data
    # "stable", "declining", "improving"
    emotional_trend = Column(String(50), default="stable")
    # "stable", "declining", "improving"
    cognitive_drift = Column(String(50), default="stable")

    # Period
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
