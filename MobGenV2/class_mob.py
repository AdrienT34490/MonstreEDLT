from . import STATS, EXP_THRESHOLD, MOD_PRICE, MOB_TYPE, SAVE_PATH, LEVEL
from .utils import *

import numpy as np
import pandas as pd
import json

import os
os.environ["QT_DEBUG_PLUGINS"] = "1"

def create_xls(display=False) -> None:
    level_list = np.linspace(0, 10, 11, endpoint=True)
    power_list = np.linspace(1, 10, 10, endpoint=True)

    rows = []

    for level in level_list:
        for power in power_list:
            mob = Mob("", int(level), int(power), "Aucune")

            rows.append({
                "Level": int(level),
                "Power": int(power),
                "Danger": mob.danger,
                "Stats": mob.stats_points,
                "Gold": mob.gold,
                "XP": mob.exp,
                "Mean Damage": mob.mean_dmg,
                "Max Damage": mob.max_dmg,
                "Mean Complexity": mob.mean_cmplx,
                "Max Complexity": mob.max_cmplx
            })

    df = pd.DataFrame(rows)
    df.to_excel("mob_stats.xlsx", index=False)
    if display:
        interactive_heatmap(df)

class Mob:
    def __init__(self, name: str, level: int, power: int, main_stat: str):
        # Assigned attribute values
        self.mob_dict: dict  = {}
        self.level: int      = level
        self.power: int      = power
        self.main_stat: str  = main_stat

        if len(name) != 0:
            self.name: str = name
        else:
            self.name: str = "defaultMobName"

        self.mob_level  = None
        for key, value in LEVEL.items():
            if self.level == value:
                self.mob_level = key

        self.mob_type   = None
        for key, value in MOB_TYPE.items():
            if self.power == value:
                self.mob_type = key

        # Default attribute values
        self._assign_default()

        # Building of attributes
        self.build_basic_stats()
        self.build_stats()
        self.build_combat()


    def __str__(self):
        """
        String representation of Mob
        :return: string representation of Mob
        """
        string  = f'This is {self.name}, from the {self.level} floor and is of the "{self.mob_type}" type.\n'
        string += f"Danger level : {self.danger}\n"

        string += f"Mob statistics:\n"
        for key, value in self.stats.items():
            string += f"\t{key}: {value}\n"

        string += f"He has an average of {self.lp} life points ({flat2dice(self.lp)}).\n"
        string += (f"He inflicts an average of {self.mean_dmg} life points ({flat2dice(self.mean_dmg)}) "
                   f"and inflicts a maximum of {self.max_dmg} life points ({flat2dice(self.max_dmg)})\n")
        string += (f"The complexity of his spell is on average {self.mean_cmplx} ({flat2dice(self.mean_dmg)}) "
                   f"and is {self.max_cmplx} ({flat2dice(self.max_cmplx)}) at most.\n")
        string += f"On death, the mob drops {self.exp} experience points and {self.gold} gold.\n"

        return string

    def __setattr__(self, key, value):
        positive_values = [
            "danger", "level", "power", "mean_dmg", "factor"
            "mean_cmplx", "max_dmg", "max_cmplx",
            "exp", "gold", "lp", "ca", "ce"
        ]

        if key in positive_values and value < 0:
                raise ValueError(f"Negative values are not allowed for {key}")

        if key == "main_stat" and value not in STATS.keys():
                raise ValueError(f"{value} is not a valid main stat. Valid main stats are {STATS.keys()}")

        if key != "mob_dict":
            self.mob_dict[key] = value

        super().__setattr__(key, value)

    def _assign_default(self):
        """
        Assign default attributes values
        """
        self.stats: dict = {}
        self.danger: int = 0
        self.factor: float = 0.0
        self.exp: int = 0
        self.gold: int = 0
        self.lp: int = 0
        self.mean_dmg: int = 0
        self.mean_cmplx: int = 0
        self.max_dmg: int = 0
        self.max_cmplx: int = 0
        self.ca: int = 0
        self.ce: int = 0
        self.sd: int = 0

    def save_mob(self, name: str | None = None):
        """
        Save mob as .json file
        """
        if name is None:
            base_name = f"{self.name}.json"
        else:
            base_name = f"{name}.json"

        SAVE_PATH.mkdir(parents=True, exist_ok=True)
        dest_path = SAVE_PATH / base_name

        file_nbr = 1
        while dest_path.exists():
            dest_path = SAVE_PATH / f"{base_name} - ({file_nbr}).json"
            file_nbr += 1

        with dest_path.open("w", encoding="utf-8") as dest:
            json.dump(self.mob_dict, dest, indent=4)



    def build_basic_stats(self):
        """
        Build basic stats for this Mob
        """
        # refs
        facteur_1 = compute_factor(1)
        facteur_4 = compute_factor(4)
        facteur_5 = compute_factor(5)
        facteur_9 = compute_factor(9)
        # Danger
        self.danger = int(self.level * 10 + self.power)

        # factor
        self.factor = float(compute_factor(self.power))

        # Experience
        delta_exp = EXP_THRESHOLD[self.level] - EXP_THRESHOLD[self.level - 1]
        self.exp = int(max(0, self.factor * 0.01 * delta_exp))

        # Gold
        po_level = (self.level*MOD_PRICE)/6
        po_power = (self.factor - facteur_4) * (self.level*(MOD_PRICE - (MOD_PRICE/6))) / (facteur_9 - facteur_4)
        self.gold = int(po_level + po_power)

        # Life Point
        lp_adder = (self.factor - facteur_5) / (facteur_1 - facteur_5) * -22
        self.lp = max(1, int(20 + self.level*7 + lp_adder))


    def build_stats(self):
        """
        Method to build the stats of the mob
        :return:
        """
        facteur_4 = compute_factor(4)
        facteur_9 = compute_factor(9)
        self.stats: dict = STATS.copy()
        del self.stats["Aucune"]

        stats_name = list(self.stats.keys())
        stats_offset = ((self.factor - facteur_4) / (facteur_9 - facteur_4)) * 3
        stats_points = int(
            np.ceil(
                (self.level-1) * 3 + (self.level * stats_offset)
            )
        )
        self.stats_points = stats_points

        if self.main_stat != "Aucune":
            points_pref = self.level
            self.stats[self.main_stat] = points_pref
            stats_points = int(stats_points - points_pref)

        for iteration in range(abs(stats_points)):
            choix = np.random.choice(stats_name, replace=True)
            if self.main_stat != "Aucune" and self.stats[choix] + 1 > self.stats[self.main_stat]:
                if np.sign(stats_points) > 0:
                    self.stats[self.main_stat] = int(self.stats[self.main_stat] + np.sign(stats_points))
                else:
                    self.stats[choix] = int(self.stats[choix] + np.sign(stats_points))
            else:
                self.stats[choix] = int(self.stats[choix] + np.sign(stats_points))

    def build_combat(self):
        """
        Method to build the mob's damage
        :return:
        """
        facteur_9 = compute_factor(9)
        facteur_4 = compute_factor(4)

        # Damage
        player_lp = 20 + self.level * 7
        player_lp_max = player_lp + 5
        avg_atk_nbr = 3

        dmg_offset = (self.factor - facteur_4) / (facteur_9 - facteur_4) * 7
        self.mean_dmg = int(player_lp / avg_atk_nbr + dmg_offset)

        dmg_max_offset = (self.factor - facteur_4) / (facteur_9 - facteur_4) * 12
        self.max_dmg = int(player_lp_max / avg_atk_nbr + dmg_max_offset)

        # Spell complexity
        self.mean_cmplx = int(flat2complexite(self.mean_dmg))
        self.max_cmplx = int(flat2complexite(self.max_dmg))

        # CA
        mod_score = ((self.factor - facteur_4) / (facteur_9 - facteur_4) * 2)+4
        print(mod_score)
        self.ca = int(
            np.ceil(
                max(
                    0,
                    7 +
                    self.stats["Adresse"] +
                    self.stats["Constitution"] +
                    mod_score
                )
            )
        )

        # CE
        self.ce = int(
            np.ceil(
                max(
                    0,
                    7 +
                    self.stats["Intelligence"] +
                    self.stats["Perception"] +
                    mod_score
                )
            )
        )

        # SD
        self.sd = int(
            np.floor(
                max(
                    0,
                    7 + self.stats["Adresse"]
                )
            )
        )

if __name__ == "__main__":
    oui = Mob("Tabouret", 0, 1, "Aucune")
    print(str(oui))