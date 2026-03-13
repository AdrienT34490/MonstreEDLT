"""
This is the file that stores global variables.
"""

from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_DIR = SCRIPT_PATH.parent

SAVE_PATH = SCRIPT_DIR / "Mobs"

MOD_PRICE = 150

EXP_THRESHOLD = [
    0,
    300,
    900,
    2700,
    6500,
    14000,
    23000,
    34000,
    48000,
    64000,
    100000
]

LEVEL = {
    "nul (0)":         0,
    "Léger (1)":       1,
    "Atténué (2)":     2,
    "Connu (3)":       3,
    "Redouté (4)":     4,
    "Craint (5)":      5,
    "Urbain (6)":      6,
    "Régionnal (7)":   7,
    "Provincial (8)":  8,
    "Continental (9)": 9,
    "Planétaire (10)": 10,
}

MOB_TYPE = {
    "Essaim (1)":       1,
    "Bénin (2)":        2,
    "Minable (3)":      3,
    "Faible (4)":       4,
    "Moyen (5)":        5,
    "Fort (6)":         6,
    "Exceptionnel (7)": 7,
    "Sous boss (8)":    8,
    "Boss (9)":         9,
    "Guardien (10)":    10
}

STATS = {
    "Aucune":           None,
    "Force":            0,
    "Adresse":          0,
    "Constitution":     0,
    "Intelligence":     0,
    "Perception":       0,
    "Charisme":         0,
}