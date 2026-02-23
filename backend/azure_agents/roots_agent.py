"""
Roots - Azure AI Identity & Family Recognition Agent

Specializes in:
- Family member identification
- Relationship recognition
- Personal connections
- Life history context
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


class RootsAgentExecutor(Executor):
    """Azure AI-powered family recognition and identity agent"""
    
    agent: ChatAgent
    db: Session
    
    def __init__(self, client: AzureAIClient, model: str, db: Session, id: str = "roots"):
        """
        Initialize Roots family recognition agent
        
        Args:
            client: Azure AI client
            model: Model deployment name
            db: Database session
            id: Executor ID
        """
        self.db = db
        
        self.agent = client.create_agent(
            model=model,
            name="RootsAgent",
            instructions="""You are Roots, a family connection specialist for Alzheimer's patients.

**Your Core Mission:**
- Help patients recognize and remember family members
- Provide warm information about relationships
- Share loving context about their connections
- Build confidence in their family bonds
- Celebrate their relationships

**When Asked About Family Members:**
1. Clearly state the person's name and relationship
2. Add warm, positive details about them
3. Reassure how much they care
4. Mention contact information if appropriate
5. Build positive feelings about the connection

**When Someone Doesn't Recognize a Person:**
1. Gently provide the relationship without judgment
2. Share positive qualities and history
3. Never make them feel bad for not remembering
4. Focus on the love and connection
5. Keep it simple and warm

**When Sharing Family Information:**
- Use warm, affectionate language
- Emphasize love and care
- Keep descriptions simple and positive
- Include practical details (phone numbers) when helpful
- Build feelings of being surrounded by love

**Communication Style:**
- Warm and affectionate
- Patient and understanding
- Never corrective or judgmental
- Celebratory of family bonds
- Clear and simple
- Focus on positive emotions

**Key Principles:**
- Family connections are vital for wellbeing
- Not remembering doesn't mean not loved
- Repetition shows importance, not failure
- Every introduction is a gift
- Focus on feelings of love and safety
- Build confidence in their relationships

Your goal is to strengthen their sense of being loved, connected, and part of a family.""",
        )
        
        super().__init__(id=id)
    
    @handler
    async def provide_family_info(
        self,
        message: ChatMessage,
        ctx: WorkflowContext[Never, Dict[str, Any]]
    ) -> None:
        """
        Provide information about family members and relationships
        
        Args:
            message: User's question about family
            ctx: Workflow context
        """
        # Get family information from database
        family_context = self._get_family_context()
        
        context_msg = ChatMessage(
            role=Role.SYSTEM,
            text=f"""Family Information:
{family_context}

Use this to answer warmly and help them feel connected to their loving family."""
        )
        
        messages = [context_msg, message]
        response = await self.agent.run(messages)
        
        await self._log_interaction(message.text, response.text, "family_recognition")
        
        await ctx.yield_output({
            'agent_type': 'roots',
            'response': response.text,
            'intent': 'family_recognition',
            'emotion_type': 'happy',
            'family_info_provided': True
        })
    
    def _get_family_context(self) -> str:
        """Get family member information from database"""
        try:
            from app.model.emergency_contact import EmergencyContact
            
            # Query family members (placeholder - would use real user_id)
            # family_members = self.db.query(EmergencyContact).filter_by(user_id=user_id).all()
            
            # For now, return template
            context = """
**Your Family:**
You have a loving family who cares deeply about you.

(Note: Specific family member details would be pulled from database based on user)

Your family thinks about you often and visits regularly.
You are surrounded by people who love you very much.
"""
            return context
            
        except Exception as e:
            print(f"Error getting family context: {e}")
            return "You have a loving family who cares about you."
    
    async def _log_interaction(self, user_input: str, agent_response: str, intent: str):
        """Log interaction to database"""
        try:
            pass
        except Exception as e:
            print(f"Error logging interaction: {e}")
