from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import datetime

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_calendar_service():
    """    
        Authenticates user with google, thene exports calendar service
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_calendar(service, calendar):
    today = datetime.datetime.now().strftime('%Y-%m-%dT00:00:00-04:00')# '-04:00' indicates timezone
    
    print('Getting the upcoming 15 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=today, maxResults=15, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    for event in events:
        strStart = event['start'].get('dateTime')
        strEnd = event['end'].get('dateTime')

        if strStart and strEnd:
            start = datetime.datetime.strptime(strStart[:19], '%Y-%m-%dT%H:%M:%S')
            end = datetime.datetime.strptime(strEnd[:19], '%Y-%m-%dT%H:%M:%S')

            if start.day == datetime.datetime.now().day:
                
                name = event['summary']

                try:
                    description = event['description']
                except:
                    description = 'No Description Available'

                try:
                    location = event['location']
                except:
                    location= 'No Location Available'

                calendar.append({'name':name,
                                'start':start,
                                'end':end,
                                'description':description,
                                'location' : location})

"""
USAGE:

calendar = []
service = get_calendar_service()
get_calendar(service, calendar)
print(calendar)

"""
