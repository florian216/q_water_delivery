"""Formulation QUBO du problème de distribution d'eau (régions administratives)."""

import numpy as np

REGION_EDGES = [
    (0, 1), (0, 5), (1, 3), (1, 10), (2, 4), (2, 6), (2, 8), (2, 9),
    (3, 5), (3, 8), (3, 10), (4, 6), (4, 9), (6, 7), (7, 8), (8, 10)
]


def gen_w(edges, population):
    """Matrice des poids w[s, r] : population normalisée de r si s et r sont voisins (ou s == r)."""
    n = len(population)
    A = np.eye(n)
    for s, r in edges:
        if max(s, r) < n:
            A[s, r] = A[r, s] = 1.0
    pop = np.asarray(population, dtype=float)
    return A * (pop / pop.max())[None, :]


def water_qubo(w, S, mu=None):  # LE QUBO DE LA SLIDE 5
    """
    QUBO : min x^T Q x + const, avec x_s = 1 si la source s est active.
    Maximise l'eau livrée sous la contrainte sum_s x_s = S (pénalité mu).
    """
    n = w.shape[0]
    a = w.sum(axis=1)
    if mu is None:
        mu = 1.1 * a.max()
    Q = np.full((n, n), mu)
    np.fill_diagonal(Q, -a + mu * (1 - 2 * S))
    return Q, mu * S**2
