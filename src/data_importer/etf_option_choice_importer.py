import pandas as pd
import re
from datetime import date
from src.expire_day_rules.etf_option_expire_rule import trading_day_rule_1


def option_data_preparation(option_df):
    option_df.drop(['历史行情', 'Unnamed: 2', 'Unnamed: 4'], axis=1, inplace=True)
    option_df.drop(option_df.index[[0, -1, -2]], inplace=True)
    option_df.columns = ['Option Code', 'Today Settlement']
    option_df.dropna(inplace=True)

    df = option_df['Option Code']
    month_code_series = []
    strike_series = []
    underlying_code_series = []
    option_type_series = []

    for i in df:
        pattern = r'\d+'
        month_code_part2 = int(re.findall(pattern, i)[1])
        if month_code_part2 >= date.today().month:
            month_code = (date.today().year % 100) * 100 + month_code_part2
        else:
            month_code = (date.today().year % 100 + 1) * 100 + month_code_part2
        strike = int(re.findall(pattern, i)[2])
        pattern = r'\D\d+\D\d+'
        underlying_code = re.split(pattern, i)[0]
        if underlying_code == '50ETF':
            underlying_code = '510050.SH'
        elif underlying_code in ['300ETF', 'XD300ETF']:
            underlying_code = '510300.SH'
        elif underlying_code == '沪深300ETF':
            underlying_code = '159919.SZ'
        elif underlying_code == '沪深300':
            underlying_code = '000300.SH'
        else:
            print('Underlying Code is wrong')
        pattern = r'\d+'
        option_type = re.split(pattern, i)[1]
        pattern = r'[^ETF]'
        option_type = re.search(pattern, option_type).group()
        if option_type == '购':
            option_type = 'C'
        elif option_type == '沽':
            option_type = 'P'
        else:
            print('Option Type is wrong')
        month_code_series.append(month_code)
        strike_series.append(strike)
        underlying_code_series.append(underlying_code)
        option_type_series.append(option_type)

    option_df['Underlying Code'] = underlying_code_series
    option_df['Option Type'] = option_type_series
    option_df['Trade Month'] = month_code_series
    option_df['Strike'] = strike_series
    option_df['Today Settlement'] = pd.to_numeric(option_df['Today Settlement']) * 1000

    return option_df


def underlying_data_preparation(underlying_df):
    underlying_df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 4'], axis=1, inplace=True)
    underlying_df.drop(underlying_df.index[[0, -1, -2]], inplace=True)
    underlying_df.columns = ['Underlying Code', 'Today Settlement']
    underlying_df.dropna(inplace=True)

    return underlying_df


def data_preparation(valuation_date, option_df, underlying_df):
    option_data = option_data_preparation(option_df)
    underlying_data = underlying_data_preparation(underlying_df)

    option_data = option_data.set_index('Option Code', drop=True, append=False)
    underlying_data = underlying_data.set_index('Underlying Code', drop=True, append=False)

    spot_price_series = []
    for i in option_data.index:
        underlying_code_content = option_data.loc[i]['Underlying Code']
        spot_price = float(underlying_data.loc[underlying_code_content]['Today Settlement']) * 1000
        spot_price_series.append(spot_price)
    option_data['Spot Price'] = spot_price_series

    moneyness_series = []
    for i in option_data.index:
        moneyness_value = option_data.loc[i]['Strike'] / option_data.loc[i]['Spot Price']
        moneyness_series.append(moneyness_value)
    option_data['Moneyness'] = moneyness_series

    maturity_day_series = []
    days_to_maturity_series = []
    ttm_series = []
    for i in option_data['Trade Month']:
        maturity_day = trading_day_rule_1(i)
        days_to_maturity = (maturity_day - valuation_date).days
        ttm = days_to_maturity / 365.0
        maturity_day_series.append(maturity_day)
        days_to_maturity_series.append(days_to_maturity)
        ttm_series.append(ttm)
    option_data['Maturity'] = maturity_day_series
    option_data['Days to Maturity'] = days_to_maturity_series
    option_data['TTM'] = ttm_series
    option_data.drop(option_data[option_data['Days to Maturity'] <= 0].index, inplace=True)
    option_data['Option Code'] = option_data.index

    return option_data
