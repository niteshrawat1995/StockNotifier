from typing import Union
import pyotp
import base64

from backend.twilio import Communication


class TOTPBackend:
    def __init__(self, phone_number: str, digits: int = 6, interval: int = 120) -> None:
        self.phone_number = phone_number
        self.digits = digits
        self.interval = interval
        user_hash = base64.b32encode(self.phone_number.encode("utf-8")).decode("utf-8")
        self.totp = pyotp.TOTP(s=user_hash, digits=self.digits, interval=self.interval)

    def generate_otp(self) -> str:
        otp = self.totp.now()
        return otp

    def verify_otp(self, otp: str) -> bool:
        return self.totp.verify(otp)

    def send_otp(self, communication: Communication) -> Union[bool, str]:
        otp = self.generate_otp()
        msg = f"Your OTP is {otp} and is valid till {self.interval} seconds"
        communication.send(to=self.phone_number, msg=msg)
        return True, otp
