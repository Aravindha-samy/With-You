'use client'

import { useState } from 'react'
import { Heart } from 'lucide-react'
import { OrientationCard } from '@/components/shared/OrientationCard'
import { LargeButton } from '@/components/shared/LargeButton'

const MOODS = [
  { id: 'happy', emoji: '😊', label: 'Happy', message: 'That\'s wonderful! Enjoy this beautiful moment.' },
  { id: 'calm', emoji: '😌', label: 'Calm', message: 'You are doing great. Stay in this peaceful moment.' },
  { id: 'worried', emoji: '😟', label: 'Worried', message: 'It\'s okay to feel worried. Your family is here for you.' },
  { id: 'tired', emoji: '😴', label: 'Tired', message: 'Rest is important. Take some time to relax and recharge.' },
]

interface MoodCheckInProps {
  onMoodSelect?: (mood: string) => void
}

export function MoodCheckIn({ onMoodSelect }: MoodCheckInProps) {
  const [selectedMood, setSelectedMood] = useState<string | null>(null)
  const [showMessage, setShowMessage] = useState(false)

  const handleMoodClick = (moodId: string) => {
    setSelectedMood(moodId)
    setShowMessage(true)
    onMoodSelect?.(moodId)
    
    // Reset after 5 seconds
    setTimeout(() => {
      setShowMessage(false)
      setSelectedMood(null)
    }, 5000)
  }

  const selectedMoodData = MOODS.find((m) => m.id === selectedMood)

  return (
    <div className="space-y-6 sm:space-y-8">
      <OrientationCard variant="default">
        <div className="flex items-center gap-3 mb-4">
          <Heart className="w-8 h-8 text-accent" />
          <h2 className="text-2xl sm:text-3xl font-bold text-foreground">
            How are you feeling?
          </h2>
        </div>

        <p className="text-lg sm:text-xl text-muted-foreground mb-8">
          Take a moment to check in with yourself. Choose how you are feeling right now.
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 sm:gap-6">
          {MOODS.map((mood) => (
            <button
              key={mood.id}
              onClick={() => handleMoodClick(mood.id)}
              className={`
                flex flex-col items-center justify-center gap-2 p-4 sm:p-6
                rounded-2xl transition-all duration-200 border-2
                ${
                  selectedMood === mood.id
                    ? 'bg-accent/20 border-accent shadow-lg scale-105'
                    : 'bg-secondary/20 border-secondary/30 hover:border-accent/50'
                }
              `}
            >
              <span className="text-4xl sm:text-6xl">{mood.emoji}</span>
              <span className="text-base sm:text-lg font-semibold text-foreground">
                {mood.label}
              </span>
            </button>
          ))}
        </div>
      </OrientationCard>

      {showMessage && selectedMoodData && (
        <OrientationCard variant="accent" className="animate-in fade-in slide-in-from-top">
          <p className="text-xl sm:text-2xl text-foreground font-semibold text-center">
            {selectedMoodData.message}
          </p>
        </OrientationCard>
      )}

      <OrientationCard variant="soft">
        <h3 className="text-2xl sm:text-3xl font-bold text-foreground mb-4 text-center">
          Words of Comfort
        </h3>
        <div className="space-y-4">
          <p className="text-lg sm:text-xl text-muted-foreground text-center leading-relaxed">
            Whatever you are feeling is okay. You are safe, loved, and supported.
          </p>
          <p className="text-lg sm:text-xl text-muted-foreground text-center leading-relaxed">
            Your family is thinking of you and wants the best for you.
          </p>
          <p className="text-lg sm:text-xl text-muted-foreground text-center leading-relaxed">
            Take each moment as it comes. You are doing your best, and that is enough.
          </p>
        </div>
      </OrientationCard>
    </div>
  )
}
