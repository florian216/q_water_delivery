"""
This module draws basic plots representing the graphs:
    - Positions of the cities
    - Their sizes and labels
    - Highlighted administrative centres
"""

import numpy as np
import matplotlib.pyplot as plt

def plot(
    df,
    n,
    city_edges=None,
    govt_edges=None,
    scale=1e3,
    fname="fname",
    selection=None,
    min_size=600,
):
    """
    Plot a graph representing cities and connections.

    Parameters:
        df (pd.DataFrame): DataFrame with GPS + population
        n (int): Number of cities to include
        city_edges (list): Edges between cities
        govt_edges (list): Edges between governorates
        scale (float): Marker scaling factor (population / scale added to min_size)
        fname (str): Output file name
        selection (array-like of 0/1, optional): QUBO result. Nodes with 1 are
            filled in colour, nodes with 0 are drawn as empty circles.
        min_size (float): Minimum marker area (points^2), so small nodes stay visible
    """

    if (city_edges is not None) + (govt_edges is not None) != 1:
        raise ValueError("Exactly one list of edges must be provided.")

    # Keep only the largest n cities (positional indexing from here on)
    df = df.head(n).reset_index(drop=True)

    longitudes = df["longitude"].to_numpy()
    latitudes = df["latitude"].to_numpy()
    pops = df["population_est"].to_numpy()

    # Normalise edges so (a, b) and (b, a) are equivalent
    edges = city_edges if city_edges is not None else govt_edges
    edges = {(min(a, b), max(a, b)) for a, b in edges}

    try:
        is_admin_centre = df["admin_centre"].values
    except Exception:
        is_admin_centre = None

    n = len(latitudes)

    if selection is not None:
        selection = np.asarray(selection).astype(int).ravel()
        if len(selection) != n:
            raise ValueError(
                f"selection has length {len(selection)}, expected {n} (one 0/1 per node)."
            )

    sizes = min_size + pops / scale

    fig, ax = plt.subplots(figsize=(4, 9))

    # Plot nodes
    for idx, (lon, lat, size) in enumerate(zip(longitudes, latitudes, sizes)):
        if selection is not None:
            # QUBO result: 1 -> filled, 0 -> empty circle
            if selection[idx]:
                ax.scatter(lon, lat, s=size, color="tab:red", edgecolors="black", lw=1.5)
            else:
                ax.scatter(lon, lat, s=size, facecolors="white", edgecolors="grey", lw=1.5)
        elif is_admin_centre is not None and is_admin_centre[idx]:
            # Highlight administrative centres
            ax.scatter(lon, lat, s=size, color="tab:orange")
        else:
            ax.scatter(lon, lat, s=size, color="tab:blue")

        # Label nodes
        ax.text(lon, lat, idx, ha="center", va="center", size=12, zorder=3)

    # Plot edges (quadratic Bézier curves)
    for city1 in range(n):
        x1, y1 = longitudes[city1], latitudes[city1]

        for city2 in range(city1):
            if (city2, city1) not in edges:
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

