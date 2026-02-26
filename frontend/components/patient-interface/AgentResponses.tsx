/**
 * Agent Response Components
 * Specialized UI components for each agent type
 */

import React from 'react';
import { Card } from '@/components/ui/card';
import { Home, Users, Heart, BookOpen, MapPin, Clock } from 'lucide-react';

// Harbor (Orientation) Response Component
export const HarborResponse = ({ message, reassuranceLevel }: { message: string; reassuranceLevel: string }) => {
    return (
        <Card className="p-6 bg-gradient-to-br from-blue-50 to-cyan-50 border-2 border-blue-200 shadow-xl hover:shadow-2xl transition-all duration-300 animate-fade-in">
            <div className="flex items-start gap-3">
                <div className="bg-gradient-to-br from-blue-500 to-blue-600 p-3 rounded-xl shadow-lg">
                    <MapPin className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                    <h3 className="font-bold text-blue-900 mb-2 text-xl">Location & Time</h3>
                    <p className="text-blue-800 text-base leading-relaxed">{message}</p>
                    {reassuranceLevel === 'high' && (
                        <div className="mt-3 p-3 bg-white/70 backdrop-blur-sm rounded-lg border border-blue-200">
                            <p className="text-blue-900 font-semibold text-base">🌿 Everything is just fine.</p>
                        </div>
                    )}
                </div>
            </div>
        </Card>
    );
};

// Roots (Identity & Relationship) Response Component
export const RootsResponse = ({
    message,
    identityReinforcement,
    suggestCall
}: {
    message: string;
    identityReinforcement: boolean;
    suggestCall: boolean;
}) => {
    return (
        <Card className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 shadow-xl hover:shadow-2xl transition-all duration-300 animate-fade-in">
            <div className="flex items-start gap-3">
                <div className="bg-gradient-to-br from-green-500 to-green-600 p-3 rounded-xl shadow-lg">
                    <Users className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                    <h3 className="font-bold text-green-900 mb-2 text-xl">Family</h3>
                    <p className="text-green-800 text-base leading-relaxed">{message}</p>
                    {suggestCall && (
                        <button className="mt-3 px-5 py-2 bg-gradient-to-r from-green-600 to-green-700 text-white text-base font-semibold rounded-lg hover:from-green-700 hover:to-green-800 transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105">
                            📞 Would you like to call?
                        </button>
                    )}
                </div>
            </div>
        </Card>
    );
};

// Solace (Emotional Support) Response Component
export const SolaceResponse = ({
    message,
    calmProtocol,
    caregiverAlert
}: {
    message: string;
    calmProtocol: string;
    caregiverAlert: boolean;
}) => {
    return (
        <Card className="p-6 bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200 shadow-xl hover:shadow-2xl transition-all duration-300 animate-fade-in">
            <div className="flex items-start gap-3">
                <div className="bg-gradient-to-br from-purple-500 to-purple-600 p-3 rounded-xl shadow-lg">
                    <Heart className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                    <h3 className="font-bold text-purple-900 mb-2 text-xl">Let's Relax</h3>
                    <p className="text-purple-800 text-base leading-relaxed">{message}</p>
                    {calmProtocol === 'breathing' && (
                        <div className="mt-3 p-4 bg-white/70 backdrop-blur-sm rounded-lg border border-purple-200">
                            <p className="text-purple-900 text-center font-semibold mb-3 text-base">Let's breathe together</p>
                            <div className="flex items-center justify-center gap-3">
                                <div className="w-16 h-16 bg-gradient-to-br from-purple-300 to-purple-400 rounded-full animate-pulse-soft shadow-lg" />
                                <p className="text-purple-800 text-base font-medium">Breathe in... and out...</p>
                            </div>
                        </div>
                    )}
                    {caregiverAlert && (
                        <p className="mt-4 text-sm text-purple-600 font-medium">✓ Your family has been notified</p>
                    )}
                </div>
            </div>
        </Card>
    );
};

// Legacy (Story & Memory) Response Component
export const LegacyResponse = ({
    message,
    storyAnchorUsed
}: {
    message: string;
    storyAnchorUsed: boolean;
}) => {
    return (
        <Card className="p-6 bg-gradient-to-br from-amber-50 to-orange-50 border-2 border-amber-200 shadow-xl hover:shadow-2xl transition-all duration-300 animate-fade-in">
            <div className="flex items-start gap-3">
                <div className="bg-gradient-to-br from-amber-500 to-amber-600 p-3 rounded-xl shadow-lg">
                    <BookOpen className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                    <h3 className="font-bold text-amber-900 mb-2 text-xl">Memory Lane</h3>
                    <p className="text-amber-800 text-base leading-relaxed italic">{message}</p>
                    {storyAnchorUsed && (
                        <p className="mt-4 text-sm text-amber-600 font-medium">📖 A cherished memory</p>
                    )}
                </div>
            </div>
        </Card>
    );
};

// Generic Agent Response (Fallback)
export const GenericAgentResponse = ({ message, agentType }: { message: string; agentType: string }) => {
    return (
        <Card className="p-6 bg-gradient-to-br from-gray-50 to-slate-50 border-2 border-gray-200 shadow-xl hover:shadow-2xl transition-all duration-300 animate-fade-in">
            <div className="flex items-start gap-3">
                <div className="bg-gradient-to-br from-gray-500 to-gray-600 p-3 rounded-xl shadow-lg">
                    <Home className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                    <h3 className="font-bold text-gray-900 mb-2 text-xl capitalize">{agentType}</h3>
                    <p className="text-gray-800 text-base leading-relaxed">{message}</p>
                </div>
            </div>
        </Card>
    );
};

// Agent Response Router Component
export const AgentResponseCard = ({ response }: { response: any }) => {
    if (!response) return null;

    switch (response.agent_type) {
        case 'harbor':
            return (
                <HarborResponse
                    message={response.response}
                    reassuranceLevel={response.reassurance_level || 'low'}
                />
            );
        case 'roots':
            return (
                <RootsResponse
                    message={response.response}
                    identityReinforcement={response.identity_reinforcement || false}
                    suggestCall={response.suggest_call || false}
                />
            );
        case 'solace':
            return (
                <SolaceResponse
                    message={response.response}
                    calmProtocol={response.calm_protocol || 'none'}
                    caregiverAlert={response.caregiver_alert || false}
                />
            );
        case 'legacy':
            return (
                <LegacyResponse
                    message={response.response}
                    storyAnchorUsed={response.story_anchor_used || false}
                />
            );
        default:
            return (
                <GenericAgentResponse
                    message={response.response}
                    agentType={response.agent_type}
                />
            );
    }
};
