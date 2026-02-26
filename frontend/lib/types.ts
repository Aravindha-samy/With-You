// User Types
export interface User {
  id: number;
  name: string;
  email: string;
  user_type: 'patient' | 'caregiver';
  is_active: boolean;
  created_at: string;
  last_login?: string;
}

// Agent Types
export interface AgentResponse {
  agent_type: string;
  response: string;
  intent?: string;
  emotion_score?: number;
  emotion_type?: string;
  alert_triggered?: boolean;
  alert_message?: string;
}

export interface AgentRequest {
  user_id: number;
  user_input: string;
  agent_type?: string;
  voice_enabled?: boolean;
}

// Memory Card Types
export interface MemoryCard {
  id: number;
  user_id: number;
  title: string;
  description?: string;
  image_url?: string;
  created_at: string;
  updated_at: string;
}

// Emergency Contact Types
export interface EmergencyContact {
  id: number;
  user_id: number;
  name: string;
  phone: string;
  email?: string;
  relationship?: string;
  is_primary: boolean;
  created_at: string;
}

// Mood Check-in Types
export interface MoodCheckIn {
  id: number;
  user_id: number;
  mood: string;
  notes?: string;
  timestamp: string;
}

// Agent Interaction Types
export interface AgentInteraction {
  id: number;
  user_id: number;
  agent_type: string;
  user_input: string;
  agent_response: string;
  intent?: string;
  emotion_score?: number;
  emotion_type?: string;
  is_routine: boolean;
  timestamp: string;
}

// Cognitive Insight Types
export interface CognitiveInsight {
  id: number;
  user_id: number;
  insight_type: string; // 'anxiety_trend', 'orientation_trend', 'repetition', 'emotional_pattern'
  metric_name: string;
  metric_value: number;
  period: string; // 'daily', 'weekly', 'monthly'
  description?: string;
  calculated_at: string;
}

// Caregiver Alert Types
export interface CaregiverAlert {
  id: number;
  user_id: number;
  caregiver_id: number;
  alert_type: string; // 'high_anxiety', 'disorientation', 'health_concern', 'needs_intervention'
  trigger_agent?: string;
  message: string;
  is_acknowledged: boolean;
  acknowledged_at?: string;
  created_at: string;
}

// Guardian Dashboard Types
export interface GuardianSummary {
  summary: string;
  emotional_trend: 'stable' | 'declining' | 'improving';
  orientation_trend: 'stable' | 'declining' | 'improving';
  alert_level: 'none' | 'monitor' | 'intervene';
}

export interface GuardianDashboard {
  user_id: number;
  daily_summary: GuardianSummary;
  weekly_report: GuardianSummary;
  intervention_needed: boolean;
  // Legacy fields for backward compatibility
  total_interactions?: number;
  anxiety_instances?: number;
  routine_questions?: number;
  insights?: CognitiveInsight[];
  recent_interactions?: AgentInteraction[];
}

// Location Info Types
export interface LocationInfo {
  location: string;
  move_year?: number;
  city?: string;
  message: string;
}

// Visits Types
export interface ScheduledVisit {
  id: number;
  name: string;
  time: string;
  relationship?: string;
}

export interface VisitsInfo {
  visits: ScheduledVisit[];
  message: string;
}

// Family Info Types
export interface FamilyInfo {
  family_members: EmergencyContact[];
  total: number;
}

// Calm Mode Types
export interface CalmModeContent {
  music?: string;
  photos: string[];
  reassurance: string;
}

export interface CalmModeResponse {
  status: string;
  message: string;
  content: CalmModeContent;
}

// Memory Patterns Types
export interface MemoryPatterns {
  user_id: number;
  total_interactions: number;
  intent_patterns: Record<string, number>;
  emotion_patterns: Record<string, number>;
  repetition_index: number;
}

// API Error Type
export interface ApiError {
  detail: string;
}
