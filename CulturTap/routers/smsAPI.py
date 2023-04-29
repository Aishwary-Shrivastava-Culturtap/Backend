from .. import *
from ..classes.SNS import SNS
from ..models.sms import messageModel, OTPmodel
from ..admin.credentials import SECRET_KEY, KEY_ID, TOKEN

router = APIRouter(prefix='/sms', tags=['SMS'])

# --SMS

client = SNS(access_key=KEY_ID, secret_key=SECRET_KEY)


@router.post('/msg', status_code=status.HTTP_201_CREATED)
def send_sms(params: messageModel, token: str):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        params = params.dict()
        params['phoneNo'] = params['countryCode']+str(params['phoneNo'])
        return client.send_sms(to=params['phoneNo'], body=params['msg'])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/otp/{phoneNo}', status_code=status.HTTP_201_CREATED, response_model=OTPmodel)
def send_OTP(phoneNo: str, token: str):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        return client.send_otp(to=phoneNo, org='CulturTap')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
