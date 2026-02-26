/**
 * Guardian Dashboard Component
 * Caregiver co-pilot interface for monitoring patient insights
 */

import React from 'react';
import { Card } from '@/components/ui/card';
import { AlertTriangle, TrendingUp, TrendingDown, Minus, Brain, Heart, Clock, Shield } from 'lucide-react';

interface GuardianSummary {
    summary: string;
    emotional_trend: 'stable' | 'declining' | 'improving';
    orientation_trend: 'stable' | 'declining' | 'improving';
    alert_level: 'none' | 'monitor' | 'intervene';
}

interface GuardianDashboardProps {
    dailySummary: GuardianSummary;
    weeklyReport: GuardianSummary;
    interventionNeeded: boolean;
}

export const GuardianDashboard = ({
    dailySummary,
    weeklyReport,
    interventionNeeded
}: GuardianDashboardProps) => {

    const getTrendIcon = (trend: string) => {
        switch (trend) {
            case 'improving':
                return <TrendingUp className="w-5 h-5 text-green-600" />;
            case 'declining':
                return <TrendingDown className="w-5 h-5 text-red-600" />;
            default:
                return <Minus className="w-5 h-5 text-gray-600" />;
        }
    };

    const getTrendColor = (trend: string) => {
        switch (trend) {
            case 'improving':
                return 'text-green-700 bg-green-50';
            case 'declining':
                return 'text-red-700 bg-red-50';
            default:
                return 'text-gray-700 bg-gray-50';
        }
    };

    const getAlertLevelColor = (level: string) => {
        switch (level) {
            case 'intervene':
                return 'bg-red-100 border-red-300 text-red-900';
            case 'monitor':
                return 'bg-yellow-100 border-yellow-300 text-yellow-900';
            default:
                return 'bg-green-100 border-green-300 text-green-900';
        }
    };

    const getAlertLevelText = (level: string) => {
        switch (level) {
            case 'intervene':
                return 'Intervention Recommended';
            case 'monitor':
                return 'Continue Monitoring';
            default:
                return 'All Clear';
        }
    };

    return (
        <div className="space-y-6">
            {/* Intervention Alert */}
            {interventionNeeded && (
                <Card className="p-6 bg-red-50 border-red-300">
                    <div className="flex items-center gap-4">
                        <AlertTriangle className="w-8 h-8 text-red-600" />
                        <div>
                            <h3 className="font-bold text-red-900 text-lg">Immediate Intervention Recommended</h3>
                            <p className="text-red-700 mt-1">
                                The patient has shown signs of significant distress. Please check in as soon as possible.
                            </p>
                        </div>
                    </div>
                </Card>
            )}

            {/* Daily Summary Card */}
            <Card className="p-6 bg-white">
                <div className="flex items-center gap-3 mb-4">
                    <div className="bg-blue-500 p-3 rounded-full">
                        <Clock className="w-6 h-6 text-white" />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900">Today's Summary</h2>
                </div>

                <p className="text-gray-700 mb-6 leading-relaxed">{dailySummary.summary}</p>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Emotional Trend */}
                    <div className={`p-4 rounded-lg ${getTrendColor(dailySummary.emotional_trend)}`}>
                        <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-2">
                                <Heart className="w-5 h-5" />
                                <span className="font-semibold">Emotional</span>
                            </div>
                            {getTrendIcon(dailySummary.emotional_trend)}
                        </div>
                        <p className="text-sm capitalize">{dailySummary.emotional_trend}</p>
                    </div>

                    {/* Orientation Trend */}
                    <div className={`p-4 rounded-lg ${getTrendColor(dailySummary.orientation_trend)}`}>
                        <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-2">
                                <Brain className="w-5 h-5" />
                                <span className="font-semibold">Orientation</span>
                            </div>
                            {getTrendIcon(dailySummary.orientation_trend)}
                        </div>
                        <p className="text-sm capitalize">{dailySummary.orientation_trend}</p>
                    </div>

                    {/* Alert Level */}
                    <div className={`p-4 rounded-lg border-2 ${getAlertLevelColor(dailySummary.alert_level)}`}>
                        <div className="flex items-center gap-2 mb-2">
                            <Shield className="w-5 h-5" />
                            <span className="font-semibold">Status</span>
                        </div>
                        <p className="text-sm font-medium">{getAlertLevelText(dailySummary.alert_level)}</p>
                    </div>
                </div>
            </Card>

            {/* Weekly Report Card */}
            <Card className="p-6 bg-white">
                <div className="flex items-center gap-3 mb-4">
                    <div className="bg-purple-500 p-3 rounded-full">
                        <TrendingUp className="w-6 h-6 text-white" />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900">Weekly Report</h2>
                </div>

                <p className="text-gray-700 mb-6 leading-relaxed">{weeklyReport.summary}</p>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Emotional Trend */}
                    <div className={`p-4 rounded-lg ${getTrendColor(weeklyReport.emotional_trend)}`}>
                        <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-2">
                                <Heart className="w-5 h-5" />
                                <span className="font-semibold">Emotional</span>
                            </div>
                            {getTrendIcon(weeklyReport.emotional_trend)}
                        </div>
                        <p className="text-sm capitalize">{weeklyReport.emotional_trend}</p>
                    </div>

                    {/* Cognitive Trend */}
                    <div className={`p-4 rounded-lg ${getTrendColor(weeklyReport.orientation_trend)}`}>
                        <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-2">
                                <Brain className="w-5 h-5" />
                                <span className="font-semibold">Cognitive</span>
                            </div>
                            {getTrendIcon(weeklyReport.orientation_trend)}
                        </div>
                        <p className="text-sm capitalize">{weeklyReport.orientation_trend}</p>
                    </div>

                    {/* Alert Level */}
                    <div className={`p-4 rounded-lg border-2 ${getAlertLevelColor(weeklyReport.alert_level)}`}>
                        <div className="flex items-center gap-2 mb-2">
                            <Shield className="w-5 h-5" />
                            <span className="font-semibold">Overall Status</span>
                        </div>
                        <p className="text-sm font-medium">{getAlertLevelText(weeklyReport.alert_level)}</p>
                    </div>
                </div>
            </Card>

            {/* Recommendations */}
            <Card className="p-6 bg-gradient-to-r from-indigo-50 to-purple-50">
                <h3 className="font-bold text-indigo-900 text-lg mb-3">Guardian Recommendations</h3>
                <ul className="space-y-2 text-indigo-800">
                    {dailySummary.alert_level === 'intervene' && (
                        <li className="flex items-start gap-2">
                            <span className="text-red-600">•</span>
                            <span>Consider scheduling a check-in call or visit today</span>
                        </li>
                    )}
                    {dailySummary.alert_level === 'monitor' && (
                        <li className="flex items-start gap-2">
                            <span className="text-yellow-600">•</span>
                            <span>Continue monitoring interactions for the next 24 hours</span>
                        </li>
                    )}
                    {dailySummary.emotional_trend === 'declining' && (
                        <li className="flex items-start gap-2">
                            <span className="text-orange-600">•</span>
                            <span>Emotional support may be beneficial - consider familiar activities or family calls</span>
                        </li>
                    )}
                    {dailySummary.orientation_trend === 'declining' && (
                        <li className="flex items-start gap-2">
                            <span className="text-blue-600">•</span>
                            <span>Increased orientation reminders may help - check calendar and location settings</span>
                        </li>
                    )}
                    {dailySummary.alert_level === 'none' && dailySummary.emotional_trend === 'stable' && (
                        <li className="flex items-start gap-2">
                            <span className="text-green-600">•</span>
                            <span>Patient is doing well - maintain current support routines</span>
                        </li>
                    )}
                </ul>
            </Card>
        </div>
    );
};
