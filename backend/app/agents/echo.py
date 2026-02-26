"""
Echo - Memory Layer Agent

Persistent memory intelligence for tracking patterns and computing metrics.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.copilot_client import generate_response_sync, get_agent_system_prompt


class Echo:
    """
    Echo - Persistent Memory Intelligence

    Responsibilities:
    - Store structured logs
    - Track cognitive patterns
    - Compute Cognitive Stability Index (CSI)
    - Identify trend shifts
    """

    def __init__(self):
        self.system_prompt = get_agent_system_prompt("echo")

    def log_interaction(
        self,
        db,
        user_id: int,
        question: str,
        response: str,
        agent_type: str,
        intent: str,
        emotion_score: float,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Log interaction to database

        Returns:
        {
            "memory_write_status": "success",
            "CSI_updated": true/false,
            "drift_flag": true/false
        }
        """

        from app.model.interaction import Interaction
        from sqlalchemy import func

        # Check for recent repetitions
        recent_time = datetime.utcnow() - timedelta(hours=1)
        repetition_count = db.query(func.count(Interaction.id)).filter(
            Interaction.user_id == user_id,
            Interaction.question.like(f"%{question[:20]}%"),
            Interaction.timestamp >= recent_time
        ).scalar() or 0

        # Create interaction log
        interaction = Interaction(
            user_id=user_id,
            question=question,
            response=response,
            agent_type=agent_type,
            intent=intent,
            emotion_score=emotion_score,
            repetition_count=repetition_count + 1,
            session_id=session_id
        )

        db.add(interaction)
        db.commit()

        # Update CSI if needed (weekly)
        csi_updated = False
        drift_flag = False

        # Check if CSI update is due
        if self._should_update_csi(db, user_id):
            csi_updated = True
            drift_flag = self._compute_csi(db, user_id)

        return {
            "memory_write_status": "success",
            "CSI_updated": csi_updated,
            "drift_flag": drift_flag
        }

    def track_repetition(self, db, user_id: int, query: str) -> int:
        """Track how many times a similar query was asked"""
        from app.model.interaction import Interaction
        from sqlalchemy import func

        recent_time = datetime.utcnow() - timedelta(hours=24)

        count = db.query(func.count(Interaction.id)).filter(
            Interaction.user_id == user_id,
            Interaction.question.like(f"%{query[:30]}%"),
            Interaction.timestamp >= recent_time
        ).scalar() or 0

        return count

    def compute_emotional_variance(self, db, user_id: int, days: int = 7) -> float:
        """Compute emotional variance over time"""
        from app.model.interaction import Interaction
        from sqlalchemy import func

        start_time = datetime.utcnow() - timedelta(days=days)

        # Get average emotion score
        avg_emotion = db.query(func.avg(Interaction.emotion_score)).filter(
            Interaction.user_id == user_id,
            Interaction.timestamp >= start_time,
            Interaction.emotion_score.isnot(None)
        ).scalar() or 0.5

        return avg_emotion

    def _should_update_csi(self, db, user_id: int) -> bool:
        """Check if CSI should be updated"""
        from app.model.cognitive_metric import CognitiveMetric

        last_metric = db.query(CognitiveMetric).filter(
            CognitiveMetric.user_id == user_id
        ).order_by(CognitiveMetric.created_at.desc()).first()

        if not last_metric:
            return True

        # Update weekly
        days_since = (datetime.utcnow() - last_metric.created_at).days
        return days_since >= 7

    def _compute_csi(self, db, user_id: int) -> bool:
        """Compute Cognitive Stability Index"""
        from app.model.cognitive_metric import CognitiveMetric
        from app.model.interaction import Interaction
        from sqlalchemy import func

        # Get metrics from last 7 days
        week_ago = datetime.utcnow() - timedelta(days=7)

        # Orientation frequency
        orientation_count = db.query(func.count(Interaction.id)).filter(
            Interaction.user_id == user_id,
            Interaction.intent == "orientation",
            Interaction.timestamp >= week_ago
        ).scalar() or 0

        # Average anxiety
        avg_anxiety = db.query(func.avg(Interaction.emotion_score)).filter(
            Interaction.user_id == user_id,
            Interaction.timestamp >= week_ago,
            Interaction.emotion_score.isnot(None)
        ).scalar() or 0.5

        # Repetition pattern
        avg_repetition = db.query(func.avg(Interaction.repetition_count)).filter(
            Interaction.user_id == user_id,
            Interaction.timestamp >= week_ago
        ).scalar() or 1.0

        # Compute CSI (simplified formula)
        csi_score = 1.0 - (
            (orientation_count / 50.0) * 0.3 +
            avg_anxiety * 0.4 +
            (min(avg_repetition, 5.0) / 5.0) * 0.3
        )
        csi_score = max(0.0, min(1.0, csi_score))

        # Determine drift flag
        drift_flag = csi_score < 0.6

        # Save metric
        metric = CognitiveMetric(
            user_id=user_id,
            csi_score=csi_score,
            orientation_frequency=orientation_count,
            anxiety_average=avg_anxiety,
            period_start=week_ago,
            period_end=datetime.utcnow(),
            cognitive_drift="declining" if drift_flag else "stable"
        )

        db.add(metric)
        db.commit()

        return drift_flag

    def analyze_memory_pattern(self, memory_log: str) -> Dict[str, Any]:
        """
        Analyze memory patterns using Copilot model
        """
        context_prompt = f"""Analyze the following memory/interaction log and identify patterns:

{memory_log}

Identify:
1. Repetition patterns (same questions asked multiple times)
2. Emotional trends (increasing/decreasing anxiety)
3. Cognitive patterns (orientation confusion, identity questions)
4. Any concerning changes

Provide a brief, objective analysis."""

        analysis = generate_response_sync(
            prompt=context_prompt,
            system_prompt=self.system_prompt,
            max_tokens=200,
            temperature=0.4
        )
        
        if not analysis:
            analysis = "Unable to analyze patterns at this time."

        return {
            "analysis": analysis
        }


# Singleton instance
echo = Echo()
