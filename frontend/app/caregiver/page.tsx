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
  GuardianDashboard,
  CognitiveInsight,
  CaregiverAlert,
  MemoryCard,
  EmergencyContact,
} from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogTitle } from '@/components/ui/alert-dialog';
import { Bell, Loader, TrendingUp, Brain, Users, AlertTriangle, CheckCircle, Trash2 } from 'lucide-react';

export default function CaregiverDashboard() {
  const { currentUser, selectedPatient, isLoading: userLoading } = useUser();
  const [dashboard, setDashboard] = useState<GuardianDashboard | null>(null);
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
            <h1 className="text-2xl font-bold text-gray-800 mb-4">Select a Patient</h1>
            <p className="text-gray-600">Please select a patient to view their dashboard</p>
            {/* TODO: Add patient selection UI here */}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Dashboard</h1>
          <p className="text-lg text-gray-600">Monitoring: {selectedPatient.name}</p>
        </div>

        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <Loader className="animate-spin w-8 h-8" />
          </div>
        ) : (
          <>
            {/* Alerts Section */}
            {alerts.length > 0 && (
              <Card className="mb-8 p-6 border-2 border-red-200 bg-red-50">
                <div className="flex items-center gap-3 mb-4">
                  <AlertTriangle className="w-6 h-6 text-red-600" />
                  <h2 className="text-2xl font-bold text-red-900">Active Alerts ({alerts.filter(a => !a.is_acknowledged).length})</h2>
                </div>
                <div className="space-y-3">
                  {alerts.map((alert) => (
                    <div key={alert.id} className="bg-white p-4 rounded-lg border border-red-200">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <p className="font-bold text-gray-900">{alert.alert_type.replace(/_/g, ' ').toUpperCase()}</p>
                          <p className="text-gray-700 mt-1">{alert.message}</p>
                          <p className="text-sm text-gray-500 mt-2">
                            {new Date(alert.created_at).toLocaleString()}
                          </p>
                        </div>
                        <div className="flex gap-2">
                          {!alert.is_acknowledged && (
                            <Button
                              onClick={() => handleAcknowledgeAlert(alert)}
                              size="sm"
                              className="bg-green-600 hover:bg-green-700"
                            >
                              <CheckCircle className="w-4 h-4 mr-1" />
                              Acknowledge
                            </Button>
                          )}
                          <Button
                            onClick={() => setAlertToDelete(alert)}
                            size="sm"
                            variant="outline"
                            className="text-red-600 hover:text-red-700"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                      {alert.is_acknowledged && (
                        <p className="text-sm text-green-600 mt-2">✓ Acknowledged</p>
                      )}
                    </div>
                  ))}
                </div>
              </Card>
            )}

            {/* Stats Grid */}
            <div className="grid grid-cols-3 gap-4 mb-8">
              <Card className="p-6 bg-white">
                <div className="text-4xl font-bold text-blue-600 mb-2">{dashboard?.total_interactions || 0}</div>
                <p className="text-gray-600">Total Interactions</p>
              </Card>
              <Card className="p-6 bg-white">
                <div className="text-4xl font-bold text-yellow-600 mb-2">{dashboard?.anxiety_instances || 0}</div>
                <p className="text-gray-600">Anxiety Instances</p>
              </Card>
              <Card className="p-6 bg-white">
                <div className="text-4xl font-bold text-green-600 mb-2">{dashboard?.routine_questions || 0}</div>
                <p className="text-gray-600">Routine Questions</p>
              </Card>
            </div>

            {/* Insights Section */}
            {insights.length > 0 && (
              <Card className="mb-8 p-6 bg-white">
                <div className="flex items-center gap-3 mb-4">
                  <Brain className="w-6 h-6 text-purple-600" />
                  <h2 className="text-2xl font-bold text-gray-900">Cognitive Insights</h2>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  {insights.map((insight) => (
                    <div key={insight.id} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                      <p className="font-bold text-gray-900 capitalize">
                        {insight.insight_type.replace(/_/g, ' ')}
                      </p>
                      <p className="text-3xl font-bold text-purple-600 mt-2">
                        {insight.metric_value.toFixed(2)}
                      </p>
                      <p className="text-sm text-gray-500 mt-2">{insight.metric_name}</p>
                      {insight.description && (
                        <p className="text-sm text-gray-700 mt-2">{insight.description}</p>
                      )}
                    </div>
                  ))}
                </div>
              </Card>
            )}

            {/* Family Contacts Section */}
            {familyContacts.length > 0 && (
              <Card className="mb-8 p-6 bg-white">
                <div className="flex items-center gap-3 mb-4">
                  <Users className="w-6 h-6 text-blue-600" />
                  <h2 className="text-2xl font-bold text-gray-900">Family Contacts</h2>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  {familyContacts.map((contact) => (
                    <div key={contact.id} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <p className="font-bold text-gray-900">{contact.name}</p>
                          <p className="text-sm text-gray-600">{contact.relationship}</p>
                          {contact.phone && (
                            <p className="text-sm text-gray-600 mt-1">📞 {contact.phone}</p>
                          )}
                          {contact.email && (
                            <p className="text-sm text-gray-600">📧 {contact.email}</p>
                          )}
                          {contact.is_primary && (
                            <span className="inline-block mt-2 px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded font-bold">
                              Primary Contact
                            </span>
                          )}
                        </div>
                        <Button
                          onClick={() => handleDeleteContact(contact.id)}
                          size="sm"
                          variant="outline"
                          className="text-red-600 hover:text-red-700"
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
              <Card className="p-6 bg-white">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Memory Cards</h2>
                <div className="grid grid-cols-2 gap-4">
                  {memories.map((memory) => (
                    <div key={memory.id} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                      {memory.image_url && (
                        <img
                          src={memory.image_url}
                          alt={memory.title}
                          className="w-full h-32 object-cover rounded mb-3"
                        />
                      )}
                      <p className="font-bold text-gray-900">{memory.title}</p>
                      {memory.description && (
                        <p className="text-sm text-gray-600 mt-2">{memory.description}</p>
                      )}
                      <p className="text-xs text-gray-500 mt-3">
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
          <AlertDialogContent>
            <AlertDialogTitle>Delete Alert</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to delete this alert? This action cannot be undone.
            </AlertDialogDescription>
            <div className="flex justify-end gap-3">
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogAction
                onClick={() => alertToDelete && handleDeleteAlert(alertToDelete)}
                className="bg-red-600 hover:bg-red-700"
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
