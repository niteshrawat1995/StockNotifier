import os
from abc import ABC, abstractmethod

from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")


class Communication(ABC):
    @abstractmethod
    def send(self, to, msg):
        pass


class Twilio(Communication):
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send(self, to, msg):
        message = self.client.messages.create(
            body=msg, from_=TWILIO_NUMBER, to=f"+91{to}"
        )
        print(message.sid)


class Console(Communication):
    def send(self, to, msg):
        print(f"Message {msg} | To {to}")
