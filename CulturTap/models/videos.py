from .. import *


class videoModel_View(BaseModel):
    uid: int
    videoId: int
    url: list[str]
    thumbURL: str = "string"
    address: str
    place: str
    district: str
    state: str
    country: str
    lat: float
    long: float
    category: str
    genre: str
    title: str
    description: str
    pros: list
    cons: list
    rating: float
    shared: bool
    draft: bool
    views: int
    likes: int
    uploadTime: str


class videoModel_Post(BaseModel):
    uid: int
    url: list = ['string']
    thumbURL: str = "string"
    address: str
    lat: float
    long: float
    category: str
    genre: str
    title: str
    description: str
    pros: list
    cons: list
    rating: float = 0
    shared: bool = True
    draft: bool = True
    views: int = 0
    likes: int = 0


class s3Response(BaseModel):
    url: list[str]
    videoKeys: list[str]
    keyTHUMB: str
    thumbURL: str
