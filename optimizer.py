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


def error_func(params: np.ndarray, model=None):
    params = ModelParams(params[0], params[1], params[2], params[3], params[4])
    error = 0
    k = params.mean_reversion_rate
    n = params.vol_of_variance
    v0 = params.initial_variance
    theta = params.long_term_mean_variance
    rho = params.correlation
    # if model is None:
    mp_sum = 0

    model = HestonModel(n, rho, k, theta, v0, 0.072)
    for strike, expiry, price in zip(df['STRIKE'], df['EXPIRY'].transform(lambda x: x / 242), df['CLOSE']):
        stock = Stock(S0)
        option = Option(strike, stock, expiry)
        mp = model.price(option).real
        print("ERR FN")

        error += ((mp - price) / price) ** 2
        mp_sum += price * price
    return error / df.size


def get_params(model, start=None):
    params = {
        "kappa": {"x0": 4, "lbub": [1e-3, 5]},
        "theta": {"x0": 0.1, "lbub": [1e-3, 0.1]},
        "v0": {"x0": 0.01, "lbub": [1e-3, 0.1]},
        "rho": {"x0": -0.88, "lbub": [-1, 0]},
        "sigma": {"x0": 0.73, "lbub": [1e-2, 1]},
    }
    x0 = [param["x0"] for key, param in params.items()]
    if start is None:
        start = x0
    print(x0)
    bnds = [param["lbub"] for key, param in params.items()]
    result = minimize(lambda x: error_func(x), start, tol=1e-3, method='SLSQP', options={'maxiter': 10000}, bounds=bnds)
    return result['x']

# [4, 0.1, 0.01, -0.88, 0.73]
# [ 3.999e+00  4.176e-02  3.103e-02 -8.467e-01  7.242e-01]
