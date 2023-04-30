from .. import *
from ..classes.database import database
from ..models.expert_card import expertCard
from ..admin.credentials import DB_URL, DB_HEADERS, TOKEN

router = APIRouter(prefix='/user/expertCard', tags=['Expert Cards'])

# --USER DATA

client = database.expertCard(url=DB_URL, header=DB_HEADERS)


@router.get("/get/{uid}", status_code=status.HTTP_200_OK, response_model=expertCard)
def get_data_by_uid(uid: int, token: str):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        return client.show(uid=uid)[0]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/get", status_code=status.HTTP_200_OK, response_model=list[expertCard])
def get_data_by_matching(params: dict, token: str):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        return client.show(**params)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/update/{uid}", status_code=status.HTTP_200_OK)
def update_by_matching(uid: int):
    try:
        toUpdate = {}
        expertCard = client.show(uid=uid)[0]
        reviews = database.Reviews(DB_URL, DB_HEADERS).show(review_to=uid)
        try:
            reviewsDf = pd.DataFrame(reviews)
            totalReviews = len(reviewsDf['ratings'])*5
            totalReviewsCount = reviewsDf['ratings'].sum()
            rating = (totalReviewsCount/totalReviews)*5
            toUpdate['rating'] = rating
            if rating < 2:
                toUpdate['status'] = 'Good'
            elif rating <= 3:
                toUpdate['status'] = 'Great'
            elif rating <= 4:
                toUpdate['status'] = 'Appreciative'
            else:
                toUpdate['status'] = 'Outstanding'
        except:
            toUpdate['rating'] = 0.0
            toUpdate['status'] = 'Good'

        videoData = database.Videos(DB_URL, DB_HEADERS)
        videos = videoData.show(uid=uid)
        toUpdate['coveredPlace'] = len(videos)
        value = expertCard.get('expertLocation')
        toUpdate['visitedPlace'] = len(value.split(','))
        return client.update(uid=uid, **toUpdate)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
