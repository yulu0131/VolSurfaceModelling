from datetime import date
from src.trading_calendar.date import Calendar


# 适用上一个月正数第3个交易日规则
def trading_day_rule_1(month_code):
    """
    函数用于返回最后交易日。输入交易月代码，根据品种规则的不同可以返回不同的到期日。
    这个规则适用于那些规定到期日为期货交割日期前一个月第3个交易日。
    :param month_code: 期权中的交易月代码，形如2201，2209
    :return: 返回期权到期日
    """
    year = month_code // 100 + 2000
    month = month_code % 100
    condition = Calendar()
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    days_count = 0
    for i in range(31):
        if condition.is_trading(date(year, month, i+1)):
            days_count += 1
        if days_count == 3:
            break
    day = i + 1
    return date(year, month, day)


# 适用上一个月正数第5个交易日规则
def trading_day_rule_2(month_code):
    """
    函数用于返回最后交易日。输入交易月代码，根据品种规则的不同可以返回不同的到期日。
    这个规则适用于那些规定到期日为期货交割日期前一个月第5个交易日。
    :param month_code: 期权中的交易月代码，形如2201，2209
    :return: 返回期权到期日
    """
    year = month_code // 100 + 2000
    month = month_code % 100
    condition = Calendar()
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    days_count = 0
    for i in range(31):
        if condition.is_trading(date(year, month, i + 1)):
            days_count += 1
        if days_count == 5:
            break
    day = i + 1
    return date(year, month, day)


# 适用上一个月倒数第5个交易日规则
def trading_day_rule_3(month_code):
    """
    函数用于返回最后交易日。输入交易月代码，根据品种规则的不同可以返回不同的到期日。
    这个规则适用于那些规定到期日为期货交割日期前一个月倒数第5个交易日。
    :param month_code: 期权中的交易月代码，形如2201，2209
    :return: 返回期权到期日
    """
    year = month_code // 100 + 2000
    month = month_code % 100
    condition = Calendar()
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    days_count = 0
    if month in [1, 3, 5, 7, 8, 10, 12]:
        for i in range(31):
            if condition.is_trading(date(year, month, 31 - i)):
                days_count += 1
            if days_count == 5:
                day = 31 - i
                break
    elif month in [4, 6, 9, 11]:
        for i in range(30):
            if condition.is_trading(date(year, month, 30 - i)):
                days_count += 1
            if days_count == 5:
                day = 30 - i
                break
    else:
        if year // 4 == 0:
            for i in range(29):
                if condition.is_trading(date(year, month, 29 - i)):
                    days_count += 1
                if days_count == 5:
                    day = 29 - i
                    break
        else:
            for i in range(28):
                if condition.is_trading(date(year, month, 28 - i)):
                    days_count += 1
                if days_count == 5:
                    day = 28 - i
                    break
    return date(year, month, day)


# 适用上一个月倒数第13个交易日规则
def trading_day_rule_4(month_code):
    """
    函数用于返回最后交易日。输入交易月代码，根据品种规则的不同可以返回不同的到期日。
    这个规则适用于那些规定到期日为期货交割日期前一个月倒数第13个交易日。
    :param month_code: 期权中的交易月代码，形如2201，2209
    :return: 返回期权到期日
    """
    year = month_code // 100 + 2000
    month = month_code % 100
    condition = Calendar()
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    days_count = 0
    if month in [1, 3, 5, 7, 8, 10, 12]:
        for i in range(31):
            if condition.is_trading(date(year, month, 31 - i)):
                days_count += 1
            if days_count == 13:
                day = 31 - i
                break
    elif month in [4, 6, 9, 11]:
        for i in range(30):
            if condition.is_trading(date(year, month, 30 - i)):
                days_count += 1
            if days_count == 13:
                day = 30 - i
                break
    else:
        if year // 4 == 0:
            for i in range(29):
                if condition.is_trading(date(year, month, 29 - i)):
                    days_count += 1
                if days_count == 13:
                    day = 29 - i
                    break
        else:
            for i in range(28):
                if condition.is_trading(date(year, month, 28 - i)):
                    days_count += 1
                if days_count == 13:
                    day = 28 - i
                    break
    return date(year, month, day)
