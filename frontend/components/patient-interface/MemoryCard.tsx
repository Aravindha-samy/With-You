'use client'

import { ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface MemoryCardProps {
  title: string
  image?: string
  children?: ReactNode
  onClick?: () => void
  className?: string
}

export function MemoryCard({
  title,
  image,
  children,
  onClick,
  className,
}: MemoryCardProps) {
  return (
    <div
      onClick={onClick}
      className={cn(
        'bg-card border border-border rounded-3xl overflow-hidden shadow-sm',
        'hover:shadow-md transition-all duration-200 hover:scale-105',
        onClick && 'cursor-pointer',
        className,
      )}
    >
      {image && (
        <div className="h-40 sm:h-56 w-full bg-muted overflow-hidden">
          <img
            src={image}
            alt={title}
            className="w-full h-full object-cover"
          />
        </div>
      )}

      <div className="p-6 sm:p-8">
        <h3 className="text-2xl sm:text-3xl font-bold text-foreground mb-2 text-balance">
          {title}
        </h3>
        {children}
      </div>
    </div>
  )
}
