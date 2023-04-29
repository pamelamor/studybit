from model import connect_to_db
from twilio.rest import Client
import os
import crud
from server import app
connect_to_db(app)


ACCOUNT_SID = os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
TWIILIO_NUM = os.environ['TWIILIO_NUM']
# MY_NUM = os.environ['MY_NUM']

# crontab_command = '0 10 * * * /Users/pam/src/capstone-project/env/bin/python3 /Users/pam/src/capstone-project/send-sms.py'
users = crud.get_all_users()

for user in users:
    if user.user_phone_num != None:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        message = client.messages \
                        .create(
                            body="You promised yourself a review! Let's do this!😤",
                            from_=TWIILIO_NUM,
                            to="+1" + user.user_phone_num
                        )

        print(message.sid)