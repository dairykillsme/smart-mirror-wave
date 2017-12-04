from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_calendar(credentials, calendar):
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    today = datetime.datetime.now().strftime('%Y-%m-%dT00:00:00-04:00')# '-04:00' indicates timezone
    
    print('Getting the upcoming 15 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=today, maxResults=15, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    for event in range(0, len(events) - 1):
        start = datetime.datetime.strptime(events[event]['start']['dateTime'][:19], '%Y-%m-%dT%H:%M:%S')
        end = datetime.datetime.strptime(events[event]['end']['dateTime'][:19], '%Y-%m-%dT%H:%M:%S')

        if start.day == datetime.datetime.now().day:
            
            name = events[event]['summary']

            try:
                description = events[event]['description']
            except:
                description = 'No Description Available'

            try:
                location = events[event]['location']
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
credentials = get_credentials()
get_calendar(credentials, calendar)
print(calendar)
"""
