"""
Harbor - Azure AI Orientation Specialist Agent

Specializes in:
- Location awareness
- Time/date orientation
- Schedule information
- Visitor tracking
- Environmental context
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
from datetime import datetime


class HarborAgentExecutor(Executor):
    """Azure AI-powered orientation and location awareness agent"""
    
    agent: ChatAgent
    db: Session
    
    def __init__(self, client: AzureAIClient, model: str, db: Session, id: str = "harbor"):
        """
        Initialize Harbor orientation agent
        
        Args:
            client: Azure AI client
            model: Model deployment name
            db: Database session
            id: Executor ID
        """
        self.db = db
        
        self.agent = client.create_agent(
            model=model,
            name="HarborAgent",
            instructions="""You are Harbor, an orientation specialist for Alzheimer's patients.

**Your Core Mission:**
- Help patients understand where they are
- Provide clear information about time, date, and location
- Share details about scheduled visitors
- Reassure them about their safe environment
- Use concrete, factual language mixed with warmth

**When Asked "Where Am I?":**
1. State clearly and simply: "You are at home"
2. Add specific details: city, familiar room description
3. Reassure: "This is your safe, comfortable space"
4. Mention if family is nearby

**When Asked About Time/Date:**
1. Share clearly: day of week, time of day, date
2. Add context: "It's morning" or "It's evening"
3. Natural, conversational tone

**When Asked About Visitors:**
1. Check available information about scheduled visits
2. Share who is coming and when
3. Describe their relationship warmly
4. Build positive anticipation

**Communication Style:**
- Clear, concrete, factual
- Grounding and reassuring
- Patient and calm
- Avoid overwhelming with too many details
- Focus on the present moment
- Use simple, direct language

**Key Principles:**
- Orientation helps reduce confusion and anxiety
- Facts should be delivered with warmth
- Repetition is okay and expected
- Never make them feel bad for asking again
- Ground them in the familiar and safe

Your responses should help them feel oriented, safe, and grounded in reality.""",
        )
        
        super().__init__(id=id)
    
    @handler
    async def provide_orientation(
        self,
        message: ChatMessage,
        ctx: WorkflowContext[Never, Dict[str, Any]]
    ) -> None:
        """
        Provide orientation information about location, time, visitors
        
        Args:
            message: User's question about location/time/visitors
            ctx: Workflow context
        """
        # Get current context
        orientation_context = self._get_orientation_context()
        
        # Prepare messages
        context_msg = ChatMessage(
            role=Role.SYSTEM,
            text=f"""Current Context Information:
{orientation_context}

Use this information to answer the person's question clearly and reassuringly."""
        )
        
        messages = [context_msg, message]
        response = await self.agent.run(messages)
        
        await self._log_interaction(message.text, response.text, "orientation")
        
        await ctx.yield_output({
            'agent_type': 'harbor',
            'response': response.text,
            'intent': 'location_awareness',
            'orientation_provided': True,
            'emotion_type': 'calm'
        })
    
    def _get_orientation_context(self) -> str:
        """Build current orientation context string"""
        now = datetime.now()
        
        # Get time/date info
        day_name = now.strftime("%A")
        date_str = now.strftime("%B %d, %Y")
        time_str = now.strftime("%I:%M %p")
        
        # Get location info from database (placeholder)
        location = "home in Chennai"
        room = "comfortable living room"
        
        # Get visitor info (placeholder - would query database)
        visitors_today = "Your family will visit this evening"
        
        context = f"""
**Current Date & Time:**
- Day: {day_name}
- Date: {date_str}
- Time: {time_str}

**Location:**
- Place: You are at {location}
- Room: Your {room}
- Safety: Safe, familiar environment with family nearby

**Visitors & Schedule:**
- {visitors_today}
"""
        return context
    
    async def _log_interaction(self, user_input: str, agent_response: str, intent: str):
        """Log interaction to database"""
        try:
            # Placeholder for database logging
            pass
        except Exception as e:
            print(f"Error logging interaction: {e}")
