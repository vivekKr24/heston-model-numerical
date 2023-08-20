import scipy.integrate as integrate
import numpy as np


class Stock:
    def __init__(self, spot):
        self.spot = spot


class Option:
    def __init__(self, strike, underlying: Stock, expiry):
        self.strike = strike
        self.expiry = expiry
        self.underlying: Stock = underlying


class HestonModel:
    def __init__(self, n, rho, kappa, theta, vol_initial, r):
        self.name = "Heston Model"
        self.n = n
        self.rho = rho
        self.kappa = kappa
        self.theta = theta
        self.vol_initial = vol_initial
        self.option = None
        self.r = r


    def alpha(self, j, u):
        k = self.kappa
        a = -1/2
        a *= u ** 2
        a += -1j * u / 2 + j * 1j * u * j

        return a

    def beta(self, j, u):
        return self.kappa - self.rho * self.n * j - self.rho * self.n * 1j * u

    def integrand(self, j, u, t, v):
        x = np.log(self.option.underlying.spot * np.exp(self.r * self.option.expiry) / self.option.strike)

        alpha = self.alpha(j, u)
        beta = self.beta(j, u)
        gamma = self.n ** 2
        gamma /= 2

        d = beta ** 2 - 4 * alpha * gamma
        d = np.sqrt(d)

        r_minus = beta - d
        r_minus /= self.n ** 2

        r_plus = beta + d
        r_plus /= self.n ** 2

        g = r_minus / r_plus

        def C(t):
            return self.kappa * (r_minus * t - (2 / self.n ** 2) * np.log((1 - g * np.exp(-d * t)) / (1 - g)))

        def D(t):
            return r_minus * ((1 - np.exp(-d * t)) / (1 - g * np.exp(-d * t)))

        return (np.exp(C(t) * self.theta + D(t) * v + 1j * u * x) / (1j * u)).real

    def P(self, j, t, v):
        p = 1 / np.pi
        integral = integrate.nquad(lambda u: self.integrand(j, u, t, v), [[0, np.inf]])
        # integral = integrate.quad(lambda u: self.integrand(j, u, t, v), 0, np.inf, limit=50)
        p *= integral[0]

        return p + 0.5

    def price(self, option: Option):
        self.option = option
        x = np.log(self.option.underlying.spot * np.exp(self.r * self.option.expiry) / self.option.strike)
        S0 = option.underlying.spot
        K = option.strike
        T = option.expiry
        var = self.vol_initial

        return K * (np.exp(x) * self.P(1, T, var) - self.P(0, T, var))
