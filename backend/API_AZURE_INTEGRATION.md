# Azure AI Agents API Integration Guide

## Overview

The WithYou backend API is now fully integrated with Azure AI Agents using Microsoft Agent Framework. The system features a multi-agent architecture where Aurora (the orchestrator) intelligently routes patient queries to specialized agents.

## Architecture

```
Patient Query → FastAPI Endpoint → Azure Agent Service → Aurora Orchestrator
                                                              ↓
                                    ┌─────────────────────────┴──────────────────────────┐
                                    ↓                 ↓                ↓                  ↓
                                 Solace           Harbor            Roots              Legacy
                              (Emotional)      (Orientation)      (Family)           (Memory)
```

## Quick Start

### 1. Install Dependencies

```bash
cd backend
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure your Azure AI settings:

```bash
cp .env.example .env
```

**For Development (Free):**
Use GitHub Models:
```env
GITHUB_TOKEN=your_github_personal_access_token
MODEL_DEPLOYMENT_NAME=gpt-4o-mini
```

**For Production:**
Use Azure AI Foundry:
```env
FOUNDRY_PROJECT_ENDPOINT=https://your-project.api.azureml.ms
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4o
```

### 3. Start the Server

```bash
python -m uvicorn main:app --reload --port 8000
```

## API Endpoints

### Main Agent Endpoint

#### POST `/agents/ask`

Send a message to the AI agent system.

**Request:**
```json
{
  "user_id": 1,
  "user_input": "I'm feeling scared and don't know where I am",
  "agent_type": null,
  "voice_enabled": false
}
```

**Response:**
```json
{
  "agent_type": "solace",
  "response": "I can sense you're feeling worried. You are safe right now. You're at home, and the people around you care deeply about you. Let's take a deep breath together...",
  "intent": "emotional_support",
  "emotion_score": 0.8,
  "emotion_type": "anxious",
  "alert_triggered": true,
  "alert_message": "Patient showing signs of anxiety (score: 0.80). May need reassurance."
}
```

**Parameters:**
- `user_id` (int, required): Patient's user ID
- `user_input` (string, required): The patient's message/question
- `agent_type` (string, optional): Specific agent to use. If omitted, Aurora routes automatically
  - Options: `"solace"`, `"harbor"`, `"roots"`, `"legacy"`, `"echo"`, `"guardian"`
- `voice_enabled` (boolean, optional): Enable voice output (future feature)

**Response Fields:**
- `agent_type`: Which agent handled the request
- `response`: The agent's response message
- `intent`: Detected intent (e.g., "emotional_support", "orientation", "family_recognition")
- `emotion_score`: Emotional intensity score (0.0 - 1.0)
- `emotion_type`: Detected emotion ("anxious", "sad", "confused", "happy", "neutral")
- `alert_triggered`: Whether a caregiver alert was created
- `alert_message`: Alert message sent to caregiver (if triggered)

### Specialized Agent Endpoints

These endpoints remain available for direct access to specific agent functionality:

#### GET `/agents/harbor/location/{user_id}`
Get orientation information (where am I?)

#### GET `/agents/harbor/visits/{user_id}`
Get scheduled visits

#### GET `/agents/roots/family/{user_id}`
Get family member information

#### GET `/agents/legacy/stories/{user_id}`
Get personal stories and memories

#### POST `/agents/solace/calm-mode/{user_id}`
Activate calm mode

#### GET `/agents/guardian/dashboard/{user_id}`
Get caregiver dashboard insights

#### GET `/agents/echo/patterns/{user_id}`
Get memory and behavior patterns

## How It Works

### 1. Request Flow

1. Patient or caregiver sends a message via `/agents/ask`
2. The API validates the user exists in the database
3. The request is passed to `AzureAgentService`
4. Aurora analyzes the message to detect:
   - Intent (what the patient needs)
   - Emotion (how the patient feels)
   - Urgency (priority level)
5. Aurora routes to the appropriate specialized agent
6. The agent generates a compassionate, contextual response
7. The interaction is logged to the database
8. If emotional distress is detected, a caregiver alert is created
9. The response is returned to the frontend

### 2. Agent Routing Logic

Aurora uses keyword analysis and emotional detection to route requests:

**Solace** - Emotional Support
- Keywords: scared, anxious, worried, upset, calm, help
- Use case: Emotional distress, anxiety, fear

**Harbor** - Orientation
- Keywords: where, when, time, date, location, visit
- Use case: Confusion about place, time, or schedule

**Roots** - Family Recognition
- Keywords: who, family, son, daughter, husband, wife
- Use case: Questions about people and relationships

**Legacy** - Memory & Stories
- Keywords: remember, memory, story, past, career
- Use case: Recalling personal history and accomplishments

**Echo** - Pattern Analysis
- Keywords: pattern, repeat, again, trends
- Use case: Meta-analysis of behavior patterns

**Guardian** - Caregiver Insights
- Keywords: report, summary, insights, alerts
- Use case: Caregiver dashboard and reports

### 3. Database Logging

Every interaction is automatically logged:

```python
# AgentInteraction table stores:
- user_id
- agent_type
- user_input
- agent_response
- intent
- emotion_score
- emotion_type
- is_routine
- timestamp
```

### 4. Caregiver Alerts

Alerts are triggered when:
- Anxiety score > 0.7
- Emotional distress indicators present
- Multiple concerning patterns detected

Alerts include:
- Alert type
- Descriptive message
- Triggering agent
- Timestamp

## Error Handling

The system includes graceful error handling:

```python
# If Azure AI fails, the system:
1. Logs the error
2. Returns a safe, gentle fallback response
3. Still logs the interaction attempt
4. Does not expose technical errors to the patient
```

Example fallback:
```json
{
  "agent_type": "aurora",
  "response": "I'm here to help. Could you please tell me more about how you're feeling?",
  "intent": "error_recovery",
  "emotion_score": 0.5,
  "emotion_type": "neutral",
  "alert_triggered": false
}
```

## Testing the Integration

### 1. Test Basic Interaction

```bash
curl -X POST "http://localhost:8000/agents/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "user_input": "Where am I?"
  }'
```

### 2. Test Emotional Support

```bash
curl -X POST "http://localhost:8000/agents/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "user_input": "I feel scared and confused"
  }'
```

### 3. Test Family Recognition

```bash
curl -X POST "http://localhost:8000/agents/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "user_input": "Who is my daughter Sarah?"
  }'
```

## Frontend Integration

Update your frontend API calls to use the new endpoint:

```typescript
// frontend/lib/api.ts

export async function askAgent(
  userId: number,
  message: string,
  agentType?: string
): Promise<AgentResponse> {
  const response = await fetch(`${API_URL}/agents/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      user_input: message,
      agent_type: agentType,
      voice_enabled: false
    })
  });
  
  if (!response.ok) {
    throw new Error('Failed to get agent response');
  }
  
  return response.json();
}
```

## Monitoring & Analytics

The integration provides built-in analytics:

### Get Interaction History
```
GET /agent_interactions?user_id=1&limit=50
```

### Get Cognitive Insights
```
GET /cognitive_insights?user_id=1
```

### Get Caregiver Alerts
```
GET /caregiver_alerts?caregiver_id=1&is_acknowledged=false
```

### Get Behavior Patterns
```
GET /agents/echo/patterns/1
```

## Production Considerations

### 1. Environment Configuration

For production:
- Use Azure AI Foundry instead of GitHub Models
- Configure proper authentication with Azure Managed Identity
- Set appropriate rate limits
- Enable request logging

### 2. Database

- Use PostgreSQL instead of SQLite
- Configure connection pooling
- Set up regular backups
- Index frequently queried fields

### 3. Security

- Implement authentication middleware
- Validate all user inputs
- Use HTTPS for all endpoints
- Sanitize patient data in logs

### 4. Scaling

- Deploy with Gunicorn + Uvicorn workers
- Use Redis for caching agent responses
- Implement request queuing for high load
- Monitor Azure AI quota usage

## Troubleshooting

### Issue: "Please configure either GITHUB_TOKEN or FOUNDRY_PROJECT_ENDPOINT"

**Solution:** 
1. Copy `.env.example` to `.env`
2. Add your GitHub token or Azure endpoint
3. Restart the server

### Issue: Agent responses are slow

**Solution:**
- Check Azure AI model endpoint latency
- Consider using a faster model (gpt-4o-mini)
- Implement response caching
- Use connection pooling

### Issue: Alerts not being created

**Solution:**
- Verify caregiver exists in database
- Check emotion score thresholds in `service.py`
- Review database logs for errors

## Next Steps

1. **Implement Voice Support**: Add text-to-speech for agent responses
2. **Enhanced Memory**: Integrate long-term conversation memory
3. **Multi-language**: Add support for multiple languages
4. **Caregiver Portal**: Build real-time alert dashboard
5. **Analytics Dashboard**: Visualize interaction patterns and trends

## Support

For issues or questions:
- Review the [Azure AI Agents Documentation](AZURE_AI_AGENTS.md)
- Check the API documentation at `http://localhost:8000/docs`
- Review logs in `logs/` directory
