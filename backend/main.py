from fastapi import FastAPI
from scheduler.scheduler import schedule_individual_meetings, schedule_group_meeting
from scheduler.models import AttendeesRequest
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Automated Meeting Scheduler")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/schedule/individual")
async def schedule_individual(attendees: AttendeesRequest):
    return schedule_individual_meetings(attendees.emails)

@app.post("/schedule/group")
async def schedule_group(attendees: AttendeesRequest):
    return schedule_group_meeting(attendees.emails)
