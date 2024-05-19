import copy
import os

from analyes.BaseAnalyes import BaseAnalyes
import pandas as pd
from config import INFO_ANALYES_URL

class Analyes(BaseAnalyes):

    """
    盈利能力指标
    """
    """
    生成毛利率报表
    period 报表时间列表，只传入一个的情况下，获取五年内数据
    返回值为毛利字典
    毛利率 = 毛利/ 营业收入 = （营业收入-营业成本）/营业收入
    """
    def get_analyse_gross_margin_to_excel(self,period):
        args=['毛利率',"revenue","oper_cost"]
        return self.profit_sheet_two_agrs_reduce_division_to_excel(period,args)
        return dic
    """
    生成 营业利润率报表
    period 报表时间列表，只传入一个的情况下，获取五年内数据
    返回值为营业利润率字典
    营业利润率 = 营业利润 / 营业收入
    """
    def get_analyse_operating_margin_to_excel(self, period):
        args=['营业利润率',"revenue","operate_profit"]
        return self.get_profit_two_args_division_to_excel(period,args)

    """
     生成 净利润率报表
     period 报表时间列表，只传入一个的情况下，获取五年内数据
     返回值为净润率字典
     净利润率 = 净利润 / 营业收入=（利润总额-所得税费用） / 营业收入
     """
    def get_net_profit_margin_to_excel(self,period=[]):
        args=['净利润率',"revenue","n_income"]
        return self.get_profit_two_args_division_to_excel(period,args)

    """
    ROE
    𝑅𝑂𝐸 = 归母净利润/(期初归母净资产归母净利润 +期末归母净资产) / 2
    """
    def get_net_ROE_to_excel(self,period):
        args = ['ROE', "n_income_attr_p","total_hldr_eqy_exc_min_int","total_hldr_eqy_exc_min_int"]
        return self.get_profit_balance_three_agrs_to_excel(period,args)

    """
    ROA
    ROA =净利润／平均资产总额×100%，是用来衡量企业每单位资产在特定时期内创造的净利润。
    其中，平均资产总额=（总资产初始额+总资产末期额）/2，在资产负债表。净利润在利润表中。
    """
    def get_net_ROA_to_excel(self, period):
        args=['ROA','n_income_attr_p', 'total_assets','total_assets']
        return self.get_profit_balance_three_agrs_to_excel(period,args)


    """
    EBIT
    period 报表时间列表，只传入一个的情况下，获取五年内数据
    EBIT利润率 = 销售息税前利润 / 销售收入×100 %
    """
    def get_analyse_EBIT_to_excel(self, period):
        args=['EBIT', "revenue",'ebit']
        return self.get_profit_two_args_division_to_excel(period,args)


    """
    营业能力指标组合方法
    """
    def get_profitability_metrics_to_excel(self,period):
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', '毛利率','营业利润率','净利润率','ROE','ROA','EBIT'], index=[i for i in range(len(period))])
        #毛利
        gross_margin = self.get_analyse_gross_margin_to_excel(period)
        print("Gross Margin:", gross_margin)
        #营业利润率
        operating_margin=self.get_analyse_operating_margin_to_excel(period)
        print("Operating Margin:", operating_margin)
        #净利润率
        profit_margin = self.get_net_profit_margin_to_excel(period)
        print("Profit Margin:", profit_margin)
        #ROE
        ROE =self.get_net_ROE_to_excel(copy.deepcopy(period))
        print("ROE:", ROE)
        #ROA
        ROA= self.get_net_ROA_to_excel(copy.deepcopy(period))
        #EBIT
        EBIT = self.get_analyse_EBIT_to_excel(period)
        print("EBIT:", EBIT)

        for i in range(len(period)):
            df.loc[i] =[self.ts_code,period[i],gross_margin[period[i]],operating_margin[period[i]],profit_margin[period[i]],ROE[period[i]],ROA[period[i]],EBIT[period[i]]]
        df.to_excel(INFO_ANALYES_URL + os.sep + f"{self.ts_code}#营业能力指标.xlsx")

    """
    运营能力指标
    """

    """
    存货周转率 
    存货周转率 = 营业成本 / （（期初存货 + 期末存货） / 2）
    """
    def get_stock_turnover_to_excel(self,period):
        args=['存货周转率',"oper_cost","inventories","inventories"]
        return self.get_profit_balance_three_agrs_to_excel(period,args)

    """
    总资产周转率
    总资产周转率 = 营业收入 / 平均总资产 = 营业收入 / ((期初总资产 + 期末总资产) / 2)
    """
    def get_total_asset_turnover_to_excel(self,period):
        args=["总资产周转率","revenue","total_assets","total_assets"]
        return self.get_profit_balance_three_agrs_to_excel(period,args)

    """
    应收账款周转率
    应收账款周转率 = 营业收入 / 平均应收账款
    """
    def get_accounts_receivable_turnover_ratio_to_excel(self,period):
        args=["应收账款周转率","revenue","accounts_receiv","accounts_receiv"]
        return self.get_profit_balance_three_agrs_to_excel(period,args)

    """
      运营能力指标组合方法
      """
    def get_operational_capability_indicators_to_excel(self,period):
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', '存货周转率','总资产周转率','应收账款周转率'], index=[i for i in range(len(period))])
        #存货周转率
        stock_turnover = self.get_stock_turnover_to_excel(copy.deepcopy(period))
        print("stock_turnover:", stock_turnover)
        #总资产周转率
        total_asset_turnover =self.get_total_asset_turnover_to_excel(copy.deepcopy(period))
        print("total_asset_turnover:", total_asset_turnover)
        #应收账款周转率
        accounts_receivable_turnover=self.get_accounts_receivable_turnover_ratio_to_excel(copy.deepcopy(period))
        print("accounts_receivable_turnover:",accounts_receivable_turnover)
        for i in range(len(period)):
            df.loc[i] =[self.ts_code,period[i],stock_turnover[period[i]],total_asset_turnover[period[i]],accounts_receivable_turnover[period[i]]]
        df.to_excel(INFO_ANALYES_URL + os.sep + f"{self.ts_code}#运营能力指标.xlsx")