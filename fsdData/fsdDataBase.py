import time
import os
import pickle as pk
import pandas as pd

class DataModel(object):
    def __init__(self):
        self.pklformat = ["code", "name", "open", "high", "low", "close", "vol", "amount"]
        self.basepth = os.path.abspath("../../..")


    def data_topkl(self, Code, DataDict, DataPth="D:\\STOCK_PKL_DATA\\"):
        """
        写入pkl数据库
        :param Code: 股票代码
        :param DataDict: pkl数据
        :param DataPth: 写入数据的路径
        :return:
        """
        stockcode = Code
        filename_ache = "data_" + stockcode + ".pkl"
        # 文件夹保存数据
        isExists = os.path.exists(DataPth)  # 判断文件夹路径是否存在
        if not isExists:
            os.makedirs(DataPth)  # 不存在创建文件夹
        pick_data_bin = open(DataPth + filename_ache, 'wb')
        pk.dump(DataDict, pick_data_bin)
        pick_data_bin.close()

    def DataFrameToDict(self, code, codename, Dataframe):
        """
        DataFrame框架转化为数据pkl字典格式
        :param code: 股票代码
        :param codename: 股票简称
        :param Dataframe: 股票数据
        :return: pkl版的字典格式
        """
        timelst = list(Dataframe["datetime"].values)
        openlst = list(Dataframe["open"].values)
        highlst = list(Dataframe["high"].values)
        lowlst = list(Dataframe["low"].values)
        closelst = list(Dataframe["close"].values)
        vollst = list(Dataframe["vol"].values)
        amountlst = list(Dataframe["amount"].values)
        opendict = dict(zip(timelst, openlst))
        highdict = dict(zip(timelst, highlst))
        lowdict = dict(zip(timelst, lowlst))
        closedict = dict(zip(timelst, closelst))
        voldict = dict(zip(timelst, vollst))
        amountdict = dict(zip(timelst, amountlst))
        pkllst = [code, codename, opendict, highdict, lowdict, closedict, voldict, amountdict]
        pkldict = dict(zip(self.pklformat, pkllst))
        return pkldict

    def pthcsv_pkl(self, inpth):
        filecsv = [inpth + i_fv for i_fv in os.listdir(inpth)]
        print(filecsv)
        for i_csvf in filecsv:
            with open(i_csvf, "r+") as csvpf:
                dataf = pd.read_csv(csvpf)
                code = "%06d" % dataf["code"].values[-1]
                print(code)
                name = dataf["name"].values[-1]
                dictpkl = self.DataFrameToDict(code, name, dataf)
                self.data_topkl(code, dictpkl, DataPth="E:\\fsdrun\\data\\pkl\\day\\")
