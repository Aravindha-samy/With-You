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
import { Volume2, Loader, Clock, Users, Heart, Music, MessageSquare, Grid3x3 } from 'lucide-react';
import { AgentResponseCard } from '@/components/patient-interface/AgentResponses';

type OperatingMode = 'structured' | 'freespeech';

export default function PatientDashboard() {
  const { currentUser, isLoading: userLoading } = useUser();
  const [mode, setMode] = useState<OperatingMode>('structured');
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 p-4 md:p-6">
      <div className="max-w-6xl mx-auto">
        {/* Modern Header with Glass Effect */}
        <div className="text-center mb-6 pt-4 animate-fade-in">
          <div className="inline-block glass rounded-xl px-6 py-4 mb-3 shadow-lg">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-2">
              Welcome Back, {currentUser.name}
            </h1>
            <p className="text-base text-gray-600 font-medium">With You – When memory fades, presence remains</p>
          </div>

          {/* Modern Mode Switcher */}
          <div className="flex justify-center gap-2 mt-6">
            <button
              onClick={() => setMode('structured')}
              className={`group relative flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all duration-300 ${mode === 'structured'
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-xl scale-105'
                  : 'bg-white text-gray-700 hover:bg-gray-50 shadow-md hover:shadow-lg'
                }`}
            >
              <Grid3x3 className="w-5 h-5" />
              <span>Quick Actions</span>
              {mode === 'structured' && (
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-pulse-soft" />
              )}
            </button>
            <button
              onClick={() => setMode('freespeech')}
              className={`group relative flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all duration-300 ${mode === 'freespeech'
                  ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-xl scale-105'
                  : 'bg-white text-gray-700 hover:bg-gray-50 shadow-md hover:shadow-lg'
                }`}
            >
              <MessageSquare className="w-5 h-5" />
              <span>Chat with Me</span>
              {mode === 'freespeech' && (
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-pulse-soft" />
              )}
            </button>
          </div>
        </div>

        {/* Structured Navigation Mode (Button Mode) */}
        {mode === 'structured' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6 animate-scale-in">
            <button
              onClick={() => handleQuickAction('location')}
              disabled={isLoading}
              className="group relative overflow-hidden p-6 bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 disabled:opacity-50 hover:scale-105"
            >
              <div className="absolute top-0 right-0 w-24 h-24 bg-blue-100 rounded-full -mr-12 -mt-12 opacity-50 group-hover:scale-150 transition-transform duration-500" />
              <div className="relative">
                <div className="text-4xl mb-3">📍</div>
                <h3 className="text-xl font-bold text-gray-800 mb-1">Where & When</h3>
                <p className="text-sm text-gray-600">Current location and time</p>
              </div>
            </button>

            <button
              onClick={() => handleQuickAction('family')}
              disabled={isLoading}
              className="group relative overflow-hidden p-6 bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 disabled:opacity-50 hover:scale-105"
            >
              <div className="absolute top-0 right-0 w-24 h-24 bg-green-100 rounded-full -mr-12 -mt-12 opacity-50 group-hover:scale-150 transition-transform duration-500" />
              <div className="relative">
                <div className="text-4xl mb-3">👨‍👩‍👧‍👦</div>
                <h3 className="text-xl font-bold text-gray-800 mb-1">My Family</h3>
                <p className="text-sm text-gray-600">Photos and updates from loved ones</p>
              </div>
            </button>

            <button
              onClick={() => handleQuickAction('visits')}
              disabled={isLoading}
              className="group relative overflow-hidden p-6 bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 disabled:opacity-50 hover:scale-105"
            >
              <div className="absolute top-0 right-0 w-24 h-24 bg-amber-100 rounded-full -mr-12 -mt-12 opacity-50 group-hover:scale-150 transition-transform duration-500" />
              <div className="relative">
                <Clock className="w-12 h-12 text-amber-600 mb-3" />
                <h3 className="text-xl font-bold text-gray-800 mb-1">Today's Plan</h3>
                <p className="text-sm text-gray-600">What's happening today</p>
              </div>
            </button>

            <button
              onClick={() => handleQuickAction('calm')}
              disabled={isLoading}
              className="group relative overflow-hidden p-6 bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 disabled:opacity-50 hover:scale-105"
            >
              <div className="absolute top-0 right-0 w-24 h-24 bg-purple-100 rounded-full -mr-12 -mt-12 opacity-50 group-hover:scale-150 transition-transform duration-500" />
              <div className="relative">
                <Music className="w-12 h-12 text-purple-600 mb-3" />
                <h3 className="text-xl font-bold text-gray-800 mb-1">Relax</h3>
                <p className="text-sm text-gray-600">Take a peaceful moment</p>
              </div>
            </button>
          </div>
        )}

        {/* Agent Response Area */}
        <div className="mb-8">
          {agentResponse ? (
            <div className="animate-fade-in">
              <AgentResponseCard response={agentResponse} />
            </div>
          ) : (
            <Card className="p-8 bg-white/80 backdrop-blur-sm text-center border-2 border-dashed border-gray-200">
              <div className="max-w-md mx-auto">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Heart className="w-8 h-8 text-blue-600" />
                </div>
                <p className="text-gray-500 text-base italic">
                  {mode === 'structured'
                    ? 'Choose any option above, or switch to Free Speech mode to chat...'
                    : 'What\'s on your mind? I\'m here to chat with you...'}
                </p>
              </div>
            </Card>
          )}
        </div>

        {/* Free Speech Mode Input */}
        {mode === 'freespeech' && (
          <Card className="mb-6 p-5 bg-white shadow-xl animate-scale-in">
            <div className="space-y-3">
              <Textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="What would you like to talk about?"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
                    e.preventDefault();
                    handleAskAgent();
                  }
                }}
                className="resize-none text-base border-2 focus:border-purple-400 rounded-lg min-h-[100px]"
              />

              <div className="flex gap-2">
                <Button
                  onClick={() => handleAskAgent()}
                  disabled={isLoading || !message.trim()}
                  className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white text-base py-6 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300"
                >
                  {isLoading ? (
                    <>
                      <Loader className="inline w-5 h-5 mr-2 animate-spin" />
                      Thinking...
                    </>
                  ) : (
                    <>
                      <MessageSquare className="inline w-5 h-5 mr-2" />
                      Send Message
                    </>
                  )}
                </Button>

                <button
                  onClick={() => setIsVoiceEnabled(!isVoiceEnabled)}
                  className={`px-6 py-3 rounded-lg font-semibold transition-all duration-300 ${isVoiceEnabled
                      ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200 shadow-md'
                    }`}
                >
                  <Volume2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          </Card>
        )}

        {/* Mood Check-in Section */}
        <Card className="p-6 bg-white shadow-xl animate-fade-in">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Heart className="w-6 h-6 text-red-500" />
            How are you feeling right now?
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {[
              { mood: 'Happy', emoji: '😊', color: 'from-yellow-400 to-orange-400' },
              { mood: 'Calm', emoji: '😌', color: 'from-blue-400 to-cyan-400' },
              { mood: 'Anxious', emoji: '😰', color: 'from-orange-400 to-red-400' },
              { mood: 'Sad', emoji: '😢', color: 'from-blue-500 to-purple-500' },
              { mood: 'Confused', emoji: '😕', color: 'from-gray-400 to-gray-500' },
              { mood: 'Content', emoji: '😊', color: 'from-green-400 to-teal-400' },
            ].map(({ mood, emoji, color }) => (
              <button
                key={mood}
                onClick={() => handleMoodCheckIn(mood)}
                className={`group p-4 rounded-lg bg-gradient-to-br ${color} text-white hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl`}
              >
                <div className="text-3xl mb-1">{emoji}</div>
                <div className="text-base font-semibold">{mood}</div>
              </button>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
