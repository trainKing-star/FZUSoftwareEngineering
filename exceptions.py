
# 文件异常类
class FileProcessException(BaseException):
    # 初始化信息
    def __init__(self, message):
        # 公有属性，能被外部访问
        self.message = "[异常]:" + message
    # 抛出时能显示异常原因
    def __str__(self):
        return self.message

