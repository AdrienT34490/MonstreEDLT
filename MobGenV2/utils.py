from . import EXP_THRESHOLD

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator


def flat2dice(x):
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

def compute_factor(base) -> float:
    """
    Computes the factor
    :param base: base value of the mob
    :return: associated factor
    """
    amplitude       = 53.01537
    shift           = -6.70181
    offset          = 1.82352

    denominator = 1 + np.exp(-(base + shift))

    return ((amplitude / denominator) + offset) * 0.01

if __name__ == "__main__":
    base_list = np.arange(0, 10, 0.1)
    floor_list = np.arange(0, 10, 0.1)
    base_mesh, floor_mesh = np.meshgrid(base_list, floor_list)

    fig, ax = plt.subplots(1, 1)
    ax.plot(base_list, compute_factor(base_list))
    plt.show()
