"""
Guardian - Caregiver Agent

Generates summaries, trends, and alerts for caregivers.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.copilot_client import generate_response_sync, get_agent_system_prompt


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
        self.system_prompt = get_agent_system_prompt("guardian")

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
            # Use Copilot to generate a helpful message when no data
            message = generate_response_sync(
                prompt="There are no patient interactions recorded for today. Generate a brief, helpful message for the caregiver.",
                system_prompt=self.system_prompt,
                max_tokens=60,
                temperature=0.5
            )
            if not message:
                message = "No interactions recorded today."
            
            return {
                "summary": message,
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
        """Generate weekly cognitive report using Copilot model"""
        from app.model.cognitive_metric import CognitiveMetric

        # Get latest metric
        metric = db.query(CognitiveMetric).filter(
            CognitiveMetric.user_id == user_id
        ).order_by(CognitiveMetric.created_at.desc()).first()

        if not metric:
            # Use Copilot to generate helpful message
            message = generate_response_sync(
                prompt="There is no cognitive data available for the weekly report yet. Generate a brief, helpful message for the caregiver explaining this.",
                system_prompt=self.system_prompt,
                max_tokens=80,
                temperature=0.5
            )
            if not message:
                message = "No data available for weekly report. Continue monitoring for more insights."
            
            return {
                "summary": message,
                "emotional_trend": "stable",
                "orientation_trend": "stable",
                "alert_level": "none"
            }

        # Build context for Copilot analysis
        context_prompt = f"""Generate a weekly cognitive health summary for a caregiver based on this data:

- CSI Score: {metric.csi_score:.2f} (1.0 = stable, lower = more challenges)
- Orientation question frequency: {metric.orientation_frequency} times this week
- Average anxiety level: {metric.anxiety_average:.2f} (0.0 = calm, 1.0 = highly anxious)
- Cognitive drift: {metric.cognitive_drift}

Provide a brief, professional summary (2-3 sentences) with actionable insights for the caregiver."""

        summary = generate_response_sync(
            prompt=context_prompt,
            system_prompt=self.system_prompt,
            max_tokens=150,
            temperature=0.5
        )
        
        if not summary:
            summary = f"CSI Score: {metric.csi_score:.2f}. "
            summary += f"Orientation frequency: {metric.orientation_frequency}. "
            summary += f"Average anxiety: {metric.anxiety_average:.2f}. "

        return {
            "summary": summary,
            "emotional_trend": metric.emotional_trend if hasattr(metric, 'emotional_trend') else "stable",
            "orientation_trend": metric.cognitive_drift,
            "alert_level": metric.escalation_flag if hasattr(metric, 'escalation_flag') else "none"
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

    def generate_caregiver_summary(self, patient_data: str) -> Dict[str, Any]:
        """
        Generate caregiver summary using Copilot model
        """
        context_prompt = f"""Generate a comprehensive caregiver summary based on this patient data:

{patient_data}

Provide:
1. Overview of patient's current state
2. Key observations and patterns
3. Recommendations for the caregiver
4. Any areas requiring attention

Keep it professional, compassionate, and actionable."""

        summary = generate_response_sync(
            prompt=context_prompt,
            system_prompt=self.system_prompt,
            max_tokens=200,
            temperature=0.5
        )
        
        if not summary:
            summary = "Unable to generate summary at this time. Please review patient data manually."

        return {
            "summary": summary
        }


# Singleton instance
guardian = Guardian()
