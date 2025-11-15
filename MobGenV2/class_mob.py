from __init__ import STATS, EXP_THRESHOLD, MOD_PRICE, MOB_TYPE, SAVE_PATH
from utils import compute_factor, flat2dice, flat2complexite

import numpy as np
import warnings
import json
from pathlib import Path

class Mob:
    def __init__(self, name: str, floor: int, base: int, main_stat: str):
        # Assigned attribute values
        self.mob_dict: dict  = {}
        self.floor: int      = floor
        self.base: int       = base
        self.main_stat: str  = main_stat

        if len(name) != 0:
            self.name: str = name
        else:
            self.name: str = "defaultMobName"

        self.mob_type   = None
        for key, value in MOB_TYPE.items():
            if self.base == value:
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
        string  = f'This is {self.name}, from the {self.floor} floor and is of the "{self.mob_type}" type.\n'
        string += f"Danger level : {self.danger}\n"
        string += f"You may encounter {self.mob_nbr} ({flat2dice(self.mob_nbr)}) mobs at a time.\n"

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
            "danger", "floor", "base", "mean_dmg", "factor"
            "mean_cmplx", "max_dmg", "max_cmplx", "mob_nbr",
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
        self.mob_nbr: int = 0
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
        # Danger
        self.danger = int(self.floor * 10 + self.base)

        # factor
        self.factor = float(compute_factor(self.base))

        # Experience
        delta_exp = EXP_THRESHOLD[self.floor] - EXP_THRESHOLD[self.floor - 1]
        self.exp = int(max(0, round(self.factor * delta_exp)))

        # Gold
        self.gold = int(round(self.factor * 2 * self.floor * MOD_PRICE))

        # Life Point
        lp_multiplier = round(self.factor * 70)
        self.lp = int(round(20 + self.floor * lp_multiplier))


    def build_stats(self):
        """
        Method to build the stats of the mob
        :return:
        """
        self.stats: dict = STATS.copy()
        del self.stats["Aucune"]

        stats_name = list(self.stats.keys())
        stats_offset = int(
            np.ceil(
                self.factor * 100 / 4
            ) - 5
        )
        stats_points = int(
            np.ceil(
                self.floor * 4 + stats_offset
            )
        )

        if self.main_stat != "Aucune":
            points_pref = self.floor
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
        # Damage
        player_lp = 20 + self.floor * 7
        avg_atk_nbr = (1 / self.factor) * 0.5
        self.mean_dmg = int(np.ceil(player_lp / avg_atk_nbr))

        player_lp_np1 = 20 + (self.floor + 1) * 7
        max_atk_nbr = (1 / self.factor) * 0.5
        self.max_dmg = int(np.ceil(player_lp_np1 / max_atk_nbr))

        # Spell complexity
        self.mean_cmplx = int(flat2complexite(self.mean_dmg))
        self.max_cmplx = int(flat2complexite(self.max_dmg))

        # Encounter
        fight_length = 3.5
        self.mob_nbr = int(np.ceil(avg_atk_nbr / fight_length))

        # CA
        self.ca = int(
            np.ceil(
                max(
                    0,
                    7 +
                    self.stats["Adresse"] +
                    self.stats["Constitution"] +
                    self.base
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
                    self.base
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