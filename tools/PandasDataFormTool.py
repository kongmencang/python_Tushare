import os

import pandas as pd

from config import INFO_ANALYES_URL


class PandasDataFormTool(object):
    """
    pandas表格相关工具
    """
    """
    获取表格某一列的n个随机值，返回值为列表，入参为excel表格地址，列名，多少个
    默认十个，不满十个返回所有
    """
    @classmethod
    def get_random_col_list(cls,excel_file,col_name,n=3):
        df = pd.read_excel(excel_file)

        if len(df) >= n:
            random_ts_codes = df[col_name].sample(n=n, random_state=1, replace=False)
        else:
            random_ts_codes = df[col_name]

        return random_ts_codes.tolist()

    """
    根据目录文件名查找文件
    dir_path 根目录
    根目录下包含名称ts—_code 的目录下 包含 table_name 的xlsx文件
    """
    @classmethod
    def get_df_from_excel_file(cls,dir_path,ts_code,table_name):
        for root, dirs, files in os.walk(dir_path):
            if ts_code in os.path.basename(root):
                for file in files:
                    if table_name in file and file.endswith('.xlsx'):
                        file_path = os.path.join(root, file)
                        return pd.read_excel(file_path)




