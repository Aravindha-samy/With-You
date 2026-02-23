#!/usr/bin/env python3
"""
Seed script to populate database with sample patient and caregiver data.
Run from backend directory: python seed_data.py
"""

from datetime import datetime, timedelta
from database import SessionLocal, engine, Base
from app.model.user import User
from app.model.mood_checkin import MoodCheckIn
from app.model.memory_card import MemoryCard
from app.model.emergency_contact import EmergencyContact
from app.model.agent_interaction import AgentInteraction, CognitiveInsight, CaregiverAlert

def seed_database():
    """Populate database with sample data"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(AgentInteraction).delete()
        db.query(CaregiverAlert).delete()
        db.query(CognitiveInsight).delete()
        db.query(MoodCheckIn).delete()
        db.query(MemoryCard).delete()
        db.query(EmergencyContact).delete()
        db.query(User).delete()
        db.commit()
        print("✓ Cleared existing data")
        
        # Create sample patients
        patients = [
            User(
                name="Margaret Johnson",
                email="margaret.johnson@example.com",
                user_type="patient",
                is_active=True
            ),
            User(
                name="David Smith",
                email="david.smith@example.com",
                user_type="patient",
                is_active=True
            ),
            User(
                name="Eleanor Thompson",
                email="eleanor.thompson@example.com",
                user_type="patient",
                is_active=True
            ),
        ]
        
        # Create sample caregivers
        caregivers = [
            User(
                name="Sarah Johnson",
                email="sarah.johnson@example.com",
                user_type="caregiver",
                is_active=True
            ),
            User(
                name="James Wilson",
                email="james.wilson@example.com",
                user_type="caregiver",
                is_active=True
            ),
        ]
        
        # Add users to database
        all_users = patients + caregivers
        db.add_all(all_users)
        db.commit()
        print(f"✓ Created {len(patients)} patients and {len(caregivers)} caregivers")
        
        # Refresh to get IDs
        for user in all_users:
            db.refresh(user)
        
        # Create family members for Margaret (patient 1)
        margaret = patients[0]
        family_members = [
            EmergencyContact(
                user_id=margaret.id,
                name="Sarah",
                phone="555-0101",
                email="sarah@example.com",
                relationship="Daughter",
                is_primary=True
            ),
            EmergencyContact(
                user_id=margaret.id,
                name="James",
                phone="555-0102",
                email="james@example.com",
                relationship="Son",
                is_primary=False
            ),
            EmergencyContact(
                user_id=margaret.id,
                name="Emma",
                phone="555-0103",
                email="emma@example.com",
                relationship="Granddaughter",
                is_primary=False
            ),
        ]
        db.add_all(family_members)
        db.commit()
        print(f"✓ Created {len(family_members)} family contacts for Margaret")
        
        # Create family members for David (patient 2)
        david = patients[1]
        family_members_david = [
            EmergencyContact(
                user_id=david.id,
                name="Lisa",
                phone="555-0201",
                email="lisa@example.com",
                relationship="Wife",
                is_primary=True
            ),
            EmergencyContact(
                user_id=david.id,
                name="Michael",
                phone="555-0202",
                email="michael@example.com",
                relationship="Son",
                is_primary=False
            ),
        ]
        db.add_all(family_members_david)
        db.commit()
        print(f"✓ Created {len(family_members_david)} family contacts for David")
        
        # Create memory cards for Margaret
        memories = [
            MemoryCard(
                user_id=margaret.id,
                title="Wedding Day",
                description="My beautiful wedding day with my husband. We were so happy!",
                image_url="https://via.placeholder.com/300x200?text=Wedding",
            ),
            MemoryCard(
                user_id=margaret.id,
                title="Family Vacation in Hawaii",
                description="Wonderful vacation with the whole family in 2015. We had such a great time!",
                image_url="https://via.placeholder.com/300x200?text=Hawaii",
            ),
            MemoryCard(
                user_id=margaret.id,
                title="Graduation Day",
                description="Sarah's graduation from university. We were so proud!",
                image_url="https://via.placeholder.com/300x200?text=Graduation",
            ),
        ]
        db.add_all(memories)
        db.commit()
        print(f"✓ Created {len(memories)} memory cards for Margaret")
        
        # Create memory cards for David
        memories_david = [
            MemoryCard(
                user_id=david.id,
                title="Our First House",
                description="The day we bought our first house together. A dream come true!",
                image_url="https://via.placeholder.com/300x200?text=House",
            ),
            MemoryCard(
                user_id=david.id,
                title="Golf Championship",
                description="Won the local golf championship in 1995. One of my proudest moments!",
                image_url="https://via.placeholder.com/300x200?text=Golf",
            ),
        ]
        db.add_all(memories_david)
        db.commit()
        print(f"✓ Created {len(memories_david)} memory cards for David")
        
        # Create mood check-ins for Margaret
        moods = ['Happy', 'Calm', 'Anxious', 'Confused', 'Sad', 'Content']
        now = datetime.utcnow()
        mood_checkins = []
        
        for i in range(14):
            mood_checkins.append(
                MoodCheckIn(
                    user_id=margaret.id,
                    mood=moods[i % len(moods)],
                    notes=f"Daily mood check-in - Day {i+1}",
                    timestamp=now - timedelta(days=14-i)
                )
            )
        
        db.add_all(mood_checkins)
        db.commit()
        print(f"✓ Created {len(mood_checkins)} mood check-ins for Margaret")
        
        # Create agent interactions for Margaret
        interactions = [
            AgentInteraction(
                user_id=margaret.id,
                agent_type="harbor",
                user_input="Where am I?",
                agent_response="You are at home in your living room. This is your safe space.",
                intent="location_awareness",
                emotion_score=0.7,
                emotion_type="calm",
                is_routine=True,
                timestamp=now - timedelta(hours=2)
            ),
            AgentInteraction(
                user_id=margaret.id,
                agent_type="roots",
                user_input="Tell me about my family",
                agent_response="You have a wonderful family. Your daughter Sarah visits every Sunday!",
                intent="family_recognition",
                emotion_score=0.8,
                emotion_type="happy",
                is_routine=True,
                timestamp=now - timedelta(hours=4)
            ),
            AgentInteraction(
                user_id=margaret.id,
                agent_type="solace",
                user_input="I feel anxious",
                agent_response="Let's take some deep breaths together. You are safe and loved.",
                intent="emotional_support",
                emotion_score=0.3,
                emotion_type="anxious",
                is_routine=False,
                timestamp=now - timedelta(hours=6)
            ),
            AgentInteraction(
                user_id=margaret.id,
                agent_type="legacy",
                user_input="Tell me a memory",
                agent_response="You had a beautiful wedding day. You looked so happy!",
                intent="memory_recall",
                emotion_score=0.9,
                emotion_type="happy",
                is_routine=False,
                timestamp=now - timedelta(hours=8)
            ),
        ]
        
        db.add_all(interactions)
        db.commit()
        print(f"✓ Created {len(interactions)} agent interactions for Margaret")
        
        # Create cognitive insights for Margaret
        insights = [
            CognitiveInsight(
                user_id=margaret.id,
                insight_type="anxiety_trend",
                metric_name="Anxiety Score",
                metric_value=0.35,
                period="weekly",
                description="Slight increase in anxiety over the past week"
            ),
            CognitiveInsight(
                user_id=margaret.id,
                insight_type="orientation_trend",
                metric_name="Orientation Index",
                metric_value=0.72,
                period="weekly",
                description="Good orientation to time and place"
            ),
            CognitiveInsight(
                user_id=margaret.id,
                insight_type="repetition",
                metric_name="Repeated Questions",
                metric_value=3.0,
                period="daily",
                description="Asked about location 3 times today - normal for patient"
            ),
            CognitiveInsight(
                user_id=margaret.id,
                insight_type="emotional_pattern",
                metric_name="Positive Emotions",
                metric_value=0.68,
                period="weekly",
                description="Strong positive emotional responses during family interactions"
            ),
        ]
        
        db.add_all(insights)
        db.commit()
        print(f"✓ Created {len(insights)} cognitive insights for Margaret")
        
        # Create caregiver alerts
        sarah_caregiver = caregivers[0]
        alerts = [
            CaregiverAlert(
                user_id=margaret.id,
                caregiver_id=sarah_caregiver.id,
                alert_type="high_anxiety",
                trigger_agent="solace",
                message="Margaret showed signs of anxiety. She expressed feeling worried about appointments.",
                is_acknowledged=True,
                acknowledged_at=now - timedelta(hours=5)
            ),
            CaregiverAlert(
                user_id=margaret.id,
                caregiver_id=sarah_caregiver.id,
                alert_type="needs_intervention",
                trigger_agent="harbor",
                message="Margaret asked about her location 5 times in the last 2 hours.",
                is_acknowledged=False,
            ),
            CaregiverAlert(
                user_id=david.id,
                caregiver_id=sarah_caregiver.id,
                alert_type="disorientation",
                trigger_agent="roots",
                message="David did not recognize family members in the photos shown to him.",
                is_acknowledged=True,
                acknowledged_at=now - timedelta(hours=24)
            ),
        ]
        
        db.add_all(alerts)
        db.commit()
        print(f"✓ Created {len(alerts)} caregiver alerts")
        
        print("\n✅ Database seeded successfully!")
        print("\nSample Users Created:")
        print("\nPatients:")
        for patient in patients:
            print(f"  - {patient.name} ({patient.email}) [ID: {patient.id}]")
        print("\nCaregivers:")
        for caregiver in caregivers:
            print(f"  - {caregiver.name} ({caregiver.email}) [ID: {caregiver.id}]")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
