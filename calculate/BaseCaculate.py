import os

import pandas as pd
from numpy import nan

from company.Company import Company
from config import INFO_ANALYES_URL
from tools.FileTools import FileTools


class BaseCaculate(Company):


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

        dir_path =INFO_ANALYES_URL + os.sep + f"{self.ts_code}"
        FileTools.make_dir(dir_path)
        df.to_excel(dir_path + os.sep + f"{self.ts_code}#{args[0]}.xlsx")
        return dic

    """
    利润表
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


        dir_path =INFO_ANALYES_URL + os.sep + f"{self.ts_code}"
        FileTools.make_dir(dir_path)
        df.to_excel(dir_path + os.sep + f"{self.ts_code}#{args[0]}.xlsx")
        return dic



    """
    资产负债表
    参数2/参数1
    agrs[列名，参数1，参数2]
    """
    def get_balance_two_args_division_to_excel(self,period,args):
        dic={}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', args[0]], index=[i for i in range(len(period))])
        for i in range(len(period)):
            b_df = pd.read_excel(self.get_balance_info_to_excel(period=period[i]))
            args1 = b_df.loc[0, args[1]]
            args2 = b_df.loc[0, args[2]]
            data = round(args2 / args1, 4)
            df.loc[i] = [self.ts_code, period[i], data]
            dic[period[i]] = data;


        dir_path =INFO_ANALYES_URL + os.sep + f"{self.ts_code}"
        FileTools.make_dir(dir_path)
        df.to_excel(dir_path + os.sep + f"{self.ts_code}#{args[0]}.xlsx")
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

        dir_path =INFO_ANALYES_URL + os.sep + f"{self.ts_code}"
        FileTools.make_dir(dir_path)
        df.to_excel(dir_path + os.sep + f"{self.ts_code}#{args[0]}.xlsx")
        return dic


    """
    资产负债表 四个参数
    运算规则
    (agrs[1]-agrs[2]-agrs[3])/args[4]
    """
    def get_balance_four_agrs_to_reduce_devision_excel(self,period,args):
        dic = {}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', args[0]], index=[i for i in range(len(period))])

        for i in range(len(period)):
            p_df = pd.read_excel(self.get_balance_info_to_excel(period=period[i]))
            args1 = p_df.loc[0, args[1]]
            args2 = p_df.loc[0, args[2]]
            args3 = p_df.loc[0, args[3]]
            args4 = p_df.loc[0, args[4]]

            data = round((args1-args2-args3) / args4, 4)
            df.loc[i] = [self.ts_code, period[i], data]
            dic[period[i]] = data;

        dir_path = INFO_ANALYES_URL + os.sep + f"{self.ts_code}"
        FileTools.make_dir(dir_path)
        df.to_excel(dir_path + os.sep + f"{self.ts_code}#{args[0]}.xlsx")
        return dic

    """
    利润表
    运算规则
    (agrs[1]-agrs[2])/agrs[3]
    其中 agrs[3] 来自上期的利润表
    """
    def get_profit_therr_agrs_reduce_devision(self,period,args):
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
            arg1 = p_df.loc[0, args[1]]

            #取上期的利润表
            arg2 = pd.read_excel(self.get_profit_info_to_excel(period=period[i + 1])).loc[0, args[2]]
            arg3 = pd.read_excel(self.get_profit_info_to_excel(period=period[i + 1])).loc[0, args[3]]

            data = round((arg1-arg2)/arg3, 4)
            df.loc[i] = [self.ts_code, period[i], data]
            dic[period[i]] = data;

        dir_path =INFO_ANALYES_URL + os.sep + f"{self.ts_code}"
        FileTools.make_dir(dir_path)
        df.to_excel(dir_path + os.sep + f"{self.ts_code}#{args[0]}.xlsx")
        return dic

    """
    负债表
    运算规则
    (agrs[1]-agrs[2])/agrs[3]
    其中 agrs[3] 来自上期的负债表
    """
    def get_banlance_therr_agrs_reduce_devision(self,period,args):
        dic = {}
        if len(period) == 1:
            for i in range(4):
                period.append(str(int(period[i]) - 10000))
        # 把最后一年的上一年也加入
        period.append(str(int(period[-1]) - 10000))
        df = pd.DataFrame(columns=['TS股票代码', '报告期', args[0]], index=[i for i in range(len(period) - 1)])
        for i in range(len(period) - 1):
            # 负债表
            p_df = pd.read_excel(self.get_balance_info_to_excel(period=period[i]))
            arg1 = p_df.loc[0, args[1]]

            #取上期的负债表
            arg2 = pd.read_excel(self.get_balance_info_to_excel(period=period[i + 1])).loc[0, args[2]]
            arg3 = pd.read_excel(self.get_balance_info_to_excel(period=period[i + 1])).loc[0, args[3]]

            data = round((arg1-arg2)/arg3, 4)
            df.loc[i] = [self.ts_code, period[i], data]
            dic[period[i]] = data;

        dir_path =INFO_ANALYES_URL + os.sep + f"{self.ts_code}"
        FileTools.make_dir(dir_path)
        df.to_excel(dir_path + os.sep + f"{self.ts_code}#{args[0]}.xlsx")
        return dic


    """
    评分
    入参为基本运算返回的字典
    返回值为字典
    如{'存货周转率': 100.0, '总资产周转率': 50.0, '应收账款周转率': 0.0}
    """
    def get_scire_info(self,data):
        num_columns = len(list(data.values())[0]) - 1
        result = [[] for _ in range(num_columns)]

        # 遍历每个日期的子字典
        for key in data.keys():
            sub_dict = data[key]
            values = list(sub_dict.values())[1:]
            for i, value in enumerate(values):
                result[i].append(value)
        keys = list(data[key].keys())[1:]
        ans = []
        for i in result:
            n = 0
            for j in range(len(i) - 1):
                if i[j] > i[j + 1] or i[j] == nan:
                    n = n + 1
            n = n / 4 * 100
            ans.append(n)
        dic = {}
        for i, key in enumerate(keys):
            dic[key] = ans[i]
        return dic

