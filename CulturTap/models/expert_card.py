from .. import *


class expertCard(BaseModel):
    uid: int
    expertLocation: str = None  # Expert in location
    visitedPlace: int = 0  # len(expertLocation)
    coveredPlace: int = 0  # Cover places in particular location
    rating: float = 0
    status: str = None
