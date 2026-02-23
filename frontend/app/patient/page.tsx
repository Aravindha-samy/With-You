'use client';

import React, { useState, useRef, useEffect } from 'react';
import { useUser } from '@/contexts/UserContext';
import {
  askAgent,
  getLocation,
  getScheduledVisits,
  getFamilyMembers,
  activateCalmMode,
  logMoodCheckIn,
} from '@/lib/api';
import { AgentResponse, LocationInfo, VisitsInfo, FamilyInfo, EmergencyContact } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Volume2, Loader, Clock, Users, Heart, Music } from 'lucide-react';

export default function PatientDashboard() {
  const { currentUser, isLoading: userLoading } = useUser();
  const [message, setMessage] = useState('');
  const [agentResponse, setAgentResponse] = useState<AgentResponse | null>(null);
  const [isVoiceEnabled, setIsVoiceEnabled] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [locationInfo, setLocationInfo] = useState<LocationInfo | null>(null);
  const [visitsInfo, setVisitsInfo] = useState<VisitsInfo | null>(null);
  const [familyMembers, setFamilyMembers] = useState<EmergencyContact[]>([]);
  const messageEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest message
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [agentResponse]);

  // Redirect if not authenticated as patient
  useEffect(() => {
    if (!userLoading && (!currentUser || currentUser.user_type !== 'patient')) {
      window.location.href = '/';
    }
  }, [currentUser, userLoading]);

  if (userLoading || !currentUser) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader className="animate-spin w-8 h-8" />
      </div>
    );
  }

  const handleAskAgent = async (userInput?: string) => {
    const input = userInput || message;
    if (!input.trim() || !currentUser) return;

    setIsLoading(true);
    try {
      const response = await askAgent(input, currentUser.id, undefined, isVoiceEnabled);
      setAgentResponse(response);
      setMessage('');
      
      // Speak the response if voice is enabled
      if (isVoiceEnabled && 'speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(response.response);
        window.speechSynthesis.speak(utterance);
      }
    } catch (error) {
      console.error('Error asking agent:', error);
      setAgentResponse({
        agent_type: 'error',
        response: 'Sorry, I encountered an error. Please try again.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickAction = async (action: 'location' | 'visits' | 'family' | 'calm') => {
    if (!currentUser) return;
    
    setIsLoading(true);
    try {
      switch (action) {
        case 'location': {
          const data = await getLocation(currentUser.id);
          setLocationInfo(data);
          await handleAskAgent(`Tell me where I am. I'm currently in ${data.location}`);
          break;
        }
        case 'visits': {
          const data = await getScheduledVisits(currentUser.id);
          setVisitsInfo(data);
          const visitsText = data.visits.map((v: any) => `${v.name} at ${v.time}`).join(', ');
          await handleAskAgent(`Who is visiting me? ${visitsText}`);
          break;
        }
        case 'family': {
          const data = await getFamilyMembers(currentUser.id);
          setFamilyMembers(data.family_members);
          const familyText = data.family_members.map((f: any) => f.name).join(', ');
          await handleAskAgent(`Tell me about my family: ${familyText}`);
          break;
        }
        case 'calm': {
          const response = await activateCalmMode(currentUser.id);
          setAgentResponse({
            agent_type: 'solace',
            response: response.message,
          });
          break;
        }
      }
    } catch (error) {
      console.error('Error with quick action:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleMoodCheckIn = async (mood: string) => {
    if (!currentUser) return;
    
    try {
      await logMoodCheckIn(currentUser.id, mood);
      setAgentResponse({
        agent_type: 'solace',
        response: `I've noted that you're feeling ${mood}. How can I help you feel better?`,
      });
    } catch (error) {
      console.error('Error logging mood:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-indigo-50 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 pt-4">
          <h1 className="text-4xl font-bold text-blue-900 mb-2">Welcome, {currentUser.name}!</h1>
          <p className="text-lg text-gray-600">How can I help you today?</p>
        </div>

        {/* Quick Action Buttons */}
        <div className="grid grid-cols-2 gap-4 mb-8">
          <button
            onClick={() => handleQuickAction('location')}
            disabled={isLoading}
            className="relative p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow disabled:opacity-50"
          >
            <div className="text-4xl mb-2">📍</div>
            <h3 className="font-bold text-gray-800">Where Am I?</h3>
            <p className="text-sm text-gray-500 mt-1">Get your current location</p>
          </button>

          <button
            onClick={() => handleQuickAction('family')}
            disabled={isLoading}
            className="relative p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow disabled:opacity-50"
          >
            <div className="text-4xl mb-2">👨‍👩‍👧‍👦</div>
            <h3 className="font-bold text-gray-800">Family Photos</h3>
            <p className="text-sm text-gray-500 mt-1">See your loved ones</p>
          </button>

          <button
            onClick={() => handleQuickAction('visits')}
            disabled={isLoading}
            className="relative p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow disabled:opacity-50"
          >
            <Clock className="w-8 h-8 text-blue-600 mb-2" />
            <h3 className="font-bold text-gray-800">Who's Visiting?</h3>
            <p className="text-sm text-gray-500 mt-1">Upcoming visits</p>
          </button>

          <button
            onClick={() => handleQuickAction('calm')}
            disabled={isLoading}
            className="relative p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow disabled:opacity-50"
          >
            <Music className="w-8 h-8 text-purple-600 mb-2" />
            <h3 className="font-bold text-gray-800">Calm Mode</h3>
            <p className="text-sm text-gray-500 mt-1">Relax and unwind</p>
          </button>
        </div>

        {/* Agent Response Area */}
        <Card className="mb-8 p-6 bg-white">
          <div className="h-64 overflow-y-auto mb-4 bg-gray-50 p-4 rounded-lg border border-gray-200">
            {agentResponse && (
              <div className="space-y-4">
                <div className="bg-blue-100 p-4 rounded-lg">
                  <p className="text-blue-900">{agentResponse.response}</p>
                  {agentResponse.emotion_type && (
                    <p className="text-sm text-blue-700 mt-2">
                      <Heart className="inline w-4 h-4 mr-1" />
                      Emotion: {agentResponse.emotion_type}
                    </p>
                  )}
                </div>
              </div>
            )}
            {!agentResponse && (
              <p className="text-gray-400 italic">Your companion's responses will appear here...</p>
            )}
            <div ref={messageEndRef} />
          </div>

          {/* Input Area */}
          <div className="space-y-4">
            <Textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type your question or message here..."
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
                  e.preventDefault();
                  handleAskAgent();
                }
              }}
              className="resize-none"
            />
            
            <div className="flex gap-2">
              <Button
                onClick={() => handleAskAgent()}
                disabled={isLoading || !message.trim()}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white"
              >
                {isLoading ? (
                  <>
                    <Loader className="inline w-4 h-4 mr-2 animate-spin" />
                    Thinking...
                  </>
                ) : (
                  'Send Message'
                )}
              </Button>

              <button
                onClick={() => setIsVoiceEnabled(!isVoiceEnabled)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  isVoiceEnabled
                    ? 'bg-purple-600 text-white hover:bg-purple-700'
                    : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
                }`}
              >
                <Volume2 className="inline w-4 h-4" />
              </button>
            </div>
          </div>
        </Card>

        {/* Mood Check-in Section */}
        <Card className="p-6 bg-white">
          <h2 className="text-xl font-bold text-gray-800 mb-4">How are you feeling?</h2>
          <div className="grid grid-cols-3 gap-2">
            {['Happy', 'Calm', 'Anxious', 'Sad', 'Confused', 'Content'].map((mood) => (
              <button
                key={mood}
                onClick={() => handleMoodCheckIn(mood)}
                className="p-3 rounded-lg bg-gray-100 hover:bg-blue-200 transition-colors text-sm font-medium text-gray-700"
              >
                {mood}
              </button>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
