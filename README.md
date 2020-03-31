# The problem

I love and hate my smartphone. But ultimately, I dont like it. I just spent too much time looking at it - time I could spend interacting with people in real life, or doing more interesting stuff like reading a book or looking at the sky.

I tried lots of things to reduce my exposure to my app - like other apps that dishable whatsapp, self enforce rules, etc -  but nothing really worked.

So, ultimately, I just bought a [**great** cheap old school phone](https://www.amazon.com/Ushining-Feature-Unlocked-Mobile-Carrier/dp/B07VRLBZ1M), and decided to turn my smartphone off. I still turn it on (and immmediately off) every night for say 20 min to check importat whatsapps from back home, but nothing more.

Can you really survive without a smartphone? Yes.

For whatsapp? Use text messages, or better, call people. And avoid tons of useless texting.

For google maps? Go into a computer and look at g maps there.

For slack, email, etc etc? Use the computer. And no, you dont need to be checking your email every 5 min.

**Now, the only thing I do need to frequently check in my phone is my calendar for the day/following day.**

# Solution

This little system allows the user to send requests to a twilio phone number - through text messages - to receiv the google calendar events of the day or the following day.

# Use

Text your twilio phone number any random message to receive a list of the remaining events of the day. Text $tomorrow_keyword to receive list of events for tomorrow.

# System overview

When someone sends a SMS to the Twilio phone number, Twilio will make an HTTP request to a server asking for instructions on what to do next. The server will be a very lightweight flask web application (receive_sms_api.py) that can accept incoming requests and process them. The web app will use the G Calendar API to process the request (calendar_requester.py).


# Setup

## Requirements

* Install python3

* Install requirements.txt 
`pip3 install -r requirements.txt`

## Files/env variables needed

* Need calendar_credentials.json in this directory, used to access g calendar API. Check Step 1 [here](https://developers.google.com/calendar/quickstart/python)

* Declare environmental variables

` export TWILIO_ACCOUNT_SID=account_sid`

` export TWILIO_AUTH_TOKEN=auth_token`
Get them from twilio.com/user/account

` export TWILIO_PHONE_NUMBER=your_twilio_phone_number`
<!-- ` export TWILIO_PHONE_NUMBER=+16672399039` -->

* Adapt config.yaml file to whatever you want your 'tomorrow' keyword to be

## Get the system running

* Log into a aws server

`ssh -i your_aws_keypair.pem ubuntu@public_dns`
<!-- `ssh -i aws_keypair.pem ubuntu@ec2-54-165-154-230.compute-1.amazonaws.com` -->

* To keep the web app and the Twilio listener alive after closing the console, use *screen*

* Set the web app running

`python3 receive_sms_api.py`

* Configure your Twilio phone number to call a webhook URL whenever a new message comes in:

`twilio phone-numbers:update "$TWILIO_PHONE_NUMBER" --sms-url="http://localhost:5000/sms"`

Thats all!


# References

My main guidelines where:

* https://www.twilio.com/docs/sms/quickstart/python#receive-and-reply-to-inbound-sms-messages-with-python, to learn about twilio configurations
* https://developers.google.com/people/quickstart/python, to learn about google calendar API
