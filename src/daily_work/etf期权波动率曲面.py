import pandas as pd
import numpy as np
from src.data_importer.etf_option_choice_importer import data_preparation
from src.surface_model.svi_model_fit import SVIModel
import datetime
import src.data_exporter.data_exporter as data_exporter
from src.market_data.market_implied_vols import MarketImpliedVols
from src.risk_free_rate.cubic_spline_curve import get_risk_free_rate
import os
# 目前适用上证50ETF，510300.SH沪深300ETF，159919.SZ沪深300ETF期权

valuation_date = datetime.datetime.now().date()
underlying_code_series = ['510050.SH', '510300.SH', '159919.SZ']
option_type_series = ['C', 'P']

option_df = pd.read_csv('D:/Market Data/' + str(valuation_date) + '/ETFOptionData.csv', encoding='Chinese')
future_df = pd.read_csv('D:/Market Data/' + str(valuation_date) + '/ETFUnderlyingData.csv', encoding='Chinese')
data_for_all_commodity = data_preparation(valuation_date, option_df, future_df)
data_for_all_commodity.to_excel('D:/Market Data/' + str(valuation_date) + '/ETFOptionData2.xlsx')
risk_free_rate = get_risk_free_rate(valuation_date)
moneyness_axis = np.linspace(0.7, 1.3, 61)


for option_type in option_type_series:
    vol_data_series = []
    svi_model_series = []
    if option_type == 'C':
        target_export_path = 'D:/Vol Surface Data2/' + str(valuation_date) + '/Call\\'
        if not os.path.exists(target_export_path):
            os.makedirs(target_export_path)
    else:
        target_export_path = 'D:/Vol Surface Data2/' + str(valuation_date) + '/Put\\'
        if not os.path.exists(target_export_path):
            os.makedirs(target_export_path)

    for i in range(len(underlying_code_series)):
        vol_data = MarketImpliedVols(data_for_all_commodity,
                                     underlying_code_series[i],
                                     option_type,
                                     valuation_date,
                                     risk_free_rate,
                                     target_export_path,
                                     'Stock Index')
        vol_data.get_market_implied_vols()
        vol_data.export_data()

        svi_model = SVIModel(vol_data)
        svi_model.fit(moneyness_axis)

        vol_data_series.append(vol_data)
        svi_model_series.append(svi_model)

        print(underlying_code_series[i] + ' modeling succeed')

    for i in range(len(underlying_code_series)):
        data_exporter.get_fitting_performance(option_type,
                                              vol_data_series[i],
                                              svi_model_series[i],
                                              moneyness_axis,
                                              valuation_date,
                                              underlying_code_series[i],
                                              target_export_path)

        print(underlying_code_series[i] + ' curve fitting succeed')

    for i in range(len(underlying_code_series)):
        data_exporter.get_variance_plot(option_type,
                                        vol_data_series[i],
                                        svi_model_series[i],
                                        moneyness_axis,
                                        valuation_date,
                                        underlying_code_series[i],
                                        target_export_path)

        print(underlying_code_series[i] + ' var plotting succeed')

    for i in range(len(underlying_code_series)):
        data_exporter.get_excel_vol(vol_data_series[i],
                                    moneyness_axis,
                                    svi_model_series[i],
                                    underlying_code_series[i],
                                    target_export_path,
                                    underlying_code_series[i])
