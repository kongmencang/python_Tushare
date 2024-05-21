import os

import matplotlib.pyplot as plt

from config import IMG_URL
from tools.FileTools import FileTools


class BaseChart(object):
    def __init__(self):
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

    def get_line_chart(self,ts_code,label,x,y):
        plt.plot(x,y,label=label)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=3, borderaxespad=4)
        plt.title(ts_code+"#"+label,loc="left")

        dir_path = IMG_URL+os.sep+ts_code
        FileTools.make_dir(dir_path)
        plt.savefig(dir_path+os.sep+ts_code+f'#{label}.png')
        plt.close()



