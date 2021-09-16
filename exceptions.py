
class FileProcessException(BaseException):
    def __init__(self, message):
        self.message = "[异常]:" + message

    def __str__(self):
        return self.message

