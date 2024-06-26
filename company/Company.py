import os
import time

import pandas as pd
import tushare as ts

from config import INFO_PRIMITIVE_URL, SLEEP_TIME
from tools.FileTools import FileTools


class Company:
    """
    公司股票类
    """

    def __init__(self, tushare_token, ts_code):
        self.__pro = ts.pro_api(tushare_token)
        self.ts_code = ts_code
        self.get_ts_info_to_excel()
        self.get_base_info_to_excel()
        print(
            f"创建股票代码：{self.ts_code} 公司名:{self.fullname} 行业:{self.industry} 对象"
        )

    # 拉取公司基本信息
    def get_base_info_to_excel(self):
        print(f"获取{self.ts_code} 的公司基本信息")
        df = self.__pro.stock_company(
            **{
                "ts_code": self.ts_code,
                "exchange": "",
                "status": "",
                "limit": "",
                "offset": "",
            },
            fields=[
                "ts_code",
                "exchange",
                "chairman",
                "manager",
                "secretary",
                "reg_capital",
                "setup_date",
                "province",
                "city",
                "website",
                "email",
                "employees",
                "main_business",
                "introduction",
                "office",
                "ann_date",
                "business_scope",
            ],
        )
        self.introduction = df["introduction"].iloc[0]
        dir_path = INFO_PRIMITIVE_URL + os.sep + f"{self.ts_code}-{self.name}"
        FileTools.make_dir(dir_path)
        df.to_excel(dir_path + os.sep + f"{self.ts_code}-{self.name}-公司基本信息.xlsx")
        return dir_path + os.sep + f"{self.ts_code}-{self.name}-公司基本信息.xlsx"

    # 拉取股票基本信息
    def get_ts_info_to_excel(self):
        print(f"获取{self.ts_code} 的股票基本信息")
        df = self.__pro.stock_basic(
            **{
                "ts_code": self.ts_code,
                "name": "",
                "exchange": "",
                "market": "",
                "is_hs": "",
                "list_status": "",
                "limit": "",
                "offset": "",
            },
            fields=[
                "ts_code",
                "fullname",
                "symbol",
                "name",
                "area",
                "industry",
                "enname",
                "cnspell",
                "market",
                "exchange",
                "curr_type",
                "list_status",
                "list_date",
                "delist_date",
                "is_hs",
                "act_name",
                "act_ent_type",
            ],
        )
        self.industry = df["industry"].iloc[0]
        self.fullname = df["fullname"].iloc[0]
        self.area = df["area"].iloc[0]
        self.name = df["name"].iloc[0]
        dir_path = INFO_PRIMITIVE_URL + os.sep + f"{self.ts_code}-{self.name}"
        FileTools.make_dir(dir_path)
        df.to_excel(dir_path + os.sep + f"{self.ts_code}-{self.name}-股票基本信息.xlsx")
        return dir_path + os.sep + f"{self.ts_code}-{self.name}-股票基本信息.xlsx"

    # 利润表
    def get_profit_info_to_excel(
        self,
        ann_date="",
        f_ann_date="",
        start_date="",
        end_date="",
        period="",
        report_type="",
        comp_type="",
        is_calc="",
        limit="",
        offset="",
    ):

        print(f"获取{self.ts_code}:{period}:的利润表")
        dir_path = INFO_PRIMITIVE_URL + os.sep + f"{self.ts_code}-{self.name}"
        path = dir_path + os.sep + f"{self.ts_code}-{self.name}-{period}-利润表.xlsx"
        if FileTools.get_dir_is_exist(path):
            print("已存在")
            return path
        df = self.__pro.income(
            **{
                "ts_code": self.ts_code,
                "ann_date": ann_date,
                "f_ann_date": f_ann_date,
                "start_date": start_date,
                "end_date": end_date,
                "period": period,
                "report_type": report_type,
                "comp_type": comp_type,
                "is_calc": is_calc,
                "limit": limit,
                "offset": offset,
            },
            fields=[
                "ts_code",
                "ann_date",
                "f_ann_date",
                "end_date",
                "report_type",
                "comp_type",
                "end_type",
                "basic_eps",
                "diluted_eps",
                "total_revenue",
                "revenue",
                "int_income",
                "prem_earned",
                "comm_income",
                "n_commis_income",
                "n_oth_income",
                "n_oth_b_income",
                "prem_income",
                "out_prem",
                "une_prem_reser",
                "reins_income",
                "n_sec_tb_income",
                "n_sec_uw_income",
                "n_asset_mg_income",
                "oth_b_income",
                "fv_value_chg_gain",
                "invest_income",
                "ass_invest_income",
                "forex_gain",
                "total_cogs",
                "oper_cost",
                "int_exp",
                "comm_exp",
                "biz_tax_surchg",
                "sell_exp",
                "admin_exp",
                "fin_exp",
                "assets_impair_loss",
                "prem_refund",
                "compens_payout",
                "reser_insur_liab",
                "div_payt",
                "reins_exp",
                "oper_exp",
                "compens_payout_refu",
                "insur_reser_refu",
                "reins_cost_refund",
                "other_bus_cost",
                "operate_profit",
                "non_oper_income",
                "non_oper_exp",
                "nca_disploss",
                "total_profit",
                "income_tax",
                "n_income",
                "n_income_attr_p",
                "minority_gain",
                "oth_compr_income",
                "t_compr_income",
                "compr_inc_attr_p",
                "compr_inc_attr_m_s",
                "ebit",
                "ebitda",
                "insurance_exp",
                "undist_profit",
                "distable_profit",
                "rd_exp",
                "fin_exp_int_exp",
                "fin_exp_int_inc",
                "transfer_surplus_rese",
                "transfer_housing_imprest",
                "transfer_oth",
                "adj_lossgain",
                "withdra_legal_surplus",
                "withdra_legal_pubfund",
                "withdra_biz_devfund",
                "withdra_rese_fund",
                "withdra_oth_ersu",
                "workers_welfare",
                "distr_profit_shrhder",
                "prfshare_payable_dvd",
                "comshare_payable_dvd",
                "capit_comstock_div",
                "continued_net_profit",
                "update_flag",
                "amodcost_fin_assets",
                "total_opcost",
                "oth_impair_loss_assets",
                "net_expo_hedging_benefits",
                "credit_impa_loss",
                "end_net_profit",
                "asset_disp_income",
                "oth_income",
                "net_after_nr_lp_correct",
            ],
        )
        dir_path = INFO_PRIMITIVE_URL + os.sep + f"{self.ts_code}-{self.name}"
        FileTools.make_dir(dir_path)
        df.to_excel(
            dir_path + os.sep + f"{self.ts_code}-{self.name}-{period}-利润表.xlsx"
        )
        time.sleep(SLEEP_TIME)
        return path

    # 负债表
    def get_balance_info_to_excel(
        self,
        ann_date="",
        f_ann_date="",
        start_date="",
        end_date="",
        period="",
        report_type="",
        comp_type="",
        is_calc="",
        limit="",
        offset="",
    ):
        print(f"获取{self.ts_code}:{period}:的负债表")
        dir_path = INFO_PRIMITIVE_URL + os.sep + f"{self.ts_code}-{self.name}"
        path = dir_path + os.sep + f"{self.ts_code}-{self.name}-{period}-负债表.xlsx"
        if FileTools.get_dir_is_exist(path):
            print("已存在")
            return path
        df = self.__pro.balancesheet(
            **{
                "ts_code": self.ts_code,
                "ann_date": ann_date,
                "f_ann_date": f_ann_date,
                "start_date": start_date,
                "end_date": end_date,
                "period": period,
                "report_type": report_type,
                "comp_type": comp_type,
                "is_calc": is_calc,
                "limit": limit,
                "offset": offset,
            },
            fields=[
                "ts_code",
                "ann_date",
                "f_ann_date",
                "end_date",
                "report_type",
                "comp_type",
                "end_type",
                "total_share",
                "cap_rese",
                "undistr_porfit",
                "surplus_rese",
                "special_rese",
                "money_cap",
                "trad_asset",
                "notes_receiv",
                "accounts_receiv",
                "oth_receiv",
                "prepayment",
                "div_receiv",
                "int_receiv",
                "inventories",
                "amor_exp",
                "nca_within_1y",
                "sett_rsrv",
                "loanto_oth_bank_fi",
                "premium_receiv",
                "reinsur_receiv",
                "reinsur_res_receiv",
                "pur_resale_fa",
                "oth_cur_assets",
                "total_cur_assets",
                "fa_avail_for_sale",
                "htm_invest",
                "lt_eqt_invest",
                "invest_real_estate",
                "time_deposits",
                "oth_assets",
                "lt_rec",
                "fix_assets",
                "cip",
                "const_materials",
                "fixed_assets_disp",
                "produc_bio_assets",
                "oil_and_gas_assets",
                "intan_assets",
                "r_and_d",
                "goodwill",
                "lt_amor_exp",
                "defer_tax_assets",
                "decr_in_disbur",
                "oth_nca",
                "total_nca",
                "cash_reser_cb",
                "depos_in_oth_bfi",
                "prec_metals",
                "deriv_assets",
                "rr_reins_une_prem",
                "rr_reins_outstd_cla",
                "rr_reins_lins_liab",
                "rr_reins_lthins_liab",
                "refund_depos",
                "ph_pledge_loans",
                "refund_cap_depos",
                "indep_acct_assets",
                "client_depos",
                "client_prov",
                "transac_seat_fee",
                "invest_as_receiv",
                "total_assets",
                "lt_borr",
                "st_borr",
                "cb_borr",
                "depos_ib_deposits",
                "loan_oth_bank",
                "trading_fl",
                "notes_payable",
                "acct_payable",
                "adv_receipts",
                "sold_for_repur_fa",
                "comm_payable",
                "payroll_payable",
                "taxes_payable",
                "int_payable",
                "div_payable",
                "oth_payable",
                "acc_exp",
                "deferred_inc",
                "st_bonds_payable",
                "payable_to_reinsurer",
                "rsrv_insur_cont",
                "acting_trading_sec",
                "acting_uw_sec",
                "non_cur_liab_due_1y",
                "oth_cur_liab",
                "total_cur_liab",
                "bond_payable",
                "lt_payable",
                "specific_payables",
                "estimated_liab",
                "defer_tax_liab",
                "defer_inc_non_cur_liab",
                "oth_ncl",
                "total_ncl",
                "depos_oth_bfi",
                "deriv_liab",
                "depos",
                "agency_bus_liab",
                "oth_liab",
                "prem_receiv_adva",
                "depos_received",
                "ph_invest",
                "reser_une_prem",
                "reser_outstd_claims",
                "reser_lins_liab",
                "reser_lthins_liab",
                "indept_acc_liab",
                "pledge_borr",
                "indem_payable",
                "policy_div_payable",
                "total_liab",
                "treasury_share",
                "ordin_risk_reser",
                "forex_differ",
                "invest_loss_unconf",
                "minority_int",
                "total_hldr_eqy_exc_min_int",
                "total_hldr_eqy_inc_min_int",
                "total_liab_hldr_eqy",
                "lt_payroll_payable",
                "oth_comp_income",
                "oth_eqt_tools",
                "oth_eqt_tools_p_shr",
                "lending_funds",
                "acc_receivable",
                "st_fin_payable",
                "payables",
                "hfs_assets",
                "hfs_sales",
                "cost_fin_assets",
                "fair_value_fin_assets",
                "contract_assets",
                "contract_liab",
                "accounts_receiv_bill",
                "accounts_pay",
                "oth_rcv_total",
                "fix_assets_total",
                "cip_total",
                "oth_pay_total",
                "long_pay_total",
                "debt_invest",
                "oth_debt_invest",
                "update_flag",
            ],
        )

        dir_path = INFO_PRIMITIVE_URL + os.sep + f"{self.ts_code}-{self.name}"
        FileTools.make_dir(dir_path)
        df.to_excel(
            dir_path + os.sep + f"{self.ts_code}-{self.name}-{period}-负债表.xlsx"
        )
        time.sleep(SLEEP_TIME)
        return path

    # 获取同行业股票代码列表
    def get_seam_industry_list(self):
        print(f"获取{self.ts_code}:的同行业股票代码列表")
        df = self.__pro.stock_basic(
            **{
                "ts_code": "",
                "name": "",
                "exchange": "",
                "market": "",
                "is_hs": "",
                "list_status": "L",
                "limit": "",
                "offset": "",
            },
            fields=["ts_code", "industry", "fullname"],
        )
        # 筛选
        df = df[(df["industry"] == self.industry) & (df["ts_code"] != self.ts_code)]

        dir_path = INFO_PRIMITIVE_URL + os.sep + f"{self.ts_code}-{self.name}"
        FileTools.make_dir(dir_path)
        df.to_excel(
            dir_path + os.sep + f"{self.ts_code}-{self.name}-同行业公司股票代码表.xlsx"
        )
        return (
            dir_path + os.sep + f"{self.ts_code}-{self.name}-同行业公司股票代码表.xlsx"
        )
