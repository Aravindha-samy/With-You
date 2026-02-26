"""
Roots - Identity & Relationship Agent

Reinforces relational identity and personal history.
Protects familiarity and belonging.
"""

from typing import Dict, Any, List
from app.copilot_client import generate_response_sync, get_agent_system_prompt


class Roots:
    """
    Roots - Identity Preservation Agent

    Mission:
    - Reinforce relational identity
    - Maintain personal history
    - Answer "Who is this?" questions
    """

    def __init__(self):
        self.tone = "affirming, personal, warm, relational"
        self.system_prompt = get_agent_system_prompt("roots")
        self.fallback_message = "This person cares about you very much. You are loved."

    def respond(
        self,
        query: str,
        person_node: Dict[str, Any] = None,
        anxiety_high: bool = False
    ) -> Dict[str, Any]:
        """
        Generate identity/relationship response using Copilot model

        Returns:
        {
            "message": "User-facing response",
            "identity_reinforcement": true,
            "suggest_call": true/false
        }
        """

        if not person_node:
            # No specific person data - use AI to generate comforting response
            context_prompt = f"""The patient is asking: "{query}"

They seem to be asking about someone but we don't have specific information about this person.
Provide a warm, comforting response that helps them feel safe and connected.
Anxiety level is {"high" if anxiety_high else "normal"}.
Keep it to 2 short sentences."""

            message = generate_response_sync(
                prompt=context_prompt,
                system_prompt=self.system_prompt,
                max_tokens=80,
                temperature=0.6
            )
            
            if not message:
                message = self.fallback_message
                
            return {
                "message": message,
                "identity_reinforcement": False,
                "suggest_call": False
            }

        name = person_node.get("name", "this person")
        relationship = person_node.get("relationship_type", "family member")
        description = person_node.get("description", "")
        importance = person_node.get("importance_level", 5)

        # Build context-aware prompt
        context_prompt = f"""The patient is asking: "{query}"

About this person:
- Name: {name}
- Relationship: {relationship}
- Description: {description}
- Anxiety is {"high - be extra reassuring" if anxiety_high else "normal"}

Help the patient remember this person with warmth and affection.
Keep it to 2-3 short, clear sentences."""

        message = generate_response_sync(
            prompt=context_prompt,
            system_prompt=self.system_prompt,
            max_tokens=100,
            temperature=0.6
        )
        
        if not message:
            # Fallback to template response
            message = f"This is your {relationship} {name}."
            if description:
                message += f" {description}"
            if anxiety_high:
                message += f" {name} cares about you very much."

        suggest_call = importance >= 8

        return {
            "message": message,
            "identity_reinforcement": True,
            "suggest_call": suggest_call
        }

    def get_family_list(self, relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get list of family members using Copilot model"""
        if not relationships:
            message = generate_response_sync(
                prompt="The patient is asking about their family, but we don't have family records yet. Provide a warm, reassuring response.",
                system_prompt=self.system_prompt,
                max_tokens=60,
                temperature=0.6
            )
            if not message:
                message = "Your family loves you very much."
            
            return {
                "message": message,
                "identity_reinforcement": True,
                "suggest_call": False
            }

        # Sort by importance
        relationships = sorted(
            relationships,
            key=lambda x: x.get("importance_level", 0),
            reverse=True
        )

        family_info = []
        for rel in relationships[:5]:  # Top 5
            name = rel.get("name", "")
            rel_type = rel.get("relationship_type", "")
            family_info.append(f"{name} (your {rel_type})")

        family_text = ", ".join(family_info)
        
        context_prompt = f"""The patient is asking about their family.

Their family members are: {family_text}

Create a warm, affirming response listing these family members in a comforting way.
Keep it to 2-3 sentences."""

        message = generate_response_sync(
            prompt=context_prompt,
            system_prompt=self.system_prompt,
            max_tokens=100,
            temperature=0.6
        )
        
        if not message:
            # Fallback to template
            family_list = [f"• {rel.get('name', '')} - your {rel.get('relationship_type', '')}" 
                          for rel in relationships[:5]]
            message = "Your family:\n" + "\n".join(family_list)

        return {
            "message": message,
            "identity_reinforcement": True,
            "suggest_call": False
        }

    def answer_identity_question(self, question: str) -> Dict[str, Any]:
        """
        Answer identity-related questions using Copilot model
        """
        message = generate_response_sync(
            prompt=f"The patient asks an identity question: \"{question}\"\n\nProvide a helpful, warm response.",
            system_prompt=self.system_prompt,
            max_tokens=100,
            temperature=0.6
        )
        
        if not message:
            message = "You are a wonderful person with a life full of meaning and love."

        return {
            "answer": message
        }


# Singleton instance
roots = Roots()
