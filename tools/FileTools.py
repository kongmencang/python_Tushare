import os


class FileTools(object):
    @classmethod
    def make_dir(cls, path):
        if not os.path.exists(path):
            os.makedirs(path)