import pandas as pd
import numpy as np
from VolSurfaceModelling.data_importer.stock_index_option_choice_importer import option_data_preparation
from VolSurfaceModelling.surface_model.svi_model_fit import SVIModel
import datetime
import VolSurfaceModelling.data_exporter.data_exporter as data_exporter
from VolSurfaceModelling.market_data.market_implied_vols import MarketImpliedVols
from VolSurfaceModelling.risk_free_rate.cubic_spline_curve import get_risk_free_rate
import os
# 目前仅适用于沪深300指数期权

valuation_date = datetime.date(2022, 3, 25)
underlying_code = '000300.SH'
option_type_series = ['C', 'P']
spot = 4174.57

option_df = pd.read_csv('D:/Market Data/' + str(valuation_date) + '/沪深300OptionData.csv', encoding='Chinese')
data = option_data_preparation(valuation_date, spot, option_df)
data.to_excel('D:/Market Data/' + str(valuation_date) + '/沪深300OptionData2.xlsx')
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

    vol_data = MarketImpliedVols(data,
                                 underlying_code,
                                 option_type,
                                 valuation_date,
                                 risk_free_rate,
                                 target_export_path,
                                 'Stock Index')
    vol_data.get_market_implied_vols()
    vol_data.export_data()

    svi_model = SVIModel(vol_data)
    svi_model.fit(moneyness_axis)

    data_exporter.get_fitting_performance(option_type,
                                          vol_data,
                                          svi_model,
                                          moneyness_axis,
                                          valuation_date,
                                          underlying_code,
                                          target_export_path)

    data_exporter.get_variance_plot(option_type,
                                    vol_data,
                                    svi_model,
                                    moneyness_axis,
                                    valuation_date,
                                    underlying_code,
                                    target_export_path)

    data_exporter.get_excel_vol(vol_data,
                                moneyness_axis,
                                svi_model,
                                underlying_code,
                                target_export_path,
                                '000300.SH')
