"""
Solace - Azure AI Emotional Support Agent

Specializes in:
- Anxiety relief
- Emotional reassurance
- Calm mode activation
- Stress reduction
- Soothing communication
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


class SolaceAgentExecutor(Executor):
    """Azure AI-powered emotional support agent"""
    
    agent: ChatAgent
    db: Session
    
    def __init__(self, client: AzureAIClient, model: str, db: Session, id: str = "solace"):
        """
        Initialize Solace emotional support agent
        
        Args:
            client: Azure AI client
            model: Model deployment name
            db: Database session
            id: Executor ID
        """
        self.db = db
        
        # Create Azure AI agent with specialized instructions
        self.agent = client.create_agent(
            model=model,
            name="SolaceAgent",
            instructions="""You are Solace, a compassionate emotional support specialist for Alzheimer's patients.

**Your Core Mission:**
- Provide calm, reassuring, and empathetic responses
- Help reduce anxiety and stress
- Offer emotional validation and comfort
- Use simple, clear, warm language
- Never overwhelm with too much information

**Communication Style:**
- Speak in gentle, soothing tones
- Use shorter sentences and simple words
- Validate their feelings first
- Offer reassurance about safety and care
- Be patient and understanding
- Focus on the present moment

**When Someone is Anxious:**
1. Acknowledge their feeling: "I can sense you're feeling worried"
2. Reassure safety: "You are safe right now"
3. Ground them: "Let's take a deep breath together"
4. Offer comfort: "You are surrounded by people who care"

**When Someone is Confused:**
1. Be gentle and patient
2. Don't correct harshly
3. Provide simple, clear information
4. Reassure them it's okay to feel this way

**When Someone is Sad:**
1. Validate their emotions
2. Remind them they are valued and loved
3. Listen without judgment
4. Offer gentle encouragement

**Key Principles:**
- Never argue or correct aggressively
- Avoid medical/clinical language
- Focus on emotional comfort, not diagnosis
- Keep responses warm and human
- Use their name when available to create connection
- Remember: Your goal is to bring peace and calm

Always end responses with gentle reassurance. You are a trusted companion.""",
        )
        
        super().__init__(id=id)
    
    @handler
    async def provide_support(
        self, 
        message: ChatMessage, 
        ctx: WorkflowContext[Never, Dict[str, Any]]
    ) -> None:
        """
        Provide emotional support based on user's message
        
        Args:
            message: User's message expressing emotions or concerns
            ctx: Workflow context for yielding output
        """
        # Get user context from database
        user_context = self._get_user_context(message)
        
        # Prepare messages with context
        messages = [
            ChatMessage(role=Role.SYSTEM, text=user_context),
            message
        ]
        
        # Get AI response
        response = await self.agent.run(messages)
        
        # Log interaction to database
        await self._log_interaction(message.text, response.text, "emotional_support")
        
        # Yield the response
        await ctx.yield_output({
            'agent_type': 'solace',
            'response': response.text,
            'intent': 'emotional_support',
            'emotion_type': 'calm',
            'support_provided': True
        })
    
    @handler
    async def activate_calm_mode(
        self,
        message: ChatMessage,
        ctx: WorkflowContext[Never, Dict[str, Any]]
    ) -> None:
        """
        Activate calming mode with breathing exercises and reassurance
        
        Args:
            message: Request for calm mode
            ctx: Workflow context
        """
        calm_instruction = ChatMessage(
            role=Role.USER,
            text="""The person needs calming support right now. Please:
1. Guide them through a gentle breathing exercise (4 counts in, 4 hold, 4 out)
2. Suggest calming activities (soft music, looking at family photos, warm drink)
3. Provide deep reassurance about safety and being cared for
4. Use very gentle, slow-paced language"""
        )
        
        messages = [calm_instruction, message]
        response = await self.agent.run(messages)
        
        await self._log_interaction(message.text, response.text, "calm_mode")
        
        await ctx.yield_output({
            'agent_type': 'solace',
            'response': response.text,
            'intent': 'calm_mode',
            'emotion_type': 'calm',
            'calm_mode_activated': True,
            'breathing_exercise': True
        })
    
    def _get_user_context(self, message: ChatMessage) -> str:
        """Get user context for personalized responses"""
        # Extract user info if available from message metadata
        # For now, return generic context
        return "Remember to use warm, personal language and address them with care."
    
    async def _log_interaction(self, user_input: str, agent_response: str, intent: str):
        """Log interaction to database"""
        try:
            from app.model.agent_interaction import AgentInteraction
            from datetime import datetime
            
            # Note: user_id would come from message metadata in real implementation
            # For now, this is a placeholder
            # interaction = AgentInteraction(
            #     user_id=1,
            #     agent_type='solace',
            #     intent=intent,
            #     user_input=user_input,
            #     agent_response=agent_response,
            #     timestamp=datetime.utcnow(),
            #     emotion_score=0.5,
            #     emotion_type='calm'
            # )
            # self.db.add(interaction)
            # self.db.commit()
            pass
        except Exception as e:
            print(f"Error logging interaction: {e}")
