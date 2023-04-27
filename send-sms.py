from model import connect_to_db
from twilio.rest import Client
import os

ACCOUNT_SID = os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
TWIILIO_NUM = os.environ['TWIILIO_NUM']
MY_NUM = os.environ['MY_NUM']

# crontab_command = '* * * * * /Users/pam/src/capstone-project/env/bin/python3 /Users/pam/src/capstone-project/send-sms.py'


client = Client(ACCOUNT_SID, AUTH_TOKEN)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_=TWIILIO_NUM,
                     to=MY_NUM
                 )

print(message.sid)


########################################################
# if __name__ == "__main__":
#     from server import app
#     connect_to_db(app)