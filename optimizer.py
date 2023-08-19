import numpy as np
from scipy.optimize import minimize

from data import get_data
from heston_model import HestonModel, Stock, Option


class ModelParams:
    def __init__(self, kappa, theta, v0, rho, n):
        self.mean_reversion_rate = kappa
        self.long_term_mean_variance = theta
        self.initial_variance = v0
        self.correlation = rho
        self.vol_of_variance = n


df = get_data()

S0 = 1590.75


def error_func(params: np.ndarray):
    params = ModelParams(params[0], params[1], params[2], params[3], params[4])
    error = 0
    for strike, expiry, price in zip(df['STRIKE'], df['EXPIRY'], df['CLOSE']):
        stock = Stock(S0)
        option = Option(strike, stock, expiry)

        k = params.mean_reversion_rate
        n = params.vol_of_variance
        v0 = params.initial_variance
        theta = params.long_term_mean_variance
        rho = params.correlation

        model = HestonModel(n, rho, k, theta, v0, 0.072)
        mp = model.price(option).real

        error += (mp - price) ** 2

    return error / df.size


print(df.size)

def get_params(start):
    result = minimize(error_func, start, method='SLSQP', options={'maxiter': 5, 'disp': True})
    return result


print(get_params(np.ones(5)))
