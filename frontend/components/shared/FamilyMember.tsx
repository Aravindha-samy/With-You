import { ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface FamilyMemberProps {
  name: string
  relationship: string
  image?: string
  description?: string
  children?: ReactNode
  className?: string
}

export function FamilyMember({
  name,
  relationship,
  image,
  description,
  children,
  className,
}: FamilyMemberProps) {
  return (
    <div
      className={cn(
        'bg-card border border-border rounded-3xl p-6 sm:p-8 shadow-sm',
        'hover:shadow-md transition-all duration-200',
        className,
      )}
    >
      {image && (
        <div className="mb-4 rounded-2xl overflow-hidden bg-muted h-40 sm:h-48 w-full">
          <img
            src={image}
            alt={name}
            className="w-full h-full object-cover"
          />
        </div>
      )}

      <h3 className="text-2xl sm:text-3xl font-bold text-foreground mb-1">
        {name}
      </h3>
      <p className="text-lg sm:text-xl text-accent font-semibold mb-3">
        {relationship}
      </p>

      {description && (
        <p className="text-base sm:text-lg text-muted-foreground mb-4 leading-relaxed">
          {description}
        </p>
      )}

      {children}
    </div>
  )
}
