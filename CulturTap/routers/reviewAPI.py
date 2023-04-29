from ..models.review import reviewModel
from ..classes.database import database
from ..admin.credentials import DB_URL, DB_HEADERS
from .. import*

client = database.Reviews(DB_URL,DB_HEADERS)
router = APIRouter(prefix='/user/review', tags=['Reviews'])

@router.get('/get',status_code=status.HTTP_200_OK,response_model=list[reviewModel])
def get_by_matching(params:dict,end:int,start:int=0):
    try:
        return client.show(**params)[start:end]
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)

@router.post('/add', status_code=status.HTTP_200_OK)
def adding_review(params: reviewModel):
    params = params.dict()
    try:
        return client.add(**params)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)
    

@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def remove_follower_by_matching(_id:str):
    client.delete(_id=ObjectId(_id))
    return {'msg':'done'}