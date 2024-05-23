import copy
import os

from calculate.BaseCaculate import BaseCaculate
import pandas as pd
from config import INFO_ANALYES_URL
from tools.FileTools import FileTools


class Calculate(BaseCaculate):
    """
    参数计算类，集成基础计算，构造方法
    """

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
        print(f"正在获取：{self.ts_code}的毛利率报表")
        args=['毛利率',"revenue","oper_cost"]
        data=self.profit_sheet_two_agrs_reduce_division_to_excel(period,args)
        print(f"获取完成：{self.ts_code}的毛利率报表")
        return data

    """
    生成 营业利润率报表
    period 报表时间列表，只传入一个的情况下，获取五年内数据
    返回值为营业利润率字典
    营业利润率 = 营业利润 / 营业收入
    """
    def get_analyse_operating_margin_to_excel(self, period):
        print(f"正在获取：{self.ts_code}的营业利润报表")
        args=['营业利润率',"revenue","operate_profit"]
        data=self.get_profit_two_args_division_to_excel(period,args)
        print(f"获取完成：{self.ts_code}的营业利润报表")
        return data


    """
     生成 净利润率报表
     period 报表时间列表，只传入一个的情况下，获取五年内数据
     返回值为净润率字典
     净利润率 = 净利润 / 营业收入=（利润总额-所得税费用） / 营业收入
     """
    def get_net_profit_margin_to_excel(self,period=[]):
        print(f"正在获取：{self.ts_code}的营业利润报表")
        args=['净利润率',"revenue","n_income"]
        data=self.get_profit_two_args_division_to_excel(period,args)
        print(f"获取完成：{self.ts_code}的营业利润报表")
        return data

    """
    ROE
    𝑅𝑂𝐸 = 归母净利润/(期初归母净资产归母净利润 +期末归母净资产) / 2
    """
    def get_net_ROE_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的ROE报表")
        args = ['ROE', "n_income_attr_p","total_hldr_eqy_exc_min_int","total_hldr_eqy_exc_min_int"]
        data=self.get_profit_balance_three_agrs_to_excel(period,args)
        print(f"获取完成：{self.ts_code}的ROE报表")
        return data

    """
    ROA
    ROA =净利润／平均资产总额×100%，是用来衡量企业每单位资产在特定时期内创造的净利润。
    其中，平均资产总额=（总资产初始额+总资产末期额）/2，在资产负债表。净利润在利润表中。
    """
    def get_net_ROA_to_excel(self, period):
        print(f"正在获取：{self.ts_code}的ROA报表")
        args=['ROA','n_income_attr_p', 'total_assets','total_assets']
        data= self.get_profit_balance_three_agrs_to_excel(period,args)
        print(f"获取完成：{self.ts_code}的ROA报表")
        return data

    """
    EBIT
    period 报表时间列表，只传入一个的情况下，获取五年内数据
    EBIT利润率 = 销售息税前利润 / 销售收入×100 %
    """
    def get_analyse_EBIT_to_excel(self, period):
        print(f"正在获取：{self.ts_code}的EBIT报表")
        args=['EBIT', "revenue",'ebit']
        data= self.get_profit_two_args_division_to_excel(period,args)
        print(f"获取完成：{self.ts_code}的EBIT报表")
        return data

    """
    营业能力指标组合方法
    """
    def get_profitability_metrics_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的营业能力指标报表")
        indicators={}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', '毛利率','营业利润率','净利润率','ROE','ROA','EBIT'], index=[i for i in range(len(period))])
        #毛利
        gross_margin = self.get_analyse_gross_margin_to_excel(period)
        #营业利润率
        operating_margin=self.get_analyse_operating_margin_to_excel(period)
        #净利润率
        profit_margin = self.get_net_profit_margin_to_excel(period)
        #ROE
        ROE =self.get_net_ROE_to_excel(copy.deepcopy(period))
        #ROA
        ROA= self.get_net_ROA_to_excel(copy.deepcopy(period))
        #EBIT
        EBIT = self.get_analyse_EBIT_to_excel(period)

        for i in range(len(period)):
            df.loc[i] =[self.ts_code,period[i],gross_margin[period[i]],operating_margin[period[i]],profit_margin[period[i]],ROE[period[i]],ROA[period[i]],EBIT[period[i]]]
            indicators[period[i]] = {
                'TS股票代码': self.ts_code,
                '毛利率': gross_margin[period[i]],
                '营业利润率': operating_margin[period[i]],
                '净利润率': profit_margin[period[i]],
                'ROE': ROE[period[i]],
                'ROA': ROA[period[i]],
                'EBIT': EBIT[period[i]]
            }
        dir_path =INFO_ANALYES_URL + os.sep + f"{self.ts_code}#{self.name}"
        FileTools.make_dir(dir_path)
        df.to_excel(dir_path + os.sep + f"{self.ts_code}#{self.name}#营业能力指标.xlsx")
        print(f"获取完成：{self.ts_code}的营业能力指标报表")
        return indicators
    """
    运营能力指标
    """

    """
    存货周转率 
    存货周转率 = 营业成本 / （（期初存货 + 期末存货） / 2）
    """
    def get_stock_turnover_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的存货周转率报表")
        args=['存货周转率',"oper_cost","inventories","inventories"]
        data =  self.get_profit_balance_three_agrs_to_excel(period,args)
        print(f"获取完成：{self.ts_code}的存货周转率报表")
        return data
    """
    总资产周转率
    总资产周转率 = 营业收入 / 平均总资产 = 营业收入 / ((期初总资产 + 期末总资产) / 2)
    """
    def get_total_asset_turnover_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的总资产周转率报表")
        args=["总资产周转率","revenue","total_assets","total_assets"]
        data= self.get_profit_balance_three_agrs_to_excel(period,args)
        print(f"获取完成：{self.ts_code}的总资产周转率报表")
        return data
    """
    应收账款周转率
    应收账款周转率 = 营业收入 / 平均应收账款
    """
    def get_accounts_receivable_turnover_ratio_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的应收账款周转率报表")
        args=["应收账款周转率","revenue","accounts_receiv","accounts_receiv"]
        data= self.get_profit_balance_three_agrs_to_excel(period,args)
        print(f"获取完成：{self.ts_code}的应收账款周转率报表")
        return data

    """
      运营能力指标组合方法
      """
    def get_operational_capability_indicators_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的运营能力指标报表")
        dic={}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', '存货周转率','总资产周转率','应收账款周转率'], index=[i for i in range(len(period))])
        #存货周转率
        stock_turnover = self.get_stock_turnover_to_excel(copy.deepcopy(period))
        #总资产周转率
        total_asset_turnover =self.get_total_asset_turnover_to_excel(copy.deepcopy(period))
        #应收账款周转率
        accounts_receivable_turnover=self.get_accounts_receivable_turnover_ratio_to_excel(copy.deepcopy(period))
        for i in range(len(period)):
            df.loc[i] =[self.ts_code,period[i],stock_turnover[period[i]],total_asset_turnover[period[i]],accounts_receivable_turnover[period[i]]]

            dic[period[i]] = {
                'TS股票代码': self.ts_code,
                '存货周转率': stock_turnover[period[i]],
                '总资产周转率': total_asset_turnover[period[i]],
                '应收账款周转率': accounts_receivable_turnover[period[i]]
            }
        dir_path =INFO_ANALYES_URL + os.sep + f"{self.ts_code}#{self.name}"
        FileTools.make_dir(dir_path)
        df.to_excel(dir_path + os.sep + f"{self.ts_code}#{self.name}#运营能力指标.xlsx")
        print(f"获取完成：{self.ts_code}的运营能力指标报表")
        return dic

    """
    偿债能力指标
    """

    """
    流动比率
    流动比率 = 流动资产总额 / 流动负债总额
    """
    def  get_liquidity_ratio_to_excle(self,period):
        print(f"正在获取：{self.ts_code}的流动比率报表")
        args=["流动比率","total_cur_liab","total_cur_assets"]
        data = self.get_balance_two_args_division_to_excel(period,args)
        print(f"获取完成：{self.ts_code}的流动比率报表")
        return  data

    """
    速动比率
    速动比率 = ( 流动资产总额 - 存货 - 预付款项) / 流动负债总额
    """
    def get_quick_ratio_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的速动比率报表")
        args=["速动比率","total_cur_assets","inventories","prepayment","total_cur_liab"]
        data= self.get_balance_four_agrs_to_reduce_devision_excel(period,args)
        print(f"获取完成：{self.ts_code}的速动比率报表")
        return data
    """
    利息保障倍数

    利息保障倍数 = 息税前利润(EBIT) / 利息费用
    """

    def get_interest_protection_multiple_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的利息保障倍数报表")
        args=["利息保障倍数","int_exp","ebit"]
        data =  self.get_profit_two_args_division_to_excel(period,args)
        print(f"获取完成：{self.ts_code}的利息保障倍数报表")
        return data

    """
    资产负债率
    资产负债率=负债总额/资产总额×100%
    """
    def get_debt_to_asset_ratio_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的资产负债率报表")
        args=["资产负债率","total_assets","total_liab"]
        data =  self.get_balance_two_args_division_to_excel(period,args)
        print(f"获取完成：{self.ts_code}的资产负债率报表")
        return data
    """
    偿债能力指标组合方法
    """
    def get_solvency_indicators_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的偿债能力指标报表")
        dic={}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', '流动比率','速动比率','利息保障倍数','资产负债率'], index=[i for i in range(len(period))])
        #流动比率
        liquidity_ratio = self.get_liquidity_ratio_to_excle(period)
        #速动比率
        quick_ratio =self.get_quick_ratio_to_excel(period)
        #利息保障倍数
        interest_protection=self.get_interest_protection_multiple_to_excel(period)
        #资产负债率
        debt_to_asset_ratio=self.get_debt_to_asset_ratio_to_excel(period)

        for i in range(len(period)):
            df.loc[i] =[self.ts_code,period[i],liquidity_ratio[period[i]],liquidity_ratio[period[i]],interest_protection[period[i]],debt_to_asset_ratio[period[i]]]
            dic[period[i]] = {
                'TS股票代码': self.ts_code,
                '流动比率': liquidity_ratio[period[i]],
                '速动比率': quick_ratio[period[i]],
                '利息保障倍数': interest_protection[period[i]],
                '资产负债率': debt_to_asset_ratio[period[i]]
            }

        dir_path =INFO_ANALYES_URL + os.sep + f"{self.ts_code}#{self.name}"
        FileTools.make_dir(dir_path)
        df.to_excel(dir_path + os.sep + f"{self.ts_code}#{self.name}#偿债能力指标.xlsx")
        print(f"获取完成：{self.ts_code}的偿债能力指标报表")
        return dic

    """
    成长能力指标
    """
    """
    营收增长率
    营收增长率 = (本期营业收入 － 上期营业收入) / 上期营业收入
    """
    def get_increase_rate_of_main_business_revenue_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的营收增长率报表")
        args=["营收增长率","revenue","revenue","revenue"]
        data= self.get_profit_therr_agrs_reduce_devision(period,args)
        print(f"获取完成：{self.ts_code}的营收增长率报表")
        return data
    """
    营业利润增长率   
    营业利润增长率= (本年营业利润总额 - 上年营业利润总额) / 上年营业利润总额
    """
    def get_operating_rofit_growth_rate_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的营业利润增长率报表")
        args=['营业利润增长率','operate_profit','operate_profit','operate_profit']
        data= self.get_profit_therr_agrs_reduce_devision(period,args)
        print(f"获取完成：{self.ts_code}的营业利润增长率报表")
        return data
    """
    净利润增长率
    净利润增长率 =（期末净利润 - 期初净利润）/ 期初净利润
    """
    def get_net_profit_growth_rate_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的净利润增长率报表")
        args=['净利润增长率','n_income','n_income','n_income']
        data=  self.get_profit_therr_agrs_reduce_devision(period,args)
        print(f"获取完成：{self.ts_code}的净利润增长率报表")
        return data
    """
    固定资产增长率
    固定资产增长率 =（期末总固定资产 - 期初总固定资产）/ 期初固定资产
    """
    def get_growth_rate_of_fixed_assets_to_excel(self, period):
        print(f"正在获取：{self.ts_code}的固定资产增长率报表")
        args = ['固定资产增长率', 'fix_assets_total', 'fix_assets_total', 'fix_assets_total']
        data= self.get_banlance_therr_agrs_reduce_devision(period, args)
        print(f"获取完成：{self.ts_code}的固定资产增长率报表")
        return data
    """
    总资产增长率
    总资产增长率 =（期末总资产 - 期初总资产）/ 期初总资产
    """
    def  get_total_asset_growth_rate_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的总资产增长率报表")
        args=['总资产增长率','total_assets','total_assets','total_assets']
        data= self.get_banlance_therr_agrs_reduce_devision(period,args)
        print(f"获取完成：{self.ts_code}的总资产增长率报表")
        return data
    """
    成长能力指标组合方法
    """
    def get_growth_capacity_indicators_to_excel(self,period):
        print(f"正在获取：{self.ts_code}的成长能力指标报表")
        dic={}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', '营收增长率', '营业利润增长率', '净利润增长率', '固定资产增长率','总资产增长率'],
                          index=[i for i in range(len(period))])
        # 营收增长率
        increase_rate = self.get_increase_rate_of_main_business_revenue_to_excel(copy.deepcopy(period))
        # 营业利润增长率
        operating_rofit_growth_rate = self.get_operating_rofit_growth_rate_to_excel(copy.deepcopy(period))
        # 净利润增长率
        net_profit_growth_rate = self.get_net_profit_growth_rate_to_excel(copy.deepcopy(period))
        #固定资产增长率
        growth_rate=self.get_growth_rate_of_fixed_assets_to_excel(copy.deepcopy(period))
        #总资产增长率
        total_asset_growth_rate = self.get_total_asset_growth_rate_to_excel(copy.deepcopy(period))


        for i in range(len(period)):
            df.loc[i] = [self.ts_code, period[i], increase_rate[period[i]], operating_rofit_growth_rate[period[i]],
                         net_profit_growth_rate[period[i]], growth_rate[period[i]],total_asset_growth_rate[period[i]]]

            dic[period[i]] = {
                'TS股票代码': self.ts_code,
                '营收增长率': increase_rate[period[i]],
                '营业利润增长率': operating_rofit_growth_rate[period[i]],
                '净利润增长率': net_profit_growth_rate[period[i]],
                '固定资产增长率': growth_rate[period[i]],
                '总资产增长率': total_asset_growth_rate[period[i]]
            }
        dir_path = INFO_ANALYES_URL + os.sep + f"{self.ts_code}#{self.name}"
        FileTools.make_dir(dir_path)
        df.to_excel(dir_path + os.sep + f"{self.ts_code}#{self.name}#成长能力指标.xlsx")
        print(f"获取完成：{self.ts_code}的成长能力指标报表")
        return dic

    """
    获取评分表
    传入参数为一个字典列表
    字典结构参考 calculate对象方法的返回值
    """
    def get_score_to_excel(self,datas,df_name):
        print(f"正在：{self.ts_code}的{df_name}")
        score_dict = {}
        #重构数据结构
        for data in datas:
            score = self.get_score_info(data)
            for date, metrics in data.items():
                for key, value in metrics.items():
                    if key != 'TS股票代码':
                        if key not in score_dict:
                            score_dict[key] = {'data': [], 'score': score[key]}
                        score_dict[key]['data'].append(value)

        cols = list(datas[0].keys())
        cols.append("评分")
        rows = list(score_dict.keys())

        df_data = []
        for i, value in enumerate(score_dict.values()):
            df_data.append(value['data'])
            df_data[i].append(value['score'])

        df = pd.DataFrame(columns=cols,index=rows,data=df_data)
        average_score = df['评分'].mean()
        # 创建总分行
        total_score_row = pd.DataFrame(
            {'20191231': [None], '20181231': [None], '20171231': [None], '20161231': [None], '20151231': [None],
             '评分': [average_score]}, index=['总分']).astype(df.dtypes.to_dict())

        # 将总分行添加到原始DataFrame
        df = pd.concat([df, total_score_row])

        dir_path = INFO_ANALYES_URL + os.sep + f"{self.ts_code}#{self.name}"
        FileTools.make_dir(dir_path)
        df.to_excel(dir_path + os.sep + f"{self.ts_code}#{self.name}#{df_name}.xlsx")
        print(f"获取完成：{self.ts_code}的{df_name}")
        return dir_path + os.sep + f"{self.ts_code}#{self.name}#{df_name}.xlsx"





