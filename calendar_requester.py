#Reference: https://developers.google.com/people/quickstart/python

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import yaml

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

config = yaml.load(open('config.yaml', 'r'), Loader=yaml.SafeLoader)

def get_events(day):

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
                'calendar_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)


    today = datetime.datetime.utcnow().date()


    # Call the Calendar API
    # Default is call for current day events
    if(day==config['tomorrow_keyworkd']):

        tomorrow = (today + datetime.timedelta(days=1))

        tomorrow_morning = datetime.datetime.combine(tomorrow, datetime.datetime.min.time()).isoformat() + 'Z' # 'Z' indicates UTC time. #+ datetime.timedelta(hours=5)

        tomorrow_midnight = datetime.datetime.combine(tomorrow, datetime.datetime.max.time()).isoformat() + 'Z'

        events_list = service.events().list(calendarId='primary', timeMin=tomorrow_morning, timeMax=tomorrow_midnight,
                                    maxResults=10, singleEvents=True,
                                    orderBy='startTime').execute()
    else:

        now = datetime.datetime.utcnow().isoformat() + 'Z'
         
        midnight = (datetime.datetime.combine(today, datetime.datetime.max.time()) + \
            datetime.timedelta(hours=5)).isoformat() + 'Z'

        events_list = service.events().list(calendarId='primary', timeMin=now, timeMax=midnight,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()

    events = events_list.get('items', [])

    if not events:
        return 'No upcoming events found.'

    events_print=[]       
    for event in events:
 
        raw_start = event['start']['dateTime']
        start = raw_start.split("T")[1].split("-")[0][:-3]
 
        event_print = start+ ":"+ event['summary']
 
        if('location' in event):
            event_print+=", "+event['location']

        events_print.append(event_print)

    return "\n".join(events_print)


if __name__ == '__main__':
    print(get_events(''))#'tmr'
