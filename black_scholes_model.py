import numpy as np
from scipy.stats import norm

N = norm.cdf


def BS_CALL(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * N(d1) - K * np.exp(-r * T) * N(d2)
    return price


def BS_PUT(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * N(-d2) - S * N(-d1)


def BS_IMPLIED_VOL(option_price, option, r):
    vol_high = 1.0
    vol_low = 0.0
    while vol_high - vol_low >= 0.00001:
        vol = vol_high + vol_low
        vol /= 2

        call_price = 0
        # if option.underlying.spot - option.strike > 0:
        call_price = BS_CALL(option.underlying.spot, option.strike, option.expiry, r, vol)
        # else:
        #     put_price = BS_PUT(option.underlying.spot, option.strike, option.expiry, r, vol)
        #     call_price = call_price_Put_Call_Parity(option, put_price, option.expiry)

        if call_price > option_price:
            vol_high = vol - 0.000001
        elif call_price < option_price:
            vol_low = vol + 0.000001
        else:
            return vol

    vol = vol_high + vol_low
    vol /= 2

    if vol == 0:
        print("CHECK")
    return vol
