// API base URL
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Main agent request handler
export async function askAgent(userInput: string, userId: number, agentType?: string, voiceEnabled?: boolean) {
  try {
    const response = await fetch(`${API_URL}/agents/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        user_input: userInput,
        agent_type: agentType || null,
        voice_enabled: voiceEnabled || false,
      }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Agent request failed:', error);
    throw error;
  }
}

// User APIs
export async function createUser(userData: { name: string; email: string; user_type: 'patient' | 'caregiver' }) {
  const response = await fetch(`${API_URL}/users/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData),
  });

  if (!response.ok) throw new Error('Failed to create user');
  return await response.json();
}

export async function getUser(userId: number) {
  const response = await fetch(`${API_URL}/users/${userId}`);
  if (!response.ok) throw new Error('Failed to fetch user');
  return await response.json();
}

export async function getUsers() {
  const response = await fetch(`${API_URL}/users/`);
  if (!response.ok) throw new Error('Failed to fetch users');
  return await response.json();
}

// Agent Endpoints
export async function getLocation(userId: number) {
  const response = await fetch(`${API_URL}/agents/harbor/location/${userId}`);
  if (!response.ok) throw new Error('Failed to get location');
  return await response.json();
}

export async function getScheduledVisits(userId: number) {
  const response = await fetch(`${API_URL}/agents/harbor/visits/${userId}`);
  if (!response.ok) throw new Error('Failed to get visits');
  return await response.json();
}

export async function getFamilyMembers(userId: number) {
  const response = await fetch(`${API_URL}/agents/roots/family/${userId}`);
  if (!response.ok) throw new Error('Failed to get family members');
  return await response.json();
}

export async function activateCalmMode(userId: number) {
  const response = await fetch(`${API_URL}/agents/solace/calm-mode/${userId}`, {
    method: 'POST',
  });
  if (!response.ok) throw new Error('Failed to activate calm mode');
  return await response.json();
}

export async function getPersonalStories(userId: number, skip = 0, limit = 10) {
  const response = await fetch(
    `${API_URL}/agents/legacy/stories/${userId}?skip=${skip}&limit=${limit}`
  );
  if (!response.ok) throw new Error('Failed to get stories');
  return await response.json();
}

export async function getCaregiverDashboard(userId: number) {
  const response = await fetch(`${API_URL}/agents/guardian/dashboard/${userId}`);
  if (!response.ok) throw new Error('Failed to get dashboard');
  return await response.json();
}

export async function getMemoryPatterns(userId: number) {
  const response = await fetch(`${API_URL}/agents/echo/patterns/${userId}`);
  if (!response.ok) throw new Error('Failed to get patterns');
  return await response.json();
}

// Memory Cards APIs
export async function createMemoryCard(userId: number, title: string, description?: string, imageUrl?: string) {
  const response = await fetch(`${API_URL}/memory-cards/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      title,
      description,
      image_url: imageUrl,
    }),
  });

  if (!response.ok) throw new Error('Failed to create memory card');
  return await response.json();
}

export async function getMemoryCards(userId: number, skip = 0, limit = 100) {
  const response = await fetch(
    `${API_URL}/memory-cards/?user_id=${userId}&skip=${skip}&limit=${limit}`
  );
  if (!response.ok) throw new Error('Failed to get memory cards');
  return await response.json();
}

// Emergency Contacts (Family) APIs
export async function addFamilyMember(
  userId: number,
  name: string,
  phone: string,
  email?: string,
  relationship?: string,
  isPrimary?: boolean
) {
  const response = await fetch(`${API_URL}/emergency-contacts/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      name,
      phone,
      email,
      relationship,
      is_primary: isPrimary || false,
    }),
  });

  if (!response.ok) throw new Error('Failed to add family member');
  return await response.json();
}

export async function getFamilyContacts(userId: number) {
  const response = await fetch(`${API_URL}/emergency-contacts/?user_id=${userId}`);
  if (!response.ok) throw new Error('Failed to get family contacts');
  return await response.json();
}

export async function updateFamilyContact(
  contactId: number,
  data: {
    name?: string;
    phone?: string;
    email?: string;
    relationship?: string;
    is_primary?: boolean;
  }
) {
  const response = await fetch(`${API_URL}/emergency-contacts/${contactId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) throw new Error('Failed to update family contact');
  return await response.json();
}

export async function deleteFamilyContact(contactId: number) {
  const response = await fetch(`${API_URL}/emergency-contacts/${contactId}`, {
    method: 'DELETE',
  });

  if (!response.ok) throw new Error('Failed to delete family contact');
  return await response.json();
}

// Mood Check-in APIs
export async function logMoodCheckIn(userId: number, mood: string, notes?: string) {
  const response = await fetch(`${API_URL}/mood-checkins/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      mood,
      notes,
    }),
  });

  if (!response.ok) throw new Error('Failed to log mood check-in');
  return await response.json();
}

export async function getMoodHistory(userId: number, skip = 0, limit = 100) {
  const response = await fetch(`${API_URL}/mood-checkins/?user_id=${userId}&skip=${skip}&limit=${limit}`);
  if (!response.ok) throw new Error('Failed to get mood history');
  return await response.json();
}

// Agent Interactions APIs
export async function logAgentInteraction(
  userId: number,
  agentType: string,
  userInput: string,
  agentResponse: string,
  intent?: string,
  emotionScore?: number,
  emotionType?: string,
  isRoutine?: boolean
) {
  const response = await fetch(`${API_URL}/agent-interactions/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      agent_type: agentType,
      user_input: userInput,
      agent_response: agentResponse,
      intent,
      emotion_score: emotionScore,
      emotion_type: emotionType,
      is_routine: isRoutine || false,
    }),
  });

  if (!response.ok) throw new Error('Failed to log agent interaction');
  return await response.json();
}

export async function getAgentInteractions(userId: number, agentType?: string, skip = 0, limit = 100) {
  const query = new URLSearchParams({
    skip: skip.toString(),
    limit: limit.toString(),
  });

  if (agentType) {
    query.append('agent_type', agentType);
  }

  const response = await fetch(`${API_URL}/agent-interactions/user/${userId}?${query}`);
  if (!response.ok) throw new Error('Failed to get agent interactions');
  return await response.json();
}

// Cognitive Insights APIs
export async function getCognitiveInsights(
  userId: number,
  insightType?: string,
  period?: string,
  skip = 0,
  limit = 100
) {
  const query = new URLSearchParams({
    skip: skip.toString(),
    limit: limit.toString(),
  });

  if (insightType) {
    query.append('insight_type', insightType);
  }

  if (period) {
    query.append('period', period);
  }

  const response = await fetch(`${API_URL}/cognitive-insights/user/${userId}?${query}`);
  if (!response.ok) throw new Error('Failed to get cognitive insights');
  return await response.json();
}

// Caregiver Alerts APIs
export async function getCaregiverAlerts(caregiverId: number, acknowledged?: boolean, skip = 0, limit = 100) {
  const query = new URLSearchParams({
    skip: skip.toString(),
    limit: limit.toString(),
  });

  if (acknowledged !== undefined) {
    query.append('acknowledged', acknowledged.toString());
  }

  const response = await fetch(`${API_URL}/caregiver-alerts/caregiver/${caregiverId}?${query}`);
  if (!response.ok) throw new Error('Failed to get alerts');
  return await response.json();
}

export async function acknowledgeAlert(alertId: number) {
  const response = await fetch(`${API_URL}/caregiver-alerts/${alertId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ is_acknowledged: true }),
  });

  if (!response.ok) throw new Error('Failed to acknowledge alert');
  return await response.json();
}

export async function deleteAlert(alertId: number) {
  const response = await fetch(`${API_URL}/caregiver-alerts/${alertId}`, {
    method: 'DELETE',
  });

  if (!response.ok) throw new Error('Failed to delete alert');
  return await response.json();
}
