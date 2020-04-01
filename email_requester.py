#References:
#https://developers.google.com/gmail/api/quickstart/python
#https://developers.google.com/gmail/api/guides/sending

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import yaml
from email.mime.text import MIMEText
import base64
import sys

config = yaml.load(open('config.yaml', 'r'), Loader=yaml.SafeLoader)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def create_email(message_text):  
  #With message in the subject

  message = MIMEText("")#better choose empty content
  message['to'] = config['email_to']
  message['subject'] = message_text

# Returned in messages.get and drafts.get responses when the format=RAW parameter is supplied.
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('gmail.token.pickle'):
        with open('gmail.token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'gmail_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('gmail.token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service

def send_email(message_text):
  service = get_gmail_service()

  email = create_email(message_text)

  try:
    message = (service.users().messages().send(userId="me", body=email).execute())
    return True
  except:
    print ('An error occurred: %s' % sys.exc_info())
    return False

if __name__ == '__main__':
  send_email("hola")
