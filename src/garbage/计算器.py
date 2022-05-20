# 定义了一个计算现值的函数，fv指的是终值，r指的是利率，单位是小数，t指的是时间，单位是一年
def pv_function(fv, r, t):
    pv = fv / ((1.+r)**t)
    return pv


print(pv_function(110, 0.1, 1))
