import os
from functools import cmp_to_key

from matplotlib import pyplot as plt

from black_scholes_model import BS_IMPLIED_VOL
from heston_model import Option, Stock

plot_path = "PLOTS\\"

if not (os.path.exists(plot_path)):
    os.mkdir(path=plot_path)


def MARKET_DATA_VS_MODEL_PREDICTION(model, S0, df):
    def cmp(T1, T2, j):
        if T1[j] == T2[j]:
            return 0
        if T1[j] < T2[j]:
            return -1
        else:
            return 1

    surface_mp = []
    surface_heston = []

    strikes_list, expiry_list, price_list = df['STRIKE'], df['EXPIRY'].transform(lambda x: x / 242), df['CLOSE']
    print(len(strikes_list), len(expiry_list), len(price_list), df.size)

    for strike, expiry, price in zip(df['STRIKE'], df['EXPIRY'].transform(lambda x: x / 242), df['CLOSE']):
        option = Option(strike, Stock(S0), expiry)
        heston_price = model.price(option)

        surface_mp.append((strike, expiry, price))
        surface_heston.append((strike, expiry, heston_price))

    surface_heston = sorted(surface_heston, key=cmp_to_key(lambda T1, T2: cmp(T1, T2, 0)))
    surface_mp = sorted(surface_mp, key=cmp_to_key(lambda T1, T2: cmp(T1, T2, 0)))
    X_MP = [x for x, y, z in surface_mp]
    X_HESTON = [x for x, y, z in surface_heston]

    surface_heston = sorted(surface_heston, key=cmp_to_key(lambda T1, T2: cmp(T1, T2, 1)))
    surface_mp = sorted(surface_mp, key=cmp_to_key(lambda T1, T2: cmp(T1, T2, 1)))
    Y_MP = [y for x, y, z in surface_mp]
    Y_HESTON = [y for x, y, z in surface_heston]

    surface_heston = sorted(surface_heston, key=cmp_to_key(lambda T1, T2: cmp(T1, T2, 2)))
    surface_mp = sorted(surface_mp, key=cmp_to_key(lambda T1, T2: cmp(T1, T2, 2)))
    Z_MP = [z for x, y, z in surface_mp]
    Z_HESTON = [z for x, y, z in surface_heston]

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.scatter(X_HESTON, Y_HESTON, Z_HESTON, antialiased=False, marker='*', edgecolor='red')
    surf2 = ax.scatter(X_MP, Y_MP, Z_MP)

    # plt.show()
    plt.savefig(plot_path + "MARKET_DATA_COMPARISON")
    plt.close()


def VOLATILITY_SURFACE(model, S0, r):
    time_to_maturity = []
    stock = Stock(S0)
    IV = []
    strikes = []
    for T in range(1, 25):
        for K in range(950, 1250, 10):
            option = Option(K, stock, T / 50)
            price = model.price(option)
            iv = BS_IMPLIED_VOL(price, option, r)
            if iv < 0.05:
                continue
            IV.append(iv)
            time_to_maturity.append(T)
            strikes.append(K)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf1 = ax.plot_trisurf([t / 10 for t in time_to_maturity], strikes, [iv for iv in IV],
                            linewidth=0.1, antialiased=False)
    surf2 = ax.plot_trisurf([t / 10 for t in time_to_maturity], strikes, [iv for iv in IV],
                            linewidth=0.1, antialiased=True, cmap='hot')
    # ax.scatter(time_to_maturity, strikes, np.array(IV))

    fig.colorbar(surf1, shrink=0.5, aspect=5)
    # plt.show()
    plt.savefig("IMPLIED_VOLATILITY_SURFACE")
