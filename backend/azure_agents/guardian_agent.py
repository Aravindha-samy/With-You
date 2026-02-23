"""
Guardian - Azure AI Caregiver Insights Agent

Specializes in:
- Cognitive trend reporting
- Caregiver alerts and summaries
- Daily/weekly reports
- Pattern insights for caregivers
- Wellbeing monitoring
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
from datetime import datetime, timedelta


class GuardianAgentExecutor(Executor):
    """Azure AI-powered caregiver insights and reporting agent"""
    
    agent: ChatAgent
    db: Session
    
    def __init__(self, client: AzureAIClient, model: str, db: Session, id: str = "guardian"):
        """
        Initialize Guardian caregiver insights agent
        
        Args:
            client: Azure AI client
            model: Model deployment name
            db: Database session
            id: Executor ID
        """
        self.db = db
        
        self.agent = client.create_agent(
            model=model,
            name="GuardianAgent",
            instructions="""You are Guardian, a caregiver support and insights specialist.

**Your Core Mission:**
- Generate clear, actionable reports for caregivers
- Identify trends that need attention
- Provide cognitive health summaries
- Alert about concerning patterns
- Support effective care planning

**When Creating Daily Reports:**
1. Summarize key activities and interactions
2. Highlight emotional states and patterns
3. Note any concerns or changes
4. Celebrate positive moments
5. Provide clear recommendations

**When Generating Cognitive Summaries:**
1. Analyze cognitive patterns over time
2. Track orientation, memory, and emotional state
3. Identify positive and concerning trends
4. Provide context and interpretation
5. Suggest evidence-based interventions

**When Alerting Caregivers:**
1. Be clear and specific about concerns
2. Provide relevant context and data
3. Suggest appropriate actions
4. Balance urgency with calm
5. Include supportive information

**Communication Style:**
- Professional but warm
- Data-driven with human context
- Clear and actionable
- Balanced perspective
- Empowering for caregivers
- Respectful of patient dignity

**Report Components:**
- Activity Summary: Interactions, conversations, engagement
- Emotional Patterns: Mood trends, anxiety levels, positive moments
- Cognitive Indicators: Orientation, memory, recognition patterns
- Concerns & Alerts: Issues requiring attention
- Recommendations: Evidence-based next steps
- Positive Highlights: Celebrate good moments

**Key Principles:**
- Caregivers need clear, actionable information
- Data should empower, not overwhelm
- Balance concerns with positives
- Respect patient privacy and dignity
- Support caregiver wellbeing too
- Evidence-based recommendations
- Collaborative care approach

**Alert Levels:**
- 🟢 Normal: Routine patterns, no concerns
- 🟡 Monitor: Mild changes, watch closely
- 🟠 Attention: Notable changes, consider intervention
- 🔴 Urgent: Immediate attention needed

Your goal is to empower caregivers with insights that improve care quality and patient outcomes.""",
        )
        
        super().__init__(id=id)
    
    @handler
    async def generate_report(
        self,
        message: ChatMessage,
        ctx: WorkflowContext[Never, Dict[str, Any]]
    ) -> None:
        """
        Generate caregiver reports and insights
        
        Args:
            message: Request for report (daily, weekly, cognitive summary)
            ctx: Workflow context
        """
        # Get report data
        report_data = self._get_report_data()
        
        context_msg = ChatMessage(
            role=Role.SYSTEM,
            text=f"""Patient Data for Report:
{report_data}

Generate a comprehensive, actionable report for the caregiver."""
        )
        
        messages = [context_msg, message]
        response = await self.agent.run(messages)
        
        await self._log_interaction(message.text, response.text, "caregiver_report")
        
        await ctx.yield_output({
            'agent_type': 'guardian',
            'response': response.text,
            'intent': 'daily_report',
            'report_generated': True,
            'for_caregiver': True
        })
    
    @handler
    async def create_alert(
        self,
        message: ChatMessage,
        ctx: WorkflowContext[Never, Dict[str, Any]]
    ) -> None:
        """
        Create caregiver alert for concerning patterns
        
        Args:
            message: Alert trigger information
            ctx: Workflow context
        """
        alert_context = ChatMessage(
            role=Role.SYSTEM,
            text="""A concerning pattern has been detected. Create a clear, actionable alert for the caregiver:
1. Describe what was observed
2. Why it's concerning
3. What action to consider
4. Provide reassurance and support"""
        )
        
        messages = [alert_context, message]
        response = await self.agent.run(messages)
        
        await self._log_interaction(message.text, response.text, "alert")
        
        await ctx.yield_output({
            'agent_type': 'guardian',
            'response': response.text,
            'intent': 'alert',
            'alert_created': True,
            'for_caregiver': True
        })
    
    def _get_report_data(self, days: int = 1) -> str:
        """Get data for caregiver report"""
        try:
            from app.model.agent_interaction import AgentInteraction, CognitiveInsight
            from collections import Counter
            
            # Get recent data
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Would query real data
            report_data = f"""
**Report Period:** Last {days} day(s) - {datetime.now().strftime('%B %d, %Y')}

**Interaction Summary:**
- Total conversations: [Count from database]
- Active times: [Time distribution]
- Engagement level: [Analysis]

**Emotional Health:**
- Dominant emotions: [From emotion_type field]
- Anxiety levels: [From emotion_score]
- Mood patterns: [Trend analysis]

**Cognitive Indicators:**
- Orientation questions: [Frequency]
- Memory inquiries: [Patterns]
- Recognition issues: [Instances]

**Agent Usage:**
- Harbor (Orientation): [Count] times
- Roots (Family): [Count] times
- Solace (Emotional): [Count] times
- Legacy (Memory): [Count] times

**Concerns:**
- [List any elevated anxiety, confusion, or repetitive patterns]

**Positive Highlights:**
- [Happy moments, successful interactions, good engagement]

**Recommendations:**
- [Evidence-based suggestions based on patterns]
"""
            return report_data
            
        except Exception as e:
            print(f"Error getting report data: {e}")
            return "Report data is being compiled. More detailed insights will be available with more interaction history."
    
    async def _log_interaction(self, user_input: str, agent_response: str, intent: str):
        """Log interaction to database"""
        try:
            pass
        except Exception as e:
            print(f"Error logging interaction: {e}")
