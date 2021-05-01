from twilio.rest import Client

account_sid = "AC88280bf2b4d41a23b63027a0be3a9b91"
auth_token = "98ed9bb9e01fda7eb55afc28b3ed9d7e"
my_twilio_number = "+13146666885"

class Twilio:
    def __init__(self):
        self.client = Client(account_sid, auth_token)

    def send(self, to, msg):
        message = (
            self.client.messages
            .create(
                body=msg,
                from_=my_twilio_number,
                to=f'+91{to}'
            )
        )
        print(message.sid)
