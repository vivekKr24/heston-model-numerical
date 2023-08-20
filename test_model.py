from heston_model import *
from black_scholes_model import BS_CALL, BS_PUT
import matplotlib.pyplot as plt

stock = Stock(1000)
option = Option(1520, Stock(1590), 0.05)
r = 0.072
# model = HestonModel(0.73, -0.88, 4, 0.1, 0.01, r)
model = HestonModel(0.61, -0.7, 6.21, 0.019, 0.010201, r)


price = model.price(Option(1520, Stock(1590), 0.05))
print("Price of option is " + str(price.real))

#  Implied vol

def call_price_Put_Call_Parity(put_option, put_price, T):
    C = put_price + option.underlying.spot - option.strike * np.exp(-r * T)
    return C


def implied_vol(option_price, option):
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


def plot_vol_surface():
    time_to_maturity = []
    IV = []
    strikes = []
    for T in range(1, 25):
        for K in range(950, 1250, 10):
            option = Option(K, stock, T / 50)
            price = model.price(option)
            iv = implied_vol(price, option)

            if iv < 0.05:
                continue
            IV.append(iv)
            time_to_maturity.append(T)
            strikes.append(K)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf1 = ax.plot_trisurf([t / 10 for t in time_to_maturity], strikes, [np.abs(iv) for iv in IV],
                           linewidth=0.1, antialiased=False)
    surf2 = ax.plot_trisurf([t / 10 for t in time_to_maturity], strikes, [np.abs(iv) for iv in IV],
                        linewidth=0.1, antialiased=True, cmap='hot')
    # ax.scatter(time_to_maturity, strikes, np.array(IV))

    fig.colorbar(surf1, shrink=0.5, aspect=5)
    # plt.show()
    plt.savefig("IMPLIED_VOLATILITY_SURFACE")
# IV vs Time to Maturity

# def price_vs_K():


def plot_K_vs_IV(T):
    time_to_maturity = []
    IV = []
    strikes = []
    for K in range(9500, 11000, 10):
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
    range = 0.5
    logKS = -range
    while logKS <= range:
        strike = np.exp(logKS) * stock.spot
        option = Option(strike, stock, T)
        price = model.price(option)
        iv = implied_vol(price, option)

        if iv < 0.05:
            logKS += 0.01
            continue
        time_to_maturity.append(T)
        IV.append(iv)
        moneyness.append(logKS)
        logKS += 0.01

    plt.figure()
    plt.scatter(moneyness, IV, marker='.')
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
    plt.scatter([t / 10 for t in time_to_maturity], [np.abs(iv) for iv in IV], marker='*')
    plt.xlabel("Time to Expiry")
    plt.ylabel("IV")
    plt.savefig("TIME VS IV")
    plt.close()


# Check trend of option prices with strikes
# vol_sample_size = 100
# vol_step = 1.0 / vol_sample_size
# plt.figure()
# plt.plot([vol_step * i for i in range(1, vol_sample_size + 1)],
#          [implied_vol(BS_CALL(option.underlying.spot, option.strike, option.expiry, r, vol_step * i), option) for i in range(1, vol_sample_size + 1)])
# plt.savefig("vol_vs_bscall")
# plt.show()
# plt.close()


plot_vol_surface()
# plot_K_vs_IV(0.1)
# plot_T_vs_IV(1000)

# price = BS_CALL(option.underlying.spot, option.strike, option.expiry, r, 0.345)
# print(implied_vol(price, option))

# for i in range(1, 1000 + 1):
#     iv = implied_vol(BS_CALL(option.underlying.spot, option.strike, option.expiry, r, .001 * i), option)
#     if iv != .001 * i:
#         print(iv, i)

plot_logKS_vs_IV(0.1)

def plot_price_vs_kappa():
    KAPPA = []
    PRICE = []
    plt.figure()
    for kappa in range(1, 6):
        model = HestonModel(0.61, -0.7, kappa, 0.019, 0.010201, r)
        price = model.price(option)
        PRICE.append(price)
        KAPPA.append(kappa)

    plt.plot(KAPPA, PRICE)
    plt.plot(KAPPA, [78.51] * len(KAPPA))

    plt.savefig("PRICE VS KAPPA")
    plt.close()


def plot_price_vs_n():
    N = []
    PRICE = []
    plt.figure()
    for n in range(1, 20):
        model = HestonModel(n / 5, -0.7, 6.21, 0.019, 0.010201, r)
        price = model.price(option)
        PRICE.append(price)
        N.append(n / 5)
    plt.plot(N, PRICE)
    plt.plot(N, [78.51] * len(N))
    plt.savefig("PRICE VS N")

    plt.close()


def plot_price_vs_rho():
    RHO = []
    PRICE = []
    plt.figure()
    for rho in range(-10, 11):
        model = HestonModel(2.5, rho / 10, 6.21, 0.019, 0.010201, r)
        price = model.price(option)
        PRICE.append(price)
        RHO.append(rho / 10)
    plt.plot(RHO, PRICE)
    plt.plot(RHO, [78.51] * len(RHO))
    plt.savefig("PRICE VS RHO")
    plt.close()


def plot_price_vs_v0():
    RHO = []
    PRICE = []
    plt.figure()
    for rho in range(-10, 11):
        model = HestonModel(2.5, rho, 6.21, 0.019, 0.010201, r)
        price = model.price(option)
        PRICE.append(price)
        RHO.append(rho)
    plt.plot(RHO, PRICE)
    plt.savefig("PRICE VS RHO")
    plt.close()


# plot_price_vs_kappa()
# plot_price_vs_n()
# plot_price_vs_rho()
