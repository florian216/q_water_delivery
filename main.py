"""
Pipeline :
    1) Pré-traitement : construction des provinces (capitale + population).
       + tracé du graphe des régions (plots/regions_<n>.svg).
    2) Formulation QUBO du problème de distribution d'eau.
"""

from pathlib import Path

import numpy as np

from plot_graphs import plot
from src.pre_treatment import provinces
from src.qubo_formulation import REGION_EDGES, gen_w, water_qubo

S = 3  # nombre de sources actives (S_max)
ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "qubos"
PLOTS_DIR = ROOT / "plots"


def main():
    # 1) Pré-traitement
    df = provinces()
    print(df.to_string())
    print(f"\nPopulation totale : {df['population_est'].sum()}\n")

    # Graphe des régions
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    plot(df, len(df), govt_edges=REGION_EDGES, scale=5e3, fname=PLOTS_DIR / "regions")
    print(f"Graphe sauvegardé dans {PLOTS_DIR / f'regions_{len(df)}.svg'}\n")

    # 2) Formulation QUBO
    w = gen_w(REGION_EDGES, df["population_est"].values)
    Q, const = water_qubo(w, S)

    np.set_printoptions(precision=3, suppress=True, linewidth=200)
    print(f"w ({w.shape[0]}x{w.shape[1]}) :\n{w}\n")
    print(f"QUBO Q ({Q.shape[0]}x{Q.shape[1]}), S={S}, mu={Q[0, 1]:.3f} :\n{Q}\n")
    print(f"Constante : {const:.3f}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / f"qubo_regions_S{S}.txt"
    np.savetxt(out, Q)
    print(f"\nQUBO sauvegardé dans {out}")

    return Q, const


if __name__ == "__main__":
    main()
