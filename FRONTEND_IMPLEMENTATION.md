# Frontend Integration Summary

This document outlines all the frontend changes made to integrate the WithYou application with the FastAPI backend.

## Files Created

### 1. **lib/types.ts** - TypeScript Types
Complete type definitions for all data models:
- `User` - Patient and Caregiver user types
- `AgentResponse` - Agent interaction responses
- `MemoryCard` - Patient memories and stories
- `EmergencyContact` - Family members
- `MoodCheckIn` - Mood tracking data
- `CognitiveInsight` - Insights about patient cognition
- `CaregiverAlert` - Alerts for caregivers
- `GuardianDashboard` - Caregiver dashboard data
- Plus 10+ supporting types for locations, visits, family info, etc.

### 2. **contexts/UserContext.tsx** - Global State Management
React Context Provider for managing:
- `currentUser` - Currently authenticated user
- `selectedPatient` - Patient being monitored (for caregivers)
- `setCurrentUser` / `setSelectedPatient` - State setters
- `isLoading` - Loading state for async operations
- `useUser()` hook - Access context from any component

Key features:
- Clears selected patient when user type changes
- 'use client' directive for client-side rendering
- Error handling if hook used outside provider

### 3. **app/layout.tsx** - Root Layout (Modified)
Updated to wrap entire app with UserProvider:
```tsx
<UserProvider>
  {children}
  <Analytics />
</UserProvider>
```

### 4. **app/page.tsx** - Home/Login Page (Replaced)
Multi-step user authentication flow:
- **Step 1: Role Selection** - Choose between Patient or Caregiver
- **Step 2: Login** - Select existing user or create new profile
- **Step 3: Register** - Create new patient/caregiver account

Features:
- Loads all users from backend on mount
- Filters patients for caregiver selection
- Creates new users via `createUser` API call
- Redirects to appropriate dashboard after login

### 5. **app/patient/page.tsx** - Patient Dashboard
Main patient interface with:

**Quick Action Buttons:**
- "Where Am I?" - Get current location
- "Family Photos" - View family members
- "Who's Visiting?" - See scheduled visits
- "Calm Mode" - Activate relaxation features

**Agent Response Area:**
- Real-time conversation display
- Emotion tracking display
- Voice response option
- Message auto-scroll

**Input Section:**
- Text message input with Enter to send
- Voice toggle button
- Loading states

**Mood Check-in:**
- 6 mood options (Happy, Calm, Anxious, Sad, Confused, Content)
- Quick mood logging

### 6. **app/caregiver/page.tsx** - Caregiver Dashboard
Comprehensive monitoring dashboard for caregivers:

**Alerts Section:**
- High-priority alert display (red background)
- Alert types (high_anxiety, disorientation, health_concern, needs_intervention)
- Acknowledge/Delete actions
- Timestamps and messages

**Statistics Cards:**
- Total interactions count
- Anxiety instances
- Routine questions

**Cognitive Insights:**
- Visual metrics display
- Insight types (anxiety_trend, orientation_trend, repetition, emotional_pattern)
- Descriptions and metric values

**Family Contacts:**
- Contact information display
- Relationship, phone, email
- Primary contact badge
- Delete functionality

**Memory Cards:**
- Image display
- Title and description
- Creation date
- Grid layout

**Selection Logic:**
- Prompts to select patient if not already selected
- Filters data by selected patient
- Confirms delete actions with dialog

## API Integration

All screens use the comprehensive API client from `lib/api.ts`:

### Patient Dashboard Uses:
- `askAgent()` - Send messages to agents
- `getLocation()` - Get location information
- `getScheduledVisits()` - Get upcoming visits
- `getFamilyMembers()` - Get family contact list
- `activateCalmMode()` - Activate calm mode
- `logMoodCheckIn()` - Log mood check-ins

### Caregiver Dashboard Uses:
- `getCaregiverDashboard()` - Get dashboard data
- `getCognitiveInsights()` - Get insights with period filter
- `getCaregiverAlerts()` - Get all alerts for caregiver
- `acknowledgeAlert()` - Mark alert as acknowledged
- `deleteAlert()` - Remove alert
- `getMemoryCards()` - Get patient's memories
- `getFamilyContacts()` - Get family contact list
- `deleteFamilyContact()` - Remove family contact

## UI Component Usage

All screens leverage existing component library:
- `Button` - CTA buttons with loading states
- `Card` - Container components
- `Input` - Text input fields
- `Textarea` - Multi-line text input
- `AlertDialog` - Confirmation dialogs
- Lucide icons - Visual indicators (`Loader`, `Bell`, `Volume2`, etc.)

## Context Integration

All screens access user state via `useUser()` hook:
```tsx
const { currentUser, selectedPatient, isLoading, setCurrentUser, setSelectedPatient } = useUser();
```

**Authentication Checks:**
- Patient pages redirect if `user_type !== 'patient'`
- Caregiver pages redirect if `user_type !== 'caregiver'`
- All pages check user loading state before rendering

## Data Flow

### Patient Registration Flow:
1. User lands on home page (`/`)
2. Selects "I'm a Patient"
3. Sees list of existing patients or creates new one
4. System creates User via `POST /users`
5. Sets context and redirects to `/patient`
6. Patient dashboard loads with `currentUser` ID

### Caregiver Flow:
1. User lands on home page (`/`)
2. Selects "I'm a Caregiver"
3. Selects patient to monitor (or creates if new)
4. System sets both `currentUser` and `selectedPatient`
5. Redirects to `/caregiver`
6. Caregiver dashboard loads all data for selected patient

### Agent Interaction Flow:
1. Patient types message in dashboard
2. `askAgent()` sends to `POST /agents/ask`
3. Aurora routes to appropriate agent
4. Agent response received and displayed
5. If voice enabled, response spoken via Web Speech API
6. Interaction logged in database

## Environment Configuration

The API client (`lib/api.ts`) uses:
```
API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
```

Add to `.env.local` for custom backend URL:
```
NEXT_PUBLIC_API_URL=http://your-backend-url:8000
```

## Key Features Implemented

✅ **Multi-role authentication** - Patient and Caregiver roles
✅ **Global state management** - UserContext with hooks
✅ **Patient dashboard** - Agent interactions, quick actions, mood tracking
✅ **Caregiver dashboard** - Alerts, insights, family management, analytics
✅ **Real-time feedback** - Loading states, error handling, voice output
✅ **Type safety** - Full TypeScript integration
✅ **Responsive design** - Mobile-friendly layouts
✅ **Error handling** - Try-catch blocks, user feedback

## Next Steps

### Immediate Enhancements:
1. **Add patient selection UI in caregiver dashboard** - Modal or sidebar for switching patients
2. **Implement voice input** - Web Speech API for patient questions
3. **Add authentication** - JWT tokens or session management
4. **Database persistence** - Save user preferences
5. **Notification system** - Real-time updates for caregivers

### Future Features:
1. **Video calls** - WebRTC integration
2. **Photos upload** - S3/Blob storage integration
3. **Scheduled medications** - Reminder system
4. **Emergency SOS** - Quick alert to primary contact
5. **Analytics dashboard** - Long-term trends
6. **Multi-language support** - i18n setup
7. **Accessibility improvements** - WCAG compliance

## Testing Checklist

- [ ] Create new patient user
- [ ] Create new caregiver user
- [ ] Patient can send message to agent
- [ ] Patient can view family members
- [ ] Patient can check location
- [ ] Patient can view upcoming visits
- [ ] Patient can activate calm mode
- [ ] Patient can log mood
- [ ] Caregiver can view patient dashboard
- [ ] Caregiver can view alerts
- [ ] Caregiver can acknowledge alerts
- [ ] Caregiver can view cognitive insights
- [ ] Caregiver can view family contacts
- [ ] Voice output works on patient dashboard
- [ ] Responsive design works on mobile
- [ ] Error handling displays proper messages

## File Structure

```
frontend/
├── app/
│   ├── layout.tsx (MODIFIED - Added UserProvider)
│   ├── page.tsx (REPLACED - New login/registration)
│   ├── patient/
│   │   └── page.tsx (NEW - Patient dashboard)
│   └── caregiver/
│       └── page.tsx (NEW - Caregiver dashboard)
├── contexts/
│   └── UserContext.tsx (NEW - Global state)
├── lib/
│   ├── api.ts (EXISTING - API client)
│   └── types.ts (NEW - Type definitions)
└── components/
    └── ui/ (EXISTING - Shadcn components)
```

## Troubleshooting

**Users not loading on home page:**
- Check backend is running on http://localhost:8000
- Verify CORS is configured in FastAPI settings
- Check console for error messages

**Agent responses not appearing:**
- Verify user ID is being passed correctly
- Check backend agent endpoints are working
- Use browser console to debug API calls

**Voice output not working:**
- Ensure browser supports Web Speech API
- Check browser permissions for audio
- Verify response text is not empty

**Caregiver dashboard shows no data:**
- Ensure patient is selected via context
- Verify patient has interactions/insights in database
- Check API returns data for that patient ID

## API Endpoint Reference

### Patient Routes
```
POST /agents/ask - Send message to agent
GET /agents/harbor/location/{user_id} - Get location
GET /agents/harbor/visits/{user_id} - Get visits
GET /agents/roots/family/{user_id} - Get family
POST /agents/solace/calm-mode/{user_id} - Activate calm
POST /mood-checkins - Log mood
```

### Caregiver Routes
```
GET /agents/guardian/dashboard/{user_id} - Get dashboard
GET /cognitive-insights - Get insights
GET /caregiver-alerts - Get alerts
PUT /caregiver-alerts/{alert_id}/acknowledge - Acknowledge alert
DELETE /caregiver-alerts/{alert_id} - Delete alert
GET /memory-cards/{user_id} - Get memories
GET /emergency-contacts/{user_id} - Get family
DELETE /emergency-contacts/{contact_id} - Delete contact
```

### User Routes
```
POST /users - Create user
GET /users - List all users
GET /users/{user_id} - Get user details
PUT /users/{user_id} - Update user
```

This integration provides a complete, type-safe frontend for the WithYou patient care system.
