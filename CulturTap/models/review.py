from .. import *


class reviewModel(BaseModel):
    review_by:int
    review_to:int
    ratings=float
    review=str