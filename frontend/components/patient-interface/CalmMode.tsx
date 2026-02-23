'use client'

import { useEffect, useState } from 'react'
import { X } from 'lucide-react'
import { OrientationCard } from '@/components/shared/OrientationCard'

interface Memory {
  id: number
  title: string
  description: string
}

interface CalmModeProps {
  memories?: Memory[]
  onClose?: () => void
}

const DEFAULT_MEMORIES = [
  {
    id: 1,
    title: 'Family Gatherings',
    description: 'Cherished moments with loved ones, full of laughter and joy.',
  },
  {
    id: 2,
    title: 'Special Holidays',
    description: 'Celebrations filled with warmth and wonderful traditions.',
  },
  {
    id: 3,
    title: 'Peaceful Moments',
    description: 'Quiet times of rest and reflection in your favorite places.',
  },
  {
    id: 4,
    title: 'Nature & Seasons',
    description: 'The beauty of the outdoors and the cycles of nature.',
  },
]

export function CalmMode({ memories = DEFAULT_MEMORIES, onClose }: CalmModeProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isAutoPlay, setIsAutoPlay] = useState(true)

  useEffect(() => {
    if (!isAutoPlay) return

    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % memories.length)
    }, 4000) // Change every 4 seconds

    return () => clearInterval(interval)
  }, [isAutoPlay, memories.length])

  const currentMemory = memories[currentIndex]

  const handlePrevious = () => {
    setCurrentIndex((prev) =>
      prev === 0 ? memories.length - 1 : prev - 1
    )
    setIsAutoPlay(false)
  }

  const handleNext = () => {
    setCurrentIndex((prev) => (prev + 1) % memories.length)
    setIsAutoPlay(false)
  }

  return (
    <div className="relative min-h-screen flex items-center justify-center p-4 sm:p-6 bg-gradient-to-br from-primary/5 via-accent/5 to-secondary/5">
      {/* Close button */}
      {onClose && (
        <button
          onClick={onClose}
          className="absolute top-4 sm:top-6 right-4 sm:right-6 p-3 rounded-full bg-card border border-border hover:bg-muted transition-colors"
          aria-label="Close calm mode"
        >
          <X className="w-6 h-6 text-foreground" />
        </button>
      )}

      <div className="w-full max-w-2xl">
        {/* Memory Display */}
        <OrientationCard variant="soft" className="mb-6 sm:mb-8 text-center min-h-64 sm:min-h-80 flex flex-col justify-center">
          <div className="text-6xl sm:text-8xl mb-6 animate-bounce">
            ✨
          </div>
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
            {currentMemory.title}
          </h2>
          <p className="text-xl sm:text-2xl text-muted-foreground leading-relaxed">
            {currentMemory.description}
          </p>
          <div className="mt-6 flex gap-2 justify-center">
            {memories.map((_, index) => (
              <div
                key={index}
                className={`h-2 sm:h-3 rounded-full transition-all ${
                  index === currentIndex
                    ? 'w-8 sm:w-10 bg-accent'
                    : 'w-2 sm:w-3 bg-muted'
                }`}
              />
            ))}
          </div>
        </OrientationCard>

        {/* Navigation Controls */}
        <div className="grid grid-cols-3 gap-4 sm:gap-6 mb-8">
          <button
            onClick={handlePrevious}
            className="h-16 sm:h-20 px-4 rounded-2xl font-bold text-lg sm:text-xl bg-card hover:bg-secondary/20 border border-border transition-all duration-200"
          >
            ← Previous
          </button>

          <button
            onClick={() => setIsAutoPlay(!isAutoPlay)}
            className="h-16 sm:h-20 px-4 rounded-2xl font-bold text-lg sm:text-xl bg-accent hover:bg-accent/90 text-accent-foreground transition-all duration-200"
          >
            {isAutoPlay ? '⏸' : '▶'}
          </button>

          <button
            onClick={handleNext}
            className="h-16 sm:h-20 px-4 rounded-2xl font-bold text-lg sm:text-xl bg-card hover:bg-secondary/20 border border-border transition-all duration-200"
          >
            Next →
          </button>
        </div>

        {/* Reassurance Message */}
        <OrientationCard variant="accent">
          <p className="text-lg sm:text-xl text-foreground text-center leading-relaxed">
            Take a deep breath. You are surrounded by love and beautiful memories. Let these moments bring you peace.
          </p>
        </OrientationCard>
      </div>
    </div>
  )
}
