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
    if os.path.exists('calendar.token.pickle'):
        with open('calendar.token.pickle', 'rb') as token:
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
        with open('calendar.token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)


    now = datetime.datetime.utcnow().isoformat() + 'Z'

    today = datetime.datetime.utcnow().date()

    tomorrow = (today + datetime.timedelta(days=1))

    tomorrow_morning = (datetime.datetime.combine(tomorrow, datetime.datetime.min.time())+ \
        datetime.timedelta(hours=5)).isoformat() + 'Z' # 'Z' indicates UTC time. #+ datetime.timedelta(hours=5)

    tomorrow_midnight = (datetime.datetime.combine(tomorrow, datetime.datetime.max.time()) + \
        datetime.timedelta(hours=5)).isoformat() + 'Z'


    #Bug here. The thing is, if current time in Z time corresponds to one day later than local time, then midnight computed will be of the following day
    #Ex, if local time is 1 pm, Z time is 6 pm, midgnight will be 11:39 pm, all good.
    #But, if local time is 10 pm, Z time will be 4 am of following day, hence midnight will be 11:39 pm of the following day
    local_midnight = (datetime.datetime.combine(today, datetime.datetime.max.time()) + \
        datetime.timedelta(hours=5)).isoformat() + 'Z'



    # Default is call for current day events
    if(day==config['tomorrows_events_keyword']):
        start_time = tomorrow_morning
        end_time = tomorrow_midnight

    else:
        start_time = now
        end_time = local_midnight


    calendars_ids = config['calendars_ids']

    all_events_captured = []
    
    for c_id in calendars_ids:
        # Call the Calendar API    
        events_list = service.events().list(calendarId=c_id, timeMin=now, timeMax=local_midnight,
            maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        all_events_captured.extend(events_list.get('items', []))


    if not all_events_captured:
        return 'No upcoming events found.'

    events_print=[]

    for event in sorted(all_events_captured, key = lambda i: i['start']['dateTime']):
 
        raw_start = event['start']['dateTime']
        start = raw_start.split("T")[1].split("-")[0][:-3]
 
        event_print = start+ ":"+ event['summary']
 
        if('location' in event):
            event_print+=", "+event['location']

        events_print.append(event_print)

    return "\n".join(events_print)


if __name__ == '__main__':
    print(get_events('tdy'))#'tmr'
