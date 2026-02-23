"""
Azure Agent Service Layer

Provides a clean interface between FastAPI endpoints and Azure AI agents.
This service manages agent lifecycle, caching, and execution.
"""

from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
import json

from .client_config import get_openai_client, get_model_deployment_name


class AzureAgentService:
    """Service for managing Azure AI agent interactions"""
    
    def __init__(self):
        """Initialize the Azure Agent Service"""
        self._client = None
        self._model = None
        self._agent_prompts = self._load_agent_prompts()
        
    def _ensure_initialized(self, db: Session):
        """Lazy initialization of OpenAI client"""
        if self._client is None:
            self._client = get_openai_client()
            self._model = get_model_deployment_name()
    
    def _load_agent_prompts(self) -> Dict[str, str]:
        """Load specialized agent prompts"""
        return {
            'solace': """You are Solace, a compassionate emotional support specialist for Alzheimer's patients.

Provide calm, reassuring, and empathetic responses. Help reduce anxiety and stress.
Use simple, clear, warm language. Validate feelings, offer reassurance about safety,
and focus on the present moment. Keep responses gentle and brief.""",
            
            'harbor': """You are Harbor, an orientation specialist for Alzheimer's patients.

Help with location awareness, time, date, and schedule information.
Provide clear, simple information about where they are, what time it is,
and who might be visiting. Be patient and reassuring.""",
            
            'roots': """You are Roots, a family recognition specialist for Alzheimer's patients.

Help identify family members and explain relationships in warm, simple terms.
Share positive information about family connections and help maintain bonds.""",
            
            'legacy': """You are Legacy, a memory and life story specialist for Alzheimer's patients.

Help recall personal memories, life stories, work history, and accomplishments.
Celebrate their life journey with warmth and respect.""",
            
            'echo': """You are Echo, a pattern analysis specialist.

Analyze interaction patterns, detect repetitions, and identify emotional trends.
Provide insights in clear, professional language.""",
            
            'guardian': """You are Guardian, a caregiver insights specialist.

Generate reports on patient well-being, cognitive patterns, and care recommendations.
Be factual, professional, and helpful to caregivers."""
        }
    
    async def process_user_message(
        self,
        user_id: int,
        user_input: str,
        db: Session,
        agent_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a user message through the Aurora orchestrator
        
        Args:
            user_id: ID of the user
            user_input: The user's message
            db: Database session
            agent_type: Optional specific agent to use (otherwise Aurora routes)
            
        Returns:
            Dict containing agent response and metadata
        """
        # Ensure workflow is initialized
        self._ensure_initialized(db)
        
        try:
            # Create chat message
            message = ChatMessage(
                role=Role.USER,
                text=user_input
            )
            
            # Execute workflow
            # Note: Since Aurora workflow returns a string, we need to adapt it
            response = await self._execute_workflow([message])
            
            # Parse response and extract metadata
            result = self._parse_response(response, user_input)
            
            return result
            
        except Exception as e:
            # Fallback to safe error response
            return {
                'agent_type': 'aurora',
                'response': "I'm here to help. Could you please tell me more about how you're feeling?",
                'intent': 'error_recovery',
                'emotion_score': 0.5,
                'emotion_type': 'neutral',
                'alert_triggered': False,
                'error': str(e)
            }
    
    async def _execute_workflow(self, messages: list) -> str:
        """Execute the Aurora workflow and get response"""
        try:
            # Run the workflow as an agent
            result = await self._workflow.run(messages)
            
            # Extract text from result
            if hasattr(result, 'text'):
                return result.text
            elif isinstance(result, str):
                return result
            else:
                return str(result)
                
        except Exception as e:
            raise Exception(f"Workflow execution failed: {str(e)}")
    
    def _parse_response(self, response: str, user_input: str) -> Dict[str, Any]:
        """
        Parse agent response and extract metadata
        
        Args:
            response: Raw response from agent
            user_input: Original user input
            
        Returns:
            Structured response dict
        """
        # Detect emotion and intent from user input
        emotion_data = self._detect_emotion(user_input.lower())
        intent_data = self._detect_intent(user_input.lower())
        
        # Check if alert should be triggered
        alert_triggered = self._should_trigger_alert(emotion_data, intent_data)
        
        return {
            'agent_type': intent_data.get('agent', 'aurora'),
            'response': response,
            'intent': intent_data.get('intent', 'general'),
            'emotion_score': emotion_data.get('score', 0.5),
            'emotion_type': emotion_data.get('type', 'neutral'),
            'alert_triggered': alert_triggered,
            'alert_message': self._get_alert_message(emotion_data, intent_data) if alert_triggered else None
        }
    
    def _detect_emotion(self, text: str) -> Dict[str, Any]:
        """Simple emotion detection from keywords"""
        anxious_keywords = ['scared', 'afraid', 'worried', 'anxious', 'panic', 'nervous', 'upset']
        sad_keywords = ['sad', 'lonely', 'miss', 'crying', 'depressed']
        confused_keywords = ['confused', 'lost', 'where', 'what', 'who', "don't know"]
        happy_keywords = ['happy', 'good', 'great', 'wonderful', 'joy', 'love']
        
        # Count keyword occurrences
        anxious_count = sum(1 for word in anxious_keywords if word in text)
        sad_count = sum(1 for word in sad_keywords if word in text)
        confused_count = sum(1 for word in confused_keywords if word in text)
        happy_count = sum(1 for word in happy_keywords if word in text)
        
        # Determine primary emotion
        if anxious_count > 0:
            return {'type': 'anxious', 'score': min(0.3 + (anxious_count * 0.2), 1.0)}
        elif sad_count > 0:
            return {'type': 'sad', 'score': min(0.4 + (sad_count * 0.2), 1.0)}
        elif confused_count > 0:
            return {'type': 'confused', 'score': min(0.3 + (confused_count * 0.15), 0.8)}
        elif happy_count > 0:
            return {'type': 'happy', 'score': max(0.7 - (happy_count * 0.05), 0.4)}
        else:
            return {'type': 'neutral', 'score': 0.5}
    
    def _detect_intent(self, text: str) -> Dict[str, Any]:
        """Simple intent detection from keywords"""
        # Emotional support
        if any(word in text for word in ['scared', 'afraid', 'worried', 'anxious', 'calm', 'help me']):
            return {'agent': 'solace', 'intent': 'emotional_support'}
        
        # Orientation
        if any(word in text for word in ['where am i', 'where', 'what day', 'what time', 'when']):
            return {'agent': 'harbor', 'intent': 'orientation'}
        
        # Family recognition
        if any(word in text for word in ['who is', 'who are', 'my son', 'my daughter', 'my family', 'this person']):
            return {'agent': 'roots', 'intent': 'family_recognition'}
        
        # Memory/stories
        if any(word in text for word in ['remember', 'memory', 'story', 'when i was', 'my past', 'tell me about']):
            return {'agent': 'legacy', 'intent': 'memory_recall'}
        
        # Pattern analysis
        if any(word in text for word in ['pattern', 'repeat', 'again', 'same thing']):
            return {'agent': 'echo', 'intent': 'pattern_analysis'}
        
        # Caregiver report
        if any(word in text for word in ['report', 'summary', 'how is', 'insights']):
            return {'agent': 'guardian', 'intent': 'caregiver_report'}
        
        # Default to general support
        return {'agent': 'solace', 'intent': 'general_support'}
    
    def _should_trigger_alert(self, emotion_data: Dict, intent_data: Dict) -> bool:
        """Determine if caregiver alert should be triggered"""
        # High anxiety score
        if emotion_data.get('type') == 'anxious' and emotion_data.get('score', 0) > 0.7:
            return True
        
        # Multiple emotional distress indicators
        if emotion_data.get('type') in ['anxious', 'sad'] and emotion_data.get('score', 0) > 0.6:
            return True
        
        return False
    
    def _get_alert_message(self, emotion_data: Dict, intent_data: Dict) -> str:
        """Generate alert message for caregiver"""
        emotion_type = emotion_data.get('type', 'neutral')
        
        if emotion_type == 'anxious':
            return f"Patient showing signs of anxiety (score: {emotion_data.get('score', 0):.2f}). May need reassurance."
        elif emotion_type == 'sad':
            return f"Patient expressing sadness (score: {emotion_data.get('score', 0):.2f}). May benefit from comfort."
        elif emotion_type == 'confused':
            return f"Patient appears confused (score: {emotion_data.get('score', 0):.2f}). May need orientation support."
        else:
            return "Patient interaction requires caregiver attention."


# Global service instance
_agent_service = None


def get_agent_service() -> AzureAgentService:
    """Get or create the global agent service instance"""
    global _agent_service
    if _agent_service is None:
        _agent_service = AzureAgentService()
    return _agent_service
