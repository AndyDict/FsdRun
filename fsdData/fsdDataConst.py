# coding:utf-8
import os
class _const:
    """
    自定义常量：（1）命名全部大写；（2）值不可修改
    """

    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__.keys():
            raise self.ConstError('Can not change const.{0}'.format(name))
        if not name.isupper():
            raise self.ConstCaseError(
                'const name {0} is not all uppercase.'.format(name))
        self.__dict__[name] = value

CT = _const()
absbasepth = os.path.abspath("../..") + "\\"

"""
通达信常量
"""

CT.BASEPTH = absbasepth
CT.DAYCSVALLDATA = CT.BASEPTH + "data\\csv\\sqldatacsv\\stockcsv\\"
CT.DAYCSVSINGLEDATA = CT.DAYCSVALLDATA + "sqlDay\\"
CT.HOURCSVSINGLEDATA = CT.DAYCSVALLDATA + "sqlHour\\"
# 通达信目录
CT.TDX_STOCKS_DATAPTH_DAY = ["vipdoc\\sh\\lday\\", "vipdoc\\sz\\lday\\"]
CT.TDX_STOCKS_DATAPTH_MIN = ["vipdoc\\sh\\fzline\\", "vipdoc\\sz\\fzline\\"]
CT.TDX_FUTURE_DATAPTH_DAY = "vipdoc\\ds\\lday\\"
CT.TDX_FUTURE_DATAPTH_MIN = "vipdoc\\ds\\fzline\\"

# CSV目录
CT.SDAY_DATACSVPTH = "\\data\\csv\\tdxdata\\stocks\\day\\"
CT.SMIN_DATACSVPTH = "\\data\\csv\\tdxdata\\stocks\\min\\"


"""SQL语句"""
CT.SQL_QUERY_ALLSTOCK = "SELECT DISTINCT(股票代码) FROM" + " stock_1day_his2"


"""标准字符串"""
CT.TIME_FORMAT = ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S")
