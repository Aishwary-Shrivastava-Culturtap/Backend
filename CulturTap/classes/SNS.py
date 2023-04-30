from .. import *

# Managing SMS


class SNS:
    id = None
    token = None

    def __init__(self, access_key: str, secret_key: str) -> None:
        import boto3
        self.access_key = access_key
        self.secret_key = secret_key
        self.client = boto3.client('sns', aws_access_key_id=self.access_key,
                                   aws_secret_access_key=self.secret_key, region_name='ap-south-1')

    def send_otp(self, to: str, org: str):
        self.to = to
        self.org = org
        self.otp = random.randint(1111, 9999)
        body = f"Hey,\nhere is your one-time password to login : {self.otp}\n- {self.org}"
        self.response = self.client.publish(
            PhoneNumber=self.to,
            Message=body,
            Subject='Verification code',
        )
        return {"status": "SENT", "code": self.otp}

    def send_sms(self, to: str, body: str):
        body += '\n- CulturTap'
        self.response = self.client.publish(
            PhoneNumber=to,
            Message=body,
            Subject='Culturtap',
        )
        return {"status": "SENT"}
