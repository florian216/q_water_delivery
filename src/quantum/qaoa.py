import itertools
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pre_treatment import provinces

REGION_EDGES = [
    (0, 1), (0, 5), (1, 3), (1, 10), (2, 4), (2, 6), (2, 8), (2, 9),
    (3, 5), (3, 8), (3, 10), (4, 6), (4, 9), (6, 7), (7, 8), (8, 10)
]


def gen_w(edges, population):
    n = len(population)
    A = np.eye(n)
    for s, r in edges:
        if max(s, r) < n:
            A[s, r] = A[r, s] = 1.0
    pop = np.asarray(population, dtype=float)
    return A * (pop / pop.max())[None, :]


def water_qubo(w, S, mu=None): # LE QUBO DE LA SLIDE 5
    n = w.shape[0]
    a = w.sum(axis=1)
    if mu is None:
        mu = 1.1 * a.max()
    Q = np.full((n, n), mu)
    np.fill_diagonal(Q, -a + mu * (1 - 2 * S))
    return Q, mu * S**2


if __name__ == "__main__":
    df = provinces()
    S = 3
    p = 3

    w = gen_w(REGION_EDGES, df["population_est"].values)
    Q, const = water_qubo(w, S)

    np.set_printoptions(precision=3, suppress=True, linewidth=200)
    print(f"w ({w.shape[0]}x{w.shape[1]}) :\n{w}\n")
    print(f"QUBO Q ({Q.shape[0]}x{Q.shape[1]}), S={S}, mu={Q[0, 1]:.3f} :\n{Q}\n")
    print(f"Constante : {const:.3f}")