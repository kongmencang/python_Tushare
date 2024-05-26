# 基于Python的财务分析框架
@茶泡饭（YK）
## 简介
基于Tushare提供的接口 ，利用python完成的一款自动化财务分析框架，能够将获取到的数据/计算出的数据缓存为excel表格，并生成图表且自动化生成分析报告<br>
包括 营业能力，运营能力，债偿能力，成长能力等四个方面的多项指标。并且能够获取同类型公司数据进行对比参考<br>
项目采用了jinja2实现HTML模版渲染，多家公司信息爬取时采用了多线程加速，pandas进行数据处理，matplotlib进行绘图<br>
## 使用方法
#### 本框架为全自动分析框架，仅需要用户配置需要分析的股票代码，报告开始的年份即可。
① 完整拉取本项目后 进入项目目录 pip install -r ./requirements.txt 安装所需环境<br>
② 配置config.py 的 PERIOD 和 TSCODE 即可<br>
③ 运行main.py  在项目目录下  python3 main.py 或 python main.py 又或者用ide打开后运行<br>
④ 打开report目录查看生成的报告<br>
## 项目结构
#### 整个项目其实比较乱（）
calculae包 负责运算各种参数 BaseCaculate封装了常用的参数计算方法 <br>
chart包封装了绘图方法 <br>
company包封装了爬取基础数据的方法，以及它是Caculate对象的父类 <br>
comparison包封装了基础的分析方法 <br>
img目录下存放的是生成的图片 <br>
info目录下存放的是生成的表格 <br>
report目录下存放的是生成的分析报告 <br>
templates目录下存放的是报告的html模版文件 <br>
tools包里封装了常用的工具类方法 <br>
congfig.py 为配置文件 <br>
main.py为核心逻辑文件 <br>

### 一点点碎碎念
因为时间关系所以整个结构较为混乱，对异常也没进行捕获，log全靠print
如有疑问移步俺的qq：1184507696
<br>

另：万穗爷给我的自信，让我吃饱了没事撑着写这玩意！
![万穗爷](./sui.png)
