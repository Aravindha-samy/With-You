"""
Legacy - Story Continuity Agent

Maintains life narrative and prevents identity erosion.
"""

from typing import Dict, Any, List
from app.copilot_client import generate_response_sync, get_agent_system_prompt


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
        self.system_prompt = get_agent_system_prompt("legacy")
        self.fallback_message = "Your life has been filled with meaningful experiences and cherished moments."

    def respond(
        self,
        query: str,
        life_stories: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate narrative continuity response using Copilot model

        Returns:
        {
            "message": "User-facing response",
            "story_anchor_used": true/false,
            "memory_reference_ids": []
        }
        """

        if not life_stories:
            # No stored stories - use AI to generate affirming response
            context_prompt = f"""The patient asks: "{query}"

They seem to be asking about their life story or past, but we don't have specific recorded memories.
Provide a warm, dignified response that affirms their life has been meaningful.
Keep it to 2 short sentences."""

            message = generate_response_sync(
                prompt=context_prompt,
                system_prompt=self.system_prompt,
                max_tokens=80,
                temperature=0.7
            )
            
            if not message:
                message = self.fallback_message
                
            return {
                "message": message,
                "story_anchor_used": False,
                "memory_reference_ids": []
            }

        # Find relevant story based on keywords
        query_lower = query.lower()
        relevant_story = None

        for story in life_stories:
            if any(keyword in query_lower for keyword in story.get("keywords", [])):
                relevant_story = story
                break

        if relevant_story:
            story_context = relevant_story.get("narrative", "")
            memory_ids = [relevant_story.get("id")]
            
            context_prompt = f"""The patient asks: "{query}"

We have this relevant memory/story about them:
{story_context}

Help them connect with this memory in a warm, story-like way.
Keep it to 2-3 sentences that bring the memory to life gently."""

            message = generate_response_sync(
                prompt=context_prompt,
                system_prompt=self.system_prompt,
                max_tokens=120,
                temperature=0.7
            )
            
            if not message:
                message = story_context
                
            return {
                "message": message,
                "story_anchor_used": True,
                "memory_reference_ids": memory_ids
            }
        else:
            # No matching story - generate affirming response
            context_prompt = f"""The patient asks: "{query}"

We have some recorded memories but none match this specific question.
Provide a warm response that acknowledges their rich life history.
Keep it to 2 short sentences."""

            message = generate_response_sync(
                prompt=context_prompt,
                system_prompt=self.system_prompt,
                max_tokens=80,
                temperature=0.7
            )
            
            if not message:
                message = "You have lived a rich and meaningful life full of wonderful experiences."
                
            return {
                "message": message,
                "story_anchor_used": False,
                "memory_reference_ids": []
            }

    def complete_narrative(self, partial_memory: str, stored_memories: List[Dict] = None) -> str:
        """Complete a partial memory with stored context using Copilot model"""
        
        # Check if we have a matching stored memory
        if stored_memories:
            for memory in stored_memories:
                if partial_memory.lower() in memory.get("description", "").lower():
                    return memory.get("description", partial_memory)

        # Use AI to gently complete the memory
        context_prompt = f"""The patient has a partial memory: "{partial_memory}"

Help complete this memory fragment in a gentle, story-like way that preserves their dignity.
Don't invent specific details - keep it warm and affirming.
Keep it to 1-2 sentences."""

        completed = generate_response_sync(
            prompt=context_prompt,
            system_prompt=self.system_prompt,
            max_tokens=80,
            temperature=0.6
        )
        
        return completed if completed else partial_memory

    def complete_narrative_fragment(self, story_fragment: str) -> Dict[str, Any]:
        """
        Complete life narrative fragment using Copilot model
        """
        context_prompt = f"""Complete this life story fragment: "{story_fragment}"

Continue the narrative in a respectful, dignified way.
Keep it story-like but concise - 2-3 sentences maximum."""

        completed_narrative = generate_response_sync(
            prompt=context_prompt,
            system_prompt=self.system_prompt,
            max_tokens=100,
            temperature=0.7
        )
        
        if not completed_narrative:
            completed_narrative = story_fragment

        return {
            "completed_narrative": completed_narrative
        }


# Singleton instance
legacy = Legacy()
