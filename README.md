# The problem

I love and hate my smartphone. But ultimately, I don't like it. I just spent too much time looking at it - time I could spend interacting with people in real life, or doing more interesting stuff like reading a book or looking at the sky.

I tried lots of things to reduce my exposure to my smartphone - like other apps that disable whatsapp, self enforce rules, etc -  but nothing really worked.

So, ultimately, I just bought a [**great** cheap old school phone](https://www.amazon.com/Ushining-Feature-Unlocked-Mobile-Carrier/dp/B07VRLBZ1M), and decided to turn my smartphone off. I still turn it on (and immediately off) every night for say 20 min to check whatsapps from back home, but nothing more.

I figure out I really dont need the smartphone. I don't need to be checking email, slack and news all the time - I can do that on the computer. For google maps I just check my routes in advance on the computer. For uber, I can always call a taxi, etc.

*The only thing I do need to frequently check in my phone is my calendar for the day/following day.* At least my calendar is something I continuously need to check, and I don't want to turn my computer on for that.

Extension: I figured out checking the weather was also useful, so included that too..

Extension 2: Now I can send auto-emails (which I love for reminders) from the phone too :D. Yeah I know, kind of transforming the simple phone to a proxy for the smartphone now :D.

![](ladrillo.png=182x102)

# Solution

This little system allows the user to send requests to a twilio phone number - through text messages (sms) - to receive the google calendar events of the day or the following day.

# Use

Text your twilio phone number to receive a list of events from google calendar. Use the specific keywords defined in config.yaml to receive events of the current day, next day (or weather!).

# System overview

When someone sends a SMS to the Twilio phone number, Twilio will make an HTTP request to a server asking for instructions on what to do next. The server will be a very lightweight flask web application (receive_sms_api.py) that can accept incoming requests and process them. The web app will use the G Calendar API for calendar requests(calendar_requester.py), or the OpenWeatherAPI for weather requests (weather_requester.py). Once Twilio receives the response from the server, it will send the SMS to the phone number that sent the request.


# Setup

## Requirements

* Install python3

* Install requirements.txt 
`pip3 install -r requirements.txt`

## Files/env variables needed

* Need calendar_credentials.json in this directory, used to access g calendar API. Check Step 1 [here](https://developers.google.com/calendar/quickstart/python)

* Same for gmail_credentials.json. Check Step 1 [here](https://developers.google.com/gmail/api/quickstart/python)

* Declare environmental variables

` export TWILIO_ACCOUNT_SID=account_sid`

` export TWILIO_AUTH_TOKEN=auth_token`
Get them from twilio.com/user/account

`export OPENWEATHER_API_KEY=your_openweather_api_key`

` export TWILIO_PHONE_NUMBER=your_twilio_phone_number`
<!-- ` export TWILIO_PHONE_NUMBER=+16672399039` -->

* Adapt config.yaml file to whatever you want your  keywords to be

## Get the system running

* Log into a aws server

`ssh -i your_aws_keypair.pem ubuntu@public_dns`
<!-- `ssh -i aws_keypair.pem ubuntu@ec2-54-165-154-230.compute-1.amazonaws.com` -->

* To keep the web app and the Twilio listener alive after closing the console, use *screen*

* Set the web app running

`python3 receive_sms_api.py`

* Create and config an ngrok acount here: https://dashboard.ngrok.com/get-started, so as to create a  tunnel that do not expire (used for pointing to the webhook) - next step.

* Configure your Twilio phone number to call a webhook URL whenever a new message comes in:

`twilio phone-numbers:update "$TWILIO_PHONE_NUMBER" --sms-url="http://localhost:5000/sms"`

Thats all!


# References

My main guidelines where:

* https://www.twilio.com/docs/sms/quickstart/python#receive-and-reply-to-inbound-sms-messages-with-python, to learn about twilio configurations
* https://developers.google.com/people/quickstart/python, to learn about google calendar API
