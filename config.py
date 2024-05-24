import os

TOKEN = "ad2353588285a75380ec022640cecf0519f399082be2170c5a8e354c"

PROJECT_URL = os.path.dirname(os.path.abspath(__file__))

INFO_PRIMITIVE_URL = PROJECT_URL + os.sep + "info" + os.sep + "primitive_info"

INFO_ANALYES_URL = PROJECT_URL + os.sep + "info" + os.sep + "analyes_info"

IMG_URL = PROJECT_URL + os.sep + "img"

PERIOD = ["20191231"]

SEAM_INDUSTRY_NUM = 10

SCORCE_TABLE_NAME = [
    "营业能力评分表",
    "运营能力评分表",
    "债偿能力评分表",
    "成长能力评分表"
]

TSCODE = "600519.SH"

"""
分析指标
可以删掉某些指标
如果添加指标，请在Calculate类中添加对应的指标计算，以及更其改组合方法
"""
ANALYES_ARGUMENT = {
    "营业能力": ["毛利率", "营业利润率", "净利润率", "ROE", "ROA", "EBIT"],
    "运营能力": ["存货周转率", "总资产周转率", "应收账款周转率"],
    "债偿能力": ["流动比率", "速动比率", "利息保障倍数", "资产负债率"],
    "成长能力": ["营收增长率","营业利润增长率","净利润增长率","固定资产增长率","总资产增长率"]
}

REPORT_SELF_ARGUMENT = {
    "营业能力": {
        "毛利率": {0.7: "极其暴利",0.5: "暴利", 0.3: "毛利率较高", 0.15: "毛利率正常", 0: "毛利率较低",-999: "亏损状态"},
        "营业利润率": {0.3: "极高", 0.2: "高", 0.1: "正常", 0: "低", -999: "亏损状态"},
        "净利润率": {0.2: "极高", 0.1: "高", 0.05: "正常", 0: "低", -999: "亏损状态"},
        "ROE": {0.2: "极高",0.15: "高",0.1: "正常",0.05: "低",0: "极低",-999: "亏损状态"},
        "ROA": {0.1: "极高", 0.07: "高",0.05: "正常",0.03: "低",0: "极低",-999: "亏损状态"},
        "EBIT": {0.2: "极高",0.15: "高",0.1: "正常",0.05: "低",0: "极低",-999: "亏损状态"},
    },
    "运营能力": {
        "存货周转率": {10: "极高", 5: "高", 3: "正常", 1: "低", 0: "极低"},
        "总资产周转率": {1: "高", 0.5: "正常", 0.3: "低", 0.1: "极低", 0: "极差"},
        "应收账款周转率": {30: "极高", 25: "高", 15: "较高", 10: "正常", 0: "极低"},
    },
    "债偿能力": {
        "流动比率": {2: "极强",1.5: "强",1: "正常",0.8: "较弱",0.5: "弱",0: "极弱"},
        "速动比率": {1.5: "极强",1: "强",0.8: "正常",0.6: "较弱",0.4: "弱",0: "极弱"},
        "利息保障倍数": {5: "极强",3: "强",1.5: "正常",1: "较弱",0: "极弱",-999: "无法偿付"},
        "资产负债率": {1: "偿债风险很大",0.6: "企业偿债风险较大",0.4: "正常",0.2: "运用外部资金的能力相对较弱",0: "运用外部资金的能力相对很弱",-999: "资不抵债"},
    },
    "成长能力": {
        "营收增长率": {0.3: "极高", 0.2: "高", 0.1: "正常", 0: "低", -999: "负增长"},
        "营业利润增长率": {0.3: "极高",0.2: "高",0.1: "正常",0: "低",-999: "负增长"},
        "净利润增长率": {0.3: "极高", 0.2: "高", 0.1: "正常", 0: "低", -999: "负增长"},
        "固定资产增长率": {0.2: "极高",0.1: "高",0.05: "正常",0: "低",-999: "负增长" },
        "总资产增长率": {0.2: "极高",0.1: "高",0.05: "正常",0: "低",-999: "负增长"}
    }
}

SELF_RSCORCE_COMENT = {
    "营业能力评分表": {
        100: "营业能力得分反映了公司的盈利能力和成本控制水平完美",
        80: "营业能力得分反映了公司的盈利能力和成本控制水平较高",
        60: "营业能力得分反映了公司的盈利能力和成本控制水平正常",
        40: "营业能力得分反映了公司的盈利能力和成本控制水平一般",
        20: "营业能力得分反映了公司的盈利能力和成本控制水平较低",
        0: "营业能力得分反映了公司的盈利能力和成本控制水平很低"
    },
    "运营能力评分表": {
        100: "运营能力得分反映了公司资产的使用效率和周转速度完美",
        80: "运营能力得分反映了公司资产的使用效率和周转速度较高",
        60: "运营能力得分反映了公司资产的使用效率和周转速度正常",
        40: "运营能力得分反映了公司资产的使用效率和周转速度一般",
        20: "运营能力得分反映了公司资产的使用效率和周转速度较低",
        0: "运营能力得分反映了公司资产的使用效率和周转速度很低"
    },
    "债偿能力评分表": {
        100: "债偿能力得分反映了公司偿还短期和长期债务的能力完美",
        80: "债偿能力得分反映了公司偿还短期和长期债务的能力较高",
        60: "债偿能力得分反映了公司偿还短期和长期债务的能力正常",
        40: "债偿能力得分反映了公司偿还短期和长期债务的能力一般",
        20: "债偿能力得分反映了公司偿还短期和长期债务的能力较低",
        0: "债偿能力得分反映了公司偿还短期和长期债务的能力很低"
    },
    "成长能力评分表": {
        100: "成长能力得分反映了公司在收入、利润和资产方面的增长完美",
        80: "成长能力得分反映了公司在收入、利润和资产方面的增长较高",
        60: "成长能力得分反映了公司在收入、利润和资产方面的增长正常",
        40: "成长能力得分反映了公司在收入、利润和资产方面的增长一般",
        20: "成长能力得分反映了公司在收入、利润和资产方面的增长较低",
        0: "成长能力得分反映了公司在收入、利润和资产方面的增长很低"
    }
}
SELF_TOTAL_SCORCE_COMENT = {
    100: "总体得分反映了公司在营业、运营、债偿和成长方面的增长完美",
    80: "总体得分反映了公司在营业、运营、债偿和成长方面的增长较高",
    60: "总体得分反映了公司在营业、运营、债偿和成长面的增长正常",
    40: "总体得分反映了公司在营业、运营、债偿和成长方面的增长一般",
    20: "总体得分反映了公司在营业、运营、债偿和成长方面的增长较低",
    0: "总体得分反映了公司在营业、运营、债偿和成长方面的增长很低"
}