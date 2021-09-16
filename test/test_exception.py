import os
from exceptions import FileProcessException

class TestExceptions:

    def test_file_exist(self):
        test_path = ["E:/1", "E:/2", "E:/3"]
        try:
            for path in test_path:
                if not os.path.exists(path) or not os.path.isfile(path):
                    raise FileProcessException("输入的关键词路径不存在或不是文件")
                elif not os.path.exists(path) or not os.path.isfile(path):
                    raise FileProcessException("输入的待检测路径不存在或不是文件")
            raise BaseException
        except FileProcessException as e:
            print(e.message)
            print("测试文件异常类正常")