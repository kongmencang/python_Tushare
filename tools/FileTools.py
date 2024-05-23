import os

#文件相关工具
class FileTools(object):
    @classmethod
    def make_dir(cls, path):
        if not os.path.exists(path):
            print(f"创建目录{path}")
            os.makedirs(path)