# WithYou Backend API

FastAPI backend for the WithYou patient care and memory management system with Azure AI Agent integration.

## Features

- ✅ FastAPI framework
- ✅ SQLite database with SQLAlchemy ORM
- ✅ User management (patients and caregivers)
- ✅ Mood check-ins tracking
- ✅ Memory cards management
- ✅ Emergency contacts management
- ✅ **Azure AI Multi-Agent System**
- ✅ **Intelligent Agent Orchestration (Aurora)**
- ✅ **6 Specialized AI Agents (Solace, Harbor, Roots, Legacy, Echo, Guardian)**
- ✅ **Automatic Caregiver Alerts**
- ✅ **Emotion Detection & Analysis**
- ✅ CORS configured
- ✅ Auto-generated API documentation

## Project Structure

```
backend/
├── app/
│   ├── api/                  # API endpoints
│   │   ├── agents.py         # ⭐ Agent interaction endpoints
│   │   ├── users.py
│   │   ├── mood_checkins.py
│   │   └── ...
│   ├── model/                # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   └── crud.py               # CRUD operations
├── azure_agents/             # ⭐ Azure AI Agent System
│   ├── aurora_workflow.py    # Main orchestrator
│   ├── solace_agent.py       # Emotional support
│   ├── harbor_agent.py       # Orientation
│   ├── roots_agent.py        # Family recognition
│   ├── legacy_agent.py       # Memory & stories
│   ├── echo_agent.py         # Pattern analysis
│   ├── guardian_agent.py     # Caregiver insights
│   ├── client_config.py      # Azure AI client config
│   └── service.py            # Agent service layer
├── tools/                    # Utility tools
├── main.py                   # FastAPI app entry point
├── database.py               # Database configuration
├── settings.py               # App settings
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── test_integration.py       # ⭐ Integration test script
└── API_AZURE_INTEGRATION.md  # ⭐ Detailed integration guide
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- pip or conda

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env and add your Azure AI configuration
```

**For Development (Free):**
Use GitHub Models:
```env
GITHUB_TOKEN=your_github_personal_access_token
MODEL_DEPLOYMENT_NAME=gpt-4o-mini
```

Get a GitHub PAT from: https://github.com/settings/tokens (needs `read:packages` scope)

**For Production:**
Use

### 6. Test the Integration (Optional)

```bash
# Test Azure AI agent integration
python test_integration.py
```

## 🤖 Azure AI Agent System

The backend features a sophisticated multi-agent system powered by Microsoft Agent Framework.

### Agent Architecture

**Aurora (Orchestrator)** - Routes requests to specialized agents:
- **Solace** - Emotional support and anxiety relief
- **Harbor** - Orientation (time, place, schedule)
- **Roots** - Family recognition
- **Legacy** - Personal memories and life stories
- **Echo** - Pattern analysis and repetition tracking
- **Guardian** - Caregiver insights and reporting

### Using the Agent API

Send a message to the AI system:

```bash
curl -X POST "http://localhost:8000/agents/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "user_input": "I feel scared and don't know where I am"
  }'
```
5. **agent_interactions** - AI agent conversation logs
6. **cognitive_insights** - Pattern analysis and metrics
7. **caregiver_alerts** - Automated alerts for caregivers

Response:
```json
{
  "agent_type": "solace",
  "response": "I can sense you're feeling worried. You are safe right now...",
  "intent": "emotional_support",
  "emotion_score": 0.8,
  "emotion_type": "anxious",
  "alert_triggered": true,
  "alert_message": "Patient showing signs of anxiety..."
}
```

📚 **See [API_AZURE_INTEGRATION.md](API_AZURE_INTEGRATION.md) for detailed documentation** Azure AI Foundry:
```env
FOUNDRY_PROJECT_ENDPOINT=https://your-project.api.azureml.ms
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4o
```

### 5. Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database

The application uses SQLite for data persistence. The database file (`app.db`) is automatically created on first run.

### Database Tables

1. **users** - User accounts (patients and caregivers)
2. **mood_checkins** - Mood tracking data
3. **memory_cards** - Memories and stories
4. **emergency_contacts** - Emergency contact information
🤖 AI Agents (New!)
- `POST /agents/ask` - ⭐ **Main agent interaction endpoint**
- `GET /agents/harbor/location/{user_id}` - Get orientation info
- `GET /agents/harbor/visits/{user_id}` - Get scheduled visits
- `GET /agents/roots/family/{user_id}` - Get family information
- `GET /agents/legacy/stories/{user_id}` - Get personal stories
- `POST /agents/solace/calm-mode/{user_id}` - Activate calm mode
- `GET /agents/guardian/dashboard/{user_id}` - Caregiver dashboard
- `GET /agents/echo/patterns/{user_id}` - Behavior patterns

### Agent Interactions
- `GET /agent_interactions` - Get interaction history
- `GET /agent_interactions/{interaction_id}` - Get specific interaction

### Cognitive Insights
- `GET /cognitive_insights` - Get cognitive analysis
- `POST /cognitive_insights` - Create insight

### Caregiver Alerts
- `GET /caregiver_alerts` - Get alerts
- `PUT /caregiver_alerts/{alert_id}` - Acknowledge alert

### 
## API Endpoints

### Users
- `POST /users/` - Create a new user
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get user details
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Mood Check-ins
- `POST /mood-checkins/` - Create mood check-in
- `GET /users/{user_id}/mood-checkins/` - Get user's mood history
- `GET /mood-checkins/{checkin_id}` - Get specific check-in
- `DELETE /mood-checkins/{checkin_id}` - Delete check-in

### Memory Cards
- `POST /memory-cards/` - Create memory card
- `GET /users/{user_id}/memory-cards/` - Get user's memories
- `GET /memory-cards/{card_id}` - Get specific memory
- `PUT /memory-cards/{card_id}` - Update memory
- `DELETE /memory-cards/{card_id}` - Delete memory
x] Add Azure AI multi-agent system
- [x] Add intelligent orchestration with Aurora
- [x] Add automatic caregiver alerts
- [x] Add emotion detection
- [x] Add pattern analysis
- [ ] Add authentication/authorization
- [ ] Add route protection with JWT tokens
- [ ] Add voice support for agent responses
- [ ] Add multi-language support
- [ ] Add long-term conversation memory
- [ ] Add database migration support (Alembic)
- [ ] Add comprehensive testing suite
- [ ] Add real-time caregiver dashboard
## Development

### Adding New Models

1. Create model in `app/models.py`
2. Create Pydantic schema in `app/schemas.py`
3. Add CRUD operations in `app/crud.py`
4. Add routes in `app/routes.py`

### Running Tests (Future)

```bash
pytest
```

## Next Steps

- [ ] Add authentication/authorization
- [ ] Add route protection with JWT tokens
- [ ] Add input validation enhancements
- [ ] Add logging
- [ ] Add error handling middleware
- [ ] Add database migration support (Alembic)
- [ ] Add integration with Agent Framework
- [ ] Add testing suite

## Troubleshooting

### Port Already in Use
Change the port in the command:
```bash
uvicorn main:app --reload --port 8001
```

### Module Not Found
Make sure your virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Database Issues
Delete `app.db` to reset the database:
```bash
rm app.db
```

## License

Part of the WithYou project.
