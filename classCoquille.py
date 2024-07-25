import random

from globalFunctions import *
from classAction import Action

"""
Infos : 
    PV d'un joueur à l'étage x : 10+xD6
    bonus de carac d'un joueur à l'étage x : 3 + x*7
    prix d'un bonus de +x : 150*x



Paramètre principal :
    étage

à générer :
    quantité de mob à rencontrer
        
    caracteristiques
        CA
        CE
        SD 
        PV 
            EXP
            PO
        degats
            nombre d'actions
"""

pallierXP = [None, 300, 900, 2700, 6500, 14000, 23000, 34000, 48000, 64000]
mobATuer = [None, 80, 80, 80, 80, 80, 80, 80, 80, 80]
elementMagie = ["feu", "air", "terre", "eau", "foudre", "glace", "vapeur", "lave", "plantes", "acide", "poison",
                "métal", "lumière", "ténèbre", "pure"]
caracteristiques = ["FOR", "ADR", "CON", "INT", "PER", "CHA"]


class Coquille:
    def __init__(self, etage):
        if etage in [4, 5, 6]:
            self.etage = 5
        else:
            self.etage = etage

        self.nom = f" étage {self.etage}"

        self.experience = 0

        self.caracteristiques = {"FOR": 0, "ADR": 0,
                                 "CON": 0, "INT": 0,
                                 "PER": 0, "CHA": 0,
                                 "PV": 10, "CA": 10,
                                 "CE": 10, "SD": 7}

        self.actions = {}

    def getActions(self):
        listeActions = []
        for action in self.actions.values():
            listeActions = listeActions + [action]

        return listeActions

    def toString(self):
        actionsPossible = ""

        for action in self.getActions():
            actionsPossible = actionsPossible + action.toString() + "\n"

        return (f"{self.nom} à les caractéristiques suivantes : \n"
                f"{self.caracteristiques} \n"
                f"Peut : \n" f"{actionsPossible}")


class Creature(Coquille):
    def __init__(self, etage, pointFort=None):
        super().__init__(etage)

        self.nom = "Créature" + self.nom

        self.PO = ""

        if pointFort is None:
            self.pointFort = "AUCUN"
        else:
            pointFort = pointFort.upper()
            pointFort = pointFort.strip()

            if pointFort in caracteristiques:
                self.pointFort = pointFort

        self.FaibResi = {"faiblesse": 0, "resistance": 0}

    def setFaibResi(self, typeMonstre):
        nombreEssai = 4
        if typeMonstre == "faible":
            print("je suis faible")
            self.FaibResi["faiblesse"] = self.FaibResi["faiblesse"] + 1
            nombreEssai = nombreEssai - 1
        elif typeMonstre == "fort":
            print("je suis fort")
            self.FaibResi["resistance"] = self.FaibResi["resistance"] + 1
            nombreEssai = nombreEssai - 1

        for essai in range(0, nombreEssai):
            resultatJet = jetDeDes(1, 6)
            if resultatJet == 1:
                print("j'ai gagné une faiblesse :(")
                self.FaibResi["faiblesse"] = self.FaibResi["faiblesse"] + 1
            elif resultatJet == 6:
                print("j'ai gagné une résistance :)")
                self.FaibResi["resistance"] = self.FaibResi["resistance"] + 1

    def toString(self):
        return (super().toString() +
                f"Sa caractéristique associée est : {self.pointFort}\n"
                f"A pour résistances et faiblesses : {self.FaibResi}\n"
                f"Rapporte : {self.experience} point d'expérience\n")

    def setCarac(self, offset, amplitude):

        if self.pointFort != "AUCUN":
            self.caracteristiques[self.pointFort] = self.etage
            bonusCarac = (offset + amplitude * self.etage) - self.etage
        else:
            bonusCarac = offset + amplitude * self.etage

        for etape in range(0, bonusCarac):
            caracChoisie = rd.choice(caracteristiques)
            self.caracteristiques[caracChoisie] = self.caracteristiques[caracChoisie] + 1

    def changeCaracMax(self):
        bonusMax = 0
        caracMax = None

        for carac in caracteristiques:
            if self.caracteristiques[carac] >= bonusMax:
                bonusMax = self.caracteristiques[carac]
                caracMax = carac

        self.caracteristiques[caracMax] = self.caracteristiques[self.pointFort]
        self.caracteristiques[self.pointFort] = bonusMax

    def setPV(self, etage, nombreDe):
        for deNumero in range(0, etage):
            self.caracteristiques["PV"] = self.caracteristiques["PV"] + jetDeDes(nombreDe, 6)

    def setExperience(self, facteur):
        self.experience = int((pallierXP[self.etage] / mobATuer[self.etage] + self.caracteristiques["PV"]) * facteur)

    def setPO(self, facteur):
        POmoyen = int(((self.etage * 150) / mobATuer[self.etage] + self.caracteristiques["PV"]) * facteur)
        self.PO = POmoyen

    def setActions(self, nombreActions):
        for i in range(1, nombreActions + 1):
            clef = f"Action{i}"
            valeur = Action()
            self.actions[clef] = valeur


class CreatureFaible(Creature):
    def __init__(self, etage, pointFort=None):
        super().__init__(etage, pointFort)

        self.setCarac(0, 4)

        if self.pointFort != "AUCUN":
            self.changeCaracMax()

        self.setPV(etage, 1)

        self.caracteristiques["CA"] = self.caracteristiques["CA"] + math.ceil(self.etage / 2)

        self.caracteristiques["CE"] = self.caracteristiques["CE"] \
                                      + math.ceil(self.caracteristiques["INT"])

        self.caracteristiques["SD"] = self.caracteristiques["SD"] \
                                      + math.ceil(self.caracteristiques["ADR"])

        self.setFaibResi("faible")

        self.setExperience(0.5)

        self.setPO(0.5)

        self.setActions(random.choice([1, 2, 3]))

        for action in self.getActions():
            action.setEtage(self.etage)
            action.setEffet("2")
            action.setDuree()
            action.setPortee()
            action.setDifficulte()


class CreatureMoyenne(Creature):
    def __init__(self, etage, pointFort=None):
        super().__init__(etage, pointFort)

        self.setCarac(3, 5)

        if self.pointFort != "AUCUN":
            self.changeCaracMax()

        self.setPV(etage, 2)

        self.caracteristiques["CA"] = self.caracteristiques["CA"] + math.ceil(self.etage / 2)

        self.caracteristiques["CE"] = self.caracteristiques["CE"] \
                                      + math.ceil(self.caracteristiques["INT"])

        self.caracteristiques["SD"] = self.caracteristiques["SD"] \
                                      + math.ceil(self.caracteristiques["ADR"])

        self.setFaibResi("moyen")

        self.setExperience(1)

        self.setPO(1)

        self.setActions(random.choice([2, 3, 4]))

        for action in self.getActions():
            action.setEtage(self.etage)
            action.setEffet("1D6")
            action.setDuree()
            action.setPortee()
            action.setDifficulte()


class CreatureForte(Creature):
    def __init__(self, etage, pointFort=None):
        super().__init__(etage, pointFort)

        self.setCarac(6, 6)

        if self.pointFort != "AUCUN":
            self.changeCaracMax()

        self.setPV(etage, 3)

        self.caracteristiques["CA"] = self.caracteristiques["CA"] + math.ceil(self.etage / 2)

        self.caracteristiques["CE"] = self.caracteristiques["CE"] \
                                      + math.ceil(self.caracteristiques["INT"])

        self.caracteristiques["SD"] = self.caracteristiques["SD"] \
                                      + math.ceil(self.caracteristiques["ADR"])

        self.setFaibResi("fort")

        self.setExperience(1)

        self.setPO(1)

        self.setActions(random.choice([3, 4, 5]))

        for action in self.getActions():
            action.setEtage(self.etage)
            action.setEffet("1D6")
            action.setDuree()
            action.setPortee()
            action.setDifficulte()
