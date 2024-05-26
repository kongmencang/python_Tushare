import os
import random

import matplotlib.pyplot as plt
import numpy as np


from config import IMG_URL
from tools.FileTools import FileTools


class BaseChart(object):
    def __init__(self):
        plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
        # plt.gcf().subplots_adjust(bottom=0.5)
        # plt.figure(figsize=(8,8))
        plt.tight_layout()

    def get_line_chart(self, ts_code, company_name, label, x, y):
        print(f"正在绘制:{ts_code}的{label}折线图")
        plt.plot(x, y, label=label)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=3, borderaxespad=4)
        plt.title(ts_code + "-" + label, loc="left")

        dir_path = IMG_URL + os.sep + ts_code + "-" + company_name + os.sep + "base"
        FileTools.make_dir(dir_path)
        plt.savefig(dir_path + os.sep + ts_code + "-" + company_name + f"-{label}.png")
        plt.close()
        print(f"绘制完成:{ts_code}的{label}折线图")

    def get_bar_chart(self, data, name, label, ts_code):
        data = sorted(data.items(), key=lambda x: x[1])
        x = [x[0] for x in data]
        d = []
        for i in data:
            if np.isnan(i[1]):
                d.append(0)
            else:
                d.append(i[1])

        # 生成随机颜色列表
        colors = []
        while len(colors) < len(x):
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            if color not in colors:
                colors.append(color)
        plt.title(name + "-" + label, loc="left")
        plt.xticks(rotation=30)
        plt.bar(x, d, color=colors)

        print(f"正在绘制:{ts_code}的{label}的柱状图")

        dir_path = IMG_URL + os.sep + ts_code + "-" + name + os.sep + "comparison"
        FileTools.make_dir(dir_path)
        plt.savefig(dir_path + os.sep + ts_code + "-" + name + f"-{label}.png")
        plt.close()
        print(f"绘制完成:{ts_code}的{label}的柱状图")

    def get_excel_chart(self, df, name, label, ts_code):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.axis("off")
        ax.table(cellText=df.values, colLabels=df.columns, loc="center")
        dir_path = IMG_URL + os.sep + ts_code + "-" + name + os.sep + "base"
        FileTools.make_dir(dir_path)
        plt.savefig(os.path.join(dir_path, ts_code + "-" + name + f"-{label}.png"))
        plt.close()
