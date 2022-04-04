import pandas as pd
import re
from src.expire_day_rules.stock_index_option_expire_rule import trading_day_rule_1
# , 'Unnamed: 4'


def option_data_preparation(valuation_date, spot_price, option_df):
    option_df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 4'], axis=1, inplace=True)
    option_df.drop(option_df.index[[0, -1, -2]], inplace=True)
    option_df.columns = ['Option Code', 'Today Settlement']
    option_df.dropna(inplace=True)

    df = option_df['Option Code']
    month_code_series = []
    strike_series = []
    exchange_series = []
    underlying_code_series = []
    option_type_series = []

    for i in df:
        pattern = r'\D+'
        month_code = int(re.split(pattern, i)[1])
        strike = int(re.split(pattern, i)[2])
        pattern = r'\d+'
        underlying_code = str(re.split(pattern, i)[0])
        if underlying_code == 'IO':
            underlying_code = '000300.SH'
        else:
            print('Underlying Code is wrong')
        option_type = str(re.split(pattern, i)[1])
        exchange_code = str(re.split(pattern, i)[2])
        pattern = r'\W'
        option_type = str(re.split(pattern, option_type)[1])
        exchange_code = str(re.split(pattern, exchange_code)[1])
        month_code_series.append(month_code)
        strike_series.append(strike)
        underlying_code_series.append(underlying_code)
        option_type_series.append(option_type)
        exchange_series.append(exchange_code)

    option_df['Exchange'] = exchange_series
    option_df['Underlying Code'] = underlying_code_series
    option_df['Option Type'] = option_type_series
    option_df['Trade Month'] = month_code_series
    option_df['Strike'] = strike_series
    option_df['Today Settlement'] = pd.to_numeric(option_df['Today Settlement'])
    option_df['Spot Price'] = spot_price

    moneyness_series = []
    for i in option_df.index:
        moneyness_value = option_df.loc[i]['Strike'] / option_df.loc[i]['Spot Price']
        moneyness_series.append(moneyness_value)
    option_df['Moneyness'] = moneyness_series

    maturity_day_series = []
    days_to_maturity_series = []
    ttm_series = []
    for i in option_df['Trade Month']:
        maturity_day = trading_day_rule_1(i)
        days_to_maturity = (maturity_day - valuation_date).days
        ttm = days_to_maturity / 365.0
        maturity_day_series.append(maturity_day)
        days_to_maturity_series.append(days_to_maturity)
        ttm_series.append(ttm)
    option_df['Maturity'] = maturity_day_series
    option_df['Days to Maturity'] = days_to_maturity_series
    option_df['TTM'] = ttm_series
    option_df.drop(option_df[option_df['Days to Maturity'] <= 0].index, inplace=True)

    return option_df
