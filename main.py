from functools import cmp_to_key

import numpy as np
from matplotlib import pyplot as plt
from data import get_data
from heston_model import HestonModel, Stock, Option
from optimizer import get_params, error_func, ModelParams


def grid_search():
    min_error = 1
    optimal_params = None
    for kappa in range(1, 5000, 100):
        for theta in range(1, 100, 10):
            for v0 in range(1, 100, 10):
                for rho in range(-10, 10):
                    for sigma in range(1, 100):
                        kappa /= 1000.
                        theta /= 1000.
                        v0 /= 1000.
                        rho /= 10.
                        m = HestonModel(sigma, rho, kappa, theta, v0, 0.072)
                        error = error_func([kappa, theta, v0, rho, sigma], m)
                        if error < min_error:
                            min_error = error
                            optimal_params = [kappa, theta, v0, rho, sigma]
                        print([kappa, theta, v0, rho, sigma], error)
    print("OPTIMAL")
    m = HestonModel(optimal_params[4], optimal_params[3], optimal_params[0], optimal_params[1], optimal_params[2], 0.072)
    error = error_func(np.ndarray(optimal_params), m)
    print(error, optimal_params)


S0 = 1590.75

p = {
    "kappa": {"x0": 4, "lbub": [1e-3, 5]},
    "theta": {"x0": 0.1, "lbub": [1e-3, 0.1]},
    "v0": {"x0": 0.01, "lbub": [1e-3, 0.1]},
    "rho": {"x0": -0.88, "lbub": [-1, 0]},
    "sigma": {"x0": 0.73, "lbub": [1e-2, 1]},
}
x0 = [param["x0"] for key, param in p.items()]
kappa, theta, v0, rho, n = x0

df = get_data()
model = HestonModel(n, rho, kappa, theta, v0, 0.072)
params = get_params(model, [1] * 5)
surface_mp = []
surface_heston = []

strikes_list, expiry_list, price_list = df['STRIKE'], df['EXPIRY'].transform(lambda x: x / 242), df['CLOSE']
print(len(strikes_list), len(expiry_list),len(price_list), df.size)

for strike, expiry, price in zip(df['STRIKE'], df['EXPIRY'].transform(lambda x: x / 242), df['CLOSE']):
    option = Option(strike, Stock(S0), expiry)
    heston_price = model.price(option)

    surface_mp.append((strike, expiry, price))
    surface_heston.append((strike, expiry, heston_price))


def cmp(T1, T2, j):
    if T1[j] == T2[j]:
        return 0
    if T1[j] < T2[j]:
        return -1
    else:
        return 1


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

# ax.scatter(time_to_maturity, strikes, np.array(IV))
print(error_func(params, model), params)
# print(error_func(np.ndarray(x0, dtype=int)))
plt.savefig("MARKET_DATA_COMPARISON")
plt.show()
plt.close()


# grid_search()
