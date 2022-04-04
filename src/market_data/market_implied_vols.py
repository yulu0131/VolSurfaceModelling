from src.option_pricer import american_option, european_option
import os
import numpy as np


class MarketImpliedVols:
    def __init__(self,
                 data_files,
                 underlying_code,
                 option_type,
                 valuation_date,
                 risk_free_rate,
                 file_path,
                 option_calculate_method):
        self._underlying_code = underlying_code
        self._option_type = option_type
        self._valuation_date = valuation_date
        self._risk_free_rate = risk_free_rate
        inner_data = data_files
        inner_data = inner_data.loc[lambda _inner_data: inner_data['Underlying Code'] == self._underlying_code]
        inner_data = inner_data.loc[lambda _inner_data: inner_data['Option Type'] == self._option_type]
        self._data = inner_data
        self._days_to_maturity = sorted(inner_data['Days to Maturity'].unique())
        self._ttms = sorted(inner_data['TTM'].unique())
        self._file_path = file_path
        self._cal_method = option_calculate_method

    def get_market_implied_vols(self):
        sample_data = self._data
        # 计算表内所有期权的IV
        for index in sample_data.index:
            spot_price = sample_data.loc[index, 'Spot Price']
            strike_price = sample_data.loc[index, 'Strike']
            ttm = sample_data.loc[index, 'TTM']
            option_price = sample_data.loc[index, 'Today Settlement']
            option_type = self._option_type
            risk_free_rate = self._risk_free_rate

            iv = self.vol_cal_method(option_type,
                                     spot_price,
                                     strike_price,
                                     ttm,
                                     risk_free_rate(ttm),
                                     option_price)
            sample_data.loc[index, 'Implied Volatility'] = iv
            sample_data.loc[index, 'Implied Variance'] = iv * iv * ttm
        # 验算表内所有期权IV，如果IV计算出来的PV和结算价差距大于1e-6，则剔除
        for index in sample_data.index:
            spot_price = sample_data.loc[index, 'Spot Price']
            strike_price = sample_data.loc[index, 'Strike']
            ttm = sample_data.loc[index, 'TTM']
            option_price = sample_data.loc[index, 'Today Settlement']
            implied_volatility = sample_data.loc[index, 'Implied Volatility']
            option_type = self._option_type
            risk_free_rate = self._risk_free_rate

            pv = self.pv_cal_method(option_type,
                                    spot_price,
                                    risk_free_rate(ttm),
                                    implied_volatility,
                                    strike_price,
                                    ttm)
            if (pv - option_price) >= 1e-6:
                sample_data.loc[index, 'Implied Volatility'] = np.nan
                sample_data.loc[index, 'Implied Variance'] = np.nan
        # 专门针对美式商品期货期权，如果位于深度实值/虚值期权区间，IV剔除
        if self._cal_method == 'Commodity Future':
            for index in sample_data.index:
                option_type = self._option_type
                spot_price = sample_data.loc[index, 'Spot Price']
                strike_price = sample_data.loc[index, 'Strike']
                option_price = sample_data.loc[index, 'Today Settlement']
                itm_check_result = self.itm_price_check(option_type, option_price, spot_price, strike_price)
                otm_check_result = self.otm_price_check(option_price)
                if itm_check_result == 'True' or otm_check_result == 'True':
                    sample_data.loc[index, 'Implied Volatility'] = np.nan
                    sample_data.loc[index, 'Implied Variance'] = np.nan

        self._data = sample_data

    def data(self):
        return self._data

    def export_data(self):
        df = self._data
        export_data = df.loc[:, ['Option Code',
                                 'Today Settlement',
                                 'Underlying Code',
                                 'Option Type',
                                 'Strike',
                                 'Spot Price',
                                 'Maturity',
                                 'Days to Maturity',
                                 'Implied Volatility']]
        export_file_path = self._file_path + '/MarketImpliedVol\\'
        if not os.path.exists(export_file_path):
            os.makedirs(export_file_path)
        export_data.to_excel(export_file_path + '/' + 'MarketImpliedVol-' + self._underlying_code + '.xlsx',
                             index=False)

    def vol_cal_method(self, option_type, spot, strike, ttm, r, pv):
        if self._cal_method == 'Commodity Future':
            return american_option.find_vol(option_type, spot, r, 0, ttm, strike, pv)
        if self._cal_method == 'Stock Index':
            return european_option.find_vol(option_type, spot, r, r, strike, ttm, pv)

    def pv_cal_method(self, option_type, spot, r, vol, strike, ttm):
        if self._cal_method == 'Commodity Future':
            return american_option.american_option(option_type, spot, r, 0, vol, ttm, strike)
        if self._cal_method == 'Stock Index':
            return european_option.vanilla(option_type, spot, r, r, vol, strike, ttm)

    def itm_price_check(self, option_type, option_price, spot, strike):
        if option_type == 'C':
            if option_price <= (spot - strike) + 0.0001:
                return 'True'
            else:
                return 'False'
        elif option_type == 'P':
            if option_price <= (strike - spot) + 0.0001:
                return 'True'
            else:
                return 'False'

    def otm_price_check(self, option_price):
        if self._underlying_code in ['CU']:
            if option_price <= 2:
                return 'True'
            else:
                return 'False'
        elif self._underlying_code in ['CF', 'AL', 'ZN', 'RU']:
            if option_price <= 1:
                return 'True'
            else:
                return 'False'
        elif self._underlying_code in ['SR', 'RM', 'TA', 'MA', 'C', 'M', 'P', 'L', 'V', 'PP']:
            if option_price <= 0.5:
                return 'True'
            else:
                return 'False'
        elif self._underlying_code in ['PG']:
            if option_price <= 0.2:
                return 'True'
            else:
                return 'False'
        elif self._underlying_code in ['ZC', 'I']:
            if option_price <= 0.1:
                return 'True'
            else:
                return 'False'
        elif self._underlying_code in ['sc']:
            if option_price <= 0.05:
                return 'True'
            else:
                return 'False'
        elif self._underlying_code in ['AU']:
            if option_price <= 0.02:
                return 'True'
            else:
                return 'False'

    def underlying_code(self):
        return self._underlying_code

    def valuation_date(self):
        return self._valuation_date

    def days_to_maturity(self):
        return self._days_to_maturity

    def ttms(self):
        return self._ttms
