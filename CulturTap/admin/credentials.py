from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    DB_API: str
    KEY_ID: str
    SECRET_KEY: str
    AWS_ACCOUNT:str
    MID: str
    KEY: str
    CLIENT_ID: str
    WEBSITE: str
    CALLBACK_URL: str
    ENVIRONMENT: str
    APP_ID: str
    APP_CERTIFICATE: str
    TOKEN: str
    KM : float

    class Config:
        env_file = r"CulturTap\admin\.env"


settings = Settings()

TOKEN = settings.TOKEN
KM = settings.KM

# Database
DB_URL = settings.DB_URL
DB_HEADERS = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': settings.DB_API,
}


# AWS S3
KEY_ID = settings.KEY_ID
SECRET_KEY = settings.SECRET_KEY
AWS_ACCOUNT = settings.AWS_ACCOUNT

# Paytm
MID = settings.MID
KEY = settings.KEY
CLIENT_ID = settings.CLIENT_ID
WEBSITE = settings.WEBSITE
CALLBACK_URL = settings.CALLBACK_URL
ENVIRONMENT = settings.ENVIRONMENT
# For Production
# CALLBACK_URL = https://securegw.paytm.in/theia/paytmCallback
# environment = LibraryConstants.PRODUCTION_ENVIRONMENT

# Agora
APP_ID = settings.APP_ID
APP_CERTIFICATE = settings.APP_CERTIFICATE
