import os

from config import IMG_URL


# 文件相关工具
class FileTools(object):
    @classmethod
    def make_dir(cls, path):
        if not os.path.exists(path):
            print(f"创建目录{path}")
            os.makedirs(path)

    @classmethod
    def get_dir_is_exist(cls, path):
        if not os.path.exists(path):
            return False
        return True

    """
    查找文件地址  dir_list是目录列表 表示查询子目录或子目录的子目录 按序查询
    """

    @classmethod
    def get_file_path(cls, dir_path, ts_code, table_name, dir_list=""):
        root_dir = os.path.abspath(dir_path)
        ts_code_dirs = [d for d in os.listdir(root_dir) if ts_code in d]
        target_dir = os.path.join(root_dir, ts_code_dirs[0])
        if dir_list:
            target_dir = os.path.join(target_dir, dir_list)

        target_files = [f for f in os.listdir(target_dir) if table_name in f]

        return os.path.join(target_dir, target_files[0])
