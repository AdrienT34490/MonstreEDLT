from globalFunctions import *

typeAction = ["utile", "defensive", "agressive"]


class Action:
    def __init__(self):
        typeEffet = rd.choice(typeAction)
        self.typeEffet = typeEffet
        self.effet = ""
        self.etage = 0
        self.duree = 0
        self.portee = 0
        self.difficulte = 0

    def setEtage(self, etage):
        self.etage = etage

    def setEffet(self, effetBase):
        bonusAConvertir = self.etage + rd.choice(range(0, 4))
        if bonusAConvertir < 0:
            bonusAConvertir = 0
        self.effet = effetBase + f" + {flatToDice(bonusAConvertir)}"
        self.effet = ajoutDe(self.effet)

    def setDuree(self):
        # durée aléatoire entre 0 et étage/3 arrondi à l'inférieur
        dureeMax = int(self.etage / 3)
        self.duree = rd.choice(range(0, dureeMax + 2))

    def setPortee(self):
        # portée aléatoire entre 0 et (étage/3 + 1)*4 arrondit à l'inférieur
        porteeMax = (int(self.etage / 3) + 1) * rd.choice(range(0, 4))
        self.portee = rd.choice(range(0, porteeMax + 1))

    def setDifficulte(self):
        # difficulté calculée à peu près de la même manière que les sorts
        complexite = diceToFlat(self.effet) + self.portee + self.duree + self.etage
        self.difficulte = 10 + int(complexite / 2)

    def toString(self):
        return (f"Action {self.typeEffet}\n"
                f"  - effet : {self.effet}\n"
                f"  - durée : {self.duree}\n"
                f"  - portée : {self.portee}\n"
                f"  - difficulté : {self.difficulte}\n")
