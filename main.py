from analyes.Analyes import Analyes
from config import TOKEN, PERIOD
from company.Company import Company

# company = Company(TOKEN, "300467.SZ")
# company.get_base_info_to_excel()
# company.get_profit_info_to_excel(period="20231231")
# company.get_balance_info_to_excel(period="20231231")


# analyes =Analyes(TOKEN,"300467.SZ")
analyes =Analyes(TOKEN,"600519.SH")
#analyes =Analyes(TOKEN,"000858.SZ")
#
# analyes.get_analyse_gross_margin_to_excel(["20231231"])
# analyes.get_analyse_operating_margin_to_excel(["20231231"])
# analyes.get_net_profit_margin_to_excel(["20231231"])
#analyes.get_net_ROE_to_excel(["20191231"])
#analyes.get_analyse_EBIT_to_excel(["20191231"])
#analyes.get_profitability_metrics_to_excel(["20191231"])
#analyes.get_stock_turnover_to_excel(["20191231"])

analyes.get_operational_capability_indicators_to_excel(PERIOD)