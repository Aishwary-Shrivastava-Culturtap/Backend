from .. import *
from ..utils import *
from ..classes.database import database
from ..classes.S3 import Boto3
from ..models.videos import videoModel_View, videoModel_Post, s3Response
from ..admin.credentials import DB_URL, DB_HEADERS, KEY_ID, SECRET_KEY, TOKEN
from ..constants import BUCKET, VIDEOS, FILETYPES, THUMBNAILS

router = APIRouter(prefix='/videos', tags=['Videos'])
user = database.Users(DB_URL, DB_HEADERS)
history = database.History(DB_URL, DB_HEADERS)
search = database.Search(DB_URL,DB_HEADERS)

# --VIDEO DATA
client = database.Videos(url=DB_URL, header=DB_HEADERS)
s3 = Boto3(KEY_ID, SECRET_KEY, BUCKET)


@router.get("/get", status_code=status.HTTP_200_OK, response_model=list[videoModel_View])
def get_all_videos(token: str, end: int, start: int = 0):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        if start == 0:
            start += 1
        return client.show()[start:end]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/get/video/{videoId}", status_code=status.HTTP_200_OK, response_model=videoModel_View)
def get_video_by_videoId(videoId: int):
    try:
        return client.show(videoId=videoId)[0]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/get/user/{uid}", status_code=status.HTTP_200_OK, response_model=list[videoModel_View])
def get_videos_by_uid(uid: int, end: int, start: int = 0):
    try:
        return client.show(uid=uid)[start:end]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/get/matching", status_code=status.HTTP_200_OK, response_model=list[videoModel_View])
def get_data_by_matching(token: str, params: dict, end: int, start: int = 0):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        return client.show(**params)[start:end]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/get/by-distance/uid={CurrentUID}", status_code=status.HTTP_200_OK, response_model=list[videoModel_View])
def get_data_by_location(CurrentUID: int, maxKm: float, filtor: dict, end: int, start: int = 0, minKm: float = 0):
    try:
        videos = []
        User = user.show(uid=CurrentUID)[0]
        lat1, long1 = round(User['lat'], 2), round(User['long'], 2)

        for i in client.show(**filtor):
            lat2, long2 = round(i['lat'], 2), round(i['long'], 2)
            if minKm <= lat_long_difference((lat2, long2), (lat1, long1)) >= maxKm:
                videos.append(i)
        df = pd.DataFrame(videos)
        views=database.views(DB_URL,DB_HEADERS).show(uid=CurrentUID)
        notShownId=[i['videoId'] for i in views]
        for i in notShownId:
            try:
                df.drop(df[df['videoId']==i].index,inplace=True)
            except:
                continue
        df["uploadTime"] = df["uploadTime"].astype('datetime64[ns]')
        flag = 1

        try:
            df2 = df.nlargest(n=10, columns='uploadTime')
            videos = df2.to_dict(orient='records')
        except:
            flag = 0
            videos = []

        df["uploadTime"] = df["uploadTime"].astype(str)
        df.sort_values(by=['views', "likes"], inplace=True, ascending=False)

        if flag:
            videos+=df.to_dict(orient='records')[:-10]
        else:
            videos+=df.to_dict(orient='records')

        return videos[start:end]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/location-follow/{uid}",status_code=status.HTTP_200_OK,response_model=list[videoModel_View])
def getFollowedLocation(uid:int,end:int,start:int=0):
    try:
        userData=database.Users(DB_URL,DB_HEADERS).show(uid=uid)[0]
        following=userData['locationFollow']
        videos=[]
        for i in following:
            videos+=client.show(**{'city':i})
        random.shuffle(videos)
        return videos[start:end]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@router.get('/search')
def get_searched_data(query:str,end:int,start:int=0):
    results=search.show(field='data',query=query)
    df = pd.DataFrame(results)
    videoList = df['videoId'].to_list()
    allSearchedVideos=[get_video_by_videoId(i) for i in videoList]
    videosDf = pd.DataFrame(allSearchedVideos)
    videosDf.sort_values(by=['views', "likes"], inplace=True, ascending=False)
    return videosDf.to_dict(orient='records')[start:end]



@router.post('/add', status_code=status.HTTP_201_CREATED)
def adding_video_content(params: videoModel_Post):
    params = params.dict()
    params['uploadTime'] = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        address=address_finder(params['lat'],params['long'])
        params['place'],params['district'],params['state'],params['country']=address.values()
        response = client.add(**params)
        searchField={"videoId":response['videoId'],'data':'|'.join([value for value in params.values()])}
        search.add(**searchField)
        history.add(**{'type': 'video', 'videoId': response['videoId'],
                    'uid': response['uid'], 'status': 'added', 'uploadTime': params['uploadTime']})
        return response
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/add-video', status_code=status.HTTP_200_OK, response_model=s3Response)
async def adding_video(videoId: int, token: str, video: list[UploadFile], thumbnails: list[UploadFile] = None, action: str = "add"):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        toUpdate = {}
        videoData = get_video_by_videoId(videoId)
        expertCard=database.expertCard(DB_URL,DB_HEADERS)
        expertCardData=expertCard.show(videoData['uid'])
        try:
            expertCardLocation=expertCardData['expertLocation']+','+videoData['district']
        except:
            expertCardLocation=videoData['district']
        expertCard.update(uid=videoData['uid'],**{'expertLocation':expertCardLocation})
        videos_keys = []
        urls = []
        if thumbnails:
            if thumbnails[0].content_type in FILETYPES:
                thumbKey = f'{uuid4()}.{FILETYPES[thumbnails[0].content_type]}'
                thumbnail = await thumbnails[0].read()
                s3.upload(file=thumbnail, key=thumbKey,
                          folder=THUMBNAILS, bucket=BUCKET)
                urlTHUMB = f'https://{BUCKET}.s3.ap-south-1.amazonaws.com/{THUMBNAILS}{thumbKey}'
                toUpdate['thumbURL'] = urlTHUMB
                toUpdate['keyTHUMB'] = f'{THUMBNAILS}{thumbKey}'

        for item in video:
            if item.content_type in FILETYPES:
                key = f'{uuid4()}.{FILETYPES[item.content_type]}'
                data = await item.read()
                s3.upload(file=data, key=key, folder=VIDEOS, bucket=BUCKET)
                url = f'https://{BUCKET}.s3.ap-south-1.amazonaws.com/{VIDEOS}{key}'
                urls.append(url)
                videos_keys.append(f"{VIDEOS}{key}")

        if action.lower() == 'add':
            existingPic = videoData['url']
            urls += existingPic
        else:
            if keys := videoData.get('videoKeys'):
                for i in keys:
                    s3.delete(bucket=BUCKET, key=i)

        toUpdate['url'] = urls
        toUpdate['videoKeys'] = videos_keys
        update_video(videoId, toUpdate)
        return toUpdate
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)


@router.patch('/update/{videoId}', status_code=status.HTTP_202_ACCEPTED)
def update_video(videoId: int, params: dict):
    try:
        video = get_video_by_videoId(videoId)
        try:
            Likes = database.likes(DB_URL, DB_HEADERS)
            if params.get('views') != None:
                params['views'] = client.show(videoId=videoId)[0]["views"]+params['views']

            likes = params.get('likes')
            if likes != None:
                if len(Likes.show(User=params['User'], videoId=videoId)) != 0:
                    if likes == 1:
                        params['likes'] = video["likes"]+likes
                        Likes.add(User=params['User'], videoId=videoId)
                    elif likes != 1:
                        params['likes'] = video["likes"]-likes
                        Likes.delete(User=params['User'], videoId=videoId)
                    del params['User']
                else:
                    return {'msg': 'already liked by the user...'}
        except:
            pass
        history.add(**{'type': 'video', 'videoId': videoId,
                    'uid': video['uid'], 'status': 'updated', 'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'), 'updates': params})
        response = client.update(videoId, **params)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)


@router.delete('/delete/{videoId}', status_code=status.HTTP_204_NO_CONTENT)
def delete_video(videoId: int):
    Likes = database.likes(DB_URL, DB_HEADERS)
    Likes.deleteMany(videoId=videoId)
    videoData = get_video_by_videoId(videoId)
    if keys := videoData.get('videoKeys'):
        for i in keys:
            s3.delete(bucket=BUCKET, key=i)
    s3.delete(bucket=BUCKET, key=videoData.get('keyTHUMB'))
    database.views(DB_URL,DB_HEADERS).delete(videoId=videoId)
    client.delete(videoId=videoId)
    search.delete(videoId=videoId)
    history.add(**{'type': 'video', 'videoId': videoId,
                'uid': videoData['uid'], 'status': 'deleted', 'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')})
    return {'detail': 'done'}
