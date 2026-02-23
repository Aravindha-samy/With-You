# WithYou Azure AI Agents

Azure AI-powered multi-agent system for Alzheimer's patient care.

## 🎯 Overview

This is a production-ready implementation of the WithYou care system using **Microsoft Agent Framework** and **Azure AI**. The system features 6 specialized AI agents orchestrated by Aurora for comprehensive Alzheimer's patient support.

## 🤖 Agent Architecture

### Aurora Orchestrator
The main coordinator that:
- Analyzes user intent and emotional state
- Routes requests to specialized agents
- Manages multi-agent workflows
- Provides streaming responses

### Specialized Agents

#### 1. **Solace** - Emotional Support Agent
- Anxiety relief and stress reduction
- Emotional reassurance
- Calm mode activation
- Breathing exercises
- Crisis de-escalation

#### 2. **Harbor** - Orientation Specialist
- Location awareness ("Where am I?")
- Time and date orientation
- Schedule information
- Visitor tracking
- Environmental context

#### 3. **Roots** - Family Recognition Agent
- Family member identification
- Relationship context
- Personal connections
- Contact information
- Building family bonds

#### 4. **Legacy** - Memory & Story Agent
- Personal memory recall
- Life story narration
- Work history and accomplishments
- Family milestones
- Biographical continuity

#### 5. **Echo** - Pattern Analysis Agent
- Interaction pattern detection
- Repetition tracking
- Emotional trend analysis
- Anxiety monitoring
- Cognitive insights

#### 6. **Guardian** - Caregiver Insights Agent
- Daily/weekly reports
- Cognitive health summaries
- Alert generation
- Trend reporting
- Care recommendations

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

### 2. Configure Environment

Choose either **GitHub Models** (free, recommended for development) or **Azure AI Foundry** (production).

#### Option A: GitHub Models (Free)

1. Get a GitHub Personal Access Token (PAT):
   - Go to https://github.com/settings/tokens
   - Generate a new token with `read:packages` scope

2. Update `.env`:
   ```env
   GITHUB_TOKEN=your_github_pat_here
   MODEL_DEPLOYMENT_NAME=gpt-4o-mini
   ```

#### Option B: Azure AI Foundry (Production)

1. Create an Azure AI Foundry project
2. Deploy a model (recommended: `gpt-4o` or `claude-sonnet-4-5`)
3. Update `.env`:
   ```env
   FOUNDRY_PROJECT_ENDPOINT=https://your-project.api.azureml.ms
   FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4o
   ```

### 3. Run the Agent Server

```bash
python agent_server.py
```

The server will start on `http://localhost:8001`

### 4. Test the Agents

```bash
# Test via HTTP POST
curl -X POST http://localhost:8001/runs \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "I feel anxious"}]}'
```

## 🔍 Debugging with AI Toolkit

### Using VS Code Debugger

1. Install AI Toolkit extension in VS Code
2. Press `F5` or select "Debug WithYou AI Agents" from the debug panel
3. The Agent Inspector will open automatically
4. Set breakpoints in agent code
5. Test agents interactively through the Inspector

### Manual Testing

```bash
# Install agentdev for interactive testing
pip install agent-dev-cli --pre

# Run with verbose logging
agentdev run agent_server.py --verbose --port 8087
```

## 📁 File Structure

```
azure_agents/
├── __init__.py              # Package exports
├── client_config.py         # Azure AI client configuration
├── aurora_workflow.py       # Main orchestrator workflow
├── solace_agent.py         # Emotional support agent
├── harbor_agent.py         # Orientation agent
├── roots_agent.py          # Family recognition agent
├── legacy_agent.py         # Memory/story agent
├── echo_agent.py           # Pattern analysis agent
└── guardian_agent.py       # Caregiver insights agent

agent_server.py             # HTTP server entry point
.env                        # Configuration (not in git)
```

## 🔧 Configuration

### Environment Variables

```env
# Azure AI Configuration
GITHUB_TOKEN=               # GitHub PAT for GitHub Models
MODEL_ENDPOINT=             # Default: https://models.github.ai/inference/
MODEL_DEPLOYMENT_NAME=      # e.g., gpt-4o-mini

# OR for Foundry
FOUNDRY_PROJECT_ENDPOINT=   # Your Foundry project endpoint
FOUNDRY_MODEL_DEPLOYMENT_NAME=  # Your deployed model

# Database
DATABASE_URL=sqlite:///./app.db

# Server
AGENT_HTTP_PORT=8001
```

## 🎨 Agent Customization

Each agent has specialized instructions that can be modified in their respective files:

```python
# Example: Customize Solace agent
self.agent = client.create_agent(
    model=model,
    name="SolaceAgent",
    instructions="""Your custom instructions here..."""
)
```

## 📊 Database Integration

Agents have access to the existing SQLAlchemy database:
- User profiles
- Memory cards
- Emergency contacts
- Interaction history
- Mood check-ins

Access the database in any agent:
```python
from app.model.user import User
user = self.db.query(User).filter_by(id=user_id).first()
```

## 🔐 Security & Privacy

- Patient data never leaves your environment
- All processing happens locally or in your Azure tenant
- Database is local SQLite (can be upgraded to Azure SQL)
- No data is sent to third parties
- HIPAA-compliant when using Azure AI Foundry

## 🚀 Deployment

### Local Development
```bash
python agent_server.py
```

### Production (Azure AI Foundry)
1. Ensure Foundry configuration in `.env`
2. Use the AI Toolkit extension:
   - Command Palette → "Microsoft Foundry: Deploy Hosted Agent"
3. Or containerize and deploy to Azure Container Apps

## 📈 Monitoring & Tracing

Add tracing to monitor agent performance:

```python
# TODO: Add Azure Monitor integration
from azure.monitor.opentelemetry import configure_azure_monitor
configure_azure_monitor()
```

## 🧪 Testing

```bash
# Test individual agents
python -m pytest tests/test_agents.py

# Test workflow
python -m pytest tests/test_workflow.py

# Integration tests
python -m pytest tests/test_integration.py
```

## 📚 Resources

- [Microsoft Agent Framework Docs](https://github.com/microsoft/agent-framework)
- [Azure AI Foundry](https://ai.azure.com)
- [GitHub Models](https://github.com/marketplace/models)
- [AI Toolkit Extension](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## 📝 License

See main project LICENSE file.

## 💡 Tips

- Start with GitHub Models (free) for development
- Use `gpt-4o-mini` for cost-effective testing
- Upgrade to `gpt-4o` or `claude-sonnet-4-5` for production
- Enable debug mode for detailed logging
- Use Agent Inspector for interactive testing
- Monitor token usage in production

## ⚠️ Important Notes

- Requires Python 3.10+
- Azure AI Agent Framework is in preview (beta)
- Pin package versions to avoid breaking changes
- Test thoroughly before production deployment
- Ensure proper error handling for patient safety

## 🆘 Support

For issues or questions:
1. Check the logs in the terminal
2. Verify `.env` configuration
3. Test with simple messages first
4. Use Agent Inspector for debugging
5. Review agent instructions for customization
