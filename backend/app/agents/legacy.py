"""
Legacy - Story Continuity Agent

Maintains life narrative and prevents identity erosion.
"""

from typing import Dict, Any, List


class Legacy:
    """
    Legacy - Life Narrative Preservation Agent

    Mission:
    - Maintain continuity of personal story
    - Complete narratives gently
    - Prevent identity erosion
    """

    def __init__(self):
        self.tone = "respectful, dignified, story-like but concise"

    def respond(
        self,
        query: str,
        life_stories: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate narrative continuity response

        Returns:
        {
            "message": "User-facing response",
            "story_anchor_used": true/false,
            "memory_reference_ids": []
        }
        """

        if not life_stories:
            return {
                "message": "Your life has been filled with meaningful experiences.",
                "story_anchor_used": False,
                "memory_reference_ids": []
            }

        # Find relevant story
        query_lower = query.lower()
        relevant_story = None

        for story in life_stories:
            if any(keyword in query_lower for keyword in story.get("keywords", [])):
                relevant_story = story
                break

        if relevant_story:
            message = relevant_story.get("narrative", "")
            memory_ids = [relevant_story.get("id")]
            story_used = True
        else:
            message = "You have lived a rich and meaningful life."
            memory_ids = []
            story_used = False

        return {
            "message": message,
            "story_anchor_used": story_used,
            "memory_reference_ids": memory_ids
        }

    def complete_narrative(self, partial_memory: str, stored_memories: List[Dict]) -> str:
        """Complete a partial memory with stored context"""
        # Find matching stored memory
        for memory in stored_memories:
            if partial_memory.lower() in memory.get("description", "").lower():
                return memory.get("description", partial_memory)

        return partial_memory


# Singleton instance
legacy = Legacy()
