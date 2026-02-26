"""
Aurora - The Orchestrator Agent

Central orchestration intelligence for the With You cognitive support system.
Routes requests to appropriate domain agents and maintains session state.
"""

from typing import Dict, Any, Optional
import json
from datetime import datetime
from app.copilot_client import generate_response_sync, get_agent_system_prompt


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
        self.system_prompt = get_agent_system_prompt("aurora")
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
        Analyze user input and determine routing using Copilot model

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

        # Use Copilot to analyze intent and emotion
        analysis_prompt = f"""Analyze this user input from someone with cognitive challenges:

Input: "{user_input}"

Context:
- Repetition count: {repetition_counter} (how many times similar questions asked recently)
- Cognitive Stability Index: {csi:.2f} (1.0 = stable, lower = more challenges)

Classify the intent as one of:
- orientation: Questions about time, date, location, schedule
- identity: Questions about people, relationships, "who is this?"
- emotional: Expression of fear, anxiety, distress, or need for comfort
- story: Questions about life history, memories, past experiences
- unknown: Cannot determine clear intent

Also assess:
- Emotional score (0.0 = calm, 1.0 = highly distressed)
- Urgency level (low, medium, high)

Respond ONLY with a JSON object (no explanation):
{{"intent": "...", "confidence": 0.0-1.0, "emotional_score": 0.0-1.0, "urgency_level": "low|medium|high"}}"""

        try:
            response = generate_response_sync(
                prompt=analysis_prompt,
                system_prompt="You are an intent classifier. Respond only with valid JSON.",
                max_tokens=100,
                temperature=0.3
            )
            
            if response:
                # Try to parse JSON response
                # Clean up response if it has markdown code blocks
                clean_response = response.strip()
                if clean_response.startswith("```"):
                    clean_response = clean_response.split("```")[1]
                    if clean_response.startswith("json"):
                        clean_response = clean_response[4:]
                    clean_response = clean_response.strip()
                
                analysis = json.loads(clean_response)
                intent = analysis.get("intent", "unknown")
                confidence = analysis.get("confidence", 0.5)
                emotional_score = analysis.get("emotional_score", 0.5)
                urgency_level = analysis.get("urgency_level", "low")
            else:
                raise ValueError("No response from model")
                
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback to keyword-based classification
            intent, confidence = self._classify_intent_fallback(user_input)
            emotional_score = self._assess_emotion_fallback(user_input)
            urgency_level = "medium" if repetition_counter > 3 else "low"

        # Determine target agent
        target_agent = self.agent_map.get(intent, "solace")

        # Adjust urgency based on repetition
        if repetition_counter > 5:
            urgency_level = "high"
        elif repetition_counter > 3:
            urgency_level = "medium"

        # Low confidence or low CSI routes to clarifier or Solace for safety
        if confidence < 0.6 or csi < 0.6:
            target_agent = "solace"  # Default to emotional support for safety

        return {
            "intent": intent,
            "confidence": confidence,
            "target_agent": target_agent,
            "urgency_level": urgency_level,
            "emotional_score": emotional_score,
            "write_memory": True
        }

    def _classify_intent_fallback(self, user_input: str) -> tuple[str, float]:
        """Fallback keyword-based intent classification"""
        input_lower = user_input.lower()
        
        # Orientation keywords
        orientation_keywords = ["where am i", "what time", "what day", "what date", "who is visiting", "schedule", "today"]
        if any(kw in input_lower for kw in orientation_keywords):
            return "orientation", 0.8
            
        # Identity keywords
        identity_keywords = ["who is", "who's this", "my family", "my son", "my daughter", "my wife", "my husband"]
        if any(kw in input_lower for kw in identity_keywords):
            return "identity", 0.8
            
        # Emotional keywords
        emotional_keywords = ["scared", "afraid", "help", "lost", "confused", "alone", "worried"]
        if any(kw in input_lower for kw in emotional_keywords):
            return "emotional", 0.9
            
        # Story keywords
        story_keywords = ["remember", "used to", "when i was", "my life", "worked", "lived"]
        if any(kw in input_lower for kw in story_keywords):
            return "story", 0.7
            
        return "unknown", 0.3

    def _assess_emotion_fallback(self, user_input: str) -> float:
        """Fallback keyword-based emotion assessment"""
        input_lower = user_input.lower()
        
        # High distress indicators
        high_distress = ["scared", "afraid", "help me", "terrified", "panic", "emergency"]
        if any(kw in input_lower for kw in high_distress):
            return 0.9
            
        # Medium distress indicators
        medium_distress = ["worried", "confused", "lost", "don't know", "uncertain"]
        if any(kw in input_lower for kw in medium_distress):
            return 0.6
            
        # Low stress/calm indicators
        calm_indicators = ["hello", "thank", "good", "nice", "love"]
        if any(kw in input_lower for kw in calm_indicators):
            return 0.2
            
        return 0.4  # Default moderate anxiety


# Singleton instance
aurora = Aurora()
