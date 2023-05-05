from .. import *
from ..utils import address_finder_full
router = APIRouter(tags=['Location'])
@router.get("/location", status_code=status.HTTP_200_OK,)
def get_data(lat: str,long:str):
    try:
        return address_finder_full(lat,long)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)