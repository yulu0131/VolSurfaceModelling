from scipy.optimize import minimize
import numpy as np
import math


# SVI模型拟合模块，运用类SVIModel，输入类MarketImpliedVols，可以自动算出一个品种的所有IV拟合曲线的SVI参数


class SVIModel:
    def __init__(self, input_data):
        data = input_data.data()
        self.underlying_code = input_data.underlying_code()
        self.valuation_date = input_data.valuation_date()
        self.model_params = None
        self.ttm = input_data.ttms()
        self.moneyness = []
        self.implied_vars = []
        self.implied_vols = []

        for ttm_value in self.ttm:
            moneyness = data[lambda _data: data['TTM'] == ttm_value]['Moneyness'].values.tolist()
            implied_vars = data[lambda _data: data['TTM'] == ttm_value]['Implied Variance'].values.tolist()
            implied_vols = data[lambda _data: data['TTM'] == ttm_value]['Implied Volatility'].values.tolist()
            self.moneyness.append(moneyness)
            self.implied_vars.append(implied_vars)
            self.implied_vols.append(implied_vols)

    # fit the market data to get SVI model params
    def fit(self, moneyness_axis, weight=None):
        x_all = []
        last_parameter = [0, 0, 0, 0, 0]
        market_moneyness = self.moneyness
        market_var = self.implied_vars

        for i in range(len(market_moneyness)):
            market_moneyness_for_svi = []
            market_var_for_svi = []

            for j in range(len(market_moneyness[i])):
                if math.isnan(market_var[i][j]):
                    continue
                market_moneyness_for_svi.append(float(market_moneyness[i][j]))
                market_var_for_svi.append(float(market_var[i][j]))

            if weight is None:
                x = svi_curve_fit(market_moneyness_for_svi,
                                  market_var_for_svi,
                                  np.ones(len(market_moneyness[i])),
                                  last_parameter,
                                  moneyness_axis)
                last_parameter = x
                x_all.append(x)

            else:
                x = svi_curve_fit(market_moneyness[i],
                                  market_var[i],
                                  weight[i],
                                  last_parameter,
                                  moneyness_axis)
                last_parameter = x
                x_all.append(x)
        self.model_params = x_all

    def total_var(self, ttm, moneyness):
        if ttm < self.ttm[0] or ttm > self.ttm[-1]:
            raise Exception('ttm out of interpolation range!')

        t_index = 0
        for i in range(len(self.ttm)):
            if self.ttm[i] > ttm:
                t_index = i
                break
        t_i = t_index - 1
        t_j = t_index
        var_i = w_svi(self.model_params[t_i], moneyness)
        var_j = w_svi(self.model_params[t_j], moneyness)
        var = var_i * (ttm - self.ttm[t_j]) / (self.ttm[t_i] - self.ttm[t_j]) + \
              var_j * (ttm - self.ttm[t_i]) / (self.ttm[t_j] - self.ttm[t_i])
        return var

    def vol(self, ttm, moneyness):
        return np.sqrt(self.total_var(ttm, moneyness) / ttm)


def w_svi(svi_params, moneyness):
    return svi_params[0] + svi_params[1] * (svi_params[2] * (np.log(moneyness) - svi_params[3]) + np.sqrt(
        (np.log(moneyness) - svi_params[3]) ** 2 + svi_params[4] ** 2))


def loss_func(svi_params, moneyness, market_total_variance, weight):
    func_sum = 0
    for i in range(len(moneyness)):
        if weight is None:
            w = 1
        else:
            w = weight[i]
        func_sum += (((w_svi(svi_params, moneyness[i]) - market_total_variance[i]) / market_total_variance[i]) ** 2) * w
    return np.sqrt(func_sum / len(moneyness))


def svi_curve_fit(moneyness, total_variance, weight, last_parameter, moneyness_range):
    ineq_cons = [{'type': 'ineq', 'fun': lambda params: (params[0] - params[3] * params[1] * (params[2] + 1)) * (
            4 - params[0] + params[3] * params[1] * (params[2] + 1)) - params[1] ** 2 * (params[2] + 1) ** 2},
                 {'type': 'ineq', 'fun': lambda params: (params[0] - params[3] * params[1] * (params[2] - 1)) * (
                         4 - params[0] + params[3] * params[1] * (params[2] - 1)) - params[1] ** 2 * (
                                                                params[2] - 1) ** 2},
                 {'type': 'ineq', 'fun': lambda params: 4 - (params[1] * (params[2] + 1)) ** 2},
                 {'type': 'ineq', 'fun': lambda params: 4 - (params[1] * (params[2] - 1)) ** 2},
                 {'type': 'ineq',
                  'fun': lambda params: w_svi(params, moneyness_range) - w_svi(last_parameter, moneyness_range)}]

    bounds = [(1e-6, np.max(total_variance)),
              (1e-6, 1),
              (-1.0, 1.0),
              (2 * np.min(np.log(moneyness)), 2 * np.max(np.log(moneyness))),
              (1e-6, 1)]

    # initial guess
    a = 0.5 * min(total_variance)
    b = 0.1
    rho = 0.5
    m = 0.1
    sigma = 0.1

    guess = np.array([a, b, rho, m, sigma])
    res = minimize(loss_func,
                   guess,
                   args=(moneyness, total_variance, weight),
                   method='SLSQP',
                   constraints=ineq_cons,
                   options={'ftol': 1e-35, 'disp': False, 'maxiter': 300},
                   bounds=bounds)

    return res.x
