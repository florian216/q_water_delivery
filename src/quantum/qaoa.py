import itertools
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pre_treatment import provinces
from qubo_formulation import REGION_EDGES, gen_w, water_qubo


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