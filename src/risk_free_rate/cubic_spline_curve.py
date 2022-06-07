import pandas as pd
import numpy as np
import os
from scipy.interpolate import CubicSpline
import datetime

#todo: 数据爬虫
def get_risk_free_rate(date):
    number_of_cycles = 10
    for i in range(number_of_cycles):
        result = os.path.exists('D:/Market Data/中债国债收益率曲线(到期)/中债国债收益率曲线(到期) ' + str(date) + '.csv')
        if result:
            break
        else:
            date = date + datetime.timedelta(days=-1)
    data = pd.read_csv('D:/Market Data/中债国债收益率曲线(到期)/中债国债收益率曲线(到期) ' + str(date) + '.csv',
                       encoding='Chinese')
    maturity_date = np.array(data['标准期限(年)'])
    risk_free_rate = np.array(data['收益率(%)']) / 100
    cubic_spline_result = CubicSpline(maturity_date, risk_free_rate)

    return cubic_spline_result
