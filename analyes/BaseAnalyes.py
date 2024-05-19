import os

import pandas as pd

from company.Company import Company
from config import INFO_ANALYES_URL


class BaseAnalyes(Company):


    """
    （参数1-参数2）/参数1
    agrs[列名，参数1，参数2]
    """
    def profit_sheet_two_agrs_reduce_division_to_excel(self,period,args):
        dic = {}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', args[0]], index=[i for i in range(len(period))])
        for i in range(len(period)):
            p_df = pd.read_excel(self.get_profit_info_to_excel(period=period[i]))
            args1 = p_df.loc[0, args[1]]
            args2 = p_df.loc[0, args[2]]
            data = round((args1 - args2) / args1, 4)
            dic[period[i]] = data;
            df.loc[i] = [self.ts_code, period[i], data]
        df.to_excel(INFO_ANALYES_URL + os.sep + f"{self.ts_code}#{args[0]}.xlsx")
        return dic

    """
    参数2/参数1
    agrs[列名，参数1，参数2]
    """
    def get_profit_two_args_division_to_excel(self,period,args):
        dic={}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', args[0]], index=[i for i in range(len(period))])
        for i in range(len(period)):
            p_df = pd.read_excel(self.get_profit_info_to_excel(period=period[i]))
            # 营业收入
            args1 = p_df.loc[0, args[1]]
            args2 = p_df.loc[0, args[2]]
            data = round(args2 / args1, 4)
            df.loc[i] = [self.ts_code, period[i], data]
            dic[period[i]] = data;
        df.to_excel(INFO_ANALYES_URL + os.sep + f"{self.ts_code}#{args[0]}.xlsx")
        return dic


    """
    三个参数的运算
    第一个参数从利润表获取
    第二个参数从当年的负债表获取
    第三个参数从去年的负债表获取
    运算规则为:arg[1]/((arg[2]+agr[3])/2 )
    """
    def get_profit_balance_three_agrs_to_excel(self, period,args):
        dic = {}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        # 把最后一年的上一年也加入
        period.append(str(int(period[-1]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', args[0]], index=[i for i in range(len(period) - 1)])
        for i in range(len(period) - 1):
            # 利润表
            p_df = pd.read_excel(self.get_profit_info_to_excel(period=period[i]))
            # 负债表
            b_df = pd.read_excel(self.get_balance_info_to_excel(period=period[i]))

            arg1 = p_df.loc[0, args[1]]
            arg2 = b_df.loc[0, args[2]]


            arg3 = pd.read_excel(self.get_balance_info_to_excel(period=period[i + 1])).loc[
                0, args[3]]
            data = round(arg1 / ((arg2 + arg3) / 2), 4)
            df.loc[i] = [self.ts_code, period[i], data]
            dic[period[i]] = data;

        df.to_excel(INFO_ANALYES_URL + os.sep + f"{self.ts_code}#{args[0]}.xlsx")
        return dic
