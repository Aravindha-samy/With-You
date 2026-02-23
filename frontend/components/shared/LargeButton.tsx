import { ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface LargeButtonProps {
  children: ReactNode
  onClick?: () => void
  variant?: 'primary' | 'secondary' | 'accent'
  disabled?: boolean
  className?: string
}

export function LargeButton({
  children,
  onClick,
  variant = 'primary',
  disabled = false,
  className,
}: LargeButtonProps) {
  const variants = {
    primary:
      'bg-primary hover:bg-primary/90 text-primary-foreground shadow-md hover:shadow-lg',
    secondary:
      'bg-secondary hover:bg-secondary/80 text-secondary-foreground shadow-md hover:shadow-lg',
    accent:
      'bg-accent hover:bg-accent/90 text-accent-foreground shadow-md hover:shadow-lg',
  }

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={cn(
        'h-16 sm:h-20 px-6 sm:px-8 rounded-2xl font-bold text-lg sm:text-2xl',
        'transition-all duration-200 active:scale-95',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        'focus:outline-none focus:ring-4 focus:ring-primary/30',
        variants[variant],
        className,
      )}
    >
      {children}
    </button>
  )
}
