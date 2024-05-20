from calculate.Calculate import Calculate
from config import TOKEN, PERIOD



calculate = Calculate(TOKEN, "600519.SH")



#
calculate.get_profitability_metrics_to_excel(PERIOD)
calculate.get_operational_capability_indicators_to_excel(PERIOD)
calculate.get_liquidity_ratio_to_excle(PERIOD)
calculate.get_growth_capacity_indicators_to_excel(PERIOD)
#ss