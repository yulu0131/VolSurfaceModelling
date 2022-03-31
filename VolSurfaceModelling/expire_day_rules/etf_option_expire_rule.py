import datetime
from VolSurfaceModelling.trading_calendar.date import Calendar
# 依照期权合约条款设计，给出的etf期权不同到期日计算规则


# 适用当月第四个星期三交易日规则
def trading_day_rule_1(month_code):
    """
    函数用于返回最后交易日。输入交易月代码，根据品种规则的不同可以返回不同的到期日。
    这个规则适用于那些规定到期日为期货交割日期当月第4个星期三，遇到节假日顺延到下一个交易日。
    :param month_code: 期权中的交易月代码，形如2201，2209
    :return: 返回期权到期日
    """
    year = month_code // 100 + 2000
    month = month_code % 100
    condition = Calendar()
    days_count = 0
    for i in range(31):
        if datetime.datetime(year, month, i+1).strftime("%w") == '3':
            days_count += 1
        if days_count == 4:
            if condition.is_trading(datetime.date(year, month, i+1)):
                break
    day = i + 1
    return datetime.date(year, month, day)
