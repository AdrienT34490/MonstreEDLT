class Forme:
    def __init__(self, color):
        self.color = color

    def aire(self):
        aire = 3.14
        pass


class Cercle(Forme):
    def __init__(self, color, rayon):
        super().__init__(color)
        self.rayon = rayon

    def aire(self):
        aire = super().aire()
        return aire * self.rayon ** 2


formeRandom = Forme("bleu")
cercleBleu = Cercle("bleu", 1)

print(formeRandom.aire())
print(cercleBleu.aire())