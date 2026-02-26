"""
Solace - Emotional Intelligence Agent

Detects and regulates emotional distress.
Protects emotional safety and dignity.
"""

from typing import Dict, Any


class Solace:
    """
    Solace - Emotional Stabilization Agent

    Primary directive:
    - Reduce fear
    - Preserve dignity
    - Increase safety perception
    """

    def __init__(self):
        self.tone = "gentle, reassuring, validating"
        self.calm_protocols = {
            "breathing": "Let's take a slow breath together. In... and out... You're doing great.",
            "memory_music": "Would you like to listen to some familiar music?",
            "family_voice": "Would you like to hear a message from your family?",
            "none": "I'm here with you. You're safe."
        }

    def respond(
        self,
        query: str,
        anxiety_score: float,
        repetition_count: int = 0,
        last_interactions: list = None
    ) -> Dict[str, Any]:
        """
        Generate emotional support response

        Returns:
        {
            "message": "User-facing response",
            "calm_protocol": "none|breathing|memory_music|family_voice",
            "caregiver_alert": true/false
        }
        """

        # Detect distress triggers
        distress_keywords = ["scared", "afraid",
                             "help", "don't know where", "lost"]
        is_distressed = any(word in query.lower()
                            for word in distress_keywords)

        # Base reassurance message
        message = "It's okay. You're safe. I'm here with you."

        # Determine calm protocol
        calm_protocol = "none"
        if anxiety_score > 0.8 or is_distressed:
            calm_protocol = "breathing"
            message = self.calm_protocols["breathing"]
        elif anxiety_score > 0.6:
            message += " Everything is alright."

        # Determine if caregiver alert needed
        caregiver_alert = False
        if anxiety_score > 0.9 or repetition_count >= 5:
            caregiver_alert = True

        return {
            "message": message,
            "calm_protocol": calm_protocol,
            "caregiver_alert": caregiver_alert
        }

    def activate_calm_mode(self, protocol: str = "breathing") -> Dict[str, Any]:
        """Activate specific calm mode protocol"""
        message = self.calm_protocols.get(
            protocol, self.calm_protocols["none"])

        return {
            "message": message,
            "calm_protocol": protocol,
            "caregiver_alert": False
        }

    def validate_emotion(self, emotion: str) -> str:
        """Validate and acknowledge emotion without dismissing"""
        validations = {
            "confused": "It's natural to feel confused sometimes. You're not alone.",
            "scared": "Feeling scared is okay. You're in a safe place.",
            "worried": "I understand you're worried. Let's take this one step at a time.",
            "sad": "It's okay to feel sad. Your feelings are important."
        }

        return validations.get(emotion.lower(), "I understand. Your feelings matter.")


# Singleton instance
solace = Solace()
