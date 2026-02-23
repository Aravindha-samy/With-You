# WithYou API Integration Guide

## Overview

The WithYou backend is fully integrated to support both **Patient** and **Caregiver** workflows using AI agents. This guide explains how the frontend should interact with the API.

---

## Architecture

### Agent System

The backend uses **7 specialized agents** orchestrated by **Aurora**:

| Agent | Role | Triggered By | Key Operations |
|-------|------|--------------|-----------------|
| **Aurora** | Orchestrator | All requests | Routes to appropriate agent |
| **Harbor** | Orientation | Location/visit questions | Location, date, scheduled visits |
| **Roots** | Identity | "Who is this?" questions | Family recognition, photos |
| **Solace** | Emotional | Anxiety/fear queries | Reassurance, calm mode activation |
| **Legacy** | Story | Personal history | Life stories, work history |
| **Echo** | Memory Intelligence | All interactions | Pattern analysis, repetition tracking |
| **Guardian** | Caregiver Dashboard | Caregiver requests | Trend analysis, insights, alerts |

---

## API Structure

### Base URL
```
http://localhost:8000
```

### API Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Core Endpoints

#### 1. User Management
```
POST   /users/               - Create user (patient or caregiver)
GET    /users/               - List users
GET    /users/{user_id}      - Get user details
PUT    /users/{user_id}      - Update user
DELETE /users/{user_id}      - Delete user
```

#### 2. Memory & Stories
```
POST   /memory-cards/              - Create memory
GET    /users/{user_id}/memory-cards/  - Get user's memories
GET    /memory-cards/{card_id}     - Get specific memory
PUT    /memory-cards/{card_id}     - Update memory
DELETE /memory-cards/{card_id}     - Delete memory
```

#### 3. Family Information
```
POST   /emergency-contacts/              - Add family member
GET    /users/{user_id}/emergency-contacts/  - Get family list
GET    /emergency-contacts/{contact_id}  - Get family member details
PUT    /emergency-contacts/{contact_id}  - Update family member
DELETE /emergency-contacts/{contact_id}  - Delete family member
```

#### 4. Mood Tracking
```
POST   /mood-checkins/        - Log mood check-in
GET    /users/{user_id}/mood-checkins/  - Get mood history
GET    /mood-checkins/{checkin_id}      - Get specific check-in
DELETE /mood-checkins/{checkin_id}      - Delete check-in
```

---

## Agent Endpoints

### Main Agent Orchestration

#### **POST /agents/ask**
The primary endpoint for patient queries. Aurora will analyze and route to appropriate agent.

**Request:**
```json
{
  "user_id": 1,
  "user_input": "Where am I?",
  "agent_type": null,  // Optional: let Aurora auto-route
  "voice_enabled": false
}
```

**Response:**
```json
{
  "agent_type": "harbor",
  "response": "You're at home in Chennai. You moved here in 2018. You're safe.",
  "intent": "location",
  "emotion_score": 0.8,
  "emotion_type": "calm",
  "alert_triggered": false
}
```

---

### Specialized Agent Endpoints

#### **Harbor Agent (Orientation)**

**GET /agents/harbor/location/{user_id}**
- Get current location and orientation info
- Response includes: location, move year, safe message

**GET /agents/harbor/visits/{user_id}**
- Get scheduled family visits
- Response includes: list of visits with times

---

#### **Roots Agent (Family Recognition)**

**GET /agents/roots/family/{user_id}**
- Get family member information
- Returns: family list with photos and descriptions

---

#### **Solace Agent (Emotional Support)**

**POST /agents/solace/calm-mode/{user_id}**
- Activate calm mode for anxious patients
- Returns: music, photos, reassurance messages

---

#### **Legacy Agent (Stories)**

**GET /agents/legacy/stories/{user_id}**
- Get personal stories and memories
- Optional query params: skip, limit
- Returns: life narrative, work history, personal stories

---

#### **Guardian Agent (Caregiver Dashboard)**

**GET /agents/guardian/dashboard/{user_id}**
- Get comprehensive caregiver insights
- Returns:
  - Anxiety trends
  - Orientation trends
  - Repetition patterns
  - Recent interactions
  - Emotional analysis

---

#### **Echo Agent (Memory Patterns)**

**GET /agents/echo/patterns/{user_id}**
- Get behavior and memory patterns
- Returns:
  - Repetition frequency
  - Anxiety patterns
  - Emotional trends
  - Question patterns

---

## Agent Interaction Logging

### Log an Agent Interaction

**POST /agent-interactions/**
```json
{
  "user_id": 1,
  "agent_type": "harbor",
  "user_input": "Where am I?",
  "agent_response": "You're at home...",
  "intent": "location",
  "emotion_score": 0.8,
  "emotion_type": "calm",
  "is_routine": false
}
```

### Get Interaction History

**GET /agent-interactions/user/{user_id}**
- Query params: agent_type, skip, limit

---

## Cognitive Insights

### Create Insight (Guardian calls this)

**POST /cognitive-insights/**
```json
{
  "user_id": 1,
  "insight_type": "anxiety_trend",
  "metric_name": "weekly_anxiety",
  "metric_value": 0.65,
  "period": "weekly",
  "description": "Anxiety increased...

"
}
```

### Get User Insights

**GET /cognitive-insights/user/{user_id}**
- Query params: insight_type, period, skip, limit
- Insight types: anxiety_trend, orientation_trend, repetition, emotional_pattern
- Periods: daily, weekly, monthly

---

## Caregiver Alerts

### Create Alert (Agents trigger this)

**POST /caregiver-alerts/**
```json
{
  "user_id": 1,
  "caregiver_id": 2,
  "alert_type": "high_anxiety",
  "message": "Patient showing signs of high anxiety",
  "trigger_agent": "solace"
}
```

Alert types:
- `high_anxiety` - Patient anxiety levels critical
- `disorientation` - Repeated orientation questions
- `health_concern` - Potential health issue detected
- `needs_intervention` - Caregiver immediate attention needed

### Get Caregiver Alerts

**GET /caregiver-alerts/caregiver/{caregiver_id}**
- Query params: acknowledged (true/false), skip, limit

### Acknowledge Alert

**PUT /caregiver-alerts/{alert_id}**
```json
{
  "is_acknowledged": true
}
```

---

## Frontend Integration Workflow

### Patient Interface Flow

1. **User Taps a Button** (e.g., "Where am I?")
   ```
   POST /agents/ask
   {
     "user_id": 1,
     "user_input": "Where am I?"
   }
   ```

2. **System Routes to Harbor Agent**
   - Aurora analyzes intent: "location"
   - Routes to Harbor
   - Harbor returns location info

3. **Response Displayed with Voice (Optional)**
   - Text: "You're at home in Chennai..."
   - If voice_enabled: Azure Speech reads it aloud
   - Log interaction via `/agent-interactions/`

4. **Memory Updated**
   - Echo Agent logs pattern
   - Checks for repetition
   - Updates mood/emotion tracking

---

### Caregiver Dashboard Flow

1. **Load Dashboard**
   ```
   GET /agents/guardian/dashboard/{patient_id}
   ```

2. **Display Insights**
   - Show anxiety trends
   - Show repetition patterns
   - Show recent interactions
   - List unacknowledged alerts

3. **View Cognitive Trends**
   ```
   GET /cognitive-insights/user/{patient_id}?period=weekly
   ```

4. **Manage Alerts**
   ```
   GET /caregiver-alerts/caregiver/{caregiver_id}?acknowledged=false
   PUT /caregiver-alerts/{alert_id}
   ```

5. **Add Family Member**
   ```
   POST /emergency-contacts/
   {
     "user_id": 1,
     "name": "Anna",
     "phone": "...",
     "relationship": "daughter"
   }
   ```

---

## Data Models

### User
```json
{
  "id": 1,
  "name": "Raj",
  "email": "raj@example.com",
  "user_type": "patient",  // or "caregiver"
  "is_active": true,
  "created_at": "2023-01-01T00:00:00",
  "last_login": "2024-02-23T10:30:00"
}
```

### AgentInteraction
```json
{
  "id": 123,
  "user_id": 1,
  "agent_type": "harbor",
  "user_input": "Where am I?",
  "agent_response": "You're at home...",
  "intent": "location",
  "emotion_score": 0.8,
  "emotion_type": "calm",
  "is_routine": true,
  "timestamp": "2024-02-23T10:30:00"
}
```

### CognitiveInsight
```json
{
  "id": 456,
  "user_id": 1,
  "insight_type": "anxiety_trend",
  "metric_name": "weekly_anxiety",
  "metric_value": 0.65,
  "period": "weekly",
  "description": "Anxiety increased this week",
  "calculated_at": "2024-02-23T10:30:00"
}
```

### CaregiverAlert
```json
{
  "id": 789,
  "user_id": 1,
  "caregiver_id": 2,
  "alert_type": "high_anxiety",
  "trigger_agent": "solace",
  "message": "Patient showing signs of high anxiety",
  "is_acknowledged": false,
  "created_at": "2024-02-23T10:30:00"
}
```

---

## Error Handling

All endpoints return standard HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Resource Not Found
- `500` - Server Error

Error response format:
```json
{
  "detail": "User not found"
}
```

---

## Environment Variables

Located in `.env`:

```
DATABASE_URL=sqlite:///./app.db
ENVIRONMENT=development
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=True
CORS_ORIGINS=['http://localhost:3000']
```

---

## Next Steps for Frontend

1. **Create User Screen**
   - POST /users/ to create patients and caregivers

2. **Patient Dashboard**
   - Show large buttons: "Where am I?", "Family Photos", "Who is visiting?", "Calm Mode"
   - POST /agents/ask for each button
   - Display agent response with optional voice

3. **Memory/Photo Upload**
   - POST /memory-cards/ for stories
   - POST /emergency-contacts/ for family members
   - Display in "Family Photos" section

4. **Caregiver Dashboard**
   - GET /agents/guardian/dashboard/ for overview
   - GET /cognitive-insights/ for trends
   - GET /caregiver-alerts/ for notifications

5. **Mood Tracking**
   - POST /mood-checkins/ when user expresses emotions
   - Display charts from Echo patterns

---

## Testing

Use Swagger UI to test all endpoints:
```
http://localhost:8000/docs
```

All endpoints are interactive and fully documented with examples!

---

## Support

For issues or questions about the API:
1. Check the Swagger UI documentation
2. Review agent-specific endpoint descriptions
3. Check error messages in response body
