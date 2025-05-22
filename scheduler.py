import datetime
import os
import pickle
import time
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes to access calendar and create meet links
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Replace this with your list of attendee emails
ATTENDEES_LIST = [
    'user1@example.com',
    'user2@example.com',
    'user3@example.com',
    'aminah30akhtar3a@gmail.com',
    # Add up to 100 emails here
]

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

def is_time_slot_free(service, start_time_utc, end_time_utc):
    events_result = service.freebusy().query(body={
        "timeMin": start_time_utc.isoformat() + 'Z',
        "timeMax": end_time_utc.isoformat() + 'Z',
        "timeZone": "UTC",
        "items": [{"id": "primary"}]
    }).execute()

    busy_times = events_result['calendars']['primary']['busy']
    return len(busy_times) == 0

# def schedule_event(service, start_time, end_time, attendee_email):
def schedule_event(service, start_time, end_time):
    event = {
        'summary': 'Auto Scheduled Meeting',
        'description': 'This is an automated meeting with a Google Meet link.',
        'start': {
            'dateTime': start_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'attendees': [
            {'email': 'aminah30akhtar3a@gmail.com'}  
            # {'email': attendee_email}
        ],
        'conferenceData': {
            'createRequest': {
                'requestId': 'meet-' + datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        },
    }

    event_result = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1,
        sendUpdates='all' 
    ).execute()

    print("Event Created:")
    # print(f"Event Created for {attendee_email}:")
    print("Summary:", event_result['summary'])
    print("Link:", event_result['htmlLink'])
    print("Meet Link:", event_result['conferenceData']['entryPoints'][0]['uri'])

def find_and_schedule():
    service = get_calendar_service()

    # Tomorrow's date
    tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)

    # Working hours (UTC)
    start_hour = 9
    end_hour = 17
    meeting_duration = datetime.timedelta(minutes=30)

    for hour in range(start_hour, end_hour):
        start_time = tomorrow.replace(hour=hour)
        end_time = start_time + meeting_duration

        if is_time_slot_free(service, start_time, end_time):
            schedule_event(service, start_time, end_time)
            return

    print("No available time slot found for tomorrow between 9 AM and 5 PM UTC.")

    # current_hour = start_hour

    # for attendee in ATTENDEES_LIST:
    #     while current_hour < end_hour:
    #         start_time = tomorrow.replace(hour=current_hour)
    #         end_time = start_time + meeting_duration

    #         if is_time_slot_free(service, start_time, end_time):
    #             schedule_event(service, start_time, end_time, attendee)
    #             current_hour += 1
    #             time.sleep(1)  # Avoid hitting API quota limits
    #             break
    #         else:
    #             current_hour += 1
    #     else:
    #         print(f"No available slot found for {attendee}.")

def schedule_group_event(service, start_time, end_time, attendee_emails):
    event = {
        'summary': 'Group Auto Scheduled Meeting',
        'description': 'Automated meeting with multiple attendees and a single Google Meet link.',
        'start': {
            'dateTime': start_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'attendees': [{'email': email} for email in attendee_emails],
        'conferenceData': {
            'createRequest': {
                'requestId': 'group-meet-' + datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        },
    }

    event_result = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1,
        sendUpdates='all' 
    ).execute()

    print("Group Event Created:")
    print("Summary:", event_result['summary'])
    print("Event Link:", event_result['htmlLink'])
    print("Meet Link:", event_result['conferenceData']['entryPoints'][0]['uri'])

def find_and_schedule_group():
    service = get_calendar_service()

    tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)

    start_hour = 9
    end_hour = 17
    meeting_duration = datetime.timedelta(minutes=60)  # Adjust duration as needed

    for hour in range(start_hour, end_hour):
        start_time = tomorrow.replace(hour=hour)
        end_time = start_time + meeting_duration

        if is_time_slot_free(service, start_time, end_time):
            schedule_group_event(service, start_time, end_time, ATTENDEES_LIST)
            return

    print("No common slot found for all attendees.")

if __name__ == '__main__':
    # find_and_schedule()
    # # Sending one meet link to multiple attendees
    find_and_schedule_group()

