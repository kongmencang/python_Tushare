from chart.BaseChart import BaseChart
from chart.Chart import Chart
from company.Company import Company
from config import ANALYES_ARGUMENT
from tools.PandasDataFormTool import PandasDataFormTool


class BaseComparison():
    """
    比较base类
    """
    """
    构造方法传入待比较的公司类
    """
    def __init__(self,calulate):
        self.chart=Chart()
        self.company = calulate

    def get_comparison_to_cart(self,companys,dir_path,comparison_object_name,row=0):
        if comparison_object_name in ANALYES_ARGUMENT.keys():#评分表结构不一样
            dic = {}
            comparison_object_name=comparison_object_name+"评分"
            companys.append(self.company)
            for company in companys:
                df = PandasDataFormTool.get_df_from_excel_file(dir_path=dir_path, ts_code=company.ts_code,
                                                               table_name=comparison_object_name)
                dic[company.name] = df.iloc[-1]["评分"]
            self.chart.get_bar_chart(data=dic, name=self.company.name, label=comparison_object_name + "对比图",
                                     ts_code=self.company.ts_code)
            return

        dic={}
        companys.append(self.company)
        for company in companys:
            df = PandasDataFormTool.get_df_from_excel_file(dir_path=dir_path,ts_code=company.ts_code,table_name=comparison_object_name)
            dic[company.name]=df.loc[row,comparison_object_name]
        self.chart.get_bar_chart(data=dic,name=self.company.name,label=comparison_object_name+"对比图",ts_code=self.company.ts_code)

    def get_totle_scorce_cart(self,companys):
        dic = {}
        for company in companys:
            dic[company.name] = company.get_avg_score()
        dic[self.company.name] = self.company.get_avg_score()
        self.chart.get_bar_chart(data=dic, name=self.company.name, label="综合评分对比表", ts_code=self.company.ts_code)




