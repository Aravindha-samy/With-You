'use client';

import React, { useState, useEffect } from 'react';
import { useUser } from '@/contexts/UserContext';
import {
  getCaregiverDashboard,
  getCognitiveInsights,
  getCaregiverAlerts,
  acknowledgeAlert,
  deleteAlert,
  getMemoryCards,
  getFamilyContacts,
  deleteFamilyContact,
} from '@/lib/api';
import {
  GuardianDashboard as GuardianDashType,
  CognitiveInsight,
  CaregiverAlert,
  MemoryCard,
  EmergencyContact,
} from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogTitle } from '@/components/ui/alert-dialog';
import { Bell, Loader, TrendingUp, Brain, Users, AlertTriangle, CheckCircle, Trash2, MessageSquare } from 'lucide-react';
import { GuardianDashboard } from '@/components/caregiver-setup/GuardianDashboard';

export default function CaregiverDashboard() {
  const { currentUser, selectedPatient, isLoading: userLoading } = useUser();
  const [dashboard, setDashboard] = useState<GuardianDashType | null>(null);
  const [insights, setInsights] = useState<CognitiveInsight[]>([]);
  const [alerts, setAlerts] = useState<CaregiverAlert[]>([]);
  const [memories, setMemories] = useState<MemoryCard[]>([]);
  const [familyContacts, setFamilyContacts] = useState<EmergencyContact[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedAlert, setSelectedAlert] = useState<CaregiverAlert | null>(null);
  const [alertToDelete, setAlertToDelete] = useState<CaregiverAlert | null>(null);

  // Redirect if not authenticated as caregiver
  useEffect(() => {
    if (!userLoading && (!currentUser || currentUser.user_type !== 'caregiver')) {
      window.location.href = '/';
    }
  }, [currentUser, userLoading]);

  // Load dashboard data
  useEffect(() => {
    if (!selectedPatient || !currentUser) return;

    const loadDashboardData = async () => {
      setIsLoading(true);
      const patientId = selectedPatient.id;
      const caregiverId = currentUser.id;
      try {
        const [dashboardData, insightsData, alertsData, memoriesData, contactsData] = await Promise.all([
          getCaregiverDashboard(patientId),
          getCognitiveInsights(patientId, 'weekly'),
          getCaregiverAlerts(caregiverId),
          getMemoryCards(patientId),
          getFamilyContacts(patientId),
        ]);

        setDashboard(dashboardData);
        setInsights(insightsData);
        setAlerts(alertsData);
        setMemories(memoriesData);
        setFamilyContacts(contactsData);
      } catch (error) {
        console.error('Error loading dashboard:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboardData();
  }, [selectedPatient]);

  const handleAcknowledgeAlert = async (alert: CaregiverAlert) => {
    try {
      await acknowledgeAlert(alert.id);
      setAlerts(alerts.map(a =>
        a.id === alert.id ? { ...a, is_acknowledged: true } : a
      ));
    } catch (error) {
      console.error('Error acknowledging alert:', error);
    }
  };

  const handleDeleteAlert = async (alert: CaregiverAlert) => {
    try {
      await deleteAlert(alert.id);
      setAlerts(alerts.filter(a => a.id !== alert.id));
      setAlertToDelete(null);
    } catch (error) {
      console.error('Error deleting alert:', error);
    }
  };

  const handleDeleteContact = async (contactId: number) => {
    if (!selectedPatient) return;
    try {
      await deleteFamilyContact(contactId);
      setFamilyContacts(familyContacts.filter(c => c.id !== contactId));
    } catch (error) {
      console.error('Error deleting contact:', error);
    }
  };

  if (userLoading || !currentUser || currentUser.user_type !== 'caregiver') {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader className="animate-spin w-8 h-8" />
      </div>
    );
  }

  if (!selectedPatient) {
    return (
      <div className="min-h-screen bg-gray-50 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center py-12">
            <h1 className="text-2xl font-bold text-gray-800 mb-4">Choose Who to Support</h1>
            <p className="text-gray-600">Please select someone to view their companion dashboard</p>
            {/* TODO: Add patient selection UI here */}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-indigo-50 p-4 md:p-6">
      <div className="max-w-6xl mx-auto">
        {/* Modern Header */}
        <div className="mb-6 animate-fade-in">
          <div className="flex items-center justify-between glass rounded-xl p-5 shadow-lg">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent mb-1">
                Guardian Dashboard
              </h1>
              <p className="text-base text-gray-600">
                Supporting: <span className="font-semibold text-gray-800">{selectedPatient.name}</span>
              </p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">Last updated</div>
              <div className="text-lg font-semibold text-gray-700">{new Date().toLocaleTimeString()}</div>
            </div>
          </div>
        </div>

        {isLoading ? (
          <div className="flex items-center justify-center py-16">
            <div className="text-center">
              <Loader className="animate-spin w-10 h-10 text-purple-600 mx-auto mb-3" />
              <p className="text-gray-600">Loading dashboard data...</p>
            </div>
          </div>
        ) : (
          <>
            {/* Guardian Dashboard - Main Feature */}
            {dashboard && dashboard.daily_summary && (
              <div className="mb-6 animate-fade-in">
                <GuardianDashboard
                  dailySummary={dashboard.daily_summary}
                  weeklyReport={dashboard.weekly_report}
                  interventionNeeded={dashboard.intervention_needed}
                />
              </div>
            )}

            {/* Alerts Section */}
            {alerts.length > 0 && (
              <Card className="mb-6 p-5 border-2 border-red-200 bg-gradient-to-br from-red-50 to-orange-50 shadow-xl animate-scale-in">
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-10 h-10 bg-red-500 rounded-full flex items-center justify-center animate-pulse-soft">
                    <AlertTriangle className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-red-900">Active Alerts</h2>
                    <p className="text-sm text-red-700">{alerts.filter(a => !a.is_acknowledged).length} requiring attention</p>
                  </div>
                </div>
                <div className="space-y-3">
                  {alerts.map((alert) => (
                    <div key={alert.id} className="bg-white p-5 rounded-lg border-2 border-red-100 shadow-lg hover:shadow-xl transition-all duration-300">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="px-3 py-1 bg-red-100 text-red-700 text-xs font-bold rounded-full uppercase">
                              {alert.alert_type.replace(/_/g, ' ')}
                            </span>
                            {alert.severity && (
                              <span className={`px-3 py-1 text-xs font-bold rounded-full ${alert.severity === 'high' ? 'bg-red-200 text-red-800' :
                                  alert.severity === 'medium' ? 'bg-yellow-200 text-yellow-800' :
                                    'bg-blue-200 text-blue-800'
                                }`}>
                                {alert.severity} priority
                              </span>
                            )}
                          </div>
                          <p className="text-gray-800 text-base font-medium mt-2">{alert.message}</p>
                          <p className="text-sm text-gray-500 mt-2 flex items-center gap-2">
                            <span className="inline-block w-2 h-2 bg-gray-400 rounded-full" />
                            {new Date(alert.created_at).toLocaleString()}
                          </p>
                        </div>
                        <div className="flex gap-2 ml-4">
                          {!alert.is_acknowledged && (
                            <Button
                              onClick={() => handleAcknowledgeAlert(alert)}
                              size="sm"
                              className="bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white shadow-md"
                            >
                              <CheckCircle className="w-4 h-4 mr-1" />
                              Acknowledge
                            </Button>
                          )}
                          <Button
                            onClick={() => setAlertToDelete(alert)}
                            size="sm"
                            variant="outline"
                            className="text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                      {alert.is_acknowledged && (
                        <div className="mt-4 pt-4 border-t border-green-100">
                          <p className="text-sm text-green-600 font-medium flex items-center gap-2">
                            <CheckCircle className="w-4 h-4" />
                            Acknowledged
                          </p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </Card>
            )}

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 animate-slide-in-right">
              <Card className="p-6 bg-white shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-blue-600 rounded-xl flex items-center justify-center">
                    <MessageSquare className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <div className="text-3xl font-bold text-blue-600 mb-1">{dashboard?.total_interactions || 0}</div>
                    <p className="text-sm text-gray-600 font-medium">Total Interactions</p>
                  </div>
                </div>
              </Card>
              <Card className="p-6 bg-white shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-yellow-400 to-orange-600 rounded-xl flex items-center justify-center">
                    <AlertTriangle className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <div className="text-3xl font-bold text-yellow-600 mb-1">{dashboard?.anxiety_instances || 0}</div>
                    <p className="text-sm text-gray-600 font-medium">Anxiety Instances</p>
                  </div>
                </div>
              </Card>
              <Card className="p-6 bg-white shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-green-600 rounded-xl flex items-center justify-center">
                    <TrendingUp className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <div className="text-3xl font-bold text-green-600 mb-1">{dashboard?.routine_questions || 0}</div>
                    <p className="text-sm text-gray-600 font-medium">Routine Questions</p>
                  </div>
                </div>
              </Card>
            </div>

            {/* Insights Section */}
            {insights.length > 0 && (
              <Card className="mb-6 p-6 bg-white shadow-xl animate-fade-in">
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-10 h-10 bg-gradient-to-br from-purple-400 to-purple-600 rounded-lg flex items-center justify-center">
                    <Brain className="w-5 h-5 text-white" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900">Cognitive Insights</h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {insights.map((insight) => (
                    <div key={insight.id} className="p-5 bg-gradient-to-br from-purple-50 to-indigo-50 rounded-lg border-2 border-purple-100 hover:border-purple-300 transition-all duration-300">
                      <p className="font-bold text-gray-900 capitalize text-base mb-2">
                        {insight.insight_type.replace(/_/g, ' ')}
                      </p>
                      <p className="text-4xl font-bold text-purple-600 mb-2">
                        {insight.metric_value.toFixed(2)}
                      </p>
                      <p className="text-sm text-gray-600 font-medium mb-2">{insight.metric_name}</p>
                      {insight.description && (
                        <p className="text-sm text-gray-700 mt-3 p-3 bg-white/70 rounded-lg">{insight.description}</p>
                      )}
                    </div>
                  ))}
                </div>
              </Card>
            )}

            {/* Family Contacts Section */}
            {familyContacts.length > 0 && (
              <Card className="mb-6 p-6 bg-white shadow-xl animate-fade-in">
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg flex items-center justify-center">
                    <Users className="w-5 h-5 text-white" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900">Family Contacts</h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {familyContacts.map((contact) => (
                    <div key={contact.id} className="p-5 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-lg border-2 border-blue-100 hover:border-blue-300 transition-all duration-300">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <p className="font-bold text-gray-900 text-base mb-1">{contact.name}</p>
                          <p className="text-sm text-blue-600 font-medium mb-3">{contact.relationship}</p>
                          {contact.phone && (
                            <p className="text-sm text-gray-700 flex items-center gap-2 mb-1">
                              <span className="text-lg">📞</span>
                              {contact.phone}
                            </p>
                          )}
                          {contact.email && (
                            <p className="text-sm text-gray-700 flex items-center gap-2">
                              <span className="text-lg">📧</span>
                              {contact.email}
                            </p>
                          )}
                          {contact.is_primary && (
                            <span className="inline-block mt-3 px-3 py-1 bg-blue-500 text-white text-xs rounded-full font-bold">
                              Primary Contact
                            </span>
                          )}
                        </div>
                        <Button
                          onClick={() => handleDeleteContact(contact.id)}
                          size="sm"
                          variant="outline"
                          className="text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            )}

            {/* Memories Section */}
            {memories.length > 0 && (
              <Card className="p-6 bg-white shadow-xl animate-fade-in">
                <h2 className="text-2xl font-bold text-gray-900 mb-5">Memory Cards</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {memories.map((memory) => (
                    <div key={memory.id} className="p-5 bg-gradient-to-br from-amber-50 to-yellow-50 rounded-lg border-2 border-amber-100 hover:border-amber-300 transition-all duration-300 hover:scale-105">
                      {memory.image_url && (
                        <img
                          src={memory.image_url}
                          alt={memory.title}
                          className="w-full h-40 object-cover rounded-lg mb-3 shadow-md"
                        />
                      )}
                      <p className="font-bold text-gray-900 text-base mb-2">{memory.title}</p>
                      {memory.description && (
                        <p className="text-sm text-gray-700 mt-3 leading-relaxed">{memory.description}</p>
                      )}
                      <p className="text-xs text-gray-500 mt-4 flex items-center gap-2">
                        <span className="inline-block w-2 h-2 bg-amber-400 rounded-full" />
                        {new Date(memory.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  ))}
                </div>
              </Card>
            )}
          </>
        )}

        {/* Alert Delete Confirmation Dialog */}
        <AlertDialog open={!!alertToDelete} onOpenChange={() => setAlertToDelete(null)}>
          <AlertDialogContent className="rounded-2xl">
            <AlertDialogTitle className="text-2xl font-bold text-gray-900">Delete Alert</AlertDialogTitle>
            <AlertDialogDescription className="text-gray-600">
              Are you sure you want to delete this alert? This action cannot be undone.
            </AlertDialogDescription>
            <div className="flex justify-end gap-3 mt-6">
              <AlertDialogCancel className="rounded-xl">Cancel</AlertDialogCancel>
              <AlertDialogAction
                onClick={() => alertToDelete && handleDeleteAlert(alertToDelete)}
                className="bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 rounded-xl"
              >
                Delete
              </AlertDialogAction>
            </div>
          </AlertDialogContent>
        </AlertDialog>
      </div>
    </div>
  );
}
