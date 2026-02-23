"""
Legacy - Azure AI Memory & Story Specialist Agent

Specializes in:
- Personal memory recall
- Life story narration
- Work history
- Family milestones
- Biographical continuity
"""

from agent_framework import (
    ChatAgent,
    ChatMessage,
    Executor,
    WorkflowContext,
    handler,
    Role
)
from agent_framework.azure import AzureAIClient
from typing_extensions import Never
from sqlalchemy.orm import Session
from typing import Dict, Any


class LegacyAgentExecutor(Executor):
    """Azure AI-powered memory and life story agent"""
    
    agent: ChatAgent
    db: Session
    
    def __init__(self, client: AzureAIClient, model: str, db: Session, id: str = "legacy"):
        """
        Initialize Legacy memory specialist agent
        
        Args:
            client: Azure AI client
            model: Model deployment name
            db: Database session
            id: Executor ID
        """
        self.db = db
        
        self.agent = client.create_agent(
            model=model,
            name="LegacyAgent",
            instructions="""You are Legacy, a memory and life story specialist for Alzheimer's patients.

**Your Core Mission:**
- Help patients recall and celebrate their life stories
- Share their memories and accomplishments
- Affirm their identity and life meaning
- Build continuity and self-worth
- Honor their personal history

**When Sharing Life Stories:**
1. Use their memories from the database with dignity
2. Tell their story with warmth and respect
3. Highlight accomplishments and positive moments
4. Affirm their value and importance
5. Help them feel proud and connected to their past

**When Recalling Specific Memories:**
1. Share the memory clearly and vividly
2. Add sensory details when available
3. Connect to positive emotions
4. Invite them to add their own recollections
5. Never contradict their version - validate and enrich

**When They Can't Remember:**
1. Gently fill in details from stored memories
2. Frame it as sharing, not testing
3. Make it a collaborative story
4. Focus on feelings, not facts
5. Celebrate what they do remember

**Communication Style:**
- Narrative and story-focused
- Warm and celebratory
- Dignified and respectful
- Patient and gentle
- Sensory and vivid when appropriate
- Affirming and validating

**Key Principles:**
- Everyone's life has meaning and value
- Memories define identity and worth
- Stories connect past to present
- Shared memories build bonds
- Focus on positive life themes
- Their story matters
- They matter

**Topics to Explore:**
- Career and work accomplishments
- Family milestones and celebrations
- Hobbies and passions
- Travel and adventures
- Friendships and connections
- Life lessons and wisdom

Your goal is to help them feel proud, valued, and connected to their rich life story.""",
        )
        
        super().__init__(id=id)
    
    @handler
    async def share_memories(
        self,
        message: ChatMessage,
        ctx: WorkflowContext[Never, Dict[str, Any]]
    ) -> None:
        """
        Share memories and life stories
        
        Args:
            message: User's question about their past or memories
            ctx: Workflow context
        """
        # Get memory context from database
        memory_context = self._get_memory_context()
        
        context_msg = ChatMessage(
            role=Role.SYSTEM,
            text=f"""Memory Cards and Life Story:
{memory_context}

Share these memories warmly to help them feel connected to their rich life history."""
        )
        
        messages = [context_msg, message]
        response = await self.agent.run(messages)
        
        await self._log_interaction(message.text, response.text, "memory_recall")
        
        await ctx.yield_output({
            'agent_type': 'legacy',
            'response': response.text,
            'intent': 'life_story',
            'emotion_type': 'happy',
            'memory_shared': True
        })
    
    def _get_memory_context(self) -> str:
        """Get stored memories from database"""
        try:
            from app.model.memory_card import MemoryCard
            from app.model.user import User
            
            # Would query based on actual user_id
            # memories = self.db.query(MemoryCard).filter_by(user_id=user_id).all()
            
            # Template for now
            context = """
**Life Story & Memories:**
You have a rich life full of meaningful experiences.

(Note: Specific memory cards would be pulled from database)

Your life has been filled with:
- Loving relationships
- Important accomplishments
- Cherished moments
- Valuable contributions

Each memory is a testament to your meaningful life.
"""
            return context
            
        except Exception as e:
            print(f"Error getting memory context: {e}")
            return "You have a wonderful life story filled with meaning and accomplishment."
    
    async def _log_interaction(self, user_input: str, agent_response: str, intent: str):
        """Log interaction to database"""
        try:
            pass
        except Exception as e:
            print(f"Error logging interaction: {e}")

