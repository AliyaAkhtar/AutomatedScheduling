'use client'

import { useState } from 'react'

export default function AutomatedSchedulerPage() {
    const [emails, setEmails] = useState([''])
    const [mode, setMode] = useState('group') // group or individual
    const [loading, setLoading] = useState(false)
    const [response, setResponse] = useState(null)

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setResponse(null)

        const url =
            mode === 'group'
                ? 'http://localhost:8000/schedule/group'
                : 'http://localhost:8000/schedule/individual'

        try {
            const res = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ emails: emails.map(e => e.trim()) }),
            })

            const data = await res.json()
            setResponse(data)
        } catch (err) {
            setResponse({ error: 'Failed to connect to backend API' })
        }

        setLoading(false)
    }

    return (
        <div className="relative min-h-screen flex flex-col items-center justify-center text-center overflow-hidden bg-gradient-to-br from-[#fce9eb] to-[#fef7f8]">
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
            <div className="bg-white rounded-2xl shadow-2xl max-w-3xl w-full p-10 md:p-16 relative z-10">
                <h1 className="text-3xl font-extrabold text-[#f05a66] mb-8 text-center">
                    Automated Meeting Scheduler
                </h1>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-gray-700 font-semibold mb-2">
                            Attendee Emails
                        </label>

                        {emails.map((email, index) => (
                            <div key={index} className="flex items-center gap-3 mb-3">
                                <input
                                    type="email"
                                    className="flex-1 rounded-lg border border-gray-300 px-4 py-2 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#f05a66] focus:border-transparent transition"
                                    value={email}
                                    onChange={(e) => {
                                        const newEmails = [...emails]
                                        newEmails[index] = e.target.value
                                        setEmails(newEmails)
                                    }}
                                    required
                                    placeholder={`user${index + 1}@example.com`}
                                />
                                <button
                                    type="button"
                                    onClick={() => {
                                        const newEmails = emails.filter((_, i) => i !== index)
                                        setEmails(newEmails)
                                    }}
                                    className="text-red-500 hover:text-red-700"
                                    title="Remove"
                                >
                                    🗑️
                                </button>
                            </div>
                        ))}

                        <button
                            type="button"
                            onClick={() => setEmails([...emails, ''])}
                            className="text-[#f05a66] font-semibold hover:text-[#e24c58] transition mt-1"
                        >
                            + Add another email
                        </button>
                    </div>


                    <fieldset className="flex gap-8 justify-center">
                        <legend className="sr-only">Select Scheduling Mode</legend>
                        <label className="flex items-center gap-3 cursor-pointer text-gray-700 font-medium">
                            <input
                                type="radio"
                                name="mode"
                                value="group"
                                checked={mode === 'group'}
                                onChange={() => setMode('group')}
                                className="accent-[#f05a66] w-5 h-5"
                            />
                            Group Meeting
                        </label>

                        <label className="flex items-center gap-3 cursor-pointer text-gray-700 font-medium">
                            <input
                                type="radio"
                                name="mode"
                                value="individual"
                                checked={mode === 'individual'}
                                onChange={() => setMode('individual')}
                                className="accent-[#f05a66] w-5 h-5"
                            />
                            Individual Meetings
                        </label>
                    </fieldset>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-[#f05a66] text-white font-semibold py-3 rounded-xl shadow-md hover:bg-[#e24c58] transition disabled:opacity-60 disabled:cursor-not-allowed"
                    >
                        {loading ? 'Scheduling...' : 'Schedule Meeting'}
                    </button>
                </form>

                {response && (
                    <div className="mt-10 p-6 bg-[#fef7f8] border border-[#f05a66] rounded-lg text-center max-h-80 overflow-auto">
                        {response.error ? (
                            <p className="text-red-600 font-semibold">{response.error}</p>
                        ) : (
                            <>
                                <p className="text-green-700 font-bold mb-4 text-lg">
                                    Meeting Scheduled Successfully!
                                </p>
                                <ul className="list-disc list-inside text-[#2c5282] break-all space-y-1 max-h-48 overflow-y-auto">
                                    {(Array.isArray(response) ? response : [response]).map((item, i) => (
                                        <li key={i}>
                                            {item.meetLink || item.htmlLink ? (
                                                <a
                                                    href={item.meetLink || item.htmlLink}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    className="underline hover:text-[#f05a66]"
                                                >
                                                    {item.meetLink || item.htmlLink}
                                                </a>
                                            ) : item.status ? (
                                                <span className="text-gray-700 font-medium">
                                                    {item.email}: {item.status}
                                                </span>
                                            ) : (
                                                <span className="text-gray-500 italic">No meeting information available.</span>
                                            )}
                                        </li>
                                    ))}
                                </ul>

                            </>
                        )}
                    </div>
                )}
            </div>
        </div>
    )
}
