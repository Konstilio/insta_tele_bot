import requests
from instaTools.instaResponses import Meta, Pagination, User, Images, DataEntry, Data
from instaTools.instaExceptions import InstaException

class InstaAccess:
    def __init__(self):
        self.access_token = 0
        self.base_url = "https://api.instagram.com/v1/"
        self.media_recent_url = "users/self/media/recent"

    def resetApi(self, access_token : str, client_secret : str):
        self.access_token = access_token
        self.client_secret = client_secret

    def getMediaRecent(self, max_id = None, min_id = None, count = None):
        payload = {'access_token' : self.access_token, 'max_id' : max_id, 'min_id' : min_id, 'count' : count}
        result_payload = {k:v for k,v in payload.items() if v is not None}
        url = self.base_url +  self.media_recent_url
        r = requests.get(url, params=result_payload)

        responseData = r.json()
        #print("getMediaRecent: " + str(responseData))
        meta = Meta.fromJson(responseData['meta'])

        #raise exception if needed
        InstaException.raiseFromMeta(meta)
        pagination = Pagination.fromJson(responseData['pagination'])

        dataJSON = responseData['data']
        data = Data.fromJson(dataJSON)

        return data, pagination





