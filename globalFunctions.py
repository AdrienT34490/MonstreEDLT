import random as rd
import math as math


def jetDeDes(nombre, faces):
    """
    Fonction permetant de jeter un dé.
    :param nombre: Nombre de dé
    :param faces: Nombre de face
    :return: nombre compris entre [nombre; nombre*faces]
    """
    resultat = 0

    for jetNumero in range(0, nombre):
        resultat = resultat + rd.choice(range(1, faces + 1))

    return resultat


def flatToDice(bonusFlat):
    """
    Fonction permettant de transformer un montant en nombre de dé 6
    :param bonusFlat: nombre à convertir
    :return: nombre de dés à jeter pour obtenir ce nombre en moyenne
    """
    de = int(bonusFlat // 3.5)
    if de < 0:
        de = 0

    bonusFlat = int(bonusFlat % 3.5)
    if bonusFlat < 0:
        bonusFlat = 0
    return f"{de}D6 + {bonusFlat}"


def diceToFlat(chaine):
    """
    Fonction permettant de transformer un montant de dé 6 en la moyenne du resultat du jet
    :param chaine: chaine de caractère qui définit le nombre de dés à jeter et un bonus éventuel
    :return: moyenne statistique de ce jet
    """
    ajoutDe(chaine)
    de, bonus = chaine.split("+")
    bonusFlat = int(bonus)
    nombre, face = de.split("D")
    bonusFlat = bonusFlat + int(nombre) * 3.5

    return int(bonusFlat)


def ajoutDe(chaine):
    """
    Fonction permettant d'ajouter des dés 6. Exemple "1D6+3D6+8" retournera 4d6+8
    :param chaine:
    :return:
    """
    chaine = chaine.split("+")

    nombreDe = 0
    for de in chaine:
        if "D" in de:
            nombreDe = nombreDe + int(de.split("D")[0])
    chaine = f"{nombreDe}D6 + {chaine[-1].strip()}"
    return chaine