class BaseException(Exception):
    pass

class InvalidColorException(BaseException):
    pass

class ServerInternalErrorException(BaseException):
    pass

class InvalidCommandException(BaseException):
    pass

class InvalidCredentialsException(BaseException):
    pass

class InvalidChannelException(BaseException):
    pass

class BulbConnectionError(BaseException):
    pass

