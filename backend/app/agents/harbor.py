"""
Harbor - The Orientation Agent

Provides calm, repetitive-safe answers about date, time, location, and upcoming events.
Goal: Reduce panic through familiarity.
"""

from typing import Dict, Any
from datetime import datetime
from app.copilot_client import generate_response_sync, get_agent_system_prompt


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
        self.system_prompt = get_agent_system_prompt("harbor")
        self.fallback_message = "You're safe. Everything is okay. I'm here with you."

    def respond(
        self,
        query: str,
        user_data: Dict[str, Any],
        repetition_counter: int = 0,
        anxiety_score: float = 0.0
    ) -> Dict[str, Any]:
        """
        Generate orientation response using Copilot model
        """
        # Build context-aware prompt
        location = user_data.get("location", "home")
        current_time = datetime.now()
        time_of_day = self._get_time_of_day(current_time.hour)
        
        context_prompt = f"""The patient is asking: "{query}"

Context:
- Location: {location}
- Time: {time_of_day}, {current_time.strftime('%A, %B %d, %Y')}
- Repetition count: {repetition_counter} (if high, be extra patient and reassuring)
- Anxiety level: {anxiety_score:.1f}/1.0 (if high, prioritize calming)

Provide a warm, reassuring response about their orientation. Keep it to 2-3 short sentences."""

        # Generate response using Copilot model
        message = generate_response_sync(
            prompt=context_prompt,
            system_prompt=self.system_prompt,
            max_tokens=100,
            temperature=0.6
        )
        
        # Fallback if model fails
        if not message:
            message = self.fallback_message
        
        # Determine reassurance and followup based on anxiety
        reassurance_level = "high" if anxiety_score > 0.7 else "medium" if anxiety_score > 0.4 else "low"
        followup_suggestion = "call_family" if anxiety_score > 0.85 else "none"

        return {
            "message": message,
            "reassurance_level": reassurance_level,
            "followup_suggestion": followup_suggestion
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
