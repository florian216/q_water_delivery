"""
This module draws basic plots representing the graphs:
    - Positions of the cities
    - Their sizes and labels
    - Highlighted administrative centres
"""

import numpy as np
import matplotlib.pyplot as plt

def plot(df, n, city_edges=None, govt_edges=None, scale=1e3, fname="fname"):
    """
    Plot a graph representing cities and connections.

    Parameters:
        df (pd.DataFrame): DataFrame with GPS + population
        n (int): Number of cities to include
        city_edges (list): Edges between cities
        govt_edges (list): Edges between governorates
        scale (float): Marker scaling factor
        fname (str): Output file name
    """

    if (city_edges is not None) + (govt_edges is not None) != 1:
        raise ValueError("Exactly one list of edges must be provided.")

    # Keep only the largest n cities
    df = df.head(n)

    longitudes = df["longitude"]
    latitudes = df["latitude"]
    pops = df["population_est"]

    try:
        is_admin_centre = df["admin_centre"].values
    except Exception:
        is_admin_centre = None

    n = len(latitudes)

    fig, ax = plt.subplots(figsize=(4, 9))

    # Plot nodes
    for idx, (lon, lat, pop) in enumerate(zip(longitudes, latitudes, pops)):
        plt.scatter(lon, lat, s=pop / scale, color="tab:blue")

        # Label nodes
        plt.text(lon, lat, idx, ha="center", va="center", size=12)

        # Highlight administrative centres
        if is_admin_centre is not None and is_admin_centre[idx]:
            plt.scatter(lon, lat, s=pop / scale, color="tab:orange")

    # Plot edges (quadratic Bézier curves)
    for city1 in range(n):
        x1, y1 = longitudes[city1], latitudes[city1]

        for city2 in range(city1):
            if city_edges is not None and (city2, city1) not in city_edges:
                continue
            if govt_edges is not None and (city2, city1) not in govt_edges:
                continue

            x2, y2 = longitudes[city2], latitudes[city2]

            # Control point for Bézier curve (simple heuristic)
            X, Y = x2 + (x1 - x2) * 0.3, y1

            t = np.linspace(0, 1, 100)
            xb = X + (1 - t) ** 2 * (x1 - X) + t**2 * (x2 - X)
            yb = Y + (1 - t) ** 2 * (y1 - Y) + t**2 * (y2 - Y)

            plt.plot(xb, yb, color="grey", lw=2, zorder=-3)

    ax.set_axis_off()
    plt.savefig(f"{fname}_{n}.svg", transparent=True, bbox_inches="tight")
    plt.close()

