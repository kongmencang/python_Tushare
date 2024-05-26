import time
from threading import Thread

import numpy as np


from comparison.BaseComparison import BaseComparison
from calculate.Calculate import Calculate
from chart.Chart import Chart

from config import TOKEN, PERIOD, SCORCE_TABLE_NAME, SEAM_INDUSTRY_NUM, INFO_ANALYES_URL, TSCODE, ANALYES_ARGUMENT, \
    REPORT_SELF_ARGUMENT, IMG_URL, SELF_RSCORCE_COMENT, SELF_TOTAL_SCORCE_COMENT, COMPARISON_COMENT

from tools.FileTools import FileTools
from tools.PandasDataFormTool import PandasDataFormTool
from jinja2 import Environment, FileSystemLoader

"""
初始化 要分析的公司Calculate 对象
"""

self_calculate = Calculate(TOKEN, TSCODE)
"""
初始化Chart对象
"""
chart = Chart()
#实例化分析类
b=BaseComparison(self_calculate)


"""
#同类型公司列表获取
"""
companys_ts_code = PandasDataFormTool.get_random_col_list(excel_file=self_calculate.get_seam_industry_list(),
                                                  col_name="ts_code",n=SEAM_INDUSTRY_NUM)
companys = []

"""获取公司列表"""
def create_company(ts_code):
    companys.append(Calculate(ts_code=ts_code, tushare_token=TOKEN))
#
ths = []
for ts_code in companys_ts_code:
    thread = Thread(target=create_company, args=(ts_code,))
    thread.start()
    ths.append(thread)

for thread in ths:
    thread.join()
#
#
#
def get_company_info(company):
    company_data = ([
        # 营业能力
        company.get_profitability_metrics_to_excel(PERIOD),
        # 运营能力
        company.get_operational_capability_indicators_to_excel(PERIOD),
        # 债偿能力
        company.get_solvency_indicators_to_excel(PERIOD),
        # 成长能力
        company.get_growth_capacity_indicators_to_excel(PERIOD)
    ])
    for i in range(len(company_data)):
        company.get_score_to_excel([company_data[i]], SCORCE_TABLE_NAME[i])
        if company.ts_code==TSCODE:
            chart.get_all_line_chart(ts_code=company.ts_code,company_name=company.name,data=company_data[i])
    company.get_score_to_excel(company_data, "趋势分析综合评分表")




#获取自身的信息
def get_self_info():
    get_company_info(company=self_calculate)
#

#获取同类型公司信息
def get_seam_industury_companys_info():
    threads = []
    for ts_code in companys:
        company=Calculate(TOKEN,ts_code)
        thread = Thread(target=get_company_info, args=(company,))
        threads.append(thread)
        thread.start()
        # 等待所有线程完成
    for thread in threads:
        thread.join()


#获取同类型公司信息
def get_seam_industury_companys_info():

    threads = []
    for company in companys:
        thread = Thread(target=get_company_info, args=(company,))
        threads.append(thread)
        thread.start()
        # 等待所有线程完成
    for thread in threads:
        thread.join()

# 多线程执行self_calculate
self_thread = Thread(target=get_self_info)
self_thread.start()
# 多线程执行其他公司信息获取
get_seam_industury_companys_info()
# 等待self_thread线程完成
self_thread.join()

#获取评分表图片
self_calculate.get_score_table()

#
#
#
comparison_totle_sc={}#综合评分对比
comparison_sc={} #常规参数
for analyes_argument in ANALYES_ARGUMENT.keys():
    s2 = b.get_comparison_to_cart(dir_path=INFO_ANALYES_URL, companys=companys, comparison_object_name=analyes_argument)
    comparison_totle_sc[analyes_argument]=s2
    for argument in ANALYES_ARGUMENT[analyes_argument]:
        #细分项
        s1=b.get_comparison_to_cart(dir_path=INFO_ANALYES_URL,companys=companys,comparison_object_name=argument)
        comparison_sc[argument]=s1



#获取综合评分（总体）的图片
sc=b.get_totle_scorce_cart(companys)
#总体评分评论
totle_comment=""
sc = sorted(sc.items(), key=lambda x: x[1], reverse=True)  # 获取对应排行字典
self_rank = None
for index, (name, _) in enumerate(sc, start=1):  # 获取排名
    if name == self_calculate.name:
        self_rank = index
        break
total_length = len(sc)
# 计算排名比率
rank_ratio = self_rank / total_length if self_rank is not None else None
for k in COMPARISON_COMENT:  # 获取对应评论
    if rank_ratio <= k:
        totle_comment = COMPARISON_COMENT[k]
        break



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

#评分分析
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
        break


comparison_scores={}#对比图片链接
comparison_score_comments={}#对比评论



comparison_totle_scores={}#综合评分图片地址
comparison_totle_score_comments={}#综合评分评论
for i in ANALYES_ARGUMENT.keys():
    #综合评分
    comparison_totle_scores[i]= FileTools.get_file_path(dir_path=IMG_URL, ts_code=self_calculate.ts_code, table_name=i,
                                                        dir_list="comparison")

    d1 = sorted(comparison_totle_sc[i].items(), key=lambda x: x[1], reverse=True)  # 获取对应排行字典
    self_rank = None
    for index, (name, _) in enumerate(d1, start=1):  # 获取排名
        if name == self_calculate.name:
            self_rank = index
            break
    total_length = len(d1)
    # 计算排名比率
    rank_ratio = self_rank / total_length if self_rank is not None else None
    for k in COMPARISON_COMENT:  # 获取对应评论
        if rank_ratio <= k:
            comparison_totle_score_comments[i] = COMPARISON_COMENT[k]
            break


    for j in ANALYES_ARGUMENT[i]:
        comparison_scores[j] = FileTools.get_file_path(dir_path=IMG_URL, ts_code=self_calculate.ts_code, table_name=j,
                                                       dir_list="comparison")
        d1 = sorted(comparison_sc[j].items(), key=lambda x: x[1],reverse=True)#获取对应排行字典
        self_rank = None
        for index, (name, _) in enumerate(d1, start=1):#获取排名
            if name == self_calculate.name:
                self_rank = index
                break
        total_length = len(d1)
        # 计算排名比率
        rank_ratio = self_rank / total_length if self_rank is not None else None
        for k in COMPARISON_COMENT:#获取对应评论
            if rank_ratio <= k:
                comparison_score_comments[j]=COMPARISON_COMENT[k]
                break


env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('template.html')

company_introduction=self_calculate.introduction
company_name = self_calculate.name
company_ts_code=self_calculate.ts_code
company_industry=self_calculate.industry
company_full_name=self_calculate.fullname

#总体（综合）评分图片地址
totle_img = FileTools.get_file_path(dir_path=IMG_URL, ts_code=self_calculate.ts_code, table_name="综合评分",
                                    dir_list="comparison")
print(f"正在生成{self_calculate.name}的财务分析报告")
with open(f"./report/{self_calculate.name}财务分析报告.html", 'w+', encoding='utf-8') as report:
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
                      score_comments=score_comments,
                      comparison_scores=comparison_scores,
                      comparison_score_comments =comparison_score_comments,
                      comparison_totle_scores = comparison_totle_scores,
                     comparison_totle_score_comments = comparison_totle_score_comments,
                    totle_img=totle_img,
                      totle_comment=totle_comment
                      )

    report.write(r)

print(f"{self_calculate.name}的财务分析报告生成完毕")









#{'毛利率': {'老白干酒': 0.6147, '五粮液': 0.7446, '顺鑫农业': 0.362, '山西汾酒': 0.7192, '天佑德酒': 0.6442, '酒鬼酒': 0.7775, '今世缘': 0.7279, '洋河股份': 0.7135, '迎驾贡酒': 0.6436, '古井贡酒': 0.7671, '贵州茅台': 0.913}, '营业利润率': {'老白干酒': 0.1178, '五粮液': 0.4838, '顺鑫农业': 0.0796, '山西汾酒': 0.2393, '天佑德酒': 0.0463, '酒鬼酒': 0.2645, '今世缘': 0.4007, '洋河股份': 0.4221, '迎驾贡酒': 0.335, '古井贡酒': 0.271, '贵州茅台': 0.6911}, '净利润率': {'老白干酒': 0.1003, '五粮液': 0.3637, '顺鑫农业': 0.0549, '山西汾酒': 0.1729, '天佑德酒': 0.0172, '酒鬼酒': 0.1981, '今世缘': 0.2994, '洋河股份': 0.3194, '迎驾贡酒': 0.2466, '古井贡酒': 0.2071, '贵州茅台': 0.5147}, 'ROE': {'老白干酒': 0.1339, '五粮液': 0.2526, '顺鑫农业': 0.1069, '山西汾酒': 0.2838, '天佑德酒': 0.0152, '酒鬼酒': 0.1299, '今世缘': 0.2192, '洋河股份': 0.2105, '迎驾贡酒': 0.2048, '古井贡酒': 0.2535, '贵州茅台': 0.3312}, 'ROA': {'老白干酒': 0.0688, '五粮液': 0.1808, '顺鑫农业': 0.0387, '山西汾酒': 0.139, '天佑德酒': 0.0126, '酒鬼酒': 0.0982, '今世缘': 0.1564, '洋河股份': 0.1433, '迎驾贡酒': 0.139, '古井贡酒': 0.159, '贵州茅台': 0.2403}, 'EBIT': {'老白干酒': 0.1139, '五粮液': 0.4533, '顺鑫农业': 0.0876, '山西汾酒': 0.2477, '天佑德酒': 0.039, '酒鬼酒': 0.2502, '今世缘': 0.3253, '洋河股份': 0.3742, '迎驾贡酒': 0.318, '古井贡酒': 0.2478, '贵州茅台': 0.6914}, '营业能力': {'老白干酒': 79.17, '五粮液': 83.33, '顺鑫农业': 41.67, '山西汾酒': 87.5, '天佑德酒': 33.33, '酒鬼酒': 87.5, '今世缘': 66.67, '洋河股份': 50, '迎驾贡酒': 75, '古井贡酒': 91.67, '贵州茅台': 58.33}, '存货周转率': {'老白干酒': 0.9682, '五粮液': 1.0051, '顺鑫农业': 1.1613, '山西汾酒': 0.7929, '天佑德酒': 0.5224, '酒鬼酒': 0.3834, '今世缘': 0.6435, '洋河股份': 0.4679, '迎驾贡酒': 0.5291, '古井贡酒': 0.8948, '贵州茅台': 0.3046}, '总资产周转率': {'老白干酒': 0.6859, '五粮液': 0.5207, '顺鑫农业': 0.7117, '山西汾酒': 0.8517, '天佑德酒': 0.4363, '酒鬼酒': 0.4958, '今世缘': 0.5222, '洋河股份': 0.449, '迎驾贡酒': 0.5641, '古井贡酒': 0.7897, '贵州茅台': 0.4983}, '应收账款周转率': {'老白干酒': 120.7343, '五粮液': 382.901, '顺鑫农业': 213.8539, '山西汾酒': 1394.6356, '天佑德酒': 34.7954, '酒鬼酒': 236.6381, '今世缘': 117.2074, '洋河股份': 2151.3069, '迎驾贡酒': 73.5162, '古井贡酒': 295.4134, '贵州茅台': nan}, '运营能力': {'老白干酒': 58.33, '五粮液': 91.67, '顺鑫农业': 66.67, '山西汾酒': 66.67, '天佑德酒': 16.67, '酒鬼酒': 75, '今世缘': 75, '洋河股份': 41.67, '迎驾贡酒': 33.33, '古井贡酒': 33.33, '贵州茅台': 83.33}, '流动比率': {'老白干酒': 1.282, '五粮液': 3.2172, '顺鑫农业': 1.4585, '山西汾酒': 1.5071, '天佑德酒': 3.2457, '酒鬼酒': 3.1458, '今世缘': 2.3368, '洋河股份': 2.2862, '迎驾贡酒': 2.3321, '古井贡酒': 2.4783, '贵州茅台': 3.8698}, '速动比率': {'老白干酒': 0.6491, '五粮液': 2.754, '顺鑫农业': 0.7622, '山西汾酒': 0.8648, '天佑德酒': 0.9924, '酒鬼酒': 1.951, '今世缘': 1.554, '洋河股份': 1.4013, '迎驾贡酒': 1.054, '古井贡酒': 1.7219, '贵州茅台': 3.2168}, '利息保障倍数': {'老白干酒': nan, '五粮液': nan, '顺鑫农业': nan, '山西汾酒': nan, '天佑德酒': nan, '酒鬼酒': nan, '今世缘': nan, '洋河股份': np.nan, '迎驾贡酒': nan, '古井贡酒': nan, '贵州茅台': 405.2271}, '资产负债率': {'老白干酒': 0.4749, '五粮液': 0.2848, '顺鑫农业': 0.6612, '山西汾酒': 0.5255, '天佑德酒': 0.1588, '酒鬼酒': 0.2472, '今世缘': 0.2838, '洋河股份': 0.3173, '迎驾贡酒': 0.3163, '古井贡酒': 0.32, '贵州茅台': 0.2249}, '债偿能力': {'老白干酒': 68.75, '五粮液': 56.25, '顺鑫农业': 62.5, '山西汾酒': 62.5, '天佑德酒': 56.25, '酒鬼酒': 75, '今世缘': 37.5, '洋河股份': 75, '迎驾贡酒': 50, '古井贡酒': 75, '贵州茅台': 62.5}, '营收增长率': {'老白干酒': 0.1248, '五粮液': 0.252, '顺鑫农业': 0.234, '山西汾酒': 0.2663, '天佑德酒': -0.0704, '酒鬼酒': 0.2738, '今世缘': 0.3035, '洋河股份': -0.0428, '迎驾贡酒': 0.0826, '古井贡酒': 0.1993, '贵州茅台': 0.1601}, '营业利润增长率': {'老白干酒': 0.1842, '五粮液': 0.2953, '顺鑫农业': 0.1158, '山西汾酒': 0.3061, '天佑德酒': -0.6489, '酒鬼酒': 0.3574, '今世缘': 0.2872, '洋河股份': -0.0973, '迎驾贡酒': 0.2097, '古井贡酒': 0.2031, '贵州茅台': 0.1499}, '净利润增长率': {'老白干酒': 0.154, '五粮液': 0.2984, '顺鑫农业': 0.124, '山西汾酒': 0.3165, '天佑德酒': -0.7881, '酒鬼酒': 0.345, '今世缘': 0.2671, '洋河股份': -0.0899, '迎驾贡酒': 0.1953, '古井贡酒': 0.2395, '贵州茅台': 0.1623}, '固定资产增长率': {'老白干酒': -0.0229, '五粮液': 0.1609, '顺鑫农业': -0.0388, '山西汾酒': 0.0137, '天佑德酒': 0.0384, '酒鬼酒': -0.1094, '今世缘': 0.344, '洋河股份': -0.0737, '迎驾贡酒': 0.0718, '古井贡酒': -0.0235, '贵州茅台': -0.0068}, '总资产增长率': {'老白干酒': 0.145, '五粮液': 0.2358, '顺鑫农业': 0.1094, '山西汾酒': 0.3583, '天佑德酒': -0.0451, '酒鬼酒': 0.1249, '今世缘': 0.1717, '洋河股份': 0.0785, '迎驾贡酒': 0.0853, '古井贡酒': 0.1088, '贵州茅台': 0.1451}, '成长能力': {'老白干酒': 35, '五粮液': 65, '顺鑫农业': 55, '山西汾酒': 55, '天佑德酒': 50, '酒鬼酒': 55, '今世缘': 70, '洋河股份': 40, '迎驾贡酒': 55, '古井贡酒': 60, '贵州茅台': 35}}
