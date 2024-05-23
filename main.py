import time
from threading import Thread

from Comparison.BaseComparison import BaseComparison
from calculate.Calculate import Calculate
from chart.Chart import Chart
from company.Company import Company
from config import TOKEN, PERIOD, SCORCE_TABLE_NAME, SEAM_INDUSTRY_NUM, INFO_ANALYES_URL, TSCODE
from tools.PandasDataFormTool import PandasDataFormTool


"""
初始化 要分析的公司Calculate 对象
"""

self_calculate = Calculate(TOKEN, TSCODE)
"""
初始化Chart对象
"""

chart = Chart()
"""
#同类型公司列表获取
"""
companys_ts_code = PandasDataFormTool.get_random_col_list(excel_file=self_calculate.get_seam_industry_list(),
                                                  col_name="ts_code",n=SEAM_INDUSTRY_NUM)
companys = []

"""获取公司列表"""
def create_company(ts_code):
    companys.append(Calculate(ts_code=ts_code, tushare_token=TOKEN))

ths = []
for ts_code in companys_ts_code:
    thread = Thread(target=create_company, args=(ts_code,))
    thread.start()
    ths.append(thread)

for thread in ths:
    thread.join()


for i in companys:
    print(i.name)



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

b=BaseComparison(self_calculate)

b.get_comparison_value(dir_path=INFO_ANALYES_URL,companys=companys,comparison_object_name="ROA")
