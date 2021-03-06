from src.option_pricer.american_option import american_option
from src.option_pricer.european_option import vanilla
from src.risk_free_rate.cubic_spline_curve import get_risk_free_rate
import datetime


valuation_date = datetime.date(2022, 5, 31)
r = get_risk_free_rate(valuation_date)
# + datetime.timedelta(days=-1))
# 计算美式期权波动率
spot = 3943
strike = 3050
ttm = 190/365.0
pv = 2
vol = 0.18959
# vol_check = ao.find_vol('C', spot, r(ttm), 0, ttm, strike, pv)
pv_check = american_option('P', spot, r(ttm), 0, vol, ttm, strike)
print(pv_check)
# print(vol_check)

# 计算欧式期权波动率
# option_type = 'P'
# spot = 4174.76
# ttm = 32/365.0
# strike = 4600
# pv = 435.8
# vol = 0.24
# vol_check = eo.find_vol(option_type, spot, r(ttm), r(ttm), strike, ttm, pv)
# pv_check = eo.vanilla(option_type, spot, r(ttm), r(ttm), vol, strike, ttm)
# print(pv_check)
# print(vol_check)


# ttm = 4/365.0
# strike_series = [4250, 4300, 4350, 4400, 4450, 4500, 4550, 4600, 4650, 4700, 4750, 4800, 4850, 4900, 4950, 5000, 5100,
#                  5200, 5300, 5400, 5500, 5600]
# pv_series = [516.8, 467, 417, 367, 317.2, 267.4, 218, 167.6, 121, 77.8, 42.2, 18.4, 6.6, 2.8, 1.2, 0.8, 0.4, 0.4, 0.4,
#              0.4, 0.2, 0.2]
# vol_series = [0.114592, 0.033885645, 0.012133708, 0.086874133, 0.077047814, 0.06612731, 0.038081396, 0.035490655,
#               0.16656447, 0.167174192, 0.162270419, 0.159058575, 0.160627239, 0.176934113, 0.192173135, 0.219564623,
#               0.269739123, 0.336804941, 0.40109388, 0.463038535, 0.487375783, 0.542241108]

# ttm = 32/365.0
# strike_series = [4250, 4300, 4350, 4400]
# pv_series = [525, 476.2, 428.4, 381]
# vol_series = [0.149631, 0.167243, 0.176279, 0.176536]

# ttm = 60/365.0
# strike_series = [4200, 4250, 4300, 4350, 4400]
# pv_series = [573.6, 527.2, 479.4, 433.6, 390.8]
# vol_series = [0.008647, 0.031485, 0.015371, 0.118904, 0.143601]

# ttm = 151 / 365.0
# strike_series = [4200, 4300, 4400, 4500, 4600, 4700, 4800, 4900, 5000, 5200, 5400, 5600, 5800]
# pv_series = [599.6, 514.6, 435.6, 364.4, 300.4, 244, 196.2, 155.4, 122.2, 77.2, 46.8, 28.2, 18.8]
# vol_series = [0.027994352, 0.117069493, 0.133362058, 0.142955392, 0.148962629, 0.153159389, 0.157051796, 0.159901426,
#               0.162885185,
#               0.171851957,
#               0.177793171,
#               0.183571752,
#               0.193474463]

# ttm = 247 / 365.0
# strike_series = [4300, 4400, 4500, 4600, 4700, 4800, 4900, 5000, 5200, 5400, 5600]
# pv_series = [539, 467.2, 404.8, 344.8, 296.2, 249.2, 211.8, 176.4, 123.6, 84, 59]
# vol_series = [0.094540702, 0.116024238, 0.129693372, 0.136113118, 0.144239735, 0.148067563, 0.153580884, 0.156387714,
#               0.163462724, 0.16800099, 0.174629879]

# 中证500期权2201看涨波动率计算（成功）
# strike_series = [4250, 4300, 4350, 4400, 4450, 4500, 4550, 4600, 4650, 4700, 4750, 4800, 4850, 4900, 4950, 5000, 5100,
#                  5200, 5300, 5400, 5500, 5600]
# pv_series = [0.2, 0.2, 0.2, 0.2, 0.4, 0.6, 1.2, 2.6, 5.4, 12.6, 27.2, 55, 91, 137, 184.6, 233.6, 335, 433, 532.8, 633,
#              733, 834.6]
# vol_series = [0.406420188, 0.368911686, 0.331519754, 0.294192756, 0.278472001, 0.251683936, 0.233369806, 0.217329136,
#               0.198597119, 0.188096302, 0.179108031, 0.185208699, 0.181661093, 0.207937951, 0.228004686, 0.253892623,
#               0.373209751, 0.395739124, 0.45924798, 0.540369321, 0.609032707, 0.750795192]

# 159919期权2201看涨波动率计算(成功)
# strike_series = [4300, 4400, 4500, 4600, 4700, 4800, 4900, 5000, 5250, 5500, 5750, 6000]
# pv_series = [464.7, 365.6, 269.6, 173.6, 90.2, 33.3, 8.3, 3, 0.9, 0.5, 0.4, 0.4]
# vol_series = [0.341481045, 0.290439125, 0.263006893, 0.208594358, 0.180302555, 0.166707051, 0.163311699, 0.188378626,
#               0.275286308, 0.360065092, 0.44606327, 0.534582725]

# for i in range(len(strike_series)):
#     strike = strike_series[i]
#     pv = pv_series[i]
#     vol = vol_series[i]
#     vol_check = eo.find_vol(option_type, spot, r(ttm), r(ttm), strike, ttm, pv)
#     pv_check = eo.vanilla(option_type, spot, r(ttm), r(ttm), vol, strike, ttm)
#     print(pv_check, vol_check)
# 测试成功