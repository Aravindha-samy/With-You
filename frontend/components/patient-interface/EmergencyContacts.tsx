import { Phone } from 'lucide-react'
import { LargeButton } from '@/components/shared/LargeButton'
import { OrientationCard } from '@/components/shared/OrientationCard'

interface Contact {
  id: number
  name: string
  role: string
  phone?: string
}

interface EmergencyContactsProps {
  contacts: Contact[]
}

export function EmergencyContacts({ contacts }: EmergencyContactsProps) {
  return (
    <div className="space-y-6 sm:space-y-8">
      <OrientationCard variant="default">
        <div className="flex items-center gap-3 mb-4">
          <Phone className="w-8 h-8 text-accent" />
          <h2 className="text-2xl sm:text-3xl font-bold text-foreground">
            Emergency Contacts
          </h2>
        </div>

        <p className="text-lg sm:text-xl text-muted-foreground mb-6">
          These are your trusted family members. Press their button to call them anytime.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
          {contacts.map((contact) => (
            <div
              key={contact.id}
              className="bg-secondary/20 rounded-2xl p-4 sm:p-6 border border-secondary/30"
            >
              <h3 className="text-xl sm:text-2xl font-bold text-foreground mb-1">
                {contact.name}
              </h3>
              <p className="text-base sm:text-lg text-accent font-semibold mb-4">
                {contact.role}
              </p>
              {contact.phone && (
                <LargeButton variant="accent" className="w-full">
                  Call {contact.name}
                </LargeButton>
              )}
            </div>
          ))}
        </div>
      </OrientationCard>

      <OrientationCard variant="accent">
        <h3 className="text-2xl sm:text-3xl font-bold text-foreground mb-4">
          Need Help?
        </h3>
        <p className="text-lg sm:text-xl text-muted-foreground mb-6">
          If you feel confused, scared, or need help, press one of the buttons above to reach your family. They are always ready to help you.
        </p>
      </OrientationCard>
    </div>
  )
}
