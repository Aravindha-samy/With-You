'use client';

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { User } from '@/lib/types';

interface UserContextType {
  currentUser: User | null;
  selectedPatient: User | null;
  setCurrentUser: (user: User | null) => void;
  setSelectedPatient: (patient: User | null) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: ReactNode }) {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [selectedPatient, setSelectedPatient] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSetCurrentUser = useCallback((user: User | null) => {
    setCurrentUser(user);
    // Clear selected patient when user changes
    if (user?.user_type === 'patient') {
      setSelectedPatient(null);
    }
  }, []);

  const handleSetSelectedPatient = useCallback((patient: User | null) => {
    setSelectedPatient(patient);
  }, []);

  const value: UserContextType = {
    currentUser,
    selectedPatient,
    setCurrentUser: handleSetCurrentUser,
    setSelectedPatient: handleSetSelectedPatient,
    isLoading,
    setIsLoading,
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}
