from chart.BaseChart import BaseChart
from company.Company import Company
from tools.PandasDataFormTool import PandasDataFormTool


class BaseComparison():
    """
    比较base类
    """
    """
    构造方法传入待比较的公司类
    """
    def __init__(self,calulate):
        self.company = calulate
    def get_comparison_value(self,companys,dir_path,comparison_object_name,row=0):
        dic={}
        companys.append(self.company)
        for company in companys:
            df = PandasDataFormTool.get_df_from_excel_file(dir_path=dir_path,ts_code=company.ts_code,table_name=comparison_object_name)
            dic[company.name]=df.loc[row,comparison_object_name]

        b=BaseChart()
        b.get_bar_chart(dic)


