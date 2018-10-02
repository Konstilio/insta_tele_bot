class ResponseItem:
    def __str__(self):
        result = "{"
        for attr, value in self.__dict__.items():
            if not value is None:
                result += "{} : {}, ".format(str(attr), str(value))

        if result == "{":
            return "{}"

        return result[0:-2] + "}"

class Meta(ResponseItem):
    def __init__(self, code : int, error_type : str = None, error_message : str = None):
        self.code = code
        self.error_type = error_type
        self.error_message = error_message

    @classmethod
    def fromJson(cls, metaData):
        return cls(metaData['code'], metaData.get('error_type'), metaData.get('error_message'))

class Pagination(ResponseItem):
    def __init__(self, next_url : str, next_max_id : str):
        self.next_url = next_url
        self.next_max_id = next_max_id

    @classmethod
    def fromJson(cls, paginationData):
        return cls(paginationData['next_url'], paginationData.get('next_max_id'))

    def __str__(self):
        next_url_str = "next_url : {}".format(self.next_url) if self.next_url else ""
        next_max_id_str = ", next_max_id : {}".format(self.next_max_id) if self.next_max_id else ""

        return "{{}{}}".format(next_url_str, next_max_id_str)

class User(ResponseItem):
    def __init__(self, id : int, full_name : str, profile_picture: str, username : str):
        self.id = id
        self.full_name = full_name
        self.profile_picture = profile_picture
        self.username = username

    @classmethod
    def fromJson(cls, userData):
        return cls(userData['id'], userData.get('full_name'), userData['profile_picture'], userData.get('username'))

class Image(ResponseItem):
    def __init__(self, width : int, height : int, url : str):
        self.width = width
        self.height = height
        self.url = url

    @classmethod
    def fromJson(cls, imageData):
        return cls(imageData['width'], imageData.get('height'), imageData['url'])

class Images(ResponseItem):
    def __init__(self, thumbnail : Image, low_resolution : Image, standard_resolution : Image):
        self.thumbnail = thumbnail
        self.low_resolution = low_resolution
        self.standard_resolution = standard_resolution

    @classmethod
    def fromJson(cls, imagesData):
        return cls(\
            Image.fromJson(imagesData['thumbnail'])\
            , Image.fromJson(imagesData['low_resolution']) \
            , Image.fromJson(imagesData['standard_resolution']) \
        )

class DataEntry(ResponseItem):
    def __init__(self, id : str, user : User, images : Images):
        self.id = id
        self.user = user
        self.images = images

    @classmethod
    def fromJson(cls, dataEntryJSON):
        return cls(\
            dataEntryJSON['id']\
            , User.fromJson(dataEntryJSON['user'])\
            , Images.fromJson(dataEntryJSON['images'])\
        )

class Data:
    def __init__(self):
        self.entries = []

    @classmethod
    def fromJson(cls, dataJSON):
        result = cls()
        for entryJSON in dataJSON:
            result.append(DataEntry.fromJson(entryJSON))

        return result

    def append(self, dataEntry : DataEntry):
        self.entries.append(dataEntry)

    def getFirst(self):
        if not self.entries:
            return None

        return self.entries[0]



