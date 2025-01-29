from parametre import liste_pallier_xp
import math
import random as rd

def flat2dice(x):
    nbr_dé = round(x // 3.5)
    bonus = round(x % 3.5)

    return(f"{nbr_dé}D6 + {bonus}")

def flat2complexite(x):
    complexite = 0
    if x >= 9:
        complexite = complexite + 9
        x = x - 11

        complexite = complexite + x
    else:
        complexite = complexite + x

    return complexite

def generer_monstre(etage, base, carac_pref=None):
    # -----{Facteur}
    ampli = 53.01537
    shift = -6.70181
    offset_facteur = 1.82352
    def calcul_facteur(y):
        expo = -(y + shift)
        return ((ampli / (1 + math.exp(expo))) + offset_facteur)*0.01
    facteur = calcul_facteur(base)
    
    # -----{Danger}
    danger = base + etage * 10

    # -----{Carac}
    carac = {
    "Force": 0,
    "Adresse": 0,
    "Constitution": 0,
    "Intelligence": 0,
    "Perception": 0, 
    "Charisme": 0,
    }
    noms_carac = list(carac.keys())
    offset_carac = math.ceil(facteur * 100 / 4) - 5
    points_carac = (etage - 1) * 4 + offset_carac

    if carac_pref != "Aucune":
        points_pref = round(points_carac * (1/6), 0)
        carac[carac_pref] = abs(points_pref)
        points_carac = int(points_carac - points_pref)

    for iter in range(abs(points_carac)):
        choix = rd.choice(noms_carac)
        if carac_pref != "Aucune" and carac[choix] + 1 > carac[carac_pref]:
            if math.copysign(1, points_carac) > 0:
                carac[carac_pref] = carac[carac_pref] + math.copysign(1, points_carac)
            else:
                carac[choix] = carac[choix] + math.copysign(1, points_carac)
        else:
            carac[choix] = carac[choix] + math.copysign(1, points_carac)
            


    # -----{Exp}
    delta_XP = liste_pallier_xp[etage] - liste_pallier_xp[etage-1]
    xp = round(facteur * delta_XP)
    if xp < 0:
        xp = 0

    # ------{PO}
    prix_mod = 150
    PO = round(facteur * 150 * 0.2 * 10 * etage)

    # -----{PV}
    multiplicateur = round(facteur * 70)
    PV_monstre = round(10 + etage * multiplicateur)

    # -----{Dégâts}
    PV_aventurier = 20 + etage * 7
    nbr_attaques_moy = (1/facteur) * (0.5)
    dgt_moy = math.ceil(PV_aventurier / nbr_attaques_moy)

    PV_aventurier_np1 = 20 + (etage+1) * 7
    nbr_attaques_max = (1/facteur) * (0.5)
    dgt_max = math.ceil(PV_aventurier_np1 / nbr_attaques_max)

    # -----{Rencontre}
    duree_combat = 3.5
    nbr_monstre = nbr_attaques_moy / duree_combat
    nbr_monstre = math.ceil(nbr_monstre)

    return {"Danger": danger,
            "Caractéristiques": carac,
            "XP": xp,
            "PV": f"{PV_monstre} | {flat2dice(PV_monstre)}",
            "PO": f"{PO} | {flat2dice(PO)}",
            "Dégâts moyens": f"{dgt_moy} | {flat2dice(dgt_moy)}",
            "Dégâts max": f"{dgt_max} | {flat2dice(dgt_max)}",
            "Complexité moyenne": f"{flat2complexite(dgt_moy)}",
            "Complexité max": f"{flat2complexite(dgt_max)}",
            "Dé de rencontre": flat2dice(nbr_monstre),
            "CA": carac["Constitution"] + 10 + etage,
            "CE": carac["Intelligence"] + 10 + etage,
            "SD": carac["Adresse"] + 7 + etage,
            }

if __name__ == "__main__":
    étage = 9
    for base in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        monstre = generer_monstre(étage, base, "Force")

        print(f"Danger de base / total : {base} / {monstre["Danger"]}")

        carac = monstre["Caractéristiques"]
        print(f"    - Carac : {carac}")

        XP = monstre["XP"]
        print(f"    - XP : {XP}")

        PV = monstre["PV"]
        print(f"    - PV : {PV} ({flat2dice(PV)})")

        dgt = monstre["Dégâts moyens"]
        dgt_max = monstre["Dégâts max"]
        print(f"    - Degats moy / max: {dgt} ({flat2dice(dgt)}) / {dgt_max} ({flat2dice(dgt_max)})")

        nbr_monstre = monstre["Dé de rencontre"]
        print(f"    - dé de rencontre: {nbr_monstre} ({flat2dice(nbr_monstre)})")

        complexite_moy = monstre["Complexité moyenne"]
        complexite_max = monstre["Complexité max"]
        print(f"    - complexité moyenne / max: {complexite_moy} / {complexite_max}")
        print("")