import pandas as pd
import os


def report_01():
    path = "E:\\fsdrun\\fsdrun\\fsdData\\tb_report\\tb_report\\"
    path = path
    postfix = ".csv"
    name_01 = "平仓分析"
    name_02 = "交易记录"
    name_03 = "资产变化"

    content_01 = pd.read_csv(path + name_01 + postfix, header=0, engine='python',
                             usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
    content_02 = pd.read_csv(path + name_02 + postfix, header=0, engine='python',
                             usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
    content_03 = pd.read_csv(path + name_03 + postfix, header=0, engine='python', usecols=[1, 2, 3, 4, 5, 6, 7, 8])

    # 转成时间格式
    content_02['建仓时间'] = pd.to_datetime(content_02['建仓时间'])
    content_02['平仓时间'] = pd.to_datetime(content_02['平仓时间'])
    content_03['时间'] = pd.to_datetime(content_03['时间'])
    # 得到时间轴
    time_index = content_03['时间'].tolist()
    time_index.sort()
    # 统计
    report_01 = []
    start_cash = content_03.loc[content_03['时间'] == time_index[0], '可用资金'].values[0]  # 记录初始资金
    for i in range(len(time_index)):
        if (i == 0):
            count_01 = content_02.loc[content_02['建仓时间'] <= time_index[i], '商品'].tolist()
            count_02 = content_02.loc[content_02['平仓时间'] <= time_index[i], '商品'].tolist()
            count_03_1 = count_01

            loss_profit = content_03.loc[content_03['时间'] == time_index[i], '动态权益'].values[0] - start_cash  # 记录盈亏
            report_01.append(
                [time_index[i], len(count_01), len(count_02), len(count_03_1), loss_profit, count_01, count_02,
                 count_03_1])
        else:
            # 建仓:ref(time,1)<建仓时间<=time
            count_01 = content_02.loc[
                (content_02['建仓时间'] > time_index[i - 1]) & (content_02['建仓时间'] <= time_index[i]), '商品'].tolist()
            # 平仓:ref(time,1)<平仓时间<=time
            count_02 = content_02.loc[
                (content_02['平仓时间'] > time_index[i - 1]) & (content_02['平仓时间'] <= time_index[i]), '商品'].tolist()
            # 持仓(open开平仓):
            #   1、ref(time,1)<建仓时间<=time;
            #   2、建仓时间<=ref(time,1) & ref(time,1)<平仓时间<=time;
            #   3、建仓时间<=ref(time,1) & 平仓时间>time

            count_03_1 = count_01
            count_03_2 = content_02.loc[
                (content_02['建仓时间'] <= time_index[i - 1]) & (content_02['平仓时间'] > time_index[i - 1]) & (
                    content_02['平仓时间'] <= time_index[i]), '商品'].tolist()
            count_03_3 = content_02.loc[
                (content_02['建仓时间'] <= time_index[i - 1]) & (content_02['平仓时间'] > time_index[i]), '商品'].tolist()

            loss_profit = content_03.loc[content_03['时间'] == time_index[i], '动态权益'].values[0] - start_cash  # 记录盈亏
            report_01.append(
                [time_index[i], len(count_01), len(count_02), len(count_03_1) + len(count_03_2) + len(count_03_3),
                 loss_profit, count_01, count_02, count_03_1 + count_03_2 + count_03_3])
    # 转dataframe
    dataframe_report_01 = pd.DataFrame(report_01, columns=['时间', '开仓数目', '平仓数目', '持仓数目', '盈亏', '开仓商品', '平仓商品', '持仓商品'])
    """写入excel"""
    dataframe_report_01.to_excel(excel_writer=path + 'report.xlsx', sheet_name="统计", index=False)


report_01()
