import time
from fsdrun.fsdData.fsdDataConst import CT
from fsdrun.fsdData.sqldata.sqldata import *
if __name__ == '__main__':
    # stocklst = SqlData().csv_split("E:\\fsdrun\\data\\csv\\sqldatacsv\\stock_1day_his2.csv")
    # SqlData().mysql_stockinfo()
    wday = time.localtime(time.time()).tm_wday
    if wday == 6:
        """转化日线数据"""
        # SqlData().csv_split(CT.DAYCSVALLDATA + "stock_1day_his2.csv")
        """转换小时数据"""
        # SqlData().csv_split(CT.DAYCSVALLDATA + "stock_1hou_his2.csv", fileType="sqlHour")
        """提取股票信息"""
        # SqlData().mysql_stockinfo()
        """转化day数据为pkl格式"""
        SqlData().pthcsv_pkl(CT.DAYCSVSINGLEDATA)
        """转化hour数据为pkl格式"""
        # SqlData().pthcsv_pkl(CT.HOURCSVSINGLEDATA)
