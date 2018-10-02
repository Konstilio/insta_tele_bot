class InstaException(Exception):
    def __init__(self, error_message : str, error_type : str):
        self.error_message = error_message
        self.error_type = error_type

    def __str__(self):
        return "InstaException type={}, message={}".format(self.error_type, self.error_message)

    @staticmethod
    def raiseFromMeta(meta):
        if not meta.error_type:
            return

        klass = globals()[meta.error_type]
        raise klass(meta.error_message)

class OAuthAccessTokenException(InstaException):
    def __init__(self, error_messae : str):
        super().__init__(error_messae, __class__.__name__)


