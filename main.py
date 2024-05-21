from numpy import nan

from calculate.Calculate import Calculate
from chart.Chart import Chart
from config import TOKEN, PERIOD



calculate = Calculate(TOKEN, "600519.SH")



#
data=[
# #营业能力
calculate.get_profitability_metrics_to_excel(PERIOD),
# #运营能力
calculate.get_operational_capability_indicators_to_excel(PERIOD),
# #债偿能力
calculate.get_solvency_indicators_to_excel(PERIOD),
# #成长能力
calculate.get_growth_capacity_indicators_to_excel(PERIOD)
]
#
#
# # cart = Chart()
# # for i in data:
# #     cart.get_all_line_chart("600519.SH",i)



for i in data:
      print(calculate.get_scire_info(i))




