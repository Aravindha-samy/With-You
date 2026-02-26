"""
Aurora - The Orchestrator Agent

Central orchestration intelligence for the With You cognitive support system.
Routes requests to appropriate domain agents and maintains session state.
"""

from typing import Dict, Any, Optional
import json
from datetime import datetime


class Aurora:
    """
    Aurora - The Orchestrator Agent

    Mission:
    - Interpret user intent
    - Assess emotional state
    - Route requests to appropriate domain agent
    - Enforce safety rules
    - Maintain session state
    - Protect identity continuity
    """

    def __init__(self):
        self.session_state = {}
        self.agent_map = {
            "orientation": "harbor",
            "identity": "roots",
            "emotional": "solace",
            "story": "legacy",
            "caregiver": "guardian",
            "memory": "echo"
        }

    def analyze_input(
        self,
        user_input: str,
        user_id: int,
        session_history: list = None,
        repetition_counter: int = 0,
        csi: float = 1.0
    ) -> Dict[str, Any]:
        """
        Analyze user input and determine routing

        Returns:
        {
            "intent": "orientation|identity|emotional|story|caregiver|unknown",
            "confidence": 0.0-1.0,
            "target_agent": "Harbor|Roots|Solace|Legacy|Guardian|Clarifier",
            "urgency_level": "low|medium|high",
            "emotional_score": 0.0-1.0,
            "write_memory": true/false
        }
        """

        # Simple intent classification (to be replaced with Azure OpenAI)
        intent, confidence = self._classify_intent(user_input)
        emotional_score = self._assess_emotion(user_input)

        # Determine target agent
        target_agent = self.agent_map.get(intent, "solace")

        # Determine urgency
        urgency_level = "low"
        if emotional_score > 0.85:
            urgency_level = "high"
            target_agent = "solace"
        elif repetition_counter > 3:
            urgency_level = "medium"

        # Low confidence routes to clarifier
        if confidence < 0.6:
            target_agent = "clarifier"

        return {
            "intent": intent,
            "confidence": confidence,
            "target_agent": target_agent,
            "urgency_level": urgency_level,
            "emotional_score": emotional_score,
            "write_memory": True
        }

    def _classify_intent(self, user_input: str) -> tuple[str, float]:
        """Classify user intent (simplified - to be replaced with AI)"""
        user_input_lower = user_input.lower()

        # Orientation keywords
        if any(word in user_input_lower for word in ["where", "when", "what day", "what time", "where am i"]):
            return "orientation", 0.85

        # Identity keywords
        if any(word in user_input_lower for word in ["who is", "who am i", "who are you", "family", "daughter", "son"]):
            return "identity", 0.85

        # Emotional keywords
        if any(word in user_input_lower for word in ["scared", "afraid", "worried", "anxious", "help", "confused"]):
            return "emotional", 0.90

        # Story keywords
        if any(word in user_input_lower for word in ["i used to", "i was", "remember when", "my life"]):
            return "story", 0.80

        return "unknown", 0.3

    def _assess_emotion(self, user_input: str) -> float:
        """Assess emotional state (simplified - to be replaced with AI)"""
        user_input_lower = user_input.lower()

        # High distress indicators
        if any(word in user_input_lower for word in ["scared", "terrified", "help", "panic"]):
            return 0.95

        # Moderate distress
        if any(word in user_input_lower for word in ["confused", "worried", "anxious", "don't know"]):
            return 0.75

        # Mild concern
        if any(word in user_input_lower for word in ["unsure", "forgot", "can't remember"]):
            return 0.55

        return 0.3  # Neutral


# Singleton instance
aurora = Aurora()
