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

