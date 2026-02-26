from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from database import Base


class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    # "daughter", "son", "spouse", etc.
    relationship_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    importance_level = Column(Integer, default=5)  # 1-10 scale
    photo_url = Column(String(500), nullable=True)
    shared_memories = Column(Text, nullable=True)  # JSON string of memory IDs
    last_visit = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
