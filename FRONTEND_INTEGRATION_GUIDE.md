# Frontend Integration Guide: Connecting UI to WithYou Agents

## Quick Overview

Your frontend needs to connect to these 3 main API categories:

1. **User Management** - Create/manage patient and caregiver accounts
2. **Agent Endpoints** - Get responses from specialized agents
3. **Data Storage** - Store/retrieve family info, memories, mood data

---

## 1. Patient Interface Integration

### Scenario 1: Large Button Click - "Where am I?"

**UI Component**: `Header.tsx` (Where am I? button)

**Frontend Code**:
```typescript
const handleWhereAmI = async () => {
  const userId = getCurrentUserId(); // Get from context/auth
  
  const response = await fetch('http://localhost:8000/agents/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      user_input: "Where am I?",
      voice_enabled: true  // Enable voice response
    })
  });
  
  const data = await response.json();
  
  // Display response
  displayMessage(data.response);
  
  // Optional: Play audio
  if (data.voice_enabled) {
    playAudio(data.response);
  }
  
  // Log interaction
  logInteraction(data);
};
```

---

### Scenario 2: Family Photos Button

**UI Component**: `MemoryCard.tsx`

**Frontend Code**:
```typescript
// On component mount, fetch family members
useEffect(() => {
  const fetchFamily = async () => {
    const response = await fetch(
      `http://localhost:8000/agents/roots/family/${userId}`
    );
    const data = await response.json();
    setFamilyMembers(data.family_members);
  };
  
  fetchFamily();
}, [userId]);

// When user taps on a family member
const handleFamilyMemberTap = async (familyMember) => {
  const response = await fetch('http://localhost:8000/agents/ask', {
    method: 'POST',
    body: JSON.stringify({
      user_id: userId,
      user_input: `Who is ${familyMember.name}?`,
      voice_enabled: true
    })
  });
  
  const data = await response.json();
  displayMessage(data.response);
};
```

---

### Scenario 3: Mood Check-In

**UI Component**: `MoodCheckIn.tsx`

**Frontend Code**:
```typescript
const handleMoodSelection = async (mood: string, notes?: string) => {
  // Log mood check-in
  const moodResponse = await fetch('http://localhost:8000/mood-checkins/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      mood: mood,
      notes: notes
    })
  });
  
  // Send to Solace for emotional response
  const agentResponse = await fetch('http://localhost:8000/agents/ask', {
    method: 'POST',
    body: JSON.stringify({
      user_id: userId,
      user_input: `I'm feeling ${mood}. ${notes || ''}`,
      voice_enabled: true
    })
  });
  
  const data = await agentResponse.json();
  
  // If anxiety is high, offer calm mode
  if (data.emotion_score > 0.7 && data.emotion_type === 'anxious') {
    handleCalmMode();
  } else {
    displayMessage(data.response);
  }
};
```

---

### Scenario 4: Calm Mode

**UI Component**: `CalmMode.tsx`

**Frontend Code**:
```typescript
const handleCalmMode = async () => {
  const response = await fetch(`http://localhost:8000/agents/solace/calm-mode/${userId}`, {
    method: 'POST'
  });
  
  const data = await response.json();
  
  // Play music
  playMusic(data.content.music);
  
  // Show photo slideshow
  showPhotoSlideshow(data.content.photos);
  
  // Display reassurance message
  displayMessage(data.content.reassurance);
  
  // Enable fullscreen calm mode
  goFullscreen();
};
```

---

### Scenario 5: Voice Input Processing

**UI Component**: `Header.tsx` (Mic button)

**Frontend Code**:
```typescript
const handleVoiceInput = async (transcript: string) => {
  // Get voice transcript from Azure Speech to Text
  // (Handled by frontend speech recognition)
  
  const response = await fetch('http://localhost:8000/agents/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      user_input: transcript,  // e.g., "Is Anna coming today?"
      agent_type: null,  // Let Aurora route automatically
      voice_enabled: true
    })
  });
  
  const data = await response.json();
  
  // Display text response
  displayMessage(data.response);
  
  // Play voice response (Azure Speech to Text)
  playVoiceResponse(data.response);
  
  // Check for alerts
  if (data.alert_triggered) {
    notifyCaregiver(data.alert_message);
  }
};
```

---

## 2. Caregiver Dashboard Integration

### Setup Screen: Add Family Member

**UI Component**: `CaregiverSetupGuide.tsx`

**Frontend Code**:
```typescript
const handleAddFamilyMember = async (formData) => {
  const response = await fetch('http://localhost:8000/emergency-contacts/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: patientId,
      name: formData.name,
      phone: formData.phone,
      email: formData.email,
      relationship: formData.relationship,
      is_primary: formData.isPrimary
    })
  });
  
  const familyMember = await response.json();
  setFamilyMembers([...familyMembers, familyMember]);
  showSuccessMessage(`${familyMember.name} added successfully!`);
};
```

---

### Dashboard: View Insights

**UI Component**: Caregiver Dashboard (new)

**Frontend Code**:
```typescript
useEffect(() => {
  const loadDashboardData = async () => {
    // Get comprehensive insights
    const dashboardResp = await fetch(
      `http://localhost:8000/agents/guardian/dashboard/${patientId}`
    );
    const dashboard = await dashboardResp.json();
    
    // Get cognitive insights
    const insightsResp = await fetch(
      `http://localhost:8000/cognitive-insights/user/${patientId}?period=weekly`
    );
    const insights = await insightsResp.json();
    
    // Get recent alerts
    const alertsResp = await fetch(
      `http://localhost:8000/caregiver-alerts/caregiver/${caregiverId}?acknowledged=false`
    );
    const alerts = await alertsResp.json();
    
    setDashboard(dashboard);
    setInsights(insights);
    setAlerts(alerts);
  };
  
  loadDashboardData();
  // Poll every 5 minutes for updates
  const interval = setInterval(loadDashboardData, 5 * 60 * 1000);
  
  return () => clearInterval(interval);
}, [patientId, caregiverId]);

// Display data in charts/components
const displayTrends = () => {
  return (
    <div>
      <h2>Cognitive Trends</h2>
      <p>Anxiety Level: {dashboard.insights[0]?.metric_value}</p>
      <p>Repetition Count: {dashboard.routine_questions}</p>
      <p>Recent Direction: {calculateTrend(insights)}</p>
    </div>
  );
};
```

---

### Dashboard: Manage Alerts

**UI Component**: Alerts section

**Frontend Code**:
```typescript
const handleAcknowledgeAlert = async (alertId: number) => {
  const response = await fetch(`http://localhost:8000/caregiver-alerts/${alertId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      is_acknowledged: true
    })
  });
  
  const updatedAlert = await response.json();
  
  // Update local state
  setAlerts(alerts.map(a => a.id === alertId ? updatedAlert : a));
  
  // Show confirmation
  showNotification('Alert acknowledged');
};

// Render alerts
return (
  <div className="alerts">
    {alerts.map(alert => (
      <div key={alert.id} className="alert-card">
        <h3>{alert.alert_type}</h3>
        <p>{alert.message}</p>
        <button onClick={() => handleAcknowledgeAlert(alert.id)}>
          Acknowledge
        </button>
      </div>
    ))}
  </div>
);
```

---

## 3. Memory Cards Upload

**UI Component**: Settings/Profile

**Frontend Code**:
```typescript
const handleUploadMemory = async (title, description, imageFile) => {
  // First upload image to Blob Storage
  const imageUrl = await uploadToBlob(imageFile);
  
  // Then create memory card
  const response = await fetch('http://localhost:8000/memory-cards/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: patientId,
      title: title,
      description: description,
      image_url: imageUrl
    })
  });
  
  const memoryCard = await response.json();
  setMemories([...memories, memoryCard]);
  showSuccessMessage('Memory saved!');
};
```

---

## 4. Handling Agent Responses with Emotions

**Utility Function**:
```typescript
// Handle different emotional states
const handleAgentResponse = (agentResponse) => {
  const { emotion_score, emotion_type, response, alert_triggered } = agentResponse;
  
  // High anxiety - offer calm mode
  if (emotion_score > 0.7 && emotion_type === 'anxious') {
    showCalmModeButton();
    notifyCaregiver('Patient showing signs of anxiety');
  }
  
  // Disorientation - offer extra orientation
  if (emotion_type === 'confused' || emotion_type === 'disoriented') {
    offerOrientationHelp();
  }
  
  // Normal state - just display response
  displayMessage({
    text: response,
    emotion: emotion_type,
    icon: getEmotionIcon(emotion_type)
  });
  
  // Create caregiver alert if needed
  if (alert_triggered) {
    createAlert({
      type: 'system_generated',
      message: response
    });
  }
};
```

---

## 5. Real-time Updates with WebSockets (Future)

For real-time alerts and mood updates, consider WebSocket integration:

```typescript
// Future implementation
const ws = new WebSocket('ws://localhost:8000/ws/caregiver/{caregiver_id}');

ws.onmessage = (event) => {
  const alert = JSON.parse(event.data);
  
  if (alert.type === 'high_anxiety') {
    showNotification('Patient needs attention!');
    playAlertSound();
  }
};
```

---

## 6. Error Handling

```typescript
const fetchAgentResponse = async (request) => {
  try {
    const response = await fetch('http://localhost:8000/agents/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    });
    
    if (!response.ok) {
      if (response.status === 404) {
        showError('User not found');
      } else if (response.status === 500) {
        showError('Server error - please try again');
      }
      return null;
    }
    
    return await response.json();
  } catch (error) {
    showError('Network error - check your connection');
    console.error(error);
    return null;
  }
};
```

---

## 7. Testing Endpoints Locally

Use Swagger UI while developing:

```
http://localhost:8000/docs
```

All endpoints are documented and testable directly in the browser!

---

## 8. Required Environment Variables (Frontend)

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENABLE_VOICE=true
REACT_APP_ENABLE_ALERTS=true
```

---

## 9. TypeScript Types (Optional but Recommended)

```typescript
// types/agent.ts
export interface AgentRequest {
  user_id: number;
  user_input: string;
  agent_type?: string;
  voice_enabled?: boolean;
}

export interface AgentResponse {
  agent_type: string;
  response: string;
  intent?: string;
  emotion_score?: number;
  emotion_type?: string;
  alert_triggered?: boolean;
  alert_message?: string;
}

export interface CaregiverAlert {
  id: number;
  user_id: number;
  caregiver_id: number;
  alert_type: string;
  message: string;
  is_acknowledged: boolean;
  created_at: string;
}
```

---

## Summary of Key API Calls

| Action | Endpoint | Method | Use Case |
|--------|----------|--------|----------|
| Ask Agent | `POST /agents/ask` | POST | Any patient query |
| Get Location | `GET /agents/harbor/location/{user_id}` | GET | "Where am I?" button |
| Get Visits | `GET /agents/harbor/visits/{user_id}` | GET | "Who is visiting?" |
| Get Family | `GET /agents/roots/family/{user_id}` | GET | Family photos screen |
| Calm Mode | `POST /agents/solace/calm-mode/{user_id}` | POST | Anxiety trigger |
| Dashboard | `GET /agents/guardian/dashboard/{user_id}` | GET | Caregiver overview |
| Get Insights | `GET /cognitive-insights/user/{user_id}` | GET | Trends & patterns |
| Get Alerts | `GET /caregiver-alerts/caregiver/{caregiver_id}` | GET | Alert list |
| Add Family | `POST /emergency-contacts/` | POST | Setup screen |
| Save Memory | `POST /memory-cards/` | POST | Memory upload |

---

Ready to build! Start with the largest buttons and work your way to advanced features.
