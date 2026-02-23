import { Heart, Users, Clock, Info } from 'lucide-react'
import { OrientationCard } from '@/components/shared/OrientationCard'

export function CaregiverSetupGuide() {
  return (
    <div className="space-y-6 sm:space-y-8 max-w-4xl mx-auto p-4 sm:p-6">
      <div className="text-center mb-8 sm:mb-10">
        <h1 className="text-4xl sm:text-5xl font-bold text-primary mb-3">
          Anchor Caregiver Setup
        </h1>
        <p className="text-lg sm:text-xl text-muted-foreground">
          Personalize the app for your loved one in just a few steps
        </p>
      </div>

      {/* Step 1: Patient Information */}
      <OrientationCard variant="default">
        <div className="flex items-start gap-4 mb-4">
          <div className="flex-shrink-0">
            <div className="flex items-center justify-center h-12 w-12 rounded-xl bg-primary/10">
              <Info className="h-6 w-6 text-primary" />
            </div>
          </div>
          <div>
            <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-2">
              Step 1: Patient Information
            </h2>
            <ul className="space-y-2 text-lg sm:text-xl text-muted-foreground">
              <li>
                <strong>Patient Name:</strong> Use the name your loved one is most comfortable with
              </li>
              <li>
                <strong>Location:</strong> The primary location (e.g., "Home", "Assisted Living")
              </li>
              <li>
                <strong>Home Details:</strong> Description of their living space for orientation
              </li>
            </ul>
            <p className="mt-3 text-base sm:text-lg text-foreground font-semibold">
              Edit in: <code className="bg-secondary/30 px-2 py-1 rounded">app/page.tsx</code>
            </p>
          </div>
        </div>
      </OrientationCard>

      {/* Step 2: Family Members */}
      <OrientationCard variant="default">
        <div className="flex items-start gap-4 mb-4">
          <div className="flex-shrink-0">
            <div className="flex items-center justify-center h-12 w-12 rounded-xl bg-accent/10">
              <Users className="h-6 w-6 text-accent" />
            </div>
          </div>
          <div>
            <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-2">
              Step 2: Add Family Members
            </h2>
            <ul className="space-y-2 text-lg sm:text-xl text-muted-foreground mb-4">
              <li>
                <strong>Name:</strong> Full name of family member
              </li>
              <li>
                <strong>Relationship:</strong> How they relate (e.g., "Your Daughter", "Your Son", "Your Grandchild")
              </li>
              <li>
                <strong>Description:</strong> Personal details (occupation, interests, how often they visit)
              </li>
            </ul>
            <div className="bg-secondary/20 rounded-lg p-4 mt-3">
              <p className="font-mono text-sm sm:text-base text-foreground">
                const SAMPLE_FAMILY_MEMBERS = [<br />
                {'  '}{'{'}
                id: 1, name: 'Sarah', ...<br />
                {'}'},<br />
                ]
              </p>
            </div>
          </div>
        </div>
      </OrientationCard>

      {/* Step 3: Daily Events */}
      <OrientationCard variant="default">
        <div className="flex items-start gap-4 mb-4">
          <div className="flex-shrink-0">
            <div className="flex items-center justify-center h-12 w-12 rounded-xl bg-secondary/10">
              <Clock className="h-6 w-6 text-secondary-foreground" />
            </div>
          </div>
          <div>
            <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-2">
              Step 3: Schedule Daily Events
            </h2>
            <ul className="space-y-2 text-lg sm:text-xl text-muted-foreground mb-4">
              <li>
                <strong>Person:</strong> Who is visiting or calling
              </li>
              <li>
                <strong>Action:</strong> What they're doing (visiting, calling, etc.)
              </li>
              <li>
                <strong>Time:</strong> When it's happening (e.g., "2:00 PM")
              </li>
            </ul>
            <div className="bg-secondary/20 rounded-lg p-4 mt-3">
              <p className="font-mono text-sm sm:text-base text-foreground">
                const SAMPLE_EVENTS_TODAY = [<br />
                {'  '}{'{'}
                id: 1, person: 'Sarah', ...<br />
                {'}'},<br />
                ]
              </p>
            </div>
          </div>
        </div>
      </OrientationCard>

      {/* Step 4: Customization Tips */}
      <OrientationCard variant="accent">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0">
            <div className="flex items-center justify-center h-12 w-12 rounded-xl bg-accent/20">
              <Heart className="h-6 w-6 text-accent" />
            </div>
          </div>
          <div>
            <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-4">
              Personalization Tips
            </h2>
            <ul className="space-y-3 text-lg sm:text-xl text-muted-foreground">
              <li>
                <strong className="text-foreground">Use Familiar Names:</strong> Use the names and terms your loved one has used throughout their life
              </li>
              <li>
                <strong className="text-foreground">Warm Descriptions:</strong> Write in a warm, loving tone. Include personal touches about each family member
              </li>
              <li>
                <strong className="text-foreground">Regular Updates:</strong> Update daily events regularly to keep content current and relevant
              </li>
              <li>
                <strong className="text-foreground">Test First:</strong> Test the app on your patient's device before making it their primary tool
              </li>
              <li>
                <strong className="text-foreground">Keep Sessions Short:</strong> 5-10 minute sessions work best to avoid cognitive overload
              </li>
              <li>
                <strong className="text-foreground">Adjust Text Size:</strong> Use browser zoom (Ctrl/Cmd + +) if needed for better readability
              </li>
            </ul>
          </div>
        </div>
      </OrientationCard>

      {/* Configuration Template */}
      <OrientationCard variant="default">
        <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-4">
          Quick Configuration Template
        </h2>
        <div className="bg-muted rounded-lg p-4 sm:p-6 overflow-auto">
          <pre className="font-mono text-sm sm:text-base text-foreground whitespace-pre-wrap break-words">
{`// Edit these in app/page.tsx

const SAMPLE_PATIENT_NAME = 'Margaret'
const SAMPLE_LOCATION = 'Home'

const SAMPLE_FAMILY_MEMBERS = [
  {
    id: 1,
    name: 'Sarah',
    relationship: 'Your Daughter',
    description: 'Sarah is a teacher and visits every Sunday.',
  },
  // Add more family members
]

const SAMPLE_EVENTS_TODAY = [
  {
    id: 1,
    person: 'Sarah',
    action: 'is visiting',
    time: '2:00 PM',
  },
  // Add more events
]`}
          </pre>
        </div>
      </OrientationCard>

      {/* Support Information */}
      <div className="text-center p-6 sm:p-8 bg-secondary/10 rounded-3xl border border-secondary/20">
        <p className="text-lg sm:text-xl text-foreground mb-3">
          Created with care for Alzheimer's patients and their caregivers.
        </p>
        <p className="text-base sm:text-lg text-muted-foreground">
          For more information, see <code className="bg-card px-2 py-1 rounded">ANCHOR_README.md</code>
        </p>
      </div>
    </div>
  )
}
