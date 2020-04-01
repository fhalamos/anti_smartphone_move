#Reference https://www.twilio.com/docs/sms/quickstart/python#receive-and-reply-to-inbound-sms-messages-with-python

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

import calendar_requester
import weather_requester
import email_requester
import yaml

app = Flask(__name__)

config = yaml.load(open('config.yaml', 'r'), Loader=yaml.SafeLoader)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming messages with a SMS according to the request sent (day for which event are retrieve)"""

    message_body = request.form['Body']

    # Start our response
    resp = MessagingResponse()

    # Add a message
    if(message_body=='' or message_body==config['todays_events_keyword'] or message_body==config['tomorrows_events_keyword']):
      resp.message(calendar_requester.get_events(message_body))
    elif(message_body==config['weather_keyword']):
      resp.message(weather_requester.get_weather())
    elif(message_body[0]==config['email_keyword']):
      email_sent = email_requester.send_email(message_body[2:])
      if(email_sent):
        return ('', 204) #Do nothing, I dont want a confirmation sms
      else:
        resp.message("Error occurr when sending email")
    else:
      resp.message('Wrong request keyword')
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
