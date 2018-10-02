class Meta:
    def __init__(self, code : int, error_type : str = None, error_message : str = None):
        self.code = code
        self.error_type = error_type
        self.error_message = error_message

    @classmethod
    def fromJson(cls, metaData):
        return cls(metaData['code'], metaData.get('error_type'), metaData.get('error_message'))

    def __str__(self):
        error_type_str = ", error_type : {}".format(self.error_type) if self.error_type else ""
        error_message_str = ", error_message : {}".format(self.error_message) if self.error_message else ""

        return "['code' : {}{}{}]".format(self.code, error_type_str, error_message_str)