import datetime
import time
from .calender_utils import get_calendar_service, is_time_slot_free

def create_event(service, start_time, end_time, attendees, request_id):
    event = {
        'summary': 'Automated Scheduled Meeting',
        'description': 'Meeting scheduled automatically with Google Meet link.',
        'start': {
            'dateTime': start_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'attendees': [{'email': email} for email in attendees],
        'conferenceData': {
            'createRequest': {
                'requestId': request_id,
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        },
    }

    return service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1,
        sendUpdates='all'
    ).execute()

def schedule_individual_meetings(attendee_emails):
    service = get_calendar_service()
    tomorrow = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
    start_hour, end_hour = 9, 17
    duration = datetime.timedelta(minutes=30)
    results = []

    for email in attendee_emails:
        for hour in range(start_hour, end_hour):
            start = tomorrow.replace(hour=hour)
            end = start + duration

            if is_time_slot_free(service, start, end):
                request_id = f"meet-{email.split('@')[0]}-{hour}"
                event = create_event(service, start, end, [email], request_id)
                results.append({
                    "email": email,
                    "summary": event['summary'],
                    "htmlLink": event['htmlLink'],
                    "meetLink": event['conferenceData']['entryPoints'][0]['uri']
                })
                time.sleep(1)
                break
        else:
            results.append({"email": email, "status": "No slot found"})

    # print("individual results:", results)
    return results

def schedule_group_meeting(attendee_emails):
    service = get_calendar_service()
    tomorrow = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
    start_hour, end_hour = 9, 17
    duration = datetime.timedelta(minutes=60)

    for hour in range(start_hour, end_hour):
        start = tomorrow.replace(hour=hour)
        end = start + duration

        if is_time_slot_free(service, start, end):
            request_id = f"group-meet-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            event = create_event(service, start, end, attendee_emails, request_id)
            # print("group results:", event)
            return {
                "summary": event['summary'],
                "htmlLink": event['htmlLink'],
                "meetLink": event['conferenceData']['entryPoints'][0]['uri'],
                "attendees": attendee_emails
            }
    return {"status": "No available slot found for group meeting"}
