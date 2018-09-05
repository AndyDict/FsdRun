import numpy as np


def IEMA(Arr, N):
    EMA = []
    mark = Arr[0] * 2 / (N + 1)
    for i in range(len(Arr) - 1):
        Y = (Arr[i + 1] * 2 + float(mark) * (N - 1)) / (N + 1)
        mark = Y
        EMA.append(Y)
    return np.array(EMA)


def Same_Len(List_1, List_2):
    if (len(List_1) > len(List_2)):
        List_1 = List_1[len(List_1) - len(List_2):]
    else:
        List_2 = List_2[len(List_2) - len(List_1):]
    return List_1, List_2


def IDMA(Arr, A):  # Arr和A 为数列
    # 将A转为大于0小于1处理
    if (A[0] > 1):
        B = A / (A * 1.0001)
    else:
        B = A
    # 同步数列长度
    if (len(Arr) > len(B)):
        Arr = Arr[len(Arr) - len(B):]
    else:
        B = B[len(B) - len(Arr):]
    # 计算DMA
    DMA = []
    mark = Arr[0] + B[0]
    for i in range(len(Arr) - 1):
        Y = B[i + 1] * Arr[i + 1] + (1 - B[i + 1]) * mark
        mark = Y
        DMA.append(Y)
    return DMA


def MAMA(Arr, N):
    DIR = []
    for i in range(len(Arr) - N):
        DIR.append(abs(Arr[i + N] - Arr[i]))

    VIR = []
    mark = []
    for i in range(len(Arr) - 1):
        mark.append(abs(Arr[i + 1] - Arr[i]))

    for i in range(len(mark) - (N - 1)):
        VIR.append(sum(mark[i:(N + i)]))

    DIR, VIR = Same_Len(DIR, VIR)
    ER = np.array(DIR) / np.array(VIR)
    CS = ER * (2 / 3 - 2 / 14) + 2 / 14
    CQ = CS * CS
    AMAA = IEMA(IDMA(Arr, CQ), 2)
    return AMAA
