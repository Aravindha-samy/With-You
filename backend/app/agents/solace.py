"""
Solace - Emotional Intelligence Agent

Detects and regulates emotional distress.
Protects emotional safety and dignity.
"""

from typing import Dict, Any
from app.copilot_client import generate_response_sync, get_agent_system_prompt


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
        self.system_prompt = get_agent_system_prompt("solace")
        self.calm_protocols = {
            "breathing": "Let's take a slow breath together. In... and out... You're doing great.",
            "memory_music": "Would you like to listen to some familiar music?",
            "family_voice": "Would you like to hear a message from your family?",
            "none": "I'm here with you. You're safe."
        }
        self.fallback_message = "It's okay. You're safe. I'm here with you."

    def respond(
        self,
        query: str,
        anxiety_score: float,
        repetition_count: int = 0,
        last_interactions: list = None
    ) -> Dict[str, Any]:
        """
        Generate emotional support response using Copilot model

        Returns:
        {
            "message": "User-facing response",
            "calm_protocol": "none|breathing|memory_music|family_voice",
            "caregiver_alert": true/false
        }
        """

        # Detect distress triggers
        distress_keywords = ["scared", "afraid", "help", "don't know where", "lost", "confused", "alone"]
        is_distressed = any(word in query.lower() for word in distress_keywords)

        # Determine calm protocol based on anxiety level
        if anxiety_score > 0.8 or is_distressed:
            calm_protocol = "breathing"
        elif anxiety_score > 0.6:
            calm_protocol = "memory_music"
        else:
            calm_protocol = "none"

        # Build context-aware prompt
        context_prompt = f"""The patient says: "{query}"

Context:
- Anxiety level: {anxiety_score:.1f}/1.0 ({"HIGH - requires calming" if anxiety_score > 0.7 else "moderate" if anxiety_score > 0.4 else "low"})
- Repetition count: {repetition_count} (if high, be extra patient)
- Detected distress: {"Yes" if is_distressed else "No"}
- Recommended calm protocol: {calm_protocol}

Provide a gentle, soothing response that validates their feelings and helps them feel safe.
{"Include a breathing exercise if anxiety is high." if anxiety_score > 0.8 else ""}
Keep it to 2-3 calming sentences."""

        message = generate_response_sync(
            prompt=context_prompt,
            system_prompt=self.system_prompt,
            max_tokens=100,
            temperature=0.5  # Lower temperature for more consistent calming responses
        )
        
        # Fallback if model fails
        if not message:
            if calm_protocol == "breathing":
                message = self.calm_protocols["breathing"]
            else:
                message = self.fallback_message

        # Determine if caregiver alert needed
        caregiver_alert = anxiety_score > 0.9 or repetition_count >= 5

        return {
            "message": message,
            "calm_protocol": calm_protocol,
            "caregiver_alert": caregiver_alert
        }

    def activate_calm_mode(self, protocol: str = "breathing") -> Dict[str, Any]:
        """Activate specific calm mode protocol using Copilot model"""
        
        context_prompt = f"""The patient needs calming. The recommended protocol is: {protocol}

Generate a soothing message for this calm mode protocol:
- breathing: Guide them through slow breathing
- memory_music: Suggest listening to familiar music
- family_voice: Suggest hearing a message from family
- none: General reassurance

Keep it to 2-3 gentle sentences."""

        message = generate_response_sync(
            prompt=context_prompt,
            system_prompt=self.system_prompt,
            max_tokens=80,
            temperature=0.5
        )
        
        if not message:
            message = self.calm_protocols.get(protocol, self.calm_protocols["none"])

        return {
            "message": message,
            "calm_protocol": protocol,
            "caregiver_alert": False
        }

    def validate_emotion(self, emotion: str) -> str:
        """Validate and acknowledge emotion using Copilot model"""
        
        context_prompt = f"""The patient is feeling: {emotion}

Validate this emotion without dismissing it. Acknowledge their feeling and provide comfort.
Keep it to 1-2 sentences."""

        validation = generate_response_sync(
            prompt=context_prompt,
            system_prompt=self.system_prompt,
            max_tokens=60,
            temperature=0.5
        )
        
        if not validation:
            validations = {
                "confused": "It's natural to feel confused sometimes. You're not alone.",
                "scared": "Feeling scared is okay. You're in a safe place.",
                "worried": "I understand you're worried. Let's take this one step at a time.",
                "sad": "It's okay to feel sad. Your feelings are important."
            }
            validation = validations.get(emotion.lower(), "I understand. Your feelings matter.")

        return validation

    def regulate_emotion(self, distress_signal: str) -> Dict[str, Any]:
        """
        Regulate emotional distress using Copilot model
        """
        context_prompt = f"""The patient shows signs of distress: "{distress_signal}"

Provide a calming response that:
1. Validates their feelings
2. Reassures them they are safe
3. Helps reduce their distress

Keep it to 2-3 soothing sentences."""

        calming_response = generate_response_sync(
            prompt=context_prompt,
            system_prompt=self.system_prompt,
            max_tokens=100,
            temperature=0.5
        )
        
        if not calming_response:
            calming_response = self.fallback_message

        return {
            "calming_response": calming_response
        }


# Singleton instance
solace = Solace()
