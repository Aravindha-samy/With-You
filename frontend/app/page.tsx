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

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-indigo-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Step 1: Role Selection */}
        {step === 'role-select' && (
          <Card className="p-8 bg-white">
            <h1 className="text-4xl font-bold text-center text-blue-900 mb-2">WithYou</h1>
            <p className="text-center text-gray-600 mb-8">Care companion for Alzheimer's patients and their caregivers</p>

            <div className="space-y-4">
              <h2 className="text-xl font-bold text-gray-800 text-center mb-6">How would you like to continue?</h2>

              <button
                onClick={() => handleSelectRole('patient')}
                className="w-full p-6 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl text-white font-bold hover:shadow-lg transition-shadow"
              >
                <div className="text-4xl mb-2">🧠</div>
                <p>I'm a Patient</p>
                <p className="text-sm font-normal text-blue-100 mt-1">Get daily orientation and emotional support</p>
              </button>

              <button
                onClick={() => handleSelectRole('caregiver')}
                className="w-full p-6 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl text-white font-bold hover:shadow-lg transition-shadow"
              >
                <div className="text-4xl mb-2">👨‍⚕️</div>
                <p>I'm a Caregiver</p>
                <p className="text-sm font-normal text-purple-100 mt-1">Monitor insights and manage care</p>
              </button>
            </div>
          </Card>
        )}

        {/* Step 2: Login / User Selection */}
        {step === 'login' && userType && (
          <Card className="p-8 bg-white">
            <button
              onClick={() => {
                setStep('role-select');
                setUserType(null);
              }}
              className="text-blue-600 hover:text-blue-700 text-sm mb-4"
            >
              ← Back to role selection
            </button>

            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              {userType === 'patient' ? 'Select Your Profile' : 'Select a Patient'}
            </h2>

            <div className="space-y-3 mb-6">
              {userType === 'patient'
                ? users
                    .filter(u => u.user_type === 'patient')
                    .map(user => (
                      <button
                        key={user.id}
                        onClick={() => handleSelectUser(user)}
                        className="w-full p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors text-left"
                      >
                        <p className="font-bold text-gray-800">{user.name}</p>
                        <p className="text-sm text-gray-500">{user.email}</p>
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
                      className="w-full p-4 border-2 border-gray-200 rounded-lg hover:border-purple-500 hover:bg-purple-50 transition-colors text-left"
                    >
                      <p className="font-bold text-gray-800">{patient.name}</p>
                      <p className="text-sm text-gray-500">{patient.email}</p>
                    </button>
                  ))}
            </div>

            <button
              onClick={() => setStep('register')}
              className="w-full p-3 border-2 border-gray-300 rounded-lg text-gray-700 font-bold hover:border-gray-400 transition-colors"
            >
              + Create New {userType === 'patient' ? 'Patient' : 'Caregiver'} Profile
            </button>
          </Card>
        )}

        {/* Step 3: Register New User */}
        {step === 'register' && userType && (
          <Card className="p-8 bg-white">
            <button
              onClick={() => setStep('login')}
              className="text-blue-600 hover:text-blue-700 text-sm mb-4"
            >
              ← Back to user selection
            </button>

            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              Create New {userType === 'patient' ? 'Patient' : 'Caregiver'} Profile
            </h2>

            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                <Input
                  value={newUserName}
                  onChange={(e) => setNewUserName(e.target.value)}
                  placeholder="Enter full name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
                <Input
                  type="email"
                  value={newUserEmail}
                  onChange={(e) => setNewUserEmail(e.target.value)}
                  placeholder="Enter email address"
                />
              </div>
            </div>

            <Button
              onClick={handleCreateUser}
              disabled={isLoading || !newUserName.trim() || !newUserEmail.trim()}
              className="w-full mb-3"
            >
              {isLoading ? (
                <>
                  <Loader className="inline w-4 h-4 mr-2 animate-spin" />
                  Creating...
                </>
              ) : (
                `Create ${userType === 'patient' ? 'Patient' : 'Caregiver'} Profile`
              )}
            </Button>

            <button
              onClick={() => setStep('login')}
              className="w-full p-2 text-gray-600 text-sm hover:text-gray-700"
            >
              Cancel
            </button>
          </Card>
        )}
      </div>
    </div>
  );
}
