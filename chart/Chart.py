
from chart.BaseChart import BaseChart


class Chart(BaseChart):
    #根据字典内容批量生成折线图
    def get_all_line_chart(self,ts_code,company_name,data):
        #年份
        yearkeys= list(data.keys())
        yearkeys.reverse()
        #参数
        parameters= list(data[yearkeys[0]].keys())
        years=[i[0:4] for i in yearkeys] #截取年份
        for parameter in parameters[1:]:
            d=[]
            for yearkey in yearkeys:
                d.append(data[yearkey][parameter])
            self.get_line_chart(ts_code=ts_code,company_name=company_name,label=parameter,x=years,y=d)











