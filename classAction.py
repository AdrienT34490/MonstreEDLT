import random

from globalFunctions import *


class Action:
    def __init__(self, typeAction, etage, typeCreature):
        self.typeAction = typeAction

        self.facteurComplexite = [0, 1]

        self.typeCreature = typeCreature
        if typeCreature == "faible":
            self.facteurComplexite = [0, 1]
        elif typeCreature == "moyen":
            self.facteurComplexite = [1, 2]
        elif typeCreature == "fort":
            self.facteurComplexite = [2, 3]

        self.complexite = random.choice(range(etage*self.facteurComplexite[0], etage*self.facteurComplexite[1]))
        print(self.complexite)

        self.effet = 0
        self.portee = 0
        self.duree = 0
        self.bonus = 0
        self.autre = 0

        def augmentation(stat):
            qteAutre = 0
            if stat == "effet":
                self.effet = self.effet + 2
                self.complexite = self.complexite - 1
            elif stat == "portee":
                self.portee = self.portee + random.choice([1, 2, 3])
                self.complexite = self.complexite - 1
            elif stat == "duree":
                self.duree = self.duree + 1
                self.complexite = self.complexite - 1
            elif stat == "Bonus":
                self.bonus = self.bonus + 1
                self.complexite = self.complexite - 2
            elif stat == "autre" and qteAutre < 3:
                qteAutre = qteAutre + 1
                valeur = random.choice([1, 2])
                self.autre = self.autre + valeur
                self.complexite = self.complexite - valeur

        etape = 0
        while self.complexite > 0:
            selection = random.random()
            etape = etape + 1
            if self.typeAction == "attaque":
                if etape == 1:
                    self.effet = self.effet + 2

                if selection < 0.25:
                    augmentation("portee")
                else:
                    augmentation("effet")

            elif self.typeAction == "agressive":
                if etape == 1:
                    self.effet = self.effet + 2

                if selection < 0.1:
                    augmentation("autre")
                elif selection < 0.2:
                    augmentation("duree")
                elif selection < 0.4:
                    augmentation("portee")
                else:
                    augmentation("effet")

            elif self.typeAction == "defensive":
                if selection < 0.1:
                    augmentation("autre")
                elif selection < 0.25:
                    augmentation("bonus")
                elif selection < 0.5:
                    augmentation("duree")
                elif selection < 0.7:
                    augmentation("portee")
                else:
                    augmentation("effet")

            elif self.typeAction == "utile":
                if selection < 0.1:
                    augmentation("autre")
                elif selection < 0.2:
                    augmentation("bonus")
                elif selection < 0.4:
                    augmentation("duree")
                else:
                    augmentation("portee")

        print(self.complexite)

    def toString(self):
        return (f"Action " + self.typeAction + " : \n"
                                                f" - Effet : {flatToDice(self.effet)} \n"
                                                f" - Portée : {self.portee} mètres \n"
                                                f" - Durée : {self.duree} tours \n"
                                                f" - Bonus : +{self.bonus} \n"
                                                f" - Autre carac : +{self.autre} points à répartir \n")