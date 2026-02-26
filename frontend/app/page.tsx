'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useUser } from '@/contexts/UserContext';
import { createUser, getUsers } from '@/lib/api';
import { User } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Loader } from 'lucide-react';

export default function Home() {
  const router = useRouter();
  const { setCurrentUser, setSelectedPatient } = useUser();
  const [step, setStep] = useState<'role-select' | 'login' | 'register'>('role-select');
  const [userType, setUserType] = useState<'patient' | 'caregiver' | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [newUserName, setNewUserName] = useState('');
  const [newUserEmail, setNewUserEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [patientsList, setPatientsList] = useState<User[]>([]);

  // Load users on mount
  useEffect(() => {
    const loadUsers = async () => {
      try {
        const data: User[] = await getUsers();
        setUsers(data);
        const patients = data.filter((u: User) => u.user_type === 'patient');
        setPatientsList(patients);
      } catch (error) {
        console.error('Error loading users:', error);
      }
    };
    loadUsers();
  }, []);

  const handleSelectRole = (role: 'patient' | 'caregiver') => {
    setUserType(role);
    setStep('login');
  };

  const handleSelectUser = (user: User) => {
    setCurrentUser(user);
    if (user.user_type === 'patient') {
      router.push('/patient');
    } else {
      router.push('/caregiver');
    }
  };

  const handleCreateUser = async () => {
    if (!newUserName.trim() || !newUserEmail.trim() || !userType) return;

    setIsLoading(true);
    try {
      const newUser = await createUser({
        name: newUserName,
        email: newUserEmail,
        user_type: userType,
      });
      setCurrentUser(newUser);
      if (userType === 'patient') {
        router.push('/patient');
      } else {
        router.push('/caregiver');
      }
    } catch (error) {
      console.error('Error creating user:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStructuredNavigation = (action: string) => {
    if (userType === 'patient') {
      if (action === 'family_photos') {
        router.push('/patient/family-photos');
      } else if (action === 'daily_schedule') {
        router.push('/patient/daily-schedule');
      }
    } else if (userType === 'caregiver') {
      if (action === 'view_alerts') {
        router.push('/caregiver/alerts');
      } else if (action === 'view_insights') {
        router.push('/caregiver/insights');
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex items-center justify-center p-4">
      <div className="w-full max-w-lg">
        {/* Step 1: Role Selection */}
        {step === 'role-select' && (
          <Card className="p-8 bg-white shadow-2xl animate-fade-in">
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-2">
                With You
              </h1>
              <p className="text-gray-600 text-base">When memory fades, presence remains</p>
              <div className="mt-3 text-sm text-gray-500 italic">
                Care companion for Alzheimer's patients and their caregivers
              </div>
            </div>

            <div className="space-y-4">
              <h2 className="text-xl font-bold text-gray-800 text-center mb-6">How would you like to continue?</h2>

              <button
                onClick={() => handleSelectRole('patient')}
                className="group w-full p-6 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl text-white font-bold hover:shadow-2xl transition-all duration-300 hover:scale-105 relative overflow-hidden"
              >
                <div className="absolute top-0 right-0 w-24 h-24 bg-white/10 rounded-full -mr-12 -mt-12 group-hover:scale-150 transition-transform duration-500" />
                <div className="relative">
                  <div className="text-5xl mb-2">🏠</div>
                  <p className="text-xl mb-1">For Me</p>
                  <p className="text-sm font-normal text-blue-100">My companion and daily helper</p>
                </div>
              </button>

              <button
                onClick={() => handleSelectRole('caregiver')}
                className="group w-full p-6 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl text-white font-bold hover:shadow-2xl transition-all duration-300 hover:scale-105 relative overflow-hidden"
              >
                <div className="absolute top-0 right-0 w-24 h-24 bg-white/10 rounded-full -mr-12 -mt-12 group-hover:scale-150 transition-transform duration-500" />
                <div className="relative">
                  <div className="text-5xl mb-2">❤️</div>
                  <p className="text-xl mb-1">For My Loved One</p>
                  <p className="text-sm font-normal text-purple-100">Support and stay connected</p>
                </div>
              </button>
            </div>
          </Card>
        )}

        {/* Step 2: Login / User Selection */}
        {step === 'login' && userType && (
          <Card className="p-8 bg-white shadow-2xl animate-scale-in">
            <button
              onClick={() => {
                setStep('role-select');
                setUserType(null);
              }}
              className="text-blue-600 hover:text-blue-700 text-sm mb-5 flex items-center gap-2 font-medium"
            >
              ← Back to role selection
            </button>

            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              {userType === 'patient' ? 'Welcome! Who are you?' : 'Who would you like to support?'}
            </h2>

            <div className="space-y-3 mb-6 max-h-[400px] overflow-y-auto">
              {userType === 'patient'
                ? users
                  .filter(u => u.user_type === 'patient')
                  .map(user => (
                    <button
                      key={user.id}
                      onClick={() => handleSelectUser(user)}
                      className="w-full p-5 border-2 border-gray-200 rounded-xl hover:border-blue-500 hover:bg-blue-50 transition-all duration-300 text-left hover:scale-105 hover:shadow-lg"
                    >
                      <p className="font-bold text-gray-800 text-base">{user.name}</p>
                      <p className="text-sm text-gray-500 mt-1">{user.email}</p>
                    </button>
                  ))
                : patientsList.map(patient => (
                  <button
                    key={patient.id}
                    onClick={() => {
                      setCurrentUser(users.find(u => u.user_type === 'caregiver') || null);
                      setSelectedPatient(patient);
                      router.push('/caregiver');
                    }}
                    className="w-full p-5 border-2 border-gray-200 rounded-xl hover:border-purple-500 hover:bg-purple-50 transition-all duration-300 text-left hover:scale-105 hover:shadow-lg"
                  >
                    <p className="font-bold text-gray-800 text-base">{patient.name}</p>
                    <p className="text-sm text-gray-500 mt-1">{patient.email}</p>
                  </button>
                ))}
            </div>

            <button
              onClick={() => setStep('register')}
              className="w-full p-4 border-2 border-dashed border-gray-300 rounded-xl text-gray-700 font-bold hover:border-gray-400 hover:bg-gray-50 transition-all duration-300"
            >
              <span className="text-xl mr-2">+</span>
              Create New Profile
            </button>
          </Card>
        )}

        {/* Step 3: Register New User */}
        {step === 'register' && userType && (
          <Card className="p-8 bg-white shadow-2xl animate-scale-in">
            <button
              onClick={() => setStep('login')}
              className="text-blue-600 hover:text-blue-700 text-sm mb-5 flex items-center gap-2 font-medium"
            >
              ← Back to user selection
            </button>

            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              Create New Profile
            </h2>

            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Full Name</label>
                <Input
                  value={newUserName}
                  onChange={(e) => setNewUserName(e.target.value)}
                  placeholder="Enter full name"
                  className="text-base py-5 border-2 focus:border-blue-400 rounded-lg"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Email Address</label>
                <Input
                  type="email"
                  value={newUserEmail}
                  onChange={(e) => setNewUserEmail(e.target.value)}
                  placeholder="Enter email address"
                  className="text-base py-5 border-2 focus:border-blue-400 rounded-lg"
                />
              </div>
            </div>

            <Button
              onClick={handleCreateUser}
              disabled={isLoading || !newUserName.trim() || !newUserEmail.trim()}
              className={`w-full py-6 text-base rounded-lg font-semibold shadow-lg transition-all duration-300 ${userType === 'patient'
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700'
                  : 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700'
                }`}
            >
              {isLoading ? (
                <>
                  <Loader className="inline w-5 h-5 mr-2 animate-spin" />
                  Creating Profile...
                </>
              ) : (
                'Create Profile'
              )}
            </Button>

            <button
              onClick={() => setStep('login')}
              className="w-full p-3 text-gray-600 text-sm hover:text-gray-700 mt-3 transition-colors"
            >
              Cancel
            </button>
          </Card>
        )}
      </div>
    </div>
  );
}
