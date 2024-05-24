import time
from threading import Thread

import numpy as np
import pandas as pd

from Comparison.BaseComparison import BaseComparison
from calculate.Calculate import Calculate
from chart.Chart import Chart

from config import TOKEN, PERIOD, SCORCE_TABLE_NAME, SEAM_INDUSTRY_NUM, INFO_ANALYES_URL, TSCODE, ANALYES_ARGUMENT, \
    REPORT_SELF_ARGUMENT, IMG_URL, SELF_RSCORCE_COMENT, SELF_TOTAL_SCORCE_COMENT

from tools.FileTools import FileTools
from tools.PandasDataFormTool import PandasDataFormTool


"""
初始化 要分析的公司Calculate 对象
"""

self_calculate = Calculate(TOKEN, TSCODE)
"""
初始化Chart对象
"""
chart = Chart()

#获取评分表图片
# self_calculate.get_score_table()

"""
#同类型公司列表获取
"""
# companys_ts_code = PandasDataFormTool.get_random_col_list(excel_file=self_calculate.get_seam_industry_list(),
#                                                   col_name="ts_code",n=SEAM_INDUSTRY_NUM)
# companys = []

# """获取公司列表"""
# def create_company(ts_code):
#     companys.append(Calculate(ts_code=ts_code, tushare_token=TOKEN))
#
# ths = []
# for ts_code in companys_ts_code:
#     thread = Thread(target=create_company, args=(ts_code,))
#     thread.start()
#     ths.append(thread)
#
# for thread in ths:
#     thread.join()
#
#
# #
# def get_company_info(company):
#     company_data = ([
#         # 营业能力
#         company.get_profitability_metrics_to_excel(PERIOD),
#         # 运营能力
#         company.get_operational_capability_indicators_to_excel(PERIOD),
#         # 债偿能力
#         company.get_solvency_indicators_to_excel(PERIOD),
#         # 成长能力
#         company.get_growth_capacity_indicators_to_excel(PERIOD)
#     ])
#     for i in range(len(company_data)):
#         company.get_score_to_excel([company_data[i]], SCORCE_TABLE_NAME[i])
#         if company.ts_code==TSCODE:
#             chart.get_all_line_chart(ts_code=company.ts_code,company_name=company.name,data=company_data[i])
#     company.get_score_to_excel(company_data, "趋势分析综合评分表")



"""
生成
"""

# #获取自身的信息
# def get_self_info():
#     get_company_info(company=self_calculate)
# #
#
# #获取同类型公司信息
# def get_seam_industury_companys_info():
#     threads = []
#     for ts_code in companys:
#         company=Calculate(TOKEN,ts_code)
#         thread = Thread(target=get_company_info, args=(company,))
#         threads.append(thread)
#         thread.start()
#         # 等待所有线程完成
#     for thread in threads:
#         thread.join()
#
#
# #获取同类型公司信息
# def get_seam_industury_companys_info():
#
#     threads = []
#     for company in companys:
#         thread = Thread(target=get_company_info, args=(company,))
#         threads.append(thread)
#         thread.start()
#         # 等待所有线程完成
#     for thread in threads:
#         thread.join()
#
# # 多线程执行self_calculate
# self_thread = Thread(target=get_self_info)
# self_thread.start()
# # 多线程执行其他公司信息获取
# get_seam_industury_companys_info()
# # 等待self_thread线程完成
# self_thread.join()
#
# b=BaseComparison(self_calculate)
#
#
#
# for analyes_argument in ANALYES_ARGUMENT.keys():
#     b.get_comparison_to_cart(dir_path=INFO_ANALYES_URL, companys=companys, comparison_object_name=analyes_argument)
#     for argument in ANALYES_ARGUMENT[analyes_argument]:
#         b.get_comparison_to_cart(dir_path=INFO_ANALYES_URL,companys=companys,comparison_object_name=argument)
#
#
#
#
# #b.get_totle_scorce_cart(companys)

"""
自身指标图像地址字典
"""
indicator_images={}
# indicator_images={
#     "营业能力":{"毛利率":r"C:\Users\11845\Desktop\财务分析\财务分析\img\600519.SH-贵州茅台\base\600519.SH-贵州茅台-毛利率.png",
#                 "ROA":r"C:\Users\11845\Desktop\财务分析\财务分析\img\600519.SH-贵州茅台\base\600519.SH-贵州茅台-ROA.png"
#                 },
#     "成长能力":{"营收增长率":r"C:\Users\11845\Desktop\财务分析\财务分析\img\600519.SH-贵州茅台\base\600519.SH-贵州茅台-营收增长率.png"}
# }
"""
分析评论字典
"""
indicator_comments={}
# indicator_comments={
#     "营业能力": {
#         "毛利率": "ff",
#         "ROA": "阿萨"
#         },
#     "成长能力": {
#         "营收增长率": "ss"}
# }


for i in REPORT_SELF_ARGUMENT.keys():
    indicator_images[i]={}
    indicator_comments[i]={}
    for j in REPORT_SELF_ARGUMENT[i].keys():
        indicator_images[i][j]=FileTools.get_file_path(dir_path=IMG_URL,ts_code=self_calculate.ts_code,table_name=j,dir_list="base")
        df=PandasDataFormTool.get_df_from_excel_file(INFO_ANALYES_URL,self_calculate.ts_code,table_name=j)
        num=df.iloc[0][j]
        for k in REPORT_SELF_ARGUMENT[i][j].keys():
            if np.isnan(num):
                #print("空值，无法分析")
                indicator_comments[i][j]="空值，无法分析"
            if num>=k:
                indicator_comments[i][j]=REPORT_SELF_ARGUMENT[i][j][k]
                break


"""
自身评分的各种参数
"""
#评分字典
s=self_calculate.get_total_score()
scores={}#图片地址地点
score_comments={}#评论
for i in SCORCE_TABLE_NAME:
    scores[i]=FileTools.get_file_path(dir_path=IMG_URL,ts_code=self_calculate.ts_code,table_name=i,dir_list="base")
    num=s[i]
    for j in SELF_RSCORCE_COMENT[i].keys():
        if np.isnan(num):
                #print("空值，无法分析")
            score_comments[i]="空值，无法分析"
        if num>=j:
            score_comments[i]=SELF_RSCORCE_COMENT[i][j]
            break

#总分
total_score=self_calculate.get_avg_score()
total_score_comment=""
for i in SELF_TOTAL_SCORCE_COMENT.keys():
    if total_score>=i:
        total_score_comment=SELF_TOTAL_SCORCE_COMENT[i]



from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('template.html')

company_introduction=self_calculate.introduction
company_name = self_calculate.name
company_ts_code=self_calculate.ts_code
company_industry=self_calculate.industry
company_full_name=self_calculate.fullname

with open("./report.html", 'w+', encoding='utf-8') as report:
    r=template.render(company_full_name=company_full_name,
                      company_name=company_name,
                      company_introduction=company_introduction,
                      company_ts_code=company_ts_code,
                      company_industry=company_industry,
                      parameters=ANALYES_ARGUMENT,
                      indicator_images=indicator_images,
                      indicator_comments=indicator_comments,
                      total_score=total_score,
                      total_score_comment=total_score_comment,
                      scores=scores,
                      score_comments=score_comments)

    report.write(r)


#
#
# """
# 遍历 parameters 字典，每个能力（如营业能力、运营能力等）都有一个标题 (<h3>{{ ability }}</h3>)。
# 每个能力包含的指标（如毛利率、营业利润率等）都会展示一个图表
# (<img src="{{ indicator_images[ability][indicator] }}" alt="{{ indicator }}图表">)
# 以及对应的评语 (<p>{{ indicator_comments[ability][indicator] }}</p>)
# """
