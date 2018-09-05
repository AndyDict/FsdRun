from fsdrun.fsdData.fsdDataBase import *
from fsdrun.fsdData.fsdDataConst import CT
import pandas as pd
import struct


class TdxData(DataModel):
    """
    通达信接口
    """

    def __init__(self, softdatapth="D:\\new_tdx\\"):
        """
        通达信接口
        :param softdatapth: 通达信软件目录
        """
        super(DataModel, self).__init__()
        self.tdx_path = softdatapth
        self.tdxStockDayPthIn = (softdatapth + CT.TDX_STOCKS_DATAPTH_DAY[0], softdatapth + CT.TDX_STOCKS_DATAPTH_DAY[1])
        self.tdxStockMinPthIn = (softdatapth + CT.TDX_STOCKS_DATAPTH_MIN[0], softdatapth + CT.TDX_STOCKS_DATAPTH_MIN[1])
        self.tdxStockCsvPthOut = (self.basepth + CT.SDAY_DATACSVPTH, self.basepth + CT.SMIN_DATACSVPTH)
        self.columns_form = ["datetime", "open", "high", "low", "close", "volumn", "amount"]

    def stockDaysBar(self):
        """
        获取通达信中day文件内行情数据。
        输出格式："datetime", "open", "high", "low", "close", "volumn", "amount"
        输出路径：日线为例: CT.SDAY_DATACSVPTH = "\\data\\csv\\tdxdata\\stocks\\day\\"
        DAY文件格式说明:
            文件名即股票代码
            每32个字节为一天数据
            每4个字节为一个字段，每个字段内低字节在前
            00 ~ 03 字节：年月日, 整型
            04 ~ 07 字节：开盘价*100， 整型
            08 ~ 11 字节：最高价*100,  整型
            12 ~ 15 字节：最低价*100,  整型
            16 ~ 19 字节：收盘价*100,  整型
            20 ~ 23 字节：成交额（元），float型
            24 ~ 27 字节：成交量（股），整型
            28 ~ 31 字节：上日收盘*100, 整型
        """
        for i_change in self.tdxStockDayPthIn:
            filenamelst = [i_change + i_filename for i_filename in os.listdir(i_change)]
            for stockfilename in filenamelst:
                filename_ache = stockfilename.split("\\")[-1].split(".")[0]
                ofile = open(stockfilename, 'rb')
                buf = ofile.read()
                ofile.close()
                num = len(buf)
                no = num / 32
                b = 0
                e = 32
                dataf_ache = pd.DataFrame(columns=self.columns_form)
                timeplst = []
                openplst = []
                highplst = []
                lowplst = []
                closeplst = []
                volplst = []
                amoplst = []
                for i in range(int(no)):
                    a = struct.unpack('IIIIIfII', buf[b:e])
                    year = int(a[0] / 10000)
                    m = int((a[0] % 10000) / 100)
                    month = str(m)
                    if m < 10:
                        month = "0" + month
                    d = (a[0] % 10000) % 100
                    day = str(d)
                    if d < 10:
                        day = "0" + str(d)
                    timeplst.append(str(year) + "-" + month + "-" + day + " 15:00:00")
                    openplst.append(a[1] / 100.0)
                    highplst.append(a[2] / 100.0)
                    lowplst.append(a[3] / 100.0)
                    closeplst.append(a[4] / 100.0)
                    amoplst.append(a[5] / 10.0)
                    volplst.append(a[6])
                    b = b + 32
                    e = e + 32
                dataf_ache[self.columns_form[0]] = timeplst
                dataf_ache[self.columns_form[1]] = openplst
                dataf_ache[self.columns_form[2]] = highplst
                dataf_ache[self.columns_form[3]] = lowplst
                dataf_ache[self.columns_form[4]] = closeplst
                dataf_ache[self.columns_form[5]] = volplst
                dataf_ache[self.columns_form[6]] = amoplst
                dataf_ache.to_csv(self.tdxStockCsvPthOut[0] + filename_ache + ".csv", index=0)

    def stockMinsBar(self):
        """
        获取通达信中MIN文件内行情数据。
        输出格式："datetime", "open", "high", "low", "close", "volumn", "amount"
        输出路径：日线为例: CT.SDAY_DATACSVPTH = "\\data\\csv\\tdxdata\\stocks\\min\\"
        LC1\LC5文件格式说明:
            通达信5分钟线*.lc5文件和*.lc1文件
                文件名即股票代码
                每32个字节为一个5分钟数据，每字段内低字节在前
                00 ~ 01 字节：日期，整型，设其值为num，则日期计算方法为：
                              year=floor(num/2048)+2004;
                              month=floor(mod(num,2048)/100);
                              day=mod(mod(num,2048),100);
                02 ~ 03 字节： 从0点开始至目前的分钟数，整型
                04 ~ 07 字节：开盘价，float型
                08 ~ 11 字节：最高价，float型
                12 ~ 15 字节：最低价，float型
                16 ~ 19 字节：收盘价，float型
                20 ~ 23 字节：成交额，float型
                24 ~ 27 字节：成交量（股），整型
                28 ~ 31 字节：（保留）
        """
        for i_change in self.tdxStockMinPthIn:
            filenamelst = [i_change + i_filename for i_filename in os.listdir(i_change)]
            for stockfilename in filenamelst:
                filename_ache = stockfilename.split("\\")[-1].split(".")[0]
                ofile = open(stockfilename, 'rb')
                buf = ofile.read()
                ofile.close()
                num = len(buf)
                no = num / 32
                b = 0
                e = 32
                dataf_ache = pd.DataFrame(columns=self.columns_form)
                timeplst = []
                openplst = []
                highplst = []
                lowplst = []
                closeplst = []
                volplst = []
                amoplst = []
                for i in range(int(no)):
                    a = struct.unpack('hhfffffii', buf[b:e])
                    year = int(a[0] / 2048) + 2004
                    m = int(a[0] % 2048 / 100)
                    month = str(m)
                    if m < 10:
                        month = "0" + month
                    d = int(a[0] % 2048 % 100)
                    day = str(d)
                    if d < 10:
                        day = "0" + str(d)
                    h = int(a[1] / 60)
                    hour = str(h)
                    if h < 10:
                        hour = "0" + str(h)
                    mm = int(a[1] % 60)
                    minutes = str(mm) + ":00"
                    if mm < 10:
                        minutes = "0" + str(mm) + ":00"
                    timeplst.append(str(year) + "-" + month + "-" + day + " " + hour + ":" + minutes)
                    openplst.append(round(a[2], 2))
                    highplst.append(round(a[3], 2))
                    lowplst.append(round(a[4], 2))
                    closeplst.append(round(a[5], 2))
                    amoplst.append(round(a[6], 2))
                    volplst.append(round(a[7], 2))
                    b = b + 32
                    e = e + 32
                dataf_ache[self.columns_form[0]] = timeplst
                dataf_ache[self.columns_form[1]] = openplst
                dataf_ache[self.columns_form[2]] = highplst
                dataf_ache[self.columns_form[3]] = lowplst
                dataf_ache[self.columns_form[4]] = closeplst
                dataf_ache[self.columns_form[5]] = volplst
                dataf_ache[self.columns_form[6]] = amoplst
                dataf_ache.to_csv(self.tdxStockCsvPthOut[1] + filename_ache + ".csv", index=0)


if __name__ == '__main__':
    mycsv = TdxData()
    # mycsv.stockDaysBar()
    mycsv.stockMinsBar()
