import { ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface OrientationCardProps {
  children: ReactNode
  variant?: 'default' | 'accent' | 'soft'
  className?: string
}

export function OrientationCard({
  children,
  variant = 'default',
  className,
}: OrientationCardProps) {
  const variants = {
    default: 'bg-card border border-border shadow-sm',
    accent: 'bg-accent/5 border border-accent/20 shadow-sm',
    soft: 'bg-secondary border border-secondary/30 shadow-sm',
  }

  return (
    <div
      className={cn(
        'rounded-3xl p-6 sm:p-8 transition-all duration-200',
        variants[variant],
        className,
      )}
    >
      {children}
    </div>
  )
}
