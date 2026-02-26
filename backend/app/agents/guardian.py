"""
Guardian - Caregiver Agent

Generates summaries, trends, and alerts for caregivers.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta


class Guardian:
    """
    Guardian - Caregiver Co-Pilot

    Generates:
    - Daily summaries
    - Emotional trends
    - Cognitive alerts
    - Predictive warnings
    """

    def __init__(self):
        pass

    def generate_daily_summary(
        self,
        db,
        user_id: int,
        date: datetime = None
    ) -> Dict[str, Any]:
        """
        Generate daily summary for caregiver

        Returns:
        {
            "summary": "...",
            "emotional_trend": "stable|declining|improving",
            "orientation_trend": "stable|declining",
            "alert_level": "none|monitor|intervene"
        }
        """

        from app.model.interaction import Interaction
        from sqlalchemy import func

        if date is None:
            date = datetime.utcnow()

        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = date.replace(
            hour=23, minute=59, second=59, microsecond=999999)

        # Get interactions for the day
        interactions = db.query(Interaction).filter(
            Interaction.user_id == user_id,
            Interaction.timestamp >= start_of_day,
            Interaction.timestamp <= end_of_day
        ).all()

        if not interactions:
            return {
                "summary": "No interactions recorded today.",
                "emotional_trend": "stable",
                "orientation_trend": "stable",
                "alert_level": "none"
            }

        # Compute metrics
        total_interactions = len(interactions)
        orientation_queries = sum(
            1 for i in interactions if i.intent == "orientation")
        avg_emotion = sum(
            i.emotion_score or 0.5 for i in interactions) / total_interactions
        max_repetition = max(i.repetition_count for i in interactions)

        # Generate summary text
        summary = f"Total interactions: {total_interactions}. "
        summary += f"Orientation queries: {orientation_queries}. "
        summary += f"Average emotional state: {avg_emotion:.2f}. "

        # Determine trends
        emotional_trend = "stable"
        if avg_emotion > 0.7:
            emotional_trend = "declining"
        elif avg_emotion < 0.4:
            emotional_trend = "improving"

        orientation_trend = "stable"
        if orientation_queries > 10:
            orientation_trend = "declining"

        # Determine alert level
        alert_level = "none"
        if avg_emotion > 0.8 or max_repetition > 5:
            alert_level = "intervene"
        elif avg_emotion > 0.6 or orientation_queries > 8:
            alert_level = "monitor"

        return {
            "summary": summary,
            "emotional_trend": emotional_trend,
            "orientation_trend": orientation_trend,
            "alert_level": alert_level
        }

    def generate_weekly_report(self, db, user_id: int) -> Dict[str, Any]:
        """Generate weekly cognitive report"""
        from app.model.cognitive_metric import CognitiveMetric

        # Get latest metric
        metric = db.query(CognitiveMetric).filter(
            CognitiveMetric.user_id == user_id
        ).order_by(CognitiveMetric.created_at.desc()).first()

        if not metric:
            return {
                "summary": "No data available for weekly report.",
                "emotional_trend": "stable",
                "orientation_trend": "stable",
                "alert_level": "none"
            }

        summary = f"CSI Score: {metric.csi_score:.2f}. "
        summary += f"Orientation frequency: {metric.orientation_frequency}. "
        summary += f"Average anxiety: {metric.anxiety_average:.2f}. "

        return {
            "summary": summary,
            "emotional_trend": metric.emotional_trend,
            "orientation_trend": metric.cognitive_drift,
            "alert_level": metric.escalation_flag
        }

    def check_intervention_needed(self, db, user_id: int) -> bool:
        """Check if immediate caregiver intervention is needed"""
        from app.model.interaction import Interaction
        from sqlalchemy import func

        # Check last hour
        hour_ago = datetime.utcnow() - timedelta(hours=1)

        # High anxiety in last hour
        high_anxiety_count = db.query(func.count(Interaction.id)).filter(
            Interaction.user_id == user_id,
            Interaction.timestamp >= hour_ago,
            Interaction.emotion_score > 0.85
        ).scalar() or 0

        # High repetition in last hour
        high_repetition = db.query(func.max(Interaction.repetition_count)).filter(
            Interaction.user_id == user_id,
            Interaction.timestamp >= hour_ago
        ).scalar() or 0

        return high_anxiety_count >= 3 or high_repetition >= 5


# Singleton instance
guardian = Guardian()
