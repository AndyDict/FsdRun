# -*- coding:utf-8 -*-
from fsdrun.fsdData.fsdDataBase import *
import pymysql as mdb
from fsdrun.fsdData.fsdDataConst import CT
import pandas as pd
import json

class SqlData(DataModel):
    def __init__(self, host="192.168.0.112", port=3306, userid="user_cl2", pwd="Zho9503", source="gsgl",
                 tablename="stock_1day_his2"):
        """
        :param host:        # 主机名或者IP地址
        :param port:        # 端口
        :param userid:      # 用户名
        :param pwd:         # 密码
        :param source:      # 连接的数据库名称
        :param tablename:   # 查询的表名
        """
        super().__init__()
        self.db_host = host
        self.db_port = port
        self.db_user = userid
        self.db_passwd = pwd
        self.db_name = source
        self.TableName = tablename

    def mysql_stocklst(self):
        """
        获取数据库A股的股票列表
        :return:
        """
        CodeList = []

        DB = mdb.connect(self.db_host, self.db_user, self.db_passwd, self.db_name, self.db_port, charset="utf8")
        sql1 = CT.SQL_QUERY_ALLSTOCK
        results = None
        try:
            Cursor = DB.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
            Cursor.execute(sql1)  # 使用 execute()  方法执行 SQL 查询
            results = Cursor.fetchall()  # 获取所有查询结果
        except SystemError as e:
            print(e, "Error: unable to fetch data")
        DB.close()  # 关闭数据库连接
        for i in results:
            CodeList.append(i[0])
        return CodeList

    def mysql_transform_pkl(self, Start_Datetime="2010-01-01 15:00:00"):
        """
        Mysql数据库转换成pkl
        :param Start_Datetime:
        :return:
        """
        CodeList = self.mysql_stocklst()
        # 打开数据库连接
        DB = mdb.connect(self.db_host, self.db_user, self.db_passwd, self.db_name, self.db_port, charset="utf8")

        for Code in CodeList:
            """查询的字段"""
            Select_Fields = "股票代码,cast(时间 as char),K_开盘价,K_收盘价,K_最高价,K_最低价,K_成交量,K_成交额,涨幅,K_换手率"
            sql = "SELECT {} FROM {} where 股票代码={} and 时间>=DATE_FORMAT('{}','%Y-%m-%d %H:%i:%s')".format(
                Select_Fields, self.TableName, Code, Start_Datetime)
            try:
                Cursor = DB.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
                Cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
                results = Cursor.fetchall()  # 获取所有查询结果
                print("成功：", Code)
            except SystemError as e:
                print(Code, e, "Error: unable to fetch data")

            """转换格式"""
            StockOBJ = dict()
            open_dict = dict()
            high_dict = dict()
            low_dict = dict()
            close_dict = dict()
            vol_dict = dict()
            amount_dict = dict()
            p_change_dict = dict()
            turnover_dict = dict()
            if len(results):
                for row in results:
                    list_1 = list(row)
                    """将dattime转换时间戳(秒)"""
                    datetime = time.strptime(list_1[1], '%Y-%m-%d %H:%M:%S')
                    int_datetime = int(time.mktime(datetime))
                    """转换成字典{'1375097400000': 15.23, '1375106400000': 15.13}......"""
                    open_dict[int_datetime] = list_1[2]
                    close_dict[int_datetime] = list_1[3]
                    high_dict[int_datetime] = list_1[4]
                    low_dict[int_datetime] = list_1[5]
                    vol_dict[int_datetime] = list_1[6]
                    amount_dict[int_datetime] = list_1[7]
                    p_change_dict[int_datetime] = list_1[8]
                    turnover_dict[int_datetime] = list_1[9]

                """
                转换成{'code': '000001', 'open': {'1375097400': 15.23, ...} , 'close': {'1375097400': 15.23, ...} ...}
                """
                StockOBJ["open"] = open_dict
                StockOBJ["close"] = close_dict
                StockOBJ["high"] = high_dict
                StockOBJ["low"] = low_dict
                StockOBJ["vol"] = vol_dict
                StockOBJ["amount"] = amount_dict
                StockOBJ["p_change"] = p_change_dict
                StockOBJ["turnover"] = turnover_dict

                """转换成pkl格式"""
                self.data_topkl(Code, StockOBJ)
            else:
                print(Code, "无数据")

    def csv_simple(self, csvpth):
        newdf = pd.DataFrame(columns=["datetime", "code", "name", "open", "high", "low", "close", "vol", "amount"])
        with open(csvpth, "r+", encoding="utf-8") as pff:
            olddf = pd.read_csv(pff, sep=",", low_memory=True)
            newdf["datetime"] = olddf["datetime"].values
            print(newdf)

    def csv_split(self, csvpth, fileType="sqlDay"):
        """
        将sql内导出的csv格式的文件按照股票名称切分，并且保存到一个文件夹下
        :param csvpth:
        :return:
        """
        with open(csvpth, "r+", encoding="utf-8") as csvpf:
            strpth = CT.BASEPTH + "data\\csv\\sqldatacsv\\stockcsv\\{}\\".format(fileType)
            isExists = os.path.exists(strpth)  # 判断文件夹路径是否存在
            if not isExists:
                os.makedirs(strpth)
            code_pre = ""  # 换行前记录上一行的代码，确定换行用
            strache_now = ""  # 当前代码行初始化
            for i_line in csvpf:
                linearr = i_line.split(",")
                code_now = linearr[1]  # 当前代码行标记
                currentcodefile = strpth + code_now + ".csv"
                tm = time.strftime(CT.TIME_FORMAT[2], time.strptime(linearr[10], CT.TIME_FORMAT[2]))
                solidformat = tm + "," + linearr[1] + "," + linearr[2] + "," + linearr[3] + "," + linearr[5] + "," + \
                                linearr[6] + "," + linearr[4] + "," + linearr[7] + "," + linearr[8] + "\n"
                if code_now != code_pre:
                    if not os.path.exists(currentcodefile):
                        # 刚开始运行时候，不存在上一个文件
                        if code_pre == "":
                            with open(currentcodefile, "a+") as af:
                                af.write("datetime,code,name,open,high,low,close,vol,amount\n")
                                strache_now = solidformat
                                af.write(strache_now)
                                af.flush()
                                code_pre = linearr[1]
                                strache_now = ""
                        else:
                            codeprefile = strpth + code_pre + ".csv"
                            if strache_now != "":
                                with open(codeprefile, "a+") as af:
                                    af.write(strache_now)
                                    af.flush()
                            with open(currentcodefile, "a+") as af:
                                af.write("datetime,code,name,open,high,low,close,vol,amount\n")
                                strache_now = solidformat
                                af.write(strache_now)
                                af.flush()
                                code_pre = linearr[1]
                                strache_now = ""
                    else:
                        codeprefile = strpth + code_pre + ".csv"
                        if strache_now != "":
                            with open(codeprefile, "a+") as af:
                                af.write(strache_now)
                                af.flush()
                        with open(currentcodefile, "a+") as af:
                            strache_now = solidformat
                            af.write(strache_now)
                            af.flush()
                            code_pre = linearr[1]
                            strache_now = ""

                else:
                    strache_now = strache_now + solidformat
                    code_pre = linearr[1]

    def mysql_stockinfo(self, funin_pthache="E:\\fsdrun\\data\\csv\\sqldatacsv\\stockcsv\\sqlDay\\"):
        filelst = [i_f for i_f in os.listdir(funin_pthache)]
        stockinfo_dict = {}
        index = 0
        for i_f in filelst:
            index += 1
            if index % 100 == 0:
                print(round(100 * index / len(filelst), 1), "%")
            achedict = dict()
            with open(funin_pthache + i_f, "r+") as pcsv:
                dfcsv_ache = pd.read_csv(pcsv, sep=",", encoding="utf-8", engine="python")
                achedict["name"] = dfcsv_ache["name"].values[-1]
                achedict["startdate"] = dfcsv_ache["datetime"].values[0].split(" ")[0]
                achedict["latestdate"] = dfcsv_ache["datetime"].values[-1].split(" ")[0]
                stockinfo_dict[i_f.split(".")[0]] = achedict
        with open(CT.BASEPTH + "\\data\\pkl\\stockinfo.json", 'w', encoding='utf-8') as json_file:
            json.dump(stockinfo_dict, json_file, ensure_ascii=False)
        print(stockinfo_dict)

    def mysql_stock_cfg(self, funin_pthache, fileType="sqlCfg"):
        bkcode = {}
        typelst = ["概念", "风格", "申万行业", "通达信二类行业", "地区"]
        with open(funin_pthache, "r+", encoding="utf-8") as csvpf:
            strpth = CT.BASEPTH + "data\\csv\\sqldatacsv\\stockcsv\\{}\\".format(fileType)
            isExists = os.path.exists(strpth)  # 判断文件夹路径是否存在
            if not isExists:
                os.makedirs(strpth)
            lines = csvpf.readlines()
            for i_line in lines:
                if i_line.split(",")[3] not in list(bkcode):
                    achedict = {}
                    lstcfg = list()
                    if i_line.split(",")[4].split("\n")[0] in typelst:
                        lstcfg.append(i_line.split(",")[1])
                        achedict["cfglen"] = len(lstcfg)
                        achedict["cfglst"] = lstcfg
                        bkcode[i_line.split(",")[3]] = achedict
                else:
                    if i_line.split(",")[4].split("\n")[0] in typelst:
                        bkcode[i_line.split(",")[3]]["cfglst"].append(i_line.split(",")[1])
                        bkcode[i_line.split(",")[3]]["cfglst"] = list(set(bkcode[i_line.split(",")[3]]["cfglst"]))
                        bkcode[i_line.split(",")[3]]["cfglen"] = len(bkcode[i_line.split(",")[3]]["cfglst"])
        with open("E:\\Work_App\\RQalpha\\通用策略\\indispensable\\platecfg_a.json", "w+") as pcf:
            json.dump(bkcode, pcf)
            print("处理完成")

if __name__ == '__main__':
    # stocklst = SqlData().csv_split("E:\\fsdrun\\data\\csv\\sqldatacsv\\stock_1day_his2.csv")
    # print(stocklst)
    SqlData().mysql_stock_cfg("E:\\fsdrun\\data\\csv\\sqldatacsv\\tdx_gncfg.csv", fileType="sqlCfg")
