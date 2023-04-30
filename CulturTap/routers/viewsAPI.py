from .. import *
from ..classes.database import database
from ..admin.credentials import DB_URL, DB_HEADERS, TOKEN

router = APIRouter(prefix='/views', tags=['Views'])

# --USER DATA

client = database.views(url=DB_URL, header=DB_HEADERS)


@router.post('/seen/{uid}')
def videoSeen(uid: int, videoId: int):
    client.add(uid=uid, videoId=videoId)
    return {'msg': "seen"}
