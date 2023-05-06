from .. import *
from ..utils import address_finder_full, lat_long_difference

router = APIRouter(tags=['Location'])

@router.get("/location", status_code=status.HTTP_200_OK,)
def get_data(lat: str,long:str):
    try:
        return address_finder_full(lat,long)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
@router.get("/compare-location", status_code=status.HTTP_200_OK,)
def get_data(lat1: float,long1:float,lat2:float,long2:float):
    try:
        result={"value":True} if lat_long_difference((lat1,long1),(lat2,long2)) <=1 else {"value":False}
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)