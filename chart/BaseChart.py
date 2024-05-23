import os
import random

import matplotlib.pyplot as plt
import numpy as np

from config import IMG_URL
from tools.FileTools import FileTools


class BaseChart(object):
    def __init__(self):
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

    def get_line_chart(self,ts_code,company_name,label,x,y):
        print(f"正在绘:{ts_code}的{label}折线图")
        plt.plot(x,y,label=label)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=3, borderaxespad=4)
        plt.title(ts_code+"#"+label,loc="left")

        dir_path = IMG_URL+os.sep+ts_code+"#"+company_name
        FileTools.make_dir(dir_path)
        plt.savefig(dir_path+os.sep+ts_code+"#"+company_name+f'#{label}.png')
        plt.close()
        print(f"绘制完成:{ts_code}的{label}折线图")

    def get_bar_chart(self,data):

        data = sorted(data.items(), key=lambda x:x[1])
        x= [x[0] for x in data]
        d=[d[1] for d in data]

        # 生成随机颜色列表
        colors = []
        colors = []
        while len(colors) < len(x):
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            if color not in colors:
                colors.append(color)

        plt.xticks(rotation=45)

        plt.bar(x, d, color=colors)
        plt.show()
        pass

