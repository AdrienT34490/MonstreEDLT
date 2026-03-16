import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns
import plotly.graph_objects as go

from matplotlib import cm
from matplotlib.ticker import LinearLocator


def flat2dice(x):
    if x > 10.5:
        x = x - 10.5
        nbr_de = 3
        bonus = int(x)
    else:
        nbr_de = round(x // 3.5)
        bonus = round(x % 3.5)

    return f"{nbr_de}D6 + {bonus}"

def flat2complexite(x):
    complexite = 0
    if x >= 9:
        complexite = complexite + 9
        x = x - 11

        complexite = complexite + x
    else:
        complexite = complexite + x

    return complexite

def compute_factor(power) -> float:
    """
    Computes the factor
    :param power: base value of the mob
    :return: associated factor in %
    """
    amplitude       = 24
    shift           = -5.83436
    offset          = 1

    denominator = 1 + np.exp(-(power + shift))

    return (amplitude / denominator) + offset

def compute_value(danger, luck) -> int:
    """
    Computes the number of PO dropped while searching with luck
    :param danger: danger of the monster
    :param luck: luck value determining the value in gold
    :return: gold value of the item dropped
    """
    return int((danger - 5) * (luck / 2) * 15)

def plot_stats(df):

    plt.figure(figsize=(10,6))

    x = df["Danger"]

    for col in df.columns:
        if col not in ["Level", "Power", "Danger"]:
            plt.plot(x, df[col], label=col)

    plt.xlabel("Danger")
    plt.ylabel("Value")
    plt.title("Mob scaling")
    plt.legend()
    plt.grid()

    plt.show()

def interactive_heatmap(df):

    stats = [
        "Danger",
        "Gold",
        "XP",
        "Mean Damage",
        "Max Damage",
        "Mean Complexity",
        "Max Complexity"
    ]

    # première stat affichée
    pivot = df.pivot(index="Level", columns="Power", values=stats[0])

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale="jet"
        )
    )

    buttons = []

    for stat in stats:
        pivot = df.pivot(index="Level", columns="Power", values=stat)

        buttons.append(
            dict(
                label=stat,
                method="update",
                args=[
                    {"z": [pivot.values]},
                    {"title": f"{stat} heatmap"}
                ]
            )
        )

    fig.update_layout(
        title=f"{stats[0]} heatmap",
        xaxis_title="Power",
        yaxis_title="Level",
        updatemenus=[
            dict(
                buttons=buttons,
                direction="down",
                showactive=True,
                x=1.15,
                y=1
            )
        ]
    )

    fig.show()

