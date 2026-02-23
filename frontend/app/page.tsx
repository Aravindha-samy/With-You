'use client'

import { useState } from 'react'
import { Header } from '@/components/patient-interface/Header'
import { MemoryCard } from '@/components/patient-interface/MemoryCard'
import { LargeButton } from '@/components/shared/LargeButton'
import { OrientationCard } from '@/components/shared/OrientationCard'
import { FamilyMember } from '@/components/shared/FamilyMember'

const SAMPLE_PATIENT_NAME = 'Margaret'
const SAMPLE_LOCATION = 'Home'

const SAMPLE_FAMILY_MEMBERS = [
  {
    id: 1,
    name: 'Sarah',
    relationship: 'Your Daughter',
    description: 'Sarah is a teacher and visits every Sunday. She brings the grandchildren to see you.',
  },
  {
    id: 2,
    name: 'James',
    relationship: 'Your Son',
    description: 'James works as an engineer. He calls you every Wednesday evening.',
  },
  {
    id: 3,
    name: 'Emma',
    relationship: 'Your Granddaughter',
    description: 'Emma is 8 years old. She loves to draw pictures and show them to you.',
  },
]

const SAMPLE_EVENTS_TODAY = [
  {
    id: 1,
    person: 'Sarah',
    action: 'is visiting',
    time: '2:00 PM',
  },
  {
    id: 2,
    person: 'James',
    action: 'will call',
    time: '7:00 PM',
  },
]

export default function Home() {
  const [currentView, setCurrentView] = useState<'home' | 'family' | 'orientation'>('home')

  const renderHome = () => (
    <div className="w-full">
      <Header patientName={SAMPLE_PATIENT_NAME} />

      <div className="px-4 sm:px-6 py-6 sm:py-8 max-w-4xl mx-auto">
        {/* Where Am I Card */}
        <OrientationCard variant="accent" className="mb-6 sm:mb-8">
          <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-3">
            Where are you?
          </h2>
          <p className="text-lg sm:text-xl text-muted-foreground mb-4 leading-relaxed">
            You are at home, in your comfortable living room. This is your safe space where you live.
          </p>
          <button
            onClick={() => setCurrentView('orientation')}
            className="text-lg sm:text-xl font-semibold text-accent hover:text-accent/80 transition-colors underline"
          >
            Learn more about your home →
          </button>
        </OrientationCard>

        {/* Today's Events */}
        <div className="mb-8 sm:mb-10">
          <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-4 sm:mb-6">
            Today's Special Moments
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
            {SAMPLE_EVENTS_TODAY.map((event) => (
              <MemoryCard key={event.id} title={event.person}>
                <p className="text-lg sm:text-xl text-muted-foreground mb-3">
                  {event.action} at <span className="font-bold text-accent">{event.time}</span>
                </p>
              </MemoryCard>
            ))}
          </div>
        </div>

        {/* Quick Action Buttons */}
        <div className="mb-8 sm:mb-10">
          <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-4 sm:mb-6">
            Quick Actions
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
            <LargeButton
              variant="primary"
              onClick={() => setCurrentView('orientation')}
            >
              Where Am I?
            </LargeButton>
            <LargeButton
              variant="accent"
              onClick={() => setCurrentView('family')}
            >
              Who Is This?
            </LargeButton>
            <LargeButton variant="secondary">
              Call Family
            </LargeButton>
            <LargeButton variant="accent">
              Calm Mode
            </LargeButton>
          </div>
        </div>

        {/* Reassurance Message */}
        <OrientationCard variant="soft" className="text-center">
          <p className="text-xl sm:text-2xl text-foreground font-semibold mb-2">
            You are safe and loved.
          </p>
          <p className="text-lg sm:text-xl text-muted-foreground">
            Your family is always here for you. Take a moment to breathe and enjoy this day.
          </p>
        </OrientationCard>
      </div>
    </div>
  )

  const renderOrientation = () => (
    <div className="w-full">
      <div className="bg-gradient-to-b from-primary/10 to-transparent p-6 sm:p-8">
        <button
          onClick={() => setCurrentView('home')}
          className="text-lg sm:text-xl font-semibold text-primary hover:text-primary/80 transition-colors mb-6"
        >
          ← Back to Home
        </button>
        <h1 className="text-3xl sm:text-4xl font-bold text-primary">Your Home</h1>
      </div>

      <div className="px-4 sm:px-6 py-6 sm:py-8 max-w-4xl mx-auto">
        <OrientationCard variant="default" className="mb-8 sm:mb-10">
          <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-4">
            Welcome Home
          </h2>
          <p className="text-lg sm:text-xl text-muted-foreground mb-6 leading-relaxed">
            This is your home, where you have lived for many years. It is your safe space, filled with memories and comfort. Everything you see around you is familiar and belongs to you.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
            <div className="bg-secondary/30 rounded-2xl p-4 sm:p-6">
              <h3 className="text-xl sm:text-2xl font-bold text-foreground mb-2">Your Living Room</h3>
              <p className="text-base sm:text-lg text-muted-foreground">
                This is where you spend your time relaxing and enjoying moments with family.
              </p>
            </div>

            <div className="bg-accent/10 rounded-2xl p-4 sm:p-6">
              <h3 className="text-xl sm:text-2xl font-bold text-foreground mb-2">Your Bedroom</h3>
              <p className="text-base sm:text-lg text-muted-foreground">
                Your comfortable bedroom where you rest and sleep peacefully at night.
              </p>
            </div>

            <div className="bg-secondary/30 rounded-2xl p-4 sm:p-6">
              <h3 className="text-xl sm:text-2xl font-bold text-foreground mb-2">Your Kitchen</h3>
              <p className="text-base sm:text-lg text-muted-foreground">
                Where delicious meals are prepared. The heart of your home.
              </p>
            </div>

            <div className="bg-accent/10 rounded-2xl p-4 sm:p-6">
              <h3 className="text-xl sm:text-2xl font-bold text-foreground mb-2">Your Garden</h3>
              <p className="text-base sm:text-lg text-muted-foreground">
                A peaceful outdoor space where you can enjoy the fresh air and nature.
              </p>
            </div>
          </div>
        </OrientationCard>

        <button
          onClick={() => setCurrentView('home')}
          className="w-full h-16 sm:h-20 px-6 sm:px-8 rounded-2xl font-bold text-lg sm:text-2xl bg-primary hover:bg-primary/90 text-primary-foreground transition-all duration-200"
        >
          Return to Home
        </button>
      </div>
    </div>
  )

  const renderFamily = () => (
    <div className="w-full">
      <div className="bg-gradient-to-b from-primary/10 to-transparent p-6 sm:p-8">
        <button
          onClick={() => setCurrentView('home')}
          className="text-lg sm:text-xl font-semibold text-primary hover:text-primary/80 transition-colors mb-6"
        >
          ← Back to Home
        </button>
        <h1 className="text-3xl sm:text-4xl font-bold text-primary">Your Family</h1>
      </div>

      <div className="px-4 sm:px-6 py-6 sm:py-8 max-w-4xl mx-auto">
        <div className="grid grid-cols-1 gap-6 sm:gap-8 mb-8">
          {SAMPLE_FAMILY_MEMBERS.map((member) => (
            <FamilyMember
              key={member.id}
              name={member.name}
              relationship={member.relationship}
              description={member.description}
            />
          ))}
        </div>

        <button
          onClick={() => setCurrentView('home')}
          className="w-full h-16 sm:h-20 px-6 sm:px-8 rounded-2xl font-bold text-lg sm:text-2xl bg-primary hover:bg-primary/90 text-primary-foreground transition-all duration-200"
        >
          Return to Home
        </button>
      </div>
    </div>
  )

  return (
    <main className="min-h-screen bg-background text-foreground">
      {currentView === 'home' && renderHome()}
      {currentView === 'orientation' && renderOrientation()}
      {currentView === 'family' && renderFamily()}
    </main>
  )
}
