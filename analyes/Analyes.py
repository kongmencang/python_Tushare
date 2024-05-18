import copy
import os

from company.Company import Company
import pandas as pd

from config import INFO_ANALYES_URL


class Analyes(Company):

    """
    生成毛利率报表
    period 报表时间列表，只传入一个的情况下，获取五年内数据
    返回值为毛利字典
    """
    def get_analyse_gross_margin_to_excel(self,period=[]):
        dic={}
        if len(period)==1:
            for i in range(4):
                period.append(str(int(period[i])-10000))
        df = pd.DataFrame(columns = ['TS股票代码','报告期','毛利率'],index=[i for i in range(len(period)) ])
        for i in range(len(period)):
            p_df= pd.read_excel(self.get_profit_info_to_excel(period=period[i]))
           # 营业收入
            revenue=p_df.loc[0,"revenue"]
            #营业成本
            oper_cost=p_df.loc[0,"oper_cost"]
            #毛利率 = 毛利/ 营业收入 = （营业收入-营业成本）/营业收入
            gross_margin=round((revenue-oper_cost)/revenue,4)
            dic[period[i]]=gross_margin;
            df.loc[i]=[self.ts_code,period[i],gross_margin]
        df.to_excel(INFO_ANALYES_URL+os.sep+f"{self.ts_code}#gross_margin.xlsx")
        return dic
    """
    生成 营业利润率报表
    period 报表时间列表，只传入一个的情况下，获取五年内数据
    返回值为营业利润率字典
    """
    def get_analyse_operating_margin_to_excel(self, period=[]):
        dic={}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', '营业利润率 '], index=[i for i in range(len(period))])
        for i in range(len(period)):
            p_df = pd.read_excel(self.get_profit_info_to_excel(period=period[i]))
            # 营业收入
            revenue = p_df.loc[0, "revenue"]
            # 营业利润
            operate_profit = p_df.loc[0, "operate_profit"]
            #营业利润率 = 营业利润 / 营业收入
            operating_margin = round(operate_profit / revenue, 4)
            df.loc[i] = [self.ts_code, period[i], operating_margin]
            dic[period[i]] = operating_margin;
        df.to_excel(INFO_ANALYES_URL + os.sep + f"{self.ts_code}#operating_margin.xlsx")
        return dic
    """
     生成 净利润率报表
     period 报表时间列表，只传入一个的情况下，获取五年内数据
     返回值为净润率字典
     """
    def get_net_profit_margin_to_excel(self,period=[]):
        dic={}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', '净利润率 '], index=[i for i in range(len(period))])
        for i in range(len(period)):
            p_df = pd.read_excel(self.get_profit_info_to_excel(period=period[i]))
            # 营业收入
            revenue = p_df.loc[0, "revenue"]
            # 净利润
            n_income = p_df.loc[0, "n_income"]
            #净利润率 = 净利润 / 营业收入=（利润总额-所得税费用） / 营业收入
            net_profit_margin = round(n_income / revenue, 4)
            df.loc[i] = [self.ts_code, period[i], net_profit_margin]
            dic[period[i]] = net_profit_margin;
        df.to_excel(INFO_ANALYES_URL + os.sep + f"{self.ts_code}#net_profit_margi.xlsx")
        return dic
    """
    ROE
    """
    def get_net_ROE_to_excel(self,period=[]):
        dic={}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        # 把最后一年的上一年也加入
        period.append(str(int(period[-1]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', 'ROE'], index=[i for i in range(len(period)-1)])
        for i in range(len(period)-1):
            #利润表
            p_df = pd.read_excel(self.get_profit_info_to_excel(period=period[i]))
            #负债表
            b_df = pd.read_excel(self.get_balance_info_to_excel(period=period[i]))
            # 归母净利润：“净利润(不含少数股东损益)
            n_income_attr_p=p_df.loc[0, "n_income_attr_p"]
            # 期末归母净利润  股东权益合计(不含少数股东权益) 负债表
            total_hldr_eqy_exc_min_int = b_df.loc[0, "total_hldr_eqy_exc_min_int"]
            #期初归母净利润 股东权益合计(不含少数股东权益) 负债表
            last_total_hldr_eqy_exc_min_int = pd.read_excel(self.get_balance_info_to_excel(period=period[i + 1])).loc[0,"total_hldr_eqy_exc_min_int"]
            """净资产收益率
            𝑅𝑂𝐸 = 归母净利润/(期初归母净资产归母净利润 +期末归母净资产) / 2
            """
            ROE =round(n_income_attr_p/((total_hldr_eqy_exc_min_int+last_total_hldr_eqy_exc_min_int)/2),4)
            df.loc[i] = [self.ts_code, period[i], ROE]
            dic[period[i]] = ROE;

        df.to_excel(INFO_ANALYES_URL + os.sep + f"{self.ts_code}#ROE.xlsx")
        return dic


    """
    ROA
    """
    def get_net_ROA_to_excel(self, period=[]):
        dic={}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        # 把最后一年的上一年也加入
        period.append(str(int(period[-1]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', 'ROA'], index=[i for i in range(len(period) - 1)])
        for i in range(len(period) - 1):
            # 利润表
            p_df = pd.read_excel(self.get_profit_info_to_excel(period=period[i]))
            # 负债表
            b_df = pd.read_excel(self.get_balance_info_to_excel(period=period[i]))
            # 净利润：“净利润(不含少数股东损益)
            n_income_attr_p = p_df.loc[0, "n_income_attr_p"]
            # 总资产初始额 负债表
            total_assets = b_df.loc[0, "total_assets"]
            # 总资产初始额  负债表
            last_total_assets = pd.read_excel(self.get_balance_info_to_excel(period=period[i + 1])).loc[
                0, "total_share"]

            """
            ROA =净利润／平均资产总额×100%，是用来衡量企业每单位资产在特定时期内创造的净利润。
            其中，平均资产总额=（总资产初始额+总资产末期额）/2，在资产负债表。净利润在利润表中。
            """

            ROA = round(n_income_attr_p / ((total_assets + last_total_assets) / 2), 4)
            df.loc[i] = [self.ts_code, period[i], ROA]
            dic[period[i]] = ROA;
        df.to_excel(INFO_ANALYES_URL + os.sep + f"{self.ts_code}#ROA.xlsx")
        return dic

        """
        EBIT
        period 报表时间列表，只传入一个的情况下，获取五年内数据
        """

    def get_analyse_EBIT_to_excel(self, period=[]):
        dic={}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', 'EBIT'], index=[i for i in range(len(period))])

        for i in range(len(period)):
            p_df = pd.read_excel(self.get_profit_info_to_excel(period=period[i]))
            # 营业收入
            revenue = p_df.loc[0, "revenue"]
            # 销售息税前利润
            ebit	= p_df.loc[0, "ebit"]
            # EBIT利润率 = 销售息税前利润 / 销售收入×100 %
            EBIT = round((ebit / revenue) , 4)
            df.loc[i] = [self.ts_code, period[i], EBIT]
            dic[period[i]] = EBIT;
        df.to_excel(INFO_ANALYES_URL + os.sep + f"{self.ts_code}#EBIT.xlsx")
        return dic

    """
    营业能力指标组合方法
    """
    def get_profitability_metrics(self,period):
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
        df.to_excel(INFO_ANALYES_URL + os.sep + f"{self.ts_code}#profitability_metrics.xlsx")
