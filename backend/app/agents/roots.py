"""
Roots - Identity & Relationship Agent

Reinforces relational identity and personal history.
Protects familiarity and belonging.
"""

from typing import Dict, Any, List


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

    def respond(
        self,
        query: str,
        person_node: Dict[str, Any] = None,
        anxiety_high: bool = False
    ) -> Dict[str, Any]:
        """
        Generate identity/relationship response

        Returns:
        {
            "message": "User-facing response",
            "identity_reinforcement": true,
            "suggest_call": true/false
        }
        """

        if not person_node:
            return {
                "message": "Let me help you remember.",
                "identity_reinforcement": False,
                "suggest_call": False
            }

        name = person_node.get("name", "this person")
        relationship = person_node.get("relationship_type", "family member")
        description = person_node.get("description", "")

        # Build response (max 3 sentences)
        message = f"This is your {relationship} {name}."

        if description:
            message += f" {description}"

        # Add reassurance if anxiety is high
        if anxiety_high:
            message += f" {name} cares about you very much."

        # Suggest call if appropriate
        suggest_call = person_node.get("importance_level", 5) >= 8

        return {
            "message": message,
            "identity_reinforcement": True,
            "suggest_call": suggest_call
        }

    def get_family_list(self, relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get list of family members"""
        if not relationships:
            return {
                "message": "Your family loves you.",
                "identity_reinforcement": True,
                "suggest_call": False
            }

        # Sort by importance
        relationships = sorted(
            relationships,
            key=lambda x: x.get("importance_level", 0),
            reverse=True
        )

        family_list = []
        for rel in relationships[:5]:  # Top 5
            name = rel.get("name", "")
            rel_type = rel.get("relationship_type", "")
            family_list.append(f"{name} - your {rel_type}")

        message = "Your family:\n" + "\n".join([f"• {f}" for f in family_list])

        return {
            "message": message,
            "identity_reinforcement": True,
            "suggest_call": False
        }


# Singleton instance
roots = Roots()
