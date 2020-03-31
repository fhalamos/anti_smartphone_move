#Reference https://www.twilio.com/docs/sms/quickstart/python#receive-and-reply-to-inbound-sms-messages-with-python

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

import calendar_requester

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming messages with a SMS according to the request sent (day for which event are retrieve)"""

    message_body = request.form['Body']

    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message(calendar_requester.get_events(message_body))
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
