from ..models.users import followList
from ..classes.database import database
from ..admin.credentials import DB_URL, DB_HEADERS, TOKEN
from .. import*

client = database.connections(DB_URL,DB_HEADERS)
router = APIRouter(prefix='/user/follow', tags=['Follow list'])


@router.get('/get',status_code=status.HTTP_200_OK,response_model=list[followList])
def get_by_matching(params:dict,token:str,end:int,start:int=0):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        return client.show(**params)[start:end]
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)

@router.post('/add', status_code=status.HTTP_200_OK)
def adding_followers(params: followList, token: str):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    params = params.dict()
    try:
        user=database.Users(DB_URL,DB_HEADERS)
        u1 = user.show(uid=params["followed_by"])
        u2 = user.show(uid=params["followed_to"])
        user.update(uid=params["followed_by"],**{'followings':u1['followings']+1})
        user.update(uid=params["followed_to"],**{'followers':u2['followers']+1})
        return client.add(**params)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)
    
@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def remove_follower_by_matching(_id:str):
    params=get_by_matching({'_id':ObjectId(_id)},TOKEN,5)[-1]
    user=database.Users(DB_URL,DB_HEADERS)
    u1 = user.show(uid=params["followed_by"])
    u2 = user.show(uid=params["followed_to"])
    user.update(uid=params["followed_by"],**{'followings':u1['followings']-1})
    user.update(uid=params["followed_to"],**{'followers':u2['followers']-1})
    client.delete(_id=ObjectId(_id))
    return {'msg':'done'}