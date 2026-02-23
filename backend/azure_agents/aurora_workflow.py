"""
Aurora - Azure AI Orchestrator Workflow

The main coordinator that:
- Analyzes user intent
- Detects emotional state  
- Routes to appropriate specialist agent
- Manages the multi-agent workflow
"""

from agent_framework import (
    ChatAgent,
    ChatMessage,
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    handler,
    Role,
    AgentRunUpdateEvent,
    AgentRunResponseUpdate,
    TextContent
)
from agent_framework.azure import AzureAIClient
from typing_extensions import Never
from sqlalchemy.orm import Session
from typing import Dict, Any
from uuid import uuid4

from .solace_agent import SolaceAgentExecutor
from .harbor_agent import HarborAgentExecutor
from .roots_agent import RootsAgentExecutor
from .legacy_agent import LegacyAgentExecutor
from .echo_agent import EchoAgentExecutor
from .guardian_agent import GuardianAgentExecutor


class AuroraOrchestrator(Executor):
    """Main orchestrator that analyzes intent and routes to specialized agents"""
    
    intent_agent: ChatAgent
    db: Session
    
    # Specialized agents
    solace: SolaceAgentExecutor
    harbor: HarborAgentExecutor
    roots: RootsAgentExecutor
    legacy: LegacyAgentExecutor
    echo: EchoAgentExecutor
    guardian: GuardianAgentExecutor
    
    def __init__(
        self,
        client: AzureAIClient,
        model: str,
        db: Session,
        solace: SolaceAgentExecutor,
        harbor: HarborAgentExecutor,
        roots: RootsAgentExecutor,
        legacy: LegacyAgentExecutor,
        echo: EchoAgentExecutor,
        guardian: GuardianAgentExecutor,
        id: str = "aurora"
    ):
        """
        Initialize Aurora orchestrator
        
        Args:
            client: Azure AI client
            model: Model deployment name
            db: Database session
            solace: Emotional support agent
            harbor: Orientation agent
            roots: Family recognition agent
            legacy: Memory agent
            echo: Pattern analysis agent
            guardian: Caregiver insights agent
            id: Executor ID
        """
        self.db = db
        self.solace = solace
        self.harbor = harbor
        self.roots = roots
        self.legacy = legacy
        self.echo = echo
        self.guardian = guardian
        
        # Create intent detection agent
        self.intent_agent = client.create_agent(
            model=model,
            name="AuroraIntentDetector",
            instructions="""You are Aurora, the intent detection coordinator for an Alzheimer's care system.

**Your Mission:**
Analyze user messages and determine which specialized agent should respond.

**Available Specialist Agents:**

1. **Solace** - Emotional Support
   - Anxiety, fear, worry, stress
   - Feeling scared, sad, confused emotionally
   - Need for calm, reassurance, comfort
   - Keywords: scared, anxious, worried, upset, calm, relax

2. **Harbor** - Orientation & Location
   - Where am I? What day is it?
   - Time and date questions
   - Schedule and visitor information
   - Keywords: where, when, time, date, location, place, visit

3. **Roots** - Family Recognition
   - Who is this person?
   - Family member questions
   - Relationship information
   - Keywords: who, family, son, daughter, husband, wife, mom, dad

4. **Legacy** - Memory & Life Story
   - Tell me about my past
   - Work history, accomplishments
   - Life stories and memories
   - Keywords: remember, memory, story, past, career, when I was

5. **Echo** - Pattern Analysis
   - What patterns do you see?
   - Am I asking the same things?
   - Analysis requests
   - Keywords: pattern, repeat, again, trends, analysis

6. **Guardian** - Caregiver Reports (for caregivers only)
   - Daily/weekly reports
   - Cognitive summaries
   - Alerts and insights
   - Keywords: report, summary, caregiver, alert, how is

**Response Format:**
Respond with ONLY a JSON object:
{
    "agent": "solace|harbor|roots|legacy|echo|guardian",
    "intent": "brief_intent_description",
    "emotion": "anxious|calm|confused|happy|sad|neutral",
    "urgency": "low|medium|high"
}

**Decision Guidelines:**
- If multiple intents, choose the most urgent/emotional first
- Emotional distress → Solace (highest priority)
- Confusion about location/time → Harbor
- Questions about people → Roots
- Questions about past → Legacy
- Meta questions about patterns → Echo
- Caregiver requests → Guardian

Respond ONLY with the JSON, no other text.""",
        )
        
        super().__init__(id=id)
    
    @handler
    async def route_request(
        self,
        messages: list[ChatMessage],
        ctx: WorkflowContext[Never, str]
    ) -> None:
        """
        Main handler: Analyze intent and route to appropriate agent
        
        Args:
            messages: User's message(s)
            ctx: Workflow context
        """
        # Get the user's latest message
        user_message = messages[-1] if messages else ChatMessage(role=Role.USER, text="Hello")
        
        # Detect intent using intent agent
        intent_response = await self.intent_agent.run([user_message])
        intent_data = self._parse_intent(intent_response.text)
        
        # Route to appropriate specialist agent
        agent_type = intent_data.get('agent', 'solace')
        
        # Get response from specialist
        if agent_type == 'solace':
            response = await self._route_to_solace(user_message, ctx)
        elif agent_type == 'harbor':
            response = await self._route_to_harbor(user_message, ctx)
        elif agent_type == 'roots':
            response = await self._route_to_roots(user_message, ctx)
        elif agent_type == 'legacy':
            response = await self._route_to_legacy(user_message, ctx)
        elif agent_type == 'echo':
            response = await self._route_to_echo(user_message, ctx)
        elif agent_type == 'guardian':
            response = await self._route_to_guardian(user_message, ctx)
        else:
            # Default to Solace for safety
            response = await self._route_to_solace(user_message, ctx)
        
        # Yield the final response
        await ctx.yield_output(response)
    
    async def _route_to_solace(self, message: ChatMessage, ctx: WorkflowContext) -> str:
        """Route to Solace emotional support agent"""
        # Create a sub-context for the agent
        # For now, call the agent's handler directly
        # In production, would use proper sub-workflow
        result = {'response': 'Solace agent response would appear here'}
        return result.get('response', 'I am here to support you.')
    
    async def _route_to_harbor(self, message: ChatMessage, ctx: WorkflowContext) -> str:
        """Route to Harbor orientation agent"""
        result = {'response': 'Harbor agent response would appear here'}
        return result.get('response', 'Let me help you understand where you are.')
    
    async def _route_to_roots(self, message: ChatMessage, ctx: WorkflowContext) -> str:
        """Route to Roots family recognition agent"""
        result = {'response': 'Roots agent response would appear here'}
        return result.get('response', 'Let me tell you about your family.')
    
    async def _route_to_legacy(self, message: ChatMessage, ctx: WorkflowContext) -> str:
        """Route to Legacy memory agent"""
        result = {'response': 'Legacy agent response would appear here'}
        return result.get('response', 'Let me share your wonderful life story.')
    
    async def _route_to_echo(self, message: ChatMessage, ctx: WorkflowContext) -> str:
        """Route to Echo pattern analysis agent"""
        result = {'response': 'Echo agent response would appear here'}
        return result.get('response', 'Let me analyze the patterns I see.')
    
    async def _route_to_guardian(self, message: ChatMessage, ctx: WorkflowContext) -> str:
        """Route to Guardian caregiver insights agent"""
        result = {'response': 'Guardian agent response would appear here'}
        return result.get('response', 'Generating caregiver report.')
    
    def _parse_intent(self, intent_text: str) -> Dict[str, Any]:
        """Parse intent detection response"""
        import json
        import re
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', intent_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Default fallback
                return {
                    'agent': 'solace',
                    'intent': 'general_support',
                    'emotion': 'neutral',
                    'urgency': 'low'
                }
        except json.JSONDecodeError:
            # Fallback to safe default
            return {
                'agent': 'solace',
                'intent': 'general_support',
                'emotion': 'neutral',
                'urgency': 'low'
            }


def create_aurora_workflow(client: AzureAIClient, model: str, db: Session):
    """
    Create the complete Aurora multi-agent workflow
    
    Args:
        client: Azure AI client
        model: Model deployment name
        db: Database session
        
    Returns:
        Workflow configured as an agent
    """
    # Create all specialized agents
    solace = SolaceAgentExecutor(client, model, db)
    harbor = HarborAgentExecutor(client, model, db)
    roots = RootsAgentExecutor(client, model, db)
    legacy = LegacyAgentExecutor(client, model, db)
    echo = EchoAgentExecutor(client, model, db)
    guardian = GuardianAgentExecutor(client, model, db)
    
    # Create orchestrator
    aurora = AuroraOrchestrator(
        client=client,
        model=model,
        db=db,
        solace=solace,
        harbor=harbor,
        roots=roots,
        legacy=legacy,
        echo=echo,
        guardian=guardian
    )
    
    # Build workflow with Aurora as the single entry point
    workflow = (
        WorkflowBuilder()
        .set_start_executor(aurora)
        .build()
        .as_agent()  # Convert workflow to agent for HTTP serving
    )
    
    return workflow
