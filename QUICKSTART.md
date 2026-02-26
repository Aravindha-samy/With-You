# WithYou - Complete Application Setup Guide

A comprehensive patient care application with AI-powered agents for Alzheimer's patients and caregiver monitoring.

## Architecture Overview

```
WithYou Application
├── Frontend (Next.js + React + TypeScript)
│   ├── Patient Dashboard - Interaction interface
│   ├── Caregiver Dashboard - Monitoring & insights
│   └── Auth Flow - User selection & registration
├── Backend (FastAPI + SQLAlchemy + SQLite)
│   ├── Agent Orchestration - Aurora router
│   ├── 7 Specialized Agents - Harbor, Roots, Solace, Legacy, Echo, Guardian, Insights
│   └── Database - User, Interactions, Insights, Alerts
└── Database (SQLite)
    └── app.db - Auto-created on first run
```

## Prerequisites

- **Python 3.8+** for backend
- **Node.js 18+** for frontend
- **Git** for version control

## Backend Setup (FastAPI)

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env File (Optional)
```bash
# backend/.env (optional - defaults provided)
DATABASE_URL=sqlite:///./app.db
ENVIRONMENT=development
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 5. Run Backend Server
```bash
python main.py
```

Expected output:
```
INFO: Uvicorn running on http://0.0.0.0:8000 [Press ENTER to quit]
```

### 6. Test Backend
- Visit: http://localhost:8000/docs (Interactive API docs)
- Visit: http://localhost:8000/redoc (Alternative API docs)

## Frontend Setup (Next.js)

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
# Using pnpm (recommended)
pnpm install

# Or using npm
npm install

# Or using yarn
yarn install
```

### 3. Create .env.local File (Optional)
```bash
# frontend/.env.local (optional - defaults to localhost:8000)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4. Run Development Server
```bash
# Using pnpm
pnpm dev

# Or using npm
npm run dev

# Or using yarn
yarn dev
```

Expected output:
```
> next dev

  ○ Localhost:3000 ready in 0s
```

### 5. Open Application
Visit: http://localhost:3000 in your browser

## User Registration & Login

### Create Patient User
1. Select "I'm a Patient" on home page
2. Click "Create New Patient Profile"
3. Enter name and email
4. System creates user and redirects to patient dashboard

### Create Caregiver User
1. Select "I'm a Caregiver" on home page
2. Click "Create New Caregiver Profile"
3. Enter name and email
4. Select a patient to monitor
5. System creates user and redirects to caregiver dashboard

## Patient Interface Features

### Quick Actions
- **Where Am I?** - Returns patient's current location
- **Family Photos** - Shows family members with descriptions
- **Who's Visiting?** - Displays scheduled visits
- **Calm Mode** - Activates relaxation features

### Agent Interaction
- Type questions or messages
- Receive AI-powered responses from specialized agents
- 7 agents available:
  - **Harbor** - Location & orientation
  - **Roots** - Family recognition
  - **Solace** - Emotional support
  - **Legacy** - Personal stories
  - **Echo** - Memory patterns
  - **Guardian** - Caregiver insights
  - **Aurora** - Main orchestrator

### Mood Tracking
- Quick mood selection (Happy, Calm, Anxious, etc.)
- Logged automatically
- Influences agent responses

### Voice Features
- Toggle voice output
- Responses spoken aloud
- Browser must support Web Speech API

## Caregiver Dashboard Features

### Real-time Alerts
- High-priority notifications
- Alert types:
  - `high_anxiety` - Patient showing anxiety signs
  - `disorientation` - Confusion/disorientation detected
  - `health_concern` - Potential health issues
  - `needs_intervention` - Caregiver attention needed
- Acknowledge/dismiss actions

### Analytics & Insights
- Total interactions count
- Anxiety instance tracking
- Routine question metrics
- Cognitive trends visualization
- Insight types:
  - Anxiety trends
  - Orientation patterns
  - Repetition index
  - Emotional patterns

### Family Management
- Family contact information
- Phone numbers and emails
- Relationship tracking
- Primary contact designation
- Edit/delete contacts

### Patient Memory Cards
- Stored personal stories
- Associated images
- Creation dates
- View/manage memories

### Patient Selection
- Monitor multiple patients
- Switch between patients
- Patient-specific insights

## Testing the System

### Patient Workflow
1. Create patient user "Margaret"
2. Send message: "Where am I?"
3. Receive location response
4. Ask: "Who is visiting me?"
5. View scheduled visits
6. Select mood "Happy"
7. Activate calm mode
8. Toggle voice and hear response

### Caregiver Workflow
1. Create caregiver user "Sarah"
2. Select patient "Margaret"
3. View alerts dashboard
4. Review cognitive insights
5. Check family contacts
6. View interaction history
7. Acknowledge any alerts

### Backend Testing (via Swagger UI)
1. Open http://localhost:8000/docs
2. Expand `/users` endpoints
3. Create test users
4. Test `/agents/ask` endpoint
5. View all interactions in `/agent-interactions`

## Database Inspection

### View SQLite Database
```bash
# Using sqlite3 command line
sqlite3 backend/app.db

# Common queries:
SELECT * FROM user;  -- View users
SELECT * FROM agent_interaction;  -- View interactions
SELECT * FROM caregiver_alert;  -- View alerts
SELECT * FROM cognitive_insight;  -- View insights
```

## Troubleshooting

### Backend Issues

**ModuleNotFoundError**
```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

**Port 8000 Already in Use**
```bash
# Change port in settings.py or use:
python main.py --port 8001
```

**Database Locked**
```bash
# Remove old database and restart
rm backend/app.db
python main.py
```

### Frontend Issues

**Module Not Found**
```bash
# Clear cache and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

**API Connection Failed**
```bash
# Ensure backend is running on port 8000
# Check CORS configuration in backend/main.py
# Verify NEXT_PUBLIC_API_URL in .env.local
```

**Build Errors**
```bash
# Clear Next.js cache
rm -rf .next

# Rebuild
pnpm build
```

## Environment Variables Reference

### Backend (backend/.env)
```
DATABASE_URL=sqlite:///./app.db      # Database connection string
ENVIRONMENT=development               # development/production
DEBUG=True                           # Enable debug mode
API_HOST=0.0.0.0                    # API host
API_PORT=8000                       # API port
CORS_ORIGINS=http://localhost:3000  # Allowed origins
APP_TITLE=WithYou                   # Application title
APP_DESCRIPTION=Care Companion      # App description
APP_VERSION=1.0.0                   # Version number
```

### Frontend (frontend/.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend API URL
```

## Common Commands

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# Run with specific port
python main.py --port 8001

# Access Swagger UI
curl http://localhost:8000/docs

# View OpenAPI schema
curl http://localhost:8000/openapi.json
```

### Frontend
```bash
# Install dependencies
pnpm install

# Development server
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start

# Run linter
pnpm lint

# Format code
pnpm format
```

## Project Structure

```
WithYou/
├── backend/
│   ├── main.py                      # FastAPI app & router setup
│   ├── settings.py                  # Configuration management
│   ├── database.py                  # SQLAlchemy setup
│   ├── requirements.txt             # Python dependencies
│   ├── .env                         # Environment variables
│   ├── app/
│   │   ├── model/                   # SQLAlchemy ORM models
│   │   │   ├── user.py
│   │   │   ├── mood_checkin.py
│   │   │   ├── memory_card.py
│   │   │   ├── emergency_contact.py
│   │   │   ├── agent_interaction.py
│   │   │   ├── cognitive_insight.py
│   │   │   └── caregiver_alert.py
│   │   ├── api/                     # Route handlers
│   │   │   ├── users.py
│   │   │   ├── agents.py
│   │   │   ├── mood_checkins.py
│   │   │   ├── memory_cards.py
│   │   │   ├── emergency_contacts.py
│   │   │   ├── agent_interactions.py
│   │   │   ├── cognitive_insights.py
│   │   │   └── caregiver_alerts.py
│   │   ├── schemas.py               # Pydantic models
│   │   └── crud.py                  # Database operations
│   └── app.db                       # SQLite database (auto-created)
├── frontend/
│   ├── app/
│   │   ├── layout.tsx               # Root layout with UserProvider
│   │   ├── page.tsx                 # Home/login page
│   │   ├── patient/
│   │   │   └── page.tsx             # Patient dashboard
│   │   ├── caregiver/
│   │   │   └── page.tsx             # Caregiver dashboard
│   │   └── globals.css              # Global styles
│   ├── components/                   # React components
│   │   ├── ui/                      # Shadcn UI components
│   │   ├── patient-interface/       # Patient-specific components
│   │   ├── shared/                  # Shared components
│   │   └── caregiver-setup/         # Caregiver setup components
│   ├── contexts/
│   │   └── UserContext.tsx          # Global user state
│   ├── lib/
│   │   ├── api.ts                   # API client (30+ functions)
│   │   ├── types.ts                 # TypeScript type definitions
│   │   └── utils.ts                 # Utility functions
│   ├── hooks/
│   │   ├── use-mobile.ts
│   │   └── use-toast.ts
│   ├── package.json                 # Frontend dependencies
│   ├── next.config.mjs              # Next.js configuration
│   ├── tsconfig.json                # TypeScript configuration
│   └── pnpm-lock.yaml               # Lock file
├── README.md                         # Project overview
├── FRONTEND_INTEGRATION_GUIDE.md    # Frontend integration examples
├── API_INTEGRATION_GUIDE.md         # API endpoint reference
└── FRONTEND_IMPLEMENTATION.md       # This file
```

## Performance Optimizations

### Frontend
- Image optimization via Next.js Image component
- Code splitting & lazy loading
- React context for efficient state management
- CSS modules for style scoping
- Debounced API calls

### Backend
- SQLAlchemy query optimization
- Database indexing on user_id
- Connection pooling
- CORS caching
- Async request handling

## Security Considerations

### Current (Development)
- No authentication (open access)
- CORS enabled for localhost:3000
- Debug mode enabled
- No rate limiting

### Recommended for Production
- JWT token authentication
- Password hashing (bcrypt)
- HTTPS/SSL encryption
- Rate limiting
- Input validation
- SQL injection prevention
- CORS restriction
- Debug mode disabled
- Environment-based configuration

## Deployment

### Backend Deployment
```bash
# Build Docker image
docker build -t withyou-backend .

# Run container
docker run -p 8000:8000 withyou-backend

# Or deploy to cloud (AWS/Azure/GCP)
```

### Frontend Deployment
```bash
# Build production bundle
pnpm build

# Deploy to Vercel, Netlify, or cloud provider
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Support & Issues

For issues or questions:
1. Check the troubleshooting section above
2. Review error console (browser DevTools)
3. Check backend logs in terminal
4. Verify API is responding: `curl http://localhost:8000/docs`
5. Test individual endpoints via Swagger UI

## Next Development Steps

1. **Authentication** - Add JWT token-based auth
2. **Voice Input** - Implement Web Speech API for patient questions
3. **Real-time Notifications** - WebSocket for instant alerts
4. **File Upload** - Add family photos functionality
5. **Data Export** - Generate PDF reports for caregivers
6. **Multi-language** - i18n support
7. **Accessibility** - WCAG 2.1 compliance
8. **Mobile App** - React Native version
9. **Cloud Integration** - Azure OpenAI, Speech Services
10. **Advanced Analytics** - Dashboard with data visualization

---

**Last Updated:** 2024
**Version:** 1.0.0
**Status:** Ready for Development & Testing
