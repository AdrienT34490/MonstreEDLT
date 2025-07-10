import numpy as np
import matplotlib.pyplot as plt

from fonctions import generer_monstre  # Import de la fonction

# Définition de la taille de la grille
etages = np.arange(1, 10)  # de 1 à 9
bases = np.arange(0, 9)   # de 1 à 9

# Création de la grille 2D
X, Y = np.meshgrid(etages, bases)
XP = np.zeros_like(X, dtype=float)  # Initialisation de XP avec des zéros

# Remplissage des valeurs de XP en fonction de la fonction `generer_monstre`
for i, etage in enumerate(etages):
    for j, base in enumerate(bases):
        monstre = generer_monstre(etage, base)
        XP[j, i] = float(monstre["PV"].strip().split("|")[0])  # j, i correspond à Y, X

# Création de la figure et du graphique 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Tracer la surface
ax.plot_surface(X, Y, XP, cmap="viridis")

# Ajout des étiquettes d'axes
ax.set_xlabel('Étages')
ax.set_ylabel('Bases')
ax.set_zlabel('XP')

# Affichage du graphique
plt.show()
