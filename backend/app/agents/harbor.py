"""
Harbor - The Orientation Agent

Provides calm, repetitive-safe answers about date, time, location, and upcoming events.
Goal: Reduce panic through familiarity.
"""

from typing import Dict, Any
from datetime import datetime


class Harbor:
    """
    Harbor - Orientation and Grounding Agent

    Purpose:
    - Provide calm answers about date, time, location
    - Handle upcoming events and daily structure
    - Reduce panic through familiarity
    """

    def __init__(self):
        self.tone = "warm, steady, low complexity, reassuring"

    def respond(
        self,
        query: str,
        user_data: Dict[str, Any],
        repetition_counter: int = 0,
        anxiety_score: float = 0.0
    ) -> Dict[str, Any]:
        """
        Generate orientation response

        Returns:
        {
            "message": "User-facing response",
            "reassurance_level": "low|medium|high",
            "followup_suggestion": "none|call_family|play_memory"
        }
        """

        current_time = datetime.now()
        day_name = current_time.strftime("%A")
        time_of_day = self._get_time_of_day(current_time.hour)

        # Base orientation message
        location = user_data.get("location", "home")
        message = f"You're at {location}. You're safe. It's {day_name} {time_of_day}."

        # Add reinforcement if high repetition
        reassurance_level = "low"
        if repetition_counter > 3:
            message += " Everything is okay."
            reassurance_level = "medium"

        # Add grounding if high anxiety
        if anxiety_score > 0.8:
            message += " Take a deep breath. You're in a familiar place."
            reassurance_level = "high"

        # Determine follow-up
        followup = "none"
        if repetition_counter > 5 or anxiety_score > 0.85:
            followup = "call_family"

        return {
            "message": message,
            "reassurance_level": reassurance_level,
            "followup_suggestion": followup
        }

    def get_scheduled_events(self, events: list) -> Dict[str, Any]:
        """Get today's scheduled events"""
        if not events:
            return {
                "message": "No visits or appointments scheduled for today.",
                "reassurance_level": "low",
                "followup_suggestion": "none"
            }

        event_list = "\n".join(
            [f"- {e['title']} at {e['time']}" for e in events[:3]])
        message = f"Here's what's happening today:\n{event_list}"

        return {
            "message": message,
            "reassurance_level": "low",
            "followup_suggestion": "none"
        }

    def _get_time_of_day(self, hour: int) -> str:
        """Get time of day description"""
        if hour < 12:
            return "morning"
        elif hour < 17:
            return "afternoon"
        else:
            return "evening"


# Singleton instance
harbor = Harbor()
