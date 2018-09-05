# -*- coding:utf-8 -*-
from fsdrun.fsdData.fsdDataBase import *
import pymysql as mdb
from fsdrun.fsdData.fsdDataConst import CT
import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

class CPlotMol(object):
    def __init__(self):
        self.lenth = 19
        self.width = 10
        self.wnum = 29
        self.lnum = 20
        self.fontsze = 10

    def set_ch(self):
        from pylab import mpl
        mpl.rcParams['font.sans-serif'] = ["LiSu"]
        mpl.rcParams['axes.unicode_minus'] = False

    def SetGs(self):
        fig = plt.gcf()  # 返回子图的标记
        fig.set_size_inches(self.lenth, self.width)  # 设置子图的大小
        gs_ache = gridspec.GridSpec(self.wnum, self.lnum, left=0.03, right=0.97, top=0.97, bottom=0.03)
        return gs_ache

    def plttext(self, location, strvalue):
        plt.text(location[0], location[1], strvalue, fontsize=self.fontsze)

def strategyEnd(jsonfile):
    # if str(context.run_info.end_date) == str(context.now)[0:10] and inthour == "15:00:00":
    data_allproit = []
    with open(jsonfile, "r") as pcf:
        json_data = json.load(pcf)
    with open("E:\Work_App\RQalpha\通用策略\AMA_TY4.0\\Fund__AMA_TY4.0.csv", "r") as pcf:
        datacsv = pd.read_csv(pcf, sep=",")
        data_allproit = datacsv["总权益"].values
        data_alllots = datacsv["持仓股票的数量"].values

    plt.figure().set_facecolor('gray')
    pltM = CPlotMol()
    pltM.set_ch()
    gs = pltM.SetGs()
    plt.subplot(gs[0:6, 0:5], facecolor="gainsboro")
    lst_roc = [0.95, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    plt.title('综合统计')
    xlocal = 0.1
    pltM.plttext((0.02, lst_roc[0]),
                 r'交易时间段：' + json_data["strategy_start_time"] + ' ~ ' + json_data["strategy_ache_time"])
    pltM.plttext((xlocal, lst_roc[2]), r'开仓次数：' + str(json_data["freq_entry"]))
    pltM.plttext((xlocal, lst_roc[3]), r'平仓次数：' + str(json_data["freq_out"]))
    pltM.plttext((xlocal, lst_roc[4]), r'胜率：' + str(json_data["freq_risk"]))
    pltM.plttext((xlocal, lst_roc[5]), r'盈亏比：' + str(json_data["pro_loss_rate"]))
    plt.xticks([0, 1], [])
    plt.yticks([0, 1.1], [])

    plt.subplot(gs[7:25, 0:17], facecolor="gainsboro")
    plt.plot(data_allproit, label="动态权益", color='darkred', linewidth="0.5")
    plt.legend(loc='upper left', prop={'family': 'SimHei', 'size': 6})
    plt.grid(True, color='white')

    plt.subplot(gs[26:, 0:17], facecolor="gainsboro")
    plt.plot(data_alllots, label="仓位分布", color='darkred', linewidth="0.5")
    plt.legend(loc='upper left', prop={'family': 'SimHei', 'size': 6})
    plt.grid(True, color='white')
    plt.show()

def load_parameter(abspth, filename):
    par_dict = {}
    with open(abspth + filename, "r+", encoding="utf-8") as pf:
        index = 0
        arrformat = []
        for i_l in pf:
            if index == 0:
                arrformat = i_l.split(",")[1:-1]
                arrformat.append(i_l.split(",")[-1].split("\n")[0])
                index += 1
            else:
                valueslst = [float(i_ache) for i_ache in i_l.split(",")[1:-1]]
                valueslst.append(float(i_l.split(",")[-1].split("\n")[0]))
                dict_ache = dict(zip(arrformat, valueslst))
                par_dict[i_l.split(",")[0]] = dict_ache
    return par_dict

if __name__ == '__main__':
    inifile = "E:\\Work_App\\RQalpha\\通用策略\\AMA_TY5.0\\Json__AMA_TY5.0.json"
    strategyEnd(inifile)
    # datadict = load_parameter("E:\\Work_App\\RQalpha\\通用策略\\indispensable\\", "parameter.csv")
    # platelst = list(datadict)
    # with open("E:\\Work_App\\RQalpha\\通用策略\\indispensable\\platecfg.json", "r") as pcf:
    #     cfg = json.load(pcf)
    # for i_l in platelst:
    #     try:
    #         if cfg[i_l]['cfglen'] < 5:
    #             print(i_l, "成分股太少")
    #         else:
    #             continue
    #     except KeyError as e:
    #         print(e, i_l, "版块成分股错误")




