'use client'

import { useEffect, useState } from 'react'

interface HeaderProps {
  patientName: string
}

export function Header({ patientName }: HeaderProps) {
  const [greeting, setGreeting] = useState('')
  const [currentDate, setCurrentDate] = useState('')
  const [currentTime, setCurrentTime] = useState('')

  useEffect(() => {
    const updateTime = () => {
      const now = new Date()
      const hours = now.getHours()

      // Determine greeting based on time of day
      if (hours < 12) {
        setGreeting('Good Morning')
      } else if (hours < 18) {
        setGreeting('Good Afternoon')
      } else {
        setGreeting('Good Evening')
      }

      // Format date
      const dateFormatter = new Intl.DateTimeFormat('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric',
      })
      setCurrentDate(dateFormatter.format(now))

      // Format time
      const timeFormatter = new Intl.DateTimeFormat('en-US', {
        hour: '2-digit',
        minute: '2-digit',
      })
      setCurrentTime(timeFormatter.format(now))
    }

    updateTime()
    const interval = setInterval(updateTime, 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="bg-gradient-to-b from-primary/10 to-transparent p-6 sm:p-8 text-center">
      <h1 className="text-4xl sm:text-5xl font-bold text-primary mb-2">
        {greeting},
      </h1>
      <h2 className="text-3xl sm:text-4xl font-semibold text-foreground mb-6">
        {patientName}
      </h2>

      <div className="flex flex-col sm:flex-row items-center justify-center gap-6 mt-8">
        <div className="bg-card rounded-2xl p-6 shadow-sm border border-border min-w-fit">
          <div className="text-sm text-muted-foreground mb-1">Today is</div>
          <div className="text-lg sm:text-xl font-semibold text-foreground text-balance">
            {currentDate}
          </div>
        </div>

        <div className="bg-accent/10 rounded-2xl p-6 shadow-sm border border-border">
          <div className="text-sm text-muted-foreground mb-1">Current time</div>
          <div className="text-3xl sm:text-4xl font-bold text-accent font-mono">
            {currentTime}
          </div>
        </div>
      </div>
    </div>
  )
}
