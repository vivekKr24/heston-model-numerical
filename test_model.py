import numpy as np
from matplotlib.ticker import LinearLocator

from heston_model import *
from black_scholes_model import BS_CALL

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt

stock = Stock(1000)
option = Option(1000, stock, 1)
r = 0.0319
model = HestonModel(0.61, -0.7, 6.21, 0.019, 0.010201, r)
# price = model.price(option)
# print("Price of option is " + str(price.real))

#  Implied vol
# Check trend of option prices with strikes
vol_sample_size = 1000
vol_step = 1 / vol_sample_size
plt.figure()
plt.plot([vol_step * i for i in range(1, vol_sample_size + 1)],
         [BS_CALL(stock.spot, option.strike, option.expiry, r, vol_step * i) for i in range(1, vol_sample_size + 1)]
         )
plt.savefig("vol_vs_bscall")
plt.close()


def implied_vol(option_price, option):
    vol_high = 100.0
    vol_low = -100.0
    while vol_high - vol_low >= 0.000001:
        vol = vol_high + vol_low
        vol /= 2

        call_price = BS_CALL(stock.spot, option.strike, option.expiry, r, vol)

        if call_price > option_price:
            vol_high = vol - 0.000001
        else:
            vol_low = vol + 0.000001

    vol = vol_high + vol_low
    vol /= 2

    if vol == 0:
        print("CHECK")
    return vol


# IV vs Time to Maturity
def plot_vol_surface():
    time_to_maturity = []
    IV = []
    strikes = []
    for T in range(10, 50):
        for K in range(800, 1200, 10):
            option = Option(K, stock, T / 10)
            price = model.price(option)
            iv = implied_vol(price, option)

            time_to_maturity.append(T)
            IV.append(iv)
            strikes.append(K)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_trisurf([t / 10 for t in time_to_maturity], strikes, [np.abs(iv) + 0.0001 for iv in IV], cmap='viridis', linewidth=0.1, antialiased=True)
    # ax.scatter(time_to_maturity, strikes, np.array(IV))

    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.savefig("3d")


def plot_K_vs_IV(T):
    time_to_maturity = []
    IV = []
    strikes = []
    for K in range(9500, 10500, 10):
        option = Option(K / 10, stock, T)
        price = model.price(option)
        iv = implied_vol(price, option)

        time_to_maturity.append(T)
        IV.append(iv)
        strikes.append(K)

    plt.figure()
    plt.scatter([K / 10 for K in strikes], [np.abs(iv) + 0.0001 for iv in IV], marker='*')
    plt.xlabel("STRIKE")
    plt.ylabel("IV")
    plt.savefig("STRIKE VS IV")
    plt.close()


def plot_logKS_vs_IV(T):
    time_to_maturity = []
    IV = []
    moneyness = []
    range = 0.4
    logKS = -range
    while logKS <= range:
        strike = np.exp(logKS) * stock.spot
        option = Option(strike, stock, T)
        price = model.price(option)
        iv = implied_vol(price, option)

        time_to_maturity.append(T)
        IV.append(iv)
        moneyness.append(logKS)
        logKS += 0.001

    plt.figure()
    plt.plot(moneyness, [np.abs(iv * iv) + 0.0001 for iv in IV])
    plt.xlabel("MONEY-NESS")
    plt.ylabel("IV")
    plt.savefig("MONEYNESS VS IV")
    plt.close()


def plot_T_vs_IV(K):
    time_to_maturity = []
    IV = []
    strikes = []
    for T in range(10, 100):
            option = Option(K, stock, T / 10)
            price = model.price(option)
            iv = implied_vol(price, option)

            time_to_maturity.append(T)
            IV.append(iv)
            strikes.append(K)

    plt.figure()
    plt.scatter([t / 10 for t in time_to_maturity], [np.abs(iv) + 0.0001 for iv in IV], marker='*')
    plt.xlabel("Time to Expiry")
    plt.ylabel("IV")
    plt.savefig("TIME VS IV")
    plt.close()


# plot_vol_surface()
# plot_K_vs_IV(1.5)
# plot_T_vs_IV(1000)
plot_logKS_vs_IV(5)




