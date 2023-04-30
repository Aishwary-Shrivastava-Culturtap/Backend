from . import *
from .admin.credentials import APP_ID, APP_CERTIFICATE, DB_URL, DB_HEADERS
from .routers import userAPI, smsAPI, videoAPI, expertAPI, callAPI, plannerAPI, guideAPI, assistanceAPI, paytmGateway, viewsAPI, followAPI, reviewAPI
from .chat.sockets import appIO
from .classes.database import database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', tags=['Home'])
async def greetings():
    return {'msg': "Welcome to Culturtap.com"}


@app.get('/agora/{channel}', tags=['Agora API'])
async def agora_token(channel: str, uid: int, role: int):
    return {'token': RtcTokenBuilder.buildTokenWithUid(
        APP_ID, APP_CERTIFICATE, channel, uid, role, time.time()+21)}


@app.post('/logs/{types}', tags=['Logs'])
async def get_Logs(types: str, params: dict = {}):
    history = database.History(DB_URL, DB_HEADERS)
    if types.lower() == 'chat':
        return database.Chat(DB_URL, DB_HEADERS).show(**params)
    elif types.lower() == 'call':
        return database.Calls(DB_URL, DB_URL).show(**params)
    elif types.lower() == 'video':
        params.update({'type': types})
        return history.show(**params)


# Routers
app.mount('/chat', app=appIO)
app.mount('/payment-gateway', app=paytmGateway.router)
app.include_router(userAPI.router)
app.include_router(viewsAPI.router)
app.include_router(followAPI.router)
app.include_router(reviewAPI.router)
app.include_router(plannerAPI.router)
app.include_router(assistanceAPI.router)
app.include_router(guideAPI.router)
app.include_router(expertAPI.router)
app.include_router(videoAPI.router)
app.include_router(smsAPI.router)
app.include_router(callAPI.router)
