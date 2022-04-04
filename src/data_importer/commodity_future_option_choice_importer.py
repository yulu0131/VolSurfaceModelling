import pandas as pd
import re
import src.expire_day_rules.commodity_future_option_expire_rule as trading_day_rules
# 用于输入choice数据，数据从choice金融终端下载，option一份文件，future一份文件。
# 最终数据整合在一起，形成一个dataframe，列名包括Option Code, Today Settlement, Exchange, Underlying Code, Option Type,
# Trade Month, Strike, Future Code, Spot Price, Moneyness, Maturity Date, Time to Maturity, TTM
# , 'Unnamed: 4'


def option_data_preparation(option_df):
    option_df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 4'], axis=1, inplace=True)
    option_df.drop(option_df.index[[0, -1, -2]], inplace=True)
    option_df.columns = ['Option Code', 'Today Settlement']
    option_df.dropna(inplace=True)

    df = option_df['Option Code']

    month_code_series = []
    strike_series = []
    for i in df:
        pattern = r'\D+'
        month_code = int(re.split(pattern, i)[1])
        strike = int(re.split(pattern, i)[2])
        month_code_series.append(month_code)
        strike_series.append(strike)

    exchange_market_series = []
    underlying_code_series = []
    option_type_series = []
    for i in df:
        pattern = r'\d+'
        df2 = re.split(pattern, i)
        pattern = r'[A-Z]+'
        underlying_code = df2[0]
        option_type = df2[1]
        exchange_market = re.search(pattern, df2[2]).group()
        exchange_market_series.append(exchange_market)
        underlying_code_series.append(underlying_code)
        option_type_series.append(option_type)

    option_df['Exchange'] = exchange_market_series
    option_df['Underlying Code'] = underlying_code_series
    option_df['Option Type'] = option_type_series
    option_df['Trade Month'] = month_code_series
    option_df['Strike'] = strike_series
    option_df['Today Settlement'] = pd.to_numeric(option_df['Today Settlement'])

    for i in option_df.index:
        if option_df.loc[i]['Exchange'] == 'CZC':
            month_value = option_df.loc[i]['Trade Month']
            option_df.loc[i, 'Trade Month'] = month_value + 2000

    return option_df


def future_data_preparation(future_df):
    future_df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 4'], axis=1, inplace=True)
    future_df.drop(future_df.index[[0, -1, -2]], inplace=True)
    future_df.columns = ['Future Code', 'Today Settlement']
    future_df.dropna(inplace=True)

    df = future_df['Future Code']

    month_code_series = []
    for i in df:
        pattern = r'\D+'
        month_code = re.split(pattern, i)[1]
        month_code_series.append(month_code)

    exchange_market_series = []
    underlying_code_series = []
    for i in df:
        pattern = r'\.'
        df2 = re.split(pattern, i)
        pattern = r'\d+'
        underlying_code = re.split(pattern, df2[0])[0]
        exchange_market = df2[1]
        exchange_market_series.append(exchange_market)
        underlying_code_series.append(underlying_code)

    future_df['Exchange'] = exchange_market_series
    future_df['Underlying Code'] = underlying_code
    future_df['Trade Month'] = month_code_series
    future_df.dropna(inplace=True)
    trade_month = pd.to_numeric(future_df['Trade Month'])
    future_df['Trade Month'] = trade_month
    future_df['Today Settlement'] = pd.to_numeric(future_df['Today Settlement'])

    return future_df


def data_preparation(valuation_date, option_df, future_df):
    option_data = option_data_preparation(option_df)
    future_data = future_data_preparation(future_df)

    option_data = option_data.set_index('Option Code', drop=True, append=False)
    future_data = future_data.set_index('Future Code', drop=True, append=False)

    future_code_series = []
    for i in option_data.index:
        if option_data.loc[i]['Exchange'] == 'SH':
            future_code = option_data.loc[i]['Underlying Code'] + \
                          str(option_data.loc[i]['Trade Month']) + '.' + \
                          option_data.loc[i]['Exchange'] + 'F'
        else:
            future_code = option_data.loc[i]['Underlying Code'] + \
                        str(option_data.loc[i]['Trade Month']) + '.' + \
                        option_data.loc[i]['Exchange']
        future_code_series.append(future_code)
    option_data['Future Code'] = future_code_series

    spot_price_series = []
    for i in option_data.index:
        future_code_content = option_data.loc[i]['Future Code']
        spot_price = future_data.loc[future_code_content]['Today Settlement']
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
    for i in option_data.index:
        month_code = option_data.loc[i]['Trade Month']
        if option_data.loc[i]['Underlying Code'] in ('SR', 'CF', 'ZC', 'TA', 'MA', 'RM'):
            maturity_day_value = trading_day_rules.trading_day_rule_1(month_code)
        elif option_data.loc[i]['Underlying Code'] in ('C', 'M', 'P', 'L', 'V', 'PP', 'I', 'PG'):
            maturity_day_value = trading_day_rules.trading_day_rule_2(month_code)
        elif option_data.loc[i]['Underlying Code'] in ('CU', 'AL', 'ZN', 'RU', 'AU'):
            maturity_day_value = trading_day_rules.trading_day_rule_3(month_code)
        elif option_data.loc[i]['Underlying Code'] in 'sc':
            maturity_day_value = trading_day_rules.trading_day_rule_4(month_code)
        days_to_maturity_value = (maturity_day_value - valuation_date).days
        ttm_value = days_to_maturity_value / 365.0
        maturity_day_series.append(maturity_day_value)
        days_to_maturity_series.append(days_to_maturity_value)
        ttm_series.append(ttm_value)
    option_data['Maturity'] = maturity_day_series
    option_data['Days to Maturity'] = days_to_maturity_series
    option_data['TTM'] = ttm_series
    option_data.drop(option_data[option_data['Days to Maturity'] <= 0].index, inplace=True)
    option_data['Option Code'] = option_data.index

    return option_data
