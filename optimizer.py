from functools import cmp_to_key

import numpy as np
from scipy.optimize import minimize

from data import preprocess_data
from heston_model import HestonModel, Stock, Option


class ModelParams:
    def __init__(self, kappa, theta, v0, rho, n):
        self.mean_reversion_rate = kappa
        self.long_term_mean_variance = theta
        self.initial_variance = v0
        self.correlation = rho
        self.vol_of_variance = n


def error_func(params, df, S0):
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

        error += ((mp - price) / price) ** 2
        mp_sum += price * price
    return error / df.size


def shrink_population(population, size, df, S0):
    print("Shrinking population from x to y".replace('x', str(len(population))).replace('y', str(size)))
    score = [(params, error_func(params, df, S0)) for params in population]

    score = sorted(score, key=cmp_to_key(lambda x, y: 0 if x[1] == y[1] else (-1 if x[1] < y[1] else 1)))

    return score[:size]


def cdf(score):
    print("Generating cdf")
    score_prefix_sum = 0

    s = [1 / x for x in score]
    p = []
    for x in s:
        score_prefix_sum += x
        p.append(score_prefix_sum)

    p = [x / score_prefix_sum for x in p]

    return p


def draw_from_population(population, p):
    i = 0
    draw = np.random.rand()
    while i < len(population):
        if draw < p[i]:
            return population[i]
        i += 1


def genetic_optimizer(n_gen, df, S0, mutation_probability=0):
    population = [np.random.random(5) for x in range(20)]
    population = [[x[0] * 5, x[1] / 10, x[2] / 10, - x[3], x[4]] for x in population]
    t = shrink_population(population, 20, df, S0)
    population, score = [x[0] for x in t], \
        [x[1] for x in t]

    p = cdf(score)

    for i in range(n_gen):
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Running for generation " + str(i))
        for i in range(20):
            parent1 = draw_from_population(population, p)
            parent2 = draw_from_population(population, p)
            offspring = [x for x in parent1]
            for i in range(len(parent1)):
                if np.random.rand() > 0.5:
                    offspring[i] = parent2[i]
            population.append(offspring)

        print("Offsprings created")
        t = shrink_population(population, 20, df,S0)
        population, score = [x[0] for x in t], \
            [x[1] for x in t]

    print(population[0], score[0])
    return population[0], score[0]
