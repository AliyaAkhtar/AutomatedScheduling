import Link from 'next/link'
import { CalendarClock } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center text-center overflow-hidden bg-gradient-to-br from-[#fce9eb] to-[#fef7f8]">
      {/* Background pattern */}
      <div className="absolute inset-0 z-0 opacity-30 pointer-events-none">
        <svg
          className="w-full h-full"
          xmlns="http://www.w3.org/2000/svg"
          preserveAspectRatio="xMidYMid slice"
        >
          <defs>
            <pattern
              id="grid"
              width="40"
              height="40"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M40 0H0V40"
                fill="none"
                stroke="#f05a66"
                strokeWidth="0.5"
              />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      {/* Content */}
      <div className="relative z-10 p-8 max-w-lg">
        <div className="mb-6">
          <CalendarClock className="w-16 h-16 text-[#f05a66] animate-pulse mx-auto" />
        </div>
        <h1 className="text-4xl font-extrabold text-[#f05a66] mb-4">
          Automated Meeting Scheduler
        </h1>
        <p className="text-gray-700 mb-8 text-lg">
          Streamline your scheduling process with smart, auto-generated Google Meet links. Invite individuals or groups with ease.
        </p>
        <Link
          href="/automatedScheduler"
          className="inline-block bg-[#f05a66] text-white px-8 py-3 rounded-lg hover:bg-[#e24c58] transition-colors shadow-lg"
        >
          Launch Scheduler
        </Link>
      </div>
    </div>
  )
}
