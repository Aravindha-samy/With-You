# Anchor - Digital Companion for Alzheimer's Patients

A warm, accessible, and emotionally intelligent digital companion designed to help Alzheimer's patients maintain daily orientation, reduce anxiety, and stay connected with their loved ones.

## Features

### Patient Interface

**Home Screen**
- Time-based greeting (Good Morning/Afternoon/Evening)
- Current date and time display
- Daily orientation context
- Today's events and visits
- Quick action buttons with large, tap-friendly targets

**Orientation Support**
- "Where Am I?" - Detailed home descriptions and location context
- Explains surroundings in calm, reassuring language
- Breaks down the patient's environment into familiar spaces

**Family Connection**
- "Who Is This?" - Family photo gallery with relationships
- Personal details about each family member
- Reduces confusion and promotes recognition

**Calm Mode**
- Memory slideshow with soothing transitions
- Auto-rotating memories with manual controls
- Emotional reassurance messages
- Peaceful visual design for anxiety reduction

**Mood Check-in**
- Emotion recognition with emoji-based selection
- Personalized responses based on mood
- Comfort messages and emotional support
- Non-clinical, warm approach to emotional awareness

**Emergency Contacts**
- Quick-call buttons for trusted family members
- Large, prominent contact information
- Simple, one-tap calling interface

### Design Principles

**Accessibility First**
- Minimum 18px text for patient interface
- Large touch targets (48px+ buttons)
- High contrast colors (WCAG AA compliant)
- Simple, clear navigation with minimal cognitive load
- Keyboard navigation support
- Reduced motion respect

**Warm, Therapeutic Aesthetic**
- Soft blue primary color (#9FB8D8 equivalent) - calming and trustworthy
- Warm cream secondary (#F5F1EB equivalent) - welcoming and safe
- Gentle green accent (#A8D5BA equivalent) - growth and healing
- Smooth, rounded corners for a gentle feel
- Soft shadows and subtle animations

**Emotional Tone**
- Never clinical or intimidating
- Always reassuring and warm
- Patient-centered language
- Dignity and respect in every interaction
- Focus on love and connection

## Component Structure

```
/components
├── /patient-interface
│   ├── Header.tsx              # Time-based greeting and date display
│   ├── MemoryCard.tsx          # Card component for memories and events
│   ├── CalmMode.tsx            # Memory slideshow for relaxation
│   ├── MoodCheckIn.tsx         # Emotional check-in interface
│   └── EmergencyContacts.tsx    # Quick-call family contacts
└── /shared
    ├── LargeButton.tsx         # Accessible large button component
    ├── OrientationCard.tsx      # Reusable card wrapper
    └── FamilyMember.tsx        # Family profile card component
```

## Pages

- `/` - Main patient dashboard
  - Home screen view
  - Orientation details view
  - Family gallery view

## Color System

The app uses a warm, therapeutic color palette designed for comfort and accessibility:

- **Primary**: Soft Blue (`oklch(0.6 0.15 260)`) - Calming, trustworthy
- **Secondary**: Warm Cream (`oklch(0.95 0.05 80)`) - Welcoming, safe
- **Accent**: Gentle Green (`oklch(0.65 0.12 140)`) - Growth, healing
- **Background**: Warm Off-White (`oklch(0.98 0.02 90)`) - Clean, comfortable
- **Foreground**: Deep Warm Brown (`oklch(0.2 0.05 30)`) - Readable, warm

## Customization

### Adding Family Members

Edit the `SAMPLE_FAMILY_MEMBERS` array in `/app/page.tsx`:

```typescript
const SAMPLE_FAMILY_MEMBERS = [
  {
    id: 1,
    name: 'Sarah',
    relationship: 'Your Daughter',
    description: 'Sarah is a teacher and visits every Sunday.',
  },
  // Add more family members...
]
```

### Customizing Patient Name

Update the `SAMPLE_PATIENT_NAME` constant in `/app/page.tsx`:

```typescript
const SAMPLE_PATIENT_NAME = 'Margaret'
```

### Adding Daily Events

Modify the `SAMPLE_EVENTS_TODAY` array to include scheduled visits:

```typescript
const SAMPLE_EVENTS_TODAY = [
  {
    id: 1,
    person: 'Sarah',
    action: 'is visiting',
    time: '2:00 PM',
  },
  // Add more events...
]
```

## Accessibility Features

- **Large Text**: Minimum 18px for patient interface
- **High Contrast**: WCAG AA compliant color combinations
- **Touch-Friendly**: All buttons are minimum 48x48px
- **Keyboard Navigation**: Full keyboard support with visible focus indicators
- **Reduced Motion**: Respects `prefers-reduced-motion` system preference
- **Screen Reader Support**: Semantic HTML with proper ARIA labels
- **Simple Navigation**: Maximum 2-3 taps to access any feature

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Optimized for tablets (iPad, Android tablets)
- Mobile-first responsive design
- Works on devices with older hardware

## Development

### Setup

```bash
pnpm install
pnpm dev
```

The app will start at `http://localhost:3000`

### Building

```bash
pnpm build
pnpm start
```

### Technologies

- **Next.js 16** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library
- **Lucide React** - Icons

## Future Enhancements

- Backend integration for data persistence
- Photo upload and memory management
- Voice message from family members
- Caregiver dashboard for profile management
- Music/audio for calm mode
- Medication reminders
- Multi-language support
- Dark mode with warm tones

## Support

This application is designed with love for Alzheimer's patients and their caregivers. For support or feature requests, please consult with healthcare professionals and patient families.

## Notes for Caregivers

- Personalize patient names and family information for maximum effectiveness
- Update daily events regularly to keep content relevant
- Use warm, encouraging language when recording messages
- Test on your patient's device before regular use
- Keep sessions short (5-10 minutes) to avoid cognitive overload
- Adjust text size if needed using browser zoom

## License

Created with care for the Alzheimer's community.
