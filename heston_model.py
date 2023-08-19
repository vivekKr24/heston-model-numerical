from cmath import exp, log as ln, sqrt
import scipy.integrate as integrate
import numpy as np


class Stock:
    def __init__(self, spot):
        self.spot = spot


class Option:
    def __init__(self, strike, underlying, expiry):
        self.strike = strike
        self.expiry = expiry
        self.underlying = underlying


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

    def characteristic_function(self, w, t=None):
        K = self.option.strike
        a = ((- w ** 2) / 2) - (1j * w / 2)
        b = self.kappa - self.rho * self.n * w * 1j
        gamma = self.n ** 2 / 2

        h = sqrt(b ** 2 - 4 * a * gamma)
        r_minus = (b - h) / (self.n ** 2)
        r_plus = (b + h) / (self.n ** 2)

        g = r_minus / r_plus

        def neg_exp_ht(t): return exp(- h * t)

        def l(t): return 1 - g * neg_exp_ht(t)

        def C(w, t): return self.kappa * (r_minus * t - 2 / (self.n ** 2) * (ln((l(t)) / (1 - g))))

        def D(w, t): return r_minus * (1 - neg_exp_ht(t)) / (l(t))

        S0 = self.option.underlying.spot

        if not t:
            t = self.option.expiry

        return exp(C(w, t) * self.theta + D(w, t) * self.vol_initial + 1j * w * ln(S0 * exp(self.r * t) / K))

    def P0(self):
        p0 = 1 / 2

        def integrand(w):
            K = self.option.strike
            I = (exp(-1j * w * ln(K)) * self.characteristic_function(w - 1j))
            I /= (1j * w * self.characteristic_function(-1j))
            return I.real

        integral = integrate.quad(lambda w: integrand(w), 0, np.inf)[0]

        p0 += 1 / np.pi * integral

        return p0

    def P1(self):
        p1 = 1/2

        def integrand(w):
            K = self.option.underlying.spot
            I = (exp(-1j * w * ln(K)) * self.characteristic_function(w))
            I /= (1j * w)

            return I.real

        integral = integrate.quad(lambda w: integrand(w), 0, np.inf)[0]

        p1 += 1 / np.pi * integral
        return p1

    def price(self, option: Option):
        self.option = option
        S0 = option.underlying.spot
        K = option.strike
        T = option.expiry

        return S0 * self.P0() - exp(-self.r * T) * K * self.P1()
