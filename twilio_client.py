import os
from twilio.rest import Client

class TwilioClient:
    def __init__(self):
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.__client = Client(account_sid, auth_token)
        self.__from_number = '+18668730605'

    def send_message(self, to_number: str, message: str):
        message = self.__client.messages.create(
            body=message,
            from_=self.__from_number,
            to=to_number
        )